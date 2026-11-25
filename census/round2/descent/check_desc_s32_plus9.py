"""check: desc_s32_plus9.  Computational part of the proof that NO descent
certificate exists (Lemma B with the 2-adic 12-cycle through -227/115,
multiplier 3^5/2^7), plus: every one-class enlargement of S0 is obstructed
(so S0 is a maximal certifiable set), and S0 itself is certifiable.
Drift and simulation are evidence only.  Exit 0 iff everything passes."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from descent_lib import *
import systems

s = systems.get("desc_s32_plus9")
check_table(2, 5, s["table"])
L, A, D, y = verify_obstruction(2, 5, s["table"], Fraction(-227, 115))
assert (L, A, D) == (12, 243, 128)
print("obstruction: period 12, multiplier 243/128, all partial multipliers > 1 from", y)

# maximality of S0: the four one-class enlargements, each with its witness
wit = {9: (Fraction(-227, 115), 12, 243, 128), 19: (Fraction(-65, 17), 10, 81, 64),
       27: (Fraction(-10), 5, 9, 8), 31: (Fraction(-1), 2, 3, 2)}
for r, (x, L0, A0, D0) in wit.items():
    t = systems.s_table(5, systems.S0 + (r,))
    assert verify_obstruction(2, 5, t, x)[:3] == (L0, A0, D0), r
assert certificate(2, 5, systems.s_table(5, systems.S0), maxK=80)["ok"]
print("S0 certifiable; S0+{9}, S0+{19}, S0+{27}, S0+{31} all obstructed")

# evidence only
mult = {r: (3 if r in systems.S0 + (9,) else 1) for r in range(1, 32, 2)}
dr = odd_markov_drift(5, mult)
assert dr < -0.8
print("random-model drift per odd step: %.3f" % dr)
cyc = cycles_from(s["step"], range(1, 200001))
print("evidence: all n <= 2e5 reach cycles with minima", sorted(min(c) for c in cyc))
print("PASS")
