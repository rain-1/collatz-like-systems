"""Check for perm_suffix_a_s1: catalog step matches the case formulas used in results/perm_suffix_a_s1.md."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from systems import get

f = get("perm_suffix_a_s1")["step"]
N = 200000


def main():
    for n in range(1, N):
        r = n % 4
        want = 2 * n if n % 2 == 0 else (n + 1 if r == 1 else (n - 1) // 2)
        assert f(n) == want
        if n % 2 == 0:
            assert f(n) % 2 == 0 and f(n) > n
    x = 1
    for k in range(1, 200):
        x = f(x); assert x == 2 ** k
    print("perm_suffix_a_s1: OK")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("perm_suffix_a_s1: FAIL", e); sys.exit(1)
