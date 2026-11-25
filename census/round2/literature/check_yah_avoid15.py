"""check_yah_avoid15: map C with classes 1,5 mod 8 sent to 1.
Computational part: (i) the mod-8/16 facts used in the proof, checked on a full
residue system; (ii) the run lemma for n = 7 mod 8 for all such n <= 10^6;
(iii) survey: every n <= 10^6 reaches 1 (evidence)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from systems import get
from _avoid_common import survey, graph_edges, max_cycle_mean
import math
f = get("yah_avoid15")["step"]
# (i) n = 3 mod 8  ->  3n+1 = 2 mod 8 and (3n+1)/2 = 1 or 5 mod 8 (depends on n mod 16)
for n in range(3, 3 + 16 * 64, 8):
    assert (3 * n + 1) % 8 == 2 and ((3 * n + 1) // 2) % 8 in (1, 5)
# (ii) run lemma: n+1 = 2^a b, a >= 3: values 3^j 2^(a-j) b - 1 (j <= a-2) are 7 mod 8 for j<a-2,
#      intermediate evens are 6 mod 8, and j = a-2 gives a value = 3 mod 8.
for n in range(7, 10**6, 8):
    a, b = 0, n + 1
    while b % 2 == 0:
        a += 1; b //= 2
    x = n
    for j in range(a - 2):
        assert x % 8 == 7 and x == 3**j * 2**(a - j) * b - 1
        y = f(x); assert y % 8 == 6 and y == 3 * x + 1
        x = f(y)
    assert x == 3**(a - 2) * 4 * b - 1 and x % 8 == 3
# (iv) the tier-2 graph method fails at every modulus: loop -1 -> -2 -> -1 (classes 7,6), slope 3/2
for j in range(3, 65):
    M = 2**j
    assert (3 * (M - 1) + 1) % M == M - 2 and (M - 2) // 2 + M // 2 == M - 1
for j in range(3, 10):
    assert abs(max_cycle_mean(graph_edges(2**j, {1, 5})) - math.log(1.5) / 2) < 1e-9
survey(f, {1}, 10**6)
print("yah_avoid15 OK; seed 27 ->", [27, f(27), f(f(27)), f(f(f(27)))])
