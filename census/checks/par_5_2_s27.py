"""Check for par_5_2_s27 (odd n -> 5n+2). The proof is elementary (odd -> odd and
5n+2 > n); this script verifies the two algebraic facts on a range and the first
terms of the seed orbit, as a sanity check only."""
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
f = get('par_5_2_s27')['step']
for n in range(1, 2 * 10**5, 2):
    m = f(n)
    assert m % 2 == 1 and m > n
n = 27; prev = 0
for _ in range(1000):
    assert n % 2 == 1 and n > prev
    prev, n = n, f(n)
# closed form: odd n -> (n + 1/2) 5^k - 1/2, i.e. 2*T^k(n)+1 == (2n+1)*5^k
n0 = 27; n = n0
for k in range(200):
    assert 2 * n + 1 == (2 * n0 + 1) * 5**k
    n = f(n)
print('PASS')
