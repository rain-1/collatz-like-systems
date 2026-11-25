"""check: desc_m3_4n5  (3|n -> n/3; 1 mod 3 -> 4n+5; 2 mod 3 -> 2n+2).
Computational part of: (i) no descent certificate (Lemma B, 3-adic 2-cycle
-5 -> -15 -> -5 with multiplier 4/3); (ii) the M3 family theorem checked
against the exhaustive engine for a,b in {1,2,4,5,7,8}, c1,c2 in 0..8.
Simulation and drift are evidence only.  Exit 0 iff everything passes."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction
from descent_lib import *
import systems

s = systems.get("desc_m3_4n5")
p, m, tab = s["p"], s["m"], s["table"]
check_table(p, m, tab)
L, A, D, y = verify_obstruction(p, m, tab, Fraction(-5))
assert (L, A, D) == (2, 4, 3)

def pred(a, c1, b, c2):
    i1, i2 = (a + c1) % 3, (2 * b + c2) % 3
    if i1 == 0 and i2 == 0:
        return a < 3 and b < 3
    if i1 == 2 and i2 == 0:
        return a * b < 3 and b < 3
    if i1 == 0 and i2 == 1:
        return a * b < 3 and a < 3
    return False

n_cert = n_obs = n_inv = 0
for a in (1, 2, 4, 5, 7, 8):
    for b in (1, 2, 4, 5, 7, 8):
        for c1 in range(9):
            for c2 in range(9):
                t = [(1, 0, 3), (a, c1, 1), (b, c2, 1)]
                P = pred(a, c1, b, c2)
                c = certificate(3, 1, t, maxK=14, maxnodes=40000 if P else 300)
                assert c["ok"] == P, (a, c1, b, c2)
                if P:
                    assert c["k"] <= 3
                    verify_certificate(3, 1, t, c["leaves"])
                    n_cert += 1
                    continue
                i1, i2 = (a + c1) % 3, (2 * b + c2) % 3
                # (a) a residue class mapped into itself / a 2-cycle of classes
                # avoiding 0: T^j(n) >= n for every n there and every j
                if i1 == 1 or i2 == 2 or (i1 == 2 and i2 == 1):
                    n_inv += 1
                    continue
                # (b) otherwise a full block with multiplier > 1 has a fixed point
                if i1 == 0 and a > 2:
                    x = Fraction(c1, 3 - a)          # (a x + c1)/3 = x
                elif i2 == 0 and b > 2:
                    x = Fraction(c2, 3 - b)
                elif i1 == 2:                        # 1 -> 2 -> 0 block
                    x = Fraction(b * c1 + c2, 3 - a * b)
                else:                                # i2 == 1: 2 -> 1 -> 0 block
                    x = Fraction(a * c2 + c1, 3 - a * b)
                verify_obstruction(3, 1, t, x)
                n_obs += 1
print("M3 family theorem: certified", n_cert, "Lemma-B obstructed", n_obs,
      "invariant-class", n_inv)

# evidence only: drift per non-multiple step = (log4+log2)/2 - 1.5 log3 < 0
assert (math.log(4) + math.log(2)) / 2 - 1.5 * math.log(3) < -0.6
cyc = cycles_from(s["step"], range(1, 20001))
print("evidence: all n <= 2e4 reach cycles with minima", sorted(min(c) for c in cyc))
print("PASS")
