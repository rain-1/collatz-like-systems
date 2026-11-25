"""Shared engine for the one-expanding-run cycle theorems (CLS-048, 053, 054, 055).

Setting (see the .md files for the proofs of the inputs used here).
An accelerated map S on a set of positive integers has exactly one expanding
branch A (S(n) > n iff the step is A).  For a cycle of S whose expanding steps
form ONE cyclic block of length k (one local minimum), with minimum n0:

  * 0 < Lam := X log P - Y log Q,  where X, Y are the total exponents of the
    divisor prime P and the multiplier prime Q over one period;
  * Lam <= (c1*k + c0) / n0;
  * n0 >= low(k)        (k consecutive A-steps force a deep congruence);
  * ylo*k <= Y <= c_hi*k + c_hi0.

Part 1 (Baker).  Laurent-Mignotte-Nesterenko 1995, Cor. 2 gives
    log|Lam| >= -24.34 * max(log b' + 0.14, 21)^2 * logA1 * logA2
with alpha1 = 2 (log A1 = 1), alpha2 = the other prime (log A2 = log of it),
b' = b1/log A2 + b2 (b1 = exponent of 2, b2 = exponent of the other prime).
We check F(k0) > 0 where F(k) = log low(k) - log(c1 k + c0) - LMN(k); F is
increasing for k >= k0 (argued in the .md), so no such cycle has k >= k0.

Part 2 (finite).  For each Y <= Ymax, let X be minimal with P^X > Q^Y and
d = P^X - Q^Y.  Then Lam >= d / P^X for every admissible X (log x >= 1 - 1/x).
A cycle needs low(k) * d <= (c1 k + c0) * P^X for some admissible k.
Survivors give n0 <= (c1 k + c0) P^X / d; all such n0 are then tested directly.
"""
import math
from fractions import Fraction as Fr


def lmn_part(low_log, c1, c0, Q, P, c_hi, c_hi0, k0):
    """Return True iff F(k0) > 0 with a margin of at least 1 (floats, margin >> rounding)."""
    two_other = Q if P == 2 else P          # the prime that is not 2
    logA2 = math.log(two_other)
    # exponent of 2 and of the other prime as functions of Y (bounds):
    # X <= Y log Q / log P + 1 (since Lam < 1 here).
    Y = float(c_hi) * k0 + float(c_hi0)
    X = Y * math.log(Q) / math.log(P) + 1
    e2, eo = (X, Y) if P == 2 else (Y, X)
    bprime = e2 / logA2 + eo
    lmn = 24.34 * max(math.log(bprime) + 0.14, 21.0) ** 2 * 1.0 * logA2
    F = low_log(k0) - math.log(float(c1) * k0 + float(c0)) - lmn
    return F, bprime


def finite_part(Q, P, low, c1, c0, ylo, c_hi, c_hi0, Ymax):
    """Return list of survivors (Y, X, nbound) and the overall bound on n0."""
    c1, c0, c_hi, c_hi0 = Fr(c1), Fr(c0), Fr(c_hi), Fr(c_hi0)
    surv = []
    qY = 1
    X = 0
    pX = 1
    for Y in range(1, Ymax + 1):
        qY *= Q
        while pX <= qY:
            pX *= P
            X += 1
        d = pX - qY
        # admissible k: ylo*k <= Y <= c_hi*k + c_hi0, k >= 1
        kmin = max(1, math.ceil((Y - c_hi0) / c_hi))
        kmax = Y // ylo
        if kmin > kmax:
            continue
        # g(k) = (c1 k + c0)/low(k) is decreasing for k >= 2; test kmin, kmin+1
        ks = [k for k in (kmin, kmin + 1) if k <= kmax]
        feasible = False
        for k in ks:
            b = c1 * k + c0
            num, den = b.numerator, b.denominator
            lk = low(k)
            # infeasible iff lk * d * den > num * pX.  Rigorous prefilter by bit
            # lengths: x >= 2^(bitlen(x)-1) and x < 2^bitlen(x).
            if (lk.bit_length() - 1) + (d.bit_length() - 1) + (den.bit_length() - 1) \
                    >= num.bit_length() + pX.bit_length():
                continue
            if lk * d * den <= num * pX:
                feasible = True
        if feasible:
            nb = math.floor((c1 * kmax + c0) * pX / d)
            surv.append((Y, X, kmin, kmax, nb))
    return surv


def one_run_cycle_length(S, n0):
    """If n0 is the minimum of an S-cycle with exactly one maximal expanding run,
    return that run length k; else None.  Expanding step <=> S(x) > x."""
    x, k = n0, 0
    while True:
        y = S(x)
        if y > x:
            x, k = y, k + 1
        else:
            break
    if k == 0:
        return None
    while True:                      # descent: must stay >= n0, no new rise
        if x == n0:
            return k
        y = S(x)
        if y > x or y < n0:
            return None
        x = y


def run_theorem(name, S, in_domain, Q, P, low, low_log, c1, c0, ylo, c_hi, c_hi0, k0,
                expected, gcheck=range(2, 200)):
    ok = True
    # g(k) = (c1 k + c0)/low(k) decreasing for k >= 2 (spot check; exponential vs linear)
    c1f, c0f = Fr(c1), Fr(c0)
    for k in gcheck:
        if not (c1f * (k + 1) + c0f) * low(k) < (c1f * k + c0f) * low(k + 1):
            print("g not decreasing at", k); ok = False
    F, bp = lmn_part(low_log, c1, c0, Q, P, c_hi, c_hi0, k0)
    print(f"[{name}] Part 1: F(k0={k0}) = {F:.2f} (need > 1), b'(k0) <= {bp:.3g}")
    if not F > 1:
        ok = False
    Ymax = math.floor(Fr(c_hi) * (k0 - 1) + Fr(c_hi0))
    surv = finite_part(Q, P, low, c1, c0, ylo, c_hi, c_hi0, Ymax)
    N = max((s[4] for s in surv), default=0)
    print(f"[{name}] Part 2: Y <= {Ymax}; {len(surv)} survivors; n0 <= {N}")
    found = [(n, one_run_cycle_length(S, n)) for n in range(1, N + 1)
             if in_domain(n) and one_run_cycle_length(S, n)]
    print(f"[{name}] one-run cycle minima (n0, k): {found}")
    if found != expected:
        print("MISMATCH, expected", expected); ok = False
    return ok


def v(x, p):
    c = 0
    while x % p == 0:
        x //= p
        c += 1
    return c
