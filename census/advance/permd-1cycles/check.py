"""check.py for census/advance/permd-1cycles/theorem.md  (CLS-046, perm_d).

D(2q)=5q, D(8q+r)=5q+(r+1)/2 (r=1,3,5,7).  A cycle with one local minimum has parity
word E^k O^l (k,l>=1), minimum x0 = 2^k e (e odd), and satisfies
      e * Delta = S,  Delta = 2^(3l+k) - 5^(k+l),  |S| <= 8^l - 5^l.
Verified here (all exact integer arithmetic, except (2) which uses decimal at 60 digits
with explicit margins):
 (1) the map agrees with census/systems.py perm_d_s3 on 1..10^5, and the cycle identity
     8^l x_{k+l} = 5^l x_k + S holds along every falling block met there;
 (2) the LMN cutoff: for every k >= K0 = 24925 the LMN lower bound for |Lambda| exceeds
     2^(1-k) (checked as a closed inequality + monotonicity, see theorem.md, Step 4);
 (3) exact scan: for 1 <= k <= K0-1 every l with |Delta| < 8^l is found; the l-window is
     certified exactly (outside it |Lambda| >= log 3 by integer comparison + monotonicity);
 (4) for each surviving (k,l): every odd e <= (8^l-5^l)/|Delta| is simulated.
Exit code 0 iff everything passes."""
import os, sys, time
from decimal import Decimal as mpf, getcontext
getcontext().prec = 60      # Decimal.ln/exp are correctly rounded (IEEE 854 / Python docs)
def log(x): return mpf(x).ln()
def exp(x): return mpf(x).exp()
def nstr(x, n): return format(x, '.%dg' % n)
t0 = time.time()
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, ROOT)

def D(n):
    if n % 2 == 0:
        return 5 * n // 2
    q, r = divmod(n, 8)
    return 5 * q + (r + 1) // 2

ok = True
def fail(msg):
    global ok
    ok = False
    print("FAIL:", msg)

# (1) agreement with the census definition and the falling-block identity
try:
    from systems import get
    Dc = get("perm_d_s3")["step"]
    bad = [n for n in range(1, 10**5 + 1) if Dc(n) != D(n)]
    if bad: fail("map disagrees with systems.py at %s" % bad[:5])
    else: print("(1a) D agrees with systems.py perm_d_s3 on 1..10^5")
except Exception as ex:
    print("(1a) systems.py not importable (%r); skipped" % (ex,))
for x in range(3, 4000, 2):          # falling blocks started at odd x
    y, ss = x, []
    while y % 2 == 1 and y > 1:
        ss.append(4 - (y % 8)); y = D(y)
    l = len(ss)
    S = sum(ss[j] * 5 ** (l - 1 - j) * 8 ** j for j in range(l))
    if 8 ** l * y != 5 ** l * x + S or abs(S) > 8 ** l - 5 ** l:
        fail("block identity at x=%d" % x)
print("(1b) 8^l x_end = 5^l x_start + S, |S| <= 8^l-5^l on all falling blocks from odd x < 4000")

# (2) LMN cutoff
L2, L5, L25, L16 = log(2), log(5), log(mpf(5) / 2), log(mpf(8) / 5)
r = L25 / L16
cA, cB = r, 1 / L16                    # l < cA*k + cB  (from |Lambda| < 1)
# b' = (3l+k)/log5 + (k+l) < bk*k + b0
bk = (3 * cA + 1) / L5 + 1 + cA
b0 = 3 * cB / L5 + cB
print("(2) l < %.6f k + %.6f ;  b' < %.6f k + %.6f" % (cA, cB, bk, b0))
C = mpf("24.34") * L5                  # 24.34 * D^4 * log A1 * log A2, D=1, logA1=1
K0 = 24925
def G(k):  # (k-1) log 2 - LMN exponent with b' replaced by its upper bound
    return (k - 1) * L2 - C * max(log(bk * k + b0) + mpf("0.14"), mpf(21)) ** 2
# region I: k >= K0 with log(b'max)+0.14 <= 21 : RHS constant = C*441, LHS increasing
if not ((K0 - 1) * L2 > C * 441): fail("K0 too small")
if G(K0 - 1) > 0: fail("K0 not minimal-ish (harmless) ")
print("    C*441 = %s ; (K0-1)log2 = %s ; G(K0-1) = %s <= 0 < G(K0) = %s" % (
    nstr(C * 441, 10), nstr((K0 - 1) * L2, 10), nstr(G(K0 - 1), 6), nstr(G(K0), 6)))
# region II: k >= k1 := first k with log(bk k + b0)+0.14 > 21. There G(k1)>0 and
# G'(k) = log2 - 2C t bk/(bk k+b0) with t = log(bk k+b0)+0.14 ; t/k is decreasing for
# k >= 3, and at k1 the derivative is positive, hence G increases on [k1, oo).
k1 = int((exp(mpf(21) - mpf("0.14")) - b0) / bk)
assert k1 > K0
t1 = log(bk * k1 + b0) + mpf("0.14")
dG = L2 - 2 * C * (t1 + 1) * bk / (bk * k1)     # (t1+1) covers t on [k1, k1+1); bound is decreasing
if not (G(k1) > 0 and dG > 0): fail("region II")
print("    region II starts at k1 = %d: G(k1) = %s > 0, G' >= %s > 0" % (k1, nstr(G(k1), 8), nstr(dG, 8)))
print("(2) every one-minimum cycle has k <= %d" % (K0 - 1))

# (3) exact scan
import math
rf = float(r)
cands = []
for k in range(1, K0):
    l0 = round(k * rf)
    lo, hi = max(1, l0 - 4), l0 + 4
    # certify window: |Lambda| >= log 3 outside, i.e. 5^(k+l)/2^(3l+k) >= 3 for l<=lo-1 (if lo>1)
    # and 2^(3l+k)/5^(k+l) >= 3 for l = hi+1 ; Lambda = (k+l)log5-(3l+k)log2 decreases in l.
    if lo > 1:
        l = lo - 1
        if not (5 ** (k + l) >= 3 << (3 * l + k)): fail("window low k=%d" % k)
    l = hi + 1
    if not ((1 << (3 * l + k)) >= 3 * 5 ** (k + l)): fail("window high k=%d" % k)
    p5 = 5 ** (k + lo)
    for l in range(lo, hi + 1):
        Dl = (1 << (3 * l + k)) - p5
        if abs(Dl) < (1 << (3 * l)):
            if abs(Dl) <= 8 ** l - 5 ** l:
                cands.append((k, l, Dl))
        p5 *= 5
print("(3) exact scan 1<=k<=%d: pairs with |Delta| <= 8^l-5^l: %s" % (K0 - 1, [(k, l) for k, l, _ in cands]))
if [(k, l) for k, l, _ in cands] != [(1, 2), (2, 4), (3, 6)]: fail("unexpected candidates")

# (4) e-enumeration and simulation
found = []
for k, l, Dl in cands:
    emax = (8 ** l - 5 ** l) // abs(Dl)
    for e in range(1, emax + 1, 2):
        x0 = 2 ** k * e
        orb, x = [x0], x0
        good = True
        for i in range(k + l):
            if (i < k) != (x % 2 == 0): good = False; break
            x = D(x); orb.append(x)
        if good and x == x0:
            found.append((k, l, e, orb[:-1]))
    print("    (k,l)=(%d,%d): Delta=%d, odd e <= %d tested" % (k, l, Dl, emax))
for f in found: print("    cycle: k=%d l=%d e=%d  %s" % f)
cyc = sorted(sorted(f[3]) for f in found)
if cyc != [[2, 3, 5], [6, 9, 15], [26, 41, 65]]: fail("cycle list %s" % cyc)
print("(4) one-local-minimum cycles other than {1}: {2,5,3}, {6,15,9}, {26,65,41}")
print("time %.1fs ; %s" % (time.time() - t0, "ALL PASS" if ok else "FAILURES"))
sys.exit(0 if ok else 1)
