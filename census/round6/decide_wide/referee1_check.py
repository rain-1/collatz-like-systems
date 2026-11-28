#!/usr/bin/env python3
"""referee1_check.py -- independent referee check for round6/decide_wide (Referee 1).

Written from scratch; it does not import twlib.py, famscan or check_*.py.  It imports
round3/dichotomy/decide.py only for the k* cross-check of one system (marked).  Exact
arithmetic (integers / Fractions) for every verdict; floats are used only to *search* for a
cycle or a potential, and every float result is re-verified exactly.  Exits 1 on any failure.

Sections
  A  Theorem B(i), B(ii): graph types at several levels + brute force of every n <= N
  B  the Q = 12 mixed type-(b) example and every mixed example in out/typeb_mixed_examples.txt
  C  Proposition P (all successor patterns, p = 2, 3, 5; random p = 7, 11)
  D  Proposition 4 (all patterns at Q = 4; types at 8, 16, 32 for unit multipliers)
  E  Lemma S and Theorem S (patterns, squarefree Q)
  F  Theorem C6: own simple-cycle enumeration vs out/classify6.md; corollaries
  G  "div23 with 5n +- 1" and the 5n+5 variant: certificate + brute force
  H  open census table maps: exact type-(c) witnesses at the base level (and lifts)
  I  falsification: 3x+1, 3x-1, 5x+1 must not be settled; wrong cycle lists must fail
  J  random sample of famscan output (CERT, B, and unlisted = C/Z members of exhaustive files)
  K  random sample of out/typeb_list.jsonl, brute force cycle lists
  L  random sample of re-settled catalog verdicts, brute force cycle lists
"""
import gzip
import json
import math
import os
import random
import sys
from fractions import Fraction
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FAILS = []
rng = random.Random(20261128)
QUICK = "quick" in sys.argv


def fail(msg):
    print("FAIL:", msg, flush=True)
    FAILS.append(msg)


def ok(cond, msg):
    if not cond:
        fail(msg)
    return cond


# ------------------------------------------------------------------ own graph machinery
def check_integral(Q, tab):
    for r, (u, v, w) in enumerate(tab):
        assert u >= 1 and w >= 1 and (u * r + v) % w == 0 and (u * Q) % w == 0, (Q, r)


def succ_level(Q, tab, K):
    """Out-edges of r mod K: T(r + K t) = (u r + v)/w + (u K / w) t."""
    S = []
    for r in range(K):
        u, v, w = tab[r % Q]
        y0 = (u * r + v) // w
        k = u * K // w
        g = math.gcd(k, K)
        S.append(sorted({(y0 + g * j) % K for j in range(K // g)}))
    return S


def sccs(N, succ):
    """Kosaraju, iterative."""
    seen = [False] * N
    order = []
    for s in range(N):
        if seen[s]:
            continue
        stack = [(s, iter(succ[s]))]
        seen[s] = True
        while stack:
            v, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                stack.pop()
                order.append(v)
            elif not seen[nxt]:
                seen[nxt] = True
                stack.append((nxt, iter(succ[nxt])))
    pred = [[] for _ in range(N)]
    for v in range(N):
        for s in succ[v]:
            pred[s].append(v)
    comp = [-1] * N
    out = []
    for v in reversed(order):
        if comp[v] >= 0:
            continue
        c = len(out)
        comp[v] = c
        members, st = [v], [v]
        while st:
            x = st.pop()
            for y in pred[x]:
                if comp[y] < 0:
                    comp[y] = c
                    members.append(y)
                    st.append(y)
        out.append(members)
    return out


def UW(Q, tab, cyc):
    U = W = 1
    for r in cyc:
        u, v, w = tab[r % Q]
        U *= u
        W *= w
    return U, W


def is_closed(succ, cyc):
    return all(cyc[(i + 1) % len(cyc)] in succ[cyc[i]] for i in range(len(cyc)))


def max_mean_cycle(nodes, E, wt):
    """Karp (floats): a closed walk of (approximately) maximal mean weight, as node list."""
    idx = {r: i for i, r in enumerate(nodes)}
    n = len(nodes)
    NEG = float("-inf")
    D = [[NEG] * n for _ in range(n + 1)]
    P = [[-1] * n for _ in range(n + 1)]
    for i in range(n):
        D[0][i] = 0.0
    for k in range(1, n + 1):
        Dk, Dp, Pk = D[k], D[k - 1], P[k]
        for i, r in enumerate(nodes):
            x = Dp[i]
            if x == NEG:
                continue
            x += wt[r]
            for s in E[r]:
                j = idx[s]
                if x > Dk[j]:
                    Dk[j] = x
                    Pk[j] = i
    best, bv = NEG, -1
    for v in range(n):
        if D[n][v] == NEG:
            continue
        m = min((D[n][v] - D[k][v]) / (n - k) for k in range(n) if D[k][v] != NEG)
        if m > best:
            best, bv = m, v
    walk, v = [], bv
    for k in range(n, -1, -1):
        walk.append(v)
        v = P[k][v] if k else v
    walk.reverse()
    pos = {}
    for i, x in enumerate(walk):
        if x in pos:
            return best, [nodes[y] for y in walk[pos[x]:i]]
        pos[x] = i
    return best, None


def exact_potential(Q, tab, nodes, E):
    """Lemma-4 style exact potential on an SCC: positive Fractions c with
    c(s) u < c(r) w on every internal edge.  Returns (c, theta) or None."""
    if len(nodes) > 400:
        return None
    for gnum, gden in ((11, 10), (101, 100), (1001, 1000), (10001, 10000)):
        gam = Fraction(gnum, gden)
        m = {r: gam * Fraction(tab[r % Q][0], tab[r % Q][2]) for r in nodes}
        g = {r: Fraction(1) for r in nodes}
        conv = False
        for _ in range(len(nodes) + 2):
            ch = False
            for r in nodes:
                b = max(g[s] for s in E[r]) * m[r]
                if b > g[r]:
                    g[r] = b
                    ch = True
            if not ch:
                conv = True
                break
        if not conv:
            continue
        th = Fraction(0)
        for r in nodes:
            u, v, w = tab[r % Q]
            for s in E[r]:
                q = g[s] * u / (g[r] * w)
                if q >= 1:
                    return None
                th = max(th, q)
        return g, th
    return None


def classify(Q, tab, K, want_potential=True):
    """Exact SCC types of G_K.  Returns list of dicts {type, nodes, cycle, U, W, ...}.
    'z' division-free cycle; 'b' single simple cycle U > W; 'n' single simple cycle U = W;
    'a' contracting (exact potential, or single cycle U < W); 'c' expanding cycle (exact)
    and not a single cycle; 'u' undecided (raise in callers)."""
    succ = succ_level(Q, tab, K)
    res = []
    for comp in sccs(K, succ):
        S = set(comp)
        E = {r: [s for s in succ[r] if s in S] for r in comp}
        ne = sum(len(x) for x in E.values())
        if ne == 0:
            continue
        rec = dict(nodes=sorted(comp))
        # division-free cycle
        zc = None
        for r0 in comp:
            path, pos, r = [], {}, r0
            while tab[r % Q][2] == 1 and r not in pos:
                pos[r] = len(path)
                path.append(r)
                r = succ[r][0]          # w = 1: single successor
                if r not in S:
                    break
            if r in pos and r in S:
                zc = path[pos[r]:]
                break
        if zc is not None:
            assert all(tab[x % Q][2] == 1 for x in zc) and is_closed(succ, zc)
            rec.update(type="z", cycle=zc)
            res.append(rec)
            continue
        if ne == len(comp):
            cyc, r = [comp[0]], E[comp[0]][0]
            while r != comp[0]:
                cyc.append(r)
                r = E[r][0]
            assert len(cyc) == len(comp) and is_closed(succ, cyc)
            U, W = UW(Q, tab, cyc)
            rec.update(cycle=cyc, U=U, W=W, type="b" if U > W else ("n" if U == W else "a"))
            res.append(rec)
            continue
        wt = {r: math.log(tab[r % Q][0]) - math.log(tab[r % Q][2]) for r in comp}
        mu, cyc = max_mean_cycle(comp, E, wt)
        if cyc is not None:
            assert is_closed(succ, cyc) and set(cyc) <= S
            U, W = UW(Q, tab, cyc)
            if U >= W:
                rec.update(type="c", cycle=cyc, U=U, W=W)
                res.append(rec)
                continue
        if not want_potential:
            rec.update(type="u")
            res.append(rec)
            continue
        pot = exact_potential(Q, tab, comp, E)
        if pot is None:
            rec.update(type="u")
        else:
            rec.update(type="a", c=pot[0], theta=pot[1])
        res.append(rec)
    return res


def types_str(cl):
    return "".join(sorted({x["type"] for x in cl}))


# ------------------------------------------------------------------ brute force
def stepper(Q, tab):
    def T(n):
        u, v, w = tab[n % Q]
        x = u * n + v
        assert x % w == 0 and x // w >= 1, n
        return x // w
    return T


def brute_cycles(Q, tab, N, cap=10 ** 6, start=1):
    """Every n in [start, N]: follow until a known point or a repeat. Returns set of
    canonical cycles; raises if an orbit exceeds `cap` steps."""
    T = stepper(Q, tab)
    known = {}
    cycles = set()
    for n in range(start, N + 1):
        if n in known:
            continue
        path, pos, x = [], {}, n
        while x not in known and x not in pos:
            pos[x] = len(path)
            path.append(x)
            x = T(x)
            if len(path) > cap:
                raise RuntimeError(f"orbit of {n} exceeds {cap}")
        if x in pos:
            cyc = path[pos[x]:]
            k = cyc.index(min(cyc))
            cycles.add(tuple(cyc[k:] + cyc[:k]))
        for y in path:
            known[y] = True
    return cycles


def canon(c):
    c = list(c)
    k = c.index(min(c))
    return tuple(c[k:] + c[:k])


def is_cycle(Q, tab, c):
    T = stepper(Q, tab)
    return all(T(c[i]) == c[(i + 1) % len(c)] for i in range(len(c)))


def lap_fixed(Q, tab, cyc):
    """x* of the lap map along the residue cycle (exact)."""
    A, B, D = Fraction(1), Fraction(0), 1
    f = (Fraction(1), Fraction(0))          # x -> a x + b
    for r in cyc:
        u, v, w = tab[r % Q]
        f = (f[0] * u / w, (f[1] * u + v) / w)
    a, b = f
    return b / (1 - a)


# ------------------------------------------------------------------ tables
def B2(u):
    tab = []
    for r in range(8):
        if r % 2 == 0:
            tab.append((1, 0, 2))
        elif r == 1:
            tab.append((1, 1, 1))
        elif r == 3:
            tab.append((u, 6 - 3 * u, 1))
        elif r == 5:
            tab.append((1, 5, 1))
        else:
            tab.append((1, 3, 1))
    return 8, tab


def Bp(p, u):
    Q = p * p
    tab = []
    for r in range(Q):
        if r % p == 0:
            tab.append((1, 0, p))
        elif r == 1:
            tab.append((u, p - u, 1))
        else:
            v = (2 * p - r) % Q
            assert 1 <= v <= Q - 1
            tab.append((1, v, 1))
    return Q, tab


def raw_div(Q, unit_branch):
    """non-units -> n/(least prime of Q dividing r); units -> unit_branch(r)."""
    ps = [p for p in range(2, Q + 1) if Q % p == 0 and all(p % q for q in range(2, p))]
    tab = []
    for r in range(Q):
        d = [p for p in ps if r % p == 0]
        tab.append((1, 0, d[0]) if d else unit_branch(r))
    return tab


def lifted_equal(Q1, t1, Q2, t2, N=20000):
    T1, T2 = stepper(Q1, t1), stepper(Q2, t2)
    return all(T1(n) == T2(n) for n in range(1, N))


# ================================================================== A. Theorem B
def section_A():
    print("A. Theorem B", flush=True)
    for u in (3, 5, 7, 9, 11, 13, 15, 21, 33, 63):
        Q, tab = B2(u)
        check_integral(Q, tab)
        for K in (8, 16, 32, 64):
            cl = classify(Q, tab, K)
            t = types_str(cl)
            ok(set(t) <= set("ab") and "b" in t, f"B2({u}) level {K} types {t}")
            for rec in cl:
                if rec["type"] == "b":
                    x = lap_fixed(Q, tab, rec["cycle"])
                    ok(x == 3 or (x.denominator == 1 and x % K == rec["cycle"][0]),
                       f"B2({u}) x* {x}")
        cl8 = classify(Q, tab, 8)
        bs = [r for r in cl8 if r["type"] == "b"]
        ok(len(bs) == 1 and sorted(bs[0]["nodes"]) == [3, 6] and bs[0]["U"] == u and bs[0]["W"] == 2,
           f"B2({u}) the (b) SCC is not {{3,6}} with u/2")
        N = 300000 if u <= 7 else 60000
        if QUICK:
            N = 20000
        cy = brute_cycles(Q, tab, N)
        ok(cy == {(1, 2), (3, 6), (5, 10)}, f"B2({u}) brute cycles {sorted(cy)[:6]}")
    for p in (3, 5, 7, 11):
        for u in [x for x in range(p + 1, p + 40) if x % p][:8] + [10 * p + 1]:
            Q, tab = Bp(p, u)
            check_integral(Q, tab)
            levels = [p * p, p ** 3] + ([p ** 4] if p == 3 else [])
            for K in levels:
                cl = classify(Q, tab, K)
                t = types_str(cl)
                ok(set(t) <= set("ab") and "b" in t, f"B{p}({u}) level {K} types {t}")
            cl = classify(Q, tab, Q)
            bs = [r for r in cl if r["type"] == "b"]
            ok(len(bs) == 1 and sorted(bs[0]["nodes"]) == [1, p] and Fraction(bs[0]["U"], bs[0]["W"]) == Fraction(u, p),
               f"B{p}({u}) (b) SCC")
            ok(lap_fixed(Q, tab, bs[0]["cycle"]) in (1, p), f"B{p}({u}) x*")
            N = 60000 if not QUICK else 5000
            cy = brute_cycles(Q, tab, N)
            ok(cy == {(1, p), (2, 2 * p)}, f"B{p}({u}) brute cycles {sorted(cy)[:6]}")
    # the "2 -> 1 / 0 -> p" detail of the proof: who reaches node 1 at level p^2
    for p in (3, 5, 7):
        Q, tab = Bp(p, p + 1)
        S = succ_level(Q, tab, Q)
        into1 = [r for r in range(Q) if 1 in S[r]]
        intop = [r for r in range(Q) if p in S[r]]
        ok(into1 == [p] and sorted(intop) == [0, 1], f"B{p}: predecessors of 1 {into1}, of p {intop}")


# ================================================================== B. mixed (b) examples
def section_B():
    print("B. mixed-modulus type (b) examples", flush=True)
    Q = 12
    tab = raw_div(12, lambda r: {1: (11, 3, 1), 5: (1, 2, 1), 7: (1, 3, 1), 11: (1, -1, 1)}[r])
    check_integral(Q, tab)
    cl = classify(Q, tab, Q)
    t = types_str(cl)
    ok(set(t) <= set("ab") and "b" in t, f"Q12 example types {t}")
    bs = [r for r in cl if r["type"] == "b"]
    ok(len(bs) == 1 and sorted(bs[0]["nodes"]) == [1, 2] and (bs[0]["U"], bs[0]["W"]) == (11, 2), "Q12 (b) SCC")
    x = lap_fixed(Q, tab, [2, 1])
    ok(x == Fraction(-2, 3), f"Q12 x* = {x}")
    cy = brute_cycles(Q, tab, 300000 if not QUICK else 20000)
    ok(cy == {(5, 7, 10)}, f"Q12 brute cycles {cy}")
    # all listed mixed examples
    n = 0
    for line in open(os.path.join(OUT, "typeb_mixed_examples.txt")):
        line = line.strip()
        if not line:
            continue
        Q, tab = eval(line, {})
        tab = [tuple(x) for x in tab]
        check_integral(Q, tab)
        ok(all(math.gcd(u, Q) == 1 and Q % w == 0 for (u, v, w) in tab), f"mixed example not Markov Q={Q}")
        cl = classify(Q, tab, Q)
        t = types_str(cl)
        ok(set(t) <= set("ab") and "b" in t, f"mixed example Q={Q} types {t}")
        # (D) holds automatically under H1/H2; check every b cycle anyway
        for rec in cl:
            if rec["type"] == "b":
                U, W = rec["U"], rec["W"]
                ok(any(W % p == 0 and U % p for p in range(2, Q + 1) if Q % p == 0), "condition (D)")
        # Theorem H' cycle list: (b) x* + exhaustive brute force must agree with itself
        cy = brute_cycles(Q, tab, 30000 if not QUICK else 3000)
        ok(len(cy) >= 1 and all(is_cycle(Q, tab, c) for c in cy), f"mixed example Q={Q} cycles")
        n += 1
    print(f"   {n} mixed examples re-typed; Q values checked", flush=True)


# ================================================================== C. Proposition P
def pattern_types(N, kinds):
    """kinds[r] = ('D',) (all successors) or ('F', s).  Returns list of SCCs that are a
    single simple cycle, as (nodes, has_division) and whether a division-free cycle exists."""
    succ = [list(range(N)) if k[0] == "D" else [k[1]] for k in kinds]
    out = []
    for comp in sccs(N, succ):
        S = set(comp)
        ne = sum(1 for r in comp for s in succ[r] if s in S)
        if ne == len(comp):
            out.append((comp, any(kinds[r][0] == "D" for r in comp)))
    # division-free cycle: functional graph on F nodes
    dfc = False
    for r0 in range(N):
        seen, r = set(), r0
        while kinds[r][0] == "F" and r not in seen:
            seen.add(r)
            r = kinds[r][1]
        if kinds[r][0] == "F" and r in seen:
            dfc = True
            break
    return out, dfc


def section_C():
    print("C. Proposition P", flush=True)
    for p in (2, 3, 5):
        opts = [("D",)] + [("F", s) for s in range(p)]
        cnt = 0
        for kinds in product(opts, repeat=p):
            single, dfc = pattern_types(p, kinds)
            if not dfc:
                ok(not single, f"Prop P pattern p={p} {kinds}")
            cnt += 1
        print(f"   p={p}: {cnt} patterns", flush=True)
    for p in (7, 11):
        opts = [("D",)] + [("F", s) for s in range(p)]
        for _ in range(20000 if not QUICK else 2000):
            kinds = [rng.choice(opts) for _ in range(p)]
            single, dfc = pattern_types(p, kinds)
            if not dfc:
                ok(not single, f"Prop P pattern p={p} {kinds}")
    # concrete Markov maps with prime modulus: census open ones are type (c) at levels p..p^4
    for name, Q, tab in [("3x+1", 2, [(1, 0, 2), (3, 1, 1)]),
                         ("m3_g", 3, [(1, 0, 3), (5, 1, 1), (5, 2, 1)]),
                         ("desc_m3_4n5", 3, [(1, 0, 3), (4, 5, 1), (2, 2, 1)]),
                         ("perm_1932", 3, [(2, 0, 3), (4, -1, 3), (4, 1, 3)])]:
        for K in [Q ** k for k in range(1, 9) if Q ** k <= 256]:
            t = types_str(classify(Q, tab, K, want_potential=False))
            ok("c" in t and "b" not in t, f"{name} level {K} types {t}")


# ================================================================== D. Proposition 4
def section_D():
    """Proposition 4 as stated in theory.md has no 'no division-free cycle' hypothesis.
    The referee found it false without one: odd class 1 in a division-free loop leaves the
    SCC {2, 3} a single expanding cycle.  This section (i) asserts that the counterexample
    exists (so the check can tell), (ii) checks the corrected statement: no type (b) at
    levels 4, 8, 16 unless a type (z) SCC is present."""
    print("D. Proposition 4", flush=True)
    cex = [(1, 0, 2), (3, 2, 1), (1, 0, 2), (3, 1, 1)]   # 1 -> 3n+2 (= 1 mod 4), 3 -> 3n+1
    t = types_str(classify(4, cex, 4, want_potential=False))
    ok(t == "abz", f"Prop 4 counterexample types {t}")
    cl = classify(4, cex, 4, want_potential=False)
    ok(any(x["type"] == "b" and x["nodes"] == [2, 3] for x in cl), "Prop 4 counterexample (b) = {2,3}")
    nb_with_z = 0
    for t1 in range(4):
        for t3 in range(4):
            for u1 in (1, 3, 5, 7, 9, 27):
                for u3 in (1, 3, 5, 7, 9, 27):
                    v1 = (t1 - u1) % 4
                    v3 = (t3 - 3 * u3) % 4
                    for add1 in (0, 4, 8):
                        for add3 in (0, 4):
                            tab = [(1, 0, 2), (u1, v1 + add1, 1), (1, 0, 2), (u3, v3 + add3, 1)]
                            check_integral(4, tab)
                            for K in (4, 8, 16):
                                t = types_str(classify(4, tab, K, want_potential=False))
                                if "z" in t:
                                    nb_with_z += "b" in t
                                    continue
                                ok("b" not in t, f"Prop 4 (corrected): {tab} level {K} types {t}")
    print(f"   corrected Prop 4 holds; (table, level) pairs with (b) next to (z): {nb_with_z}", flush=True)
    ok(nb_with_z > 0, "expected (b)+(z) cases for the uncorrected Prop 4")


# ================================================================== E. Lemma S / Theorem S
def primes(Q):
    return [p for p in range(2, Q + 1) if Q % p == 0 and all(p % q for q in range(2, p))]


def sqfree(Q):
    return all(Q % (p * p) for p in primes(Q))


def section_E():
    print("E. Lemma S and Theorem S", flush=True)
    # Lemma S with an arbitrary rule q(S) (S = set of primes of Q dividing r)
    for Q in [Q for Q in range(2, 400) if sqfree(Q) and len(primes(Q)) >= 2]:
        ps = primes(Q)
        subsets = sorted({tuple(p for p in ps if r % p == 0) for r in range(Q)} - {()})
        rules = [dict((S, S[0]) for S in subsets), dict((S, S[-1]) for S in subsets)]
        if len(subsets) <= 7:
            rules = [dict(zip(subsets, ch)) for ch in product(*subsets)]
        elif len(rules) < 50:
            rules += [dict((S, rng.choice(S)) for S in subsets) for _ in range(20)]
        for rule in rules:
            q_of = {r: rule[tuple(p for p in ps if r % p == 0)] for r in range(Q) if math.gcd(r, Q) > 1}
            tab = [(1, 0, q_of[r]) if r in q_of else (1, 1, 1) for r in range(Q)]
            succ = succ_level(Q, tab, Q)
            for q in ps:
                qn = [r for r in q_of if q_of[r] == q]
                img = []
                for r in qn:
                    z = [s for s in succ[r] if s % q == 0]
                    if not ok(len(z) == 1 and z[0] in q_of and q_of[z[0]] == q, f"Lemma S Q={Q} r={r}"):
                        break
                    img.append(z[0])
                ok(sorted(img) == sorted(qn), f"Lemma S permutation Q={Q} q={q}")
    # Theorem S pattern level: every single-cycle SCC of G_Q consists of unit nodes only
    for Q, M in ((6, None), (10, None), (14, 30000), (15, 30000), (30, 6000), (21, 10000), (35, 3000), (42, 2000)):
        units = [r for r in range(Q) if math.gcd(r, Q) == 1]
        def run(targets):
            kinds = []
            ps = primes(Q)
            for r in range(Q):
                if math.gcd(r, Q) > 1:
                    kinds.append(("D", [p for p in ps if r % p == 0][0]))
                else:
                    kinds.append(("F", targets[units.index(r)]))
            tab = [(1, 0, k[1]) if k[0] == "D" else (1, (k[1] - r) % Q or Q, 1) for r, k in enumerate(kinds)]
            succ = succ_level(Q, tab, Q)
            for comp in sccs(Q, succ):
                S = set(comp)
                ne = sum(1 for r in comp for s in succ[r] if s in S)
                if ne == len(comp) and ne > 0:
                    # a single-cycle SCC is all units (division-free) or all non-units
                    # (then it is the s*-cycle Z of n/q steps, contracting)
                    nu = [math.gcd(r, Q) == 1 for r in comp]
                    ok(all(nu) or not any(nu), f"Theorem S Q={Q} targets {targets}")
        if M is None:
            for targets in product(range(Q), repeat=len(units)):
                run(targets)
        else:
            for _ in range(M if not QUICK else M // 10):
                run([rng.randrange(Q) for _ in units])
    # theory.md: with general branches type (b) occurs at Q = 6, 10 (check_theory.py part 4
    # examples, re-typed here with own code) and at Q = 4 (referee example, raw table with a
    # division-free loop); Q = 15 is claimed but no example is given anywhere.
    GEN = [(6, [(7, -4, 2), (1, 3, 1), (13, -2, 3), (13, 5, 1), (1, -2, 2), (13, -5, 1)]),
           (10, [(1, 5, 1), (11, -2, 1), (1, -1, 1), (9, 3, 2), (7, -6, 1), (1, 5, 2), (11, 4, 1),
                 (11, -1, 2), (3, 3, 1), (3, 3, 2)])]
    for Q, tab in GEN:
        check_integral(Q, tab)
        ok(all(math.gcd(u, Q) == 1 and Q % w == 0 for (u, v, w) in tab), f"general Q={Q} not Markov")
        ok(all((u * (r or Q) + v) // w >= 1 for r, (u, v, w) in enumerate(tab)), f"general Q={Q} (P)")
        t = types_str(classify(Q, tab, Q))
        ok(t in ("ab", "b"), f"general-branch example Q={Q}: types {t}")
        cy = brute_cycles(Q, tab, 100000 if not QUICK else 5000)
        ok(len(cy) >= 1, f"general Q={Q} cycles")
        print(f"   general-branch Q={Q}: types {t}, cycles {sorted(cy)}", flush=True)


# ================================================================== F. Theorem C6
def simple_cycles(N, succ):
    out = []
    for s in range(N):
        stack = [(s, [s])]
        while stack:
            v, path = stack.pop()
            for t in succ[v]:
                if t == s:
                    out.append(path[:])
                elif t > s and t not in path:
                    stack.append((t, path + [t]))
    return out


def c6_table():
    rows = {}
    for line in open(os.path.join(OUT, "classify6.md")):
        parts = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(parts) == 3 and parts[0].isdigit():
            rows[(int(parts[0]), int(parts[1]))] = parts[2]
    return rows


def c6_eval(cond, u1, u5):
    if cond.startswith("never"):
        return False
    env = {"u1": u1, "u5": u5}
    return all(eval(c.strip(), {}, env) for c in cond.split(" and "))


def section_F():
    print("F. Theorem C6", flush=True)
    rows = c6_table()
    ok(len(rows) == 36, f"classify6.md has {len(rows)} rows")
    us = [u for u in range(1, 60) if math.gcd(u, 6) == 1]
    for (s1, s5), cond in rows.items():
        succ = [[0, 3], [s1], [1, 4], [1, 3, 5], [2, 5], [s5]]
        cyc = simple_cycles(6, succ)
        w = {0: 2, 2: 2, 4: 2, 3: 3, 1: 1, 5: 1}
        dfree = any(all(w[r] == 1 for r in c) for c in cyc)
        for u1 in us:
            for u5 in us:
                mult = {0: Fraction(1, 2), 2: Fraction(1, 2), 4: Fraction(1, 2), 3: Fraction(1, 3),
                        1: Fraction(u1), 5: Fraction(u5)}
                cert = (not dfree) and all(math.prod(mult[r] for r in c) < 1 for c in cyc)
                ok(cert == c6_eval(cond, u1, u5), f"C6 row ({s1},{s5}) u1={u1} u5={u5}: {cond}")
                if cert:
                    ok(u1 in (1, 5) and u5 in (1, 5), "C6 corollary u in {1,5}")
                if u1 == u5 == 5:
                    ok(cert == ((s1, s5) == (0, 0)), f"C6 (5,5) corollary row ({s1},{s5})")
    # actual maps: own SCC classification at level 6 against the table (random v)
    for _ in range(3000 if not QUICK else 300):
        u1, u5 = rng.choice(us[:8]), rng.choice(us[:8])
        v1, v5 = rng.randrange(-u1 + 1, 30), rng.randrange(-5 * u5 + 1, 30)
        tab = raw_div(6, lambda r: (u1, v1, 1) if r == 1 else (u5, v5, 1))
        cl = classify(6, tab, 6)
        own = types_str(cl) == "a"
        tabc = c6_eval(rows[((u1 + v1) % 6, (5 * u5 + v5) % 6)], u1, u5)
        ok(own == tabc, f"C6 map u1={u1} v1={v1} u5={u5} v5={v5}: own {types_str(cl)} table {tabc}")


# ================================================================== G. div23 with 5n +- 1
def section_G():
    print("G. div23 with 5n+-1", flush=True)
    tab = raw_div(6, lambda r: (5, 1, 1) if r == 1 else (5, -1, 1))
    check_integral(6, tab)
    ok(types_str(classify(6, tab, 6)) == "a", "5n+-1 not all contracting")
    N = 2 * 10 ** 6 if not QUICK else 50000
    ok(brute_cycles(6, tab, N) == {(1, 6, 3)}, "5n+-1 cycles")
    tab2 = raw_div(6, lambda r: (5, 1, 1) if r == 1 else (5, 5, 1))
    ok(types_str(classify(6, tab2, 6)) == "a", "5n+5 variant")
    ok(brute_cycles(6, tab2, N // 4) == {(1, 6, 3), (5, 30, 15)}, "5n+5 variant cycles")
    # k* cross-check with decide.py (not own code)
    sys.path.insert(0, os.path.join(HERE, "..", "..", "round3", "dichotomy"))
    try:
        import decide as D
        r = D.decide(6, tab, want_cycles=True, want_depth=True)
        ok(r["verdict"] == "CERT" and r.get("kstar") == 4, f"decide.py on 5n+-1: {r.get('verdict')} k*={r.get('kstar')}")
    except Exception as e:  # pragma: no cover
        fail(f"decide.py import/run: {e!r}")


# ================================================================== H. open census entries
OWN_OPEN = {
    "split5_1": (4, [(1, 0, 2), (5, 1, 1), (1, 0, 2), (1, 1, 1)]),
    "split5_3": (4, [(1, 0, 2), (5, 3, 1), (1, 0, 2), (1, 3, 1)]),
    "desc_split7_1": (4, [(1, 0, 2), (7, 1, 1), (1, 0, 2), (1, 1, 1)]),
    "desc_m3_4n5": (3, [(1, 0, 3), (4, 5, 1), (2, 2, 1)]),
    "m3_b": (3, [(1, 0, 3), (4, -1, 3), (4, 1, 3)]),
    "m3_d": (3, [(1, 0, 3), (4, 2, 1), (4, 1, 1)]),
    "m3_g": (3, [(1, 0, 3), (5, 1, 1), (5, 2, 1)]),
    "div23_5n1": (6, raw_div(6, lambda r: (5, 1, 1))),
    "div23_7n1": (6, raw_div(6, lambda r: (7, 1, 1))),
    "div235_7n1": (30, raw_div(30, lambda r: (7, 1, 1))),
    "perm_1932": (3, [(2, 0, 3), (4, -1, 3), (4, 1, 3)]),
    "desc_s32_plus9": (32, [(1, 0, 2) if r % 2 == 0 else
                            ((3, 1, 1) if r in {1, 3, 5, 7, 9, 11, 13, 15, 17, 21, 23, 25, 29} else (1, 1, 1))
                            for r in range(32)]),
}


def section_H():
    print("H. open census table maps", flush=True)
    sweep = json.load(open(os.path.join(OUT, "catalog_sweep.json")))["records"]
    rows = json.load(open(os.path.join(OUT, "catalog_rows.json")))
    status = {}
    for r in rows:
        for i in r["ids"]:
            status[i] = r["st"]
    open_recs = [rec for rec in sweep if any(status.get(i, "").startswith("OPEN") for i in rec["ids"])]
    ncls = sum(1 for rec in open_recs if any(status.get(i) == "OPEN-CLS" for i in rec["ids"]))
    print(f"   {len(open_recs)} open records ({ncls} OPEN-CLS)", flush=True)
    noc = []
    for rec in open_recs:
        Q, tab, zero = rec["Q"], [tuple(x) for x in rec["table"]], rec.get("zero", False)
        check_integral(Q, tab)
        markov = all(math.gcd(u, Q) == 1 and Q % w == 0 for (u, v, w) in tab)
        pos = all((u * (r if (r or zero) else Q) + v) // w >= (0 if zero else 1) for r, (u, v, w) in enumerate(tab))
        if not pos:
            noc.append((rec["ids"][0], "positivity fails"))
            continue
        t = types_str(classify(Q, tab, Q, want_potential=False))
        if "c" not in t:
            noc.append((rec["ids"][0], t, markov))
    print("   open records without a type-(c) witness at the base level:", noc, flush=True)
    for x in noc:
        ok(x[1] == "positivity fails" or "c" in str(x[1]) or not x[2], f"open entry without (c): {x}")
    # own tables vs the extracted catalog tables, and lifted levels for the mixed ones
    for name, (Q, tab) in OWN_OPEN.items():
        check_integral(Q, tab)
        hit = [rec for rec in open_recs if any(i.startswith(name) for i in rec["ids"])]
        if hit:
            rq = hit[0]
            ok(lifted_equal(Q, tab, rq["Q"], [tuple(x) for x in rq["table"]]),
               f"own table for {name} differs from the catalog table")
        else:
            print(f"   note: no open catalog record id starting with {name}", flush=True)
        levels = [Q * d for d in (1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 27, 32, 36, 48, 54, 64, 72, 96)
                  if Q * d <= (600 if len(primes(Q)) > 1 else 256) and all(p in primes(Q) for p in primes(d))]
        for K in levels:
            t = types_str(classify(Q, tab, K, want_potential=False))
            ok("c" in t and "b" not in t, f"{name} level {K} types {t}")
        print(f"   {name}: type (c), no (b), at levels {levels}", flush=True)


# ================================================================== I. falsification
def section_I():
    print("I. falsification", flush=True)
    for name, Q, tab in [("3x+1", 2, [(1, 0, 2), (3, 1, 1)]), ("3x-1", 2, [(1, 0, 2), (3, -1, 1)]),
                         ("5x+1", 2, [(1, 0, 2), (5, 1, 1)]), ("3x+5", 2, [(1, 0, 2), (3, 5, 1)])]:
        for K in (2, 4, 8, 16, 32, 64, 128, 256, 512):
            t = types_str(classify(Q, tab, K, want_potential=False))
            ok("c" in t, f"{name} level {K} not type (c): {t}")
    # the brute-force tester must reject a wrong cycle list
    Q, tab = B2(3)
    ok(brute_cycles(Q, tab, 2000) != {(1, 2), (5, 10)}, "wrong cycle list accepted")
    # a deliberately perturbed B2: 7 -> n+11 instead of n+3 sends 7 to 18 = 2 (mod 8): types unchanged;
    # 7 -> 3n+... into 6 would join {3,6} with 7 and must give (c)
    tab2 = list(tab)
    tab2[7] = (3, 1, 1)          # 7 -> 22 = 6 (mod 8): 6 -> 7 -> 6 is a second cycle through 6
    t = types_str(classify(8, tab2, 8, want_potential=False))
    ok("c" in t, f"perturbed B2 should be (c), got {t}")


# ================================================================== J. famscan sample
def fam_opts(name):
    sys.path.insert(0, HERE)
    import families as F            # option menus only (definitions, not verdicts)
    return F.family(name)


def read_fam(name):
    fn = os.path.join(OUT, f"fam_{name}.txt.gz")
    kinds = {}
    summ = None
    with gzip.open(fn, "rt") as f:
        for line in f:
            p = line.split()
            if p[0] == "SUMMARY":
                summ = line
                continue
            kinds[p[1]] = p
    return kinds, summ


def section_J():
    print("J. famscan sample", flush=True)
    exhaustive = {"P2_2_u1357v1357m", "P2_3_u1357v1357m", "P2_4_u135v13", "P3_1_u12457v12m",
                  "P3_2_u1245v12m", "P5_1_u12346v12m", "M_6_u157v123m", "M_10_u1357v12m",
                  "M_12_u157v123m", "M_18_u157v123m", "M_24_u157v12"}
    names = ["P2_2_u1357v1357m", "P2_3_u1357v1357m", "P2_4_u135v13", "P2_4_u1357v1357m", "P2_5_u135v13",
             "P3_1_u12457v12m", "P3_2_u1245v12m", "P3_3_u1245v12m", "G3_2", "P5_1_u12346v12m",
             "P5_2_u1234v12m", "M_6_u157v123m", "M_10_u1357v12m", "M_12_u157v123m", "M_18_u157v123m",
             "M_24_u157v12", "M_24_u157v123m", "M_36_u157v12"]
    per = 25 if not QUICK else 4
    for name in names:
        Q, opts = fam_opts(name)
        kinds, summ = read_fam(name)
        ok(summ is not None, f"{name}: no SUMMARY")
        sp = summ.split()
        tot = int(sp[2])
        cnt = {sp[i]: int(sp[i + 1]) for i in range(3, 15, 2)}
        ok(cnt["CERT"] + cnt["B"] + cnt["C"] + cnt["Z"] + cnt["ZN"] + cnt["FALLBACK"] == tot, f"{name} counts")
        ok(cnt["FALLBACK"] == 0, f"{name} has FALLBACK members")
        if name in exhaustive:
            ok(tot == math.prod(len(o) for o in opts), f"{name}: exhaustive total {tot}")
        certs = [k for k, p in kinds.items() if p[0] == "CERT"]
        bees = [k for k, p in kinds.items() if p[0] == "B"]
        ok(len(bees) == cnt["B"] or name not in exhaustive, f"{name}: B lines {len(bees)} vs {cnt['B']}")
        sample = rng.sample(certs, min(per, len(certs))) + rng.sample(bees, min(per, len(bees)))
        for ix in sample:
            digits = [int(x) for x in ix.split(".")]
            tab = [opts[r][d] for r, d in enumerate(digits)]
            check_integral(Q, tab)
            cl = classify(Q, tab, Q)
            t = types_str(cl)
            claimed = kinds[ix][0]
            if claimed == "CERT":
                ok(t == "a", f"{name} {ix}: claimed CERT, own types {t}")
                nc = int(kinds[ix][3])
                if nc >= 0 and Q <= 36:
                    cy = brute_cycles(Q, tab, 20000 if not QUICK else 2000)
                    ok(len(cy) == nc, f"{name} {ix}: famscan {nc} cycles, brute {len(cy)}")
            else:
                ok(set(t) <= set("ab") and "b" in t, f"{name} {ix}: claimed B, own types {t}")
        if name in exhaustive:
            # members not printed must be C or Z (division-free, divergent) by own code
            radix = [len(o) for o in opts]
            m = 0
            for _ in range(per * 4):
                digits = [rng.randrange(k) for k in radix]
                ix = ".".join(map(str, digits))
                if ix in kinds:
                    continue
                tab = [opts[r][d] for r, d in enumerate(digits)]
                t = types_str(classify(Q, tab, Q, want_potential=False))
                ok("c" in t or "z" in t, f"{name} {ix}: unlisted but own types {t}")
                if "z" in t:
                    # unlisted z must be divergent (ZN is listed)
                    cl = classify(Q, tab, Q, want_potential=False)
                    zz = [x for x in cl if x["type"] == "z"]
                    neutral = all(all(opts_u(tab, Q, r) == 1 for r in x["cycle"]) and
                                  sum(tab[r][1] for r in x["cycle"]) == 0 for x in zz)
                    ok(not neutral, f"{name} {ix}: unlisted but only neutral df cycles")
                m += 1
        print(f"   {name}: sampled {len(sample)} listed, ok", flush=True)


def opts_u(tab, Q, r):
    return tab[r % Q][0]


# ================================================================== K. type-(b) list
def section_K():
    print("K. typeb_list sample", flush=True)
    lines = open(os.path.join(OUT, "typeb_list.jsonl")).read().splitlines()
    ok(len(lines) == 10734, f"typeb_list has {len(lines)} lines")
    for line in rng.sample(lines, 150 if not QUICK else 20):
        d = json.loads(line)
        Q, tab = d["Q"], [tuple(x) for x in d["table"]]
        check_integral(Q, tab)
        cl = classify(Q, tab, Q)
        t = types_str(cl)
        ok(set(t) <= set("ab") and "b" in t, f"typeb {d['index']}: own types {t}")
        listed = {canon(c) for c in d["cycles"]}
        cy = brute_cycles(Q, tab, 20000 if not QUICK else 2000)
        ok(cy == listed, f"typeb {d['family']} {d['index']}: listed {sorted(listed)} brute {sorted(cy)}")
        for b in d["b"]:
            x = lap_fixed(Q, tab, b["cycle"])
            ok(str(x) == b["xstar"], f"typeb x* {x} vs {b['xstar']}")


# ================================================================== L. catalog re-settled sample
def section_L():
    print("L. catalog sample", flush=True)
    recs = json.load(open(os.path.join(OUT, "catalog_sweep.json")))["records"]
    glob = [r for r in recs if "GLOBAL" in str(r["result"].get("H", ""))]
    print(f"   {len(glob)} records with a Theorem H' GLOBAL verdict", flush=True)
    for rec in rng.sample(glob, min(40 if not QUICK else 8, len(glob))):
        Q, tab, zero = rec["Q"], [tuple(x) for x in rec["table"]], rec.get("zero", False)
        listed = {canon(c) for c in rec["result"]["H_cycles"]}
        N = 20000 if Q <= 500 else 3000
        try:
            cy = brute_cycles(Q, tab, N, start=0 if zero else 1)
        except AssertionError:
            fail(f"catalog {rec['ids'][0]}: positivity broken in brute force")
            continue
        ok(cy == listed, f"catalog {rec['ids'][0]}: listed {sorted(listed)[:5]} brute {sorted(cy)[:5]}")
        if all(math.gcd(u, Q) == 1 and Q % w == 0 for (u, v, w) in tab) and Q <= 64:
            K = int(rec["result"]["H"].split("K=")[1])
            if K <= 256:
                t = types_str(classify(Q, tab, K))
                ok("c" not in t and "u" not in t, f"catalog {rec['ids'][0]}: own types at {K}: {t}")


if __name__ == "__main__":
    which = [a for a in sys.argv[1:] if len(a) == 1] or list("ABCDEFGHIJKL")
    for s in which:
        globals()["section_" + s]()
    print("FAILURES:", len(FAILS))
    for f in FAILS[:50]:
        print("  ", f)
    sys.exit(1 if FAILS else 0)
