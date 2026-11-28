"""Exact counts of non-descending cylinder words, by number of divisions.

N(E) = number of residues mod p^(K+E) whose walk keeps slope >= 1 at each of
its first E divisions (Markov property: one residue per walk).  Exact integer
DP over (node, exponent of l).  The growth exponent H = lim log_p N(E) / E (in base-p
digits per division) is the word-count exponent, an upper bound for the
Hausdorff dimension of the non-descending p-adic set (dim_H N_inf <= liminf
log_p N(E)/E; revised after REFEREE2, it was called the dimension); it is estimated from N (EVIDENCE) and also computed from the
variational formula H = min_theta s(theta), rho(M_{theta,s}) = 1 (floats).

Usage: python3 count_nondesc.py [Emax]   (prints a table; measurement only).
       python3 count_nondesc.py --check  (DP = direct residue counts; exits 0/1).
       python3 count_nondesc.py --hcheck (stated H values = variational minimum,
           minimizer interior, exact-count fit at E = 600 consistent; exits 0/1).
Revision after REFEREE1: the theta grid was [0, 3]; it is now [0, 12] with a
guard.  The old core13 / core135 values 0.4565 / 0.3755 were s(3), not the
minimum; the corrected values are 0.4281 / 0.3593.
"""
import sys
from math import log
import numpy as np
import cwlib as L


def macro(sysd, K, l):
    """For each node r: follow division-free steps; return list of
    (a_total, e, target) for the p^e branches of the first dividing step,
    where a_total is the l-exponent gained (including the dividing step)."""
    p, m, t = sysd['p'], sysd['m'], sysd['table']
    E = L.graph(sysd, K)
    out = {}
    for r in E:
        a = 0
        cur = r
        seen = set()
        while True:
            u, v, w = t[cur % p ** m]
            e = L.vexp(w, p)[0]
            au, rest = L.vexp(u, l) if u > 1 else (0, 1)
            assert rest == 1
            if e == 0:
                assert cur not in seen, 'division-free cycle'
                seen.add(cur)
                a += au
                (nxt, *_r), = E[cur]
                cur = nxt
                continue
            out[r] = [(a + au, e, s) for (s, *_r) in E[cur]]
            break
    return out


def counts(sysd, K, l, Emax):
    p = sysd['p']
    mac = macro(sysd, K, l)
    # state: dict (node, a) -> count, all at division depth D
    layer = {}
    for r in mac:
        layer[(r, 0)] = layer.get((r, 0), 0) + 1
    byD = {0: layer}
    N = [sum(layer.values())]
    pend = {}  # depth -> dict
    for D in range(0, Emax):
        cur = byD.pop(D, {})
        for (r, a), c in cur.items():
            for (da, e, s) in mac[r]:
                D2, a2 = D + e, a + da
                if l ** a2 < p ** D2:
                    continue
                d = byD.setdefault(D2, {})
                d[(s, a2)] = d.get((s, a2), 0) + c
        nxt = byD.get(D + 1, {})
        N.append(sum(nxt.values()))
    return N


def H_variational(sysd, K, l):
    p = sysd['p']
    mac = macro(sysd, K, l)
    nodes = sorted(mac)
    idx = {r: i for i, r in enumerate(nodes)}

    def rho(theta, s):
        M = np.zeros((len(nodes), len(nodes)))
        for r in nodes:
            for (da, e, t) in mac[r]:
                M[idx[r], idx[t]] += p ** (-s * e) * (l ** da / p ** e) ** theta
        return max(abs(np.linalg.eigvals(M)))

    def s_of(theta):
        lo, hi = 0.0, 1.0
        if rho(theta, 1.0) >= 1:
            return 1.0
        for _ in range(60):
            mid = (lo + hi) / 2
            if rho(theta, mid) > 1:
                lo = mid
            else:
                hi = mid
        return hi
    # Revision after REFEREE1: the original grid stopped at theta = 3, and for
    # core13 / core135 the minimizer lies near 4.65 / 4.00, so s(3) was
    # reported instead of the minimum.  Now the grid is [0, THMAX] and the run
    # aborts if the grid minimizer is at the right end (the true minimizer
    # would then lie beyond the grid).  s(theta) is the local dimension
    # function; H = min over theta >= 0.
    THMAX, NG = 12.0, 241
    th = np.linspace(0, THMAX, NG)
    vals = [s_of(x) for x in th]
    i = int(np.argmin(vals))
    if i == NG - 1 and vals[i] < 1.0:
        raise RuntimeError('variational minimizer at grid end theta = %g' % THMAX)
    a, b = th[max(i - 1, 0)], th[min(i + 1, NG - 1)]
    for _ in range(60):
        c1, c2 = a + (b - a) / 3, b - (b - a) / 3
        if s_of(c1) < s_of(c2):
            b = c2
        else:
            a = c1
    tmin = (a + b) / 2
    smin = s_of(tmin)
    if vals[i] <= smin:
        return vals[i], th[i]
    return smin, tmin


def main():
    Emax = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    print('%-9s %-3s %-12s %-10s %-10s %-8s %-10s' % ('system', 'K', 'N(Emax)', 'H_fit', 'H_var', 'theta*', 'crit 1/(1-H)'))
    for nm in ['3x+1', '3x-1', '3x+5', '5x+1', 'K7', 'core13', 'core135', 'core57',
               'core157', 'core357', 'core17', 'coreW', 'split5_3', 'split5_1', 'm3_b']:
        sysd, l, *_ = L.SYSTEMS[nm]
        K = sysd['m']
        N = counts(sysd, K, l, Emax)
        p = sysd['p']
        e1, e2 = Emax // 2, Emax
        Hfit = (log(N[e2]) - log(N[e1])) / ((e2 - e1) * log(p)) if N[e2] > 0 else 0.0
        Hv, thv = H_variational(sysd, K, l)
        crit = 1 / (1 - Hv) if Hv < 1 - 1e-9 else float('inf')
        print('%-9s %-3d %-12.4e %-10.5f %-10.5f %-8.3f %-10.4f' % (nm, K, N[Emax], Hfit, Hv, thv, crit))


def brute(sysd, K, l, E):
    """Direct count over residues mod p^(K+E) (independent of the DP)."""
    p, m, t = sysd['p'], sysd['m'], sysd['table']
    Mod = p ** (K + E)
    cnt = 0
    for r in range(Mod):
        n = r + Mod * 1000003
        a, D, ok = 0, 0, True
        while D < E:
            u, v, w = t[n % p ** m]
            e = L.vexp(w, p)[0]
            au = L.vexp(u, l)[0] if u > 1 else 0
            n = (u * n + v) // w
            a += au
            D += e
            if e and l ** a < p ** D:
                ok = False
                break
        cnt += ok
    return cnt


def selfcheck():
    bad = 0
    for nm in ['3x+1', '3x-1', '5x+1', 'K7', 'core13', 'core135', 'split5_3', 'm3_b']:
        sysd, l, *_ = L.SYSTEMS[nm]
        K = sysd['m']
        N = counts(sysd, K, l, 12)
        Emax = 12 if sysd['p'] == 2 else 7
        for E in range(1, Emax + 1):
            b = brute(sysd, K, l, E)
            if b != N[E]:
                print('MISMATCH', nm, E, b, N[E])
                bad += 1
    print('DP counts agree with direct residue counts' if not bad else 'FAIL')
    return bad


STATED_H = {  # values quoted in README / theorem_P.md after the revision
    '3x+1': 0.9500, 'K7': 0.7491, 'core13': 0.4281, 'core135': 0.3593,
    'core57': 0.7193, 'core157': 0.7735, 'core357': 0.7880, 'core17': 0.7901,
    'split5_3': 0.5807, 'split5_1': 0.9369, 'm3_b': 0.9648, '5x+1': 1.0,
    'coreW': 1.0}


def hcheck(Emax=600):
    """Revision after REFEREE1: consistency check of the stated H values
    (floats, EVIDENCE).  Fails if a quoted value differs from the variational
    minimum by more than 5e-4, if the minimizer is at the grid end, or if the
    exact-count fit over [Emax/2, Emax] is more than 0.01 below or 0.002
    above the variational value (the fit approaches H from below)."""
    bad = 0
    for nm, Hs in STATED_H.items():
        sysd, l, *_ = L.SYSTEMS[nm]
        K, p = sysd['m'], sysd['p']
        Hv, thv = H_variational(sysd, K, l)
        N = counts(sysd, K, l, Emax)
        e1 = Emax // 2
        Hfit = (log(N[Emax]) - log(N[e1])) / ((Emax - e1) * log(p))
        ok = abs(Hv - Hs) < 5e-4 and -0.01 < Hfit - Hv < 0.002
        print('%-9s stated %.4f  H_var %.5f (theta* %.3f)  H_fit %.5f  %s'
              % (nm, Hs, Hv, thv, Hfit, 'ok' if ok else 'FAIL'))
        bad += not ok
    return bad


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--hcheck':
        sys.exit(1 if hcheck() else 0)
    if len(sys.argv) > 1 and sys.argv[1] == '--check':
        sys.exit(1 if selfcheck() else 0)
    main()
