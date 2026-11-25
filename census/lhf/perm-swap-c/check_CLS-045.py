"""check for CLS-045 (lhf/perm-swap-c). Exact integers; exit 0 iff all pass.
Theorem part is proved in CLS-045.md; this script checks the identities used and the
predicted residue-graph structure for every modulus M <= 300 (finite confirmation only)."""
import sys
from _core_check import run
ok = run("C,S".split(","), 300, "CLS-045")
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
