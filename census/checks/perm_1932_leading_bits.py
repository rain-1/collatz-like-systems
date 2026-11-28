"""Exact finite certificate for the four leading bits of the 1932 permutation."""

from fractions import Fraction

from _perm_common import T, Tinv


WINDOW = 17
SMALL = 1024
DIGITS = set(range(8, 16))
SMALL_CYCLES = ((1,), (2, 3), (4, 5, 7, 9, 6))
CHAIN = (38, 51, 34, 45, 30, 20, 27, 18, 12, 8)


def missing(start, length):
    seen = set()
    n = start
    for _ in range(length):
        seen.add((8 * n) >> (n.bit_length() - 1))
        n = T(n)
    return DIGITS - seen


def check_large_values():
    # Normalize 1/3^j into [1, 2) by multiplying by a power of two.
    denominators = [3**j for j in range(WINDOW)]
    points = sorted(Fraction(1 << (d - 1).bit_length(), d) for d in denominators)
    successors = points[1:] + [2 * points[0]]
    gap = max(y / x for x, y in zip(points, successors))
    assert gap == Fraction(256, 243)

    distortion = Fraction(201, 200)
    step_error = Fraction(1, 4 * SMALL)
    assert (1 - step_error) ** (WINDOW - 1) >= 1 / distortion
    assert (1 + step_error) ** (WINDOW - 1) <= distortion
    assert gap * distortion**2 < Fraction(16, 15)


def check_small_values():
    candidates = set()
    for value in range(1, SMALL):
        n = value
        for _ in range(WINDOW):
            candidates.add(n)
            predecessor = Tinv(n)
            assert T(predecessor) == n
            n = predecessor
    assert len(candidates) == 2339

    expected = {n: {14} for n in CHAIN[:7]}
    small = set()
    for cycle in SMALL_CYCLES:
        assert all(T(x) == y for x, y in zip(cycle, cycle[1:] + cycle[:1]))
        omitted = missing(cycle[0], len(cycle))
        assert omitted
        for n in cycle:
            expected[n] = omitted
            small.add(n)
    assert all(T(x) == y for x, y in zip(CHAIN, CHAIN[1:]))
    assert not (small & set(CHAIN))
    actual = {}
    for n in candidates:
        omitted = missing(n, WINDOW)
        if omitted:
            actual[n] = omitted
    assert actual == expected
    assert all(not missing(n, 24) for n in actual.keys() - small)
    assert missing(38, 23) == {14}


if __name__ == "__main__":
    check_large_values()
    check_small_values()
    print("Verified the rotation bound, all 2339 candidates, and the sharp 24-term bound.")
