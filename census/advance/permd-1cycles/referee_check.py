"""Referee (round 1) independent check for census/advance/permd-1cycles/theorem.md (CLS-046).

Written independently of check.py; no code is shared with it. Exit 0 iff all parts pass.
 (A) The map is rebuilt from the mod-8 table of census/systems.py perm_d_s3, as (a*n+b)/c.
     Every cycle met by orbits from n <= 20000 within 300 steps is listed. For each one the
     check confirms that #local minima (strict, cyclic) = #maximal even runs.
 (B) The LMN cutoff, recomputed with decimal at 80 digits (ln is correctly rounded):
     * b' <= bk*k + b0, from l < (k log(5/2) + 1)/log(8/5);
     * for 24925 <= k <= 10^8, log(b') + 0.14 < 21, so the LMN exponent equals 24.34*log5*441.
       There (k-1) log 2 > that constant.
     * for k >= 10^8, (k-1)log2 > 24.34 log5 (log(bk k+b0)+0.14)^2 holds at k = 10^8. The
       ratio RHS/k is decreasing there, because d/dk[(log(ak+b)+c)^2/k] has the sign of
       2ak/(ak+b) - (log(ak+b)+c) < 2 - 20 < 0. Meanwhile (k-1)log2/k increases.
 (C) Exact scan for 1 <= k <= 31000. This is beyond the claimed 24924, so that replacing 24.34
     by 30 is also covered. For each k, the full set of l >= 1 with 1/3 < 5^(k+l)/2^(3l+k) < 3
     is found by exact integer comparisons, walking from a float guess to both sign changes.
     The ratio is strictly decreasing in l (factor 5/8), so the walk finds the whole set, and
     every l with |Lambda| < 1 lies in it. The exact test |Delta| <= 8^l - 5^l is applied there.
 (D) For each survivor (k,l), the equation e*Delta = S is solved over all 4^l sign vectors s.
     Each solution is accepted only if a simulation reproduces the parity word and the s-vector.
"""
import sys, itertools, time
from decimal import Decimal as Dec, getcontext
getcontext().prec = 80
t0 = time.time()
ok = True
def bad(m):
    global ok; ok = False; print("FAIL", m)

TAB = [(5, 0, 2), (5, 3, 8), (5, 0, 2), (5, 1, 8), (5, 0, 2), (5, -1, 8), (5, 0, 2), (5, -3, 8)]
def D(n):
    a, b, c = TAB[n % 8]
    v = a * n + b
    assert v % c == 0 and v > 0
    return v // c
try:
    sys.path.insert(0, "/home/riv/Code/collatz/census")
    from systems import get
    Dc = get("perm_d_s3")["step"]
    if any(Dc(n) != D(n) for n in range(1, 50001)): bad("map mismatch with systems.py")
    else: print("(A0) D matches systems.py perm_d_s3 on 1..50000")
except Exception as ex:
    print("(A0) systems.py not importable: %r" % (ex,))

# (A)
cycles = set()
for n in range(1, 20001):
    x, path = n, set()
    for i in range(300):
        if x in path:
            cyc, y = [], x
            while True:
                cyc.append(y); y = D(y)
                if y == x: break
            j = cyc.index(min(cyc)); cycles.add(tuple(cyc[j:] + cyc[:j])); break
        path.add(x); x = D(x)
for c in sorted(cycles, key=lambda c: (len(c), c[0])):
    L = len(c)
    mins = sum(1 for i in range(L) if c[i - 1] > c[i] and c[(i + 1) % L] > c[i])
    runs = sum(1 for i in range(L) if c[i] % 2 == 0 and c[i - 1] % 2 == 1)
    if mins != runs: bad("minima != even runs on %s" % (c,))
    print("(A) cycle len %d min %d: local minima %d, even runs %d %s" % (L, c[0], mins, runs, c if L <= 12 else ""))

# (B)
L2, L5 = Dec(2).ln(), Dec(5).ln()
L25, L16 = L5 - L2, 3 * L2 - L5
r, cB = L25 / L16, 1 / L16
bk = (3 * r + 1) / L5 + 1 + r
b0 = 3 * cB / L5 + cB
C = Dec("24.34") * L5
print("(B) b' <= %s k + %s" % (format(bk, '.10g'), format(b0, '.10g')))
K2 = 10 ** 8
t = (bk * K2 + b0).ln() + Dec("0.14")
if not t < 21: bad("log b'+0.14 >= 21 at 1e8")
if not (24925 - 1) * L2 > C * 441: bad("region I")
if not (24924 - 1) * L2 <= C * 441: print("    note: cutoff not tight")
lhs2 = (K2 - 1) * L2; rhs2 = C * t * t
if not lhs2 > rhs2: bad("region II start")
print("    region I: (24924)log2 - 24.34*441*log5 = %s > 0 ; log b'+0.14 at 1e8 = %s < 21" % (
    format((24925 - 1) * L2 - C * 441, '.6g'), format(t, '.6g')))
print("    region II: at 1e8 lhs-rhs = %s > 0 ; monotone beyond => every cycle has k <= 24924" % format(lhs2 - rhs2, '.6g'))

# (C)
KMAX = 31000
rf = float(r)
surv = []
for k in range(1, KMAX + 1):
    cache = {}
    l0 = max(1, int(round(rf * k)))
    base = 5 ** (k + l0)
    def p5(l):
        if l not in cache:
            cache[l] = base * 5 ** (l - l0) if l >= l0 else base // 5 ** (l0 - l)
        return cache[l]
    def cls(l):
        a, b = p5(l), 1 << (3 * l + k)
        if 3 * a <= b: return -1
        if a >= 3 * b: return 1
        return 0
    l = l0
    while cls(l) == 1: l += 1
    while l > 1 and cls(l) == -1 and cls(l - 1) != 1: l -= 1
    a = l
    while a > 1 and cls(a - 1) == 0: a -= 1
    b = l
    while cls(b + 1) == 0: b += 1
    if a > 1 and cls(a - 1) != 1: bad("lower boundary k=%d" % k)
    if cls(b + 1) != -1: bad("upper boundary k=%d" % k)
    for l in range(a, b + 1):
        if cls(l) != 0: continue
        Dl = (1 << (3 * l + k)) - p5(l)
        if abs(Dl) <= 8 ** l - 5 ** l: surv.append((k, l, Dl))
print("(C) exact scan 1<=k<=%d: survivors %s" % (KMAX, [(k, l, d) for k, l, d in surv]))
if [(k, l) for k, l, _ in surv] != [(1, 2), (2, 4), (3, 6)]: bad("survivors")

# (D)
sols = set()
for k, l, Dl in surv:
    for s in itertools.product((3, 1, -1, -3), repeat=l):
        S = sum(s[j] * 5 ** (l - 1 - j) * 8 ** j for j in range(l))
        if S % Dl or S // Dl <= 0 or (S // Dl) % 2 == 0: continue
        e = S // Dl; x0 = 2 ** k * e; orb = [x0]
        for i in range(k + l): orb.append(D(orb[-1]))
        if orb[-1] == x0 and all((orb[i] % 2 == 0) == (i < k) for i in range(k + l)) \
                and all(4 - orb[k + j] % 8 == s[j] for j in range(l)):
            sols.add((k, l, e, tuple(orb[:-1])))
for s in sorted(sols): print("(D) solution k=%d l=%d e=%d cycle %s" % s)
if sorted(sorted(s[3]) for s in sols) != [[2, 3, 5], [6, 9, 15], [26, 41, 65]]: bad("solutions")
print("time %.1fs ; %s" % (time.time() - t0, "ALL PASS" if ok else "FAILURES"))
sys.exit(0 if ok else 1)
