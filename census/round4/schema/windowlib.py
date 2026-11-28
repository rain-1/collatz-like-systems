"""windowlib.py -- window approximants (window.md, Theorems W1-W4).

For a unit-multiplier table (modulus p^m, table[r] = (u, v, p^e)) and a level K >= m,
the WINDOW of a residue r mod p^K is the sequence of steps i = 0, 1, ... taken by the
integers of the class r + p^K Z while the number D_i of divisions made before step i
satisfies D_i <= K - m.  These steps are the same for every integer of the class.

R_K(delta) = { r mod p^K : U_w(r) > p^((1-delta) D_w(r)) }, where U_w is the product of
the u's and D_w the total division exponent of the window.  (Haar-typical windows have
U_w << p^{D_w}; R_K is a large-deviation set.)

The window approximant T_K agrees with T off R_K and is the reset n -> floor(n/p^K)+1 on
R_K.  Exact integer arithmetic throughout.
"""
from fractions import Fraction
import math


def window(p, m, table, K, r):
    """(list of e's, U, D) of the window of the class r mod p^K."""
    Q = p ** m
    x = r  # representative; the window steps depend only on r mod p^K
    D, U, es = 0, 1, []
    while D <= K - m:
        u, v, w = table[x % Q]
        e = 0
        while w % p == 0:
            w //= p
            e += 1
        es.append(e)
        U *= u
        D += e
        x = (u * x + v) // (p ** e)
        if e == 0 and len(es) > 10 ** 6:
            raise RuntimeError("division-free loop")
    return es, U, D


def in_R(U, D, p, delta):
    """U > p^((1-delta) D), delta a Fraction in (0,1): exact via integer powers."""
    a, b = delta.numerator, delta.denominator
    # U^b > p^((b-a) D)
    return U ** b > p ** ((b - a) * D)


def approximant(p, m, table, K, delta):
    """(Q, table_K, R) for the window approximant T_K."""
    Q = p ** K
    tab, R = [], []
    for r in range(Q):
        es, U, D = window(p, m, table, K, r)
        if in_R(U, D, p, delta):
            R.append(r)
            tab.append((1, (Q - r) % Q, Q) if r else (1, 0, Q))
        else:
            tab.append(table[r % (p ** m)])
    return Q, tab, R


# ---------------------------------------------------------------- 3x+1 specifics

def parity_window(r, N):
    """first N parity bits of the accelerated 3x+1 map started at the integer r."""
    bits, x = [], r
    for _ in range(N):
        b = x & 1
        bits.append(b)
        x = (3 * x + 1) >> 1 if b else x >> 1
    return bits


def collatz_R(N, num=5, den=8):
    """R_N = residues mod 2^N whose N-window has more than (num/den) N odd steps."""
    return [r for r in range(2 ** N) if den * sum(parity_window(r, N)) > num * N]


def collatz_TN(N, num=5, den=8):
    Q = 2 ** N
    Rset = set(collatz_R(N, num, den))
    tab = []
    for r in range(Q):
        if r in Rset:
            tab.append((1, (Q - r) % Q, Q) if r else (1, 0, Q))
        else:
            tab.append((1, 0, 2) if r % 2 == 0 else (3, 1, 2))
    return Q, tab, Rset


def schema_weights(N, gamma, num=5, den=8, M=Fraction(1, 2)):
    """The explicit potential of Theorem W2: for r not in R_N,
         c(r) = max_{0 <= s <= N-1} gamma^s * prod_{i<s} q(b_i(r)),  q(1) = 3/2, q(0) = 1/2,
    and c(r) = M on R_N."""
    Q = 2 ** N
    c = []
    for r in range(Q):
        b = parity_window(r, N)
        if den * sum(b) > num * N:
            c.append(M)
            continue
        best, P = Fraction(1), Fraction(1)
        for s in range(1, N):
            P *= gamma * (Fraction(3, 2) if b[s - 1] else Fraction(1, 2))
            best = max(best, P)
        c.append(best)
    return c
