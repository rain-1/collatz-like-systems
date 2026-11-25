# m3_g_s7: 3|n -> n/3; n=1 -> 5n+1; n=2 -> 5n+2. seed 7.
from _m3_common import get, seed_fate, all_below_reach, expanding_run
f = get('m3_g_s7')['step']
mu, lam, cyc = seed_fate(f, 7)
assert mu == 0 and lam == 5 and sorted(cyc) == [4, 7, 12, 21, 36], (mu, lam, cyc)
c8 = set(seed_fate(f, 8)[2])
assert c8 == {8, 42, 14, 72, 24}
bad = all_below_reach(f, 200000, set(cyc) | c8)
assert bad is None, bad
for j in range(1, 40):
    assert expanding_run(f, 1, j) >= j, j
print("m3_g_s7 OK: seed 7 returns after 5 steps; n<2e5 all reach the 4- or 8-cycle")
