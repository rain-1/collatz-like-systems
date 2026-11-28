"""Exact checks for round6/countlaw_wide.  Exits 0 iff every check passes; each part can fail.

 1. digit automaton and DP survivor counts |R_b| against an independent brute force that runs p^k lifts of
    every residue in parallel and applies a step only while all lifts use the same row (all systems).
 2. cw gfun against the DP (|R_b| by both), all systems.
 3. Theorem R_G: L <= N(p^m, m+j) <= U against brute-force counts, and sum Cnt*|S| = |R_{m+j}|
    (14 systems, 1452 cases); Lemma T_G node by node; mutation: replacing the multiplier g^A by g^(A+1) must break the bracket.
 4. Lemma F_G constant: the index iota_L = [(Z/p^L)^*: <g>] is constant for L from its stabilisation point
    to L = 20, and equals the closed form; Lemma F_G inequality checked exactly on small cases.
 5. Lemma P_G data: G, the rescue condition (P) (B acyclic, or every simple cycle in B strictly contracting,
    and every B state reaches G), and m_GG(K) >= 1 for K0 <= K < 2 K0 at K0 = 40 (positivity used in the
    supermultiplicative iteration).
 6. Lemma B1 data for the systems with (Pot): the relabelling identity re-verified exactly on every
    transition, and an explicit surviving buffer word w0 with log slope >= Delta + dip, exactly.
 7. Lemma X (slope survival = actual survival): exact list of exceptional octaves m <= 3000 for every system,
    and brute force on all n in [p^{m-1}, p^m) for small m: outside the flagged octaves the two counts agree
    for every b <= m + 4.
 8. Theorem U'_G: cw uprime against a naive Python evaluation of the definition (two systems, small L), and
    reproduction of the round-5 fourier constants for 3x+1 at L = 14.
 9. (added after REFEREE1) Theorem R_G for 3x+1 at m = 1000, K = 24, j = 1..8 against the round-5
    certificates round5/microrange/data/certified_siblings.txt (d = 1 rows): the rounded relative errors
    must agree to the printed 5 decimals.
"""
import os, sys, math, itertools, subprocess, tempfile, random
from fractions import Fraction
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cwlib
from cwlib import System, SYS, index_of_g, log_exact
import cert
import cwconst

FAILS = []


def ok(cond, msg):
    if not cond:
        FAILS.append(msg)
        print("FAIL:", msg, flush=True)


# ---------------------------------------------------------------------------------------------------- 1
def brute_R(S, b):
    p, Q = S.p, S.Q
    cnt = 0
    for r in range(p ** b):
        xs = [r + p ** b * j for j in range(Q)]
        A = E = 0
        alive = True
        while True:
            rows = [S.rows[x % Q] for x in xs]
            if any(rw != rows[0] for rw in rows):
                break
            u, v, e = rows[0]
            xs = [(u * x + v) // p ** e for x in xs]
            A += log_exact(S.g, u)
            E += e
            if S.g ** A < p ** E:
                alive = False
                break
        cnt += alive
    return cnt


def part1():
    for name in SYS:
        S = System(name)
        b = 9 if S.p == 2 else 6
        sc = S.surv_counts(b)
        for bb in range(b + 1):
            ok(sc[bb] == brute_R(S, bb), f"part1 {name} b={bb}")
    print("part 1 done", flush=True)


def part2():
    for name in SYS:
        S = System(name)
        b = 16 if S.p == 2 else 10
        ok(int(cert.cont_set(S, S.root, 0, 0, b).sum()) == S.surv_counts(b)[b], f"part2 {name}")
    print("part 2 done", flush=True)


# ---------------------------------------------------------------------------------------------------- 3
def part3():
    names = ["3x+1", "3x-1", "3x+5", "K7", "sf3_7", "sf3_57", "sf3_13", "split5_1", "split5_3",
             "desc_split7_1", "desc_s32_plus9", "m3_b", "m3_g", "desc_m3_4n5"]
    tot = 0
    for name in names:
        S = System(name)
        p = S.p
        ms = [12, 15, 18] if p == 2 else [7, 9, 11]
        Kmax = 12 if p == 2 else 8
        for m in ms:
            for j in range(1, 5):
                for K in range(j + 1, Kmax + 1):
                    if m + j - K < 0:
                        continue
                    d = m + j - K
                    c = S.dp(d, keep={d})[d]
                    Lo, Up, mean, nt = cert.bracket(S, m, j, K, c)
                    Nb = cert.brute_N(S, m, m + j)
                    tot += 1
                    ok(Lo <= Nb <= Up, f"part3 {name} m={m} j={j} K={K}: {Lo} {Nb} {Up}")
                    ok(mean == S.surv_counts(m + j)[m + j], f"part3 identity {name} {m} {j} {K}")
    print(f"part 3: {tot} bracket cases", flush=True)
    # Lemma T_G node by node (exact identity, with the true intercept), and a mutation test
    broke = 0
    cases = 0
    for name in ["3x+1", "3x-1", "K7", "sf3_57", "split5_3", "desc_s32_plus9", "m3_b", "desc_m3_4n5"]:
        S = System(name)
        p = S.p
        for (d, K) in ([(9, 6), (11, 5)] if p == 2 else [(5, 4), (6, 3)]):
            j = 2
            Rfull = cert.cont_set(S, S.root, 0, 0, d + K)
            am = cert.amin_array(S, d + K + S.k + 2)
            for r in range(p ** d):
                steps, s_, c_ = S.chain(d, r)
                if not S.passes(0, 0, steps):
                    continue
                x = r
                for _ in steps:
                    u_, v_, e_ = S.rows[x % S.Q]
                    x = (u_ * x + v_) // p ** e_
                A, E = (steps[-1] if steps else (0, 0))
                mask = cert.cont_set(S, (s_, c_), A, E, K, am)
                Bint = (x // p ** s_) % p ** K
                for mult, tag in ((pow(S.g, A, p ** K), "true"), (pow(S.g, A + 1, p ** K), "mut")):
                    lhs = sum(1 for t in range(p ** (K - j)) if mask[(mult * t + Bint) % p ** K])
                    rhs = sum(1 for t in range(p ** (K - j)) if Rfull[r + p ** d * t])
                    if tag == "true":
                        cases += 1
                        ok(lhs == rhs, f"part3 Lemma T_G {name} d={d} K={K} r={r}: {lhs} vs {rhs}")
                    else:
                        broke += lhs != rhs
    ok(broke > 0, "part3 mutation (multiplier g^(A+1)) was not detected")
    print(f"part 3: Lemma T_G exact on {cases} nodes; the wrong multiplier g^(A+1) breaks {broke} of them", flush=True)


# ---------------------------------------------------------------------------------------------------- 4
def iota_closed(p, g):
    if p == 2:
        if g % 4 == 1:
            return 2 ** (len(bin((g - 1) & -(g - 1))) - 4)      # 2^{v2(g-1) - 1}
        v = 0
        x = g * g - 1
        while x % 2 == 0:
            x //= 2
            v += 1
        return 2 ** (v - 2)
    o = 1
    while pow(g, o, p) != 1:
        o += 1
    w = 0
    x = g ** o - 1
    while x % p == 0:
        x //= p
        w += 1
    return (p - 1) // o * p ** (w - 1)


def lemmaF_exact(p, K, j, S, g):
    Q = p ** K
    N = p ** (K - j)
    H = []
    u = 1
    while True:
        H.append(u)
        u = u * g % Q
        if u == 1:
            break
    tot = Fraction(0)
    for u in H:
        best = 0
        for B in range(Q):
            phi = sum(1 for t in range(N) if (u * t + B) % Q in S)
            best = max(best, abs(Fraction(phi) - Fraction(N * len(S), Q)))
        tot += best
    lhs = tot / len(H)
    iota = max(index_of_g(p, g, L)[0] for L in range(1, K + 1))
    GK = iota * p / (p - 1) * (1 + K * math.log(p))
    rhs = GK * math.sqrt(len(S) * (1 - len(S) / Q))
    return float(lhs), rhs


def part4():
    for (p, g) in [(2, 3), (2, 5), (2, 7), (3, 4), (3, 5), (3, 7), (3, 2), (2, 9)]:
        idx = [index_of_g(p, g, L)[0] for L in range(1, 21)]
        ok(idx[-1] == iota_closed(p, g), f"part4 closed form iota p={p} g={g}: {idx[-1]} vs {iota_closed(p, g)}")
        ok(max(idx) == idx[-1] and idx[-6:] == [idx[-1]] * 6, f"part4 iota stabilises p={p} g={g}: {idx}")
    random.seed(1)
    worst = 0
    for (p, g, K) in [(2, 3, 7), (2, 5, 7), (3, 4, 4), (3, 2, 4), (2, 7, 7)]:
        Q = p ** K
        for j in (1, 2):
            for trial in range(3):
                S = set(random.sample(range(Q), random.randint(1, Q - 1)))
                lhs, rhs = lemmaF_exact(p, K, j, S, g)
                ok(lhs <= rhs, f"part4 Lemma F_G p={p} g={g} K={K} j={j}")
                worst = max(worst, lhs / rhs)
    print(f"part 4 done (Lemma F_G: largest lhs/rhs = {worst:.3f})", flush=True)


# ---------------------------------------------------------------------------------------------------- 5
def gg_counts(S, G, depth):
    """for every start state in G: list over K = 0..depth of #{z in All_K(sigma,1) whose path ends in G}"""
    out = {}
    for st in G:
        res = S.dp(depth, start=st)
        out[st] = [sum(c for (s1, A), c in r.items() if s1 in G) for r in res]
    return out


def simple_cycles(succ, nodes):
    cyc = []
    nodes = sorted(nodes)
    for i, s in enumerate(nodes):
        allowed = set(nodes[i:])
        stack = [(s, [s])]
        while stack:
            v, path = stack.pop()
            for w in succ[v]:
                if w == s:
                    cyc.append(path[:])
                elif w in allowed and w not in path:
                    stack.append((w, path + [w]))
    return cyc


def part5():
    K0 = 40
    for name in SYS:
        S = System(name)
        ms, G, r = cwconst.mstar(S, K0)
        B = [s for s in S.states1 if s not in G]
        ok(len(G) > 0, f"part5 {name}: G empty")
        # every B state reaches G
        for b in B:
            seen, todo = {b}, [b]
            reach = False
            while todo:
                v = todo.pop()
                for (w, steps) in S.trans[v]:
                    if w in G:
                        reach = True
                    elif w not in seen:
                        seen.add(w)
                        todo.append(w)
            ok(reach, f"part5 {name}: B state {b} does not reach G")
        if r is None:
            # every simple cycle inside B strictly contracting (exact)
            succ = {}
            lab = {}
            for v in B:
                succ[v] = []
                for (w, steps) in S.trans[v]:
                    if w in B:
                        succ[v].append(w)
                        a, e = (steps[-1] if steps else (0, 0))
                        lab.setdefault((v, w), []).append((a, e))
            for cyc in simple_cycles(succ, B):
                edges = list(zip(cyc, cyc[1:] + cyc[:1]))
                for choice in itertools.product(*[lab[ed] for ed in edges]):
                    a = sum(x for x, y in choice)
                    e = sum(y for x, y in choice)
                    ok(S.g ** a < S.p ** e, f"part5 {name}: non-contracting cycle in B {cyc}")
        cnt = gg_counts(S, G, 2 * K0)
        mn = [min(cnt[st][K] for st in G) for K in range(2 * K0 + 1)]
        ok(all(x >= 1 for x in mn[K0:2 * K0]), f"part5 {name}: m_GG(K) = 0 for some K in [K0, 2K0)")
        # supermultiplicativity spot check
        for K1 in (5, 11, 17):
            for K2 in (7, 13):
                ok(mn[K1 + K2] >= mn[K1] * mn[K2], f"part5 {name}: supermultiplicativity {K1} {K2}")
    print("part 5 done", flush=True)


# ---------------------------------------------------------------------------------------------------- 6
def part6():
    for name in SYS:
        S = System(name)
        pot = cwconst.potential(S)
        if pot is None:
            continue
        mv = S.digit_moves()
        f = pot["f"]
        phi = {eval(k): v for k, v in pot["phi"].items()}
        perm = {eval(k): v for k, v in pot["perm"].items()}
        for s in S.states1:
            for dl in range(S.p):
                (s1, a, e) = mv[s][perm[s][dl]]
                ok((Fraction(a), Fraction(e)) == (f[dl][0] + phi[s1][0] - phi[s][0], f[dl][1] + phi[s1][1] - phi[s][1]),
                   f"part6 {name}: potential identity")
        # Delta and dip as (a, e) vectors compared via logs exactly: x = a log g - e log p
        def val(ae):
            return ae[0] * math.log(S.g) - ae[1] * math.log(S.p)
        vals = [val(v) for v in phi.values()]
        Delta = max(vals) - min(vals)
        dip = 0.0
        for s in S.states1:
            for (s1, steps) in S.trans[s]:
                for (a, e) in steps:
                    dip = max(dip, -val((a, e)))
        need = Delta + dip
        # find a surviving buffer word from the root with log slope >= need: search the DP for the least depth
        found = None
        for depth in range(1, 200):
            c = S.dp(depth, keep={depth})[depth]
            for (st, A), n in c.items():
                E = depth - st[0]
                # exact test g^A >= p^E * exp(need): use a rational upper bound of exp(need) via integers
                # need = alpha log g - beta log p with rationals; compare g^(A*D - aD) >= p^(E*D - bD) exactly
                if A * math.log(S.g) - E * math.log(S.p) >= need + 1e-9:
                    found = (depth, st, A, E)
                    break
            if found:
                break
        ok(found is not None, f"part6 {name}: no buffer word")
        # exact confirmation of the found inequality (Delta, dip are sums of terms a log g - e log p: rebuild)
        if found:
            depth, st, A, E = found
            # Delta + dip as an explicit rational combination: recompute exactly
            phis = list(phi.values())
            hi = max(phis, key=val)
            lo = min(phis, key=val)
            dipv = (0, 0)
            for s in S.states1:
                for (s1, steps) in S.trans[s]:
                    for (a, e) in steps:
                        if -val((a, e)) > -val(dipv) + 0 and -val((a, e)) > 0:
                            dipv = (a, e)
            # need = (hi - lo) - dipv  in (a, e) coordinates
            na = hi[0] - lo[0] - dipv[0]
            ne = hi[1] - lo[1] - dipv[1]
            D = 1
            for x in (na, ne):
                D = D * Fraction(x).denominator // math.gcd(D, Fraction(x).denominator)
            # A log g - E log p >= na log g - ne log p  <=>  g^{(A - na) D} >= p^{(E - ne) D}
            ea, ee = (A - na) * D, (E - ne) * D
            ea, ee = int(ea), int(ee)
            lhs = S.g ** ea if ea >= 0 else Fraction(1, S.g ** (-ea))
            rhs = S.p ** ee if ee >= 0 else Fraction(1, S.p ** (-ee))
            ok(lhs >= rhs, f"part6 {name}: buffer inequality not exact")
            print(f"  {name}: (Pot) holds; Delta+dip = {need:.4f}; buffer word of length {depth}", flush=True)
    print("part 6 done", flush=True)


# ---------------------------------------------------------------------------------------------------- 7
def tau(S):
    return max(len(steps) for st in S.states for (s1, steps) in S.trans[st])


def exceptional_octaves(S, mmax, c=2.0):
    """octaves m in [10, mmax] for which some (A, E) with 1 <= E <= m + c log_p m + k has
    0 < |g^A/p^E - 1| < 5 t V / p^{m-1}, t = tau*(m + c log_p m + k) (exact integers), or 8 t V > p^{m-1}"""
    p, g = S.p, S.g
    t_ = tau(S)
    bad = set()
    Emax = int(mmax + c * math.log(mmax, p)) + S.k + 2
    # candidate pairs: for each E the A nearest to E log_g p (two neighbours)
    lam = math.log(p) / math.log(g)
    pairs = []
    for E in range(1, Emax + 1):
        A0 = int(E * lam)
        for A in (A0 - 1, A0, A0 + 1, A0 + 2):
            if A >= 0:
                pairs.append((A, E))
    for m in range(10, mmax + 1):
        bmax = int(m + c * math.log(m, p)) + S.k
        tt = t_ * bmax
        if 8 * tt * S.V > p ** (m - 1):
            bad.add(m)
            continue
    # the condition |g^A - p^E| * p^{m-1} < 4 tt V p^E  ; for fixed (A, E) it holds for m <= some m0
    for (A, E) in pairs:
        diff = abs(g ** A - p ** E)
        if diff == 0:
            continue
        # m from max(10, E - c log E - k) to mmax with E <= bmax(m)
        for m in range(max(10, E - int(c * math.log(mmax, p)) - S.k - 2), mmax + 1):
            bmax = int(m + c * math.log(m, p)) + S.k
            if E > bmax:
                continue
            tt = t_ * bmax
            if diff * p ** (m - 1) < 5 * tt * S.V * p ** E:
                bad.add(m)
            else:
                break
    return sorted(bad)


def actual_vs_slope(S, m, b):
    """number of n in [p^{m-1}, p^m) where slope survival and actual survival over b digits differ"""
    mask = cert.cont_set(S, S.root, 0, 0, b) if S.p ** b <= 2 ** 26 else None
    diff = 0
    for n in range(S.p ** (m - 1), S.p ** m):
        sl = bool(mask[n % S.p ** b]) if mask is not None else S.node_survives(n, b)
        ac = S.node_survives_actual(n, b)
        diff += sl != ac
    return diff


def part7():
    import json
    allbad = {}
    for name in SYS:
        S = System(name)
        if not S.H0:
            print(f"  {name}: hypothesis H0 fails")
            continue
        bad = exceptional_octaves(S, 3000)
        allbad[name] = bad
        print(f"  {name}: exceptional octaves m in [10, 3000]: {bad[:12]}{' ...' if len(bad) > 12 else ''} "
              f"(count {len(bad)})", flush=True)
        mm = 16 if S.p == 2 else 10
        for m in range(4, mm + 1):
            for b in range(m, m + 5):
                dd = actual_vs_slope(S, m, b)
                if m >= 10 and m not in bad:
                    ok(dd == 0, f"part7 {name}: m={m} b={b}: {dd} disagreements in an unflagged octave")
    json.dump(allbad, open(os.path.join(HERE, "data", "exceptional_octaves.json"), "w"))
    print("part 7 done", flush=True)


# ---------------------------------------------------------------------------------------------------- 8
def naive_uprime(S, L, m):
    p, g = S.p, S.g
    N = p ** L
    best = Fraction(0)
    units = []
    u = 1
    while True:
        units.append(u)
        u = u * g % N
        if u == 1:
            break
    for st in sorted(set(S.states1) | {S.root}):
        # independent evaluation of the minimum prefix slope by direct simulation in Python
        gv = []
        for z in range(N):
            steps, s1, c1 = S.chain(st[0] + L, st[1] + p ** st[0] * z)
            best_sl = Fraction(1)
            for (a, e) in steps:
                best_sl = min(best_sl, Fraction(g ** a, p ** e))
            gv.append(best_sl)
        levels = sorted(set(gv))
        for gam in levels[1:]:
            Sset = [z for z in range(N) if gv[z] >= gam]
            sz = len(Sset)
            W = N // p ** m
            for w in units:
                ind = [0] * N
                for z in Sset:
                    ind[w * z % N] = 1
                for c in range(N):
                    C = sum(ind[(c + y) % N] for y in range(W))
                    best = max(best, abs(Fraction(C * p ** m, sz) - 1))
    return best


def part8():
    import everyoct
    for name, L in [("K7", 7), ("m3_b", 4), ("sf3_57", 6)]:
        S = System(name)
        fast = everyoct.uprime(S, L, 2)
        for m in (1, 2):
            nv = naive_uprime(S, L, m)
            ok(fast[m] == nv, f"part8 {name} L={L} m={m}: {fast[m]} vs naive {nv}")
    S = System("3x+1")
    best = everyoct.uprime(S, 14, 3)
    ok((best[1], best[2], best[3]) == (Fraction(213, 1627), Fraction(213, 749), Fraction(349, 749)),
       f"part8 3x+1 L=14 does not reproduce round5/fourier U': {best}")
    print("part 8 done", flush=True)


# ---------------------------------------------------------------------------------------------------- 9
def part9():
    ref = os.path.join(HERE, "..", "..", "round5", "microrange", "data", "certified_siblings.txt")
    rows = {}
    for line in open(ref):
        f = line.split()
        if len(f) == 6 and f[0] == "1" and f[1] == "1000":
            rows[int(f[2])] = (float(f[4]), float(f[5]))
    ok(sorted(rows) == list(range(1, 9)), "part9: could not read the d = 1 rows of the round-5 file")
    S = System("3x+1")
    m, K = 1000, 24
    ds = {m + j - K for j in rows} | {m + j for j in rows}
    allc = S.dp(max(ds), keep=ds)
    for j, (rl0, ru0) in sorted(rows.items()):
        Lo, Up, mean_pj, nt = cert.bracket_fast(S, m, j, K, allc[m + j - K])
        R = sum(allc[m + j].values())
        ok(mean_pj == R, f"part9: identity fails at j={j}")
        rl = (Lo * 2 ** j - R) / R
        ru = (Up * 2 ** j - R) / R
        good = abs(rl - rl0) <= 6e-6 and abs(ru - ru0) <= 6e-6
        print(f"  3x+1 m=1000 K=24 j={j}: [{rl:+.6f}, {ru:+.6f}]  round5 [{rl0:+.5f}, {ru0:+.5f}]  {'agree' if good else 'DIFFER'}", flush=True)
        ok(good, f"part9: j={j} differs from round 5")
    print("part 9 done", flush=True)


if __name__ == "__main__":
    parts = sys.argv[1:] or ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for pnum in parts:
        globals()["part" + pnum]()
    if FAILS:
        print(f"{len(FAILS)} FAILURES")
        sys.exit(1)
    print("ALL CHECKS PASSED")
