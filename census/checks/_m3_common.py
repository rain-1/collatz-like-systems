"""Shared exact-integer helpers for the m3_* checks."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from systems import get


def seed_fate(f, seed, max_steps=10**6):
    seen = {}
    x, t = seed, 0
    while x not in seen and t < max_steps:
        seen[x] = t
        x = f(x)
        t += 1
    if x not in seen:
        return None
    mu = seen[x]
    lam = t - mu
    cyc = []
    y = x
    for _ in range(lam):
        cyc.append(y)
        y = f(y)
    return mu, lam, cyc


def affine_iter(f, m, r, steps):
    """Return (a, b) with f^steps(m*k + r) = a*k + b for all k >= 0,
    verified by checking a branch-constancy condition: the residues used at each
    step depend only on r because the composed affine maps keep the modulus.
    We derive a,b from k=0,1 and confirm on many k (the maps are affine on the
    class, so exact agreement on the class follows once branch choice is fixed;
    branch choice is fixed when each intermediate coefficient is divisible by 3)."""
    b = r
    a = m
    for _ in range(steps):
        # current value a*k + b; branch determined by b mod 3 provided 3 | a
        assert a % 3 == 0, "branch not determined"
        v0 = f(b)
        v1 = f(a + b)
        a, b = v1 - v0, v0
    return a, b


def descent_exceptions(f, plan):
    """plan: list of (r, steps) covering residues mod 3. For each class n=3k+r,
    f^steps(n) = a*k+b with a < 3; returns list of n in the class with
    f^steps(n) >= n (finite since a < 3), and asserts a < 3."""
    exc = []
    for r, steps in plan:
        a, b = affine_iter(f, 3, r, steps)
        assert a < 3, (r, a, b)
        # a*k + b >= 3k + r  <=>  k <= (b - r)/(3 - a)
        kmax = (b - r) // (3 - a) if b >= r else -1
        for k in range(0, kmax + 1):
            n = 3 * k + r
            if n >= 1:
                exc.append(n)
        # spot-check the affine formula
        for k in range(0, 2000):
            x = 3 * k + r
            for _ in range(steps):
                x = f(x)
            assert x == a * k + b
    return sorted(exc)


def all_below_reach(f, N, targets, max_steps=10**5):
    for n in range(1, N):
        x = n
        for _ in range(max_steps):
            if x in targets:
                break
            x = f(x)
        else:
            return n
    return None


def expanding_run(f, branch_c, j):
    """n = 3^j - 1: check the accelerated map stays on the n=2 mod 3 branch
    j-1 times (value 4^i*3^(j-i)-1 style growth), i.e. -1 is a 3-adic fixed
    point of the expanding branch. Returns the number of consecutive
    non-divisible accelerated steps observed."""
    n = 3 ** j - 1
    x, cnt = n, 0
    while x % 3 == 2:
        y = f(x)
        if y % 3 == 0:
            y = f(y)
        x = y
        cnt += 1
    return cnt
