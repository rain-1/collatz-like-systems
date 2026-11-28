#!/usr/bin/env python3
"""Referee's independent check for lens 'dichotomy' (round 3).  Exits 0 iff all pass.

Uses only referee_lib.py (written by the referee) plus, for comparison only, the prover's
systems.py tables and the census step functions.  Parts:

 S  the 17 settled systems: tables rebuilt from the WRITTEN rules (claims / <id>.md) and
    compared with systems.py; hypotheses; independent integer potential; exceptional bound;
    complete cycle list by iterating every n <= max N_r; k* by an independent layered search;
    a witness progression built by the referee's own congruence solver, iterated at two
    large t; random starts in [1e20, 1e40] reach the listed cycles (EVIDENCE); maximality
    notes (B27a2 max 14 with 8 sets, D36 maxima 8 / 7); C9-critical divergence.
 T  theorem-level tests on random tables (prime-power and mixed moduli):
    Lemma 1 against brute force; Lemma 2(a) on random walks; Theorem 1 + Theorem 3 against a
    brute-force cylinder computation of the minimal certificate depth; lifting invariance;
    Section 6 counterexample; translation-chain family k* = 2^(m-1).
 P  phase counts: C9 (8^6 tables), B9 (all a), D36 (a = 5, 7), B27 maxima for a <= 8.
 7  Theorem 7: periodic 3x+1 orbits of period <= m/2 are disjoint simple cycles mod 2^m
    (m <= 16); exact dist_{2^m}(3x+1) for m <= 7 by an independent implicit hitting set.
 N  open tables: rebuilt from census step functions, all OBST; every one of the 1330
    stored CERT neighbours re-decided and its cycle list recomputed.
Runtime: about 70 s; --full adds part F (about 6 min); --quick samples.
"""
import sys, os, random, itertools, math, json, time, importlib.util
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from referee_lib import (hyp, stepper, graph, translation_cycle, bad_cycle, potential,
                         verdict, fast_verdict, progression, depth, bounds, all_cycles_upto,
                         settle)

rnd = random.Random(424242)
t0 = time.time()
QUICK = "--quick" in sys.argv


def say(*a):
    print(f"[{time.time() - t0:6.1f}s]", *a, flush=True)


# ============================================================ S: systems from written rules
def B3(Q, a, S):          # 3|n -> n/3; S -> a n + 1; other units -> n+1
    return [(1, 0, 3) if r % 3 == 0 else ((a, 1, 1) if r in S else (1, 1, 1)) for r in range(Q)]


def C(Q, ch):             # 3|n -> n/3; unit r -> ch[r] = (a, b): a n + b
    return [(1, 0, 3) if r % 3 == 0 else (ch[r][0], ch[r][1], 1) for r in range(Q)]


def D(Q, a, S):           # 2|n -> n/2; else 3|n -> n/3; else S -> a n+1 else n+1
    return [(1, 0, 2) if r % 2 == 0 else (1, 0, 3) if r % 3 == 0 else
            ((a, 1, 1) if r in S else (1, 1, 1)) for r in range(Q)]


def S2(m, S, odd_default=(1, 1, 1)):
    Q = 2 ** m
    return [(1, 0, 2) if r % 2 == 0 else ((3, 1, 1) if r in S else odd_default) for r in range(Q)]


c27 = {}
for r in (1, 10, 14, 19, 23, 26): c27[r] = (1, 1)
c27[16] = (1, 2)
for r in (5, 20): c27[r] = (2, 1)
for r in (2, 7, 8, 13): c27[r] = (2, -1)
c27[25] = (4, 1); c27[11] = (4, -1)
for r in (4, 22): c27[r] = (5, 1)
c27[17] = (5, -1)
assert sorted(c27) == [r for r in range(27) if r % 3]

s32p9 = {1, 3, 5, 7, 9, 11, 13, 15, 17, 21, 23, 25, 29}
t_s32 = [(1, 0, 2) if r % 2 == 0 else ((3, 1, 1) if r % 32 in s32p9 else (1, 1, 1)) for r in range(64)]
t_s32[13] = (1, 1, 1)
t_s32[18] = (1, 46, 64)

MINE = {
    "dch_C27_2466": (27, C(27, c27)),
    "dch_B81a2_655": (81, B3(81, 2, {2, 7, 14, 16, 19, 20, 23, 25, 28, 32, 34, 37, 38, 40, 41, 44, 47,
                                     49, 50, 53, 55, 56, 58, 59, 62, 67, 70, 71, 73, 77, 79})),
    "dch_S6_332": (64, S2(6, {5, 7, 13, 23, 25, 31, 33, 35, 39, 47, 49, 51, 59, 61})),
    "dch_B81a5_254": (81, B3(81, 5, {1, 2, 7, 8, 10, 11, 14, 22, 29, 31, 47, 55, 59, 61, 67, 70, 73,
                                     76, 77, 79})),
    "dch_B81a4_184": (81, B3(81, 4, {8, 14, 16, 17, 19, 25, 29, 32, 34, 35, 40, 53, 55, 59, 64, 70,
                                     73, 74})),
    "dch_B27a5_66": (27, B3(27, 5, {2, 4, 16, 17, 23})),
    "dch_B27a8_65": (27, B3(27, 8, {7, 8, 14, 17})),
    "dch_B27a4_49": (27, B3(27, 4, {4, 11, 14, 17, 22})),
    "dch_B27a2_max14": (27, B3(27, 2, {1, 2, 4, 5, 7, 10, 11, 13, 14, 17, 19, 20, 22, 25})),
    "dch_C9_33": (9, C(9, dict(zip([1, 2, 4, 5, 7, 8], [(5, -1), (2, 1), (2, -1), (1, 1), (4, 1), (2, -1)])))),
    "dch_C9_prod2500": (9, C(9, dict(zip([1, 2, 4, 5, 7, 8], [(5, 1), (5, -1), (4, -1), (5, 1), (5, 1), (1, 1)])))),
    "dch_D36a5_8": (36, D(36, 5, {1, 5, 7, 17, 23, 25, 29, 31})),
    "dch_D36a7_7": (36, D(36, 7, {5, 11, 13, 23, 25, 29, 31})),
    "dch_D36a7_43": (36, D(36, 7, {1, 31})),
    "dch_split5_1_nb8": (8, [(1, 0, 2) if r % 2 == 0 else (5, 1, 1) if r == 1 else (3, 1, 1) if r == 5
                             else (1, 1, 1) for r in range(8)]),
    "dch_div23_5n1_nb12": (12, [(1, 0, 2) if r % 2 == 0 else (1, 0, 3) if r % 3 == 0 else
                                ((1, 1, 1) if r in (5, 11) else (5, 1, 1)) for r in range(12)]),
    "dch_s32p9_nb64": (64, t_s32),
}
CLAIM = {   # id: (complete cycle list, k*)  -- from the prover's JSON claims / deep.md
    "dch_C27_2466": ([(1, 2, 3), (5, 11, 43, 45, 15), (125, 624, 208, 209, 419, 420, 140, 281, 1123, 1125, 375)], 2466),
    "dch_B81a2_655": ([(2, 5, 6), (22, 23, 47, 95, 191, 192, 64, 65, 66)], 655),
    "dch_S6_332": ([(1, 2)], 332),
    "dch_B81a5_254": ([(2, 11, 56, 57, 19, 20, 21, 7, 36, 12, 4, 5, 6), (8, 41, 42, 14, 71, 72, 24)], 254),
    "dch_B81a4_184": ([(1, 2, 3)], 184),
    "dch_B27a5_66": ([(1, 2, 11, 12, 4, 21, 7, 8, 9, 3), (28, 29, 146, 147, 49, 50, 251, 252, 84)], 66),
    "dch_B27a8_65": ([(1, 2, 3), (7, 57, 19, 20, 21), (8, 65, 66, 22, 23, 24), (13, 14, 113, 114, 38, 39),
                      (16, 17, 137, 138, 46, 47, 48)], 65),
    "dch_B27a4_49": ([(1, 2, 3)], 49),
    "dch_B27a2_max14": ([(1, 3)], 39),
    "dch_C9_33": ([(2, 5, 6)], 33),
    "dch_C9_prod2500": ([(1, 6, 2, 9, 3)], 6),
    "dch_D36a5_8": ([(1, 6, 3)], 27),
    "dch_D36a7_7": ([(1, 2)], 15),
    "dch_D36a7_43": ([(1, 8, 4, 2)], 43),
    "dch_split5_1_nb8": ([(1, 6, 3, 4, 2)], 5),
    "dch_div23_5n1_nb12": ([(1, 6, 3)], 4),
    "dch_s32p9_nb64": ([(1, 4, 2), (7, 22, 11, 34, 17, 52, 26, 13, 14)], 46),
}

import systems as PS       # prover's tables, compared only
assert set(PS.BY_ID) == set(MINE), set(PS.BY_ID) ^ set(MINE)
for sid, (Q, tab) in MINE.items():
    ps = PS.BY_ID[sid]
    assert ps["Q"] == Q and [tuple(t) for t in ps["table"]] == tab, sid
    T = stepper(Q, tab)
    for n in range(1, 5000):
        assert T(n) == ps["step"](n)
    assert sorted(ps["cycles"]) == sorted(CLAIM[sid][0]) and ps["kstar"] == CLAIM[sid][1], sid
# the census open map desc_s32_plus9 really is the map being modified
spec = importlib.util.spec_from_file_location("r2sys", os.path.join(HERE, "..", "..", "round2", "descent", "systems.py"))
r2 = importlib.util.module_from_spec(spec); sys.path.insert(0, os.path.dirname(spec.origin)); spec.loader.exec_module(r2)
r2s = {s["id"]: s for s in r2.SYSTEMS}["desc_s32_plus9"]["step"]
Ts = stepper(64, t_s32)
for n in range(1, 20000):
    if n % 64 not in (13, 18):
        assert Ts(n) == r2s(n)
say("S0 tables from written rules == systems.py (17 systems)")

for sid, (Q, tab) in MINE.items():
    assert hyp(Q, tab), sid
    res = settle(Q, tab)
    assert res["verdict"] == "CERT", sid
    assert res["cycles"] == sorted(CLAIM[sid][0]), (sid, res["cycles"])
    k, walk = depth(Q, tab, want_walk=True)
    assert k == CLAIM[sid][1], (sid, k)
    pr = progression(Q, tab, walk)
    assert pr is not None
    a, M, A, B, Dd = pr
    T = stepper(Q, tab)
    for t in (10 ** 12, 10 ** 30 + 7):
        n = a + M * t
        x = n
        for i in range(1, k):
            x = T(x)
            assert x >= n, (sid, i)
        assert T(x) < n
    # random large starts reach a listed cycle (EVIDENCE only; GLOBAL is proved by the potential)
    pts = {y for cy in res["cycles"] for y in cy}
    for _ in range(40 if not QUICK else 5):
        x = rnd.randrange(10 ** 20, 10 ** 40)
        it = 0
        while x not in pts:
            x = T(x)
            it += 1
            assert it < 10 ** 7
    say(f"S1 {sid}: CERT, cycles {len(res['cycles'])} (all n <= {res['X']} iterated), k*={k}, witness ok")

# C9-critical: 3|n -> n/3; n+1 on 1,4,7; n+2 on 2,5,8 mod 9 -- every orbit diverges
crit = C(9, {1: (1, 1), 4: (1, 1), 7: (1, 1), 2: (1, 2), 5: (1, 2), 8: (1, 2)})
assert verdict(9, crit)[0] == "OBST-critical"
T = stepper(9, crit)
for r in (1, 2, 4, 5, 7, 8):          # every unit class maps into units, T^6 = +9 symbolically
    u, v, w = crit[r]
    assert (r + v) % 3 != 0
x = 1
for r in (1, 2, 4, 5, 7, 8):
    pass
for n in list(range(1, 3000)) + [rnd.randrange(10 ** 30) for _ in range(50)]:
    y = n
    while y % 3 == 0:
        y = T(y)
    z = y
    for _ in range(6):
        z = T(z)
    assert z == y + 9
say("S2 C9-critical: units closed under T, T^6 = n + 9 on units -> all orbits diverge")

# ============================================================ T: theorem-level random tests
def rand_table(Q, us=(1, 1, 1, 2, 3, 4, 5, 7, 11)):
    divs = [d for d in range(1, Q + 1) if Q % d == 0 and d <= 6]
    tab = []
    for r in range(Q):
        u = rnd.choice([x for x in us if math.gcd(x, Q) == 1])
        w = rnd.choice(divs)
        v = (-u * r) % w + w * rnd.randint(-1, 2)
        n0 = r or Q
        while (u * n0 + v) // w < 1:
            v += w
        tab.append((u, v, w))
    return tab


# Lemma 1 against brute force (mixed moduli included)
for it in range(150):
    Q = rnd.choice([2, 3, 4, 6, 8, 9, 10, 12, 15, 18])
    tab = rand_table(Q)
    T = stepper(Q, tab)
    succ = graph(Q, tab)
    for n in range(1, 300):
        assert T(n) % Q in succ[n % Q]
    for _ in range(4):
        walk = [rnd.randrange(Q)]
        for _ in range(rnd.randint(1, 4)):
            walk.append(rnd.choice(succ[walk[-1]]))
        a, M, A, B, Dd = progression(Q, tab, walk)
        W = math.prod(tab[r][2] for r in walk[:-1])
        assert M == Q * W
        X = 3 * M + a
        brute = []
        for n in range(1, X + 1):
            x, ok = n, True
            for i, r in enumerate(walk):
                if x % Q != r:
                    ok = False; break
                if i < len(walk) - 1:
                    x = T(x)
            if ok:
                brute.append(n)
                assert Dd * x == A * n + B
        assert brute == [a + M * t for t in range((X - a) // M + 1)], (Q, tab, walk)
say("T1 Lemma 1: progression = brute-force set, modulus Q*prod(w)  (150 tables, mixed moduli)")

# Lemma 2(a): random walks with prod u == prod w are translation walks
for it in range(300):
    Q = rnd.choice([4, 6, 9, 12, 30, 36])
    tab = rand_table(Q, us=(1, 1, 1, 1, 2, 5, 7))
    succ = graph(Q, tab)
    walk = [rnd.randrange(Q)]
    for _ in range(rnd.randint(1, 10)):
        walk.append(rnd.choice(succ[walk[-1]]))
    U = math.prod(tab[r][0] for r in walk[:-1]); W = math.prod(tab[r][2] for r in walk[:-1])
    if U == W:
        assert all(tab[r][0] == 1 and tab[r][2] == 1 for r in walk[:-1])
say("T2 Lemma 2(a) on random walks")


def brute_depth(Q, tab, kmax):
    """Minimal max-j of a certificate at modulus Q^(kmax+1), from integers: for each class
    a mod Q^(kmax+1), first j <= kmax with T^j(n) < n at n = a + Q^(kmax+1) * 10^40.
    Returns max over classes (None if some class has no such j)."""
    M = Q ** (kmax + 1)
    T = stepper(Q, tab)
    worst = 0
    for a in range(M):
        n = (a or M) + M * 10 ** 40
        x, j = n, 0
        while j < kmax:
            x = T(x); j += 1
            if x < n:
                break
        else:
            return None
        worst = max(worst, j)
    return worst


nc = no = 0
for it in range(400):
    Q = rnd.choice([2, 3, 4, 6])
    tab = rand_table(Q, us=(1, 1, 1, 2, 3, 5))
    v, c = verdict(Q, tab)
    if v == "CERT":
        k = depth(Q, tab)
        if Q ** (k + 1) > 60000:
            continue
        bd = brute_depth(Q, tab, k)
        assert bd == k, (Q, tab, k, bd)
        if Q ** k <= 60000 and k >= 2:
            assert brute_depth(Q, tab, k - 1) is None or brute_depth(Q, tab, k - 1) > k - 1
        nc += 1
    else:
        # obstruction: the cycle (rotated) is followed by a progression that does not descend
        cyc = c
        U = math.prod(tab[r][0] for r in cyc); W = math.prod(tab[r][2] for r in cyc)
        assert U >= W
        L = len(cyc)
        if U > W:
            pre = [Fraction(1)]
            for r in cyc:
                pre.append(pre[-1] * Fraction(tab[r][0], tab[r][2]))
            mn = min(pre[:L]); i0 = max(i for i in range(L) if pre[i] == mn)
            cyc = cyc[i0:] + cyc[:i0]
        else:
            pre = [0]
            for r in cyc:
                pre.append(pre[-1] + tab[r][1])
            mn = min(pre[:L]); i0 = max(i for i in range(L) if pre[i] == mn)
            cyc = cyc[i0:] + cyc[:i0]
        walk = cyc * 4 + [cyc[0]]
        a, M, A, B, Dd = progression(Q, tab, walk)
        T = stepper(Q, tab)
        n = a + M * 10 ** 30
        x = n
        for i in range(4 * L):
            x = T(x)
            assert x >= n
        no += 1
say(f"T3 Theorems 1/3 vs brute-force cylinders: {nc} CERT tables (k* exact), {no} OBST tables (non-descending laps)")

# lifting invariance and Theorem 1 consistency at a lifted modulus
for it in range(100):
    Q = rnd.choice([2, 3, 4, 6, 9])
    tab = rand_table(Q)
    d = rnd.choice([2, 3])
    big = [tab[r % Q] for r in range(Q * d)]
    if not hyp(Q * d, big):
        continue
    assert (verdict(Q, tab)[0] == "CERT") == (verdict(Q * d, big)[0] == "CERT")
    assert fast_verdict(Q, tab) == verdict(Q, tab)[0] or (fast_verdict(Q, tab).startswith("OBST") and
                                                          verdict(Q, tab)[0].startswith("OBST"))
say("T4 lifting invariance; fast_verdict agrees with verdict")

# Section 6: Q=2, n/2 even, 4n+4 odd
tab6 = [(1, 0, 2), (4, 4, 1)]
assert not hyp(2, tab6)
T = lambda n: n // 2 if n % 2 == 0 else 4 * n + 4
for n in list(range(1, 20001, 2)) + [2 * rnd.randrange(10 ** 40) + 1 for _ in range(100)]:
    x = n
    for _ in range(4):
        x = T(x)
    assert x == (n + 1) // 2 and (n == 1 or x < n)
# residue graph cycle 1 -> 0 -> 1 has multiplier 4 * (1/2) = 2 > 1 in the over-approximating graph
assert (4 * 1 + 4) % 2 == 0
say("T5 Section 6 counterexample")

# translation chains: k* = 2^(m-1), single cycle
for m in range(2, 9):
    Q = 2 ** m
    t = [(1, 0, 2) if r % 2 == 0 else ((1, 1, Q) if r == Q - 1 else (1, 2, 1)) for r in range(Q)]
    res = settle(Q, t)
    assert res["verdict"] == "CERT" and res["cycles"] == [tuple(range(1, Q, 2))]
    assert depth(Q, t) == 2 ** (m - 1)
say("T6 translation-chain family: k* = 2^(m-1), single cycle (m <= 8)")

# ============================================================ P: phase counts
from collections import Counter
CH = [(1, 1), (1, 2), (2, 1), (2, -1), (4, 1), (4, -1), (5, 1), (5, -1)]
U9 = [1, 2, 4, 5, 7, 8]
cnt = Counter()
best_prod, best_tabs = 0, []
cert_tabs = []
for combo in itertools.product(range(8), repeat=6):
    tab = C(9, {r: CH[i] for r, i in zip(U9, combo)})
    v = fast_verdict(9, tab)
    cnt[v] += 1
    if v == "CERT":
        cert_tabs.append(tab)
        p = math.prod(CH[i][0] for i in combo)
        if p > best_prod:
            best_prod, best_tabs = p, [tab]
        elif p == best_prod:
            best_tabs.append(tab)
assert cnt == {"CERT": 11956, "OBST-expanding": 250187, "OBST-critical": 1}, cnt
assert best_prod == 2500 and MINE["dch_C9_prod2500"][1] in best_tabs
say(f"P1 C9 counts {dict(cnt)}; max product of certifiable tables 2500 ({len(best_tabs)} tables)")
if not QUICK:
    kd = Counter(depth(9, tab) for tab in cert_tabs)
    assert max(kd) == 33 and kd[33] == 1, kd
    say(f"P1b C9 depth distribution max 33 (unique); distribution {sorted(kd.items())}")

B9 = {2: (24, 4), 4: (10, 3), 5: (8, 3), 7: (6, 2), 8: (6, 2), 10: (1, 0), 11: (1, 0), 13: (1, 0)}
U9s = [r for r in range(9) if r % 3]
for a, exp in B9.items():
    n = mx = 0
    for k in range(7):
        for S in itertools.combinations(U9s, k):
            if fast_verdict(9, B3(9, a, set(S))) == "CERT":
                n += 1; mx = max(mx, k)
    assert (n, mx) == exp, (a, n, mx)
say("P2 B9 counts")

U36 = [r for r in range(36) if r % 2 and r % 3]
for a, exp, mxs in ((5, 756, (8, 6)), (7, 336, (7, 2))):
    n = 0
    bys = Counter()
    for k in range(13):
        for S in itertools.combinations(U36, k):
            if fast_verdict(36, D(36, a, set(S))) == "CERT":
                n += 1; bys[k] += 1
    mx = max(bys)
    assert n == exp and (mx, bys[mx]) == mxs, (a, n, bys)
say("P3 D36 counts and maxima (5: 756, max 8 by 6 sets; 7: 336, max 7 by 2 sets)")

U27 = [r for r in range(27) if r % 3]
B27max = {2: (14, 8), 4: (13, 1), 5: (10, 7), 7: (8, 5), 8: (8, 6)}
for a, (mx, nmx) in B27max.items():
    if QUICK and a == 5:
        continue
    for k in range(mx, 19):
        c = sum(fast_verdict(27, B3(27, a, set(S))) == "CERT" for S in itertools.combinations(U27, k))
        assert c == (nmx if k == mx else 0), (a, k, c)
say("P4 B27 maxima for a = 2, 4, 5, 7, 8 (no larger certifiable set; number of maximal sets)")

# ============================================================ 7: Theorem 7
def necklaces(L):
    for bits in itertools.product((0, 1), repeat=L):
        if any(bits[i] and bits[(i + 1) % L] for i in range(L)):
            continue
        rots = {bits[i:] + bits[:i] for i in range(L)}
        if len(rots) == L and min(rots) == bits:
            yield bits


for m in range(2, 17):
    Q = 2 ** m
    tab = [(1, 0, 2) if r % 2 == 0 else (3, 1, 1) for r in range(Q)]
    succ = graph(Q, tab)
    used = set()
    for L in range(1, m // 2 + 1):
        for wd in necklaces(L):
            a = sum(wd)
            if 3 ** a <= 2 ** (L - a):
                continue
            # 2-adic periodic point: x = (A x + B)/D
            A, B, Dd = 1, 0, 1
            for b in wd:
                if b:
                    A, B = 3 * A, 3 * B + Dd
                else:
                    Dd *= 2
            x = Fraction(B, Dd - A)
            assert x.denominator % 2 == 1
            res = []
            for b in wd:
                xr = x.numerator * pow(x.denominator, -1, Q) % Q
                assert xr % 2 == b
                res.append(xr)
                x = 3 * x + 1 if b else x / 2
            assert x == Fraction(B, Dd - A)
            assert len(set(res)) == L and not (set(res) & used)
            assert all(res[(i + 1) % L] in succ[res[i]] for i in range(L))
            used |= set(res)
say("7a periodic orbits of period <= m/2: disjoint simple cycles of G_{2^m}, m <= 16")


def min_hitting_set(sets, ub):
    """Exact minimum hitting set by branch and bound (sets: list of frozensets)."""
    best = [None]
    sets = sorted(sets, key=len)

    def rec(chosen, k):
        if best[0] is not None and len(chosen) >= len(best[0]):
            return
        un = next((s for s in sets if not (s & chosen)), None)
        if un is None:
            best[0] = set(chosen)
            return
        # disjoint-packing lower bound
        lb, cov = 0, set()
        for s in sets:
            if not (s & chosen) and not (s & cov):
                lb += 1; cov |= s
        if best[0] is not None and len(chosen) + lb >= len(best[0]):
            return
        if len(chosen) + lb > ub:
            return
        for x in sorted(un):
            rec(chosen | {x}, k)
    rec(frozenset(), 0)
    return best[0]


def hitting_sets_of_size(sets, k):
    """All hitting sets of size exactly k (as frozensets), possibly with repeats."""
    def rec(chosen):
        un = next((s for s in sets if not (s & chosen)), None)
        if un is None:
            if len(chosen) <= k:
                yield chosen
            return
        if len(chosen) == k:
            return
        for x in sorted(un):
            yield from rec(chosen | {x})
    seen = set()
    for h in rec(frozenset()):
        if h not in seen:
            seen.add(h)
            yield h


def distance_exact(Q, tab, max_iter=2000):
    """Implicit hitting set: lower = min hitting set of collected bad cycles of the ORIGINAL
    graph (valid by Proposition 6); upper = some minimum hitting set whose reset table is
    CERT.  Returns (lo, up) with up None if no minimum hitting set's reset table certifies."""
    cycles = [frozenset(bad_cycle(Q, tab))]
    for _ in range(max_iter):
        k = len(min_hitting_set(cycles, Q))
        restart = False
        for R in hitting_sets_of_size(cycles, k):
            bc = bad_cycle(Q, tab, alive=set(range(Q)) - R)
            if bc is not None:
                cycles.append(frozenset(bc))
                restart = True
                break
            t2 = list(tab)
            for r in R:
                t2[r] = (1, (Q - r) % Q, Q)
            assert hyp(Q, t2)
            if fast_verdict(Q, t2) == "CERT":
                return k, k
        if not restart:
            return k, None
    raise RuntimeError


for m, dexp in {1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 4, 7: 5}.items():
    Q = 2 ** m
    tab = [(1, 0, 2) if r % 2 == 0 else (3, 1, 1) for r in range(Q)]
    lo, up = distance_exact(Q, tab)
    assert lo == dexp and up == dexp, (m, lo, up)
say("7b dist_{2^m}(3x+1) = 1,1,1,2,2,4,5 for m = 1..7 (independent implicit hitting set)")

# ============================================================ N: open tables and neighbours
_sp = importlib.util.spec_from_file_location("census_systems", os.path.join(HERE, "..", "..", "systems.py"))
census = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(census)


def table_from_step(Q, step, probe=(1, 2, 3)):
    """Recover the affine branch on each class r mod Q from the census step function and
    verify it on many points; w taken as the least positive denominator."""
    tab = []
    for r in range(Q):
        ns = [r + Q * k for k in range(1, 6)]
        ys = [step(n) for n in ns]
        # slope = (y1-y0)/Q as fraction
        sl = Fraction(ys[1] - ys[0], Q)
        ic = ys[0] - sl * ns[0]
        w = math.lcm(sl.denominator, ic.denominator)
        u, v = int(sl * w), int(ic * w)
        for n in range(r or Q, 6000, Q):
            assert step(n) * w == u * n + v
        tab.append((u, v, w))
    return tab


CEN = {"m3_b_s8": 3, "m3_d_s7": 3, "m3_e_s7": 3, "m3_g_s7": 3, "par_3_13_s27": 2, "par_3_1_s27": 2,
       "par_3_m1_s27": 2, "par_5_1_s5": 2, "par_7_1_s1": 2, "par_9_1_s5": 2, "perm_1932_s8": 3,
       "perm_1932inv_s8": 4, "perm_b_s7": 3, "perm_c_s8": 4, "perm_d_s3": 8, "perm_swap_s8": 3,
       "split5_1_s27": 4, "split5_3_s27": 4, "div23_5n1_s7": 6, "div23_7n1_s5": 6, "div235_7n1_s11": 30}
mine_open = set()
for cid, Q in CEN.items():
    tab = table_from_step(Q, census.get(cid)["step"])
    assert hyp(Q, tab), cid
    v = verdict(Q, tab)[0]
    assert v.startswith("OBST"), (cid, v)
    mine_open.add((Q, tuple(tab)))
for a, ds in ((3, (1, 3, 5, 7, 9, 13, 17, -1)), (5, (1, 3, 5, 7, 11, 131, 353)), (7, (1, 7)), (9, (1,))):
    for d in ds:
        mine_open.add((2, ((1, 0, 2), (a, d, 1))))
mine_open.add((3, ((1, 0, 3), (4, 5, 1), (2, 2, 1))))                       # desc_m3_4n5 (rule text)
mine_open.add((4, ((1, 0, 2), (7, 1, 1), (1, 0, 2), (1, 1, 1))))            # desc_split7_1 (rule text)
mine_open.add((32, tuple((1, 0, 2) if r % 2 == 0 else ((3, 1, 1) if r in s32p9 else (1, 1, 1))
                         for r in range(32))))                              # desc_s32_plus9
import open_tables as _ot
for key, (Q, tab) in _ot.OPEN.items():
    assert (Q, tuple(tuple(t) for t in tab)) in mine_open, key
assert len(_ot.OPEN) == 36   # README/neighbours.md say 34; the list has 36
for d in (1, 3, 5, 7, 9, 13, 17, -1):
    assert verdict(2, [(1, 0, 2), (3, d, 1)])[0].startswith("OBST")
for d in (1, 3, 5, 7, 11, 131, 353):
    assert verdict(2, [(1, 0, 2), (5, d, 1)])[0].startswith("OBST")
for a, d in ((7, 1), (7, 7), (9, 1)):
    assert verdict(2, [(1, 0, 2), (a, d, 1)])[0].startswith("OBST")
for tab in ([(1, 0, 3), (4, 5, 1), (2, 2, 1)], [(1, 0, 2), (7, 1, 1), (1, 0, 2), (1, 1, 1)]):
    assert verdict(len(tab), tab)[0].startswith("OBST")
v, _ = verdict(64, [(1, 0, 2) if r % 2 == 0 else ((3, 1, 1) if r % 32 in s32p9 else (1, 1, 1)) for r in range(64)])
assert v.startswith("OBST")
say("N1 all 36 open table maps of open_tables.py match the referee rebuild (21 from census step functions, 15 from rule text) and are OBST")

NB = json.load(open(os.path.join(HERE, "scratch", "neighbours.json")))
assert len(NB) == 1330
OPEN_BASE = {}
import open_tables   # prover's base tables: re-checked against census above for the 21 census ids
for i, e in enumerate(NB):
    if QUICK and i % 10:
        continue
    Q0, base = open_tables.OPEN[e["entry"]]
    Q = e["Q"]
    assert Q % Q0 == 0
    tab = [tuple(base[r % Q0]) for r in range(Q)]
    for r, kind, br in e["mods"]:
        br = tuple(br)
        if kind == "reset":
            assert br == (1, (Q - r) % Q, Q)
        else:
            assert br[0] < tab[r][0] and br[1:] == tab[r][1:]
        tab[r] = br
    assert hyp(Q, tab)
    res = settle(Q, tab)
    assert res["verdict"] == "CERT", e
    # neighbours.json truncates long cycles with '...': compare count and stored prefixes
    assert len(res["cycles"]) == e["ncycles"] == len(e["cycles"]), e
    stored = sorted(tuple(x for x in c if x != "...") for c in e["cycles"])
    mine_c = sorted(res["cycles"])
    for a_, b_ in zip(stored, mine_c):
        assert b_[:len(a_)] == a_ and (len(a_) == len(b_) or len(a_) == 40), (e, mine_c)
    assert depth(Q, tab) == e["kstar"], e
say("N2 all stored CERT neighbours re-decided: CERT, cycle lists and k* agree")

# ============================================================ F: heavier items (--full, ~5 min)
if "--full" in sys.argv:
    tab8 = [(1, 0, 2) if r % 2 == 0 else (3, 1, 1) for r in range(256)]
    assert distance_exact(256, tab8) == (8, 8)
    say("F1 dist_{2^8}(3x+1) = 8 (exact, independent)")
    # m = 9: implicit-hitting-set lower bound reaches 10
    Q = 512
    tab9 = [(1, 0, 2) if r % 2 == 0 else (3, 1, 1) for r in range(Q)]
    cyc9, R = [], frozenset()
    while len(R) < 10:
        bc = bad_cycle(Q, tab9, alive=set(range(Q)) - R)
        assert bc is not None
        cyc9.append(frozenset(bc))
        R = frozenset(min_hitting_set(cyc9, Q))
    say(f"F2 dist_{{2^9}}(3x+1) >= 10 ({len(cyc9)} verified bad cycles)")
    Q = 1024
    tab10 = [(1, 0, 2) if r % 2 == 0 else (3, 1, 1) for r in range(Q)]
    used, k = set(), 0
    while True:
        bc = bad_cycle(Q, tab10, alive=set(range(Q)) - used)
        if bc is None:
            break
        used |= set(bc); k += 1
    assert k >= 16
    say(f"F3 dist_{{2^10}}(3x+1) >= {k} by a greedy vertex-disjoint packing")
    # round-2 engine agreement claimed in deep.md (engine imported for comparison only)
    sys.path.insert(0, os.path.join(HERE, "..", "..", "round2", "descent"))
    import descent_lib as DL
    S0 = {1, 3, 5, 7, 11, 13, 15, 17, 21, 23, 25, 29}
    t32 = [(1, 0, 2) if r % 2 == 0 else ((3, 1, 1) if r in S0 else (1, 1, 1)) for r in range(32)]
    assert depth(32, t32) == 44 and DL.certificate(2, 5, t32, maxK=200, maxnodes=10 ** 6)["k"] == 44
    c = DL.certificate(2, 6, MINE["dch_S6_332"][1], maxK=400, maxnodes=3 * 10 ** 6)
    assert c["ok"] and c["k"] == 332 and len(c["leaves"]) == 111849
    say("F4 desc_s32_max k*=44 and dch_S6_332 k=332 (111849 leaves) agree with the round-2 engine")
    def liftt(Q0, t, Q1): return [t[r % Q0] for r in range(Q1)]
    for name, Q0, t, lst in (("perm_1932", 3, [(2, 0, 3), (4, -1, 3), (4, 1, 3)], [(9, 4), (27, 8)]),
                             ("split5_1", 4, [(1, 0, 2), (5, 1, 1), (1, 0, 2), (1, 1, 1)], [(8, 1), (16, 1), (32, 2), (64, 3)]),
                             ("div23_5n1", 6, [(1, 0, 2), (5, 1, 1), (1, 0, 2), (1, 0, 3), (1, 0, 2), (5, 1, 1)], [(12, 2), (24, 2), (48, 4)]),
                             ("m3_b", 3, [(1, 0, 3), (4, -1, 3), (4, 1, 3)], [(9, 3), (27, 6), (81, 12)])):
        for Q1, d in lst:
            assert distance_exact(Q1, liftt(Q0, t, Q1)) == (d, d), (name, Q1)
    say("F5 neighbours.md distances spot-checked exactly (perm_1932, split5_1, div23_5n1, m3_b)")
print("REFEREE CHECK: ALL OK")
