#!/usr/bin/env python3
"""Referee 2: independent check of round4/integrality (written from scratch).

Imports no prover module (only the standard library).  Exact integers and
Fractions everywhere a claim is decided; floats are used only in Karp's
max-mean-cycle search, where every compared quantity is separated from 0 by a
margin far above float error (stated at each use), and the extremal cycle is
then re-checked exactly.

usage:  python3 referee2_check.py [N]      (N = brute-force bound, default 10^6)
Exit 0 iff every check passes.  Planted errors make it fail (see [neg-*]).
"""
import sys, math, re, os, json, random
from fractions import Fraction
from itertools import product

N = int(sys.argv[1]) if len(sys.argv) > 1 else 10 ** 6
HERE = os.path.dirname(os.path.abspath(__file__))
R3 = os.path.join(HERE, "..", "..", "round3")
OK = True


def claim(name, cond, info=""):
    global OK
    print(("PASS " if cond else "FAIL ") + name + (("  " + str(info)) if info != "" else ""), flush=True)
    OK = OK and bool(cond)


# ============================================================ generic tables
# A table is a list over residues r mod p^m of (u, v, w): T(n) = (u n + v)/w.
def step(table, Q):
    def T(n):
        u, v, w = table[n % Q]
        x = u * n + v
        assert x % w == 0, (n, u, v, w)
        return x // w
    return T


def graph(table, p, m, K):
    """Residue graph at level K >= m: node r mod p^K -> list of (s, Fraction(u, w))."""
    Q, QK = p ** m, p ** K
    G = {}
    for r in range(QK):
        u, v, w = table[r % Q]
        e = 0
        ww = w
        while ww % p == 0:
            ww //= p
            e += 1
        assert ww == 1 and e <= K
        t0 = (u * r + v)
        assert t0 % w == 0
        t0 //= w
        tg = sorted({(t0 + u * p ** (K - e) * k) % QK for k in range(p ** e)})
        G[r] = [(s, Fraction(u, w)) for s in tg]
    return G


def sccs(G):
    idx, low, on, st, out, c = {}, {}, set(), [], [], [0]
    sys.setrecursionlimit(10000)

    def dfs(v):
        idx[v] = low[v] = c[0]
        c[0] += 1
        st.append(v)
        on.add(v)
        for s, _ in G[v]:
            if s not in idx:
                dfs(s)
                low[v] = min(low[v], low[s])
            elif s in on:
                low[v] = min(low[v], idx[s])
        if low[v] == idx[v]:
            comp = []
            while True:
                x = st.pop()
                on.discard(x)
                comp.append(x)
                if x == v:
                    break
            out.append(comp)
    for v in G:
        if v not in idx:
            dfs(v)
    return out


def karp(G, comp, sign):
    """max over cycles in comp of sign*mean(log multiplier); returns value (float)."""
    S = set(comp)
    nodes = list(comp)
    n = len(nodes)
    NEG = -1e300
    src = nodes[0]
    D = [{v: NEG for v in nodes} for _ in range(n + 1)]
    D[0][src] = 0.0
    for k in range(1, n + 1):
        for v in nodes:
            if D[k - 1][v] == NEG:
                continue
            for s, f in G[v]:
                if s in S:
                    val = D[k - 1][v] + sign * math.log(f)
                    if val > D[k][s]:
                        D[k][s] = val
    best = NEG
    for v in nodes:
        if D[n][v] == NEG:
            continue
        worst = min((D[n][v] - D[k][v]) / (n - k) for k in range(n) if D[k][v] != NEG)
        best = max(best, worst)
    return best


def has_cycle(G, comp):
    S = set(comp)
    return len(comp) > 1 or any(s == comp[0] for s, _ in G[comp[0]])


def classify(table, p, m, K=None):
    """('a' | 'b' | 'c_mixed' | 'c_exp').  Float margins: for the families used
    here every non-division-free cycle has |log multiplier| >= 0.05 (checked by
    the assertion below on the returned value), so the sign is exact."""
    K = K or m
    G = graph(table, p, m, K)
    kinds = []
    for comp in sccs(G):
        if not has_cycle(G, comp):
            continue
        mx = karp(G, comp, +1)
        if mx <= 0:
            assert mx < -1e-9
            continue
        S = set(comp)
        simple = all(sum(1 for s, _ in G[v] if s in S) == 1 for v in comp)
        if simple:
            kinds.append("b")
        else:
            mn = karp(G, comp, -1)          # = -min mean
            kinds.append("c_mixed" if mn > 1e-9 else "c_exp")
    if not kinds:
        return "a"
    if "c_mixed" in kinds:
        return "c_mixed"
    if "c_exp" in kinds:
        return "c_exp"
    return "b"


def positive(table, Q):
    T = step(table, Q)
    return all(T(r if r else Q) >= 1 for r in range(Q))


# ============================================================ the systems
def TS(S):
    return lambda n: n // 2 if n % 2 == 0 else (3 * n + 1 if n % 8 in S else n + 1)


def G3(n):
    return (4 * n + 1) // 3 if n % 9 == 8 else -((-n) // 3)


def K7(z):
    if z % 2 == 0:
        return z // 2
    return (3 * z + 1) // 2 if z % 4 == 3 else (z - 1) // 4


CORES = {"sf3_7": ({7}, [[1, 2]]), "sf3_17": ({1, 7}, [[1, 4, 2]]),
         "sf3_57": ({5, 7}, [[1, 2]]), "sf3_157": ({1, 5, 7}, [[1, 4, 2]]),
         "sf3_357": ({3, 5, 7}, [[1, 2]]), "sf3_13": ({1, 3}, [[1, 4, 2], [3, 10, 5, 6]]),
         "sf3_135": ({1, 3, 5}, [[1, 4, 2]])}


def sf_table(S):
    return [(1, 0, 2) if r % 2 == 0 else ((3, 1, 1) if r in S else (1, 1, 1)) for r in range(8)]


G3_TABLE = [(4, 1, 3) if r == 8 else (1, (-r) % 3, 3) for r in range(9)]


def all_drop(T, n_max, cycle_elems, cap_steps=10 ** 5, cap_val=10 ** 40):
    """first n <= n_max (not a listed cycle element) whose orbit does not drop below n, or None."""
    for n in range(1, n_max + 1):
        if n in cycle_elems:
            continue
        x, t = T(n), 1
        while x >= n:
            if x == n or t > cap_steps or x > cap_val:
                return n
            x = T(x)
            t += 1
    return None


def cycles_upto(T, n_max, cap_steps=10 ** 5, cap_val=10 ** 40):
    """set of cycles (as frozenset) reached from n <= n_max; None in set if a start escapes."""
    found, known = set(), {}
    for n in range(1, n_max + 1):
        path, x = [], n
        seen = {}
        while True:
            if x in known:
                res = known[x]
                break
            if x in seen:
                i = seen[x]
                cyc = frozenset(path[i:])
                found.add(cyc)
                res = cyc
                break
            if len(path) > cap_steps or x > cap_val:
                res = None
                found.add(None)
                break
            seen[x] = len(path)
            path.append(x)
            x = T(x)
        for y in path:
            if y < 10 * n_max:
                known[y] = res
    return found


# ============================================================ 1. type (c) of the cores
print("== types")
t = classify(G3_TABLE, 3, 2)
G = graph(G3_TABLE, 3, 2, 2)
comps = [c for c in sccs(G) if has_cycle(G, c)]
claim("[type-G3] G3 residue graph mod 9: one SCC = all 9 nodes, loop 8->8 (4/3), loop 1->1 (1/3), not a simple cycle; c_mixed",
      t == "c_mixed" and len(comps) == 1 and len(comps[0]) == 9
      and (8, Fraction(4, 3)) in G[8] and (1, Fraction(1, 3)) in G[1])
claim("[type-G3] also c_mixed at level 3 (mod 27)", classify(G3_TABLE, 3, 2, 3) == "c_mixed")
claim("[type-G3] table reproduces G3 (= ceil(n/3) off 8 mod 9)",
      all(step(G3_TABLE, 9)(n) == G3(n) for n in range(1, 5000)))
good = True
for name, (S, _) in CORES.items():
    good &= classify(sf_table(S), 2, 3) == "c_mixed" and classify(sf_table(S), 2, 3, 5) == "c_mixed"
claim("[type-S] the 7 S-family cores are c_mixed at levels 3 and 5", good)
claim("[type-K7] K7(z) = (g(2z+1)-1)/2 with g = next odd value of sf3_7, z < 2*10^5",
      all((lambda n: (lambda f: f(f, TS({7})(n)))(lambda f, x: x if x % 2 else f(f, x // 2)))(2 * z + 1)
          == 2 * K7(z) + 1 for z in range(1, 200000)))

# ============================================================ 2. completeness of cycle lists
print("== cycle lists, brute force n <=", N)
for name, (S, cycs) in CORES.items():
    T = TS(S)
    el = {x for c in cycs for x in c}
    bad = all_drop(T, N, el)
    found = cycles_upto(T, min(N, 3 * 10 ** 5))
    claim(f"[drop-{name}] every n <= {N} off the listed cycles drops below itself", bad is None, bad if bad else "")
    claim(f"[cyc-{name}] cycles reached from n <= 3*10^5 are exactly the listed ones",
          found == {frozenset(c) for c in cycs}, sorted(sorted(c) for c in found if c) if found != {frozenset(c) for c in cycs} else "")
bad = all_drop(G3, N, {1})
claim(f"[drop-G3] every n <= {N}, n != 1, drops below itself", bad is None)
claim("[cyc-G3] only cycle reached from n <= 3*10^5 is (1)", cycles_upto(G3, 3 * 10 ** 5) == {frozenset([1])})
claim("[cyc-K7] only cycle reached from 1 <= z <= 3*10^5 is (0)", cycles_upto(K7, 3 * 10 ** 5) == {frozenset([0])})
# negative controls
claim("[neg-drop] sf3_13 without (3 10 5 6) is rejected", all_drop(TS({1, 3}), 1000, {1, 2, 4}) == 3)
TW = TS({1, 3, 7})
Wel = set()
for st in (1, 3, 7, 39):                       # W's four known cycles (round3 sfamily_obst.md)
    x = st
    while True:
        Wel.add(x)
        x = TW(x)
        if x == st:
            break
claim("[neg-drop] W = sf3_137 with all 4 known cycles listed is still rejected, first at n = 15 (orbit passes 10^40)",
      all_drop(TW, 1000, Wel) == 15 and len(Wel) == 3 + 4 + 9 + 15)
claim("[neg-drop] W with only (1 4 2), (3 10 5 6) listed is rejected at n = 7, which lies on W's 9-cycle (7 22 ... 14)",
      all_drop(TW, 1000, {1, 2, 4, 3, 10, 5, 6}) == 7 and 7 in Wel)
claim("[neg-drop] 5x+1 (n/2, 5n+1) is rejected below 100 (cycle at 13, orbit of 7)",
      all_drop(lambda n: n // 2 if n % 2 == 0 else 5 * n + 1, 100, {1, 2, 3, 6, 16, 8, 4}) is not None)

# ============================================================ 3. Theorem C
print("== Theorem C")


def scan(Z0, p, a, c, Ymax=10 ** 6):
    """Independent full scan from Y = 0: least Y with X = least exponent p^X > a^Y
    such that (*) Z0 (p^X - a^Y) < c X a^Y holds.  c may be a Fraction."""
    c = Fraction(c)
    PY = 1
    X = 0
    PX = 1
    for Y in range(0, Ymax + 1):
        if Y:
            PY *= a
        while PX <= PY:
            PX *= p
            X += 1
        if Z0 * (PX - PY) * c.denominator < c.numerator * X * PY:
            return Y, X
    return None


EXP = {(10 ** 9, 2, 3, 2): (15601, 24727), (10 ** 11, 2, 3, 2): (190537, 301994),
       (10 ** 9, 3, 4, 4): (25254, 31867), (10 ** 11, 3, 4, 4): (176251, 222404)}
for (z, p, a, c), e in EXP.items():
    got = scan(z, p, a, c)
    claim(f"[C-scan] Z0={z} p={p} a={a} c={c}: (Y_fail, X_fail) = {e}", got == e, got)
Yf, Xf = 190537, 301994
# X log 2 - Y log 3 at the convergent, by exact rational bracketing of the logs via big ints
d = Fraction(2 ** Xf - 3 ** Yf, 3 ** Yf)      # = 2^X/3^Y - 1 ~ delta
claim("[C-conv] 2^301994/3^190537 - 1 is in (6.3e-8, 6.5e-8) (the near-critical convergent)",
      Fraction(63, 10 ** 9) < d < Fraction(65, 10 ** 9), float(d))
claim("[C-sum] lengths: 301994+190537 = 492531; 10^11 G3: 222404", Xf + Yf == 492531)
# planted errors must fail
claim("[neg-C] planted error: Z0 = 10^7 (instead of 10^9) gives a different (Y_fail, X_fail)",
      scan(10 ** 7, 2, 3, 2) != (15601, 24727))

# falsification: Theorem C must hold on every real cycle of maps in its class
viol, tested, viol_small = 0, 0, 0
for k in range(1, 400, 2):
    if k % 3 == 0:
        continue
    T = lambda n, k=k: n // 2 if n % 2 == 0 else 3 * n + k
    cyc = [cy for cy in cycles_upto(T, 3000, cap_steps=5000, cap_val=10 ** 15) if cy]
    for cy in cyc:
        cy = sorted(cy)
        X = sum(1 for n in cy if n % 2 == 0)
        Y = len(cy) - X
        Z0 = cy[0] - 1
        beta, gamma = Fraction(k, 3), 1           # v = k <= beta*3, odd steps <= X
        cc = 2 * beta * gamma
        if Z0 < 1 or not X < Z0 * math.log(2) / float(beta * gamma):
            continue
        tested += 1
        lhs = Z0 * (2 ** X - 3 ** Y)
        if not (2 ** X > 3 ** Y and 2 ** (X - 1) < 3 ** Y and lhs < cc * X * 3 ** Y):
            viol += 1
        if not lhs < (cc / 8) * X * 3 ** Y:
            viol_small += 1
claim(f"[C-false] Theorem C holds on all {tested} tested cycles of 3x+k (k<400) inside its range", viol == 0 and tested > 50)
claim(f"[neg-C] with c/8 the inequality is violated on {viol_small} of them (the test has teeth)", viol_small > 0)
# 5x+1 cycles (minima 1, 13, 17)
T5 = lambda n: n // 2 if n % 2 == 0 else 5 * n + 1
ok5 = True
for start in (13, 17):
    cy, x = [start], T5(start)
    while x != start:
        cy.append(x)
        x = T5(x)
    X = sum(1 for n in cy if n % 2 == 0)
    Y = len(cy) - X
    Z0 = min(cy) - 1
    ok5 &= Z0 * (2 ** X - 5 ** Y) < Fraction(2, 5) * X * 5 ** Y and 2 ** (X - 1) < 5 ** Y < 2 ** X
claim("[C-false] 5x+1 cycles 13, 17 satisfy (*) (a = 5, beta = 1/5, c = 2/5)", ok5)
# calibration against the literature, 3x+1 (n/2, 3n+1), Z0 = 2^40.
# (i) Theorem C's own constants (beta = 1/3, gamma = 1, c = 2/3) give X_fail = 301994.
# (ii) Eliahou's sharper form X ln2 - Y ln3 <= Y ln(1 + 1/(3 Z0)) reproduces his 17,087,915
#      (float screen, then 60-digit Decimal test).  So the scanner is right and Theorem C
#      is weaker than Eliahou's inequality by one convergent level (P_+ <= X and e^t <= 1+2t).
from decimal import Decimal, getcontext
getcontext().prec = 60
claim("[C-cal] 3x+1, Z0 = 2^40, Theorem C constants: (Y_fail, X_fail) = (190537, 301994)",
      scan(2 ** 40, 2, 3, Fraction(2, 3)) == (190537, 301994))
L2, L3 = math.log(2), math.log(3)
D2, D3 = Decimal(2).ln(), Decimal(3).ln()
cal = None
for Y in range(10 ** 7, 11 * 10 ** 6):          # the convergent 17087915/10781274 lies here
    X = math.floor(Y * L3 / L2) + 1
    if X * L2 - Y * L3 < 1e-5:
        if Decimal(X) * D2 - Decimal(Y) * D3 <= Decimal(Y) * (1 + Decimal(1) / (3 * 2 ** 40)).ln():
            cal = (Y, X)
            break
ok_lo = all(not (Decimal(X) * D2 - Decimal(Y) * D3 <= Decimal(Y) * (1 + Decimal(1) / (3 * 2 ** 40)).ln())
            for Y, X in ((Y, (3 ** Y).bit_length()) for Y in (190537, 111202, 79335, 15601)))
claim("[C-cal] Eliahou's form at Z0 = 2^40 excludes the earlier convergents and first admits X = 17,087,915",
      cal == (10781274, 17087915) and ok_lo, cal)

# ============================================================ 4. Theorem M, R on G3 (exact, finite precision)
print("== Theorem M / R")
L = 12
M3 = 3 ** L
# M(1): D_d = {n = -1 mod 3^(2+d), n != -1 mod 3^(3+d)}; R = -1 + (4/3)^d (n+1)
good = True
for d in range(0, 9):
    for _ in range(200):
        c0 = random.randrange(1, 10 ** 6)
        if c0 % 3 == 0:
            continue
        n = 3 ** (2 + d) * c0 - 1
        x = n
        for _ in range(d):              # d laps of the loop 8 -> 8 (each one step)
            assert x % 9 == 8
            x = G3(x)
        # after d laps the point is back in [8]_2 but no longer = -1 mod 27: it is in D_0
        good &= x == 4 ** d * 9 * c0 - 1 and x % 9 == 8 and x % 27 != 26
        good &= (n + 1) % 3 ** (2 + d) == 0 and (n + 1) % 3 ** (3 + d) != 0
        good &= Fraction(x) == -1 + Fraction(4, 3) ** d * (n + 1)
claim("[M-run] G3: n = 3^(2+d) c - 1 (3 !| c) makes exactly d laps and R(n) = 9*4^d c - 1 in D_0 (d <= 8)", good)
claim("[M-def] lap-count wording: n = 8 follows 0 laps (G3(8) = 11 = 2 mod 9), n = 26 follows 1",
      G3(8) % 9 != 8 and G3(26) % 9 == 8 and G3(G3(26)) % 9 != 8)
# M(2): first-return words to [8]_2, decided exactly mod 3^L.
counts, images = {}, {}
for r in range(8, M3, 9):
    x, prec, word = r, L, []
    while True:
        word.append(x % 9)              # the walk in G_2 (residues mod 9)
        x = G3(x)
        prec -= 1
        if prec < 2:
            word = None
            break
        if x % 9 == 8:
            break
    if word is None:
        continue
    key = tuple(word)
    counts[key] = counts.get(key, 0) + 1
    images.setdefault(key, []).append(x % 3 ** prec)
good = True
for key, cnt in counts.items():
    E = len(key)
    good &= cnt == 3 ** (L - 2 - E)
    im = images[key]
    good &= len(set(im)) == len(im) and all(y % 9 == 8 for y in im) and len(im) == 3 ** (L - E - 2)
claim(f"[M-full] G3: each of {len(counts)} first-return words pi to [8]_2 (decided mod 3^{L}) has exactly "
      "3^(L-2-E) residues and its image is ALL of [8]_2 mod 3^(L-E) (full branch)", good and len(counts) > 50)
# R: n_d identity (G3: x* = -1, K = 2, c' = 1) and Cobham hypothesis
def lapcount_G3(n):
    """largest d with residues mod 9 at times 0..d all = 8 (d steps along the loop)."""
    d, x = 0, n
    while x % 9 == 8 and G3(x) % 9 == 8:
        x = G3(x)
        d += 1
    return d, x


claim("[R-nd] G3: n_d = 3^(2+d) - 1 has lap count d and R(n_d) = 9*4^d - 1 (d < 40)",
      all(lapcount_G3(3 ** (2 + d) - 1) == (d, 9 * 4 ** d - 1) for d in range(40)))
# F5: even n/2, 1 mod 4 -> n+1, 3 mod 4 -> (5n-1)/2 ; x* = 1/3, lambda = 5/2
F5 = lambda n: n // 2 if n % 2 == 0 else (n + 1 if n % 4 == 1 else (5 * n - 1) // 2)
claim("[R-F5] F5 fixed point 1/3: (5x-1)/2 = x at x = 1/3, and 3 = 1/3 mod 8 has branch (5n-1)/2",
      Fraction(5 * Fraction(1, 3) - 1, 2) == Fraction(1, 3) and (3 * 3) % 8 == 1)

# ============================================================ 5. K7 (K1-K3)
print("== K7")
good = True
for z in range(1, 400000, 2):
    j = ((z + 1) & -(z + 1)).bit_length() - 1
    u = (z + 1) >> j
    x = z
    for _ in range(j):
        x = K7(x)
    good &= x == (3 ** (j - 1) * u - 1) // 2 and (3 ** (j - 1) * u - 1) % 2 == 0
    y = 3 ** (j - 1) * u - 1
    if y:
        v = (y & -y).bit_length() - 1
        S = y >> v
        good &= Fraction(S) + Fraction(1, 2) <= Fraction(3 ** (j - 1), 2 ** (j + 1)) * (z + 1)
        good &= (Fraction(S) + Fraction(1, 2) == Fraction(3 ** (j - 1), 2 ** (j + 1)) * (z + 1)) == (v == 1)
        good &= 6 * S + 3 <= (z + 1) ** 1.5849625007211563 + 1e-6 * (z + 1) ** 1.6
        if j <= 4:
            good &= S < z
claim("[K1/K2/K3] excursion formula, first inequality with exact equality case, ceiling, S<z for j<=4 (odd z < 4e5)", good)
claim("[K2-eq] z = 2^j - 1 attains S = (3^(j-1)-1)/2 iff j even (j <= 60)",
      all(((3 ** (j - 1) - 1) % 4 == 2) == (j % 2 == 0) for j in range(2, 61)))
dl = Fraction(0)
for j in range(5, 401):
    s = Fraction(0)
    v = 1
    while 2 ** (j + v) < 3 ** (j - 1):
        s += Fraction(1, 2 ** v)
        v += 1
    dl += Fraction(1, 2 ** j) * s
claim("[K3-delta] delta1 partial sum (j <= 400) = 0.0362745023...", abs(float(dl) - 0.0362745023) < 1e-10, float(dl))
# rising families: z with first k excursions (j, v) = (6, 1); count classes mod 2^(7k+1)
good = True
for k in range(1, 4):
    mod = 2 ** (7 * k + 1)
    cnt = 0
    for z in range(1, mod, 2):
        x, okk = z, True
        for _ in range(k):
            j = ((x + 1) & -(x + 1)).bit_length() - 1
            if j != 6:
                okk = False
                break
            y = 3 ** 5 * ((x + 1) >> 6) - 1
            if (y & -y).bit_length() - 1 != 1:
                okk = False
                break
            x = y >> 1
        if okk:
            # must hold for the whole class: test z + mod * t
            cnt += 1
    good &= cnt == 1
claim("[K3-rise] for k = 1..3 exactly one class mod 2^(7k+1) has k excursions with (j, v) = (6, 1)", good)

# ============================================================ 6. census recount (independent typer)
print("== census (independent enumeration and typing)")


def two_vs(u, r, w):
    if w == 1:
        return [1, -1]
    v0 = (-u * r) % w
    return [v0, v0 - w]


def fam(name):
    if name == "F2m2":
        p, m, us, ws = 2, 2, (1, 3, 5), (1, 2, 4)
    elif name == "F3m2":
        p, m, us, ws = 3, 2, (1, 2, 4), (3,)
    Q = p ** m
    units = [r for r in range(Q) if r % p]
    menus = [[(u, v, w) for u in us for w in ws for v in two_vs(u, r, w)] for r in units]
    for choice in product(*menus):
        tab = [(1, 0, p)] * Q
        for r, ch in zip(units, choice):
            tab[r] = ch
        yield p, m, tab


EXPECT = {"F2m2": {"fails (P)": 86, "a": 54, "b": 0, "c_mixed": 168, "c_exp": 16},
          "F3m2": {"fails (P)": 20736, "a": 9200, "b": 36, "c_mixed": 16668, "c_exp": 16}}
typeb_mine = []
for name in ("F2m2", "F3m2"):
    cnt = {k: 0 for k in EXPECT[name]}
    for p, m, tab in fam(name):
        if not positive(tab, p ** m):
            cnt["fails (P)"] += 1
            continue
        k = classify(tab, p, m)
        cnt[k] += 1
        if k == "b":
            typeb_mine.append(tab)
    claim(f"[census-{name}] independent counts {cnt}", cnt == EXPECT[name])

# type (b): 36 tables, cycle lists by brute force
tb = json.load(open(os.path.join(HERE, "typeb_cycles.json")))
mine = {tuple(map(tuple, t)) for t in typeb_mine}
theirs = {tuple(map(tuple, o["table"])) for o in tb}
claim("[typeb-set] my 36 type-(b) tables are exactly those in typeb_cycles.json", mine == theirs and len(mine) == 36)
good = True
for o in tb:
    T = step([tuple(x) for x in o["table"]], 9)
    found = cycles_upto(T, 20000)
    good &= None not in found and sorted(min(c) for c in found) == sorted(o["cycles"])
claim("[typeb-cyc] for all 36, the cycle minima reached from n <= 20000 equal the listed ones", good)

# ============================================================ 7. dch_C27_2466 (the 80/81 statement)
print("== dch_C27_2466")
rules = {}
for r in range(27):
    if r % 3 == 0:
        rules[r] = (1, 0, 3)
for rs, f in (((1, 10, 14, 19, 23, 26), (1, 1, 1)), ((16,), (1, 2, 1)), ((5, 20), (2, 1, 1)),
              ((2, 7, 8, 13), (2, -1, 1)), ((25,), (4, 1, 1)), ((11,), (4, -1, 1)),
              ((4, 22), (5, 1, 1)), ((17,), (5, -1, 1))):
    for r in rs:
        rules[r] = f
claim("[2466-rule] rule table covers all 27 residues exactly once", sorted(rules) == list(range(27)))
TC = [rules[r] for r in range(27)]
TT = step(TC, 27)
found = cycles_upto(TT, N)
want = {frozenset([1, 2, 3]), frozenset([5, 11, 43, 45, 15]),
        frozenset([125, 624, 208, 209, 419, 420, 140, 281, 1123, 1125, 375])}
claim(f"[2466-cyc] cycles reached from n <= {N} are exactly the 3 listed", found == want)
GC = graph(TC, 3, 3, 3)
comps = [c for c in sccs(GC) if has_cycle(GC, c)]
mx = max(karp(GC, c, +1) for c in comps)
cyc11 = [125, 624, 208, 209, 419, 420, 140, 281, 1123, 1125, 375]
mult = Fraction(1)
for n in cyc11:
    u, v, w = TC[n % 27]
    mult *= Fraction(u, w)
walk_ok = all(any(s == cyc11[(i + 1) % 11] % 27 for s, _ in GC[n % 27]) for i, n in enumerate(cyc11))
claim("[2466-8081] the integer 11-cycle (125 ... 375) traces a residue cycle of multiplier 80/81 = 2^4*5/3^4",
      walk_ok and mult == Fraction(80, 81))
prod_id = Fraction(1)
for n in cyc11:
    u, v, w = TC[n % 27]
    prod_id *= 1 + Fraction(v, u * n)
claim("[2466-id] Theorem C's cycle identity on that cycle: prod(1 + v/(u n)) = 81/80 exactly",
      prod_id == Fraction(81, 80) and TT(cyc11[-1]) == cyc11[0])
claim("[2466-maxmean] Karp: max cycle mean of the residue graph = ln(80/81)/11 = -0.0011294 (all cycles contract)",
      abs(mx - math.log(80 / 81) / 11) < 1e-12 and mx < 0, mx)
txt = open(os.path.join(R3, "dichotomy", "dch_C27_2466.md")).read()
mm = re.search(r"n ≡ (\d+) \(mod (\d+)\)", txt)
a0, M0 = int(mm.group(1)), int(mm.group(2))
n0 = a0 + M0 * 10 ** 12
x, okw = n0, True
for i in range(1, 2466):
    x = TT(x)
    if x < n0:
        okw = False
        break
claim("[2466-wit] witness progression: T^i(n) >= n for 1 <= i < 2466 at n = a + M*10^12 (modulus bits = 1424)",
      okw and M0.bit_length() == 1424)

print("ALL PASS" if OK else "SOME FAIL")
sys.exit(0 if OK else 1)
