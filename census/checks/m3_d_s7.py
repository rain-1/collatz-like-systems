# m3_d_s7: 3|n -> n/3; n=1 -> 4n+2; n=2 -> 4n+1. seed 7.
from _m3_common import get, seed_fate, all_below_reach, expanding_run
f = get('m3_d_s7')['step']
mu, lam, cyc = seed_fate(f, 7)
assert mu == 0 and lam == 16 and cyc[0] == 7, (mu, lam, cyc)
c1 = set(seed_fate(f, 1)[2]); c7 = set(cyc)
assert c1 == {1, 6, 2, 9, 3}
bad = all_below_reach(f, 200000, c1 | c7)
assert bad is None, bad
for j in range(1, 40):
    assert expanding_run(f, 1, j) >= j, j
print("m3_d_s7 OK: seed 7 returns after 16 steps; n<2e5 all reach {1,6,2,9,3} or the 7-cycle")
