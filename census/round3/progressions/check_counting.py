"""Check for Theorem C (theorem_C_counting.md). Exact rational verification of every stored
exponent certificate (counting_results.json), randomized tests of the tree children, the m3_a
sigma -> 1 statement, and (EVIDENCE) the heuristic exponents.  Exits 0 iff all checks pass."""

import json
import os
import random
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plib
import systems
import counting

FAIL = []
rng = random.Random(11)


def ok(c, m):
    if not c:
        FAIL.append(m)
        print("FAIL:", m, flush=True)


recs = json.load(open(os.path.join(HERE, "counting_results.json")))
nver = 0
for r in recs:
    S = systems.get(r["id"])["sys"]
    W, H = r["W"], r["H"]
    rows, big = counting.child_table(S, W, H)
    if S.U:
        ia = plib.ia_game(S)
        G = counting.good_types(S, W, rows, ia["enter"], ia["L2"])
    else:
        G = counting.good_types(S, W, rows)
    for kind in ("uniform", "weighted"):
        sig = r["sigma_" + kind]
        if sig is None:
            continue
        Gs = r["G_" + kind]
        ok(sorted(G) == sorted(Gs), f"good types {r['id']}")
        if kind == "uniform":
            w = {t: Fr(1) for t in G}
        else:
            w = {int(k): Fr(v) for k, v in r["weights"].items()}
        cert = dict(W=W, G=sorted(G), sigma=Fr(sig), weights=w, rows=rows)
        ok(all(x > 0 for x in w.values()), f"positive weights {r['id']}")
        ok(counting.verify_certificate(S, cert), f"certificate {r['id']} {kind} sigma={sig}")
        nver += 1
    # randomized: the children are ancestors with the predicted type and ratio
    for _ in range(300):
        z0 = rng.choice([z for z in rows if z % W in G])
        z = z0 + big * rng.randrange(10 ** 6, 10 ** 9)
        for (tp, rho, rr, h) in rows[z0]:
            m = S.moves()[rr]
            c = (S.p ** (h + 1) * z - m["v"]) // m["u"]
            ok((S.p ** (h + 1) * z - m["v"]) % m["u"] == 0, f"child integral {r['id']}")
            ok(S.T(c) == S.p ** h * z and c % S.p != 0, f"child is ancestor {r['id']}")
            ok(c % W == tp, f"child type {r['id']}")
            ok(z < c <= rho * (1 + counting.EPS) * z, f"child ratio {r['id']}")
print(f"{nver} exponent certificates verified exactly", flush=True)
ok(nver >= 60, "number of certificates")

# m3_a: every h admits exactly one child, all children are 3-units; sigma = 99/100 certified
S = systems.get("m3_a")["sys"]
for z in [rng.randrange(1, 10 ** 12) for _ in range(500)]:
    if z % 3 == 0:
        continue
    for h in range(10):
        kids = [m for m in S.moves() if m["kind"] != "D" and (3 ** (h + 1) * z - m["v"]) % m["u"] == 0]
        ok(len(kids) == 1, "m3_a exactly one child per h")
sigma = Fr(99, 100)
tot = sum(counting.rat_lower_pow(Fr(3 ** (h + 1), 2) * (1 + counting.EPS), 99, 100) for h in range(30))
ok(tot >= 1, "m3_a sigma = 0.99 uniform certificate")
print("m3_a: sigma = 99/100 certified with 30 children per vertex", flush=True)
# split5_3 improvement over 0.2383
r53 = [r for r in recs if r["id"] == "split5_3"][0]
ok(Fr(r53["sigma_weighted"]) >= Fr(42, 100), "split5_3 weighted sigma >= 0.42")
# the round-2 exponent: 4^-s + (1024/5)^-s = 1 has root 0.2382...; 0.42 is larger
s0 = 0.2382
ok(abs(4 ** -s0 + (1024 / 5) ** -s0 - 1) < 1e-3, "round-2 exponent value")

# EVIDENCE: heuristic exponents (floats)
def root(a):
    f = lambda g: 2 ** -g + (1 / a) * (a / 2) ** g - 1
    gs = [i / 10000 for i in range(1, 10000)]
    m = min(gs, key=f)
    if f(m) >= 0:
        return None
    lo, hi = 1e-4, m
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) > 0 else (lo, mid)
    return lo
print("heuristic exponents (EVIDENCE):", {a: root(a) for a in (3, 5, 7, 9)})
ok(root(3) is None and abs(root(5) - 0.6509) < 1e-3, "heuristic roots")

# ------------------------------------------------------------------------------------------
# Repair of Lemma C2 (REFEREE1 GAP): scope of Lemma C2' (bounded U-valuation) and Lemma R.
# For every certificate: either (bounded case) every type tau in G has v_l(tau) < v_l(W) for all
# l in U, so every vertex of type in G has v_l(z) = v_l(tau) <= v_l(W) - 1; or (R case) U = {l},
# every p-unit state has a move as in Lemma R (exact finite condition), the chosen v_r are > 0,
# and every residue mod L2 is enterable.
# ------------------------------------------------------------------------------------------
import construct
from plib import vp


def lemma_R_data(S):
    """For each p-unit state sigma: least (h, move) with v_r > 0, u_r | v_r, and the state
    condition p^h sigma = src (mod p^(kappa-1)).  Exact: these are the only conditions (theorem
    file, Lemma R)."""
    out = {}
    for st in range(S.S):
        if S.kappa > 1 and st % S.p == 0:
            continue
        f = None
        for h in range(0, S.kappa + 1):
            for m in S.moves():
                if m["kind"] == "D" or m["v"] <= 0 or m["v"] % m["u"]:
                    continue
                if (S.p ** h * st) % S.S == m["src"]:
                    f = (h, m)
                    break
            if f:
                break
        out[st] = f
    return out


n_bounded, n_R = 0, 0
R_TABLE = {}
for r in recs:
    S = systems.get(r["id"])["sys"]
    W = r["W"]
    Gall = set(r["G_uniform"] or []) | set(r["G_weighted"] or [])
    if not S.U:
        n_bounded += 1
        continue
    bounded = all(vp(t, l) < vp(W, l) for t in Gall for l in S.U)
    if bounded:
        n_bounded += 1
        continue
    n_R += 1
    ok(len(S.U) == 1, f"R case needs a single numerator prime: {r['id']}")
    l = S.U[0]
    ia = plib.ia_game(S)
    ok(ia["enter"] == set(range(ia["L2"])), f"every residue mod L2 enterable: {r['id']}")
    RD = lemma_R_data(S)
    ok(all(v is not None for v in RD.values()), f"Lemma R move exists for every p-unit state: {r['id']}")
    if not all(v is not None for v in RD.values()):
        continue
    VR = max(vp(m["v"], l) for (h, m) in RD.values())
    hmax = max(h for (h, m) in RD.values())
    R_TABLE[r["id"]] = (l, VR, hmax, {st: (h, m["r"], m["u"], m["v"]) for st, (h, m) in RD.items()})
    for st, (h, m) in RD.items():
        # exact finite content
        ok(m["v"] > 0 and m["v"] % m["u"] == 0 and (S.p ** h * st) % S.S == m["src"], "R conditions")
        ok(all(q == l for q in plib.primes_of(m["u"])) or m["u"] == 1, "u_r is a power of l")
        # wide randomized test of the conclusion
        for _ in range(150):
            e = rng.randrange(VR + 1, 60)
            # z = l^e * j' with j' coprime to l, z = st (mod p^(kappa-1)), z a p-unit
            jj = (st * pow(l ** e, -1, S.S)) % S.S if S.S > 1 else 0
            jp = jj + S.S * rng.randrange(1, 10 ** 9)
            if jp % l == 0 or (S.S == 1 and jp % S.p == 0) or (l ** e * jp) % S.p == 0:
                continue
            z = l ** e * jp
            ok(vp(z, l) == e and z % S.S == st and z % S.p != 0, "R test vertex")
            c = (S.p ** (h + 1) * z - m["v"]) // m["u"]
            ok((S.p ** (h + 1) * z - m["v"]) % m["u"] == 0, f"R integral {r['id']}")
            ok(S.T(c) == S.p ** h * z, f"R ancestor {r['id']}")
            w = c
            for _ in range(h + 1):
                w = S.T(w)
            ok(w == z, f"R: T^(h+1)(c) = z {r['id']}")
            ok(c % S.p != 0, f"R: c is a p-unit {r['id']}")
            ok(vp(c, l) == vp(m["v"], l) - vp(m["u"], l) <= VR, f"R valuation {r['id']}")
            ok(0 < c <= S.p ** (h + 1) * z, f"R size {r['id']}")
            ok(c % ia["L2"] in ia["enter"], f"R: c enterable {r['id']}")
print(f"Lemma C2' scope: {n_bounded} certificates with bounded valuation, {n_R} via Lemma R", flush=True)
for k, v in R_TABLE.items():
    print("   Lemma R", k, "l =", v[0], "V_R =", v[1], "h_max =", v[2], "moves (state: h, r, u, v):", v[3])
ok(sorted(R_TABLE) == sorted(["m3_a", "desc_s32_d65", "split_5", "split_13", "split_73", "split_97",
                              "split_7081", "splitB_7", "splitB_71", "split5_1", "desc_split7_1",
                              "desc_s32_plus9", "desc_m3_4n5"]), f"R systems {sorted(R_TABLE)}")

# Executed repair (illustration of the bounded construction + exact replay): for vertices z of
# growing l-valuation, construct from c = R(z) and replay; the IA ball-word count stays bounded.
for sid in ["split5_1", "m3_a", "desc_s32_d65"]:
    S = systems.get(sid)["sys"]
    info = construct.prepare(S)
    l, VR, hmax, RDs = R_TABLE[sid]
    lens = []
    for e in range(VR + 1, VR + 9):
        z = next(l ** e * j for j in range(1, 10 ** 4)
                 if (l ** e * j) % S.p and vp(l ** e * j, l) == e)
        st = z % S.S
        h, rr, u, v = RDs[st]
        c = (S.p ** (h + 1) * z - v) // u
        x = next(xx for xx in range(1, 10 ** 4) if construct.g(S, info, xx) == construct.g(S, info, z))
        N = 11 * 16 * 9
        n, data = construct.construct(S, info, c, x, N)
        construct.verify(S, c, x, N, n, data)
        w = c
        for _ in range(h + 1):
            w = S.T(w)
        ok(w == z and n % N == x % N, f"repaired construction merges with z ({sid})")
        lens.append(len(data["ball_words"]))
    ok(max(lens) - min(lens) <= 1, f"{sid}: ball words bounded after Lemma R {lens}")
    print(f"   {sid}: IA ball words from c = R(z), v_l(z) = {VR+1}..{VR+8}: {lens}", flush=True)

if FAIL:
    print(len(FAIL), "FAILURES")
    sys.exit(1)
print("ALL CHECKS PASSED")
