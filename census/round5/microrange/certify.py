"""Certified beyond-horizon counts for 3x+1 (Theorem R evaluated exactly). Exits 0 if every bound
was computed and is consistent (lower <= main <= upper, main = 2^m P(m+j)).

Writes data/certified.txt.
  Table 1: m in {100, 1000, 3000}, j = 1..12 (K = j + j' = 28).
  Table 2: every m in [35, 1000] with j = 4, j' = 18 (K = 22): worst relative half-width.
Run time: about 10 minutes on 6 cores (nice).
usage: python3 certify.py [quick|odd|siblings]
  quick    : Table 1 with m = 100 only, K = 24 (about 10 s)
  odd      : (added after REFEREE1) Table 1 rows for the missing j in {5, 7, 9, 11}, K = 28,
             m in {100, 1000, 3000}; writes data/certified_odd.txt (about 6 min)
  siblings : (added after REFEREE1) certificates for 3x+d, d in {-1, 5, -3, 7}, m = 1000, K = 24,
             j = 1..8, with the multiplier 3^A d^-1; checks that d = -1 reproduces d = 1 exactly
             (reflection identity); writes data/certified_siblings.txt (about 2 min)
"""
import os
import sys
import time
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from microlib import HERE, Disc, bounds_many

mode = sys.argv[1] if len(sys.argv) > 1 else 'full'
assert mode in ('full', 'quick', 'odd', 'siblings')
quick = mode == 'quick'
D = Disc()
out = []
ok = True


def rel(x, M):
    return float(Fraction(x) / M - 1)


if mode == 'siblings':
    t0 = time.time()
    params = [(1000, j, 24 - j) for j in range(1, 9)]
    base = bounds_many(params, D, 1)
    out.append('Sibling certificates (Theorem R with multiplier 3^A d^-1), m = 1000, K = j + jp = 24.')
    out.append('%4s %5s %3s %3s %12s %12s' % ('d', 'm', 'j', 'jp', 'rel_lower', 'rel_upper'))
    for dd in (1, -1, 5, -3, 7):
        res = base if dd == 1 else bounds_many(params, D, dd)
        for r, b in zip(res, base):
            M = r['main']
            ok &= r['lower'] <= M <= r['upper'] and M == r['main_direct']
            if dd == -1:   # reflection identity: the 3x-1 certificate equals the 3x+1 one exactly
                ok &= (r['lower'], r['upper']) == (b['lower'], b['upper'])
            out.append('%4d %5d %3d %3d %+12.5f %+12.5f' % (dd, r['m'], r['j'], r['jp'],
                                                           rel(r['lower'], M), rel(r['upper'], M)))
    out.append('d = -1 rows equal d = 1 rows exactly: %s' % ok)
    out.append('(%.0f s)' % (time.time() - t0))
    txt = '\n'.join(out)
    print(txt)
    with open(os.path.join(HERE, 'data', 'certified_siblings.txt'), 'w') as f:
        f.write(txt + '\n')
    sys.exit(0 if ok else 1)

Kt = 24 if quick else 28
ms = [100] if quick else [100, 1000, 3000]
js = [5, 7, 9, 11] if mode == 'odd' else [1, 2, 3, 4, 6, 8, 10, 12]
t0 = time.time()
params = [(m, j, Kt - j) for m in ms for j in js]
res = bounds_many(params, D)
out.append('Table 1. Theorem R bounds, K = j + jp = %d. rel = (bound - 2^m P(m+j)) / 2^m P(m+j).' % Kt)
out.append('%5s %3s %3s %12s %12s   %12s %12s   %s' % ('m', 'j', 'jp', 'rel_lower', 'rel_upper',
                                                   'triv_lower', 'triv_upper', 'P(m+j)/P(m)'))
for r in res:
    M = r['main']
    ok &= r['lower'] <= M <= r['upper'] and M == r['main_direct']
    pr = float(M / r['triv_hi'])
    out.append('%5d %3d %3d %+12.5f %+12.5f   %+12.4f %+12.4f   %.4f' % (
        r['m'], r['j'], r['jp'], rel(r['lower'], M), rel(r['upper'], M), rel(r['triv_lo'], M),
        rel(r['triv_hi'], M), pr))
out.append('(%.0f s)' % (time.time() - t0))

if mode == 'full':
    t0 = time.time()
    params = [(m, 4, 18) for m in range(35, 1001)]
    res = bounds_many(params, D)
    worst = []
    for r in res:
        M = r['main']
        ok &= r['lower'] <= M <= r['upper'] and M == r['main_direct']
        hw = max(-rel(r['lower'], M), rel(r['upper'], M))
        tw = max(-rel(r['triv_lo'], M), rel(r['triv_hi'], M))
        worst.append((hw, r['m'], tw))
    worst.sort(reverse=True)
    hws = sorted(w[0] for w in worst)
    out.append('')
    out.append('Table 2. every m in [35, 1000], j = 4, jp = 18 (K = 22): half-width of the certified interval')
    out.append('  median %.5f, 90%% %.5f, max %.5f (at m = %d); in-horizon sandwich half-width there %.4f'
               % (hws[len(hws) // 2], hws[int(0.9 * len(hws))], worst[0][0], worst[0][1], worst[0][2]))
    out.append('  ten worst m: ' + ', '.join('%d (%.4f)' % (m, h) for h, m, _ in worst[:10]))
    out.append('  smallest in-horizon sandwich half-width over the range: %.4f' % min(w[2] for w in worst))
    out.append('(%.0f s)' % (time.time() - t0))

txt = '\n'.join(out)
print(txt)
if mode in ('full', 'odd'):
    with open(os.path.join(HERE, 'data', 'certified.txt' if mode == 'full' else 'certified_odd.txt'), 'w') as f:
        f.write(txt + '\n')
sys.exit(0 if ok else 1)
