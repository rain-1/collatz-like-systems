"""Find the cycles met by 1..20000 and run the exact C range verifier.
Usage: python3 run_ranges.py LOG2N0 [id ...].  Writes data/ranges_<L>_<id>.json."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chainlib as L
import chain_systems as S
HERE = os.path.dirname(os.path.abspath(__file__))
lg = int(sys.argv[1]); ids = sys.argv[2:] or [s["id"] for s in S.NAMED if s["kind"] == "contracting"]
out = {}
for id in ids:
    T = S.BY_ID[id]["T"]
    cyc = L.find_cycles(T.step, 20000)
    elems = sorted({x for c in cyc.values() for x in c})
    args = [os.path.join(HERE, "verify_range"), str(lg), str(T.Q)]
    for (u, v, w) in T.table:
        args += [str(u), str(v), str(w)]
    args += ["--"] + [str(x) for x in elems]
    r = subprocess.run(args, capture_output=True, text=True)
    lines = r.stdout.split("\n")
    big = [int(l.split()[1]) for l in lines if l.startswith("BIG")]
    es = set(elems)
    for n in big:   # finish exactly with Python integers
        x, k = T.step(n), 1
        while not (x < n or x in es):
            x, k = T.step(x), k + 1
            assert k < 10 ** 8
    res = [l for l in lines if l.startswith("OK") or l.startswith("FAIL")]
    print(id, sorted(cyc), res, "big finished:", len(big), flush=True)
    out[id] = dict(cycle_minima=sorted(cyc), cycles={str(k): v for k, v in cyc.items()},
                   log2N0=lg, result=res, big=len(big), ok=(r.returncode == 0))
for id in out:
    json.dump({id: out[id]}, open(os.path.join(HERE, "data", "ranges_%d_%s.json" % (lg, id)), "w"), indent=1)
