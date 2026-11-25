"""Computational (finite) check: residue graphs of the iterates F^k (k=2,3) for F in {T,Tinv,S,C}
mod every M <= MMAX have no edge crossing strongly connected components, so no periodic F^k-closed
set separates n from F^k(n) for these k, M. Branch modulus of F^k is B^k."""
import sys
from _common import BRANCH, edges, scc
MMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 60
ok = True
for name, (F, B) in BRANCH.items():
    for k in (2, 3):
        Fk = (lambda F, k: (lambda n: [n := F(n) for _ in range(k)][-1]))(F, k)
        bad = []
        for M in range(1, MMAX + 1):
            adj = edges(Fk, B**k, M); comp = scc(adj)
            if any(comp[u] != comp[v] for u in range(M) for v in adj[u]):
                bad.append(M); continue
            nc = len(set(comp))
            exp = 1 if (name in ("T", "Tinv") or M % 5) else 2
            if nc != exp: bad.append(M)
        print(f"{name}^{k}: moduli <= {MMAX} with unexpected SCC structure: {bad}")
        ok = ok and not bad
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
