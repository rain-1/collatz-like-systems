"""Check for par_5_3_s27 (even n -> n/2, odd n -> 5n+3, seed 27). FATE is OPEN.
Verified: 3Z is invariant and T(3m) = 3*U(m) with U the 5x+1 map; 27 = 3*9, and the
5x+1 orbit of 7 passes through 9 (7->36->18->9). Hence the T-orbit of 27 is 3 * (U-orbit of 9).
Also checks: T(n) mod 3 != 0 whenever n mod 3 != 0 (complement of 3Z invariant too)."""
import sys

def T(n):
    return n // 2 if n % 2 == 0 else 5 * n + 3

def U(m):
    return m // 2 if m % 2 == 0 else 5 * m + 1

def main():
    ok = all(T(3 * m) == 3 * U(m) for m in range(1, 200001))
    ok &= all(T(n) % 3 != 0 for n in range(1, 200001) if n % 3)
    n, m = 27, 9
    for _ in range(20000):
        ok &= (n == 3 * m)
        n, m = T(n), U(m)
    ok &= [7, U(7), U(U(7)), U(U(U(7)))] == [7, 36, 18, 9]
    print("conjugacy + orbit correspondence over 20000 steps:", ok)
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
