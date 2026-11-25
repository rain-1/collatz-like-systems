"""Exact finite checks for the occupation bound and bounded-merger obstruction."""

from fractions import Fraction as Q
from math import comb

from check_split5_3_range import step


def moment_checks():
    for depth in range(1, 11):
        for initial_odd in (False, True):
            total = Q(0)
            for residue in range(2**depth):
                x = 2 * residue + 1 if initial_odd else residue + 1
                y = x
                slope = Q(1)
                odd = initial_odd
                for _ in range(depth):
                    if not odd:
                        if y % 2:
                            odd = True
                        else:
                            y = step(y)
                            slope /= 2
                    elif y % 4 == 1:
                        y = step(step(step(y)))
                        slope *= Q(5, 4)
                        odd = False
                    else:
                        y = step(step(y))
                        slope /= 2
                assert 0 <= y - slope*x <= 6 * (Q(5, 4)**depth - 1)
                total += slope**2 * (Q(5, 4) if odd else 1)
            initial_weight = Q(5, 4) if initial_odd else 1
            assert total == initial_weight * Q(3, 2)**depth

    j = 48
    error_term = 24 * Q(5, 6)**j * (1 + Q(7, 10)*j)
    assert Q(9, 4) + error_term < 4 * Q(2, 3)
    assert Q(5, 6) * (1 + Q(7, 10)*(j+1)) < 1 + Q(7, 10)*j
    log_error = 72 * Q(3, 4)**48
    assert 1/(1-log_error) < Q(1000073, 1000000)


def merger_bound():
    mass = Q(1, 5)
    for h in range(1, 21):
        threshold = next(b for b in range(3*h+1, 4*h+1) if 5**b > 2**h * 4**b)
        words = 2**h * sum(comb(j + threshold + h - 2, h - 1) for j in range(7*h+1))
        mass += Q(words, 5**threshold)
    ratio = Q(72, 125)
    tail = ratio**21 / 5 * (148/(1-ratio) + 7*ratio/(1-ratio)**2)
    assert mass + tail < Q(245, 1000)


def block(x):
    if x % 2 == 0:
        return x // 2
    return (5*x+3)//4 if x % 4 == 1 else (x+3)//2


def check_example(start, depth, first_drop, dropped_value):
    y = start
    pending = []
    for _ in range(depth + 1):
        pending.append((y, depth))
        y = block(y)
    seen = {}
    while pending:
        y, remaining = pending.pop()
        assert y >= start
        if remaining == 0 or remaining <= seen.get(y, -1):
            continue
        seen[y] = remaining
        # Every inverse update at y >= start sends y+3 to at least 4(y+3)/5.
        # Before the first smaller value this gives a valid lower bound.
        if 4**remaining * (y+3) >= 5**remaining * (start+3):
            continue
        pending.append((2*y, remaining-1))
        if y % 2:
            pending.append((2*y-3, remaining-1))
        if y % 5 == 2:
            pending.append(((4*y-3)//5, remaining-1))
    x = start
    for _ in range(first_drop):
        assert x >= start
        x = block(x)
    assert x == dropped_value < start


if __name__ == "__main__":
    moment_checks()
    merger_bound()
    check_example(4**21 - 3, 20, 32, 3637978807093)
    start = 2**64 - 3
    check_example(start, 33, 53, 16940658945086006783)
    smaller = 18014398509481983997
    assert smaller < start
    for seed, blocks in ((smaller, 30), (start, 34)):
        y = seed
        for _ in range(blocks):
            y = block(y)
        assert y == (5**32 + 3)//4
    print("Occupation constants, inverse-word count and merger-depth examples verified.")
