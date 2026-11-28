"""z3 existence search for type-(b) members of a choice family too large to enumerate.
Every hit is settled exactly with tblib.prove_H and the proof object is appended to
data/sat_<family>_H.json (verify with verify_H.py).

Usage: python sat_family.py NAME maxsol
NAME: any key of families.FAMILIES, or SPL_d1_m5, SH3_m5, D27 (built here).
"""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import families as FM
import tblib as TB
from sat_typeH import search

name, maxsol = sys.argv[1], int(sys.argv[2])
extra = {"SPL_d1_m5": (2, 5, FM.split_family(5, 1)), "SH3_m5": (2, 5, FM.shift_family(5)),
         "SH3_m6": (2, 6, FM.shift_family(6)), "S3_m6": (2, 6, FM.s_family(6, 3))}
p, m, opts = FM.FAMILIES[name] if name in FM.FAMILIES else extra[name]
t0 = time.time()
sols, res = search(p, m, opts, maxsol=maxsol, timeout_ms=1200000)
out = []
for ch, C in sols:
    tab = [opts[r][ch[r]] for r in range(p ** m)]
    P = TB.prove_H(p, m, tab)
    if P is None:
        print("HIT NOT CONFIRMED", ch)
        continue
    print(TB.fmt_rule(p, m, tab), "| cycles", [c[0] for c in P["cycles"]],
          "| isolated expanding x*:", [str(c["xstar"][0]) for c in P["comps"] if c["kind"] == "b"],
          flush=True)
    out.append(TB.to_json(P, f"{name} sat"))
os.makedirs(os.path.join(HERE, "data"), exist_ok=True)
json.dump(out, open(os.path.join(HERE, "data", f"sat_{name}_H.json"), "w"))
print(name, "solver result:", res, "hits:", len(out), f"{time.time() - t0:.0f}s")
