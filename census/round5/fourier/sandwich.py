"""Compare Theorem U' (exact constants) with the trivial sandwich, 3x+1, k = 1 (README revision, R-B).

Trivial sandwich: R_b cap [0, 2^{b-m}) is contained in R_{b-m} (as residues), and each of the other 2^m - 1 blocks
[i 2^{b-m}, (i+1) 2^{b-m}) holds at most |R_{b-m}| elements of R_b.  With rho = 2^m |R_{b-m}| / |R_b| >= 1:
    -(2^m - 1)(rho - 1) <= N(2^{b-m}, b) / (2^{b-m} P(b)) - 1 <= rho - 1,
so the sandwich certifies |dev| <= (2^m - 1)(rho - 1) (m >= 1) and needs |R_{b-m}|, |R_b| for that b.
Exact integers; |R_b| from decay.txt / decay_c31_28.txt / topdigits.txt and |R_29| = 6385637 (rb count 1 29 1).
"""
import os
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))

def sizes():
    R = {}
    lines = open(os.path.join(HERE, "decay.txt")).read().split("\n")
    for ln in lines[:15]:          # first block = 3x+1, b = 12..26
        w = ln.split(); R[int(w[0])] = int(w[1])
    for ln in open(os.path.join(HERE, "decay_c31_28.txt")):
        w = ln.split(); R[int(w[0])] = int(w[1])
    R[29] = 6385637
    for ln in open(os.path.join(HERE, "topdigits.txt")):
        w = list(map(int, ln.split()))
        if w[0] == 1: assert R.get(w[1], w[2]) == w[2]; R[w[1]] = w[2]
    return R

DPRIME = {1: Fraction(129, 1057), 2: Fraction(213, 749), 3: Fraction(349, 749)}   # L = 16 (b >= 16)

if __name__ == "__main__":
    R = sizes()
    print(" b   sandwich m=1   m=2     m=3    | U' (b>=16): 0.1220 0.2844 0.4660")
    worst = {1: 0, 2: 0, 3: 0}
    for b in range(16, 31):
        row = []
        for m in (1, 2, 3):
            rho = Fraction((1 << m) * R[b - m], R[b]); s = ((1 << m) - 1) * (rho - 1)
            row.append(float(s)); worst[m] = max(worst[m], float(s))
        print(f"{b:3d}   " + "  ".join(f"{x:.4f}" for x in row))
    print("max sandwich over b = 16..30:", {m: round(v, 4) for m, v in worst.items()})
