A, D = 1, 1
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

agree_with_catalog("par_1_1_s27", 27)
# descent: odd n >= 3 -> n+1 -> (n+1)/2 < n ; even n -> n/2 < n. Base: only n=1,2 remain.
for n in range(3, 20001, 2):
    assert T(n) % 2 == 0 and T(T(n)) < n
pre, cyc = orbit_to_cycle(1); assert pre == [] and sorted(cyc) == [1, 2]
pre, cyc = orbit_to_cycle(27)
assert sorted(cyc) == [1, 2] and 27 not in cyc
print("preperiod", len(pre), "cycle", cyc)
for n in range(1, 100001):
    _, c = orbit_to_cycle(n); assert sorted(c) == [1, 2]
print("OK")
