"""Library for round 6, lens cutoff_wide.

A *table system* is (p, m, table) with table[r] = (u, v, w), meaning
n = r (mod p^m) -> (u n + v)/w, w = p^e, p not dividing u, and u a power of one
other prime l (the numerator prime).  Every step is exact on its class.

Everything here is exact (Python ints and Fractions) unless a function name
ends in _float.
"""
from fractions import Fraction as F
from math import log, gcd
import itertools


# ---------------------------------------------------------------- systems
def terras(a, b):
    """(a n + b)/2 on odd n, n/2 on even n.  p = 2."""
    return dict(p=2, m=1, table=[(1, 0, 2), (a, b, 2)])


def s_family(m, S):
    """even -> n/2; odd -> 3n+1 if n mod 2^m in S else n+1."""
    t = []
    for r in range(2 ** m):
        if r % 2 == 0:
            t.append((1, 0, 2))
        elif r in S:
            t.append((3, 1, 1))
        else:
            t.append((1, 1, 1))
    return dict(p=2, m=m, table=t)


SYSTEMS = {
    # name: (system dict, numerator prime l, expanding cycle seed x*, note)
    '3x+1': (terras(3, 1), 3, -1, 'Terras form (3n+1)/2'),
    '3x-1': (terras(3, -1), 3, 1, 'control: extra cycles'),
    '3x+5': (terras(3, 5), 3, -5, 'control: extra cycles'),
    '5x+1': (terras(5, 1), 5, F(-1, 3), 'control: divergence expected'),
    'K7': (s_family(3, {7}), 3, -1, 'core S={7}'),
    'core13': (s_family(3, {1, 3}), 3, -5, 'core S={1,3} mod 8'),
    'core135': (s_family(3, {1, 3, 5}), 3, -5, 'core S={1,3,5} mod 8'),
    'core57': (s_family(3, {5, 7}), 3, -1, 'core S={5,7}'),
    'core157': (s_family(3, {1, 5, 7}), 3, -1, 'core S={1,5,7}'),
    'core357': (s_family(3, {3, 5, 7}), 3, -1, 'core S={3,5,7}'),
    'core17': (s_family(3, {1, 7}), 3, -1, 'core S={1,7}'),
    'coreW': (s_family(3, {1, 3, 7}), 3, -1, 'core W, S={1,3,7}'),
    'split5_3': (dict(p=2, m=2, table=[(1, 0, 2), (5, 3, 1), (1, 0, 2), (1, 3, 1)]),
                 5, -3, 'CLS-049'),
    'split5_1': (dict(p=2, m=2, table=[(1, 0, 2), (5, 1, 1), (1, 0, 2), (1, 1, 1)]),
                 5, None, 'CLS-048'),
    'm3_b': (dict(p=3, m=1, table=[(1, 0, 3), (4, -1, 3), (4, 1, 3)]), 2, 1,
             'CLS-004 (p = 3, l = 2)'),
}


def step(sysd, n):
    p, m, t = sysd['p'], sysd['m'], sysd['table']
    u, v, w = t[n % p ** m]
    x = u * n + v
    assert x % w == 0
    return x // w


def step_q(sysd, x):
    """Step on a p-adic-integral rational x (denominator prime to p)."""
    p, m, t = sysd['p'], sysd['m'], sysd['table']
    r = padic_res(x, p ** m)
    u, v, w = t[r]
    return (u * x + v) / w if isinstance(x, F) else F(u * x + v, w)


def padic_res(x, M):
    x = F(x)
    assert x.denominator % gcd(x.denominator, M) == x.denominator or gcd(x.denominator, M) == 1
    return (x.numerator * pow(x.denominator, -1, M)) % M


def vexp(n, q):
    """exponent of prime q in integer n > 0."""
    k = 0
    while n % q == 0:
        n //= q
        k += 1
    return k, n


# ---------------------------------------------------------- cylinder graph
def graph(sysd, K):
    """Cylinder graph G_K.  Edge (r, s, u, v, e).  Nodes residues mod p^K."""
    p, m, t = sysd['p'], sysd['m'], sysd['table']
    assert K >= m
    M = p ** K
    E = {}
    for r in range(M):
        u, v, w = t[r % p ** m]
        e, one = vexp(w, p)
        assert one == 1
        base = (u * r + v)
        assert base % w == 0
        base //= w
        # targets: (u (r + M j) + v)/w mod p^K for j = 0..p^e - 1
        outs = []
        for j in range(p ** e):
            s = ((u * (r + M * j) + v) // w) % M
            outs.append((s, u, v, e))
        E[r] = outs
    return E


def walk_affine(sysd, walk):
    """walk = list of nodes r_0, ..., r_L (mod p^K) given as steps; returns the
    composed affine map n -> (A n + B)/D as (A, B, D) with D = p^(divisions)."""
    p, m, t = sysd['p'], sysd['m'], sysd['table']
    A, B, D = 1, 0, 1
    for r in walk:
        u, v, w = t[r % p ** m]
        A, B, D = u * A, u * B + v * D, D * w
    return A, B, D


def follow_class(sysd, walk, K):
    """Set of integers n whose first len(walk) iterates lie in the given nodes
    (mod p^K) and whose next iterate is in node walk_end (if given).  Returns
    (rho, Mod) with the set = rho + Mod Z, or None if empty.  Exact, uses CRT
    step by step (Markov property: never None for a walk of G_K)."""
    p = sysd['p']
    PK = p ** K
    rho, Mod = walk[0] % PK, PK
    A, B, D = 1, 0, 1
    t, m = sysd['table'], sysd['m']
    for idx in range(1, len(walk)):
        r = walk[idx - 1]
        u, v, w = t[r % p ** m]
        A, B, D = u * A, u * B + v * D, D * w
        # need (A n + B)/D == walk[idx] mod p^K, with n = rho + Mod*z
        # (A rho + B) + A Mod z == D*target mod D*p^K
        target = walk[idx] % PK
        big = D * PK
        lhs0 = (A * rho + B)
        # solve A*Mod*z == D*target - lhs0 (mod big)
        rhs = (D * target - lhs0) % big
        g = gcd(A * Mod, big)
        if rhs % g:
            return None
        a2, r2, b2 = (A * Mod) // g, rhs // g, big // g
        z0 = (r2 * pow(a2, -1, b2)) % b2 if b2 > 1 else 0
        rho = rho + Mod * z0
        Mod = Mod * b2
        rho %= Mod
    return rho, Mod


def slope(sysd, walk):
    A, B, D = walk_affine(sysd, walk)
    return F(A, D)


def prefix_slopes(sysd, walk):
    p, m, t = sysd['p'], sysd['m'], sysd['table']
    s = F(1)
    out = []
    for r in walk:
        u, v, w = t[r % p ** m]
        s *= F(u, w)
        out.append(s)
    return out


def cycle_nodes(sysd, x, K, maxlen=10000):
    """Orbit of the rational x until it returns; returns list of points."""
    pts = [F(x)]
    y = F(x)
    for _ in range(maxlen):
        y = step_q(sysd, y)
        if y == pts[0]:
            return pts
        pts.append(y)
    raise ValueError('not periodic')


def rotate_cycle_lemma(sysd, pts):
    """Rotate a cycle (list of points) so that every partial product of
    slopes from the start is > 1 (requires total slope > 1)."""
    p, m = sysd['p'], sysd['m']
    sl = []
    for x in pts:
        u, v, w = sysd['table'][padic_res(x, p ** m)]
        sl.append(F(u, w))
    L = len(pts)
    best = None
    for start in range(L):
        s = F(1)
        ok = True
        for j in range(L):
            s *= sl[(start + j) % L]
            if s <= 1:
                ok = False
                break
        if ok:
            best = start
            break
    assert best is not None
    return pts[best:] + pts[:best]


def nodes_of_points(pts, p, K):
    return [padic_res(x, p ** K) for x in pts]


# ------------------------------------------------------------ cycles in G_K
def simple_cycles(E, maxlen):
    """All simple cycles (as node lists, smallest node first) up to maxlen."""
    out = []
    nodes = sorted(E)
    for s in nodes:
        stack = [(s, [s])]
        while stack:
            r, path = stack.pop()
            for (t, u, v, e) in E[r]:
                if t == s:
                    out.append(list(path))
                elif t > s and t not in path and len(path) < maxlen:
                    stack.append((t, path + [t]))
    # dedupe
    seen, res = set(), []
    for c in out:
        key = tuple(c)
        if key not in seen:
            seen.add(key)
            res.append(c)
    return res


def periodic_point(sysd, walk):
    A, B, D = walk_affine(sysd, walk)
    assert A != D
    return F(B, D - A)


def expanding_cycle(sysd, K, maxlen=8):
    """An expanding simple cycle of G_K of least length with its periodic point."""
    E = graph(sysd, K)
    best = None
    for c in simple_cycles(E, maxlen):
        s = slope(sysd, c)
        if s > 1:
            if best is None or len(c) < len(best[0]) or (len(c) == len(best[0]) and s > best[1]):
                best = (c, s)
    return best


def reach(E, src):
    seen = {src: None}
    order = [src]
    for r in order:
        for (t, u, v, e) in E[r]:
            if t not in seen:
                seen[t] = r
                order.append(t)
    return seen


def path_to(E, a, b):
    """shortest node path a -> ... -> b (list including a, excluding b), or None;
    for a == b returns []."""
    if a == b:
        return []
    par = reach(E, a)
    if b not in par:
        return None
    path = [b]
    while path[-1] != a:
        path.append(par[path[-1]])
    path.reverse()
    return path[:-1]


def reentry_walk(E, cnodes):
    """A closed walk at cnodes[0] (node list, start included, return excluded)
    that uses an edge not among the edges of the cycle cnodes.  None if the
    SCC of the cycle is the cycle alone (type (b))."""
    L = len(cnodes)
    cedges = {(cnodes[i], cnodes[(i + 1) % L]) for i in range(L)}
    r0 = cnodes[0]
    fromr0 = reach(E, r0)
    best = None
    for a in fromr0:
        for (b, u, v, e) in E[a]:
            if (a, b) in cedges:
                continue
            back = path_to(E, b, r0)
            if back is None:
                continue
            w = path_to(E, r0, a) + [a] + back
            if best is None or len(w) < len(best):
                best = w
    return best
