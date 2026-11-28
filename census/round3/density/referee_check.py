"""REFEREE check for round 3 / lens "density" (independent of the prover's code).

Written from scratch by the referee.  It imports NOTHING from density_lib.py,
check_density.py or make_certificates.py.  From the prover's files it reads
only certificates.json (the numbers to be verified) and systems.py (whose step
functions are compared against the referee's own rule-text step functions).

Parts (exit 0 iff every EXACT part passes; parts marked EVIDENCE only print):
 [R1] referee step functions written from the rule text agree with the prover's
      tables on 1..30000 and on 300 random 120-bit inputs (negative-free maps).
 [R2] independent state-graph builder (Lemma 1, liberal decision rule
      w | u*a instead of the prover's w | K); Lemma 1's "children depend only
      on the state" is tested on many representatives (a = K u0, b = beta+K m);
      the graph is compared with the prover's state counts; faithful
      abstraction tested on random 150-bit n by direct iteration.
 [R3] exact stationary law, Delta, Lambda; unique closed class; c0 compared
      with the closed forms printed in results.md.
 [R4] every certificate in certificates.json: exact check N_{s,gamma} w <= w
      with the referee's own rational upper bounds (integer k-th roots), using
      the prover's w, AND a referee-constructed w; theta recomputed.
 [R5] deterministic parts of Theorems 1/4/5 on random large n (200-400 bits):
      first crossing below c_* / tau really gives an iterate < n / < n^c;
      non-exceptional n in Theorem 5 really reach an iterate > n^c.
 [R6] Theorem 6: q bounds recomputed exactly (own DP) to depth 300 and 400.
 [R7] EVIDENCE: Theorem 3 hidden hypothesis (closed class dominates rho(P_s)
      near s*); Theorem 6 density at non-block X.
Runtime: about 1-2 minutes.
"""
import json, math, os, random, sys, time
from fractions import Fraction as Fr
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
FAIL = []


def ok(c, m):
    if not c:
        FAIL.append(m)
        print("FAIL:", m, flush=True)


# ------------------------------------------------------------ [R1] maps ---
def mk_par(a, d):
    return lambda n: n // 2 if n % 2 == 0 else a * n + d


def mk_split(a, d):
    def f(n):
        if n % 2 == 0:
            return n // 2
        return a * n + d if n % 4 == 1 else n + d
    return f


def mk_div(primes, a, d):
    def f(n):
        for p in primes:
            if n % p == 0:
                return n // p
        return a * n + d
    return f


RULES = {
    "div235_7n1": mk_div((2, 3, 5), 7, 1),
    "div23_5n1": mk_div((2, 3), 5, 1),
    "div23_7n1": mk_div((2, 3), 7, 1),
    "m3_b": lambda n: n // 3 if n % 3 == 0 else ((4 * n - 1) // 3 if n % 3 == 1 else (4 * n + 1) // 3),
    "m3_d": lambda n: n // 3 if n % 3 == 0 else (4 * n + 2 if n % 3 == 1 else 4 * n + 1),
    "m3_e": lambda n: n // 3 if n % 3 == 0 else (7 * n + 2 if n % 3 == 1 else 7 * n + 1),
    "m3_g": lambda n: n // 3 if n % 3 == 0 else (5 * n + 1 if n % 3 == 1 else 5 * n + 2),
    "split5_1": mk_split(5, 1), "split5_3": mk_split(5, 3),
    "desc_m3_4n5": lambda n: n // 3 if n % 3 == 0 else (4 * n + 5 if n % 3 == 1 else 2 * n + 2),
    "desc_s32_plus9": lambda n: n // 2 if n % 2 == 0 else
    (3 * n + 1 if n % 32 not in (19, 27, 31) else n + 1),
    "desc_split7_1": mk_split(7, 1),
    "perm_1932": lambda n: [2 * (n // 3), 4 * (n // 3) + 1, 4 * (n // 3) + 3][n % 3],
    "perm_1932inv": lambda n: 3 * (n // 2) if n % 2 == 0 else
    (3 * (n // 4) + 1 if n % 4 == 1 else 3 * (n // 4) + 2),
    "perm_swap": lambda n: [2 * (n // 3), 4 * (n // 3) + 3, 4 * (n // 3) + 1][n % 3],
    "perm_b": lambda n: [4 * (n // 3), 4 * (n // 3) + 2, 2 * (n // 3) + 1][n % 3],
    "perm_c": lambda n: 3 * (n // 2) if n % 2 == 0 else
    (3 * (n // 4) + 2 if n % 4 == 1 else 3 * (n // 4) + 1),
    "perm_d": lambda n: 5 * (n // 2) if n % 2 == 0 else 5 * (n // 8) + (n % 8 + 1) // 2,
}
for a, d in [(3, 1), (3, -1), (3, 3), (3, 5), (3, 7), (3, 9), (3, 13), (3, 17), (5, 1), (5, 3),
             (5, 5), (5, 7), (5, 11), (5, 131), (5, 353), (7, 1), (7, 7), (9, 1), (6, 2), (10, 2)]:
    RULES["par_%d_%s%d" % (a, "m" if d < 0 else "", abs(d))] = mk_par(a, d)


# ------------------------------------------------- referee table + graph ---
def primes_of(Q):
    ps, x, p = [], Q, 2
    while x > 1:
        if x % p == 0:
            ps.append(p)
            while x % p == 0:
                x //= p
        p += 1
    return ps


def ppart(x, ps):
    r = 1
    for p in ps:
        while x % p == 0:
            x //= p
            r *= p
    return r


def vp(x, p):
    k = 0
    while x % p == 0:
        x //= p
        k += 1
    return k


class Map:
    """Table extracted from the referee's own step function by interpolation:
    on residue r mod Q the step is affine; recover (u, v, w) from two points
    and verify on many more."""

    def __init__(self, name, f, Q):
        self.name, self.f, self.Q, self.ps = name, f, Q, primes_of(Q)
        self.rows = []
        for r in range(Q):
            n0, n1 = r + Q, r + 2 * Q
            y0, y1 = f(n0), f(n1)
            slope = Fr(y1 - y0, Q)
            icpt = y0 - slope * n0
            den = (slope.denominator * icpt.denominator) // gcd(slope.denominator, icpt.denominator)
            u, v, w = int(slope * den), int(icpt * den), den
            for t in range(1, 60):
                n = r + Q * t
                assert f(n) * w == u * n + v, (name, r)
            self.rows.append((u, v, w))

    def row(self, x):
        return self.rows[x % self.Q]


def process(T, a, b):
    """node values a t + b; apply decided rows. returns (a, b, F, G, steps).
    Decision (referee version): all residues of a t + b mod Q give one row and
    w | u a, w | u b + v."""
    F, G, k = Fr(1), Fr(0), 0
    while True:
        g = gcd(a, T.Q)
        rows = {T.rows[x] for x in range(b % g, T.Q, g)}
        if len(rows) != 1:
            return a, b, F, G, k
        (u, v, w), = rows
        if (u * a) % w or (u * b + v) % w:
            return a, b, F, G, k
        a, b = u * a // w, (u * b + v) // w
        F, G = F * Fr(u, w), G * Fr(u, w) + Fr(v, w)
        k += 1
        if k > 5000:
            raise RuntimeError("loop")


def state_of(T, a, b):
    K = ppart(a, T.ps)
    return (K, b % K)


def split_prime(T, K):
    for q in T.ps:
        if vp(K, q) < vp(T.Q, q):
            return q
    return T.ps[0]


def children(T, a, b):
    K = ppart(a, T.ps)
    q = split_prime(T, K)
    out = []
    for e in range(q):
        a2, b2, F, G, k = process(T, q * a, b + a * e)
        out.append((state_of(T, a2, b2), F, G, k, e))
    return q, out


def build(T):
    a0, b0, F0, G0, k0 = process(T, 1, 0)
    assert k0 == 0
    root = state_of(T, 1, 0)
    states, idx, edges = [root], {root: 0}, []
    i = 0
    while i < len(states):
        K, beta = states[i]
        q = split_prime(T, K)
        # children by value residue beta + K j (BFS order identical to the
        # natural ordering of lifts j = 0..q-1)
        for j in range(q):
            a2, b2, F, G, k = process(T, K * q, (beta + K * j) % (K * q))
            st = state_of(T, a2, b2)
            if st not in idx:
                idx[st] = len(states)
                states.append(st)
                assert len(states) < 3000
            edges.append((i, idx[st], q, F, G, k))
        i += 1
    return states, idx, edges


def lemma1_test(T, states, idx, edges, rnd):
    """children multiset (state, F, G, steps) is the same for many
    representatives (a, b) = (K u0, beta + K m) of each state."""
    good = True
    for i, (K, beta) in enumerate(states):
        ref = sorted((idx[s], F, G, k) for (s, F, G, k, e) in children(T, K, beta)[1])
        mine = sorted((d, F, G, k) for (s, d, q, F, G, k) in edges if s == i)
        if ref != mine:
            good = False
        for _ in range(6):
            u0 = rnd.randrange(1, 10 ** 6)
            while gcd(u0, T.Q) != 1:
                u0 += 1
            m = rnd.randrange(0, 10 ** 12)
            ch = children(T, K * u0, beta + K * m)[1]
            got = sorted((idx.get(s, -1), F, G, k) for (s, F, G, k, e) in ch)
            if got != ref:
                good = False
    return good


def follow(T, states, idx, edges_by, n, Y=None, depth=None):
    """walk n down the referee tree; yields (depth, M, A, B, ksteps) after each split
    (including root).  Stops when M >= Y (or depth reached)."""
    M, r, a, b, st, ks, d = 1, 0, 1, 0, 0, 0, 0
    out = [(0, M, Fr(1), Fr(0), 0, a, b, r)]
    while (Y is not None and M < Y) or (depth is not None and d < depth):
        K, beta = states[st]
        q = split_prime(T, K)
        e = ((n - r) // M) % q
        a2, b2, F, G, k = process(T, q * a, b + a * e)
        s2 = state_of(T, a2, b2)
        # find the edge with that destination/F/G in the graph (consistency)
        assert any(dd == idx[s2] and FF == F and GG == G and kk == k for (dd, FF, GG, kk) in edges_by[st])
        M, r = M * q, r + M * e
        a, b, st, ks, d = a2, b2, idx[s2], ks + k, d + 1
        A = Fr(a, M)
        B = b - Fr(a * r, M)
        out.append((d, M, A, B, ks, a, b, r))
    return out


# ------------------------------------------------- exact linear algebra ---
def sccs(nv, adj):
    index, low, onst, st, res, c = {}, {}, set(), [], [], [0]
    sys.setrecursionlimit(10000)

    def dfs(v):
        index[v] = low[v] = c[0]
        c[0] += 1
        st.append(v)
        onst.add(v)
        for w in adj[v]:
            if w not in index:
                dfs(w)
                low[v] = min(low[v], low[w])
            elif w in onst:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = []
            while True:
                w = st.pop()
                onst.discard(w)
                comp.append(w)
                if w == v:
                    break
            res.append(comp)
    for v in range(nv):
        if v not in index:
            dfs(v)
    return res


def solve(A, bvec):
    n = len(A)
    M = [row[:] + [bvec[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        iv = 1 / M[c][c]
        M[c] = [x * iv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] for i in range(n)]


def logvec(x):
    x = Fr(x)
    out = {}
    for val, sgn in ((x.numerator, 1), (x.denominator, -1)):
        p = 2
        while val > 1:
            while val % p == 0:
                val //= p
                out[p] = out.get(p, 0) + sgn
            p += 1
    return out


# ------------------------------------------------- rigorous powers ---
def iroot_ceil(N, k):
    lo, hi = 0, 1 << ((N.bit_length() + k - 1) // k + 1)
    while lo < hi:
        mid = (lo + hi) // 2
        if mid ** k >= N:
            hi = mid
        else:
            lo = mid + 1
    return lo


PB = 60


def up(x, r):
    """rational U >= x^r, x>0 rational, r rational (exact integer root)."""
    x, r = Fr(x), Fr(r)
    if r == 0 or x == 1:
        return Fr(1)
    if r < 0:
        x, r = 1 / x, -r
    a, b = r.numerator, r.denominator
    num = x.numerator ** a << (PB * b)
    den = x.denominator ** a
    N = -(-num // den)
    return Fr(iroot_ceil(N, b), 1 << PB)


def lo_pow(x, r):
    x, r = Fr(x), Fr(r)
    if r == 0 or x == 1:
        return Fr(1)
    if r < 0:
        x, r = 1 / x, -r
    a, b = r.numerator, r.denominator
    N = (x.numerator ** a << (PB * b)) // x.denominator ** a
    k = iroot_ceil(N, b)
    if k ** b > N:
        k -= 1
    return Fr(k, 1 << PB)


def check_sm(edges, ns, s, gamma, w, cache):
    for i in range(ns):
        tot = Fr(0)
        for (src, dst, q, F, G, k) in edges:
            if src != i:
                continue
            key = (q, F, s, gamma)
            if key not in cache:
                cache[key] = up(q, gamma - 1) * up(F, s)
            tot += cache[key] * w[dst]
        if tot > w[i]:
            return False
    return True


def float_N(edges, ns, s, gamma):
    import numpy as np
    N = np.zeros((ns, ns))
    for (src, dst, q, F, G, k) in edges:
        N[src, dst] += float(q) ** (gamma - 1) * math.exp(s * math.log(float(F)))
    return N


def own_w(edges, ns, s, gamma):
    import numpy as np
    for slack in (0, 1e-9, 1e-7, 1e-5):
        N = float_N(edges, ns, float(s), float(gamma) + slack)
        try:
            w = np.linalg.solve(np.eye(ns) - N, np.ones(ns))
        except Exception:
            continue
        if min(w) <= 0:
            continue
        w = w / max(w)
        W = [Fr(float(x)).limit_denominator(10 ** 12) for x in w]
        if check_sm(edges, ns, Fr(s), Fr(gamma), W, {}):
            return W
    return None


def rho(edges, ns, s, gamma=0.0, comp=None):
    import numpy as np
    N = float_N(edges, ns, s, gamma)
    if comp is not None:
        N = N[np.ix_(comp, comp)]
    return float(max(abs(np.linalg.eigvals(N))))


# ---------------------------------------------------------------- closed forms
L2, L3, L5, L7 = (math.log(x) for x in (2, 3, 5, 7))
C0 = {
    "div235_7n1": 40165 * L7 / (80330 * L2 + 27334 * L3 + 14445 * L5),
    "div23_5n1": 7 * L5 / (14 * L2 + 6 * L3), "div23_7n1": 5 * L7 / (10 * L2 + 3 * L3),
    "m3_b": 4 / 3 * L2 / L3, "m3_d": 4 / 3 * L2 / L3, "m3_g": 2 / 3 * L5 / L3,
    "split5_1": L5 / L2 / 4, "split5_3": L5 / L2 / 4, "desc_m3_4n5": L2 / L3,
    "desc_s32_plus9": 22 / 67 * L3 / L2, "desc_split7_1": L7 / L2 / 6,
    "m3_e": 2 / 3 * L7 / L3, "perm_1932": 5 / 3 * L2 / L3, "perm_1932inv": 2 / 3 * L3 / L2,
    "perm_swap": 5 / 3 * L2 / L3, "perm_b": 5 / 3 * L2 / L3, "perm_c": 2 / 3 * L3 / L2,
    "perm_d": L5 / L2 / 2,
}
for k in RULES:
    if k.startswith("par_3") or k == "par_6_2":
        C0[k] = L3 / L2 / 2
    if k.startswith("par_5") or k == "par_10_2":
        C0[k] = L5 / L2 / 2
    if k.startswith("par_7"):
        C0[k] = L7 / L2 / 2
    if k == "par_9_1":
        C0[k] = L3 / L2


def ilt_pow(x, n, c):     # x < n^c exactly, c rational, x,n positive ints
    return x ** c.denominator < n ** c.numerator


def main():
    t0 = time.time()
    rnd = random.Random(7_2026_1127)
    sys.path.insert(0, HERE)
    import systems as PS                     # only for step comparison
    certs = json.load(open(os.path.join(HERE, "certificates.json")))
    QMOD = {s["id"]: s["T"].Q for s in PS.SYSTEMS}

    print("[R1] step functions")
    for S in PS.SYSTEMS:
        sid = S["id"]
        f = RULES[sid]
        good = all(f(n) == S["step"](n) for n in range(1, 30001))
        good &= all(f(n) == S["step"](n) for n in (rnd.getrandbits(120) + 1 for _ in range(300)))
        ok(good, "[R1] step mismatch " + sid)
    ok(set(RULES) == {S["id"] for S in PS.SYSTEMS}, "[R1] id sets differ")

    summary = []
    for sid in RULES:
        T = Map(sid, RULES[sid], QMOD[sid])
        states, idx, edges = build(T)
        ns = len(states)
        ok(ns == certs[sid]["states"], "[R2] state count %s %d vs %s" % (sid, ns, certs[sid]["states"]))
        ok(lemma1_test(T, states, idx, edges, rnd), "[R2] Lemma 1 representative test " + sid)
        edges_by = [[(d, F, G, k) for (s, d, q, F, G, k) in edges if s == i] for i in range(ns)]
        qs = [split_prime(T, K) for (K, b) in states]
        qmax = max(qs)
        Gmax = max(abs(e[4]) for e in edges)
        ok(str(Gmax) == certs[sid]["Gmax"], "[R2] Gmax " + sid)
        # faithful abstraction on random big n
        for _ in range(25):
            n = rnd.getrandbits(150) | 1 << 149
            path = follow(T, states, idx, edges_by, n, depth=40)
            for (d, M, A, B, ks, a, b, r) in path[::7]:
                x = n
                for _ in range(ks):
                    x = T.f(x)
                ok(x == A * n + B, "[R2] node value " + sid)
        # [R3] closed classes, stationary law, drift
        adj = [sorted({e[1] for e in edges if e[0] == i}) for i in range(ns)]
        comps = sccs(ns, adj)
        comp_of = {v: ci for ci, c in enumerate(comps) for v in c}
        closed = [c for c in comps if all(comp_of[w] == comp_of[c[0]] for v in c for w in adj[v])]
        ok(len(closed) == 1, "[R3] closed classes %s: %d" % (sid, len(closed)))
        C = sorted(closed[0])
        pos = {v: i for i, v in enumerate(C)}
        m = len(C)
        P = [[Fr(0)] * m for _ in range(m)]
        for (s_, d_, q, F, G, k) in edges:
            if s_ in pos:
                P[pos[s_]][pos[d_]] += Fr(1, q)
        # pi P = pi, sum pi = 1
        A = [[P[j][i] - (1 if i == j else 0) for j in range(m)] for i in range(m)]
        A[-1] = [Fr(1)] * m
        rhs = [Fr(0)] * (m - 1) + [Fr(1)]
        pi = solve(A, rhs)
        ok(all(x > 0 for x in pi), "[R3] pi positive " + sid)
        Dv, Lv = {}, {}
        for (s_, d_, q, F, G, k) in edges:
            if s_ in pos:
                for p, e in logvec(F).items():
                    Dv[p] = Dv.get(p, 0) + pi[pos[s_]] * Fr(e, q)
        for v in C:
            q = qs[v]
            Lv[q] = Lv.get(q, 0) + pi[pos[v]]
        ok({str(k): str(v) for k, v in Dv.items() if v != 0} ==
           {k: v for k, v in certs[sid]["Delta"].items() if Fr(v) != 0}, "[R3] Delta dict " + sid)
        Df = sum(float(c) * math.log(p) for p, c in Dv.items())
        Lf = sum(float(c) * math.log(p) for p, c in Lv.items())
        c0 = 1 + Df / Lf
        ok(abs(c0 - C0[sid]) < 1e-12, "[R3] c0 %s %.10f vs closed form %.10f" % (sid, c0, C0[sid]))

        # [R4] certificates
        rec = certs[sid]
        cache = {}
        for kind in ("never_drop", "korec", "korec_sharp", "expanding"):
            if kind not in rec:
                continue
            Cc = rec[kind]
            s, gm, c = Fr(Cc["s"]), Fr(Cc["gamma"]), Fr(Cc["c"])
            w = [Fr(x) for x in Cc["w"]]
            ok(len(w) == ns and min(w) > 0, "[R4] w " + sid)
            ok(check_sm(edges, ns, s, gm, w, cache), "[R4] prover w fails %s %s" % (sid, kind))
            W = own_w(edges, ns, s, gm)
            ok(W is not None, "[R4] referee w not found %s %s" % (sid, kind))
            th = 1 - gm + s * (1 - c)
            ok(th == Fr(Cc["theta"]) and th < 1, "[R4] theta " + sid)
            sign_ok = {"never_drop": s > 0 and c == 1 and 0 <= gm <= 1,
                       "korec": s > 0 and c0 < c < 1 and 0 <= gm <= 1,
                       "korec_sharp": s < 0 and c < c0 < 1 and gm + (c - 1) * s > 0,
                       "expanding": s < 0 and 1 < c < c0 and 0 <= gm <= 1}[kind]
            ok(sign_ok, "[R4] parameter ranges %s %s" % (sid, kind))
        # [R5] deterministic parts on random big n
        for kind in ("never_drop", "korec", "expanding"):
            if kind not in rec:
                continue
            c = Fr(rec[kind]["c"])
            hits = 0
            for _ in range(12):
                bits = rnd.choice([200, 300, 400])
                n = rnd.getrandbits(bits) | (1 << (bits - 1))
                Y = 1 << (bits - 1)
                path = follow(T, states, idx, edges_by, n, Y=Y)
                if kind == "never_drop":
                    hit = next((p for p in path if p[2] < Fr(1, 2)), None)
                    if hit:
                        x = n
                        for _ in range(hit[4]):
                            x = T.f(x)
                        ok(x < n and x == hit[2] * n + hit[3], "[R5] Thm1 %s" % sid)
                        hits += 1
                elif kind == "korec":
                    tau = lo_pow(Fr(2 * Y), c - 1) / 2
                    hit = next((p for p in path if p[2] < tau), None)
                    if hit:
                        x = n
                        for _ in range(hit[4]):
                            x = T.f(x)
                        ok(ilt_pow(x, n, c), "[R5] Thm4 %s" % sid)
                        hits += 1
                else:
                    cut = path[-1]
                    sp = -Fr(rec[kind]["s"])
                    th1 = Fr(rec[kind]["theta"])
                    eps = Fr(math.floor(float((1 - th1) / sp) * 1000) - 1, 1000)
                    tau = 4 * up(Fr(2 * Y), c - 1)
                    dip = up(Fr(Y), -eps)
                    if cut[2] >= tau and all(p[2] >= dip for p in path):
                        x = n
                        for _ in range(cut[4]):
                            x = T.f(x)
                        ok(x ** c.denominator > n ** c.numerator, "[R5] Thm5 %s" % sid)
                        hits += 1
            summary.append((sid, kind, hits))
        # [R6] early-drop q
        if "early_drop" in rec:
            ok(ns == 1, "[R6] single state expected")
            E = rec["early_drop"]
            s = Fr(E["s"])
            Fs = [e[3] for e in edges]
            p = edges[0][2]
            Us = {F: up(F, s) for F in Fs}
            ok(sum(Us[F] for F in Fs) / p <= 1, "[R6] supermartingale q " + sid)
            for L in (300, 400):
                # DP over log-slope exponent vector
                cur = {(): 1}
                vecs = [tuple(sorted(logvec(F).items())) for F in Fs]
                cur = {Fr(1): 1}
                lo = Fr(0)
                for i in range(1, L + 1):
                    nxt = {}
                    killed = 0
                    for A, cnt in cur.items():
                        for F in Fs:
                            A2 = A * F
                            if A2 < 1:
                                killed += cnt
                            else:
                                nxt[A2] = nxt.get(A2, 0) + cnt
                    lo += Fr(killed, p ** i)
                    cur = nxt
                # tail: P(cross later | A) <= A^s (single state, w const); A^s bound
                tail = Fr(0)
                for A, cnt in cur.items():
                    tail += cnt * up(A, s)
                hi = lo + tail / p ** L
                print("   %-12s q in [%.6f, %.6f] (depth %d)" % (sid, float(lo), float(hi), L), flush=True)
                if L == 300:
                    ok(float(lo) >= E["q_lo"] - 1e-3 and float(hi) <= E["q_hi"] + 1e-3, "[R6] q " + sid)
                    summary.append((sid, "q300", (float(lo), float(hi))))
                else:
                    summary.append((sid, "q400", (float(lo), float(hi))))
        print("  %-15s states=%-3d c0=%.6f  (%.1fs)" % (sid, ns, c0, time.time() - t0), flush=True)

        # [R7] EVIDENCE: Theorem 3 closed-class dominance
        if len(set(qs)) == 1 and Df < 0 and ns > 1:
            import numpy as np
            best = min((rho(edges, ns, s_), s_) for s_ in np.linspace(0.01, 6, 600))
            sstar = best[1]
            rC = rho(edges, ns, sstar, comp=C)
            print("   [R7] %s: s*=%.3f rho_full=%.6f rho_closed=%.6f (transient states %d)"
                  % (sid, sstar, best[0], rC, ns - len(C)))
            summary.append((sid, "domin", (best[0], rC)))

    print("\nsummary of random large-n hits:", [x for x in summary if isinstance(x[2], int)])
    print("total %.1fs" % (time.time() - t0))
    if FAIL:
        print("%d FAILURES" % len(FAIL))
        sys.exit(1)
    print("REFEREE CHECKS PASSED")


if __name__ == "__main__":
    main()
