"""Exact rational periodic realization of the 183-bit word in perm_1932_s8.md."""

from fractions import Fraction
from math import gcd

from _perm_common import T
from perm_1932_prefix_frequency import certificate, count_upper, upper_bit


NUMERATOR = (2, 4, 4)
OFFSET = (0, -1, 1)


def rational_cycle(word):
    # The composed map is (q*x + s)/d.
    q, s, d = 1, 0, 1
    for r in word:
        q, s, d = NUMERATOR[r] * q, NUMERATOR[r] * s + OFFSET[r] * d, 3 * d
    start = Fraction(s, d - q)
    orbit = []
    x = start
    for r in word:
        assert gcd(x.denominator, 6) == 1
        assert x.numerator * pow(x.denominator, -1, 3) % 3 == r
        orbit.append(x)
        x = (NUMERATOR[r] * x + OFFSET[r]) / 3
    assert x == start
    return orbit


def rational_bit(x):
    assert x > 0
    scale = Fraction(2) ** (x.numerator.bit_length() - x.denominator.bit_length())
    if x < scale:
        scale /= 2
    return int(2 * x >= 3 * scale)


def check_word():
    n = 4055
    segment = [n]
    word = []
    for _ in range(130):
        word.append(n % 3)
        n = T(n)
        segment.append(n)
    assert (segment[53], segment[65], segment[-1]) == (8, 129, 16315)
    word += [0] * 12 + list(map(int, "11121221121222122221222222212")) + [0] * 12
    orbit = rational_cycle(word)
    assert len(set(orbit)) == len(orbit) == 183
    assert min(orbit) == orbit[53] and 0 < orbit[53] - 8 < Fraction(1, 10**9)
    assert all(0 < x - z < Fraction(1, 100000) for x, z in zip(orbit, segment))
    assert all((x - z).numerator % 11 == 0 and x.denominator % 11 != 0
               for x, z in zip(orbit, segment))
    assert orbit[53].denominator.bit_length() == 286
    bits = [rational_bit(x) for x in orbit]

    n = 2033
    previous_word = []
    for _ in range(183):
        previous_word.append(upper_bit(n))
        n = T(n)
    assert bits == previous_word[53:] + previous_word[:53]
    assert (sum(bits[:65]), sum(bits[65:130]), sum(bits)) == (28, 26, 76)

    n = 4055
    for j in range(235):
        assert upper_bit(n) == bits[j % 183]
        n = T(n)
    assert n == 6237833 and upper_bit(n) == 0 and bits[235 % 183] == 1
    n = 62
    for _ in range(65):
        n = T(n)
    assert count_upper(n, 65) == 27


def check_frequency():
    sign, min_limit, period_limit = certificate("11", Fraction(76, 183))
    assert (sign, min_limit, period_limit) == (-1, 1395, 32768)
    cycles = {}
    visited = set()
    for m in range(1, min_limit):
        # If an earlier, smaller seed visited m, injectivity rules out m
        # as the minimum of a finite cycle.
        if m in visited:
            continue
        n = m
        for length in range(1, period_limit + 1):
            if n < min_limit:
                visited.add(n)
            n = T(n)
            if n < m:
                break
            if n == m:
                cycles[m] = length
                break
    assert cycles == {1: 1, 2: 2, 4: 5, 44: 12}


def check_modular_construction():
    # The padded integer segment starts at 18. The four minus branches
    # steer the composite back to 18 mod 5 before its fixed point is taken.
    anchor = [2] * 4 + [0] * 3
    word = [0, 0, 2, 2, 0] + [1] * 4 + anchor * 72 + [2] * 106 + [0] * 74
    orbit = rational_cycle(word)
    assert len(set(orbit)) == 693 and min(orbit) > 8
    for x, target in zip(orbit[1:4], (12, 8, 11)):
        difference = x - target
        assert 0 < difference < Fraction(1, 2)
        assert gcd(difference.denominator, 30) == 1 and difference.numerator % 30 == 0


if __name__ == "__main__":
    check_word()
    check_frequency()
    check_modular_construction()
    print("Verified the rational 183-cycle, the exact 235-bit match, and the integer frequency exclusion.")
