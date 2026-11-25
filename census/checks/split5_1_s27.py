"""Check for split5_1_s27.
FATE (proved, tier 0): exact simulation of seed 27.
GLOBAL (open): (a) witness that up-runs n -> (5n+1)/2 of every length k exist
(n = -1/3 mod 2^(k+2)), so no bounded-window descent can work; (b) evidence
only: every start <= 10^5 reaches the cycle {1,6,3,4,2} or {13,...}."""
import sys
from _split_common import check_fate, get
cyc = check_fate("split5_1_s27", 5, 5)
assert sorted(cyc) == [1, 2, 3, 4, 6]
f = get("split5_1_s27")["step"]
for k in (5, 20, 60):
    M = 2 ** (k + 2)
    n = (-pow(3, -1, M)) % M
    m, ups = n, 0
    while m % 4 == 1:
        m = f(m); assert m % 4 == 2; m //= 2; ups += 1
    assert ups >= k
    print(f"up-run witness k={k}: n={n} makes {ups} consecutive x5/2 steps")
known = {}
mins = set()
for s in range(1, 10 ** 5 + 1):
    seen = {}; n = s; path = []
    while n not in known and n not in seen:
        seen[n] = 1; path.append(n); n = f(n)
    c = known[n] if n in known else min(path[path.index(n):])
    for p in path: known[p] = c
    mins.add(c)
print("cycles reached from 1..1e5 (min elements):", sorted(mins), "(evidence only)")
assert sorted(mins) == [1, 13]
print("PASS")
sys.exit(0)
