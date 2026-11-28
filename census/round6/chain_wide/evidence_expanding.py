"""EVIDENCE only (finite orbit segments, floats for logs): the chain structure on
long orbit segments of the expanding maps 5x+1, 7x+1 and core W, which are
expected (not proved) to have divergent orbits.  For each start we follow the
update chain for N updates and report
  * sum of 1/y_l over the segment (the multiplier bound needs this finite),
  * the spread of log Z_l = log y_l - log P_l (Z is nondecreasing; exact),
  * successive multiplier minima over the segment (selected among the first
    half, so that the 'tail minimum' is not an artefact of the cut-off),
    their link ratios (must be in (1, rho]) and the minimum count of selected
    starts in any window of 10 octaves (THEORY.md Theorem 4(e) predicts at
    least A(10) for a genuinely escaping orbit).
"""
import math
import os
import sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import chainlib as L  # noqa: E402
import chain_systems as S  # noqa: E402


def flog(x):
    x = Fr(x)
    return math.log(x.numerator) - math.log(x.denominator)


def run(id, x0, N):
    T = S.BY_ID[id]["T"]
    g = L.D.build_graph(T)
    rho = max(e.F for e in g.edges)
    ch = L.update_chain(g, x0, N)
    ly = [math.log(y) if y < 1 << 1000 else y.bit_length() * math.log(2) for (_, y, _) in ch]
    ly = [flog(y) for (_, y, _) in ch]
    lP = [flog(P) for (_, _, P) in ch]
    lZ = [a - b for a, b in zip(ly, lP)]
    mono = all(lZ[i + 1] >= lZ[i] - 1e-9 for i in range(len(lZ) - 1))
    inv = sum(math.exp(-a) for a in ly)
    # successive last minimisers of P over the segment
    sel, t = [], -1
    while True:
        rest = range(t + 1, len(lP))
        if not rest:
            break
        m = min(lP[i] for i in rest)
        t = max(i for i in rest if lP[i] <= m + 1e-12)
        if t >= len(lP) // 2:
            break
        sel.append(t)
    ratios = [math.exp(lP[b] - lP[a]) for a, b in zip(sel, sel[1:])]
    A10 = L.chain_count(rho, 10)
    oct_ = [ly[i] / math.log(2) for i in sel]
    wins = []
    if oct_:
        for m in range(int(oct_[0]) + 1, int(oct_[-1]) - 10):
            wins.append(sum(1 for o in oct_ if m <= o < m + 10))
    print("%-8s x0=%d N=%d final 2^%.0f | Z nondecreasing: %s, log Z_N - log Z_0 = %.3g, sum 1/y = %.6g"
          % (id, x0, N, ly[-1] / math.log(2), mono, lZ[-1] - lZ[0], inv))
    print("          selected %d; link ratios in (1, %s]: %s (max %.4f); min per 10 octaves %s (A(10) = %d)"
          % (len(sel), rho, all(1 < r <= float(rho) * (1 + 1e-9) for r in ratios), max(ratios) if ratios else 0,
             min(wins) if wins else None, A10))


if __name__ == "__main__":
    for id, x0, N in [("par_5_1", 7, 6000), ("par_5_1", 9, 6000), ("par_7_1", 3, 4000),
                      ("par_7_1", 5, 4000), ("sf3_137", 15, 8000)]:
        run(id, x0, N)
