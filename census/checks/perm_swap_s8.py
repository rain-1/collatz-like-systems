"""perm_swap_s8: orbit of 8 is an 11-cycle (tier 0); also checks S(n) = 5*T(n/5) (3-adic T)."""
import sys
from fractions import Fraction
from _perm_common import get, S, Sinv, agrees, is_mutual_inverse, cycle_of

def T_rat(x):  # 1932 map on rationals with denominator prime to 3
    r = (x.numerator * pow(x.denominator, -1, 3)) % 3
    return (Fraction(2, 3) * x, (4 * x - 1) / 3, (4 * x + 1) / 3)[r]

s = get("perm_swap_s8")
ok = agrees(s["step"], S, 200000) and is_mutual_inverse(S, Sinv, 200000)
ok = ok and all(S(n) == 5 * T_rat(Fraction(n, 5)) for n in range(1, 20001))
x, y = 40, 8          # multiples of 5 are S-invariant and S(5y) = 5 T(y)
from _perm_common import T
for _ in range(20000):
    x, y = S(x), T(y)
    ok = ok and x == 5 * y
cyc = cycle_of(s["step"], 8, 1000)
ok = ok and cyc == [8, 9, 6, 4, 7, 11, 13, 19, 27, 18, 12]
print("cycle:", cyc, "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
