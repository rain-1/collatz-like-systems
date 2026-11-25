"""Exact certificate for the seven-run exclusion in CLS-037.md."""

import sys
from fractions import Fraction
from math import gcd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from census.round2.rewriting.check_split5_3_cycles import log_bounds
from census.systems import get


def verify_bounds():
    log2_lo, log2_hi = log_bounds(3)
    log3_lo, log3_hi = log_bounds(2)
    alpha_lo = 2 * log3_lo / log2_hi
    alpha_hi = 2 * log3_hi / log2_lo
    assert log2_lo > Fraction(1, 2) and log2_hi < 1 and log3_hi < 2
    assert 3 < alpha_lo < alpha_hi < Fraction(16, 5)
    assert (Fraction(16, 5)**7 - 1) / 2 < 1800
    assert (Fraction(14, 10) * 30**5 * 2)**2 * 2**9 < (2 * 10**9)**2
    assert 3600 * (3 + 2 * 10**9) < 10**13
    assert Fraction(8, 3)**37 > 4 * 10**15  # e > 8/3
    assert 10**13 * 38 < 10**15

    approximants = [(19763055687104648, 6234549927241963), (603988, 190537)]
    odd_steps_bound = 10**15
    for p, q in approximants:
        assert odd_steps_bound < q and gcd(p, q) == 1
        error = max(abs(Fraction(p, q) - x) for x in (alpha_lo, alpha_hi))
        assert error < Fraction(1, 2*q*q)
        minimum_bound = 4*q
        # bit_length gives an upper bound on log_2(7m+1).
        odd_steps_bound = 1800 * (7*minimum_bound + 1).bit_length()
    assert minimum_bound == 762148
    return minimum_bound


def exclude_small_minima(bound):
    step = get("par_9_1_s5")["step"]
    for start in range(1, bound, 2):
        n = start
        for runs in range(1, 8):
            while n % 2:
                n = step(step(n))  # odd step and its mandatory halving
            while n % 2 == 0:
                n = step(n)
            if n == start:
                raise AssertionError(f"cycle from {start} after {runs} rising runs")
            if n < start:
                break  # this start cannot be the cycle minimum
    print(f"Excluded each of the {bound//2:,} odd candidate minima through seven rising runs.")


if __name__ == "__main__":
    exclude_small_minima(verify_bounds())
