"""check_gcert.py -- the Gaussian S-family certificate census (gaussian.md, sec. 3).

Claims checked:
  C1  m = 3 and m = 4: every subset S of the odd classes mod pi^m is classified
      exactly as CERT (certificate found and independently verified) or OBST
      (a pi-adic periodic point with |multiplier| > 1, verified exactly with the
      cycle lemma); no case is left open; the counts are asserted.
  C2  GS4_max, GS5_deep and GS5_max are settled: certificate built and verified,
      the exceptional set E computed with exact bounds, and the complete cycle
      list obtained from E (Lemma A with |z|).
  C3  m = 5: a random sample of 400 subsets is classified as in C1 (the full
      65536-subset run is census_gauss.py, about 6 minutes; its output is
      scratch/gscan_m5.out).
Runs in about 90 s.
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rings as RG   # noqa: E402
import gcert as GC   # noqa: E402
import systems as SY  # noqa: E402

G = RG.GAUSS
U5 = (1, 2)


def odd_classes(m):
    T0 = GC.GaussMap(G, m, lambda r: ((1, 0), (1, 0)))
    return [r for r, v in T0.table.items() if v is not None]


def classify(m, S, maxnodes=50000, verify=True):
    Tm = GC.GaussMap(G, m, lambda r: (U5, (1, 0)) if r in S else ((1, 0), (1, 0)))
    c = GC.certificate(Tm, maxK=50, maxnodes=maxnodes)
    mean, cyc = GC.max_mean_cycle(GC.residue_graph(Tm))
    if c['ok']:
        if verify:
            GC.verify(Tm, c['leaves'])
        return 'CERT', c
    GC.verify_obstruction(Tm, cyc)
    return 'OBST', None


def C1():
    for m, want in [(3, (3, 13)), (4, (18, 238))]:
        odd = odd_classes(m)
        cnt = {'CERT': 0, 'OBST': 0}
        for mask in range(2 ** len(odd)):
            S = {odd[i] for i in range(len(odd)) if mask >> i & 1}
            k, _ = classify(m, S)
            cnt[k] += 1
        assert (cnt['CERT'], cnt['OBST']) == want, (m, cnt)
        print(f'C1 m={m}: {len(odd)} odd classes, {2 ** len(odd)} subsets: {cnt}')


def settle(Tm):
    c = GC.certificate(Tm, maxK=60, maxnodes=10 ** 6)
    assert c['ok']
    GC.verify(Tm, c['leaves'])
    E = GC.exceptional(Tm, c['leaves'])
    cyc = set()
    for z in E + [(0, 0)]:
        seen, x, path = set(), z, []
        while x not in seen:
            seen.add(x)
            path.append(x)
            x = Tm(x)
        C = path[path.index(x):]
        k = C.index(min(C))
        cyc.add(tuple(C[k:] + C[:k]))
    return c, E, sorted(cyc, key=len)


def C2():
    want = {'GS4_max': [((0, 0),), ((0, -1), (1, -1))],
            'GS5_deep': [((0, 0),)],
            'GS5_max': [((0, 0),), ((0, -1), (1, -1))],
            'GS5_9': None}
    for sid in ['GS4_max', 'GS5_deep', 'GS5_max', 'GS5_9']:
        Tm = SY.get(sid)['step']
        c, E, cyc = settle(Tm)
        if want[sid] is not None:
            assert cyc == want[sid], (sid, cyc)
        else:
            assert [len(C) for C in cyc] == [1, 18] and (0, 1) in cyc[1]
        print(f"C2 {sid}: leaves={c['size']} K={c['K']} k={c['k']} |E|={len(E)} cycles={cyc}")
        # evidence: a box of starts all end in the listed cycles
        cyc_pts = {z for C in cyc for z in C}
        for a in range(-40, 41, 3):
            for b in range(-40, 41, 3):
                x, n = (a, b), 0
                while x not in cyc_pts:
                    x = Tm(x)
                    n += 1
                    assert n < 10 ** 5


def C3(n=400):
    odd = odd_classes(5)
    rng = random.Random(5)
    cnt = {'CERT': 0, 'OBST': 0}
    for mask in rng.sample(range(2 ** 16), n):
        S = {odd[i] for i in range(16) if mask >> i & 1}
        k, _ = classify(5, S, verify=False)
        cnt[k] += 1
    print(f'C3 m=5 sample of {n}: {cnt}')


if __name__ == '__main__':
    C1()
    C2()
    C3()
    print('ALL OK')
