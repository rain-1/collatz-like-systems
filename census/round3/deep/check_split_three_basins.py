"""Check the positive basin theorem against raw iteration and inverse constructions."""

from collections import Counter
from functools import lru_cache
from math import comb

from basins_lib import all_cycles, orbit_classes, sigma_step, sigma_table


def split_parameter(d):
    exponent = 0
    while d % 3 == 0:
        exponent += 1
        d //= 3
    return exponent, d


@lru_cache(maxsize=None)
def raw_minimum(d, start):
    step = sigma_step(d)
    seen = set()
    n = start
    while n not in seen:
        seen.add(n)
        n = step(n)
    cycle = [n]
    n = step(n)
    while n != cycle[0]:
        cycle.append(n)
        n = step(n)
    return min(cycle)


def predicted_minima(d):
    a, u = split_parameter(d)
    minima = {3**a * n for n in all_cycles(sigma_step(u), u)}
    visited = set()
    for seed in range(1, d + 1):
        if seed in visited or seed % 3**a == 0:
            continue
        cycle = []
        n = seed
        while n not in visited:
            visited.add(n)
            cycle.append(n)
            n = (2 * n - 1) % d + 1
        if all((n + d) % 4 == 0 for n in cycle if n % 2):
            minima.add(min(cycle))
    return minima


def binary_decision(d, n, labels, class_cycles):
    """Return a cycle minimum, or the tuple of candidates in a shared terminal class."""
    _, u = split_parameter(d)
    parameter, carry, unread = d, 0, n
    while unread and parameter != u:
        bit = unread % 2
        unread //= 2
        v = bit + carry
        if v % 2 == 0:
            carry = v // 2
        else:
            v += 2 * (unread % 2)
            unread //= 2
            if (v + parameter) % 4 == 0:
                carry = (v + parameter) // 4
            else:
                parameter //= 3
                assert (v + parameter) % 4 == 0
                carry = (v + parameter) // 4
        assert 0 <= carry <= d + 1
    if parameter == u:
        candidates = tuple(sorted((d // u) * c for c in class_cycles[labels[n % u]]))
        return candidates[0] if len(candidates) == 1 else candidates
    return (d // parameter) * raw_minimum(parameter, carry)


def inverse_check(d, j, endpoint, bits):
    """Grow backwards, then identify each start by the raw forward map."""
    initial_parameter = d // 3**j
    expected_min = 3**j * raw_minimum(initial_parameter, endpoint)
    stack = [(endpoint, initial_parameter, bits, j)]
    found = set()
    while stack:
        x, parameter, left, marks = stack.pop()
        if left == 0:
            if marks == 0:
                assert parameter == d and x not in found
                assert raw_minimum(d, x) == expected_min
                found.add(x)
            continue
        stack.append((2 * x, parameter, left - 1, marks))
        if left >= 2:
            stack.append((4 * x - parameter, parameter, left - 2, marks))
            if marks:
                stack.append((4 * x - parameter, 3 * parameter, left - 2, marks - 1))
    # Choose the number of length-two tiles, their positions, then mark j of them.
    expected = sum(comb(bits - k, k) * comb(k, j) for k in range(j, bits // 2 + 1))
    assert len(found) == expected


def main():
    checked = Counter()
    for d in sorted(set(range(3, 151, 6)) | {243, 729}):
        a, u = split_parameter(d)
        expected = set(all_cycles(sigma_step(d), d))
        assert expected == predicted_minima(d)
        if u == 1:
            assert expected == {d, d // 3}
        _, _, _, classes = sigma_table(u)
        labels, _ = orbit_classes(u, [2, 3])
        for n in range(1, 4097):
            actual = raw_minimum(d, n)
            result = binary_decision(d, n, labels, classes)
            if isinstance(result, tuple):
                assert actual in result
                assert all(c % 3**a == 0 for c in result)
                checked['shared class'] += 1
            else:
                assert result == actual
                checked['cycle label'] += 1
    for a in range(1, 5):
        d = 3**a
        for bits in range(0, 15):
            # A power of two is in the small basin at parameter 3.
            inverse_check(d, a - 1, 1 << d.bit_length(), bits)
    print('Raw iteration comparisons:', dict(checked))
    print('Cycle lists agree for 27 shifts; inverse counts agree for 60 parameter/length pairs.')


if __name__ == '__main__':
    main()
