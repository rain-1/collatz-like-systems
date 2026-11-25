"""Check for perm_suffix_b_s8: catalog step matches the case formulas used in results/perm_suffix_b_s8.md."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from systems import get

f = get("perm_suffix_b_s8")["step"]
N = 200000


def main():
    for n in range(1, N):
        if n % 2 == 1:
            assert f(n) == 8 * n + 4 and f(f(n)) == 2 * n + 1
        elif n % 8 == 4: assert f(n) == (n - 4) // 4 + 1
        elif n % 4 == 2: assert f(n) == n
        elif n % 16 == 0: assert f(n) == n // 2
        else: assert n % 16 == 8 and f(n) == n - 4
    assert f(8) == 4 and f(4) == 1
    x = 1
    for k in range(1, 200):
        y = f(x); assert y == 8 * x + 4
        x = f(y); assert x == 2 ** (k + 1) - 1
    print("perm_suffix_b_s8: OK")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("perm_suffix_b_s8: FAIL", e); sys.exit(1)
