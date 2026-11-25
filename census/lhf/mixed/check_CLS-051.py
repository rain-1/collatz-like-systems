"""CLS-051 desc_m3_4n5: the only cycle with one expanding run is {16,23} (T-cycle 16,69,23,48). Exit 0 iff pass."""
import sys, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as Fr
from onerun_lib import run_theorem, v


def S(n):                       # map on non-multiples of 3
    m = 4 * n + 5 if n % 3 == 1 else 2 * n + 2
    return m // 3 ** v(m, 3)


ok = run_theorem("m3_4n5", S, lambda n: n % 3 != 0, Q=2, P=3,
                 low=lambda k: max(4, 3 ** k - 5),
                 low_log=lambda k: k * math.log(3) - 1e-6,  # log(3^k - 5) for k >= 50
                 c1=Fr(32225, 10000), c0=Fr(5561, 1000), ylo=2,
                 c_hi=Fr(51558, 10000), c_hi0=Fr(8897, 1000), k0=10800,
                 expected=[(16, 1)])
j1 = math.log(4 / 3) / math.log(6 / 5); j0 = math.log(9 / 4) / math.log(6 / 5)
assert j1 < 1.5779 and j0 < 4.448
assert 1.25 * (1 + 1.5779) <= 3.2225 and 1.25 * 4.448 <= 5.561
assert 2 * (1 + 1.5779) <= 5.1558 and 2 * 4.448 <= 8.897
for n in range(1, 300001):
    if n % 3 == 0:
        continue
    up = S(n) > n
    assert up == (n % 3 == 1 and (4 * n + 5) % 9 != 0)
    if up:
        assert S(n) + 5 == 4 * (n + 5) // 3
    elif n >= 4:
        assert 6 * S(n) <= 5 * n
    else:
        assert S(n) <= n
print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
