"""Round 3, lens 'accel': exact tools for the SCC trichotomy (trichotomy.md).

A *unit-multiplier p-adic system* is (p, m, table) with table[r] = (u, v, w)
for r in range(p**m): n = r (mod p^m) -> (u*n + v)//w, where w = p^e (e >= 0),
p does not divide u, u >= 1, and w | u*n + v on the whole class.  (Same format
as census/round2/descent/descent_lib.py.)

The level-K cylinder graph G_K (K >= m) has nodes r mod p^K and, for the step
n -> (u n + v)/p^e on class r, the p^e edges r -> s with
s = (u r + v)/p^e (mod p^(K-e)); every edge carries the exact multiplier u/p^e.
Because u is a p-adic unit, the image of the class r mod p^K is exactly the
union of the classes s mod p^K above (the graph is Markov).

Everything that is used as proof data is exact (ints / Fractions).  Floating
point is used only to *find* weights, which are then verified exactly.
"""
from fractions import Fraction
import math


def check_system(p, m, table, upto=3000):
    Q = p ** m
    for r in range(Q):
        u, v, w = table[r]
        assert u >= 1 and u % p != 0, (r, u)
        e = 0
        ww = w
        while ww % p == 0:
            ww //= p
            e += 1
        assert ww == 1, (r, w)
        # divisibility on the whole class: check r and r + Q
        assert (u * r + v) % w == 0 and (u * (r + Q) + v) % w == 0, r
    for n in range(1, upto):
        u, v, w = table[n % Q]
        assert (u * n + v) % w == 0 and (u * n + v) // w >= 1, n


def step_fn(p, m, table):
    Q = p ** m

    def T(n):
        u, v, w = table[n % Q]
        x = u * n + v
        assert x % w == 0
        return x // w
    return T


def graph(p, m, table, K):
    """Edges of G_K as a dict r -> list of (s, Fraction multiplier)."""
    assert K >= m
    Q, PK = p ** m, p ** K
    E = {}
    for r in range(PK):
        u, v, w = table[r % Q]
        e = round(math.log(w, p)) if w > 1 else 0
        assert p ** e == w
        assert e <= K
        base = ((u * r + v) // w) % (PK // w)
        E[r] = [(base + i * (PK // w), Fraction(u, w)) for i in range(w)]
    return E


def tarjan(nodes, E):
    """Iterative Tarjan; returns list of SCCs (lists of nodes)."""
    index, low, onst, st, out = {}, {}, set(), [], []
    c = 0
    for v0 in nodes:
        if v0 in index:
            continue
        work = [(v0, 0)]
        index[v0] = low[v0] = c
        c += 1
        st.append(v0)
        onst.add(v0)
        while work:
            v, i = work[-1]
            succ = E[v]
            if i < len(succ):
                work[-1] = (v, i + 1)
                w = succ[i][0]
                if w not in index:
                    index[w] = low[w] = c
                    c += 1
                    st.append(w)
                    onst.add(w)
                    work.append((w, 0))
                elif w in onst:
                    low[v] = min(low[v], index[w])
            else:
                work.pop()
                if work:
                    u = work[-1][0]
                    low[u] = min(low[u], low[v])
                if low[v] == index[v]:
                    comp = []
                    while True:
                        w = st.pop()
                        onst.discard(w)
                        comp.append(w)
                        if w == v:
                            break
                    out.append(comp)
    return out


def internal_edges(comp, E):
    cs = set(comp)
    return [(r, s, q) for r in comp for s, q in E[r] if s in cs]


def simple_cycle(comp, E):
    """If the SCC is a single simple cycle, return its node sequence and exact
    multiplier; otherwise None."""
    ed = internal_edges(comp, E)
    if len(ed) != len(comp) or not ed:
        return None
    nxt = {r: (s, q) for r, s, q in ed}
    assert len(nxt) == len(comp)
    seq, lam, r = [comp[0]], Fraction(1), comp[0]
    while True:
        s, q = nxt[r]
        lam *= q
        if s == comp[0]:
            break
        seq.append(s)
        r = s
    assert len(seq) == len(comp)
    return seq, lam


def karp_max_mean(comp, E):
    """Float max mean of log-multipliers over cycles inside the SCC (search only)."""
    ix = {v: i for i, v in enumerate(comp)}
    ed = [(ix[r], ix[s], math.log(q.numerator) - math.log(q.denominator))
          for r, s, q in internal_edges(comp, E)]
    n = len(comp)
    NEG = float("-inf")
    D = [[NEG] * n for _ in range(n + 1)]
    D[0] = [0.0] * n
    for k in range(1, n + 1):
        Dk, Dp = D[k], D[k - 1]
        for a, b, wt in ed:
            if Dp[a] != NEG and Dp[a] + wt > Dk[b]:
                Dk[b] = Dp[a] + wt
    best = NEG
    for v in range(n):
        if D[n][v] == NEG:
            continue
        best = max(best, min((D[n][v] - D[k][v]) / (n - k)
                             for k in range(n) if D[k][v] != NEG))
    return best


def contraction_weights(comp, E):
    """For an SCC all of whose cycles contract, return (theta, c) with theta a
    Fraction < 1 and c: node -> positive Fraction such that for every internal
    edge r -> s with multiplier q:  c[s] * q <= theta * c[r]  (verified
    exactly).  Returns None if the search fails (e.g. an expanding cycle)."""
    mu = karp_max_mean(comp, E)
    if not mu < -1e-12:
        return None
    for frac in (0.5, 0.3, 0.7, 0.15, 0.85):
        lt = mu * frac                       # log theta used for the search
        theta = Fraction(math.exp(mu * frac * 0.5)).limit_denominator(10 ** 6)
        if not theta < 1:
            continue
        # longest-path potentials with edge weights log q - lt (no positive cycle)
        phi = {v: 0.0 for v in comp}
        ed = internal_edges(comp, E)
        for _ in range(len(comp) + 1):
            ch = False
            for r, s, q in ed:
                val = phi[r] + math.log(q.numerator) - math.log(q.denominator) - lt
                if val > phi[s] + 1e-15:
                    phi[s] = val
                    ch = True
            if not ch:
                break
        mx = max(phi.values())
        c = {v: Fraction(math.exp(mx - phi[v])).limit_denominator(10 ** 9) for v in comp}
        if all(c[s] * q <= theta * c[r] for r, s, q in ed) and all(x > 0 for x in c.values()):
            return theta, c
    return None


def classify(p, m, table, K):
    """Exact SCC classification of G_K.  Returns (E, list of dicts) with kind in
    'trivial' (no internal edge), 'simple' (one simple cycle; lam exact),
    'contracting' (exact weights found), 'other' (none of these)."""
    E = graph(p, m, table, K)
    out = []
    for comp in tarjan(list(range(p ** K)), E):
        ed = internal_edges(comp, E)
        if not ed:
            out.append(dict(kind="trivial", nodes=comp))
            continue
        sc = simple_cycle(comp, E)
        if sc is not None:
            out.append(dict(kind="simple", nodes=comp, cycle=sc[0], lam=sc[1]))
            continue
        cw = contraction_weights(comp, E)
        if cw is not None:
            out.append(dict(kind="contracting", nodes=comp, theta=cw[0], c=cw[1]))
        else:
            out.append(dict(kind="other", nodes=comp, nedges=len(ed)))
    return E, out


def compose_along(p, m, table, K, cyc):
    """Composed affine map x -> (A x + B) along the residue cycle cyc (level K),
    exact.  Returns (A, B) as Fractions."""
    Q = p ** m
    A, B = Fraction(1), Fraction(0)
    for r in cyc:
        u, v, w = table[r % Q]
        A, B = A * Fraction(u, w), (B * u + v) / Fraction(w)
    return A, B


def padic_residue(x, p, K):
    a, b = x.numerator, x.denominator
    assert b % p != 0
    return (a * pow(b, -1, p ** K)) % p ** K


def theorem_H(p, m, table, K, cap=10 ** 7):
    """Apply Theorem H (trichotomy.md).  Returns dict with the exact proof data
    and the complete cycle list, or raises AssertionError if the hypotheses fail.
    """
    check_system(p, m, table)
    T = step_fn(p, m, table)
    E, comps = classify(p, m, table, K)
    assert all(c["kind"] != "other" for c in comps), "hypothesis of Theorem H fails"
    PK = p ** K
    cycles = set()
    expanding = []
    bounds = []
    for c in comps:
        if c["kind"] == "simple":
            A, B = compose_along(p, m, table, K, c["cycle"])
            # Theorem H needs a division on every cycle (no division-free cycle)
            assert any(table[r % p ** m][2] > 1 for r in c["cycle"]), "division-free cycle"
            if A == 1:
                raise AssertionError("neutral simple cycle")
            x = B / (1 - A)                       # fixed point of the composed map
            # the fixed point follows the cycle (Markov + unit multipliers)
            assert padic_residue(x, p, K) == c["cycle"][0]
            c["xstar"] = x
            if A > 1:
                expanding.append(c)
            if x.denominator == 1 and x > 0:
                # positive integer periodic point: it is a genuine T-cycle
                y, orb = int(x), []
                while True:
                    orb.append(y)
                    y = T(y)
                    if y == orb[0]:
                        break
                cycles.add(min(orb))
            if A < 1:
                # contracting simple cycle: V(n) = |n - x*| decreases; points
                # staying in it converge to x*, so the only cycle is x* itself.
                pass
        elif c["kind"] == "contracting":
            theta, w = c["theta"], c["c"]
            Q = p ** m
            beta = Fraction(0)
            for r in c["nodes"]:
                u, v, ww = table[r % Q]
                for s, q in E[r]:
                    if s in w:
                        beta = max(beta, w[s] * Fraction(max(v, 0), ww))
            Vmax = beta / (1 - theta)
            nmax = math.floor(Vmax / min(w.values()))
            assert nmax <= cap, ("bound too large", nmax)
            bounds.append((len(c["nodes"]), theta, beta, nmax))
            nodes = set(c["nodes"])
            for n in range(1, nmax + 1):
                if n % PK in nodes and w[n % PK] * n <= Vmax:
                    # candidate cycle point; follow the orbit until it repeats
                    seen, y = {}, n
                    while y not in seen:
                        seen[y] = len(seen)
                        y = T(y)
                    cyc, z = [y], T(y)
                    while z != y:
                        cyc.append(z)
                        z = T(z)
                    cycles.add(min(cyc))
    return dict(comps=comps, expanding=expanding, cycles=sorted(cycles), bounds=bounds)


def cycle_of(T, n):
    seen, y = set(), n
    while y not in seen:
        seen.add(y)
        y = T(y)
    cyc, z = [y], T(y)
    while z != y:
        cyc.append(z)
        z = T(z)
    return cyc


# ---------------------------------------------------------------- Theorem N
def orbit_residues(x, p, m, table, K, maxlen=10000):
    """Exact orbit of a rational p-adic periodic point x; returns the residue
    cycle mod p^K and the exact multiplier over one period."""
    Q = p ** m
    x0, res, lam = Fraction(x), [], Fraction(1)
    y = x0
    for _ in range(maxlen):
        r = padic_residue(y, p, K)
        res.append(r)
        u, v, w = table[r % Q]
        lam *= Fraction(u, w)
        y = (u * y + v) / w
        assert y.denominator % p != 0
        if y == x0:
            return res, lam
    raise AssertionError("not periodic")


def walk_point(p, m, table, K, walk):
    """Exact periodic point following the closed walk `walk` (list of level-K
    nodes, walk[i] -> walk[i+1] -> ... -> walk[0]) and its multiplier.  The
    point is verified to follow the walk."""
    A, B = compose_along(p, m, table, K, walk)
    assert A != 1
    x = B / (1 - A)
    res, lam = orbit_residues(x, p, m, table, K)
    L = len(walk)
    assert len(res) % L == 0 or L % len(res) == 0
    for i in range(L):
        assert res[i % len(res)] == walk[i], "point does not follow the walk"
    return x, A


def bfs_path(E, nodes, a, b):
    """Shortest path a -> b inside `nodes` (list of nodes, a first, b excluded
    unless a == b handled by caller)."""
    from collections import deque
    prev, dq = {a: None}, deque([a])
    while dq:
        x = dq.popleft()
        if x == b and x != a:
            break
        for y, _ in E[x]:
            if y in nodes and y not in prev:
                prev[y] = x
                dq.append(y)
    if b not in prev:
        return None
    path, y = [], b
    while y is not None:
        path.append(y)
        y = prev[y]
    return path[::-1]


def barrier_witness(p, m, table, K, x_exp, dmax=8):
    """Theorem N data.  x_exp: a rational expanding periodic point.  Returns
    (C, W, rows) where C is its residue cycle at level K, W a closed walk through
    C[0] in the same SCC that is not a power of C, and rows = [(d, y_d, lam_d)]
    for the periodic points of C^d W, all exact."""
    E = graph(p, m, table, K)
    C, lamC = orbit_residues(x_exp, p, m, table, K)
    assert lamC > 1
    comp = next(c for c in tarjan(list(range(p ** K)), E) if C[0] in c)
    cs = set(comp)
    cedges = set(zip(C, C[1:] + C[:1]))
    other = [(a, b) for a in comp for b, _ in E[a] if b in cs and (a, b) not in cedges]
    assert other, "SCC of C is a simple cycle (type b): Theorem N does not apply"
    a, b = other[0]
    P1 = bfs_path(E, cs, C[0], a) if a != C[0] else [C[0]]
    P2 = bfs_path(E, cs, b, C[0]) if b != C[0] else [C[0]]
    W = P1 + P2[:-1]            # closed walk C[0] -> ... -> a -> b -> ... -> C[0]
    rows = []
    for d in range(0, dmax + 1):
        walk = C * d + W
        y, lam = walk_point(p, m, table, K, walk)
        rows.append((d, y, lam))
    return C, lamC, W, rows


def integer_cycles_upto(p, m, table, L):
    """All T-cycles of positive integers whose period is <= L, exactly.

    Every periodic positive integer n of period l defines the closed walk of its
    residues in G_m, and is the unique fixed point x = B/(W - A) of the composed
    map (A x + B)/W along that walk (A != W because every closed walk contains a
    division and the multipliers are p-adic units).  So enumerating all closed
    walks of length <= L and keeping the positive-integer fixed points that
    really are periodic gives every cycle of period <= L.  Returns sorted list
    of cycle minima together with the number of walks examined."""
    Q = p ** m
    E = graph(p, m, table, m)
    T = step_fn(p, m, table)
    found = set()
    walks = 0
    for r0 in range(Q):
        # iterative DFS: (node, depth, A, B, W)
        stack = [(r0, 0, 1, 0, 1)]
        while stack:
            r, dpt, A, B, W = stack.pop()
            u, v, w = table[r % Q]
            A2, B2, W2 = A * u, B * u + v * W, W * w
            # careful: composed map is x -> (A x + B)/W ; next (u y + v)/w with
            # y = (A x + B)/W gives (u A x + u B + v W)/(W w)
            for s, _ in E[r]:
                d2 = dpt + 1
                if s == r0:
                    walks += 1
                    den = W2 - A2
                    if den != 0 and B2 % den == 0:
                        x = B2 // den
                        if x > 0 and x % Q == r0:
                            y, ok = x, True
                            for _ in range(d2):
                                y = T(y)
                            if y == x:
                                cyc = [x]
                                z = T(x)
                                while z != x:
                                    cyc.append(z)
                                    z = T(z)
                                found.add(min(cyc))
                if d2 < L:
                    stack.append((s, d2, A2, B2, W2))
    return sorted(found), walks
