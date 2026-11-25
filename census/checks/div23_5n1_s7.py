"""Check for div23_5n1_s7: exact simulation of the seed orbit (FATE, tier 0).
Also re-runs a descent survey of 1 <= n <= 2*10^5 and reports cycles found.
The survey is evidence only; it proves nothing about GLOBAL (which is OPEN)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from systems import get
s = get("div23_5n1_s7"); f = s["step"]; seed = 7
seen = {}; x = seed; k = 0
while x not in seen:
    seen[x] = k; x = f(x); k += 1
pre = seen[x]; period = k - pre
cyc = [x]; y = f(x)
while y != x:
    cyc.append(y); y = f(y)
assert seed not in cyc, "seed lies on its cycle"
assert sorted(cyc) == sorted([1,6,3]), cyc
print("seed", seed, "preperiod", pre, "period", period, "cycle", cyc)
cmins = set()
for n in range(1, 2 * 10**5 + 1):
    x, seen = n, set()
    while x >= n:
        if x in seen:
            c = [x]; y = f(x)
            while y != x:
                c.append(y); y = f(y)
            cmins.add(min(c)); break
        seen.add(x); x = f(x)
print("survey n<=2e5: every orbit drops below its start or closes a cycle; cycle minima:", sorted(cmins))
