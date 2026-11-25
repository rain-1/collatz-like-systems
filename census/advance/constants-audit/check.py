"""constants-audit: re-derive every Baker/Pade cutoff in the census from a CONSULTED
bound, then rerun / extend the finite scans.  Exit 0 iff everything passes.

Transcendence input (consulted, see theorem.md):
  M. Laurent, Linear forms in two logarithms and interpolation determinants II,
  Acta Arith. 133 (2008) 325-348, Corollary 2 + Table 1:
    alpha1, alpha2 multiplicatively independent, alpha_i, log alpha_i real > 0,
    Lambda = b2 log alpha2 - b1 log alpha1, b1, b2 positive integers,
    D = [Q(a1,a2):Q]/[R(a1,a2):R],  log A_i >= max(h(a_i), |log a_i|/D, 1/D),
    b' = b1/(D log A2) + b2/(D log A1);  then for each (m, C2(m)) of Table 1
    log|Lambda| >= -C2 D^4 (max(log b' + 0.38, m/D, 1))^2 log A1 log A2.
Here alpha1 = 2 (log A1 = 1), alpha2 = p an odd prime (log A2 = log p), D = 1.

Logs are evaluated with decimal at 60 significant digits (correctly rounded ln);
every inequality is required with an explicit margin (>= 1 for function values,
>= 1e-4 for derivative bounds), which dwarfs the rounding error (< 1e-50).
All scans use exact Python integers.
"""
import os
import sys
import time
from decimal import Decimal as Dec, getcontext
from fractions import Fraction as Fr

getcontext().prec = 60
HERE = os.path.dirname(os.path.abspath(__file__))
MIXED = os.path.join(HERE, "..", "..", "lhf", "mixed")
sys.path.insert(0, os.path.abspath(MIXED))
import onerun_lib as OL  # read-only reuse of the refereed finite-part engine

TABLE1_C2 = {10: 25.2, 12: 23.4, 14: 22.1, 16: 21.1, 18: 20.3, 20: 19.7,
             22: 19.2, 24: 18.8, 26: 18.4, 28: 18.1, 30: 17.9}
LN2, LN3 = Dec(2).ln(), Dec(3).ln()
OK = True


def D(x):
    if isinstance(x, Fr):
        return Dec(x.numerator) / Dec(x.denominator)
    return Dec(str(x)) if isinstance(x, float) else Dec(x)


def report(name, ok):
    global OK
    OK &= bool(ok)
    print(("PASS " if ok else "FAIL ") + name)
    return ok


def laurent_term(C, m, logp, bp):
    """C2 * max(log b' + 0.38, m, 1)^2 * log A1 * log A2  with log A1 = 1."""
    u = max(D(bp).ln() + Dec("0.38"), Dec(m))
    return D(C) * u * u * logp


def cutoff(G, dG, start=2, stop=10 ** 6):
    """Smallest k0 >= start with G(k0) >= 1 and dG(k0) >= 1e-4, for the best (m, C2).
    dG(k) is a lower bound for G' on [k, oo) that is NONDECREASING in k (each use
    below is of the form a - (decreasing positive terms)), so G is increasing and
    > 0 on [k0, oo).  Returns (k0, m, C)."""
    best = None
    for m, C in TABLE1_C2.items():
        lo, hi = start, stop
        if not (G(hi, m, C) >= 1 and dG(hi, m, C) >= Dec("1e-4")):
            continue
        while lo < hi:  # binary search for the first k where both hold (both monotone past it)
            mid = (lo + hi) // 2
            if G(mid, m, C) >= 1 and dG(mid, m, C) >= Dec("1e-4"):
                hi = mid
            else:
                lo = mid + 1
        k0 = lo
        assert G(k0, m, C) >= 1 and dG(k0, m, C) >= Dec("1e-4")
        if best is None or k0 < best[0]:
            best = (k0, m, C)
    return best


# =========================================================== (c1) Steiner 1-cycles
def steiner():
    print("== Steiner 1-cycles of 3x+1 (round2/literature/steiner_1cycle.md)")
    # 0 < Lambda = (k+l)log2 - k log3 < 2^(1-k);  b1 = k+l <= 2k, b2 = k;
    # b' = (k+l)/log3 + k <= k(2/log3 + 1).
    a = 2 / LN3 + 1
    G = lambda k, m, C: (k - 1) * LN2 - laurent_term(C, m, LN3, a * k)
    dG = lambda k, m, C: LN2 - 2 * D(C) * LN3 * (max(D(a * k).ln() + Dec("0.38"), Dec(m))) / k
    k0, m, C = cutoff(G, dG)
    report(f"Laurent cutoff: no 1-cycle with k >= {k0} (m={m}, C2={C})", True)
    t = time.time()
    found = []
    for k in range(1, k0):
        p3 = 3 ** k
        K = p3.bit_length()           # least K with 2^K > 3^k (3^k is not a power of 2)
        l = K - k
        d = (1 << K) - p3
        if l >= 1 and d < (1 << l) and ((1 << l) - 1) % d == 0:
            found.append((k, l))
    report(f"exact scan k < {k0}: solutions {found} == [(1, 1)]  ({time.time()-t:.1f}s)",
           found == [(1, 1)])
    report("old scan bound KMAX=10000 >= new cutoff (old check already sufficient)", k0 <= 10000)
    return k0


# =========================================================== (c2) perm1932 1-cycles
def perm1932_step(x):
    q, r = divmod(x, 3)
    return 2 * q if r == 0 else (4 * q + 1 if r == 1 else 4 * q + 3)


def perm1932_is_1cycle(x0, k, l):
    """x0 minimum; k non-multiples of 3, then l multiples of 3, back to x0."""
    x = x0
    for _ in range(k):
        if x % 3 == 0:
            return False
        x = perm1932_step(x)
    for _ in range(l):
        if x % 3 != 0:
            return False
        x = perm1932_step(x)
    return x == x0


def perm1932():
    print("== perm1932 1-cycles (round2/literature/perm1932_1cycle.md)")
    # l >= 2: |Lambda| < 2^(1-l), Lambda = (2k+l)log2 - (k+l)log3, k <= 2l+3;
    # b' = (2k+l)/log3 + (k+l) <= (5l+6)/log3 + 3l + 3 <= a*l with a = 8/log3 + 6 for l >= 2... use exact affine:
    a1, a0 = 5 / LN3 + 3, 6 / LN3 + 3
    bp = lambda l: a1 * l + a0
    G = lambda l, m, C: (l - 1) * LN2 - laurent_term(C, m, LN3, bp(l))
    # d/dl max(log(a1 l + a0)+0.38, m)^2 <= 2 u * a1/(a1 l + a0) <= 2u/l
    dG = lambda l, m, C: LN2 - 2 * D(C) * LN3 * max(bp(l).ln() + Dec("0.38"), Dec(m)) / l
    l0, m, C = cutoff(G, dG)
    report(f"Laurent cutoff: no 1-cycle with l >= {l0} (m={m}, C2={C})", True)
    # Exact scan for 1 <= l < l0, all 1 <= k <= 2l+3, of |D| <= 4^k - 3^k
    # with D = 3^(k+l) - 2^(2k+l).  Dividing by 4^k 2^l, with R(k) = 3^(k+l)/2^(2k+l)
    # (strictly decreasing in k), |D| < 4^k <=> |R(k) - 1| < 2^-l, an interval of k.
    # For l <= 600 every k is tested directly (as in the original check); for larger l
    # we locate the interval exactly: ka = least k with 3^(k+l) 2^l < 2^(2k+l)(2^l+1).
    t = time.time()
    cands = []
    for l in range(1, l0):
        if l <= 600:
            ks = range(1, 2 * l + 4)
        else:
            # estimate then pin ka exactly by monotonicity
            est = int(float(l) * float((LN3 - LN2) / (2 * LN2 - LN3)))
            up = lambda k: 3 ** (k + l) * (1 << l) < (1 << (2 * k + l)) * ((1 << l) + 1)
            ka = max(1, est - 3)
            assert not up(ka) or ka == 1
            while not up(ka):
                ka += 1
            assert ka == 1 or not up(ka - 1)
            ks = []
            k = ka
            # R(k) > 1 - 2^-l  <=>  3^(k+l) 2^l > 2^(2k+l) (2^l - 1)
            while k <= 2 * l + 3 and 3 ** (k + l) * (1 << l) > (1 << (2 * k + l)) * ((1 << l) - 1):
                ks.append(k)
                k += 1
        for k in ks:
            Dv = 3 ** (k + l) - (1 << (2 * k + l))
            if Dv != 0 and abs(Dv) <= 4 ** k - 3 ** k:
                cands.append((k, l))
    report(f"exact scan l < {l0}: candidate pairs {cands} ({time.time()-t:.1f}s)",
           cands == [(1, 1), (2, 1), (3, 2), (4, 3), (7, 5)])
    cycles = []
    for k, l in cands:
        Dv = abs(3 ** (k + l) - (1 << (2 * k + l)))
        for e in range(1, (4 ** k - 3 ** k) // Dv + 1):
            if e % 3 and perm1932_is_1cycle((1 << l) * e, k, l):
                cycles.append((k, l, e))
    report(f"e-enumeration: 1-cycles (k,l,e) = {cycles} == [(1,1,1),(3,2,1)]",
           cycles == [(1, 1, 1), (3, 2, 1)])
    report(f"old scan bound LMAX=600 vs new cutoff {l0}: old check was "
           + ("sufficient" if l0 <= 600 else "INSUFFICIENT, extended here"), True)
    return l0


# =========================================================== (b) collatz3 Theorem 1C
def T(d):
    return lambda n: n // 2 if n % 2 == 0 else (3 * n + d) // 2


def verify_one_cycle(d, k, l, x):
    t, y = T(d), x
    for _ in range(k):
        if y % 2 != 1:
            return False
        y = t(y)
    for _ in range(l):
        if y % 2 != 0:
            return False
        y = t(y)
    return y == x


def one_cycles_fast(d, kmax):
    """All (k, l, x) with k <= kmax, l >= 0, x = d(3^k-2^k)/(2^(k+l)-3^k) a positive
    integer.  Uses only the proved necessary condition 0 < |D| <= |d|(2^l - 1) (l >= 1),
    i.e. 3^k/2^l in (2^k - |d|, 2^k + |d|), whose l-set is an interval found exactly."""
    ad = abs(d)
    out = [(1, 0, -d)] if d < 0 else []
    for k in range(1, kmax + 1):
        a, b = 3 ** k, 1 << k
        num = d * (a - b)
        # least l >= 1 with 3^k < 2^l (2^k + |d|)
        l = max(1, a.bit_length() - k - ad.bit_length() - 2)
        while (l > 1) and a < (1 << (l - 1)) * (b + ad):
            l -= 1
        while not a < (1 << l) * (b + ad):
            l += 1
        # all l with 3^k > 2^l (2^k - |d|)  (or every l if 2^k <= |d|, bounded below)
        lcap = 4 * k + 8 + 2 * ad.bit_length()
        while l <= lcap and (b <= ad or a > (1 << l) * (b - ad)):
            Dv = (1 << (k + l)) - a
            if Dv != 0 and num % Dv == 0 and num // Dv > 0:
                out.append((k, l, num // Dv))
            l += 1
    return out


EXPECTED_1C = {1: [(1, 1, 1)], -1: [(1, 0, 1), (2, 1, 5)], 3: [(1, 1, 3)],
               5: [(1, 1, 5), (1, 2, 1), (3, 2, 19)], 7: [(1, 1, 7), (2, 2, 5)],
               9: [(1, 1, 9)], 13: [(1, 1, 13), (1, 3, 1), (5, 3, 211)], 17: [(1, 1, 17)]}


def collatz3():
    print("== collatz3 Theorem 1C (lhf/collatz3/*.md, d in {1,-1,3,5,7,9,13,17})")
    # |Lambda| = |K log2 - k log3|.  Either |Lambda| >= 1 (then 2^k < 2|d| <= 34, k <= 5)
    # or |Lambda| < 2|d| 2^-k <= 34 * 2^-k.  K <= k log2(3) + log2(18), so
    # b' = K/log3 + k <= k(1/log2 + 1) + log2(18)/log3.
    a1, a0 = 1 / LN2 + 1, (Dec(18).ln() / LN2) / LN3
    bp = lambda k: a1 * k + a0
    G = lambda k, m, C: k * LN2 - Dec(34).ln() - laurent_term(C, m, LN3, bp(k))
    dG = lambda k, m, C: LN2 - 2 * D(C) * LN3 * max(bp(k).ln() + Dec("0.38"), Dec(m)) / k
    k0, m, C = cutoff(G, dG)
    report(f"Laurent cutoff: no 1-cycle with k >= {k0} for any |d| <= 17 (m={m}, C2={C})", True)
    t = time.time()
    allok = True
    for d, exp in EXPECTED_1C.items():
        cyc = one_cycles_fast(d, k0)
        good = cyc == exp and all(verify_one_cycle(d, *c) for c in cyc)
        allok &= good
        print(f"   d={d:3d}: {cyc}" + ("" if good else f"  EXPECTED {exp}"))
    report(f"exact scan k <= {k0} for every d: lists equal the census lists, all simulated "
           f"({time.time()-t:.1f}s)", allok)
    report(f"old scan bound k <= 1000 vs new cutoff {k0}: old check was "
           + ("sufficient" if k0 <= 1000 else "INSUFFICIENT, extended here"), True)
    return k0


# =========================================================== (a) one-run theorems
def S048(n):
    if n % 4 == 1:
        return (5 * n + 1) // 2
    m = n + 1
    return m >> OL.v(m, 2)


def S051(n):
    m = 4 * n + 5 if n % 3 == 1 else 2 * n + 2
    return m // 3 ** OL.v(m, 3)


SET052 = {1, 3, 5, 7, 9, 11, 13, 15, 17, 21, 23, 25, 29}


def S052(n):
    m = 3 * n + 1 if n % 32 in SET052 else n + 1
    return m >> OL.v(m, 2)


def S053(n):
    m = 7 * n + 1 if n % 4 == 1 else n + 1
    return m >> OL.v(m, 2)


# name, S, domain, Q, P, low, (alpha, beta) with log low(k) >= alpha k + beta for k >= 3,
# c1, c0, ylo, c_hi, c_hi0, old k0, expected   -- all copied from check_CLS-0xx.py
ONERUN = [
    ("CLS-048 split5_1", S048, lambda n: n % 2 == 1, 5, 2, lambda k: (2 ** (k + 1) - 1) // 3,
     (LN2, LN2 - Dec(6).ln()),       # floor((2^(k+1)-1)/3) >= 2^(k+1)/6
     Fr(153, 100), Fr(42, 100), 1, 1, 0, 25000, [(1, 1)]),
    ("CLS-051 m3_4n5", S051, lambda n: n % 3 != 0, 2, 3, lambda k: max(4, 3 ** k - 5),
     (LN3, -LN2),                    # 3^k - 5 >= 3^k / 2 for k >= 2
     Fr(32225, 10000), Fr(5561, 1000), 2, Fr(51558, 10000), Fr(8897, 1000), 10800, [(16, 1)]),
    ("CLS-052 s32_plus9", S052, lambda n: n % 2 == 1, 3, 2, lambda k: 2 ** (k + 1) - 1,
     (LN2, Dec(0)),                  # 2^(k+1) - 1 >= 2^k
     Fr(2558, 1000), Fr(1578, 1000), 1, Fr(32240, 10000), Fr(15779, 10000), 17100, []),
    ("CLS-053 split7_1", S053, lambda n: n % 2 == 1, 7, 2, lambda k: (2 ** (2 * k + 1) - 1) // 3,
     (2 * LN2, -LN3),                # floor((2^(2k+1)-1)/3) >= 2^(2k)/3
     Fr(5455, 1000), Fr(613, 1000), 1, Fr(63116, 10000), Fr(6126, 10000), 15100, []),
]


def onerun():
    print("== one-run theorems (lhf/mixed/CLS-048/051/052/053.md)")
    res = {}
    for (name, S, dom, Q, P, low, (al, be), c1, c0, ylo, c_hi, c_hi0, k0old, expected) in ONERUN:
        p = Q if P == 2 else P
        logp = D(p).ln()
        # exponents: Y (of Q) <= c_hi k + c_hi0;  X (of P) <= Y log Q / log P + 1.
        # b' = e2/log p + e_p.
        if P == 2:   # e2 = X <= Y logp/log2 + 1, e_p = Y
            a1 = (1 / LN2 + 1) * D(c_hi)
            a0 = (1 / LN2 + 1) * D(c_hi0) + 1 / logp
        else:        # Q = 2: e2 = Y, e_p = X <= Y log2/logp + 1
            a1 = (1 + LN2) / logp * D(c_hi)
            a0 = (1 + LN2) / logp * D(c_hi0) + 1
        bp = lambda k: a1 * k + a0
        # sanity: low bound really holds on a sample
        for k in range(3, 400):
            assert D(low(k)).ln() >= al * k + be
        G = lambda k, m, C: (al * k + be - (D(c1) * k + D(c0)).ln()
                             - laurent_term(C, m, logp, bp(k)))
        # d/dk: al - c1/(c1k+c0) - 2C logp u a1/(a1 k + a0) >= al - 1/k - 2 C logp u / k
        dG = lambda k, m, C: (al - Dec(1) / k
                              - 2 * D(C) * logp * max(bp(k).ln() + Dec("0.38"), Dec(m)) / k)
        k0, m, C = cutoff(G, dG, start=50)
        report(f"[{name}] Laurent cutoff: one-run cycles have k < {k0} (m={m}, C2={C}); "
               f"old LMN k0 = {k0old}", True)
        Ymax = int((Fr(c_hi) * (k0 - 1) + Fr(c_hi0)))
        t = time.time()
        surv = OL.finite_part(Q, P, low, c1, c0, ylo, c_hi, c_hi0, Ymax)
        N = max((s[4] for s in surv), default=0)
        found = [(n, OL.one_run_cycle_length(S, n)) for n in range(1, N + 1)
                 if dom(n) and OL.one_run_cycle_length(S, n)]
        report(f"[{name}] finite part Y <= {Ymax}: {len(surv)} survivors, n0 <= {N}; "
               f"one-run minima {found} == {expected} ({time.time()-t:.1f}s)", found == expected)
        res[name] = (k0, k0old)
    return res


if __name__ == "__main__":
    t0 = time.time()
    s = steiner()
    p = perm1932()
    c = collatz3()
    o = onerun()
    print(f"summary: steiner k0={s}, perm1932 l0={p}, collatz3 k0={c}, onerun {o}")
    print(f"total {time.time()-t0:.1f}s")
    print("ALL PASS" if OK else "SOME FAIL")
    sys.exit(0 if OK else 1)
