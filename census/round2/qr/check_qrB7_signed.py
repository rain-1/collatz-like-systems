"""Classify signed qrB7_c53 starts given on the command line, or verify the theorem."""
import argparse
from collections import Counter
from random import Random

from qrlib import basin, basin_table, cycles_in, famB


# State (a, j) denotes the function t -> L(a*(t+j) + a-1).
START = (1, 0)
STATES = [(1, j) for j in range(13)] + [(2, j) for j in range(7)]
# Cycle minima for the arguments -1, 0, ..., 13, in that order.
TERMINAL = (5, 0, 1, 1, 3, 1, 5, 3, 7, 1, 1, 5, 1, 3, 3)
WEIGHTS = (0, 282, 282, 312, 252, 186, 438, 292, 212, 114,
           258, 264, 174, 141, 297, 219, 365, 163, 261, 87)


def transition(state, bit):
    a, j = state
    h, e = divmod(j + bit, 2)
    if a == 1:
        return (1 + e, h)
    return (1, h + (6 if e else 9))


def argument(state, t):
    a, j = state
    return a * (t + j) + a - 1


def cycle_minimum(n):
    state = START
    while n not in (0, -1):
        n, bit = divmod(n, 2)
        state = transition(state, bit)
    return TERMINAL[argument(state, n) + 1]


def reachable(initial):
    seen = {initial}
    pending = [initial]
    while pending:
        state = pending.pop()
        for bit in (0, 1):
            target = transition(state, bit)
            if target not in seen:
                seen.add(target)
                pending.append(target)
    return seen


def verify():
    step = famB(7, 5, 3)
    box = range(36)
    assert all(step(n) in box for n in box)
    cycles = cycles_in(step, box)
    ordered = []
    for cycle in cycles:
        i = cycle.index(min(cycle))
        ordered.append(tuple(cycle[i:] + cycle[:i]))
    assert sorted(ordered) == [(0,), (1, 18, 9, 22, 11, 16, 8, 4, 2),
                               (3, 12, 6), (5, 20, 10), (7, 14)]
    labels = basin_table(step, cycles)
    assert tuple(basin(step, labels, n) for n in range(-1, 14)) == TERMINAL
    assert reachable(START) == set(STATES)
    signatures = {tuple(basin(step, labels, argument(s, t)) for t in range(1, 6))
                  for s in STATES}
    assert len(signatures) == 20
    for n in range(-2**17, 2**17 + 1):
        assert cycle_minimum(n) == basin(step, labels, n)
    rng = Random(7)
    for size in (128, 512, 2048):
        for _ in range(100):
            n = rng.getrandbits(size)
            for x in (n, -n):
                assert cycle_minimum(x) == basin(step, labels, x)

    recurrent = set(STATES) - {START}
    assert all(reachable(s) == recurrent for s in recurrent)
    assert transition((1, 1), 1) == (1, 1)
    incoming = Counter()
    for state, weight in zip(STATES, WEIGHTS):
        for bit in (0, 1):
            incoming[transition(state, bit)] += weight
    assert sum(WEIGHTS) == 4599
    assert [incoming[s] for s in STATES] == [2*w for w in WEIGHTS]
    expected = {0: (0, 1971, 1308, 663, 657), 4: (0, 1971, 990, 981, 657),
                -1: (282, 1971, 763, 1208, 375), -3: (312, 1971, 715, 1256, 345)}
    for t, row in expected.items():
        mass = Counter()
        for s, w in zip(STATES, WEIGHTS):
            mass[basin(step, labels, argument(s, t))] += w
        assert tuple(mass[c] for c in (0, 1, 3, 5, 7)) == row
    print("Verified five cycles, the minimal signed classifier, and all four density witnesses.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("starts", type=int, nargs="*")
    starts = parser.parse_args().starts
    if starts:
        for n in starts:
            print(f"{n} -> cycle with minimum {cycle_minimum(n)}")
    else:
        verify()
