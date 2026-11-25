"""Check for auto_1932_s8 (the FATE/NONRETURN question itself is OPEN).

Default (pure Python, < 60 s): complete backtracking over transition tables
shows that no automaton certificate for NONRETURN of 8 exists with
  <= 6 states reading base-2 digits, and <= 4 states reading base-3 digits.
Every constraint used is necessary for any certificate:
  forward iterates G^n(8), n = 1..60, accepted; backward iterates G^-n(8),
  n = 0..60, rejected; n accepted => G(n) accepted for all sample n <= 300.
Candidate tables that pass the sample are re-checked exactly (all integers).

Optional:  python3 check_auto_1932_s8.py --sat   (needs python-sat)
reruns the SAT bounds reported in the .md (base 2 and base 3: <= 11 states;
this takes tens of minutes per base at the top end).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from autolib import check_partition, make_step, exhaust

G = [(3, 0, 2, 0), (3, 1, 4, 1), (3, 2, 4, 3)]
Gi = [(v, s, u, r) for u, r, v, s in G]
check_partition(G)
check_partition(Gi)
g, gi = make_step(G), make_step(Gi)
f, x = [], g(8)
for _ in range(60):
    f.append(x)
    x = g(x)
b, x = [], 8
for _ in range(60):
    b.append(x)
    x = gi(x)
assert len(set(f) | set(b)) == 120          # no coincidence in the computed range

for base, kmax in ((2, 6), (3, 4)):
    for k in range(1, kmax + 1):
        assert exhaust(base, G, 8, k, 300, f, b) is None, (base, k)
    print(f"base {base}: no certificate with <= {kmax} states: ok")

if "--sat" in sys.argv:
    from satlib import search
    f2, x = [], g(8)
    for _ in range(300):
        f2.append(x)
        x = g(x)
    b2, x = [], 8
    for _ in range(300):
        b2.append(x)
        x = gi(x)
    for base, kmax in ((2, 11), (3, 11)):
        k, dfa = search(base, G, 8, f2, b2, kmax=kmax, N=3000)
        assert k is None, (base, k, dfa)
        print(f"SAT: base {base}: no certificate with <= {kmax} states")
print("ALL OK")
