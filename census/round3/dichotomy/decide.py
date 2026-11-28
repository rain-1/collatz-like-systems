#!/usr/bin/env python3
"""decide.py -- decision procedure for descent certificates of Markov table maps.

A *table map* is given by a modulus Q >= 1 and, for every residue r mod Q, a
triple (u_r, v_r, w_r) of integers; it acts on positive integers by

        T(n) = (u_r * n + v_r) / w_r        for n = r (mod Q).

Hypotheses checked exactly by `check_hypotheses` (see dichotomy.md):

  (H1) u_r >= 1 and gcd(u_r, Q) = 1;
  (H2) w_r >= 1, w_r | Q and w_r | u_r * r + v_r   (exact division on the class);
  (P)  T(n) >= 1 for every n >= 1                  (checked at the least n of each class).

Under (H1)(H2) the residue graph G_T (edge r -> s iff s = (u_r r + v_r)/w_r mod Q/w_r)
is *Markov*: every walk of G_T is followed by an arithmetic progression of positive
integers.  The Dichotomy Theorem (dichotomy.md, Theorem 1) says:

    a descent certificate exists  <=>  every cycle of G_T has  prod u / prod w < 1.

`decide(Q, table)` returns either

  CERT: an integer weight vector c with  c(s) u_r < c(r) w_r  for every edge r -> s
        (verified with integers), the exceptional set F (finite, explicit), and the
        COMPLETE list of cycles of T on the positive integers (every orbit reaches one);
        plus the exact minimal stopping-time depth k* and leaf count of the minimal
        certificate (computed on the graph, Theorem 3), and the a-priori depth bound.

  OBST: a cycle of G_T with prod u >= prod w (verified exactly), the progression of
        integers that follows it (verified), and, when it exists in Z_hat, the exact
        rational periodic point with its expanding multiplier (verified with Fractions).

Floating point is used ONLY to *find* a candidate cycle or a candidate potential;
every output is re-verified in exact integer/Fraction arithmetic, and if a float
candidate fails, an exact Bellman-Ford (Fractions) decides.

CLI:   python3 decide.py Q "[(u,v,w), ...]"        (list of Q triples, index = residue)
       python3 decide.py --id <system id from systems.py>
"""
from fractions import Fraction
import math
import sys
import os


# --------------------------------------------------------------------------- basics

def check_hypotheses(Q, table):
    """Raise AssertionError unless (H1), (H2), (P) hold.  Exact."""
    assert len(table) == Q and Q >= 1
    for r, (u, v, w) in enumerate(table):
        assert u >= 1 and math.gcd(u, Q) == 1, ("H1", r)
        assert w >= 1 and Q % w == 0 and (u * r + v) % w == 0, ("H2", r)
        n0 = r if r > 0 else Q                   # least positive n in the class
        assert (u * n0 + v) // w >= 1, ("P", r)  # T is increasing in n on the class
    return True


def step_fn(Q, table):
    def T(n):
        u, v, w = table[n % Q]
        x = u * n + v
        assert x % w == 0
        return x // w
    return T


def residue_graph(Q, table):
    """succ[r] = list of residues s mod Q that T(n) takes for n = r (mod Q)."""
    succ = []
    for r, (u, v, w) in enumerate(table):
        base = ((u * r + v) // w) % (Q // w)
        succ.append([base + (Q // w) * i for i in range(w)])
    return succ


def path_progression(Q, table, nodes):
    """Integers n >= 1 with n = nodes[0] (mod Q) and T^i(n) = nodes[i] (mod Q) for all i.
    Returns (a, M, A, B, D): that set is {a + M t : t >= 0} (a >= 1), and on it
    T^L(n) = (A n + B)/D with L = len(nodes)-1.  Exact; raises if the walk is not realised."""
    a, M = nodes[0] % Q, Q
    if a == 0:
        a = Q
    Y, K = a, M            # current iterate T^i(a + M t) = Y + K t
    A, B, D = 1, 0, 1
    for i in range(len(nodes) - 1):
        r = nodes[i]
        u, v, w = table[r]
        assert Y % Q == r and K % Q == 0
        assert (u * Y + v) % w == 0 and (u * K) % w == 0
        y0, k = (u * Y + v) // w, (u * K) // w
        s = nodes[i + 1]
        g = math.gcd(k, Q)
        assert (s - y0) % g == 0, "walk not realised"
        t0 = ((s - y0) // g) * pow(k // g, -1, Q // g) % (Q // g) if Q // g > 1 else 0
        a, M = a + M * t0, M * (Q // g)
        Y, K = y0 + k * t0, k * (Q // g)
        A, B, D = u * A, u * B + v * D, D * w
    return a, M, A, B, D


# --------------------------------------------------------------------------- cycles

def translation_cycles(Q, table):
    """Cycles of G_T made of translation nodes (u = w = 1); these are exactly the
    cycles with multiplier 1 (Lemma 2).  Returns list of (cycle nodes, drift)."""
    tr = {r for r, (u, v, w) in enumerate(table) if u == 1 and w == 1}
    out, seen = [], set()
    for r0 in tr:
        if r0 in seen:
            continue
        path, pos, r = [], {}, r0
        while r in tr and r not in seen and r not in pos:
            pos[r] = len(path)
            path.append(r)
            r = (r + table[r][1]) % Q
        if r in pos:
            cyc = path[pos[r]:]
            out.append((cyc, sum(table[x][1] for x in cyc)))
        seen.update(path)
    return out


def karp_float(Q, table, succ):
    """Max mean cycle of log(u/w) (floating point, search only).  Returns (mu, cycle)."""
    n = Q
    wt = [math.log(u) - math.log(w) for (u, v, w) in table]
    NEG = -float("inf")
    D = [[0.0] * n]
    par = [[None] * n]
    for k in range(1, n + 1):
        prev = D[-1]
        cur = [NEG] * n
        pk = [None] * n
        for r in range(n):
            x = prev[r]
            if x == NEG:
                continue
            x += wt[r]
            for s in succ[r]:
                if x > cur[s]:
                    cur[s] = x
                    pk[s] = r
        D.append(cur)
        par.append(pk)
    best, bv = NEG, None
    for v in range(n):
        if D[n][v] == NEG:
            continue
        worst = min((D[n][v] - D[k][v]) / (n - k) for k in range(n) if D[k][v] != NEG)
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
            return best, walk[pos[x]:i]
        pos[x] = i
    return best, None


def karp_np(Q, table, succ):
    """Same as karp_float, vectorised with numpy (for Q up to a few thousand)."""
    import numpy as np
    src = np.array([r for r in range(Q) for s in succ[r]], dtype=np.int64)
    dst = np.array([s for r in range(Q) for s in succ[r]], dtype=np.int64)
    wt = np.array([math.log(table[r][0]) - math.log(table[r][2]) for r in range(Q)])[src]
    n = Q
    D = np.full((n + 1, n), -np.inf)
    D[0, :] = 0.0
    P = np.zeros((n + 1, n), dtype=np.int64)
    for k in range(1, n + 1):
        cand = D[k - 1, src] + wt
        # max per dst, remember argmax source
        o = np.lexsort((cand, dst))
        last = np.r_[dst[o][1:] != dst[o][:-1], True]
        sel = o[last]
        D[k, dst[sel]] = cand[sel]
        P[k, dst[sel]] = src[sel]
    with np.errstate(invalid="ignore"):
        ks = np.arange(n)
        diffs = (D[n][None, :] - D[:n]) / (n - ks)[:, None]
        diffs[np.isnan(diffs)] = np.inf
        worst = diffs.min(axis=0)
    worst[np.isneginf(D[n])] = -np.inf
    bv = int(np.argmax(worst))
    best = float(worst[bv])
    walk, k, v = [], n, bv
    while k > 0:
        walk.append(v)
        v = int(P[k, v])
        k -= 1
    walk.append(v)
    walk.reverse()
    pos = {}
    for i, x in enumerate(walk):
        if x in pos:
            return best, walk[pos[x]:i]
        pos[x] = i
    return best, None


def cycle_multiplier(table, cyc):
    U = W = 1
    for r in cyc:
        U *= table[r][0]
        W *= table[r][2]
    return U, W


def exact_bad_cycle(Q, table, succ):
    """Exact multiplicative Bellman-Ford: return a cycle with prod u > prod w, or None.
    (Cycles with product exactly 1 are translation cycles and are found separately.)"""
    d = [Fraction(1)] * Q
    pred = [None] * Q
    mult = [Fraction(u, w) for (u, v, w) in table]
    last = None
    for it in range(Q + 1):
        last = None
        for r in range(Q):
            x = d[r] * mult[r]
            for s in succ[r]:
                if x > d[s]:
                    d[s] = x
                    pred[s] = r
                    last = s
        if last is None:
            return None
    x = last
    for _ in range(Q):
        x = pred[x]
    cyc, y = [x], pred[x]
    while y != x:
        cyc.append(y)
        y = pred[y]
    cyc.reverse()
    U, W = cycle_multiplier(table, cyc)
    assert U > W
    return cyc


def is_graph_cycle(succ, cyc):
    L = len(cyc)
    return all(cyc[(i + 1) % L] in succ[cyc[i]] for i in range(L))


# --------------------------------------------------------------------------- potentials

def float_potential(Q, table, succ, mu, frac):
    """phi(r) = max over walks from r of sum(log(u/w) + eps), eps = -mu*frac.
    Returns integer weights c(r) ~ exp(phi(r)) (to be verified exactly)."""
    eps = -mu * frac
    wt = [math.log(u) - math.log(w) + eps for (u, v, w) in table]
    phi = [0.0] * Q
    for _ in range(Q + 2):
        ch = False
        for r in range(Q):
            best = max(phi[s] for s in succ[r]) + wt[r]
            if best > phi[r] + 1e-15:
                phi[r] = best
                ch = True
        if not ch:
            break
    lo = min(phi)
    # integer weights with ~60 significant bits
    return [int(round(math.ldexp(1.0, 60) * math.exp(min(p - lo, 600.0)))) for p in phi]


def exact_potential(Q, table, succ, gamma):
    """Exact: g(r) = max over walks from r of prod(gamma*u/w) (empty walk = 1), if all
    gamma-cycles are <= 1; else None.  Returned as integers (common denominator cleared)."""
    mult = [gamma * Fraction(u, w) for (u, v, w) in table]
    g = [Fraction(1)] * Q
    for it in range(Q + 2):
        ch = False
        for r in range(Q):
            best = max(g[s] for s in succ[r]) * mult[r]
            if best > g[r]:
                g[r] = best
                ch = True
        if not ch:
            L = 1
            for x in g:
                L = L * x.denominator // math.gcd(L, x.denominator)
            return [int(x * L) for x in g]
    return None


def verify_potential(Q, table, succ, c):
    """Exact: c(s)*u_r < c(r)*w_r for every edge.  Returns theta = max c(s)u/(c(r)w) < 1."""
    th = Fraction(0)
    for r, (u, v, w) in enumerate(table):
        assert c[r] > 0
        for s in succ[r]:
            assert c[s] * u < c[r] * w, ("potential fails", r, s)
            th = max(th, Fraction(c[s] * u, c[r] * w))
    return th


def exceptional_set(Q, table, c, cap=3 * 10 ** 7):
    """F = {n >= 1 : V(T n) >= V(n)} with V(n) = c(n mod Q) n.  Exact and complete:
    for n > N_r (bound below) the inequality V(Tn) < V(n) is proved symbolically."""
    succ = residue_graph(Q, table)
    bounds = []
    for r, (u, v, w) in enumerate(table):
        Nr = 0
        if v > 0:
            for s in succ[r]:
                # V(Tn) < V(n)  <=>  n*(c_r w - c_s u) > c_s v
                Nr = max(Nr, (c[s] * v) // (c[r] * w - c[s] * u))
        bounds.append(Nr)
    work = sum(N // Q + 1 for N in bounds)
    if work > cap:
        return None, bounds
    F = []
    for r, (u, v, w) in enumerate(table):
        n = r if r > 0 else Q
        while n <= bounds[r]:
            y = (u * n + v) // w
            if c[y % Q] * y >= c[r] * n:
                F.append(n)
            n += Q
    return sorted(F), bounds


def cycles_from(Q, table, starts, cap=10 ** 7):
    """Follow every start until it repeats; return the set of cycles (tuples from min)."""
    T = step_fn(Q, table)
    owner = {}
    cycles = []
    for e in starts:
        seen, x, path = {}, e, []
        while x not in seen and x not in owner:
            seen[x] = len(path)
            path.append(x)
            x = T(x)
            assert len(path) < cap, ("orbit too long", e)
        if x in owner:
            cid = owner[x]
        else:
            cyc = path[seen[x]:]
            k = cyc.index(min(cyc))
            cyc = tuple(cyc[k:] + cyc[:k])
            cycles.append(cyc)
            cid = len(cycles) - 1
        for y in path:
            owner[y] = cid
    return cycles


# --------------------------------------------------------------------------- depth

def stopping_depth(Q, table, succ, maxstates=2 * 10 ** 6):
    """Exact minimal stopping-time data on the graph (Theorem 3):
    k* = max over walks of the first index j with prefix multiplier < 1 (or = 1 with
    negative translation drift); also the number of leaves of the minimal certificate
    when rows are distinguished by their residue mod Q (each leaf = node word r0..r_{j-1})."""
    mult = [Fraction(u, w) for (u, v, w) in table]
    trans = [(u == 1 and w == 1) for (u, v, w) in table]
    # state: (node, P, drift or None) -> multiplicity
    layer = {(r, Fraction(1), 0): 1 for r in range(Q)}
    j, leaves, kstar = 0, 0, 0
    while layer:
        j += 1
        nxt = {}
        for (r, P, c), m in layer.items():
            nP = P * mult[r]
            nc = (c + table[r][1]) if (c is not None and trans[r]) else None
            if nP < 1 or (nP == 1 and nc is not None and nc < 0):
                leaves += m
                kstar = j
                continue
            for s in succ[r]:
                key = (s, nP, nc if nP == 1 else None)
                nxt[key] = nxt.get(key, 0) + m
        layer = nxt
        assert len(layer) < maxstates and j < 10 ** 5, "depth search too large"
    return kstar, leaves


def deepest_walk(Q, table, succ, maxstates=2 * 10 ** 6):
    """A non-descending walk of maximal length Lambda = k* - 1 (Theorem 3), as a list of
    Lambda + 1 residues (the last one is the start of the descending step)."""
    mult = [Fraction(u, w) for (u, v, w) in table]
    trans = [(u == 1 and w == 1) for (u, v, w) in table]
    layer = {(r, Fraction(1), 0): None for r in range(Q)}
    history = [layer]
    while True:
        nxt = {}
        for st in layer:
            r, P, c = st
            nP = P * mult[r]
            nc = (c + table[r][1]) if (c is not None and trans[r]) else None
            if nP < 1 or (nP == 1 and nc is not None and nc < 0):
                continue
            for s in succ[r]:
                key = (s, nP, nc if nP == 1 else None)
                if key not in nxt:
                    nxt[key] = st
        if not nxt:
            break
        history.append(nxt)
        layer = nxt
        assert len(layer) < maxstates
    st = next(iter(history[-1]))
    walk = [st[0]]
    for lay in reversed(history[1:]):
        st = lay[st]
        walk.append(st[0])
    walk.reverse()
    return walk


def depth_bound(c, theta):
    """Smallest j with (cmax/cmin) * theta^j < 1 (exact): every walk of length j has
    multiplier < 1, so a certificate of uniform depth j exists (Theorem 3(b))."""
    ratio = Fraction(max(c), min(c))
    j, x = 0, ratio
    while x >= 1:
        x *= theta
        j += 1
    return j


# --------------------------------------------------------------------------- obstruction

def rotate_cycle(table, cyc):
    """Rotate so that every partial multiplier (over any number of laps) is > 1
    (cycle lemma; requires total multiplier > 1)."""
    L = len(cyc)
    pref = [Fraction(1)]
    for r in cyc:
        pref.append(pref[-1] * Fraction(table[r][0], table[r][2]))
    mn = min(pref[:L])
    i0 = max(i for i in range(L) if pref[i] == mn)
    return cyc[i0:] + cyc[:i0]


def verify_obstruction(Q, table, succ, cyc, laps=3):
    """Exact certificate that no descent certificate exists (Lemma 4).
    Returns a dict with the progression following `laps` laps and, if it exists in
    Z_hat (denominator prime to Q), the rational periodic point."""
    assert is_graph_cycle(succ, cyc)
    U, W = cycle_multiplier(table, cyc)
    out = dict(cycle=list(cyc), U=U, W=W)
    L = len(cyc)
    if U == W:     # translation cycle (critical case, Lemma 2)
        drift = sum(table[r][1] for r in cyc)
        assert all(table[r][0] == 1 and table[r][2] == 1 for r in cyc) and drift >= 0
        # rotate after the last minimum of partial drifts
        pref = [0]
        for r in cyc:
            pref.append(pref[-1] + table[r][1])
        mn = min(pref[:L])
        i0 = max(i for i in range(L) if pref[i] == mn)
        rc = cyc[i0:] + cyc[:i0]
        T = step_fn(Q, table)
        for n in (rc[0] or Q, rc[0] + 1000003 * Q):
            x = n
            for i in range(laps * L):
                x = T(x)
                assert x >= n
        out.update(kind="critical", drift=drift, rotated=rc)
        return out
    assert U > W
    rc = rotate_cycle(table, cyc)
    walk = (rc * laps) + [rc[0]]
    a, M, A, B, D = path_progression(Q, table, walk)
    # every partial multiplier > 1 along the rotated cycle (exact)
    P = Fraction(1)
    for r in walk[:-1]:
        P *= Fraction(table[r][0], table[r][2])
        assert P > 1
    # integers on the progression really follow the walk (direct iteration)
    T = step_fn(Q, table)
    for t in (0, 1, 7, 10 ** 6 + 3):
        n = a + M * t
        x = n
        for i in range(len(walk) - 1):
            assert x % Q == walk[i]
            x = T(x)
        assert x % Q == walk[-1] and x * D == A * n + B
    out.update(kind="expanding", rotated=rc, progression=(a, M))
    # rational periodic point of the composed lap map (U x + B1)/W
    a1, M1, A1, B1, D1 = path_progression(Q, table, rc + [rc[0]])
    x = Fraction(B1, D1 - A1)
    if x.denominator % 1 == 0 and math.gcd(x.denominator, Q) == 1:
        # verify it follows the cycle in Z_hat and returns to itself
        y = x
        for r in rc:
            res = (y.numerator * pow(y.denominator, -1, Q)) % Q
            if res != r:
                break
            u, v, w = table[r]
            y = (u * y + v) / w
        else:
            if y == x:
                out["periodic_point"] = x
    return out


# --------------------------------------------------------------------------- main

def decide(Q, table, want_cycles=True, want_depth=True, fracs=(0.5, 0.8, 0.95, 0.25),
           cap=3 * 10 ** 7):
    table = [tuple(t) for t in table]
    check_hypotheses(Q, table)
    succ = residue_graph(Q, table)
    tc = translation_cycles(Q, table)
    if tc:
        cyc, drift = tc[0]
        assert drift >= 0      # forced by (P), Lemma 2
        return dict(verdict="OBST", obst=verify_obstruction(Q, table, succ, cyc))
    mu, cyc = (karp_float if Q <= 64 else karp_np)(Q, table, succ)
    if cyc is not None:
        U, W = cycle_multiplier(table, cyc)
        if U > W:
            return dict(verdict="OBST", mu=mu, obst=verify_obstruction(Q, table, succ, cyc))
    # try to certify
    best = None
    if mu < 0:
        for f in fracs:
            c = float_potential(Q, table, succ, mu, f)
            try:
                th = verify_potential(Q, table, succ, c)
            except AssertionError:
                continue
            F, bounds = exceptional_set(Q, table, c, cap=0)
            work = sum(N // Q + 1 for N in bounds)
            if best is None or work < best[0]:
                best = (work, c, th)
    if best is None:
        bad = exact_bad_cycle(Q, table, succ)
        if bad is not None:
            return dict(verdict="OBST", mu=mu, obst=verify_obstruction(Q, table, succ, bad))
        gamma = Fraction(1) + Fraction(1, 2)
        while True:
            c = exact_potential(Q, table, succ, gamma)
            if c is not None:
                break
            gamma = 1 + (gamma - 1) / 4
        th = verify_potential(Q, table, succ, c)
        best = (None, c, th)
    _, c, th = best
    res = dict(verdict="CERT", mu=mu, weights=c, theta=th, depth_bound=depth_bound(c, th))
    if want_cycles:
        F, bounds = exceptional_set(Q, table, c, cap=cap)
        res["bounds"] = bounds
        if F is not None:
            res["F"] = F
            res["cycles"] = cycles_from(Q, table, F)
    if want_depth:
        k, nl = stopping_depth(Q, table, succ)
        assert k <= res["depth_bound"]
        res["kstar"], res["leaves"] = k, nl
    return res


def report(Q, table, res):
    lines = []
    if res["verdict"] == "CERT":
        lines.append(f"CERT  (max cycle mean of log(u/w) ~ {res['mu']:.6f})")
        lines.append(f"  potential c = {res['weights'] if Q <= 32 else '(%d weights)' % Q}")
        lines.append(f"  theta = max c(s)u/(c(r)w) = {float(res['theta']):.6f} < 1  (exact check)")
        lines.append(f"  minimal stopping depth k* = {res.get('kstar')}  leaves = {res.get('leaves')}"
                     f"  a-priori bound {res['depth_bound']}")
        if "F" in res:
            lines.append(f"  exceptional set |F| = {len(res['F'])}  (max {max(res['F']) if res['F'] else 0})")
            lines.append(f"  COMPLETE cycle list ({len(res['cycles'])}):")
            for cyc in sorted(res["cycles"], key=lambda c: c[0]):
                s = " ".join(map(str, cyc)) if len(cyc) <= 24 else \
                    " ".join(map(str, cyc[:20])) + f" ... (length {len(cyc)})"
                lines.append(f"    ({s})")
        else:
            lines.append(f"  exceptional bound too large to enumerate: {max(res['bounds'])}")
    else:
        o = res["obst"]
        lines.append(f"OBST  {o['kind']} cycle of the residue graph, length {len(o['cycle'])}, "
                     f"multiplier {o['U']}/{o['W']}")
        lines.append(f"  residues {o['rotated']}")
        if o["kind"] == "critical":
            lines.append(f"  translation cycle with drift {o['drift']} >= 0: T^L(n) = n + drift on a whole class")
        else:
            lines.append(f"  progression following 3 laps: n = {o['progression'][0]} mod {o['progression'][1]}")
            if "periodic_point" in o:
                lines.append(f"  expanding rational periodic point x* = {o['periodic_point']}")
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--id":
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import systems
        s = systems.BY_ID[sys.argv[2]]
        Q, tab = s["Q"], s["table"]
        print(s["id"], ":", s["rule"])
    else:
        Q = int(sys.argv[1])
        tab = eval(sys.argv[2], {})
    r = decide(Q, tab)
    print(report(Q, tab, r))
