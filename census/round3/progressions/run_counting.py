"""Compute Theorem C exponent certificates for every system where Theorem A applies.
Writes counting_results.json (sigma uniform and weighted, W, H).  nice python3 run_counting.py"""
import json, sys, time
import systems, counting, plib
from certify import certify

CHOICES = {}   # default: W = p^kappa * L2 (coprime to the invariant modulus)


def main(weighted_limit=400, only=None):
    out = []
    for e in systems.SYSTEMS:
        if only and e['id'] not in only:
            continue
        c = certify(e)
        if not c.get("theorem_A") or e["id"] == "m3_c":
            continue
        S = e["sys"]
        L2 = plib.ia_game(S)["L2"] if S.U else 1
        W = S.P * L2
        if S.U == [] and S.P < 8:
            W = S.P * 4 if S.p != 2 else S.P * 3
        H = {'par_7_1': 30, 'par_9_1': 30}.get(e['id'], 16)
        t0 = time.time()
        cu = counting.certificate(S, W, H, False)
        cw = counting.certificate(S, W, H, True) if W * max(u for u, v in S.table.values()) <= weighted_limit * 50 else None
        rec = dict(id=e["id"], W=W, H=H,
                   sigma_uniform=str(cu["sigma"]) if cu else None,
                   uniform_ok=counting.verify_certificate(S, cu) if cu else None,
                   sigma_weighted=str(cw["sigma"]) if cw else None,
                   weighted_ok=counting.verify_certificate(S, cw) if cw else None,
                   seconds=round(time.time() - t0, 1),
                   G_uniform=cu["G"] if cu else None,
                   G_weighted=cw["G"] if cw else None,
                   weights=({str(k): str(v) for k, v in cw["weights"].items()} if cw else None))
        print({k: rec[k] for k in rec if k not in ('weights', 'G_uniform', 'G_weighted')}, flush=True)
        out.append(rec)
    if only:
        old = json.load(open("counting_results.json"))
        old = [r for r in old if r["id"] not in only] + out
        out = old
    json.dump(out, open("counting_results.json", "w"), indent=1)


if __name__ == "__main__":
    main(only=sys.argv[1:] or None)
