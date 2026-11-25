"""Check for par_10_2_s7 (odd n -> 10n+2). Verifies the exact reduction to the
5x+1 map  T(n) = n/2 (n even), 5n+1 (n odd):  F(F(n)) = T(n) for n odd, F = T on
evens; and records that the seed orbit has no repeat in the first 20000 steps.
The latter is NOT a proof of divergence (the fate is OPEN)."""
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
F = get('par_10_2_s7')['step']
T = lambda n: n // 2 if n % 2 == 0 else 5 * n + 1
for n in range(1, 2 * 10**5):
    if n % 2: assert F(n) % 2 == 0 and F(F(n)) == T(n)
    else: assert F(n) == T(n)
# simulate seed 7 for 20000 steps, exact ints, check all distinct
n = 7; seen = set()
for _ in range(20000):
    assert n not in seen
    seen.add(n); n = F(n)
print('seed 7: 20000 distinct terms, current size', len(str(n)), 'digits')
print('PASS')
