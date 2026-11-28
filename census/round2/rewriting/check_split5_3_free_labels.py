"""Check the free-label binary and five-adic codes and the complementary sums."""

from collections import Counter
from fractions import Fraction
from itertools import combinations, product

from check_split5_3_link_strip import S, floors
from check_split5_3_shifted_links import lift


def schedule(e):
    table = floors(e)
    a = table[e] + 1
    cumulative = [0] + [a-table[e-i] for i in range(1, e+1)]
    halves = [2*k+i for i, k in enumerate(cumulative)]
    runs = [v-u for u, v in zip(cumulative, cumulative[1:])]
    slopes = [Fraction(5**k, 2**h) for k, h in zip(cumulative, halves)]
    return cumulative, halves, runs, slopes


def path(bits, runs, slopes):
    betas = [Fraction(3*(1+bit), 2) for bit in bits]
    y, ends = lift(runs, betas)
    heights = [y] + ends
    for i in range(len(bits), 0, -1):
        residue = 2*heights[i] % 5
        assert residue in (1, 3)
        bit = int(residue == 1)
        assert bit == bits[i-1]
        numerator = 2*heights[i] - 3*(1+bit)
        k = runs[i-1]
        assert numerator % 5**k == 0
        assert 4**k * (numerator // 5**k) == heights[i-1]
    assert y + sum(b/p for b, p in zip(betas, slopes[1:])) == heights[-1]/slopes[-1]
    return heights, betas


def check_full_family(e):
    ks, h, runs, slopes = schedule(e)
    words = list(product((0, 1), repeat=e))
    values = [path(bits, runs, slopes)[0] for bits in words]
    for j, k in combinations(range(len(words)), 2):
        a, b = words[j], words[k]
        first = next(i for i in range(e) if a[i] != b[i])
        delta = abs(values[j][0]-values[k][0])
        assert (delta & -delta) == 1 << (h[first+1]-1)
        # A matching interval contributes an exact binary factor at its start
        # and a five-adic factor at its end, even when other labels differ.
        low = 0
        for high in range(1, e+1):
            if a[high-1] != b[high-1]:
                low = high
                continue
            du = values[j][low] - values[k][low]
            dv = values[j][high] - values[k][high]
            assert du and dv
            assert dv * 2**(h[high]-h[low]) == du * 5**(ks[high]-ks[low])


def check_folding(q, record):
    ks, h, runs, slopes = schedule(2*q)
    shifts = [ks[i+q]-ks[i] for i in range(q+1)]
    k, majority = Counter(shifts[1:]).most_common(1)[0]
    assert 2*majority >= q
    if record:
        # Find the nearest integer to kappa*q by real multiplicative distance.
        k = min(set(shifts[1:]) | {floors(q)[q], floors(q)[q]+1},
                key=lambda a: max(S**a/2**q, 2**q/S**a))
        assert sum(a != k for a in shifts[1:]) <= 2
    v = [a-k for a in shifts]
    free = [i for i in range(q) if record or v[i+1] == 0]
    if len(free) <= 9:
        assignments = product((0, 1), repeat=len(free))
    else:
        assignments = [([0, 1] * len(free))[:len(free)], [1]*len(free)]
    for assignment in assignments:
        first = [0] * q
        for i, bit in zip(free, assignment):
            first[i] = bit
        bits = first + [1-bit for bit in first]
        heights, betas = path(bits, runs, slopes)
        w = [heights[i] + S**(-v[i])*heights[i+q] for i in range(q+1)]
        corrections = [betas[i-1] + S**(-v[i])*betas[i+q-1] for i in range(1, q+1)]
        assert all(c == Fraction(9, 2) for i, c in enumerate(corrections, 1) if v[i] == 0)
        assert all(w[i] == slopes[i]/slopes[i-1]*w[i-1]+corrections[i-1] for i in range(1, q+1))
        assert w[0]+sum(c/p for c, p in zip(corrections, slopes[1:])) == w[-1]/slopes[q]


if __name__ == "__main__":
    check_full_family(7)
    table = floors(48)
    minimum = None
    for q in range(1, 49):
        distance = min(max(S**k/2**q, 2**q/S**k) for k in (table[q], table[q]+1))
        record = minimum is None or distance < minimum
        if record:
            minimum = distance
        check_folding(q, record=False)
        if record:
            check_folding(q, record=True)
    print("All seven-exit word pairs decoded; two-half sums and record exceptions checked through q=48.")
