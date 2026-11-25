"""check for CLS-038 (lhf/perm-swap-c). Exact integers; exit 0 iff all pass.
Theorem part is proved in CLS-038.md; this script checks the identities used and the
predicted residue-graph structure for every modulus M <= 300 (finite confirmation only)."""
import sys
from _core_check import run
ok = run("T,Tinv".split(","), 300, "CLS-038")
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
