"""Exact helpers for the downfrom5 check scripts (integer arithmetic only)."""
from math import gcd
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from systems import get, T, sigma, D  # noqa: E402,F401


def residue_graph(P, K, L):
    """Exact successor sets of the residue graph mod K for a map P that is
    affine on each residue class mod L (L = a piece modulus of P).
    For n = x + K*t, the piece is fixed by t mod L1, L1 = L/gcd(K, L); on such
    a t-class P(n) = base + step*u, so the residues hit mod K are exactly
    base + gcd(K, step)*Z."""
    L1 = L // gcd(K, L)
    succ = {}
    for x in range(K):
        x0 = x if x > 0 else K
        out = set()
        for t0 in range(L1):
            n0 = x0 + K * t0
            base = P(n0)
            step = P(n0 + K * L1) - base
            g = gcd(K, step)
            out.update(range(base % g, K, g))
        succ[x] = out
    return succ


def closure(succ, start):
    seen = {start}
    stack = [start]
    while stack:
        v = stack.pop()
        for w in succ[v]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return seen


def separates(P, L, seed, K):
    succ = residue_graph(P, K, L)
    C = closure(succ, P(seed) % K)
    return (seed % K) not in C


def is_affine_on_classes(P, L, reps=6):
    """Check P(n + L) - P(n) is constant on each class mod L (spot check of the
    piece modulus used by residue_graph) for several periods."""
    for r in range(1, L + 1):
        d = P(r + L) - P(r)
        for k in range(1, reps):
            if P(r + (k + 1) * L) - P(r + k * L) != d:
                return False
    return True


def bijective_window(P, N):
    """P injective on [1, N] and every m <= N/2 has a preimage <= 2N (spot)."""
    img = {}
    for n in range(1, 2 * N + 1):
        m = P(n)
        if m < 1 or m in img:
            return False
        img[m] = n
    return all(m in img for m in range(1, N // 2 + 1))


def first_return(P, seed, nmax):
    x = seed
    for i in range(1, nmax + 1):
        x = P(x)
        if x == seed:
            return i
    return None
