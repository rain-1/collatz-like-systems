"""Finite checks accompanying the all-base nonautomaticity proof."""
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
# identities used in the proof: basin(2n) = basin(n), basin(3n) = basin(n) for all n
ok &= all(B[2 * n] == B[n] for n in range(1, N // 2))
ok &= all(B[3 * n] == B[n] for n in range(1, N // 3 + 1))
# Check both inverse branches and the reverse lap at each unit cycle.
for y in range(19, 2000, 2):
    ok &= T(3 * y) == T(3 * y - 34) == y
    for c in (1, 5):
        x = c + 18 * (y - c)
        ok &= T(T(T(x))) == y

# Sample every residue of these moduli, including powers of 17 and mixed moduli.
for modulus in (1, 17, 34, 51, 72, 175, 289, 2**4 * 3**2 * 17):
    for r in range(modulus):
        if modulus % 17 or r % 17:
            labels = B[r + modulus::modulus]
            ok &= 1 in labels and 5 in labels

# Walk every word of length 4 through the explicit section construction.
for k, p in ((2, 3), (3, 2), (6, 2), (7, 2), (17, 2), (34, 2)):
    word_modulus = p**4
    D = k
    while D <= 2 * word_modulus:
        D *= k
    for d in range(word_modulus):
        r = (-D * d) % word_modulus
        if r % 17 == 0:
            r += word_modulus
        for j in range(5):
            scale = p**j
            prefix = d % scale
            offset, remainder = divmod(D * prefix + r, scale)
            ok &= remainder == 0 and 0 <= offset < D
            ok &= D % 17 != 0 or offset % 17 != 0
            for n in (1, 2, 5):
                ok &= B[D * (scale * n + prefix) + r] == B[D * n + offset]
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
