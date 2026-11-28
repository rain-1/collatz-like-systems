"""Round 6, lens typeb_wide: exact tools for the SCC trichotomy and Theorem H.

System format (same as round3/accel/accel_lib.py): (p, m, table) with
table[r] = (u, v, w) for r in range(p**m): n = r (mod p^m) -> (u n + v)/w,
w = p^e, p does not divide u, u >= 1, w | u n + v on the whole class.

Main entry points
  classify(p, m, table, K=None)   exact SCC types (a)/(b)/(c)/trivial at level K (default m)
  prove_H(p, m, table, K=None)    the full Theorem-H proof object (dict of exact data) or None
  (the independent verifier is verify_H.py; it does not import this module)

Exactness: every verdict is backed by exact integer / Fraction data.
  type (b): a simple-cycle SCC with exact multiplier > 1;
  type (c): a non-simple SCC plus an exact closed walk in it with multiplier > 1;
  type (a): exact weights c(r) and theta < 1 with c(s) q <= theta c(r) on every internal edge;
  'unknown' is returned when the float search does not produce exact data (never seen in
  practice; it is counted separately in every table).
"""
from fractions import Fraction
import math


def val(n, p):
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e, n


def check_table(p, m, table):
    """Exact hypotheses: unit multipliers, w a power of p, divisibility on each class,
    and T(Z>0) in Z>0.  Returns the list of division exponents."""
    Q = p ** m
    assert len(table) == Q
    es = []
    for r in range(Q):
        u, v, w = table[r]
        assert u >= 1 and u % p != 0, (r, u)
        e, rest = val(w, p)
        assert rest == 1, (r, w)
        assert e <= m, (r, w)
        # divisibility on the whole class r + Q Z: u r + v = 0 mod w and u Q = 0 mod w
        assert (u * r + v) % w == 0 and (u * Q) % w == 0, r
        # positivity: smallest positive member of the class is r (or Q if r = 0);
        # the branch is increasing in n because u > 0
        n0 = r if r > 0 else Q
        assert u * n0 + v >= w, ("T does not keep Z>0", r)
        es.append(e)
    return es


def step_fn(p, m, table):
    Q = p ** m

    def T(n):
        u, v, w = table[n % Q]
        x = u * n + v
        assert x % w == 0
        return x // w
    return T


def graph(p, m, table, K):
    """G_K: dict r -> list of (s, u, e) (multiplier u / p^e)."""
    Q, PK = p ** m, p ** K
    E = []
    for r in range(PK):
        u, v, w = table[r % Q]
        e = val(w, p)[0]
        step = PK // w
        base = ((u * r + v) // w) % step
        E.append([(base + i * step, u, e) for i in range(w)])
    return E


def tarjan(N, succ):
    """Iterative Tarjan on nodes 0..N-1, succ[v] = list of node ids. Returns SCC list in
    reverse topological order (sinks first)."""
    index = [-1] * N
    low = [0] * N
    onst = [False] * N
    st, out = [], []
    c = 0
    for v0 in range(N):
        if index[v0] >= 0:
            continue
        work = [(v0, 0)]
        index[v0] = low[v0] = c
        c += 1
        st.append(v0)
        onst[v0] = True
        while work:
            v, i = work[-1]
            sv = succ[v]
            if i < len(sv):
                work[-1] = (v, i + 1)
                w = sv[i]
                if index[w] < 0:
                    index[w] = low[w] = c
                    c += 1
                    st.append(w)
                    onst[w] = True
                    work.append((w, 0))
                elif onst[w]:
                    if index[w] < low[v]:
                        low[v] = index[w]
            else:
                work.pop()
                if work:
                    u = work[-1][0]
                    if low[v] < low[u]:
                        low[u] = low[v]
                if low[v] == index[v]:
                    comp = []
                    while True:
                        w = st.pop()
                        onst[w] = False
                        comp.append(w)
                        if w == v:
                            break
                    out.append(comp)
    return out


def lam_gt1(p, U, e):
    """exact: U / p^e > 1 ?  (U = product of u's)"""
    return U > p ** e


def max_mean_cycle(comp, ed, lp):
    """Karp on the SCC, floats.  ed: list of (i, j, weight) with local indices.
    Returns (mu, cycle as list of local edge indices) - cycle extracted from the
    policy graph of the optimal walk (best effort; verified by caller)."""
    n = len(comp)
    NEG = float("-inf")
    D = [[NEG] * n for _ in range(n + 1)]
    P = [[-1] * n for _ in range(n + 1)]
    D[0] = [0.0] * n
    for k in range(1, n + 1):
        Dk, Dp, Pk = D[k], D[k - 1], P[k]
        for idx, (a, b, wt) in enumerate(ed):
            if Dp[a] != NEG and Dp[a] + wt > Dk[b]:
                Dk[b] = Dp[a] + wt
                Pk[b] = idx
    best, bv = NEG, -1
    for v in range(n):
        if D[n][v] == NEG:
            continue
        mv = min((D[n][v] - D[k][v]) / (n - k) for k in range(n) if D[k][v] != NEG)
        if mv > best:
            best, bv = mv, v
    # walk back from (n, bv) to find a repeated node: that segment is a cycle
    cyc = None
    if bv >= 0:
        seen, v, k, path = {}, bv, n, []
        while k > 0:
            if v in seen:
                j = seen[v]
                cyc = path[j:]
                break
            seen[v] = len(path)
            idx = P[k][v]
            path.append(idx)
            v = ed[idx][0]
            k -= 1
    return best, cyc


def find_expanding_cycle(comp, ed_exact, p):
    """Exact search for a closed walk with multiplier > 1 inside an SCC.
    ed_exact: list of (i, j, u, e).  Uses Karp to locate it, then checks exactly.
    Returns list of edge indices or None."""
    ed = [(a, b, math.log(u) - e * math.log(p)) for a, b, u, e in ed_exact]
    mu, cyc = max_mean_cycle(comp, ed, p)
    if cyc and mu > 0:
        U, e = 1, 0
        for i in cyc:
            U *= ed_exact[i][2]
            e += ed_exact[i][3]
        if U > p ** e:
            return cyc[::-1]
    # fallback: Bellman-Ford longest paths; a node still relaxing after n rounds leads,
    # through predecessor pointers, to a cycle of positive weight (checked exactly)
    n = len(comp)
    for shift in (0.0, mu / 4 if mu > 0 else 0.0, mu / 2 if mu > 0 else 0.0):
        dist = [0.0] * n
        pred = [-1] * n
        last = -1
        for _ in range(n + 1):
            last = -1
            for idx, (a, b, wt) in enumerate(ed):
                if dist[a] + wt - shift > dist[b] + 1e-13:
                    dist[b] = dist[a] + wt - shift
                    pred[b] = idx
                    last = b
            if last < 0:
                break
        if last < 0:
            continue
        v = last
        for _ in range(n):
            v = ed[pred[v]][0]
        cyc, x = [], v
        while True:
            idx = pred[x]
            cyc.append(idx)
            x = ed[idx][0]
            if x == v:
                break
        U, e = 1, 0
        for i in cyc:
            U *= ed_exact[i][2]
            e += ed_exact[i][3]
        if U > p ** e:
            return cyc[::-1]
    return None


def contraction_weights(comp, ed_exact, p):
    """Exact (theta, c) with c[j] * u/p^e <= theta * c[i] on every internal edge
    (i -> j), c > 0, theta < 1.  None if not found."""
    ed = [(a, b, math.log(u) - e * math.log(p)) for a, b, u, e in ed_exact]
    mu, _ = max_mean_cycle(comp, ed, p)
    if not mu < -1e-12:
        return None
    n = len(comp)
    for frac in (0.5, 0.3, 0.7, 0.15, 0.85, 0.05):
        lt = mu * frac
        theta = Fraction(math.exp(lt * 0.5)).limit_denominator(10 ** 6)
        if not theta < 1:
            continue
        phi = [0.0] * n
        for _ in range(n + 2):
            ch = False
            for a, b, wt in ed:
                x = phi[a] + wt - lt
                if x > phi[b] + 1e-15:
                    phi[b] = x
                    ch = True
            if not ch:
                break
        mx = max(phi)
        c = [Fraction(math.exp(mx - x)).limit_denominator(10 ** 9) for x in phi]
        if all(x > 0 for x in c) and all(c[b] * Fraction(u, p ** e) <= theta * c[a]
                                         for a, b, u, e in ed_exact):
            return theta, c
    return None


def classify(p, m, table, K=None, weights=True):
    """Exact SCC classification of G_K.  Returns dict:
       comps: list of dicts (kind in trivial / a / b / c / unknown / neutral),
       E: graph, types: set of kinds, divfree: True if some cycle of G_K has no division
       (standing hypothesis fails; then kind 'neutral' or 'divfree' is reported)."""
    if K is None:
        K = m
    N = p ** K
    E = graph(p, m, table, K)
    succ = [[s for s, _, _ in E[r]] for r in range(N)]
    comps = tarjan(N, succ)
    cid = [0] * N
    for i, c in enumerate(comps):
        for v in c:
            cid[v] = i
    out = []
    divfree = False
    for i, comp in enumerate(comps):
        loc = {v: j for j, v in enumerate(comp)}
        ed = [(loc[r], loc[s], u, e) for r in comp for s, u, e in E[r] if cid[s] == i]
        if not ed:
            out.append(dict(kind="trivial", nodes=comp))
            continue
        # division-free cycle inside this SCC?  (sub-graph of e = 0 edges has a cycle)
        z = [[] for _ in comp]
        for a, b, u, e in ed:
            if e == 0:
                z[a].append(b)
        zc = tarjan(len(comp), z)
        if any(len(c) > 1 or c[0] in z[c[0]] for c in zc):
            divfree = True
            out.append(dict(kind="divfree", nodes=comp))
            continue
        if len(ed) == len(comp):
            # each node has exactly one internal out-edge: a single simple cycle
            nxt = {a: (b, u, e) for a, b, u, e in ed}
            seq, U, ee, a = [0], 1, 0, 0
            while True:
                b, u, e = nxt[a]
                U *= u
                ee += e
                if b == 0:
                    break
                seq.append(b)
                a = b
            assert len(seq) == len(comp)
            cyc = [comp[j] for j in seq]
            kind = "b" if U > p ** ee else "a"
            out.append(dict(kind=kind, nodes=comp, simple=True, cycle=cyc, U=U, e=ee))
            continue
        edf = [(a, b, math.log(u) - e * math.log(p)) for a, b, u, e in ed]
        mu, _ = max_mean_cycle(comp, edf, p)
        xc = find_expanding_cycle(comp, ed, p) if mu > 0 else None
        if xc is not None:
            walk = [comp[ed[j][0]] for j in xc]
            out.append(dict(kind="c", nodes=comp, walk=walk, nedges=len(ed)))
            continue
        if mu > -1e-9:
            out.append(dict(kind="unknown", nodes=comp, nedges=len(ed), mu=mu))
            continue
        if not weights:
            out.append(dict(kind="a", nodes=comp, simple=False, nedges=len(ed), mu=mu,
                            unweighted=True))
            continue
        cw = contraction_weights(comp, ed, p)
        if cw is None:
            out.append(dict(kind="unknown", nodes=comp, nedges=len(ed)))
        else:
            theta, c = cw
            out.append(dict(kind="a", nodes=comp, simple=False, theta=theta,
                            c={comp[j]: c[j] for j in range(len(comp))}, nedges=len(ed)))
    types = set(c["kind"] for c in out)
    return dict(p=p, m=m, K=K, E=E, comps=out, cid=cid, types=types, divfree=divfree)


def verdict(cl):
    t = cl["types"]
    if "divfree" in t:
        return "divfree"
    if "c" in t:
        return "c"
    if "unknown" in t or "a?" in t:
        return "unknown"
    if "b" in t:
        return "b"
    return "a"


def compose(p, m, table, cyc):
    """(A, B) exact with T^len(cyc) = A x + B along the residue sequence cyc."""
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


def dag_levels(cl):
    """lev[i] for SCC i: 0 for sinks, else 1 + max over successor SCCs."""
    comps, cid, E = cl["comps"], cl["cid"], cl["E"]
    lev = [0] * len(comps)
    # tarjan returns sinks first: successors of SCC i have index < i
    for i, c in enumerate(comps):
        L = 0
        for r in c["nodes"]:
            for s, _, _ in E[r]:
                j = cid[s]
                if j != i:
                    assert j < i
                    L = max(L, lev[j] + 1)
        lev[i] = L
    return lev


def cycle_of(T, n, cap=10 ** 6):
    seen, y = {}, n
    while y not in seen:
        seen[y] = 1
        y = T(y)
        assert len(seen) < cap
    cyc, z = [y], T(y)
    while z != y:
        cyc.append(z)
        z = T(z)
    k = cyc.index(min(cyc))
    return cyc[k:] + cyc[:k]


def prove_H(p, m, table, K=None, cap=10 ** 7):
    """Theorem-H proof object, or None if some SCC is not (a)/(b)/trivial.
    Every number in it is exact (ints / Fractions); verify_H.py re-checks it."""
    check_table(p, m, table)
    if K is None:
        K = m
    cl = classify(p, m, table, K)
    if verdict(cl) not in ("a", "b"):
        return None
    T = step_fn(p, m, table)
    PK = p ** K
    lev = dag_levels(cl)
    Q = p ** m
    comps_out, cycles = [], {}
    for i, c in enumerate(cl["comps"]):
        rec = dict(id=i, kind=c["kind"], nodes=sorted(c["nodes"]), level=lev[i])
        if c["kind"] == "trivial":
            comps_out.append(rec)
            continue
        if c.get("simple"):
            A, B = compose(p, m, table, c["cycle"])
            x = B / (1 - A)
            assert padic_residue(x, p, K) == c["cycle"][0]
            # the whole periodic orbit x_0 .. x_{l-1}, exact
            pts, y = [], x
            for r in c["cycle"]:
                assert padic_residue(y, p, K) == r
                pts.append(y)
                u, v, w = table[r % Q]
                y = (u * y + v) / w
            assert y == x
            rec.update(cycle=c["cycle"], A=A, B=B, xstar=pts)
            if x.denominator == 1 and x > 0:
                cyc = cycle_of(T, int(x))
                cycles[min(cyc)] = cyc
                rec["integer_cycle"] = True
            else:
                rec["integer_cycle"] = False
            if c["kind"] == "a":
                # contracting simple cycle: |T^l n - x| = A |n - x|, so an integer orbit that
                # stays forever converges to x and is eventually equal to x.
                pass
            comps_out.append(rec)
            continue
        # contracting non-simple SCC: weights
        theta, w = c["theta"], c["c"]
        beta = Fraction(0)
        for r in c["nodes"]:
            u, v, ww = table[r % Q]
            for s, _, _ in cl["E"][r]:
                if s in w:
                    beta = max(beta, w[s] * Fraction(max(v, 0), ww))
        Vmax = beta / (1 - theta)
        cmin = min(w.values())
        nmax = math.floor(Vmax / cmin)
        assert nmax <= cap, ("search bound too large", nmax)
        found = []
        nodes = set(c["nodes"])
        for n in range(1, nmax + 1):
            r = n % PK
            if r in nodes and w[r] * n <= Vmax:
                cyc = cycle_of(T, n)
                if cyc[0] not in cycles:
                    cycles[cyc[0]] = cyc
                found.append(n)
        rec.update(theta=theta, c={r: w[r] for r in sorted(w)}, beta=beta, Vmax=Vmax, nmax=nmax,
                   ncand=len(found))
        comps_out.append(rec)
    return dict(p=p, m=m, K=K, table=[list(t) for t in table], comps=comps_out,
                cycles=[cycles[k] for k in sorted(cycles)],
                verdict=verdict(cl))


def fmt_rule(p, m, table):
    groups = {}
    Q = p ** m
    for r, t in enumerate(table):
        groups.setdefault(tuple(t), []).append(r)
    parts = []
    for (u, v, w), rs in sorted(groups.items(), key=lambda kv: kv[1][0]):
        num = (f"{u}n" if u != 1 else "n") + (f"+{v}" if v > 0 else (f"{v}" if v < 0 else ""))
        f = num if w == 1 else f"({num})/{w}"
        parts.append(f"{{{','.join(map(str, rs))}}} -> {f}")
    return f"mod {Q}: " + "; ".join(parts)


def to_json(P, name=""):
    """Serializable copy of a prove_H object (Fractions as strings)."""
    def conv(x):
        if isinstance(x, Fraction):
            return str(x)
        if isinstance(x, dict):
            return {str(k): conv(v) for k, v in x.items()}
        if isinstance(x, (list, tuple)):
            return [conv(v) for v in x]
        return x
    out = conv(P)
    out["name"] = name
    return out
