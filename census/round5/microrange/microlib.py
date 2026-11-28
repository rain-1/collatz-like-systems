"""Shared exact routines for the microrange lens (3x+1 Terras map, coefficient stopping time).

Everything here is exact integer / Fraction arithmetic.

Notation (README section 1):
  A_i(n)   = number of odd steps among the first i Terras steps of n
  amin(b)  = least a with 3^a >= 2^b
  F(n, b)  = [A_i(n) >= amin(i) for all 1 <= i <= b]   ("not dropped within b steps", coefficient sense)
  N(m, b)  = #{0 <= n < 2^m : F(n, b)}
  P(b)     = 2^-b #{r mod 2^b : F(r, b)}
"""
import os
import subprocess
from fractions import Fraction
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))


@lru_cache(maxsize=None)
def amin(b):
    """least a >= 0 with 3^a >= 2^b (exact)."""
    if b <= 0:
        return 0
    a = (b * 6309) // 10000          # log_3 2 = 0.63092975...
    while 3 ** a >= 2 ** b:
        a -= 1
    while 3 ** a < 2 ** b:
        a += 1
    return a


_cnt_cache = {}


def cnt(d):
    """dict A -> #{r mod 2^d : F(r, d), A_d(r) = A}. Residues mod 2^d <-> parity vectors of length d."""
    if d in _cnt_cache:
        return _cnt_cache[d]
    # incremental from the largest cached depth below d
    start = max([e for e in _cnt_cache if e <= d], default=0)
    cur = dict(_cnt_cache[start]) if start else {0: 1}
    for i in range(start + 1, d + 1):
        nxt = {}
        lo = amin(i)
        for a, c in cur.items():
            for a2 in (a, a + 1):
                if a2 >= lo:
                    nxt[a2] = nxt.get(a2, 0) + c
        cur = nxt
        if i % 50 == 0 or i == d:
            _cnt_cache[i] = dict(cur)
    _cnt_cache[d] = cur
    return cur


def survivors(b):
    """#{r mod 2^b : F(r, b)} = 2^b P(b)."""
    return sum(cnt(b).values())


def thresholds(d, A, K):
    """th_i = amin(d+i) - A, i = 1..K: the continuation x of a depth-d node with A odd steps
    survives the next K steps iff A_i(x) >= th_i for all i."""
    return [amin(d + i) - A for i in range(1, K + 1)]


class Disc:
    """Runs `disc batch` (parallel, exact) on a list of jobs; results are cached."""

    def __init__(self):
        self.exe = os.path.join(HERE, 'disc')
        if not os.path.exists(self.exe):
            subprocess.check_call(['gcc', '-O3', '-march=native', '-fopenmp', '-o', self.exe,
                                   os.path.join(HERE, 'disc.c')])
        self.cache = {}

    def run(self, keys):
        todo = sorted(set(k for k in keys if k not in self.cache), key=lambda k: -k[0])
        if todo:
            inp = ''.join('%d %d %d %s\n' % (K, jp, u, ' '.join(map(str, th))) for K, jp, u, th in todo)
            out = subprocess.run(['nice', self.exe, 'batch'], input=inp, capture_output=True, text=True,
                                 check=True).stdout.split('\n')
            for k, line in zip(todo, out):
                self.cache[k] = tuple(map(int, line.split()))
        return [self.cache[k] for k in keys]


def _jobs(m, j, jp, dd=1):
    """dd = the odd constant of the map 3x+dd. By T_dd(x) = dd T_1(x/dd) the survivor set of 3x+dd is
    dd*S, so the line u s + B meets it as often as the line (u/dd) s + B/dd meets S: the multiplier
    to scan is 3^A dd^-1 mod 2^K."""
    d, K = m - jp, j + jp
    assert d >= 0 and jp >= j and dd % 2 == 1
    Q = 1 << K
    inv = pow(dd % Q, -1, Q)
    out = []
    for A, w in sorted(cnt(d).items()):
        th = thresholds(d, A, K)
        key = None if max(th) <= 0 else (K, jp, pow(3, A, Q) * inv % Q, tuple(th))
        out.append((A, w, key))
    return out


def bounds_many(params, disc, dd=1):
    """Theorem R bounds for each (m, j, jp) in params; split depth d = m - jp, K = j + jp.
    Returns a list of dicts with exact integers / Fractions:
      lower, upper  : Sum_A Cnt_d(A) min_B Phi, Sum_A Cnt_d(A) max_B Phi   (lower <= N(m,m+j) <= upper)
      main          : Sum_A Cnt_d(A) |S|/2^j  ( = 2^m P(m+j) )
      main_direct   : survivors(m+j) / 2^j    (independent computation of 2^m P(m+j))
      triv_lo, triv_hi : the in-horizon sandwich (README, section 2)
      window        : [(A, Cnt, |S|, max, min)] for the A whose continuation can die
    """
    alljobs = [_jobs(m, j, jp, dd) for (m, j, jp) in params]
    disc.run([k for jl in alljobs for (_, _, k) in jl if k is not None])
    res = []
    for (m, j, jp), jl in zip(params, alljobs):
        K = j + jp
        lower = upper = 0
        main = Fraction(0)
        win = []
        for A, w, key in jl:
            if key is None:
                size, mx, mn = 1 << K, 1 << jp, 1 << jp
            else:
                size, mx, mn = disc.cache[key]
                win.append((A, w, size, mx, mn))
            lower += w * mn
            upper += w * mx
            main += Fraction(w * size, 1 << j)
        cm = cnt(m)
        triv_hi = sum(cm.values())
        triv_lo = sum(w for A, w in cm.items() if max(thresholds(m, A, j)) <= 0)
        res.append(dict(m=m, j=j, jp=jp, lower=lower, upper=upper, main=main,
                        main_direct=Fraction(survivors(m + j), 1 << j),
                        triv_lo=triv_lo, triv_hi=triv_hi, window=win))
    return res


def bounds(m, j, jp, disc, dd=1):
    return bounds_many([(m, j, jp)], disc, dd)[0]
