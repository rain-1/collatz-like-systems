"""Generic strict descent certificates on Z for residue-class affine maps.

A map is (Q, table): n = r (mod Q) -> (u n + v) / w, u, w > 0, exact division
on the whole class (w | u*Q and w | u*r + v).  Q is arbitrary (mixed primes
allowed).  A *strict Z-certificate* is a finite partition of Z into classes
n = L t + r (0 <= r < L) with step counts j and exact affine forms
T^j(L t + r) = P t + R valid for ALL t in Z, with 0 < P < L.  Then
|T^j(n)| < |n| except for finitely many n (Theorem Z, see theorem_Z.md).
All arithmetic is exact.
"""
from math import gcd


def step_fn(Q, table):
    def T(n):
        u, v, w = table[n % Q]
        x = u * n + v
        assert x % w == 0, (n, Q)
        return x // w
    return T


def check_table(Q, table):
    for r in range(Q):
        u, v, w = table[r]
        assert u > 0 and w > 0
        assert (u * Q) % w == 0 and (u * r + v) % w == 0, r


def certificate(Q, table, maxL=10 ** 40, maxnodes=500000):
    """Search: node (L, r, P, R, j) means n = L t + r maps to P t + R after j
    steps for every integer t.  Close at the first j >= 1 with P < L.  If the
    branch of P t + R is not constant in t (mod Q) or the division is not
    exact for all t, split t -> Q t' + s."""
    check_table(Q, table)
    leaves, stack, nodes = [], [(1, 0, 1, 0, 0)], 0
    while stack:
        L, r, P, R, j = stack.pop()
        nodes += 1
        if nodes > maxnodes:
            return dict(ok=False, open=(L, r, j), reason='nodes')
        if j > 0 and P < L:
            leaves.append((L, r, j, P, R))
            continue
        g = gcd(P, Q)
        rows = {table[(R + g * i) % Q] for i in range(Q // g)}
        u, v, w = next(iter(rows))
        if len(rows) == 1 and (u * P) % w == 0 and (u * R + v) % w == 0:
            stack.append((L, r, u * P // w, (u * R + v) // w, j + 1))
        else:
            if L * Q > maxL:
                return dict(ok=False, open=(L, r, j), reason='depth')
            for s in range(Q):
                stack.append((L * Q, r + s * L, Q * P, R + s * P, j))
    return dict(ok=True, leaves=leaves, k=max(l[2] for l in leaves),
                Lmax=max(l[0] for l in leaves), size=len(leaves))


def verify(Q, table, leaves, ts=(0, 1, 2, 7, -1, -2, -7, 10 ** 15 + 3, -(10 ** 15) - 7)):
    """Independent check: (a) the classes partition Z (sum 1/L = 1 and no class
    contains another); (b) 0 < P < L; (c) the affine form equals the true
    iterate at several t of both signs.  Since T^j restricted to a class on
    which every intermediate branch is constant is affine in t, agreement on
    two values already pins the form; we test nine."""
    from fractions import Fraction
    T = step_fn(Q, table)
    assert sum(Fraction(1, L) for L, *_ in leaves) == 1
    cls = sorted((L, r) for L, r, *_ in leaves)
    for i, (L, r) in enumerate(cls):
        for L2, r2 in cls[:i]:
            if L % L2 == 0:
                assert r % L2 != r2, ((L, r), (L2, r2))
            if L2 % L == 0:
                assert r2 % L != r, ((L, r), (L2, r2))
    for L, r, j, P, R in leaves:
        assert 0 < P < L
        for t in ts:
            x = L * t + r
            for _ in range(j):
                x = T(x)
            assert x == P * t + R, (L, r, j, t)
    return True


def exceptional_Z(leaves):
    """Integers n with |T^j(n)| >= |n| in their leaf.  Such n = L t + r need
    (L - P)|t| <= |R| + |r|; each candidate t is tested exactly."""
    E = set()
    for L, r, j, P, R in leaves:
        B = (abs(R) + abs(r)) // (L - P)
        for t in range(-B - 1, B + 2):
            if abs(P * t + R) >= abs(L * t + r):
                E.add(L * t + r)
    return sorted(E)


def cycles_from(T, starts, cap=10 ** 7):
    cycles = set()
    for e in starts:
        seen, x = set(), e
        while x not in seen:
            seen.add(x)
            x = T(x)
            assert len(seen) < cap
        c, y = [x], T(x)
        while y != x:
            c.append(y)
            y = T(y)
        k = c.index(min(c))
        cycles.add(tuple(c[k:] + c[:k]))
    return sorted(cycles, key=lambda c: (min(c), len(c)))


def settle_Z(Q, table, **kw):
    c = certificate(Q, table, **kw)
    if not c['ok']:
        return c
    verify(Q, table, c['leaves'])
    E = exceptional_Z(c['leaves'])
    T = step_fn(Q, table)
    c['E'] = E
    c['cycles'] = cycles_from(T, E)
    return c
