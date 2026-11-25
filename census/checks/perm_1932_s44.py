"""perm_1932_s44: the orbit of 44 under the 1932 permutation is a 12-cycle (tier 0)."""
import sys
from _perm_common import get, T, Tinv, agrees, is_mutual_inverse, cycle_of
s = get("perm_1932_s44")
ok = agrees(s["step"], T, 200000) and is_mutual_inverse(T, Tinv, 200000)
cyc = cycle_of(s["step"], 44, 1000)
ok = ok and cyc == [44, 59, 79, 105, 70, 93, 62, 83, 111, 74, 99, 66]
print("cycle:", cyc, "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
