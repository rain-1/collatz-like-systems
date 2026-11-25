"""Check for par_5_5_s27 (even n -> n/2, odd n -> 5n+5, seed 27). FATE is OPEN.
Verified: T(5m) = 5*U(m) (U = 5x+1 map); T(odd n) = 5(n+1) is in 5Z, so every orbit enters 5Z
at its first odd step and stays. 27 -> 140 = 5*28, and U: 28 -> 14 -> 7, so the T-orbit of 27
from step 1 on is 5 * (U-orbit of 28), which merges with the U-orbit of 7 (and of 9)."""
import sys

def T(n):
    return n // 2 if n % 2 == 0 else 5 * n + 5

def U(m):
    return m // 2 if m % 2 == 0 else 5 * m + 1

def main():
    ok = all(T(5 * m) == 5 * U(m) for m in range(1, 200001))
    ok &= all(T(n) % 5 == 0 for n in range(1, 200001, 2))
    ok &= T(27) == 140 and U(28) == 14 and U(14) == 7
    n, m = 140, 28
    for _ in range(20000):
        ok &= (n == 5 * m)
        n, m = T(n), U(m)
    print("conjugacy + orbit correspondence over 20000 steps:", ok)
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
