"""twlib.py -- one harness for table maps  T(n) = (u_r n + v_r)/w_r  on classes r mod Q.

Round 6, lens "decision procedure and trichotomy, applied to everything".

Input: a modulus Q and table[r] = (u, v, w) for r in range(Q), integers with u >= 1, w >= 1,
and T integral on every class: w | u r + v and w | u Q.  No unit hypothesis is assumed here;
when (H1) gcd(u, Q) = 1 and (H2) w | Q hold the map is *Markov* and the full theory of
round 3 applies (decide.py, Theorems H, N, T, Lundberg exponents).

What `analyse` returns (all verdicts exact; floats only for searching and for the exponents):

  hyp        which of H1, H2, P hold
  decide     decide.py verdict (CERT/OBST, k*, cycle list) when H1, H2, P hold
  levels     for each level K (a multiple of Q with the same primes): the SCC types of the
             level-K residue graph (exact), see `classify_level`
  H          the verdict of Theorem H' (theory.md) at the first level that has no type (c)
             SCC: complete cycle list, or a proved divergent class
  theta1, theta_run, gap, drift  (floats, Markov maps only; round4/lundberg)

The level-K residue graph G_K: nodes r mod K; for n = r + K t one has
T(n) = y0 + k t with y0 = (u r + v)/w, k = u K / w, so T(n) mod K runs over the residues
y0 + g j (g = gcd(k, K)).  These are the out-edges of r; each carries the multiplier u/w.
Every residue walk of an orbit is a walk of G_K (this needs no hypothesis).  Under H1, H2
the graph is Markov (round3/dichotomy Lemma 1); otherwise it only over-approximates.
"""
from fractions import Fraction
import math
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(CENSUS, "round3", "dichotomy"))
import decide as D  # noqa: E402

sys.setrecursionlimit(100000)


# ----------------------------------------------------------------------------- basics

def primes_of(n):
    out, p = [], 2
    while p * p <= n:
        if n % p == 0:
            out.append(p)
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        out.append(n)
    return out


def check_table(Q, table):
    """Integrality on every class and u, w >= 1.  Raises AssertionError."""
    assert len(table) == Q
    for r, (u, v, w) in enumerate(table):
        assert u >= 1 and w >= 1, ("u,w>=1", r)
        assert (u * r + v) % w == 0 and (u * Q) % w == 0, ("integral", r)


def hypotheses(Q, table, zero=False):
    """zero=True: the domain is N0 = {0, 1, 2, ...} and (P) means T(N0) in N0."""
    h1 = all(math.gcd(u, Q) == 1 for (u, v, w) in table)
    h2 = all(Q % w == 0 for (u, v, w) in table)
    pos = True
    for r, (u, v, w) in enumerate(table):
        n0 = r if (r > 0 or zero) else Q
        if (u * n0 + v) // w < (0 if zero else 1):   # T is increasing on each class (u >= 1)
            pos = False
    return dict(H1=h1, H2=h2, P=pos, markov=h1 and h2)


def step_fn(Q, table):
    def T(n):
        u, v, w = table[n % Q]
        x = u * n + v
        assert x % w == 0
        return x // w
    return T


def lift(Q, table, K):
    assert K % Q == 0
    return [table[r % Q] for r in range(K)]


def graph(Q, table, K):
    """succ[r] for r mod K (exact over-approximation; exact image set under H1/H2)."""
    assert K % Q == 0
    succ = []
    for r in range(K):
        u, v, w = table[r % Q]
        y0 = (u * r + v) // w
        k = (u * K) // w
        g = math.gcd(k, K)
        b = y0 % g
        succ.append([b + g * j for j in range(K // g)])
    return succ


def tarjan(N, succ):
    index = [-1] * N
    low = [0] * N
    onst = [False] * N
    st, comps, c = [], [], 0
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
            if i < len(succ[v]):
                work[-1] = (v, i + 1)
                w = succ[v][i]
                if index[w] < 0:
                    index[w] = low[w] = c
                    c += 1
                    st.append(w)
                    onst[w] = True
                    work.append((w, 0))
                elif onst[w]:
                    low[v] = min(low[v], index[w])
            else:
                work.pop()
                if work:
                    low[work[-1][0]] = min(low[work[-1][0]], low[v])
                if low[v] == index[v]:
                    comp = []
                    while True:
                        w = st.pop()
                        onst[w] = False
                        comp.append(w)
                        if w == v:
                            break
                    comps.append(comp)
    return comps


def mult_of(Q, table, r):
    u, v, w = table[r % Q]
    return u, w


def walk_UW(Q, table, cyc):
    U = W = 1
    for r in cyc:
        u, w = mult_of(Q, table, r)
        U *= u
        W *= w
    return U, W


def walk_map(Q, table, cyc):
    """Composition of the branches along cyc: x -> (A x + B)/Dn (exact rationals)."""
    A, B, Dn = 1, 0, 1
    for r in cyc:
        u, v, w = table[r % Q]
        A, B, Dn = u * A, u * B + v * Dn, Dn * w
    g = math.gcd(math.gcd(A, B), Dn)
    return A // g, B // g, Dn // g


# ----------------------------------------------------------------------------- SCC analysis

def internal(comp, succ):
    S = set(comp)
    return {r: [s for s in succ[r] if s in S] for r in comp}


def karp(comp, E, wt):
    """Max mean cycle (floats) of edge weight wt[r] (on every out-edge of r) inside comp.
    Returns (mu, cycle) with cycle a list of nodes (closed walk)."""
    nodes = list(comp)
    idx = {r: i for i, r in enumerate(nodes)}
    n = len(nodes)
    NEG = -float("inf")
    Dm = [[0.0] * n]
    par = [[-1] * n]
    for k in range(1, n + 1):
        prev = Dm[-1]
        cur = [NEG] * n
        pk = [-1] * n
        for i, r in enumerate(nodes):
            x = prev[i]
            if x == NEG:
                continue
            x += wt[r]
            for s in E[r]:
                j = idx[s]
                if x > cur[j]:
                    cur[j] = x
                    pk[j] = i
        Dm.append(cur)
        par.append(pk)
    best, bv = NEG, None
    for v in range(n):
        if Dm[n][v] == NEG:
            continue
        worst = min((Dm[n][v] - Dm[k][v]) / (n - k) for k in range(n) if Dm[k][v] != NEG)
        if worst > best:
            best, bv = worst, v
    walk, k, v = [], n, bv
    while k > 0:
        walk.append(v)
        v = par[k][v]
        k -= 1
    walk.append(v)
    walk.reverse()
    pos = {}
    for i, x in enumerate(walk):
        if x in pos:
            return best, [nodes[y] for y in walk[pos[x]:i]]
        pos[x] = i
    return best, None


def exact_expanding_cycle(comp, E, Q, table):
    """Exact multiplicative Bellman-Ford inside comp: a cycle with U >= W, or None."""
    d = {r: Fraction(1) for r in comp}
    pred = {r: None for r in comp}
    mult = {r: Fraction(*mult_of(Q, table, r)) for r in comp}
    for it in range(len(comp) + 1):
        last = None
        for r in comp:
            x = d[r] * mult[r]
            for s in E[r]:
                if x > d[s]:
                    d[s] = x
                    pred[s] = r
                    last = s
        if last is None:
            return None
    x = last
    for _ in range(len(comp)):
        x = pred[x]
    cyc, y = [x], pred[x]
    while y != x:
        cyc.append(y)
        y = pred[y]
    cyc.reverse()
    return cyc


def potential(comp, E, Q, table, mu):
    """Positive rationals c on comp and theta < 1 with c(s) u_r <= theta c(r) w_r on every
    internal edge r -> s (exactly verified).  None if the float candidates fail and the
    exact fallback finds an expanding cycle."""
    for frac in (0.5, 0.25, 0.8, 0.95):
        lt = mu * frac                      # log theta, mu < lt < 0
        wt = {r: math.log(table[r % Q][0]) - math.log(table[r % Q][2]) - lt for r in comp}
        phi = {r: 0.0 for r in comp}
        for _ in range(len(comp) + 2):
            ch = False
            for r in comp:
                if not E[r]:
                    continue
                b = max(phi[s] for s in E[r]) + wt[r]
                if b > phi[r] + 1e-13:
                    phi[r] = b
                    ch = True
            if not ch:
                break
        lo = min(phi.values())
        c = {r: Fraction(int(round(math.ldexp(1.0, 52) * math.exp(min(phi[r] - lo, 700.0)))))
             for r in comp}
        th = Fraction(0)
        ok = True
        for r in comp:
            u, w = mult_of(Q, table, r)
            for s in E[r]:
                q = Fraction(c[s] * u, c[r] * w)
                if q >= 1:
                    ok = False
                    break
                th = max(th, q)
            if not ok:
                break
        if ok:
            return c, th
    # exact fallback: gamma-scaled longest multiplicative path
    if exact_expanding_cycle(comp, E, Q, table) is not None:
        return None
    gamma = Fraction(3, 2)
    for _ in range(60):
        mult = {r: gamma * Fraction(*mult_of(Q, table, r)) for r in comp}
        g = {r: Fraction(1) for r in comp}
        okk = False
        for it in range(len(comp) + 2):
            ch = False
            for r in comp:
                if not E[r]:
                    continue
                b = max(g[s] for s in E[r]) * mult[r]
                if b > g[r]:
                    g[r] = b
                    ch = True
            if not ch:
                okk = True
                break
        if okk:
            th = max(Fraction(g[s]) * Fraction(*mult_of(Q, table, r)) / g[r]
                     for r in comp for s in E[r])
            assert th < 1
            return g, th
        gamma = 1 + (gamma - 1) / 4
    raise RuntimeError("no potential found")


def classify_level(Q, table, K):
    """Exact SCC classification of G_K.  Returns dict with
       comps: list of dicts {nodes, type, ...} for SCCs with an internal edge, where type is
         'a'  every cycle contracts: exact potential c, theta
         'b'  single simple cycle with U > W; data: cycle, U, W, lap map, p-adic test
         'c'  contains an expanding cycle (exact witness) and is not a single cycle
         'z'  contains a cycle with W = 1 (no division): U > 1 or translation
    """
    succ = graph(Q, table, K)
    comps = tarjan(K, succ)
    out = []
    for comp in comps:
        E = internal(comp, succ)
        ne = sum(len(x) for x in E.values())
        if ne == 0:
            continue
        rec = dict(nodes=sorted(comp), size=len(comp), edges=ne)
        # division-free cycles: nodes with w = 1 have a single successor
        nodiv = [r for r in comp if table[r % Q][2] == 1]
        zc = None
        nd = set(nodiv)
        for r0 in nodiv:
            path, pos, r = [], {}, r0
            while r in nd and r not in pos and E[r]:
                pos[r] = len(path)
                path.append(r)
                r = E[r][0]
            if r in pos:
                zc = path[pos[r]:]
                break
        if zc is not None:
            U, W = walk_UW(Q, table, zc)
            A, B, Dn = walk_map(Q, table, zc)
            rec.update(type="z", cycle=zc, U=U, W=W, lap=(A, B, Dn))
            out.append(rec)
            continue
        if ne == len(comp):                          # single simple cycle
            r0 = comp[0]
            cyc, r = [r0], E[r0][0]
            while r != r0:
                cyc.append(r)
                r = E[r][0]
            U, W = walk_UW(Q, table, cyc)
            if U < W:
                c = {r: Fraction(1) for r in comp}
                res = potential(comp, E, Q, table, (math.log(U) - math.log(W)) / len(cyc))
                rec.update(type="a", c=res[0], theta=res[1], cycle=cyc)
            else:
                A, B, Dn = walk_map(Q, table, cyc)
                rec.update(type="b", cycle=cyc, U=U, W=W, lap=(A, B, Dn))
            out.append(rec)
            continue
        wt = {r: math.log(table[r % Q][0]) - math.log(table[r % Q][2]) for r in comp}
        mu, cyc = karp(comp, E, wt)
        if cyc is not None:
            U, W = walk_UW(Q, table, cyc)
            if U >= W:
                rec.update(type="c", cycle=cyc, U=U, W=W, mu=mu)
                out.append(rec)
                continue
        if mu < 0:
            res = potential(comp, E, Q, table, mu)
        else:
            res = None
        if res is None:
            bad = exact_expanding_cycle(comp, E, Q, table)
            assert bad is not None
            U, W = walk_UW(Q, table, bad)
            rec.update(type="c", cycle=bad, U=U, W=W, mu=mu)
        else:
            rec.update(type="a", c=res[0], theta=res[1], mu=mu)
        out.append(rec)
    # exact re-verification of every witness
    for rec in out:
        verify_rec(Q, table, succ, rec)
    return dict(K=K, comps=out, types="".join(sorted(set(x["type"] for x in out))))


def is_closed_walk(succ, cyc):
    L = len(cyc)
    return all(cyc[(i + 1) % L] in succ[cyc[i]] for i in range(L))


def verify_rec(Q, table, succ, rec):
    t = rec["type"]
    S = set(rec["nodes"])
    if t in "bcz":
        cyc = rec["cycle"]
        assert set(cyc) <= S and is_closed_walk(succ, cyc)
        U, W = walk_UW(Q, table, cyc)
        assert (U, W) == (rec["U"], rec["W"])
        if t in "bc":
            assert U >= W
        if t == "z":
            assert W == 1
        if t == "b":
            assert sum(1 for r in S for s in succ[r] if s in S) == len(S) == len(cyc)
        if t == "c":
            assert sum(1 for r in S for s in succ[r] if s in S) > len(S)
    else:
        c, th = rec["c"], rec["theta"]
        assert th < 1
        for r in S:
            u, w = mult_of(Q, table, r)
            for s in succ[r]:
                if s in S:
                    assert c[s] * u <= th * c[r] * w


# ----------------------------------------------------------------------------- Theorem H'

def padic_kill(U, W):
    """A prime p with v_p(W) > v_p(U), or None (then the lap ratio U/W is an integer)."""
    for p in primes_of(W):
        a, b = U, W
        vu = vw = 0
        while a % p == 0:
            a //= p
            vu += 1
        while b % p == 0:
            b //= p
            vw += 1
        if vw > vu:
            return p
    return None


def theorem_H(Q, table, lev, cap=2 * 10 ** 6, orbit_cap=10 ** 7, zero=False):
    """Theorem H' (theory.md).  `lev` is the output of classify_level.  Requires P.
    Returns dict(status=..., cycles=[...], ...):
       'GLOBAL'   every positive orbit eventually periodic; cycles is the complete list
       'DIVERGES' a type-z SCC gives a whole residue class with T^L(n) = U n + B/.. > n
       'NONE'     some SCC is of type c, or a type-b/z cycle is not resolved by the lemma
    """
    K = lev["K"]
    TK = lift(Q, table, K)
    T = step_fn(Q, table)
    for rec in lev["comps"]:
        if rec["type"] == "c":
            return dict(status="NONE", why="type (c) SCC")
    for rec in lev["comps"]:
        if rec["type"] == "z":
            A, B, Dn = rec["lap"]
            if A > Dn or (A == Dn and B > 0):
                # whole class follows the division-free cycle (each node has one successor)
                r0 = rec["cycle"][0]
                n0 = r0 if (r0 > 0 or zero) else K
                while A * n0 + B <= n0:          # Dn = 1 here (W = 1)
                    n0 += K
                # exact check: n0 follows the cycle and T^L(n0) = A n0 + B > n0
                y = n0
                for r in rec["cycle"]:
                    assert y % K == r
                    y = T(y)
                assert Dn == 1 and y == A * n0 + B and y > n0 and y % K == r0
                return dict(status="DIVERGES", why="division-free cycle", cycle=rec["cycle"],
                            lap=rec["lap"], start=n0)
            return dict(status="NONE", why="neutral division-free cycle")
    cycles = []
    for rec in lev["comps"]:
        if rec["type"] == "b":
            U, W = rec["U"], rec["W"]
            p = padic_kill(U, W)
            if p is None:
                return dict(status="NONE", why="type (b) with integral lap ratio")
            A, B, Dn = rec["lap"]
            x = Fraction(B, Dn - A)
            rec["xstar"] = x
            rec["p"] = p
            if x.denominator == 1 and x >= (0 if zero else 1):
                # does the integer x* follow the cycle?
                y, ok = int(x), True
                for r in rec["cycle"]:
                    if y % K != r:
                        ok = False
                        break
                    y = T(y)
                if ok and y == x:
                    cyc = [int(x)]
                    z = T(int(x))
                    while z != int(x):
                        cyc.append(z)
                        z = T(z)
                    cycles.append(tuple(cyc))
    for rec in lev["comps"]:
        if rec["type"] != "a":
            continue
        c, th = rec["c"], rec["theta"]
        S = set(rec["nodes"])
        beta = Fraction(0)
        for r in S:
            u, v, w = TK[r]
            for s in graph_succ(Q, table, K, r):
                if s in S:
                    beta = max(beta, c[s] * max(v, 0) / w)
        bound = beta / (1 - th)
        rec["Vbound"] = bound
        work = sum(int(bound / c[r]) // K + 1 for r in S)
        if work > cap:
            return dict(status="NONE", why=f"candidate set too large ({work})")
        for r in S:
            nmax = int(bound / c[r])
            n = r if (r > 0 or zero) else K
            while n <= nmax:
                cycles.extend(cycles_from_start(T, n, orbit_cap))
                n += K
    # canonical, unique
    canon = set()
    for cyc in cycles:
        k = cyc.index(min(cyc))
        canon.add(tuple(cyc[k:] + cyc[:k]))
    return dict(status="GLOBAL", cycles=sorted(canon, key=lambda c: (c[0], len(c))))


def graph_succ(Q, table, K, r):
    u, v, w = table[r % Q]
    y0 = (u * r + v) // w
    k = (u * K) // w
    g = math.gcd(k, K)
    return [y0 % g + g * j for j in range(K // g)]


_seen_cycle_cache = {}


def cycles_from_start(T, n, cap):
    seen, x, path = {}, n, []
    while x not in seen:
        seen[x] = len(path)
        path.append(x)
        x = T(x)
        if len(path) > cap:
            raise RuntimeError(f"orbit of {n} longer than {cap}")
    return [tuple(path[seen[x]:])]


# ----------------------------------------------------------------------------- exponents

def theta_data(Q, table, K=None):
    """Lundberg tail exponent theta_1, run exponent theta_run, gap and drift (floats).
    Markov maps only.  M_theta[r,s] = (1/w)(u/w)^theta over edges."""
    import numpy as np
    K = K or Q
    succ = graph(Q, table, K)
    comps = [c for c in tarjan(K, succ)]
    src, dst, lu, lw = [], [], [], []
    for r in range(K):
        u, v, w = table[r % Q]
        for s in succ[r]:
            src.append(r)
            dst.append(s)
            lu.append(math.log(u))
            lw.append(math.log(w))
    src, dst, lu, lw = map(np.array, (src, dst, lu, lw))

    def rho(th):
        best = 0.0
        val = np.exp(-lw + th * (lu - lw))
        for comp in comps:
            S = set(comp)
            if len(comp) == 1 and comp[0] not in succ[comp[0]]:
                continue
            idx = {r: i for i, r in enumerate(comp)}
            M = np.zeros((len(comp), len(comp)))
            for e in range(len(src)):
                if src[e] in S and dst[e] in S:
                    M[idx[src[e]], idx[dst[e]]] += val[e]
            best = max(best, max(abs(np.linalg.eigvals(M))))
        return best
    # drift: stationary measure of M_0 on each closed (terminal) class
    drift = None
    cid = {}
    for i, comp in enumerate(comps):
        for r in comp:
            cid[r] = i
    closed = [comp for comp in comps if all(cid[s] == cid[comp[0]] for r in comp for s in succ[r])]
    drifts = []
    for comp in closed:
        idx = {r: i for i, r in enumerate(comp)}
        n = len(comp)
        M = np.zeros((n, n))
        for r in comp:
            w = table[r % Q][2]
            for s in succ[r]:
                M[idx[r], idx[s]] += 1.0 / w
        vals, vecs = np.linalg.eig(M.T)
        i = int(np.argmin(abs(vals - 1)))
        pi = np.real(vecs[:, i])
        pi = pi / pi.sum()
        drifts.append(float(sum(pi[idx[r]] * (math.log(table[r % Q][0]) - math.log(table[r % Q][2]))
                                for r in comp)))
    drift = max(drifts) if drifts else None
    # theta_1
    if rho(1e-7) > 1 + 1e-12:
        t1 = 0.0
    elif rho(80.0) <= 1 + 1e-12:
        t1 = math.inf
    else:
        lo, hi = 0.0, 80.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if rho(mid) > 1 + 1e-12:
                hi = mid
            else:
                lo = mid
        t1 = lo
    # theta_run: least t such that some cycle has t log U - (1+t) log W >= 0 (parametric)
    def has_nonneg_cycle(t):
        wt = {r: t * math.log(table[r % Q][0]) - (1 + t) * math.log(table[r % Q][2])
              for r in range(K)}
        for comp in comps:
            E = internal(comp, succ)
            if sum(len(x) for x in E.values()) == 0:
                continue
            mu, cyc = karp(comp, E, wt)
            if mu >= -1e-12:
                return True
        return False
    if not has_nonneg_cycle(1e6):
        tr = math.inf
    else:
        lo, hi = 0.0, 1e6
        for _ in range(80):
            mid = (lo + hi) / 2
            if has_nonneg_cycle(mid):
                hi = mid
            else:
                lo = mid
        tr = hi
    return dict(theta1=t1, theta_run=tr, gap=(tr - t1) if (tr < math.inf and t1 < math.inf) else None,
                drift=drift)


# ----------------------------------------------------------------------------- driver

def default_levels(Q, maxnodes=2000):
    """Levels K = Q * d, d a product of primes of Q, K <= maxnodes, in increasing order;
    always includes Q itself."""
    ps = primes_of(Q) or [2]
    ks = {Q}
    frontier = [Q]
    while frontier:
        nxt = []
        for k in frontier:
            for p in ps:
                if k * p <= maxnodes and k * p not in ks:
                    ks.add(k * p)
                    nxt.append(k * p)
        frontier = nxt
    return sorted(ks)


def analyse(Q, table, levels=None, want_decide=True, want_theta=True, maxnodes=600,
            cap=2 * 10 ** 6, decide_cap=3 * 10 ** 7, zero=False):
    table = [tuple(t) for t in table]
    check_table(Q, table)
    hyp = hypotheses(Q, table, zero)
    res = dict(Q=Q, hyp=hyp, zero=zero)
    if zero:
        want_decide = False          # decide.py is stated on the positive integers
    if not hyp["P"]:
        res["note"] = "positivity fails"
        return res
    if want_decide and hyp["markov"]:
        try:
            dres = D.decide(Q, table, want_cycles=True, want_depth=(Q <= 400), cap=decide_cap)
            res["decide"] = dict(verdict=dres["verdict"], kstar=dres.get("kstar"),
                                 cycles=dres.get("cycles"), leaves=dres.get("leaves"),
                                 obst=dres.get("obst"))
        except AssertionError as e:
            res["decide"] = dict(verdict="ERR", err=repr(e))
    levels = levels or default_levels(Q, maxnodes)
    res["levels"] = []
    for K in levels:
        lev = classify_level(Q, table, K)
        res["levels"].append(lev)
        if "c" not in lev["types"]:
            res["H"] = theorem_H(Q, table, lev, cap=cap, zero=zero)
            res["H"]["K"] = K
            if res["H"]["status"] != "NONE":
                break
        if hyp["markov"] and len(primes_of(Q)) <= 1:
            # prime power, Markov: types are level independent (round3 Lemma L)
            break
    if want_theta and hyp["markov"]:
        res["theta"] = theta_data(Q, table)
    return res


def summary(res):
    s = {}
    s["Q"] = res["Q"]
    s["markov"] = res["hyp"]["markov"]
    if "note" in res:
        s["note"] = res["note"]
        return s
    if "decide" in res:
        d = res["decide"]
        s["decide"] = d["verdict"]
        if d["verdict"] == "CERT":
            s["kstar"] = d.get("kstar")
            s["ncycles"] = len(d["cycles"]) if d.get("cycles") is not None else None
            s["cycle_mins"] = [c[0] for c in sorted(d["cycles"])] if d.get("cycles") else None
        elif d["verdict"] == "OBST":
            o = d["obst"]
            s["obst"] = f"{o['kind']} {o['U']}/{o['W']} on {o['rotated']}"
    s["types"] = {lev["K"]: lev["types"] for lev in res["levels"]}
    if "H" in res:
        h = res["H"]
        s["H"] = h["status"] + (f" at K={h['K']}" if "K" in h else "")
        if h["status"] == "GLOBAL":
            s["H_cycle_mins"] = [c[0] for c in h["cycles"]]
    if "theta" in res:
        t = res["theta"]
        s.update({k: (round(v, 5) if isinstance(v, float) and math.isfinite(v) else v)
                  for k, v in t.items()})
    return s


if __name__ == "__main__":
    Q = int(sys.argv[1])
    tab = eval(sys.argv[2], {})
    r = analyse(Q, tab)
    import pprint
    pprint.pprint(summary(r))
