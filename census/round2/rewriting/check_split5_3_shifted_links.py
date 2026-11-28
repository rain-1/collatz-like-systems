"""Check the shifted difference on integer paths, using exact arithmetic."""

from fractions import Fraction

from check_split5_3_link_strip import S, floors


def closest_shift(table, limit):
    # |log(s^k/2^q)| is minimized by minimizing max(r,1/r).
    candidates = []
    for q in range(1, limit + 1):
        for k in (table[q], table[q] + 1):
            r = S**k / 2**q
            candidates.append((max(r, 1/r), q, k))
    return min(candidates)[1:]


def lift(counts, betas):
    numerator = h = 0
    for k, beta in zip(counts, betas):
        numerator *= 5**k
        h += 2*k + 1
        numerator += int(beta * (1 << h))
    modulus = 1 << (h+8)
    y = -numerator * pow(5**sum(counts), -1, modulus) % modulus + modulus
    height = y
    heights = []
    for k, beta in zip(counts, betas):
        assert height % (4**k) == 0
        before_exit = height // (4**k) * 5**k
        if beta == 3:
            assert before_exit % 4 == 2
        else:
            assert beta == Fraction(3, 2) and before_exit % 2
        height = int(Fraction(before_exit, 2) + beta)
        heights.append(height)
    assert height % 256 == 0
    return y, heights


def check(e, mode):
    table = floors(e)
    a = table[e] + 1
    base = [a - table[e-i] for i in range(1, e+1)]
    # s^{theta_i} is an exact rational. It gives the order of the phases.
    phases = [Fraction(2**k, S**table[k]) for k in reversed(range(e))]
    offsets = [0] * e
    betas = [Fraction(3)] * e
    pieces = [0] * e
    if mode == "exit":
        betas[e//2] /= 2
        pieces = [int(i >= e//2) + int(i > e//2) for i in range(e)]
    elif mode == "move":
        for i in range(e//4, 3*e//4):
            offsets[i] = 1
        pieces = [int(i >= e//4) + int(i >= 3*e//4) for i in range(e)]
    elif mode == "arc":
        for i, phase in enumerate(phases):
            if Fraction(21, 20) <= phase < Fraction(23, 20):
                offsets[i] = 1
                betas[i] /= 2

    cumulative = [b+u for b, u in zip(base, offsets)]
    counts = [v-u for u, v in zip([0]+cumulative, cumulative)]
    start, heights = lift(counts, betas)
    assert start.bit_length() == 2*a+e+9

    for limit in (3, e//9, e//4):
        q, k = closest_shift(table, limit)
        v = [cumulative[i+q]-cumulative[i]-k for i in range(e-q)]
        z = [S**(-vi)*heights[i+q]-heights[i] for i, vi in enumerate(v)]
        g = [S**(-vi)*betas[i+q]-betas[i] for i, vi in enumerate(v)]
        assert all(z[i] == S**counts[i]*z[i-1]/2 + g[i] for i in range(1, len(z)))

        # The one floor discontinuity and at most two arc cuts can each affect
        # at most two positions per block of 'limit' away from a piece switch.
        for j in range(0, len(v), limit):
            unmatched = [i for i in range(j, min(j+limit, len(v)))
                         if pieces[i] == pieces[i+q] and (v[i] or betas[i] != betas[i+q])]
            assert len(unmatched) <= (6 if mode == "arc" else 2)

        powers = [ai-cumulative[0] for ai in cumulative[:len(z)]]
        h = [2*p+i for i, p in enumerate(powers)]
        leading = 5**powers[-1] * z[0]
        terms = [(1 << h[i]) * 5**(powers[-1]-powers[i]) * g[i]
                 for i in range(1, len(z))]
        assert leading + sum(terms) == (1 << h[-1]) * z[-1]
        assert abs(leading) > sum(map(abs, terms))

        denominator = 2 * 20**max(map(abs, v))
        assert all((denominator*t).denominator == 1 for t in z + g)
        grouped_total = 0
        i = 1
        while i < len(z):
            j = i
            if pieces[i] != pieces[i+q]:
                while j+1 < len(z) and pieces[j+1] != pieces[j+1+q]:
                    j += 1
            inner = sum((1 << (h[t]-h[i])) * 5**(powers[j]-powers[t])
                        * int(denominator*g[t]) for t in range(i, j+1))
            grouped_total += (1 << h[i]) * 5**(powers[-1]-powers[j]) * inner
            i = j+1
        assert denominator*leading + grouped_total == (1 << h[-1]) * denominator*z[-1]


if __name__ == "__main__":
    for e in (31, 63, 97, 150, 241):
        for mode in ("max", "exit", "move", "arc"):
            check(e, mode)
    print("Integer lifts, phase exceptions, affine differences, and leading-term "
          "dominance verified for all four families at five sizes.")
