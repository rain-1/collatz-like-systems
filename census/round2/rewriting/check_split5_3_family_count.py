"""Check the free-label residue measures, Fourier factors and phase intervals."""

from fractions import Fraction
from itertools import product

from check_split5_3_link_strip import S, floors
from check_split5_3_shifted_links import lift


def rotation_lists(d, extra=0):
    table = floors(d)
    # s^{frac(kappa*j)} preserves the order of the cuts, including equality.
    cuts = [Fraction(2**j, S**table[j]) for j in range(1, d+1)]
    ordered = sorted([Fraction(1)] + cuts)
    for phase, upper in zip(ordered, ordered[1:]+[S]):
        cumulative = [0] + [table[j]+(cut > phase)+extra for j, cut in enumerate(cuts, 1)]
        yield phase, upper, tuple(b-a for a, b in zip(cumulative, cumulative[1:]))


def duration(runs):
    return 2*sum(runs) + len(runs)


def offsets(runs, terminal):
    """Starting residue offsets before reduction, as rationals with odd denominator."""
    halvings = expansions = 0
    weights = []
    for run in runs:
        expansions += run
        halvings += 2*run + 1
        weights.append(Fraction(3 << (halvings-1), 5**expansions))
    for labels in product((1, 2), repeat=len(runs)):
        r = -sum((a*b for a, b in zip(weights, labels)), Fraction(0))
        yield r
        if terminal and labels[-1] == 1:
            yield r + Fraction(1 << halvings, 5**expansions)


def residue(x, modulus):
    return x.numerator * pow(x.denominator, -1, modulus) % modulus


def follows(y, runs):
    for k in runs:
        if y % 4**k:
            return False
        pre = y // 4**k * 5**k
        if pre % 4 == 0:
            return False
        y = (pre + (3 if pre % 2 else 6)) // 2
    return True


def check_period(runs):
    q = 1 << (duration(runs)+1)
    coded = {residue(x, q) for x in offsets(runs, terminal=True)}
    assert len(coded) == 3 * 2**(len(runs)-1)
    direct = {r for r in range(q) if follows(r+q, runs)}
    assert coded == direct


def check_factors(runs):
    # 2013265921 = 15*2^27+1, with primitive root 31.
    prime = 2013265921
    modulus = 1 << (duration(runs)+1)
    assert (prime-1) % modulus == 0
    root = pow(31, (prime-1)//modulus, prime)
    assert pow(root, modulus//2, prime) == prime-1
    h1, middle, tail = runs[:1], runs[1:-1], runs[-1:]
    scale1 = Fraction(1 << duration(h1), 5**sum(h1))
    scale2 = Fraction(1 << duration(h1+middle), 5**sum(h1+middle))

    def transform(block, terminal, scale, xi):
        return sum(pow(root, xi*residue(scale*x, modulus), prime)
                   for x in offsets(block, terminal)) % prime

    for xi in (1, 2, 5, 10, 32):
        full = transform(runs, True, 1, xi)
        split = (transform(h1, False, 1, xi)*transform(middle, False, scale1, xi)
                 * transform(tail, True, scale2, xi)) % prime
        assert full == split


def check_cells(e, d):
    table = floors(e)
    ks = [0] + [table[e]+1-table[e-i] for i in range(1, e+1)]
    runs = tuple(v-u for u, v in zip(ks, ks[1:]))
    r = S**ks[-1] / 2**e
    cells = list(rotation_lists(d))
    assert len({w for _, _, w in cells}) == d+1
    for labels in ([3]*e, [6]*e, [3, 6]*(e//2)):
        start, heights = lift(runs, [Fraction(x, 2) for x in labels])
        for i in range(1, e-d+1):
            phase = Fraction(2**(e-i), S**table[e-i])
            lower, upper, word = next(cell for cell in cells if cell[0] <= phase < cell[1])
            assert word == runs[i:i+d]
            assert r*start*lower <= heights[i-1] < r*start*upper + 5*e


if __name__ == "__main__":
    for extra in (0, 1):
        for d in (1, 2, 3):
            for _, _, word in rotation_lists(d, extra):
                if duration(word) < 20:
                    check_period(word)
                if d == 3:
                    check_factors(word)
    for d in (1, 4, 9, 19):
        check_cells(40, d)
    print("Verified legal residue sets on full periods, Fourier products in a prime "
          "field, and phase intervals on integer trajectories.")
