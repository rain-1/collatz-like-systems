"""Check for split5_3_s27.
FATE (proved, tier 0): exact simulation of seed 27.
GLOBAL (open): (a) witness that up-runs n -> (5n+3)/4 of every length k exist
(n = 4^(k+1) - 3), so no bounded-window descent can work; (b) evidence only:
every start <= 10^5 reaches one of the five known cycles."""
import sys
from _split_common import check_fate, get
cyc = check_fate("split5_3_s27", 8, 2)
assert sorted(cyc) == [3, 6]
f = get("split5_3_s27")["step"]
for k in (5, 20, 60):
    n = 4 ** (k + 1) - 3
    m, ups = n, 0
    while m % 4 == 1:
        m = f(m); assert m % 4 == 0; m //= 4
        if m % 2 == 0: break
        ups += 1
    assert ups >= k
    print(f"up-run witness k={k}: {ups} consecutive x5/4 steps from 4^{k+1}-3")
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
assert sorted(mins) == [1, 3, 5, 61, 125]
print("PASS")
sys.exit(0)
