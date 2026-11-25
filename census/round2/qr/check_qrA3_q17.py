"""qrA3_q17: finite ingredients of the non-periodicity theorem, plus (non-proof) evidence
that the basin is not 2- or 3-automatic (kernel growth on a finite window)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qrlib import famA, cycles_in, basin_table, subgroup

q = 17
T = famA(q, 3)
ok = all(1 <= T(n) <= q for n in range(1, q + 1))
cyc = cycles_in(T, range(1, q + 1))
cid = basin_table(T, cyc)
ok &= sorted(sorted(c) for c in cyc) == [[1, 3, 6], [5, 10, 13], [17]]
ok &= subgroup([2, 3], q) == set(range(1, q))          # <2,3> = (Z/17)^*: one unit coset
ok &= all(T(n) == (n + 17 * (n % 3)) // 3 for n in range(1, 3000, 2))   # c = n mod 3

N = 1 << 20
B = bytearray(N + 1)
for n in range(1, N + 1):
    if n <= q:
        x = n
        while x not in cid: x = T(x)
        B[n] = cid[x]
    else:
        x = T(n)
        while x >= n: x = T(x)
        B[n] = B[x]
ok &= B[1] == 1 and B[5] == 5 and B[17] == 17
# identities used in the proof: basin(2n) = basin(n), basin(3n) = basin(n) for odd n
ok &= all(B[2 * n] == B[n] for n in range(1, N // 2))
ok &= all(B[3 * n] == B[n] for n in range(1, N // 3, 2))
# evidence only: k-kernel growth on window W
W = 256
for k, E in [(2, 9), (3, 6)]:
    sizes = []
    for e in range(E):
        if k ** e * W > N: break
        sizes.append(len({bytes(B[k ** e * n + r] for n in range(1, W)) for r in range(k ** e)}))
    print(f"base {k}: distinct kernel sequences at level e:", sizes)
print("qrA3_q17", "OK" if ok else "FAILED")
sys.exit(0 if ok else 1)
