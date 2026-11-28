"""Verify four escaping seed-8 orbits and account for the many-to-one box."""

from collections import Counter
from itertools import combinations, product
from math import gcd

from systems import shiftT


SLOPES = (2, 4, 4)  # numerators, in input residue order
CASES = {
    (3, 11, 7): (13, 11),
    (6, 8, 4): (8, 7),
    (9, 5, 1): (11, 7),
    (12, 2, -2): (8, 4),
}


def step(constants, n):
    r = n % 3
    quotient, remainder = divmod(SLOPES[r] * n + constants[r], 3)
    assert remainder == 0
    return quotient


def branch_images_overlap(constants):
    # On each positive input progression the image is first + slope * k, k >= 0.
    # Two such progressions intersect iff their starts agree modulo the gcd.
    starts = [step(constants, n) for n in (3, 1, 2)]
    return any(
        (starts[r] - starts[s]) % gcd(SLOPES[r], SLOPES[s]) == 0
        for r, s in combinations(range(3), 2)
    )


def verify_escape():
    chain = (2, 3, 4, 5, 7, 9, 8, 11)
    assert all(shiftT(n) == m for n, m in zip(chain, chain[1:]))
    assert [shiftT(n) for n in (3, 1, 2)] == [4, 1, 3]
    reference = (12, 2, -2)
    for constants, (entry, coordinate) in CASES.items():
        t = constants[0] // 3
        assert constants == (3 * t, 14 - 3 * t, 10 - 3 * t)
        shift = 3 * (4 - t)
        # Each side is affine on each input class modulo 3. Two values
        # on each class determine both its constant and its slope.
        for n in range(1, 7):
            assert step(reference, n + shift) == step(constants, n) + shift
            assert step(reference, 2 * n) == 2 * shiftT(n)
            assert step(constants, n) % 2 == t % 2
        assert step(constants, 1) == step(constants, 2)
        assert entry == (8 if t % 2 == 0 else step(constants, 8))
        assert entry + shift == 2 * coordinate and coordinate in chain


def census():
    counts = Counter()
    for constants in product(range(-6, 13, 3), range(-7, 12, 3), range(-8, 12, 3)):
        if min(step(constants, n) for n in (1, 2, 3)) < 1:
            continue
        if not branch_images_overlap(constants):
            continue
        n = 8
        seen = set()
        for _ in range(256):
            seen.add(n)
            n = step(constants, n)
            if n in seen:
                assert constants not in CASES
                counts["returns" if n == 8 else "enters cycle"] += 1
                break
        else:
            counts["proved escape" if constants in CASES else "unresolved here"] += 1
    assert counts == {"returns": 13, "enters cycle": 100, "proved escape": 4,
                      "unresolved here": 42}
    return dict(counts)


if __name__ == "__main__":
    verify_escape()
    print("Four affine reductions and the common escaping orbit verified.")
    print(census())
