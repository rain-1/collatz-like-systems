#!/usr/bin/env python3
"""Referee 2: independent check of round6/countlaw_wide (written from scratch; exits 0 iff every check passes).

Only section Z imports the prover's code or data, and only to compare numbers with the ones computed here.

  A  tables re-inferred from the census rule strings (exact affine fitting on residue classes)
  B  my own digit-tree engine: |R_b| by node-by-node evaluation equals |R_b| by my own state DP
  C  Theorem R_G and Lemma T_G against brute force (random cases, all systems), identity sum|S| = |R_{m+j}|,
     literal min/max over every intercept B for small K, and a mutation (g^A -> g^(A+1)) that must be detected
  D  Lemma X: exact Diophantine scan of exceptional octaves 18 <= m <= 3000 (rigorous |log x| >= |x-1|/max(x,1)),
     and actual survival = slope survival on whole octaves
  E  Theorem U'_G: exact constants for systems not recomputed by REFEREE1, and the theorem against brute force
  F  constants h, H2, alpha, c2, C* from my own transfer matrix; h0(K0) <= h sanity
  G  hypothesis (P): G, B, reachability, cycle contraction, own computation for all 23 systems
  H  iota closed forms (orders of g mod p^L, L <= 18)
  I  Lemma F_G inequality, exact enumeration on random sets
  J  h_* = h for split5_3 inside the present coding: potential, buffer words from every state (the fix proposed)
  K  hypothesis-scan spot checks (first empty R_b; (F) failure)
  Z  comparison with the prover's code and data files

usage: python referee2_check.py [sections, e.g. ABC]   (numpy needed)
"""
import sys, os, math, random, itertools, re
from fractions import Fraction
from functools import lru_cache
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FAILS = []
random.seed(20261128)


def ok(cond, msg):
    if not cond:
        FAILS.append(msg)
        print("  FAIL:", msg, flush=True)
    return cond


# ------------------------------------------------------------------------------------------------ A: systems
def R_sf(S, mod=8):
    return lambda n: n // 2 if n % 2 == 0 else (3 * n + 1 if n % mod in S else n + 1)


def R_split(a, d):
    return lambda n: n // 2 if n % 2 == 0 else (a * n + d if n % 4 == 1 else n + d)


def R_m3(a1, b1, a2, b2, div1=1, div2=1):
    return lambda n: n // 3 if n % 3 == 0 else ((a1 * n + b1) // div1 if n % 3 == 1 else (a2 * n + b2) // div2)


S0 = (1, 3, 5, 7, 11, 13, 15, 17, 21, 23, 25, 29)
RULES = {
    # name: (p, k, g, rule)   -- rule strings from census/systems.py, round2/descent, round3/progressions,
    #                            round3/accel/sfamily_obst.md, round4/integrality/k7.md
    "3x+1": (2, 1, 3, lambda n: n // 2 if n % 2 == 0 else 3 * n + 1),
    "3x-1": (2, 1, 3, lambda n: n // 2 if n % 2 == 0 else 3 * n - 1),
    "3x+5": (2, 1, 3, lambda n: n // 2 if n % 2 == 0 else 3 * n + 5),
    "5x+1": (2, 1, 5, lambda n: n // 2 if n % 2 == 0 else 5 * n + 1),
    "K7": (2, 2, 3, lambda z: z // 2 if z % 2 == 0 else ((3 * z + 1) // 2 if z % 4 == 3 else (z - 1) // 4)),
    "sf3_7": (2, 3, 3, R_sf({7})), "sf3_17": (2, 3, 3, R_sf({1, 7})), "sf3_57": (2, 3, 3, R_sf({5, 7})),
    "sf3_157": (2, 3, 3, R_sf({1, 5, 7})), "sf3_357": (2, 3, 3, R_sf({3, 5, 7})),
    "sf3_137": (2, 3, 3, R_sf({1, 3, 7})), "sf3_13": (2, 3, 3, R_sf({1, 3})), "sf3_135": (2, 3, 3, R_sf({1, 3, 5})),
    "split5_1": (2, 2, 5, R_split(5, 1)), "split5_3": (2, 2, 5, R_split(5, 3)),
    "desc_split7_1": (2, 2, 7, R_split(7, 1)),
    "desc_s32_plus9": (2, 5, 3, R_sf(set(S0) | {9}, 32)),
    "m3_b": (3, 1, 4, R_m3(4, -1, 4, 1, 3, 3)), "m3_d": (3, 1, 4, R_m3(4, 2, 4, 1)),
    "m3_g": (3, 1, 5, R_m3(5, 1, 5, 2)), "m3_e": (3, 1, 7, R_m3(7, 2, 7, 1)),
    "desc_m3_4n5": (3, 1, 2, R_m3(4, 5, 2, 2)),
    "perm_1932": (3, 1, 2, lambda n: 2 * (n // 3) if n % 3 == 0 else (4 * (n // 3) + 1 if n % 3 == 1 else 4 * (n // 3) + 3)),
}
EXTRA = {   # hypothesis-scan spot checks
    "split_7081": (2, 2, 3, lambda n: n // 2 if n % 2 == 0 else (3 * n + 7081 if n % 4 == 1 else n + 7081)),
    "split_5": (2, 2, 3, lambda n: n // 2 if n % 2 == 0 else (3 * n + 5 if n % 4 == 1 else n + 5)),
    "splitB_71": (2, 2, 3, lambda n: n // 2 if n % 2 == 0 else (n + 71 if n % 4 == 1 else 3 * n + 71)),
    "desc_s8_35": (2, 3, 3, R_sf({3, 5}, 8)),
    "desc_s32_max": (2, 5, 3, R_sf(set(S0), 32)),
    "desc_s32_d65": (2, 5, 3, lambda n: n // 2 if n % 2 == 0 else (3 * n + 65 if n % 32 in S0 else n + 65)),
    "m3_a": (3, 1, 2, R_m3(2, 1, 2, 2, 3, 3)), "m3_c": (3, 1, 2, R_m3(2, 1, 2, 2)),
    "par_3_2": (2, 1, 3, lambda n: n // 2 if n % 2 == 0 else 3 * n + 2),
    "par_3_4": (2, 1, 3, lambda n: n // 2 if n % 2 == 0 else 3 * n + 4),
}


def infer_rows(p, k, rule):
    Q = p ** k
    rows = []
    for r in range(Q):
        n0 = r + 50 * Q
        sl = Fraction(rule(n0 + Q) - rule(n0), Q)
        num, den = sl.numerator, sl.denominator
        e = 0
        while den % p == 0:
            den //= p
            e += 1
        assert den == 1 and num > 0 and num % p != 0, (r, sl)
        u = num
        v = rule(n0) * p ** e - u * n0
        for t in range(-3, 30):        # exactness on the class, including negative members
            n = r + Q * t
            if n > 0:
                assert (u * n + v) % p ** e == 0 and (u * n + v) // p ** e == rule(n), (r, n)
        rows.append((u, v, e))
    return rows


def dlog(g, u):
    a, x = 0, 1
    while x < u:
        x *= g
        a += 1
    if x != u:
        return None
    return a


class Sys:
    def __init__(self, name, spec=None):
        p, k, g, rule = (spec or RULES[name])
        self.name, self.p, self.k, self.g = name, p, k, g
        self.Q = p ** k
        self.rows = infer_rows(p, k, rule)
        self.a = [dlog(g, u) for (u, v, e) in self.rows]
        self.SG = all(x is not None for x in self.a)
        self.V = max(abs(v) for (u, v, e) in self.rows)
        self.H0 = all(v >= 0 for (u, v, e), a in zip(self.rows, self.a) if a == 0 and e == 0)
        self._amin = {}
        self._build()

    # ---- engine
    def row_of(self, s, x):
        """the row forced by knowing x mod p^s, or None"""
        p, k, Q = self.p, self.k, self.Q
        if s >= k:
            return x % Q
        ps = p ** s
        base = x % ps
        r0 = base
        for i in range(1, p ** (k - s)):
            if self.rows[base + ps * i] != self.rows[r0]:
                return None
        return r0

    def chain(self, s, x, limit=5000):
        """apply every decided step to the integer representative x known mod p^s.
        returns (list of cumulative (A, E, value)), s, x"""
        out = []
        A = E = 0
        while True:
            r = self.row_of(s, x)
            if r is None:
                return out, s, x
            u, v, e = self.rows[r]
            y = u * x + v
            assert y % self.p ** e == 0
            x = y // self.p ** e
            s -= e
            A += self.a[r]
            E += e
            out.append((A, E, x))
            if len(out) > limit:
                raise RuntimeError("infinite decided chain")

    def amin(self, E):
        if E <= 0:
            return 0
        if E not in self._amin:
            A, x, pe = 0, 1, self.p ** E
            A = max(0, int(E * math.log(self.p) / math.log(self.g)) - 3)
            x = self.g ** A
            while x < pe:
                x *= self.g
                A += 1
            assert self.g ** A >= pe and (A == 0 or self.g ** (A - 1) < pe)
            self._amin[E] = A
        return self._amin[E]

    def slope_ok(self, A, E):
        return self.g ** A >= self.p ** E if A >= 0 else False

    def survives(self, r, b):
        steps, _, _ = self.chain(b, r)
        return all(self.g ** A >= self.p ** E for (A, E, _) in steps)

    def survives_actual(self, n, b):
        steps, _, _ = self.chain(b, n)
        return all(x >= n for (_, _, x) in steps)

    def _build(self):
        p = self.p
        self.root = (0, 0)
        self.trans = {}
        todo, seen = [self.root], {self.root}
        while todo:
            st = todo.pop()
            s, c = st
            lst = []
            for dg in range(p):
                steps, s1, x1 = self.chain(s + 1, c + dg * p ** s)
                nst = (s1, x1 % p ** s1)
                lst.append((nst, [(A, E) for (A, E, _) in steps]))
                if nst not in seen:
                    seen.add(nst)
                    todo.append(nst)
            self.trans[st] = lst
        rec, fr = set(), {t[0] for t in self.trans[self.root]}
        while fr:
            rec |= fr
            fr = {t[0] for s in fr for t in self.trans[s]} - rec
        self.states1 = sorted(rec)
        self.tau = max(len(stp) for st in self.trans for (_, stp) in self.trans[st])

    def dp(self, depth, start=None, A0=0):
        """alive nodes after `depth` digits from `start` with initial slope g^A0 (E0 = 0), grouped by (state, A)."""
        st0 = start or self.root
        cur = {(st0, A0): 1}
        hist = [cur]
        for j in range(depth):
            nxt = {}
            for (st, A), c in cur.items():
                E = j + st0[0] - st[0]
                for (st1, steps) in self.trans[st]:
                    if all(A + a >= self.amin(E + e) for (a, e) in steps):
                        a1 = steps[-1][0] if steps else 0
                        key = (st1, A + a1)
                        nxt[key] = nxt.get(key, 0) + c
            cur = nxt
            hist.append(cur)
        return hist

    def minslope(self, st, K):
        """per z < p^K: (a*, e*) of the minimum prefix slope (start (0,0) included), from value c + p^s z"""
        s, c = st
        p, g = self.p, self.g
        aa = np.zeros(p ** K, dtype=np.int64)
        ee = np.zeros(p ** K, dtype=np.int64)
        for z in range(p ** K):
            steps, _, _ = self.chain(s + K, c + p ** s * z)
            ba, be = 0, 0
            for (A, E, _) in steps:
                if g ** A * p ** be < g ** ba * p ** E:     # g^A/p^E < g^ba/p^be
                    ba, be = A, E
            aa[z], ee[z] = ba, be
        return aa, ee


_MS = {}


def contset(S, st, A, E, K):
    key = (S.name, st, K)
    if key not in _MS:
        _MS[key] = S.minslope(st, K)
    aa, ee = _MS[key]
    am = np.array([S.amin(E + x) for x in range(int(ee.max()) + 1)], dtype=np.int64)
    return (A + aa) >= am[ee]


def windows(mask, u, N, Q):
    z = np.nonzero(mask)[0]
    if len(z) == 0:
        return 0, 0
    ui = pow(int(u), -1, Q)
    ind = np.zeros(Q, dtype=np.int64)
    ind[(z * ui) % Q] = 1
    ext = np.concatenate((ind, ind[:N]))
    cs = np.concatenate(([0], np.cumsum(ext)))
    w = cs[N:N + Q] - cs[:Q]
    return int(w.max()), int(w.min())


def windows_literal(mask, u, N, Q):
    vals = []
    for B in range(Q):
        vals.append(sum(1 for t in range(N) if mask[(u * t + B) % Q]))
    return max(vals), min(vals)


def my_bracket(S, m, j, K, hist=None):
    p = S.p
    d = m + j - K
    hist = hist or S.dp(d)
    Q, N = p ** K, p ** (K - j)
    Lo = Up = tot = 0
    for (st, A), cnt in hist[d].items():
        E = d - st[0]
        if A >= S.amin(E + K + st[0] + 1):
            Lo += cnt * N; Up += cnt * N; tot += cnt * Q
            continue
        mask = contset(S, st, A, E, K)
        sz = int(mask.sum())
        tot += cnt * sz
        if sz == Q:
            Lo += cnt * N; Up += cnt * N
        elif sz:
            mx, mn = windows(mask, pow(S.g, A, Q), N, Q)
            Lo += cnt * mn; Up += cnt * mx
    return Lo, Up, tot


SYSS = {}


def get(name):
    if name not in SYSS:
        SYSS[name] = Sys(name, RULES.get(name) or EXTRA.get(name))
    return SYSS[name]


def secA():
    print("A: tables from rule strings", flush=True)
    for n in RULES:
        S = get(n)
        ok(S.SG, f"A {n}: multipliers not powers of g")
        ok(all(math.gcd(u, S.p) == 1 for (u, _, _) in S.rows), f"A {n}: non-unit multiplier")
        ok(S.H0, f"A {n}: H0 fails")
    print(f"  {len(RULES)} systems: SG, units, H0 hold; states1 sizes:",
          {n: len(get(n).states1) for n in RULES}, flush=True)


# ------------------------------------------------------------------------------------------------ B
def secB():
    print("B: |R_b| node-by-node vs DP", flush=True)
    for n in RULES:
        S = get(n)
        bmax = 11 if S.p == 2 else 7
        h = S.dp(bmax)
        for b in range(bmax + 1):
            direct = sum(S.survives(r, b) for r in range(S.p ** b))
            ok(direct == sum(h[b].values()), f"B {n} b={b}: direct {direct} dp {sum(h[b].values())}")
    print("  done", flush=True)


# ------------------------------------------------------------------------------------------------ C
def secC():
    print("C: Theorem R_G / Lemma T_G vs brute force", flush=True)
    ncase = nnode = mut = 0
    lit = 0
    for n in RULES:
        S = get(n)
        p = S.p
        for _ in range(4):
            if p == 2:
                m = random.randint(5, 10); j = random.randint(1, 4); K = random.randint(j + 1, min(m + j, 9))
            else:
                m = random.randint(3, 6); j = random.randint(1, 3); K = random.randint(j + 1, min(m + j, 6))
            b = m + j
            brute = sum(S.survives(x, b) for x in range(p ** m))
            Rb = sum(S.survives(x, b) for x in range(p ** b))
            Lo, Up, tot = my_bracket(S, m, j, K)
            ok(Lo <= brute <= Up, f"C {n} m={m} j={j} K={K}: {Lo} <= {brute} <= {Up} fails")
            ok(tot == Rb, f"C {n} m={m} j={j} K={K}: sum|S| {tot} != |R_b| {Rb}")
            ncase += 1
            # node-by-node Lemma T_G and the mutation
            d = m + j - K
            Q = p ** K
            for r in range(p ** d):
                steps, s, x = S.chain(d, r)
                if not all(S.g ** A >= p ** E for (A, E, _) in steps):
                    continue
                A = steps[-1][0] if steps else 0
                E = d - s
                ok(E == (steps[-1][1] if steps else 0), "C E != d - s")
                mask = contset(S, (s, x % p ** s), A, E, K)
                for t in range(p ** (K - j)):
                    lhs = S.survives(r + p ** d * t, d + K)
                    rhs = bool(mask[(S.g ** A * t + x // p ** s) % Q])
                    ok(lhs == rhs, f"C T_G {n} r={r} d={d} t={t}")
                    bad = bool(mask[(S.g ** (A + 1) * t + x // p ** s) % Q])
                    mut += (bad != lhs)
                nnode += 1
                if K <= 6 and lit < 60 and 0 < mask.sum() < Q:
                    ok(windows(mask, pow(S.g, A, Q), p ** (K - j), Q) ==
                       windows_literal(mask, pow(S.g, A, Q), p ** (K - j), Q), f"C windows {n}")
                    lit += 1
    print(f"  {ncase} bracket cases, {nnode} nodes, {lit} literal window checks; mutation detected {mut} times",
          flush=True)
    ok(mut > 0, "C mutation g^(A+1) never detected")


# ------------------------------------------------------------------------------------------------ D
def secD(mmax=3000, c=2.0):
    print("D: Lemma X", flush=True)
    res = {}
    for n in RULES:
        S = get(n)
        p, g, V, tau = S.p, S.g, S.V, S.tau
        lam = math.log(p) / math.log(g)
        Emax = int(mmax + c * math.log(mmax, p)) + 2
        flagged = set()
        for m in range(2, mmax + 1):
            bm = int(m + c * math.log(m, p)) + 1
            if 8 * tau * bm * V > p ** (m - 1):
                flagged.add(m)
        # rigorous: hypothesis of (i) holds for every n >= p^(m-1) if for all (A,E) != (0,0), E <= bm:
        #   |x - 1| / max(x, 1) >= 3 t V / p^(m-1),  x = g^A / p^E,  t = tau * bm
        # i.e. |g^A - p^E| p^(m-1) >= 3 t V max(g^A, p^E).  Only A near E*lam can fail.
        for E in range(0, Emax + 1):
            A0 = int(E * lam)
            for A in range(max(0, A0 - 1), A0 + 3):
                if A == 0 and E == 0:
                    continue
                diff = abs(g ** A - p ** E)
                big = max(g ** A, p ** E)
                for m in range(max(2, E - 60), mmax + 1):
                    bm = int(m + c * math.log(m, p)) + 1
                    if E > bm:
                        continue
                    if diff * p ** (m - 1) < 3 * tau * bm * V * big:
                        flagged.add(m)
                    else:
                        break
        fl = sorted(flagged)
        res[n] = fl
        hi = [m for m in fl if m >= 18]
        ok(not hi, f"D {n}: flagged octaves >= 18: {hi[:10]}")
    print("  largest flagged octave per system:", {n: (max(v) if v else None) for n, v in res.items()}, flush=True)
    # whole octaves
    for n, m in [("3x+5", 18), ("K7", 18), ("sf3_13", 18), ("split5_3", 18), ("desc_s32_plus9", 18),
                 ("desc_split7_1", 18), ("m3_b", 11), ("desc_m3_4n5", 11), ("m3_g", 11)]:
        S = get(n)
        p = S.p
        for b in (m, m + 3):
            dis = 0
            for x in range(p ** (m - 1), p ** m):
                steps, _, _ = S.chain(b, x)
                sl = all(S.g ** A >= p ** E for (A, E, _) in steps)
                ac = all(v >= x for (_, _, v) in steps)
                dis += sl != ac
            ok(dis == 0, f"D octave {n} m={m} b={b}: {dis} disagreements")
        print(f"  whole octave {n} m={m}: slope = actual at b = m, m+3", flush=True)
    return res


# ------------------------------------------------------------------------------------------------ E
def uprime(S, L, mmax):
    p, g = S.p, S.g
    N = p ** L
    units = [1]
    while True:
        u = units[-1] * g % N
        if u == 1:
            break
        units.append(u)
    units = np.array(units, dtype=np.int64)
    best = {m: Fraction(0) for m in range(1, mmax + 1)}
    for st in sorted(set(S.states1) | {S.root}):
        aa, ee = S.minslope(st, L)
        pairs = sorted(set(zip(aa.tolist(), ee.tolist())), key=lambda ae: Fraction(g ** ae[0], p ** ae[1]))
        # distinct slope values (a, e) pairs are distinct slopes by unique factorisation
        rank = {ae: i for i, ae in enumerate(pairs)}
        rk = np.array([rank[(a, e)] for a, e in zip(aa.tolist(), ee.tolist())])
        for q in range(1, len(pairs)):
            z = np.nonzero(rk >= q)[0]
            sz = len(z)
            for i0 in range(0, len(units), 256):
                W = units[i0:i0 + 256]
                pos = (W[:, None] * z[None, :]) % N
                B = np.zeros((len(W), N), dtype=np.int32)
                np.put_along_axis(B, pos, 1, axis=1)
                ext = np.concatenate((np.zeros((len(W), 1), dtype=np.int32), B, B), axis=1)
                cs = np.cumsum(ext, axis=1)
                for m in range(1, mmax + 1):
                    Wd = N // p ** m
                    C = cs[:, Wd:Wd + N] - cs[:, :N]
                    mx, mn = int(C.max()), int(C.min())
                    val = max(Fraction(abs(mx * p ** m - sz), sz), Fraction(abs(sz - mn * p ** m), sz))
                    if val > best[m]:
                        best[m] = val
    return best


def secE():
    print("E: Theorem U'_G", flush=True)
    out = {}
    for n, L in [("m3_d", 9), ("sf3_357", 14), ("split5_1", 14), ("sf3_13", 14)]:
        S = get(n)
        out[n] = (L, uprime(S, L, 3))
        print(f"  {n} L={L}: " + ", ".join(f"m={m}: {v} = {float(v):.6f}" for m, v in out[n][1].items()), flush=True)
    # the theorem itself against brute force, small L
    for n, L in [("K7", 6), ("split5_3", 6), ("m3_g", 4), ("desc_s32_plus9", 7)]:
        S = get(n)
        p = S.p
        D = uprime(S, L, 3)
        for b in range(L, L + 4):
            Rb = sum(S.survives(x, b) for x in range(p ** b))
            for m in (1, 2, 3):
                if b - m < 0 or m >= L:
                    continue
                Nb = sum(S.survives(x, b) for x in range(p ** (b - m)))
                pred = Fraction(Rb, p ** m)
                if pred == 0:
                    continue
                ok(abs(Fraction(Nb) / pred - 1) <= D[m], f"E U' {n} L={L} b={b} m={m}: {Nb} vs {pred}, D={D[m]}")
    print("  U' theorem holds against brute force (K7, split5_3, m3_g, desc_s32_plus9)", flush=True)
    return out


# ------------------------------------------------------------------------------------------------ F
def transfer(S, theta):
    st = S.states1
    ix = {s: i for i, s in enumerate(st)}
    M = np.zeros((len(st), len(st)))
    lg, lp = math.log(S.g), math.log(S.p)
    for s in st:
        for (s1, steps) in S.trans[s]:
            a, e = (steps[-1] if steps else (0, 0))
            M[ix[s], ix[s1]] += math.exp(theta * (a * lg - e * lp))
    return M


def rho(S, theta):
    M = transfer(S, theta)
    r = max(abs(np.linalg.eigvals(M)))
    return r, r


def max_cycle_mean(S):
    st = S.states1
    best = {}
    for s in st:
        for (s1, steps) in S.trans[s]:
            a = steps[-1][0] if steps else 0
            best[(s, s1)] = max(best.get((s, s1), -1), a)
    bestmean = None
    succ = {s: [t for (u, t) in best if u == s] for s in st}

    def dfs(start, cur, path, tot):
        nonlocal bestmean
        for t in succ[cur]:
            w = tot + best[(cur, t)]
            if t == start:
                v = Fraction(w, len(path))
                bestmean = v if bestmean is None or v > bestmean else bestmean
            elif t not in path and t > start:
                dfs(start, t, path + [t], w)
    for s in st:
        dfs(s, s, [s], 0)
    return bestmean


def consts(S):
    f = lambda th: math.log(rho(S, th)[1])
    a, b = 0.0, 40.0
    gr = (math.sqrt(5) - 1) / 2
    for _ in range(120):
        c1, d1 = b - gr * (b - a), a + gr * (b - a)
        if f(c1) < f(d1):
            b = d1
        else:
            a = c1
    th = (a + b) / 2
    if f(0.0) <= f(th):
        th = 0.0
    lo, hi = rho(S, th)
    h = math.log(hi) / math.log(S.p)
    H2 = 2 * h - math.log(rho(S, 2 * th)[1]) / math.log(S.p)
    al = max_cycle_mean(S)
    lgp = math.log(S.g) / math.log(S.p)
    c2 = min(1.0, h / 2 + H2 / (2 * float(al) * lgp))
    return dict(theta=th, h=h, H2=H2, alpha=al, c2=c2, Cstar=(1 / (1 - h) if h < 1 - 1e-9 else float("inf")))


def secF():
    print("F: constants", flush=True)
    res = {}
    for n in RULES:
        S = get(n)
        res[n] = consts(S)
        # sanity: h0(K0) <= h for a small K0 (m_GG <= |continuations| <= C rho^K)
        K0 = 60 if S.p == 2 else 40
        h = S.dp(K0)
        tot = sum(h[K0].values())
        ok(math.log(tot, S.p) / K0 <= res[n]["h"] + math.log(100 * len(S.states1), S.p) / K0,
           f"F {n}: survivors exceed rho^K")
    print("  " + "\n  ".join(f"{n:15s} th*={r['theta']:.5f} h={r['h']:.6f} H2={r['H2']:.5f} alpha={r['alpha']} "
                             f"c2={r['c2']:.5f} C*={r['Cstar']:.4f}" for n, r in res.items()), flush=True)
    return res


# ------------------------------------------------------------------------------------------------ G
def secG(K0=40):
    print("G: hypothesis (P)", flush=True)
    res = {}
    for n in RULES:
        S = get(n)
        G = set(S.states1)
        ends = {st: S.dp(K0, start=st)[K0] for st in S.states1}
        while True:
            drop = {st for st in G if sum(c for (s1, A), c in ends[st].items() if s1 in G) == 0}
            if not drop:
                break
            G -= drop
        B = [s for s in S.states1 if s not in G]
        ok(bool(G), f"G {n}: G empty")
        # reachability of G from B
        for s in B:
            seen, fr = {s}, [s]
            hit = False
            while fr:
                x = fr.pop()
                for (t, _) in S.trans[x]:
                    if t in G:
                        hit = True
                    elif t not in seen:
                        seen.add(t); fr.append(t)
            ok(hit, f"G {n}: B-state {s} does not reach G")
        # simple cycles in B (multi-edges kept), slope product < 1
        edges = [(s, t, (stp[-1] if stp else (0, 0))) for s in B for (t, stp) in S.trans[s] if t in B]
        cyc_bad = []
        ncyc = 0

        def dfs(start, cur, visited, A, E):
            nonlocal ncyc
            for (s, t, (a, e)) in edges:
                if s != cur:
                    continue
                if t == start:
                    ncyc += 1
                    if not (S.g ** (A + a) < S.p ** (E + e)):
                        cyc_bad.append((start, A + a, E + e))
                elif t not in visited and B.index(t) > B.index(start):
                    dfs(start, t, visited | {t}, A + a, E + e)
        for s in B:
            dfs(s, s, {s}, 0, 0)
        ok(not cyc_bad, f"G {n}: non-contracting cycle in B {cyc_bad[:3]}")
        # m_GG(K) >= 1 for K0 <= K < 2K0 follows from supermultiplicativity once it holds on [K0, 2K0); check K0..2K0
        hh = {st: S.dp(2 * K0, start=st) for st in G}
        mins = [min(sum(c for (s1, A), c in hh[st][K].items() if s1 in G) for st in G) for K in range(K0, 2 * K0)]
        ok(min(mins) >= 1, f"G {n}: m_GG(K) = 0 for some K in [K0, 2K0)")
        res[n] = (sorted(B), ncyc)
    print("  B and #simple cycles in B:", {n: v for n, v in res.items() if v[0]}, flush=True)
    return res


# ------------------------------------------------------------------------------------------------ H
def order(g, P):
    o, x = 1, g % P
    while x != 1:
        x = x * g % P
        o += 1
    return o


def secH():
    print("H: iota", flush=True)
    claim = {(2, 3): 2, (2, 5): 2, (2, 7): 4, (3, 4): 2, (3, 7): 2, (3, 2): 1, (3, 5): 1, (2, 9): 4}
    for (p, g), io in claim.items():
        idx = []
        for L in range(1, 19 if p == 2 else 12):
            P = p ** L
            idx.append((P - P // p) // order(g, P))
        ok(max(idx) == io and idx[-1] == io, f"H iota({p},{g}) = {idx} vs {io}")
    print("  closed values 2,2,4 (p=2; g=3,5,7) and 2,2,1,1 (p=3; g=4,7,2,5) confirmed", flush=True)


# ------------------------------------------------------------------------------------------------ I
def secI():
    print("I: Lemma F_G exact", flush=True)
    worst = 0
    for (p, g, K) in [(2, 3, 7), (2, 5, 8), (2, 7, 8), (3, 4, 5), (3, 2, 5), (3, 5, 4), (3, 7, 5)]:
        Q = p ** K
        iota = max((p ** L - p ** (L - 1)) // order(g, p ** L) for L in range(1, K + 1))
        H = [1]
        while True:
            u = H[-1] * g % Q
            if u == 1:
                break
            H.append(u)
        for _ in range(4):
            sz = random.randint(1, Q - 1)
            Sset = random.sample(range(Q), sz)
            j = random.randint(1, K - 1)
            N = p ** (K - j)
            mask = np.zeros(Q, dtype=bool)
            mask[Sset] = True
            mean = 0.0
            for u in H:
                mx, mn = windows(mask, u, N, Q)
                mean += max(abs(mx - N * sz / Q), abs(mn - N * sz / Q))
            mean /= len(H)
            bound = iota * p / (p - 1) * (1 + K * math.log(p)) * math.sqrt(sz * (1 - sz / Q))
            worst = max(worst, mean / bound)
            ok(mean <= bound, f"I F_G p={p} g={g} K={K} j={j} |S|={sz}: {mean} > {bound}")
    print(f"  largest ratio {worst:.3f}", flush=True)


# ------------------------------------------------------------------------------------------------ J
def secJ():
    print("J: split5_3, h_* = h in the present coding", flush=True)
    S = get("split5_3")
    mv = {st: [(t, stp[-1] if stp else (0, 0), min([Fraction(1)] + [Fraction(5 ** a, 2 ** e) for a, e in stp]))
               for (t, stp) in S.trans[st]] for st in S.states1}
    print("  digit moves:", mv, flush=True)
    # potential: phi(root)=0, phi(other)=c; log-slope per edge = f(label) + phi(t) - phi(s)
    st = S.states1
    ok(len(st) == 2, "J split5_3 not 2 states")
    # edge slopes as Fractions: f-values must be the same two-element multiset at both states
    # with phi(1,1) - phi(0,0) = -(1/2) log(5/4): f = (slope) * exp(phi(s) - phi(t))  (multiplicatively)
    # check:  label multiset {1/2, sqrt5/2} at both states, i.e. slope^2 * (5/4)^{+-1} in {1/4, 5/4}
    other = [s for s in st if s != (0, 0)][0]
    lab = {}
    for s in st:
        sq = []
        for (t, (a, e), mn) in mv[s]:
            x = Fraction(5 ** a, 2 ** e) ** 2
            # multiplicative potential psi = exp(2 phi): psi(0,0) = 1, psi(other) = 4/5
            psi = {(0, 0): Fraction(1), other: Fraction(4, 5)}
            sq.append(x * psi[s] / psi[t])
        lab[s] = sorted(sq)
    ok(lab[(0, 0)] == lab[other] == [Fraction(1, 4), Fraction(5, 4)], f"J potential fails: {lab}")
    # buffer: need a surviving word from each state with log slope >= Delta + dip, Delta = (1/2)log(5/4),
    # dip = max over moves of (log total - log min prefix within the digit) (min prefix taken relative to 1).
    dip = max(min(1 / mn, Fraction(5 ** a, 2 ** e) / mn) for s in st for (t, (a, e), mn) in mv[s])
    # buffer words: from (0,0) "1,0" ; from (1,1) "0"
    for s0, word in [((0, 0), (1, 0)), (other, (0,))]:
        s, L, okk = s0, Fraction(1), True
        for dgt in word:
            t, (a, e), mn = mv[s][dgt]
            okk &= L * mn >= 1
            L *= Fraction(5 ** a, 2 ** e)
            s = t
        # need L^2 >= (5/4) * dip^2
        ok(okk and L * L >= Fraction(5, 4) * dip * dip, f"J buffer from {s0}: L={L}, dip={dip}")
    print(f"  potential and buffer words from both states exist (dip = {dip}); Raney/types gives h_* = h", flush=True)
    # numerical: m_GG(K) vs rho*^K K^{-3/2}
    h = 0.580684
    hist = {s: S.dp(800, start=s) for s in st}
    for K in (100, 200, 400, 800):
        m = min(sum(hist[s][K].values()) for s in st)
        print(f"   K={K}: log2 m_GG(K)/K = {math.log2(m) / K:.5f}, normalised log2(m 2^(-hK) K^1.5) = "
              f"{math.log2(m) - h * K + 1.5 * math.log2(K):+.3f}", flush=True)


# ------------------------------------------------------------------------------------------------ K
def secK():
    print("K: hypothesis-scan spot checks", flush=True)
    claims = {"split_7081": 2, "split_5": 2, "splitB_71": 2, "desc_s8_35": 4, "desc_s32_max": 30,
              "desc_s32_d65": 30, "m3_a": 1, "m3_c": 1}
    for n, b0 in claims.items():
        S = get(n)
        h = S.dp(b0 + 1)
        cnt = [sum(x.values()) for x in h]
        ok(cnt[b0] == 0 and cnt[b0 + 1] == 0 and (b0 == 1 or cnt[b0 - 1] > 0) and (b0 > 1 or cnt[0] > 0),
           f"K {n}: first empty R_b claimed {b0}, counts {cnt[max(0, b0 - 2):]}")
    for n in ("par_3_2", "par_3_4"):
        try:
            get(n)
            ok(False, f"K {n}: no infinite chain found")
        except RuntimeError:
            pass
    print("  first empty depths as stated; (F) fails for 3n+2, 3n+4", flush=True)


# ------------------------------------------------------------------------------------------------ Z
def secZ(Fres=None, Eres=None):
    print("Z: comparison with the prover's code and data", flush=True)
    sys.path.insert(0, HERE)
    import cwlib, cert
    for n in RULES:
        P = cwlib.SYS[n]
        S = get(n)
        ok(P["p"] == S.p and P["g"] == S.g and P["k"] == S.k and list(map(tuple, P["rows"])) == S.rows,
           f"Z table {n}: prover {P['rows']} vs mine {S.rows}")
    print("  tables identical for all 23 systems", flush=True)
    # constants
    txt = open(os.path.join(HERE, "data", "constants_K1500.txt")).read()
    if Fres:
        for n, r in Fres.items():
            mm = re.search(rf"^{re.escape(n)}\s.*?h=([\d.]+).*?H2=([\d.]+) c1=[\d.]+ c2=([\d.]+)", txt, re.M)
            ok(mm is not None, f"Z constants {n} missing")
            if mm:
                ok(abs(float(mm.group(1)) - r["h"]) < 2e-6, f"Z h {n}: {mm.group(1)} vs {r['h']}")
                ok(abs(float(mm.group(3)) - r["c2"]) < 2e-5, f"Z c2 {n}: {mm.group(3)} vs {r['c2']}")
        print("  h and c2 agree with data/constants_K1500.txt", flush=True)
    if Eres:
        eo = open(os.path.join(HERE, "data", "everyoct.txt")).read()
        for n, (L, D) in Eres.items():
            for m, v in D.items():
                mm = re.search(rf"^{re.escape(n)} L={L} m={m} D'=(\d+)/(\d+)", eo, re.M)
                ok(mm is not None and Fraction(int(mm.group(1)), int(mm.group(2))) == v,
                   f"Z U' {n} L={L} m={m}: prover {mm.groups() if mm else None} vs mine {v}")
        print("  U' constants identical to data/everyoct.txt", flush=True)
    # brackets against the prover's bracket (moderate K, m = 100)
    for n, K, js in [("K7", 14, (1, 3, 6)), ("split5_3", 14, (1, 4)), ("m3_b", 9, (1, 3)),
                     ("desc_s32_plus9", 13, (2,)), ("sf3_135", 13, (1, 2))]:
        S = get(n)
        P = cwlib.System(n)
        for j in js:
            mine = my_bracket(S, 100, j, K)
            Lo, Up, mean, _ = cert.bracket(P, 100, j, K)
            ok(mine == (Lo, Up, mean), f"Z bracket {n} m=100 j={j} K={K}: mine {mine} prover {(Lo, Up, mean)}")
            R = mine[2]
            print(f"   {n} m=100 j={j} K={K}: rel [{(mine[0] * S.p ** j - R) / R:+.5f}, {(mine[1] * S.p ** j - R) / R:+.5f}]",
                  flush=True)
    print("  brackets identical", flush=True)
    # README certified table vs data files (K = 28 / 17 lines)
    rd = open(os.path.join(HERE, "README.md")).read()
    rows = re.findall(r"^\| (\d+) \| (\[.*)$", rd, re.M)
    files = [("K7", 28, 100), ("K7", 28, 1000), ("split5_3", 28, 100), ("split5_3", 28, 1000), ("m3_b", 17, 100),
             ("m3_b", 17, 1000)]
    data = {}
    for (n, K, m) in files:
        for line in open(os.path.join(HERE, "data", f"certified_{n}.txt")):
            mm = re.match(rf"m=\s*{m} j=\s*(\d+) K={K} .*rel_lower=([-+\d.]+) rel_upper=([-+\d.]+)", line)
            if mm:
                data[(n, m, int(mm.group(1)))] = (float(mm.group(2)), float(mm.group(3)))
    nchk = 0
    for jstr, rest in rows:
        cells = re.findall(r"\[([-+\d.]+), ([-+\d.]+)\]", rest)
        if len(cells) != 6:
            continue
        j = int(jstr)
        for (n, K, m), (lo, up) in zip(files, cells):
            dv = data.get((n, m, j))
            ok(dv is not None and abs(dv[0] - float(lo)) < 6e-6 and abs(dv[1] - float(up)) < 6e-6,
               f"Z README C_G {n} m={m} j={j}: README [{lo},{up}] data {dv}")
            nchk += 1
    print(f"  README certified table: {nchk} cells agree with data/certified_*.txt", flush=True)


def main():
    secs = sys.argv[1] if len(sys.argv) > 1 else "ABCDEFGHIJKZ"
    Fres = Eres = None
    if "A" in secs: secA()
    if "B" in secs: secB()
    if "C" in secs: secC()
    if "D" in secs: secD()
    if "E" in secs: Eres = secE()
    if "F" in secs: Fres = secF()
    if "G" in secs: secG()
    if "H" in secs: secH()
    if "I" in secs: secI()
    if "J" in secs: secJ()
    if "K" in secs: secK()
    if "Z" in secs: secZ(Fres, Eres)
    print("ALL REFEREE-2 CHECKS PASSED" if not FAILS else f"{len(FAILS)} FAILURES")
    sys.exit(0 if not FAILS else 1)


if __name__ == "__main__":
    main()
