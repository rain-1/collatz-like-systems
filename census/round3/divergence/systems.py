"""Round 3, lens "divergence": the new systems, as Python step functions.

Each entry: id, rule (text), step (function), seed, question.
Use get(id).  Systems marked with `rcwa` also carry an exact divlib.RCWA form.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from divlib import RCWA, modify  # noqa: E402
from race_common import R as _race  # noqa: E402

SYSTEMS = []


def add(id, rule, step, seed, question, rcwa=None):
    SYSTEMS.append(dict(id=id, rule=rule, step=step, seed=seed,
                        question=question, rcwa=rcwa))


# --- 1. the race map (non-injective, FRACTRAN type) -----------------------
add("race_s21",
    "5|n: 6n/7 if 7|n else 3n/5;  5∤n: 49n/6 if 6|n, 5n if n odd & 3|n, "
    "n/2 if n even & 3∤n, n if gcd(n,30)=1",
    _race, 21,
    "GLOBAL (exact divergent set and cycle list); FATE of 21; sizes of "
    "automaton certificates in bases 6, 2^j, 3^j")

# --- 2. 5x+1 with one class modified ---------------------------------------
B5 = RCWA(2, [(1, 0, 2), (5, 1, 1)], "5x+1")
FX10 = modify(B5, 64, {10: (5, 5, 1)}, "fx10_64")
FX26 = modify(B5, 32, {26: (7, 1, 1)}, "fx26_32")
add("fx10_64_s7",
    "5x+1 (n/2 even, 5n+1 odd) except n = 10 (mod 64) -> 5n+5",
    FX10, 7,
    "FATE of 7; which residue classes consist of divergent orbits", FX10)
add("fx26_32_s7",
    "5x+1 (n/2 even, 5n+1 odd) except n = 26 (mod 32) -> 7n+1",
    FX26, 7,
    "FATE of 7; which residue classes consist of divergent orbits", FX26)

# --- 3. accelerated 3x+1 (average contraction) with one class modified ----
T3 = RCWA(2, [(1, 0, 2), (3, 1, 2)], "T3x+1")
C62 = modify(T3, 64, {62: (4, 5, 1)}, "c62_64")
add("c62_64_s27",
    "accelerated 3x+1 (n/2 even, (3n+1)/2 odd) except n = 62 (mod 64) -> 4n+5",
    C62, 27, "FATE of 27", C62)

# --- 4. a new mixed-slope permutation --------------------------------------
P12 = RCWA(12, [(2, -9, 1), (4, 19, 1), (2, 8, 3), (1, 3, 3), (2, -1, 1), (2, -7, 3),
                (2, -9, 1), (4, 19, 1), (2, 8, 3), (2, -7, 1), (2, -1, 1), (2, -7, 3)],
           "perm12")
add("perm12_s7",
    "n=0 (6) -> 2n-9; n=1 (6) -> 4n+19; n=2 (6) -> (2n+8)/3; n=3 (12) -> (n+3)/3; "
    "n=9 (12) -> 2n-7; n=4 (6) -> 2n-1; n=5 (6) -> (2n-7)/3   (a permutation)",
    P12, 7, "FATE of 7", P12)


# --- 5. a two-swap neighbour of the 1932 permutation ----------------------
def _G(n):
    q, r = divmod(n, 3)
    return (2 * q, 4 * q + 1, 4 * q + 3)[r]


def _swT2_8(n):
    m = _G(n)
    r = m % 18
    return m + 1 if r in (2, 8) else (m - 1 if r in (3, 9) else m)


add("swT2_8_s8",
    "Q = sigma o G, G the 1932 permutation, sigma swaps n <-> n+1 for n = 2, 8 (mod 18)",
    _swT2_8, 8, "FATE of 8")


def get(id):
    for s in SYSTEMS:
        if s["id"] == id:
            return s
    raise KeyError(id)
