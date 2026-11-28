#!/usr/bin/env python3
"""REFEREE 1 independent check for census/round6/countlaw_wide.  Written from scratch by the referee.

Sections A-J use only this file (own engine, own systems from the census rule strings, own DP, own brackets,
own U' constants, own Diophantine scan).  Section Z imports the prover's modules ONLY to compare their
numbers with ours.  Exit code 0 iff every check passes; every check can fail (mutation tests included).

usage:  python referee1_check.py            (all sections, ~10-20 min)
        python referee1_check.py A C F      (selected sections)
"""
import sys, os, math, random, itertools, importlib.util, time
from fractions import Fraction
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.abspath(os.path.join(HERE, "..", ".."))
FAILS = []


def check(cond, msg):
    if not cond:
        FAILS.append(msg)
        print("  FAIL:", msg, flush=True)
    return cond


# ===================================================================================== systems (own transcription)
def sfam(S, m=3, d=1):
    M = 2 ** m
    return lambda n: n // 2 if n % 2 == 0 else (3 * n + d if n % M in S else n + d)


def mod3(f1, f2):
    return lambda n: n // 3 if n % 3 == 0 else (f1(n) if n % 3 == 1 else f2(n))


def split(c, d):
    return lambda n: n // 2 if n % 2 == 0 else (c * n + d if n % 4 == 1 else n + d)


S0 = (1, 3, 5, 7, 11, 13, 15, 17, 21, 23, 25, 29)
# name: (p, k, g, step) -- step functions transcribed from the rule strings in census/systems.py,
# round2/descent/systems.py, round4/integrality/k7.md and round3 S-family definitions.
DEFS = {
    "3x+1": (2, 1, 3, lambda n: n // 2 if n % 2 == 0 else 3 * n + 1),
    "3x-1": (2, 1, 3, lambda n: n // 2 if n % 2 == 0 else 3 * n - 1),
    "3x+5": (2, 1, 3, lambda n: n // 2 if n % 2 == 0 else 3 * n + 5),
    "5x+1": (2, 1, 5, lambda n: n // 2 if n % 2 == 0 else 5 * n + 1),
    "K7": (2, 2, 3, lambda z: z // 2 if z % 2 == 0 else ((3 * z + 1) // 2 if z % 4 == 3 else (z - 1) // 4)),
    "sf3_7": (2, 3, 3, sfam({7})), "sf3_17": (2, 3, 3, sfam({1, 7})), "sf3_57": (2, 3, 3, sfam({5, 7})),
    "sf3_157": (2, 3, 3, sfam({1, 5, 7})), "sf3_357": (2, 3, 3, sfam({3, 5, 7})),
    "sf3_137": (2, 3, 3, sfam({1, 3, 7})), "sf3_13": (2, 3, 3, sfam({1, 3})),
    "sf3_135": (2, 3, 3, sfam({1, 3, 5})),
    "split5_1": (2, 2, 5, split(5, 1)), "split5_3": (2, 2, 5, split(5, 3)),
    "desc_split7_1": (2, 2, 7, split(7, 1)),
    "desc_s32_plus9": (2, 5, 3, sfam(set(S0 + (9,)), m=5)),
    "m3_b": (3, 1, 4, mod3(lambda n: (4 * n - 1) // 3, lambda n: (4 * n + 1) // 3)),
    "m3_d": (3, 1, 4, mod3(lambda n: 4 * n + 2, lambda n: 4 * n + 1)),
    "m3_g": (3, 1, 5, mod3(lambda n: 5 * n + 1, lambda n: 5 * n + 2)),
    "m3_e": (3, 1, 7, mod3(lambda n: 7 * n + 2, lambda n: 7 * n + 1)),
    "desc_m3_4n5": (3, 1, 2, mod3(lambda n: 4 * n + 5, lambda n: 2 * n + 2)),
    "perm_1932": (3, 1, 2, lambda n: 2 * (n // 3) if n % 3 == 0 else (4 * (n // 3) + 1 if n % 3 == 1 else 4 * (n // 3) + 3)),
}
CONTRACTING = ["3x+1", "K7", "sf3_7", "sf3_17", "sf3_57", "sf3_157", "sf3_357", "sf3_13", "sf3_135", "split5_1",
               "split5_3", "desc_split7_1", "desc_s32_plus9", "m3_b", "m3_g", "desc_m3_4n5"]


def vp(x, p):
    v = 0
    while x % p == 0:
        x //= p
        v += 1
    return v


def infer_rows(p, k, step):
    Q = p ** k
    rows = []
    for r in range(Q):
        ns = [r + Q * t for t in range(1, 60)]
        ys = [step(n) for n in ns]
        sl = Fraction(ys[1] - ys[0], Q)
        assert all(Fraction(y - ys[0]) == sl * (n - ns[0]) for n, y in zip(ns, ys)), "not affine"
        e = vp(sl.denominator, p)
        assert sl.denominator == p ** e and sl.numerator % p != 0 and sl.numerator > 0
        u = sl.numerator
        v = ys[0] * p ** e - u * ns[0]
        rows.append((u, v, e))
    return rows


class TM:
    """unit-multiplier p-adic table map; own implementation of the digit tree"""

    def __init__(self, name):
        p, k, g, step = DEFS[name]
        self.name, self.p, self.k, self.g, self.step = name, p, k, g, step
        self.Q = p ** k
        self.rows = infer_rows(p, k, step)
        self.a = []
        for (u, v, e) in self.rows:
            a, x = 0, 1
            while x < u:
                x *= g
                a += 1
            assert x == u, (name, u, g)
            self.a.append(a)
        self.V = max(abs(v) for (u, v, e) in self.rows)
        # dec[s][c] = row index decided by c mod p^s (s <= k), else None
        self.dec = []
        for s in range(k + 1):
            ps = p ** s
            tab = []
            for c in range(ps):
                rs = {self.rows[r] for r in range(c, self.Q, ps)}
                tab.append(c % self.Q if len(rs) == 1 and s == k else
                           (next(r for r in range(c, self.Q, ps)) if len(rs) == 1 else None))
            self.dec.append(tab)
        self._am = {}
        self._tr = {}
        self.root = (0, 0)
        self.build()

    def amin(self, E):
        if E <= 0:
            return 0
        if E not in self._am:
            A, x, pe = 0, 1, self.p ** E
            A = max(0, int(E * math.log(self.p) / math.log(self.g)) - 3)
            x = self.g ** A
            while x < pe:
                x *= self.g
                A += 1
            self._am[E] = A
        return self._am[E]

    def run(self, s, x):
        """x: an integer representing a value known mod p^s.  Apply decided steps.
        returns (list of cumulative (A, E) after each step, s', x')"""
        p, k = self.p, self.k
        out = []
        A = E = 0
        n = 0
        while True:
            kk = s if s < k else k
            r = self.dec[kk][x % p ** kk]
            if r is None:
                return out, s, x
            u, v, e = self.rows[r]
            y = u * x + v
            assert y % p ** e == 0
            x = y // p ** e
            s -= e
            A += self.a[r]
            E += e
            out.append((A, E))
            n += 1
            if n > 5000:
                raise RuntimeError("infinite decided chain")

    def ok_steps(self, A0, E0, steps):
        return all(A0 + a >= self.amin(E0 + e) for (a, e) in steps)

    def survives(self, r, b):
        steps, s, x = self.run(b, r)
        return self.ok_steps(0, 0, steps)

    def survives_lifts(self, r, b):
        """independent semantics: lifts r + p^b t (t < p^(k+1)) evolve in parallel while they agree on the row"""
        p = self.p
        xs = [r + p ** b * t for t in range(p ** (self.k + 1))]
        A = E = 0
        while True:
            rs = [self.rows[x % self.Q] for x in xs]
            if any(q != rs[0] for q in rs):
                return True
            u, v, e = rs[0]
            xs = [(u * x + v) // p ** e for x in xs]
            A += self.a[self.rows.index(rs[0])]
            E += e
            if self.g ** A < p ** E:
                return False

    def build(self):
        p = self.p
        todo, seen = [self.root], {self.root}
        while todo:
            st = todo.pop()
            s, c = st
            lst = []
            for dg in range(p):
                steps, s1, x1 = self.run(s + 1, c + dg * p ** s)
                st1 = (s1, x1 % p ** s1)
                lst.append((st1, steps))
                if st1 not in seen:
                    seen.add(st1)
                    todo.append(st1)
            self._tr[st] = lst
        rec, fr = set(), {t[0] for t in self._tr[self.root]}
        while fr:
            rec |= fr
            fr = {t[0] for q in fr for t in self._tr[q]} - rec
        self.states1 = sorted(rec)
        self.allstates = sorted(seen)
        self.tau0 = max(len(steps) for q in self._tr for (_, steps) in self._tr[q])

    def counts(self, depth, start=None, keep=None):
        """DP over (state, A); E = depth + s_start - s.  Returns dict depth -> {(state, A): count}"""
        st0 = self.root if start is None else start
        cur = {(st0, 0): 1}
        res = {}
        if keep is None or 0 in keep:
            res[0] = dict(cur)
        for j in range(depth):
            nxt = {}
            for (st, A), c in cur.items():
                E = j + st0[0] - st[0]
                for (st1, steps) in self._tr[st]:
                    if steps and not self.ok_steps(A, E, steps):
                        continue
                    a = steps[-1][0] if steps else 0
                    key = (st1, A + a)
                    nxt[key] = nxt.get(key, 0) + c
            cur = nxt
            if keep is None or j + 1 in keep:
                res[j + 1] = dict(cur)
        return res

    def Rcounts(self, depth):
        c = self.counts(depth)
        return [sum(c[b].values()) for b in range(depth + 1)]

    def contset(self, st, A, E, K):
        """boolean array over z < p^K: value c + p^s z, s+K known digits, every decided step passes"""
        s, c = st
        p = self.p
        out = np.zeros(p ** K, dtype=bool)
        for z in range(p ** K):
            steps, _, _ = self.run(s + K, c + p ** s * z)
            out[z] = self.ok_steps(A, E, steps)
        return out

    def gmin(self, st, L):
        """min prefix slope (start included) as (a, e) for every z < p^L"""
        s, c = st
        p, g = self.p, self.g
        res = []
        for z in range(p ** L):
            steps, _, _ = self.run(s + L, c + p ** s * z)
            best = (0, 0)
            bv = Fraction(1)
            for (a, e) in steps:
                v = Fraction(g ** a, p ** e)
                if v < bv:
                    bv, best = v, (a, e)
            res.append(bv)
        return res


_CACHE = {}


def T(name):
    if name not in _CACHE:
        _CACHE[name] = TM(name)
    return _CACHE[name]


def window_minmax(mask, u, N, Q):
    """min and max over all B of #{0 <= t < N : (u t + B) mod Q in S} (cyclic)"""
    z = np.nonzero(mask)[0].astype(object)
    ui = pow(int(u), -1, Q)
    ind = np.zeros(Q, dtype=np.int64)
    for zz in z:
        ind[int(zz) * ui % Q] = 1
    cs = np.concatenate(([0], np.cumsum(np.concatenate((ind, ind[:N])))))
    w = cs[N:N + Q] - cs[:Q]
    return int(w.min()), int(w.max())


# ===================================================================================== A: rows, engine, |R_b|
def secA():
    print("A: tables, digit tree vs lift semantics, H0, (F)", flush=True)
    for name in DEFS:
        t = T(name)
        b = 9 if t.p == 2 else 6
        for bb in range(1, b + 1):
            s1 = [t.survives(r, bb) for r in range(t.p ** bb)]
            s2 = [t.survives_lifts(r, bb) for r in range(t.p ** bb)]
            check(s1 == s2, f"A {name} b={bb}: node rule and lift semantics differ")
        R = t.Rcounts(b)
        check(R[b] == sum(t.survives(r, b) for r in range(t.p ** b)), f"A {name}: DP count != enumeration")
        H0 = all(v >= 0 for (u, v, e), a in zip(t.rows, t.a) if a == 0 and e == 0)
        check(H0, f"A {name}: H0 fails")
        print(f"  {name:15s} p={t.p} k={t.k} g={t.g} rows={t.rows} states1={len(t.states1)} tau0={t.tau0} V={t.V}")


# ===================================================================================== B: h, H2, alpha, c2, B2 trend
def Mtheta(t, th):
    st = t.states1
    ix = {s: i for i, s in enumerate(st)}
    M = np.zeros((len(st), len(st)))
    for s in st:
        for (s1, steps) in t._tr[s]:
            a, e = steps[-1] if steps else (0, 0)
            M[ix[s], ix[s1]] += math.exp(th * (a * math.log(t.g) - e * math.log(t.p)))
    return M


def logrho(t, th):
    return math.log(max(abs(np.linalg.eigvals(Mtheta(t, th)))))


def h_of(t):
    from scipy.optimize import minimize_scalar
    r = minimize_scalar(lambda th: logrho(t, th), bounds=(0, 40), method="bounded",
                        options=dict(xatol=1e-12))
    th = r.x if r.fun < logrho(t, 0.0) else 0.0
    return th, min(r.fun, logrho(t, 0.0)) / math.log(t.p)


def karp_alpha(t):
    # brute: max mean of a over simple cycles of the digit graph (small graphs), exact
    st = t.states1
    edges = {}
    for s in st:
        for (s1, steps) in t._tr[s]:
            a = steps[-1][0] if steps else 0
            edges.setdefault(s, []).append((s1, a))
    best = Fraction(-1)
    n = len(st)
    # all closed walks up to length n through DFS (enough: max mean attained on a simple cycle)
    for s in st:
        stack = [(s, 0, 0, (s,))]
        while stack:
            v, L, A, path = stack.pop()
            for (w, a) in edges[v]:
                if w == s:
                    best = max(best, Fraction(A + a, L + 1))
                elif w not in path and L + 1 < n:
                    stack.append((w, L + 1, A + a, path + (w,)))
    return best


def secB():
    print("B: growth exponent h, alpha, H2, c2; B2 trend", flush=True)
    import json
    cons = {o["name"]: o for o in json.load(open(os.path.join(HERE, "data", "constants_K1500.json")))}
    for name in DEFS:
        t = T(name)
        th, h = h_of(t)
        o = cons[name]
        check(abs(h - o["h"]) < 2e-6, f"B {name}: h {h:.7f} vs prover {o['h']:.7f}")
        al = karp_alpha(t)
        check(str(al) == str(o["alpha"]) or Fraction(o["alpha"]) == al, f"B {name}: alpha {al} vs {o['alpha']}")
        line = f"  {name:15s} theta*={th:.5f} h={h:.6f} (prover {o['h']:.6f}) alpha={al}"
        if th > 1e-9:
            H2 = 2 * h - logrho(t, 2 * th) / math.log(t.p)
            c2 = min(1.0, h / 2 + H2 / (2 * float(al) * math.log(t.g) / math.log(t.p)))
            check(abs(c2 - o["c2"]) < 1e-5, f"B {name}: c2 {c2} vs {o['c2']}")
            line += f" H2={H2:.5f} c2={c2:.5f} C*={1 / (1 - h):.3f}"
        print(line, flush=True)
    # split5_3 two-ended constant against the closed form of split5_3_s27.md
    q = 1 - 2 / math.log2(5)
    pp = 1 - q
    H = -pp * math.log2(pp) - q * math.log2(q)
    cst = H / 2 + (-math.log2(pp * pp + q * q)) / math.log2(5)
    th, h = h_of(T("split5_3"))
    check(abs(h - H) < 1e-7, f"B split5_3 h {h} vs binary entropy {H}")
    check(abs(cons["split5_3"]["c2"] - cst) < 1e-6, f"B split5_3 c2 vs s27 c_* {cst}")
    print(f"  split5_3: s27 closed forms H={H:.8f} c_*={cst:.8f}", flush=True)
    # B2 trend: |R_n| rho*^-n n^{3/2} at several n (own DP)
    NM = 600
    for name in CONTRACTING:
        t = T(name)
        th, h = h_of(t)
        R = t.Rcounts(NM)
        lr = h * math.log(t.p)
        vals = []
        for n in (100, 200, 300, 400, 500, 600):
            x = R[n]
            lx = math.log(x)
            vals.append(lx - n * lr + 1.5 * math.log(n))
        # local exponent estimate: slope of log|R_n| - n log rho* against log n between 450 and 900
        ex = -(vals[-1] - 1.5 * math.log(600) - vals[2] + 1.5 * math.log(300)) / math.log(2)
        print(f"  B2 {name:15s} normalised log ratio at n=100..600: " + " ".join(f"{v:+.3f}" for v in vals)
              + f"  local exponent (300->600) {ex:.3f}", flush=True)


# ===================================================================================== C: Theorem R_G and Lemma T_G
def own_bracket_enum(t, m, j, K, mutate=False):
    p, g = t.p, t.g
    d = m + j - K
    N = p ** (K - j)
    Q = p ** K
    Lo = Up = tot = 0
    node_bad = 0
    cache = {}
    for r in range(p ** d):
        steps, s, x = t.run(d, r)
        if not t.ok_steps(0, 0, steps):
            continue
        A, E = steps[-1] if steps else (0, 0)
        key = ((s, x % p ** s), A, E)
        if key not in cache:
            cache[key] = t.contset((s, x % p ** s), A, E, K)
        mask = cache[key]
        tot += int(mask.sum())
        u = pow(g, A + (1 if mutate else 0), Q)
        mn, mx = window_minmax(mask, u, N, Q)
        Lo += mn
        Up += mx
        B0 = (x // p ** s) % Q
        lhs = sum(1 for tt in range(N) if mask[(u * tt + B0) % Q])
        rhs = sum(1 for tt in range(N) if t.survives(r + p ** d * tt, m + j))
        node_bad += lhs != rhs
    return Lo, Up, tot, node_bad


def secC():
    print("C: Theorem R_G bracket and Lemma T_G, own enumeration vs brute force", flush=True)
    random.seed(20261128)
    cases = mut = 0
    for name in ["3x+1", "3x+5", "K7", "sf3_57", "sf3_13", "split5_3", "desc_s32_plus9", "m3_b", "m3_g",
                 "desc_m3_4n5", "perm_1932"]:
        t = T(name)
        p = t.p
        for _ in range(4):
            m = random.randint(8, 12) if p == 2 else random.randint(5, 7)
            j = random.randint(1, 3)
            K = random.randint(j + 1, j + (6 if p == 2 else 4))
            if m + j - K < 1:
                continue
            Lo, Up, tot, nb = own_bracket_enum(t, m, j, K)
            Nb = sum(t.survives(n, m + j) for n in range(p ** m))
            Rmj = t.Rcounts(m + j)[m + j]
            check(Lo <= Nb <= Up, f"C {name} m={m} j={j} K={K}: bracket [{Lo},{Up}] misses {Nb}")
            check(tot == Rmj, f"C {name} identity sum|S| {tot} != |R| {Rmj}")
            check(nb == 0, f"C {name} Lemma T_G fails on {nb} nodes")
            _, _, _, nbm = own_bracket_enum(t, m, j, K, mutate=True)
            mut += nbm > 0
            cases += 1
    check(mut > 0, "C mutation g^(A+1) never detected")
    print(f"  {cases} random (system, m, j, K) cases; mutation detected in {mut}", flush=True)


# ===================================================================================== D: types (G1 proof) and Lemma P_G
def secD():
    print("D: G1 type structure (sigma, v, pattern) and the Delta formula; Lemma P_G numerically", flush=True)
    for name in ["K7", "sf3_57", "split5_3", "desc_s32_plus9", "m3_b", "desc_m3_4n5"]:
        t = T(name)
        K = 8 if t.p == 2 else 5
        lam = math.log(t.p) / math.log(t.g)
        kk = K + t.k
        seen = {}
        bad = 0
        for st in t.states1:
            for E in range(1, 70):
                for v in range(0, int(kk * lam) + 3):
                    A = t.amin(E) + v
                    # Delta formula
                    for e in range(1, kk + 1):
                        D = t.amin(E + e) - t.amin(E)
                        fE, fe = (E * lam) % 1, (e * lam) % 1
                        check(D == math.floor(e * lam) + (1 if fE + fe >= 1 else 0), f"D {name} Delta E={E} e={e}")
                    patt = tuple(t.amin(E + e) - t.amin(E) for e in range(kk + 1))
                    key = (st, v, patt)
                    if (st, E % 7) != (st, 0) and E > 20 and key in seen:
                        continue
                    S = t.contset(st, A, E, K).tobytes()
                    if key in seen and seen[key] != S:
                        bad += 1
                    seen[key] = S
        npat = len({k[2] for k in seen})
        check(bad == 0, f"D {name}: continuation set not determined by (sigma, v, pattern)")
        check(npat <= kk + 1, f"D {name}: {npat} patterns > K+k+1")
        print(f"  {name}: {len(seen)} (sigma,v,pattern) keys, {npat} patterns (bound {kk + 1}); set determined by key", flush=True)
    # Lemma P_G numerically: own G, m_GG, and min nonempty continuation set
    for name in ["sf3_57", "sf3_357", "sf3_13", "sf3_17", "desc_s32_plus9"]:
        t = T(name)
        K0 = 24
        G = set(t.states1)
        while True:
            badset = set()
            for st in G:
                c = t.counts(K0, start=st, keep={K0})[K0]
                if sum(v for (s1, A), v in c.items() if s1 in G) == 0:
                    badset.add(st)
            if not badset:
                break
            G -= badset
        B = [s for s in t.states1 if s not in G]
        Kmax = 10
        mGG = []
        for K in range(Kmax + 1):
            mGG.append(min(sum(v for (s1, A), v in t.counts(K, start=st, keep={K})[K].items() if s1 in G) for st in G))
        r = len(B)
        out = []
        for K in range(6, Kmax + 1):
            mn = None
            for st in t.states1:
                for E in range(1, 21):
                    for v in range(0, int((K + t.k) * math.log(t.p) / math.log(t.g)) + 3):
                        sz = int(t.contset(st, t.amin(E) + v, E, K).sum())
                        if sz > 0:
                            mn = sz if mn is None else min(mn, sz)
            lb = min(mGG[K - rr] for rr in range(0, r + 1))
            out.append((K, mn, lb))
            check(mn >= lb, f"D {name}: Lemma P_G fails at K={K}: min nonempty {mn} < {lb}")
        print(f"  P_G {name}: G={sorted(G)} B={B}; (K, min nonempty |S|, bound): {out}", flush=True)


# ===================================================================================== E: Lemma F_G, iota
def secE():
    print("E: iota closed forms (L <= 24) and Lemma F_G exactly on random sets", flush=True)

    def index(p, g, L):
        P = p ** L
        o, x = 1, g % P
        while x != 1:
            x = x * g % P
            o += 1
        return (P - P // p) // o

    def closed(p, g):
        if p == 2:
            return 2 ** (vp(g - 1, 2) - 1) if g % 4 == 1 else 2 ** (vp(g * g - 1, 2) - 2)
        o = 1
        while pow(g, o, p) != 1:
            o += 1
        return (p - 1) // o * p ** (vp(g ** o - 1, p) - 1)

    for (p, g) in [(2, 3), (2, 5), (2, 7), (2, 9), (3, 2), (3, 4), (3, 5), (3, 7)]:
        idx = [index(p, g, L) for L in range(1, 25 if p == 2 else 15)]
        check(max(idx) == idx[-1] == closed(p, g), f"E iota p={p} g={g}: {idx} closed {closed(p, g)}")
        print(f"  iota(p={p}, g={g}) = {idx[-1]}", flush=True)
    random.seed(7)
    worst = 0
    for (p, g, K) in [(2, 3, 8), (2, 7, 8), (3, 4, 5), (3, 2, 5), (2, 5, 8)]:
        Q = p ** K
        H = []
        u = 1
        while True:
            H.append(u)
            u = u * g % Q
            if u == 1:
                break
        iota = max(index(p, g, L) for L in range(1, K + 1))
        GK = iota * p / (p - 1) * (1 + K * math.log(p))
        for j in (1, 2, 3):
            for _ in range(3):
                Ssz = random.randint(1, Q - 1)
                S = np.zeros(Q, dtype=bool)
                S[random.sample(range(Q), Ssz)] = True
                N = p ** (K - j)
                tot = Fraction(0)
                for u in H:
                    mn, mx = window_minmax(S, u, N, Q)
                    tot += max(abs(Fraction(mx) - Fraction(N * Ssz, Q)), abs(Fraction(mn) - Fraction(N * Ssz, Q)))
                lhs = float(tot / len(H))
                rhs = GK * math.sqrt(Ssz * (1 - Ssz / Q))
                check(lhs <= rhs, f"E Lemma F_G p={p} g={g} K={K} j={j}")
                worst = max(worst, lhs / rhs)
    print(f"  Lemma F_G: largest lhs/rhs = {worst:.3f}", flush=True)


# ===================================================================================== F: Lemma X exceptional octaves
def secF():
    print("F: Lemma X, exact Diophantine scan 18 <= m <= 3000 (constant 3 of the lemma, rigorous log bound)", flush=True)
    for name in DEFS:
        t = T(name)
        p, g = t.p, t.g
        lam = math.log(p) / math.log(g)
        flagged = set()

        def bm(m):
            return int(m + 2 * math.log(m, p)) + t.k + 1

        for m in range(18, 3001):
            if 8 * t.tau0 * bm(m) * t.V > p ** (m - 1):
                flagged.add(m)
        Emax = bm(3000)
        for E in range(1, Emax + 1):
            A0 = int(E * lam)
            for A in (A0 - 1, A0, A0 + 1, A0 + 2):
                if A < 0:
                    continue
                ga, pe = g ** A, p ** E
                diff, mx = abs(ga - pe), max(ga, pe)
                # rigorous: |log(ga/pe)| >= diff/mx.  Need diff/mx >= 3 t V / p^{m-1}, t = tau0 * b(m)
                m = 18
                while m <= 3000 and bm(m) < E:
                    m += 1
                while m <= 3000:
                    if diff * p ** (m - 1) >= 3 * t.tau0 * bm(m) * t.V * mx:
                        break
                    flagged.add(m)
                    m += 1
        check(not flagged, f"F {name}: flagged octaves in [18, 3000]: {sorted(flagged)[:10]}")
        print(f"  {name:15s} flagged octaves m in [18,3000]: {sorted(flagged)}", flush=True)
    # brute force: slope count vs actual count on whole octaves, m = 18 (p=2) / 12 (p=3)
    for name in ["3x+5", "3x-1", "K7", "sf3_57", "split5_3", "desc_s32_plus9", "m3_b", "desc_m3_4n5"]:
        t = T(name)
        m = 18 if t.p == 2 else 11
        dis = 0
        for b in (m, m + 2, m + 4):
            for n in range(t.p ** (m - 1), t.p ** m):
                steps, s, x = t.run(b, n)
                sl = t.ok_steps(0, 0, steps)
                y, ac = n, True
                for _ in steps:
                    u, v, e = t.rows[y % t.Q]
                    y = (u * y + v) // t.p ** e
                    if y < n:
                        ac = False
                        break
                dis += sl != ac
        check(dis == 0, f"F {name}: {dis} slope/actual disagreements in octave m={m}")
        print(f"  octave brute force {name} m={m}, b in {{m, m+2, m+4}}: {dis} disagreements", flush=True)


# ===================================================================================== G: U'_G constants (own)
def uprime_own(t, L, M):
    p, g = t.p, t.g
    N = p ** L
    units = []
    u = 1
    while True:
        units.append(u)
        u = u * g % N
        if u == 1:
            break
    best = {m: Fraction(0) for m in range(1, M + 1)}
    for st in sorted(set(t.states1) | {t.root}):
        gv = t.gmin(st, L)
        levels = sorted(set(gv))
        if len(levels) == 1:
            continue
        rank = np.array([levels.index(x) for x in gv], dtype=np.int32) if len(levels) < 60 else \
            np.array([{v: i for i, v in enumerate(levels)}[x] for x in gv], dtype=np.int32)
        zs = np.arange(N, dtype=np.int64)
        for w in units:
            pos = (zs * w) % N
            rk = np.empty(N, dtype=np.int32)
            rk[pos] = rank
            for q in range(1, len(levels)):
                ind = (rk >= q).astype(np.int64)
                sz = int(ind.sum())
                cs = np.concatenate(([0], np.cumsum(np.concatenate((ind, ind)))))
                for m in range(1, M + 1):
                    W = N // p ** m
                    win = cs[W:W + N] - cs[:N]
                    dev = max(int(win.max()) * p ** m - sz, sz - int(win.min()) * p ** m)
                    f = Fraction(dev, sz)
                    if f > best[m]:
                        best[m] = f
    return best


def secG():
    print("G: Theorem U'_G constants recomputed (own minimum-slope function, own window counts)", flush=True)
    targets = [("m3_b", 9, [Fraction(289, 832), Fraction(17, 28), Fraction(13, 14)]),
               ("desc_m3_4n5", 9, [Fraction(61, 103), Fraction(122, 103), Fraction(98, 37)]),
               ("m3_g", 9, [Fraction(139, 768), Fraction(45, 128), Fraction(17, 32)]),
               ("3x+1", 14, [Fraction(213, 1627), Fraction(213, 749), Fraction(349, 749)]),
               ("split5_3", 14, [Fraction(4, 5), Fraction(19, 9), Fraction(23, 5)]),
               ("K7", 14, [Fraction(29, 77), Fraction(127, 137), Fraction(73, 55)])]
    for name, L, want in targets:
        t0 = time.time()
        got = uprime_own(T(name), L, 3)
        check([got[1], got[2], got[3]] == want, f"G {name} L={L}: own {got} vs prover {want}")
        print(f"  {name} L={L}: " + ", ".join(f"{got[m]}" for m in (1, 2, 3)) + f"  ({time.time() - t0:.0f} s)", flush=True)
    # the theorem itself on a brute-force instance: |N(p^{b-m}, b)/(p^{b-m}P(b)) - 1| <= D'
    t = T("m3_b")
    D = uprime_own(t, 6, 2)
    for b in (6, 8, 10):
        R = t.Rcounts(b)[b]
        for m in (1, 2):
            Nn = sum(t.survives(n, b) for n in range(3 ** (b - m)))
            dev = abs(Fraction(Nn * 3 ** m, R) - 1)
            check(dev <= D[m], f"G U' theorem m3_b L=6 b={b} m={m}: {dev} > {D[m]}")
    print(f"  U'_G theorem verified by brute force for m3_b, L=6 (D'={D[1]}, {D[2]}), b = 6, 8, 10", flush=True)


# ===================================================================================== H: wide-scan sample
def secH():
    print("H: spot check of the hypothesis scan on census systems (own engine on census step functions)", flush=True)

    def load(path, nm):
        spec = importlib.util.spec_from_file_location(nm, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    mods = [load(os.path.join(CENSUS, "systems.py"), "c0"), load(os.path.join(CENSUS, "round2", "descent", "systems.py"), "c1")]
    by = {}
    for md in mods:
        for s in md.SYSTEMS:
            by[s["id"]] = s
    # (id, p, k, g, claimed first b with R_b empty)
    claims = [("split_7081_s27", 2, 2, 3, 2), ("split_5_s27", 2, 2, 3, 2), ("splitB_71_s27", 2, 2, 3, 2),
              ("m3_a_s100", 3, 1, 2, 1), ("m3_c_s100", 3, 1, 2, 1), ("desc_s8_35", 2, 3, 3, 4),
              ("desc_s32_max", 2, 5, 3, 30)]
    for (sid, p, k, g, b0) in claims:
        DEFS["tmp_" + sid] = (p, k, g, by[sid]["step"])
        t = TM("tmp_" + sid)
        R = t.Rcounts(b0)
        check(R[b0] == 0 and R[b0 - 1] > 0, f"H {sid}: |R_b| = {R[max(0, b0 - 2):b0 + 1]} (claimed first empty at {b0})")
        print(f"  {sid}: |R_{b0 - 1}| = {R[b0 - 1]}, |R_{b0}| = {R[b0]}", flush=True)
    # (F) failure for 3n+2 (odd n -> 3n+2 stays odd)
    DEFS["tmp_3n2"] = (2, 1, 3, by["par_3_2_s27"]["step"])
    try:
        TM("tmp_3n2")
        check(False, "H par_3_2: no infinite chain found")
    except (RuntimeError, RecursionError):
        print("  par_3_2_s27: infinite decided chain confirmed (F fails)", flush=True)


# ===================================================================================== Z: comparison with the prover's code
def secZ():
    print("Z: cross-comparison with the prover's modules (cwlib, cert)", flush=True)
    sys.path.insert(0, HERE)
    import cwlib, cert
    for name in DEFS:
        if name.startswith("tmp_"):
            continue
        t = T(name)
        S = cwlib.System(name)
        check(list(S.rows) == list(t.rows), f"Z {name}: rows differ {S.rows} vs own {t.rows}")
        check(S.g == t.g and S.p == t.p and S.k == t.k, f"Z {name}: p,k,g differ")
        b = 40 if t.p == 2 else 25
        check(S.surv_counts(b) == t.Rcounts(b), f"Z {name}: |R_b| differ")
        check(len(S.states1) == len(t.states1), f"Z {name}: number of states differ")
    # grouped bracket at m = 100: own (DP by (state, A), own continuation sets) vs prover's bracket and bracket_fast
    os.environ.setdefault("CW_CACHE", os.path.join(os.environ.get("TMPDIR", "/tmp"), "ref1_cw_cache"))
    for name, K in [("K7", 11), ("split5_3", 11), ("sf3_57", 10), ("m3_b", 7), ("desc_s32_plus9", 10)]:
        t = T(name)
        S = cwlib.System(name)
        p = t.p
        for m, j in [(100, 1), (100, 3), (60, 5)]:
            d = m + j - K
            c = t.counts(d, keep={d})[d]
            N, Q = p ** (K - j), p ** K
            Lo = Up = tot = 0
            for ((st, A), cnt) in c.items():
                E = d - st[0]
                mask = t.contset(st, A, E, K)
                sz = int(mask.sum())
                tot += cnt * sz
                if sz == 0:
                    continue
                mn, mx = window_minmax(mask, pow(t.g, A, Q), N, Q)
                Lo += cnt * mn
                Up += cnt * mx
            Rmj = t.Rcounts(m + j)[m + j]
            check(tot == Rmj, f"Z {name} m={m} j={j}: identity")
            pc = S.dp(d, keep={d})[d]
            L2, U2, mean2, _ = cert.bracket(S, m, j, K, pc)
            L3, U3, mean3, _ = cert.bracket_fast(S, m, j, K, pc)
            check((Lo, Up, tot) == (L2, U2, mean2) == (L3, U3, mean3),
                  f"Z {name} m={m} j={j} K={K}: own {(Lo, Up)} vs prover {(L2, U2)} / fast {(L3, U3)}")
            print(f"  {name} m={m} j={j} K={K}: rel [{(Lo * p ** j - Rmj) / Rmj:+.5f}, {(Up * p ** j - Rmj) / Rmj:+.5f}] "
                  f"agrees with prover's bracket and bracket_fast", flush=True)


if __name__ == "__main__":
    secs = sys.argv[1:] or list("ABCDEFGHZ")
    for s in secs:
        t0 = time.time()
        globals()["sec" + s]()
        print(f"  [section {s}: {time.time() - t0:.0f} s]", flush=True)
    if FAILS:
        print(f"{len(FAILS)} FAILURES")
        for f in FAILS:
            print("  ", f)
        sys.exit(1)
    print("ALL REFEREE-1 CHECKS PASSED")
