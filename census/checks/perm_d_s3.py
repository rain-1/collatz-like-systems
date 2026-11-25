"""perm_d_s3: orbit of 3 is the 3-cycle 3 -> 2 -> 5 -> 3 (tier 0)."""
import sys
from _perm_common import get, D, Dinv, agrees, is_mutual_inverse, cycle_of
s = get("perm_d_s3")
ok = agrees(s["step"], D, 200000) and is_mutual_inverse(D, Dinv, 200000)
cyc = cycle_of(s["step"], 3, 1000)
ok = ok and cyc == [3, 2, 5]
print("cycle:", cyc, "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
