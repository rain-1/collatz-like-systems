"""Exact checks for round6/chain_wide (THEORY.md).  Exit 0 iff every check passes.

[1] tables agree with census/round3/density/systems.py and round3/accel/systems.py
[2] restart lemma (Lemma 1): the update chain of an integer, restarted at any
    update l in the state sigma_l, follows the sigma_l-tree of y_l exactly; and
    every y_l is an actual orbit value
[3] certificates: N_{s,gamma} w <= w exactly (rigorous rational powers), and the
    moment lemma numerically on all classes to depth 10 (p=2) / 6 (p=3)
[4] survivor classes: forced congruences (split5_3: y = 253 mod 256 as in the
    repo; 3x+1: 3 mod 4) and an independent necessary-direction test by raw
    iteration of random 200-bit integers
[5] chain counts A(B) by exact integer powers; multiplier constants recomputed
    exactly and compared with data/named.json; split5_3 constants compared with
    the repo (31 per ten octaves; multiplier error below log 1.000073 at 2^48)
[6] cycle multipliers: positive constants give lambda < 1 on every listed cycle
    (3x+1, 3x+5, split5_3, ...); 3x-1 (negative constant) has a cycle with
    lambda > 1, so the signed statements must not claim lambda < 1
[7] range certificates in data/ are present and OK
"""
import json
import math
import os
import random
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import chainlib as L  # noqa: E402
import chain_systems as S  # noqa: E402

FAIL = []


def claim(name, ok):
    print(("PASS " if ok else "FAIL ") + name, flush=True)
    if not ok:
        FAIL.append(name)


random.seed(20261128)
CONTR = [s for s in S.NAMED if s["kind"] == "contracting"]

# [1] -------------------------------------------------------------------
import importlib.util  # noqa: E402


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(path))
    spec.loader.exec_module(m)
    sys.path.pop(0)
    return m


DS = load(os.path.join(L.CENSUS, "round3", "density", "systems.py"), "dens_sys")
AS = load(os.path.join(L.CENSUS, "round3", "accel", "systems.py"), "acc_sys")
for s in S.NAMED:
    id = s["id"]
    if id in DS.BY_ID:
        ref = DS.BY_ID[id]["step"]
    elif id.startswith("sf3_"):
        ref = AS.get(id)["step"]
    else:
        claim("[1] reference for " + id, False)
        continue
    claim("[1] table %s agrees on 1..20000" % id, all(s["T"].step(n) == ref(n) for n in range(1, 20001)))

# [2] -------------------------------------------------------------------
for s in S.NAMED:
    T = s["T"]
    g = L.D.build_graph(T)
    p = T.primes[0]
    ok = True
    for trial in range(6):
        x0 = random.getrandbits(160) + 1
        ch = L.update_chain(g, x0, 60)
        # orbit values
        orb, x = {x0: 0}, x0
        for k in range(1, 1200):
            x = T.step(x)
            orb.setdefault(x, k)
        times = [orb.get(y) for (_, y, _) in ch]
        ok &= all(t is not None for t in times) and times == sorted(times)
        for l in (0, 7, 23):
            sig, y, P = ch[l]
            nd = L.sigma_root(g, sig)
            ok &= (y - nd.r) % nd.M == 0
            for j in range(1, 25):
                t = (y - nd.r) // nd.M
                nd = L.children(g, nd)[t % p][0]
                tt = (y - nd.r) // nd.M
                ok &= nd.state == ch[l + j][0]
                ok &= nd.a * tt + nd.b == ch[l + j][1]
                ok &= nd.A == ch[l + j][2] / P
                # real form y_{l+j} = A y + B with B = b - a r / M
                ok &= nd.A * y + (nd.b - Fr(nd.a * nd.r, nd.M)) == ch[l + j][1]
    claim("[2] restart lemma and orbit values, " + s["id"], ok)

# [3] -------------------------------------------------------------------
CERT = {}
for s in CONTR:
    g = L.D.build_graph(s["T"])
    C = L.certificate(g)
    CERT[s["id"]] = (g, C)
    claim("[3] exact supermartingale certificate, %s (theta = %s)" % (s["id"], 1 - C.gamma),
          L.D.check_supermartingale(g, C.s, C.gamma, C.w) is not None and 0 < C.gamma < 1)
    p = s["T"].primes[0]
    depth = 10 if p == 2 else 6
    sf, th = float(C.s), float(1 - C.gamma)
    ok = True
    for k in range(len(g.states)):
        level = [L.sigma_root(g, k)]
        for j in range(1, depth + 1):
            level = [c for nd in level for (c, F) in L.children(g, nd)]
            tot = sum(float(nd.A) ** sf for nd in level)
            ok &= tot <= (float(C.w[k]) / float(C.wmin)) * p ** (j * th) * (1 + 1e-9)
            ok &= len(level) == p ** j and len({nd.r for nd in level}) == p ** j
    claim("[3] moment lemma on all classes to depth %d, %s" % (depth, s["id"]), ok)

# [4] -------------------------------------------------------------------
fc = L.forced_congruence(CERT["split5_3"][0], 14)
claim("[4] split5_3 survivors are y = 253 mod 256 (repo: 256 | x+3)", fc[0] == 8 and fc[1] == 253)
fc = L.forced_congruence(CERT["par_3_1"][0], 14)
claim("[4] 3x+1 survivors are 3 mod 4", fc[0] == 2 and fc[1] == 3)
for s in CONTR:
    g, C = CERT[s["id"]]
    T = s["T"]
    p = T.primes[0]
    fc = L.forced_congruence(g, 12 if p == 2 else 8)
    Dd, res = fc[0], fc[1]
    if Dd == 0:
        continue
    # least tree depth Kf at which the congruence mod p^D is already forced;
    # surviving Kf*R raw steps covers the first Kf updates (R = max raw steps per edge)
    Kf = next(K for K in range(1, 15) if L.forced_congruence(g, K)[0] >= Dd)
    H = Kf * L.raw_constants(g)[0]
    hits, ok = 0, True
    nsamp = int(min(10 ** 6, max(10 ** 5, 60 / float(fc[3]))))
    for _ in range(nsamp):
        n = random.getrandbits(200) | (1 << 199)
        x, P, surv = n, Fr(1), True
        for k in range(H):
            u, v, w = T.table[x % T.Q]
            x = (u * x + v) // w
            P *= Fr(u, w)
            if P < 1:
                surv = False
                break
        if surv:
            hits += 1
            ok &= n % p ** Dd == res
    if hits == 0:
        print("SKIP [4] no raw survivor through %d raw steps among %d samples for %s (tree mass %.2g);"
              " only the exact tree computation supports its forced class" % (H, nsamp, s["id"], float(fc[3])))
        continue
    claim("[4] raw-multiplier survivors through %d raw steps (%d found) lie in the forced class %d mod %d^%d, %s"
          % (H, hits, res, p, Dd, s["id"]), ok)

# [5] -------------------------------------------------------------------
claim("[5] split5_3: A(10) = 31", L.chain_count(Fr(5, 4), 10) == 31)
claim("[5] 3x+1: A(1) = 1, A(10) = 17", L.chain_count(Fr(3, 2), 1) == 1 and L.chain_count(Fr(3, 2), 10) == 17)
for F, B in [(Fr(5, 4), 10), (Fr(3, 2), 10), (Fr(4, 3), 10), (Fr(5, 3), 10), (Fr(7, 4), 10), (Fr(5, 2), 10)]:
    k = L.chain_count(F, B)
    claim("[5] chain_count(%s, %d) = %d by integer powers" % (F, B, k),
          F ** k < 2 ** B <= F ** (k + 1))
g, C = CERT["split5_3"]
E48 = L.multiplier_E(g, C, 48)
claim("[5] split5_3 multiplier error at 2^48 (%.3g) < log(1.000073)" % float(E48),
      E48 is not None and float(E48) < math.log(1.000073))
named = os.path.join(HERE, "data", "named.json")
if os.path.exists(named):
    NJ = json.load(open(named))
    ok = True
    for id, row in NJ.items():
        g, _ = CERT[id]
        for k0, e in row["E"].items():
            C2 = L.certificate_at(g, Fr(e["s"]))
            ok &= C2 is not None and C2.gamma == Fr(e["gamma"])
            E2 = L.multiplier_E_signed(g, C2, e["k0p"])
            ok &= E2 == Fr(e["E"])
        ok &= L.chain_count(Fr(row["rho"]), 10) == row["A10"]
    claim("[5] data/named.json multiplier constants recomputed exactly", ok)
else:
    claim("[5] data/named.json present", False)

# [6] -------------------------------------------------------------------
def cycle_lambda(T, c):
    lam = Fr(1)
    for x in c:
        u, v, w = T.table[x % T.Q]
        lam *= Fr(u, w)
    return lam


ok = True
for s in CONTR:
    T = s["T"]
    cyc = L.find_cycles(T.step, 3000)
    for m, c in cyc.items():
        lam = cycle_lambda(T, c)
        if L.nonneg_constants(T):
            ok &= lam < 1
claim("[6] every cycle met below 3000 has multiplier < 1 when all constants are >= 0", ok)
T = S.BY_ID["par_3_m1"]["T"]
lams = {m: cycle_lambda(T, c) for m, c in L.find_cycles(T.step, 3000).items()}
claim("[6] 3x-1 has a cycle with multiplier > 1 (%s)" % {m: str(l) for m, l in lams.items()},
      any(l > 1 for l in lams.values()))

x, P, ok = 1, Fr(1), True
for k in range(300):
    u, v, w = T.table[x % T.Q]
    x = (u * x + v) // w
    P *= Fr(u, w)
    ok &= P >= 1
claim("[6] 3x-1: the cycle point 1 has every raw prefix multiplier >= 1 (300 steps), so N^mult "
      "contains periodic points when a constant is negative", ok)

# [7] -------------------------------------------------------------------
import glob  # noqa: E402
got = {}
for fp in glob.glob(os.path.join(HERE, "data", "ranges_*_*.json")):
    for k, v in json.load(open(fp)).items():
        if v["ok"]:
            got[k] = max(got.get(k, 0), v["log2N0"])
claim("[7] range certificates present for all contracting systems: %s" % got,
      all(s["id"] in got for s in CONTR))

print("ALL CHECKS PASSED" if not FAIL else "FAILED: %s" % FAIL)
sys.exit(1 if FAIL else 0)
