"""Exact checks for the repairs made after REFEREE1 (README section 9). Exits 0 iff all pass.

  1. Reflection identity Phi(-u, B) = Phi(u, B - u(N-1)) for random S (K = 6..10), and the coset
     decomposition (Z/2^K)^* = <3> u -<3> for K = 3..20 (so every coset c<3> is <3> or -<3>).
     A mutated shift B - uN must fail somewhere (shows the check can fail).
  2. Lemma M explicit form: log2 #surv(K) >= (K - 2000) h0 for every K <= 6000, where
     h0 = log2 #surv(2000)/2000, and h0 >= 0.9430 (exact: #surv(2000)^10000 >= 2^(2000*9430)).
  3. sigma versus tau (3x+1, n < 2^34): Nsig - Ntau = 1 for all m <= 34, m <= b <= m+8, except
     m = b = 1 where it is 0.
  4. Certified tables: every j in 1..12 present for m in {100, 1000, 3000} (certified.txt plus
     certified_odd.txt); max |delta| at j = 1 is <= 3.2e-5 and > 2e-5 (the old README constant was
     wrong); max |delta| at j = 12 is <= 0.0193.
  5. Sibling certificates: the d = -1 rows equal the d = 1 rows, the d = 5 rows differ from them.
  6. The j = 1 constant exactly (the tables are rounded to 5 decimals): recompute Theorem R at
     j = 1, K = 28 for m = 100, 1000, 3000 and check max |delta| <= 3.2e-5 exactly (about 1 min).
usage: python3 check_revision.py
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from microlib import HERE, survivors

fails = []


def check(c, what):
    if not c:
        fails.append(what)


# 1. reflection identity and coset decomposition
def phi(u, B, S, N, Q):
    return sum(1 for s in range(N) if (u * s + B) % Q in S)


rng = random.Random(1)
mut_broke = 0
for K in range(6, 11):
    Q = 1 << K
    for j in (1, 2, 3):
        N = 1 << (K - j)
        for _ in range(6):
            S = set(x for x in range(Q) if rng.random() < rng.choice((0.1, 0.5, 0.8)))
            for u in rng.sample(range(1, Q, 2), 4):
                for B in rng.sample(range(Q), 4):
                    check(phi(-u % Q, B, S, N, Q) == phi(u, (B - u * (N - 1)) % Q, S, N, Q),
                          ('reflect', K, j, u, B))
                    mut_broke += phi(-u % Q, B, S, N, Q) != phi(u, (B - u * N) % Q, S, N, Q)
check(mut_broke > 0, 'mutation of the reflection shift was not detected')
for K in range(3, 21):
    Q = 1 << K
    g, x = set(), 1
    while x not in g:
        g.add(x)
        x = 3 * x % Q
    neg = set((-y) % Q for y in g)
    check(len(g) == Q // 4 and not (g & neg) and len(g | neg) == Q // 2, ('coset', K))
print('1. reflection identity and (Z/2^K)^* = <3> u -<3>; mutation detected in %d cases' % mut_broke)

# 2. Lemma M explicit lower bound
s2000 = survivors(2000)
# h0 >= 0.9430  <=>  s2000 >= 2^(1886)
check(s2000 >= 1 << 1886, 'h0 < 0.9430')
# log2 #surv(K) >= (K-2000) h0  <=>  #surv(K)^2000 >= #surv(2000)^(K-2000)  (for K > 2000)
bitl = s2000.bit_length()
for K in range(2001, 6001, 1):
    sK = survivors(K)
    # cheap sufficient test first, exact test if close
    if (sK.bit_length() - 1) * 2000 >= bitl * (K - 2000):
        continue
    check(sK ** 2000 >= s2000 ** (K - 2000), ('lemmaM', K))
for K in range(1, 2001):
    check(survivors(K) >= 1, ('surv>=1', K))
print('2. Lemma M explicit bound log2 #surv(K) >= (K-2000) h0 for K <= 6000; h0 >= 0.9430')

# 3. sigma versus tau
tau, sig = {}, {}
for line in open(os.path.join(HERE, 'data', 'brute34_3x1.txt')):
    w = line.split()
    if w and w[0] in ('tau', 'sig'):
        (tau if w[0] == 'tau' else sig)[int(w[1])] = list(map(int, w[2:]))
for m in range(1, 35):
    for b in range(m, m + 9):
        diff = sig[m][b] - tau[m][b]
        check(diff == (0 if m == b == 1 else 1), ('sigma', m, b, diff))
print('3. Nsig - Ntau = 1 for m <= 34, m <= b <= m+8, except m = b = 1 (0)')


# 4. certified tables
def rows(fn):
    out = {}
    for line in open(os.path.join(HERE, 'data', fn)):
        w = line.split()
        if len(w) == 8 and w[0].isdigit():
            out[(int(w[0]), int(w[1]))] = (float(w[3]), float(w[4]))
        if line.startswith('Table 2'):
            break
    return out


T = rows('certified.txt')
T.update(rows('certified_odd.txt'))
for m in (100, 1000, 3000):
    for j in range(1, 13):
        check((m, j) in T, ('missing', m, j))
d1 = max(max(-T[m, 1][0], T[m, 1][1]) for m in (100, 1000, 3000))
d12 = max(max(-T[m, 12][0], T[m, 12][1]) for m in (100, 1000, 3000))
check(2e-5 < d1 <= 3.2e-5, ('j=1 constant', d1))
check(d12 <= 0.0193, ('j=12 constant', d12))
allhw = max(max(-a, b) for a, b in T.values())
print('4. all j = 1..12 certified at m = 100, 1000, 3000; max|delta| j=1: %.2e, j=12: %.4f, overall %.4f'
      % (d1, d12, allhw))

# 5. siblings
sib = {}
for line in open(os.path.join(HERE, 'data', 'certified_siblings.txt')):
    w = line.split()
    if len(w) == 6 and w[0].lstrip('-').isdigit():
        sib[(int(w[0]), int(w[2]))] = (w[4], w[5])
for j in range(1, 9):
    check(sib[(-1, j)] == sib[(1, j)], ('sib -1', j))
check(any(sib[(5, j)] != sib[(1, j)] for j in range(1, 9)), 'd = 5 certificate equals d = 1 (unexpected)')
print('5. sibling certificates: d = -1 equals d = 1; d = 5 differs')

# 6. exact j = 1 constant
from fractions import Fraction
from microlib import Disc, bounds_many
ex = []
for r in bounds_many([(m, 1, 27) for m in (100, 1000, 3000)], Disc()):
    M = r['main']
    hw = max(1 - Fraction(r['lower']) / M, Fraction(r['upper']) / M - 1)
    ex.append(hw)
    check(hw <= Fraction(32, 10 ** 6), ('exact j=1', r['m'], float(hw)))
check(max(ex) > Fraction(2, 10 ** 5), 'exact j=1 constant unexpectedly <= 2e-5')
print('6. exact j = 1 half-widths at m = 100, 1000, 3000: ' + ', '.join('%.3e' % float(h) for h in ex))

if fails:
    print('FAIL', fails[:10])
    sys.exit(1)
print('all checks passed')
