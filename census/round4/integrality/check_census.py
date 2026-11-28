#!/usr/bin/env python3
"""Check for census_small.md (task 1).

  [E-count] Recomputes the four families of census_small.py from scratch and
            compares the type counts with the stored enum_*.json.
  [E-obst]  Every type-(c) table is OBST for dichotomy/decide.py (asserted
            inside census_small.main during recomputation).
  [E-lift]  Lemma L sanity: for 200 random type-(c_mixed) tables per family, the
            classification at level m+1 is again type (c) (some SCC of G_{m+1}
            has an expanding cycle and is not a simple cycle).
  [E-G3]    The highlighted core G3 is in F3m2, is c_mixed at levels 2 and 3,
            and its expanding fixed point is -1 with multiplier 4/3.
Exit 0 iff all PASS (about 1 minute).
"""
import sys, os, json, random, io, contextlib
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import intlib as IL
import census_small as CS

ok = True


def claim(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name, flush=True)
    ok = ok and bool(cond)


random.seed(3)
for fam in ["F2m2", "F2m3", "F3m2", "F3m2b"]:
    stored = json.load(open(os.path.join(HERE, "enum_%s.json" % fam)))
    counts = {}
    mixed = []
    for p, m, table in CS.family(fam):
        if not IL.positivity_ok(p, m, table):
            counts["fails (P)"] = counts.get("fails (P)", 0) + 1
            continue
        if CS.division_free_cycle(p, m, table):
            counts["division-free cycle"] = counts.get("division-free cycle", 0) + 1
            continue
        kind, comps = IL.system_type(p, m, table)
        counts[kind] = counts.get(kind, 0) + 1
        if kind in ("c_mixed", "c_exp"):
            assert IL.decide_verdict(p, m, table) == "OBST"
        if kind == "c_mixed":
            mixed.append((p, m, table))
    claim(f"[E-count] {fam}: {counts} equals stored counts", counts == stored["counts"])
    smp = random.sample(mixed, min(200, len(mixed)))
    good = True
    for p, m, table in smp:
        k2, _ = IL.system_type(p, m, table, m + 1)
        if k2 not in ("c_mixed", "c_exp"):
            good = False
    claim(f"[E-lift] {fam}: {len(smp)} sampled c_mixed tables are type (c) at level m+1 too", good)
claim("[E-obst] every type-(c) table is OBST for decide.py (asserted above)", True)

G3 = [(1, 0, 3), (1, 2, 3), (1, 1, 3), (1, 0, 3), (1, 2, 3), (1, 1, 3), (1, 0, 3), (1, 2, 3), (4, 1, 3)]
inF = any(list(map(tuple, t)) == G3 for _, _, t in CS.family("F3m2"))
k2, c2 = IL.system_type(3, 2, G3, 2)
k3, c3 = IL.system_type(3, 2, G3, 3)
x, lam = IL.periodic_point(3, 2, G3, 2, [8])
claim("[E-G3] G3 in F3m2, c_mixed at levels 2 and 3, fixed point -1 with multiplier 4/3",
      inF and k2 == "c_mixed" and k3 == "c_mixed" and x == -1 and lam == Fraction(4, 3))

print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
