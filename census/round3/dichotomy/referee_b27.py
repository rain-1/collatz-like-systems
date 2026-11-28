#!/usr/bin/env python3
"""Referee: independent recount of the B(27, a) phase-diagram numbers in phase_base3.md
(2^18 tables per a, exact verdict by referee_lib.fast_verdict).  Runtime ~8-10 minutes.
Exits 0 iff every count and maximum matches."""
import sys, os, itertools, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from referee_lib import fast_verdict
U = [r for r in range(27) if r % 3]
EXP = {2: (57816, 14), 4: (11661, 13), 5: (4364, 10), 7: (1328, 8), 8: (1074, 8),
       10: (69, 4), 11: (76, 5), 13: (64, 5)}
t0 = time.time()
for a, exp in EXP.items():
    n = mx = 0
    for mask in range(1 << 18):
        S = {U[i] for i in range(18) if mask >> i & 1}
        tab = [(1, 0, 3) if r % 3 == 0 else ((a, 1, 1) if r in S else (1, 1, 1)) for r in range(27)]
        if fast_verdict(27, tab) == "CERT":
            n += 1
            mx = max(mx, len(S))
    print(a, (n, mx), "claimed", exp, f"{time.time() - t0:.0f}s", flush=True)
    assert (n, mx) == exp
print("B27 ALL OK")
