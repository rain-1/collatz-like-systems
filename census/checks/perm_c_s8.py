"""perm_c_s8: perm_c is the inverse of perm_swap; orbit of 8 is an 11-cycle (tier 0)."""
import sys
from _perm_common import get, S, Sinv, agrees, cycle_of
s = get("perm_c_s8")
ok = agrees(s["step"], Sinv, 200000) and all(S(Sinv(n)) == n and Sinv(S(n)) == n
                                              for n in range(1, 200001))
from _perm_common import Tinv
ok = ok and all(Sinv(5 * y) == 5 * Tinv(y) for y in range(1, 100001))
cyc = cycle_of(s["step"], 8, 1000)
ok = ok and cyc == [8, 12, 18, 27, 19, 13, 11, 7, 4, 6, 9]
print("cycle:", cyc, "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
