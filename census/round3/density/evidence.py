"""EVIDENCE only (floating point / finite simulation; nothing here is a proof).

 [E1] Theorem 3 numerically: the number O_j of depth-j tree nodes whose slope
      never fell below 1/2 grows like p^(theta* j) j^(-3/2); estimate
      theta_est = (log_p O_L - log_p O_{L/2} + 1.5 log_p 2) / (L/2).
 [E2] Mixed-prime maps: theta* and c0 do not depend on the order in which
      the adaptive tree splits by 2, 3, 5.
 [E3] Expanding maps: the fraction of n in [2^17, 2^18) that drop below n
      within log2 n tree steps (Theorem 6 says the density is q) and the
      fraction that drop at all within 20000 raw steps / before exceeding n^4.
 [E4] Contracting maps: the actual number of n <= 2^18 that do not drop
      below n within 20000 steps, against the proved bound exponent.
Run: nice python3 evidence.py   (about 1-2 minutes)
"""
import itertools, math, os, sys, time
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from systems import SYSTEMS, get, div_else
from density_lib import *

t0 = time.time()
print("[E1] growth of the uncertified node count O_j (single-prime maps)")
for sid, L in [('par_3_1', 800), ('m3_d', 500), ('m3_g', 400), ('split5_1', 300),
               ('split5_3', 300), ('desc_split7_1', 300), ('desc_m3_4n5', 300),
               ('desc_s32_plus9', 160)]:
    g = build_graph(get(sid)['T'])
    s, gm, th = optimize(g)
    _, _, ac, ps, p = slope_walk(g, L, 1, 2)
    lp = lambda x: math.log(x) / math.log(p)
    est = (lp(ac[L]) - lp(ac[L // 2]) + 1.5 * lp(2)) / (L / 2)
    print("   %-15s theta*=%.5f  log_p(O_L)/L=%.5f  corrected estimate=%.5f  (L=%d)"
          % (sid, th, lp(ac[L]) / L, est, L), flush=True)

print("[E2] split-order invariance (mixed primes)")
for name, (pr, a) in {'div23_5n1': ((2, 3), 5), 'div23_7n1': ((2, 3), 7),
                      'div235_7n1': ((2, 3, 5), 7)}.items():
    Q, t = div_else(pr, a, 1)
    vals = set()
    for order in itertools.permutations(pr):
        g = build_graph(TableMap(name, Q, t, primes=list(order)))
        D, Lm, Df, Lf = drift(g)
        s, gm, th = optimize(g)
        vals.add((round(1 + Df / Lf, 9), round(th, 4)))
        print("   %-11s order=%s states=%d c0=%.6f theta*=%.5f" % (name, order, len(g.states), 1 + Df / Lf, th))
    print("   ->", "invariant" if len(vals) == 1 else "ORDER-DEPENDENT", flush=True)

print("[E3] expanding maps: early drops vs all drops, n in [2^17, 2^18)")
for sid in ('par_5_1', 'par_7_1', 'par_9_1', 'm3_e'):
    S = get(sid)
    g = build_graph(S['T'])
    step = S['step']
    lo, hi = 1 << 17, 1 << 18
    early = ever = 0
    for n in range(lo, hi):
        path = path_of(g, n, 1 << 17)
        if any(nd[3] * ((n - nd[2]) // nd[1]) + nd[4] < n for nd in path[1:]):
            early += 1
        x, k = n, 0
        while k < 20000:
            x = step(x)
            k += 1
            if x < n:
                ever += 1
                break
            if x > n ** 4:
                break
    tot = hi - lo
    print("   %-8s early-drop fraction %.5f   dropped at all (<=20000 steps, before n^4) %.5f"
          % (sid, early / tot, ever / tot), flush=True)

print("[E4] contracting maps: starts n <= 2^18 with no drop within 20000 steps")
for sid in ('par_3_1', 'par_3_5', 'm3_d', 'm3_g', 'div23_5n1', 'div23_7n1', 'div235_7n1',
            'split5_1', 'split5_3', 'desc_m3_4n5', 'desc_s32_plus9', 'desc_split7_1'):
    step = get(sid)['step']
    nd = []
    for n in range(1, 1 << 18):
        x = n
        for _ in range(20000):
            x = step(x)
            if x < n:
                break
        else:
            nd.append(n)
    print("   %-15s count=%d  first few=%s" % (sid, len(nd), nd[:12]), flush=True)
print("done (%.0fs)" % (time.time() - t0))
