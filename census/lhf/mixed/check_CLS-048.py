"""CLS-048 split5_1: every cycle with one expanding run is {1,3} (odd map). Exit 0 iff pass."""
import sys, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
from onerun_lib import run_theorem, v


def S(n):                       # odd-to-odd map of split5_1
    if n % 4 == 1:
        return (5 * n + 1) // 2
    m = n + 1
    return m >> v(m, 2)


ok = run_theorem("split5_1", S, lambda n: n % 2 == 1, Q=5, P=2,
                 low=lambda k: (2 ** (k + 1) - 1) // 3,
                 low_log=lambda k: (k + 1) * math.log(2) - math.log(3) - 1e-9,
                 c1=Fr(153, 100), c0=Fr(42, 100), ylo=1, c_hi=1, c_hi0=0, k0=25000,
                 expected=[(1, 1)])
# sanity: the descent-step and run lemmas on small n
for n in range(1, 200001, 2):
    if n % 4 == 1:
        assert S(n) % 2 == 1 and 3 * S(n) + 1 == 5 * (3 * n + 1) // 2
    else:
        assert S(n) <= (n + 1) // 4
for n0 in range(1, 20001, 2):
    k, x = 0, n0
    while S(x) > x:
        x, k = S(x), k + 1
    assert k == 0 or v(3 * n0 + 1, 2) == k + 1
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
