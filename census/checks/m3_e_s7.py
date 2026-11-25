# m3_e_s7: 3|n -> n/3; n=1 -> 7n+2; n=2 -> 7n+1. seed 7.
# Evidence only: the fate of 7 is OPEN. This re-runs the simulation.
from _m3_common import get, seed_fate
f = get('m3_e_s7')['step']
assert sorted(seed_fate(f, 1)[2]) == [1, 3, 9]
c4 = set(seed_fate(f, 4)[2]); assert len(c4) == 14
cyc = set(seed_fate(f, 1)[2]) | c4
x = 7
for t in range(200000):
    x = f(x)
    assert x not in cyc and x != 7
b = x.bit_length()
assert b > 30000, b   # roughly 0.17 bits/step, matching the drift heuristic
print(f"m3_e_s7 OK (evidence only): 2e5 steps, no cycle hit, size {b} bits")
