"""The race map R (round 3, divergence lens).  Shared by check_race_s21.py.

R(n) =  6n/7   if 5|n and 7|n          (R1)
        3n/5   if 5|n and 7∤n          (R2)
        49n/6  if 5∤n and 6|n          (S1)
        5n     if 5∤n, n odd, 3|n      (S2)
        n/2    if 5∤n, n even, 3∤n     (S3)
        n      if gcd(n, 30) = 1        (S4)
"""
from fractions import Fraction


def R(n):
    if n % 5 == 0:
        return 6 * n // 7 if n % 7 == 0 else 3 * n // 5
    if n % 6 == 0:
        return 49 * n // 6
    if n % 2 and n % 3 == 0:
        return 5 * n
    if n % 2 == 0 and n % 3:
        return n // 2
    return n


def lam(r):
    """Multiplier on the class r mod 210 (R is linear on each class)."""
    n = r if r else 210
    return Fraction(R(n), n)


# (u, r, v, s): 210 q + r -> v q + s, the autolib branch format
BRANCHES = []
for r in range(210):
    l = lam(r)
    v = l * 210
    s = l * r
    assert v.denominator == 1 and s.denominator == 1
    BRANCHES.append((210, r, int(v), int(s)))


def v(n, p):
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


def divergent(n):
    """The exact divergent set D of race.md."""
    a, b, g = v(n, 2), v(n, 3), v(n, 5)
    return a < b + g


def in_C0(n):
    """Certificate C0 = {5∤n, v2<v3} u {5|n, v2<=v3}."""
    a, b = v(n, 2), v(n, 3)
    return a < b if n % 5 else a <= b


def round_point(k):
    """P_k = 2^(2^k) 3^(2^k+k+2): the orbit of 21 at the k-th exit of R2."""
    e = 2 ** k
    return 2 ** e * 3 ** (e + k + 2)
