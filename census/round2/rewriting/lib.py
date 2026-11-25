"""Shared exact machinery for census/round2/rewriting.

All arithmetic is on Python integers / Fractions. Nothing here uses floats in a
decision.

Systems are generalized Collatz maps given by a modulus M and a table
table[r] = (u, v, w): n = r (mod M) -> (u*n + v) / w (exact division).
"""
from fractions import Fraction
import sys

sys.setrecursionlimit(10000)


def mod_table(M, table):
    def step(n):
        u, v, w = table[n % M]
        x = u * n + v
        assert x % w == 0
        return x // w
    return step


def div_else_table(primes, a, d):
    """2|n -> n/2 else 3|n -> n/3 ... else a*n+d, as a mod-(prod primes) table."""
    M = 1
    for p in primes:
        M *= p
    tab = []
    for r in range(M):
        for p in primes:
            if r % p == 0:
                tab.append((1, 0, p))
                break
        else:
            tab.append((a, d, 1))
    return M, tab


# ---------------------------------------------------------------- systems
SPLIT5_1 = (4, [(1, 0, 2), (5, 1, 1), (1, 0, 2), (1, 1, 1)])
SPLIT5_3 = (4, [(1, 0, 2), (5, 3, 1), (1, 0, 2), (1, 3, 1)])
M3_B = (3, [(1, 0, 3), (4, -1, 3), (4, 1, 3)])
M3_D = (3, [(1, 0, 3), (4, 2, 1), (4, 1, 1)])
M3_G = (3, [(1, 0, 3), (5, 1, 1), (5, 2, 1)])
DIV23_5N1 = div_else_table([2, 3], 5, 1)
DIV235_7N1 = div_else_table([2, 3, 5], 7, 1)
DIV23_7N1 = div_else_table([2, 3], 7, 1)


def descends(step, n, cap):
    """True if some iterate T^k(n), 1<=k<=cap, is < n."""
    x = n
    for _ in range(cap):
        x = step(x)
        if x < n:
            return True
    return False


def descent_tree(system, max_mod, max_steps=10**9, small_cap=100000):
    """Coefficient-stopping-time tree.

    Explores classes n = Q*t + r (t >= 0) with the exact affine image A*t + B
    after s steps. A class is CLOSED when A < Q; then T^s(n) < n for all
    t > t0 = (B - r) / (Q - A), and the finitely many n with t <= t0 are
    checked directly (they are recorded in `small`).
    A class is OPEN (exceptional) when Q would exceed max_mod.

    Returns (open_classes, closed_count, small_failures) where open_classes is
    a list of (Q, r) and small_failures lists the n (from closed classes with
    small t) whose orbit does not go below n within small_cap steps.
    """
    M, tab = system
    step = mod_table(M, tab)
    open_classes = []
    small_fail = []
    closed = 0
    # stack items: (Q, r, A, B, s)
    stack = [(1, 0, 1, 0, 0)]
    while stack:
        Q, r, A, B, s = stack.pop()
        # can we read the image mod M?
        g = M // _gcd(A, M)
        if g > 1:
            if Q * g > max_mod:
                open_classes.append((Q, r))
                continue
            for i in range(g):
                # t = g*t' + i
                stack.append((Q * g, r + Q * i, A * g, B + A * i, s))
            continue
        res = B % M
        u, v, w = tab[res]
        A2, B2 = u * A, u * B + v
        assert A2 % w == 0 and B2 % w == 0
        A2 //= w
        B2 //= w
        s += 1
        if A2 < Q:
            closed += 1
            # T^s(n) < n  iff  (Q - A2) t > B2 - r
            num = B2 - r
            den = Q - A2
            t = 0
            while den * t <= num:
                n = Q * t + r
                if n >= 1 and not descends(step, n, small_cap):
                    small_fail.append(n)
                t += 1
            continue
        if s >= max_steps:
            open_classes.append((Q, r))
            continue
        stack.append((Q, r, A2, B2, s))
    return open_classes, closed, small_fail


def density(open_classes):
    return sum((Fraction(1, Q) for Q, _ in open_classes), Fraction(0))


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return abs(a)


def in_open(open_classes, n):
    return any(n % Q == r for Q, r in open_classes)


# ------------------------------------------------------------ partial theorem
def orbit_cycle_min(step, n, cap=10**6):
    """Return min of the cycle reached from n (exact Floyd-free dict walk)."""
    seen = {}
    x = n
    for i in range(cap):
        if x in seen:
            c, y = [x], step(x)
            while y != x:
                c.append(y)
                y = step(y)
            return min(c), len(c)
        seen[x] = i
        x = step(x)
    return None


def check_partial(name, system, modulus, exp_count, exp_density, exp_small,
                  cycles, runs):
    """Re-derive the exceptional set E at `modulus` and compare with the
    recorded certificate.  `cycles` maps cycle minimum -> cycle length; every
    small exception must lie on one of these cycles.  `runs` is a list of
    (p_adic_start_fn, length) witnesses that E is nonempty at every depth."""
    M, tab = system
    step = mod_table(M, tab)
    o, closed, small = descent_tree(system, modulus, small_cap=100000)
    dens = density(o)
    assert len(o) == exp_count, (len(o), exp_count)
    assert dens == exp_density, (dens, exp_density)
    assert sorted(set(small)) == sorted(exp_small), sorted(set(small))
    for n in set(small):
        cm = orbit_cycle_min(step, n)
        assert cm is not None and cm[0] in cycles and cycles[cm[0]] == cm[1], (n, cm)
        # n itself is periodic
        x = step(n)
        for _ in range(cm[1] - 1):
            x = step(x)
        assert x == n, n
    for c, L in cycles.items():
        x = c
        for _ in range(L):
            x = step(x)
        assert x == c
    # every listed cycle minimum must be exceptional (it cannot descend)
    for c in cycles:
        assert in_open(o, c) or c in small, c
    return o, closed, dens
