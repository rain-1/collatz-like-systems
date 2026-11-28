"""Print the per-system markdown tables of README.md from data/named.json."""
import json, math, os
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
N = json.load(open(os.path.join(HERE, "data", "named.json")))
print("| system | origin | theta (certified) | W | rho | A(1) | A(10) | k* | forced class (depth 14 / 9) | survivor mass | C* = 1/(1-theta) | verified range | E* (own range) | E* (literature range) |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for id, r in N.items():
    p = 3 if id.startswith("m3") or id == "desc_m3_4n5" else 2
    fc = r["forced"]
    fcs = "none (D = 0)" if not fc or fc["D"] == 0 else "%d mod %d^%d" % (fc["residue"], p, fc["D"])
    def e(k):
        if k is None or str(k) not in r["E"]:
            return "-"
        x = r["E"][str(k)]
        return "%.3g (s = %s)" % (x["E_f"], x["s"])
    lit = r.get("lit")
    print("| %s%s | %s | %s = %.5f | %.3g | %s | %d | %d | %d | %s | %.3g | %.2f | %s | %s | %s |" % (
        id, " (signed)" if r["signed"] else "", r["origin"], r["theta"], r["theta_f"], r["W_f"], r["rho"],
        r["A1"], r["A10"], r["kstar"], fcs, fc["mass_f"] if fc else 0, r["Cstar"],
        ("2^%d" % r["range"]) if r["range"] else "-", e(r["range"]),
        (e(lit[0]) + " at 2^%d" % lit[0]) if lit else "-"))
