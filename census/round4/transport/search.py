"""Transport searcher: hash-join of canonical induced maps.

For every system T in the population and every class X = rX (mod MX) from a fixed family,
compute the first-return map of T to X (exact pieces, bounded return time only), conjugate it
by h(z) = MX z + rX and reduce to canonical table form.  Two (system, X) pairs with the same
canonical form are related by an exact identity

    h_A^{-1} o R_A^X o h_A  =  h_B^{-1} o R_B^Y o h_B      (as maps on Z),

which is a transport of orbits from A on X to B on Y.  Output: JSON with all collisions
between different systems.  EVIDENCE-level tool; every reported identity is re-proved in
check_transport.py.

usage: python3 search.py [population] [out.json]
   population: lib (library only), sfam4 (library + S-family m=4), rand (library + random)
"""
import json
import random
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from transport_lib import induced_canonical, table_canonical, check_table  # noqa
from library import build, s_table, unit_prime  # noqa

CLASSES = [(1, 0)] + [(M, r) for M in (2, 3, 4, 6, 8, 9, 12, 16, 18, 27, 5, 10) for r in range(M)]


def population(kind, seed=1, nrand=2000):
    pop = [dict(s) for s in build()]
    if kind in ('sfam4', 'rand'):
        for mask in range(1, 256):
            S = tuple(2 * i + 1 for i in range(8) if mask >> i & 1)
            pop.append(dict(id="sf4_" + "-".join(map(str, S)), Q=16, table=s_table(4, S),
                            status='random', p=2))
    if kind == 'rand':
        rng = random.Random(seed)
        menu = [(3, 1, 1), (1, 1, 1), (3, 1, 2), (1, 1, 2), (3, -1, 2), (1, -1, 2), (5, 1, 2),
                (5, -1, 2), (3, 1, 4), (3, -1, 4), (1, 3, 4), (1, -1, 4), (1, 1, 4), (5, 3, 4),
                (5, -3, 4), (7, 1, 4), (7, -1, 4), (1, 3, 1), (3, 3, 2), (9, 1, 4)]
        seen = set()
        while len(seen) < nrand:
            m = rng.choice((2, 3))
            Q = 2 ** m
            t = []
            for r in range(Q):
                if r % 2 == 0:
                    t.append((1, 0, 2))
                    continue
                ok = [x for x in menu if (x[0] * r + x[1]) % x[2] == 0 and
                      (x[0] * Q) % x[2] == 0 and (x[0] * r + x[1]) // x[2] >= 1 or
                      ((x[0] * r + x[1]) % x[2] == 0 and (x[0] * Q) % x[2] == 0 and r == 1
                       and (x[0] + x[1]) // x[2] >= 1)]
                ok = [x for x in ok if (x[0] * (r if r > 0 else Q) + x[1]) // x[2] >= 1]
                t.append(rng.choice(ok))
            key = (Q, tuple(t))
            if key in seen:
                continue
            seen.add(key)
            pop.append(dict(id="rnd_%d" % len(seen), Q=Q, table=t, status='random', p=2))
    return pop


def run(pop, tmax=24, pmax=20000, Lmax=4096, log=None):
    H = {}
    for s in pop:
        Q, t = s['Q'], s['table']
        for (MX, rX) in CLASSES:
            if MX == 1:
                canon, st = table_canonical(Q, t), 'ok'
            else:
                try:
                    canon, pcs, st = induced_canonical(Q, t, MX, rX, tmax=tmax, pmax=pmax,
                                                       Lmax=Lmax)
                except AssertionError:
                    continue
            if st != 'ok' or canon is None:
                continue
            key = json.dumps(canon)
            H.setdefault(key, []).append((s['id'], MX, rX, s['status']))
    hits = []
    for key, lst in H.items():
        ids = set(x[0] for x in lst)
        if len(ids) >= 2:
            hits.append(dict(canon=json.loads(key), members=lst))
    return hits


if __name__ == "__main__":
    kind = sys.argv[1] if len(sys.argv) > 1 else 'lib'
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'results', 'search_%s.json' % kind)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    t0 = time.time()
    pop = population(kind)
    hits = run(pop)
    json.dump(dict(population=kind, nsystems=len(pop), nclasses=len(CLASSES), hits=hits),
              open(out, 'w'), indent=0)
    print("systems", len(pop), "hits", len(hits), "time %.1f s" % (time.time() - t0))
