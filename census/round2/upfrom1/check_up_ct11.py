"""up_ct11: n=3 mod 4 -> n+4 (trap); else accelerated Collatz T.
Claim: every orbit is either trapped (infinite) or reaches the cycle {1,2}."""
import sys
from systems import ct11_step as S, T
from _ctcommon import untrapped_fate
ok = True
def fail(m):
    global ok; ok = False; print("FAIL", m)
# n = 1 mod 4: two steps give (3n+1)/4 < n for n > 1 (identity on a window)
for n in range(1, 200001, 4):
    if S(n) != (3 * n + 1) // 2 or S(S(n)) * 4 != 3 * n + 1:
        fail(f"identity {n}")
for n in range(1, 300000):
    f = untrapped_fate(S, lambda x: x % 4 == 3, n)
    if f not in [("D",), ("C", 1)]:
        fail(f"{n}: {f}"); break
print("PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
