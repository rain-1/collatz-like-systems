#!/usr/bin/env python3
"""REFEREE 2 (round 6, lens chain_wide): independent checks, written from scratch.

Nothing here imports the prover's graph, tree or constant code for VERIFICATION.  The
prover's modules are imported only (i) to read their tables for a comparison with my own
tables written from the census rules, and (ii) to obtain candidate certificate weight
vectors w, which are then verified exactly by my own code (a certificate is a witness: how
it was found does not matter).

Checks (each can fail; exit status 1 if any FAIL):
 [A] my tables (from the rule text in census/open_collatz_systems.txt) = prover tables
 [B] my state graph G(T): states, slopes, rho, g, R, c_raw, (R), (S1), signs, units,
     A(1), A(10), k*, compared with data/named.json
 [C] exact certificate check (my own rational power bounds) of the prover's w at the
     claimed (s, gamma); theta and W compared with named.json
 [D] E* recomputed (rigorous upper bound, my own code, 60-bit rounding) from the verified
     certificate; named.json value must be >= mine; split5_3 at 2^48 < 5.4e-5;
     3x+1 e^{E*} < 31.7 (2^68) and < 1.7e5 (2^32)
 [E] survivor classes in the sigma-trees (my own tree), depth 14 / 9: D, residue, number,
     mass vs named.json
 [F] brute force: every n < 2^BITS reaches a value < n or returns to n (my own C program);
     the cycle minima found = named.json "cycles"; leftovers finished in Python
 [G] Theorem 4 / Lemma 1 on integer orbit segments built in deep multiplier-survivor
     classes: restart lemma, (a) raw multiplier >= 1 and raw values > x_i (when (R), (P)),
     (b) link ratio and last-edge sign and two-slope count, (c) strip, (d) forced class;
     negative control: core W must exhibit a raw drop
 [H] families: (R)-failures, no-expanding-edge members, graph errors, counts; random sample
     of certified members: my graph vs families.json and an exact certificate check
 [I] the 63 no-expanding-edge members: brute force of all n <= 20000 (all eventually
     periodic) -- the README calls them trivially GLOBAL
"""
import json
import math
import os
import random
import subprocess
import sys
import tempfile
from decimal import Decimal, getcontext
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
BITS = int(os.environ.get("R2_BITS", "26"))
FAILS = []
NPASS = [0]
random.seed(424242)
getcontext().prec = 80


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" | " + str(detail)) if detail else ""), flush=True)
    if ok:
        NPASS[0] += 1
    else:
        FAILS.append(name)


# ------------------------------------------------------------------ [A] tables
def t_par(a, d):
    return 2, 2, [(1, 0, 2), (a, d, 1)]


def t_sf(m, S):
    Q = 2 ** m
    return 2, Q, [(1, 0, 2) if r % 2 == 0 else ((3, 1, 1) if r in S else (1, 1, 1)) for r in range(Q)]


def t_split(a, d):
    return 2, 4, [(1, 0, 2), (a, d, 1), (1, 0, 2), (1, d, 1)]


def t_m3(r1, r2):
    return 3, 3, [(1, 0, 3), r1, r2]


MINE = {}
for d in (1, -1, 3, 5, 7, 9, 13, 17):
    MINE["par_3_%s%d" % ("m" if d < 0 else "", abs(d))] = t_par(3, d)
for S, nm in [((7,), "sf3_7"), ((1, 7), "sf3_17"), ((5, 7), "sf3_57"), ((1, 5, 7), "sf3_157"),
              ((3, 5, 7), "sf3_357"), ((1, 3), "sf3_13"), ((1, 3, 5), "sf3_135"),
              ((1, 3, 7), "sf3_137")]:
    MINE[nm] = t_sf(3, S)
MINE["split5_1"] = t_split(5, 1)
MINE["split5_3"] = t_split(5, 3)
MINE["desc_split7_1"] = t_split(7, 1)
MINE["m3_b"] = t_m3((4, -1, 3), (4, 1, 3))      # (4n-1)/3, (4n+1)/3
MINE["m3_d"] = t_m3((4, 2, 1), (4, 1, 1))
MINE["m3_g"] = t_m3((5, 1, 1), (5, 2, 1))
MINE["desc_m3_4n5"] = t_m3((4, 5, 1), (2, 2, 1))
MINE["desc_s32_plus9"] = t_sf(5, tuple(r for r in range(1, 32, 2) if r not in (19, 27, 31)))
MINE["par_5_1"] = t_par(5, 1)
MINE["par_7_1"] = t_par(7, 1)

sys.path.insert(0, HERE)
import chain_systems as PS  # noqa: E402  (tables and families only)
import chainlib as PL  # noqa: E402  (only to obtain candidate w vectors)

for nm, (p, Q, tab) in MINE.items():
    T = PS.BY_ID[nm]["T"]
    check("[A] %s: my table = prover table" % nm, T.Q == Q and list(T.table) == tab)


def step_of(Q, tab):
    def f(n):
        u, v, w = tab[n % Q]
        y = u * n + v
        assert y % w == 0 and y > 0
        return y // w
    return f


# ------------------------------------------------------------------ my graph
class LoopError(Exception):
    pass


def vp(x, p):
    k = 0
    while x % p == 0:
        x //= p
        k += 1
    return k


def decide(Q, tab, K, beta):
    g = math.gcd(K, Q)
    rows = set(tab[r] for r in range(beta % g, Q, g))
    if len(rows) != 1:
        return None
    u, v, w = next(iter(rows))
    if K % w or (u * beta + v) % w:
        return None
    return u, v, w


def run(p, Q, tab, K, beta):
    """apply all decided steps to the class beta mod K (K a power of p)"""
    F, G, trace, nv, seen = Fr(1), Fr(0), [], 0, set()
    while True:
        row = decide(Q, tab, K, beta)
        if row is None:
            return K, beta, F, G, trace, nv
        if (K, beta) in seen:
            raise LoopError((K, beta))
        seen.add((K, beta))
        u, v, w = row
        assert u % p != 0
        K2 = K // w
        beta = ((u * beta + v) // w) % K2
        K = K2
        F *= Fr(u, w)
        G = G * Fr(u, w) + Fr(v, w)
        trace.append((F, v))
        nv += (v != 0)


class Graph:
    pass


def graph(p, Q, tab):
    K0, b0, F0, G0, tr0, _ = run(p, Q, tab, 1, 0)
    assert not tr0
    states = [(K0, b0)]
    idx = {(K0, b0): 0}
    edges = []
    i = 0
    while i < len(states):
        K, beta = states[i]
        for d in range(p):
            K1, b1, F, G, tr, nv = run(p, Q, tab, K * p, beta + K * d)
            if (K1, b1) not in idx:
                idx[(K1, b1)] = len(states)
                states.append((K1, b1))
                if len(states) > 3000:
                    raise ValueError("too many states")
            edges.append(dict(src=i, dst=idx[(K1, b1)], d=d, F=F, G=G, steps=len(tr),
                              trace=[f for f, _ in tr], nv=nv))
        i += 1
    g = Graph()
    g.p, g.Q, g.tab, g.states, g.idx, g.edges = p, Q, tab, states, idx, edges
    return g


def A_of(F, B):
    """largest k >= 0 with F^k < 2^B (None if F <= 1)"""
    if F <= 1:
        return None
    k = 0
    while F ** (k + 1) < 2 ** B:
        k += 1
    return k


def kstar(g):
    rho = max(e["F"] for e in g.edges)
    co = [e["F"] for e in g.edges if e["F"] < 1]
    if rho <= 1 or not co:
        return None
    km = max(co)
    k = 0
    while rho ** k * km <= 1:
        k += 1
    return k


def props(g):
    rho = max(e["F"] for e in g.edges)
    gerr = max((abs(e["G"]) / e["F"] for e in g.edges if e["G"] != 0), default=Fr(0))
    R = max(e["steps"] for e in g.edges)
    craw = Fr(1)
    Rok = True
    for e in g.edges:
        for x in e["trace"][:-1]:
            craw = min(craw, x)
        lo = min(Fr(1), e["F"])
        if any(x < lo for x in e["trace"]):
            Rok = False
    s1 = max(e["nv"] for e in g.edges)
    return dict(rho=rho, gerr=gerr, R=R, c_raw=craw, Rok=Rok, S1=s1,
                signed=any(v < 0 for (_, v, _) in g.tab), units=all(u % g.p for (u, _, _) in g.tab),
                slopes=sorted(set(e["F"] for e in g.edges)), A1=A_of(rho, 1), A10=A_of(rho, 10),
                kstar=kstar(g))


# ------------------------------------------------------- rigorous powers (mine)
def _dec(fr):
    return Decimal(fr.numerator) / Decimal(fr.denominator)


def pow_bound(x, r, upper=True, bits=60):
    """rational U >= x^r (upper) or L <= x^r, verified with exact integers"""
    x, r = Fr(x), Fr(r)
    if r < 0:
        x, r = 1 / x, -r
    if r == 0 or x == 1:
        return Fr(1)
    a, b = r.numerator, r.denominator
    f = (_dec(x).ln() * _dec(r)).exp()
    y = Fr(f) * (1 + Fr(1, 1 << bits)) if upper else Fr(f) * (1 - Fr(1, 1 << bits))
    lhs = lambda y: y.numerator ** b * x.denominator ** a  # noqa: E731
    rhs = lambda y: x.numerator ** a * y.denominator ** b  # noqa: E731
    while (lhs(y) < rhs(y)) if upper else (lhs(y) > rhs(y)):
        y = y * (1 + Fr(1, 1 << (bits // 2))) if upper else y * (1 - Fr(1, 1 << (bits // 2)))
    return y


def cert_ok(g, s, gamma, wmap):
    """exact: sum_e p^(gamma-1) F_e^s w(dst) <= w(src) for every state (upper bounds)"""
    qg = pow_bound(g.p, gamma - 1)
    cache = {}
    for i, st in enumerate(g.states):
        tot = Fr(0)
        for e in g.edges[i * g.p:(i + 1) * g.p]:
            assert e["src"] == i
            F = e["F"]
            if F not in cache:
                cache[F] = pow_bound(F, s)
            tot += qg * cache[F] * wmap[g.states[e["dst"]]]
        if tot > wmap[st]:
            return False
    return True


def Estar(p, theta, s, W, gp, k0):
    """rigorous upper bound of g' W p^th S1 / (1 - g' s S2) (THEORY Thm 3)"""
    a = pow_bound(p, theta)
    b = pow_bound(p, -k0 * (1 - theta))
    c = pow_bound(p, -(1 - theta))
    S1 = a * b / (1 - c)
    q = Fr(1, p)
    S2 = q ** k0 * (Fr(k0 + 1) / (1 - q) + q / (1 - q) ** 2)
    lam = gp * s * S2
    if lam >= 1:
        return None, lam
    return gp * W * a * S1 / (1 - lam), lam


# ---------------------------------------------------------- sigma-tree (mine)
def apply_decided(g, a, b):
    F = Fr(1)
    G = Fr(0)
    while True:
        K = g.p ** vp(a, g.p)
        row = decide(g.Q, g.tab, K, b % K)
        if row is None:
            return a, b, F, G
        u, v, w = row
        assert (u * a) % w == 0 and (u * b + v) % w == 0
        a, b = u * a // w, (u * b + v) // w
        F *= Fr(u, w)
        G = G * Fr(u, w) + Fr(v, w)


def tree_child(g, node, d):
    M, r, a, b, A = node
    M2, r2, a2, b2 = M * g.p, r + M * d, a * g.p, b + a * d
    a2, b2, F, G = apply_decided(g, a2, b2)
    return (M2, r2, a2, b2, A * F), F, G


def state_of(g, node):
    a, b = node[2], node[3]
    K = g.p ** vp(a, g.p)
    return g.idx[(K, b % K)]


def survivors(g, depth):
    allc = []
    for (K, beta) in g.states:
        level = [(K, beta, K, beta, Fr(1))]
        for _ in range(depth):
            nxt = []
            for nd in level:
                for d in range(g.p):
                    c, _, _ = tree_child(g, nd, d)
                    if c[4] > 1:
                        nxt.append(c)
            level = nxt
        allc += [(nd[0], nd[1]) for nd in level]
    if not allc:
        return None
    D, res = 0, 0
    for Dd in range(1, depth + 1):
        s = set(r % g.p ** Dd for (_, r) in allc)
        if len(s) == 1:
            D, res = Dd, s.pop()
        else:
            break
    return dict(D=D, residue=res, classes=len(allc), mass=sum(Fr(1, M) for (M, _) in allc))


# ======================================================================== run
NJ = json.load(open(os.path.join(HERE, "data", "named.json")))
GR = {}
for nm, (p, Q, tab) in MINE.items():
    GR[nm] = graph(p, Q, tab)

print("---- [B] state graphs")
for nm, row in NJ.items():
    g = GR[nm]
    pr = props(g)
    ok = (len(g.states) == row["states"] and pr["rho"] == Fr(row["rho"]) and pr["gerr"] == Fr(row["gerr"])
          and pr["R"] == row["R"] and pr["c_raw"] == Fr(row["c_raw"]) and pr["Rok"] == row["raw_prefix_ok"]
          and pr["signed"] == row["signed"] and pr["A1"] == row["A1"] and pr["A10"] == row["A10"]
          and pr["kstar"] == row["kstar"] and [str(x) for x in pr["slopes"]] == row["slopes"])
    check("[B] %s: states %d rho %s g %s R %d c_raw %s (R) %s A1 %s A10 %s k* %s" % (
        nm, len(g.states), pr["rho"], pr["gerr"], pr["R"], pr["c_raw"], pr["Rok"], pr["A1"], pr["A10"],
        pr["kstar"]), ok)
    check("[B] %s: unit multipliers" % nm, pr["units"])
    if pr["signed"]:
        check("[B] %s (signed): (S1) at most one v != 0 raw step per edge (max %d)" % (nm, pr["S1"]), pr["S1"] <= 1)
    else:
        check("[B] %s: (P) every v_r >= 0" % nm, all(v >= 0 for (_, v, _) in g.tab))
for nm, want in (("par_5_1", True), ("par_7_1", True), ("sf3_137", False)):
    check("[B] expanding %s: (R) = %s" % (nm, want), props(GR[nm])["Rok"] == want)
# negative control for my (S1) counter
gneg = graph(2, 4, [(1, 0, 2), (1, 2, 1), (1, 0, 2), (3, 1, 1)])
check("[B] negative control: n+2 then 3n+1 in one edge is detected by my (S1) counter",
      props(gneg)["S1"] >= 2)

print("---- [C] certificates, [D] multiplier constants")


def their_w(nm, s=None):
    T = PS.BY_ID[nm]["T"]
    pg = PL.D.build_graph(T)
    C = PL.certificate(pg) if s is None else PL.certificate_at(pg, Fr(s))
    return {pg.states[i]: C.w[i] for i in range(len(pg.states))}, C


for nm, row in NJ.items():
    g = GR[nm]
    wm, C = their_w(nm)
    ok = set(wm) == set(g.states) and cert_ok(g, C.s, C.gamma, wm)
    W = sum(wm.values()) / min(wm.values())
    check("[C] %s: N_{s,gamma} w <= w exactly at s=%s, theta=%s; W=%.4g matches" % (nm, C.s, 1 - C.gamma, float(W)),
          ok and 1 - C.gamma == Fr(row["theta"]) and C.s == Fr(row["s"]) and W == Fr(row["W"]))
    pr = props(g)
    for key, e in row["E"].items():
        wm2, C2 = their_w(nm, e["s"])
        ok2 = cert_ok(g, C2.s, C2.gamma, wm2) and C2.gamma == Fr(e["gamma"])
        W2 = sum(wm2.values()) / min(wm2.values())
        gp = pr["gerr"] * (2 if pr["signed"] else 1)
        k0 = e["k0p"]
        bound_bits = int(key)
        ok3 = g.p ** k0 <= 2 ** bound_bits and (not pr["signed"] or pr["gerr"] <= Fr(g.p ** k0, 2))
        Em, lam = Estar(g.p, 1 - C2.gamma, C2.s, W2, gp, k0)
        okE = Em is not None and Fr(e["E"]) >= Em
        check("[D] %s range 2^%s (k0=%d): cert ok, json E*=%.10g >= mine %.10g (g'=%s), lam=%.2e" % (
            nm, key, k0, float(Fr(e["E"])), float(Em) if Em else -1, gp, float(lam)), ok2 and ok3 and okE)
        if nm == "split5_3":
            E48, _ = Estar(2, 1 - C2.gamma, C2.s, W2, gp, 48)
            check("[D] split5_3 at 2^48: E* = %.4g < 5.4e-5 < log 1.000073" % float(E48),
                  E48 < Fr(54, 10 ** 6) and Decimal(float(E48)) < Decimal("1.000073").ln())
        if nm == "par_3_1":
            lim = {"68": Decimal("31.7"), "32": Decimal("1.7e5")}[key]
            check("[D] 3x+1 at 2^%s: e^{E*} = %.6g < %s" % (key, math.exp(float(Em)), lim),
                  _dec(Em).exp() < lim)
# README 3x+1 row: theta = 1082/1139, W = 1 and E* bounds 3.46 / 12.04
r31 = NJ["par_3_1"]
check("[D] 3x+1 row numbers: E(2^68)=%.4f <= 3.46, E(2^32)=%.4f <= 12.04" % (
    r31["E"]["68"]["E_f"], r31["E"]["32"]["E_f"]),
    Fr(r31["E"]["68"]["E"]) <= Fr(346, 100) and Fr(r31["E"]["32"]["E"]) <= Fr(1204, 100))
# signed values from the README revision table
check("[D] signed values: 3x-1 E* = %.10f, m3_b E* = %.10f" % (
    NJ["par_3_m1"]["E"]["32"]["E_f"], NJ["m3_b"]["E"]["32"]["E_f"]),
    abs(NJ["par_3_m1"]["E"]["32"]["E_f"] - 24.0788944447) < 1e-9 and
    abs(NJ["m3_b"]["E"]["32"]["E_f"] - 50.7372625433) < 1e-9)

print("---- [E] survivor classes")
for nm, row in NJ.items():
    g = GR[nm]
    depth = row["forced"]["depth"]
    sv = survivors(g, depth)
    f = row["forced"]
    check("[E] %s depth %d: D=%d residue %d classes %d mass %s" % (nm, depth, sv["D"], sv["residue"],
                                                                 sv["classes"], sv["mass"]),
          sv["D"] == f["D"] and sv["residue"] == f["residue"] and sv["classes"] == f["classes"]
          and sv["mass"] == Fr(f["mass"]))

print("---- [F] brute force, all n < 2^%d" % BITS)
CSRC = r"""
#include <stdio.h>
#include <stdlib.h>
typedef __int128 i128;
int main(int argc, char **argv){
  int bits = atoi(argv[1]); long Q = atol(argv[2]); long U[64],V[64],W[64]; int k=3;
  for (long r=0;r<Q;r++){U[r]=atol(argv[k++]);V[r]=atol(argv[k++]);W[r]=atol(argv[k++]);}
  unsigned long long N = 1ULL<<bits; i128 LIM = ((i128)1)<<110;
  for (unsigned long long n=1;n<N;n++){
    i128 x=n; long s=0;
    for(;;){ long r=(long)(x%Q); i128 y=(i128)U[r]*x+V[r];
      if (y<=0 || y%W[r]) {printf("BAD %llu\n",n); return 1;}
      x=y/W[r]; s++;
      if (x<(i128)n) break;
      if (x==(i128)n){printf("CYC %llu\n",n); break;}
      if (x>LIM || s>2000000){printf("LEFT %llu\n",n); break;}
    }
  }
  printf("DONE\n"); return 0;
}
"""
tmpd = tempfile.mkdtemp(prefix="r2chk_")
csrc = os.path.join(tmpd, "bf.c")
open(csrc, "w").write(CSRC)
exe = os.path.join(tmpd, "bf")
subprocess.run(["gcc", "-O2", "-o", exe, csrc], check=True)


def brute(nm, bits):
    p, Q, tab = MINE[nm]
    args = [exe, str(bits), str(Q)] + [str(x) for row in tab for x in row]
    out = subprocess.run(args, capture_output=True, text=True).stdout.split("\n")
    cyc, left, bad = [], [], []
    for ln in out:
        if ln.startswith("CYC"):
            cyc.append(int(ln.split()[1]))
        elif ln.startswith("LEFT"):
            left.append(int(ln.split()[1]))
        elif ln.startswith("BAD"):
            bad.append(ln)
    return cyc, left, bad, out


procs = {}
for nm, row in NJ.items():
    bits = BITS - 4 if nm == "m3_g" else BITS
    procs[nm] = bits
from concurrent.futures import ThreadPoolExecutor  # noqa: E402
with ThreadPoolExecutor(10) as ex:
    res = dict(zip(procs, ex.map(lambda kv: brute(*kv), procs.items())))
for nm, row in NJ.items():
    cyc, left, bad, out = res[nm]
    f = step_of(MINE[nm][1], MINE[nm][2])
    extra = set()
    for n in left:   # finish exactly with cycle detection
        x, seen = n, set()
        while x >= n and x not in seen:
            seen.add(x)
            x = f(x)
            if x.bit_length() > 4000:
                raise RuntimeError("orbit too large")
        if x >= n:    # entered a cycle that never goes below n
            c, y = [x], f(x)
            while y != x:
                c.append(y)
                y = f(y)
            extra.add(min(c))
    mins = sorted(set(cyc) | extra)
    check("[F] %s: all n < 2^%d settle; cycle minima %s = listed %s (%d leftovers finished exactly)" % (
        nm, procs[nm], mins, row["cycles"], len(left)),
        not bad and "DONE" in out and mins == sorted(row["cycles"]))
# negative control: drop the cycle at 61 for split5_3 -> must be found as an unlisted cycle
check("[F] negative control: brute force finds the split5_3 cycle 61 (so a missing cycle would fail)",
      61 in res["split5_3"][0])

print("---- [G] Theorem 4 / Lemma 1 on orbit segments")


def root_path_start(g, L, rng):
    """random start whose first L root-tree updates keep P >= 1 (as far as possible)"""
    # beam search in the root tree: keep classes whose P stays above a slowly growing
    # floor, so that the selected minima are spread over the segment
    level = [(1, 0, 1, 0, Fr(1))]
    for j in range(L):
        ch = [tree_child(g, nd, d)[0] for nd in level for d in range(g.p)]
        floor = Fr(51, 50) ** max(0, j - 12)
        good = [c for c in ch if c[4] >= floor]
        if not good:
            good = sorted(ch, key=lambda c: c[4])[-16:]
        level = rng.sample(good, min(24, len(good)))
    nd = rng.choice(level)
    return nd[1] + nd[0] * rng.getrandbits(30)


def update_chain(g, x0, L):
    nd = (1, 0, 1, 0, Fr(1))
    out = [dict(y=x0, P=Fr(1), st=state_of(g, nd), F=None, G=None, steps=0)]
    for _ in range(L):
        t = (x0 - nd[1]) // nd[0]
        d = t % g.p
        c, F, G = tree_child(g, nd, d)
        nd = c
        tt = (x0 - nd[1]) // nd[0]
        out[-1]["F"], out[-1]["G"] = F, G
        out.append(dict(y=nd[2] * tt + nd[3], P=nd[4], st=state_of(g, nd), F=None, G=None))
    return out


for nm in list(NJ) + ["par_5_1", "par_7_1", "sf3_137"]:
    g = GR[nm]
    pr = props(g)
    f = step_of(g.Q, g.tab)
    forced = NJ[nm]["forced"] if nm in NJ else None
    rng = random.Random(hash(nm) & 0xffff)
    L = 160 if g.p == 2 else 110
    nlinks = viol = 0
    lemma1 = True
    rawdrop = False
    for trial in range(5):
        x0 = root_path_start(g, L, rng)
        ch = update_chain(g, x0, L)
        # the y_l are orbit values in order
        x, ys = x0, set()
        for _ in range(6 * L):
            ys.add(x)
            x = f(x)
        if not all(c["y"] in ys for c in ch):
            lemma1 = False
        # Lemma 1 at random l: sigma_l-tree path of y_l
        for _ in range(3):
            l = rng.randrange(0, L - 20)
            K, beta = g.states[ch[l]["st"]]
            y = ch[l]["y"]
            nd = (K, beta, K, beta, Fr(1))
            for j in range(1, 20):
                d = ((y - nd[1]) // nd[0]) % g.p
                nd, _, _ = tree_child(g, nd, d)
                tt = (y - nd[1]) // nd[0]
                if not (state_of(g, nd) == ch[l + j]["st"] and nd[4] == ch[l + j]["P"] / ch[l]["P"]
                        and nd[2] * tt + nd[3] == ch[l + j]["y"]):
                    lemma1 = False
        # selection on the segment
        P = [c["P"] for c in ch]
        sel, t = [], -1
        while t + 1 < len(P) - 1:
            m = min(P[t + 1:])
            t = max(i for i in range(t + 1, len(P)) if P[i] == m)
            sel.append(t)
        for i in range(len(sel) - 1):
            ti, tj = sel[i], sel[i + 1]
            if tj >= L:
                break
            nlinks += 1
            xi, xj = ch[ti]["y"], ch[tj]["y"]
            Fs = [ch[l]["F"] for l in range(ti, tj)]
            Gs = [ch[l]["G"] for l in range(ti, tj)]
            r = P[tj] / P[ti]
            ok = 1 < r <= Fs[0] <= pr["rho"] and Fs[0] > 1
            nonunit = [F for F in Fs if F != 1]
            if len(nonunit) > 1:
                ok &= nonunit[-1] < 1
            # two-slope count
            if len(set(nonunit)) <= 2 and len([v for v in set(e["F"] for e in g.edges) if v != 1]) == 2:
                rho_, kap = pr["rho"], min(e["F"] for e in g.edges)
                a = sum(1 for F in nonunit if F > 1)
                ee = sum(1 for F in nonunit if F < 1)
                ok &= 1 < rho_ ** a * kap ** ee <= rho_
                ok &= a == math.floor(ee * math.log(1 / kap) / math.log(rho_)) + 1
            # strip (c), exact
            C = xj - r * xi
            Ck, prod = Fr(0), Fr(1)
            for k in range(len(Fs) - 1, -1, -1):
                Ck += Gs[k] * prod
                prod *= Fs[k]
            ok &= C == Ck
            if not pr["signed"]:
                lo = Gs[0] * r / Fs[0] + (Gs[-1] if len(Fs) > 1 else 0)
                ok &= lo <= C <= sum(Gs)
            else:
                ok &= abs(C) <= sum(abs(G) for G in Gs)
            # (d) forced class: needs the next `depth` updates inside the segment
            if forced and forced["D"] > 0 and ti + forced["depth"] <= L:
                ok &= xi % g.p ** forced["D"] == forced["residue"]
            # (a) raw: from x_i up to the raw time of update L
            if pr["Rok"]:
                xr, Pr_, okr = xi, Fr(1), True
                target = ch[-1]["y"]
                cnt = 0
                while xr != target and cnt < 20000:
                    u, v, w = g.tab[xr % g.Q]
                    xr = (u * xr + v) // w
                    Pr_ *= Fr(u, w)
                    cnt += 1
                    okr &= Pr_ >= 1 and (pr["signed"] or xr > xi)
                ok &= okr and xr == target
            else:
                xr, Pr_ = xi, Fr(1)
                target = ch[-1]["y"]
                cnt = 0
                while xr != target and cnt < 20000:
                    u, v, w = g.tab[xr % g.Q]
                    xr = (u * xr + v) // w
                    Pr_ *= Fr(u, w)
                    cnt += 1
                    if Pr_ < 1 or xr < xi:
                        rawdrop = True
            viol += not ok
    check("[G] %s: Lemma 1 restart + orbit values on 5 segments; Thm 4 (a)(b)(c)(d) on %d links, %d violations"
          % (nm, nlinks, viol), lemma1 and viol == 0 and nlinks >= 20)
    if not pr["Rok"]:
        check("[G] %s fails (R): a raw drop below a selected start was found on the segments" % nm, rawdrop)

print("---- [H] families")
FJ = json.load(open(os.path.join(HERE, "data", "families.json")))
fams = dict(S3=PS.family_S(3), S4=PS.family_S(4), split=PS.family_split(), m3=PS.family_m3())
tot_cert = tot_noexp = 0
failR = {}
graph_err = {}
sample = []
NOEXP = []
for fname, rows in FJ.items():
    members = dict((str(k), T) for k, T in fams[fname])
    check("[H] %s: %d rows = %d members" % (fname, len(rows), len(members)), len(rows) == len(members))
    failR[fname] = 0
    graph_err[fname] = 0
    for r in rows:
        T = members[r["key"]]
        p = T.primes[0]
        try:
            g = graph(p, T.Q, list(T.table))
        except LoopError:
            graph_err[fname] += 1
            if "graph" not in (r.get("error") or ""):
                check("[H] %s %s: my graph has a loop but json has no graph error" % (fname, r["key"]), False)
            continue
        if not r.get("contracting"):
            continue
        tot_cert += 1
        pr = props(g)
        if not pr["Rok"]:
            failR[fname] += 1
        same = (len(g.states) == r["states"] and str(pr["rho"]) == r["rho"] and pr["Rok"] == r["raw_prefix_ok"]
                and pr["A10"] == r["A10"] and (pr["rho"] <= 1) == bool(r.get("no_expanding_edge"))
                and all(v >= 0 for (_, v, _) in g.tab) and pr["units"])
        if not same:
            check("[H] %s %s: my graph properties differ from families.json" % (fname, r["key"]), False)
        if pr["rho"] <= 1:
            tot_noexp += 1
            NOEXP.append((fname, r["key"], T))
        sample.append((fname, r, T, g))
check("[H] certified members %d = 343; no expanding edge %d = 63" % (tot_cert, tot_noexp),
      tot_cert == 343 and tot_noexp == 63)
check("[H] (R) failures among certified: %s (README: 35 in S4, 0 elsewhere)" % failR,
      failR == dict(S3=0, S4=35, split=0, m3=0))
check("[H] graph errors (division-free branch loops) by my builder: %s (README: 270 in m3)" % graph_err,
      graph_err == dict(S3=0, S4=0, split=0, m3=270))
npos = sum(1 for rows in FJ.values() for r in rows if not r.get("contracting")
           and "graph" not in (r.get("error") or "") and r.get("drift") is not None and r["drift"] > 0)
print("INFO non-certified members with positive drift: %d (README line 'positive drift (97)')" % npos)
rng = random.Random(77)
sub = rng.sample(sample, 30)
okc = True
okf = True
for fname, r, T, g in sub:
    pg = PL.D.build_graph(T)
    C = PL.certificate(pg)
    wm = {pg.states[i]: C.w[i] for i in range(len(pg.states))}
    okc &= set(wm) == set(g.states) and cert_ok(g, C.s, C.gamma, wm) and str(1 - C.gamma) == r["theta"]
    if r["forced"] is not None:
        sv = survivors(g, r["forced"]["depth"])
        okf &= sv is not None and sv["D"] == r["forced"]["D"] and sv["residue"] == r["forced"]["residue"] \
            and sv["mass"] == Fr(r["forced"]["mass"])
check("[H] 30 random certified members: exact certificate check of theta (my powers)", okc)
check("[H] same 30: forced class D, residue, mass recomputed by my tree", okf)

print("---- [J] negative controls and the Cor. 5 'update multiplier > 1' clause")
# certificate checker must reject a too-large gamma with the same w
wm, C = their_w("par_3_1")
check("[J] cert checker rejects 3x+1 at gamma + 1/1000 (w fixed)",
      not cert_ok(GR["par_3_1"], C.s, C.gamma + Fr(1, 1000), wm))
wm, C = their_w("split5_3")
check("[J] cert checker rejects split5_3 at gamma + 1/1000 (w fixed)",
      not cert_ok(GR["split5_3"], C.s, C.gamma + Fr(1, 1000), wm))
# THEORY Cor. 5 says N_b may equivalently be defined by 'every update multiplier over the
# first b updates is > 1'.  Read with the root tree of n (the only tree computable from n),
# this excludes every odd n for split5_3 and the S-family: the first root edge
# (1,0) -> (2,1) is a pure split with F = 1.  Record that this happens.
for nm in ("split5_3", "sf3_7"):
    g = GR[nm]
    e = [e for e in g.edges if e["src"] == 0 and e["d"] == 1][0]
    ch = update_chain(g, 253 + 256 * 12345, 3)
    check("[J] %s: root edge (1,0)->digit 1 is a pure split (F=1, 0 raw steps), so every odd start, "
          "including every selected start, has root-tree update multiplier P_1 = 1 (not > 1)" % nm,
          e["F"] == 1 and e["steps"] == 0 and ch[1]["P"] == 1)

print("---- [I] no-expanding-edge members")
okI = True
for fname, key, T in NOEXP:
    f = T.step
    for n in range(1, 20001):
        x, seen = n, set()
        while x not in seen:
            seen.add(x)
            x = f(x)
            if len(seen) > 100000:
                okI = False
                break
check("[I] all 63 no-expanding-edge members: every n <= 20000 is eventually periodic", okI)

print("\n%d PASS, %d FAIL" % (NPASS[0], len(FAILS)))
if FAILS:
    print("FAILED:", FAILS)
sys.exit(1 if FAILS else 0)
