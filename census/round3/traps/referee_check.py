"""referee_check.py -- independent referee checks for census/round3/traps.

Written from scratch; it imports NOTHING from the prover's code (traps_lib,
verify, census, family, entropy, minsize, check).  systems.py is read only
to compare its step functions with the written rules.  Exit 0 = all PASS.

  [R1] exact integer weights for the expansion test (used by the C census)
  [R2] full census recomputation (referee_census.c, own graph/SCC/BF) for
       the 9 censuses; compare counts, minimal provable sets, P0/P1 types,
       maximal H sets with results/census_*.json; YAH mod-8 table; F*.
  [R3] YAH homoclinic witnesses of theory.md re-stepped exactly; Theorem 3
       instance: the SCC of x* is non-simple at every level m = k..12.
  [R4] level independence (Cor. 5 / Lemma 6) on random (a,b,k,A), own code.
  [R5] named systems: own Theorem-2-style certificate (own potential, own
       B, own simulation), cycle lists compared; systems.py vs rule;
       hand-proof congruences (incl. the false '16 | 5n+1' claim).
  [R6] Theorem F: type-F minimal sets recomputed vs results/family_*.json;
       E/o thresholds behind Corollaries F2/F3; F1 hand-proof stress test.
  [R7] Theorem E: exact Perron certificates with lambda < 2 for all 130
       maximal H sets (shortcut graph), F*; frontier exponent range.
  [R8] minimum provable odd trap sizes for 3x+1, k = 3..6 (own search).
Runtime: about 1-2 minutes.
"""
import sys, os, json, math, random, subprocess, time
from fractions import Fraction
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
SCR = os.environ.get("REF_SCRATCH", "/tmp")
random.seed(777001)
t0 = time.time()


def say(*a):
    print(*a, flush=True)


# ------------------------------------------------------------------ basics
def res(x, m):
    x = Fraction(x)
    assert x.denominator % 2 == 1
    return (x.numerator * pow(x.denominator, -1, 1 << m)) % (1 << m)


def Cstep(a, b, x):
    """C_{a,b} on Z_(2) rationals / ints"""
    if res(x, 1) == 0:
        return Fraction(x) / 2
    return a * Fraction(x) + b


def graph(a, b, k, m, A):
    M = 1 << m
    bad = lambda r: (r % (1 << k)) in A
    adj = {}
    for r in range(M):
        if bad(r):
            continue
        if r & 1:
            s = [(a * r + b) % M]
        else:
            s = [r // 2, r // 2 + M // 2]
        adj[r] = [x for x in s if not bad(x)]
    return adj


def sccs(adj):
    """Kosaraju, iterative.  Returns list of SCCs (lists)."""
    order, seen = [], set()
    for v0 in adj:
        if v0 in seen:
            continue
        seen.add(v0)
        st = [(v0, iter(adj[v0]))]
        while st:
            v, itr = st[-1]
            nxt = next(itr, None)
            if nxt is None:
                st.pop(); order.append(v)
            elif nxt not in seen:
                seen.add(nxt); st.append((nxt, iter(adj[nxt])))
    radj = {v: [] for v in adj}
    for u in adj:
        for v in adj[u]:
            radj[v].append(u)
    comp, out = {}, []
    for v0 in reversed(order):
        if v0 in comp:
            continue
        c = [v0]; comp[v0] = len(out); st = [v0]
        while st:
            u = st.pop()
            for w in radj[u]:
                if w not in comp:
                    comp[w] = len(out); c.append(w); st.append(w)
        out.append(c)
    return out


_W = {}


def weights(a):
    """(P_up, P_lo, Q) with a^Q < 2^P_up and 2^P_lo < a^Q, for growing Q"""
    out = []
    for Q in (94, 1024, 16384, 262144):
        Pl = int(Q * math.log2(a)) - 2
        while 2 ** (Pl + 1) < a ** Q:
            Pl += 1
        Pu = Pl + 1
        assert 2 ** Pl < a ** Q < 2 ** Pu
        out.append((Pu, Pl, Q))
    return out


def pos_cycle(S, adj, wo, we):
    """Bellman-Ford: is there a cycle in S with sum of weights > 0
    (odd-node edge weight wo, even-node edge weight we)?"""
    Ss = set(S)
    d = {u: 0 for u in S}
    for it in range(len(S) + 1):
        ch = False
        for u in S:
            w = wo if u & 1 else we
            for v in adj[u]:
                if v in Ss and d[u] + w > d[v]:
                    d[v] = d[u] + w; ch = True
        if not ch:
            return False
    return True


def has_expanding(a, S, adj):
    if a not in _W:
        _W[a] = weights(a)
    for (Pu, Pl, Q) in _W[a]:
        if not pos_cycle(S, adj, Pu, -Q):
            return False          # o Pu - E Q <= 0 for all cycles => a^o < 2^E
        if pos_cycle(S, adj, Pl, -Q):
            return True           # some cycle o Pl > E Q => a^o > 2^E
    raise RuntimeError("expansion test undecided")


def classify(a, b, k, m, A):
    """'H', 'P1' or 'P0' (own implementation of the SCC criterion)"""
    adj = graph(a, b, k, m, A)
    anyexp = False
    for S in sccs(adj):
        Ss = set(S)
        outd = [sum(1 for v in adj[u] if v in Ss) for u in S]
        if sum(outd) == 0:
            continue
        simple = all(d == 1 for d in outd)
        exp = has_expanding(a, S, adj)
        anyexp |= exp
        if exp and not simple:
            return "H"
    return "P1" if anyexp else "P0"


# ------------------------------------------------------------------ [R1]
PQ = {3: (149, 94), 5: (202, 87), 7: (233, 83)}
for a, (P, Q) in PQ.items():
    for o in range(1, 65):
        for E in range(0, 201):
            assert (o * P - E * Q != 0) and ((o * P - E * Q > 0) == (a ** o > 2 ** E))
say("[R1] exact weights for the C census verified (o <= 64, E <= 200)  PASS")

# ------------------------------------------------------------------ [R2]
exe = os.path.join(SCR, "ref_census")
src = os.path.join(HERE, "referee_census.c")
if not os.path.exists(exe) or os.path.getmtime(exe) < os.path.getmtime(src):
    subprocess.check_call(["gcc", "-O2", "-o", exe, src])

runs = [(3, 3, "all"), (3, 4, "all"), (3, 5, "odd"), (5, 3, "all"), (5, 4, "all"),
        (5, 5, "odd"), (7, 3, "all"), (7, 4, "all"), (7, 5, "odd")]
CEN = {}
tot_min = tot_max = 0
for a, k, uni in runs:
    P, Q = PQ[a]
    s = subprocess.check_output(["nice", exe, str(a), str(k), uni, str(P), str(Q)]).decode().strip()
    U = [r for r in range(1 << k) if uni == "all" or r % 2]
    n = len(U)
    assert len(s) == 1 << n
    prov = [c != "0" for c in s]
    # monotonicity (node-deleted subgraphs)
    for mask in range(1 << n):
        if prov[mask]:
            for j in range(n):
                assert prov[mask | (1 << j)], ("monotone", a, k, mask)
    minimal = [mask for mask in range(1 << n) if prov[mask]
               and all(not prov[mask & ~(1 << j)] for j in range(n) if mask >> j & 1)]
    maximal = [mask for mask in range(1 << n) if not prov[mask]
               and all(prov[mask | (1 << j)] for j in range(n) if not mask >> j & 1)]
    toset = lambda mask: sorted(U[j] for j in range(n) if mask >> j & 1)
    stored = json.load(open(os.path.join(HERE, "results", f"census_C{a}_k{k}_{uni}.json")))
    st = {"P": sum(prov), "H": (1 << n) - sum(prov)}
    assert st == stored["stats"], (a, k, uni, st, stored["stats"])
    mins = sorted(toset(x) for x in minimal)
    assert mins == sorted(m["A"] for m in stored["minimal_provable"]), (a, k, uni)
    typ = {tuple(toset(x)): ("P0" if s[x] == "2" else "P1") for x in minimal}
    for m in stored["minimal_provable"]:
        assert typ[tuple(m["A"])] == m["type"], (a, k, m["A"], typ[tuple(m["A"])], m["type"])
    maxs = sorted(toset(x) for x in maximal)
    assert maxs == sorted(stored["maximal_H"]), (a, k, uni)
    CEN[(a, k, uni)] = (U, s, mins, maxs, typ)
    tot_min += len(mins); tot_max += len(maxs)
    say(f"     C{a} k={k} {uni}: P={st['P']} H={st['H']} minimal={len(mins)} "
        f"(P0={sum(1 for t in typ.values() if t == 'P0')}) maxH={len(maxs)}  matches JSON")
assert tot_min == 490 and tot_max == 130
# YAH mod-8 statement: provable iff A not subset of {1} and not subset of {0,5,7}
U, s, mins, maxs, typ = CEN[(3, 3, "all")]
for mask in range(256):
    A = {r for r in range(8) if mask >> r & 1}
    pv = s[mask] != "0"
    assert pv == (not A <= {1} and not A <= {0, 5, 7}), A
for A in [{2}, {3}, {4}, {6}, {1, 5}, {1, 7}]:
    assert s[sum(1 << r for r in A)] != "0"
for A in [{0}, {1}, {5}, {7}, {5, 7}]:
    assert s[sum(1 << r for r in A)] == "0"
# F*: the unique maximal H set mod 16 containing the lift of {5,7}
U, s, mins, maxs, typ = CEN[(3, 4, "all")]
lift57 = {5, 7, 13, 15}
cont = [m for m in maxs if lift57 <= set(m)]
assert cont == [[0, 3, 5, 7, 8, 10, 13, 14, 15]], cont
Fstar = {0, 3, 5, 7, 8, 10, 13, 14, 15}
fm = lambda A: sum(1 << r for r in A)
assert s[fm(Fstar)] == "0"
assert sorted(r for r in range(16) if r not in Fstar and s[fm(Fstar | {r})] != "0") == [1, 2, 4, 6, 9, 11, 12]
for lifted, expect in [({7, 15}, 3), ({1, 9}, 2), ({0, 8}, 2), ({5, 13}, 2)]:
    assert len([m for m in maxs if lifted <= set(m)]) == expect
# no minimal provable odd set mod 32 is P0 for 5x+1, 7x+1
for a in (5, 7):
    assert all(t == "P1" for t in CEN[(a, 5, "odd")][4].values())
say(f"[R2] 9 censuses recomputed independently: {tot_min} minimal, {tot_max} maximal H, "
    "all counts/types match; YAH mod-8 rule; F* unique  PASS")

# ------------------------------------------------------------------ [R3]
def orbit_cycle(a, b, x, maxL=200):
    o = [Fraction(x)]
    while True:
        y = Cstep(a, b, o[-1])
        if y == o[0]:
            return o
        o.append(y)
        assert len(o) < maxL


wit = {(7,): (-20, -28), (5, 7): (-14, Fraction(-58, 3)), (1,): (-1, Fraction(-17, 9)),
       (0,): (-1, Fraction(-35, 27)), (5,): (-2, Fraction(-26, 9))}
for A, (x, z) in wit.items():
    A = set(A)
    orb = orbit_cycle(3, 1, x)
    o = sum(1 for y in orb if res(y, 1) == 1); E = len(orb) - o
    assert 3 ** o > 2 ** E
    assert all(res(y, 3) not in A for y in orb)
    z = Fraction(z)
    assert z not in orb and res(z, 3) == res(x, 3)
    y, j = z, 0
    while y not in orb:
        assert res(y, 3) not in A
        y = Cstep(3, 1, y); j += 1
        assert j < 100
# Theorem 3 instance: at every level m <= 12 the SCC through x*'s residues is
# non-simple (and contains the expanding cycle of x*)
for A, (x, z) in list(wit.items()) + [(tuple(Fstar), (-14, None))]:
    k = 3 if len(A) < 6 else 4
    A = set(A)
    orb = orbit_cycle(3, 1, x)
    assert all(res(y, k) not in A for y in orb)
    for m in range(k, 13):
        adj = graph(3, 1, k, m, A)
        r0 = res(orb[0], m)
        S = next(c for c in sccs(adj) if r0 in c)
        Ss = set(S)
        assert all(res(y, m) in Ss for y in orb)
        assert any(sum(1 for v in adj[u] if v in Ss) >= 2 for u in S), (A, m)
say("[R3] YAH witnesses re-stepped exactly; SCC of x* non-simple at levels k..12 "
    "for {0},{1},{5},{7},{5,7},F*  PASS")

# ------------------------------------------------------------------ [R4]
cnt = {"P": 0, "H": 0}
for trial in range(250):
    a = random.choice([3, 5, 7, 9, 11, 13])
    b = random.choice([1, 3, 5, 7])
    k = random.choice([3, 4])
    A = {r for r in range(1 << k) if random.random() < random.choice([0.15, 0.3])}
    v = [classify(a, b, k, m, A) == "H" for m in range(k, k + 4)]
    assert len(set(v)) == 1, (a, b, k, A, v)
    cnt["H" if v[0] else "P"] += 1
# compare own Python classifier with own C census on random sets (b = 1)
for (a, k, uni), (U, s, *_ ) in CEN.items():
    for _ in range(150):
        mask = random.randrange(1 << len(U))
        A = {U[j] for j in range(len(U)) if mask >> j & 1}
        c = classify(a, 1, k, k, A)
        assert (c == "H") == (s[mask] == "0")
        if c != "H":
            assert (c == "P0") == (s[mask] == "2")
say(f"[R4] verdict independent of level k..k+3 on 250 random (a,b,k,A) {cnt}; "
    "Python and C classifiers agree  PASS")

# ------------------------------------------------------------------ [R5]
sys.path.insert(0, HERE)
import systems as SY  # step functions only


def own_certificate(a, b, k, A):
    """Theorem-2 certificate built with my own potential:
    V(n) = n * 2^(psi(n mod 2^k)/Q), psi(u) >= psi(v) + w(u->v) + 1 on every
    internal edge of a non-simple SCC, w = P (odd) or -Q (halving),
    a^Q < 2^P.  Then odd step ratio <= (a + b/n) 2^(-(P+1)/Q) and halving
    ratio <= 2^(-1/Q).  Returns (B, cycles reached from [1, B] avoiding A,
    positive integer lifts of simple components)."""
    adj = graph(a, b, k, k, A)
    comps = sccs(adj)
    cid = {u: i for i, c in enumerate(comps) for u in c}
    lifts, used = [], []
    for S in comps:
        Ss = set(S)
        ie = [(u, v) for u in S for v in adj[u] if v in Ss]
        if not ie:
            continue
        outd = {u: 0 for u in S}
        for u, v in ie:
            outd[u] += 1
        if all(d == 1 for d in outd.values()):
            nxt = dict(ie); cyc = [S[0]]
            while nxt[cyc[-1]] != S[0]:
                cyc.append(nxt[cyc[-1]])
            # exact lift: compose the affine branches, value = num*x + c
            num, c = Fraction(1), Fraction(0)
            for r in cyc:
                if r & 1:
                    num, c = num * a, a * c + b
                else:
                    num, c = num / 2, c / 2
            x = c / (1 - num)
            y = x
            for r in cyc:
                assert res(y, k) == r
                y = Cstep(a, b, y)
            assert y == x
            if x.denominator == 1 and x > 0:
                lifts.append(int(x))
            continue
        ok = False
        for Q in (2 ** 8, 2 ** 11, 2 ** 14, 2 ** 17):
            P = int(Q * math.log2(a)) - 1
            while a ** Q >= 2 ** P:
                P += 1
            psi = {u: 0 for u in S}
            for it in range(len(S) + 2):
                ch = False
                for u, v in ie:
                    w = (P if u & 1 else -Q) + 1
                    if psi[v] + w > psi[u]:
                        psi[u] = psi[v] + w; ch = True
                if not ch:
                    ok = True; break
            if ok:
                for u, v in ie:
                    assert psi[u] >= psi[v] + (P if u & 1 else -Q) + 1
                used.append((Q, P))
                break
        assert ok, "no potential"
    # B: least n0 with ((a n0 + b)/n0)^Q < 2^(P+1), max over the (Q, P) used
    B = 0
    for (Q, P) in used:
        assert a ** Q < 2 ** P
        n0 = 1
        while not ((a * n0 + b) ** Q < 2 ** (P + 1) * n0 ** Q):
            n0 = n0 * 2
        lo, hi = n0 // 2, n0
        while hi - lo > 1:
            mid = (lo + hi) // 2
            if (a * mid + b) ** Q < 2 ** (P + 1) * mid ** Q:
                hi = mid
            else:
                lo = mid
        B = max(B, hi)
    # simulate [1, B]
    Mk = 1 << k
    cycles = set()
    for n0 in range(1, B + 1):
        x, seen = n0, {}
        while x % Mk not in A and x not in seen:
            seen[x] = len(seen)
            x = x // 2 if x % 2 == 0 else a * x + b
            assert len(seen) < 10 ** 6
        if x % Mk not in A:
            cyc = [y for y, i in sorted(seen.items(), key=lambda t: t[1]) if i >= seen[x]]
            i = cyc.index(min(cyc))
            cycles.add(tuple(cyc[i:] + cyc[:i]))
    for p in lifts:
        cyc = [p]; y = a * p + b if p % 2 else p // 2
        while y != p:
            cyc.append(y); y = a * y + b if y % 2 else y // 2
        i = cyc.index(min(cyc)); cycles.add(tuple(cyc[i:] + cyc[:i]))
    return B, sorted(cycles), lifts


claimed = {
    "trap7_57": [(1, 8, 4, 2)],
    "trap5_17": [],
    "trap5_hi16": [(1, 6, 3, 16, 8, 4, 2)],
    "trap5_c13": [(13, 66, 33, 166, 83, 416, 208, 104, 52, 26)],
    "trap7_m32": [(1, 8, 4, 2)],
    "trap3_m32": [(1, 4, 2)],
}
written = {  # the rules as written in the <id>.md files
    "trap7_57": (7, 3, {5, 7}), "trap5_17": (5, 3, {1, 7}), "trap5_hi16": (5, 4, {9, 11, 13, 15}),
    "trap5_c13": (5, 5, {3, 5, 7, 15, 17, 23}), "trap7_m32": (7, 5, {5, 7, 13, 23, 27}),
    "trap3_m32": (3, 5, {7, 15, 25}),
}
for sid, (a, k, A) in written.items():
    a2, b2, k2, A2, _ = SY.SYSTEMS[sid]
    assert (a2, b2, k2, set(A2)) == (a, 1, k, A), sid
    step = SY.STEP[sid]
    for n in list(range(1, 5000)) + [random.getrandbits(200) for _ in range(500)]:
        exp = 1 if n % (1 << k) in A else (n // 2 if n % 2 == 0 else a * n + 1)
        assert step(n) == exp
    assert classify(a, 1, k, k, A) != "H"
    B, cyc, lifts = own_certificate(a, 1, k, A)
    assert cyc == claimed[sid], (sid, cyc)
    # minimality claims (trap5_c13, trap7_m32, trap3_m32): every deletion is H
    if sid in ("trap5_c13", "trap7_m32", "trap3_m32"):
        for q in A:
            assert classify(a, 1, k, k, A - {q}) == "H"
    # evidence: random huge n meet A, or fall to <= B
    for _ in range(100):
        x = random.getrandbits(random.choice([100, 400, 1000]))
        t = 0
        while x % (1 << k) not in A and x > B:
            x = x // 2 if x % 2 == 0 else a * x + 1; t += 1
            assert t < 10 ** 6
    say(f"     {sid}: own B={B}, cycles {cyc}")
# trap5_c13: exactly 10 minimal odd sets mod 32 whose cycle list is just the 13-cycle
stored = json.load(open(os.path.join(HERE, "results", "census_C5_k5_odd.json")))
c13 = [m["A"] for m in stored["minimal_provable"]
       if [list(c) for c in m["cycles"]] == [[13, 66, 33, 166, 83, 416, 208, 104, 52, 26]]]
assert len(c13) == 10 and [3, 5, 7, 15, 17, 23] in c13
for A in c13[:4]:
    assert own_certificate(5, 1, 5, set(A))[1] == [(13, 66, 33, 166, 83, 416, 208, 104, 52, 26)]
# hand-proof congruences: the written '16 | 5n+1' (trap7_57) and '16 | 3n+1'
# (trap5_17) are FALSE as stated; the true statement is 8 | ., and suffices.
assert (5 * 11 + 1) % 16 != 0 and 11 % 8 == 3
assert (3 * 13 + 1) % 16 != 0 and 13 % 8 == 5
for n in range(1, 1 << 16, 2):
    assert (n % 8 == 3) == ((5 * n + 1) % 8 == 0)
    assert (n % 8 == 5) == ((3 * n + 1) % 8 == 0)
    assert (n % 16 == 5) == ((3 * n + 1) % 16 == 0)      # trap5_hi16 version is right
    if n % 8 == 3:
        N = (7 * n + 1) // 2
        assert (7 * n + 1) % 4 == 2 and N % 4 == 3 and 5 * N + 1 == Fraction(7, 2) * (5 * n + 1)
    if n % 8 == 5:
        N = (5 * n + 1) // 2
        assert (5 * n + 1) % 4 == 2 and N % 4 == 1 and 3 * N + 1 == Fraction(5, 2) * (3 * n + 1)
# trap5_hi16 hand potential, exact: ratios along edges for n >= 64
w = {1: Fraction(63, 25), 3: Fraction(1), 7: Fraction(79, 25)}
for (c, c2, d) in [(1, 3, 2), (3, 1, 16), (3, 3, 16), (3, 7, 16), (7, 1, 4)]:
    assert w[c2] * (5 + Fraction(1, 64)) / (d * w[c]) < 1
# the odd-step transitions on untrapped classes mod 16 (from n mod 2^10)
for n in range(1, 1 << 12, 2):
    r = n % 16
    y, v = 5 * n + 1, 0
    while y % 2 == 0:
        y //= 2; v += 1
    if r == 1: assert v == 1 and y % 16 in (3, 11)
    if r == 3: assert v >= 4
    if r == 5: assert v == 1 and y % 16 in (5, 13)
    if r == 7: assert v == 2 and y % 16 in (1, 5, 9, 13)
say("[R5] named systems: own certificates reproduce all cycle lists; systems.py matches "
    "rules; minimality; hand-proof facts (two congruences mis-stated, see REFEREE.md)  PASS")

# ------------------------------------------------------------------ [R6]
def typeF(a0, b0, k, A):
    adj = graph(a0, b0, k, k, A)
    simple = []
    for S in sccs(adj):
        Ss = set(S)
        outd = [sum(1 for v in adj[u] if v in Ss) for u in S]
        if sum(outd) == 0:
            continue
        if any(d != 1 for d in outd):
            return None
        o = sum(1 for u in S if u & 1)
        simple.append((o, len(S) - o))
    return simple


for k, uni, fn in [(3, "odd", "family_k3_odd.json"), (3, "all", "family_k3_all.json"),
                   (4, "odd", "family_k4_odd.json")]:
    stored = json.load(open(os.path.join(HERE, "results", fn)))
    U = [r for r in range(1 << k) if uni == "all" or r % 2]
    thr = 2 if k == 3 else 3
    for a0 in range(1, 1 << k, 2):
        for b0 in range(1, 1 << k, 2):
            mins = []
            for size in range(len(U) + 1):
                for A in combinations(U, size):
                    if any(set(m) <= set(A) for m in mins):
                        continue
                    if typeF(a0, b0, k, set(A)) is not None:
                        mins.append(A)
            assert sorted(map(list, mins)) == sorted(stored[f"{a0},{b0}"]), (k, uni, a0, b0)
            if uni == "odd":
                assert len(mins) == (2 if k == 3 else 6)
                for A in mins:
                    for (o, E) in typeF(a0, b0, k, set(A)):
                        assert o == 0 or E <= thr * o, (a0, b0, A, o, E)
            else:
                assert (4,) in mins
fam_table = {(1, 1): [[3, 7], [5, 7]], (1, 3): [[1, 5], [5, 7]], (1, 5): [[1, 3], [3, 7]],
             (1, 7): [[1, 3], [1, 5]], (3, 1): [[1, 5], [3, 5]], (3, 3): [[1, 7], [3, 7]],
             (3, 5): [[1, 5], [1, 7]], (3, 7): [[3, 5], [3, 7]], (5, 1): [[1, 3], [3, 7]],
             (5, 3): [[1, 3], [1, 5]], (5, 5): [[3, 7], [5, 7]], (5, 7): [[1, 5], [5, 7]],
             (7, 1): [[1, 5], [1, 7]], (7, 3): [[3, 5], [3, 7]], (7, 5): [[1, 5], [3, 5]],
             (7, 7): [[1, 7], [3, 7]]}
stored = json.load(open(os.path.join(HERE, "results", "family_k3_odd.json")))
for (a0, b0), pairs in fam_table.items():
    assert sorted(stored[f"{a0},{b0}"]) == sorted(pairs), (a0, b0)
# F1 and F2 stress test (EVIDENCE): huge a, b, n
for _ in range(3000):
    a = random.randrange(3, 10 ** 6, 2); b = random.randrange(1, 10 ** 6, 2)
    n = random.getrandbits(random.choice([20, 200]))
    if n == 0:
        continue
    x, t = n, 0
    while x % 8 != 4:
        x = x // 2 if x % 2 == 0 else a * x + b; t += 1
        assert t < 10 ** 5
    if a >= 5:
        for A in fam_table[(a % 8, b % 8)]:
            x, t = n, 0
            while x % 8 not in A:
                x = x // 2 if x % 2 == 0 else a * x + b; t += 1
                assert t < 10 ** 5
say("[R6] Theorem F: type-F minimal sets recomputed (mod 8 all/odd, mod 16 odd) = JSON; "
    "E <= 2o (mod 8), E <= 3o (mod 16) on all simple cycles; family table; stress test  PASS")

# ------------------------------------------------------------------ [R7]
import numpy as np


def shortcut_adj(a, b, k, A):
    K = 1 << k
    adj = {}
    for r in range(K):
        if r in A:
            continue
        y = (a * r + b) // 2 if r & 1 else r // 2
        adj[r] = [s for s in ((y % (K // 2)), (y % (K // 2)) + K // 2) if s not in A]
    return adj


def perron(adj):
    nodes = sorted(adj); ix = {u: i for i, u in enumerate(nodes)}
    M = np.zeros((len(nodes), len(nodes)))
    for u in nodes:
        for v in adj[u]:
            M[ix[u], ix[v]] += 1
    rho = max(abs(np.linalg.eigvals(M))) if nodes else 0.0
    lam = Fraction(int(rho * 1e7) + 3, 10 ** 7)
    vf = np.linalg.solve(np.eye(len(nodes)) - M / float(lam), np.ones(len(nodes)))
    assert min(vf) > 0
    v = {u: Fraction(int(vf[ix[u]] * 1e6) + 1, 10 ** 6) for u in nodes}
    assert all(sum(v[w] for w in adj[u]) <= lam * v[u] for u in nodes)   # exact
    return lam, rho


nH = 0
exps = []
for (a, k, uni), (U, s, mins, maxs, typ) in CEN.items():
    for Hs in maxs:
        lam, rho = perron(shortcut_adj(a, 1, k, set(Hs)))
        assert lam < 2
        nH += 1
        if (a, k, uni) == (3, 5, "odd"):
            exps.append(math.log2(rho))
lamF, rhoF = perron(shortcut_adj(3, 1, 4, Fstar))
assert abs(min(exps) - 0.2232) < 1e-3 and abs(max(exps) - 0.6125) < 1e-3
# walk-count bijection, brute force, for F* (even residues included)
adjF = shortcut_adj(3, 1, 4, Fstar)
for Lb in range(4, 13):
    good = 0
    for n in range(1 << Lb):
        x, ok = n, True
        for i in range(Lb - 4 + 1):
            if x % 16 in Fstar:
                ok = False; break
            x = x // 2 if x % 2 == 0 else (3 * x + 1) // 2
        good += ok
    cnt = {u: 1 for u in adjF}
    for _ in range(Lb - 4):
        cnt = {u: sum(cnt[v] for v in adjF[u]) for u in adjF}
    assert good == sum(cnt.values())
say(f"[R7] Theorem E: exact lambda < 2 for all {nH} maximal H sets; 3x+1 mod-32 frontier "
    f"exponents [{min(exps):.4f}, {max(exps):.4f}]; F* exponent {math.log2(rhoF):.4f}  PASS")

# ------------------------------------------------------------------ [R8]
expect = {3: (1, 1), 4: (2, 5), 5: (3, 9), 6: (4, 5)}
for k, (sz, cnum) in expect.items():
    U = [r for r in range(1 << k) if r % 2]
    for size in range(0, sz):
        for A in combinations(U, size):
            assert classify(3, 1, k, k, set(A)) == "H", (k, A)
    found = [A for A in combinations(U, sz) if classify(3, 1, k, k, set(A)) != "H"]
    assert len(found) == cnum, (k, len(found))
    if k == 6:
        assert sorted(map(list, found)) == [[7, 15, 27, 59], [7, 15, 39, 57], [7, 15, 39, 59],
                                            [9, 15, 47, 57], [9, 15, 47, 59]]
say("[R8] minimum provable odd trap sizes 1,2,3,4 (k=3..6) by exhaustive own search  PASS")
say(f"ALL PASS ({time.time() - t0:.1f} s)")
