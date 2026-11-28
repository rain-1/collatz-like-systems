#!/usr/bin/env python3
"""evidence_window.py -- EVIDENCE only (not a proof): the quantitative statement (S_C) of
window.md.  For each start n, A(n) is the largest N such that some window of N
consecutive steps of the orbit of n (followed into its final cycle) has more than
(5/8) N expanding steps:

  3x+1 (accelerated): expanding step = odd step (multiplier 3/2);
  K7 (z-coordinates): measured per division as in windowlib (window = steps while the
    division count stays <= N - 2), R_N(1/5) membership tested directly.

(S_C) says A(n) <= C log2(n) for all n >= 2.  We print max A(n)/log2(n) over ranges and
the maximising n.
"""
import sys, math
import numpy as np
from fractions import Fraction


def collatz_parities(n):
    bits, x, seen = [], n, 0
    while x != 1:
        bits.append(x & 1)
        x = (3 * x + 1) >> 1 if x & 1 else x >> 1
    L = len(bits)
    bits += [1, 0] * (2 * L + 8)        # the cycle (1 2), long enough to cover any window
    return np.array(bits, dtype=np.int64), L


def A_collatz(n):
    b, L = collatz_parities(n)
    cs = np.concatenate([[0], np.cumsum(b)])
    best = 0
    # a window that has > 5N/8 ones must start before the cycle is reached (the cycle alone
    # gives at most ceil(N/2)), and its length is at most 4(L + 2)
    for N in range(1, 4 * L + 9):
        if N > len(b):
            break
        starts = np.arange(0, min(L + 1, len(b) - N + 1))
        ones = cs[starts + N] - cs[starts]
        if (8 * ones > 5 * N).any():
            best = N
    return best


def main():
    hi = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    worst = (0, None)
    for n in range(2, hi + 1):
        a = A_collatz(n)
        r = a / math.log2(n)
        if r > worst[0]:
            worst = (r, n, a)
    print(f"3x+1, n <= {hi}: max A(n)/log2 n = {worst[0]:.3f} at n = {worst[1]} (A = {worst[2]})")
    for n in (27, 703, 10971, 77671, 837799, 8400511, 63728127, 670617279):
        a = A_collatz(n)
        print(f"   n = {n}: A(n) = {a}, A/log2 n = {a / math.log2(n):.3f}")


if __name__ == "__main__":
    main()
