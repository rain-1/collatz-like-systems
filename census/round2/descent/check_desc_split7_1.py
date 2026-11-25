"""check: desc_split7_1  (even -> n/2; 1 mod 4 -> 7n+1; 3 mod 4 -> n+1).
Computational part of the proof that NO descent certificate exists (Lemma B
with the 2-adic 3-cycle through -1/3), plus the SPLIT family theorem checked
against the exhaustive certificate engine for a,b <= 31, d <= 7.
Simulation and drift are evidence only.  Exit 0 iff everything passes."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from descent_lib import *
import systems

s = systems.get("desc_split7_1")
p, m, tab = s["p"], s["m"], s["table"]
check_table(p, m, tab)

# 1. obstruction: -1/3 -> 7(-1/3)+1 = -4/3 -> -2/3 -> -1/3, multiplier 7/4
L, A, D, y = verify_obstruction(p, m, tab, Fraction(-1, 3))
assert (L, A, D) == (3, 7, 4), (L, A, D)

# 2. SPLIT family theorem: certificate <=> a < 2^va and b < 2^vb
def split(a, b, d):
    return [(1, 0, 2), (a, d, 1), (1, 0, 2), (b, d, 1)]

count = 0
for d in (1, 3, 5, 7):
    for a in range(1, 32, 2):
        for b in range(1, 32, 2):
            va = 1 if (a + d) % 4 == 2 else 2
            vb = 1 if (3 * b + d) % 4 == 2 else 2
            pred = a < 2 ** va and b < 2 ** vb
            t = split(a, b, d)
            c = certificate(2, 2, t, maxK=30, maxnodes=50000)
            assert c["ok"] == pred, (a, b, d)
            if pred:
                assert c["K"] <= 2 and c["k"] <= 3   # one block suffices
                verify_certificate(2, 2, t, c["leaves"])
            else:
                if a >= 2 ** va:
                    x = Fraction(d, 2 ** va - a)
                    assert (x.numerator * pow(x.denominator, -1, 4)) % 4 == 1
                else:
                    x = Fraction(d, 2 ** vb - b)
                    assert (x.numerator * pow(x.denominator, -1, 4)) % 4 == 3
                verify_obstruction(2, 2, t, x)
            count += 1
print("SPLIT family theorem verified on", count, "parameter triples")

# 3. evidence only
assert odd_markov_drift(2, {1: 7, 3: 1}) < -1.0
T = s["step"]
cyc = cycles_from(T, range(1, 100001))
print("evidence: all n <= 1e5 reach cycles with minima", sorted(min(c) for c in cyc))
print("PASS")
