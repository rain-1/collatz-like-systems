"""Exact check of the residue-graph structure for T, T^{-1}, S, C=S^{-1} modulo every M <= MMAX.
Expected (theorem in CLS-038/035/038 notes):
  T, Tinv : one strongly connected component for every M.
  S, C    : one SCC if 5 does not divide M; exactly two SCCs {r: 5|r}, {r: 5 not | r} if 5 | M,
            and no edge between them.
Consequently no edge crosses components, i.e. no periodic forward-closed set separates any n from F(n)."""
import sys
from _common import BRANCH, edges, scc
MMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 400
ok = True
for name, (F, B) in BRANCH.items():
    bad = []
    for M in range(1, MMAX + 1):
        adj = edges(F, B, M); comp = scc(adj)
        ncomp = len(set(comp))
        crossing = any(comp[u] != comp[v] for u in range(M) for v in adj[u])
        if name in ("T", "Tinv") or M % 5:
            good = ncomp == 1
        else:
            good = ncomp == 2 and all((comp[r] == comp[0]) == (r % 5 == 0) for r in range(M))
        if not good or crossing: bad.append(M)
    print(f"{name}: moduli <= {MMAX} violating the predicted structure: {bad}")
    ok = ok and not bad
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
