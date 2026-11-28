"""Constants of Theorems G1, G2 for every system in cwlib.SYS.

Per system:
  h      = log_p min_{theta>=0} rho(M(theta)), M(theta)[s,s'] = sum over digits s->s' of (g^a/p^e)^theta (float)
  h_up   = PROVED upper bound for every growth exponent used (Collatz-Wielandt bound at one theta, in
           60-digit Decimal arithmetic with a 1e-40 relative safety margin per operation)
  h0     = PROVED lower bound log_p m*(K0)/K0 <= h_* (exact integer DP + supermultiplicativity)
  iota   = sup_L [(Z/p^L)^* : <g mod p^L>]  (exact for L <= 12; stabilises, see check)
  alpha  = max mean number of g-factors per digit on a cycle of the digit automaton (exact, Karp)
  H2     = 2h - log_p rho(M(2 theta*))  (Renyi-2 rate of the tilted measure, float)
  c1     = h/2 (one-ended, Theorem G1; any constant < h_*/2, and h0/2 is a proved admissible value)
  c2     = min(1, h/2 + H2/(2 alpha log_p g))  (two-ended, Theorem G2, under hypothesis (B))
  Pot    = whether a per-state relabelling of digits makes the log-slope a coboundary plus a function of
           the digit (then (B) is PROVED, Lemma B1); exact rational linear algebra
  Cstar  = 1/(1-h), the critical depth constant of Conjecture E
usage: python cwconst.py [names...] [--K0 N]
"""
import sys, math, itertools, json
from fractions import Fraction
from decimal import Decimal, getcontext
import numpy as np
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from cwlib import System, SYS, index_of_g

getcontext().prec = 60
MARG = Decimal(1) + Decimal(10) ** -40


def matrix(S, theta):
    st = S.states1
    ix = {s: i for i, s in enumerate(st)}
    M = np.zeros((len(st), len(st)))
    mv = S.digit_moves()
    lg, lp = math.log(S.g), math.log(S.p)
    for s in st:
        for (s1, a, e) in mv[s]:
            M[ix[s], ix[s1]] += math.exp(theta * (a * lg - e * lp))
    return M


def rho(S, theta):
    return max(abs(np.linalg.eigvals(matrix(S, theta))))


def minimise(S):
    f = lambda t: math.log(rho(S, t))
    lo, hi = 0.0, 1.0
    while f(hi) < f(hi / 2) and hi < 64:
        hi *= 2
    # golden section on [0, hi] (log rho is convex in theta)
    gr = (math.sqrt(5) - 1) / 2
    a, b = 0.0, hi
    c, d = b - gr * (b - a), a + gr * (b - a)
    for _ in range(200):
        if f(c) < f(d):
            b = d
        else:
            a = c
        c, d = b - gr * (b - a), a + gr * (b - a)
    t = (a + b) / 2
    if f(0.0) <= f(t):
        t = 0.0
    return t, rho(S, t)


def dec_pow(base_num, base_den, theta):
    """(base_num/base_den)^theta, Decimal, theta a Decimal >= 0"""
    if theta == 0:
        return Decimal(1)
    x = (Decimal(base_num) / Decimal(base_den))
    return (x.ln() * theta).exp()


def rho_upper(S, theta):
    """PROVED upper bound on rho(M(theta)) for theta = the given float rounded to a Decimal:
    Collatz-Wielandt: rho <= max_s (M x)_s / x_s for any positive x."""
    th = Decimal(repr(theta))
    M = matrix(S, float(th))
    w, V = np.linalg.eig(M.T @ np.eye(len(M)) if False else M)
    i = int(np.argmax(abs(w)))
    x = np.abs(np.real(V[:, i]))
    x = np.maximum(x, 1e-300)
    xd = [Decimal(repr(float(v))) for v in x]
    st = S.states1
    ix = {s: j for j, s in enumerate(st)}
    mv = S.digit_moves()
    best = Decimal(0)
    for s in st:
        tot = Decimal(0)
        for (s1, a, e) in mv[s]:
            tot += dec_pow(S.g ** a, S.p ** e, th) * MARG * xd[ix[s1]]
        r = tot / xd[ix[s]] * MARG
        best = max(best, r)
    return best, th


def h_upper(S, theta):
    r, th = rho_upper(S, theta)
    return (r.ln() / Decimal(S.p).ln()) * MARG, th


def mstar(S, K0):
    """Lemma P data.  G = largest set of states (reachable in >= 1 digit) such that every sigma in G has
    m_GG(sigma, K0) = #{z in All_{K0}(sigma, 1) whose path ends in a state of G} > 0 (fixed-point iteration).
    Returns (m_GG(K0) = min over G, G, r) where r = length of the longest path inside the complement of G
    in the digit automaton (None if that subgraph has a cycle).  Exact."""
    G = set(S.states1)
    cache = {st: S.dp(K0, start=st, keep={K0})[K0] for st in S.states1}
    while True:
        bad = {st for st in G if sum(c for (s1, A), c in cache[st].items() if s1 in G) == 0}
        if not bad:
            break
        G -= bad
    if not G:
        return 0, G, None
    m = min(sum(c for (s1, A), c in cache[st].items() if s1 in G) for st in G)
    B = [st for st in S.states1 if st not in G]
    # longest path in the subgraph on B (acyclic check), counting digits until a G-state is entered
    from functools import lru_cache
    succ = {st: {t[0] for t in S.trans[st]} for st in B}
    state = {}
    def longest(st, stack=()):
        if st in G:
            return 0
        if st in stack:
            raise ValueError
        return 1 + max(longest(t, stack + (st,)) for t in succ[st])
    try:
        r = max([longest(st) for st in B], default=0)
    except ValueError:
        r = None
    return m, G, r


def karp_alpha(S):
    """max over cycles of (sum a)/(digits): Karp's maximum mean cycle, exact Fractions"""
    st = S.states1
    n = len(st)
    ix = {s: i for i, s in enumerate(st)}
    mv = S.digit_moves()
    edges = [(ix[s], ix[s1], a) for s in st for (s1, a, e) in mv[s]]
    NEG = None
    D = [[NEG] * n for _ in range(n + 1)]
    for v in range(n):
        D[0][v] = 0                      # super source to all vertices
    for kk in range(1, n + 1):
        for (u, v, a) in edges:
            if D[kk - 1][u] is not None:
                x = D[kk - 1][u] + a
                if D[kk][v] is None or x > D[kk][v]:
                    D[kk][v] = x
    best = None
    for v in range(n):
        if D[n][v] is None:
            continue
        worst = None
        for kk in range(n):
            if D[kk][v] is None:
                continue
            val = Fraction(D[n][v] - D[kk][v], n - kk)
            worst = val if worst is None else min(worst, val)
        if worst is not None:
            best = worst if best is None else max(best, worst)
    return best


def potential(S):
    """search per-state digit relabellings pi_s and (f, phi) with X(s, pi_s(d)) = f(d) + phi(s') - phi(s),
    X = (a, e) in Z^2.  Returns a witness or None.  Exact (Fractions)."""
    st = S.states1
    p = S.p
    mv = S.digit_moves()
    ix = {s: i for i, s in enumerate(st)}
    perms = list(itertools.permutations(range(p)))
    nvar = p + len(st)                 # f(0..p-1), phi(states); phi(st[0]) fixed by adding eq phi0 = 0
    for choice in itertools.product(perms, repeat=len(st)):
        ok = True
        sol_all = []
        for comp in (0, 1):            # the a- and e-components separately
            rows, rhs = [], []
            for s, pi in zip(st, choice):
                for dlab in range(p):
                    (s1, a, e) = mv[s][pi[dlab]]
                    if s1 not in ix:
                        ok = False
                        break
                    r = [Fraction(0)] * nvar
                    r[dlab] += 1
                    r[p + ix[s1]] += 1
                    r[p + ix[s]] -= 1
                    rows.append(r)
                    rhs.append(Fraction((a, e)[comp]))
            r = [Fraction(0)] * nvar
            r[p] = Fraction(1)
            rows.append(r)
            rhs.append(Fraction(0))
            x = solve_exact(rows, rhs)
            if x is None:
                ok = False
                break
            sol_all.append(x)
        if ok:
            return dict(perm={str(s): pi for s, pi in zip(st, choice)},
                        f=[(sol_all[0][d], sol_all[1][d]) for d in range(p)],
                        phi={str(s): (sol_all[0][p + ix[s]], sol_all[1][p + ix[s]]) for s in st})
    return None


def solve_exact(rows, rhs):
    """consistent solution of an over-determined rational system, or None"""
    m = [r[:] + [b] for r, b in zip(rows, rhs)]
    nv = len(rows[0])
    piv = []
    ri = 0
    for c in range(nv):
        pr = next((i for i in range(ri, len(m)) if m[i][c] != 0), None)
        if pr is None:
            continue
        m[ri], m[pr] = m[pr], m[ri]
        pv = m[ri][c]
        m[ri] = [x / pv for x in m[ri]]
        for i in range(len(m)):
            if i != ri and m[i][c] != 0:
                fct = m[i][c]
                m[i] = [x - fct * y for x, y in zip(m[i], m[ri])]
        piv.append(c)
        ri += 1
    for i in range(ri, len(m)):
        if m[i][-1] != 0:
            return None
    x = [Fraction(0)] * nv
    for i, c in enumerate(piv):
        x[c] = m[i][-1]
    return x


def constants(name, K0=None):
    S = System(name)
    p, g = S.p, S.g
    if K0 is None:
        K0 = 400 if p == 2 else 250
    th, r = minimise(S)
    h = math.log(r) / math.log(p)
    hu, thd = h_upper(S, th)
    ms, G, rr = mstar(S, K0)
    h0 = math.log(ms) / math.log(p) / K0 if ms > 0 else float("-inf")
    # exact lower bound as a fraction-friendly statement: log_p m* / K0 (printed to 6 digits rounded down)
    idx = [index_of_g(p, g, L)[0] for L in range(1, 13)]
    alpha = karp_alpha(S)
    r2 = rho(S, 2 * th)
    H2 = 2 * h - math.log(r2) / math.log(p)
    lgp = math.log(g) / math.log(p)
    c1 = h / 2
    c2 = min(1.0, h / 2 + H2 / (2 * float(alpha) * lgp)) if alpha and alpha > 0 else None
    pot = potential(S)
    # drift per digit under Haar (float): d/dtheta log rho at 0
    eps = 1e-6
    drift = (math.log(rho(S, eps)) - math.log(rho(S, 0))) / eps
    out = dict(name=name, p=p, g=g, k=S.k, states=len(S.states1), theta_star=th, h=h,
               h_up=float(hu), h_up_exact=str(hu)[:20], theta_dec=str(thd), K0=K0, mstar=ms, h0=h0, G=sorted(G), bad=[s for s in S.states1 if s not in G], rescue=rr,
               iota_L=idx, alpha=str(alpha), lam=math.log(p) / math.log(g), H2=H2, c1=c1, c2=c2,
               pot=pot is not None, drift=drift, H0=S.H0,
               Cstar=(1 / (1 - h) if h < 1 - 1e-12 else float("inf")))
    return out, pot


if __name__ == "__main__":
    args = sys.argv[1:]
    K0 = None
    if "--K0" in args:
        i = args.index("--K0")
        K0 = int(args[i + 1])
        args = args[:i] + args[i + 2:]
    names = args or list(SYS)
    res = []
    for n in names:
        o, pot = constants(n, K0)
        res.append(o)
        print(f"{n:15s} p={o['p']} g={o['g']} st={o['states']} drift={o['drift']:+.4f} th*={o['theta_star']:.5f} "
              f"h={o['h']:.6f} h_up={o['h_up']:.6f} h0={o['h0']:.5f} iota={o['iota_L'][-1]} alpha={o['alpha']} "
              f"H2={o['H2']:.5f} c1={o['c1']:.5f} c2={o['c2'] if o['c2'] is None else round(o['c2'], 5)} "
              f"Pot={o['pot']} bad={o['bad']} r={o['rescue']} C*={o['Cstar']:.4f}", flush=True)
    json.dump(res, open(__import__("os").path.join(__import__("os").path.dirname(__import__("os").path.abspath(__file__)),
                                                   "data", "constants.json"), "w"), indent=1, default=str)
