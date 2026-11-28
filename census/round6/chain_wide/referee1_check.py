"""REFEREE 1 independent checks for round6/chain_wide.  Written from scratch by the referee.

Exit status 0 iff every check passes.  Known findings are reported as FAIL lines (they are
real defects of the submission, see REFEREE1.md), so the script is expected to exit 1 until
they are repaired.

Independent of the prover's code: the maps are re-typed from the rule strings in README.md,
the adaptive tree / state graph / survivor classes / update chains are re-implemented here,
the exact power bounds use integer n-th roots (not density_lib.upow), E* is recomputed with
50-digit Decimal arithmetic from the formula in THEORY.md Theorem 3, the range check is a
numpy re-run, and the chain theorem is tested on actual integer orbits.
The only things taken from the prover's code are DATA: their certificate weight vectors w
(which are then verified exactly here) and the rows of data/*.json being checked.

Usage: <numpy python> referee1_check.py [--quick]
"""
import json
import math
import os
import random
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as Fr
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
QUICK = "--quick" in sys.argv
FAILS = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" | " + detail) if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)


def info(s):
    print("INFO " + s, flush=True)


random.seed(424242)

# ---------------------------------------------------------------- A. maps from rule text ---
S_PLUS9 = tuple(r for r in range(1, 32, 2) if r not in (19, 27, 31))


def m_par(a, d):
    return 2, 2, {0: (1, 0, 2), 1: (a, d, 1)}


def m_sf(S, Q=8, a=3):
    return 2, Q, {r: ((1, 0, 2) if r % 2 == 0 else ((a, 1, 1) if r in S else (1, 1, 1))) for r in range(Q)}


def m_split(a, d):
    return 2, 4, {0: (1, 0, 2), 2: (1, 0, 2), 1: (a, d, 1), 3: (1, d, 1)}


MY = {}
for d in (1, -1, 3, 5, 7, 9, 13, 17):
    MY["par_3_%s%d" % ("m" if d < 0 else "", abs(d))] = m_par(3, d)
for S, nm in [((7,), "sf3_7"), ((1, 7), "sf3_17"), ((5, 7), "sf3_57"), ((1, 5, 7), "sf3_157"),
              ((3, 5, 7), "sf3_357"), ((1, 3), "sf3_13"), ((1, 3, 5), "sf3_135")]:
    MY[nm] = m_sf(S)
MY["split5_1"] = m_split(5, 1)
MY["split5_3"] = m_split(5, 3)
MY["m3_b"] = (3, 3, {0: (1, 0, 3), 1: (4, -1, 3), 2: (4, 1, 3)})
MY["m3_d"] = (3, 3, {0: (1, 0, 3), 1: (4, 2, 1), 2: (4, 1, 1)})
MY["m3_g"] = (3, 3, {0: (1, 0, 3), 1: (5, 1, 1), 2: (5, 2, 1)})
MY["desc_split7_1"] = m_split(7, 1)
MY["desc_m3_4n5"] = (3, 3, {0: (1, 0, 3), 1: (4, 5, 1), 2: (2, 2, 1)})
MY["desc_s32_plus9"] = m_sf(S_PLUS9, Q=32)
EXPANDING = {"par_5_1": m_par(5, 1), "par_7_1": m_par(7, 1), "sf3_137": m_sf((1, 3, 7))}


def step_of(m):
    p, Q, tb = m

    def st(n):
        u, v, w = tb[n % Q]
        x = u * n + v
        assert x % w == 0 and x > 0
        return x // w
    return st


sys.path.insert(0, HERE)
import chain_systems as CS  # noqa: E402  (prover's tables: compared, not used)

for id, m in list(MY.items()) + list(EXPANDING.items()):
    T = CS.BY_ID[id]["T"]
    st = step_of(m)
    check("[A] my table for %s (from rule text) agrees with prover's on 1..100000" % id,
          all(st(n) == T.step(n) for n in range(1, 100001)))
    p, Q, tb = m
    check("[A] %s: unit multipliers (p does not divide u) and w a power of p" % id,
          all(u % p and (w & (w - 1) == 0 if p == 2 else w in (1, 3)) for (u, v, w) in tb.values()))


# ---------------------------------------------------------------- B. my state graph ---
def pp(x, p):
    k = 1
    while x % p == 0:
        x //= p
        k *= p
    return k


def decide(m, K, beta):
    p, Q, tb = m
    g = gcd(K, Q)
    rows = {tb[r] for r in range(beta % g, Q, g)}
    if len(rows) != 1:
        return None
    u, v, w = next(iter(rows))
    if K % w or (u * beta + v) % w:
        return None
    return u, v, w


def process(m, K, beta):
    """apply decided steps; returns K, beta, F, G, raw list of (u,v,w)"""
    F, G, raw, seen = Fr(1), Fr(0), [], set()
    while True:
        row = decide(m, K, beta)
        if row is None:
            return K, beta, F, G, raw
        if (K, beta) in seen:
            raise ValueError("loop")
        seen.add((K, beta))
        u, v, w = row
        K2 = pp(K * u // w, m[0])
        beta = ((u * beta + v) // w) % K2
        K = K2
        F *= Fr(u, w)
        G = G * Fr(u, w) + Fr(v, w)
        raw.append(row)


class G_:
    pass


def graph(m):
    p = m[0]
    K0, b0, _, _, raw0 = process(m, 1, 0)
    assert not raw0
    states, idx, edges = [(K0, b0)], {(K0, b0): 0}, []
    i = 0
    while i < len(states):
        K, beta = states[i]
        for d in range(p):
            yres = beta + K * d   # residue of y mod pK
            K1, b1, F, G, raw = process(m, K * p, yres % (K * p))
            if (K1, b1) not in idx:
                idx[(K1, b1)] = len(states)
                states.append((K1, b1))
                if len(states) > 3000:
                    raise ValueError("too many states")
            edges.append(dict(src=i, dst=idx[(K1, b1)], yres=yres % (K * p), F=F, G=G, raw=raw))
        i += 1
    g = G_()
    g.m, g.p, g.states, g.idx, g.edges = m, p, states, idx, edges
    g.out = {}
    for e in edges:
        g.out[(e["src"], e["yres"])] = e
    return g


def prefix_slopes(raw):
    out, F = [], Fr(1)
    for (u, v, w) in raw:
        F *= Fr(u, w)
        out.append(F)
    return out


def graph_facts(g):
    Fs = [e["F"] for e in g.edges]
    rho = max(Fs)
    R = max(len(e["raw"]) for e in g.edges)
    craw = Fr(1)
    Rok = True
    for e in g.edges:
        ps = prefix_slopes(e["raw"])
        for x in ps[:-1]:
            craw = min(craw, x)
        lo = min(Fr(1), e["F"])
        if any(x < lo for x in ps):
            Rok = False
    signed = any(e["G"] < 0 for e in g.edges)
    gerr = max((abs(e["G"]) / e["F"] for e in g.edges if e["G"] != 0), default=Fr(0))
    return dict(rho=rho, R=R, craw=craw, Rok=Rok, signed=signed, gerr=gerr,
                slopes=sorted(set(Fs)), nstates=len(g.states))


def A_of(F, B, base=2):
    F = Fr(F)
    k = 0
    while F ** (k + 1) < Fr(base) ** B:
        k += 1
    return k


def kstar(g):
    sl = sorted(set(e["F"] for e in g.edges))
    rho = max(sl)
    km = max(v for v in sl if v < 1)
    k = 0
    while rho ** k * km <= 1:
        k += 1
    return k


# ---------------------------------------------------------- C. survivors (sigma-trees) ---
def tree_children(g, nd):
    m, p = g.m, g.p
    M, r, a, b, A = nd
    out = []
    for d in range(p):
        M2, r2, a2, b2, A2 = M * p, r + M * d, a * p, b + a * d, A
        while True:
            K = pp(a2, p)
            row = decide(m, K, b2 % K)
            if row is None:
                break
            u, v, w = row
            assert (u * a2) % w == 0 and (u * b2 + v) % w == 0
            a2, b2, A2 = u * a2 // w, (u * b2 + v) // w, A2 * Fr(u, w)
        out.append((M2, r2, a2, b2, A2))
    return out


def survivors(g, depth):
    allc = []
    for (K, beta) in g.states:
        level = [(K, beta % K, K, beta % K, Fr(1))]
        for _ in range(depth):
            level = [c for nd in level for c in tree_children(g, nd) if c[4] > 1]
        allc += [(nd[0], nd[1]) for nd in level]
    p = g.p
    D, res = 0, 0
    for Dd in range(1, depth + 1):
        s = {r % p ** Dd for (M, r) in allc}
        if len(s) == 1:
            D, res = Dd, s.pop()
        else:
            break
    mass = sum(Fr(1, M) for (M, r) in allc)
    return D, res, len(allc), mass


# ------------------------------------------------------------- D. exact power bounds ---
def iroot(N, b):
    """floor(N^(1/b)) for N >= 0"""
    if N < 2:
        return N
    x = 1 << (N.bit_length() // b + 1)
    while True:
        y = ((b - 1) * x + N // x ** (b - 1)) // b
        if y >= x:
            break
        x = y
    while x ** b > N:
        x -= 1
    while (x + 1) ** b <= N:
        x += 1
    return x


PREC = 70


def pow_up(x, r):
    """rational U >= x^r, x > 0 rational, r rational"""
    x, r = Fr(x), Fr(r)
    if r < 0:
        x, r = 1 / x, -r
    if r == 0 or x == 1:
        return Fr(1)
    a, b = r.numerator, r.denominator
    num = x.numerator ** a << (PREC * b)
    den = x.denominator ** a
    N = -(-num // den)
    y = iroot(N, b)
    if y ** b < N:
        y += 1
    return Fr(y, 1 << PREC)


def verify_cert(g, s, gamma, wmap):
    """sum_e p^(gamma-1) F^s w(dst) <= w(src), exactly; wmap: state key -> Fraction"""
    pg = pow_up(g.p, gamma - 1)
    cache = {}
    for i, key in enumerate(g.states):
        tot = Fr(0)
        for e in g.edges:
            if e["src"] != i:
                continue
            F = e["F"]
            if F not in cache:
                cache[F] = pow_up(F, s)
            tot += pg * cache[F] * wmap[g.states[e["dst"]]]
        if tot > wmap[key]:
            return False
    return True


# ------------------------------------------------------------ E. E* in Decimal ---
getcontext().prec = 50


def Dpow(p, x):
    return (Decimal(p).ln() * Decimal(x.numerator) / Decimal(x.denominator)).exp()


def Estar(p, theta, s, W, gerr, k0, signed):
    th = theta
    gp = Decimal(2 * gerr.numerator) / gerr.denominator if signed else Decimal(gerr.numerator) / gerr.denominator
    S1 = Dpow(p, th) * Dpow(p, -k0 * (1 - th)) / (1 - Dpow(p, -(1 - th)))
    q = Decimal(1) / p
    S2 = sum((k + 1) * q ** k for k in range(k0, k0 + 400))
    lam = gp * Decimal(s.numerator) / s.denominator * S2
    E = gp * Decimal(W.numerator) / W.denominator * Dpow(p, th) * S1 / (1 - lam)
    return E, lam


# -------------------------------------------------------------- run on named systems ---
NJ = json.load(open(os.path.join(HERE, "data", "named.json")))
README_CLAIMS = {  # rho, A1, A10, k*, D, residue (README per-system table)
    "par_3_1": ("3/2", 1, 17, 2, 2, 3), "par_3_m1": ("3/2", 1, 17, 2, 2, 1), "par_3_3": ("3/2", 1, 17, 2, 2, 1),
    "par_3_5": ("3/2", 1, 17, 2, 2, 3), "par_3_7": ("3/2", 1, 17, 2, 2, 1), "par_3_9": ("3/2", 1, 17, 2, 2, 3),
    "par_3_13": ("3/2", 1, 17, 2, 2, 3), "par_3_17": ("3/2", 1, 17, 2, 2, 3),
    "sf3_7": ("3/2", 1, 17, 2, 6, 63), "sf3_17": ("3/2", 1, 17, 1, 6, 63), "sf3_57": ("3/2", 1, 17, 2, 6, 63),
    "sf3_157": ("3/2", 1, 17, 1, 6, 63), "sf3_357": ("3/2", 1, 17, 2, 4, 15), "sf3_13": ("3/2", 1, 17, 1, 10, 1019),
    "sf3_135": ("9/8", 5, 58, 3, 10, 1019), "split5_1": ("5/2", 0, 7, 1, 3, 5), "split5_3": ("5/4", 3, 31, 4, 8, 253),
    "m3_b": ("4/3", 2, 24, 4, 0, None), "m3_d": ("4/3", 2, 24, 4, 0, None), "m3_g": ("5/3", 1, 13, 3, 0, None),
    "desc_split7_1": ("7/4", 1, 12, 2, 4, 5), "desc_m3_4n5": ("4/3", 2, 24, 2, 2, 4),
    "desc_s32_plus9": ("9/4", 0, 8, 1, 3, 7)}

sys.path.insert(0, os.path.join(HERE, "..", "..", "round3", "density"))
import chainlib as L  # noqa: E402  (only to obtain certificate weight vectors w as data)
from density_lib import TableMap  # noqa: E402

GRAPHS = {}
for id, m in MY.items():
    g = graph(m)
    GRAPHS[id] = g
    f = graph_facts(g)
    row = NJ[id]
    cl = README_CLAIMS[id]
    check("[B] %s: states %d, slopes, rho, R, c_raw, (R), signed, g match named.json" % (id, f["nstates"]),
          f["nstates"] == row["states"] and [str(x) for x in f["slopes"]] == row["slopes"]
          and str(f["rho"]) == row["rho"] and f["R"] == row["R"] and str(f["craw"]) == row["c_raw"]
          and f["Rok"] == row["raw_prefix_ok"] and f["signed"] == row["signed"] and str(f["gerr"]) == row["gerr"])
    A1, A10 = A_of(f["rho"], 1), A_of(f["rho"], 10)
    check("[H] %s: rho = %s, A(1) = %d, A(10) = %d, k* = %d as in README" % (id, cl[0], cl[1], cl[2], cl[3]),
          str(f["rho"]) == cl[0] and A1 == cl[1] and A10 == cl[2] and kstar(g) == cl[3]
          and f["rho"] ** A10 < 2 ** 10 <= f["rho"] ** (A10 + 1))
    depth = 14 if g.p == 2 else 9
    if QUICK and id.startswith("desc_s32"):
        depth = 10
    D, res, ncl, mass = survivors(g, depth)
    fr = row["forced"]
    ok = D == cl[4] and (cl[5] is None or res == cl[5])
    if depth == fr["depth"]:
        ok &= ncl == fr["classes"] and str(mass) == fr["mass"]
    check("[C] %s: forced class at depth %d: D=%d residue %d, %d classes, mass %.3g (README/json agree)"
          % (id, depth, D, res, ncl, float(mass)), ok)

# certificates (their w, my exact check), theta, W; then E*
for id, g in GRAPHS.items():
    row = NJ[id]
    g2 = L.D.build_graph(CS.BY_ID[id]["T"])
    C = L.certificate(g2)
    wmap = {g2.states[k]: Fr(C.w[k]) for k in range(len(g2.states))}
    ok = set(wmap) == set(g.states) and verify_cert(g, C.s, C.gamma, wmap)
    W = sum(wmap.values()) / min(wmap.values())
    check("[D] %s: Thm-1/2 certificate (s=%s, theta=%s, W=%.4g) verified exactly by referee code"
          % (id, C.s, 1 - C.gamma, float(W)), ok and str(1 - C.gamma) == row["theta"] and str(W) == row["W"])
    f = graph_facts(g)
    for key, e in row["E"].items():
        C2 = L.certificate_at(g2, Fr(e["s"]))
        wmap2 = {g2.states[k]: Fr(C2.w[k]) for k in range(len(g2.states))}
        ok2 = C2.gamma == Fr(e["gamma"]) and verify_cert(g, C2.s, C2.gamma, wmap2)
        W2 = sum(wmap2.values()) / min(wmap2.values())
        k0 = e["k0p"]
        rng = row["range"] if key == str(row["range"]) else int(key)
        ok2 &= g.p ** k0 <= 2 ** rng
        Etrue, lam = Estar(g.p, 1 - C2.gamma, C2.s, W2, f["gerr"], k0, f["signed"])
        Ejs = Fr(e["E"])
        Edec = Decimal(Ejs.numerator) / Decimal(Ejs.denominator)
        rel = (Edec - Etrue) / Etrue
        check("[E] %s k0=%s^%d: E* (json %.10g) >= E* recomputed from THEORY Thm 3 (%.10g), rel diff %.2e, lambda %.2e"
              % (id, g.p, k0, float(Edec), float(Etrue), float(rel), float(lam)),
              ok2 and Edec >= Etrue and rel < Decimal("1e-6"))
        if f["signed"]:
            # Theorem 3 needs gerr/p^k0 <= 1/2 for |log(1+u)| <= 2|u|
            check("[E] %s signed: g p^-k0 <= 1/2" % id, f["gerr"] <= Fr(g.p ** k0, 2))

# signed systems: raw-time claim of Theorem 3 needs intermediate raw Z inside an edge
for id, g in GRAPHS.items():
    if graph_facts(g)["signed"]:
        mx = max(sum(1 for (u, v, w) in e["raw"] if v != 0) for e in g.edges)
        check("[E] %s signed: every edge has <= 1 raw step with nonzero constant (so raw-time Z equals an "
              "update-time Z and the raw-time two-sided bound follows from the update-level E)" % id, mx <= 1)

# 3x+1 headline numbers
r = NJ["par_3_1"]
check("[E] 3x+1: e^{E*(2^68)} < 31.7 and e^{E*(2^32)} < 1.7e5",
      math.exp(r["E"]["68"]["E_f"]) < 31.7 and math.exp(r["E"]["32"]["E_f"]) < 1.7e5,
      "%.4f, %.4g" % (math.exp(r["E"]["68"]["E_f"]), math.exp(r["E"]["32"]["E_f"])))
# theta for 3x+1 vs optimum and Lagarias
th = Fr(1082, 1139)
s = Fr(41, 84)
lhs = pow_up(2, (1 - th) - 1) * (pow_up(Fr(1, 2), s) + pow_up(Fr(3, 2), s))
check("[D] 3x+1 single-state certificate 2^(gamma-1)((1/2)^s + (3/2)^s) <= 1 at s = 41/84, theta = 1082/1139",
      lhs <= 1, "lhs = 1 - %.3g" % float(1 - lhs))
lo, hi = 0.3, 0.7
f = lambda t: math.log2(2 ** -t + 1.5 ** t)
for _ in range(200):
    a, b = lo + (hi - lo) / 3, hi - (hi - lo) / 3
    if f(a) < f(b):
        hi = b
    else:
        lo = a
info("3x+1 optimal moment exponent theta* = %.9f (float), certified 1082/1139 = %.9f, Lagarias 1-eta = 0.94996"
     % (f(lo), float(th)))

# ----------------------------------------------------- F. range / cycle brute force ---
import numpy as np  # noqa: E402


def cycles_upto(st, N, cap=10 ** 6):
    mins = set()
    for n in range(1, N + 1):
        x, seen = n, set()
        for _ in range(cap):
            if x in seen:
                break
            seen.add(x)
            x = st(x)
        c, y = [x], st(x)
        while y != x:
            c.append(y)
            y = st(y)
        mins.add(min(c))
    return mins


def np_range(m, cyc_elems, LG):
    p, Q, tb = m
    U = np.array([tb[r][0] for r in range(Q)], dtype=np.int64)
    V = np.array([tb[r][1] for r in range(Q)], dtype=np.int64)
    Wt = np.array([tb[r][2] for r in range(Q)], dtype=np.int64)
    ce = np.array(sorted(cyc_elems), dtype=np.int64)
    n = np.arange(1, 1 << LG, dtype=np.int64)
    x = n.copy()
    alive = np.ones(n.size, bool)
    big = []
    st = step_of(m)
    for it in range(100000):
        idx = np.nonzero(alive)[0]
        if idx.size == 0:
            return True, it, big
        xi = x[idx]
        r = xi % Q
        hot = xi > (1 << 56)
        if hot.any():
            for j in idx[hot]:
                big.append(int(n[j]))
            alive[idx[hot]] = False
            idx, xi, r = idx[~hot], xi[~hot], r[~hot]
        y = U[r] * xi + V[r]
        if np.any(y % Wt[r]):
            return False, it, -1
        y //= Wt[r]
        x[idx] = y
        done = (y < n[idx]) | np.isin(y, ce)
        alive[idx[done]] = False
    return False, -1, big


for id, m in MY.items():
    st = step_of(m)
    Nc = 1 << (12 if id == "m3_g" else 16)
    mins = cycles_upto(st, Nc)
    check("[F] %s: cycle minima met by all starts <= %d are %s = named.json list"
          % (id, Nc, sorted(mins)), sorted(mins) == NJ[id]["cycles"])
    elems = set()
    for c in json.load(open(os.path.join(HERE, "data", "ranges_%d_%s.json" % (NJ[id]["range"], id))))[id]["cycles"].values():
        elems |= set(c)
    LG = 16 if id == "m3_g" else (18 if QUICK else 22)
    ok, its, big = np_range(m, elems, LG)
    nb = len(big) if isinstance(big, list) else big
    for n0 in (big if isinstance(big, list) else []):   # finish exactly with Python ints
        x, k = st(n0), 1
        while not (x < n0 or x in elems):
            x, k = st(x), k + 1
            if k > 10 ** 7:
                ok = False
                break
    check("[F] %s: every n < 2^%d reaches a smaller value or a listed cycle (numpy; %d starts went above 2^56 and "
          "were finished exactly)" % (id, LG, nb), ok)

# big ones exactly (m3_g etc.) done inside: re-run exactly for those flagged
# (np_range marks them; finish here)
def finish_big(m, elems, LG):
    st = step_of(m)
    p, Q, tb = m
    # recompute which starts go above 2^56 in Python (small LG only)
    bad = 0
    for n in range(1, 1 << LG):
        x = n
        for _ in range(10 ** 6):
            x = st(x)
            if x < n or x in elems:
                break
        else:
            bad += 1
    return bad == 0


elems_g = set()
for c in NJ["m3_g"].get("cycles") and json.load(open(os.path.join(HERE, "data", "ranges_27_m3_g.json")))["m3_g"]["cycles"].values():
    elems_g |= set(c)
check("[F] m3_g: every n < 2^14 reaches a smaller value or a listed cycle (pure Python, exact)",
      finish_big(MY["m3_g"], elems_g, 14))


# ------------------------------------------------- G. chain theorem on integer orbits ---
def update_chain(g, x0, nupd):
    """my own: list of (state index, y_l, P_l, raw time k_l, edge)"""
    p = g.p
    nd = (1, 0, 1, 0, Fr(1))
    st0 = g.idx[(1, 0)]
    out = [(st0, x0, Fr(1), 0, None)]
    k = 0
    for _ in range(nupd):
        M, r, a, b, A = nd
        t = (x0 - r) // M
        d = t % p
        y = a * t + b
        K = pp(a, p)
        sidx = g.idx[(K, b % K)]
        e = g.out[(sidx, y % (K * p))]
        nd = tree_children(g, nd)[d]
        M, r, a, b, A = nd
        y2 = a * ((x0 - r) // M) + b
        assert y2 == e["F"] * y + e["G"], "Lemma 1 / edge form violated"
        assert A == out[-1][2] * e["F"]
        k += len(e["raw"])
        K2 = pp(a, p)
        out.append((g.idx[(K2, b % K2)], y2, A, k, e))
    return out


def beam_start(g, depth, beam=300):
    """a start whose root-tree path keeps every prefix slope > 1 for `depth` updates"""
    level = [(1, 0, 1, 0, Fr(1))]
    for _ in range(depth):
        nxt = [c for nd in level for c in tree_children(g, nd) if c[4] >= 1]
        if not nxt:
            return None
        random.shuffle(nxt)
        level = nxt[:beam]
    M, r = level[0][0], level[0][1]
    return r + M * random.getrandbits(32)


def chain_tests(id, g, x0, nupd, residue=None, D=0, depth=14, Pmode=True):
    ch = update_chain(g, x0, nupd)
    L_ = len(ch) - 1
    P = [c[2] for c in ch]
    Y = [c[1] for c in ch]
    st = step_of(g.m)
    raw = [x0]
    for _ in range(ch[-1][3]):
        raw.append(st(raw[-1]))
    for (_, y, _, k, _) in ch:
        assert raw[k] == y
    rho = max(e["F"] for e in g.edges)
    Z = [Fr(Y[l]) / P[l] for l in range(L_ + 1)]
    ok = {"Z": all(Z[l + 1] >= Z[l] for l in range(L_)) if Pmode else True}
    sel, t = [], -1
    while t < L_:
        rest = range(t + 1, L_ + 1)
        mn = min(P[l] for l in rest)
        t = max(l for l in rest if P[l] == mn)
        sel.append(t)
    links = list(zip(sel, sel[1:]))
    okb = okc = okd = oka = okf = True
    nf = 0
    two = None
    vals = sorted({e["F"] for e in g.edges if e["F"] != 1})
    if len([v for v in vals if v > 1]) == 1 and len([v for v in vals if v < 1]) == 1:
        two = ([v for v in vals if v > 1][0], [v for v in vals if v < 1][0])
    for (a, b) in links:
        edges = [ch[l + 1][4] for l in range(a, b)]
        ri = P[b] / P[a]
        okb &= edges[0]["F"] > 1 and 1 < ri <= edges[0]["F"] <= rho
        nonunit = [e for e in edges if e["F"] != 1]
        if len(nonunit) > 1:
            okb &= nonunit[-1]["F"] < 1
        if two:
            ae = sum(1 for e in edges if e["F"] == two[0])
            ce = sum(1 for e in edges if e["F"] == two[1])
            Lr = math.log(1 / two[1]) / math.log(two[0])
            okb &= ae == math.floor(ce * Lr) + 1
        Ci = Y[b] - ri * Y[a]
        lo = edges[0]["G"] * ri / edges[0]["F"] + (edges[-1]["G"] if len(edges) > 1 else 0)
        hi = sum(e["G"] for e in edges)
        if Pmode:
            okc &= lo <= Ci <= hi
        # (a): raw multiplier from k_a never below 1 within segment, raw values > x_a
        ka = ch[a][3]
        Pr = Fr(1)
        for k in range(ka, ch[L_][3]):
            u, v, w = g.m[2][raw[k] % g.m[1]]
            Pr *= Fr(u, w)
            oka &= Pr >= 1
            if Pmode:
                oka &= raw[k + 1] > Y[a]
        if a + depth <= L_ and D:
            nf += 1
            okd &= Y[a] % g.p ** D == residue
    return dict(links=len(links), forced_tested=nf, Z=ok["Z"], a=oka, b=okb, c=okc, d=okd)


starts = {}
for id, g in GRAPHS.items():
    D, res = README_CLAIMS[id][4], README_CLAIMS[id][5]
    depth = 14 if g.p == 2 else 9
    tot = dict(links=0, forced_tested=0)
    allok = True
    for trial in range(3 if QUICK else 6):
        x0 = beam_start(g, 120 if g.p == 2 else 80)
        if x0 is None:
            check("[G] %s: beam search found a 120/80-update survivor path" % id, False)
            break
        r = chain_tests(id, g, x0, 120 if g.p == 2 else 80, res, D, depth, Pmode=not graph_facts(g)["signed"])
        tot["links"] += r["links"]
        tot["forced_tested"] += r["forced_tested"]
        allok &= r["Z"] and r["a"] and r["b"] and r["c"] and r["d"]
    check("[G] %s: Thm 4 (a),(b),(c),(d) and Z monotone on %d links / %d forced-class tests of selected starts "
          "(beam-constructed long survivor orbits)" % (id, tot["links"], tot["forced_tested"]), allok)

for id, m in EXPANDING.items():
    g = graph(m)
    x0 = {"par_5_1": 7, "par_7_1": 3, "sf3_137": 15}[id]
    r = chain_tests(id, g, x0, 1500, None, 0)
    Rok = graph_facts(g)["Rok"]
    check("[G] expanding %s x0=%d: (b),(c), Z monotone on %d links of the finite-segment selection"
          % (id, x0, r["links"]), r["Z"] and r["b"] and r["c"])
    # README lists core W under Prop. 7, which assumes (R); (a) is the raw-time conclusion
    check("[G] expanding %s: hypothesis (R) of Prop. 7 holds (README applies Prop. 7 to it)" % id, Rok)
    check("[G] expanding %s: raw-time survival (a) on the segment (expected to hold iff (R))" % id,
          r["a"] or not Rok, "" if r["a"] else "raw survival fails, e.g. core W x0=15: selected 263 -> ... -> 223")

# 3x+d forced class for N^mult (raw definition), all d: n in N^mult up to 12 raw steps => class mod 4
for d in (1, -1, 3, 5, 7, 9, 13, 17):
    st = step_of(m_par(3, d))
    want = 3 if d % 4 == 1 else 1
    ok = True
    hits = 0
    for _ in range(20000):
        n = random.getrandbits(80) | 1
        x, P, sv = n, Fr(1), True
        for k in range(12):
            P *= Fr(1, 2) if x % 2 == 0 else Fr(3)
            x = st(x)
            if P < 1:
                sv = False
                break
        if sv:
            hits += 1
            ok &= n % 4 == want
    check("[G] 3x%+d: raw-multiplier survivors of 12 raw steps (%d) are all %d mod 4" % (d, hits, want), ok and hits > 0)

# ------------------------------------------------------------- I. families spot check ---
FJ = json.load(open(os.path.join(HERE, "data", "families.json")))
fam_maps = {"S3": {str(S): m_sf(S, 8) for S in [tuple(r for i, r in enumerate((1, 3, 5, 7)) if mk >> i & 1) for mk in range(16)]},
            "S4": {str(S): m_sf(S, 16) for S in [tuple(r for i, r in enumerate(range(1, 16, 2)) if mk >> i & 1) for mk in range(256)]},
            "split": {str((a, d)): m_split(a, d) for a in (3, 5, 7, 9) for d in (1, 3, 5, 7, 9, 11, 13, 15)},
            "m3": {str((a, c1, c2)): (3, 3, {0: (1, 0, 3), 1: (a, c1, 1), 2: (a, c2, 1)})
                   for a in (2, 4, 5, 7, 8) for c1 in range(9) for c2 in range(9)}}
for f, rows in FJ.items():
    check("[I] %s: json rows = family size %d" % (f, len(fam_maps[f])), len(rows) == len(fam_maps[f]))
cert_rows = [(f, r) for f, rows in FJ.items() for r in rows if r.get("contracting")]
check("[I] 240 certified members, 31 S4 members fail (R)",
      len(cert_rows) == 240 and sum(1 for f, r in cert_rows if f == "S4" and not r["raw_prefix_ok"]) == 31)
sample = random.sample(cert_rows, 8 if QUICK else 30)
okI = True
bad = []
for f, r in sample:
    m = fam_maps[f][r["key"]]
    g = graph(m)
    fa = graph_facts(g)
    ok = (fa["nstates"] == r["states"] and str(fa["rho"]) == r["rho"] and fa["Rok"] == r["raw_prefix_ok"]
          and A_of(fa["rho"], 1) == r["A1"] and A_of(fa["rho"], 10) == r["A10"] and fa["signed"] == r["signed"])
    D, res, ncl, mass = survivors(g, r["forced"]["depth"] if not QUICK else 8)
    if not QUICK:
        ok &= D == r["forced"]["D"] and res == r["forced"]["residue"] and str(mass) == r["forced"]["mass"]
    if not ok:
        bad.append((f, r["key"]))
    okI &= ok
check("[I] random sample of %d certified family members: states, rho, A(1), A(10), (R), sign, forced class recomputed"
      % len(sample), okI, "mismatch: %s" % bad if bad else "")

# certified exponent for the sample, exact
okc = True
for f, r in sample[:10]:
    m = fam_maps[f][r["key"]]
    g = graph(m)
    # rebuild the prover's TableMap to get w
    T = TableMap("x", m[1], [m[2][i] for i in range(m[1])])
    g2 = L.D.build_graph(T)
    C = L.certificate(g2)
    wmap = {g2.states[k]: Fr(C.w[k]) for k in range(len(g2.states))}
    okc &= str(1 - C.gamma) == r["theta"] and verify_cert(g, C.s, C.gamma, wmap)
check("[I] exact certificate re-check (referee powers) for 10 sampled family members", okc)

# the coverage statement: non-certified = positive drift or graph error?
neg = [(f, r) for f, rows in FJ.items() for r in rows
       if not r.get("contracting") and r.get("drift") is not None and r["drift"] < 0]
okn = True
for f, r in neg[:12]:
    m = fam_maps[f][r["key"]]
    T = TableMap("x", m[1], [m[2][i] for i in range(m[1])])
    g2 = L.D.build_graph(T)
    C = L.D.best_certificate(g2, c=Fr(1), sign=+1)
    g = graph(m)
    wmap = {g2.states[k]: Fr(C.w[k]) for k in range(len(g2.states))}
    # gamma > 1 certificate implies (N) with gamma = 1 (theta = 0): N_{s,1} <= N_{s,gamma} entrywise
    okn &= C.gamma > 1 and verify_cert(g, C.s, Fr(1), wmap)
info("%d non-certified family members have NEGATIVE drift; first 12 satisfy (N) exactly at gamma = 1 "
     "(theta = 0): %s" % (len(neg), okn))
check("[I] README: 'Non-certified means positive drift or a graph error' (true iff no negative-drift member "
      "was dropped)", len(neg) == 0, "%d negative-drift members were dropped by the assertion gamma <= 1" % len(neg))

print("ALL REFEREE CHECKS PASSED" if not FAILS else "REFEREE CHECK FAILURES (%d): %s" % (len(FAILS), FAILS))
sys.exit(1 if FAILS else 0)
