"""Check for perm_flip_s27: catalog step matches the case formulas used in results/perm_flip_s27.md."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from systems import get

f = get("perm_flip_s27")["step"]
N = 200000


def main():
    for n in range(1, N):
        assert f(n) == (n + 1 if n % 2 else n - 1)
        assert f(f(n)) == n and f(n) != n
    assert f(27) == 28 and f(28) == 27
    print("perm_flip_s27: OK")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print("perm_flip_s27: FAIL", e); sys.exit(1)
