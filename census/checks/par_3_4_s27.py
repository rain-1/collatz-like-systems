A, D = 3, 4
import sys
sys.path.insert(0, __import__("os").path.join(__import__("os").path.dirname(__file__), ".."))
from systems import get

def T(n):
    return n // 2 if n % 2 == 0 else A * n + D

def orbit_to_cycle(n, limit=10**6):
    seen = {}
    seq = []
    while n not in seen:
        assert len(seq) < limit, "no cycle within limit"
        seen[n] = len(seq); seq.append(n); n = T(n)
    mu = seen[n]
    return seq[:mu], seq[mu:]

def agree_with_catalog(sid, seed):
    s = get(sid)
    assert s["seed"] == seed
    n = seed
    for _ in range(2000):
        assert s["step"](n) == T(n), n
        n = T(n)
        if n.bit_length() > 3000:
            break

agree_with_catalog("par_3_4_s27", 27)
# odd n  ->  3n+4 which is odd: check the identity on residues symbolically
# n = 2k+1:  value = 6k+7
for k in range(0, 5000):
    n = 2*k + 1
    m = T(n)
    assert m % 2 == 1 and m > n and m == 3*n+4
# seed orbit: odd subsequence strictly increasing for the first 3000 odd visits
n, last, cnt = 27, 0, 0
while cnt < 3000:
    if n % 2:
        assert n > last; last = n; cnt += 1
    n = T(n)
print("OK")
