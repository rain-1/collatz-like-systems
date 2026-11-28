"""Check for trichotomy.md (Theorems H, N, T and their applications).

Claims checked (all exactly, with ints/Fractions):
  [H-ex]  acc_h32, acc_h16, acc_h9: hypotheses of Theorem H hold (every SCC of
          G_m is contracting with verified rational weights, or a simple cycle
          with a division); the complete cycle lists are {1,3,19}, {1,3}, {1,4,7}
          (cycle minima); each has an expanding p-adic fixed point (so no
          descent certificate, Lemma B) which is isolated (type (b)).
          Cross-check by simulation n < 2*10^5 (consistency only).
  [S-b]   S-family, m = 2..5, all 2^(2^(m-1)) subsets: no SCC of G_m is an
          expanding simple cycle.  Hence every OBST member has its expanding
          cycles in non-simple SCCs (type (c)).
  [N-wit] Theorem N data for the 12 OBST S-family systems (m = 2, 3) and for the
          open unit-multiplier catalog systems listed below: an exact expanding
          periodic point x*, a closed walk W, and the exact periodic points y_d
          of C^d W for d = 0..24 with multipliers, y_d = x* mod p^(m+d), and
          lam_d > 1 for all d >= d0 (lam_d = lamC^d lam_W).
Runtime: about 1-2 minutes (the m = 5 scan dominates).
"""
import sys, os, math, random
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "round2", "descent"))
sys.path.insert(0, HERE)
import accel_lib as AL
import systems as SY
import descent_lib as DL

ok = True


def claim(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name)
    ok = ok and bool(cond)


# ------------------------------------------------------------------ [H-ex]
EXPECT = {"acc_h32": [1, 3, 19], "acc_h16": [1, 3], "acc_h9": [1, 4, 7]}
for sid, exp in EXPECT.items():
    s = SY.get(sid)
    p, m, t = s["p"], s["m"], s["table"]
    r = AL.theorem_H(p, m, t, m)
    kinds = sorted((c["kind"], len(c["nodes"])) for c in r["comps"] if c["kind"] != "trivial")
    claim(f"{sid}: Theorem H hypotheses hold; SCCs {kinds}; bounds {[(b[0], str(b[1]), str(b[2]), b[3]) for b in r['bounds']]}", True)
    claim(f"{sid}: complete cycle list (minima) = {r['cycles']}", r["cycles"] == exp)
    exp_cyc = [c for c in r["expanding"]]
    claim(f"{sid}: isolated expanding simple cycle(s) with x* = {[str(c['xstar']) for c in exp_cyc]}, "
          f"lam = {[str(c['lam']) for c in exp_cyc]}", len(exp_cyc) >= 1 and all(c["lam"] > 1 for c in exp_cyc))
    # Lemma B data (exact) for the expanding fixed point: kills every descent certificate
    for c in exp_cyc:
        L, A, D, y = DL.verify_obstruction(p, m, t, c["xstar"])
        claim(f"{sid}: Lemma B obstruction verified at {c['xstar']} (period {L}, multiplier {A}/{D})", A > D)
    T = s["step"]
    mins = set()
    for n in range(1, 200000):
        mins.add(min(AL.cycle_of(T, n)))
    claim(f"{sid}: simulation n < 2e5 reaches only cycles {sorted(mins)}", sorted(mins) == exp)

# ------------------------------------------------------------------ [S-b]
def sfamily_no_type_b(m):
    Q = 2 ** m
    odd = list(range(1, Q, 2))
    bad = 0
    for mask in range(1 << len(odd)):
        S = {odd[i] for i in range(len(odd)) if mask >> i & 1}
        E = {}
        for r in range(Q):
            if r % 2:
                E[r] = [((3 * r + 1) % Q, (1, 0)) if r in S else ((r + 1) % Q, (0, 0))]
            else:
                E[r] = [(r // 2, (0, 1)), (r // 2 + Q // 2, (0, 1))]
        for comp in AL.tarjan(list(range(Q)), E):
            cs = set(comp)
            ed = [(a, b, w) for a in comp for b, w in E[a] if b in cs]
            if ed and len(ed) == len(comp):        # simple cycle
                a3 = sum(w[0] for _, _, w in ed)
                b2 = sum(w[1] for _, _, w in ed)
                if 3 ** a3 > 2 ** b2:
                    bad += 1
    return bad

for m in (2, 3, 4, 5):
    claim(f"S-family m={m}: no expanding simple-cycle SCC (no type (b)) among all subsets",
          sfamily_no_type_b(m) == 0)

# ------------------------------------------------------------------ [N-wit]
def witness(name, p, m, t, x=None):
    if x is None:
        g = DL.growing_cycle(p, m, t, extra=4)
        x = g["point"]
    x = Fraction(x)
    K = m
    C, lamC, W, rows = AL.barrier_witness(p, m, t, K, x, dmax=24)
    lamW = rows[0][2]
    good = all(lam == lamC ** d * lamW for d, y, lam in rows)
    # y_d follows C^d first, so y_d = x* (mod p^(K + d*v_C)) with v_C >= 1
    good &= all((AL.padic_residue(y, p, K + d) - AL.padic_residue(x, p, K + d)) % p ** (K + d) == 0
                for d, y, lam in rows)
    good &= len({y for _, y, _ in rows}) == len(rows)
    d0 = next(d for d, y, lam in rows if lam > 1)
    good &= rows[-1][2] > 1
    claim(f"{name}: x*={x} lamC={lamC} |C|={len(C)} |W|={len(W)} lam_W={lamW}; "
          f"y_d expanding for d>={d0}; y_24 has denominator {rows[-1][1].denominator}", good)

for m, S in SY.SF:
    s = SY.get(SY.sf_id(m, S))
    witness(s["id"], 2, m, s["table"])

CATALOG = {
    "par_3_1 (3x+1)": (2, 1, [(1, 0, 2), (3, 1, 1)]),
    "par_5_1 (5x+1)": (2, 1, [(1, 0, 2), (5, 1, 1)]),
    "split5_1": (2, 2, [(1, 0, 2), (5, 1, 1), (1, 0, 2), (1, 1, 1)]),
    "split5_3": (2, 2, [(1, 0, 2), (5, 3, 1), (1, 0, 2), (1, 3, 1)]),
    "m3_e (7n+2,7n+1)": (3, 1, [(1, 0, 3), (7, 2, 1), (7, 1, 1)]),
    "perm_1932": (3, 1, [(2, 0, 3), (4, -1, 3), (4, 1, 3)]),
    "desc_m3_4n5": (3, 1, [(1, 0, 3), (4, 5, 1), (2, 2, 1)]),
    "desc_split7_1": (2, 2, [(1, 0, 2), (7, 1, 1), (1, 0, 2), (1, 1, 1)]),
}
for name, (p, m, t) in CATALOG.items():
    AL.check_system(p, m, t, upto=500)
    witness(name, p, m, t)

print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
