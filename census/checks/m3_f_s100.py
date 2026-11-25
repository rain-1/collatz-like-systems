# m3_f_s100: 3|n -> n/3; n=1 -> n+2; n=2 -> n+1. seed 100.
from _m3_common import get, seed_fate, descent_exceptions
f = get('m3_f_s100')['step']
mu, lam, cyc = seed_fate(f, 100)
assert (mu, lam, sorted(cyc)) == (8, 2, [1, 3]), (mu, lam, cyc)
exc = descent_exceptions(f, [(0, 1), (1, 2), (2, 2)])
assert exc == [1], exc
assert f(1) == 3 and f(3) == 1
print("m3_f_s100 OK: seed enters {1,3}; two-step descent; unique cycle {1,3}")
