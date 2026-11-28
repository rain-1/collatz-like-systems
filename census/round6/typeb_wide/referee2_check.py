"""Referee 2, round 6 lens typeb_wide: independent check script, written from scratch.

Imports nothing from this folder (only round3/dichotomy/open_tables.py for the census
definitions of the open maps).  Reads the prover's data files only to compare with.
Exact arithmetic (ints / Fractions) wherever a claim is exact; floats only to *locate*
certificates that are then checked exactly, or where a separation bound computed here
makes a float sign decision exact.  Exit 0 iff every claim passes.

Sections
 [NAMED]  named type-(b) systems and open-map representatives: hypotheses, type (b) at
          level m, own Theorem-H cycle list, brute force over all n <= N.
 [P8]     Theorem P8: random (a, d) pairs; exact G_3 structure; cycles; brute force; the
          x* values quoted in the README.
 [Y]      Theorem Y: y_d periodic with word HEH (EEH)^d for d = 0..150, exact multiplier,
          pairwise disjoint orbits; rising integer progressions for d = 9..13.
 [ISO63]  S3 m = 6: own enumeration of the members with {62,63} an SCC; per-slice equality
          with the C scan (stronger than the total); every member: no other expanding
          simple-cycle SCC, ghost cycle -5,-7,-10 in a non-simple SCC.
 [SCAN]   random samples of SH3 m=4, SH5 m=4, C9 against the stored type-(b) index lists;
          full recounts B9 (all a), S5 m=5, SPL m=3 (d = 1, 3, 5: Prop. K).
 [MODS]   own menu; recount of one-class par_9_1@8, desc_split7_1@8, split5_3@16 and
          two-class perm_c@8; 60 random stored neighbours re-settled + brute force.
 [PREC]   own recomputation of the z3 completeness bound (SC = 2^22 and 4096).
 [M]      Proposition M (i) for p = 2, 3, 5 over all shapes; (iii) modulus-4 shapes with n/2.
 [G1]     exact Collatz-Wielandt certificate for the gap example, exact t > theta_C.
 [NEG]    3x+1, 3x-1, 5x+1, 7x+1, 3x+5: type (c) at levels 1..10 with exact expanding walks.
"""
import sys, os, json, math, random, itertools
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OK = True


def claim(name, cond, extra=""):
    global OK
    print(("PASS " if cond else "FAIL ") + name + (("  " + extra) if extra else ""), flush=True)
    OK = OK and bool(cond)


# ----------------------------------------------------------------------------- core
def ev(w, p):
    e = 0
    while w % p == 0:
        w //= p
        e += 1
    assert w == 1
    return e


def hyp(p, m, tab):
    """unit multipliers u >= 1, w = p^e (e <= m), exact on the class, T(Z>0) in Z>0"""
    Q = p ** m
    if len(tab) != Q:
        return False
    for r, (u, v, w) in enumerate(tab):
        if u < 1 or u % p == 0:
            return False
        ww = w
        while ww % p == 0:
            ww //= p
        if ww != 1 or w > Q:
            return False
        if (u * r + v) % w or (u * Q) % w:
            return False
        n0 = r if r else Q
        if u * n0 + v < w:          # least positive member; branch increasing (u >= 1)
            return False
    return True


def Tfun(p, m, tab):
    Q = p ** m

    def T(n):
        u, v, w = tab[n % Q]
        x = u * n + v
        assert x % w == 0
        return x // w
    return T


def cyl(p, m, tab, K):
    """G_K as list of (successors, u, e) per node"""
    Q, N = p ** m, p ** K
    G = []
    for r in range(N):
        u, v, w = tab[r % Q]
        e = ev(w, p)
        step = N // w
        b = ((u * r + v) // w) % step
        G.append(([b + i * step for i in range(w)], u, e))
    return G


def kosaraju(N, succ):
    order, seen = [], [False] * N
    for s in range(N):
        if seen[s]:
            continue
        seen[s] = True
        st = [(s, iter(succ[s]))]
        while st:
            v, it = st[-1]
            for w in it:
                if not seen[w]:
                    seen[w] = True
                    st.append((w, iter(succ[w])))
                    break
            else:
                st.pop()
                order.append(v)
    pred = [[] for _ in range(N)]
    for v in range(N):
        for w in succ[v]:
            pred[w].append(v)
    comp = [-1] * N
    c = 0
    for s in reversed(order):
        if comp[s] >= 0:
            continue
        comp[s] = c
        st = [s]
        while st:
            v = st.pop()
            for w in pred[v]:
                if comp[w] < 0:
                    comp[w] = c
                    st.append(w)
        c += 1
    return comp, c


def karp(nodes, ed):
    """float max cycle mean; ed list of (i, j, wt) local; returns (mu, D table, pred)"""
    n = len(nodes)
    NEG = -1e300
    D = [[NEG] * n for _ in range(n + 1)]
    P = [[-1] * n for _ in range(n + 1)]
    D[0] = [0.0] * n
    for k in range(1, n + 1):
        Dp, Dk, Pk = D[k - 1], D[k], P[k]
        for idx, (a, b, wt) in enumerate(ed):
            if Dp[a] > NEG / 2 and Dp[a] + wt > Dk[b]:
                Dk[b] = Dp[a] + wt
                Pk[b] = idx
    best, bv = NEG, -1
    for v in range(n):
        if D[n][v] <= NEG / 2:
            continue
        mv = min((D[n][v] - D[k][v]) / (n - k) for k in range(n) if D[k][v] > NEG / 2)
        if mv > best:
            best, bv = mv, v
    return best, D, P, bv


def exact_mult(p, edges_list):
    U, e = 1, 0
    for (_, _, u, ee) in edges_list:
        U *= u
        e += ee
    return U, e


def expanding_walk(p, nodes, ede, mu, P, bv):
    """exact expanding closed walk (list of local edge indices) or None"""
    n = len(nodes)
    # decompose the Karp path of length n ending at bv into cycles; test each exactly
    v, k, path = bv, n, []
    while k > 0:
        idx = P[k][v]
        if idx < 0:
            break
        path.append(idx)
        v = ede[idx][0]
        k -= 1
    path.reverse()                 # edges in forward order
    seq = [ede[i][0] for i in path]
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            if seq[i] == seq[j]:
                cyc = path[i:j]
                U, e = exact_mult(p, [ede[t] for t in cyc])
                if U > p ** e:
                    return cyc
    # fallback: Bellman-Ford with shifted weights
    for frac in (0.0, 0.25, 0.5, 0.75):
        sh = mu * frac
        dist, pred, last = [0.0] * n, [-1] * n, -1
        for _ in range(n + 1):
            last = -1
            for idx, (a, b, u, e) in enumerate(ede):
                wt = math.log(u) - e * math.log(p) - sh
                if dist[a] + wt > dist[b] + 1e-12:
                    dist[b] = dist[a] + wt
                    pred[b] = idx
                    last = b
            if last < 0:
                break
        if last < 0:
            continue
        x = last
        for _ in range(n):
            x = ede[pred[x]][0]
        cyc, y = [], x
        while True:
            cyc.append(pred[y])
            y = ede[pred[y]][0]
            if y == x:
                break
        U, e = exact_mult(p, [ede[i] for i in cyc])
        if U > p ** e:
            return cyc
    return None


def weights(p, nodes, ede, mu):
    """exact (theta, c) with c[j] u/p^e <= theta c[i] on all internal edges, or None"""
    n = len(nodes)
    for lt_f, ph_f in ((0.5, 0.75), (0.3, 0.6), (0.7, 0.85), (0.2, 0.5)):
        theta = Fr(math.exp(mu * lt_f)).limit_denominator(10 ** 7)
        if not (0 < theta < 1):
            continue
        lt2 = mu * ph_f
        phi = [0.0] * n
        for _ in range(n + 2):
            ch = False
            for (a, b, u, e) in ede:
                x = phi[a] + math.log(u) - e * math.log(p) - lt2
                if x > phi[b] + 1e-14:
                    phi[b] = x
                    ch = True
            if not ch:
                break
        mx = max(phi)
        c = [Fr(math.exp(mx - x)).limit_denominator(10 ** 10) for x in phi]
        if all(x > 0 for x in c) and all(c[b] * Fr(u, p ** e) <= theta * c[a]
                                         for (a, b, u, e) in ede):
            return theta, c
    return None


def classify(p, m, tab, K=None, need_weights=True, margin=None):
    """own SCC classification of G_K.  Returns (verdict, comps).  Each comp: dict.
    verdict: divfree / c / unknown / b / a.  Exactness: (b) and simple (a) exact products;
    (c) exact expanding walk; non-simple (a) exact weights (need_weights) or, for bulk counts,
    float Karp with |mu| > margin, margin a proved separation bound passed by the caller."""
    if K is None:
        K = m
    N = p ** K
    G = cyl(p, m, tab, K)
    comp, nc = kosaraju(N, [g[0] for g in G])
    members = [[] for _ in range(nc)]
    for v in range(N):
        members[comp[v]].append(v)
    out = []
    kinds = set()
    for ci in range(nc):
        nodes = members[ci]
        loc = {v: j for j, v in enumerate(nodes)}
        ede = [(loc[r], loc[s], G[r][1], G[r][2]) for r in nodes for s in G[r][0] if comp[s] == ci]
        if not ede:
            out.append(dict(kind="trivial", nodes=nodes))
            continue
        # division-free cycle?  Kahn on e = 0 internal edges
        z = [[] for _ in nodes]
        indeg = [0] * len(nodes)
        for (a, b, u, e) in ede:
            if e == 0:
                z[a].append(b)
                indeg[b] += 1
        q = [i for i in range(len(nodes)) if indeg[i] == 0]
        rem = len(nodes)
        while q:
            i = q.pop()
            rem -= 1
            for j in z[i]:
                indeg[j] -= 1
                if indeg[j] == 0:
                    q.append(j)
        if rem > 0:
            out.append(dict(kind="divfree", nodes=nodes))
            kinds.add("divfree")
            continue
        if len(ede) == len(nodes):
            nxt = {a: (b, u, e) for (a, b, u, e) in ede}
            seq, U, E, a = [0], 1, 0, 0
            while True:
                b, u, e = nxt[a]
                U *= u
                E += e
                if b == 0:
                    break
                seq.append(b)
                a = b
            if len(seq) != len(nodes):
                raise AssertionError("simple comp not a single cycle")
            k = "b" if U > p ** E else "a"
            out.append(dict(kind=k, nodes=nodes, simple=True, cycle=[nodes[j] for j in seq],
                            U=U, e=E))
            kinds.add(k)
            continue
        edf = [(a, b, math.log(u) - e * math.log(p)) for (a, b, u, e) in ede]
        mu, D, P, bv = karp(nodes, edf)
        if mu > 0:
            w = expanding_walk(p, nodes, ede, mu, P, bv)
            if w is not None:
                out.append(dict(kind="c", nodes=nodes, walk=[nodes[ede[i][0]] for i in w]))
                kinds.add("c")
                continue
            out.append(dict(kind="unknown", nodes=nodes))
            kinds.add("unknown")
            continue
        if not need_weights:
            if margin is not None and mu < -margin:
                out.append(dict(kind="a", nodes=nodes, simple=False))
                kinds.add("a")
            else:
                out.append(dict(kind="unknown", nodes=nodes))
                kinds.add("unknown")
            continue
        W = weights(p, nodes, ede, mu)
        if W is None:
            out.append(dict(kind="unknown", nodes=nodes))
            kinds.add("unknown")
            continue
        out.append(dict(kind="a", nodes=nodes, simple=False, theta=W[0],
                        c={nodes[j]: W[1][j] for j in range(len(nodes))}))
        kinds.add("a")
    for k in ("divfree", "c", "unknown", "b"):
        if k in kinds:
            return k, out
    return "a", out


def padic(x, p, K):
    return (x.numerator * pow(x.denominator, -1, p ** K)) % p ** K


def cycle_from(T, n, cap=10 ** 6):
    seen = set()
    y = n
    while y not in seen:
        seen.add(y)
        y = T(y)
        if len(seen) > cap:
            raise AssertionError("no cycle within cap")
    c = [y]
    z = T(y)
    while z != y:
        c.append(z)
        z = T(z)
    k = c.index(min(c))
    return c[k:] + c[:k]


def theorem_H_cycles(p, m, tab, K=None):
    """own Theorem-H cycle list (requires verdict a or b with exact weights)"""
    if K is None:
        K = m
    Q, PK = p ** m, p ** K
    v_, comps = classify(p, m, tab, K)
    if v_ not in ("a", "b"):
        return None, v_, comps
    T = Tfun(p, m, tab)
    G = cyl(p, m, tab, K)
    cycles = {}
    for c in comps:
        if c["kind"] == "trivial":
            continue
        if c.get("simple"):
            A, B = Fr(1), Fr(0)
            for r in c["cycle"]:
                u, v, w = tab[r % Q]
                A, B = A * Fr(u, w), (B * u + v) / w
            x = B / (1 - A)
            assert x.denominator % p != 0 and padic(x, p, K) == c["cycle"][0]
            y = x
            orbit = []
            for r in c["cycle"]:           # the whole periodic orbit follows the residues
                assert padic(y, p, K) == r
                orbit.append(y)
                u, v, w = tab[r % Q]
                y = (u * y + v) / w
            assert y == x
            c["xstar"] = x
            c["orbit"] = orbit
            if x.denominator == 1 and x > 0:
                cy = cycle_from(T, int(x))
                cycles[cy[0]] = cy
            continue
        th, cw = c["theta"], c["c"]
        ns = set(c["nodes"])
        beta = Fr(0)
        for r in ns:
            u, v, w = tab[r % Q]
            for s in G[r][0]:
                if s in ns:
                    beta = max(beta, cw[s] * Fr(max(v, 0), w))
        Vmax = beta / (1 - th)
        nmax = math.floor(Vmax / min(cw.values()))
        assert nmax <= 5 * 10 ** 6, nmax
        for n in range(1, nmax + 1):
            r = n % PK
            if r in ns and cw[r] * n <= Vmax:
                cy = cycle_from(T, n)
                cycles[cy[0]] = cy
    return [cycles[k] for k in sorted(cycles)], v_, comps


def brute(p, m, tab, N, cycles, cap=10 ** 5):
    """every n <= N reaches one of the listed cycles (exact integer iteration)"""
    T = Tfun(p, m, tab)
    pts = {x for c in cycles for x in c}
    done = set()
    for n0 in range(1, N + 1):
        n, steps = n0, 0
        path = []
        while n not in pts and n not in done:
            path.append(n)
            n = T(n)
            steps += 1
            if steps > cap:
                return False, n0
        done.update(x for x in path if x <= N)
    return True, None


# ----------------------------------------------------------------------------- [NAMED]
H2, H3 = (1, 0, 2), (1, 0, 3)


def even_half(m, odd, default=(3, 1, 1)):
    return [H2 if r % 2 == 0 else odd.get(r, default) for r in range(2 ** m)]


def lifted(base, Q2, mods):
    Q = len(base)
    t = [tuple(base[r % Q]) for r in range(Q2)]
    for r, b in mods.items():
        t[r] = b
    return t


def named():
    perm1932inv = [(3, 0, 2), (3, 1, 4), (3, 0, 2), (3, -1, 4)]
    permc = [(3, 0, 2), (3, 5, 4), (3, 0, 2), (3, -5, 4)]
    split53 = [(1, 0, 2), (5, 3, 1), (1, 0, 2), (1, 3, 1)]
    S = {
        # README section 2 / results table descriptions, transcribed by the referee
        "sh8": (2, 3, even_half(3, {1: (1, 1, 1), 5: (1, 5, 1)}), [1, 5], "-1", 10 ** 6),
        "sh4": (2, 2, [(1, 1, 1), (1, 1, 1), (1, 2, 2), (3, 1, 2)], [2, 4], "-1", 10 ** 6),
        "sh16": (2, 4, even_half(4, {5: (1, 5, 1), 9: (1, 1, 1), 13: (1, 7, 1)}), [1, 5], None, 10 ** 6),
        "sh32": (2, 5, even_half(5, {**{r: (1, 1, 1) for r in (1, 3, 9, 25)},
                                     **{r: (1, 5, 1) for r in (5, 15, 21, 29)},
                                     **{r: (1, 3, 1) for r in (7, 17, 23)},
                                     **{r: (1, 7, 1) for r in (11, 13, 19, 27)}}), [1, 5], "-1", 3 * 10 ** 5),
        "5x+1 relative": (2, 3, even_half(3, {1: (5, 1, 1), 5: (5, 1, 1), 3: (1, 3, 1), 7: (1, 7, 1)}),
                          [3, 7], "-1/3", 10 ** 6),
        "c9a": (3, 2, [H3, (5, 1, 1), (2, 1, 1), H3, (5, 1, 1), (1, 1, 1), H3, (4, 1, 1), (2, -1, 1)],
                [2], "-1/2", 10 ** 6),
        "c9b": (3, 2, [H3, (4, -1, 1), (2, 1, 1), H3, (4, 1, 1), (1, 1, 1), H3, (4, 1, 1), (2, -1, 1)],
                [1, 2], "1", 10 ** 6),
        "perm_1932inv rep": (2, 3, lifted(perm1932inv, 8, {2: (1, 2, 2), 6: (1, -4, 1)}), [1, 2], "0", 10 ** 6),
        "perm_c rep": (2, 3, lifted(permc, 8, {1: (1, 2, 1), 7: (1, -2, 1)}), [1, 5], "0", 10 ** 6),
        "split5_3 rep": (2, 3, lifted(split53, 8, {0: (1, 2, 2), 2: (1, 1, 1)}), [3, 7], "-5/3", 10 ** 6),
        "3x+1 + P8": (2, 3, [H2, (3, 1, 1), H2, (3, 1, 1), (1, 4, 1), (3, 1, 1), H2, (3, 1, 1)], [4], "-1", 10 ** 6),
        "3x-1 + P8": (2, 3, [H2, (3, -1, 1), H2, (3, -1, 1), (1, 4, 1), (3, -1, 1), H2, (3, -1, 1)], [1, 4], "1", 10 ** 6),
    }
    for name, (p, m, tab, mins, xs_expect, N) in S.items():
        h = hyp(p, m, tab)
        cyc, v_, comps = theorem_H_cycles(p, m, tab) if h else (None, None, None)
        got = [c[0] for c in cyc] if cyc else None
        bx = [[str(y) for y in c["orbit"]] for c in comps if c["kind"] == "b"] if cyc else []
        okx = xs_expect is None or any(xs_expect in o for o in bx)
        br, bad = brute(p, m, tab, N, cyc) if cyc else (False, None)
        claim(f"[NAMED] {name}: hypotheses {h}, verdict {v_}, cycle minima {got} (README {mins}), "
              f"isolated expanding x* {bx}, brute force n <= {N}",
              h and v_ == "b" and got == mins and okx and br, "" if br else f"bad start {bad}")
    # a few of the extra multiplier facts
    p, m, tab = 3, 2, S["c9b"][2]
    _, comps = classify(p, m, tab)
    b = [c for c in comps if c["kind"] == "b"]
    claim("[NAMED] c9b: the isolated expanding SCC is the positive cycle (1 3) with multiplier 4/3",
          len(b) == 1 and Fr(b[0]["U"], 3 ** b[0]["e"]) == Fr(4, 3) and sorted(b[0]["nodes"]) == [1, 3])


# ----------------------------------------------------------------------------- [P8]
def p8():
    rnd = random.Random(7)
    pairs = set()
    while len(pairs) < 150:
        a = rnd.randrange(3, 64, 2)
        d = rnd.randrange(1 - a, 120, 2) if (1 - a) % 2 else rnd.randrange(2 - a, 120, 2)
        if d % 2 and a + d >= 1:
            pairs.add((a, d))
    pairs |= {(3, 1), (3, -1), (3, 13), (5, 1), (5, 353), (7, 1), (7, 7), (9, 1), (3, -1), (5, -3), (7, -5), (9, -7)}
    bad = []
    for a, d in sorted(pairs):
        tab = [H2 if r % 2 == 0 else (a, d, 1) for r in range(8)]
        tab[4] = (1, 4, 1)
        if not hyp(2, 3, tab):
            bad.append((a, d, "hyp"))
            continue
        cyc, v_, comps = theorem_H_cycles(2, 3, tab)
        xs = Fr(-d, a - 2)
        exp = [[4, 8]]
        if xs.denominator == 1 and xs > 0:
            exp = sorted([[4, 8], [int(xs), 2 * int(xs)]])
        # exact structure: SCC {0,4} contracting; one simple expanding 2-cycle at x*, 2x*
        nt = [c for c in comps if c["kind"] != "trivial"]
        x8 = padic(xs, 2, 3)
        struct = (len(nt) == 2 and any(sorted(c["nodes"]) == [0, 4] and c["kind"] == "a" for c in nt)
                  and any(c["kind"] == "b" and sorted(c["nodes"]) == sorted([x8, (2 * x8) % 8])
                          and Fr(c["U"], 2 ** c["e"]) == Fr(a, 2) for c in nt))
        okb, _ = brute(2, 3, tab, 20000, cyc) if cyc else (False, 0)
        if not (v_ == "b" and cyc == exp and struct and okb):
            bad.append((a, d))
    claim(f"[P8] {len(pairs)} pairs (a, d), a <= 63, d >= 1 - a: type (b), G_3 = contracting {{0,4}} + "
          f"isolated 2-cycle (x*, 2x*) of multiplier a/2, cycles as predicted, brute force n <= 20000",
          not bad, str(bad[:5]))
    # the proof's key step, directly: an orbit that never meets M4 is the orbit of x*
    a, d = 3, 1
    tab = [H2 if r % 2 == 0 else (a, d, 1) for r in range(8)]
    tab[4] = (1, 4, 1)
    T = Tfun(2, 3, tab)
    okm = True
    for n in range(1, 50001):
        y, k = n, 0
        while y % 4 and k < 200:
            y = T(y)
            k += 1
        okm &= y % 4 == 0
    claim("[P8] 3x+1 + P8: every n <= 50000 enters M4 within 200 steps (x* = -1 not positive)", okm)
    # README: "keeps each one's expanding fixed point: -1, -1/3, -2/5 for 7x+1, -2/7 for 9x+1"
    fx = {a: Fr(-1, a - 2) for a in (3, 5, 7, 9)}
    print(f"   [P8] note: odd fixed points x* = -d/(a-2) for d = 1: { {a: str(x) for a, x in fx.items()} }; "
          f"-2/5 and -2/7 are the even points 2x* of the same 2-cycles")
    claim("[P8] 7x+1: x* = -1/5 and 2x* = -2/5 lie on the isolated 2-cycle (README quotes -2/5)",
          fx[7] == Fr(-1, 5) and 7 * fx[7] + 1 == Fr(-2, 5))


# ----------------------------------------------------------------------------- [Y]
def mb_step(x):
    """mb_s3_27 on rationals with denominators prime to 6; returns (letter, image, mult)"""
    a, b = x.numerator, x.denominator
    assert b % 2 and b % 3
    if (a * pow(b, -1, 27)) % 27 == 26:
        return "D", (x + 1) / 27, Fr(1, 27)
    if a % 2 == 0:
        return "H", x / 2, Fr(1, 2)
    return "E", (3 * x + 1) / 2, Fr(3, 2)


def mb_int(n):
    if n % 27 == 26:
        return (n + 1) // 27
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2


def thmY():
    ok = True
    orbits = []
    ghost = {Fr(-5), Fr(-7), Fr(-10)}
    for d in range(0, 151):
        y = Fr(27 * 9 ** d, 8 ** (d + 1) - 3 * 9 ** d) - 5
        word, x, mult, orb = "", y, Fr(1), []
        for _ in range(3 * d + 3):
            orb.append(x)
            l, x, q = mb_step(x)
            word += l
            mult *= q
        ok &= x == y and word == "HEH" + "EEH" * d and mult == Fr(9, 8) ** d * Fr(3, 8)
        ok &= (mult > 1) == (d >= 9)
        ok &= not (set(orb) & ghost)
        s = y + 5
        ok &= s.numerator % 2 == 1 and s.denominator % 2 == 1
        v3 = 0
        num = s.numerator
        while num % 3 == 0:
            num //= 3
            v3 += 1
        ok &= v3 == 2 * d + 3 and s.denominator % 3 != 0
        orbits.append(set(orb))
    disj = all(not (orbits[i] & orbits[j]) for i in range(len(orbits)) for j in range(i))
    claim("[Y] y_d periodic with word HEH(EEH)^d, multiplier (9/8)^d 3/8 (>1 iff d >= 9), v_2(s_d) = 0, "
          "v_3(s_d) = 2d+3, orbits avoid -5,-7,-10 and are pairwise disjoint, d = 0..150", ok and disj)
    # rising integer progressions
    okr = True
    for d in range(9, 14):
        y = Fr(27 * 9 ** d, 8 ** (d + 1) - 3 * 9 ** d) - 5
        orb, ms, x = [], [], y
        L = 3 * d + 3
        for _ in range(L):
            orb.append(x)
            l, x, q = mb_step(x)
            ms.append(q)
        # cycle lemma: rotation with all partial products > 1
        j0 = None
        for j in range(L):
            pr, good = Fr(1), True
            for k in range(L):
                pr *= ms[(j + k) % L]
                if pr <= 1:
                    good = False
                    break
            if good:
                j0 = j
                break
        okr &= j0 is not None
        z = orb[j0]
        Nn = 6 ** (4 * L + 10)
        n = (z.numerator * pow(z.denominator, -1, Nn)) % Nn + Nn
        n0, cur, rising = n, n, True
        for k in range(L):
            cur = mb_int(cur)
            rising &= cur > n0
        okr &= rising
    claim("[Y] integers n = y_d (mod 6^N) stay above n for a whole period, d = 9..13 (cycle-lemma point)", okr)


# ----------------------------------------------------------------------------- [ISO63]
def iso63():
    Q, Hh = 64, 32

    def sc(r, Sset):
        if r % 2 == 0:
            return [r // 2, r // 2 + Hh]
        return [(3 * r + 1) % Q] if r in Sset else [(r + 1) % Q]

    # own enumeration: worklist of (forced-in, forced-out, closure, frontier)
    configs = []

    def explore(inS, outS, closure, frontier):
        frontier = list(frontier)
        closure = set(closure)
        while frontier:
            r = frontier.pop()
            if r % 2 == 1 and r not in inS and r not in outS:
                explore(inS | {r}, outS, closure, frontier + [r])
                explore(inS, outS | {r}, closure, frontier + [r])
                return
            nxt = sc(r, inS)
            for q in nxt:
                if q in (62, 63):
                    return
                if q not in closure:
                    closure.add(q)
                    frontier.append(q)
        configs.append((inS, outS))

    explore(frozenset({63}), frozenset(), {31}, [31])
    odd = list(range(1, 64, 2))
    members = []
    for inS, outS in configs:
        free = [r for r in odd if r not in inS and r not in outS]
        for bits in range(2 ** len(free)):
            members.append(frozenset(inS | {free[i] for i in range(len(free)) if bits >> i & 1}))
    distinct = len(set(members))

    def mask(Sset):
        return sum(1 << ((r - 1) // 2) for r in Sset)

    per_slice = {}
    for Sset in members:
        sl = mask(Sset) >> 20
        per_slice[sl] = per_slice.get(sl, 0) + 1
    import glob, re
    nb = {}
    for f in glob.glob(os.path.join(HERE, "out", "brute", "a3_m6_*.txt")):
        mm = re.search(r"DONE a=3 d=1 m=6 slice=(\d+)/4096 nb=(\d+) nH=(\d+) nunc=(\d+)", open(f).read())
        if mm:
            nb[int(mm.group(1))] = (int(mm.group(2)), int(mm.group(3)), int(mm.group(4)))
    slices_ok = len(nb) == 4096 and all(nb[s][0] == per_slice.get(s, 0) for s in range(4096))
    nH = sum(v[1] for v in nb.values()) + sum(v[2] for v in nb.values())
    claim(f"[ISO63] own enumeration: {len(configs)} configurations, {len(members)} members "
          f"({distinct} distinct) with {{62,63}} an SCC; equals C-scan nb slice by slice (4096 slices); "
          f"C-scan nH + nunc = {nH}",
          len(members) == distinct == 34560 and slices_ok and nH == 0)
    # every member: no other expanding simple SCC; ghost residue cycle in a non-simple SCC
    ghost = [59, 50, 57, 44, 54]
    badc = 0
    for Sset in members:
        succ = [sc(r, Sset) for r in range(Q)]
        comp, nc = kosaraju(Q, succ)
        size = [0] * nc
        ned = [0] * nc
        A = [0] * nc
        B = [0] * nc
        for r in range(Q):
            size[comp[r]] += 1
            for s in succ[r]:
                if comp[s] == comp[r]:
                    ned[comp[r]] += 1
                    if r % 2:
                        A[comp[r]] += r in Sset
                    else:
                        B[comp[r]] += 1
        iso = [c for c in range(nc) if ned[c] == size[c] > 0 and 3 ** A[c] > 2 ** B[c]]
        isonodes = sorted(r for r in range(Q) if comp[r] in iso)
        g = comp[59]
        good = (isonodes == [62, 63] and 59 in Sset and 57 in Sset
                and all(comp[x] == g for x in ghost) and ned[g] > size[g])
        badc += not good
    claim("[ISO63] all 34,560 members: {62,63} is the only expanding simple-cycle SCC; the ghost "
          "cycle 59,50,57,44,54 (exact multiplier 9/8) lies in one non-simple SCC (type (c), no "
          "division-free cycles in S3)", badc == 0, f"bad {badc}")
    # random members through the full classifier (exact (c) walk)
    rnd = random.Random(11)
    okf = True
    for Sset in rnd.sample(members, 60):
        tab = [H2 if r % 2 == 0 else ((3, 1, 1) if r in Sset else (1, 1, 1)) for r in range(Q)]
        v_, comps = classify(2, 6, tab)
        bs = [c for c in comps if c["kind"] == "b"]
        okf &= v_ == "c" and len(bs) == 1 and sorted(bs[0]["nodes"]) == [62, 63]
    claim("[ISO63] 60 random members through the full exact classifier: verdict (c), unique (b) SCC {62,63}", okf)


# ----------------------------------------------------------------------------- [SCAN]
def table_at(opts, idx):
    t = []
    for o in opts:
        t.append(o[idx % len(o)])
        idx //= len(o)
    return t


def sep_margin(p, mults, maxlen, maxdiv):
    """min |A log u... | over nonzero count vectors, a lower bound for |cycle log multiplier|;
    returned divided by maxlen as a bound on |cycle mean| (mults: list of u, divisions <= maxdiv)"""
    best = float("inf")
    for counts in itertools.product(*[range(maxlen + 1) for _ in mults]):
        if sum(counts) > maxlen:
            continue
        for e in range(0, maxdiv + 1):
            if sum(counts) == 0 and e == 0:
                continue
            U = 1
            for u, c in zip(mults, counts):
                U *= u ** c
            if U == p ** e:
                continue
            best = min(best, abs(sum(c * math.log(u) for u, c in zip(mults, counts)) - e * math.log(p)))
    return best / maxlen


def scans():
    rnd = random.Random(5)
    HALF = (1, 0, 2)
    fam = {
        "SH3_m4": (2, 4, [[HALF] if r % 2 == 0 else [(3, 1, 1)] + [(1, d, 1) for d in (1, 3, 5, 7)] for r in range(16)]),
        "SH5_m4": (2, 4, [[HALF] if r % 2 == 0 else [(5, 1, 1)] + [(1, d, 1) for d in (1, 3, 5, 7)] for r in range(16)]),
        "C9": (3, 2, [[H3] if r % 3 == 0 else [(1, 1, 1), (1, 2, 1), (2, 1, 1), (2, -1, 1), (4, 1, 1), (4, -1, 1),
                                                (5, 1, 1), (5, -1, 1)] for r in range(9)]),
    }
    for name, (p, m, opts) in fam.items():
        st = json.load(open(os.path.join(HERE, "data", f"scan_{name}.json")))
        tb = set(st["typeb_indices"])
        total = 1
        for o in opts:
            total *= len(o)
        sample = set(rnd.sample(sorted(tb), min(60, len(tb)))) | set(rnd.randrange(total) for _ in range(1500))
        bad = 0
        cnt = {}
        for idx in sample:
            tab = table_at(opts, idx)
            if not hyp(p, m, tab):
                bad += 1
                continue
            v_, comps = classify(p, m, tab)
            cnt[v_] = cnt.get(v_, 0) + 1
            if (v_ == "b") != (idx in tb):
                bad += 1
            if v_ == "b" and idx in tb and rnd.random() < 0.3:
                cyc, _, _ = theorem_H_cycles(p, m, tab)
                okb, _ = brute(p, m, tab, 20000, cyc)
                bad += not okb
        claim(f"[SCAN] {name}: {len(sample)} sampled members ({len(tb & sample)} stored type (b)), own verdict "
              f"(b) iff index in stored list; sampled (b) settled + brute force", bad == 0 and "unknown" not in cnt,
              str(cnt))
    # full recounts
    for a in (2, 4, 5, 7, 8, 10, 11, 13):
        opts = [[H3] if r % 3 == 0 else [(1, 1, 1), (a, 1, 1)] for r in range(9)]
        cnt = {}
        for idx in range(64):
            v_, _ = classify(3, 2, table_at(opts, idx))
            cnt[v_] = cnt.get(v_, 0) + 1
        st = json.load(open(os.path.join(HERE, "data", f"scan_B9_a{a}.json")))["counts"]
        claim(f"[SCAN] B9_a{a} full recount {cnt} = stored {st}", cnt == st)
    # S5 m = 5 full recount with float Karp and a proved separation margin
    mg = sep_margin(2, [5], 16, 16)        # simple cycle of G_5: <= 16 odd steps, <= 16 halvings
    opts = [[HALF] if r % 2 == 0 else [(1, 1, 1), (5, 1, 1)] for r in range(32)]
    cnt = {}
    for idx in range(2 ** 16):
        v_, _ = classify(2, 5, table_at(opts, idx), need_weights=False, margin=mg / 2)
        cnt[v_] = cnt.get(v_, 0) + 1
    st = json.load(open(os.path.join(HERE, "data", "scan_S5_m5.json")))["counts"]
    claim(f"[SCAN] S5_m5 full recount {cnt} = stored {st} (cycle-mean separation {mg:.2e} >> float error)",
          cnt == st)
    # SPL m = 3, d = 1, 3, 5: identical type counts (Prop. K) and = stored
    res = {}
    for d in (1, 3, 5):
        opts = [[HALF] if r % 2 == 0 else [(u, d, 1) for u in (1, 3, 5)] for r in range(8)]
        cnt = {}
        for idx in range(3 ** 4):
            v_, _ = classify(2, 3, table_at(opts, idx))
            cnt[v_] = cnt.get(v_, 0) + 1
        res[d] = cnt
        st = json.load(open(os.path.join(HERE, "data", f"scan_SPL_d{d}_m3.json")))["counts"]
        claim(f"[SCAN] SPL_d{d}_m3 recount {cnt} = stored {st}", cnt == st)
    claim("[SCAN] Prop. K: SPL_d1, d3, d5 rows identical at m = 3", res[1] == res[3] == res[5])
    # the conjugacy itself: x -> d x maps member tables of d=1 to d=3 with identical G_3 edge multisets
    okk = True
    for idx in range(81):
        o1 = [[HALF] if r % 2 == 0 else [(u, 1, 1) for u in (1, 3, 5)] for r in range(8)]
        t1 = table_at(o1, idx)
        for d in (3, 5):
            td = [None] * 8
            for r in range(8):
                u, v, w = t1[r]
                td[(d * r) % 8] = (u, d * v, w)
            G1, Gd = cyl(2, 3, t1, 3), cyl(2, 3, td, 3)
            for r in range(8):
                okk &= sorted((d * s) % 8 for s in G1[r][0]) == sorted(Gd[(d * r) % 8][0])
                okk &= (G1[r][1], G1[r][2]) == (Gd[(d * r) % 8][1], Gd[(d * r) % 8][2])
    claim("[SCAN] Prop. K: x -> d x is a graph isomorphism G_3(d=1 member) -> G_3(d member), d = 3, 5", okk)


# ----------------------------------------------------------------------------- [MODS]
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
            seen = set()
            X = w2 * M + 2 * Q2
            for v2 in sorted(range(-X, X + 1), key=abs):
                if (u2 * r + v2) % w2:
                    continue
                t = ((u2 * r + v2) // w2) % M
                if t in seen:
                    continue
                n0 = r if r else Q2
                if u2 * n0 + v2 < w2:
                    continue
                seen.add(t)
                if (u2, v2, w2) != tuple(br):
                    out.append((u2, v2, w2))
                if len(seen) == M:
                    break
    return out


def mods():
    sys.path.insert(0, os.path.join(HERE, "..", "..", "round3", "dichotomy"))
    from open_tables import OPEN
    one = json.load(open(os.path.join(HERE, "data", "mods_ONE_81.json")))
    two = json.load(open(os.path.join(HERE, "data", "mods_TWO_9.json")))
    byprefix = {k.split(" ")[0]: v for k, v in OPEN.items()}

    def recount(name, Q2, mode):
        Q, base = byprefix[name]
        p = 2 if Q % 2 == 0 else 3
        m = round(math.log(Q2, p))
        bl = [tuple(base[r % Q]) for r in range(Q2)]
        menus = [menu(p, Q2, r, bl[r]) for r in range(Q2)]
        cnt = {}
        if mode == "ONE":
            tasks = [((r, b),) for r in range(Q2) for b in menus[r]]
        else:
            tasks = [((r1, b1), (r2, b2)) for r1, r2 in itertools.combinations(range(Q2), 2)
                     for b1 in menus[r1] for b2 in menus[r2]]
        for t in tasks:
            tab = list(bl)
            for r, b in t:
                tab[r] = b
            if not hyp(p, m, tab):
                v_ = "inadmissible"
            else:
                v_, _ = classify(p, m, tab)
            cnt[v_] = cnt.get(v_, 0) + 1
        return cnt

    for name, Q2, mode in (("par_9_1", 8, "ONE"), ("desc_split7_1", 8, "ONE"), ("split5_3", 16, "ONE"),
                           ("perm_1932inv", 32, "ONE"), ("perm_c", 8, "TWO")):
        cnt = recount(name, Q2, mode)
        D = one if mode == "ONE" else two
        key = [k for k in D if k.startswith(name + " ") and k.endswith(f"@{Q2}")]
        st = D[key[0]]["counts"] if key else None
        claim(f"[MODS] {mode} {name}@{Q2}: own recount {cnt} = stored {st}", cnt == st)
    # random stored neighbours re-settled
    rnd = random.Random(3)
    allb = [(k, rec) for D in (one, two) for k, v in D.items() for rec in v["typeb"]]
    bad = []
    for k, rec in rnd.sample(allb, 60):
        name, Q2 = k.split(" ")[0], int(k.split("@")[1])
        Q, base = byprefix[name]
        p = 2 if Q % 2 == 0 else 3
        m = round(math.log(Q2, p))
        bl = [tuple(base[r % Q]) for r in range(Q2)]
        tab = list(bl)
        menu_ok = True
        for r, b in rec["mods"]:
            b = tuple(b)
            menu_ok &= b in menu(p, Q2, r, bl[r])
            tab[r] = b
        menu_ok &= [tuple(x) for x in rec["proof"]["table"]] == tab
        h = hyp(p, m, tab)
        cyc, v_, comps = theorem_H_cycles(p, m, tab)
        okb, _ = brute(p, m, tab, 100000, cyc) if cyc else (False, 0)
        if not (menu_ok and h and v_ == "b" and [c[0] for c in cyc] == rec["cycles"] and okb):
            bad.append(k)
    claim("[MODS] 60 random stored type-(b) neighbours: in the menu, hypotheses hold, own verdict (b), "
          "own Theorem-H cycle list = stored, brute force n <= 10^5", not bad, str(bad[:3]))
    tot1 = sum(sum(v["counts"].values()) for v in one.values())
    tot2 = sum(sum(v["counts"].values()) for v in two.values())
    nb = sum(len(v["typeb"]) for D in (one, two) for v in D.values())
    claim(f"[MODS] table totals one-class {tot1}, two-class {tot2}, stored neighbours {nb} "
          f"(README 304,296 / 530,668 / 1,974)", (tot1, tot2, nb) == (304296, 530668, 1974))


# ----------------------------------------------------------------------------- [PREC]
def prec():
    HALF = (1, 0, 2)

    def sfam(m, a):
        return 2, m, [[HALF] if r % 2 == 0 else [(1, 1, 1), (a, 1, 1)] for r in range(2 ** m)]

    def dfam(Q):
        out = []
        for r in range(Q):
            if r % 3 == 0:
                out.append([H3])
                continue
            o = []
            for u in (2, 4, 5):
                for v in (1, 2, -1, -2, 4, 5, 7):
                    if (u * r + v) % 3 == 0:
                        o.append((u, v, 3))
                        break
            out.append(o)
        return 3, 3, out

    rows = {"S3_m7": sfam(7, 3), "S3_m8": sfam(8, 3), "S5_m7": sfam(7, 5), "S7_m6": sfam(6, 7),
            "SPL_d1_m5": (2, 5, [[HALF] if r % 2 == 0 else [(u, 1, 1) for u in (1, 3, 5)] for r in range(32)]),
            "D27": dfam(27)}

    def bound(p, m, opts, SC, oddeven):
        Q = p ** m
        types = sorted({(u, w) for o in opts for (u, v, w) in o})
        k = len(types)
        offers = [{types.index((u, w)) for (u, v, w) in o} for o in opts]
        subsets = []
        for mask in range(1, 2 ** k):
            Tset = {i for i in range(k) if mask >> i & 1}
            subsets.append((Tset, sum(1 for of in offers if of & Tset)))
        lq = [math.log2(u) - math.log2(w) for (u, w) in types]     # the encoder's expression
        cw = [math.ceil(SC * x) + 1 for x in lq]
        fw = [math.floor(SC * x) for x in lq]
        nd = [i for i, (u, w) in enumerate(types) if w == 1]
        hv = [i for i, (u, w) in enumerate(types) if w == 2]
        worst_c, worst_e = -10 ** 18, 10 ** 18
        for vec in itertools.product(*[range(Q + 1) for _ in range(k)]):
            if sum(vec) == 0 or sum(vec) > Q:
                continue
            if any(sum(vec[i] for i in Ts) > c for Ts, c in subsets):
                continue
            if oddeven and sum(vec[i] for i in nd) > sum(vec[i] for i in hv):
                continue
            num = den = 1
            for (u, w), n in zip(types, vec):
                num *= u ** n
                den *= w ** n
            if num < den:
                worst_c = max(worst_c, sum(c * n for c, n in zip(cw, vec)))
            elif num > den:
                worst_e = min(worst_e, sum(f * n for f, n in zip(fw, vec)))
        return worst_c <= 0 and worst_e >= 1, worst_c, worst_e

    res4096 = set()
    for name, (p, m, opts) in rows.items():
        oe = p == 2
        ok, wc, we = bound(p, m, opts, 2 ** 22, oe)
        claim(f"[PREC] {name}: z3 encoding complete at SC = 2^22 (max contracting slack {wc}, "
              f"min expanding slack {we})", ok)
        ok4, _, _ = bound(p, m, opts, 4096, oe)
        if not ok4:
            res4096.add(name)
    claim(f"[PREC] at SC = 4096 incomplete rows: {sorted(res4096)} (REFEREE1: S3_m8, D27)",
          res4096 == {"S3_m8", "D27"})


# ----------------------------------------------------------------------------- [M]
def propM():
    okall = True
    for p in (2, 3, 5):
        # shape per class: ('f', target) division-free single successor, or ('d',) all successors
        opts = [("f", t) for t in range(p)] + [("d",)]
        for shape in itertools.product(opts, repeat=p):
            succ = [[s[1]] if s[0] == "f" else list(range(p)) for s in shape]
            comp, nc = kosaraju(p, succ)
            # division-free cycle: functional graph on 'f' nodes
            divfree = False
            for r in range(p):
                seen, x = set(), r
                while shape[x][0] == "f" and x not in seen:
                    seen.add(x)
                    x = shape[x][1]
                if shape[x][0] == "f" and x in seen:
                    divfree = True
            simple_div = False
            for c in range(nc):
                ns = [r for r in range(p) if comp[r] == c]
                ned = sum(1 for r in ns for s in succ[r] if comp[s] == c)
                if ned == len(ns) and any(shape[r][0] == "d" for r in ns):
                    simple_div = True
            if simple_div and not divfree:
                okall = False
    claim("[M] Prop. M (i): no shape at modulus p in {2, 3, 5} has a simple-cycle SCC with a division "
          "and no division-free cycle", okall)
    # (iii) modulus 4 with n/2 on both even classes: odd class shapes (e, target set)
    def shapes_odd():
        out = [((0,), (t,)) for t in range(4)]
        out += [((1,), (t, t + 2)) for t in range(2)]
        out += [((2,), (0, 1, 2, 3))]
        return out
    cnt = 0
    for s1 in shapes_odd():
        for s3 in shapes_odd():
            succ = {0: [0, 2], 2: [1, 3], 1: list(s1[1]), 3: list(s3[1])}
            e = {0: 1, 2: 1, 1: s1[0][0], 3: s3[0][0]}
            sl = [succ[r] for r in range(4)]
            comp, nc = kosaraju(4, sl)
            # division-free cycle?
            divfree = False
            for r in range(4):
                x, seen = r, set()
                while e[x] == 0 and x not in seen:
                    seen.add(x)
                    x = succ[x][0]
                if e[x] == 0 and x in seen:
                    divfree = True
            adm = False
            for c in range(nc):
                ns = [r for r in range(4) if comp[r] == c]
                ned = sum(1 for r in ns for s in sl[r] if comp[s] == c)
                if ned == len(ns) and any(e[r] > 0 for r in ns) and any(r % 2 for r in ns):
                    adm = True
            cnt += adm and not divfree
    claim("[M] Prop. M (iii): 0 of the 49 modulus-4 shapes with n/2 on even classes admit type (b)", cnt == 0)


# ----------------------------------------------------------------------------- [G1]
def g1():
    S = {3, 7, 15, 23, 31, 35, 39, 41, 47, 51, 55, 57, 59, 63}
    tab = [H2 if r % 2 == 0 else ((3, 1, 1) if r in S else (1, 1, 1)) for r in range(64)]
    v_, comps = classify(2, 6, tab)
    kinds = sorted((c["kind"], len(c["nodes"])) for c in comps if c["kind"] != "trivial")
    bs = [c for c in comps if c["kind"] == "b"]
    t = Fr(665, 389)
    # t > theta_C = log 2 / log(3/2)  <=>  2 < (3/2)^t  <=>  2^(389+665) < 3^665
    tgt = 2 ** (389 + 665) < 3 ** 665
    # M_t entries: odd 3n+1: 3^t; odd n+1: 1; even: (1/2)(1/2)^t.  Rational upper bounds:
    def up(q):      # U >= q^t, exact check U^389 >= q^665
        U = Fr(float(q) ** float(t) * (1 + 1e-9)).limit_denominator(10 ** 12)
        while U ** 389 < q ** 665:
            U *= Fr(1000001, 1000000)
        return U
    U3, Uh = up(Fr(3)), up(Fr(1, 2))
    G = cyl(2, 6, tab, 6)
    okcert = True
    for c in comps:
        if c["kind"] in ("a", "c") and not c.get("simple"):
            ns = c["nodes"]
            idx = {v: i for i, v in enumerate(ns)}
            n = len(ns)

            def ent(r):
                u, v, w = tab[r % 64]
                if w == 2:
                    return Fr(1, 2) * Uh
                return U3 if u == 3 else Fr(1)
            # Perron vector by float power iteration on the upper matrix, then exact test
            x = [1.0] * n
            for _ in range(3000):
                y = [sum(float(ent(r)) * x[idx[s]] for s in G[r][0] if s in idx) for r in ns]
                mx = max(y)
                x = [v / mx for v in y]
            xs = [Fr(max(v, 1e-6)).limit_denominator(10 ** 9) for v in x]
            for r in ns:
                tot = sum((ent(r) * xs[idx[s]] for s in G[r][0] if s in idx), Fr(0))
                okcert &= tot <= xs[idx[r]]
    claim(f"[G1] S-family member: verdict {v_}, non-trivial SCCs {kinds}, unique (b) SCC {{62,63}}; "
          f"t = 665/389 > theta_C exactly; exact Collatz-Wielandt M^up_t x <= x on every non-simple SCC",
          v_ == "c" and len(bs) == 1 and sorted(bs[0]["nodes"]) == [62, 63] and tgt and okcert
          and ("c", 34) in kinds)


# ----------------------------------------------------------------------------- [NEG]
def neg():
    ok = True
    for nm, tab in (("3x+1", [H2, (3, 1, 1)]), ("3x-1", [H2, (3, -1, 1)]), ("5x+1", [H2, (5, 1, 1)]),
                    ("7x+1", [H2, (7, 1, 1)]), ("3x+5", [H2, (3, 5, 1)])):
        for K in range(1, 11):
            v_, _ = classify(2, 1, tab, K)
            ok &= v_ == "c"
    claim("[NEG] 3x+1, 3x-1, 5x+1, 7x+1, 3x+5: type (c) at levels 1..10 (exact expanding walks)", ok)


if __name__ == "__main__":
    only = sys.argv[1:]
    for sec, f in (("NAMED", named), ("P8", p8), ("Y", thmY), ("M", propM), ("NEG", neg), ("G1", g1),
                   ("PREC", prec), ("ISO63", iso63), ("MODS", mods), ("SCAN", scans)):
        if not only or sec in only:
            f()
    print("ALL PASS" if OK else "SOME CHECK FAILED")
    sys.exit(0 if OK else 1)
