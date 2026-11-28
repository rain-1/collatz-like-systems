"""check.py: every claim of census/round3/traps (exit 0 = all PASS).

Sections (claims in README.md / theory.md / census.md / family.md / systems):
  [1] YAH mod-8 table (Corollary 5): status of the 11 YAH sets.
  [2] Census reproduction (Census Theorem): for 9 censuses, every minimal
      provable set has an independently verified certificate and every
      one-element-smaller set has a verified homoclinic witness; every
      maximal H set has a verified witness and every one-element-larger set
      is provable; the stored JSON counts are reproduced.
  [3] Level independence (Theorems 3, 4 and Lemma 6): on 600 random
      (map, A) instances the SCC verdict at levels k..k+3 agrees, and every
      H verdict yields a verified homoclinic witness by the Theorem-4
      construction.
  [4] Theorem F families: type-F minimal sets mod 8 and mod 16 recomputed on
      the brute-force graph; exact lift formula vs. simulation for many
      (a, b) in each class (the simulation part is EVIDENCE); exact check
      that every simple cycle has E <= 2o (mod 8) / E <= 3o (mod 16).
  [5] Named systems: certificates verified; hand-proof facts of trap7_57,
      trap5_17 (incl. the congruence equivalences 8 | 5n+1, 8 | 3n+1),
      trap5_hi16 checked; random huge n checked to meet A or go
      below B (EVIDENCE, consistency only).
  [6] Theorem E (entropy bounds) exact Perron-vector certificates; lam < 2
      for all 130 maximal H sets.
Runtime: about 1-2 minutes.
"""
import sys, os, json, random, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from fractions import Fraction
import traps_lib as L
import verify as V
import census as CEN
import family as FAM
from systems import SYSTEMS, make_step

random.seed(20261127)
t0 = time.time()


def cert_check(T, A, k, m=None):
    """build (traps_lib) and verify (verify.py) a certificate."""
    if m is None:
        m = max(k, T.beta)
    r = L.scc_method(T, A, k, m)
    assert r["ok"]
    cert = L.finish_certificate(T, A, k, m, r)
    comps = [(kd, comp, data) for kd, comp, data in cert["comps"]]
    assert V.check_certificate(T.br, T.beta, set(A), k, m, comps, cert["B"], cert["cycles"])
    return cert


def witness_check(T, A, k, m=None):
    if m is None:
        m = max(k, T.beta)
    r = L.scc_method(T, A, k, m)
    assert not r["ok"]
    comp, pc = r["bad"][0]
    x, Lp, z, j, i = L.homoclinic_from_scc(T, A, k, m, r["adj"], comp)
    assert V.check_homoclinic(T.br, T.beta, set(A), k, x, Lp, z, j)
    return x, Lp, z, j


# ---------------------------------------------------------------- [1]
C3 = L.collatz_a(3)
yah_proved = [{2}, {3}, {4}, {6}, {1, 5}, {1, 7}]
yah_open = [{0}, {1}, {5}, {7}, {5, 7}]
for A in yah_proved:
    c = cert_check(C3, A, 3)
for A in yah_open:
    witness_check(C3, A, 3)
print("[1] YAH mod-8 table: 6 proved sets certified, 5 open sets have homoclinic witnesses  PASS")

# ---------------------------------------------------------------- [2]
runs = [(3, 3, "all"), (3, 4, "all"), (3, 5, "odd"), (5, 3, "all"), (5, 4, "all"),
        (5, 5, "odd"), (7, 3, "all"), (7, 4, "all"), (7, 5, "odd")]
tot_min = tot_maxH = 0
for a, k, uni in runs:
    T = L.collatz_a(a)
    fn = os.path.join(HERE, "results", f"census_C{a}_k{k}_{uni}.json")
    stored = json.load(open(fn))
    out = CEN.run(a, k, uni)
    assert out["stats"] == stored["stats"], (fn, out["stats"], stored["stats"])
    assert [m["A"] for m in out["minimal_provable"]] == [m["A"] for m in stored["minimal_provable"]]
    assert out["maximal_H"] == stored["maximal_H"]
    Uv = [r for r in range(1 << k) if uni == "all" or r % 2]
    for m in out["minimal_provable"]:
        A = set(m["A"])
        c = cert_check(T, A, k)
        assert [list(x) for x in c["cycles"]] == [list(x) for x in m["cycles"]]
        for q in A:
            witness_check(T, A - {q}, k)
    for Hs in out["maximal_H"]:
        A = set(Hs)
        witness_check(T, A, k)
        for q in Uv:
            if q not in A:
                r = L.scc_method(T, A | {q}, k, k)
                assert r["ok"]
    tot_min += len(out["minimal_provable"]); tot_maxH += len(out["maximal_H"])
print(f"[2] censuses reproduced; {tot_min} minimal certificates verified independently, "
      f"{tot_maxH} maximal H sets with witnesses; minimality/maximality checked  PASS")

# ---------------------------------------------------------------- [3]
cnt = {"P": 0, "H": 0}
for trial in range(600):
    a = random.choice([1, 3, 5, 7, 9, 11, 13, 15, 17])
    b = random.choice([1, 3, 5, 7, 9, 11])
    k = random.choice([3, 4, 5])
    T = L.collatz_a(a, b=b)
    A = {r for r in range(1 << k) if random.random() < random.choice([0.15, 0.25, 0.35])}
    verdicts = []
    for m in range(k, k + 4):
        r = L.scc_method(T, A, k, m)
        verdicts.append(r["ok"])
        if not r["ok"]:
            comp, pc = r["bad"][0]
            x, Lp, z, j, i = L.homoclinic_from_scc(T, A, k, m, r["adj"], comp)
            assert V.check_homoclinic(T.br, T.beta, A, k, x, Lp, z, j)
    assert len(set(verdicts)) == 1, (a, b, k, sorted(A), verdicts)
    cnt["P" if verdicts[0] else "H"] += 1
    if verdicts[0] and trial % 10 == 0 and a > 1:
        cert_check(T, A, k, k + 1)
print(f"[3] level independence on 600 random instances ({cnt}); all H witnesses verified  PASS")

# ---------------------------------------------------------------- [4]
def typeF_brute(a0, b0, A, k):
    br = [(1, 0, 1), (a0, b0, 0)]
    adj = V.brute_graph(br, 1, k, set(A), k)
    T = L.AffMap("x", 1, br)
    adj2 = {u: [(v, u % 2) for v in vs] for u, vs in adj.items()}
    for comp in L.tarjan(adj2):
        cs = set(comp)
        outd = [sum(1 for v in adj[u] if v in cs) for u in comp]
        if sum(outd) == 0:
            continue
        if any(d != 1 for d in outd):
            return False
    return True


fam3 = FAM.run(3, "odd"); fam3a = FAM.run(3, "all"); fam4 = FAM.run(4, "odd")
for key, mins in list(fam3.items()) + list(fam3a.items()):
    a0, b0 = map(int, key.split(","))
    for A in mins:
        assert typeF_brute(a0, b0, A, 3)
for key, mins in fam4.items():
    a0, b0 = map(int, key.split(","))
    for A in mins:
        assert typeF_brute(a0, b0, A, 4)
# (referee) exact finite content of the "no exceptions" claims F2 (a >= 5) and
# F3 (a >= 9): every simple cycle of every minimal odd type-F set has
# E <= 2o (mod 8) resp. E <= 3o (mod 16), where o = odd steps (odd nodes) and
# E = halvings (even nodes).  Then a^o >= 5^o > 4^o >= 2^E (resp. a^o >= 9^o >
# 8^o >= 2^E), so no lift is a positive integer.  Cycles with o = 0 are
# all-halving loops with lift 0 and are harmless.
def simple_cycle_oE(a0, b0, A, k):
    br = [(1, 0, 1), (a0, b0, 0)]
    adj = V.brute_graph(br, 1, k, set(A), k)
    adj2 = {u: [(v, u % 2) for v in vs] for u, vs in adj.items()}
    out = []
    for comp in L.tarjan(adj2):
        cs = set(comp)
        nxt = {u: [v for v in adj[u] if v in cs] for u in comp}
        if all(len(s) == 0 for s in nxt.values()):
            continue
        assert all(len(s) == 1 for s in nxt.values())
        c0 = comp[0]; cyc = [c0]; y = nxt[c0][0]
        while y != c0:
            cyc.append(y); y = nxt[y][0]
        assert set(cyc) == cs
        out.append((sum(r % 2 for r in cyc), sum(1 - r % 2 for r in cyc)))
    return out


n_oE = 0
for fam, k, c in ((fam3, 3, 2), (fam4, 4, 3)):
    for key, mins in fam.items():
        a0, b0 = map(int, key.split(","))
        for A in mins:
            assert all(x % 2 for x in A)
            for o, E in simple_cycle_oE(a0, b0, A, k):
                assert o == 0 or E <= c * o, (key, A, k, o, E)
                n_oE += 1
# {4} mod 8 works for every class
assert all([4] in v for v in fam3a.values())
assert all(len(v) == 2 for v in fam3.values())
# exact lifts vs. simulation (evidence for the conclusion; the theorem's
# finite content is the type-F property checked above)
nsim = 0
for key, mins in fam3.items():
    a0, b0 = map(int, key.split(","))
    for A in mins + [[4]]:
        k = 3
        for a in range(a0, 60, 8):
            for b in range(b0, 40, 8):
                T = L.collatz_a(a, b=b)
                cyc = FAM.simple_cycles_of(T, set(A), k)
                ints = set()
                for c in cyc:
                    x, num, E = L.lift_cycle(T, k, c["nodes"])
                    if x.denominator == 1 and x > 0:
                        ints.add(int(x))
                Ak = set(A)
                for n in range(1, 400):
                    y = n; seen = set()
                    while y % 8 not in Ak and y not in seen:
                        seen.add(y)
                        y = T.step(y)
                        assert len(seen) < 10 ** 5
                    if y % 8 not in Ak:
                        # ended in a cycle avoiding A: must be a listed lift
                        cy = [y]; z = T.step(y)
                        while z != y:
                            cy.append(z); z = T.step(z)
                        assert ints & set(cy), (a, b, A, cy)
                    nsim += 1
print(f"[4] Theorem F: type-F sets verified on brute graphs (mod 8, mod 16); "
      f"E <= 2o (mod 8) / E <= 3o (mod 16) on all {n_oE} simple cycles; {nsim} orbits consistent with exact lifts  PASS")

# ---------------------------------------------------------------- [5]
for sid, (a, b, k, A, desc) in SYSTEMS.items():
    T = L.collatz_a(a, b=b)
    c = cert_check(T, set(A), k)
    step = make_step(a, b, k, A)
    # evidence: huge random n meet A or drop to <= B
    for _ in range(200):
        n = random.getrandbits(random.choice([64, 128, 256])) | 1
        x = n; t = 0
        while x % (1 << k) not in A and x > c["B"]:
            x = T.step(x); t += 1
            assert t < 10 ** 6
    # systems.py step function: every n <= 3000 ends in a cycle of T_A made of
    # the certified avoiding cycles and the cycle through 1
    TA = make_step(a, b, k, A)
    allowed = set(x for cy in c["cycles"] for x in cy)
    y = 1; one = set()
    while y not in one:
        one.add(y); y = TA(y)
    for n in range(1, 3001):
        y = n; seen = set()
        while y not in seen:
            seen.add(y); y = TA(y)
        assert y in allowed or y in one, (sid, n, y)
    print(f"    {sid}: m={c['m']} B={c['B']} avoiding cycles={c['cycles']}")
# hand-proof facts
# trap7_57: n=3 mod 8 -> (7n+1)/2 = 3 or 7 mod 8 ; n=1 mod 8 -> 8 | 7n+1
for n in range(1, 1 << 14, 2):
    if n % 8 == 3:
        assert (7 * n + 1) % 4 == 2 and ((7 * n + 1) // 2) % 8 in (3, 7)
        assert 5 * ((7 * n + 1) // 2) + 1 == Fraction(7, 2) * (5 * n + 1)
    if n % 8 == 1:
        assert (7 * n + 1) % 8 == 0
# trap5_17: n=3 mod 8 -> 8 | 5n+1 ; n=5 mod 8 -> (5n+1)/2 = 1 or 5 mod 8
    if n % 8 == 3:
        assert (5 * n + 1) % 8 == 0
    if n % 8 == 5:
        assert (5 * n + 1) % 4 == 2 and ((5 * n + 1) // 2) % 8 in (1, 5)
        assert 3 * ((5 * n + 1) // 2) + 1 == Fraction(5, 2) * (3 * n + 1)
    # (referee) the congruence equivalences used in the run arguments, and the
    # valuation drop along the run
    assert (n % 8 == 3) == ((5 * n + 1) % 8 == 0)          # trap7_57
    assert (n % 8 == 5) == ((3 * n + 1) % 8 == 0)          # trap5_17
    if n % 8 == 3:
        assert L.v2(5 * ((7 * n + 1) // 2) + 1) == L.v2(5 * n + 1) - 1
    if n % 8 == 5:
        assert L.v2(3 * ((5 * n + 1) // 2) + 1) == L.v2(3 * n + 1) - 1
# trap5_hi16 transition table on odd classes mod 16 (next odd value)
def next_odd(n, a=5):
    y = a * n + 1
    e = 0
    while y % 2 == 0:
        y //= 2; e += 1
    return y, e
tab = {}
for n in range(1, 1 << 16, 2):
    r = n % 16
    if r in (1, 3, 5, 7):
        y, e = next_odd(n)
        tab.setdefault(r, set()).add((y % 16, min(e, 4)))
assert tab[1] == {(3, 1), (11, 1)}
assert {e for _, e in tab[3]} == {4}
assert tab[5] == {(5, 1), (13, 1)}
assert tab[7] == {(1, 2), (5, 2), (9, 2), (13, 2)}
# trap5_hi16 hand potential: w1 = 63/25, w3 = 1, w7 = 79/25, threshold n >= 64.
# Ratio bounds are decreasing in n, so checking at n = 64 suffices; also the limit.
w = {1: Fraction(63, 25), 3: Fraction(1), 7: Fraction(79, 25)}
edges = [(1, 3, 2), (3, 1, 16), (3, 3, 16), (3, 7, 16), (7, 1, 4)]
for n in (64, 10 ** 12):
    for (c, c2, d) in edges:
        bound = w[c2] * (5 + Fraction(1, n)) / (d * w[c])
        assert bound < 1, (c, c2, bound)
# the edge set is complete for untrapped transitions (classes 1,3,7) and 5 only to {5,13}
for r, S in tab.items():
    for (s, e) in S:
        if r == 1: assert s in (3, 11)
        if r == 7: assert s in (1, 5, 9, 13)
# finite part: every n <= 64 meets A or reaches 1
for n in range(1, 65):
    x = n; t = 0
    while x % 16 not in (9, 11, 13, 15) and x != 1:
        x = x // 2 if x % 2 == 0 else 5 * x + 1; t += 1
        assert t < 10 ** 5
print("[5] named systems certified; hand-proof facts (incl. trap5_hi16 potential) verified  PASS")

# ---------------------------------------------------------------- [6]
import entropy as ENT
ENT.check_all()
# (referee) exact certificate M v <= lam v with lam < 2 (theta < 1) for ALL
# 130 maximal H sets of the 9 censuses, including the mod-8 and mod-16 sets
# with even residues such as F*.  For arbitrary A the bound applies to
# C_{a,1}-avoiders because the T-orbit is a subsequence of the C-orbit.
n_lam = 0
Fstar_theta = None
for a, k, uni in runs:
    d = json.load(open(os.path.join(HERE, "results", f"census_C{a}_k{k}_{uni}.json")))
    for Hs in d["maximal_H"]:
        adj = ENT.adjacency(a, 1, k, set(Hs))
        lam, v = ENT.perron_certificate(adj)
        assert all(v[u] > 0 for u in adj)
        for u in adj:
            assert sum(v[w] for w in adj[u]) <= lam * v[u]
        assert lam < 2, (a, k, Hs, lam)
        n_lam += 1
        if (a, k) == (3, 4) and sorted(Hs) == [0, 3, 5, 7, 8, 10, 13, 14, 15]:
            Fstar_theta = ENT.theta(lam)
assert n_lam == 130 and Fstar_theta is not None
print(f"[6] Theorem E exponent certificates verified; lam < 2 certified exactly for all "
      f"{n_lam} maximal H sets (F*: theta = {Fstar_theta:.4f})  PASS")
# ---------------------------------------------------------------- [7]
import minsize as MS
expect = {3: 1, 4: 2, 5: 3, 6: 4}
for k, sz in expect.items():
    s, sets = MS.min_sets(3, k, "odd", 6)
    assert s == sz, (k, s)
    stored = os.path.join(HERE, "results", f"minsize_C3_k{k}_odd.json")
    if os.path.exists(stored):
        assert json.load(open(stored))["sets"] == sets
    for A in sets:
        cert_check(C3, set(A), k)
print("[7] minimum sizes of provable odd trap sets mod 2^k (k=3..6) = 1,2,3,4; "
      "all minimum sets certified  PASS")
print(f"ALL PASS  ({time.time() - t0:.1f} s)")
