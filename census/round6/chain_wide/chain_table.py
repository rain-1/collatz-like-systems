"""Compute the per-system constants of THEORY.md for the named systems and the
families.  Writes data/named.json and data/families.json.  About 2-4 minutes.

Exact quantities are stored as strings of Fractions; floats are for reading.
Run run_ranges.py first (data/ranges_32.json, data/ranges_27.json).
"""
import json
import math
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import chainlib as L  # noqa: E402
import chain_systems as S  # noqa: E402

LIT = {"par_3_1": (68, "Barina 2021 (J. Supercomputing), 2^68, quoted from memory"),
       "split5_3": (66, "census/round2/rewriting/split5_3_s27.md, 2^66 (repo, exact)")}


def kstar(g):
    vals = sorted({e.F for e in g.edges})
    rho = max(vals)
    if rho <= 1:   # no expanding edge (revision: the loop below never ended); see analyse
        return None
    km = max(v for v in vals if v < 1)
    k = 0
    while rho ** k * km <= 1:
        k += 1
    return k


def ranges():
    r = {}
    import glob
    for fp in sorted(glob.glob(os.path.join(HERE, "data", "ranges_*_*.json"))):
        if True:
            for k, v in json.load(open(fp)).items():
                if v["ok"] and v["log2N0"] >= r.get(k, {}).get("log2N0", 0):
                    r[k] = v
    return r


def analyse(T, depth=None, N0log=None, extra_k0=()):
    g = L.D.build_graph(T)
    p = T.primes[0]
    out = dict(states=len(g.states), slopes=[str(x) for x in L.slope_values(g)],
               signed=L.signed(g), raw_prefix_ok=(len(L.raw_prefix_ok(g)) == 0))
    C = L.certificate(g)
    oc = L.occupation_constants(g, C)
    rho = oc["Fmax"]
    out.update(theta=str(oc["theta"]), theta_f=float(oc["theta"]), s=str(C.s), W=str(oc["W"]),
               W_f=float(oc["W"]), rho=str(rho), phi=math.log(rho) / math.log(p),
               gerr=str(oc["gerr"]), Cstar=1 / (1 - float(oc["theta"])),
               kstar=kstar(g))
    if rho > 1:
        out.update(A1=L.chain_count(rho, 1), A10=L.chain_count(rho, 10), A1p=L.chain_count(rho, 1, p))
    else:
        # every edge slope <= 1, so P_l <= 1 on every orbit; by Cor. 3.1 (P_l -> infinity on a
        # non-eventually-periodic orbit) every orbit is eventually periodic.  No chain exists.
        out.update(A1=None, A10=None, A1p=None, no_expanding_edge=True)
    R, craw = L.raw_constants(g)
    out.update(R=R, c_raw=str(craw))
    ef = L.expansion_formula(g)
    out["expansion_formula"] = None if ef is None else dict(rho=str(ef[0]), kappa=str(ef[1]), Lratio=ef[2])
    depth = depth or (14 if p == 2 else 9)
    fc = L.forced_congruence(g, depth)
    out["forced"] = None if fc is None else dict(depth=depth, D=fc[0], residue=fc[1], classes=fc[2],
                                                 mass=str(fc[3]), mass_f=float(fc[3]))
    Es = {}
    for k0 in ([N0log] if N0log else []) + list(extra_k0):
        k0p = k0 if p == 2 else int(k0 * math.log(2) / math.log(p))   # p^k0p <= 2^k0
        b = L.best_E(g, k0p)
        if b is not None:
            Es[str(k0)] = dict(k0p=k0p, E=str(b[0]), E_f=float(b[0]), s=str(b[1].s),
                               gamma=str(b[1].gamma), mult_const=math.exp(float(b[0])) if b[0] < 700 else "e^%.1f" % float(b[0]))
    out["E"] = Es
    return out


def main(which=("named", "families")):
    rg = ranges()
    named = {}
    for s in (S.NAMED if "named" in which else []):
        if s["kind"] != "contracting":
            continue
        id = s["id"]
        N0log = rg[id]["log2N0"] if id in rg else None
        extra = [LIT[id][0]] if id in LIT else []
        a = analyse(s["T"], N0log=N0log, extra_k0=extra)
        a.update(origin=s["origin"], rule=s["rule"], range=rg.get(id, {}).get("log2N0"),
                 cycles=rg.get(id, {}).get("cycle_minima"), lit=LIT.get(id))
        named[id] = a
        print(id, a["theta_f"], a["rho"], a["A1"], a["A10"], a["forced"], a["E"], flush=True)
    if "named" in which:
        json.dump(named, open(os.path.join(HERE, "data", "named.json"), "w"), indent=1)
    if "families" not in which:
        return

    fam = {}
    for famname, members in [("S3", S.family_S(3)), ("S4", S.family_S(4)),
                             ("split", S.family_split()), ("m3", S.family_m3())]:
        rows = []
        for key, T in members:
            row = dict(key=str(key))
            try:
                g = L.D.build_graph(T)
                try:
                    row["drift"] = L.D.drift(g)[2]
                except Exception:
                    row["drift"] = None
            except Exception as ex:
                row["error"] = "graph: %s" % ex
                rows.append(row)
                continue
            try:
                a = analyse(T)
                row.update(a)
                row["contracting"] = True
            except Exception as ex:
                row["contracting"] = False
                row["error"] = "cert: %s" % str(ex)[:80]
            rows.append(row)
        fam[famname] = rows
        print(famname, len(rows), sum(1 for r in rows if r.get("contracting")), flush=True)
    json.dump(fam, open(os.path.join(HERE, "data", "families.json"), "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1:] or ("named", "families"))
