#!/usr/bin/env python3
"""Integrality bound on cycle length (Theorem C of cycles.md), exact.

Let a cycle of a unit table map have X divisions by p and Y steps with
multiplier a (all other steps have multiplier 1), and suppose every element of
the cycle exceeds Z0 and X <= Z0 / c'.  Theorem C shows

        1 < p^X / a^Y <= 1 + c X / Z0,

so X is the least integer with p^X > a^Y.  This script finds, exactly, the least
Y >= 1 for which the integer inequality

        Z0 * (p^X - a^Y) >= c * X * a^Y      (X = least with p^X > a^Y)

FAILS.  For every smaller Y it holds, which excludes that Y.

usage: python3 cycle_bound.py Z0 [p a c Ymax]     (defaults p=2 a=3 c=2)
prints: (Y_fail, X_fail)
"""
import sys


def first_failure(Z0, p=2, a=3, c=2, Ymax=10 ** 7):
    X, PX, PY = 0, 1, 1          # PX = p^X, PY = a^Y
    for Y in range(1, Ymax + 1):
        PY *= a
        while PX <= PY:
            PX *= p
            X += 1
        if Z0 * (PX - PY) < c * X * PY:
            return Y, X
    return None


if __name__ == "__main__":
    Z0 = int(sys.argv[1])
    p, a, c = (int(x) for x in sys.argv[2:5]) if len(sys.argv) > 4 else (2, 3, 2)
    Ymax = int(sys.argv[5]) if len(sys.argv) > 5 else 10 ** 6
    print(first_failure(Z0, p, a, c, Ymax))
