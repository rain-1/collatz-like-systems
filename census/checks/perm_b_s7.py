"""perm_b_s7 (OPEN).  Verifies the exact conjugacy B(n) = T(n+1) - 1 (spot range; the
algebraic proof is in the write-up), and that the orbit of 7 is the 1932 orbit of 8 shifted by 1."""
import sys
from _perm_common import get, T, B, agrees
s = get("perm_b_s7")
ok = agrees(s["step"], B, 200000) and all(B(n) == T(n + 1) - 1 for n in range(1, 200001))
x, y = 7, 8
for _ in range(20000):
    x, y = s["step"](x), T(y)
    if x != y - 1 or x == 7:
        ok = False
        break
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
