"""traps_lib: avoider graphs, SCC certificates and homoclinic obstructions.

A *2-adic affine map* T is given by beta and a list of 2**beta branches
(a, b, e): for n = i (mod 2**beta),  T(n) = (a*n + b) / 2**e,
with a odd, 2**e | a*i + b and e <= beta (so the division is exact on
the whole class, and T extends continuously to Z_2).

A *trap set* is a set A of residues mod 2**k.  The statement under study:

    S(T, A):  every positive integer orbit meets A (some iterate is = a
              (mod 2**k), a in A) or is eventually periodic, and the
              cycles of the second kind form an explicit finite list.

Everything that is used in a proof is computed with Python integers or
Fractions.  Floating point is used only to *search* (to guess a
positive cycle or a value of Q); every guess is re-verified exactly.
"""
from fractions import Fraction
import math
import sys

sys.setrecursionlimit(100000)


# ----------------------------------------------------------------- maps
class AffMap:
    def __init__(self, name, beta, branches):
        self.name = name
        self.beta = beta
        self.mod = 1 << beta
        assert len(branches) == self.mod
        self.br = [tuple(x) for x in branches]
        for i, (a, b, e) in enumerate(self.br):
            assert a % 2 == 1 and a > 0, "multipliers must be odd positive"
            assert e <= beta
            assert (a * i + b) % (1 << e) == 0, (i, a, b, e)

    def step(self, n):
        a, b, e = self.br[n % self.mod]
        y = a * n + b
        assert y % (1 << e) == 0
        return y >> e

    def step_q(self, x):
        """exact step on a 2-adic rational (Fraction with odd denominator)"""
        a, b, e = self.br[res(x, self.beta)]
        y = (a * x + b) / Fraction(1 << e)
        assert y.denominator % 2 == 1
        return y

    def preimages_q(self, y):
        out = []
        for i, (a, b, e) in enumerate(self.br):
            n = (Fraction(1 << e) * y - b) / a
            if res(n, self.beta) == i:
                out.append(n)
        return out


def res(x, m):
    """x mod 2**m for an int or a Fraction with odd denominator"""
    M = 1 << m
    if isinstance(x, int):
        return x % M
    x = Fraction(x)
    q = x.denominator
    assert q % 2 == 1
    return (x.numerator * pow(q, -1, M)) % M


def v2(x):
    if x == 0:
        return 10 ** 9
    x = Fraction(x)
    p = abs(x.numerator)
    return (p & -p).bit_length() - 1


def collatz_a(a, shortcut=False, b=1):
    """C_{a,b}: n/2 (even), a n + b (odd);  shortcut: (a n + b)/2 (odd)."""
    nm = f"{a}" if b == 1 else f"{a},{b}"
    if shortcut:
        return AffMap(f"T{nm}", 1, [(1, 0, 1), (a, b, 1)])
    return AffMap(f"C{nm}", 1, [(1, 0, 1), (a, b, 0)])


# ---------------------------------------------------------------- graph
def build_graph(T, m, A, k):
    """Avoider graph G_m^A.  Nodes: residues r mod 2**m with r mod 2**k not
    in A.  Edges r -> s whenever some n = r (mod 2**m) has T(n) = s (mod
    2**m).  Returns (nodes, adj) with adj[r] = list of (s, branch)."""
    assert m >= T.beta and m >= k
    M = 1 << m
    Ak = set(a % (1 << k) for a in A)
    good = [((r % (1 << k)) not in Ak) for r in range(M)]
    adj = {}
    for r in range(M):
        if not good[r]:
            continue
        i = r % T.mod
        a, b, e = T.br[i]
        y = a * r + b
        assert y % (1 << e) == 0
        base = (y >> e) % (1 << (m - e))
        lst = []
        for j in range(1 << e):
            s = base + (j << (m - e))
            if good[s]:
                lst.append((s, i))
        adj[r] = lst
    return adj


def tarjan(adj):
    """iterative Tarjan; returns list of SCCs (lists of nodes) in reverse
    topological order (sinks first)."""
    index = {}
    low = {}
    onst = set()
    st = []
    out = []
    c = 0
    for v0 in adj:
        if v0 in index:
            continue
        work = [(v0, 0)]
        index[v0] = low[v0] = c; c += 1
        st.append(v0); onst.add(v0)
        while work:
            v, pi = work[-1]
            nb = adj[v]
            if pi < len(nb):
                work[-1] = (v, pi + 1)
                w = nb[pi][0]
                if w not in index:
                    index[w] = low[w] = c; c += 1
                    st.append(w); onst.add(w)
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
                        w = st.pop(); onst.discard(w)
                        comp.append(w)
                        if w == v:
                            break
                    out.append(comp)
    return out


def internal_edges(adj, comp):
    cs = set(comp)
    return [(u, s, i) for u in comp for (s, i) in adj[u] if s in cs]


# ------------------------------------------------------ cycle machinery
def lift_cycle(T, m, cyc):
    """cyc = [r0, r1, ..., r_{L-1}] closed walk in G_m (r_{L} = r0).
    Returns the unique 2-adic point x* = r0 (mod 2**m) following it,
    with T^L(x*) = x*, plus multiplier (A, E) = (prod a, sum e)."""
    Acoef, c, E = 1, 0, 0  # value = (Acoef*x + c) / 2^E
    for r in cyc:
        a, b, e = T.br[r % T.mod]
        Acoef, c, E = a * Acoef, a * c + b * (1 << E), E + e
    assert E >= 1
    x = Fraction(c, (1 << E) - Acoef)
    # exact verification: x follows the residues and returns
    y = x
    for r in cyc:
        assert res(y, m) == r % (1 << m), "lift does not follow the cycle"
        y = T.step_q(y)
    assert y == x
    return x, Acoef, E


def orbit_q(T, x, L):
    o = [x]
    for _ in range(L - 1):
        o.append(T.step_q(o[-1]))
    assert T.step_q(o[-1]) == x
    return o


def find_positive_cycle(T, adj, comp):
    """float Bellman-Ford (search only) for a cycle with product of
    multipliers > 1 inside comp; returns the node list of the cycle,
    verified exactly, or None."""
    edges = internal_edges(adj, comp)
    if not edges:
        return None
    w = {}
    for (u, s, i) in edges:
        a, b, e = T.br[i]
        w[(u, s)] = max(w.get((u, s), -1e18), math.log2(a) - e)
    dist = {u: 0.0 for u in comp}
    pred = {u: None for u in comp}
    n = len(comp)
    last = None
    for it in range(n + 1):
        last = None
        for (u, s), ww in w.items():
            if dist[u] + ww > dist[s] + 1e-12:
                dist[s] = dist[u] + ww
                pred[s] = u
                last = s
        if last is None:
            return None
    # walk back n steps to land on a cycle
    x = last
    for _ in range(n):
        x = pred[x]
    cyc = [x]
    y = pred[x]
    while y != x:
        cyc.append(y)
        y = pred[y]
    cyc.reverse()  # now cyc[j] -> cyc[j+1]
    num = 1; E = 0
    for r in cyc:
        a, b, e = T.br[r % T.mod]
        num *= a; E += e
    if num > (1 << E):
        return cyc
    return None


def contract_potential(T, adj, comp, Qs=(16, 64, 256, 1024, 4096, 16384)):
    """Try to build an integer potential phi on comp with
        phi(u) >= phi(v) + P_a - Q e + 1   for every internal edge u->v
    where a^Q < 2^{P_a}.  Returns (Q, P, phi) or None."""
    edges = internal_edges(adj, comp)
    mults = sorted(set(T.br[i][0] for (_, _, i) in edges))
    for Q in Qs:
        P = {}
        for a in mults:
            if a == 1:
                P[a] = 0
            else:
                p = int(Q * math.log2(a)) + 1
                while a ** Q >= (1 << p):
                    p += 1
                P[a] = p
        W = {}
        for (u, s, i) in edges:
            a, b, e = T.br[i]
            ww = P[a] - Q * e + 1
            W[(u, s)] = max(W.get((u, s), -10 ** 18), ww)
        phi = {u: 0 for u in comp}
        ok = False
        for it in range(len(comp) + 2):
            ch = False
            for (u, s), ww in W.items():
                if phi[s] + ww > phi[u]:
                    phi[u] = phi[s] + ww
                    ch = True
            if not ch:
                ok = True
                break
        if ok:
            return Q, P, phi
    return None


def verify_potential(T, adj, comp, Q, P, phi):
    for a, p in P.items():
        assert (a ** Q < (1 << p)) or (a == 1 and p == 0)
    cs = set(comp)
    for u in comp:
        for (s, i) in adj[u]:
            if s in cs:
                a, b, e = T.br[i]
                assert phi[u] >= phi[s] + P[a] - Q * e + 1, (u, s)
    return True


def bound_B(T, comp_branches, Q):
    """least B >= 1 (searched upward from an estimate) with
    (a(B+1)+|b|)^Q < 2 (a(B+1))^Q for all branches used."""
    B = 1
    for i in comp_branches:
        a, b, e = T.br[i]
        if b == 0:
            continue
        lo = max(1, int(abs(b) * Q / (a * 0.6931)) - 2)
        while not ((a * (lo + 1) + abs(b)) ** Q < 2 * (a * (lo + 1)) ** Q):
            lo += 1
        B = max(B, lo)
    return B


# ---------------------------------------------------------- the method
def scc_method(T, A, k, m, want_cert=False):
    """Apply the SCC criterion at level m.
    Returns dict with 'ok' and either the certificate or the bad SCCs."""
    adj = build_graph(T, m, A, k)
    comps = tarjan(adj)
    info = []
    bad = []
    for comp in comps:
        ie = internal_edges(adj, comp)
        if not ie:
            info.append(("trivial", comp, None))
            continue
        outdeg = {u: 0 for u in comp}
        for (u, s, i) in ie:
            outdeg[u] += 1
        if all(d == 1 for d in outdeg.values()):
            # simple cycle: order it
            nxt = {u: s for (u, s, i) in ie}
            c0 = comp[0]; cyc = [c0]; y = nxt[c0]
            while y != c0:
                cyc.append(y); y = nxt[y]
            x, num, E = lift_cycle(T, m, cyc)
            info.append(("simple", comp, (cyc, x, num, E)))
            continue
        pc = find_positive_cycle(T, adj, comp)
        if pc is not None:
            bad.append((comp, pc))
            info.append(("expanding", comp, pc))
            continue
        pot = contract_potential(T, adj, comp)
        if pot is None:
            bad.append((comp, None))
            info.append(("unknown", comp, None))
            continue
        info.append(("contracting", comp, pot))
    return {"ok": not bad, "adj": adj, "comps": comps, "info": info, "bad": bad}


def pure_test(T, A, k, m=None):
    """P0 test: all cycles of G_m^A contracting (m = max(k, beta) by
    default; by the dichotomy theorem the answer does not depend on m).
    Returns (True, None) or (False, expanding cycle)."""
    if m is None:
        m = max(k, T.beta)
    adj = build_graph(T, m, A, k)
    for comp in tarjan(adj):
        if not internal_edges(adj, comp):
            continue
        pc = find_positive_cycle(T, adj, comp)
        if pc is not None:
            return False, (m, pc)
    return True, None


def simulate_fates(T, A, k, B, cap=10 ** 7):
    """For every 1 <= n <= B: follow the orbit until it meets A or repeats.
    Returns (cycles avoiding A, number trapped).  Exact integers."""
    Mk = 1 << k
    Ak = set(a % Mk for a in A)
    fate = {}
    cycles = set()
    steps = 0
    for n0 in range(1, B + 1):
        path = []
        pos = {}
        x = n0
        while True:
            if x in fate:
                f = fate[x]; break
            if x % Mk in Ak:
                f = "A"; fate[x] = f; break
            if x in pos:
                cyc = path[pos[x]:]
                mn = min(cyc)
                i = cyc.index(mn)
                f = tuple(cyc[i:] + cyc[:i])
                cycles.add(f)
                for y in cyc:
                    fate[y] = f
                break
            pos[x] = len(path); path.append(x)
            x = T.step(x)
            steps += 1
            if steps > cap:
                raise RuntimeError("simulation cap exceeded")
        for y in path:
            if y not in fate:
                fate[y] = f
    trapped = sum(1 for n in range(1, B + 1) if fate[n] == "A")
    return sorted(cycles), trapped


def certificate(T, A, k, mmax=14, mmin=None, verbose=False):
    """Run the SCC method at levels mmin..mmax; on success return a full
    certificate dict (verified)."""
    if mmin is None:
        mmin = max(k, T.beta)
    for m in range(mmin, mmax + 1):
        r = scc_method(T, A, k, m)
        if r["ok"]:
            return finish_certificate(T, A, k, m, r)
        if verbose:
            print("level", m, "bad SCCs", [len(c) for c, _ in r["bad"]])
    return None


def finish_certificate(T, A, k, m, r):
    adj = r["adj"]
    B = 1
    comps = []
    simple_pts = []
    for kind, comp, data in r["info"]:
        if kind == "contracting":
            Q, P, phi = data
            verify_potential(T, adj, comp, Q, P, phi)
            brs = set(i for (_, _, i) in internal_edges(adj, comp))
            B = max(B, bound_B(T, brs, Q))
            comps.append(("contracting", comp, (Q, P, phi)))
        elif kind == "simple":
            cyc, x, num, E = data
            simple_pts.append((x, num, E, len(cyc)))
            comps.append(("simple", comp, data))
        else:
            comps.append((kind, comp, None))
    cycles, trapped = simulate_fates(T, A, k, B)
    # a simple component whose periodic point is a positive integer is a
    # genuine cycle: add it (never happens for expanding ones)
    extra = []
    for (x, num, E, L) in simple_pts:
        if x.denominator == 1 and x > 0:
            extra.append(int(x))
            cyc = [int(x)]
            y = T.step(int(x))
            while y != cyc[0]:
                cyc.append(y); y = T.step(y)
            i = cyc.index(min(cyc))
            c = tuple(cyc[i:] + cyc[:i])
            if c not in cycles:
                cycles = sorted(set(cycles) | {c})
    return {"map": T.name, "A": sorted(A), "k": k, "m": m, "B": B,
            "cycles": cycles, "trapped_le_B": trapped,
            "simple_points": simple_pts, "extra_int_points": extra,
            "ncomp": len(r["comps"]),
            "kinds": {kd: sum(1 for c in comps if c[0] == kd)
                      for kd in ("contracting", "simple", "trivial")},
            "comps": comps}


# ------------------------------------------------- homoclinic witnesses
def homoclinic(T, A, k, x0, L, maxnodes=200000, maxdepth=60):
    """x0: expanding periodic avoider point of period L.  Search backward
    from its orbit for z with: z not on the orbit, orbit of z avoids A,
    T^j(z) on the orbit, and z = x_i (mod 2**m0) for some orbit point x_i,
    m0 = max(k, beta).  Returns (z, j, i) or None."""
    m0 = max(k, T.beta)
    Mk = 1 << k
    Ak = set(a % Mk for a in A)
    orb = orbit_q(T, x0, L)
    orbset = set(orb)
    resid = {}
    for i, x in enumerate(orb):
        resid.setdefault(res(x, m0), i)
    frontier = [(x, 0) for x in orb]
    seen = set(orb)
    count = 0
    while frontier:
        nf = []
        for (y, d) in frontier:
            if d >= maxdepth:
                continue
            for z in T.preimages_q(y):
                if z in seen:
                    continue
                if res(z, k) in Ak:
                    continue
                seen.add(z)
                count += 1
                r0 = res(z, m0)
                if r0 in resid:
                    return z, d + 1, resid[r0]
                nf.append((z, d + 1))
                if count > maxnodes:
                    return None
        # prefer small denominators/heights: sort by height
        nf.sort(key=lambda t: abs(t[0].numerator) + t[0].denominator)
        frontier = nf
    return None


def verify_homoclinic(T, A, k, x0, L, z, j, i):
    """exact check of a homoclinic witness (see homoclinic())."""
    m0 = max(k, T.beta)
    Mk = 1 << k
    Ak = set(a % Mk for a in A)
    orb = orbit_q(T, x0, L)
    # x0 expanding
    num, E = 1, 0
    for x in orb:
        a, b, e = T.br[res(x, T.beta)]
        num *= a; E += e
    assert num > (1 << E)
    for x in orb:
        assert res(x, k) not in Ak
    assert z not in set(orb)
    assert res(z, m0) == res(orb[i], m0)
    y = z
    for t in range(j):
        assert res(y, k) not in Ak
        assert y not in set(orb) or t > 0
        y = T.step_q(y)
    assert y in set(orb)
    # z itself not on the orbit (checked), and the path reaches the orbit
    return True


def composite(T, x, L):
    """coefficients (num, c, E) with T^L(y) = (num*y + c)/2^E for all y
    following the branches of x for L steps"""
    num, c, E = 1, 0, 0
    y = x
    for _ in range(L):
        a, b, e = T.br[res(y, T.beta)]
        num, c, E = a * num, a * c + b * (1 << E), E + e
        y = T.step_q(y)
    return num, c, E


def upgrade_witness(T, x0, L, z, i, K):
    """Replace z by g^u(z) (g = local inverse of T^L along orb[i]) until
    z = orb[i] (mod 2^K).  Returns (z', path) where path is the exact orbit
    of z' up to and including its first point on the orbit of x0."""
    orb = orbit_q(T, x0, L)
    base = orb[i]
    num, c, E = composite(T, base, L)
    zz = z
    while v2(zz - base) < K:
        w = (Fraction(1 << E) * zz - c) / num
        # w must follow base's branches for L steps and land on zz
        y = w
        for t in range(L):
            assert res(y, T.beta) == res(orb[(i + t) % L], T.beta)
            y = T.step_q(y)
        assert y == zz
        zz = w
    orbset = set(orb)
    path = [zz]
    y = zz
    while y not in orbset:
        y = T.step_q(y)
        path.append(y)
        assert len(path) < 10 ** 5
    assert zz not in orbset
    return zz, path


def witness_residues(T, x0, L, path, K):
    orb = orbit_q(T, x0, L)
    return frozenset(res(x, K) for x in orb + path)


# ---------------- Theorem 4: a non-simple expanding SCC gives a homoclinic orbit
def _bfs_path(adj, comp_set, src, dst_pred):
    """shortest path (list of nodes) inside comp from src to a node v with
    dst_pred(v) true (path of length >= 0)."""
    from collections import deque
    prev = {src: None}
    dq = deque([src])
    while dq:
        u = dq.popleft()
        if dst_pred(u):
            p = [u]
            while prev[p[-1]] is not None:
                p.append(prev[p[-1]])
            return p[::-1]
        for (s, i) in adj[u]:
            if s in comp_set and s not in prev:
                prev[s] = u
                dq.append(s)
    return None


def simple_expanding_cycle(T, adj, comp):
    """an expanding *simple* cycle inside comp (exactly verified)."""
    pc = find_positive_cycle(T, adj, comp)
    if pc is None:
        return None
    # decompose the closed walk into simple cycles; one of them expands
    walk = pc
    stack = []
    pos = {}
    cycles = []
    for v in walk + walk[:1]:
        if v in pos:
            j = pos[v]
            cyc = stack[j:]
            cycles.append(cyc)
            for w in cyc:
                del pos[w]
            stack = stack[:j]
        pos[v] = len(stack)
        stack.append(v)
    for cyc in cycles:
        num, E = 1, 0
        for r in cyc:
            a, b, e = T.br[r % T.mod]
            num *= a; E += e
        if num > (1 << E):
            assert len(set(cyc)) == len(cyc)
            return cyc
    raise AssertionError("no expanding simple cycle in decomposition")


def lift_walk_to(T, m, walk, target):
    """walk = [w0, ..., w_l] (l >= 1 edges) in G_m; returns the unique
    2-adic w following the walk with T^l(w) = target (target must be
    = w_l mod 2^m)."""
    num, c, E = 1, 0, 0
    for r in walk[:-1]:
        a, b, e = T.br[r % T.mod]
        num, c, E = a * num, a * c + b * (1 << E), E + e
    w = (Fraction(1 << E) * target - c) / num
    y = w
    for r in walk[:-1]:
        assert res(y, m) == r
        y = T.step_q(y)
    assert res(y, m) == walk[-1] and y == target
    return w


def homoclinic_from_scc(T, A, k, m, adj, comp):
    """Constructive proof of Theorem 4.  comp: a non-simple SCC of G_m^A
    with an expanding cycle.  Returns (x*, L, z, j, i) with z homoclinic."""
    cs = set(comp)
    C1 = simple_expanding_cycle(T, adj, comp)
    x, num, E = lift_cycle(T, m, C1)
    r0 = C1[0]
    u = None
    for v in comp:
        if sum(1 for (s, i) in adj[v] if s in cs) >= 2:
            u = v; break
    assert u is not None
    P = _bfs_path(adj, cs, r0, lambda v: v == u)
    for (s, i) in adj[u]:
        if s not in cs:
            continue
        Q = _bfs_path(adj, cs, s, lambda v: v == r0)
        W = P + Q  # closed walk r0 -> ... -> u -> s -> ... -> r0
        if len(W) < 2:
            continue
        w = lift_walk_to(T, m, W, x)
        orb = orbit_q(T, x, len(C1))
        if w in set(orb):
            continue  # this branch reproduces the cycle; the other works
        return x, len(C1), w, len(W) - 1, 0
    raise AssertionError("Theorem 4 construction failed")
