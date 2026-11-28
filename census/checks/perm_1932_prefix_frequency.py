"""Exact frequency certificates for leading binary prefixes of the 1932 permutation."""

from fractions import Fraction

from _perm_common import T, Tinv


def certificate(prefix, threshold):
    """For a proper prefix and rational threshold in [0,1], bound exceptional cycles.

    Return the sign of the escaping frequency minus the threshold, a strict
    upper bound on an exceptional cycle's minimum, and a period upper bound.
    The construction guarantees termination, not efficiency for close cuts.
    """
    if len(prefix) < 2 or prefix[0] != "1" or set(prefix) - {"0", "1"}:
        raise ValueError("expected a binary prefix of length at least two starting in 1")
    if not 0 <= threshold <= 1:
        raise ValueError("expected a threshold in [0,1]")
    h = int(prefix, 2)
    width = Fraction(h + 1, h)
    p, q = threshold.as_integer_ratio()
    sign = 1 if (h + 1) ** q > h**q * 2**p else -1
    if prefix == "11":
        a, b = 2 ** (2 * q - p), 3**q
        delta = Fraction(abs(a - b), q * max(a, b))
        j = 0
        while 3 * delta * 2**j <= 1 + j:
            j += 1
        return sign, int((1 + 1 / delta) / 4) + 1, 2**j
    if sign < 0:
        width = 2 / width
        p = q - p

    k = 1
    points = [Fraction(1)]
    denominator = 1
    while True:
        required = k * p // q + 1
        ordered = sorted(points)
        wrapped = ordered + [2 * x for x in ordered]
        gap = max(wrapped[i + required] / x for i, x in enumerate(ordered))
        if gap < width:
            break
        for _ in range(k):
            denominator *= 3
            points.append(Fraction(1 << (denominator - 1).bit_length(), denominator))
        k *= 2

    height = 1
    while gap * Fraction(4 * height + 1, 4 * height - 1) ** (k - 1) >= width:
        height *= 2
    period = k * (height - 1) * required * q // (required * q - k * p)
    return sign, height, period


def compare_frequency(seed, prefix, threshold):
    """Compare the limiting frequency with a Fraction in [0,1], returning -1, 0, or 1."""
    if seed < 1:
        raise ValueError("expected a positive seed")
    sign, _, period_bound = certificate(prefix, threshold)
    h = int(prefix, 2)
    n = seed
    count = 0
    for length in range(1, period_bound + 1):
        leading = (n << (len(prefix) - 1)) >> (n.bit_length() - 1)
        count += leading == h
        n = T(n)
        if n == seed:
            difference = count * threshold.denominator - length * threshold.numerator
            return (difference > 0) - (difference < 0)
    return sign


def upper_bit(n):
    return int(2 * n >= 3 * (1 << (n.bit_length() - 1)))


def count_upper(start, length):
    n = start
    count = 0
    for _ in range(length):
        count += upper_bit(n)
        n = T(n)
    return count


def check_outer_frequencies():
    assert 900 * (3**12 - 2**19) > 12 * 3**12
    assert 900 * (2**8 - 3**5) > 5 * 2**8
    found = {}
    for minimum in range(1, 226):
        n = minimum
        count = 0
        for length in range(1, 4097):
            count += upper_bit(n)
            n = T(n)
            if n < minimum:
                break
            if n == minimum:
                freq = Fraction(count, length)
                if not Fraction(2, 5) < freq < Fraction(5, 12):
                    found[minimum] = (length, freq)
                break
    assert found == {1: (1, 0), 2: (2, Fraction(1, 2)), 4: (5, Fraction(2, 5)),
                     44: (12, Fraction(5, 12))}


def check_65_windows():
    height = 2048
    error = Fraction(1, 4 * height)
    assert (Fraction(4, 3) * (1 - error))**65 > 2**26
    assert (Fraction(4, 3) * (1 + error))**65 < 2**27
    candidates = set()
    for n in range(1, height):
        for _ in range(65):
            candidates.add(n)
            n = Tinv(n)
    assert len(candidates) == 9569
    exceptions = {}
    for n in candidates:
        count = count_upper(n, 65)
        if count not in (26, 27):
            exceptions[n] = count
    assert exceptions == {1: 0, 2: 32, 3: 33, 62: 28, 4055: 28}

    n = 44
    counts = []
    for _ in range(12):
        counts.append(count_upper(n, 65))
        n = T(n)
    assert n == 44 and counts.count(27) == 11 and counts.count(28) == 1
    n = 4055
    for _ in range(53):
        n = T(n)
    assert n == 8
    for _ in range(12):
        n = T(n)
    assert n == 129 and count_upper(n, 65) == 26


def check_periodic_bit_word():
    n = 8
    for _ in range(106):
        n = Tinv(n)
    assert n == 2033
    bits = []
    for _ in range(183):
        bits.append(upper_bit(n))
        n = T(n)
    assert n == 16315 and sum(bits) == 76
    for bit in bits[:64]:
        assert upper_bit(n) == bit
        n = T(n)
    doubled = bits + bits
    counts = [sum(doubled[j:j+65]) for j in range(183)]
    assert [counts.count(i) for i in (26, 27, 28)] == [2, 180, 1]

    # Each cumulative count cuts out a half-open interval of initial significands.
    phase_bounds = [Fraction(1)]
    for bit in bits[:64]:
        phase_bounds.append(phase_bounds[-1] * 2**bit * Fraction(3, 4))
    assert max(phase_bounds) < 2 * min(phase_bounds)


if __name__ == "__main__":
    assert compare_frequency(8, "11", Fraction(0)) == 1
    assert compare_frequency(2, "101", Fraction(1, 2)) == -1
    assert compare_frequency(1, "11", Fraction(0)) == 0
    assert compare_frequency(8, "11", Fraction(2, 5)) == 1
    assert compare_frequency(8, "11", Fraction(5, 12)) == -1
    assert compare_frequency(44, "11", Fraction(5, 12)) == 0
    check_outer_frequencies()
    check_65_windows()
    check_periodic_bit_word()
    print("Verified the four exceptional frequency cycles and all five exceptional 65-term starts.")
