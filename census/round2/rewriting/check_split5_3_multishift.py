"""Exact checks for periodic runs, several shifted heights and the coding example."""

from fractions import Fraction
from itertools import combinations, groupby, product
from random import Random

from check_split5_3_free_labels import path, schedule
from check_split5_3_link_strip import S, floors


def check_shifts(p, table):
    ks, _, runs, slopes = schedule(6*p)
    k = min((table[p], table[p]+1),
            key=lambda a: max(S**a/2**p, 2**p/S**a))
    shifts = (0, p, 2*p)
    nearest = (0, k, 2*k)
    patterns = product(range(3), repeat=p) if p <= 3 else [[i % 3 for i in range(p)]]
    for chosen in patterns:
        bits = [int(chosen[i] == block % 3) for block in range(6) for i in range(p)]
        heights, betas = path(bits, runs, slopes)
        v = [[ks[i+q]-ks[i]-a for q, a in zip(shifts, nearest)] for i in range(4*p+1)]
        assert sum(any(row) for row in v[1:]) <= 20
        for coefficients in ((1, 1, 1), (1, -2, 1)):
            weights = [[c*S**(-b) for c, b in zip(coefficients, row)] for row in v]
            w = [sum(u*heights[i+q] for u, q in zip(row, shifts))
                 for i, row in enumerate(weights)]
            g = [sum(u*betas[i+q-1] for u, q in zip(weights[i], shifts))
                 for i in range(1, 4*p+1)]
            assert all(w[i] == slopes[i]/slopes[i-1]*w[i-1]+g[i-1]
                       for i in range(1, 4*p+1))
            assert w[0]+sum(x/s for x, s in zip(g, slopes[1:])) == w[-1]/slopes[4*p]
            if coefficients == (1, 1, 1):
                assert all(x == 6 for row, x in zip(v[1:], g) if not any(row))


def check_repetitions(e):
    ks, _, _, _ = schedule(e)
    table = floors(e)
    # Exact s^theta instead of a floating-point rotation.
    phases = [Fraction(2**(e-i), S**table[e-i]) for i in range(e+1)]
    found = 0
    for p in range(1, e//4):
        k = table[p]
        for j in range(1, e-2*p):
            laps = min(5, (e-j-p+1)//p)
            if laps < 2:
                continue
            positions = range(j, j+p)
            if all(ks[t+laps*p]-ks[t] == laps*k for t in positions):
                power = (Fraction(2**p, S**k))**laps
                assert min(phases[t] for t in positions) >= power
                found += 1
    assert found


def mul(a, b):
    """Multiply in GF(64) modulo X^6 + X + 1."""
    result = 0
    while b:
        if b & 1:
            result ^= a
        b >>= 1
        a <<= 1
        if a & 64:
            a ^= 67
    return result


def check_code():
    e, b = 60, 6
    _, h, _, _ = schedule(e)
    m = 5*h[-1]//12
    k = max(i for i in range(e//b+1) if h[i*b] <= m)
    inverses = {a: next(c for c in range(1, 64) if mul(a, c) == 1) for a in range(1, 64)}

    def encode(coefficients):
        bits = [(a >> j) & 1 for a in coefficients for j in range(b)]
        y = 2**m + sum(bit << (h[i+1]-1) for i, bit in enumerate(bits))
        word = []
        for x in range(e//b):
            value = 0
            for j, a in enumerate(coefficients):
                term = a
                for u in range(j):
                    term = mul(term, mul(x ^ u, inverses[j ^ u]))
                value ^= term
            word.extend((value >> j) & 1 for j in range(b))
        return y, word

    rng = Random(517)
    samples = {tuple(rng.randrange(64) for _ in range(k)) for _ in range(48)}
    samples.update(tuple(a if j == t else 0 for j in range(k))
                   for t in range(k) for a in (0, 1, 32))
    for (a, (y, word)), (b_coeff, (z, other)) in combinations([(a, encode(a)) for a in samples], 2):
        assert 2**m <= min(y, z) <= max(y, z) < 2**(m+1)
        first = next(i for i, pair in enumerate(zip(word, other), 1) if pair[0] != pair[1])
        gap = abs(y-z)
        assert (gap & -gap) == 1 << (h[first]-1)
        degree = max(i for i, pair in enumerate(zip(a, b_coeff)) if pair[0] != pair[1])
        assert sum(word[j:j+b] == other[j:j+b] for j in range(0, e, b)) <= degree
        agreed = sorted((sum(1 for _ in group) for key, group in
                         groupby(x == u for x, u in zip(word, other)) if key), reverse=True)
        for intervals in (1, 2, 3):
            assert sum(agreed[:intervals]) <= b*(degree+2*intervals+1)
        assert 127*gap >= 126*(1 << (h[b*degree+1]-1))


if __name__ == "__main__":
    table = floors(85)
    best = None
    for p in range(1, len(table)):
        error = min(max(S**k/2**p, 2**p/S**k) for k in (table[p], table[p]+1))
        if best is None or error < best:
            best = error
            check_shifts(p, table)
    check_repetitions(155)
    check_code()
    print("Verified multi-shift recurrences, rotation gaps for repeated runs, "
          "and the binary Newton code.")
