"""Check for perm_suffix_c_s1: catalog step matches the case formulas used in results/perm_suffix_c_s1.md."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from systems import get

f = get("perm_suffix_c_s1")["step"]
N = 200000


def main():
    for n in range(1, N):
        want = n // 2 if n % 4 == 0 else (n + 1 if n % 4 == 2 else 2 * n - 1)
        assert f(n) == want
        if n % 2 == 1 and n > 1:
            assert f(n) % 2 == 1 and f(n) > n
    assert f(1) == 1
    x = 3
    for k in range(200):
        y = f(x); assert y == 2 * x - 1 and y > x; x = y
    print("perm_suffix_c_s1: OK")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("perm_suffix_c_s1: FAIL", e); sys.exit(1)
