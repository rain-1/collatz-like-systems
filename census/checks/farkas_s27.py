"""Check for farkas_s27.
1. Seed 27 reaches the fixed point 1 (exact simulation).
2. Sanity check of the block lemma (proved by algebra in results/farkas_s27.md):
   for odd x > 1, x != 1 mod 3, write x + 1 = 2^a * b (b odd); then after
   exactly 2a+1 steps the orbit is at (b-1)/2, or it hit 1 earlier (only when b = 1).
   Also verifies every 1 < n <= 10^6 drops below n.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from systems import get
s = get("farkas_s27"); f = s["step"]

x, path = 27, [27]
for _ in range(1000):
    x = f(x); path.append(x)
    if x == 1:
        break
assert x == 1 and f(1) == 1 and 27 not in path[1:], path
print("seed 27 reaches fixed point 1 after", len(path) - 1, "steps:", path)

N = 10**6
for x in range(3, N + 1, 2):
    if x % 3 == 1:
        continue
    a, b = 0, x + 1
    while b % 2 == 0:
        a += 1; b //= 2
    y = x
    for i in range(2 * a + 1):
        y = f(y)
        if y == 1:
            break
    assert (y == (b - 1) // 2) or (y == 1 and b == 1), (x, a, b, y)
for n in range(2, N + 1):
    assert f(n) < n or (n % 2 == 1 and n % 3 != 1), n
print("block lemma verified for all odd x <= 10^6; every 1 < n <= 10^6 descends")
