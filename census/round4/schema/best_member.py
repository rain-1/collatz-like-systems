"""Search helper (not proof): best entry rotation and largest h for a given Christoffel
loop (a, b) at modulus 2^m, ranked in floating point; the reported k* and the CERT
condition are then computed exactly (depthlib.predicted).  Usage: best_member.py m a b"""
import sys, math
import numpy as np
from fractions import Fraction
import depthlib as D

m, a, b = map(int, sys.argv[1:4])
loop = [(3, 0) if c == 'U' else (1, 1) for c in D.christoffel(a, b)]
L, Q = a + b, 2 ** m
w = np.array([math.log(3) if e == 0 else -math.log(2) for (u, e) in loop])
S = np.concatenate([[0.0], np.cumsum(np.concatenate([w, w]))])
idx = np.arange(L)[:, None] + np.arange(1, L + 1)[None, :]
pref = S[idx] - S[:L, None]                       # P_i(s), s = 1..L (logs)
isexit = np.array([e == 1 for (u, e) in loop] * 2)
ex = np.where(isexit[idx - 1], pref, -np.inf).max(axis=1)   # max exit prefix per rotation
gap = -S[L]
cands = []
for i0 in range(L):
    h = int((m * math.log(2) - ex[i0]) / math.log(3))
    h = min(h, Q // 2 - 3 - L)
    est = h + L * (h * math.log(3) + pref[i0].min()) / gap
    cands.append((est, i0, h))
cands.sort(reverse=True)
best = None
for est, i0, h in cands[:6]:
    while h >= 0 and not D.predicted_big(2, m, loop, h, 3, i0)[0]:
        h -= 1
    cert, k, G = D.predicted_big(2, m, loop, h, 3, i0)
    if cert and (best is None or k > best[0]):
        best = (k, a, b, i0, h)
print(m, best)
