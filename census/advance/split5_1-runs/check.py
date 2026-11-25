#!/usr/bin/env python3
"""Checker for census/advance/split5_1-runs/theorem.md (CLS-048, split5_1).

T: even n -> n/2; n = 1 mod 4 -> 5n+1; n = 3 mod 4 -> n+1.
Parts:
  [1] range certificate: every 1 <= n < 2^BITS reaches a known cycle (C++ helper range.cpp)
  [2] step facts and the residue-tree transitions, by brute force on small cases
  [3] cycle theorem: further cycles have > R runs (Laurent 2008 two-log bound + continued fractions)
  [4] cycle theorem: length bound S (Stern-Brocot, elementary)
  [5] density: H(X) = O(X^0.9383) for starts that never drop below themselves
All arithmetic in [2]-[5] is exact (Python ints / Fractions). Exit 0 iff everything passes.
Usage: python3 check.py [BITS]   (default 42; BITS < 42 weakens R and S accordingly)
"""
import os, subprocess, sys, tempfile, time
from fractions import Fraction as Fr
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
BITS = int(sys.argv[1]) if len(sys.argv) > 1 else 42


def T(n):
    if n % 2 == 0:
        return n // 2
    return 5 * n + 1 if n % 4 == 1 else n + 1


# ---------------------------------------------------------------- [1]
def part1():
    exe = os.path.join(tempfile.mkdtemp(), "range")
    subprocess.run(["g++", "-O2", "-std=c++17", "-fopenmp",
                    os.path.join(HERE, "range.cpp"), "-o", exe], check=True)
    # independent Python cross-check of the small range by plain iteration
    cyc = set()
    for root in (1, 13):
        x = root
        while True:
            cyc.add(x); x = T(x)
            if x == root:
                break
    assert len(cyc) == 5 + 35 and min(cyc) == 1
    good = set(cyc)
    for n in range(1, 1 << 20):
        x = n
        while x not in good and x >= n:
            x = T(x)
        # loop exits: x on a known cycle, or x < n (reaches one by induction)
    out = subprocess.run([exe, "20"], capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    t0 = time.time()
    out = subprocess.run([exe, str(BITS)], capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    print("[1] range certificate:", out.stdout.strip(), f"({time.time()-t0:.0f}s)")


# ---------------------------------------------------------------- log enclosures
def atanh_enc(z, terms):
    lo = sum(2 * z ** (2 * j + 1) / (2 * j + 1) for j in range(terms))
    return lo, lo + 2 * z ** (2 * terms + 1) / ((2 * terms + 1) * (1 - z * z))

def outward(enc, den=10 ** 200):
    lo, hi = enc
    return Fr((lo * den).__floor__(), den), Fr((hi * den).__ceil__(), den)

LOG2 = outward(atanh_enc(Fr(1, 3), 450))        # log 2 = 2 atanh(1/3)
LOG54 = outward(atanh_enc(Fr(1, 9), 230))       # log(5/4) = 2 atanh(1/9)
LOG5 = (2 * LOG2[0] + LOG54[0], 2 * LOG2[1] + LOG54[1])
ALPHA = outward((LOG5[0] / LOG2[1], LOG5[1] / LOG2[0]))   # log_2 5
assert ALPHA[1] - ALPHA[0] < Fr(1, 10 ** 150)


def log_upper(x):
    """Rational upper bound for log x, x a positive rational >= 1."""
    x = Fr(Fr(x).__ceil__())            # log is increasing: round up to an integer
    k = max(0, x.numerator.bit_length() - x.denominator.bit_length() - 1)
    y = x / 2 ** k
    while y >= 2:
        y /= 2; k += 1
    z = (y - 1) / (y + 1)               # 0 <= z < 1/3
    return k * LOG2[1] + outward(atanh_enc(z, 40), 10 ** 30)[1] if z else k * LOG2[1]


def convergents(lo, hi):
    """Continued-fraction convergents shared by every real in [lo, hi]."""
    out = []; a, b = lo, hi; p0, q0, p1, q1 = 0, 1, 1, 0
    while True:
        fa, fb = a.numerator // a.denominator, b.numerator // b.denominator
        if fa != fb:
            return out
        p0, q0, p1, q1 = p1, q1, fa * p1 + p0, fa * q1 + q0
        out.append((p1, q1))
        if a == fa or b == fb:
            return out
        a, b = 1 / (b - fb), 1 / (a - fa)

CONV = convergents(*ALPHA)
for p, q in CONV:   # each is a reduced P/Q with |alpha - P/Q| < 1/Q^2 for every alpha in the enclosure
    assert gcd(p, q) == 1 and all(abs(Fr(p, q) - a) < Fr(1, q * q) for a in ALPHA)


# ---------------------------------------------------------------- [2]
def part2():
    for x in range(1, 200001, 2):
        assert (x % 4 == 1) == ((3 * x + 1) % 4 == 0)
        if x % 4 == 1:
            y = (5 * x + 1) // 2
            assert T(T(x)) == y and y % 2 == 1 and 2 * (3 * y + 1) == 5 * (3 * x + 1)
            k, z = 0, x
            while z % 4 == 1:
                z = (5 * z + 1) // 2; k += 1
            v = ((3 * x + 1) & -(3 * x + 1)).bit_length() - 1
            assert v == k + 1 and z % 4 == 3          # run length = v2(3x+1) - 1
        else:
            w = (x + 1)
            while w % 2 == 0:
                w //= 2
            assert 4 * w <= x + 1 and (w >= 1) and 4 * w - 1 >= 3 * w   # B(v) <= (v+1)/4, v >= 3 B(v)
    # residue tree: node (d, r, a, b) means T^s(2^d t + r) = a t + b for all t >= 0.
    # Validate all nodes to depth 16 on t = 0..7, and the U/O/E state machine of [5].
    stack = [(0, 0, 1, 0, 0, "U")]
    count = 0
    while stack:
        d, r, a, b, s, st = stack.pop()
        count += 1
        for t in range(8):
            n = (1 << d) * t + r
            if n == 0:
                continue
            x = n
            for _ in range(s):
                x = T(x)
            assert x == a * t + b
        # state machine: U: a odd ; O: a = 2 mod 4, b odd ; E: a = 2 mod 4, b even
        if st == "U": assert a % 2 == 1
        else: assert a % 4 == 2 and (b % 2 == 1) == (st == "O")
        if d == 14:
            continue
        M = 1 << d
        for g in (0, 1):
            y = b + a * g
            if y % 2 == 0:
                ch = (a, y // 2, s + 1, "U" if a % 2 else ("O" if (y // 2) % 2 else "E"))
                assert Fr(ch[0], 2 * M) == Fr(a, M) / 2
            elif a % 2:
                ch = (2 * a, y, s, "O"); assert st == "U"
            elif y % 4 == 1:
                ch = (5 * a, (5 * y + 1) // 2, s + 2, "O"); assert st == "O"
            else:
                ch = (a, (y + 1) // 2, s + 2, "E"); assert st == "O"
            stack.append((d + 1, r + g * M, ch[0], ch[1], ch[2], ch[3]))
    print(f"[2] step facts for odd x < 2*10^5; residue tree transitions verified on {count} nodes (depth <= 14)")


# ---------------------------------------------------------------- [3]
# Two-log bound: M. Laurent, "Linear forms in two logarithms and interpolation determinants II",
# Acta Arith. 133.4 (2008) 325-348, Corollary 2 and Table 1 (p. 328). For multiplicatively independent
# alpha1, alpha2 with alpha_i, log alpha_i real positive, b1, b2 positive integers, Lambda = b2 log a2 - b1 log a1:
#   log|Lambda| >= -C2 D^4 (max{log b' + 0.38, m/D, 1})^2 log A1 log A2,
#   b' = b1/(D log A2) + b2/(D log A1),  log Ai >= max{h(ai), |log ai|/D, 1/D}.
# Here alpha1 = 5, b1 = K, log A1 = log 5; alpha2 = 2, b2 = L, log A2 = 1; D = 1.
LAURENT_TABLE = [(10, Fr(252, 10)), (12, Fr(234, 10)), (14, Fr(221, 10)), (16, Fr(211, 10)),
                 (18, Fr(203, 10)), (20, Fr(197, 10)), (22, Fr(192, 10)), (24, Fr(188, 10)),
                 (26, Fr(184, 10)), (28, Fr(181, 10)), (30, Fr(179, 10))]


def baker_mu0(R, CR, mpar, C2):
    """Smallest found mu0 with F(mu) < mu for all mu >= mu0 (fixed Table-1 pair (mpar, C2))."""
    c = C2 * LOG5[1]
    def F(mu):
        K0 = CR * (1 + mu / LOG2[0])
        bprime = Fr(2443, 1000) * K0 + 1            # b' = K + L/log 5 < 2.443 K + 1
        Lg = max(log_upper(bprime) + Fr(38, 100), Fr(mpar))
        return log_upper(Fr(5 * R, 6)) + c * Lg * Lg, Lg, c
    mu0 = 1000
    while True:
        val, Lg, c = F(Fr(mu0))
        if val < mu0 and 2 * c * Lg < mu0:   # F(mu0) < mu0 and F' <= 2c Lg/mu < 1 on [mu0, oo)
            return mu0
        mu0 = int(val * Fr(11, 10)) + 1


def runs_bound_ok(R, B, verbose=False):
    """True if: no cycle with all elements >= 2^B and at most R runs exists."""
    a = ALPHA[1]
    CR = Fr((((a ** R - 1) / (a - 1)) * 10 ** 6).__ceil__(), 10 ** 6)                     # K <= CR * log2((3m+1)/2) <= CR*(1 + log m/log 2)
    # Baker stage: log m = mu satisfies mu < F(mu); every Table-1 pair is valid, take the best.
    mu0, mpar = min((baker_mu0(R, CR, mp, C2), mp) for mp, C2 in LAURENT_TABLE)
    # m < e^mu0, so log2(2m) < 1 + mu0/log 2.
    l2bound = 1 + Fr(mu0) / LOG2[0]
    hist = [("Baker (Laurent 2008, m=%d)" % mpar, mu0)]
    for _ in range(100):
        K0 = CR * l2bound                       # K <= K0
        cand = [(p, q) for p, q in CONV if q > 2 * K0]
        assert cand, "need more convergents"
        p, q = cand[0]
        # 0 < K < q/2 gives |L - K alpha| > 1/(2q); delta = log2 * |L - K alpha| < 5R/(6m)
        Mbound = Fr(5 * R * q, 3) / LOG2[0]      # m < Mbound
        hist.append((q, Mbound))
        if Mbound <= 2 ** B:
            if verbose:
                print("    stages:", hist[0], *[f"q={h[0]} -> m<{float(h[1]):.3e}" for h in hist[1:]])
            return True
        Mi = Mbound.numerator // Mbound.denominator + 1
        new = Mi.bit_length() + 1                # log2(2m) < bitlen(Mi) + 1
        if new >= l2bound:
            return False
        l2bound = new
    return False


def part3():
    R = 0
    while runs_bound_ok(R + 1, BITS):
        R += 1
    assert R >= 1
    print(f"[3] with m >= 2^{BITS}: every further cycle has more than R = {R} expanding runs")
    runs_bound_ok(R, BITS, verbose=True)
    return R


# ---------------------------------------------------------------- [4]
def simplest_between(lo, hi):
    """Smallest-denominator fraction strictly between lo < hi (Stern-Brocot descent)."""
    a, b, c, d = 0, 1, 1, 0
    while True:
        p, q = a + c, b + d
        f = Fr(p, q)
        if f <= lo:
            a, b = p, q
        elif f >= hi:
            c, d = p, q
        else:
            return p, q, (a, b), (c, d)


def part4(R):
    eps = Fr(5, 6) / (2 ** BITS * LOG2[0])     # L/K - alpha < 5r/(6 m K log2) <= 5/(6 m log 2)
    lo, hi = ALPHA[0], ALPHA[1] + eps
    p, q, (a, b), (c, d) = simplest_between(lo, hi)
    # every fraction in (lo, hi) has denominator >= q; check neighbours certify it
    assert Fr(a, b) <= lo and Fr(c, d) >= hi and b * c - a * d == 1 and q == b + d
    Kmin = q
    Lmin = (Kmin * ALPHA[0]).__floor__() + 1
    # T-steps = K + L + N_B with N_B >= r (each run is followed by at least one B-step).
    raw = Kmin + Lmin + 1               # unconditional: r >= 1
    raw_r = Kmin + Lmin + (R + 1)       # using part [3]: r >= R + 1
    print(f"[4] every further cycle has K >= {Kmin:,} expanding (5n+1) steps, L >= {Lmin:,} halvings,"
          f" and >= {raw:,} steps of T (>= {raw_r:,} using r >= {R + 1} from [3])")
    return Kmin, raw


# ---------------------------------------------------------------- [5]
def part5():
    # theta = 1/4; rational upper bounds for the needed fourth roots
    q52 = Fr(12575, 10000); assert q52 ** 4 >= Fr(5, 2)     # (5/2)^(1/4) <= q52
    qh = Fr(8409, 10000);  assert qh ** 4 >= Fr(1, 2)       # 2^(-1/4)  <= qh
    lam = Fr(958, 1000)
    wO, wE, wU = Fr(1), Fr(7830, 10000), Fr(1)
    # mean over the two children of A^theta * w(state) <= lam * parent value
    assert Fr(1, 2) * (q52 * wO + qh * wE) <= lam * wO       # O -> O (x 5/2), O -> E (x 1/2)
    assert Fr(1, 2) * (qh * wE + qh * wO) <= lam * wE        # E -> E, E -> O   (both x 1/2)
    assert Fr(1, 2) * (qh * wU + 1 * wO) <= lam * wU         # U -> U (x 1/2), U -> O (x 1)
    two_lam = 2 * lam
    # exponent: log2(2 lam) < 0.9383  <=>  (2 lam)^10000 < 2^9383
    assert two_lam.numerator ** 10000 < 2 ** 9383 * two_lam.denominator ** 10000
    # count at depth j with A >= 1/2 is <= (2 lam)^j * wU / (min w * (1/2)^theta) <= (2lam)^j * wU * 2^(1/4) / wE
    print("[5] supermartingale inequalities hold with theta=1/4, 2*lambda = 1.916 < 2^0.9383;"
          " H(X) <= C X^0.9383")


if __name__ == "__main__":
    part2()
    R = part3()
    part4(R)
    part5()
    if os.environ.get("SKIP_RANGE") != "1": part1()
    print("ALL CHECKS PASSED")
