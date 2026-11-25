"""check_yah_avoid57: map C with classes 5,7 mod 8 sent to 1 (YAH Conjecture 4.14).
The question is OPEN; this check only verifies the stated evidence and obstructions:
(i) survey: every n <= 10^6 enters {1,2,4};
(ii) obstruction: for every j = 3..64 the residue graph mod 2^j contains the cycle
     -7 -> -20 -> -10 -> -5 -> -14 -> -7 (classes 1,4,6,3,2 mod 8) of slope 9/8 > 1;
(iii) for j = 3..9 the maximum mean log-slope cycle equals log(9/8)/5 exactly (float);
(iv) YAH Prop. 4.15 reduction: from n = 1 mod 32 the orbit reaches (3n+1)/4, from
     n = 57 mod 64 it reaches (9n+7)/8, through allowed classes only; every other odd
     n = 1 mod 8 meets class 5 or 7 (or 1 is reached) before its next value = 1 mod 8."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from systems import get
from _avoid_common import survey, graph_edges, max_cycle_mean
f = get("yah_avoid57")["step"]
survey(f, {1, 2, 4}, 10**6)
K = {5, 7}
for j in range(3, 65):
    M = 2**j
    path = [(-7) % M, (-20) % M, (-10) % M, (-5) % M, (-14) % M, (-7) % M]
    assert [p % 8 for p in path] == [1, 4, 6, 3, 2, 1]
    for u, v in zip(path, path[1:]):
        if u % 2:
            assert v == (3 * u + 1) % M
        else:
            assert v in (u // 2, u // 2 + M // 2)
for j in range(3, 10):
    mm = max_cycle_mean(graph_edges(2**j, K))
    assert abs(mm - math.log(9 / 8) / 5) < 1e-9, (j, mm)
def to_next_1mod8(n):
    """Follow C from odd n = 1 mod 8 until the next odd value = 1 mod 8; None if 5/7 met."""
    x = 3 * n + 1
    while True:
        if x % 8 in K:
            return None
        if x % 2 and x % 8 == 1:
            return x
        x = x // 2 if x % 2 == 0 else 3 * x + 1
for n in range(9, 10**6, 8):
    nx = to_next_1mod8(n)
    if n % 32 == 1:
        assert nx == (3 * n + 1) // 4
    elif n % 64 == 57:
        assert nx == (9 * n + 7) // 8
    else:
        assert nx is None, n
print("yah_avoid57 checks OK (question remains OPEN)")
