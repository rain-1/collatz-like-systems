#!/usr/bin/env python3
"""Exact induced odd-state map for Collatz's 1932 permutation.

This reformulates the unsolved orbit of 8; it does NOT prove infinitude.
"""

def G(n):
    assert n > 0
    q, r = divmod(n, 3)
    return (2*q, 4*q+1, 4*q+3)[r]

def valuation(n, p):
    t = 0
    while n % p == 0:
        n //= p
        t += 1
    return t

def H(x):
    """First return to an odd integer; x must be positive and odd."""
    assert x > 0 and x % 2 == 1
    t = valuation(x, 3)
    u = x // 3**t
    y = (2**t)*u
    eps = +1 if y % 3 == 2 else -1
    z = (4*y + eps)//3
    assert z % 2 == 1
    return z, t

def H_inverse(y):
    """Inverse of H on positive odd integers."""
    assert y > 0 and y % 2 == 1
    z = (3*y + (1 if y%4==1 else -1))//4
    t = valuation(z, 2)
    x = 3**t*(z//2**t)
    assert H(x)[0] == y
    return x

def verify_blocks(x, number_of_blocks):
    total_zeros = 0
    for _ in range(number_of_blocks):
        y, t = H(x)
        seq = [x]
        for _ in range(t):
            seq.append(G(seq[-1]))
        assert G(seq[-1]) == y
        assert [valuation(n,2) for n in seq] == list(reversed([valuation(n,3) for n in seq]))
        assert H_inverse(y) == x
        total_zeros += t
        x = y
    return x, total_zeros

if __name__ == '__main__':
    assert G(8) == 11
    for odd in range(1, 1000, 2):
        assert H(H_inverse(odd))[0] == odd
        assert H_inverse(H(odd)[0]) == odd
    for N in (100, 1000, 10000):
        x, zeros = verify_blocks(11,N)
        print(f'{N:,} odd-return steps: {zeros:,} zero-branch steps, '
              f'average v3={zeros/N:.6f}, '
              f'G zero-branch fraction={zeros/(zeros+N):.6f}, '
              f'final value has {x.bit_length()} bits')
    print('Identity: G-orbit of 8 closes iff H-orbit of 11 closes.')
    print('No assertion of infinitude.')
