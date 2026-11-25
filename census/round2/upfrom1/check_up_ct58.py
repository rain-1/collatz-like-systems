"""up_ct58: n mod 256 in R -> n+256 (R: 8-step parity word has >= 6 ones); else accelerated Collatz T.
Claim: every orbit is trapped (infinite) or reaches {1,2}."""
import sys, itertools
from systems import ct58_step as S, CT58_TRAPS as R, parity_word
from _ctcommon import affine, residue_has_word, untrapped_fate
ok = True
def fail(m):
    global ok; ok = False; print("FAIL", m)
trapped = lambda x: x % 256 in R
if len(R) != 37:
    fail(f"|R|={len(R)}")
for r in range(256):
    good, w = residue_has_word(r, 256, 8)
    if not good or ((sum(w) >= 6) != (r in R)):
        fail(f"residue {r}")
bmax = max(affine(w)[1] for w in itertools.product([0, 1], repeat=8) if sum(w) <= 5)
if bmax != 1688:
    fail(f"bmax {bmax}")
if not (243 * 130 + 1688 < 256 * 130 and (243 * 129 + 1688) // 256 <= 129):
    fail("descent constants")
for n in range(1, 300000):
    f = untrapped_fate(S, trapped, n)
    if f not in [("D",), ("C", 1)]:
        fail(f"{n}: {f}"); break
print("PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
