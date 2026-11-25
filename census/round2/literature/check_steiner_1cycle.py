"""check_steiner_1cycle: 1-cycles of T(n) = n/2, (3n+1)/2.
A 1-cycle with k odd steps and l even steps exists iff d = 2^(k+l) - 3^k > 0 and
d | 2^l - 1 (proof in steiner_1cycle.md); it then has minimum n = 2^k (2^l-1)/d - 1.
(i) exact scan of every k <= 10000 (l is forced): only (k,l) = (1,1) survives;
(ii) Rhin-bound arithmetic: (k-1) log 2 < 13.3 log(2k) fails for all k > 103, and the
     scan covers far beyond; (iii) brute force: every T-cycle with all elements <= 10^6
     having one local minimum is found by direct search, and it is only {1,2}."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from systems import get
T = get("steiner_1cycle")["step"]
KMAX = 10000
found = []
p3 = 1
for k in range(1, KMAX + 1):
    p3 *= 3
    l = p3.bit_length() - k            # least l with 2^(k+l) > 3^k
    if l < 1:
        continue
    d = (1 << (k + l)) - p3
    assert d > 0
    # any larger l gives d >= 2^(k+l) - 3^k with 2^(k+l) - 2^l growing past 3^k; check l, l+1
    for L in (l, l + 1):
        dd = (1 << (k + L)) - p3
        if dd < (1 << L) and ((1 << L) - 1) % dd == 0:
            found.append((k, L, (1 << k) * (((1 << L) - 1) // dd) - 1))
assert found == [(1, 1, 1)], found
B = max(k for k in range(1, 5000) if (k - 1) * math.log(2) < 13.3 * math.log(2 * k))
assert B == 103 and B < KMAX
# (iii) direct search of small cycles
seen_min = set()
for n in range(1, 10**6 + 1, 2):
    x, mx, steps = n, n, 0
    while True:
        x = T(x); steps += 1
        if x <= n or x > 10**12 or steps > 10**4:
            break
    if x == n:
        seen_min.add(n)
assert seen_min == {1}, seen_min
print("steiner_1cycle OK: only (k,l)=(1,1) for k <=", KMAX, "; Rhin cutoff k <=", B)
