# m3_b_s8: 3|n -> n/3; n=1 -> (4n-1)/3; n=2 -> (4n+1)/3. seed 8.
from _m3_common import get, seed_fate, all_below_reach, expanding_run
f = get('m3_b_s8')['step']
mu, lam, cyc = seed_fate(f, 8)
assert (mu, lam, cyc) == (7, 1, [1]), (mu, lam, cyc)
# Evidence only (not a proof): every n < 2*10^5 reaches the fixed point 1.
bad = all_below_reach(f, 200000, {1})
assert bad is None, bad
# Obstruction to a finite descent table: n = 3^j - 1 grows for j steps.
for j in range(1, 40):
    assert expanding_run(f, 1, j) >= j, j
print("m3_b_s8 OK: seed 8 -> 1 in 7 steps; n<2e5 all reach 1; 3^j-1 ascends j steps")
