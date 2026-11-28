"""Census of trap sets (Theorems 2-4 of README.md).

Every subset A of a universe of residues mod 2^k is classified, for the map
C_{a,b} (n/2 on evens, a n + b on odds), at the single level m0 = k:

  P0 : every cycle of G_k^A contracts (pure potential / descent certificate)
  P1 : every SCC of G_k^A is contracting or a simple cycle (Theorem 2),
       and some cycle expands
  H  : some SCC is non-simple and has an expanding cycle; Theorem 4 then
       constructs a homoclinic avoider orbit, so by Theorem 3 no SCC
       certificate exists at any level and no descent certificate exists.

By Theorems 2-4 these are exhaustive (there is no 'undecided').
Provability is monotone in A, so only minimal provable sets and
maximal H sets are stored.  For each minimal provable set the full
certificate (with B and the finite simulation) is built and verified.
Usage: python3 census.py a k odd|all [b]
"""
import sys, json, time
sys.path.insert(0, __file__.rsplit('/', 1)[0] if '/' in __file__ else '.')
from traps_lib import *


def classify(T, A, k):
    m = max(k, T.beta)
    r = scc_method(T, A, k, m)
    kinds = [kd for kd, _, _ in r["info"]]
    assert "unknown" not in kinds
    if r["ok"]:
        return ("P0" if "simple" not in kinds or all(
            d[2] < (1 << d[3]) for kd, _, d in r["info"] if kd == "simple") else "P1"), r
    return "H", r


def run(a, k, universe, b=1, log=print):
    T = collatz_a(a, b=b)
    K = 1 << k
    U = [r for r in range(K) if (universe == 'all' or r % 2 == 1)]
    n = len(U)
    pos = {r: j for j, r in enumerate(U)}
    minimal, witnesses = [], []
    stats = {"P": 0, "H": 0}
    t0 = time.time()
    for s in sorted(range(1 << n), key=lambda s: (bin(s).count('1'), s)):
        if any((s & mm) == mm for mm, _ in minimal):
            stats["P"] += 1; continue
        if any((s & W) == 0 for W, _ in witnesses):
            stats["H"] += 1; continue
        A = {U[j] for j in range(n) if s >> j & 1}
        kind, r = classify(T, A, k)
        if kind != "H":
            cert = finish_certificate(T, A, k, max(k, T.beta), r)
            minimal.append((s, {"A": sorted(A), "type": kind, "B": cert["B"],
                                "cycles": cert["cycles"],
                                "simple_points": [str(x) for x, *_ in cert["simple_points"]],
                                "kinds": cert["kinds"]}))
            stats["P"] += 1
            continue
        comp, pc = r["bad"][0]
        x, L, z, j, i = homoclinic_from_scc(T, A, k, max(k, T.beta), r["adj"], comp)
        assert verify_homoclinic(T, A, k, x, L, z, j, i)
        path = [z]
        for _ in range(j):
            path.append(T.step_q(path[-1]))
        W = witness_residues(T, x, L, path, k)
        Wm = sum(1 << pos[q] for q in W if q in pos)
        num, c, E = composite(T, x, L)
        witnesses.append((Wm, {"x": str(x), "L": L, "mult": f"{num}/2^{E}",
                               "z": str(z), "j": j}))
        stats["H"] += 1
    full = (1 << n) - 1
    maxH = {full & ~W for W, _ in witnesses}
    maxH = [m for m in maxH if not any(m != m2 and (m & m2) == m for m2 in maxH)]
    return {"map": T.name, "k": k, "universe": universe, "stats": stats,
            "time": round(time.time() - t0, 1),
            "minimal_provable": [i for _, i in minimal],
            "maximal_H": sorted(sorted(U[j] for j in range(n) if m >> j & 1) for m in maxH),
            "witnesses": [dict(d, W=sorted(U[j] for j in range(n) if Wm >> j & 1))
                          for Wm, d in witnesses]}


if __name__ == "__main__":
    a, k, uni = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    b = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    out = run(a, k, uni, b)
    fn = f"census_{out['map'].replace(',', '_')}_k{k}_{uni}.json"
    json.dump(out, open(fn, "w"), indent=1)
    print(fn, out["stats"], "time", out["time"], "minimal", len(out["minimal_provable"]),
          "maxH", len(out["maximal_H"]))
