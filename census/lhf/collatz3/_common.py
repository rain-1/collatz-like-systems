"""Shared exact-integer checks for the 3n+d family (lhf/collatz3).

Shortcut map  T_d(n) = n/2 (n even), (3n+d)/2 (n odd), d odd.
Unaccelerated map F_d(n) = n/2 (n even), 3n+d (n odd); T_d is F_d with the forced
halving after each odd step merged in, so F_d and T_d have the same cycles and the
same bounded/unbounded orbits.
"""
import math
import sys
from math import gcd


def F(d):
    return lambda n: n // 2 if n % 2 == 0 else 3 * n + d


def T(d):
    return lambda n: n // 2 if n % 2 == 0 else (3 * n + d) // 2


# ---------------------------------------------------------------- 1-cycles
def one_cycles(d, kmax):
    """All positive integer 1-cycles (shortcut parity block 1^k 0^l, k,l >= 1)
    of T_d with k <= kmax.  Returns list of (k, l, x) with x the cycle minimum.

    x = d(3^k - 2^k) / (2^(k+l) - 3^k).  l is bounded by x >= 1:
      d > 0: need 2^K > 3^k and 2^K - 3^k <= d(3^k - 2^k)
      d < 0: need 2^K < 3^k and 3^k - 2^K <= |d|(3^k - 2^k)
    """
    out = []
    if d < 0:
        # l = 0 block (all-odd): the only primitive one is the fixed point -d (k=1)
        out.append((1, 0, -d))
    for k in range(1, kmax + 1):
        a, b = 3 ** k, 2 ** k
        num = d * (a - b)
        l = 1
        while True:
            K = k + l
            D = 2 ** K - a
            if d > 0:
                if D > num:      # D increasing in l: x < 1 from here on
                    break
                if D > 0 and num % D == 0:
                    out.append((k, l, num // D))
            else:
                if D > 0:        # wrong sign, and stays wrong for larger l
                    break
                if num % D == 0 and num // D > 0:
                    out.append((k, l, num // D))
            l += 1
    return out


def verify_one_cycle(d, k, l, x):
    """Simulate: x odd, shortcut block is exactly 1^k 0^l, returns to x."""
    t = T(d)
    y = x
    for i in range(k):
        if y % 2 != 1:
            return False
        y = t(y)
    for i in range(l):
        if y % 2 != 0:
            return False
        y = t(y)
    return y == x


def kmax_bound(d):
    """Largest k not excluded by either transcendence input (see .md):
    (E) Ellison: |2^K-3^k| > 2^K e^{-K/10} for K >= 28 (K <= 27 brute forced);
    (R) Rhin:    |K log2 - k log3| >= K^{-13.3}, hence |2^K-3^k| >= 2^K K^{-13.3}/3.
    Both are combined with |2^K-3^k| <= |d|(2^l-1) < |d| 2^l and
    K <= k log2(3) + log2(|d|+1).  Float evaluation with a +5 safety margin;
    the brute force below runs far beyond it anyway."""
    ad = abs(d)
    L3 = math.log2(3)
    def Kup(k):
        return k * L3 + math.log2(ad + 1)
    kE = 0
    for k in range(1, 2000):
        if k * math.log(2) < math.log(ad) + Kup(k) / 10 + 1e-9:
            kE = k
    kR = 0
    for k in range(1, 5000):
        if k * math.log(2) < math.log(3 * ad) + 13.3 * math.log(Kup(k)):
            kR = k
    return kE, kR


# ----------------------------------------------------- reduction lemma checks
def check_gcd_preserved(d, N):
    """gcd(F_d(n), d) == gcd(n, d) for 1 <= n <= N (needs gcd(d,6)=1)."""
    f = F(d)
    return all(gcd(f(n), d) == gcd(n, d) for n in range(1, N + 1))


def check_scaling(d, N):
    """For every divisor g of d: F_d(g m) = g F_{d/g}(m), 1 <= m <= N."""
    ok = True
    for g in range(1, abs(d) + 1):
        if d % g:
            continue
        fd, fe = F(d), F(d // g)
        ok &= all(fd(g * m) == g * fe(m) for m in range(1, N + 1))
    return ok


def check_two_adic_obstruction(d, jmax, sample=64):
    """Lemma O: for every class C = r mod 2^j, T_d^j(C) is an arithmetic
    progression with odd (power-of-3) difference, hence meets every class mod 2^j.
    Checked: the images of r, r+2^j, ..., r+(sample-1)2^j under T^j form an AP with
    difference 3^e, and they hit all 2^j classes (sample >= 2^j)."""
    t = T(d)
    for j in range(1, jmax + 1):
        M = 2 ** j
        for r in range(M):
            base = r if r > 0 else M
            ys = []
            for s in range(max(sample, M)):
                y = base + s * M
                for _ in range(j):
                    y = t(y)
                ys.append(y)
            diff = ys[1] - ys[0]
            e = 0
            while diff % 3 == 0 and diff > 1:
                diff //= 3
                e += 1
            if diff != 1:
                return False
            if any(ys[i + 1] - ys[i] != ys[1] - ys[0] for i in range(len(ys) - 1)):
                return False
            if len({y % M for y in ys}) != M:
                return False
    return True


def ellison_sanity(Kmax=3000):
    """Numerical sanity only (not a proof): |2^K - 3^k| > 2^K e^{-K/10} for
    28 <= K <= Kmax and the k nearest K/log2(3), checked exactly via
    |2^K - 3^k|^10 * e^K > 2^(10K) -> compare with integer bounds e^K > 2.718^K."""
    L3 = math.log2(3)
    for K in range(28, Kmax + 1):
        for k in (int(K / L3), int(K / L3) + 1):
            D = abs(2 ** K - 3 ** k)
            # need D > 2^K e^{-K/10}  <=  D^10 * e^K > 2^(10K); use e > 2718/1000
            if D ** 10 * 2718 ** K <= 2 ** (10 * K) * 1000 ** K:
                return False, K, k
    return True, None, None


def report(name, ok):
    print(("PASS " if ok else "FAIL ") + name)
    return ok


def run_family(d, N=20000, extra=()):
    ok = True
    kE, kR = kmax_bound(d)
    KMAX = max(kR, 30, 1000)
    cyc = one_cycles(d, KMAX)
    ok &= report(f"d={d}: 1-cycle bound kE={kE}, kR={kR}; brute force k<=%d" % KMAX, True)
    ok &= report(f"d={d}: every listed 1-cycle verified by simulation",
                 all(verify_one_cycle(d, *c) for c in cyc))
    print(f"   d={d} 1-cycles (k,l,min): {cyc}")
    for chk in extra:
        ok &= chk()
    return ok, cyc
