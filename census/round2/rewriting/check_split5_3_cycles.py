"""Rational certificates for the cycle bounds and the inverse path in split5_3_s27.md."""

from fractions import Fraction
from math import gcd


def log_bounds(denominator, terms=64):
    """Enclose log((d+1)/(d-1)) by the positive atanh series."""
    z = Fraction(1, denominator)
    lower = sum(2 * z**(2*j + 1) / (2*j + 1) for j in range(terms))
    tail = 2 * z**(2*terms + 1) / ((2*terms + 1) * (1 - z*z))
    return lower, lower + tail


def verify():
    log_two_lo, log_two_hi = log_bounds(3)
    log_ratio_lo, log_ratio_hi = log_bounds(9)
    alpha_lo = 2 + log_ratio_lo / log_two_hi
    alpha_hi = 2 + log_ratio_hi / log_two_lo
    floor_minimum = 2**48
    left = Fraction(4268621, 1838395)
    right = Fraction(227268, 97879)
    assert left < alpha_lo < alpha_hi + Fraction(11, floor_minimum) < right
    assert right.numerator * left.denominator - left.numerator * right.denominator == 1
    k_min = left.denominator + right.denominator
    assert k_min == 1936274 and int(k_min * alpha_lo) + 1 == 4495889
    assert log_two_lo > Fraction(2, 3) and log_ratio_lo > Fraction(1, 5)
    assert alpha_hi < Fraction(7, 3)
    assert Fraction(7, 6)**100 < 10**7

    # For K < q/2, these data imply |L-K*alpha| > 1/(2q).
    approximants = [
        (992575246277942597707, 427478890695834754646, 10**20),
        (57567975761, 24793177656, 3 * 10**9),
    ]
    for p, q, k_bound in approximants:
        assert gcd(p, q) == 1 and 2 * k_bound < q
        assert max(abs(Fraction(p,q) - x) for x in (alpha_lo, alpha_hi)) < Fraction(1, q*q)
    # e > 8/3 gives exact elementary checks for the logarithms in the proof.
    assert Fraction(8,3)**55 > 4 * 10**20
    assert 15 * 10**16 * (1+55) < 10**20
    assert Fraction(8,3)**59 > 2200 * approximants[0][1] + 3
    assert 5 * 10**7 * 59 < 3 * 10**9
    assert 2200 * approximants[1][1] < floor_minimum

    assert pow(4, 250, 625) == 1 and (2 * pow(4, 53, 625) - 3) % 625 == 0
    for u in range(1, 500, 2):
        n = (625*u-3)//2
        x = 256*u-3
        assert 0 < x < n
        for _ in range(4):
            assert x % 4 == 1
            x = (5*x + 3)//4
        assert x == 2*n
    print(f"Cycle bounds verified: at least {k_min:,} expanding blocks, "
          "6,432,163 original steps, and 101 expanding runs.")
    print("Backward merge verified for n = 311 mod 625.")



def verify_64_bit_bounds():
    two_lo, two_hi = log_bounds(3)
    ratio_lo, ratio_hi = log_bounds(9)
    alpha_lo, alpha_hi = 2 + ratio_lo/two_hi, 2 + ratio_hi/two_lo
    left = Fraction(1344399137, 579001193)
    right = Fraction(5136409418, 2212131129)
    assert left < alpha_lo < alpha_hi + Fraction(11, 2**64) < right
    assert right.numerator*left.denominator - left.numerator*right.denominator == 1
    k_min = left.denominator + right.denominator
    assert k_min == 2791132322 and k_min + int(k_min*alpha_lo) + 1 == 9271940877

    coefficient = 47 * 10**12
    assert alpha_hi/2 < Fraction(1161, 1000) and ratio_lo > Fraction(1, 5)
    assert 5*Fraction(1161, 1000)**200 < coefficient
    assert Fraction(8, 3)**61 > 4*10**25
    assert coefficient * 3 * 10**9 * 62 < 10**25

    approximants = [
        (116521770536551532152706941, 50183195075299715266313813),
        (8009031126156845, 3449301958915901),
    ]
    for (p, q), factor in zip(approximants, (1, 8)):
        assert gcd(p, q) == 1
        assert max(abs(Fraction(p, q) - x) for x in (alpha_lo, alpha_hi)) < Fraction(1, factor*q*q)
    first_q, last_q = (q for p, q in approximants)
    assert 2*10**25 < first_q
    assert Fraction(8, 3)**70 > 4400*first_q + 3
    assert 70*coefficient < last_q
    assert Fraction(8*2200*last_q, 7) < 2**64
    print("64-bit range implies at least 9,271,940,877 raw steps and 201 expanding runs per further cycle.")


if __name__ == "__main__":
    verify()
    verify_64_bit_bounds()
