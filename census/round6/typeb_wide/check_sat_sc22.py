"""After REFEREE1 item 4: re-validation of the z3 encoding at the raised scale SC = 2^22.
SAT direction: the number of distinct type-(b) members found by z3 (all hits confirmed by
tblib.prove_H) equals the exhaustive count for C9 (53), SH3 m = 3 (2), SH5 m = 3 (3) and
D9 (0).  UNSAT direction: the stored outputs out/sc22/*.txt of the re-runs of every z3 row
say 'unsat'.  Completeness of those UNSAT answers is check_sat_precision.py.
Writes nothing.  Exit 0 iff all pass.  Needs the venv python (z3)."""
import sys, os, glob, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import families as FM, tblib as TB, sat_typeH as ST
OK = True
def claim(n, c):
    global OK
    print(("PASS " if c else "FAIL ") + n, flush=True); OK = OK and bool(c)
claim(f"SC = {ST.SC} = 2^22", ST.SC == 2 ** 22)
for name, want in (("C9", 53), ("SH3_m3", 2), ("SH5_m3", 3), ("D9", 0)):
    p, m, opts = FM.FAMILIES[name]
    st = json.load(open(os.path.join(HERE, "data", f"scan_{name}.json")))
    sols, res = ST.search(p, m, opts, maxsol=10 * want + 10, timeout_ms=1200000)
    good = 0
    for ch, C in sols:
        P = TB.prove_H(p, m, [opts[r][ch[r]] for r in range(p ** m)])
        good += P is not None and P["verdict"] == "b"
    claim(f"{name}: z3 found {len(sols)} members, {good} confirmed type (b), solver ended '{res}', "
          f"exhaustive count {st['counts'].get('b', 0)}",
          len(sols) == good == want == st["counts"].get("b", 0) and str(res) == "unsat")
fs = sorted(glob.glob(os.path.join(HERE, "out", "sc22", "*.txt")))
claim(f"{len(fs)} stored SC=2^22 re-runs, all unsat",
      len(fs) == 8 and all("unsat" in open(f).read() and "hits: 0" in open(f).read() or
                           "solver: unsat solutions: 0" in open(f).read() for f in fs))
print("ALL PASS" if OK else "FAIL"); sys.exit(0 if OK else 1)
