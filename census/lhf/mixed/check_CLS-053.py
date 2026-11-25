"""CLS-053 desc_split7_1: no cycle of the odd map has exactly one expanding run. Exit 0 iff pass."""
import sys, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
from onerun_lib import run_theorem, v


def S(n):                       # odd-to-odd map of desc_split7_1
    m = 7 * n + 1 if n % 4 == 1 else n + 1
    return m >> v(m, 2)


ok = run_theorem("split7_1", S, lambda n: n % 2 == 1, Q=7, P=2,
                 low=lambda k: (2 ** (2 * k + 1) - 1) // 3,
                 low_log=lambda k: (2 * k + 1) * math.log(2) - math.log(3) - 1e-9,
                 c1=Fr(5455, 1000), c0=Fr(613, 1000), ylo=1,
                 c_hi=Fr(63116, 10000), c_hi0=Fr(6126, 10000), k0=15100,
                 expected=[])
# constants: j <= (k log(7/4) + log(16/15)) / log(10/9)
j1 = math.log(7 / 4) / math.log(10 / 9); j0 = math.log(16 / 15) / math.log(10 / 9)
assert j1 < 5.3116 and j0 < 0.6126 and 1 / 7 + j1 < 5.455
for n in range(1, 200001, 2):
    up = S(n) > n
    assert up == (n % 8 == 5)
    if up:
        assert 3 * S(n) + 1 == 7 * (3 * n + 1) // 4
    elif n >= 5:
        assert 10 * S(n) <= 9 * n
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
