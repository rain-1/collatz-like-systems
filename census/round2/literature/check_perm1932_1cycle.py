"""check_perm1932_1cycle: cycles of g(3q)=2q, g(3q+1)=4q+1, g(3q+2)=4q+3 with one
maximal block of non-multiples of 3 (proof in perm1932_1cycle.md).
A cycle with k ascent steps and l >= 1 descent steps has minimum x0 = 2^l e (3 !| e) and
satisfies e * D = S with D = 3^(k+l) - 2^(2k+l), |S| <= 4^k - 3^k.
(i) exact scan: for every l <= 600 and every k <= 2l+3 list (k,l) with |D| <= 4^k - 3^k,
    enumerate all e <= (4^k-3^k)/|D|, and test x0 = 2^l e by direct simulation;
(ii) Rhin-bound arithmetic: (3.82 l + 4.82)^(-13.3) < 2^(1-l) fails for all l > LB, LB < 600;
(iii) the k-range lemma k < (l log(3/2) + log 2)/log(4/3) <= 2l+3 is checked numerically."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from systems import get
g = get("perm1932_1cycle")["step"]
LMAX = 600
P3 = [1]
for _ in range(3 * LMAX + 10):
    P3.append(P3[-1] * 3)
cands, cycles = [], set()
for l in range(1, LMAX + 1):
    kbound = (l * math.log(1.5) + math.log(2)) / math.log(4 / 3)
    assert kbound <= 2 * l + 3
    for k in range(1, 2 * l + 4):
        D = P3[k + l] - (1 << (2 * k + l))
        bound = (1 << (2 * k)) - P3[k]
        if abs(D) > bound:
            continue
        assert k < kbound + 1e-9, (k, l)
        cands.append((k, l))
        for e in range(1, bound // abs(D) + 1):
            if e % 3 == 0:
                continue
            x0 = (1 << l) * e
            xs = [x0]
            for _ in range(k + l):
                xs.append(g(xs[-1]))
            ok = (xs[-1] == x0 and all(x % 3 for x in xs[:k])
                  and all(x % 3 == 0 for x in xs[k:k + l]))
            if ok:
                cycles.add(tuple(sorted(xs[:-1])))
assert cands == [(1, 1), (2, 1), (3, 2), (4, 3), (7, 5)], cands
assert cycles == {(2, 3), (4, 5, 6, 7, 9)}, cycles
# l = 0: pure ascent, g(x) >= x with equality only at x = 1
for x in range(1, 10**5):
    if x % 3:
        assert g(x) > x or x == 1
LB = max(l for l in range(2, 5000) if -13.3 * math.log(3.82 * l + 4.82) < (1 - l) * math.log(2))
assert LB < LMAX
print("perm1932_1cycle OK: candidate (k,l) =", cands, "; cycles", sorted(cycles), "+ (1); Rhin cutoff l <=", LB)
