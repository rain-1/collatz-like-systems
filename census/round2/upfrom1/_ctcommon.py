"""Shared helpers for the Collatz-with-trapdoors checks (exact integer arithmetic)."""
import itertools
from systems import T, parity_word


def affine(word):
    """x_L = (a*x + b) / 2^L for an orbit with the given parity word."""
    a, b = 1, 0
    for i, p in enumerate(word):
        if p:
            a, b = 3 * a, 3 * b + 2 ** i
    return a, b


def residue_has_word(r, mod, L):
    """parity word of length L (L <= log2 mod) is the same for r, r+mod, r+2mod, ..."""
    w = parity_word(r + mod, L)
    return all(parity_word(r + k * mod, L) == w for k in range(2, 40)), w


def untrapped_fate(step, trapped, n, limit=10**7):
    """Run until trapped ('D') or a cycle is closed; return ('D',) or ('C', min of cycle)."""
    seen = {}
    i = 0
    while n not in seen:
        if trapped(n):
            return ("D",)
        seen[n] = i
        n = step(n)
        i += 1
        if i > limit:
            return ("?",)
    cyc = [x for x, j in seen.items() if j >= seen[n]]
    return ("C", min(cyc))
