"""Shared exact-integer helpers for the permutation-family checks."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from systems import get  # noqa: E402


def T(n):            # Collatz 1932 permutation, written independently of systems.py
    q, r = divmod(n, 3)
    return (2 * q, 4 * q + 1, 4 * q + 3)[r]


def Tinv(n):
    q, r = divmod(n, 4)
    if r % 2 == 0:
        return 3 * (n // 2)
    return 3 * q + 1 if r == 1 else 3 * q + 2


def S(n):            # perm_swap, written independently
    q, r = divmod(n, 3)
    return (2 * q, 4 * q + 3, 4 * q + 1)[r]


def Sinv(n):
    q, r = divmod(n, 4)
    if r % 2 == 0:
        return 3 * (n // 2)
    return 3 * q + 2 if r == 1 else 3 * q + 1


def B(n):            # perm_b
    q, r = divmod(n, 3)
    return (4 * q, 4 * q + 2, 2 * q + 1)[r]


def D(n):            # perm_d
    if n % 2 == 0:
        return 5 * (n // 2)
    q, r = divmod(n, 8)
    return 5 * q + (r + 1) // 2


def Dinv(n):
    q, r = divmod(n, 5)
    return 2 * q if r == 0 else 8 * q + 2 * r - 1


def agrees(f, g, N):
    return all(f(n) == g(n) for n in range(1, N + 1))


def is_mutual_inverse(f, g, N):
    """f(g(n)) = n and g(f(n)) = n on 1..N, and both stay positive."""
    for n in range(1, N + 1):
        a, b = f(n), g(n)
        if a < 1 or b < 1 or g(a) != n or f(b) != n:
            return False
    return True


def cycle_of(f, seed, limit):
    x, k = f(seed), 1
    orb = [seed]
    while x != seed:
        if k >= limit:
            return None
        orb.append(x)
        x, k = f(x), k + 1
    return orb


def no_return(f, seed, steps):
    x = seed
    for _ in range(steps):
        x = f(x)
        if x == seed:
            return False, x
    return True, x


def has_periodic_separator(f, branch_mod, seed, M):
    """Is there a union C of residue classes mod M with f(C) in C (on positives),
    f(seed) in C, seed not in C?  Smallest candidate: forward closure of f(seed) mod M
    in the residue graph r -> f(r + M t) mod M, t = 0..branch_mod-1 (f's branch depends
    on n mod branch_mod, and its affine pieces are exact on those classes)."""
    def succ(r):
        out = set()
        base = r if r > 0 else M
        for t in range(branch_mod):
            out.add(f(base + M * t) % M)
        return out
    start = f(seed) % M
    seen, stack = {start}, [start]
    while stack:
        r = stack.pop()
        for s in succ(r):
            if s not in seen:
                seen.add(s)
                stack.append(s)
    return (seed % M) not in seen
