A, D = 1, 5
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

agree_with_catalog("par_1_5_s27", 27)
# descent: odd n > 5 -> n+5 (even) -> (n+5)/2 < n ; even n -> n/2 < n.
for n in range(7, 20001, 2):
    assert T(n) % 2 == 0 and T(T(n)) < n
# finite table: every n in 1..5 lies on a cycle
cycles = set()
for n in range(1, 6):
    pre, cyc = orbit_to_cycle(n)
    assert pre == [], n
    cycles.add(tuple(sorted(cyc)))
assert cycles == {(1, 2, 3, 4, 6, 8), (5, 10)}, cycles
pre, cyc = orbit_to_cycle(27)
assert tuple(sorted(cyc)) == (1, 2, 3, 4, 6, 8) and 27 not in cyc
print("seed 27: preperiod", pre, "cycle", cyc)
for n in range(1, 100001):
    _, c = orbit_to_cycle(n); assert tuple(sorted(c)) in cycles
print("OK")
