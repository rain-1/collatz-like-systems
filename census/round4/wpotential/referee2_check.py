"""Referee 2: independent check of round4/wpotential (written from scratch).

Imports nothing from the prover or from round 3 (reads only mi_chains.json as data).
Exact int / Fraction arithmetic throughout; the one rank computation is done
modulo the prime 998244353 (rank mod p <= rank over Q, so it is a valid lower
bound), with exact integer checks for the kernel vectors.

Sections
 [TYPE]     own cylinder graph G_K, SCC decomposition, exact type decision
            (8 cores n-form, K7 z-form, 3x+1, 5x+1 must be type (c);
             acc_h16 and a CERT control must NOT be type (c))
 [BRUTE]    every start below a bound reaches the stated cycles
 [SHADOW]   Theorem W shadowing identity at x*, exact
 [DENSE]    Corollary W1: random walks in the type-(c) SCC are followed by
            expanding rational periodic points
 [NEUTRAL]  the division-free case of W2 "only if" (multiplier can be exactly 1)
 [TYPEB]    REFEREE1's counter certificate for acc_h16, rebuilt independently
 [BIJ] [PUMP] [STEP3] [RANK] [KER]   Theorem A
 [CTRL-A]   positive control: a window potential DOES certify a CERT system with
            a x3 branch (Theorem A must not over-reach)
 [MB]       mb_s3_27 periodic orbits (own Lyndon-word enumeration), homoclinic pts
 [SRS]      rule semantics (own rule lists) and the stored z3 chains (own algebra)
Exits 0 iff all pass; several checks are negative controls that must fail-detect.
"""
import json
import os
import random
import sys
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OK = True


def claim(msg, cond):
    global OK
    print(("PASS " if cond else "FAIL ") + msg, flush=True)
    OK = OK and bool(cond)


# ------------------------------------------------------------------ systems
def s_family(S):          # n-form, m = 3
    return dict(p=2, m=3, tab=[(1, 0, 2) if r % 2 == 0 else ((3, 1, 1) if r in S else (1, 1, 1))
                               for r in range(8)])


CORES = {"sf3_7": (7,), "sf3_17": (1, 7), "sf3_57": (5, 7), "sf3_157": (1, 5, 7),
         "sf3_357": (3, 5, 7), "sf3_137": (1, 3, 7), "sf3_13": (1, 3), "sf3_135": (1, 3, 5)}
SYS = {k: s_family(S) for k, S in CORES.items()}
SYS["K7z"] = dict(p=2, m=2, tab=[(1, 0, 2), (1, -1, 4), (1, 0, 2), (3, 1, 2)])
SYS["3x+1"] = dict(p=2, m=1, tab=[(1, 0, 2), (3, 1, 2)])
SYS["5x+1"] = dict(p=2, m=1, tab=[(1, 0, 2), (5, 1, 1)])


def acc_h16_tab():
    t = []
    for r in range(16):
        if r % 2 == 0:
            t.append((1, 0, 2))
        elif r in (5, 9):
            t.append((1, 1, 1))
        elif r == 13:
            t.append((1, 5, 1))
        else:
            t.append((3, 1, 1))
    return t


SYS["acc_h16"] = dict(p=2, m=4, tab=acc_h16_tab())
# CERT control: even n/2; n=1(4): (3n+1)/4; n=3(4): (3n+3)/4.  All multipliers < 1.
SYS["cert_ctrl"] = dict(p=2, m=2, tab=[(1, 0, 2), (3, 1, 4), (1, 0, 2), (3, 3, 4)])


def T_int(sd, n):
    Q = sd["p"] ** sd["m"]
    u, v, w = sd["tab"][n % Q]
    x = u * n + v
    assert x % w == 0
    return x // w


def res(x, p, K):
    x = Fr(x)
    assert x.denominator % p
    return x.numerator * pow(x.denominator, -1, p ** K) % p ** K


def T_rat(sd, x):
    p, m = sd["p"], sd["m"]
    u, v, w = sd["tab"][res(x, p, m)]
    return (u * Fr(x) + v) / w, Fr(u, w)


def vp(n, p):
    k = 0
    while n % p == 0:
        n //= p
        k += 1
    return k


# ------------------------------------------------------------------ graph
def graph(sd, K):
    """G_K edges: node -> list of (target, multiplier, divisions)."""
    p, m, tab = sd["p"], sd["m"], sd["tab"]
    assert K >= m
    N = p ** K
    G = {}
    for r in range(N):
        u, v, w = tab[r % p ** m]
        e = vp(w, p)
        assert p ** e == w and u % p
        base = (u * r + v)
        assert base % w == 0
        base //= w
        mod = p ** (K - e)
        tg = sorted({(base % mod) + j * mod for j in range(p ** e)})
        G[r] = [(s, Fr(u, w), e) for s in tg]
    return G


def sccs(G):
    idx, low, onst, st, out, cnt = {}, {}, set(), [], [], [0]
    sys.setrecursionlimit(100000)

    def dfs(v):
        idx[v] = low[v] = cnt[0]
        cnt[0] += 1
        st.append(v)
        onst.add(v)
        for (w, _, _) in G[v]:
            if w not in idx:
                dfs(w)
                low[v] = min(low[v], low[w])
            elif w in onst:
                low[v] = min(low[v], idx[w])
        if low[v] == idx[v]:
            comp = []
            while True:
                w = st.pop()
                onst.discard(w)
                comp.append(w)
                if w == v:
                    break
            out.append(frozenset(comp))
    for v in G:
        if v not in idx:
            dfs(v)
    return out


def division_free_acyclic(G):
    H = {v: [w for (w, _, e) in G[v] if e == 0] for v in G}
    color = {}

    def has_cycle(v):
        color[v] = 1
        for w in H[v]:
            if color.get(w) == 1:
                return True
            if color.get(w) is None and has_cycle(w):
                return True
        color[v] = 2
        return False
    return not any(color.get(v) is None and has_cycle(v) for v in G)


def internal_edges(G, C):
    return [(a, b, q) for a in C for (b, q, _) in G[a] if b in C]


def contracting_potential(G, C, theta):
    """Exact c(r) > 0 on C with c(s) q <= theta c(r) on internal edges, or None."""
    E = internal_edges(G, C)
    c = {r: Fr(1) for r in C}
    for _ in range(4 * len(C) + 5):
        ch = False
        for a, b, q in E:
            need = c[b] * q / theta
            if need > c[a]:
                c[a] = need
                ch = True
        if not ch:
            break
    if all(c[b] * q <= theta * c[a] for a, b, q in E):
        return c
    return None


def orbit_walk(sd, y, K, maxlen=5000):
    x, lam, nodes = Fr(y), Fr(1), []
    for _ in range(maxlen):
        nodes.append(res(x, sd["p"], K))
        x, q = T_rat(sd, x)
        lam *= q
        if x == y:
            return nodes, lam
    raise AssertionError


def classify(sd, K, xstar=None):
    G = graph(sd, K)
    comps = sccs(G)
    info = dict(G=G, comps=comps, hyp=division_free_acyclic(G))
    types = []
    for C in comps:
        E = internal_edges(G, C)
        if not E:
            continue
        simple = len(E) == len(C)
        pot = contracting_potential(G, C, Fr(999, 1000))
        if pot is not None:
            types.append((C, "a"))
        elif simple:
            # multiplier of the cycle
            lam, a = Fr(1), min(C)
            v = a
            for _ in range(len(C)):
                (b, q) = [(b, q) for (b, q, _) in G[v] if b in C][0]
                lam *= q
                v = b
            types.append((C, "b" if lam > 1 else "a?"))
        else:
            types.append((C, "c?"))   # non-simple, no contracting potential found
    info["types"] = types
    if xstar is not None:
        nodes, lam = orbit_walk(sd, xstar, K)
        Cx = [C for C in comps if nodes[0] in C][0]
        info["xstar_lam"] = lam
        info["xstar_type_c"] = (lam > 1 and all(n in Cx for n in nodes)
                                and len(internal_edges(G, Cx)) > len(Cx))
        info["xstar_comp"] = Cx
    return info


XS = {"sf3_7": -1, "sf3_17": -1, "sf3_57": -1, "sf3_157": -1, "sf3_357": -1, "sf3_137": -1,
      "sf3_13": -5, "sf3_135": -5, "K7z": -1, "3x+1": -1, "5x+1": Fr(-1, 3)}

for name, x in XS.items():
    sd = SYS[name]
    good = True
    for K in (sd["m"], sd["m"] + 2):
        inf = classify(sd, K, Fr(x))
        good = good and inf["hyp"] and inf["xstar_type_c"]
    claim(f"[TYPE] {name}: hypothesis holds, x* = {x} expanding (lambda = {inf['xstar_lam']}), "
          f"its SCC is not a simple cycle (type (c)) at K = m and m+2", good)

inf = classify(SYS["K7z"], 2)
claim("[TYPE] K7z: G_2 is one SCC (Lambda = Z_2)", len(inf["comps"]) == 1)

# negative controls
inf = classify(SYS["acc_h16"], 4, Fr(-1))
sizes = sorted(len(C) for C in inf["comps"])
tys = sorted(t for _, t in inf["types"])
claim(f"[TYPE] control acc_h16: SCC sizes {sizes}, types {tys}: no type (c) (must not be (c))",
      inf["hyp"] and not inf["xstar_type_c"] and "c?" not in tys and "b" in tys)
inf = classify(SYS["cert_ctrl"], 4)
claim("[TYPE] control cert_ctrl: every SCC contracting (CERT)",
      inf["hyp"] and all(t == "a" for _, t in inf["types"]))


# ------------------------------------------------------------------ [BRUTE]
def brute(sd, N, lo=1, cap=10 ** 30, maxsteps=20000):
    minima, escaped = set(), []
    for n0 in range(lo, N):
        x, steps, seen = n0, 0, None
        while True:
            x = T_int(sd, x)
            steps += 1
            if x < n0:
                break
            if x == n0:
                minima.add(n0)
                break
            if x > cap:
                escaped.append(n0)
                break
            if steps > maxsteps:
                # cycle above n0 not containing n0: find it
                seen = {}
                y = x
                while y not in seen:
                    seen[y] = 1
                    y = T_int(sd, y)
                    if y > cap:
                        escaped.append(n0)
                        break
                break
    return sorted(minima), escaped


expected = {"sf3_7": [1], "sf3_17": [1], "sf3_57": [1], "sf3_157": [1], "sf3_357": [1],
            "sf3_13": [1, 3], "sf3_135": [1]}
for name, ex in expected.items():
    mins, esc = brute(SYS[name], 10 ** 6)
    claim(f"[BRUTE] {name}: all n < 10^6 reach cycles with minima {mins}", mins == ex and not esc)
mins, esc = brute(SYS["K7z"], 10 ** 6, lo=1)
claim(f"[BRUTE] K7z: all 1 <= z < 10^6 reach 0 (cycle minima found {mins}; 0 is the fixed point)",
      mins == [] and not esc and T_int(SYS["K7z"], 0) == 0 and T_int(SYS["K7z"], 1) == 0)
mins, esc = brute(SYS["sf3_137"], 20000)
claim(f"[BRUTE] sf3_137 (expected divergent, not claimed): {len(esc)} starts < 2e4 pass 10^30; "
      f"cycle minima seen {mins}", len(esc) > 0)


# ------------------------------------------------------------------ [SHADOW]
def shadow(sd, y, k, N):
    """Integers n = y mod p^M follow y for k periods and n' = y + lam^k (n - y)."""
    nodes, lam = orbit_walk(sd, y, 1)
    L = len(nodes)
    p = sd["p"]
    D = 0
    x, prod = Fr(y), Fr(1)
    for _ in range(L * k):
        x, q = T_rat(sd, x)
        prod *= q
    assert prod == lam ** k
    # total divisions over k periods
    D = vp(prod.denominator, p)
    M = N + D + sd["m"] + 2
    base = res(y, p, M)
    good = True
    for j in range(1, 6):
        n = base + p ** M * (10 ** 6 * j + random.randrange(10 ** 6))
        z, mn = n, n
        for _ in range(L * k):
            z = T_int(sd, z)
            mn = min(mn, z)
        good = good and Fr(z) - y == lam ** k * (Fr(n) - y)
        good = good and res(z, p, N) == res(y, p, N) and z >= 2 * n and 8 * mn >= n
    return good, lam


random.seed(20261127)
for name in ["sf3_7", "sf3_13", "sf3_137", "K7z", "3x+1", "5x+1"]:
    sd = SYS[name]
    nodes, lam = orbit_walk(sd, Fr(XS[name]), 1)
    k = 1
    while lam ** k < 2:
        k += 1
    g, lam = shadow(sd, Fr(XS[name]), k + 1, 20)
    claim(f"[SHADOW] {name}: n = x* (mod p^M) gives T^(kL) n - x* = lam^k (n - x*), n' >= 2n, "
          f"n' = x* mod 2^20, orbit stays >= n/8", g)


# ------------------------------------------------------------------ [DENSE]
def walk_point(sd, K, walk):
    """walk = list of nodes (closed: walk[0] after walk[-1]). Returns (y, lam)."""
    p, m, tab = sd["p"], sd["m"], sd["tab"]
    A, B = Fr(1), Fr(0)
    for i, r in enumerate(walk):
        u, v, w = tab[r % p ** m]
        A, B = A * Fr(u, w), (u * B + v) / w
    y = B / (1 - A)
    return y, A


def check_walk(sd, K, walk):
    y, A = walk_point(sd, K, walk)
    if y.denominator % sd["p"] == 0:
        return False
    x = y
    for r in walk:
        if res(x, sd["p"], K) != r:
            return False
        x, _ = T_rat(sd, x)
    return x == y and A > 1


def bfs_path(G, C, a, b):
    from collections import deque
    prev = {a: None}
    dq = deque([a])
    while dq:
        v = dq.popleft()
        if v == b and v != a or (v == b and a == b and len(prev) > 1):
            break
        for (w, _, _) in G[v]:
            if w in C and w not in prev:
                prev[w] = v
                dq.append(w)
    path, v = [], b
    while v != a:
        path.append(v)
        v = prev[v]
    return path[::-1]     # excludes a, ends with b


for name in ["K7z", "sf3_13", "3x+1"]:
    sd = SYS[name]
    K = sd["m"] + 1
    inf = classify(sd, K, Fr(XS[name]))
    G, C = inf["G"], inf["xstar_comp"]
    cyc, _ = orbit_walk(sd, Fr(XS[name]), K)
    good, cnt = True, 0
    for t in (10, 20, 40):
        for _ in range(4):
            v = random.choice(sorted(C))
            walk = [v]
            for _ in range(t - 1):
                v = random.choice([b for (b, _, _) in G[v] if b in C])
                walk.append(v)
            to_r = bfs_path(G, C, walk[-1], cyc[0]) if walk[-1] != cyc[0] else []
            seg = walk + to_r                    # ends at cyc[0]
            for d in range(1, 200):
                full = seg + (cyc[1:] + [cyc[0]]) * d    # d full turns, ends at cyc[0]
                back = bfs_path(G, C, cyc[0], walk[0]) if cyc[0] != walk[0] else []
                full2 = full + back[:-1] if back else full[:-1]   # closing edge -> walk[0]
                y, A = walk_point(sd, K, full2)
                if A > 1:
                    good = good and check_walk(sd, K, full2)
                    cnt += 1
                    break
            else:
                good = False
    claim(f"[DENSE] {name}: {cnt} random walks (length 10/20/40) in the type-(c) SCC at K = m+1 "
          f"are realised by expanding rational periodic points (checked by iteration)", good and cnt == 12)
# negative control of check_walk: a contracting walk must be rejected
sd = SYS["cert_ctrl"]
claim("[DENSE] control: a contracting closed walk is rejected by the walk checker",
      not check_walk(sd, 2, [1]))


# ------------------------------------------------------------------ [NEUTRAL]
# theory.md W2 "only if", division-free case: "Its multiplier is the product of the u's,
# which is > 1".  A division-free cycle with all u = 1 has multiplier exactly 1.
neut = dict(p=2, m=2, tab=[(1, 0, 2), (1, 4, 1), (1, 0, 2), (3, 1, 2)])
G = graph(neut, 2)
loop = [(s, q, e) for (s, q, e) in G[1] if s == 1]
claim("[NEUTRAL] n = 1 (4) -> n + 4 gives a division-free G_2 self-loop with multiplier exactly 1 "
      "(so 'product of the u's > 1' is false; the conclusion 'no certificate' still holds: "
      "the class diverges)", loop == [(1, Fr(1), 0)] and not division_free_acyclic(G)
      and T_int(neut, T_int(neut, 5)) == 13)


# ------------------------------------------------------------------ [TYPEB]
sd = SYS["acc_h16"]
G = graph(sd, 4)
comps = sccs(G)
comp_of = {v: i for i, C in enumerate(comps) for v in C}
# DAG height: lev(C) = 1 + max lev(successor component), sinks 0
lev = {}


def height(i):
    if i in lev:
        return lev[i]
    succ = {comp_of[b] for a in comps[i] for (b, _, _) in G[a]} - {i}
    lev[i] = 1 + max((height(j) for j in succ), default=-1)
    return lev[i]


for i in range(len(comps)):
    height(i)
big = [C for C in comps if len(C) == 10][0]
shad = [C for C in comps if len(C) == 2][0]
theta = Fr(99, 100)
# theory.md's Remark puts c(r) n only on the 10-node SCC and 0 on "transient nodes".  But
# {0} is a 1-node SCC WITH a self-loop (n = 0 (16) -> n/2 can be = 0 (16)), so it is a
# contracting SCC, not transient.  The as-written V must fail on n = 0 (32); the repaired
# V puts c(r) n on every contracting SCC with an internal edge.
contr = [C for C in comps if internal_edges(G, C) and C != shad]
c = {}
for C in contr:
    cc = contracting_potential(G, C, theta)
    assert cc is not None
    c.update(cc)
beta = max(c.values()) * 5        # max v = 5, w = 1 or 2
cond = shad == frozenset({14, 15}) and sorted(len(C) for C in contr) == [1, 10] \
    and any(C == frozenset({0}) for C in contr)
AS_WRITTEN = False


def V(n):
    r = n % 16
    L = height(comp_of[r])
    if r in c and (not AS_WRITTEN or r in big):
        ph = c[r] * n
    elif r == 15:
        ph = Fr(2 * vp(n + 1, 2))
    elif r == 14:
        ph = Fr(2 * vp(n // 2 + 1, 2) + 1)
    else:
        ph = Fr(0)
    return (L, int(2 * ph))      # floor(2 phi), phi >= 0


bad = []
for n in range(1, 300000):
    if not V(T_int(sd, n)) < V(n):
        bad.append(n)
# proven threshold: inside big SCC, phi(Tn) <= theta phi + beta <= phi - 1/2 once
# (1 - theta) phi >= beta + 1/2, i.e. n >= (beta + 1/2)/((1-theta) min c)
thr = (beta + Fr(1, 2)) / ((1 - theta) * min(c.values()))
claim(f"[TYPEB] acc_h16: own lexicographic (level, floor 2 phi) counter potential descends for all "
      f"n < 3e5 except {len(bad)} values, all < {max(bad) + 1 if bad else 0} <= proven threshold "
      f"{float(thr):.0f}; shadow SCC {sorted(shad)}", cond and all(b < thr for b in bad))
AS_WRITTEN = True
bad_w = [n for n in range(1, 20000) if not V(T_int(sd, n)) < V(n)]
AS_WRITTEN = False
claim(f"[TYPEB] the Remark's V AS WRITTEN (c(r) n only on the 10-node SCC, 0 elsewhere) fails "
      f"at infinitely many n: {len(bad_w)} failures < 2e4, all n = 0 (32) above 2400",
      all(n % 32 == 0 for n in bad_w if n > 2400) and sum(1 for n in bad_w if n > 2400) > 500)
# the two counter identities, exactly
ok15 = all(2 * vp((3 * n + 1) // 2 + 1, 2) + 1 == 2 * vp(n + 1, 2) - 1
           for n in range(15, 10 ** 5, 16))
claim("[TYPEB] counter step 15 -> 14 lowers phi by exactly 1", ok15)

# ------------------------------------------------------------------ Theorem A
MODP = 998244353


def closed_walks(u, k):
    out = {}
    for x in range(2 ** k):
        for c0 in range(u):
            c, y = c0, 0
            for i in range(k):
                t = u * ((x >> i) & 1) + c
                y |= (t & 1) << i
                c = t >> 1
            if c == c0:
                out.setdefault(x, []).append((c0, y))
    return out


good = True
for u in (3, 5):
    for k in range(1, 14, 2):
        cw = closed_walks(u, k)
        good = good and len(cw) == 2 ** k and all(len(v) == 1 for v in cw.values()) \
            and sorted(v[0][1] for v in cw.values()) == list(range(2 ** k)) \
            and all(v[0][1] == u * x - v[0][0] * (2 ** k - 1) for x, v in cw.items())
claim("[BIJ] u = 3, 5, odd k <= 13: one closed walk per word, x -> y a permutation", good)
cw = closed_walks(3, 4)
claim("[BIJ] control u = 3, k = 4 (3 | 2^4 - 1): bijection fails",
      not (all(len(v) == 1 for v in cw.values()) and len(cw) == 16))


def window(n, i, s):
    return (n >> i) & ((1 << s) - 1) if i >= 0 else (n << (-i)) & ((1 << s) - 1)


def Vf(f, s, n):
    return sum(f[window(n, i, s)] for i in range(n.bit_length()))


def Ef(f, s, h):
    return sum(f[window(h, i, s)] - f[0] for i in range(-(s - 1), h.bit_length()))


def Fcyc(f, s, x, k):
    xx = x | (x << k)     # doubled for cyclic windows
    return sum(f[(xx >> i) & ((1 << s) - 1)] for i in range(k))


# [PUMP] 3x+1 odd branch (3n+1)/2 on r = 1 mod 2; s = 3
s = 3
good = True
for trial in range(3):
    f = [random.randrange(-5, 6) for _ in range(2 ** s)]
    for k in range(1, 6):
        for x, lst in closed_walks(3, k).items():
            c0, y = lst[0]
            Phi = Fcyc(f, s, y, k) - Fcyc(f, s, x, k)
            b = 4
            betas = [bt for bt in range(2 ** b) if (3 * (1 + 2 * bt) + 1) >> (1 + b) == c0]
            if not betas:
                good = False
                continue
            bt = betas[0]
            diffs = []
            for M in range(4, 10):
                XM = sum(x << (k * j) for j in range(M))
                n = 1 + 2 * (bt + (XM << b))
                Tn = (3 * n + 1) // 2
                diffs.append(Vf(f, s, Tn) - Vf(f, s, n) - M * Phi)
            good = good and len(set(diffs)) == 1
claim("[PUMP] V(T n_M) - V(n_M) - M Phi(x) is independent of M (3x+1 branch, s = 3, k <= 5)", good)

# [STEP3]
good = True
for u in (3, 5):
    for s in (3, 4):
        f = [random.randrange(-9, 10) for _ in range(2 ** s)]
        for h in range(1, 200):
            k = (u * h).bit_length() + s
            k += 1 - k % 2
            (c0, y), = closed_walks(u, k)[h] if k <= 13 else [(0, u * h)]
            good = good and c0 == 0 and y == u * h
            good = good and Fcyc(f, s, y, k) - Fcyc(f, s, h, k) == Ef(f, s, u * h) - Ef(f, s, h)
            good = good and Fcyc(f, s, h, k) == f[0] * k + Ef(f, s, h)
claim("[STEP3] F(y) - F(x) = E_f(uh) - E_f(h) and F(x) = c0 k + E_f(h) (exact)", good)


def rank_mod(A, p=MODP):
    A = np.array(A, dtype=np.int64) % p
    rows, cols = A.shape
    r = 0
    for col in range(cols):
        piv = None
        nz = np.nonzero(A[r:, col])[0]
        if len(nz) == 0:
            continue
        piv = r + nz[0]
        A[[r, piv]] = A[[piv, r]]
        inv = pow(int(A[r, col]), p - 2, p)
        A[r] = (A[r] * inv) % p
        below = A[r + 1:, col].copy()
        idx = np.nonzero(below)[0]
        if len(idx):
            A[r + 1 + idx] = (A[r + 1 + idx] - (below[idx, None] * A[r]) % p) % p
        r += 1
        if r == rows:
            break
    return r


def ematrix(u, s):
    rows = []
    for h in range(1, 2 ** (s + 2)):
        row = [0] * (2 ** s)
        for hh, sg in ((u * h, 1), (h, -1)):
            for i in range(-(s - 1), hh.bit_length()):
                row[window(hh, i, s)] += sg
                row[0] -= sg
        rows.append(row)
    return rows


def kernel_basis(s):
    vecs = [[1] * (2 ** s)]
    for a in range(2 ** (s - 1)):        # coboundary of the indicator of word a (length s-1)
        v = [0] * (2 ** s)
        for w in range(2 ** s):
            hi = w >> 1                  # digits w_1..w_{s-1}
            lo = w & ((1 << (s - 1)) - 1)  # digits w_0..w_{s-2}
            v[w] += (hi == a) - (lo == a)
        vecs.append(v)
    return vecs


for u, smax in ((3, 10), (5, 8), (1, 6)):
    res_ = []
    good = True
    for s in range(1, smax + 1):
        A = ematrix(u, s)
        rk = rank_mod(A)
        res_.append(rk)
        target = 2 ** (s - 1) if u != 1 else 0
        good = good and rk == target
        if u != 1 and s <= 8:
            Kb = kernel_basis(s)
            An = np.array(A, dtype=np.int64)
            good = good and all(not np.any(An @ np.array(v, dtype=np.int64)) for v in Kb)
            good = good and rank_mod(Kb) == 2 ** (s - 1)
    lab = "control u = 1 must give rank 0" if u == 1 else f"rank = 2^(s-1) for s <= {smax}"
    claim(f"[RANK] u = {u}: ranks {res_} ({lab}); constants+coboundaries in kernel, dim 2^(s-1)", good)

# [CTRL-A] positive control.  cert_ctrl has a x3 branch and no expanding point; the window
# potential V = (len - 1) + log2(top8/128) (c0 = 1, h = top-digit term) descends by 1/3 for
# n >= 128.  Exact form: 2 * W(Tn)^3 <= W(n)^3 with W(n) = top8(n) * 2^(len(n)-1)/128 ... compare
# integers t^3 2^(3 len).
def topw(n):
    L = n.bit_length()
    t = n >> (L - 8)
    return t, L


good = True
for n in range(128, 400000):
    m = T_int(SYS["cert_ctrl"], n)
    if m < 128:
        continue
    t1, L1 = topw(m)
    t0, L0 = topw(n)
    good = good and 2 * t1 ** 3 * 2 ** (3 * L1) <= t0 ** 3 * 2 ** (3 * L0)
claim("[CTRL-A] a width-1 window potential with a top-digit term certifies the CERT x3 system "
      "(consistent: Theorem A needs an expanding periodic point)", good)

# ------------------------------------------------------------------ [MB]
BR = {"Z": (1, 1, 27), "E": (1, 0, 2), "O": (3, 1, 2)}


def mb_branch(x):
    x = Fr(x)
    if res(x, 3, 3) == 26:
        return "Z"
    return "E" if res(x, 2, 1) == 0 else "O"


def lyndon(alpha, nmax):
    w = [-1]
    k = len(alpha)
    while w:
        w[-1] += 1
        yield "".join(alpha[i] for i in w)
        m = len(w)
        while len(w) < nmax:
            w.append(w[len(w) - m])
        while w and w[-1] == k - 1:
            w.pop()


orbits = []
for word in lyndon("EOZ", 12):
    A, B = Fr(1), Fr(0)
    for b in word:
        u, v, w = BR[b]
        A, B = A * Fr(u, w), (u * B + v) / w
    if A == 1:
        continue
    y = B / (1 - A)
    if y.denominator % 2 == 0 or y.denominator % 3 == 0:
        continue
    x, good = y, True
    for b in word:
        if mb_branch(x) != b:
            good = False
            break
        u, v, w = BR[b]
        x = (u * x + v) / w
    if good and x == y:
        orbits.append((word, y, A))
expw = sorted((len(wd), str(A)) for wd, y, A in orbits if A > 1)
cyc5 = [-5]
for _ in range(3):
    b = mb_branch(cyc5[-1])
    u, v, w = BR[b]
    cyc5.append((u * Fr(cyc5[-1]) + v) / w)
claim(f"[MB] own Lyndon enumeration: {len(orbits)} rational periodic orbits of period <= 12; "
      f"expanding (period, multiplier): {expw}; -5 -> {cyc5[1]} -> {cyc5[2]} -> {cyc5[3]}",
      len(orbits) == 16274 and expw == [(3, "9/8"), (11, "2187/2048")]
      and cyc5 == [-5, -7, -10, -5])
mem = [y for wd, y, A in orbits if len(wd) == 11 and A > 1][0]
orb11 = [mem]
for _ in range(10):
    b = mb_branch(orb11[-1])
    u, v, w = BR[b]
    orb11.append((u * orb11[-1] + v) / w)
claim("[MB] the 11-cycle passes through -10138/139", Fr(-10138, 139) in orb11)
good = True
for d, tail in ((10, "OE"), (20, "EE"), (40, "EE")):
    word = "OOE" * d + tail
    A, B = Fr(1), Fr(0)
    for b in word:
        u, v, w = BR[b]
        A, B = A * Fr(u, w), (u * B + v) / w
    y = B / (1 - A)
    x, g = y, y.denominator % 6 != 0 and y.denominator % 2 != 0 and y.denominator % 3 != 0
    for b in word:
        g = g and mb_branch(x) == b
        u, v, w = BR[b]
        x = (u * x + v) / w
    good = good and g and x == y and A > 1 and y not in (-5, -7, -10)
claim("[MB] homoclinic expanding points (OOE)^d w for d = 10, 20, 40 (exact)", good)

# ------------------------------------------------------------------ [SRS]
VAL = {"f": (2, 0), "t": (2, 1), "a": (3, 0), "b": (3, 1), "c": (3, 2), "p": (1, 1)}


def aff(word):         # word without L/R acting on prefix value: x -> mul x + add
    mul, add = 1, 0
    for ch in word:
        b, d = VAL[ch]
        mul, add = mul * b, add * b + d
    return mul, add


def bitsw(n, width=None):
    s = bin(n)[2:] if n else ""
    if width:
        s = s.rjust(width, "0")
    return "".join("t" if ch == "1" else "f" for ch in s)


def common():
    R = []
    for x in "ft":
        for e in "abc":
            tot = 3 * VAL[x][1] + VAL[e][1]
            R.append(("swap_" + x + e, x + e, "abc"[tot // 2] + "ft"[tot % 2]))
    return R + [("left_a", "La", "L"), ("left_b", "Lb", "Lt"), ("left_c", "Lc", "Ltf")]


def k7_rules():
    return [("e0", "fR", "R"), ("e1", "ftR", "R"), ("e3", "ttR", "ctR"), ("small1", "LtR", "LR")] + common()


def core_rules(S, three_on_cycle):
    R = [("even", "fR", "R"), ("lead0", "Lf", "L")]
    for r in (1, 3, 5, 7):
        if r in S:
            q, rem = divmod(3 * r + 1, 8)
            R.append((f"odd{r}", bitsw(r, 3) + "R", "abc"[q] + bitsw(rem, 3) + "R"))
        elif r < 7:
            R.append((f"inc{r}", bitsw(r, 3) + "R", bitsw(r + 1, 3) + "R"))
        else:
            R.append(("inc7", "tttR", "pfffR"))
    R += [("p_f", "fp", "t"), ("p_t", "tp", "pf"), ("p_a", "ap", "b"), ("p_b", "bp", "c"),
          ("p_c", "cp", "pa"), ("p_L", "Lp", "Lt")]
    if not three_on_cycle:
        T3 = 10 if 3 in S else 4
        R.append(("small3", "LttR", "L" + bitsw(T3) + "R"))
    return R + common()


def rule_sem_ok(rule, Tfun):
    _, l, r = rule
    if l[0] == "L":
        lv, rv = aff(l[1:].rstrip("R")), aff(r[1:].rstrip("R"))
        if l.endswith("R"):                      # whole number: L w R -> L w' R
            return Tfun(lv[1]) == rv[1]
        return lv[1] == rv[1]                    # anchored at L (prefix value 0): same value
    if l.endswith("R"):
        lv, rv = aff(l[:-1]), aff(r[:-1])
        return all(Tfun(lv[0] * x + lv[1]) == rv[0] * x + rv[1] for x in range(0, 200))
    return aff(l) == aff(r)


def K7T(z):
    return T_int(SYS["K7z"], z)


good = all(rule_sem_ok(rl, K7T) for rl in k7_rules())
claim("[SRS] K7 rules (own list, 13): every rule preserves value or applies K7 to the whole number",
      good and len(k7_rules()) == 13)
for name, S in CORES.items():
    if name == "sf3_137":
        continue
    toc = name == "sf3_13"
    Tf = (lambda n, S=S: T_int(SYS[name], n))
    rules = core_rules(S, toc)
    good = all(rule_sem_ok(rl, Tf) for rl in rules if not rl[0] == "small3") and \
        all(rule_sem_ok(rl, Tf) for rl in rules if rl[0] == "small3")
    claim(f"[SRS] {name}: {len(rules)} rules semantically correct", good)
bad_rule = ("e3bad", "ttR", "ctfR")
claim("[SRS] control: a wrong map rule is rejected", not rule_sem_ok(bad_rule, K7T))


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def interp(word, I, d):
    M = [[int(i == j) for j in range(d)] for i in range(d)]
    v = [0] * d
    for ch in word:                              # [a1...ak] = f_a1 o ... o f_ak
        Ma, va = I[ch]
        v = [v[i] + sum(M[i][k] * va[k] for k in range(d)) for i in range(d)]
        M = mm(M, Ma)
    return M, v


def chain_check(rules, chain):
    rem = list(rules)
    for d, I in chain:
        for ch, (M, v) in I.items():
            if M[0][0] < 1 or min(min(r) for r in M) < 0 or min(v) < 0:
                return None
        strict = []
        for nm, l, r in rem:
            Ml, vl = interp(l, I, d)
            Mr, vr = interp(r, I, d)
            if any(Ml[i][j] < Mr[i][j] for i in range(d) for j in range(d)) or any(vl[i] < vr[i] for i in range(d)):
                return None
            if vl[0] > vr[0]:
                strict.append(nm)
        if not strict:
            return None
        rem = [x for x in rem if x[0] not in strict]
    return [x[0] for x in rem]


with open(os.path.join(HERE, "mi_chains.json")) as fh:
    CH = json.load(fh)
allok = True
for name, data in CH.items():
    if name == "K7":
        rules = k7_rules()
    else:
        S = CORES[name]
        rules = core_rules(S, name == "sf3_13")
    chain = [(d, {k: (v[0], v[1]) for k, v in I.items()}) for d, I in data["chain"]]
    rem = chain_check(rules, chain)
    allok = allok and rem is not None and sorted(rem) == sorted(data["remaining"]) \
        and len(rules) == data["n_rules"]
    mapr = {"K7": ["e0", "e1", "e3"]}.get(name)
    if mapr is None:
        mapr = [r[0] for r in rules if r[0].startswith(("odd", "inc", "even"))]
    removed = sorted(set(r[0] for r in rules) - set(rem or []))
    allok = allok and all(m in (rem or []) for m in mapr)
    print(f"   {name}: removed {removed}")
claim("[SRS] stored chains re-verified with own algebra; every class map rule remains", allok)

print("ALL PASS" if OK else "SOME FAILED")
sys.exit(0 if OK else 1)
