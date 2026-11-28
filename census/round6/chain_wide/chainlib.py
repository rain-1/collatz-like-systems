"""Round 6, lens "chain_wide": occupation bound, multiplier bound and chain
theorem for a general single-prime table map (theory in THEORY.md).

Exact objects only enter proofs: Fractions and Python ints.  Floating point is
used to *search* (the moment parameter s) and for printing.

Re-uses the state graph G(T) and the exact supermartingale certificates of
census/round3/density (density_lib.build_graph, density_lib.best_certificate).
"""
import math
import os
import sys
from fractions import Fraction as Fr
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(CENSUS, "round3", "density"))
import density_lib as D  # noqa: E402


# ------------------------------------------------------------------ maps ---

def table_map(name, Q, table, rule=""):
    return D.TableMap(name, Q, table, rule=rule)


def single_prime(T):
    return len(T.primes) == 1


def nonneg_constants(T):
    return all(v >= 0 for (_, v, _) in T.table)


# ------------------------------------------------- raw prefix slopes -------

def _process_trace(T, K, beta):
    """Like density_lib._process, but returns the list of cumulative raw
    slopes (Fractions) of the decided steps."""
    F = Fr(1)
    trace = []
    seen = set()
    while True:
        row = D._decide(T, K, beta)
        if row is None:
            return K, beta, trace
        assert (K, beta) not in seen
        seen.add((K, beta))
        u, v, w = row
        K2 = K * u // w
        keep = 1
        for p in T.primes:
            keep *= p ** D.vp(K2, p)
        beta = ((u * beta + v) // w) % keep
        K = keep
        F *= Fr(u, w)
        trace.append(F)


def raw_prefix_ok(g):
    """Every raw intermediate slope inside an edge is >= min(1, F_edge)."""
    T = g.T
    bad = []
    for e in g.edges:
        K, beta = g.states[e.src]
        _, _, tr = _process_trace(T, K * e.q, (beta + K * e.digit) % (K * e.q))
        assert (tr[-1] if tr else Fr(1)) == e.F
        lo = min(Fr(1), e.F)
        if any(x < lo for x in tr):
            bad.append((e.src, e.digit, tr))
    return bad


# ------------------------------------------- the sigma-tree on integers ---

class Node:
    __slots__ = ("M", "r", "a", "b", "A", "state")


def sigma_root(g, k):
    """Root of the tree of state k: integers y = beta (mod K), value y."""
    K, beta = g.states[k]
    n = Node()
    n.M, n.r, n.a, n.b, n.A, n.state = K, beta % K, K, beta % K, Fr(1), k
    return n


def _qpart(T, x):
    keep = 1
    for p in T.primes:
        keep *= p ** D.vp(x, p)
    return keep


def children(g, nd):
    """Split once by p and apply decided branches.  Returns list of
    (child, F) in the order of t's digit e (child.r = nd.r + nd.M e)."""
    T = g.T
    p = T.primes[0]
    out = []
    for e in range(p):
        c = Node()
        c.M, c.r = nd.M * p, nd.r + nd.M * e
        a, b = nd.a * p, nd.b + nd.a * e
        F = Fr(1)
        while True:
            K = _qpart(T, a)
            row = D._decide(T, K, b % K)
            if row is None:
                break
            u, v, w = row
            assert (u * a) % w == 0 and (u * b + v) % w == 0
            a, b = u * a // w, (u * b + v) // w
            F *= Fr(u, w)
        c.a, c.b = a, b
        c.A = nd.A * F
        K = _qpart(T, a)
        c.state = g.index[(K, b % K)]
        out.append((c, F))
    return out


def survivor_classes(g, depth):
    """For each state k: the classes y mod M (M = K_k p^depth) whose tree
    path has every prefix slope (after >= 1 edge) strictly > 1.
    Returns dict k -> list of (M, r)."""
    res = {}
    for k in range(len(g.states)):
        level = [sigma_root(g, k)]
        for d in range(depth):
            nxt = []
            for nd in level:
                for c, F in children(g, nd):
                    if c.A > 1:
                        nxt.append(c)
            level = nxt
        res[k] = [(nd.M, nd.r) for nd in level]
    return res


def forced_congruence(g, depth):
    """Largest D <= depth with all survivor classes (all states) in one class
    y mod p^D; returns (D, residue, number of classes, density)."""
    p = g.T.primes[0]
    sc = survivor_classes(g, depth)
    allc = [(M, r) for k in sc for (M, r) in sc[k]]
    if not allc:
        return None
    best = (0, 0)
    for Dd in range(1, depth + 1):
        s = {r % p ** Dd for (M, r) in allc}
        if len(s) == 1:
            best = (Dd, s.pop())
        else:
            break
    dens = sum(Fr(1, M) for (M, r) in allc)   # Haar mass of all survivor classes
    return best[0], best[1], len(allc), dens


# --------------------------------------------------- occupation constants ---

def certificate(g):
    """Certificate (N) with 0 < gamma <= 1.  REVISION after REFEREE1: a best
    certificate with gamma > 1 (very strongly contracting map) is clipped to
    gamma = 1 (theta = 0).  This is valid because N_{s,1} = p^{1-gamma} N_{s,gamma}
    <= N_{s,gamma} entrywise; the clipped inequality is re-checked exactly."""
    C = D.best_certificate(g, c=Fr(1), sign=+1)
    assert C.s > 0 and 0 < C.gamma
    C.gamma_unclipped = C.gamma
    if C.gamma > 1:
        C.gamma = Fr(1)
        C.theta = Fr(0)
    # exact re-check of the supermartingale inequality at the gamma actually used
    assert D.check_supermartingale(g, C.s, C.gamma, C.w) is not None
    return C


def occupation_constants(g, C):
    """Exact constants for THEORY.md Theorems 1-2 (single-prime maps).
    W = sum_k w(k)/w_min; Fmax; g_err = max over edges with G != 0 of |G|/F;
    Gpos = max positive G."""
    W = sum(C.w) / C.wmin
    Fmax = max(e.F for e in g.edges)
    gerr = max((abs(e.G) / e.F for e in g.edges if e.G != 0), default=Fr(0))
    Gpos = max((e.G for e in g.edges if e.G > 0), default=Fr(0))
    return dict(W=W, Fmax=Fmax, gerr=gerr, Gpos=Gpos, theta=1 - C.gamma, s=C.s,
                nstates=len(g.states))


def multiplier_E(g, C, k0, p=None, kmax=4000, factor=1):
    """Upper bound for E = total log error of a non-eventually-periodic orbit
    all of whose values are >= p^k0 (Theorem 3).  Exact rational arithmetic
    with rigorous upper bounds for the irrational powers.  Returns a Fraction
    or None if the self-consistency factor is >= 1.
    factor = 1 under (P) (g' = g), factor = 2 for signed maps (g' = 2g); g' is
    used in BOTH the numerator and the self-consistency factor lam
    (REVISION after REFEREE1: the signed value used g in lam before)."""
    p = p or g.T.primes[0]
    oc = occupation_constants(g, C)
    th, s, W, ge = oc["theta"], oc["s"], oc["W"], oc["gerr"] * factor
    if ge == 0:
        return Fr(0)
    # S1 = sum_{k>=k0} p^{(k+1)th - k} = p^th * p^{-k0(1-th)} / (1 - p^{-(1-th)})
    a = D.upow(p, th)
    b = D.upow(p, -k0 * (1 - th))
    c = D.upow(p, -(1 - th))
    if c >= 1:
        return None
    S1 = a * b / (1 - c)
    # S2 = sum_{k>=k0} (k+1)/p^k = p^{-k0} (k0+1 - k0/p) / (1-1/p)^2  (exact)
    q = Fr(1, p)
    S2 = q ** k0 * ((k0 + 1) * (1 - q) + q) / (1 - q) ** 2
    lam = ge * s * S2
    if lam >= 1:
        return None
    return ge * W * a * S1 / (1 - lam)


def chain_count(F, B, base=2):
    """Largest k >= 0 with F^k < base^B (exact)."""
    F = Fr(F)
    k = 0
    while (F ** (k + 1)) < base ** B:
        k += 1
    return k


def slope_values(g):
    return sorted({e.F for e in g.edges})


# ---------------------------------------------------- exact orbit tools ---

def find_cycles(step, N=20000, cap=100000):
    """Cycles met by orbits of 1..N (Brent); raises if some orbit exceeds cap."""
    cyc = {}
    for n in range(1, N + 1):
        x, seen = n, {}
        for t in range(cap):
            if x in seen:
                break
            seen[x] = t
            x = step(x)
        else:
            raise RuntimeError("orbit of %d not periodic within cap" % n)
        # x is on the cycle
        c, y = [x], step(x)
        while y != x:
            c.append(y)
            y = step(y)
        m = min(c)
        cyc[m] = c
    return cyc


def signed(g):
    return any(e.G < 0 for e in g.edges)


def multiplier_E_signed(g, C, k0):
    """As multiplier_E, valid also with negative intercepts: |log(1+u)| <= 2|u|
    for |u| <= 1/2, so the error constant doubles (needs gerr / p^k0 <= 1/2)."""
    p = g.T.primes[0]
    oc = occupation_constants(g, C)
    if not signed(g):
        return multiplier_E(g, C, k0)
    assert oc["gerr"] <= Fr(p ** k0, 2)
    return multiplier_E(g, C, k0, factor=2)


def certificate_at(g, s):
    """Exact certificate at a given rational s > 0 with gamma just below gamma*(s)."""
    gs = D.gamma_star(g, float(s))
    if gs <= 1e-6:
        return None
    gamma = D.simple_rational_in(gs - 3e-6, gs - 2e-7)
    if gamma <= 0:
        return None
    gamma = min(gamma, Fr(1))   # clip (see certificate); N_{s,1} <= N_{s,gamma}
    try:
        C = D.certify(g, Fr(s), gamma)
    except ValueError:
        return None
    C.theta = 1 - C.gamma
    return C


def best_E(g, k0, grid=None):
    """Smallest certified multiplier error over a grid of s (exact for each)."""
    best = None
    grid = grid or [Fr(i, 40) for i in range(1, 200)]
    for s in grid:
        C = certificate_at(g, s)
        if C is None:
            continue
        E = multiplier_E_signed(g, C, k0)
        if E is not None and (best is None or E < best[0]):
            best = (E, C)
    return best


def raw_constants(g):
    """R = max raw steps per edge; c_raw = min(1, min non-final raw prefix slope)."""
    T = g.T
    R, c = 0, Fr(1)
    for e in g.edges:
        K, beta = g.states[e.src]
        _, _, tr = _process_trace(T, K * e.q, (beta + K * e.digit) % (K * e.q))
        R = max(R, len(tr))
        for x in tr[:-1]:
            c = min(c, x)
    return R, c


def expansion_formula(g):
    """If the edge slopes other than 1 are exactly {rho > 1, kappa < 1}, a link
    with e contracting edges has exactly a = floor(e*L) + 1 expanding edges,
    L = log(1/kappa)/log(rho).  Returns (rho, kappa, L) or None."""
    vals = sorted({e.F for e in g.edges if e.F != 1})
    ex = [v for v in vals if v > 1]
    co = [v for v in vals if v < 1]
    if len(ex) == 1 and len(co) == 1:
        return ex[0], co[0], math.log(1 / co[0]) / math.log(ex[0])
    return None


def update_chain(g, x0, nupd):
    """The update chain of the integer x0 in the root tree: list of
    (state, value y_l, cumulative slope P_l, raw steps so far)."""
    T = g.T
    p = T.primes[0]
    nd = sigma_root(g, 0)
    assert g.states[0] == (1, 0)
    out = [(0, x0, Fr(1))]
    for _ in range(nupd):
        t = (x0 - nd.r) // nd.M
        e = t % p
        c, F = children(g, nd)[e]
        nd = c
        tt = (x0 - nd.r) // nd.M
        out.append((nd.state, nd.a * tt + nd.b, nd.A))
    return out


# ------------------------------------------------ REVISION after REFEREE1 ---

def all_constants_nonneg(T):
    """Hypothesis (P) as used in the proofs: every v_r >= 0 (this gives G_e >= 0
    and nonnegative partial intercepts inside every edge)."""
    return all(v >= 0 for (_, v, _) in T.table)


def max_nonzero_v_steps_per_edge(g):
    """Largest number of raw steps with v != 0 inside one edge.  If it is <= 1,
    the raw-time value of Z = x/P inside an edge equals Z at one of the two
    updates bounding the edge (steps with v = 0 leave Z unchanged)."""
    T = g.T
    best = 0
    for e in g.edges:
        K, beta = g.states[e.src]
        KK, bb = K * e.q, (beta + K * e.digit) % (K * e.q)
        cnt = 0
        while True:
            row = D._decide(T, KK, bb)
            if row is None:
                break
            u, v, w = row
            cnt += (v != 0)
            K2 = KK * u // w
            keep = 1
            for pp in T.primes:
                keep *= pp ** D.vp(K2, pp)
            bb = ((u * bb + v) // w) % keep
            KK = keep
        best = max(best, cnt)
    return best
