#!/usr/bin/env python3
"""Sort the type-(c) tables found by census_small.py by excursion structure,
and attach orbit EVIDENCE.

Structure classes of a type-(c_mixed) SCC (exact):
  FP(s, sign): the SCC contains an expanding self-loop (an expanding fixed
               point x* = v/(w-u) of one branch); s = v_p(u - 1) measures how
               many low digits of u^k are fixed (u^k = 1 mod p^s); sign of x*:
               'neg-int', 'zero', 'nonint' (x* not an integer).
  LONG:        every expanding cycle of the SCC has length >= 2.
Orbit statistics (n <= N, EVIDENCE only): number of tables where every orbit
reached a cycle, and the cycle minima.
"""
import sys, os, json, random
from fractions import Fraction
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import intlib as IL

N = int(os.environ.get("NORB", "1500"))
SAMPLE = int(os.environ.get("SAMPLE", "150"))
random.seed(1)

out = {}
for fam in ["F2m2", "F2m3", "F3m2", "F3m2b"]:
    d = json.load(open(os.path.join(HERE, "enum_%s.json" % fam)))
    p, m = (2, 2) if fam == "F2m2" else (2, 3) if fam == "F2m3" else (3, 2)
    cls = Counter()
    bycls = defaultdict(list)
    for row in d["typec"]:
        if row["kind"] != "c_mixed":
            continue
        fps = row["fixed_points"]
        if not fps:
            key = "LONG"
        else:
            keys = []
            for fp in fps:
                x = Fraction(fp["x"])
                sg = "zero" if x == 0 else ("neg-int" if x.denominator == 1 and x < 0 else
                                            ("pos-int" if x.denominator == 1 else "nonint"))
                keys.append("FP(u=%d,s=%d,%s)" % (fp["u"], fp["s"], sg))
            key = " + ".join(sorted(set(keys)))
        cls[key] += 1
        bycls[key].append(row["table"])
    ev = {}
    for key, tabs in bycls.items():
        smp = tabs if len(tabs) <= SAMPLE else random.sample(tabs, SAMPLE)
        allconv = 0
        cycset = Counter()
        worst = 0.0
        for t in smp:
            T = IL.step_fn(p, m, t)
            cm, esc, w = IL.run_orbits(T, N, maxsteps=5000, cap=10 ** 30)
            if esc == 0:
                allconv += 1
                worst = max(worst, w)
            cycset[len(cm)] += 1
        ev[key] = dict(count=len(tabs), sampled=len(smp), all_converge=allconv,
                       ncycles_hist=dict(sorted(cycset.items())), worst_exponent=round(worst, 3))
    out[fam] = dict(counts=d["counts"], classes=ev)
    print("==", fam, d["counts"])
    for key in sorted(ev, key=lambda k: -ev[k]["count"]):
        print("  %-40s %s" % (key, ev[key]))
json.dump(out, open(os.path.join(HERE, "census_small_summary.json"), "w"), indent=1)
