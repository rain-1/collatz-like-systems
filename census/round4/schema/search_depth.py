"""Search (not proof) for the deepest member of the designed family
D(2, m, Christoffel(a, b), h) of depth.md, for each m.

For each loop length L the letter count a is the largest with 3^a < 2^b (b = L - a).
Loops are ranked by L / |log lam|; for the best `nloops` the entry rotations are ranked in
floating point, and for the best few rotations the largest admissible h and the exact
k* are computed with depthlib.predicted_big (exact CERT criterion G_exit < Q of
Theorem A1 and exactly certified t*).  Usage: python3 search_depth.py m_lo m_hi
"""
import sys, math
import numpy as np
import depthlib as D

LOG3, LOG2 = math.log(3), math.log(2)


def loop_of(a, b):
    return [(3, 0) if c == 'U' else (1, 1) for c in D.christoffel(a, b)]


def best_rotations(m, a, b, top):
    loop = loop_of(a, b)
    L, Q = a + b, 2 ** m
    w = np.array([LOG3 if e == 0 else -LOG2 for (u, e) in loop])
    S = np.concatenate([[0.0], np.cumsum(np.concatenate([w, w]))])
    idx = np.arange(L)[:, None] + np.arange(1, L + 1)[None, :]
    pref = S[idx] - S[:L, None]
    isexit = np.array([e == 1 for (u, e) in loop] * 2)
    ex = np.where(isexit[idx - 1], pref, -np.inf).max(axis=1)
    gap = -S[L]
    c = []
    for i0 in range(L):
        h = min(int((m * LOG2 - ex[i0]) / LOG3), Q // 2 - 3 - L)
        if h < 0:
            continue
        c.append((h + L * (h * LOG3 + pref[i0].min()) / gap, i0, h))
    c.sort(reverse=True)
    return loop, c[:top]


def best_for(m, nloops=6, top=4):
    Q = 2 ** m
    loops = []
    for L in range(3, Q // 2 - 3):
        a = int(L / (1 + math.log2(3)))
        while 3 ** (a + 1) < 2 ** (L - a - 1):
            a += 1
        while 3 ** a >= 2 ** (L - a):
            a -= 1
        b = L - a
        if a >= 1 and math.gcd(a, b) == 1:
            loops.append((L / (b * LOG2 - a * LOG3), a, b))
    loops.sort(reverse=True)
    best = None
    for _, a, b in loops[:nloops]:
        loop, cands = best_rotations(m, a, b, top)
        for est, i0, h in cands:
            while h >= 0 and not D.predicted_big(2, m, loop, h, 3, i0)[0]:
                h -= 1
            if h < 0:
                continue
            cert, k, G = D.predicted_big(2, m, loop, h, 3, i0)
            if cert and (best is None or k > best[0]):
                best = (k, a, b, i0, h)
    return best


if __name__ == "__main__":
    for m in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        print(m, best_for(m), flush=True)
