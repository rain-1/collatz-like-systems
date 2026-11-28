"""Summarise data/families.json (written by chain_table.py) as markdown tables."""
import collections, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
F = json.load(open(os.path.join(HERE, "data", "families.json")))
for fam, rows in F.items():
    c = [r for r in rows if r.get("contracting")]
    def reason(r):  # revised after REFEREE1: classify by drift sign instead of the raw message
        e = r.get("error") or ""
        if e.startswith("graph"):
            return "graph error: " + e[7:47]
        d = r.get("drift")
        if d is None:
            return "drift not computed"
        return "drift > 0" if d > 0 else ("drift = 0" if d == 0 else "drift < 0 (NOT EXPECTED)")
    errs = collections.Counter(reason(r) for r in rows if not r.get("contracting"))
    print("## %s: %d members, %d with a certified negative drift" % (fam, len(rows), len(c)))
    print("non-certified reasons:", dict(errs))
    by = collections.Counter((r["rho"], r["A1"], r["A10"]) for r in c)
    print("no expanding edge (all slopes <= 1, GLOBAL trivially by Cor. 3.1):", sum(1 for r in c if r.get("no_expanding_edge")))
    print("clipped to gamma = 1 (theta = 0):", sum(1 for r in c if r["theta"] == "0"))
    print("| rho | A(1) | A(10) | members | theta range | C* range | forced D range | raw (R) ok | signed |")
    print("|---|---|---|---|---|---|---|---|---|")
    for (rho, a1, a10), n in sorted(by.items(), key=lambda kv: -kv[1]):
        rs = [r for r in c if (r["rho"], r["A1"], r["A10"]) == (rho, a1, a10)]
        th = [r["theta_f"] for r in rs]; cs = [r["Cstar"] for r in rs]
        ds = [r["forced"]["D"] if r["forced"] else -1 for r in rs]
        print("| %s | %s | %s | %d | %.4f-%.4f | %.2f-%.2f | %d-%d | %s | %s |" % (
            rho, a1, a10, n, min(th), max(th), min(cs), max(cs), min(ds), max(ds),
            all(r["raw_prefix_ok"] for r in rs), sum(r["signed"] for r in rs)))
    print()
