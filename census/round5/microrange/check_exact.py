"""Exact checks for Theorem R (the uniform-in-intercept reduction). Exits 0 only if every check passes.

  1. disc (fast: digit-tree build + sliding window) equals the naive definition on random jobs,
     including multipliers that are not powers of 3.
  2. Terras' identity T^d(r + 2^d s) = 3^{A_d(r)} s + T^d(r) and equal parity vectors, for 3x+1, 3x-1, 3x+5.
  3. The conjugacy T_dd(x) = dd T_1(x/dd): parity vectors of x under 3x+dd equal those of x/dd under
     3x+1 (mod 2^K), so the survivor set of 3x+dd is dd*S.
  4. In-horizon identity N(m, b) = 2^(m-b) #surv(b) for b <= m against brute force (n < 2^34, 3x+1).
  5. Theorem R against brute force: lower <= N(m, m+j) <= upper and main == 2^m P(m+j) computed
     independently, for 3x+1 (m <= 34), 3x-1 and 3x+5 (m <= 32), j = 1..8, several split depths.
     Also records how much tighter the bound is than the in-horizon sandwich.

Brute-force data: data/brute34_3x1.txt (./brute 34), data/brute32_3xm1.txt (./brute 32 -1),
data/brute32_3xp5.txt (./brute 32 5); regenerated here if missing (about 1 minute).
"""
import os
import random
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from microlib import HERE, amin, cnt, survivors, thresholds, Disc, bounds_many

fails = 0


def check(cond, msg):
    global fails
    if not cond:
        fails += 1
        print('FAIL', msg)


def T(x, dd):
    return (3 * x + dd) // 2 if x & 1 else x // 2


def pv(x, k, dd):
    out = []
    for _ in range(k):
        out.append(x & 1)
        x = T(x, dd)
    return out, x


random.seed(20261127)
D = Disc()

# 1. fast == naive
keys = []
for t in range(60):
    K = random.randint(3, 13)
    jp = random.randint(1, K)
    d = random.randint(0, 400)
    A = amin(d) + random.randint(0, K)
    th = thresholds(d, A, K)
    u = pow(3, A, 1 << K) if t % 2 else random.randrange(1, 1 << K, 2)
    keys.append((K, jp, u, tuple(th)))
res = D.run(keys)
for k, r in zip(keys, res):
    K, jp, u, th = k
    out = subprocess.run([os.path.join(HERE, 'disc'), 'naive', str(K), str(jp), str(u)] + list(map(str, th)),
                         capture_output=True, text=True, check=True).stdout
    check(tuple(map(int, out.split())) == r, ('naive', k, out, r))
print('1. disc fast == naive on %d jobs' % len(keys))

# 2. Terras identity
for dd in (1, -1, 5):
    for _ in range(300):
        d = random.randint(0, 60)
        r = random.randrange(0, 1 << d) if d else 0
        s = random.randrange(0, 1 << random.randint(0, 80))
        p1, Tr = pv(r, d, dd)
        p2, Tn = pv(r + (s << d), d, dd)
        A = sum(p1)
        check(p1 == p2 and Tn == 3 ** A * s + Tr, ('terras', dd, d, r, s))
print('2. Terras identity ok for 3x+1, 3x-1, 3x+5')

# 3. conjugacy of parity vectors mod 2^K
for dd in (-1, 5, 7, -3):
    for K in (5, 9, 12):
        Q = 1 << K
        inv = pow(dd % Q, -1, Q)
        for x in random.sample(range(Q), min(200, Q)):
            check(pv(x, K, dd)[0] == pv(x * inv % Q, K, 1)[0], ('conj', dd, K, x))
print('3. parity vectors of 3x+dd at x = parity vectors of 3x+1 at x/dd')


def load(fn, M, dd):
    path = os.path.join(HERE, 'data', fn)
    if not os.path.exists(path):
        exe = os.path.join(HERE, 'brute')
        if not os.path.exists(exe):
            subprocess.check_call(['gcc', '-O3', '-march=native', '-fopenmp', '-o', exe, os.path.join(HERE, 'brute.c')])
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            subprocess.check_call(['nice', exe, str(M), str(dd)], stdout=f)
    B = {}
    for line in open(path):
        p = line.split()
        if p[0] == 'tau':
            B[int(p[1])] = list(map(int, p[2:]))
    return B


# 4. in-horizon identity
B1 = load('brute34_3x1.txt', 34, 1)
for m in range(1, 35):
    for b in range(1, m + 1):
        check(B1[m][b] == survivors(b) << (m - b), ('inhorizon', m, b))
print('4. in-horizon identity N(m,b) = 2^(m-b) #surv(b), all b <= m <= 34')

# 5. Theorem R against brute force
gains = []
for fn, M, dd in (('brute34_3x1.txt', 34, 1), ('brute32_3xm1.txt', 32, -1), ('brute32_3xp5.txt', 32, 5)):
    Bd = load(fn, M, dd)
    params = [(m, j, jp) for m in range(16, M + 1) for j in range(1, 9)
              for jp in (j + 2, j + 6, j + 10, j + 14) if jp <= m and j + jp <= 22]
    allr = bounds_many(params, D, dd)
    for r in allr:
        m, j = r['m'], r['j']
        N = Bd[m][m + j]
        check(r['main'] == r['main_direct'], ('main', dd, m, j, r['jp']))
        check(r['lower'] <= N <= r['upper'], ('bound', dd, m, j, r['jp'], r['lower'], N, r['upper']))
        check(r['triv_lo'] <= N <= r['triv_hi'], ('triv', dd, m, j))
        gains.append((r['upper'] - r['lower']) / max(1, r['triv_hi'] - r['triv_lo']))
    print('5. 3x%+d: %d cases (m <= %d, j <= 8): lower <= N(m,m+j) <= upper, main = 2^m P(m+j)'
          % (dd, len(allr), M))
gains.sort()
print('   width of the Theorem R interval / width of the in-horizon sandwich: median %.4f, max %.4f'
      % (float(gains[len(gains) // 2]), float(gains[-1])))

if fails:
    print('%d FAILURES' % fails)
    sys.exit(1)
print('all checks passed')
