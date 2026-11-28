"""Round 4, lens 'transport': exact tools for transport identities between table maps.

A *table map* is (Q, table) with table[r] = (u, v, w) for r in range(Q):
    n = r (mod Q)  ->  (u n + v) / w      (exact on the whole class).
Q is arbitrary (prime power, mixed, ...).  Multipliers may be non-units.

Everything here is integer arithmetic.  The central object is a *piece*

    (Mod, c, a, b, d)   meaning   for every integer n = c (mod Mod):  F(n) = (a n + b)/d,

with d > 0 and d | a*c + b and d | a*Mod (so F is integral on the whole class).

The first-return map of T to a class set X (residues mod MX) is computed by refining
pieces until the branch of T, and membership in X, are constant on each piece.  When every
piece returns within the time bound, the induced map is an exact finite list of pieces; it
is conjugated by h(z) = MX*z + rX to a map on z and put into canonical table form
(the smallest modulus on whose classes it is affine).  Equal canonical forms are exact
identities between induced maps (proved by the finite piece computation: two affine maps
that agree as formulas agree everywhere on the class).
"""
from math import gcd
from fractions import Fraction


def lcm(a, b):
    return a // gcd(a, b) * b


# ------------------------------------------------------------------ table maps
def check_table(Q, table, upto=2000, positive=True):
    assert len(table) == Q
    for r in range(Q):
        u, v, w = table[r]
        assert w >= 1 and u >= 1
        # exact division on the whole class
        assert (u * r + v) % w == 0 and (u * Q) % w == 0, (r, table[r])
    if positive:
        for n in range(1, upto):
            u, v, w = table[n % Q]
            assert (u * n + v) // w >= 1, n


def step_fn(Q, table):
    def T(n):
        u, v, w = table[n % Q]
        x = u * n + v
        assert x % w == 0
        return x // w
    return T


def refine_factor(Mod, a, d, N):
    """For F(n) = (a n + b)/d on n = c (mod Mod): the factor k by which Mod must be
    multiplied so that F mod N is constant on each sub-class."""
    inc = a * Mod // d            # F(c + Mod s) = F(c) + inc*s
    assert (a * Mod) % d == 0
    g = gcd(N, inc)
    return N // g


def apply_step(Q, table, piece):
    """piece = (Mod, c, a, b, d) with F(n) mod Q constant on the class.
    Returns the piece for T o F (same class), exact."""
    Mod, c, a, b, d = piece
    x = (a * c + b)
    assert x % d == 0
    r = (x // d) % Q
    u, v, w = table[r]
    # T(F(n)) = (u (a n + b)/d + v)/w = (u a n + u b + v d)/(d w)
    a2, b2, d2 = u * a, u * b + v * d, d * w
    g = gcd(gcd(a2, b2), d2)
    a2, b2, d2 = a2 // g, b2 // g, d2 // g
    if d2 < 0:
        a2, b2, d2 = -a2, -b2, -d2
    assert (a2 * c + b2) % d2 == 0 and (a2 * Mod) % d2 == 0
    return (Mod, c, a2, b2, d2)


def split(piece, k):
    Mod, c, a, b, d = piece
    return [(Mod * k, c + i * Mod, a, b, d) for i in range(k)]


def value_mod(piece, N):
    Mod, c, a, b, d = piece
    return ((a * c + b) // d) % N


def first_return(Q, table, MX, RX, tmax=40, pmax=200000, start=None):
    """First-return map of T to X = {n : n mod MX in RX}, starting from the classes in
    `start` (default: X itself).  Returns (pieces, status) where pieces is a list of
    (Mod, c, t, a, b, d): for n = c (mod Mod), the first t >= 1 with T^t(n) in X is t and
    T^t(n) = (a n + b)/d.  status is 'ok' or 'unbounded' (some piece did not return within
    tmax, or more than pmax pieces were needed)."""
    RX = set(RX)
    if start is None:
        start = [(MX, r, 1, 0, 1) for r in sorted(RX)]
    out = []
    stack = [(p, 0) for p in start]
    while stack:
        piece, t = stack.pop()
        Mod, c, a, b, d = piece
        k = refine_factor(Mod, a, d, Q)          # make the branch of T constant
        if k > 1:
            stack.extend((q, t) for q in split(piece, k))
            if len(stack) + len(out) > pmax:
                return out, 'unbounded'
            continue
        piece = apply_step(Q, table, piece)
        t += 1
        Mod, c, a, b, d = piece
        k = refine_factor(Mod, a, d, MX)         # make membership in X constant
        for q in (split(piece, k) if k > 1 else [piece]):
            if value_mod(q, MX) in RX:
                Mq, cq, aq, bq, dq = q
                out.append((Mq, cq, t, aq, bq, dq))
            elif t >= tmax:
                return out, 'unbounded'
            else:
                stack.append((q, t))
        if len(stack) + len(out) > pmax:
            return out, 'unbounded'
    return out, 'ok'


# ------------------------------------------------------------------ z-coordinates
def to_z(pieces, MX, rX):
    """Conjugate induced pieces on X = rX (mod MX) by h(z) = MX z + rX.
    Returns z-pieces (Modz, cz, A, B, D): z = cz (mod Modz) -> (A z + B)/D."""
    zp = []
    for (Mod, c, t, a, b, d) in pieces:
        assert Mod % MX == 0 and c % MX == rX % MX
        Modz, cz = Mod // MX, ((c - rX) // MX) % (Mod // MX)
        # B(z) = ((a (MX z + rX) + b)/d - rX)/MX
        A, B, D = a * MX, a * rX + b - rX * d, d * MX
        g = gcd(gcd(A, B), D)
        A, B, D = A // g, B // g, D // g
        zp.append((Modz, cz, A, B, D))
    return zp


def canonical(zpieces, Lmax=1 << 16):
    """Canonical table form of a piecewise affine map given by a partition into classes.
    Returns (Q, tuple of (A, B, D)) with the least Q (a divisor of the lcm of the piece
    moduli) such that the map is a single affine formula on each class mod Q; or None if
    the lcm exceeds Lmax."""
    L = 1
    for (M, c, A, B, D) in zpieces:
        L = lcm(L, M)
        if L > Lmax:
            return None
    full = [None] * L
    for (M, c, A, B, D) in zpieces:
        for r in range(c % M, L, M):
            assert full[r] is None, "pieces overlap"
            full[r] = (A, B, D)
    assert all(f is not None for f in full), "pieces do not cover"
    divs = sorted(q for q in range(1, L + 1) if L % q == 0)
    for q in divs:
        if all(full[r] == full[r % q] for r in range(L)):
            return (q, tuple(full[:q]))
    raise AssertionError


def as_table(canon):
    """(Q, ((A,B,D),...)) -> (Q, table) in (u, v, w) format (u = A, v = B, w = D)."""
    Q, rows = canon
    return Q, [tuple(r) for r in rows]


def induced_canonical(Q, table, MX, rX, tmax=40, pmax=200000, Lmax=1 << 16):
    pcs, st = first_return(Q, table, MX, [rX], tmax=tmax, pmax=pmax)
    if st != 'ok':
        return None, pcs, st
    zp = to_z(pcs, MX, rX)
    return canonical(zp, Lmax=Lmax), pcs, st


def table_canonical(Q, table):
    zp = []
    for r in range(Q):
        u, v, w = table[r]
        g = gcd(gcd(u, v), w)
        zp.append((Q, r, u // g, v // g, w // g))
    return canonical(zp)


# ------------------------------------------------------------------ verification
def verify_identity_pieces(QA, tA, pieces, MX, rX, QB, tB, upto=3000):
    """Numerical cross-check (not a proof; the proof is the symbolic computation):
    for z < upto, A^t(h z) = h(B z) with t from the pieces."""
    TA, TB = step_fn(QA, tA), step_fn(QB, tB)
    for (Mod, c, t, a, b, d) in pieces:
        for n in range(c if c > 0 else c + Mod, c + Mod * 40, Mod):
            y = n
            for i in range(t):
                y = TA(y)
                if i < t - 1:
                    assert y % MX != rX % MX, "not first return"
            assert y * d == a * n + b
            z = (n - rX) // MX
            assert h(MX, rX, TB(z)) == y if z >= 0 and TB(z) >= 0 else True
    return True


def h(MX, rX, z):
    return MX * z + rX


# ------------------------------------------------------------------ residue graph (any Q)
def residue_graph(Q, table):
    succ = {}
    for r in range(Q):
        u, v, w = table[r]
        base = ((u * r + v) // w) % (Q // w) if Q % w == 0 else None
        assert base is not None
        succ[r] = sorted(set(base + i * (Q // w) for i in range(w)))
    return succ


def tarjan(nodes, succ):
    index, low, onst, st, comps = {}, {}, set(), [], []
    counter = [0]
    import sys
    sys.setrecursionlimit(100000)

    def strong(v):
        index[v] = low[v] = counter[0]
        counter[0] += 1
        st.append(v)
        onst.add(v)
        for w in succ[v]:
            if w not in index:
                strong(w)
                low[v] = min(low[v], low[w])
            elif w in onst:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = []
            while True:
                w = st.pop()
                onst.discard(w)
                comp.append(w)
                if w == v:
                    break
            comps.append(comp)
    for v in nodes:
        if v not in index:
            strong(v)
    return comps


def reachable(succ, starts):
    seen = set(starts)
    st = list(starts)
    while st:
        x = st.pop()
        for y in succ[x]:
            if y not in seen:
                seen.add(y)
                st.append(y)
    return seen


def lift_table(Q, table, Q2):
    assert Q2 % Q == 0
    return [table[r % Q] for r in range(Q2)]


def periodic_points(Q, table, L):
    """All periodic points of period dividing L of the extension of T to the profinite
    completion that are rational (closed walks of length L in the residue graph at modulus
    Q), with their exact real multipliers.  Returns list of (walk, x (Fraction), lam)."""
    succ = residue_graph(Q, table)
    res = []

    def rec(walk, A, B, W):
        if len(walk) == L:
            if walk[0] in succ[walk[-1]] or True:
                pass
            return
    out = []
    stack = [([r], 1, 0, 1) for r in range(Q)]
    while stack:
        walk, A, B, W = stack.pop()
        r = walk[-1]
        u, v, w = table[r]
        A2, B2, W2 = A * u, B * u + v * W, W * w
        if len(walk) == L:
            if walk[0] in succ[r] and W2 != A2:
                x = Fraction(B2, W2 - A2)
                out.append((tuple(walk), x, Fraction(A2, W2)))
            continue
        for s in succ[r]:
            stack.append((walk + [s], A2, B2, W2))
    return out


# ------------------------------------------------------------------ sufficiency
def overapprox_succ(Q, table, M):
    """Successor sets of classes mod M (M a multiple of Q and of every w) under T:
    T(x + M t) = T(x) + (u M / w) t, so T(n) mod M lies in T(x) + gcd(uM/w, M) Z.
    This over-approximates the residues that T can reach (exact for unit multipliers)."""
    assert M % Q == 0
    succ = {}
    for x in range(M):
        u, v, w = table[x % Q]
        assert M % w == 0 and (u * x + v) % w == 0
        y = (u * x + v) // w
        g = gcd(u * M // w, M)
        succ[x] = sorted(set((y + g * i) % M for i in range(M // g)))
    return succ


def dilation_prime(Q, table):
    """p if T(p n) = n for every n (table[r] = (1, 0, p) for all r = 0 mod p), else None."""
    for p in range(2, Q + 1):
        if Q % p == 0 and all(p % s for s in range(2, p)):
            if all(table[r] == (1, 0, p) for r in range(0, Q, p)):
                return p
    return None


def sufficient(Q, table, MX, rX, allow_contracting=False):
    """Exact sufficient condition for 'every merging class of positive integers meets
    X = rX (mod MX)'.  Let G = {c mod MX : d^j c = rX (mod MX) for some j >= 0}, where d is
    the dilation prime of T (T(d n) = n), or G = {rX} if T has none.  This implements the full
    Lemma S of transport_theorems.md (docstring corrected after REFEREE1; it used to say
    "acyclic"): with M = lcm(Q, MX, all w), every strongly connected component with an internal
    edge of the over-approximate residue graph mod M restricted to the classes outside G must be
    pure dilation (every vertex has the branch n -> n/d) or, if allow_contracting, contracting
    (every closed walk has prod u / prod w < 1, tested exactly).  Then every positive orbit is
    eventually periodic inside a contracting component or visits G, and if c in G is on the
    orbit, d^j c lies in X and merges with it.
    Returns (True, data) or (False, reason)."""
    M = lcm(Q, MX)
    for (u, v, w) in table:
        M = lcm(M, w)
    d = dilation_prime(Q, table)
    G = {rX % MX}
    if d is not None:
        for c in range(MX):
            x = c
            for j in range(4 * MX + 4):
                if x % MX == rX % MX:
                    G.add(c)
                    break
                x = (x * d) % MX
    succ = overapprox_succ(Q, table, M)
    bad = [x for x in range(M) if x % MX not in G]
    badset = set(bad)
    sub = {x: [y for y in succ[x] if y in badset] for x in bad}
    contracting = []
    for comp in tarjan(bad, sub):
        cs = set(comp)
        if not any(y in cs for x in comp for y in sub[x]):
            continue
        # an orbit can stay in this SCC forever only if it uses only pure dilations n -> n/d,
        # which no positive integer can do forever
        if all(d is not None and table[x % Q] == (1, 0, d) for x in comp):
            continue
        if allow_contracting and contracting_scc(table, Q, succ, comp):
            contracting.append(sorted(comp))
            continue
        return False, "bad SCC with a non-dilation vertex mod %d: %s" % (M, sorted(comp)[:8])
    return True, dict(M=M, G=sorted(G), dilation=d, contracting=contracting)


def contracting_scc(table, Q, succ, comp):
    """Exact: every closed walk inside comp (over-approximate graph mod M) has multiplier < 1.
    Multipliers are inflated by the factor 1001/1000 so that a cycle of product exactly 1 is
    also caught (conservative: may reject a contracting SCC, never accepts a bad one)."""
    cs = list(comp)
    ns = set(cs)
    infl = Fraction(1001, 1000)
    d = {r: Fraction(1) for r in cs}
    mult = {r: Fraction(table[r % Q][0], table[r % Q][2]) * infl for r in cs}
    for it in range(len(cs) + 1):
        changed = False
        for r in cs:
            x = d[r] * mult[r]
            for s in succ[r]:
                if s in ns and x > d[s]:
                    d[s] = x
                    changed = True
        if not changed:
            return True
    return False


# ------------------------------------------------------------------ trichotomy type (unit p-adic)
def scc_type(Q, table):
    """For a table map satisfying (H1)-(P), decide CERT/OBST with decide.py and, if OBST by an
    expanding cycle, report whether that cycle lies in a non-simple SCC of the residue graph
    (type (c) in the sense of accel/trichotomy.md at level Q).  Returns a dict."""
    import os as _os, sys as _sys
    _sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', '..',
                                      'round3', 'dichotomy'))
    import decide as _dec
    res = _dec.decide(Q, [tuple(t) for t in table], want_cycles=False, want_depth=False)
    out = dict(verdict=res['verdict'])
    if res['verdict'] == 'CERT':
        out['type'] = 'a'
        return out
    o = res['obst']
    out['kind'] = o['kind']
    if o['kind'] == 'critical':
        out['type'] = 'critical'
        return out
    cyc = [r % Q for r in o['cycle']]
    U, W = o['U'], o['W']
    assert U > W
    succ = residue_graph(Q, table)
    comp = next(c for c in tarjan(list(range(Q)), succ) if cyc[0] in c)
    cs = set(comp)
    nint = sum(1 for a in comp for b in succ[a] if b in cs)
    out.update(cycle=cyc, U=U, W=W, scc_size=len(comp), scc_edges=nint)
    # standing hypothesis: no division-free cycle (all w = 1 on a cycle)
    nodiv = {r: [s for s in succ[r]] for r in range(Q) if table[r][2] == 1}
    out['division_free_cycle'] = any(len(c) > 1 or (c[0] in nodiv.get(c[0], []))
                                     for c in tarjan(list(nodiv), {r: [s for s in nodiv[r] if s in nodiv]
                                                                   for r in nodiv}))
    out['type'] = 'c' if nint > len(comp) else 'b?'
    return out


# ------------------------------------------------------------------ exact type of a unit p-adic table
def prime_power(Q):
    if Q < 2:
        return None
    p = next(d for d in range(2, Q + 1) if Q % d == 0)
    x = Q
    while x % p == 0:
        x //= p
    return p if x == 1 else None


def is_unit_padic(Q, rows):
    p = prime_power(Q)
    if p is None:
        return None
    for (u, v, w) in rows:
        if u < 1 or u % p == 0 or w < 1:
            return None
        x = w
        while x % p == 0:
            x //= p
        if x != 1 or Q % w != 0:
            return None
    return p


def bad_cycle_in(Q, rows, succ, nodes):
    """Exact multiplicative Bellman-Ford inside the node set: a cycle with prod u > prod w."""
    nodes = list(nodes)
    ns = set(nodes)
    d = {r: Fraction(1) for r in nodes}
    pred = {r: None for r in nodes}
    mult = {r: Fraction(rows[r][0], rows[r][2]) for r in nodes}
    last = None
    for it in range(len(nodes) + 1):
        last = None
        for r in nodes:
            x = d[r] * mult[r]
            for s in succ[r]:
                if s in ns and x > d[s]:
                    d[s], pred[s], last = x, r, s
        if last is None:
            return None
    x = last
    for _ in range(len(nodes)):
        x = pred[x]
    cyc, y = [x], pred[x]
    while y != x:
        cyc.append(y)
        y = pred[y]
    cyc.reverse()
    U = W = 1
    for r in cyc:
        U *= rows[r][0]
        W *= rows[r][2]
    assert U > W
    return cyc, U, W


def unit_type(Q, rows):
    """Exact trichotomy type of a unit p-adic table at level Q (accel/trichotomy.md):
    returns dict(p, type in {'a','b','c','critical'}, ...).  'critical' = a division-free
    cycle exists (standing hypothesis fails).  Type (c): some non-simple SCC contains a cycle
    with multiplier > 1 (verified exactly)."""
    p = is_unit_padic(Q, rows)
    assert p is not None
    succ = residue_graph(Q, rows)
    comps = tarjan(list(range(Q)), succ)
    # division-free cycles
    nd = [r for r in range(Q) if rows[r][2] == 1]
    ndset = set(nd)
    for comp in tarjan(nd, {r: [s for s in succ[r] if s in ndset] for r in nd}):
        cs = set(comp)
        if any(s in cs for r in comp for s in succ[r]):
            return dict(p=p, type='critical', cycle=comp)
    best = 'a'
    info = {}
    for comp in comps:
        cs = set(comp)
        nint = sum(1 for a in comp for b in succ[a] if b in cs)
        if nint == 0:
            continue
        bc = bad_cycle_in(Q, rows, succ, comp)
        if bc is None:
            continue
        if nint > len(comp):
            return dict(p=p, type='c', cycle=bc[0], U=bc[1], W=bc[2], scc=sorted(comp))
        best = 'b'
        info = dict(cycle=bc[0], U=bc[1], W=bc[2])
    out = dict(p=p, type=best)
    out.update(info)
    return out
