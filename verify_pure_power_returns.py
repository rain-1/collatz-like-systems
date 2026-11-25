"""Exact finite certificates for pure-power returns in short or partly expanding paths.

Run with Python 3. The accompanying proof uses Matveev's theorem to reduce
the three-branch-run and one-contraction cases to a < 200, and the case of
three contracting runs to a < 1024. A run is a maximal block of steps with
the same input residue modulo 3. Counting starts at 2**a, after the forced
contraction from 3**a.
"""

from fractions import Fraction
from math import gcd


def log_bounds(n):
    """Enclose log(n) by the atanh series and a geometric tail bound."""
    z = Fraction(n - 1, n + 1)
    terms = 100
    lower = 2 * sum(z ** (2 * k + 1) / (2 * k + 1) for k in range(terms))
    first_omitted = 2 * z ** (2 * terms + 1) / (2 * terms + 1)
    return lower, lower + first_omitted / (1 - z * z)


def check_approximation():
    p, q = 9881527843552324, 6234549927241963
    lo2, hi2 = log_bounds(2)
    lo3, hi3 = log_bounds(3)
    assert gcd(p, q) == 1
    assert Fraction(p * q - 1, q * q) < lo3 / hi2
    assert hi3 / lo2 < Fraction(p * q + 1, q * q)
    assert 2 * 16 * (10**12 + 1) < q
    assert 4 * q * 7 * 201 < 2**100
    assert 2 * 125 * 10**12 < q
    assert 4 * q * 50 * 1024 < 2**128


def power_of_three_exponent(n):
    exponent = 0
    while n % 3 == 0:
        n //= 3
        exponent += 1
    return exponent if n == 1 and exponent > 0 else None


def first_hit(a):
    n = 2**a
    for run in range(1, 4):
        residue = n % 3
        while n % 3 == residue:
            quotient = n // 3
            n = (2 * quotient, 4 * quotient + 1, 4 * quotient + 3)[residue]
            b = power_of_three_exponent(n)
            if b is not None:
                return a, b, run
    return None


def nonincreasing_hits(a, run_limit, step_limit):
    """Yield all power hits until the proved step or contracting-run bound."""
    n = 2**a
    previous_residue = None
    contracting_runs = 0
    for step in range(1, step_limit + 1):
        quotient, residue = divmod(n, 3)
        if residue == 0 and previous_residue != 0:
            contracting_runs += 1
            if contracting_runs > run_limit:
                break
        previous_residue = residue
        n = (2 * quotient, 4 * quotient + 1, 4 * quotient + 3)[residue]
        b = power_of_three_exponent(n)
        if b is not None and b <= a:
            yield a, b, step, contracting_runs


if __name__ == "__main__":
    check_approximation()
    hits = [hit for a in range(1, 200) if (hit := first_hit(a)) is not None]
    assert hits == [(1, 1, 1), (2, 2, 3)]
    print("Verified the rational approximation and cutoff comparisons.")
    print("First hits (starting exponent, ending exponent, run):", hits)
    downward_hits = [
        hit[:3] for a in range(1, 200)
        if (hit := next(nonincreasing_hits(a, 1, 8 * a), None)) is not None
    ]
    assert downward_hits == [(1, 1, 1), (2, 2, 3)]
    print("First nonincreasing hits with at most one contracting run (a, b, step):",
          downward_hits)
    three_run_hits = [
        hit for a in range(3, 1024) for hit in nonincreasing_hits(a, 3, 74 * a)
    ]
    assert three_run_hits == [(5, 3, 9, 3)]
    print("All nonincreasing hits for a >= 3 with at most three contracting runs"
          " (a, b, step, runs):", three_run_hits)
