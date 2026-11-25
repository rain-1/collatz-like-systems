"""Round 2, automata lens: systems (same style as census/systems.py).

Each entry: id, rule, step, seed, plus `branches` (list of (u, r, v, s):
u*q + r -> v*q + s for q >= 0) and the one question asked.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from autolib import make_step, suffix_branches  # noqa: E402

SYSTEMS = []


def add(id, rule, branches, seed, question):
    SYSTEMS.append(dict(id=id, rule=rule, branches=branches,
                        step=make_step(branches), seed=seed, question=question))


# Binary suffix permutation with seven rules (found by random search, kept
# because its orbit through 17 rises and falls forever in BOTH time directions).
SFX7 = [("00", "00"), ("001", "100110"), ("00101", "1110"), ("10", "1"),
        ("10101", "10110"), ("11", "010"), ("1101", "000110")]
SFX7_RULE = ("binary suffix rewrite: ..00->..00, ..001->..100110, ..00101->..1110, "
             "..10->..1, ..10101->..10110, ..11->..010, ..1101->..000110 "
             "(4q->4q, 8q+1->64q+38, 32q+5->16q+14, 4q+2->2q+1, 32q+21->32q+22, "
             "4q+3->8q+2, 16q+13->64q+6)")

add("auto_sfx7_s17", SFX7_RULE, suffix_branches(SFX7), 17,
    "FATE of 17 (answer: infinite)")

add("auto_sfx7_far", SFX7_RULE, suffix_branches(SFX7), 2 ** 21 + 5,
    "FATE of 2^21+5 (answer: infinite); side question: smallest binary "
    "automaton certificate")

# Mixed-slope permutation found by CEGAR automaton search (base-3 certificate).
add("auto_mix3_s7",
    "6|n -> n/2; n=2 mod 6 -> (3n+2)/2; n=4 mod 12 -> (3n-8)/4; "
    "n=10 mod 12 -> (3n-2)/4; n odd -> (3n+1)/2",
    [(6, 0, 3, 0), (6, 2, 9, 4), (12, 4, 9, 1), (12, 10, 9, 7), (2, 1, 3, 2)], 7,
    "FATE of 7 (answer: infinite)")

# The 1932 Collatz permutation, orbit of 8 (round 1: perm_1932_s8, tier 5).
add("auto_1932_s8", "3q->2q; 3q+1->4q+1; 3q+2->4q+3",
    [(3, 0, 2, 0), (3, 1, 4, 1), (3, 2, 4, 3)], 8,
    "NONRETURN of 8 (OPEN); side result: no small base-2/base-3 automaton certificate")

BY_ID = {s["id"]: s for s in SYSTEMS}


def get(id):
    return BY_ID[id]
