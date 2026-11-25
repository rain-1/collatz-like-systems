#!/usr/bin/env python3
"""Exact checks for census/advance/split7_1-runs/theorem.md  (CLS-053, desc_split7_1).

T: even n -> n/2; n = 1 mod 4 -> 7n+1; n = 3 mod 4 -> n+1.

Part 1  range certificate: every 1 <= n < 2^BITS reaches (1 8 4 2)   [C++ helper range.cpp]
        + independent pure-Python certificate at 2^26 and brute force below 2^20.
Part 2  every cycle other than (1 8 4 2) has more than R expanding runs  [exact intervals]
Part 3  density bound for never-dropping starts  [exact Fractions + brute-force sanity]

Exit status 0 iff every check passes.  Runtime: ~1 minute on 12 cores.
"""
import os
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction as Fr
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
BITS = 50          # range certificate 1 <= n < 2^BITS
R_CLAIM = 69       # cycles other than (1 8 4 2) have more than R_CLAIM runs

FAIL = []


def ok(cond, msg):
    print(("  PASS " if cond else "  FAIL ") + msg)
    if not cond:
        FAIL.append(msg)


def T(n):
    if n % 2 == 0:
        return n // 2
    return 7 * n + 1 if n % 4 == 1 else n + 1


# ---------------------------------------------------------------------------
# Part 1: range certificate
# ---------------------------------------------------------------------------
def py_tree(bits):
    """Pure-Python port of range.cpp (sequential); returns number of covered starts."""
    bound = 1 << bits
    covered = 0
    stack = [(0, 0, 1, 0)]
    while stack:
        depth, r, a, b = stack.pop()
        M = 1 << depth
        if a < M or (a == M and b < r) or depth == bits:
            stop = bound >> depth
            first = 1 if r == 0 else 0
            covered += stop - first
            if a <= M and b < r:
                continue
            if a < M:
                stop = min(stop, (b - r) // (M - a) + 1 if b >= r else 0)
            for t in range(first, stop):
                n = M * t + r
                x = a * t + b
                assert x == iterate_check(n, a, b, t)
                s = 0
                while x >= n and x != 1:
                    x = T(x)
                    s += 1
                    if s > 10 ** 6:
                        raise RuntimeError(n)
            continue
        for d in (0, 1):
            cr = r + d * M
            y = b + d * a
            if y % 2 == 0:
                stack.append((depth + 1, cr, a, y // 2))
            elif a % 2:
                stack.append((depth + 1, cr, 2 * a, y))
            elif y % 4 == 1:
                stack.append((depth + 1, cr, 7 * (a // 2), (7 * y + 1) // 4))
            else:
                stack.append((depth + 1, cr, a // 2, (y + 1) // 4))
    return covered


_seen = [0]


def iterate_check(n, a, b, t):
    # spot check (every 97th call) that a*t+b really is an iterate T^k(n)
    _seen[0] += 1
    x = a * t + b
    if _seen[0] % 97:
        return x
    y = n
    for _ in range(2000):
        if y == x:
            return x
        y = T(y)
    raise AssertionError(("not an iterate", n, x))


def part1():
    print("Part 1: every 1 <= n < 2^%d reaches (1 8 4 2)" % BITS)
    # cycle
    ok([1, T(1), T(T(1)), T(T(T(1))), T(T(T(T(1))))] == [1, 8, 4, 2, 1], "(1 8 4 2) is a 4-cycle of T")
    # brute force below 2^20 (independent of the tree)
    lim = 1 << 20
    good = bytearray(lim)
    good[1] = 1
    allok = True
    for n in range(2, lim):
        x = n
        steps = 0
        while x >= n:
            x = T(x)
            steps += 1
            if steps > 10 ** 5:
                allok = False
                break
        good[n] = 1 if (allok and good[x]) else 0
        if not good[n]:
            allok = False
            break
    ok(allok, "brute force: every n < 2^20 drops below itself, hence reaches 1")
    # pure python tree
    cov = py_tree(26)
    ok(cov == (1 << 26) - 1, "pure-Python residue tree certifies all %d starts below 2^26" % cov)
    # C++ tree
    cxx = shutil.which("g++") or shutil.which("clang++")
    if not cxx:
        ok(False, "no C++ compiler found for range.cpp")
        return
    with tempfile.TemporaryDirectory() as td:
        exe = os.path.join(td, "range")
        subprocess.run([cxx, "-O3", "-std=c++17", "-pthread", os.path.join(HERE, "range.cpp"), "-o", exe],
                       check=True)
        for bits in (26, BITS):
            res = subprocess.run([exe, str(bits), "16"], capture_output=True, text=True)
            print("   ", res.stdout.strip(), res.stderr.strip())
            want = "covered=%d " % ((1 << bits) - 1)
            ok(res.returncode == 0 and want in res.stdout and res.stdout.strip().endswith("OK"),
               "C++ residue tree certifies every 1 <= n < 2^%d" % bits)


# ---------------------------------------------------------------------------
# Rigorous interval arithmetic for logs (directed dyadic rounding)
# ---------------------------------------------------------------------------
P = 1 << 420


def dn(q):
    return Fr((q.numerator * P) // q.denominator, P)


def up(q):
    return Fr(-((-q.numerator * P) // q.denominator), P)


def log_iv(x):
    """Interval [lo, hi] containing log(x), x a positive Fraction (or int)."""
    x = Fr(x)
    assert x > 0
    k = x.numerator.bit_length() - x.denominator.bit_length()
    f = x / Fr(2) ** k
    while f >= 2:
        f /= 2
        k += 1
    while f < 1:
        f *= 2
        k -= 1
    y = (f - 1) / (f + 1)          # 0 <= y < 1/3
    y2 = y * y
    N = 140
    lo = hi = Fr(0)
    plo = dn(y)
    phi = up(y)
    for j in range(N):
        lo += dn(plo / (2 * j + 1))
        hi += up(phi / (2 * j + 1))
        plo = dn(plo * y2)
        phi = up(phi * y2)
    # tail: sum_{j>=N} y^(2j+1)/(2j+1) <= y^(2N+1)/((2N+1)(1-y^2)), and phi >= y^(2N+1)
    hi += up(phi / ((2 * N + 1) * (1 - y2)))
    lo, hi = 2 * lo, 2 * hi
    if k:
        l2lo, l2hi = LOG2
        lo += k * l2lo if k > 0 else k * l2hi
        hi += k * l2hi if k > 0 else k * l2lo
    return lo, hi


def _log2_direct():
    # log 2 = 2 atanh(1/3)
    y = Fr(1, 3)
    y2 = y * y
    lo = hi = Fr(0)
    plo = phi = y
    N = 140
    for j in range(N):
        lo += dn(plo / (2 * j + 1))
        hi += up(phi / (2 * j + 1))
        plo = dn(plo * y2)
        phi = up(phi * y2)
    hi += up(phi / ((2 * N + 1) * (1 - y2)))
    return 2 * lo, 2 * hi


LOG2 = _log2_direct()
L7 = log_iv(7)
L4 = (2 * LOG2[0], 2 * LOG2[1])
ALPHA = (L7[0] / LOG2[1], L7[1] / LOG2[0])            # log_2 7
RHO = (L7[0] / L4[1], L7[1] / L4[0])                  # log_4 7
L74 = log_iv(Fr(7, 4))
L87 = log_iv(Fr(8, 7))


def fl(q):
    return float(q)


# ---------------------------------------------------------------------------
# Part 2: cycles with at most R expanding runs
# ---------------------------------------------------------------------------
def stern_brocot(K):
    """Neighbours a/b < alpha < c/d, bc - ad = 1, b + d > K (decided with the alpha interval)."""
    alo, ahi = ALPHA
    a, b, c, d = 2, 1, 3, 1
    assert Fr(a, b) < alo and Fr(c, d) > ahi
    while b + d <= K:
        med = Fr(a + c, b + d)
        if med < alo:
            # largest j >= 1 with (a+jc)/(b+jd) < alpha and b + jd + d <= K
            def good(j):
                return Fr(a + j * c, b + j * d) < alo and b + j * d + d <= K
            hi = 1
            while good(hi * 2):
                hi *= 2
            lo = hi
            hi2 = hi * 2
            while hi2 - lo > 1:
                mid = (lo + hi2) // 2
                if good(mid):
                    lo = mid
                else:
                    hi2 = mid
            a, b = a + lo * c, b + lo * d
        elif med > ahi:
            def good(j):
                return Fr(c + j * a, d + j * b) > ahi and d + j * b + b <= K
            hi = 1
            while good(hi * 2):
                hi *= 2
            lo = hi
            hi2 = hi * 2
            while hi2 - lo > 1:
                mid = (lo + hi2) // 2
                if good(mid):
                    lo = mid
                else:
                    hi2 = mid
            c, d = c + lo * a, d + lo * b
        else:
            raise AssertionError("alpha interval too wide")
        assert b * c - a * d == 1
    assert Fr(a, b) < alo and Fr(c, d) > ahi and b * c - a * d == 1 and b + d > K
    return a, b, c, d


def kmax_from_logbound(lbound, r):
    """Upper bound (integer) for K given log(3m+1) <= lbound:  K <= 5.2*K_exp + 1,
    K_exp <= (log(3m+1) - log 2) * rho^r / log(7/4)."""
    kexp = (lbound - LOG2[0]) * RHO[1] ** r / L74[0]
    K = Fr(52, 10) * kexp + 1
    return K.numerator // K.denominator + 1


def part2_for(r, verbose=False):
    """Return True if every cycle with exactly r expanding runs and min m >= 2^BITS is impossible."""
    C = Fr(134, 100)            # delta < C r / m
    H2 = Fr(195, 100)           # >= log 7
    # --- LMN/Laurent step: find mu1 with log m < mu1.
    # For mu = log m:  log(3m+1) <= mu + 11/10.
    # K <= kmax(mu + 1.1);  b' <= 2.442 K + 0.52 ;
    # log m < log(C r) + 25.2*H2*max(log b' + 0.38, 10)^2.
    def g_upper(mu):
        K = kmax_from_logbound(mu + Fr(11, 10), r)
        bp = Fr(2442, 1000) * K + Fr(52, 100)
        lb = log_iv(bp)[1] + Fr(38, 100)
        lbm = max(lb, Fr(10))
        return log_iv(C * r)[1] + Fr(252, 10) * H2 * lbm * lbm, lb, K
    mu1 = Fr(10 ** 6)
    for _ in range(60):
        gv, lb, K = g_upper(mu1)
        if gv >= mu1:
            break
        newmu = up(gv) + 1
        if newmu >= mu1:
            break
        mu1 = newmu
    gv, lb, K = g_upper(mu1)
    # monotonicity: for mu >= mu1 the bound g(mu) < mu persists if lb >= 10 (max is attained by
    # the log term) and 2*25.2*H2*lb/mu1 < 1 (derivative of g is below 1, see theorem.md)
    cond = gv < mu1 and lb >= 10 and 2 * Fr(252, 10) * H2 * lb / mu1 < 1
    if not cond:
        return False, "LMN step failed"
    # --- Farey reduction: m < M_i
    # from log m < mu1:  log(3m+1) <= mu1 + 1.1
    lbound = mu1 + Fr(11, 10)
    hist = [fl(mu1)]
    for it in range(40):
        K = kmax_from_logbound(lbound, r)
        a, b, c, d = stern_brocot(K)
        gap = c - d * ALPHA[1]           # lower bound for c - d*alpha > 0
        assert gap > 0
        Mb = C * r / (LOG2[0] * gap)     # m < Mb
        Mint = Mb.numerator // Mb.denominator + 1
        hist.append(Mint.bit_length())
        if Mint <= (1 << BITS):
            if verbose:
                print("    r=%d: log m < %.1f (Laurent), then m < 2^%s via Farey neighbours; "
                      "last pair denominators b=%d d=%d (K <= %d)"
                      % (r, hist[0], hist[1:], b, d, K))
            return True, hist
        newl = log_iv(3 * Mint + 1)[1]
        if newl >= lbound:
            return False, hist
        lbound = newl
    return False, hist


def part2():
    print("Part 2: every cycle other than (1 8 4 2) has more than %d expanding runs" % R_CLAIM)
    # constants
    ok(L7[1] < Fr(195, 100), "log 7 < 1.95 (so H2 = 1.95 is admissible)")
    ok(ALPHA[1] < Fr(281, 100), "log_2 7 < 2.81")
    ok(ALPHA[1] - ALPHA[0] < Fr(1, 10 ** 100), "alpha = log_2 7 known to within 1e-100")
    lam = L74[1] / L87[0]
    ok(lam < Fr(42, 10), "log(7/4)/log(8/7) < 4.2  (so K <= 5.2 K_exp + 1)")
    # gap-telescoping inequality constants at m >= 2^BITS:
    m0 = Fr(1 << BITS)
    cgap = (7 * m0 + 1) / (7 * m0 - 7)
    ok(Fr(1, 3) + cgap < Fr(134, 100), "1/3 + (7m+1)/(7m-7) < 1.34 for m >= 2^%d" % BITS)
    ok(Fr(1, 4) * (1 + Fr(1, 1)) <= Fr(7, 8), "B-step ratio (1/4)(1+1/x) <= 7/8 for x >= 1")
    ok(log_iv(3)[1] + Fr(1, 3) * Fr(1, 1 << BITS) < Fr(11, 10), "log(3m+1) <= log m + 1.1")
    # all r = 1..R_CLAIM
    allok = True
    for r in range(1, R_CLAIM + 1):
        res, hist = part2_for(r, verbose=(r in (1, 50, R_CLAIM)))
        if not res:
            allok = False
            print("    r=%d fails: %s" % (r, hist))
    ok(allok, "for every r = 1..%d: Laurent bound + Farey reduction force m < 2^%d (contradiction)"
       % (R_CLAIM, BITS))
    res, hist = part2_for(R_CLAIM + 1)
    print("    (for information: r=%d %s with this method)" % (R_CLAIM + 1, "also passes" if res else "does not pass"))
    # sanity: step facts and the run congruence for small odd n
    good = True
    for x in range(1, 200001, 2):
        if x % 8 == 5:
            y = (7 * x + 1) // 4
            good &= (7 * x + 1) % 4 == 0 and y % 2 == 1 and y > x and 3 * y + 1 == Fr(7, 4) * (3 * x + 1)
            good &= (3 * x + 1) % 8 == 0
        else:
            good &= (3 * x + 1) % 8 != 0
    ok(good, "x = 5 mod 8 <=> 8 | 3x+1, and then S(x) = (7x+1)/4 with 3S(x)+1 = (7/4)(3x+1)  (odd x < 2e5)")


# ---------------------------------------------------------------------------
# Part 3: density of never-dropping starts
# ---------------------------------------------------------------------------
def part3():
    print("Part 3: H(X) <= (54/11) X^{log2(27/16)}")
    lam, w = Fr(27, 32), Fr(32, 27)
    ok(Fr(1, 2) * 1 + 1 * w <= 2 * lam * 1, "U node: A/2*W_U + A*W_O <= 2*lam*A*W_U")
    ok(Fr(7, 4) + Fr(1, 4) <= 2 * lam * w, "O node: (7/4)A*W_U + (1/4)A*W_U <= 2*lam*A*W_O")
    # exact verification of sum_{classes mod 2^j} A_j W_j <= (27/16)^j and intercept bound, j <= 18
    level = [(Fr(1), Fr(0), 'U', 0)]   # (A, B, state, n7)
    g1 = g2 = g3 = True
    for j in range(1, 19):
        new = []
        for A, B, s, n7 in level:
            if s == 'U':
                new.append((A / 2, B / 2, 'U', n7))
                new.append((A, B, 'O', n7))
            else:
                new.append((A * Fr(7, 4), (7 * B + 1) / 4, 'U', n7 + 1))
                new.append((A / 4, (B + 1) / 4, 'U', n7))
        level = new
        tot = sum(A * (1 if s == 'U' else w) for A, B, s, n7 in level)
        g1 &= tot <= Fr(27, 16) ** j
        g2 &= all(0 <= B and B + Fr(1, 3) <= Fr(2, 3) * Fr(7, 4) ** n7 and 2 * n7 <= j
                  and B < Fr(2) ** (j - 1) for A, B, s, n7 in level)
        g3 &= sum(1 for A, B, s, n7 in level if A >= Fr(1, 2)) <= 2 * Fr(27, 16) ** j
    ok(g1, "full depth-j tree, j <= 18: sum over 2^j classes of A*W <= (27/16)^j")
    ok(g2, "full depth-j tree, j <= 18: 0 <= B, B + 1/3 <= (2/3)(7/4)^{#7}, 2*#7 <= j, B < 2^(j-1)")
    ok(g3, "full depth-j tree, j <= 18: #{classes with A >= 1/2} <= 2(27/16)^j")
    ok(Fr(2, 3) < 1 and Fr(2, 3) * Fr(7, 4) < 2 and Fr(7, 4) < 4,
       "(2/3)(7/4)^{floor(j/2)} < 2^(j-1) for j = 1, 2, and j -> j+2 multiplies the sides by 7/4 < 4")
    # brute force count of never-dropping starts (drop within 10^4 steps counted as drop;
    # a start counted as non-dropping here only makes the test harder)
    good = True
    for j in range(0, 21):
        cnt = 0
        for n in range(1 << j, 1 << (j + 1)):
            x = n
            dropped = False
            for _ in range(10000):
                x = T(x)
                if x < n:
                    dropped = True
                    break
            cnt += not dropped
        good &= cnt <= 2 * Fr(27, 16) ** j
    ok(good, "brute force: #{never-dropping n in [2^j,2^(j+1))} <= 2(27/16)^j for j <= 20")


if __name__ == "__main__":
    part1()
    part2()
    part3()
    print("ALL CHECKS PASSED" if not FAIL else "FAILED: %s" % FAIL)
    sys.exit(1 if FAIL else 0)
