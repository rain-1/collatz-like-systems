"""Exact check of hypothesis (H), first half, of Theorem 3 for every
single-prime contracting system: there is a path from the root whose partial
slope products stay >= 1, ending at a state sigma, and a cycle sigma -> sigma
whose partial products are all > 1.  Also checks numerically (EVIDENCE) that
rho(P_s) has an interior minimiser (second half of (H)).
Exit 0 iff all exact checks pass.  Runtime: seconds.
"""
import os, sys
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from systems import SYSTEMS
from density_lib import build_graph, drift, rho, optimize, closed_classes


def find_H(g, maxlen=10):
    C = set(closed_classes(g)[0])
    # states reachable from the root along partial products >= 1 (product kept)
    reach = {}
    frontier = [(0, Fr(1), [])]
    for _ in range(maxlen):
        nf = []
        for st, A, path in frontier:
            if st not in reach or reach[st][0] < A:
                reach[st] = (A, path)
            for e in g.out[st]:
                A2 = A * e.F
                if A2 >= 1 and len(path) < maxlen:
                    nf.append((e.dst, A2, path + [e]))
        frontier = nf[:2000]
    for sigma in reach:
        if sigma not in C:
            continue
        # cycle sigma -> sigma with all partial products > 1
        stack = [(sigma, Fr(1), 0)]
        while stack:
            st, A, L = stack.pop()
            for e in g.out[st]:
                A2 = A * e.F
                if A2 <= 1:
                    continue
                if e.dst == sigma:
                    return sigma, reach[sigma][0], L + 1
                if L + 1 < maxlen:
                    stack.append((e.dst, A2, L + 1))
    return None


bad = 0
for S in SYSTEMS:
    g = build_graph(S['T'])
    if len(set(g.qs)) != 1:
        continue
    D, L, Df, Lf = drift(g)
    if Df >= 0:
        continue
    r = find_H(g)
    s, gm, th = optimize(g)
    interior = rho(g, s * 0.8, 0) > rho(g, s, 0) < rho(g, s * 1.25, 0) and s < 11
    print("%-15s (H) path+cycle: %s   s*~%.3f interior(EVIDENCE): %s" % (S['id'], r is not None, s, interior))
    if r is None:
        bad += 1
print("ALL (H) PATH CHECKS PASSED" if not bad else "%d FAILED" % bad)
sys.exit(1 if bad else 0)
