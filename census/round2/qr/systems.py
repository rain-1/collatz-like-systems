"""Round 2, lens `qr`: quadratic-residue and multiplicative-coset invariants.

Every map here has the shape  n -> (n + c*q)/m  with m in a fixed multiplier set
and c in [0, m-1] the unique value making the division exact (or c from a fixed
table, family B).  Hence T(n) = n * m^{-1} (mod q): the class of n in
(Z/q)/<multipliers> is invariant, and every orbit descends into a finite box.
The question for each system is BASIN (or CYCLES+BASIN): which cycle does n reach.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qrlib import famA, famB, famC

SYSTEMS = []


def add(id, rule, step, seed, question):
    SYSTEMS.append(dict(id=id, rule=rule, step=step, seed=seed, question=question))


add("qrA3_q23", "even n -> n/2; odd n -> (n + 23c)/3, c in {0,1,2} minimal with 3 | n+23c",
    famA(23, 3), 27,
    "BASIN: classify every n by the cycle it reaches (cycles {1,8,4,2}, {5,...}, {23})")
add("qrA3_q307", "even n -> n/2; odd n -> (n + 307c)/3, c in {0,1,2} minimal",
    famA(307, 3), 27,
    "BASIN: classify every n by the cycle it reaches (cycles through 1, 5, 7, and {307})")
add("qrA5_q251", "even n -> n/2; odd n -> (n + 251c)/5, c in {0..4} minimal",
    famA(251, 5), 27,
    "BASIN: classify every n by the cycle it reaches (cycles through 1,3,7,9,21 and {251})")
add("qrC_q311", "even -> n/2; n=1 (4) -> (n+311c)/3; n=3 (4) -> (n+311c)/5; c minimal",
    famC(311), 27,
    "BASIN: classify every n by the cycle it reaches (cycles through 3, 11, and {311})")
add("qrA3_q95", "even n -> n/2; odd n -> (n + 95c)/3, c in {0,1,2} minimal",
    famA(95, 3), 27,
    "BASIN: classify every n by the cycle it reaches (cycles through 1, 7, 5, 19 and {95})")
add("qrB7_c53", "even -> n/2; n=1 (4) -> (n+35)/2; n=3 (4) -> (n+21)/2",
    famB(7, 5, 3), 27,
    "BASIN: classify every n by the cycle it reaches ({1,18,9,22,11,16,8,4,2}, {3,12,6}, {5,20,10}, {7,14})")
add("qrA3_q17", "even n -> n/2; odd n -> (n + 17c)/3, c = n mod 3",
    famA(17, 3), 27,
    "BASIN: give a finite-state (automatic) rule deciding whether n reaches {1,6,3} or {5,13,10}")


def get(id):
    return next(s for s in SYSTEMS if s["id"] == id)
