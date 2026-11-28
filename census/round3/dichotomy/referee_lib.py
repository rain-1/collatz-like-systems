"""Referee's independent library for lens 'dichotomy' (round 3).

Written from scratch from the statements in dichotomy.md; it does NOT import decide.py,
distance.py, neighbours.py or families.py.  Exact arithmetic (ints / Fractions) in every
verdict; floats are used only to propose a potential that is then verified with integers.

Table map: Q, tab[r] = (u, v, w):  n = r (mod Q) -> (u n + v) / w.
"""
from fractions import Fraction
import math


def hyp(Q, tab):
    """(H1), (H2), (P).  Returns True/False (no exceptions)."""
    if len(tab) != Q:
        return False
    for r, (u, v, w) in enumerate(tab):
        if u < 1 or math.gcd(u, Q) != 1:
            return False
        if w < 1 or Q % w or (u * r + v) % w:
            return False
        n0 = r if r else Q
        if (u * n0 + v) // w < 1:
            return False
    return True


def stepper(Q, tab):
    def T(n):
        u, v, w = tab[n % Q]
        x = u * n + v
        if x % w:
            raise ArithmeticError("inexact division")
        return x // w
    return T


def graph(Q, tab):
    """succ[r]: all s mod Q with s = (u r + v)/w (mod Q/w)  (out-degree w_r)."""
    out = []
    for r, (u, v, w) in enumerate(tab):
        h = Q // w
        y = (u * r + v) // w
        out.append(sorted({(y + h * i) % Q for i in range(w)}))
    return out


# ------------------------------------------------------------------ exact verdict

def translation_cycle(Q, tab):
    """A cycle of translation vertices (u = w = 1), or None."""
    tr = [u == 1 and w == 1 for (u, v, w) in tab]
    color = [0] * Q
    for r0 in range(Q):
        if not tr[r0] or color[r0]:
            continue
        path, pos, r = [], {}, r0
        while tr[r] and color[r] == 0 and r not in pos:
            pos[r] = len(path)
            path.append(r)
            r = (r + tab[r][1]) % Q
        if tr[r] and r in pos:
            return path[pos[r]:]
        for x in path:
            color[x] = 1
    return None


def bad_cycle(Q, tab, alive=None):
    """Exact: a cycle of G_T (inside `alive`) with prod u >= prod w, or None.
    Translation cycles first (product exactly 1); then multiplicative Bellman-Ford
    with Fractions for product > 1 (product exactly 1 forces a translation cycle,
    Lemma 2(a), which is re-verified independently in referee_check part T)."""
    succ = graph(Q, tab)
    if alive is None:
        alive = set(range(Q))
    # translation cycles inside alive
    tr = [tab[r][0] == 1 and tab[r][2] == 1 and r in alive for r in range(Q)]
    seen = set()
    for r0 in range(Q):
        if not tr[r0] or r0 in seen:
            continue
        path, pos, r = [], {}, r0
        while tr[r] and r not in seen and r not in pos:
            pos[r] = len(path)
            path.append(r)
            r = (r + tab[r][1]) % Q
        if tr[r] and r in pos:
            return path[pos[r]:]
        seen.update(path)
    mult = [Fraction(u, w) for (u, v, w) in tab]
    d = {r: Fraction(1) for r in alive}
    pred = {}
    last = None
    nodes = sorted(alive)
    for it in range(len(nodes) + 1):
        last = None
        for r in nodes:
            x = d[r] * mult[r]
            for s in succ[r]:
                if s in alive and x > d[s]:
                    d[s] = x
                    pred[s] = r
                    last = s
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
        U *= tab[r][0]
        W *= tab[r][2]
    assert U > W and all(cyc[(i + 1) % len(cyc)] in succ[cyc[i]] for i in range(len(cyc)))
    return cyc


def potential(Q, tab):
    """Integer weights c with c(s) u_r < c(r) w_r on every edge, or None.
    Float proposal (value iteration) verified exactly; exact Lemma-4 fallback with gamma."""
    succ = graph(Q, tab)
    # float proposal: phi(r) = max over walks of sum(log(u/w) + eps)
    lw = [math.log(u / w) for (u, v, w) in tab]
    for eps in (1e-3, 1e-4, 2e-5, 3e-3, 1e-2, 5e-2):
        phi = [0.0] * Q
        ok = False
        for _ in range(4 * Q + 10):
            ch = False
            for r in range(Q):
                b = lw[r] + eps + max(phi[s] for s in succ[r])
                if b > phi[r] + 1e-13:
                    phi[r] = b
                    ch = True
            if not ch:
                ok = True
                break
            if max(phi) > 700:
                break
        if not ok:
            continue
        lo = min(phi)
        c = [int(math.ldexp(math.exp(p - lo), 62)) + 1 for p in phi]
        if all(c[s] * tab[r][0] < c[r] * tab[r][2] for r in range(Q) for s in succ[r]):
            return c
    # exact fallback (Lemma 4): g(r) = max over walks of prod(gamma u / w)
    gamma = Fraction(3, 2)
    for _ in range(40):
        mult = [gamma * Fraction(u, w) for (u, v, w) in tab]
        g = [Fraction(1)] * Q
        conv = False
        for _ in range(Q + 2):
            ch = False
            for r in range(Q):
                b = mult[r] * max(g[s] for s in succ[r])
                if b > g[r]:
                    g[r] = b
                    ch = True
            if not ch:
                conv = True
                break
        if conv:
            L = 1
            for x in g:
                L = L * x.denominator // math.gcd(L, x.denominator)
            c = [int(x * L) for x in g]
            assert all(c[s] * tab[r][0] < c[r] * tab[r][2] for r in range(Q) for s in succ[r])
            return c
        gamma = 1 + (gamma - 1) / 2
    return None


def verdict(Q, tab):
    """'CERT' (with a verified integer potential) / 'OBST-critical' / 'OBST-expanding'."""
    assert hyp(Q, tab)
    tc = translation_cycle(Q, tab)
    if tc is not None:
        return "OBST-critical", tc
    bc = bad_cycle(Q, tab)
    if bc is not None:
        return "OBST-expanding", bc
    c = potential(Q, tab)
    assert c is not None, "no bad cycle but no potential: contradicts Lemma 4"
    return "CERT", c


def fast_verdict(Q, tab):
    """Exact verdict without a potential (for bulk counts): compress the w = 1 chains.
    Returns 'CERT', 'OBST-critical' or 'OBST-expanding'."""
    succ = graph(Q, tab)
    one = [w == 1 for (u, v, w) in tab]
    # w=1 vertices form a functional graph; a cycle inside it has product prod u >= 1
    state = [0] * Q   # 0 unknown, 1 leads to a w>1 vertex
    target = [None] * Q
    mul = [1] * Q
    crit = exp = False
    for r0 in range(Q):
        if not one[r0] or state[r0]:
            continue
        path, pos, r = [], {}, r0
        while one[r] and not state[r] and r not in pos:
            pos[r] = len(path)
            path.append(r)
            r = succ[r][0]
        if one[r] and r in pos:     # cycle of w=1 vertices
            cyc = path[pos[r]:]
            if all(tab[x][0] == 1 for x in cyc):
                crit = True
            else:
                exp = True
            for x in path:
                state[x] = 2
            continue
        if one[r] and state[r] == 2:
            for x in path:
                state[x] = 2
            continue
        # r is a w>1 vertex or a resolved w=1 vertex
        if one[r]:
            t, m = target[r], mul[r]
        else:
            t, m = r, 1
        for x in reversed(path):
            m *= tab[x][0]
            target[x], mul[x] = t, m
            state[x] = 1
    if crit:
        return "OBST-critical"
    if exp:
        return "OBST-expanding"
    big = [r for r in range(Q) if not one[r]]
    edges = []
    for x in big:
        u, v, w = tab[x]
        for s in succ[x]:
            if one[s]:
                if state[s] != 1:
                    continue      # leads into a w=1 cycle (already reported)
                edges.append((x, target[s], Fraction(u * mul[s], w)))
            else:
                edges.append((x, s, Fraction(u, w)))
    d = {x: Fraction(1) for x in big}
    for it in range(len(big) + 1):
        ch = False
        for (x, y, m) in edges:
            z = d[x] * m
            if z > d[y]:
                d[y] = z
                ch = True
        if not ch:
            return "CERT"
    return "OBST-expanding"


# ------------------------------------------------------------------ progressions (Lemma 1)

def progression(Q, tab, walk):
    """Return (a, M, A, B, D): {n >= 1 following walk} = {a + M t : t >= 0} and
    T^L n = (A n + B)/D on it.  Built by solving one linear congruence per step."""
    a = walk[0] % Q or Q
    M = Q
    A, B, D = 1, 0, 1
    for i in range(len(walk) - 1):
        u, v, w = tab[walk[i]]
        A, B, D = A * u, B * u + v * D, D * w
        # T^{i+1}(a + M t) = (A (a + M t) + B)/D = y0 + K t
        assert (A * a + B) % D == 0 and (A * M) % D == 0
        y0, K = (A * a + B) // D, (A * M) // D
        g = math.gcd(K, Q)
        s = walk[i + 1]
        if (s - y0) % g:
            return None
        h = Q // g
        t0 = ((s - y0) // g * pow(K // g, -1, h)) % h if h > 1 else 0
        a, M = a + M * t0, M * h
    return a, M, A, B, D


# ------------------------------------------------------------------ depth (Theorem 3)

def depth(Q, tab, want_walk=False, maxstates=3 * 10 ** 6):
    """Lambda = max length of a non-descending walk; returns k* = Lambda + 1
    (and one deepest walk, a list of Lambda+1 residues followed by the descending vertex)."""
    mult = [Fraction(u, w) for (u, v, w) in tab]
    succ = graph(Q, tab)
    trans = [u == 1 and w == 1 for (u, v, w) in tab]
    # state after a non-descending prefix: (current vertex, product, drift if translation-only)
    layer = {(r, Fraction(1), 0): None for r in range(Q)}
    hist = [layer]
    j = 0
    while True:
        j += 1
        nxt = {}
        for st in layer:
            r, P, dr = st
            nP = P * mult[r]
            nd = dr + tab[r][1] if (dr is not None and trans[r]) else None
            if nP < 1 or (nP == 1 and nd < 0):
                continue                  # this prefix (length j) descends
            for s in succ[r]:
                key = (s, nP, nd if nP == 1 else None)
                if key not in nxt:
                    nxt[key] = st
        if not nxt:
            break
        assert len(nxt) < maxstates
        if want_walk:
            hist.append(nxt)
        layer = nxt
    kstar = j
    if not want_walk:
        return kstar
    st = next(iter(hist[-1]))
    walk = [st[0]]
    for lay in reversed(hist[1:]):
        st = lay[st]
        walk.append(st[0])
    walk.reverse()
    return kstar, walk


# ------------------------------------------------------------------ GLOBAL (Theorem 2)

def bounds(Q, tab, c):
    succ = graph(Q, tab)
    N = []
    for r, (u, v, w) in enumerate(tab):
        b = 0
        for s in succ[r]:
            den = c[r] * w - c[s] * u
            assert den > 0
            if v > 0:
                b = max(b, (c[s] * v) // den)
        N.append(b)
    return N


def all_cycles_upto(Q, tab, X, cap=10 ** 7):
    """Cycles reached from every start 1..X (each written from its minimum)."""
    T = stepper(Q, tab)
    done = {}
    cycles = set()
    for n in range(1, X + 1):
        path, pos, x = [], {}, n
        while x not in done and x not in pos:
            pos[x] = len(path)
            path.append(x)
            x = T(x)
            assert len(path) < cap
        if x in pos:
            cyc = path[pos[x]:]
            k = cyc.index(min(cyc))
            cycles.add(tuple(cyc[k:] + cyc[:k]))
        for y in path:
            done[y] = 1
    return sorted(cycles)


def settle(Q, tab):
    """Full independent settlement: verdict, potential, cycle list, k*, witness walk."""
    v, c = verdict(Q, tab)
    if v != "CERT":
        return dict(verdict=v, cycle=c)
    N = bounds(Q, tab, c)
    X = max(N + [Q])
    cyc = all_cycles_upto(Q, tab, X)
    return dict(verdict=v, c=c, X=X, cycles=cyc)
