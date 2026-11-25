"""Tier-0 check for par_3_m1_s27: simulate the seed orbit exactly until a repeat."""
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
s = get('par_3_m1_s27')
r = fate('par_3_m1_s27')
assert r is not None, 'no cycle found'
tail, cyc = r
print('par_3_m1_s27', s['rule'], 'seed', s['seed'], 'tail', tail, 'cycle', cyc)
assert s['seed'] not in cyc
assert tail == 3
assert sorted(cyc) == [5, 7, 10, 14, 20]
print('PASS')
