"""Evidence check for par_5_11_s27 (OPEN fate): even n -> n/2; odd n -> 5n+11, seed 27.
Verifies that the first N iterates are pairwise distinct (the value at step N is a
strict record, so preperiod+period > N) and reports the bit length. This is
EVIDENCE ONLY, not a proof of divergence."""
import sys
a, d, seed, N = 5, 11, 27, 200000
n = seed; mx = seed; last = 0
for k in range(1, N + 1):
    n = n >> 1 if n % 2 == 0 else a * n + d
    if n > mx: mx, last = n, k
# a record at step 'last' means x_last differs from all earlier iterates
ok = last > N - 1000  # then preperiod + period > last
print("par_5_11_s27", "steps", N, "bits", n.bit_length(), "last record at", last, "OK" if ok else "FAIL")
sys.exit(0 if ok else 1)
