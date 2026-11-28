"""Transport equivalence classes (union-find over exact induced-map identities).

Two systems A, B are joined when there are classes X (for A) and Y (for B) such that
  * the first-return maps R_A^X, R_B^Y have bounded return time (exact piece computation),
  * h_X^{-1} R_A^X h_X and h_Y^{-1} R_B^Y h_Y have the same canonical table (an exact identity),
  * X is sufficient for A and Y is sufficient for B (transport_lib.sufficient).
By Theorem E (README / transport_theorems.md) GLOBAL(A) <=> GLOBAL(B) up to the boundary point
z = 0, which check_transport.py examines for every reported join.

usage: python3 equiv.py POP OUT.json      POP in {lib, sfam4, sfam5}
"""
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from transport_lib import induced_canonical, table_canonical, sufficient, scc_type  # noqa
from library import build, s_table  # noqa

FULL = [(1, 0)] + [(M, r) for M in (2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 16, 18, 24, 27, 32)
                   for r in range(M)]
LIGHT = [(1, 0), (2, 1), (3, 1), (3, 2), (6, 1), (6, 2), (6, 4), (6, 5), (9, 2), (9, 4),
         (9, 8), (9, 5), (9, 7), (9, 1)] + [(4, r) for r in range(4)] + [(8, r) for r in range(8)]


def population(kind):
    pop = [dict(s) for s in build()]
    if kind in ('sfam4', 'sfam5'):
        ms = (4,) if kind == 'sfam4' else (4, 5)
        for m in ms:
            for mask in range(1, 2 ** (2 ** (m - 1))):
                S = tuple(2 * i + 1 for i in range(2 ** (m - 1)) if mask >> i & 1)
                pop.append(dict(id="sf%d_%s" % (m, "-".join(map(str, S))), Q=2 ** m,
                                table=s_table(m, S), status='family', p=2))
    return pop


class UF:
    def __init__(self):
        self.p = {}

    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        self.p[self.find(a)] = self.find(b)


def run(kind, classes):
    pop = population(kind)
    # dedupe identical maps (same canonical table)
    canon_of, rep = {}, {}
    for s in pop:
        c = json.dumps(table_canonical(s['Q'], s['table']))
        if c in rep:
            canon_of[s['id']] = rep[c]
        else:
            rep[c] = s['id']
            canon_of[s['id']] = s['id']
    uniq = [s for s in pop if canon_of[s['id']] == s['id']]
    H = {}
    for s in uniq:
        Q, t = s['Q'], s['table']
        cl = classes if s['status'] == 'family' else FULL
        for (MX, rX) in cl:
            if MX == 1:
                canon = table_canonical(Q, t)
            else:
                try:
                    canon, pcs, st = induced_canonical(Q, t, MX, rX, tmax=24, pmax=20000, Lmax=4096)
                except AssertionError:
                    continue
                if st != 'ok' or canon is None:
                    continue
            ok, _ = sufficient(Q, t, MX, rX, allow_contracting=True) if MX > 1 else (True, None)
            H.setdefault(json.dumps(canon), []).append((s['id'], MX, rX, ok))
    uf = UF()
    joins = []
    implications = set()
    for key, lst in H.items():
        for a in lst:
            for b in lst:
                if a[0] != b[0] and b[3]:
                    implications.add((a[0], b[0]))     # GLOBAL(a) => GLOBAL(b)
        lst = [x for x in lst if x[3]]
        ids = sorted(set(x[0] for x in lst))
        for i in ids[1:]:
            if uf.find(i) != uf.find(ids[0]):
                joins.append(dict(canon=json.loads(key), members=lst))
            uf.union(i, ids[0])
    classes_out = {}
    for s in uniq:
        classes_out.setdefault(uf.find(s['id']), []).append(s['id'])
    st = {s['id']: s['status'] for s in pop}
    multi = [sorted(v) for v in classes_out.values() if len(v) > 1]
    return dict(population=kind, nsystems=len(pop), nunique=len(uniq),
                duplicates={k: v for k, v in canon_of.items() if k != v},
                classes=multi,
                implications=sorted(i for i in implications if (i[1], i[0]) not in implications
                                    and uf.find(i[0]) != uf.find(i[1])),
                statuses={i: st[i] for c in multi for i in c}, joins=joins)


if __name__ == "__main__":
    kind = sys.argv[1] if len(sys.argv) > 1 else 'lib'
    out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'results', 'equiv_%s.json' % kind)
    t0 = time.time()
    res = run(kind, FULL if kind != 'sfam5' else LIGHT)
    res['seconds'] = round(time.time() - t0, 1)
    json.dump(res, open(out, 'w'), indent=0)
    print(kind, "systems", res['nsystems'], "unique", res['nunique'], "classes",
          len(res['classes']), "time", res['seconds'])
    for c in res['classes']:
        print(len(c), [(i, res['statuses'][i]) for i in c[:8]])
    print("one-way implications GLOBAL(A) => GLOBAL(B):", len(res['implications']))
    for a, b in res['implications'][:40]:
        print("  ", a, "=>", b)
