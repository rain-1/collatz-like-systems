"""Re-run the cheap part of the matrix-interpretation search (z3; search only)
and store every chain found in mi_chains.json, for exact re-verification by
check_srs.py.  Settings: triangular natural matrices, dims 1-2, entries <= 7,
30 s per z3 call.  The longer runs (dims 3-4, up to 500 s per call) are in
scratch/*.out; they found nothing beyond these chains."""
import json
import srs_lib, srs_cores, mi_z3

K7_RULES = [("e0", "fR", "R"), ("e1", "ftR", "R"), ("e3", "ttR", "ctR"), ("small1", "LtR", "LR")]
SPECS = {"K7": K7_RULES + srs_lib.common_rules()}
for nm, Sset, three in (("sf3_17", {1, 7}, False), ("sf3_57", {5, 7}, False), ("sf3_157", {1, 5, 7}, False),
                        ("sf3_357", {3, 5, 7}, False), ("sf3_13", {1, 3}, True), ("sf3_135", {1, 3, 5}, False)):
    SPECS[nm] = srs_cores.core_rules(Sset, three)
out = {}
for nm, rules in SPECS.items():
    print("==", nm, flush=True)
    chain, rem = mi_z3.search(rules, (1, 2), 7, timeout_ms=30000, triangular=True)
    out[nm] = dict(chain=chain, remaining=[r[0] for r in rem], n_rules=len(rules))
    print("   remaining core:", out[nm]["remaining"], flush=True)
json.dump(out, open("mi_chains.json", "w"))
