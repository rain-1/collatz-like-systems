"""check_yah_avoid6: map C with class 6 mod 8 sent to 1.
(i) transition facts of the proof on a full residue system mod 2^10;
(ii) the odd-to-odd descent claims for every odd o <= 10^6 whose next odd is reached
     without meeting class 6 mod 8;
(iii) Yolcu-Aaronson-Heule's own method: max mean log-slope cycle of the mod-8 graph < 0;
(iv) survey: every n <= 10^6 enters {1,2,4} (evidence)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from systems import get
from _avoid_common import survey, graph_edges, max_cycle_mean
f = get("yah_avoid6")["step"]
M = 2**10
for n in range(1, 64 * M, 2):
    r = n % 8
    if r == 7:
        assert (3 * n + 1) % 8 == 6
    if r == 3:
        assert (3 * n + 1) % 8 == 2 and ((3 * n + 1) // 2) % 8 in (1, 5)
    if r == 1:
        assert (3 * n + 1) % 8 == 4
        if ((3 * n + 1) // 2) % 8 == 2:
            assert ((3 * n + 1) // 4) % 8 in (1, 5)
    if r == 5:
        assert (3 * n + 1) % 8 == 0
def next_odd(o):
    """Next odd value of the C_6 orbit after odd o, or None if class 6 is met."""
    x = f(o)
    while x % 2 == 0:
        if x % 8 == 6:
            return None
        x = f(x)
    return x
for o in range(3, 10**6, 2):
    if o % 8 == 7:
        continue
    p = next_odd(o)
    if p is None:
        continue
    if o % 8 == 3:
        assert p % 8 in (1, 5) and p == (3 * o + 1) // 2
    elif o % 8 == 1:
        assert p % 8 in (1, 5) and p == (3 * o + 1) // 4 and p < o
    else:  # o = 5 mod 8
        assert p * 8 <= 3 * o + 1 and p < o
        if p % 8 == 3:
            q = next_odd(p)
            if q is not None:
                assert 16 * q <= 9 * o + 11 and q < o
assert max_cycle_mean(graph_edges(8, {6})) < 0
survey(f, {1, 2, 4}, 10**6)
print("yah_avoid6 OK; mod-8 max cycle mean =", round(max_cycle_mean(graph_edges(8, {6})), 4))
