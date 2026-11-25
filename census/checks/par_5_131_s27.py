"""Exact check for par_5_131_s27: even n -> n/2; odd n -> 5n+131, seed 27.
Expect preperiod 0, period 33, seed in cycle: True."""
import sys
a, d, seed = 5, 131, 27
T = lambda n: n // 2 if n % 2 == 0 else a * n + d
seen = {seed: 0}; n = seed; k = 0
while True:
    n = T(n); k += 1
    if n in seen:
        pre, per = seen[n], k - seen[n]
        break
    seen[n] = k
    if k > 10**6: sys.exit("no cycle found")
cyc = [n]
for _ in range(per - 1): cyc.append(T(cyc[-1]))
assert T(cyc[-1]) == cyc[0]
ok = (pre, per, seed in cyc) == (0, 33, True)
print("par_5_131_s27", "preperiod", pre, "period", per, "cycle min", min(cyc), "seed in cycle", seed in cyc, "OK" if ok else "FAIL")
sys.exit(0 if ok else 1)
