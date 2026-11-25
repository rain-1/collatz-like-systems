"""Tier-0 check for par_3_3_s27: simulate the seed orbit exactly until a repeat."""
import sys, os
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from systems import get

def fate(sid, max_steps=10**6):
    """Exact Brent-free simulation with a dict; returns (tail, cycle list) or None."""
    s = get(sid); f = s['step']; n = s['seed']; seen = {}; k = 0
    while n not in seen and k < max_steps:
        seen[n] = k; n = f(n); k += 1
    if n not in seen:
        return None
    cyc = [n]; m = f(n)
    while m != n:
        cyc.append(m); m = f(m)
    return seen[n], cyc
s = get('par_3_3_s27')
r = fate('par_3_3_s27')
assert r is not None, 'no cycle found'
tail, cyc = r
print('par_3_3_s27', s['rule'], 'seed', s['seed'], 'tail', tail, 'cycle', cyc)
assert s['seed'] not in cyc
assert tail == 17
assert sorted(cyc) == [3, 6, 12]
# 3Z conjugacy n=3m with Collatz C: F(3m) == 3*C(m)
C = lambda m: m//2 if m%2==0 else 3*m+1
assert all(s["step"](3*m) == 3*C(m) for m in range(1, 10**5))
# every odd n maps into 3Z
assert all(s["step"](n) % 3 == 0 for n in range(1, 10**5, 2))
print('PASS')
