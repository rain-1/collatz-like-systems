"""up_ct3: n=7 mod 8 -> n+8; else accelerated Collatz T.  OPEN.
Computational part: (a) every n < 10^6 is trapped or reaches {1,2};
(b) the window method provably fails: for every j there is an untrapped stretch of
3j steps with parity word (110)^j, multiplier (9/8)^j; (c) the untrapped 2-adic/negative
cycle -5 -> -7 -> -10 -> -5 realizes (110)^infinity."""
import sys
from systems import ct3_step as S, T, parity_word
from _ctcommon import untrapped_fate
ok = True
def fail(m):
    global ok; ok = False; print("FAIL", m)
trapped = lambda x: x % 8 == 7
for n in range(1, 1000000):
    f = untrapped_fate(S, trapped, n)
    if f not in [("D",), ("C", 1)]:
        fail(f"{n}: {f}"); break
for j in range(1, 15):
    L = 3 * j
    # the residue class mod 2^L with word (110)^j: solve by building digits
    target = [1, 1, 0] * j
    r = next(r for r in range(1 << L) if parity_word(r, L) == target) if L <= 18 else None
    if r is None:
        # lift: search r = r0 + k*2^(L-3)
        r = next(r0 + k * (1 << (L - 3)) for k in range(8) if parity_word(r0 + k * (1 << (L - 3)), L) == target)
    x = r + (1 << L)           # a positive representative
    for _ in range(L):
        if trapped(x):
            fail(f"(110)^{j} stretch trapped"); break
        x = S(x)
    r0 = r
if not (T(-5) == -7 and T(-7) == -10 and T(-10) == -5 and all(v % 8 != 7 for v in (-5, -7, -10))):
    fail("negative cycle")
print("PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
