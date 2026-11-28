"""Search (floating point) and then certify (exact rationals) the density
exponents for every system in systems.py.  Writes certificates.json, which
check_density.py re-verifies exactly from scratch.

Run: nice python3 make_certificates.py   (a few seconds)
"""
import json, math, os, sys
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from systems import SYSTEMS
from density_lib import *

L_EARLY = 400


def fs(x):
    return str(Fr(x))


def cert_json(C):
    return dict(s=fs(C.s), gamma=fs(C.gamma), c=fs(C.c), theta=fs(C.theta),
                w=[fs(x) for x in C.w], theta_float_opt=C.theta_float_opt,
                s_float_opt=C.s_float_opt)


out = {}
for S in SYSTEMS:
    g = build_graph(S['T'])
    D, L, Df, Lf = drift(g)
    c0 = 1 + Df / Lf
    rec = dict(id=S['id'], cls=S['cls'], rule=S['rule'], states=len(g.states),
               Delta={str(p): fs(a) for p, a in D.items()},
               Lambda={str(p): fs(a) for p, a in L.items()},
               c0_float=c0, Gmax=fs(g.Gmax), Gmin=fs(g.Gmin),
               single_prime=len(set(g.qs)) == 1)
    if Df < 0:
        C = best_certificate(g, Fr(1), +1)
        rec['never_drop'] = cert_json(C)
        cK = Fr(math.ceil(c0 * 100) + 2, 100)
        if cK >= 1:
            cK = Fr(math.ceil((c0 + 1) / 2 * 1000), 1000)
        CK = best_certificate(g, cK, +1)
        rec['korec'] = cert_json(CK)
        # sharpness of c0 for the method (Proposition 4.2): c below c0
        cS = Fr(math.floor(c0 * 100) - 2, 100)
        CS = best_certificate(g, cS, -1)
        rec['korec_sharp'] = cert_json(CS)
    else:
        cE = Fr(math.floor(c0 * 100) - 2, 100)
        CE = best_certificate(g, cE, -1)
        rec['expanding'] = cert_json(CE)
        if rec['single_prime'] and g.Gmin >= 0:
            lo, hi = -20.0, -1e-6
            for _ in range(60):
                mid = (lo + hi) / 2
                if rho(g, mid, 0.0) <= 1:
                    hi = mid
                else:
                    lo = mid
            s = Fr(hi * 0.9).limit_denominator(50)
            Cq = certify(g, s, Fr(0))
            qlo, qhi = early_drop_bounds(g, L_EARLY, s, Cq.w)
            rec['early_drop'] = dict(s=fs(s), w=[fs(x) for x in Cq.w], L=L_EARLY,
                                     q_lo=float(qlo), q_hi=float(qhi))
    out[S['id']] = rec
    msg = '%-15s c0=%.5f' % (S['id'], c0)
    for k in ('never_drop', 'korec', 'korec_sharp', 'expanding'):
        if k in rec:
            msg += '  %s c=%s theta<=%.5f' % (k, rec[k]['c'], float(Fr(rec[k]['theta'])))
    if 'early_drop' in rec:
        msg += '  q in [%.6f, %.6f]' % (rec['early_drop']['q_lo'], rec['early_drop']['q_hi'])
    print(msg, flush=True)
json.dump(out, open(os.path.join(HERE, 'certificates.json'), 'w'), indent=1)
