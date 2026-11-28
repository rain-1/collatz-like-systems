"""All-m bound at K = 16 (added after REFEREE2, item N2). Exits 0 iff the quoted constants are reproduced.

By Theorem R and Lemma P, for every m >= K - j + 1 (split depth j' = K - j, d = m - j' >= 1) the relative
error |N(2^m, m+j)/2^mP(m+j) - 1| is at most max_k r(3^{A_k} mod 2^K, pattern_k(m)). Every multiplier lies
in <3> mod 2^K (a = 0 .. 2^(K-2)-1) and every pattern is one of the slot patterns of Lemma P, so the
maximum of r over all of them bounds the error for every such m. r is computed exactly (integers from
`disc allu`, ratio as a Fraction); the slot patterns are enumerated as in `analytic.py` (the breakpoints
are floats, but their minimum gap is 0.047, far above the 1e-9 tolerance, and the thresholds themselves
are exact integers from amin). About 3 minutes.
"""
import math
import os
import subprocess
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from microlib import HERE, amin

LAM = math.log(2) / math.log(3)
K = 16
EXPECTED = {1: Fraction(129, 1057), 2: Fraction(213, 749), 3: Fraction(349, 749)}

bps = sorted(set([0.0, 1.0] + [1 - (i * LAM - math.floor(i * LAM)) for i in range(1, K + 1)]))
gap = min(b - a for a, b in zip(bps, bps[1:]))
pats = []
for lo, hi in zip(bps, bps[1:]):
    d = next(d for d in range(1, 10 ** 6) if lo + 1e-9 < d * LAM - math.floor(d * LAM) < hi - 1e-9)
    for k in range(0, K + 2):
        A = amin(d) + k
        th = [amin(d + i) - A for i in range(1, K + 1)]
        if max(th) > 0:
            pats.append(tuple(th))
print('K = %d: %d breakpoint intervals (min width %.4f), %d nontrivial slot patterns'
      % (K, len(bps) - 1, gap, len(pats)))

fails = 0
for j in (1, 2, 3):
    jp = K - j
    worst = Fraction(0)
    for th in pats:
        out = subprocess.run(['nice', os.path.join(HERE, 'disc'), 'allu', str(K), str(jp)] + list(map(str, th)),
                             capture_output=True, text=True, check=True).stdout.split('\n')
        size = int(out[0].split()[1])
        for line in out[1:]:
            if not line:
                continue
            _, mx, mn = map(int, line.split())
            worst = max(worst, Fraction(max(mx * (1 << j) - size, size - mn * (1 << j)), size))
    ok = worst == EXPECTED[j]
    fails += not ok
    print('j = %d: for every m >= %d, |N(2^m, m+j)/2^mP(m+j) - 1| <= %s = %.6f  %s'
          % (j, K - j + 1, worst, float(worst), 'ok' if ok else 'FAIL (expected %s)' % EXPECTED[j]))
sys.exit(1 if fails else 0)
