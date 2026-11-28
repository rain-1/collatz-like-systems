"""Round 4, lens 'integrality': shared exact tools.

Table format (same as round3/accel/accel_lib.py): (p, m, table) with
table[r] = (u, v, w) for r in range(p**m), acting as n -> (u n + v)/w on
n = r (mod p^m); w = p^e, p does not divide u, u >= 1.

Everything returned as proof data is exact (int / Fraction).
"""
import sys, os, math
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
R3 = os.path.join(HERE, "..", "..", "round3")
sys.path.insert(0, os.path.join(R3, "accel"))
sys.path.insert(0, os.path.join(R3, "dichotomy"))
import accel_lib as AL      # noqa: E402
import decide as DC         # noqa: E402


# ----------------------------------------------------------------- basics
def step_fn(p, m, table):
    Q = p ** m

    def T(n):
        u, v, w = table[n % Q]
        x = u * n + v
        assert x % w == 0
        return x // w
    return T


def positivity_ok(p, m, table, upto=None):
    """(P): T(n) >= 1 for n >= 1 (T increasing on each class, so check the
    least positive n of each class) and exact divisibility on each class."""
    Q = p ** m
    for r in range(Q):
        u, v, w = table[r]
        if u < 1 or u % p == 0:
            return False
        ww, e = w, 0
        while ww % p == 0:
            ww //= p
            e += 1
        if ww != 1 or e > m:
            return False
        if (u * r + v) % w or (u * (r + Q) + v) % w:
            return False
        n0 = r if r > 0 else Q
        if (u * n0 + v) // w < 1:
            return False
    return True


# ----------------------------------------------------------------- exact cycle search
def _exact_extreme_cycle(nodes, E, sign):
    """Exact multiplicative Bellman-Ford on the subgraph `nodes`.
    sign=+1: return a cycle with multiplier > 1 if one exists, else None.
    sign=-1: return a cycle with multiplier < 1 if one exists, else None."""
    ns = list(nodes)
    S = set(ns)
    ed = [(r, s, q if sign > 0 else 1 / q) for r in ns for s, q in E[r] if s in S]
    d = {r: Fraction(1) for r in ns}
    pred = {r: None for r in ns}
    last = None
    for _ in range(len(ns) + 1):
        last = None
        for r, s, q in ed:
            x = d[r] * q
            if x > d[s]:
                d[s] = x
                pred[s] = r
                last = s
        if last is None:
            return None
    x = last
    for _ in range(len(ns)):
        x = pred[x]
    cyc, y = [x], pred[x]
    while y != x:
        cyc.append(y)
        y = pred[y]
    cyc.reverse()
    return cyc


def cycle_mult(E, cyc):
    lam = Fraction(1)
    L = len(cyc)
    for i in range(L):
        r, s = cyc[i], cyc[(i + 1) % L]
        qs = [q for t, q in E[r] if t == s]
        assert qs, "not a walk"
        lam *= qs[0]
    return lam


def scc_types(p, m, table, K=None):
    """Exact SCC classification of G_K (trichotomy.md) refined by whether a
    type-(c) SCC also contains a contracting cycle.

    Returns (E, comps); each comp is a dict with
      kind: 'trivial' | 'a' (all cycles contract, exact weights) |
            'b' (single simple cycle; lam exact) |
            'c_mixed' (expanding AND contracting cycle, not a simple cycle) |
            'c_exp'   (expanding cycle, no contracting cycle, not simple) |
            'neutral' (anything else: e.g. only multiplier-1 cycles)
      exp_cycle / con_cycle: explicit exact witness cycles where relevant.
    """
    if K is None:
        K = m
    E = AL.graph(p, m, table, K)
    out = []
    for comp in AL.tarjan(list(range(p ** K)), E):
        if not AL.internal_edges(comp, E):
            out.append(dict(kind="trivial", nodes=comp))
            continue
        sc = AL.simple_cycle(comp, E)
        if sc is not None:
            out.append(dict(kind="b" if sc[1] > 1 else ("a" if sc[1] < 1 else "neutral"),
                            nodes=comp, cycle=sc[0], lam=sc[1]))
            continue
        ce = _exact_extreme_cycle(comp, E, +1)
        cc = _exact_extreme_cycle(comp, E, -1)
        if ce is None:
            out.append(dict(kind="a" if cc is not None else "neutral", nodes=comp))
            continue
        le = cycle_mult(E, ce)
        assert le > 1
        if cc is not None:
            lc = cycle_mult(E, cc)
            assert lc < 1
            out.append(dict(kind="c_mixed", nodes=comp, exp_cycle=ce, exp_lam=le,
                            con_cycle=cc, con_lam=lc))
        else:
            out.append(dict(kind="c_exp", nodes=comp, exp_cycle=ce, exp_lam=le))
    return E, out


def system_type(p, m, table, K=None):
    _, comps = scc_types(p, m, table, K)
    kinds = {c["kind"] for c in comps}
    for k in ("c_mixed", "c_exp", "b", "neutral", "a"):
        if k in kinds:
            return k, comps
    return "a", comps


def compose(p, m, table, walk_residues):
    """Composed affine map x -> A x + B along a list of residues (mod p^m)."""
    Q = p ** m
    A, B = Fraction(1), Fraction(0)
    for r in walk_residues:
        u, v, w = table[r % Q]
        A, B = A * Fraction(u, w), (B * u + v) / Fraction(w)
    return A, B


def periodic_point(p, m, table, K, cyc):
    """Exact periodic point of the closed walk cyc in G_K and its multiplier."""
    A, B = compose(p, m, table, cyc)
    assert A != 1
    x = B / (1 - A)
    # it follows the walk
    y = x
    for r in cyc:
        assert AL.padic_residue(y, p, K) == r
        u, v, w = table[r % p ** m]
        y = (u * y + v) / w
    assert y == x
    return x, A


def decide_verdict(p, m, table):
    res = DC.decide(p ** m, table, want_cycles=False, want_depth=False)
    return res["verdict"]


# ----------------------------------------------------------------- orbits (EVIDENCE only)
def run_orbits(T, N, maxsteps=20000, cap=10 ** 40):
    """Iterate n = 1..N; returns (cycle minima found, number of n that passed
    cap or maxsteps, max over n of log(max orbit)/log(n) for n >= 16)."""
    known = {}
    cyc_min = set()
    escaped = 0
    worst = 0.0
    for n in range(1, N + 1):
        seen = {}
        x = n
        mx = n
        t = 0
        while x not in seen and x not in known:
            seen[x] = t
            x = T(x)
            t += 1
            if x > mx:
                mx = x
            if x > cap or t > maxsteps:
                break
        else:
            if x in seen:
                # new cycle
                c = [x]
                y = T(x)
                while y != x:
                    c.append(y)
                    y = T(y)
                cm = min(c)
                cyc_min.add(cm)
                tgt = cm
            else:
                tgt = known[x]
            for y in seen:
                known[y] = tgt
            if n >= 16:
                worst = max(worst, math.log(mx) / math.log(n))
            continue
        escaped += 1
    return sorted(cyc_min), escaped, worst
