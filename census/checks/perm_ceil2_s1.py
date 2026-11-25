"""Check for perm_ceil2_s1: catalog step matches the case formulas used in results/perm_ceil2_s1.md."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from systems import get

f = get("perm_ceil2_s1")["step"]
N = 200000


def main():
    d = 2
    for n in range(1, N):
        if n % 2 == 0:
            m = n // 2
            assert f(n) == 2 * (m + (m + d - 1) // d) and f(n) > n
        elif n % 4 == 1: assert f(n) == 2 * ((d + 1) * (n // 4) + 1)
        else: assert f(n) == n // 2
    assert f(1) == 2
    x = 2
    for k in range(2000):
        y = f(x); assert y % 2 == 0 and y > x; x = y
    print("perm_ceil2_s1: OK")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("perm_ceil2_s1: FAIL", e); sys.exit(1)
