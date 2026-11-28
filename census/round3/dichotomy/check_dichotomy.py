#!/usr/bin/env python3
"""Checks for dichotomy.md (Lemmas 1-4, Theorems 1-3, Section 6, Proposition 6, Theorem 7).
Exact arithmetic throughout; exits 0 on success.  Runtime ~2 minutes.

 A  decide.py vs the independent round-2 cylinder engine (descent_lib.certificate) on
    random p-power tables (p = 2, 3, 5): CERT <=> engine certificate, and k* = engine k.
 B  exhaustive S-family m = 2..5: CERT counts 2, 6, 84, 16656 (round-2 family_scan.out);
    SPLIT (Theorem 1 of lemmas.md) and M3 (Theorem 2) classifications reproduced.
 C  Lemma 1 on random walks of random tables, prime-power AND mixed moduli (6, 12, 18, 30, 36):
    progression modulus = Q * prod(w), direct iteration agrees.
 D  Lemma 2 / critical case: the base-3 translation cycle is detected, drift 9 >= 0,
    T^6(n) = n + 9 on its class.
 E  Section 6 counterexample (gcd(u,Q) > 1).
 F  lifting invariance on random tables.
 G  Theorem 2 consistency: for CERT tables, all n <= 3000 reach a listed cycle.
 H  Theorem 7: periodic 3x+1 orbits of period <= m/2 are vertex-disjoint simple cycles
    of G_{2^m} (m <= 14); exact distances dist_{2^m}(3x+1) for m <= 7.
 J  deep.md: k* = 2^(m-1) for the translation-chain maps, m <= 8.
 I  mixed-modulus census maps div23_5n1, div23_7n1, div235_7n1 are OBST (with verified
    expanding cycles), and a mixed CERT example is cross-checked by brute force.
"""
import sys, os, random, math, itertools
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "round2", "descent"))
from decide import *
from families import s_family, lift, base3_table
import descent_lib as DL

rnd = random.Random(20261127)


def rand_table(Q, us=(1, 1, 2, 3, 4, 5, 7, 8, 11, 13), wide=False):
    tab = []
    divs = [d for d in range(1, Q + 1) if Q % d == 0]
    if wide:
        divs = divs[1:] + divs[1:]
    for r in range(Q):
        while True:
            u = rnd.choice(us)
            if math.gcd(u, Q) == 1:
                break
        w = rnd.choice(divs[:4])
        v = (-u * r) % w + w * rnd.randint(-1, 3)
        n0 = r if r else Q
        while (u * n0 + v) // w < 1:
            v += w
        tab.append((u, v, w))
    return tab


# ---------------------------------------------------------------- A
agree = dict(CERT=0, OBST=0)
for it in range(400):
    p = rnd.choice([2, 2, 3, 5])
    m = {2: rnd.choice([1, 2, 3]), 3: rnd.choice([1, 2]), 5: 1}[p]
    Q = p ** m
    tab = rand_table(Q, us=(1, 1, 2, 3, 4, 5, 7), wide=(it % 2 == 0))
    res = decide(Q, tab, want_cycles=False)
    c = DL.certificate(p, m, tab, maxK=50, maxnodes=20000)
    if res["verdict"] == "CERT":
        if not c["ok"]:
            c = DL.certificate(p, m, tab, maxK=400, maxnodes=2 * 10 ** 6)
        assert c["ok"], tab
        DL.verify_certificate(p, m, tab, c["leaves"])
        assert c["k"] == res["kstar"], (tab, c["k"], res["kstar"])
        agree["CERT"] += 1
    else:
        assert not c["ok"], ("engine found a certificate for an OBST table", tab)
        agree["OBST"] += 1
print("A ok", agree)

# ---------------------------------------------------------------- B
expect = {2: 2, 3: 6, 4: 84, 5: 16656}
for m in range(2, 6):
    odd = list(range(1, 2 ** m, 2))
    n = 0
    for mask in range(1 << len(odd)):
        S = {odd[i] for i in range(len(odd)) if mask >> i & 1}
        if decide(2 ** m, s_family(m, S), want_cycles=False, want_depth=False)["verdict"] == "CERT":
            n += 1
    assert n == expect[m], (m, n)
# SPLIT(a,b,d): certifiable iff a < 2^{v_a} and b < 2^{v_b}
for a in range(1, 32, 2):
    for b in range(1, 32, 2):
        for d in (1, 3, 5, 7):
            va = 1 if (a + d) % 4 == 2 else 2
            vb = 1 if (3 * b + d) % 4 == 2 else 2
            tab = [(1, 0, 2), (a, d, 1), (1, 0, 2), (b, d, 1)]
            v = decide(4, tab, want_cycles=False, want_depth=False)["verdict"]
            assert (v == "CERT") == (a < 2 ** va and b < 2 ** vb), (a, b, d)
# M3(a,c1,b,c2) (Theorem 2 of lemmas.md)
for a, b in itertools.product((1, 2, 4, 5, 7, 8), repeat=2):
    for c1, c2 in itertools.product(range(9), repeat=2):
        tab = [(1, 0, 3), (a, c1, 1), (b, c2, 1)]
        i1, i2 = (a + c1) % 3, (2 * b + c2) % 3
        thm = ((i1, i2) == (0, 0) and a <= 2 and b <= 2) or \
              ((i1, i2) == (2, 0) and a * b <= 2 and b <= 2) or \
              ((i1, i2) == (0, 1) and a * b <= 2 and a <= 2)
        v = decide(3, tab, want_cycles=False, want_depth=False)["verdict"]
        assert (v == "CERT") == thm, (a, c1, b, c2, v)
print("B ok")

# ---------------------------------------------------------------- C
for it in range(300):
    Q = rnd.choice([2, 4, 8, 3, 9, 6, 12, 18, 30, 36, 10])
    tab = rand_table(Q)
    check_hypotheses(Q, tab)
    succ = residue_graph(Q, tab)
    T = step_fn(Q, tab)
    # Lemma 1(1): every n follows edges
    for n in range(1, 400):
        assert T(n) % Q in succ[n % Q]
    # Lemma 1(2): random walks are realised with modulus Q * prod w
    for _ in range(5):
        walk = [rnd.randrange(Q)]
        for _ in range(rnd.randint(1, 12)):
            walk.append(rnd.choice(succ[walk[-1]]))
        a, M, A, B, D = path_progression(Q, tab, walk)
        W = 1
        for r in walk[:-1]:
            W *= tab[r][2]
        assert M == Q * W
        for t in (0, 1, 2, 5, 10 ** 9 + 7):
            n = a + M * t
            x = n
            for i in range(len(walk) - 1):
                assert x % Q == walk[i]
                x = T(x)
            assert x % Q == walk[-1] and D * x == A * n + B
print("C ok")

# ---------------------------------------------------------------- D
choice = {1: (1, 1), 2: (1, 2), 4: (1, 1), 5: (1, 2), 7: (1, 1), 8: (1, 2)}
tab = base3_table(9, choice)
res = decide(9, tab, want_cycles=False)
assert res["verdict"] == "OBST" and res["obst"]["kind"] == "critical" and res["obst"]["drift"] == 9
T = step_fn(9, tab)
for n in range(1, 3000, 9):
    x = n
    for _ in range(6):
        x = T(x)
    assert x == n + 9
print("D ok")

# ---------------------------------------------------------------- E
tab = [(1, 0, 2), (4, 4, 1)]
try:
    check_hypotheses(2, tab)
    raise SystemExit("H1 should fail")
except AssertionError:
    pass
U, W = 4 * 1, 1 * 2      # cycle 1 -> 0 -> 1 of the over-approximating graph
assert U > W
T = lambda n: n // 2 if n % 2 == 0 else 4 * n + 4
for n in list(range(3, 20001, 2)) + [10 ** 30 + 1]:
    x = n
    for _ in range(4):
        x = T(x)
    assert x == (n + 1) // 2 < n
# symbolically: n odd -> 4n+4 -> 2n+2 -> n+1 (even) -> (n+1)/2
assert T(1) == 8 and T(8) == 4 and T(4) == 2 and T(2) == 1
print("E ok")

# ---------------------------------------------------------------- F
for it in range(200):
    p = rnd.choice([2, 3])
    Q = p ** rnd.choice([1, 2])
    tab = rand_table(Q)
    v1 = decide(Q, tab, want_cycles=False, want_depth=False)["verdict"]
    v2 = decide(Q * p, lift(Q, tab, p), want_cycles=False, want_depth=False)["verdict"]
    assert v1 == v2
print("F ok")

# ---------------------------------------------------------------- G
ng = 0
for it in range(300):
    Q = rnd.choice([2, 4, 3, 9, 6, 12])
    tab = rand_table(Q, us=(1, 1, 1, 2, 3, 5))
    res = decide(Q, tab, cap=10 ** 6)
    if res["verdict"] != "CERT" or "cycles" not in res:
        continue
    ng += 1
    cyc_pts = {x: i for i, c in enumerate(res["cycles"]) for x in c}
    T = step_fn(Q, tab)
    for n in range(1, 3001):
        x, k = n, 0
        while x not in cyc_pts:
            x = T(x)
            k += 1
            assert k < 10 ** 6
    # potential and exceptional set re-verified
    th = verify_potential(Q, tab, residue_graph(Q, tab), res["weights"])
    assert th < 1
print("G ok", ng, "CERT tables")

# ---------------------------------------------------------------- H
def words(L):
    for bits in itertools.product((0, 1), repeat=L):
        if any(bits[i] and bits[(i + 1) % L] for i in range(L)):
            continue
        # primitive and canonical (least rotation)
        rots = [bits[i:] + bits[:i] for i in range(L)]
        if min(rots) != bits or len(set(rots)) != L:
            continue
        yield bits


def periodic_point(w):
    # lap map x -> (A x + B)/D following parity word w (0: x/2, 1: 3x+1)
    A, B, D = 1, 0, 1
    for b in w:
        if b:
            A, B = 3 * A, 3 * B + D
        else:
            D *= 2
    return Fraction(B, D - A)


def orbit(x, w):
    pts = []
    for b in w:
        assert (x.numerator * pow(x.denominator, -1, 2)) % 2 == b   # parity in Z_2
        pts.append(x)
        x = 3 * x + 1 if b else x / 2
    return pts, x


for m in range(2, 15):
    Q = 2 ** m
    nodes_seen = set()
    count = 0
    for L in range(1, m // 2 + 1):
        for w in words(L):
            a = sum(w)
            if 3 ** a <= 2 ** (L - a):
                continue
            x = periodic_point(w)
            pts, back = orbit(x, w)
            assert back == x
            res = [(p.numerator * pow(p.denominator, -1, Q)) % Q for p in pts]
            assert len(set(res)) == L                      # simple cycle
            assert not (set(res) & nodes_seen)             # disjoint from the others
            nodes_seen |= set(res)
            count += 1
    if m == 14:
        assert count >= 3
from distance import implicit_hitting_set
exact = {1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 4, 7: 5}
for m, d in exact.items():
    lo, up, R, nc, ex = implicit_hitting_set(2 ** m, lift(2, [(1, 0, 2), (3, 1, 1)], 2 ** (m - 1)))
    assert ex and lo == d, (m, lo, up)
    t = lift(2, [(1, 0, 2), (3, 1, 1)], 2 ** (m - 1))
    for r in R:
        t[r] = (1, (2 ** m - r) if r else 0, 2 ** m)
    assert decide(2 ** m, t, want_cycles=False, want_depth=False)["verdict"] == "CERT"
from neighbours import packing_lower_bound
for m, lb in ((10, 16), (11, 19)):
    cyc = packing_lower_bound(2 ** m, lift(2, [(1, 0, 2), (3, 1, 1)], 2 ** (m - 1)))
    t = lift(2, [(1, 0, 2), (3, 1, 1)], 2 ** (m - 1))
    succ = residue_graph(2 ** m, t)
    seen = set()
    for c in cyc:
        assert is_graph_cycle(succ, c) and not (set(c) & seen)
        U, W = cycle_multiplier(t, c)
        assert U > W
        seen |= set(c)
    assert len(cyc) >= lb
print("H ok")

# ---------------------------------------------------------------- I
from open_tables import OPEN
for key in ("div23_5n1 (CLS-002/059)", "div23_7n1 (CLS-003/060)", "div235_7n1 (CLS-001/058)"):
    Q, tab = OPEN[key]
    res = decide(Q, tab, want_cycles=False, want_depth=False)
    assert res["verdict"] == "OBST" and res["obst"]["U"] > res["obst"]["W"]
# mixed CERT example: 2|n -> n/2; else 3|n -> n/3; else n+1   (Q = 6)
tab = [(1, 0, 2), (1, 1, 1), (1, 0, 2), (1, 0, 3), (1, 0, 2), (1, 1, 1)]
res = decide(6, tab)
assert res["verdict"] == "CERT" and res["cycles"] == [(1, 2)]
T = step_fn(6, tab)
for n in range(1, 20000):
    x = n
    while x not in (1, 2):
        x = T(x)
print("I ok")
# ---------------------------------------------------------------- J  (deep.md: cheap unbounded depth)
for m in range(2, 9):
    Q = 2 ** m
    t = [(1, 0, 2) if r % 2 == 0 else ((1, 1, Q) if r == Q - 1 else (1, 2, 1)) for r in range(Q)]
    res = decide(Q, t)
    assert res["kstar"] == 2 ** (m - 1) and res["cycles"] == [tuple(range(1, Q, 2))]
print("J ok")
print("ALL OK")
