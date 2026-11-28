"""Exact checks of the extremal split5_3 links and their integer cylinders."""

from fractions import Fraction
from itertools import combinations_with_replacement, product

S = Fraction(5, 4)


def floors(limit):
    """floor(k * log(2)/log(5/4)), calculated by integer comparison."""
    a = 0
    table = []
    for k in range(limit + 1):
        while 5**(a + 1) <= 1 << (2 * (a + 1) + k):
            a += 1
        table.append(a)
    return table


def check_lift(counts, doubled_constants, correction):
    a = h = c = 0
    for k, twice_beta in zip(counts, doubled_constants):
        c *= 5**k
        a += k
        h += 2 * k
        c += twice_beta << h
        h += 1
    modulus = 1 << (h + 8)
    start = -c * pow(5**a, -1, modulus) % modulus + modulus
    assert start % 256 == 0
    height = start
    for k, twice_beta in zip(counts, doubled_constants):
        for _ in range(k):
            assert height % 4 == 0
            height = 5 * height // 4
        if twice_beta == 3:
            assert height % 2
        else:
            assert twice_beta == 6 and height % 4 == 2
        height = (height + twice_beta) // 2
    assert height % 256 == 0
    assert (height << h) == 5**a * start + c
    assert Fraction(c, 1 << h) == correction


def exhaustive(e, a, lower, upper):
    r = S**a / 2**e
    observed_min = observed_max = None
    for prefix in combinations_with_replacement(range(a + 1), e - 1):
        slopes = [S**k / (1 << j) for j, k in enumerate(prefix, 1)]
        if any(p <= r for p in slopes):
            continue
        for betas in product((Fraction(3, 2), 3), repeat=e):
            correction = sum(b * r / p for b, p in zip(betas, slopes + [r]))
            if observed_min is None or correction < observed_min:
                observed_min = correction
            if observed_max is None or correction > observed_max:
                observed_max = correction
    assert (observed_min, observed_max) == (lower, upper)


if __name__ == "__main__":
    table = floors(150)
    widths = []
    upper = 0
    for e in range(1, len(table)):
        a = table[e] + 1
        cumulative = [0] + [a - table[e-j] for j in range(1, e+1)]
        runs = [v - u for u, v in zip(cumulative, cumulative[1:])]
        upper += 3 * S**table[e-1] / 2**(e-1)
        lower = 3 * (1 - Fraction(1, 2**e))
        check_lift(runs, [6] * e, upper)
        check_lift([a] + [0] * (e-1), [3] * e, lower)
        if e <= 4:
            exhaustive(e, a, lower, upper)
        widths.append(upper - lower)
        for d in range(1, min(18, e)):
            patterns = {tuple(runs[j:j+d]) for j in range(1, e-d+1)}
            assert len(patterns) <= d+1
            assert all(sum(p) in (table[d], table[d]+1) for p in patterns)
    assert all(v > u for u, v in zip(widths, widths[1:]))
    assert 255 < widths[95] < 256 and 258 < widths[96] < 259
    print("Both integer lifts through 150 exits, extrema through four exits, "
          "and run-word counts verified. First width at least 256: 97 exits.")
