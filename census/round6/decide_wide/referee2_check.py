#!/usr/bin/env python3
"""referee2_check.py -- Referee 2's own check of round6/decide_wide.  Written from scratch.

It does NOT import twlib.py, famscan, check_*.py or referee1_check.py.  It imports
families.py only to decode the option menus of the family files (pure data), and reads the
prover's output files only as the claims to be tested.

Own code: residue graph at level K, Tarjan SCC, exact SCC typing (exact rational potential
certificate for (a); exact cycle product witness for (b)/(c); (z) by division-free cycle),
an own implementation of Theorem H' (exact lap fixed points, exact potentials, enumeration
bound), and a brute-force orbit tester.

Sections
  A  hand-built systems: B2(u), Bp(u), E15, Q=12 mixed example, div23 5n+-1 (and 5n+5),
     Prop 4 counterexample; types at several levels and brute force over large ranges
  B  Proposition 4 (corrected): all successor patterns, many (u, v), levels 4..32
  C  Proposition P at lifted levels p^k (the README claim "no type (b) at any level")
  D  Theorem S / Lemma S on random raw full-division tables, squarefree Q, level Q
  E  falsification: 3x+1, 3x-1, 5x+1, split5_1, split5_3, div23_5n1 must stay unsettled;
     wrong cycle lists and perturbed tables must be detected
  F  exhaustive recount of the small families (P2_2, P3_1, M_6, P5_1, M_10, M_12)
  G  random sample of every family file (listed CERT / B lines and unlisted members)
  H  random sample of out/typeb_list.jsonl
  I  catalog: sample of re-settled records, every open record has a (c) SCC, coverage count
  J  Theorem C6 corollaries on a grid
Exit status 0 iff every assertion holds.  Argument "quick" shrinks the ranges.
"""
import gzip
import json
import math
import os
import random
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
QUICK = "quick" in sys.argv
FAILS = []


def check(cond, msg):
    if not cond:
        FAILS.append(msg)
        print("FAIL:", msg, flush=True)
    return cond


# ---------------------------------------------------------------------------- maps
def step(Q, tab, n):
    u, v, w = tab[n % Q]
    x = u * n + v
    assert x % w == 0, ("non-integer step", Q, tab[n % Q], n)
    return x // w


def orbit_cycle(Q, tab, n, cap_steps=200000, cap_val=10 ** 80, lo=1):
    """Follow n until it repeats; return the cycle as a tuple starting at its minimum,
    or None if the caps are hit.  Asserts the orbit stays >= lo."""
    seen = {}
    x = n
    path = []
    while x not in seen:
        if len(path) > cap_steps or x > cap_val:
            return None
        if x < lo:
            raise AssertionError(("positivity fails", n, x))
        seen[x] = len(path)
        path.append(x)
        x = step(Q, tab, x)
    cyc = path[seen[x]:]
    i = cyc.index(min(cyc))
    return tuple(cyc[i:] + cyc[:i])


def brute_cycles(Q, tab, N, lo=1, cap_steps=200000):
    """All cycles reached from lo <= n <= N.  Memoised on values < n (already resolved)."""
    res = {}
    cycles = set()
    bad = []
    for n in range(lo, N + 1):
        x = n
        seen = {}
        path = []
        out = None
        while True:
            if x < n:  # resolved before
                out = res[x]
                break
            if x in seen:
                cyc = path[seen[x]:]
                i = cyc.index(min(cyc))
                out = tuple(cyc[i:] + cyc[:i])
                cycles.add(out)
                break
            if len(path) > cap_steps:
                out = "CAP"
                bad.append(n)
                break
            seen[x] = len(path)
            path.append(x)
            x = step(Q, tab, x)
            if x < lo:
                raise AssertionError(("positivity", n, x))
        res[n] = out
    return cycles, bad


def norm_cycle(c):
    c = list(c)
    i = c.index(min(c))
    return tuple(c[i:] + c[:i])


# ---------------------------------------------------------------------------- graph
def graph(Q, tab, K):
    assert K % Q == 0
    succ = []
    lab = []
    for r in range(K):
        u, v, w = tab[r % Q]
        assert (u * r + v) % w == 0 and (u * K) % w == 0, ("table condition", r, tab[r % Q])
        y0 = (u * r + v) // w
        k = u * K // w
        g = math.gcd(k, K)
        s = sorted({(y0 + g * j) % K for j in range(K // g)})
        succ.append(s)
        lab.append((u, w))
    return succ, lab


def tarjan(succ):
    n = len(succ)
    index = [None] * n
    low = [0] * n
    onst = [False] * n
    st = []
    comps = []
    cnt = 0
    for root in range(n):
        if index[root] is not None:
            continue
        work = [(root, 0)]
        index[root] = low[root] = cnt
        cnt += 1
        st.append(root)
        onst[root] = True
        while work:
            v, i = work[-1]
            if i < len(succ[v]):
                work[-1] = (v, i + 1)
                w = succ[v][i]
                if index[w] is None:
                    index[w] = low[w] = cnt
                    cnt += 1
                    st.append(w)
                    onst[w] = True
                    work.append((w, 0))
                elif onst[w]:
                    low[v] = min(low[v], index[w])
            else:
                work.pop()
                if work:
                    p = work[-1][0]
                    low[p] = min(low[p], low[v])
                if low[v] == index[v]:
                    comp = []
                    while True:
                        w = st.pop()
                        onst[w] = False
                        comp.append(w)
                        if w == v:
                            break
                    comps.append(comp)
    return comps


def has_cycle(nodes, succ):
    S = set(nodes)
    color = {x: 0 for x in nodes}
    for s0 in nodes:
        if color[s0]:
            continue
        stack = [(s0, iter([y for y in succ[s0] if y in S]))]
        color[s0] = 1
        while stack:
            v, it = stack[-1]
            nxt = next(it, None)
            if nxt is None:
                color[v] = 2
                stack.pop()
            elif color[nxt] == 1:
                return True
            elif color[nxt] == 0:
                color[nxt] = 1
                stack.append((nxt, iter([y for y in succ[nxt] if y in S])))
    return False


def karp(nodes, edges):
    """max mean cycle (float) on log-weights; edges: list (a, b, wt).  Returns (lam, cycle)."""
    idx = {x: i for i, x in enumerate(nodes)}
    n = len(nodes)
    NEG = -1e300
    D = [[NEG] * n for _ in range(n + 1)]
    P = [[-1] * n for _ in range(n + 1)]
    for i in range(n):
        D[0][i] = 0.0
    E = [(idx[a], idx[b], w) for a, b, w in edges]
    for k in range(1, n + 1):
        Dk, Dp, Pk = D[k], D[k - 1], P[k]
        for a, b, w in E:
            if Dp[a] > NEG / 2 and Dp[a] + w > Dk[b]:
                Dk[b] = Dp[a] + w
                Pk[b] = a
    best, bv = -1e300, None
    for v in range(n):
        if D[n][v] <= NEG / 2:
            continue
        m = min((D[n][v] - D[k][v]) / (n - k) for k in range(n) if D[k][v] > NEG / 2)
        if m > best:
            best, bv = m, v
    # walk back from bv at length n; it contains a cycle
    walk = [bv]
    v = bv
    for k in range(n, 0, -1):
        v = P[k][v]
        walk.append(v)
    walk.reverse()
    cycles = []
    pos = {}
    for i, x in enumerate(walk):
        if x in pos:
            cycles.append([nodes[y] for y in walk[pos[x]:i]])
        pos[x] = i
    return best, cycles


def cycle_mult(cyc, lab):
    U = W = 1
    for r in cyc:
        u, w = lab[r]
        U *= u
        W *= w
    return U, W


def exact_potential(nodes, iedges, lab, lam):
    """Try to certify exactly that every cycle in the SCC has multiplier < 1.
    Returns (theta, c) with c(s) u <= theta c(r) w on every internal edge, or None."""
    if not lam < 0:
        return None
    l1, l2 = 2 * lam / 3, lam / 3
    d = {x: 0.0 for x in nodes}
    for _ in range(len(nodes) + 2):
        ch = False
        for a, b in iedges:
            u, w = lab[a]
            val = d[a] + math.log(u / w) - l1
            if val > d[b] + 1e-15:
                d[b] = val
                ch = True
        if not ch:
            break
    else:
        return None
    m = min(d.values())
    theta = Fr(math.exp(l2)).limit_denominator(10 ** 6)
    if not theta < 1:
        return None
    c = {x: Fr(math.exp(-(d[x] - m))).limit_denominator(10 ** 12) for x in nodes}
    for a, b in iedges:
        u, w = lab[a]
        if not c[b] * u <= theta * c[a] * w:
            return None
    if any(c[x] <= 0 for x in nodes):
        return None
    return theta, c


def classify(Q, tab, K, want_detail=False):
    """Return dict with list of SCC records (nodes, type, extra).  Raises on undecided."""
    succ, lab = graph(Q, tab, K)
    comps = tarjan(succ)
    out = []
    for comp in comps:
        S = set(comp)
        iedges = [(a, b) for a in comp for b in succ[a] if b in S]
        if not iedges:
            continue
        rec = {"nodes": comp}
        df = [x for x in comp if lab[x][1] == 1]
        if df and has_cycle(df, [[y for y in succ[x] if lab[y][1] == 1] if lab[x][1] == 1 else []
                                 for x in range(K)]):
            rec["type"] = "z"
            out.append(rec)
            continue
        outdeg = {}
        for a, b in iedges:
            outdeg[a] = outdeg.get(a, 0) + 1
        if all(outdeg.get(x, 0) == 1 for x in comp):
            # single simple cycle
            nxt = {a: b for a, b in iedges}
            cyc = [comp[0]]
            while nxt[cyc[-1]] != comp[0]:
                cyc.append(nxt[cyc[-1]])
            assert len(cyc) == len(comp)
            U, W = cycle_mult(cyc, lab)
            rec["cycle"] = cyc
            rec["UW"] = (U, W)
            rec["type"] = "b" if U > W else ("a" if U < W else "n")
            if rec["type"] == "a":
                lam = math.log(U / W) / len(cyc)
                pot = exact_potential(comp, iedges, lab, lam)
                if pot is None:
                    raise AssertionError(("no potential for contracting single cycle", Q, K))
                rec["pot"] = pot
            out.append(rec)
            continue
        ed = [(a, b, math.log(lab[a][0] / lab[a][1])) for a, b in iedges]
        lam, cycs = karp(comp, ed)
        pot = exact_potential(comp, iedges, lab, lam) if lam < -1e-9 else None
        if pot is not None:
            rec["type"] = "a"
            rec["pot"] = pot
        else:
            wit = None
            for cy in cycs:
                U, W = cycle_mult(cy, lab)
                if U >= W:
                    wit = (cy, U, W)
                    break
            if wit is None:
                raise AssertionError(("undecided SCC", Q, K, lam))
            rec["type"] = "c"
            rec["witness"] = wit
        out.append(rec)
    return out, succ, lab


def types_str(recs):
    return "".join(sorted({r["type"] for r in recs}))


# ---------------------------------------------------------------------------- Theorem H'
def vp(x, p):
    x = Fr(x)
    if x == 0:
        return 10 ** 9
    a, b = x.numerator, x.denominator
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    while b % p == 0:
        b //= p
        k -= 1
    return k


def primes_of(n):
    ps, d = [], 2
    while d * d <= n:
        if n % d == 0:
            ps.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        ps.append(n)
    return ps


def theorem_H(Q, tab, K, lo=1, enum_cap=3_000_000):
    """Own Theorem H'.  Returns ('GLOBAL', cycles) or ('NONE', reason)."""
    recs, succ, lab = classify(Q, tab, K)
    cycles = set()
    for rec in recs:
        t = rec["type"]
        if t not in "ab":
            return "NONE", t
    for rec in recs:
        if rec["type"] == "b":
            cyc = rec["cycle"]
            U, W = rec["UW"]
            if not any(vp(W, p) > vp(U, p) for p in primes_of(W)):
                return "NONE", "D"
            # lap map from cyc[0]
            A, B = Fr(1), Fr(0)
            for r in cyc:
                u, v, w = tab[r % Q]
                A, B = A * u / w, (B * u + v) / w
            xs = B / (1 - A)
            if xs.denominator == 1 and xs >= lo and int(xs) % K == cyc[0]:
                x = int(xs)
                pts = [x]
                ok = True
                for i in range(len(cyc)):
                    if pts[-1] % K != cyc[i]:
                        ok = False
                    pts.append(step(Q, tab, pts[-1]))
                if ok and pts[-1] == x:
                    cycles.add(orbit_cycle(Q, tab, x, lo=lo))
        else:
            theta, c, *_ = rec["pot"]
            S = set(rec["nodes"])
            beta = Fr(0)
            for a in rec["nodes"]:
                u, v, w = tab[a % Q]
                for b in succ[a]:
                    if b in S:
                        beta = max(beta, c[b] * max(v, 0) / w)
            bound = beta / (1 - theta)
            cnt = 0
            for r in rec["nodes"]:
                nmax = math.floor(bound / c[r])
                n = r if r >= lo else r + K
                while n <= nmax:
                    cnt += 1
                    if cnt > enum_cap:
                        return "NONE", "enum cap"
                    cy = orbit_cycle(Q, tab, n, lo=lo)
                    if cy is None:
                        return "NONE", "orbit cap"
                    if all((x % K) in S for x in cy):
                        cycles.add(cy)
                    n += K
    return "GLOBAL", cycles


# ---------------------------------------------------------------------------- tables
def table_B2(u):
    t = [None] * 8
    for r in range(0, 8, 2):
        t[r] = (1, 0, 2)
    t[1] = (1, 1, 1)
    t[3] = (u, 6 - 3 * u, 1)
    t[5] = (1, 5, 1)
    t[7] = (1, 3, 1)
    return 8, t


def table_Bp(p, u):
    Q = p * p
    t = []
    for s in range(Q):
        if s % p == 0:
            t.append((1, 0, p))
        elif s == 1:
            t.append((u, p - u, 1))
        else:
            vs = (2 * p - s) % Q
            if vs == 0:
                vs = Q
            t.append((1, vs, 1))
    return Q, t


def table_E15():
    t = []
    for r in range(15):
        if r % 3 == 0:
            t.append((1, (15 - r) % 15, 5))
        elif r == 1:
            t.append((7, -1, 3))
        elif r == 2:
            t.append((1, 14, 1))
        else:
            t.append((1, 15 - r, 1))
    return 15, t


def raw_div(Q, units):
    """2|n->n/2, else least other prime p|n -> n/p, else units[r]."""
    ps = primes_of(Q)
    t = []
    for r in range(Q):
        d = next((p for p in ps if r % p == 0), None)
        t.append((1, 0, d) if d else units[r])
    return Q, t


def lift(Q, tab, K):
    return [tab[r % Q] for r in range(K)]


# ---------------------------------------------------------------------------- A
def section_A():
    print("== A: hand-built systems", flush=True)
    N1 = 200000 if QUICK else 1000000
    N2 = 50000 if QUICK else 200000
    for u in [3, 5, 7, 9, 11, 15, 17, 31, 63, 127]:
        Q, t = table_B2(u)
        for K in [8, 16, 32, 64, 128]:
            recs, _, _ = classify(Q, t, K)
            ts = types_str(recs)
            check(ts == "ab", f"B2({u}) level {K} types {ts}")
            bs = [r for r in recs if r["type"] == "b"]
            check(len(bs) == 1 and Fr(*bs[0]["UW"]) == Fr(u, 2), f"B2({u}) K={K} b-cycle {bs and bs[0]['UW']}")
        v, cy = theorem_H(Q, t, 8)
        check(v == "GLOBAL" and cy == {(1, 2), (3, 6), (5, 10)}, f"B2({u}) H' {v} {cy}")
        cyc, bad = brute_cycles(Q, t, N1 if u <= 7 else N2)
        check(cyc == {(1, 2), (3, 6), (5, 10)} and not bad, f"B2({u}) brute {sorted(cyc)[:5]} bad {bad[:3]}")
    for p in [3, 5, 7, 11, 13]:
        for u in sorted({p + 1, p + 2, 2 * p + 1, 3 * p - 1, 4 * p + 3, 100 * p + 1}):
            if u % p == 0:
                continue
            Q, t = table_Bp(p, u)
            levels = [Q, Q * p] + ([Q * p * p] if p <= 5 else [])
            for K in levels:
                recs, _, _ = classify(Q, t, K)
                ts = types_str(recs)
                check(ts == "ab", f"B{p}({u}) level {K} types {ts}")
                bs = [r for r in recs if r["type"] == "b"]
                check(len(bs) == 1 and Fr(*bs[0]["UW"]) == Fr(u, p), f"B{p}({u}) b {[b['UW'] for b in bs]}")
            v, cy = theorem_H(Q, t, Q)
            check(v == "GLOBAL" and cy == {(1, p), (2, 2 * p)}, f"B{p}({u}) H' {v} {cy}")
            cyc, bad = brute_cycles(Q, t, N2 if p <= 5 else N2 // 4)
            check(cyc == {(1, p), (2, 2 * p)} and not bad, f"B{p}({u}) brute {cyc}")
    # E15
    Q, t = table_E15()
    recs, _, _ = classify(Q, t, 15)
    check(types_str(recs) == "ab", f"E15 types {types_str(recs)}")
    bs = [r for r in recs if r["type"] == "b"]
    check(len(bs) == 1 and sorted(bs[0]["cycle"]) == [1, 2] and Fr(*bs[0]["UW"]) == Fr(7, 3), "E15 b cycle")
    v, cy = theorem_H(Q, t, 15)
    check(v == "GLOBAL" and cy == {(3,)}, f"E15 H' {v} {cy}")
    for K in [45, 75, 135]:
        print("   E15 level", K, types_str(classify(Q, t, K)[0]))
    cyc, bad = brute_cycles(Q, t, N1)
    check(cyc == {(3,)} and not bad, f"E15 brute {cyc}")
    # Q = 12 mixed example: 2|n -> n/2; else 3|n -> n/3; 1,5,7,11 -> 11n+3, n+2, n+3, n-1
    Q, t = raw_div(12, {1: (11, 3, 1), 5: (1, 2, 1), 7: (1, 3, 1), 11: (1, -1, 1)})
    recs, _, _ = classify(Q, t, 12)
    check(types_str(recs) == "ab", f"Q12 types {types_str(recs)}")
    bs = [r for r in recs if r["type"] == "b"]
    check(len(bs) == 1 and sorted(bs[0]["cycle"]) == [1, 2] and Fr(*bs[0]["UW"]) == Fr(11, 2), f"Q12 b {bs}")
    A, B = Fr(1), Fr(0)
    for r in [2, 1]:
        u, v, w = t[r]
        A, B = A * u / w, (B * u + v) / w
    check(B / (1 - A) == Fr(-2, 3), f"Q12 x*(2) = {B / (1 - A)}")
    v, cy = theorem_H(Q, t, 12)
    check(v == "GLOBAL" and cy == {(5, 7, 10)}, f"Q12 H' {v} {cy}")
    cyc, bad = brute_cycles(Q, t, N1)
    check(cyc == {(5, 7, 10)} and not bad, f"Q12 brute {cyc}")
    # div23 with 5n +- 1 and 5n+5
    for v5, want in [(-1, {(1, 6, 3)}), (5, {(1, 6, 3), (5, 30, 15)})]:
        Q, t = raw_div(6, {1: (5, 1, 1), 5: (5, v5, 1)})
        recs, _, _ = classify(Q, t, 6)
        check(types_str(recs) == "a", f"5n{v5:+d} types {types_str(recs)}")
        cyc, bad = brute_cycles(Q, t, N1)
        check(cyc == want and not bad, f"5n{v5:+d} brute {cyc}")
    # Prop 4 counterexample
    t = [(1, 0, 2), (3, 2, 1), (1, 0, 2), (3, 1, 1)]
    recs, _, _ = classify(4, t, 4)
    ty = {tuple(sorted(r["nodes"])): r["type"] for r in recs}
    check(ty.get((2, 3)) == "b" and ty.get((1,)) == "z", f"Prop4 counterexample {ty}")
    check(theorem_H(4, t, 4)[0] == "NONE", "Prop4 counterexample must not be settled")


# ---------------------------------------------------------------------------- B
def has_divfree(Q, tab, K):
    succ, lab = graph(Q, tab, K)
    df = [x for x in range(K) if lab[x][1] == 1]
    return has_cycle(df, [[y for y in succ[x] if lab[y][1] == 1] if lab[x][1] == 1 else [] for x in range(K)])


def section_B():
    print("== B: Proposition 4 (corrected)", flush=True)
    us = [1, 3, 5, 7, 9, 27]
    vs = list(range(-3, 12))
    n_hyp = n_nohyp_b = n_tab = 0
    levels = [4, 8, 16] if QUICK else [4, 8, 16, 32]
    for u1 in us:
        for v1 in vs:
            if u1 * 1 + v1 < 1:
                continue
            for u3 in us:
                for v3 in vs:
                    if 3 * u3 + v3 < 1:
                        continue
                    t = [(1, 0, 2), (u1, v1, 1), (1, 0, 2), (u3, v3, 1)]
                    n_tab += 1
                    hyp = not has_divfree(4, t, 4)
                    if hyp:
                        n_hyp += 1
                    for K in levels if (hyp or random.random() < 0.2) else [4]:
                        if K > 8 and random.random() < 0.7:
                            continue
                        recs, _, _ = classify(4, t, K)
                        ts = types_str(recs)
                        if hyp:
                            check("b" not in ts, f"Prop4 b at K={K} {t} {ts}")
                            check(not has_divfree(4, t, K), f"Prop4 divfree appears at K={K} {t}")
                        else:
                            check("z" in ts, f"Prop4 no-hyp but no z at K={K} {t}")
                            if "b" in ts:
                                n_nohyp_b += 1
                            check(theorem_H(4, t, K)[0] == "NONE", f"Prop4 H' settled a (z) table {t}")
    print(f"   {n_tab} tables, {n_hyp} satisfy the hypothesis; (b)-next-to-(z) cases seen: {n_nohyp_b}")
    check(n_nohyp_b > 0, "expected some (b) next to (z) without the hypothesis")


# ---------------------------------------------------------------------------- C
def rand_markov_prime(p, rng, maxu=40, vr=12):
    t = []
    for r in range(p):
        while True:
            w = rng.choice([1, p])
            u = rng.randrange(1, maxu)
            if u % p == 0:
                continue
            v = rng.randrange(-vr, vr + 1)
            if (u * r + v) % w:
                continue
            n0 = r if r > 0 else p
            if (u * n0 + v) // w < 1:
                continue
            t.append((u, v, w))
            break
    return t


def section_C():
    print("== C: Proposition P at lifted levels", flush=True)
    rng = random.Random(2)
    cnt = {}
    for p, levels, trials in [(2, [2, 4, 8, 16, 32, 64], 300), (3, [3, 9, 27, 81], 300), (5, [5, 25, 125], 150),
                              (7, [7, 49], 100)]:
        if QUICK:
            trials //= 3
        for _ in range(trials):
            t = rand_markov_prime(p, rng)
            if has_divfree(p, t, p):
                continue
            base = types_str(classify(p, t, p)[0])
            check("b" not in base, f"PropP base (b) p={p} {t}")
            for K in levels[1:]:
                ts = types_str(classify(p, t, K)[0])
                check("b" not in ts, f"PropP lifted (b) p={p} K={K} {t} {ts}")
                check(("c" in ts) == ("c" in base), f"PropP: (c) not level independent p={p} K={K} {t}")
                cnt[p] = cnt.get(p, 0) + 1
    # named census maps
    named = {"3x+1": (2, [(1, 0, 2), (3, 1, 1)]), "3x-1": (2, [(1, 0, 2), (3, -1, 1)]),
             "5x+1": (2, [(1, 0, 2), (5, 1, 1)]), "desc_m3_4n5": (3, [(1, 0, 3), (4, 5, 1), (2, 2, 1)])}
    for nm, (p, t) in named.items():
        for K in [p ** k for k in range(1, 8) if p ** k <= 256]:
            ts = types_str(classify(p, t, K)[0])
            check("c" in ts and "b" not in ts, f"{nm} level {K} types {ts}")
    print("   lifted (table, level) pairs checked:", cnt)


# ---------------------------------------------------------------------------- D
def section_D():
    print("== D: Theorem S / Lemma S", flush=True)
    rng = random.Random(3)
    Qs = [6, 10, 14, 15, 21, 22, 30, 35, 42, 66, 70, 105]
    nchk = 0
    for Q in Qs:
        ps = primes_of(Q)
        assert all(Q % (p * p) for p in ps)
        for trial in range(60 if not QUICK else 20):
            # random prime-support rule q(S)
            rule = {}
            units = {}
            for r in range(Q):
                S = frozenset(p for p in ps if r % p == 0)
                if S and S not in rule:
                    rule[S] = rng.choice(sorted(S))
            t = []
            for r in range(Q):
                S = frozenset(p for p in ps if r % p == 0)
                if S:
                    t.append((1, 0, rule[S]))
                else:
                    while True:
                        u = rng.randrange(1, 4 * Q)
                        if math.gcd(u, Q) != 1:
                            continue
                        v = rng.randrange(-Q, Q)
                        if u * r + v >= 1:
                            break
                    t.append((u, v, 1))
            # Lemma S: s* permutes q-nodes
            succ, lab = graph(Q, t, Q)
            for q in ps:
                qn = [r for r in range(Q) if lab[r][1] == q and r % q == 0 and t[r][1] == 0]
                img = []
                for r in qn:
                    ss = [s for s in succ[r] if s % q == 0]
                    check(len(ss) == 1, f"LemmaS unique s* Q={Q} r={r}")
                    img.append(ss[0])
                check(sorted(img) == sorted(qn), f"LemmaS permutation Q={Q} q={q}")
            recs, _, _ = classify(Q, t, Q)
            for rec in recs:
                if rec["type"] == "b":
                    check(all(lab[x][1] == 1 for x in rec["nodes"]), f"ThmS (b) with division node Q={Q} {t}")
                if rec["type"] in "bc" or rec["type"] == "z":
                    pass
            nchk += 1
    # hypothesis needed: E15 and a Q=6 general-branch example give (b) with division node
    print("   random squarefree tables checked:", nchk)


# ---------------------------------------------------------------------------- E
def section_E():
    print("== E: falsification", flush=True)
    sys_ = {"3x+1": (2, [(1, 0, 2), (3, 1, 1)]), "3x-1": (2, [(1, 0, 2), (3, -1, 1)]),
            "3x+5": (2, [(1, 0, 2), (3, 5, 1)]), "5x+1": (2, [(1, 0, 2), (5, 1, 1)]),
            "split5_1": (4, [(1, 0, 2), (5, 1, 1), (1, 0, 2), (1, 1, 1)]),
            "split5_3": (4, [(1, 0, 2), (5, 3, 1), (1, 0, 2), (1, 3, 1)]),
            "desc_split7_1": (4, [(1, 0, 2), (7, 1, 1), (1, 0, 2), (1, 1, 1)]),
            "div23_5n1": raw_div(6, {1: (5, 1, 1), 5: (5, 1, 1)}),
            "div23_7n1": raw_div(6, {1: (7, 1, 1), 5: (7, 1, 1)}),
            "div235_7n1": raw_div(30, {r: (7, 1, 1) for r in range(30) if math.gcd(r, 30) == 1})}
    for nm, (Q, t) in sys_.items():
        levels = [Q * m for m in [1, 2, 4, 8, 16, 32] if Q * m <= 300] + ([Q * 3, Q * 9] if Q % 3 == 0 else [])
        for K in levels:
            v, why = theorem_H(Q, t, K)
            check(v == "NONE" and why == "c", f"{nm} settled or not (c) at level {K}: {v} {why}")
    # wrong cycle list for B2(3) must differ from brute force
    Q, t = table_B2(3)
    cyc, _ = brute_cycles(Q, t, 20000)
    check(cyc != {(1, 2), (5, 10)}, "wrong list must be detected")
    # perturbed B2: 7 -> n+7 instead of n+3 (7 -> 6 joins {3,6})
    t2 = list(t)
    t2[7] = (1, 7, 1)
    ts = types_str(classify(Q, t2, 8)[0])
    check("c" in ts, f"perturbed B2 should be (c): {ts}")
    check(theorem_H(Q, t2, 8)[0] == "NONE", "perturbed B2 must not be settled")


# ---------------------------------------------------------------------------- F/G
def load_family(name):
    sys.path.insert(0, HERE)
    import families  # data only
    return families.family(name)


def member_class(Q, tab):
    recs, _, _ = classify(Q, tab, Q)
    ts = types_str(recs)
    if "z" in ts:
        return "Z", recs
    if "c" in ts:
        return "C", recs
    if "n" in ts:
        return "N", recs
    if "b" in ts:
        return "B", recs
    return "CERT", recs


def section_F():
    print("== F: exhaustive recount of small families", flush=True)
    claimed = {"P2_2_u1357v1357m": (483, 48, 0, 435, 0), "P3_1_u12457v12m": (323, 13, 0, 152, 158),
               "M_6_u157v123m": (240, 20, 0, 188, 32), "P5_1_u12346v12m": (129200, 2041, 0, 30887, 96272),
               "M_10_u1357v12m": (61440, 3907, 0, 45757, 11776), "M_12_u157v123m": (61440, 2033, 1, 51470, 7936)}
    import itertools
    for name, (tot, ce, b, c, z) in claimed.items():
        if QUICK and tot > 1000:
            continue
        Q, opts = load_family(name)
        cnt = {"CERT": 0, "B": 0, "C": 0, "Z": 0, "N": 0}
        n = 0
        for choice in itertools.product(*opts):
            k, _ = member_class(Q, list(choice))
            cnt[k] += 1
            n += 1
        got = (n, cnt["CERT"], cnt["B"], cnt["C"], cnt["Z"])
        print(f"   {name}: {got}", flush=True)
        check(got == (tot, ce, b, c, z) and cnt["N"] == 0, f"family {name} counts {got} vs {(tot, ce, b, c, z)}")


def section_G():
    print("== G: family file samples", flush=True)
    rng = random.Random(5)
    outd = os.path.join(HERE, "out")
    files = sorted(f for f in os.listdir(outd) if f.startswith("fam_"))
    check(len(files) == 18, f"18 family files, got {len(files)}")
    nb = nc = nu = 0
    for f in files:
        name = f[4:-7]
        Q, opts = load_family(name)
        lines = gzip.open(os.path.join(outd, f), "rt").read().split("\n")
        cert = [l.split() for l in lines if l.startswith("CERT ")]
        bl = [l.split() for l in lines if l.startswith("B ")]
        summ = [l for l in lines if l.startswith("SUMMARY")][0].split()
        sd = {summ[i]: summ[i + 1] for i in range(1, 15, 2)}
        check(int(sd["CERT"]) == len(cert) and int(sd["B"]) == len(bl), f"{name} summary vs lines")
        check(int(sd["FALLBACK"]) == 0, f"{name} fallback")
        check(int(sd["total"]) == sum(int(sd[k]) for k in ["CERT", "B", "C", "Z", "ZN", "FALLBACK"]),
              f"{name} summary sum")
        ns = 6 if QUICK else 25
        for parts in rng.sample(cert, min(ns, len(cert))):
            tab = [opts[r][int(d)] for r, d in enumerate(parts[1].split("."))]
            k, recs = member_class(Q, tab)
            check(k == "CERT", f"{name} CERT line {parts[1]} is {k}")
            ncl = int(parts[3])
            cyc, bad = brute_cycles(Q, tab, 3000 if Q > 20 else 20000)
            check(len(cyc) == ncl and not bad, f"{name} {parts[1]} cycles {len(cyc)} vs {ncl}")
            nc += 1
        for parts in rng.sample(bl, min(ns, len(bl))):
            tab = [opts[r][int(d)] for r, d in enumerate(parts[1].split("."))]
            k, recs = member_class(Q, tab)
            check(k == "B", f"{name} B line {parts[1]} is {k}")
            nb += 1
        # unlisted members (exhaustive files): must be C or Z
        sizes = [len(o) for o in opts]
        total = 1
        for s in sizes:
            total *= s
        if total == int(sd["total"]):
            listed = {p[1] for p in cert} | {p[1] for p in bl}
            for _ in range(8 if QUICK else 40):
                ix = ".".join(str(rng.randrange(s)) for s in sizes)
                tab = [opts[r][int(d)] for r, d in enumerate(ix.split("."))]
                k, _ = member_class(Q, tab)
                if ix in listed:
                    continue
                check(k in ("C", "Z"), f"{name} unlisted {ix} is {k}")
                nu += 1
    print(f"   CERT lines {nc}, B lines {nb}, unlisted {nu}")


def section_H():
    print("== H: typeb_list.jsonl sample", flush=True)
    rng = random.Random(7)
    L = [json.loads(l) for l in open(os.path.join(HERE, "out", "typeb_list.jsonl"))]
    check(len(L) == 10734, f"typeb lines {len(L)}")
    from collections import Counter
    byfam = Counter(x["family"] for x in L)
    print("   per family:", dict(byfam))
    for x in rng.sample(L, 40 if QUICK else 200):
        Q = x["Q"]
        tab = [tuple(e) for e in x["table"]]
        v, cy = theorem_H(Q, tab, Q)
        want = {norm_cycle(c) for c in x["cycles"]}
        check(v == "GLOBAL" and cy == want, f"typeb {x['family']} {x['index']}: {v} {cy} vs {want}")
        bc, bad = brute_cycles(Q, tab, 20000 if Q <= 16 else 5000)
        check(bc == want and not bad, f"typeb brute {x['index']} {bc} vs {want}")
        recs, _, lab = classify(Q, tab, Q)
        for b in x["b"]:
            A, B = Fr(1), Fr(0)
            for r in b["cycle"]:
                u, vv, w = tab[r]
                A, B = A * u / w, (B * u + vv) / w
            check(B / (1 - A) == Fr(b["xstar"]), f"typeb x* {x['index']}")


# ---------------------------------------------------------------------------- I
def section_I():
    print("== I: catalog", flush=True)
    rng = random.Random(11)
    d = json.load(open(os.path.join(HERE, "out", "catalog_sweep.json")))
    R = d["records"]
    check(len(R) == 540, f"540 tables, got {len(R)}")
    rows = json.load(open(os.path.join(HERE, "out", "catalog_rows.json")))
    from collections import Counter
    st = Counter(r["st"] for r in rows)
    print("   status labels:", dict(st))
    # open records have a (c) SCC at base level
    nopen = 0
    for rec, row in zip(R, rows):
        assert rec["ids"] == row["ids"]
        if row["st"] in ("OPEN", "OPEN-CLS"):
            Q = rec["Q"]
            tab = [tuple(e) for e in rec["table"]]
            if Q > 700:
                continue
            ts = types_str(classify(Q, tab, Q)[0])
            check("c" in ts, f"open {rec['ids'][0]} base types {ts}")
            check(theorem_H(Q, tab, Q, lo=0 if rec["zero"] else 1)[0] == "NONE",
                  f"open {rec['ids'][0]} settled by own H'?")
            nopen += 1
    print("   open records with a (c) SCC at base level:", nopen, " open-CLS:", st.get("OPEN-CLS"))
    # sample of re-settled GLOBAL records
    glob = [(rec, row) for rec, row in zip(R, rows) if str((rec.get("result") or {}).get("H", "")).startswith("GLOBAL")]
    print("   GLOBAL-by-H' records:", len(glob))
    for rec, row in rng.sample(glob, min(len(glob), 25 if QUICK else 80)):
        res = rec["result"]
        K = int(res["H"].split("K=")[1].split()[0])
        Q = rec["Q"]
        tab = [tuple(e) for e in rec["table"]]
        lo = 0 if rec["zero"] else 1
        if K > 700:
            continue
        v, cy = theorem_H(Q, tab, K, lo=lo)
        want = {norm_cycle(c) for c in res["H_cycles"]}
        check(v == "GLOBAL" and cy == want, f"catalog {rec['ids'][0]} K={K}: own {v} {sorted(cy)[:4] if v == 'GLOBAL' else cy} vs {sorted(want)[:4]}")
        bc, bad = brute_cycles(Q, tab, 20000 if Q <= 64 else 4000, lo=lo)
        check(bc <= want and not bad, f"catalog brute {rec['ids'][0]} {sorted(bc)[:4]} vs {sorted(want)[:4]}")
        check(row["st"] in ("yes", "n/a"), f"catalog settled record label {row['st']} {rec['ids'][0]}")
    # coverage: classify the 38 OPEN-CLS tables
    cov = Counter()
    for rec, row in zip(R, rows):
        if row["st"] != "OPEN-CLS":
            continue
        Q = rec["Q"]
        tab = [tuple(e) for e in rec["table"]]
        markov = all(math.gcd(u, Q) == 1 and Q % w == 0 for u, v, w in tab)
        ps = primes_of(Q)
        if markov and len(ps) == 1 and Q == ps[0] and not has_divfree(Q, tab, Q):
            cov["PropP"] += 1
        elif Q == 4 and tab[0] == (1, 0, 2) and tab[2] == (1, 0, 2) and tab[1][2] == 1 and tab[3][2] == 1 \
                and not has_divfree(Q, tab, Q):
            cov["Prop4"] += 1
        elif all(Q % (p * p) for p in ps) and len(ps) > 1 and all(
                (tab[r] == (1, 0, next(p for p in ps if r % p == 0)) if math.gcd(r, Q) > 1 else
                 (tab[r][2] == 1 and math.gcd(tab[r][0], Q) == 1)) for r in range(Q)):
            cov["ThmS"] += 1
        else:
            cov["none:" + row["ids"][0].split("@")[0]] += 1
    print("   coverage of OPEN-CLS tables:", dict(cov))
    check(sum(cov.values()) == 38, "38 OPEN-CLS tables")
    check(cov["PropP"] + cov["Prop4"] == 29 and cov["ThmS"] == 3, f"coverage 29 + 3: {dict(cov)}")


# ---------------------------------------------------------------------------- J
def section_J():
    print("== J: Theorem C6 corollaries", flush=True)
    us = [1, 5, 7, 11, 13, 17, 25]
    n = 0
    for u1 in us:
        for u5 in us:
            for v1 in range(-5, 7):
                for v5 in range(-5, 7):
                    if u1 + v1 < 1 or 5 * u5 + v5 < 1:
                        continue
                    Q, t = raw_div(6, {1: (u1, v1, 1), 5: (u5, v5, 1)})
                    k, _ = member_class(Q, t)
                    if k == "CERT":
                        check(u1 in (1, 5) and u5 in (1, 5), f"C6: certificate with u1={u1}, u5={u5}")
                    if u1 == u5 == 5:
                        s1, s5 = (u1 + v1) % 6, (5 * u5 + v5) % 6
                        check((k == "CERT") == (s1 == 0 and s5 == 0), f"C6: (5,5) v1={v1} v5={v5} -> {k}")
                    n += 1
    print("   D6 members checked:", n)


def section_K():
    print("== K: mixed-modulus type-(b) tables and the non-Markov mixedbase records", flush=True)
    import ast
    M = [(6, [(7, -4, 2), (1, 3, 1), (13, -2, 3), (13, 5, 1), (1, -2, 2), (13, -5, 1)]),
         (10, [(1, 5, 1), (11, -2, 1), (1, -1, 1), (9, 3, 2), (7, -6, 1), (1, 5, 2), (11, 4, 1),
               (11, -1, 2), (3, 3, 1), (3, 3, 2)])]
    for line in open(os.path.join(HERE, "out", "typeb_mixed_examples.txt")):
        M.append(ast.literal_eval(line))
    qs = set()
    for Q, tab in M:
        markov = all(math.gcd(u, Q) == 1 and Q % w == 0 for u, v, w in tab)
        check(markov, f"mixed example Q={Q} not Markov")
        ts = types_str(classify(Q, tab, Q)[0])
        check(ts == "ab", f"mixed example Q={Q} types {ts}")
        v, cy = theorem_H(Q, tab, Q)
        bc, bad = brute_cycles(Q, tab, 20000 if not QUICK else 3000)
        check(v == "GLOBAL" and cy == bc and not bad, f"mixed example Q={Q}: {v} {cy} vs brute {bc}")
        qs.add(Q)
    print("   mixed examples:", len(M), "moduli", sorted(qs))
    d = json.load(open(os.path.join(HERE, "out", "catalog_sweep.json")))
    nmb = 0
    for rec in d["records"]:
        nm = rec["ids"][0].split("@")[0]
        res = rec.get("result") or {}
        if nm.startswith("mb_") and str(res.get("H", "")).startswith("GLOBAL") and not res.get("markov"):
            K = int(res["H"].split("K=")[1].split()[0])
            Q = rec["Q"]
            tab = [tuple(e) for e in rec["table"]]
            lo = 0 if rec["zero"] else 1
            recs = classify(Q, tab, K)[0]
            v, cy = theorem_H(Q, tab, K, lo=lo)
            want = {norm_cycle(c) for c in res["H_cycles"]}
            check(types_str(recs) == "a" and v == "GLOBAL" and cy == want,
                  f"{nm} K={K}: {types_str(recs)} {v} {cy} vs {want}")
            bc, bad = brute_cycles(Q, tab, 20000 if not QUICK else 3000, lo=lo)
            check(bc <= want and not bad, f"{nm} brute {bc}")
            nmb += 1
    print("   non-Markov mixedbase records re-settled by H' (own check):", nmb)
    check(nmb == 14, f"14 mixedbase records expected, got {nmb}")


if __name__ == "__main__":
    random.seed(1)
    for sec in [section_A, section_B, section_C, section_D, section_E, section_F, section_G, section_H,
                section_I, section_J, section_K]:
        try:
            sec()
        except AssertionError as e:
            check(False, f"{sec.__name__} raised {e!r}")
    print("FAILURES:", len(FAILS))
    sys.exit(1 if FAILS else 0)
