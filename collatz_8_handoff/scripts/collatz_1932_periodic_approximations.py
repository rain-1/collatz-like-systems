#!/usr/bin/env python3
"""Construct exact positive *rational* cycles approximating both sides of
Collatz's original 1932 permutation orbit of 8.

The extension of G to rationals with denominators coprime to 3 is defined
by the same branch formulas, choosing the residue r in Z/3Z.

This demonstrates that finite modular itinerary information cannot on its
own distinguish 8 from positive rational periodic points. It does NOT
prove that the orbit of the integer 8 is infinite.
"""
from fractions import Fraction
import argparse

BRANCHES = ((2, 0), (4, -1), (4, 1))


def forward_integer(n):
    q, r = divmod(n, 3)
    return (2*q, 4*q+1, 4*q+3)[r]


def backward_integer(n):
    if n % 2 == 0:
        return 3*n//2
    if n % 4 == 1:
        return (3*n + 1)//4
    return (3*n - 1)//4


def forward_residues(n, k):
    result = []
    for _ in range(k):
        result.append(n % 3)
        n = forward_integer(n)
    return result


def backward_residues(n, l):
    result = []
    for _ in range(l):
        n = backward_integer(n)
        result.append(n % 3)
    return list(reversed(result))


def coefficients(word):
    """Return Q, D=3^length, S with F_word(x)=(Q*x+S)/D."""
    Q, D, S = 1, 1, 0
    for r in word:
        q, s = BRANCHES[r]
        S = q*S + s*D
        Q *= q
        D *= 3
    return Q, D, S


def periodic_point(word):
    Q, D, S = coefficients(word)
    if Q == D:
        raise ValueError('Degenerate affine fixed point')
    return Fraction(S, D-Q)


def residue3(x):
    assert x.denominator % 3
    return (x.numerator * pow(x.denominator, -1, 3)) % 3


def validate_cycle(word, x):
    assert x.denominator % 6 in (1, 5)
    y = x
    minimum = y
    for r in word:
        assert y > 0
        assert residue3(y) == r
        minimum = min(minimum, y)
        q, s = BRANCHES[r]
        y = (q*y+s)/3
    assert y == x
    return minimum


def construct_closing_cycle(forward_length, backward_length, minimum_start=8):
    W = forward_residues(8, forward_length)
    V = backward_residues(8, backward_length)
    # For each t, append 0^t 2^s between W and V. Choose s maximal
    # subject to the full affine slope being <1. As t grows, the fixed
    # point tends to +infinity and every intermediate rational is >0.
    Qwv, Dwv, _ = coefficients(W + V)
    t = 0
    while True:
        t += 1
        # The slope is (Qwv/Dwv)*(2/3)^t*(4/3)^s.
        num = Qwv * 2**t
        den = Dwv * 3**t
        if num >= den:
            continue
        s = 0
        while 4*num < 3*den:
            num *= 4
            den *= 3
            s += 1
        word = W + [0]*t + [2]*s + V
        x = periodic_point(word)
        if x <= minimum_start:
            continue
        try:
            smallest = validate_cycle(word, x)
        except AssertionError:
            continue
        e = sum(1 if r == 0 else 2 for r in V)
        assert (x.numerator - 8*x.denominator) % (3**forward_length) == 0
        assert (x.numerator - 8*x.denominator) % (2**e) == 0
        return dict(x=x, word=word, t=t, s=s, minimum=smallest,
                    forward_length=forward_length,
                    backward_length=backward_length, two_adic_bits=e)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('-k', '--forward-length', type=int, default=6)
    p.add_argument('-l', '--backward-length', type=int, default=4)
    a = p.parse_args()
    assert a.forward_length > 0 and a.backward_length > 0
    result = construct_closing_cycle(a.forward_length, a.backward_length)
    x = result['x']
    print('Cyclic residue word:', ''.join(map(str, result['word'])))
    print('Period:', len(result['word']))
    print('Initial rational:', x)
    print('Difference from 8:', x-8)
    print('Smallest value in the rational cycle:', result['minimum'])
    print('x is congruent to 8 modulo 3^%d and 2^%d' %
          (a.forward_length, result['two_adic_bits']))
    print('All iterates positive; exact return and residues verified.')
    print('This is NOT a periodic orbit of the integer 8.')

if __name__ == '__main__':
    main()
