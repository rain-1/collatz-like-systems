"""Exact check for par_7_7_s9: even n -> n/2; odd n -> 7n+7, seed 9.
Expect preperiod 9, period 4, seed in cycle: False."""
import sys
a, d, seed = 7, 7, 9
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
ok = (pre, per, seed in cyc) == (9, 4, False)
print("par_7_7_s9", "preperiod", pre, "period", per, "cycle min", min(cyc), "seed in cycle", seed in cyc, "OK" if ok else "FAIL")
if not ok: sys.exit(1)
# conjugacy: T77(7m) = 7*T71(m) and the cycle is 7*{1,8,4,2}
T71 = lambda m: m // 2 if m % 2 == 0 else 7 * m + 1
assert all(T(7 * m) == 7 * T71(m) for m in range(1, 10**5))
assert sorted(cyc) == [7, 14, 28, 56]
print("conjugacy and cycle 7*{1,2,4,8} OK")
sys.exit(0)
