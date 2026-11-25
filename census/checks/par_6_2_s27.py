A, D = 6, 2
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

agree_with_catalog("par_6_2_s27", 27)
def syr(n):  # classical Syracuse odd->odd map
    m = 3*n + 1
    while m % 2 == 0: m //= 2
    return m
def nxt_odd(n):  # next odd value along a T-orbit from odd n
    m = T(n)
    while m % 2 == 0: m //= 2
    return m
for n in range(1, 200001, 2):
    assert T(n) == 2*(3*n+1) and T(T(n)) == 3*n+1 and nxt_odd(n) == syr(n)
pre, cyc = orbit_to_cycle(27)
assert sorted(cyc) == [1, 2, 4, 8] and 27 not in cyc
print("seed 27 preperiod", len(pre), "max", max(pre), "cycle", cyc)
assert len(pre) == 149
print("OK")
