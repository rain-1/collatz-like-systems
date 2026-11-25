"""Exact certificate for the one-minimum theorem in results/perm_d_s3.md."""

import sys
from fractions import Fraction
from math import gcd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from census.round2.rewriting.check_split5_3_cycles import log_bounds
from census.systems import get


def verify_exponent_reduction():
    two_lo, two_hi = log_bounds(3)
    ratio_lo, ratio_hi = log_bounds(9)
    alpha_lo = 2 + ratio_lo / two_hi
    alpha_hi = 2 + ratio_hi / two_lo
    p, q = 8009031126156845, 3449301958915901
    assert gcd(p, q) == 1
    assert max(abs(x - Fraction(p, q)) for x in (alpha_lo, alpha_hi)) < Fraction(1, q*q)
    # Square the coefficient comparison to avoid evaluating sqrt(2).
    assert (Fraction(14, 10) * 30**5 * 2)**2 * 2**9 < (2 * 10**9)**2
    assert two_lo > Fraction(1, 2)
    assert Fraction(8, 3)**32 > 16 * 10**12  # e > 8/3
    assert 10**12 * two_lo > 2 * 10**9 * 33
    assert 2 * 16 * 10**12 < q and 8*q < 2**55


def verify_cycles():
    step = get("perm_d_s3")["step"]
    assert step(1) == 1
    bounds = {}
    cycles = []
    for k in range(1, 55):
        for ell in range(1, 3*k + 2):
            gap = abs(2**(k + 3*ell) - 5**(k + ell))
            upper = (8**ell - 5**ell) // gap
            if upper:
                bounds[k, ell] = upper
            for u in range(1, upper + 1, 2):
                start = 2**k * u
                n = start
                orbit = []
                for i in range(k + ell):
                    if n % 2 != int(i >= k):
                        break
                    orbit.append(n)
                    n = step(n)
                else:
                    if n == start:
                        cycles.append(tuple(orbit))
    assert bounds == {(1, 2): 13, (2, 4): 4, (3, 6): 1}
    assert cycles == [(2, 5, 3), (6, 15, 9), (26, 65, 41)]
    print("Verified exponent reduction, all candidate bounds, and cycles:", cycles)


if __name__ == "__main__":
    verify_exponent_reduction()
    verify_cycles()
