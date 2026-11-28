"""Exact tools for the round-3 "divergence" lens.

Maps
----
An RCWA map is given on a modulus L by rules[r] = (a, b, d) for r = 0..L-1:
    T(n) = (a*n + b) // d     for n = r (mod L),  with d | a*n + b on the class.
We require a >= 1, d >= 1, b >= 0 ("nonnegative offsets") unless stated, and
T(n) >= 1 for n >= 1.  Every function here is exact (Python integers).

Residue graph
-------------
For K a multiple of L, the class r (mod K) is mapped by T onto the progression
T(r0) + (a*K/d)*t (t >= 0), r0 the least positive member of the class.  Its
residues mod K are exactly T(r0) + g*Z (mod K), g = gcd(a*K/d, K).  A union U of
classes mod K satisfies T(U) <= U  iff  every edge of this graph out of U stays
in U.  (Exact: every residue of the progression is hit by infinitely many t.)

Ascent certificate (Lemma A-up, see ascent.md)
----------------------------------------------
U forward closed, every closed walk of the residue graph inside U has slope
product > 1, all offsets b >= 0  ==>  U contains no periodic point, so every
orbit that enters U is unbounded.  `ascent_certificate` returns an exact
witness: integer lower bounds W_u <= N*log2(a_u/d_u) (each verified by an
integer power comparison) and an integer potential phi with
    S*W_u - 1 + phi(u) - phi(v) >= 0   on every edge u -> v of U,   S = |U|+1.
Summing over a simple cycle of length l <= |U| gives S*sum(W) >= l > 0 ... see
ascent.md for the full argument.  `verify_ascent` re-checks a witness.
"""

from math import gcd
from collections import deque


# ------------------------------------------------------------------ maps ---
class RCWA:
    def __init__(self, L, rules, name=""):
        self.L = L
        self.rules = [tuple(x) for x in rules]
        self.name = name
        assert len(self.rules) == L

    def __call__(self, n):
        a, b, d = self.rules[n % self.L]
        x = a * n + b
        assert x % d == 0, (n, self.name)
        return x // d

    def check(self):
        """Integrality on every whole class, positivity, b >= 0."""
        L = self.L
        for r, (a, b, d) in enumerate(self.rules):
            assert a >= 1 and d >= 1
            r0 = r if r > 0 else L
            assert (a * r0 + b) % d == 0 and (a * L) % d == 0, (r, a, b, d)
            assert (a * r0 + b) // d >= 1
        return True

    def slope(self, r):
        a, b, d = self.rules[r % self.L]
        return a, d


def from_function(L, f, name=""):
    """Recover (a, b, d) per class from an affine-on-classes function f.
    d is taken minimal; verified on several members."""
    from fractions import Fraction
    rules = []
    for r in range(L):
        r0 = r if r > 0 else L
        y0, y1 = f(r0), f(r0 + L)
        slope = Fraction(y1 - y0, L)
        off = Fraction(y0) - slope * r0
        d = (slope.denominator * off.denominator) // gcd(slope.denominator, off.denominator)
        a = slope * d
        b = off * d
        assert a.denominator == 1 and b.denominator == 1
        for t in (2, 7, 101):
            assert f(r0 + t * L) == (a.numerator * (r0 + t * L) + b.numerator) // d
        rules.append((a.numerator, b.numerator, d))
    return RCWA(L, rules, name)


def modify(base, L, changes, name=""):
    """Refine `base` to modulus L (multiple of base.L) and overwrite classes."""
    assert L % base.L == 0
    rules = [base.rules[r % base.L] for r in range(L)]
    for r, rule in changes.items():
        rules[r % L] = tuple(rule)
    return RCWA(L, rules, name)


# ------------------------------------------------------- residue graph ---
def images(T, K, r):
    """Residues mod K of T on the class r (mod K)."""
    assert K % T.L == 0
    a, b, d = T.rules[r % T.L]
    r0 = r if r > 0 else K
    base = (a * r0 + b) // d
    step = a * K // d
    assert (a * K) % d == 0
    g = gcd(step, K)
    return [(base + g * j) % K for j in range(K // g)]


def forward_closure(T, K, start):
    seen = set(start)
    todo = list(start)
    while todo:
        u = todo.pop()
        for v in images(T, K, u):
            if v not in seen:
                seen.add(v)
                todo.append(v)
    return seen


def is_closed(T, K, U):
    U = set(U)
    return all(v in U for u in U for v in images(T, K, u))


# --------------------------------------------------- ascent certificates ---
def log2_floor_scaled(a, d, N):
    """Largest integer W with 2^W <= (a/d)^N, i.e. W = floor(N*log2(a/d))."""
    num, den = a ** N, d ** N
    # find W with 2^W * den <= num < 2^(W+1) * den
    W = num.bit_length() - den.bit_length()

    def le(W):  # 2^W * den <= num
        return (den << W) <= num if W >= 0 else den <= (num << (-W))
    while not le(W):
        W -= 1
    while le(W + 1):
        W += 1
    return W


def cycles_positive_potential(nodes, adj, W):
    """Integer potential phi with S*W[u]-1+phi[u]-phi[v] >= 0 on all edges
    (S = len(nodes)+1), or None.  Exists iff every cycle has sum(W) >= 1."""
    S = len(nodes) + 1
    phi = {u: 0 for u in nodes}
    inq = {u: True for u in nodes}
    q = deque(nodes)
    cnt = {u: 0 for u in nodes}
    while q:
        u = q.popleft()
        inq[u] = False
        w = S * W[u] - 1
        for v in adj[u]:
            if phi[u] + w < phi[v]:
                phi[v] = phi[u] + w
                cnt[v] += 1
                if cnt[v] > len(nodes) + 1:
                    return None
                if not inq[v]:
                    inq[v] = True
                    q.append(v)
    return phi


def vp(x, p):
    k = 0
    while x % p == 0:
        x //= p
        k += 1
    return k


def aperiodic_certificate(T, K, U, p=2):
    """Witness that every cycle of the residue graph on U has net p-adic
    valuation of the slope product <= -1 (a nontrivial p-power denominator).
    Then (itinerary lemma) an infinite orbit in U has a non-eventually-periodic
    itinerary.  Returns phi for weights W[u] = -(v_p(a)-v_p(d)), or None."""
    U = sorted(U)
    W = {}
    for u in U:
        a, d = T.slope(u)
        W[u] = -(vp(a, p) - vp(d, p))
    adj = {u: sorted(set(images(T, K, u))) for u in U}
    phi = cycles_positive_potential(U, adj, W)
    if phi is None:
        return None
    return dict(K=K, p=p, U=U, W=W, phi=phi)


def verify_aperiodic(T, cert):
    K, p, U, W, phi = cert["K"], cert["p"], cert["U"], cert["W"], cert["phi"]
    Uset = set(U)
    S = len(U) + 1
    for u in U:
        a, d = T.slope(u)
        assert W[u] == -(vp(a, p) - vp(d, p))
        for v in images(T, K, u):
            assert v in Uset
            assert S * W[u] - 1 + phi[u] - phi[v] >= 0
    return True


def ascent_certificate(T, K, U, N=64):
    """Return (W, phi) or None.  W[u] = floor(N log2 slope), phi potential."""
    U = sorted(U)
    idx = {u: i for i, u in enumerate(U)}
    S = len(U) + 1
    cache = {}
    W = {}
    for u in U:
        a, d = T.slope(u)
        if (a, d) not in cache:
            cache[(a, d)] = log2_floor_scaled(a, d, N)
        W[u] = cache[(a, d)]
    adj = {u: sorted(set(images(T, K, u))) for u in U}
    for u in U:
        for v in adj[u]:
            if v not in idx:
                return None          # not closed
    phi = cycles_positive_potential(U, adj, W)
    if phi is None:
        return None
    return dict(K=K, N=N, U=U, W=W, phi=phi)


def verify_ascent(T, cert):
    """Exact re-check of an ascent witness.  Returns True or raises."""
    K, N, U, W, phi = cert["K"], cert["N"], cert["U"], cert["W"], cert["phi"]
    Uset = set(U)
    S = len(U) + 1
    for u in U:
        a, b, d = T.rules[u % T.L]
        assert b >= 0, "offsets must be nonnegative"
        w = W[u]
        # 2^w <= (a/d)^N exactly
        if w >= 0:
            assert (d ** N) << w <= a ** N
        else:
            assert d ** N <= (a ** N) << (-w)
        for v in images(T, K, u):
            assert v in Uset, ("not closed", u, v)
            assert S * w - 1 + phi[u] - phi[v] >= 0, ("potential", u, v)
    return True


# ------------------------------------------------------------- falls ---
def is_fall_class(T, K, u):
    """True iff T(x) < x for every positive x = u (mod K)."""
    a, b, d = T.rules[u % T.L]
    x0 = u if u > 0 else K
    if a >= d:
        return False
    # (a x + b)/d < x  <=>  (d - a) x > b ; increasing in x, so test x0
    return (d - a) * x0 > b


def nonfall_subgraph_acyclic(T, K, U):
    """Every cycle inside U uses a fall class  <=>  non-fall subgraph acyclic."""
    U = set(U)
    nodes = [u for u in U if not is_fall_class(T, K, u)]
    nset = set(nodes)
    adj = {u: [v for v in set(images(T, K, u)) if v in nset] for u in nodes}
    color = {u: 0 for u in nodes}
    for s in nodes:
        if color[s]:
            continue
        stack = [(s, iter(adj[s]))]
        color[s] = 1
        while stack:
            u, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                color[u] = 2
                stack.pop()
            elif color[nxt] == 1:
                return False
            elif color[nxt] == 0:
                color[nxt] = 1
                stack.append((nxt, iter(adj[nxt])))
    return True


# ------------------------------------------------------------ orbits ---
def orbit(T, n, steps):
    out = [n]
    for _ in range(steps):
        n = T(n)
        out.append(n)
    return out


def find_cycle_from(T, n, cap=10 ** 6, bound=10 ** 60):
    """Simulate; return (cycle_min, length) if the orbit cycles within cap, else None."""
    seen = {}
    i = 0
    while i < cap and n < bound:
        if n in seen:
            j = seen[n]
            cyc = []
            m = n
            while True:
                cyc.append(m)
                m = T(m)
                if m == n:
                    break
            return min(cyc), len(cyc)
        seen[n] = i
        n = T(n)
        i += 1
    return None
