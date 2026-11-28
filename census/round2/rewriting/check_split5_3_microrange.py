"""Check the halving-clock Haar counts and continuation sets for split5_3."""

from collections import Counter
from fractions import Fraction
from itertools import product


def haar_counts(limit):
    # In a fresh state the modulus is 2^h. If evenness is known it is 2^(h+1).
    fresh, even, arriving = Counter({0: 1}), Counter(), Counter()
    in_transit = 0
    minimum = 0
    power = 1
    for h in range(limit + 1):
        while power < 1 << h:
            power *= 5
            minimum += 1
        live_f = Counter({a: w for a, w in fresh.items() if a >= minimum})
        live_e = Counter({a: w for a, w in even.items() if a >= minimum})
        endings = sum(live_f.values()) + sum(live_e.values())
        yield 2 * sum(live_f.values()) + sum(live_e.values()) + in_transit
        both = live_f + live_e
        fresh, even, arriving = arriving + live_f, both, Counter({a+1: w for a, w in both.items()})
        in_transit = endings


def raw_passes(n, b):
    a = h = 0
    while h < b:
        if n % 2 == 0:
            n //= 2
            h += 1
        elif n % 4 == 1:
            n = 5*n + 3
            a += 1
        else:
            n += 3
        if 5**a < 1 << h:
            return False
    return True


def code(y, length, flag=0):
    a = 0
    states = []
    for _ in range(length):
        if y % 2:
            y = (y+3)//2
        else:
            a += flag
            y = (5 if flag else 1)*y//2
            flag ^= 1
        states.append((a, flag, y))
    return states


def check_residues():
    for b, total in enumerate(haar_counts(13)):
        modulus = 1 << (b+1)
        count = 0
        for y in range(modulus):
            states = code(y, b+1)
            passes = all(5**a >= 1 << (i-s) for i, (a, s, _) in enumerate(states, 1) if i-s <= b)
            assert passes == raw_passes(y+modulus*4-3, b)
            count += passes
        assert count == total
    # Test both entry flags and partially sampled residue classes.
    for h, k in product(range(1, 7), range(1, 7)):
        for r in range(1 << h):
            prefix = code(r, h)
            a, s, intercept = prefix[-1]
            if any(5**e < 1 << (i-f) for i, (e, f, _) in enumerate(prefix, 1)):
                continue
            for t in range(3, (1 << k)+3):
                y = r + (t << h)
                assert code(y,h)[-1] == (a, s, 5**a*t+intercept)
                continuation = code((5**a*t+intercept) % (1 << k), k, s)
                predicted = all(5**(a+e) >= 1 << (h+i-f) for i, (e, f, _) in
                                enumerate(continuation, 1) if i < k or f == 1)
                assert predicted == raw_passes(y-3, h+k-1)


if __name__ == "__main__":
    check_residues()
    sizes = (8,12,16,20,24,28,32,100,500,1000,2000)
    depths = {(12*m+4)//5: m for m in sizes}
    for b, count in enumerate(haar_counts(max(depths))):
        if b in depths:
            m = depths[b]
            prediction = Fraction(count << m, 1 << (b+1))
            print(f"m={m:4}, b={b:4}, predicted count {float(prediction):.8g}")
