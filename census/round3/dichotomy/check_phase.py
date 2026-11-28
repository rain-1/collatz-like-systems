#!/usr/bin/env python3
"""Re-derives the aggregate counts quoted in phase_base3.md for the parts that run in under
~2 minutes: family B(9, a) for all a, family C9 (8^6 tables), and D(36, a) (mixed modulus).
Every verdict is exact (decide.py verifies an integer potential or an expanding/critical
cycle).  The B(27, a) counts (2^18 tables per a, ~1 min each) are reproduced by
`python3 scan_base3.py B27`; pass --full to re-check them here too.
"""
import sys, os, itertools, collections
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from decide import decide
from families import base3_S, base3_table
from systems import D_table

full = "--full" in sys.argv


def countB(Q, a):
    units = [r for r in range(Q) if r % 3]
    c = collections.Counter()
    mx = 0
    for mask in range(1 << len(units)):
        S = {units[i] for i in range(len(units)) if mask >> i & 1}
        v = decide(Q, base3_S(Q, a, S), want_cycles=False, want_depth=False)["verdict"]
        c[v] += 1
        if v == "CERT":
            mx = max(mx, len(S))
    return c["CERT"], mx


B9 = {2: (24, 4), 4: (10, 3), 5: (8, 3), 7: (6, 2), 8: (6, 2), 10: (1, 0), 11: (1, 0), 13: (1, 0)}
for a, exp in B9.items():
    assert countB(9, a) == exp, (a, countB(9, a))
print("B9 ok")
if full:
    B27 = {2: (57816, 14), 4: (11661, 13), 5: (4364, 10), 7: (1328, 8), 8: (1074, 8),
           10: (69, 4), 11: (76, 5), 13: (64, 5)}
    for a, exp in B27.items():
        assert countB(27, a) == exp, a
    print("B27 ok")

C8 = [(1, 1), (1, 2), (2, 1), (2, -1), (4, 1), (4, -1), (5, 1), (5, -1)]
units = [1, 2, 4, 5, 7, 8]
c = collections.Counter()
for combo in itertools.product(range(8), repeat=6):
    res = decide(9, base3_table(9, {r: C8[i] for r, i in zip(units, combo)}),
                 want_cycles=False, want_depth=False)
    c[res["verdict"] + ("-" + res["obst"]["kind"] if res["verdict"] == "OBST" else "")] += 1
assert c == {"CERT": 11956, "OBST-expanding": 250187, "OBST-critical": 1}, c
print("C9 ok")

for a, exp in ((5, (756, 8)), (7, (336, 7))):
    u36 = [r for r in range(36) if r % 2 and r % 3]
    n = mx = 0
    for mask in range(1 << 12):
        S = {u36[i] for i in range(12) if mask >> i & 1}
        if decide(36, D_table(36, a, S), want_cycles=False, want_depth=False)["verdict"] == "CERT":
            n += 1
            mx = max(mx, len(S))
    assert (n, mx) == exp
print("D36 ok")
print("ALL OK")
