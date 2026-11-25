"""CLS-052 desc_s32_plus9: classify cycles of the odd map with one expanding run. Exit 0 iff pass."""
import sys, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
from onerun_lib import run_theorem, v

SET = {1, 3, 5, 7, 9, 11, 13, 15, 17, 21, 23, 25, 29}


def S(n):
    m = 3 * n + 1 if n % 32 in SET else n + 1
    return m >> v(m, 2)


ok = run_theorem("s32_plus9", S, lambda n: n % 2 == 1, Q=3, P=2,
                 low=lambda k: 2 ** (k + 1) - 1,
                 low_log=lambda k: (k + 1) * math.log(2) - 1e-9,
                 c1=Fr(2558, 1000), c0=Fr(1578, 1000), ylo=1,
                 c_hi=Fr(32240, 10000), c_hi0=Fr(15779, 10000), k0=17100,
                 expected=[])
j1 = math.log(3 / 2) / math.log(6 / 5); j0 = math.log(4 / 3) / math.log(6 / 5)
assert j1 < 2.2240 and j0 < 1.5779
assert 1 / 3 + 2.2240 <= 2.558 and 1 + 2.2240 <= 3.2240
for n in range(1, 200001, 2):
    up = S(n) > n
    assert up == (n % 4 == 3 and n % 32 in SET)
    if up:
        assert S(n) + 1 == 3 * (n + 1) // 2
    elif n >= 3:
        assert 6 * S(n) <= 5 * n

print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
