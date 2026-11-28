"""Verify whole-prefix differencing on integer paths with large excursions."""

from fractions import Fraction
from itertools import groupby, product
from math import floor, prod

from check_split5_3_link_strip import S, floors
from check_split5_3_shifted_links import closest_shift, lift


def integer(value):
    assert value.denominator == 1
    return int(value)


def outside_part(n):
    n = abs(integer(n))
    assert n
    for p in (2, 5):
        while n % p == 0:
            n //= p
    return n


def check_prefix(start, end, h, a, k_at_exit, betas, labels, q, k):
    d = 2*k + q
    gamma = Fraction(5**k, 2**d)
    m = 2**d - 5**k
    scale = 2**(d+1) * 5**a
    halves = [2*v+i for i, v in enumerate(k_at_exit, 1)]
    inverse_slopes = [Fraction(2**j, 5**v) for j, v in zip(halves, k_at_exit)]
    tau = [b*p for b, p in zip(betas, inverse_slopes)]
    assert all(t <= 3 for t in tau)
    assert start + sum(tau) == Fraction((1 << h)*end, 5**a)

    terms = []

    def add_term(value, outside_bound):
        assert outside_part(value * scale) <= outside_bound
        terms.append(value)

    def add_end(first, last, coefficient):
        core = sum(integer(2*betas[i]) * 2**(halves[i]-halves[first])
                   * 5**(k_at_exit[last]-k_at_exit[i]) for i in range(first, last+1))
        value = Fraction(core * 2**halves[first], 2*5**k_at_exit[last])
        assert value == sum(tau[first:last+1])
        add_term(coefficient * value, core)

    for label, positions in groupby(range(len(labels)), key=labels.__getitem__):
        indices = list(positions)
        p, v = indices[0], indices[-1]
        if label.startswith("ramp"):
            assert k_at_exit[p] == k_at_exit[v]
            assert betas[p:v+1] == sorted(betas[p:v+1])
            for beta, subpositions in groupby(indices, key=betas.__getitem__):
                sub = list(subpositions)
                first, last = sub[0], sub[-1]
                assert sum(tau[first:last+1]) == beta*(2*inverse_slopes[last]-inverse_slopes[first])
                for factor in (1, -gamma):
                    add_term(factor*2*tau[last], 3)
                    add_term(-factor*tau[first], 3)
        else:
            length = min(q, len(indices))
            add_end(v-length+1, v, 1)
            add_end(p, p+length-1, -gamma)
            for i in range(p, v-q+1):
                if tau[i] != gamma*tau[i+q]:
                    add_term(tau[i], 3)
                    add_term(-gamma*tau[i+q], 3)

    assert sum(terms) == (1-gamma)*sum(tau)
    leading = (1-gamma)*start
    assert abs(leading) > sum(map(abs, terms))
    assert scale*(leading + sum(terms)) == 2*m*(1 << h)*end


def check_path(length, initial):
    e = 3*length
    table = floors(e)
    a = table[e]+1
    base = [a-table[e-i] for i in range(1, e+1)]
    cumulative = base.copy()
    labels = ["rotation"]*e
    betas = [Fraction(3)] * e
    begin = 0 if initial else length-1
    stop = 2*length
    for i in range(begin, stop):
        cumulative[i] = base[stop-1]
        labels[i] = "ramp"
        betas[i] = Fraction(3, 2) if 2*i < begin+stop else Fraction(3)
    # Off the ramp use a true one-cut phase rule.
    for i in range(e):
        if labels[i] == "rotation":
            phase = Fraction(2**(e-i-1), S**table[e-i-1])
            betas[i] = Fraction(3, 2) if phase < Fraction(9, 8) else Fraction(3)

    runs = [after-before for before, after in zip([0]+cumulative, cumulative)]
    start, heights = lift(runs, betas)
    assert start.bit_length() == 2*a+e+9
    # Check full and truncated identities. Include a cut inside the large jump.
    cuts = [(e, 0), (stop-2, 0), (begin, runs[begin]//2), (min(e, stop+1), 0)]
    for seen, extra in cuts:
        expansions = (cumulative[seen-1] if seen else 0) + extra
        h = 2*expansions + seen
        end = integer((heights[seen-1] if seen else start) * S**extra)
        for limit in (1, max(2, e//12), max(2, e//5)):
            q, k = closest_shift(table, limit)
            check_prefix(start, end, h, expansions, cumulative[:seen], betas[:seen],
                         labels[:seen], q, k)


def check_multiple_rates():
    rates = [Fraction(7, 2), Fraction(11, 7), Fraction(239, 17)]
    lengths = [31, 37, 19]
    expansions = []
    betas = []
    intervals = []
    previous = 220  # Initial expansions keep every subsequent prefix above one.
    for rate, length in zip(rates, lengths):
        first = len(expansions)
        for i in range(length):
            t = Fraction(2, 5) - rate*i
            phase = t - floor(t)
            expansions.append(previous - floor(t))
            betas.append(Fraction(3, 2) if phase < Fraction(2, 3) else Fraction(3))
        intervals.append((first, first+length))
        previous = expansions[-1] + 4

    runs = [b-a for a, b in zip([0]+expansions, expansions)]
    start, heights = lift(runs, betas)
    h = [2*k+i for i, k in enumerate(expansions, 1)]
    tau = [b*Fraction(2**j, 5**k) for b, j, k in zip(betas, h, expansions)]
    assert all(t <= 3 for t in tau)
    for budget in (3, 7):
        gammas = []
        differences = []
        sum_d = 0
        for rate, (first, stop) in zip(rates, intervals):
            q = min(range(1, budget+1), key=lambda t: abs(rate*t-round(rate*t)))
            k = round(rate*q)
            d = 2*k+q
            gamma = Fraction(5**k, 2**d)
            sum_d += d
            gammas.append(gamma)
            terms = [sum(tau[stop-q:stop]), -gamma*sum(tau[first:first+q])]
            for i in range(first, stop-q):
                if tau[i] != gamma*tau[i+q]:
                    terms.extend((tau[i], -gamma*tau[i+q]))
            assert sum(terms) == (1-gamma)*sum(tau[first:stop])
            differences.append(terms)

        total_factor = prod(1-g for g in gammas)
        clearing = 2**(sum_d+1)*5**expansions[-1]
        corrections = []
        for i, terms in enumerate(differences):
            factors = [(1, -g) for j, g in enumerate(gammas) if j != i]
            for monomial in product(*factors):
                corrections.extend(prod(monomial)*t for t in terms)
        leading = total_factor*start
        assert abs(leading) > sum(map(abs, corrections))
        assert all((clearing*t).denominator == 1 for t in corrections)
        assert sum(corrections) + leading == total_factor*Fraction(
            2**h[-1]*heights[-1], 5**expansions[-1])
        assert integer(clearing*(leading+sum(corrections))) % 2**h[-1] == 0


if __name__ == "__main__":
    for length in (7, 19, 47, 83):
        for initial in (False, True):
            check_path(length, initial)
    check_multiple_rates()
    print("Multiple-rate products and full and truncated identities verified for large initial and internal jumps, "
          "including legal exit-type changes on ramps.")
