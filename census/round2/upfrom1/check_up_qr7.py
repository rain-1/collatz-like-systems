"""Check for up_qr7: even n -> n/2; n=3 mod 28 -> n+28; other odd n -> n+7.
Claim: orbit infinite  <=>  n = 3,5,6 mod 7 (quadratic non-residues mod 7)."""
import sys
from systems import qr7_step as S

A = {0: 0, 1: 1, 2: 1, 4: 1, 3: 3, 5: 3, 6: 3}   # class label of n mod 7
ok = True

def fail(msg):
    global ok
    ok = False
    print("FAIL", msg)

# 1. invariance: S(n) mod 7 class depends only on n mod 28; check two full periods
for n in range(1, 2 * 28 * 7 + 1):
    if A[S(n) % 7] != A[n % 7]:
        fail(f"class not invariant at {n}")
# trap class invariant and increasing
for n in range(3, 3 + 28 * 50, 28):
    if not (S(n) % 28 == 3 and S(n) > n):
        fail(f"trap at {n}")

# 2. g = the n+7 map (S without the trap).  Block descent: odd n>7 -> (n+7)/2 < n.
g = lambda n: n // 2 if n % 2 == 0 else n + 7
for n in range(1, 8):           # [1,7] closed under blocks, intermediates <= 14
    m = g(n)
    if m > 14 or (n % 2 and g(m) > 7) or (n % 2 == 0 and m > 7):
        fail(f"block closure at {n}")
# g-cycles in [1,14]
cycles = set()
for n in range(1, 15):
    seen = []
    x = n
    while x not in seen:
        seen.append(x); x = g(x)
    cyc = seen[seen.index(x):]
    cycles.add(tuple(sorted(cyc)))
expect = {(1, 2, 4, 8), (3, 5, 6, 10, 12), (7, 14)}
if cycles != expect:
    fail(f"g-cycles {cycles}")
if 3 not in (3, 5, 6, 10, 12) or 3 % 28 != 3:
    fail("3 not trap")

# 3. exhaustive cross-check of the classification
def fate(n):
    seen = set()
    while n not in seen:
        if n % 28 == 3:
            return "D"
        seen.add(n); n = S(n)
    return "C1" if n in (1, 2, 4, 8) else ("C7" if n in (7, 14) else "other")
for n in range(1, 200000):
    f = fate(n)
    want = "D" if n % 7 in (3, 5, 6) else ("C7" if n % 7 == 0 else "C1")
    if f != want:
        fail(f"classification at {n}: {f} vs {want}"); break

# 4. control: trap moved to 19 mod 28 (19 = 5 mod 7, 3 mod 4) is NOT on the A3 g-cycle,
#    so the divergent set is no longer all of A3: the finite table is load-bearing.
def S19(n):
    return n // 2 if n % 2 == 0 else (n + 28 if n % 28 == 19 else n + 7)
def trapped19(n):
    seen = set()
    while n not in seen:
        if n % 28 == 19:
            return True
        seen.add(n); n = S19(n)
    return False
if trapped19(3):
    fail("control: 3 should escape the 19-trap")

print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
