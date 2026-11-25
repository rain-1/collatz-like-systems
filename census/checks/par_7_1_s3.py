"""Evidence check for par_7_1_s3 (OPEN fate): even n -> n/2; odd n -> 7n+1, seed 3.
Verifies that the first N iterates are pairwise distinct (the value at step N is a
strict record, so preperiod+period > N) and reports the bit length. This is
EVIDENCE ONLY, not a proof of divergence."""
import sys
a, d, seed, N = 7, 1, 3, 200000
n = seed; mx = seed; last = 0
for k in range(1, N + 1):
    n = n >> 1 if n % 2 == 0 else a * n + d
    if n > mx: mx, last = n, k
# a record at step 'last' means x_last differs from all earlier iterates
ok = last > N - 1000  # then preperiod + period > last
print("par_7_1_s3", "steps", N, "bits", n.bit_length(), "last record at", last, "OK" if ok else "FAIL")
# Proof part: S = {1,2,4} mod 7 (the subgroup <2> = quadratic residues) is forward-invariant.
# Check over residues mod 14 (parity and residue mod 7 both determined).
S = {1, 2, 4}
for r in range(14):
    if r % 7 not in S: continue
    for t in range(5):  # several lifts n = r + 14 t
        m = r + 14 * t
        if m == 0: continue
        img = m // 2 if m % 2 == 0 else 7 * m + 1
        assert img % 7 in S, (m, img)
# algebraic reason: odd step gives 1 mod 7; halving multiplies by 4 = 2^{-1} mod 7, and 4 in S
assert (7 * seed + 1) % 7 == 1 and seed % 7 not in S
print("mod-7 invariant: orbit of 3 after step 1 stays in {1,2,4} mod 7; 3 never recurs. OK")
sys.exit(0 if ok else 1)
