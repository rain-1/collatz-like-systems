# m3_a_s100: 3|n -> n/3; n=1 mod 3 -> (2n+1)/3; n=2 mod 3 -> (2n+2)/3. seed 100.
from _m3_common import get, seed_fate, descent_exceptions
f = get('m3_a_s100')['step']
mu, lam, cyc = seed_fate(f, 100)
assert (mu, lam, cyc) == (7, 1, [1]), (mu, lam, cyc)
exc = descent_exceptions(f, [(0, 1), (1, 1), (2, 1)])
assert exc == [1, 2], exc          # only fixed points fail to descend
assert f(1) == 1 and f(2) == 2
print("m3_a_s100 OK: seed -> fixed point 1 after 7 steps; f(n)<n for n>=3; fixed points {1},{2}")
