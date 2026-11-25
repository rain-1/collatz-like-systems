"""perm_1932inv_s8 (OPEN).  step == T^{-1}; no return of 8 in 1e5 steps (evidence);
no periodic separator modulo M <= 150."""
import sys
from _perm_common import get, T, Tinv, agrees, is_mutual_inverse, no_return, has_periodic_separator
s = get("perm_1932inv_s8")
ok = agrees(s["step"], Tinv, 200000) and is_mutual_inverse(T, Tinv, 200000)
nr, x = no_return(s["step"], 8, 100000)
print("no return in 1e5 steps:", nr, "bits at end:", x.bit_length())
seps = [M for M in range(1, 151) if has_periodic_separator(Tinv, 4, 8, M)]
print("moduli <=150 with a separator:", seps)
ok = ok and nr and not seps
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
