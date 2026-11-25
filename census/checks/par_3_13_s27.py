"""Check for par_3_13_s27: even n -> n/2, odd n -> 3n+13, seed 27.
Exact simulation until a value repeats (Floyd-free: dict of visited values).
Asserts: preperiod 24, period 5, seed not on the cycle; plus the invariant-subgroup
conjugacy used for GLOBAL: on multiples of c (c = d or a suitable factor), T(c*m) = c*U(m)."""
import sys

A, D, SEED = 3, 13, 27

def T(n):
    return n // 2 if n % 2 == 0 else A * n + D

def main():
    seen, n, i, path = {}, SEED, 0, []
    while n not in seen:
        if i > 10**6:
            print("no repeat in 1e6 steps"); return 1
        seen[n] = i; path.append(n); n = T(n); i += 1
    pre, per = seen[n], i - seen[n]
    cyc = path[pre:]
    print(f"preperiod={pre} period={per} cycle_min={min(cyc)} seed_on_cycle={SEED in cyc}")
    ok = (pre, per) == (24, 5) and SEED not in cyc
    # conjugacy identity on the invariant sublattice cZ (c = D, valid since D | A*c*m + D)
    U = (lambda m: m // 2 if m % 2 == 0 else A * m + 1)
    c = D
    ok &= all(T(c * m) == c * U(m) for m in range(1, 200001))
    print("conjugacy T(D*m)=D*U(m), U = odd->A m+1, verified m<=2e5:", ok)
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
