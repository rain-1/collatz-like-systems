"""REFEREE #2 independent check for the progressions lens (round 3, after the REFEREE1 repairs).

Written from scratch: maps are re-defined here from the raw census rules (no plib/systems/counting
code is used for the maps, the children, the (W) inequality, the IA game or Lemma R).  The only
inputs read from the prover are the *certificate data* in counting_results.json (W, H, G, sigma,
weights) and, for comparison only, plib.ia_game / systems.get(...).T.

Sections
 1. raw maps, shortcuts, Lemma 0 (S(n) in {R(n), R(R(n))}); agreement with systems.py T.
 2. IA game re-implemented from theorem_A_sufficiency.md section 4; every residue mod L2
    enterable for the 13 Lemma-R systems; comparison with plib.ia_game.
 3. Lemma R re-derived: own search of the (h, r) move per p-unit state, exact conditions, wide
    randomized tests with v_l(z) up to 90, and an exhaustive hunt for violations.
 4. Theorem C case split: which certificates have bounded G (case (a)) vs need Lemma R (case (b));
    gcd(W, d*) = 1; G consists of p-units and enterable types.
 5. (W) certificates re-verified exactly with an independent child enumeration (8 systems).
 6. m3_a sigma -> 1: exact certificates with rho' = rho for sigma = 99/100 and 999/1000.
 7. 1932 permutation: Proposition P0 (exhaustive orbit test + all progressions N <= 60) and the
    integrality step of Proposition P on random periodic words.
 8. Theorem B (S2) finite content for m3_a: basins of 1 and 2 exhaust [1, 2*10^5] (EVIDENCE; GLOBAL
    is the census result) and (S1) evidence: both basins in every class mod q <= 60.
Exit code 0 iff every check passes.
"""
import json
import os
import random
import sys
from fractions import Fraction as Fr
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
FAIL = []
rng = random.Random(20261127)


def ok(c, m):
    if not c:
        FAIL.append(m)
        if not m.startswith("(W) fails split5_3 weighted"):
            print("FAIL:", m, flush=True)


def vp(n, l):
    if n == 0:
        return 10 ** 9
    k = 0
    n = abs(n)
    while n % l == 0:
        n //= l
        k += 1
    return k


# ----------------------------------------------------------------------------- 1. maps
S0 = {1, 3, 5, 7, 11, 13, 15, 17, 21, 23, 25, 29}


def raw_rule(sid):
    """Return (p, kappa, raw map R).  R(n) = n/p on multiples of p, else an affine branch whose
    value is a multiple of p (census raw form)."""
    if sid in ("m3_a",):
        return 3, 1, lambda n: n // 3 if n % 3 == 0 else (2 * n + 1 if n % 3 == 1 else 2 * n + 2)
    if sid == "desc_m3_4n5":
        return 3, 1, lambda n: n // 3 if n % 3 == 0 else (4 * n + 5 if n % 3 == 1 else 2 * n + 2)
    if sid == "m3_e":
        return 3, 1, lambda n: n // 3 if n % 3 == 0 else (7 * n + 2 if n % 3 == 1 else 7 * n + 1)
    if sid.startswith("split_") or sid.startswith("splitB_"):
        d = int(sid.split("_")[1])
        B = sid.startswith("splitB_")
        def R(n, d=d, B=B):
            if n % 2 == 0:
                return n // 2
            big = (n % 4 == 3) if B else (n % 4 == 1)
            return 3 * n + d if big else n + d
        return 2, 2, R
    if sid in ("split5_1", "split5_3", "desc_split7_1"):
        a, d = {"split5_1": (5, 1), "split5_3": (5, 3), "desc_split7_1": (7, 1)}[sid]
        return 2, 2, lambda n: n // 2 if n % 2 == 0 else (a * n + d if n % 4 == 1 else n + d)
    if sid in ("desc_s32_d65", "desc_s32_plus9"):
        d, SS = (65, S0) if sid == "desc_s32_d65" else (1, S0 | {9})
        return 2, 5, lambda n: n // 2 if n % 2 == 0 else (3 * n + d if n % 32 in SS else n + d)
    if sid.startswith("par_"):
        a = int(sid.split("_")[1])
        ds = sid.split("_")[2]
        d = -int(ds[1:]) if ds.startswith("m") else int(ds)
        return 2, 1, lambda n: n // 2 if n % 2 == 0 else a * n + d
    raise KeyError(sid)


def shortcut(p, R):
    return lambda n: n // p if n % p == 0 else R(n) // p


def table_of(p, kappa, R):
    """(u_r, v_r) of the shortcut S(n) = (u n + v)/p on n = r mod p^kappa, derived numerically from
    R by two evaluations and then verified on many points."""
    P = p ** kappa
    tab = {}
    for r in range(P):
        if r % p == 0:
            tab[r] = (1, 0)
            continue
        n1, n2 = r + P, r + 2 * P
        u = (R(n2) - R(n1)) // P
        v = R(n1) - u * n1
        tab[r] = (u, v)
    return tab


R13 = ["m3_a", "desc_s32_d65", "split_5", "split_13", "split_73", "split_97", "split_7081",
       "splitB_7", "splitB_71", "split5_1", "desc_split7_1", "desc_s32_plus9", "desc_m3_4n5"]

sys.path.insert(0, HERE)
import systems as prover_systems   # comparison only
import plib as prover_plib         # comparison only

MAPS = {}
for sid in R13 + ["split5_3", "par_3_1", "par_5_1", "m3_e", "par_7_1"]:
    p, kappa, R = raw_rule(sid)
    S = shortcut(p, R)
    tab = table_of(p, kappa, R)
    MAPS[sid] = (p, kappa, R, S, tab)
    PT = prover_systems.get(sid)["sys"]
    for _ in range(3000):
        n = rng.randrange(1, 10 ** 15)
        s = S(n)
        ok(s in (R(n), R(R(n))), f"Lemma 0 {sid} {n}")
        ok(s == PT.T(n), f"map definition differs from systems.py: {sid} at {n}")
        u, v = tab[n % p ** kappa]
        ok(p * s == u * n + v, f"table {sid}")
    ok({r: tuple(x) for r, x in PT.table.items()} == tab, f"table equals systems.py table {sid}")
print("1. raw maps / shortcuts agree with systems.py for", len(MAPS), "systems", flush=True)


# ----------------------------------------------------------------------------- 2. IA game
def U_of(tab):
    out = set()
    for (u, v) in tab.values():
        m, q = u, 2
        while m > 1:
            if m % q == 0:
                out.add(q)
                m //= q
            else:
                q += 1
    return sorted(out)


def my_ia(p, kappa, tab):
    U = U_of(tab)
    L = 1
    for l in U:
        L *= l ** max(vp(u, l) for (u, v) in tab.values())
    L2 = L * L
    Sm = p ** (kappa - 1)
    mv = []
    for r, (u, v) in tab.items():
        src = ((u * r + v) // p) % Sm
        mv.append((r, u, v, src))
    rad = 1
    for l in U:
        rad *= l
    iso = [m for m in mv if m[1] == 1]
    exp = [m for m in mv if m[1] > 1]
    ok(all(m[1] % rad == 0 for m in exp), "no mixed moves")
    nodes = [(s, x) for s in range(Sm) for x in range(L2)]
    opts = {}
    for nd in nodes:
        seen, st = {nd}, [nd]
        while st:
            s, x = st.pop()
            for (r, u, v, src) in iso:
                if src == s:
                    y = (r % Sm, (p * x - v) % L2)
                    if y not in seen:
                        seen.add(y)
                        st.append(y)
        o = []
        for (s, x) in seen:
            for (r, u, v, src) in exp:
                if src == s and (p * x - v) % u == 0:
                    md = L2 // u
                    w = ((p * x - v) // u) % md
                    o.append(frozenset((r % Sm, w + md * k) for k in range(u)))
        opts[nd] = o
    live = set(nodes)
    while True:
        new = {nd for nd in live if any(o <= live for o in opts[nd])}
        if new == live:
            break
        live = new
    enter = set()
    for z in range(L2):
        for h in range(kappa - 1, kappa + L2 + 2):
            if (0, (p ** h * z) % L2) in live:
                enter.add(z)
                break
    return dict(U=U, L2=L2, live=live, enter=enter)


IA = {}
for sid, (p, kappa, R, S, tab) in MAPS.items():
    ia = my_ia(p, kappa, tab)
    IA[sid] = ia
    pia = prover_plib.ia_game(prover_systems.get(sid)["sys"])
    ok(ia["L2"] == pia["L2"] and ia["live"] == pia["live"] and ia["enter"] == pia["enter"],
       f"IA game differs from plib: {sid}")
    if sid in R13:
        ok(ia["enter"] == set(range(ia["L2"])), f"every residue mod L2 enterable: {sid}")
print("2. IA game re-implemented; all residues enterable in the 13 Lemma-R systems", flush=True)


# ----------------------------------------------------------------------------- 3. Lemma R
def find_R_move(p, kappa, tab, st, hmax=8):
    Sm = p ** (kappa - 1)
    for h in range(hmax + 1):
        for r in sorted(tab):
            u, v = tab[r]
            if r % p == 0 or v <= 0 or v % u:
                continue
            if (p ** h * st) % Sm == ((u * r + v) // p) % Sm:
                return h, r, u, v
    return None


RDATA = {}
for sid in R13:
    p, kappa, R, S, tab = MAPS[sid]
    U = IA[sid]["U"]
    ok(len(U) == 1, f"single numerator prime {sid}")
    l = U[0]
    Sm = p ** (kappa - 1)
    states = [s for s in range(Sm) if kappa == 1 or s % p]
    if kappa == 1:
        states = [0]
    D = {st: find_R_move(p, kappa, tab, st) for st in states}
    ok(all(x is not None for x in D.values()), f"Lemma R move for every p-unit state {sid}")
    VR = max(vp(v, l) for (h, r, u, v) in D.values())
    hm = max(h for (h, r, u, v) in D.values())
    ok(VR <= 1 and hm <= 4, f"V_R <= 1, h <= 4: {sid} {VR} {hm}")
    RDATA[sid] = (l, VR, hm, D)
    ntest = 0
    for st, (h, r, u, v) in D.items():
        ok(all(q == l for q in U_of({0: (u, 0)})) , "u_r power of l")
        for _ in range(400):
            e = rng.randrange(VR + 1, 91)
            # random p-unit z with state st and v_l(z) = e exactly
            while True:
                j = rng.randrange(1, 10 ** 12)
                z = l ** e * j
                if j % l and z % p and z % Sm == st % Sm:
                    break
                # adjust j to the state if possible
                if Sm > 1:
                    j = (j - j % Sm) + (st * pow(l ** e, -1, Sm)) % Sm
                    z = l ** e * j
                    if j > 0 and j % l and z % p and z % Sm == st:
                        break
            num = p ** (h + 1) * z - v
            ok(num % u == 0, f"R integral {sid}")
            c = num // u
            ok(c % p != 0 and c > 0, f"R p-unit positive {sid}")
            w = c
            for _ in range(h + 1):
                w = S(w)
            ok(w == z, f"R: S^(h+1)(c) = z {sid}")
            ok(S(c) == p ** h * z, f"R: S(c) = p^h z {sid}")
            ok(vp(c, l) == vp(v, l) - vp(u, l) <= VR, f"R valuation {sid}")
            ok(c <= p ** (h + 1) * z, f"R size {sid}")
            ok((c % IA[sid]["L2"]) in IA[sid]["enter"], f"R enterable {sid}")
            ntest += 1
    # exhaustive hunt: every p-unit z <= 20000 with v_l(z) > V_R gets an ancestor of valuation <= V_R
    # within h+1 steps (direct search over all preimages, no use of the table move)
    bad = 0
    vmax = max(abs(v) for (u, v) in tab.values())
    for z in range(1, 20001 + vmax):
        if z % p == 0 or vp(z, l) <= VR or p * z <= vmax:   # Lemma R needs p^(h+1) z > v_r
            continue
        found = False
        for h in range(0, 5):
            y = p ** h * z
            for r, (u, v) in tab.items():
                if r % p == 0:
                    continue
                if (p * y - v) % u == 0:
                    c = (p * y - v) // u
                    if c > 0 and c % (p ** kappa) == r and S(c) == y and vp(c, l) <= VR:
                        found = True
                        break
            if found:
                break
        bad += not found
    ok(bad == 0, f"exhaustive Lemma R hunt {sid}: {bad} vertices without a bounded ancestor")
    print(f"   Lemma R {sid}: l={l} V_R={VR} h_max={hm} moves={D} ({ntest} random tests)", flush=True)
print("3. Lemma R re-derived for 13 systems", flush=True)

# the table rows of theorem_C_counting.md section 2
EXPECT = {"m3_a": (0, 2, 2, 2), "desc_m3_4n5": (0, 2, 2, 2), "split5_1": (1, 3, 1, 1),
          "desc_split7_1": (1, 3, 1, 1)}
for d in (5, 13, 73, 97, 7081):
    EXPECT[f"split_{d}"] = (1, 3, 1, d)
for d in (7, 71):
    EXPECT[f"splitB_{d}"] = (1, 1, 1, d)
for sid, row in EXPECT.items():
    ok(all(x == row for x in RDATA[sid][3].values()), f"md table row {sid}: {RDATA[sid][3]}")
for sid in ("desc_s32_d65", "desc_s32_plus9"):
    hs = {x[0] for x in RDATA[sid][3].values()}
    ok(hs <= {0, 1, 4} and all(x[2] == 1 for x in RDATA[sid][3].values()),
       f"{sid}: I moves with h in {{0,1,4}}: {sorted(hs)}")

# ----------------------------------------------------------------------------- 4. case split
recs = json.load(open(os.path.join(HERE, "counting_results.json")))
certs = {c["id"]: c for c in json.load(open(os.path.join(HERE, "certificates.json")))}
caseb = []
for r in recs:
    sid = r["id"]
    W = r["W"]
    ds = certs[sid]["invariant_modulus"]
    ok(ds and gcd(W, ds) == 1, f"gcd(W, d*) = 1 for {sid}")
    p = certs[sid]["p"]
    U = certs[sid]["U"]
    Gall = set(r["G_uniform"] or []) | set(r["G_weighted"] or [])
    ok(all(t % p for t in Gall), f"G p-units {sid}")
    bounded = (not U) or all(vp(t, l) < vp(W, l) for t in Gall for l in U)
    if not bounded:
        caseb.append(sid)
ok(sorted(caseb) == sorted(R13), f"case (b) systems {sorted(caseb)}")
print(f"4. case (a): {len(recs) - len(caseb)} certificates, case (b): {len(caseb)}", flush=True)


# ----------------------------------------------------------------------------- 5. (W)
def lower_pow(rho, s, t):
    """A rational q > 0 with q^t * rho^s <= 1 (q <= rho^(-s/t)), verified exactly."""
    f = float(rho) ** (-s / t) * (1 - 1e-9)
    q = Fr(f).limit_denominator(10 ** 9) if f > 1e-6 else Fr(f)
    while q ** t * rho ** s > 1:
        q *= Fr(999999, 1000000)
    return q


def verify_W(sid, rec, kind):
    p, kappa, R, S, tab = MAPS[sid]
    W, Hh = rec["W"], rec["H"]
    sig = Fr(rec["sigma_" + kind])
    G = set(rec["G_" + kind])
    w = ({t: Fr(1) for t in G} if kind == "uniform"
         else {int(k): Fr(x) for k, x in rec["weights"].items()})
    ok(set(w) >= G, "weights for every type")
    Lu = 1
    for (u, v) in tab.values():
        Lu = Lu * u // gcd(Lu, u)
    M = W * Lu
    Sm = p ** (kappa - 1)
    qcache = {}
    worst = None
    for tau in G:
        for k in range(Lu):
            zeta = tau + W * k
            zz = zeta + M * 10 ** 6          # a concrete large lift for exact replay
            tot = Fr(0)
            for h in range(Hh + 1):
                for r, (u, v) in tab.items():
                    if r % p == 0:
                        continue
                    if (p ** h * zeta) % Sm != ((u * r + v) // p) % Sm:
                        continue
                    if (p ** (h + 1) * zeta - v) % u:
                        continue
                    rho = Fr(p ** (h + 1), u)
                    if rho <= 1:
                        continue
                    c = (p ** (h + 1) * zz - v) // u
                    ok(S(c) == p ** h * zz and c % p, f"child replay {sid}")
                    tc = c % W
                    if tc not in G:
                        continue
                    key = rho
                    if key not in qcache:
                        qcache[key] = lower_pow(rho * Fr(1001, 1000), sig.numerator, sig.denominator)
                    tot += w[tc] * qcache[key]
            ok(tot >= w[tau], f"(W) fails {sid} {kind} tau={tau} lift={zeta}")
            ratio = tot / w[tau]
            worst = ratio if worst is None or ratio < worst else worst
    return worst


for sid in ["m3_a", "split5_1", "desc_s32_d65", "split_5", "par_3_1", "par_5_1", "m3_e",
            "split5_3", "desc_m3_4n5"]:
    rec = [r for r in recs if r["id"] == sid][0]
    for kind in ("uniform", "weighted"):
        if rec["sigma_" + kind] is None:
            continue
        wr = verify_W(sid, rec, kind)
        print(f"   (W) {sid} {kind} sigma={rec['sigma_' + kind]}: min slack ratio {float(wr):.6f}",
              flush=True)
print("5. (W) certificates re-verified independently", flush=True)

# negative control: the (W) check must fail if sigma is raised a lot
rec = dict([r for r in recs if r["id"] == "split5_3"][0])
rec["sigma_weighted"] = "6/10"
nf = len(FAIL)
verify_W("split5_3", rec, "weighted")
neg = len(FAIL) - nf
del FAIL[nf:]
ok(neg > 0, "negative control: (W) at sigma = 0.6 must fail for split5_3")
print("   negative control: (W) detects an inflated sigma", flush=True)

# ----------------------------------------------------------------------------- 6. m3_a sigma -> 1
for s, t, Hh in [(99, 100, 40), (999, 1000, 400)]:
    tot = Fr(0)
    for h in range(Hh):
        tot += lower_pow(Fr(3 ** (h + 1), 2), s, t)
    ok(tot >= 1, f"m3_a exact certificate sigma={s}/{t} rho'=rho with {Hh} children")
    print(f"6. m3_a: sigma = {s}/{t} certified with rho' = rho, {Hh} children: sum = {float(tot):.6f}")
p, kappa, R, S, tab = MAPS["m3_a"]
for _ in range(2000):
    z = rng.randrange(3, 10 ** 15)
    if z % 3 == 0:
        continue
    for h in range(8):
        kids = [r for r in (1, 2) if (3 ** (h + 1) * z - tab[r][1]) % 2 == 0]
        ok(len(kids) == 1, "m3_a one child per h")
        r = kids[0]
        c = (3 ** (h + 1) * z - tab[r][1]) // 2
        ok(c % 3 == r and S(c) == 3 ** h * z and z < c < Fr(3 ** (h + 1), 2) * z, "m3_a child")

# ----------------------------------------------------------------------------- 7. 1932
def T32(n):
    q, r = divmod(n, 3)
    return 2 * q if r == 0 else (4 * q + 1 if r == 1 else 4 * q + 3)


for n in range(1, 300001):
    m, k = n, 0
    while m % 2 == 0:
        ok(m % 3 == 0 or T32(m) % 2 == 1, "1932 parity")
        nm = T32(m)
        if m % 3 == 0:
            ok(nm < m, "1932 descent on 3q")
        m = nm
        k += 1
        ok(k < 100, "1932 odd reached")
ok(T32(1) == 1 and T32(2) == 3 and T32(3) == 2, "1932 cycles")
suff = [(x, N) for N in range(1, 61) for x in range(N)
        if 1 % N == x and (2 % N == x or 3 % N == x)]
ok(suff == [(0, 1), (1, 2)], f"1932: progressions meeting (1) and (2 3): {suff}")
# bijectivity spot check
img = {T32(n) for n in range(1, 3 * 10 ** 5)}
ok(len(img) == 3 * 10 ** 5 - 1, "1932 injective")
# Proposition P integrality step: a periodic word W forces n_0 = fixed point c*
UV = {0: (2, 0), 1: (4, -1), 2: (4, 1)}
for _ in range(300):
    L = rng.randrange(1, 9)
    word = [rng.randrange(3) for _ in range(L)]
    a, b = Fr(1), Fr(0)            # T^L on the cylinder: n -> a n + b
    for r in word:
        u, v = UV[r]
        a, b = a * Fr(u, 3), (u * b + v) / 3
    cstar = b / (1 - a)
    # all integers n in [1, 3^(L*4)] whose itinerary is word^4: only n = cstar if integral
    per = 3 ** (4 * L)
    hits = []
    for n0 in range(0, per):
        m, good = n0, True
        if n0 == 0:
            continue
        for i in range(4 * L):
            if m % 3 != word[i % L]:
                good = False
                break
            m = T32(m)
        if good:
            hits.append(n0)
        if per > 3 ** 12:
            break
    if per <= 3 ** 12:
        ok(len(hits) <= 1, "cylinder of W^4 is a single class mod 3^(4L)")
print("7. 1932: P0 and the Proposition-P cylinder step checked", flush=True)

# ----------------------------------------------------------------------------- 8. (S1)/(S2) m3_a
p, kappa, R, S, tab = MAPS["m3_a"]
LIM = 200000
bas = {}
for n in range(1, LIM + 1):
    m, path = n, []
    while m not in bas and m not in (1, 2):
        path.append(m)
        m = S(m)
        ok(len(path) < 10 ** 4, "m3_a orbit length")
    lab = bas.get(m, m)
    for x in path:
        if x <= LIM:
            bas[x] = lab
    bas[n] = lab
ok(set(bas[n] for n in range(1, LIM + 1)) == {1, 2}, "m3_a two basins exhaust [1, LIM] (EVIDENCE)")
for q in range(2, 61):
    for x in range(q):
        labs = {bas[n] for n in range(LIM // 2 + (x - LIM // 2) % q, LIM + 1, q)}
        ok(labs == {1, 2}, f"m3_a both basins in {x} mod {q} beyond {LIM//2} (EVIDENCE)")
print("8. m3_a: both basins in every class mod q <= 60 (EVIDENCE for (S1))", flush=True)

if FAIL:
    print(len(FAIL), "FAILURES")
    for f in FAIL[:20]:
        print("  ", f)
    sys.exit(1)
print("ALL REFEREE2 CHECKS PASSED")
