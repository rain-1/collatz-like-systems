"""Check the negative-multiple basin automaton against the original integer map."""
from fractions import Fraction
from random import Random

from qrlib import famB

STEP = famB(7, 5, 3)
TRANSITIONS = ((0, 1), (2, 0), (3, 0), (2, 2))


def accepts(index, state=0):
    while index:
        state = TRANSITIONS[state][index % 2]
        index //= 2
    return state == 0


def reaches_zero(index):
    n = -7 * index
    while n < 0:
        n = STEP(n)
    assert n in (0, 7, 14)
    return n == 0


def verify():
    assert STEP(0) == 0 and STEP(7) == 14 and STEP(14) == 7
    for index in range(1 << 17):
        assert accepts(index) == reaches_zero(index)
    rng = Random(7)
    for _ in range(1000):
        index = rng.getrandbits(512)
        assert accepts(index) == reaches_zero(index)

    # Distinguishing continuations t=1,2 also supply two of the block profiles.
    profiles = [[int(accepts(t, state)) for state in range(4)] for t in range(3)]
    assert len(set(zip(profiles[1], profiles[2]))) == 4
    weight = (4, 2, 2, 1)
    incoming = [0] * 4
    for source, row in enumerate(TRANSITIONS):
        for target in row:
            incoming[target] += weight[source]
    assert incoming == [2 * w for w in weight]
    limits = [Fraction(sum(w*b for w, b in zip(weight, row)), 9) for row in profiles]
    assert limits[0] == Fraction(4, 9) and sum(limits)/3 == Fraction(11, 27)
    print("Verified orbit labels, four distinguishable states, and both cutoff limits.")


if __name__ == "__main__":
    verify()
