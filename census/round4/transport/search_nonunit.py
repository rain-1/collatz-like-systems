"""Search: induced maps of SETTLED non-unit systems that are unit-multiplier p-adic tables.

For each settled non-unit system B (Farkas pairing family P(a, K, x*) with K = 1 or
(a, K) = (3, 2), proved in round3/mixedbase/pairing_family.md P3; dressed maps, proved in
round3/accel/dressing.md Theorem K) and each class Y = rY (mod MY), compute the first-return map
R of B to Y (exact, bounded return time only), conjugate by h(z) = MY z + rY, and test whether
the canonical table of R is a unit-multiplier p-adic table.  If it is, compute its exact
trichotomy type.  A type-(c) hit is a unit-multiplier type-(c) system all of whose orbits are
subsequences of B-orbits, hence settled by transport.

usage: python3 search_nonunit.py [maxM] [out.json]
"""
import json
import os
import sys
import time
from math import gcd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from transport_lib import induced_canonical, is_unit_padic, unit_type, lcm  # noqa


def pairing_table(a, K, xs):
    """P(a, K, x*): n = r (mod m) -> (n + c)/m first; even -> n/2; odd -> (a n + b)/2."""
    m = a ** K
    r = (xs * pow(2, -1, m)) % m
    c = (m - 1) * xs // 2
    b = (2 - a) * xs
    Q = 2 * m
    t = []
    for n in range(Q):
        if n % m == r:
            t.append((1, c, m))
        elif n % 2 == 0:
            t.append((1, 0, 2))
        else:
            t.append((a, b, 2))
    return Q, t


def dressed_table(p, q, e, g):
    """D(x) = q^e x/p if p|x; x/q if q|x (and p does not); g(x) = (u x + v)/w otherwise.
    g given as (u, v, w) with w = 1 (applied on the rough classes)."""
    Q = p * q
    t = []
    for n in range(Q):
        if n % p == 0:
            t.append((q ** e, 0, p))
        elif n % q == 0:
            t.append((1, 0, q))
        else:
            t.append(g)
    return Q, t


def population():
    pop = []
    for a in (3, 5, 7, 9, 11):
        for xs in (1, -1, 3, -3, 5, -5, 7, -7):
            if gcd(a, xs) != 1:
                continue
            Q, t = pairing_table(a, 1, xs)
            pop.append(dict(id="P(%d,1,%d)" % (a, xs), Q=Q, table=t,
                            domain='Z', proof='pairing P3 (K=1)'))
    for xs in (1, -1, 5, -5):
        Q, t = pairing_table(3, 2, xs)
        pop.append(dict(id="P(3,2,%d)" % xs, Q=Q, table=t, domain='Z', proof='pairing P3 (3,2)'))
    for (p, q, e) in ((2, 3, 1), (2, 3, 2), (3, 2, 2), (2, 5, 1), (3, 5, 1), (2, 7, 1)):
        Q, t = dressed_table(p, q, e, (1, 1, 1))
        pop.append(dict(id="dress_%d%d_e%d_x1" % (p, q, e), Q=Q, table=t, domain='N+',
                        proof='dressing Theorem K, R(w) = rough(w+1) < w'))
    return pop


def moduli(maxM):
    out = []
    for i in range(0, 8):
        for j in range(0, 5):
            for k in range(0, 3):
                for l in range(0, 2):
                    M = 2 ** i * 3 ** j * 5 ** k * 7 ** l
                    if 2 <= M <= maxM:
                        out.append(M)
    return sorted(set(out))


def run(maxM=96, tmax=30, pmax=4000):
    hits = []
    stats = dict(pairs=0, bounded=0, unit=0)
    for B in population():
        for MY in moduli(maxM):
            for rY in range(MY):
                stats['pairs'] += 1
                try:
                    canon, pcs, st = induced_canonical(B['Q'], B['table'], MY, rY, tmax=tmax,
                                                       pmax=pmax, Lmax=1 << 14)
                except (AssertionError, ZeroDivisionError):
                    continue
                if st != 'ok' or canon is None:
                    continue
                stats['bounded'] += 1
                Q, rows = canon
                if Q == 1 or is_unit_padic(Q, rows) is None:
                    continue
                stats['unit'] += 1
                ty = unit_type(Q, rows)
                hits.append(dict(B=B['id'], MY=MY, rY=rY, canon=canon, type=ty['type'],
                                 tinfo={k: v for k, v in ty.items() if k != 'scc'}))
    return hits, stats


if __name__ == "__main__":
    maxM = int(sys.argv[1]) if len(sys.argv) > 1 else 96
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'results', 'nonunit_%d.json' % maxM)
    t0 = time.time()
    hits, stats = run(maxM)
    json.dump(dict(maxM=maxM, stats=stats, hits=hits), open(out, 'w'), indent=0)
    print(stats, "time %.1f" % (time.time() - t0))
    from collections import Counter
    print(Counter(h['type'] for h in hits))
    for h in hits:
        if h['type'] in ('c', 'b'):
            print(h['B'], h['MY'], h['rY'], h['type'], h['canon'][0], h['canon'][1][:8])
