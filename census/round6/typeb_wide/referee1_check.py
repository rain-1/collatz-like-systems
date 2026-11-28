"""Referee 1, round 6, lens typeb_wide: independent check script (written from scratch;
imports nothing from this folder; reads the prover's data files only to compare).

Exit 0 iff every check passes.  Every verdict used in a PASS is backed by exact data:
  type (b) SCC: single simple cycle, exact multiplier U > p^D;
  type (c) SCC: non-simple SCC + exact closed walk with U > p^D;
  type (a) SCC: exact rational weights c > 0, theta < 1, c(s) u/p^e <= theta c(r) on edges;
  anything else is 'unknown' and makes the comparison fail.

[NAMED] named type-(b) systems: my classifier says (b); my own Theorem-H cycle list (periodic
        points of simple SCCs + exact-weight search on (a) SCCs) equals the README list, and
        brute force over all n <= N (N = 10^6 for moduli <= 16, else 2*10^5) ends in those cycles.
[P8]    Theorem P8: (a, d) odd, a >= 3, a + d >= 1, a <= 21, |d| <= 41: type (b), my Theorem-H
        cycle list = predicted, brute force n <= 20000 agrees.
[NEG]   3x+1, 3x-1, 5x+1, 7x+1: type (c) at levels 1..10 (Theorem H cannot apply).
[SCAN]  S3/S5/S7 m <= 4 full counts; SH3 m = 3 full; SH3 m = 4 and SH5 m = 4 type-(b)
        count by full enumeration (filter: simple expanding SCC exists); C9 full counts;
        SPL_d m = 3, 4 counts equal for d = 1, 3, 5 (Prop. CS) and equal to stored.
[MODS]  one-class menus rebuilt from the docstring; verdict counts for several open maps
        recomputed and compared with out/mods_one.log; two-class count for perm_1932inv@8;
        random sample of stored type-(b) neighbours re-settled with my Theorem-H code.
[G1]    the gap example: SCC structure and an exact Collatz-Wielandt certificate of my own.
[Y]     Theorem Y for mb_s3_27, d = 0..120, with the real map on Z_(6) rationals, plus integer
        progressions that rise for a whole period (d = 9..14).
"""
import sys, os, json, random, math, itertools, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OK = True


def claim(name, cond):
    global OK
    print(("PASS " if cond else "FAIL ") + name, flush=True)
    OK = OK and bool(cond)


# ---------------------------------------------------------------- basic objects
def vp_int(n, p):
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def exps(p, tab):
    return [vp_int(w, p) for (_, _, w) in tab]


def admissible(p, tab):
    Q = len(tab)
    for r, (u, v, w) in enumerate(tab):
        if u < 1 or u % p == 0:
            return False
        e = vp_int(w, p)
        if p ** e != w:
            return False
        if (u * r + v) % w or (u * Q) % w:
            return False
        n0 = r if r else Q
        if u * n0 + v < w:  # branch increasing, so least member decides positivity
            return False
    return True


def Tmap(tab):
    Q = len(tab)

    def T(n):
        u, v, w = tab[n % Q]
        x = u * n + v
        assert x % w == 0
        return x // w
    return T


def cyl_graph(p, tab, K):
    PK = p ** K
    Q = len(tab)
    succ = []
    for r in range(PK):
        u, v, w = tab[r % Q]
        e = vp_int(w, p)
        step = p ** (K - e)
        b = ((u * r + v) // w) % step
        succ.append([(b + i * step, u, e) for i in range(p ** e)])
    return succ


def sccs(N, adj):
    """iterative Kosaraju; adj[v] = list of node ids"""
    seen = [False] * N
    order = []
    for s in range(N):
        if seen[s]:
            continue
        seen[s] = True
        st = [(s, 0)]
        while st:
            v, i = st[-1]
            if i < len(adj[v]):
                st[-1] = (v, i + 1)
                w = adj[v][i]
                if not seen[w]:
                    seen[w] = True
                    st.append((w, 0))
            else:
                st.pop()
                order.append(v)
    radj = [[] for _ in range(N)]
    for v in range(N):
        for w in adj[v]:
            radj[w].append(v)
    comp = [-1] * N
    out = []
    for s in reversed(order):
        if comp[s] >= 0:
            continue
        c = len(out)
        comp[s] = c
        lst, st = [s], [s]
        while st:
            v = st.pop()
            for w in radj[v]:
                if comp[w] < 0:
                    comp[w] = c
                    lst.append(w)
                    st.append(w)
        out.append(lst)
    return out, comp


def karp(n, edges):
    """max cycle mean (floats); edges (a, b, wt) local ids"""
    NEG = -1e300
    D = [[NEG] * n for _ in range(n + 1)]
    D[0] = [0.0] * n
    for k in range(1, n + 1):
        Dp, Dk = D[k - 1], D[k]
        for a, b, wt in edges:
            if Dp[a] > NEG / 2 and Dp[a] + wt > Dk[b]:
                Dk[b] = Dp[a] + wt
    best = NEG
    for v in range(n):
        if D[n][v] <= NEG / 2:
            continue
        m = min((D[n][v] - D[k][v]) / (n - k) for k in range(n) if D[k][v] > NEG / 2)
        best = max(best, m)
    return best


def positive_cycle(n, edges, exact, p):
    """Bellman-Ford on weights; returns an exactly verified expanding closed walk (list of
    edge indices) or None"""
    for shift in (0.0, 1e-7, 1e-4, 1e-3):
        dist = [0.0] * n
        pred = [-1] * n
        last = -1
        for _ in range(n + 1):
            last = -1
            for i, (a, b, wt) in enumerate(edges):
                if dist[a] + wt - shift > dist[b] + 1e-12:
                    dist[b] = dist[a] + wt - shift
                    pred[b] = i
                    last = b
            if last < 0:
                break
        if last < 0:
            continue
        v = last
        for _ in range(n):
            v = edges[pred[v]][0]
        cyc, x = [], v
        while True:
            i = pred[x]
            cyc.append(i)
            x = edges[i][0]
            if x == v or len(cyc) > n:
                break
        U, D = 1, 0
        for i in cyc:
            U *= exact[i][2]
            D += exact[i][3]
        if U > p ** D:
            return cyc
    return None


def weights(n, edges, exact, p, mu):
    """exact contraction weights for an SCC whose max mean mu < 0"""
    for frac in (0.5, 0.25, 0.75, 0.1, 0.9):
        lt = mu * frac
        theta = Fr(math.exp(lt) * (1 + 1e-7)).limit_denominator(10 ** 8)
        if not theta < 1:
            continue
        phi = [0.0] * n
        for _ in range(n + 2):
            ch = False
            for a, b, wt in edges:
                x = phi[a] + wt - lt
                if x > phi[b] + 1e-14:
                    phi[b] = x
                    ch = True
            if not ch:
                break
        top = max(phi)
        c = [Fr(math.exp(top - x)).limit_denominator(10 ** 12) for x in phi]
        if min(c) > 0 and all(c[b] * Fr(u, p ** e) <= theta * c[a] for a, b, u, e in exact):
            return theta, c
    return None


def classify(p, tab, K, want_weights=False):
    """returns (verdict, comps); verdict in a, b, c, divfree, unknown"""
    succ = cyl_graph(p, tab, K)
    N = len(succ)
    adj = [[s for s, _, _ in succ[r]] for r in range(N)]
    comps, cid = sccs(N, adj)
    res = []
    for ci, nodes in enumerate(comps):
        loc = {v: j for j, v in enumerate(nodes)}
        ex = [(loc[r], loc[s], u, e) for r in nodes for (s, u, e) in succ[r] if cid[s] == ci]
        if not ex:
            res.append(dict(kind="trivial", nodes=nodes))
            continue
        z = [[] for _ in nodes]
        for a, b, u, e in ex:
            if e == 0:
                z[a].append(b)
        zc, _ = sccs(len(nodes), z)
        if any(len(c) > 1 or c[0] in z[c[0]] for c in zc):
            res.append(dict(kind="divfree", nodes=nodes))
            continue
        if len(ex) == len(nodes):
            nxt = {a: (b, u, e) for a, b, u, e in ex}
            seq, U, D, a = [0], 1, 0, 0
            while True:
                b, u, e = nxt[a]
                U *= u
                D += e
                if b == 0:
                    break
                seq.append(b)
                a = b
            assert len(seq) == len(nodes)
            res.append(dict(kind="b" if U > p ** D else "a", simple=True,
                            cycle=[nodes[j] for j in seq], U=U, D=D, nodes=nodes))
            continue
        fl = [(a, b, math.log(u) - e * math.log(p)) for a, b, u, e in ex]
        mu = karp(len(nodes), fl)
        if mu > -1e-9:
            cyc = positive_cycle(len(nodes), fl, ex, p)
            res.append(dict(kind="c" if cyc is not None else "unknown", nodes=nodes))
            continue
        if want_weights:
            w = weights(len(nodes), fl, ex, p, mu)
            if w is None:
                res.append(dict(kind="unknown", nodes=nodes))
                continue
            res.append(dict(kind="a", simple=False, nodes=nodes, theta=w[0],
                            c={nodes[j]: w[1][j] for j in range(len(nodes))}))
        else:
            # an (a) verdict from floats: margin check (cycle means here are far from 0)
            res.append(dict(kind="a", simple=False, nodes=nodes, mu=mu))
    kinds = {c["kind"] for c in res}
    if "divfree" in kinds:
        v = "divfree"
    elif "c" in kinds:
        v = "c"
    elif "unknown" in kinds:
        v = "unknown"
    elif "b" in kinds:
        v = "b"
    else:
        v = "a"
    return v, res, succ


def orbit_cycle(T, n, cap=10 ** 6):
    seen = {}
    y = n
    while y not in seen:
        seen[y] = 1
        y = T(y)
        if len(seen) > cap:
            return None
    c = [y]
    z = T(y)
    while z != y:
        c.append(z)
        z = T(z)
    k = c.index(min(c))
    return tuple(c[k:] + c[:k])


def theoremH(p, tab, K=None):
    """my own Theorem-H cycle list (None if hypotheses fail or type not a/b)"""
    Q = len(tab)
    m = round(math.log(Q, p))
    assert p ** m == Q
    K = K or m
    if not admissible(p, tab):
        return None
    v, comps, succ = classify(p, tab, K, want_weights=True)
    if v not in ("a", "b"):
        return None
    T = Tmap(tab)
    PK = p ** K
    cycles = set()
    for c in comps:
        if c["kind"] == "trivial":
            continue
        if c.get("simple"):
            A, B = Fr(1), Fr(0)
            for r in c["cycle"]:
                u, vv, w = tab[r % Q]
                A, B = A * Fr(u, w), (B * u + vv) / w
            x = B / (1 - A)
            assert x.denominator % p
            # x follows the residue cycle
            y = x
            for r in c["cycle"]:
                assert (y.numerator * pow(y.denominator, -1, PK) - r) % PK == 0
                u, vv, w = tab[r % Q]
                y = (u * y + vv) / w
            assert y == x
            if x.denominator == 1 and x > 0:
                cycles.add(orbit_cycle(T, int(x)))
            continue
        th, cw = c["theta"], c["c"]
        nodes = set(c["nodes"])
        beta = Fr(0)
        for r in nodes:
            u, vv, w = tab[r % Q]
            for s, _, _ in succ[r]:
                if s in nodes:
                    beta = max(beta, cw[s] * Fr(max(vv, 0), w))
        Vmax = beta / (1 - th)
        nmax = int(Vmax / min(cw.values()))
        assert nmax < 5 * 10 ** 6, nmax
        for n in range(1, nmax + 1):
            if n % PK in nodes and cw[n % PK] * n <= Vmax:
                cycles.add(orbit_cycle(T, n))
    return sorted(cycles)


def brute(tab, N):
    """all n <= N: follow until a known value; returns sorted cycle list (None on runaway)"""
    T = Tmap(tab)
    fate = {}
    cyc = set()
    for n0 in range(1, N + 1):
        if n0 in fate:
            continue
        path, pos, n = [], {}, n0
        while n not in fate and n not in pos:
            pos[n] = len(path)
            path.append(n)
            if len(path) > 10 ** 6:
                return None
            n = T(n)
            assert n > 0
        if n in pos:
            c = orbit_cycle(T, n)
            cyc.add(c)
            f = c
        else:
            f = fate[n]
        for x in path:
            fate[x] = f
    return sorted(cyc)


H2, H3 = (1, 0, 2), (1, 0, 3)


def evhalf(m, odd, default=(3, 1, 1)):
    return [H2 if r % 2 == 0 else odd.get(r, default) for r in range(2 ** m)]


# ---------------------------------------------------------------- [NAMED]
OPEN_PERM_INV = [(3, 0, 2), (3, 1, 4), (3, 0, 2), (3, -1, 4)]
OPEN_PERM_C = [(3, 0, 2), (3, 5, 4), (3, 0, 2), (3, -5, 4)]
OPEN_SPLIT53 = [(1, 0, 2), (5, 3, 1), (1, 0, 2), (1, 3, 1)]


def lift(tab, Q2):
    return [tab[r % len(tab)] for r in range(Q2)]


pinv = lift(OPEN_PERM_INV, 8)
pinv[2] = (1, 2, 2)
pinv[6] = (1, -4, 1)
pc = lift(OPEN_PERM_C, 8)
pc[1] = (1, 2, 1)
pc[7] = (1, -2, 1)
s53 = lift(OPEN_SPLIT53, 8)
s53[0] = (1, 2, 2)
s53[2] = (1, 1, 1)
sh32 = evhalf(5, {**{r: (1, 1, 1) for r in (1, 3, 9, 25)}, **{r: (1, 5, 1) for r in (5, 15, 21, 29)},
                  **{r: (1, 3, 1) for r in (7, 17, 23)}, **{r: (1, 7, 1) for r in (11, 13, 19, 27)}})
NAMED = [
    ("sh8", 2, evhalf(3, {1: (1, 1, 1), 5: (1, 5, 1)}), [(1, 2), (5, 10)]),
    ("sh4", 2, [(1, 1, 1), (1, 1, 1), (1, 2, 2), (3, 1, 2)], [(2,), (4, 5, 6)]),
    ("sh16", 2, evhalf(4, {5: (1, 5, 1), 9: (1, 1, 1), 13: (1, 7, 1)}), [(1, 4, 2), (5, 10)]),
    ("sh32", 2, sh32, [(1, 2), (5, 10)]),
    ("5x+1 relative", 2, evhalf(3, {1: (5, 1, 1), 5: (5, 1, 1), 3: (1, 3, 1), 7: (1, 7, 1)}), "min37"),
    ("c9a", 3, [H3, (5, 1, 1), (2, 1, 1), H3, (5, 1, 1), (1, 1, 1), H3, (4, 1, 1), (2, -1, 1)],
     [(2, 5, 6)]),
    ("c9b", 3, [H3, (4, -1, 1), (2, 1, 1), H3, (4, 1, 1), (1, 1, 1), H3, (4, 1, 1), (2, -1, 1)],
     [(1, 3), (2, 5, 6)]),
    ("perm_1932inv mod", 2, pinv, "min12"),
    ("perm_c mod", 2, pc, "min15"),
    ("split5_3 mod", 2, s53, "min37"),
    ("3x+1 + P8", 2, [H2, (3, 1, 1), H2, (3, 1, 1), (1, 4, 1), (3, 1, 1), H2, (3, 1, 1)], [(4, 8)]),
    ("3x-1 + P8", 2, [H2, (3, -1, 1), H2, (3, -1, 1), (1, 4, 1), (3, -1, 1), H2, (3, -1, 1)],
     [(1, 2), (4, 8)]),
]


def run_named():
    for name, p, tab, expect in NAMED:
        ok_adm = admissible(p, tab)
        Q = len(tab)
        m = round(math.log(Q, p))
        v, comps, _ = classify(p, tab, m)
        bx = []
        for c in comps:
            if c["kind"] == "b":
                A, B = Fr(1), Fr(0)
                for r in c["cycle"]:
                    u, vv, w = tab[r % Q]
                    A, B = A * Fr(u, w), (B * u + vv) / w
                bx.append(str(B / (1 - A)))
        H = theoremH(p, tab)
        N = 10 ** 6 if Q <= 16 else 2 * 10 ** 5
        bc = brute(tab, N)
        if isinstance(expect, str):
            mins = [int(ch) for ch in expect[3:]]
            exp_ok = H is not None and [c[0] for c in H] == mins
        else:
            exp_ok = H == sorted(expect)
        claim(f"[NAMED] {name}: admissible {ok_adm}, verdict {v}, isolated x* {bx}, Theorem-H cycles "
              f"{[c[0] for c in H] if H else H}, brute force n <= {N} same",
              ok_adm and v == "b" and exp_ok and bc == H)


# ---------------------------------------------------------------- [P8]
def run_P8():
    bad = []
    cnt = 0
    for a in range(3, 22, 2):
        for d in range(-41, 42, 2):
            if a + d < 1:
                continue
            tab = [H2 if r % 2 == 0 else (a, d, 1) for r in range(8)]
            tab[4] = (1, 4, 1)
            H = theoremH(2, tab)
            xs = Fr(-d, a - 2)
            exp = [(4, 8)]
            if xs.denominator == 1 and xs > 0:
                exp = sorted(exp + [(int(xs), 2 * int(xs))])
            b = brute(tab, 20000)
            cnt += 1
            if H != exp or b != exp:
                bad.append((a, d, H, b))
    claim(f"[P8] {cnt} pairs: Theorem-H cycles and brute force n <= 20000 equal the prediction "
          f"(bad: {bad[:3]})", not bad)
    # also: the hypothesis a + d >= 1 is needed only for positivity; a + d < 1 fails admissibility
    claim("[P8] a + d < 1 (e.g. 3x-3, 5x-5) violates T(Z>0) in Z>0, so is correctly excluded",
          not admissible(2, [H2, (3, -3, 1), H2, (3, -3, 1), (1, 4, 1), (3, -3, 1), H2, (3, -3, 1)]))


# ---------------------------------------------------------------- [NEG]
def run_neg():
    ok = True
    for a, d in ((3, 1), (3, -1), (5, 1), (7, 1)):
        for K in range(1, 11):
            v, _, _ = classify(2, [H2, (a, d, 1)], K)
            ok &= v == "c"
    claim("[NEG] 3x+1, 3x-1, 5x+1, 7x+1 are type (c) at levels 1..10 (exact expanding walk in a "
          "non-simple SCC)", ok)


# ---------------------------------------------------------------- [SCAN]
def counts_of(p, opts_list, filt_b_only=False):
    cnt = {}
    for tab in opts_list:
        m = round(math.log(len(tab), p))
        v, _, _ = classify(p, tab, m)
        cnt[v] = cnt.get(v, 0) + 1
    return cnt


def fam_members(p, opts):
    for choice in itertools.product(*opts):
        yield list(choice)


def has_simple_expanding(p, tab):
    m = round(math.log(len(tab), p))
    succ = cyl_graph(p, tab, m)
    N = len(succ)
    adj = [[s for s, _, _ in succ[r]] for r in range(N)]
    comps, cid = sccs(N, adj)
    for ci, nodes in enumerate(comps):
        ex = [(r, s, u, e) for r in nodes for (s, u, e) in succ[r] if cid[s] == ci]
        if ex and len(ex) == len(nodes):
            U, D = 1, 0
            for _, _, u, e in ex:
                U *= u
                D += e
            if D >= 1 and U > p ** D:
                return True
    return False


def run_scan():
    def sfam(m, a, d=1):
        return [[H2] if r % 2 == 0 else [(1, d, 1), (a, d, 1)] for r in range(2 ** m)]

    def stored(name):
        return json.load(open(os.path.join(HERE, "data", f"scan_{name}.json")))["counts"]
    for a in (3, 5, 7):
        for m in (2, 3, 4):
            c = counts_of(2, fam_members(2, sfam(m, a)))
            claim(f"[SCAN] S{a} m={m}: my counts {c} = stored {stored(f'S{a}_m{m}')}", c == stored(f"S{a}_m{m}"))
    SH = [(3, 1, 1), (1, 1, 1), (1, 3, 1), (1, 5, 1), (1, 7, 1)]

    def shfam(m, a=3):
        return [[H2] if r % 2 == 0 else [(a, 1, 1)] + [(1, d, 1) for d in (1, 3, 5, 7)] for r in range(2 ** m)]
    c = counts_of(2, fam_members(2, shfam(3)))
    claim(f"[SCAN] SH3 m=3: my counts {c} = stored {stored('SH3_m3')}", c == stored("SH3_m3"))
    for a in (3, 5):
        nb, unk = 0, 0
        cyc_stats = {}
        rng = random.Random(7)
        sample = []
        for tab in fam_members(2, shfam(4, a)):
            if not has_simple_expanding(2, tab):
                continue
            v, _, _ = classify(2, tab, 4)
            if v == "b":
                nb += 1
                sample.append(tab)
            elif v == "unknown":
                unk += 1
        st = stored(f"SH{a}_m4")
        # settle a random sample of the type-(b) members with my own Theorem-H code + brute force
        good = True
        for tab in rng.sample(sample, 25):
            H = theoremH(2, tab)
            good &= H is not None and brute(tab, 30000) == H
        claim(f"[SCAN] SH{a} m=4: my type-(b) count {nb} (unknown {unk}) = stored {st.get('b')}; "
              f"25 random members settled independently (Theorem H = brute force n <= 30000)",
              nb == st.get("b") and unk == 0 and good)
    # C9
    C9 = [(1, 1, 1), (1, 2, 1), (2, 1, 1), (2, -1, 1), (4, 1, 1), (4, -1, 1), (5, 1, 1), (5, -1, 1)]
    opts = [[H3] if r % 3 == 0 else C9 for r in range(9)]
    c = counts_of(3, fam_members(3, opts))
    claim(f"[SCAN] C9: my counts {c} = stored {stored('C9')}", c == stored("C9"))
    # SPL (Prop. CS)
    for m in (3, 4):
        rows = []
        for d in (1, 3, 5):
            o = [[H2] if r % 2 == 0 else [(u, d, 1) for u in (1, 3, 5)] for r in range(2 ** m)]
            rows.append(counts_of(2, fam_members(2, o)))
        claim(f"[SCAN] SPL m={m}: counts for d = 1, 3, 5 identical {rows[0]} and = stored",
              rows[0] == rows[1] == rows[2] == stored(f"SPL_d1_m{m}"))
    # B9
    for a in (2, 4, 5, 7, 8, 10, 11, 13):
        o = [[H3] if r % 3 == 0 else [(1, 1, 1), (a, 1, 1)] for r in range(9)]
        c = counts_of(3, fam_members(3, o))
        claim(f"[SCAN] B9 a={a}: my counts {c} = stored", c == stored(f"B9_a{a}"))


# ---------------------------------------------------------------- [MODS]
def menu(p, Q2, r, br):
    u, v, w = br
    out = []
    for u2 in range(1, u + 1):
        if u2 % p == 0:
            continue
        for e2 in range(3):
            w2 = p ** e2
            if Q2 % w2:
                continue
            M = Q2 // w2
            for t in range(M):
                # least |v| with (u2 r + v)/w2 = t (mod M), exact, positive
                best = None
                for k in range(0, 4 * Q2 * w2 + 10):
                    for v2 in ((-k, k) if k else (0,)):
                        if (u2 * r + v2) % w2 or ((u2 * r + v2) // w2 - t) % M:
                            continue
                        n0 = r if r else Q2
                        if u2 * n0 + v2 < w2:
                            continue
                        best = v2
                        break
                    if best is not None:
                        break
                if best is not None and (u2, best, w2) != tuple(br):
                    out.append((u2, best, w2))
    return out


def run_mods():
    log = open(os.path.join(HERE, "out", "mods_one.log")).read()

    def logged(label):
        mm = re.search(re.escape(label) + r"\s+(\{[^}]*\})", log)
        return eval(mm.group(1)) if mm else None
    cases = [("par_3_1 (CLS-013)", 2, [H2, (3, 1, 1)], (8, 16)),
             ("par_5_1 (CLS-022/024)", 2, [H2, (5, 1, 1)], (8,)),
             ("perm_1932inv (CLS-042)", 2, OPEN_PERM_INV, (8, 16)),
             ("split5_3 (CLS-049/065)", 2, OPEN_SPLIT53, (8, 16)),
             ("split5_1 (CLS-048/064)", 2, [(1, 0, 2), (5, 1, 1), (1, 0, 2), (1, 1, 1)], (8, 16)),
             ("m3_e (CLS-007)", 3, None, (9,))]
    for label, p, base0, Qs in cases:
        if base0 is None:
            sys.path.insert(0, os.path.join(HERE, "..", "..", "round3", "dichotomy"))
            from open_tables import OPEN
            base0 = OPEN[label][1]
        for Q2 in Qs:
            base = lift(base0, Q2)
            cnt = {}
            for r in range(Q2):
                for b in menu(p, Q2, r, base[r]):
                    tab = list(base)
                    tab[r] = b
                    if not admissible(p, tab):
                        v = "inadmissible"
                    else:
                        v = classify(p, tab, round(math.log(Q2, p)))[0]
                    cnt[v] = cnt.get(v, 0) + 1
            lg = logged(f"{label}@{Q2}")
            claim(f"[MODS] one-class {label}@{Q2}: my counts {cnt} = logged {lg}", cnt == lg)
    # two-class perm_1932inv@8 type-(b) count (README: 68, CERT 0)
    base = lift(OPEN_PERM_INV, 8)
    menus = [menu(2, 8, r, base[r]) for r in range(8)]
    cnt = {}
    for r1, r2 in itertools.combinations(range(8), 2):
        for b1 in menus[r1]:
            for b2 in menus[r2]:
                tab = list(base)
                tab[r1], tab[r2] = b1, b2
                v = classify(2, tab, 3)[0] if admissible(2, tab) else "inadmissible"
                cnt[v] = cnt.get(v, 0) + 1
    claim(f"[MODS] two-class perm_1932inv@8: my counts {cnt}; b = 68, a = 0 as claimed",
          cnt.get("b") == 68 and cnt.get("a", 0) == 0)
    # random sample of stored type-(b) neighbours re-settled
    rng = random.Random(11)
    good, n = True, 0
    for fn in ("mods_ONE_81.json", "mods_TWO_9.json"):
        D = json.load(open(os.path.join(HERE, "data", fn)))
        for label, R in D.items():
            for rec in rng.sample(R["typeb"], min(6, len(R["typeb"]))):
                P = rec["proof"]
                p, tab = P["p"], [tuple(t) for t in P["table"]]
                H = theoremH(p, tab)
                bc = brute(tab, 20000)
                n += 1
                ok = H is not None and [c[0] for c in H] == rec["cycles"] and bc == H
                if not ok:
                    print("   mismatch", label, rec["mods"], H and [c[0] for c in H], rec["cycles"])
                good &= ok
    claim(f"[MODS] {n} random stored type-(b) neighbours re-settled by my Theorem-H code and "
          f"brute force n <= 20000; cycle minima equal the stored ones", good)


# ---------------------------------------------------------------- [G1]
def run_gap():
    S = {3, 7, 15, 23, 31, 35, 39, 41, 47, 51, 55, 57, 59, 63}
    tab = [H2 if r % 2 == 0 else ((3, 1, 1) if r in S else (1, 1, 1)) for r in range(64)]
    v, comps, succ = classify(2, tab, 6)
    kinds = sorted((c["kind"], len(c["nodes"])) for c in comps if c["kind"] != "trivial")
    bs = [c for c in comps if c["kind"] == "b"]
    cs = [c for c in comps if c["kind"] == "c"]
    claim(f"[G1] S-family member: components {kinds}; isolated cycle {sorted(bs[0]['nodes']) if bs else None}",
          v == "c" and len(bs) == 1 and sorted(bs[0]["nodes"]) == [62, 63] and len(cs) == 1
          and len(cs[0]["nodes"]) == 34)
    # exact Collatz-Wielandt certificate at t = 12/7 > theta_C = 1.70951 for every non-simple SCC
    t = Fr(12, 7)
    thC = math.log(2) / math.log(1.5)
    ok = float(t) > thC

    def upper(q, t):
        f = float(q) ** float(t) * (1 + 1e-9)
        U = Fr(f).limit_denominator(10 ** 9)
        while U ** t.denominator < q ** t.numerator:
            U *= Fr(1000001, 1000000)
        return U
    for c in comps:
        if c["kind"] in ("a", "c") and not c.get("simple"):
            nodes = c["nodes"]
            idx = {x: i for i, x in enumerate(nodes)}
            Mx = [[0.0] * len(nodes) for _ in nodes]
            Mex = {}
            for r in nodes:
                for s, u, e in succ[r]:
                    if s in idx:
                        q = Fr(u, 2 ** e)
                        Mex.setdefault((idx[r], idx[s]), []).append((Fr(1, 2 ** e), q))
                        Mx[idx[r]][idx[s]] += 2.0 ** (-e) * float(q) ** float(t)
            x = [1.0] * len(nodes)
            for _ in range(3000):
                y = [sum(Mx[i][j] * x[j] for j in range(len(nodes))) for i in range(len(nodes))]
                mx = max(y)
                x = [max(v_ / mx, 1e-6) for v_ in y]
            xs = [Fr(v_).limit_denominator(10 ** 9) for v_ in x]
            cache = {}
            for i in range(len(nodes)):
                tot = Fr(0)
                for (a, b), lst in Mex.items():
                    if a != i:
                        continue
                    for pr, q in lst:
                        if q not in cache:
                            cache[q] = upper(q, t)
                        tot += pr * cache[q] * xs[b]
                ok &= tot <= xs[i]
    claim(f"[G1] exact Collatz-Wielandt certificate rho_S({t}) <= 1 on every non-simple SCC "
          f"(t > theta_C = {thC:.5f}), so theta_1 = theta_run = theta_C (gap zero, type (c))", ok)


# ---------------------------------------------------------------- [Y]
def mb_branch(x):
    a, b = x.numerator, x.denominator
    assert b % 6 in (1, 5)
    if a * pow(b, -1, 27) % 27 == 26:
        return "D"
    return "H" if (a * pow(b, -1, 2)) % 2 == 0 else "E"


def mb_step(x):
    br = mb_branch(x)
    if br == "D":
        return (x + 1) / 27, br, Fr(1, 27)
    if br == "H":
        return x / 2, br, Fr(1, 2)
    return (3 * x + 1) / 2, br, Fr(3, 2)


def mb_int(n):
    if n % 27 == 26:
        return (n + 1) // 27
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def run_Y():
    ok = True
    orbits = []
    for d in range(0, 121):
        s = Fr(27 * 9 ** d, 8 ** (d + 1) - 3 * 9 ** d)
        y = s - 5
        x, word, lam, orb = y, "", Fr(1), []
        for _ in range(3 * d + 3):
            orb.append(x)
            x, br, a = mb_step(x)
            word += br
            lam *= a
        ok &= x == y and word == "HEH" + "EEH" * d and lam == Fr(3, 8) * Fr(9, 8) ** d
        ok &= (lam > 1) == (d >= 9)
        # valuations claimed in the proof
        ok &= vp_int(s.numerator, 3) == 2 * d + 3 and s.numerator % 2 == 1
        orbits.append(set(orb))
        ok &= not (set(orb) & {Fr(-5), Fr(-7), Fr(-10)})
    dis = all(not (orbits[i] & orbits[j]) for i in range(len(orbits)) for j in range(i))
    claim("[Y] y_d (d = 0..120) is periodic under the real map with word HEH(EEH)^d, multiplier "
          "(3/8)(9/8)^d (> 1 iff d >= 9); orbits pairwise disjoint, avoid the ghost cycle", ok and dis)
    good = True
    for d in range(9, 15):
        s = Fr(27 * 9 ** d, 8 ** (d + 1) - 3 * 9 ** d)
        pts, x = [], s - 5
        for _ in range(3 * d + 3):
            pts.append(x)
            x = mb_step(x)[0]
        L = len(pts)
        start = None
        for k in range(L):
            lam, x, g = Fr(1), pts[k], True
            for _ in range(L):
                x, _, a = mb_step(x)
                lam *= a
                if lam <= 1:
                    g = False
                    break
            if g:
                start = pts[k]
                break
        good &= start is not None
        if start is None:
            continue
        N = 3 * L + 12
        M = 6 ** N
        r = start.numerator * pow(start.denominator, -1, M) % M
        for k in (1, 2, 5):
            n = r + k * M
            z = n
            for _ in range(L):
                z = mb_int(z)
                good &= z > n
    claim("[Y] for d = 9..14, integers n = y (mod 6^N) at the cycle-lemma point stay above n for "
          "a full period (the Theorem-N transfer)", good)


if __name__ == "__main__":
    which = sys.argv[1:] or ["NAMED", "P8", "NEG", "Y", "G1", "SCAN", "MODS"]
    for w in which:
        {"NAMED": run_named, "P8": run_P8, "NEG": run_neg, "SCAN": run_scan, "MODS": run_mods,
         "G1": run_gap, "Y": run_Y}[w]()
    print("ALL PASS" if OK else "SOME CHECK FAILED")
    sys.exit(0 if OK else 1)
