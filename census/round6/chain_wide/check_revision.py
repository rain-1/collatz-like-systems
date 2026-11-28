"""Exact checks for the revision after REFEREE1 (THEORY.md §8, README "Revision after REFEREE1").
Exit 0 iff every check passes; each check can fail.

[R1] signed multiplier constants: data/named.json E* for 3x-1 and m3_b is >= an independent
     50-digit Decimal evaluation of THEORY Thm 3 with g' = 2g in numerator AND denominator
     (the pre-revision values, kept below as constants, are < it: the check would have failed);
     every (P) value also still >= its Decimal evaluation; self-consistency factor < 1.
[R2] (S1) for the signed named systems: at most one raw step with v != 0 per edge; and on random
     orbits every raw-time Z = x_t/P_t (exact Fractions) equals Z at some update.
[R3] core W (sf3_137) fails (R) (the bad edge with prefix slopes 1, 1/2, 3/2, 3/4); 5x+1 and 7x+1
     satisfy (R); the concrete raw drop 263 -> ... -> 223 on the orbit of 15, where 263 is the last
     minimiser of P over updates 0..8000 among the tail after the previous selection.
[R4] families: every member with a state graph and negative drift is now certified; the clipped
     (gamma -> 1) members re-checked exactly at gamma = 1; counts match README.
[R5] (P) as "every v_r >= 0": holds for every non-signed named system and every non-signed
     certified family member.
"""
import json
import os
import random
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import chainlib as L  # noqa: E402
import chain_systems as S  # noqa: E402

FAIL = []
random.seed(11281)


def claim(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ((" | " + detail) if detail else ""), flush=True)
    if not ok:
        FAIL.append(name)


getcontext().prec = 50


def Dpow(p, x):
    return (Decimal(p).ln() * Decimal(x.numerator) / Decimal(x.denominator)).exp()


def Estar_dec(p, th, s, W, gprime, k0):
    S1 = Dpow(p, th) * Dpow(p, -k0 * (1 - th)) / (1 - Dpow(p, -(1 - th)))
    q = Decimal(1) / p
    S2 = sum((k + 1) * q ** k for k in range(k0, k0 + 600))
    gp = Decimal(gprime.numerator) / gprime.denominator
    lam = gp * Decimal(s.numerator) / s.denominator * S2
    return gp * Decimal(W.numerator) / W.denominator * Dpow(p, th) * S1 / (1 - lam), lam


NJ = json.load(open(os.path.join(HERE, "data", "named.json")))
OLD_SIGNED = {"par_3_m1": Decimal("24.078894381182597"), "m3_b": Decimal("50.73726248757482")}

# [R1] -------------------------------------------------------------------------------------
allP = True
for id, row in NJ.items():
    T = S.BY_ID[id]["T"]
    g = L.D.build_graph(T)
    p = T.primes[0]
    sg = L.signed(g)
    for k0, e in row["E"].items():
        C = L.certificate_at(g, Fr(e["s"]))
        oc = L.occupation_constants(g, C)
        gp = oc["gerr"] * (2 if sg else 1)
        Ed, lam = Estar_dec(p, oc["theta"], oc["s"], oc["W"], gp, e["k0p"])
        Ej = Fr(e["E"])
        Ejd = Decimal(Ej.numerator) / Ej.denominator
        ok = Ejd >= Ed and (Ejd - Ed) / Ed < Decimal("1e-7") and lam < 1
        if sg or id in ("par_3_1", "split5_3"):
            claim("[R1] %s k0=%s: json E* %.12f >= Decimal %.12f (g' = %sg), lambda %.2e"
                  % (id, k0, Ejd, Ed, 2 if sg else 1, lam), ok)
        allP &= ok
        if id in OLD_SIGNED and k0 == "32":
            claim("[R1] %s: the pre-revision value %s is below the proved bound (check can fail)"
                  % (id, OLD_SIGNED[id]), OLD_SIGNED[id] < Ed)
claim("[R1] every E* in named.json (all systems, all ranges) is >= its Decimal evaluation, within 1e-7", allP)

# [R2] -------------------------------------------------------------------------------------
for id in ("par_3_m1", "m3_b"):
    T = S.BY_ID[id]["T"]
    g = L.D.build_graph(T)
    mx = L.max_nonzero_v_steps_per_edge(g)
    claim("[R2] %s: (S1) at most one raw step with v != 0 per edge (max = %d)" % (id, mx), mx <= 1)
    ok = True
    for trial in range(8):
        x0 = random.getrandbits(120) + 1
        ch = L.update_chain(g, x0, 50)
        Zupd = {Fr(y) / P for (_, y, P) in ch}
        last_y = ch[-1][1]
        x, P = x0, Fr(1)
        while x != last_y:
            u, v, w = T.table[x % T.Q]
            x = (u * x + v) // w
            P *= Fr(u, w)
            ok &= (Fr(x) / P) in Zupd
    claim("[R2] %s: every raw-time Z on 8 random orbits (50 updates) equals an update-time Z" % id, ok)
# negative control: a signed map with two nonzero constants in one edge must be detected
# (1 mod 4 -> n+2 lands in 3 mod 4, decided, -> 3n+1: two nonzero constants in one edge)
Tneg = L.table_map("ctrl", 4, [(1, 0, 2), (1, 2, 1), (1, 0, 2), (3, 1, 1)])
gneg = L.D.build_graph(Tneg)
mneg = L.max_nonzero_v_steps_per_edge(gneg)
claim("[R2] negative control: a map with n+2 then 3n+1 inside one edge gives max %d >= 2" % mneg, mneg >= 2)

# [R3] -------------------------------------------------------------------------------------
for id, want in (("par_5_1", True), ("par_7_1", True), ("sf3_137", False)):
    g = L.D.build_graph(S.BY_ID[id]["T"])
    bad = L.raw_prefix_ok(g)
    claim("[R3] %s: (R) holds = %s" % (id, want), (len(bad) == 0) == want,
          "" if not bad else "bad edges: %s" % [(g.states[b[0]], b[1], [str(x) for x in b[2]]) for b in bad])
    if id == "sf3_137":
        claim("[R3] core W bad edge from state (4,1), prefix slopes 1, 1/2, 3/2, 3/4",
              any(g.states[b[0]] == (4, 1) and b[2] == [1, Fr(1, 2), Fr(3, 2), Fr(3, 4)] for b in bad))
T = S.BY_ID["sf3_137"]["T"]
g = L.D.build_graph(T)
N = 8000
ch = L.update_chain(g, 15, N)
P = [c[2] for c in ch]
# successive last minimisers of P over the tail (finite segment)
sel, t = [], -1
while t + 1 < len(P) and len(sel) < 200:
    m = min(P[t + 1:])
    t = max(i for i in range(t + 1, len(P)) if P[i] == m)
    sel.append(t)
yv = [ch[i][1] for i in sel]
claim("[R3] core W orbit of 15: 263 is a selected (last-minimiser) update value on 8000 updates",
      263 in yv, "first selected values %s" % yv[:8])
x, Pr, raw = 263, Fr(1), [263]
for _ in range(9):
    u, v, w = T.table[x % T.Q]
    x = (u * x + v) // w
    Pr *= Fr(u, w)
    raw.append(x)
claim("[R3] raw orbit 263 -> ... -> 223 with raw multiplier 27/32 < 1",
      raw == [263, 790, 395, 1186, 593, 1780, 890, 445, 446, 223] and Pr == Fr(27, 32), str(raw))

# [R4] -------------------------------------------------------------------------------------
FJ = json.load(open(os.path.join(HERE, "data", "families.json")))
fams = dict(S3=S.family_S(3), S4=S.family_S(4), split=S.family_split(), m3=S.family_m3())
tot_cert, tot_clip, okc = 0, 0, True
counts = {}
for f, rows in FJ.items():
    members = dict((str(k), T) for k, T in fams[f])
    neg_uncert = [r for r in rows if not r.get("contracting") and "graph" not in (r.get("error") or "")
                  and r.get("drift") is not None and r["drift"] < 0]
    claim("[R4] %s: no negative-drift member without a certificate (%d)" % (f, len(neg_uncert)),
          len(neg_uncert) == 0)
    cert = [r for r in rows if r.get("contracting")]
    clip = [r for r in cert if r["theta"] == "0"]
    counts[f] = (len(rows), len(cert), len(clip),
                 sum(1 for r in cert if not r["raw_prefix_ok"]),
                 sum(1 for r in rows if "graph" in (r.get("error") or "")))
    tot_cert += len(cert)
    tot_clip += len(clip)
    for r in clip:
        g = L.D.build_graph(members[r["key"]])
        C = L.D.best_certificate(g, c=Fr(1), sign=+1)
        okc &= C.gamma > 1 and L.D.check_supermartingale(g, C.s, Fr(1), C.w) is not None
    # every non-certified, non-graph-error member has drift >= 0
    okd = all(r.get("contracting") or "graph" in (r.get("error") or "") or
              (r.get("drift") is not None and r["drift"] >= 0) for r in rows)
    claim("[R4] %s: every non-certified member is a graph error or has drift >= 0" % f, okd)
print("INFO family counts (members, certified, clipped to theta=0, fail (R), graph error):", counts)
claim("[R4] clipped members satisfy N_{s,1} w <= w exactly (%d members)" % tot_clip, okc and tot_clip > 0)
claim("[R4] total certified family members = %d (240 before revision + %d clipped)" % (tot_cert, tot_clip),
      tot_cert == 240 + tot_clip)

# [R5] -------------------------------------------------------------------------------------
ok = True
for s in S.NAMED:
    g = L.D.build_graph(s["T"])
    if not L.signed(g):
        ok &= L.all_constants_nonneg(s["T"])
claim("[R5] every non-signed named system has all v_r >= 0", ok)
ok, n = True, 0
for f, rows in FJ.items():
    members = dict((str(k), T) for k, T in fams[f])
    for r in rows:
        if r.get("contracting") and not r["signed"]:
            ok &= L.all_constants_nonneg(members[r["key"]])
            n += 1
claim("[R5] every non-signed certified family member (%d) has all v_r >= 0" % n, ok)

print("ALL REVISION CHECKS PASSED" if not FAIL else "FAILED: %s" % FAIL)
sys.exit(1 if FAIL else 0)
