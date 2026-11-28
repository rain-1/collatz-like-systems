"""The integer counterpart of Theorem F, checked exactly.

For the accelerated map x -> x/2 (x even), (3x+d)/2 (x odd) on Z, a parity word w of length L
with a odd steps acts on its 2-adic cylinder as x -> (3^a x + d*H_w)/2^L, so its periodic point
is x_w = d*H_w/(2^L - 3^a). Theorem F's mechanism (denominator a unit) needs 2^L - 3^a = +-1.
Revision after REFEREE1: the solutions with L >= 1, a >= 0 are exactly (L, a) = (1, 0), (1, 1),
(2, 1), (3, 2); this is elementary (theory sec. 5: mod 3 / mod 4 and factoring), Mihailescu
is not needed, and (1, 0) (the trivial cycle {0}) was omitted before. We check that these words
give exactly the cycles {0}, {-1}, {1, 2}, {-5, -7, -10} of 3x+1 (and their d-multiples for 3x+d),
that no other (L, a) with L <= 200 has |2^L - 3^a| = 1 (a sanity check of the elementary proof),
and that Generalisation G's exceptions are strictly larger than this set: the 3x+1 cycle
through -17 (L = 11, a = 7, 2^L - 3^a = -139) and the 3x+5 cycles with minima 187 and 347
(L = 27, a = 17, 2^L - 3^a = 5077565) have non-unit denominators.
Exits 1 on failure.
"""
import itertools, sys
from fractions import Fraction

fail = []
sols = [(L, a) for L in range(1, 201) for a in range(0, L + 1) if abs(2 ** L - 3 ** a) == 1]
if sols != [(1, 0), (1, 1), (2, 1), (3, 2)]:
    fail.append(('catalan', sols))


def T(x, d):
    return x // 2 if x % 2 == 0 else (3 * x + d) // 2


def periodic_point(word, d):
    # compose x -> (3^a x + H)/2^L
    A, H, L = Fraction(1), Fraction(0), 0
    for o in word:
        if o:
            A, H = 3 * A, 3 * H + d * 2 ** L
        L += 1
    # T^L(x) = (A x + H)/2^L
    return Fraction(H) / (2 ** L - A)


for d in (1, 5, -1):
    cycles = set()
    for (L, a) in sols:
        for word in set(itertools.permutations([1] * a + [0] * (L - a))):
            x = periodic_point(word, d)
            if x.denominator != 1:
                fail.append(('not integral', d, word))
                continue
            x = int(x)
            orb, y = [], x
            for o in word:
                if (y % 2 == 1) != bool(o):
                    fail.append(('word mismatch', d, word))
                orb.append(y)
                y = T(y, d)
            if y != x:
                fail.append(('not periodic', d, word))
            cycles.add(tuple(sorted(set(orb))))
    print(f'3x+{d}: cycles from Catalan words: {sorted(cycles)}')
    if d == 1 and sorted(cycles) != [(-10, -7, -5), (-1,), (0,), (1, 2)]:
        fail.append(('3x+1 cycles', cycles))
# non-unit-denominator cycles (exceptions of G that are not of Frobenius type)
for d, s0, Lx, ax in ((1, -17, 11, 7), (5, 187, 27, 17), (5, 347, 27, 17)):
    y, L, a = s0, 0, 0
    while True:
        a += y % 2
        y = T(y, d)
        L += 1
        if y == s0 or L > 1000:
            break
    den = 2 ** L - 3 ** a
    print(f'3x+{d}: cycle through {s0}: L = {L}, a = {a}, 2^L - 3^a = {den}')
    if (L, a) != (Lx, ax) or abs(den) == 1:
        fail.append(('G exception example', d, s0, L, a))
if fail:
    print('FAIL', fail)
    sys.exit(1)
print('integer Catalan check passed')
