"""up_ct35: n=7 mod 8 -> n+8; n=27 mod 32 -> n+32; else accelerated Collatz T.
Claim: every orbit is trapped (infinite) or reaches {1,2}."""
import sys, itertools
from systems import ct35_step as S, T, parity_word
from _ctcommon import affine, residue_has_word, untrapped_fate
ok = True
def fail(m):
    global ok; ok = False; print("FAIL", m)
trapped = lambda x: x % 8 == 7 or x % 32 == 27

# 1. parity lemma: x = 7 mod 8 <=> word3 = 111 ; x = 27 mod 32 <=> word5 = 11011
for r in range(32):
    good, w = residue_has_word(r, 32, 5)
    if not good:
        fail(f"word not determined by residue {r}")
    if (w[:3] == [1, 1, 1]) != (r % 8 == 7) or (w == [1, 1, 0, 1, 1]) != (r == 27):
        fail(f"trap/word mismatch r={r} w={w}")

# 2. word lemma + affine bound: allowed 5-words have <= 3 ones and b <= 58
bmax = 0
for w in itertools.product([0, 1], repeat=5):
    s = "".join(map(str, w))
    if "111" in s or s == "11011":
        continue
    a, b = affine(w)
    if a > 27:
        fail(f"word {s} has 4+ ones")
    bmax = max(bmax, b)
if bmax != 58:
    fail(f"bmax {bmax}")
# descent: (27x+58)/32 < x for x >= 12 ; [1,11] closed: (27*11+58)//32 <= 11
if not (27 * 12 + 58 < 32 * 12 and (27 * 11 + 58) // 32 <= 11):
    fail("descent constants")
# check the 5-step bound directly on untrapped orbits from a window of starts
for n in range(1, 100000):
    x, ok5 = n, True
    for _ in range(5):
        if trapped(x):
            ok5 = False; break
        x = S(x)
    if ok5 and 32 * x > 27 * n + 58:
        fail(f"5-step bound at {n}")

# 3. shortest window is 5: for L=1..4 exhibit an untrapped stretch with multiplier 3^k > 2^L
for L, word in [(1, [1]), (2, [1, 1]), (3, [1, 1, 0]), (4, [1, 1, 0, 1])]:
    found = None
    for n in range(1, 5000):
        if parity_word(n, L) == word:
            x, good = n, True
            for _ in range(L):
                if trapped(x):
                    good = False; break
                x = S(x)
            if good:
                found = n; break
    if found is None or 3 ** sum(word) <= 2 ** L:
        fail(f"window {L}")

# 4. finite table: n <= 11 -> trapped or cycle {1,2}; and global cross-check
for n in range(1, 400000):
    f = untrapped_fate(S, trapped, n)
    if f not in [("D",), ("C", 1)]:
        fail(f"{n}: {f}"); break
print("PASS" if ok else "FAIL"); sys.exit(0 if ok else 1)
