"""Check for perm_suffix_d_s1: catalog step matches the case formulas used in results/perm_suffix_d_s1.md."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from systems import get

f = get("perm_suffix_d_s1")["step"]
N = 200000


def main():
    for n in range(1, N):
        if n % 2 == 0: want = 4 * n
        elif n % 4 == 1: want = (n + 1) // 2
        elif n % 8 == 3: want = (n + 1) // 2
        else: want = n - 3
        assert f(n) == want
    assert f(1) == 1
    x = 2
    for k in range(200):
        y = f(x); assert y == 4 * x and y % 2 == 0; x = y
    print("perm_suffix_d_s1: OK")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("perm_suffix_d_s1: FAIL", e); sys.exit(1)
