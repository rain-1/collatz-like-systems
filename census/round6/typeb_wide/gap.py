"""Tail exponent theta_1 versus run exponent theta_run (round4/lundberg Theorem 1), exact
certificates.

M_theta[r, s] = sum over edges r -> s of p^-e (u/p^e)^theta on G_m; rho_S its spectral radius
on a component S.  theta_C = v_C log p / log lambda_C for an expanding simple cycle.

Certificate that rho_S(theta) <= 1 for all theta in [0, t] (t rational): a positive rational
vector x with (M^up_t x)_r <= x_r for r in S, where M^up_t >= M_t entrywise is built from
rational upper bounds U >= (u/p^e)^t verified by exact integer powers (U^den >= (u/p^e)^num).
Then rho_S(t) <= 1 (Collatz-Wielandt), and log rho_S is convex with rho_S(0) <= 1 (lundberg
Theorem 1 (i)), so rho_S <= 1 on [0, t].

Use: certify_gap_zero(p, m, table) for a system with an isolated expanding cycle C (type-b SCC)
and other components of any type.  If theta_C is the least run exponent of the isolated cycles
and every other non-trivial component S has rho_S(t) <= 1 at some rational t >= theta_C, then
theta_1 = theta_C.  If moreover some component is of type (c), its expanding cycles have
run exponent > theta_S >= theta_C (lundberg Theorem 1 (ii), strict for a non-simple SCC), so
theta_run = theta_C = theta_1: the gap is zero although the system is of type (c).
"""
import math
from fractions import Fraction as Fr
import numpy as np
import tblib as TB


def upper_pow(q, t):
    """rational U >= q**t (q, t positive Fractions), checked exactly"""
    a, b = t.numerator, t.denominator
    f = float(q) ** float(t)
    U = Fr(f * (1 + 1e-9)).limit_denominator(10 ** 12)
    if U < Fr(f):
        U = Fr(f * (1 + 1e-8))
    # exact check  U^b >= q^a
    assert U ** b >= q ** a
    return U


def comp_matrix(p, m, table, nodes, t_float):
    idx = {v: i for i, v in enumerate(nodes)}
    E = TB.graph(p, m, table, m)
    M = np.zeros((len(nodes), len(nodes)))
    for r in nodes:
        for s, u, e in E[r]:
            if s in idx:
                M[idx[r], idx[s]] += p ** (-e) * (u / p ** e) ** t_float
    return M


def rho(p, m, table, nodes, t):
    M = comp_matrix(p, m, table, nodes, t)
    return max(abs(np.linalg.eigvals(M)))


def certify_rho_le1(p, m, table, nodes, t):
    """exact certificate that rho_S(t) <= 1 (t a Fraction); returns True/False"""
    tf = float(t)
    M = comp_matrix(p, m, table, nodes, tf)
    w, V = np.linalg.eig(M.T)          # left/right does not matter for the test below
    w2, V2 = np.linalg.eig(M)
    k = int(np.argmax(abs(w2)))
    x = np.abs(np.real(V2[:, k]))
    x = x / x.max()
    x = np.maximum(x, 1e-6)
    xs = [Fr(float(v)).limit_denominator(10 ** 9) for v in x]
    idx = {v: i for i, v in enumerate(nodes)}
    E = TB.graph(p, m, table, m)
    cache = {}
    for r in nodes:
        tot = Fr(0)
        for s, u, e in E[r]:
            if s in idx:
                q = Fr(u, p ** e)
                if q not in cache:
                    cache[q] = upper_pow(q, t)
                tot += Fr(1, p ** e) * cache[q] * xs[idx[s]]
        if tot > xs[idx[r]]:
            return False
    return True


def theta_C(p, U, e):
    return e * math.log(p) / (math.log(U) - e * math.log(p))


def analyse(p, m, table):
    cl = TB.classify(p, m, table, weights=False)
    bs = [c for c in cl["comps"] if c["kind"] == "b"]
    others = [c for c in cl["comps"] if c["kind"] in ("a", "c") and not c.get("simple")]
    if not bs:
        return None
    thb = min(theta_C(p, c["U"], c["e"]) for c in bs)
    # rational t slightly above theta_C
    t = Fr(thb).limit_denominator(1000)
    while float(t) < thb:
        t += Fr(1, 1000)
    res = dict(theta_b=thb, t=t, types=sorted(cl["types"]), comps=[])
    allok = True
    for c in others:
        r_ = rho(p, m, table, c["nodes"], float(t))
        ok = r_ < 1 - 1e-9 and certify_rho_le1(p, m, table, c["nodes"], t)
        res["comps"].append((c["kind"], len(c["nodes"]), r_, ok))
        allok &= ok
    res["gap_zero_certified"] = allok
    return res
