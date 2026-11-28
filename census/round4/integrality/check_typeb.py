#!/usr/bin/env python3
"""Revision after REFEREE1: actually run Theorem H on the type-(b) tables of
the small census (census_small.md said "settled by Theorem H" without running it).

  [B-count]  Re-enumerates F3m2 and finds exactly 36 tables of type (b)
             (no type-(c) SCC, at least one expanding simple-cycle SCC).
  [B-H]      For each, round3/accel/accel_lib.theorem_H is applied at the least
             level K in {2,3,4} where its hypotheses hold (every SCC trivial,
             simple, or with exact contraction weights; no division-free cycle;
             no neutral simple cycle).  It returns the complete cycle list
             (PROVED by Theorem H of trichotomy.md).
  [B-brute]  Independent cross-check (not part of the proof, but it can fail):
             every n <= 20000 reaches one of the listed cycles, and no orbit
             of n <= 20000 meets a cycle that is not listed.
Writes typeb_cycles.json.  Exit 0 iff all PASS (about 10 s).
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import intlib as IL
import census_small as CS

ok = True


def claim(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name, flush=True)
    ok = ok and bool(cond)


typeb = []
for p, m, table in CS.family("F3m2"):
    if not IL.positivity_ok(p, m, table) or CS.division_free_cycle(p, m, table):
        continue
    kind, _ = IL.system_type(p, m, table)
    if kind == "b":
        typeb.append(table)
claim(f"[B-count] F3m2 has {len(typeb)} type-(b) tables (census_small.md says 36)", len(typeb) == 36)


def cycle_min(T, n, cap=10 ** 30, maxsteps=10 ** 5):
    seen = {}
    y = n
    for _ in range(maxsteps):
        if y in seen:
            c, z = [y], T(y)
            while z != y:
                c.append(z)
                z = T(z)
            return min(c)
        if y > cap:
            return None
        seen[y] = 1
        y = T(y)
    return None


out = []
allH = True
allbrute = True
for table in typeb:
    res, Kused = None, None
    for K in (2, 3, 4):
        try:
            res = IL.AL.theorem_H(3, 2, table, K)
            Kused = K
            break
        except AssertionError:
            continue
    if res is None:
        allH = False
        print("  Theorem H hypotheses fail at K <= 4 for", table)
        continue
    cyc = res["cycles"]
    T = IL.step_fn(3, 2, table)
    mins = set()
    for n in range(1, 20001):
        c = cycle_min(T, n)
        if c is None or c not in cyc:
            allbrute = False
            print("  brute force disagrees:", table, n, c, cyc)
            break
        mins.add(c)
    out.append(dict(table=table, K=Kused, cycles=cyc,
                    expanding_xstar=[str(c["xstar"]) for c in res["expanding"]]))
claim("[B-H] Theorem H applies to all 36 type-(b) tables and returns their cycle lists", allH and len(out) == 36)
claim("[B-brute] every n <= 20000 reaches a listed cycle (independent cross-check)", allbrute)

# negative control: dropping one cycle from a two-cycle list must be detected
two = [o for o in out if len(o["cycles"]) >= 2][0]
Tn = IL.step_fn(3, 2, two["table"])
short = two["cycles"][1:]
detected = any(cycle_min(Tn, n) not in short for n in range(1, 20001))
claim("[B-neg] control: a cycle list with one cycle removed is rejected by the brute-force check", detected)

with open(os.path.join(HERE, "typeb_cycles.json"), "w") as f:
    json.dump(out, f, indent=1)
from collections import Counter
print("cycle-list distribution:", Counter(tuple(o["cycles"]) for o in out))
print("levels used:", Counter(o["K"] for o in out))
print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
