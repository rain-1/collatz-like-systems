"""Instances of the general whole-prefix cutoff (Theorem W, theorem_W.md) on
every census system of the table, exact checks plus an EVIDENCE table.

For each system: expanding cycle C (rotated, node r0, periodic point x*), a
re-entry walk W at r0 with slope lambda_W < 1, rate kappa = log(1/lambda_W) /
log(lambda_C), and the near-critical rigid family
    C^{k_1} W C^{k_2} W ... C^{k_e} W,   K_i = k_1 + ... + k_i = floor(kappa i) + 1.

Exact checks (assertions):
  (a) shifted form: T_C(x*+y) = x* + lambda_C y and T_W(x*+y) = x* + lambda_W y + c_W
      with c_W != 0 (Fractions, symbolic in y via two evaluations);
  (b) the whole-prefix identity y_0 + sum_i c_W/P_i = y_e/P_e on the actual
      integer orbit of the least positive start realizing the word (e = 80);
  (c) the shift-and-subtract decomposition: for the Dirichlet-minimizing
      q <= Q = floor(delta e) (delta = 1/4) and k = round(kappa q),
         (1-gamma)(y_0 + sum tau) = (1-gamma) y_0 + sum_{i>e-q} tau_i
               - gamma sum_{i<=q} tau_i + sum_{i in X} (tau_i - gamma tau_{i+q})
      exactly, where X = {i : K_{i+q}-K_i != k}; and |X| <= ceil((e-q)/Q)
      (Lemma R as revised after REFEREE1: the exceptional set is a half-open
      arc of length ||kappa q||, holding <= 1 of any Q consecutive phases);
  (c') the window count of Lemma R: ceil(n / floor(delta n)) <= 2/delta + 1
      for all delta = 1/d, d = 5..40, and n with delta n >= 2, n <= 4000;
  (d) prefix slopes P_i >= 1 at every W-boundary (the family is non-descending).

EVIDENCE (printed, also asserted loosely): least positive and least negative
integer lifts y of the word with e blocks; Theorem W says log_p|y| / h -> 1
(h = number of divisions).  A lift with ratio < 0.8 for e >= 100 fails the run.
Exits 0 iff all assertions hold.
"""
import sys
from fractions import Fraction as F
from decimal import Decimal, getcontext
from math import log, ceil
import cwlib as L

getcontext().prec = 80
FAIL = []


def claim(name, cond):
    if not cond:
        FAIL.append(name)
        print('FAIL', name)


def dlog(x):
    return Decimal(x.numerator).ln() - Decimal(x.denominator).ln()


def closed_walks(E, r0, Lmax):
    stack = [(r0, [r0])]
    while stack:
        r, path = stack.pop()
        for (t, *_x) in E[r]:
            if t == r0:
                yield list(path)
            if len(path) < Lmax:
                stack.append((t, path + [t]))


def contracting_reentry(sysd, E, cn, Lmax=12):
    Lc = len(cn)
    cedges = {(cn[i], cn[(i + 1) % Lc]) for i in range(Lc)}
    best = None
    for w in closed_walks(E, cn[0], Lmax):
        seq = w + [w[0]]
        if all((seq[i], seq[i + 1]) in cedges for i in range(len(w))):
            continue
        s = L.slope(sysd, w)
        if s < 1 and (best is None or len(w) < len(best[0]) or
                      (len(w) == len(best[0]) and s > best[1])):
            best = (w, s)
    return best


def setup(name):
    sysd, l, seed, note = L.SYSTEMS[name]
    p, K = sysd['p'], sysd['m']
    E = L.graph(sysd, K)
    c, lam = L.expanding_cycle(sysd, K, maxlen=10)
    x = L.periodic_point(sysd, c)
    pts = L.rotate_cycle_lemma(sysd, L.cycle_nodes(sysd, x, K))
    cn = L.nodes_of_points(pts, p, K)
    xs = pts[0]
    W, lamW = contracting_reentry(sysd, E, cn)
    lamC = L.slope(sysd, cn)
    kappa = -dlog(lamW) / dlog(lamC)
    return sysd, p, K, cn, xs, W, lamC, lamW, kappa


def affine(sysd, walk):
    A, B, D = L.walk_affine(sysd, walk)
    return lambda n: F(A * n + B, D)


def cycle_check(b, xs, n0, laps=60):
    """Revision after REFEREE1 (section 5): an expanding integer cycle of the
    Terras map (3n+b)/2 | n/2, read in y = n - x* around the fixed point x*,
    is a path satisfying (H0)-(H4): one geometric piece (period = events per
    lap), |tau_i| <= 1, labels c = -x* (step (y + c)/2), from the bounded start y_0 = n0 - x*,
    with E unbounded.  So it is not (H2) that keeps cycles out of Theorem W;
    only the ineffective threshold y_* (which must exceed |y_0|) does."""
    xs = F(xs)
    n, y0 = n0, F(n0) - xs
    A, E, taus, evs = 0, 0, [], []
    for _ in range(laps):
        while True:
            if n % 2:
                n = (3 * n + b) // 2
                A += 1
                E += 1
                # odd step in y: y -> 3y/2 + (x* + b)/2, no event iff x* + b = 0
                claim('odd step has no event (b=%d)' % b, xs + b == 0)
            else:
                c = -xs  # even step y -> (y + c)/2 in the (l^a y + c)/p^e convention
                taus.append(c * F(2) ** E / F(3) ** A)
                evs.append((A, E))
                n //= 2
                E += 1
            if n == n0:
                break
    claim('cycle identity b=%d' % b, y0 + sum(taus) == F(2) ** E * (F(n) - xs) / F(3) ** A)
    claim('cycle |tau| <= 1 b=%d' % b, all(abs(t) <= 1 for t in taus))
    per = len(evs) // laps
    vec = {(evs[i + per][0] - evs[i][0], evs[i + per][1] - evs[i][1]) for i in range(len(evs) - per)}
    claim('cycle is one geometric piece b=%d' % b, len(vec) == 1 and vec != {(0, 0)})
    claim('cycle expands b=%d' % b, F(3) ** A > F(2) ** E)
    return abs(y0), E


def window_count_check():
    for d in range(5, 41):
        delta = F(1, d)
        for n in range(2 * d, 4001):
            Qn = (delta * n).numerator // (delta * n).denominator
            claim('window count d=%d n=%d' % (d, n), -(-n // Qn) <= 2 / delta + 1)


def schedule(kappa, e):
    Ks = [0] + [int((kappa * i).to_integral_value(rounding='ROUND_FLOOR')) + 1 for i in range(1, e + 1)]
    # floor safety margin
    for i in range(1, e + 1):
        fr = kappa * i - int((kappa * i).to_integral_value(rounding='ROUND_FLOOR'))
        assert Decimal('1e-30') < fr < 1 - Decimal('1e-30')
    return Ks


def word_of(cn, W, Ks):
    w = []
    for i in range(1, len(Ks)):
        w += cn * (Ks[i] - Ks[i - 1]) + W
    return w


def run(name, e_exact=80, e_list=(100, 150, 200, 250, 300)):
    sysd, p, K, cn, xs, W, lamC, lamW, kappa = setup(name)
    TC, TW = affine(sysd, cn), affine(sysd, W)
    # (a) shifted forms (affine maps: two evaluations determine them)
    for y in (F(0), F(1)):
        pass
    claim(name + ' C fixes x*', TC(xs) == xs)
    claim(name + ' C linear in y', TC(xs + 1) - xs == lamC)
    cW = TW(xs) - xs
    claim(name + ' W shifted slope', TW(xs + 1) - TW(xs) == lamW)
    claim(name + ' c_W != 0', cW != 0)
    # (b) identity on actual orbit
    Ks = schedule(kappa, e_exact)
    word = word_of(cn, W, Ks)
    rho, Mod = L.follow_class(sysd, word + [cn[0]], K)
    n = rho if rho > 0 else rho + Mod
    y0 = F(n) - xs
    P = F(1)
    Ps, taus = [], []
    cur = n
    pos = 0
    ok_follow = True
    for i in range(1, e_exact + 1):
        P *= lamC ** (Ks[i] - Ks[i - 1]) * lamW
        Ps.append(P)
        taus.append(cW / P)
    for r in word:
        ok_follow &= (cur % p ** K == r)
        cur = L.step(sysd, cur)
    claim(name + ' integer follows word', ok_follow)
    ye = F(cur) - xs
    claim(name + ' whole-prefix identity', y0 + sum(taus) == ye / Ps[-1])
    claim(name + ' prefix slopes >= 1', all(x >= 1 for x in Ps))
    # (c) shift and subtract
    e = e_exact
    Q = e // 4
    q = min(range(1, Q + 1), key=lambda j: abs(kappa * j - (kappa * j).to_integral_value()))
    k = int((kappa * q).to_integral_value())
    gamma = lamC ** k * lamW ** q
    tau = [None] + taus  # 1-indexed
    X = [i for i in range(1, e - q + 1) if Ks[i + q] - Ks[i] != k]
    lhs = (1 - gamma) * (y0 + sum(taus))
    rhs = (1 - gamma) * y0 + sum(tau[i] for i in range(e - q + 1, e + 1)) \
        - gamma * sum(tau[i] for i in range(1, q + 1)) \
        + sum(tau[i] - gamma * tau[i + q] for i in X)
    claim(name + ' shift-subtract decomposition', lhs == rhs)
    claim(name + ' paired terms vanish off X', all(tau[i] == gamma * tau[i + q]
                                                    for i in range(1, e - q + 1) if i not in X))
    # Revision after REFEREE1: the exceptional set of the floor is a half-open
    # arc of length ||kappa q||, which holds at most one of any Q consecutive
    # phases, so |X| <= ceil((e - q)/Q) (one per window); the old check used
    # the weaker 2 * ceil((e - q)/Q).
    claim(name + ' |X| bound (half-open arcs)', len(X) <= ceil((e - q) / Q))
    claim(name + ' RHS equals (1-gamma) y_e/P_e', lhs == (1 - gamma) * ye / Ps[-1])
    # EVIDENCE: lift ratios
    ratios = []
    for ee in e_list:
        Ks2 = schedule(kappa, ee)
        w2 = word_of(cn, W, Ks2)
        rho, Mod = L.follow_class(sysd, w2 + [cn[0]], K)
        h = L.vexp(Mod, p)[0] - K
        pos_lift = rho if rho > 0 else rho + Mod
        neg_lift = Mod - pos_lift
        rp = log(pos_lift) / (h * log(p))
        rn = log(neg_lift) / (h * log(p))
        ratios.append((ee, h, rp, rn))
        claim(name + ' lift ratio e=%d' % ee, min(rp, rn) > 0.8)
    return dict(name=name, lamC=lamC, lamW=lamW, kappa=float(kappa), lenW=len(W),
                q=q, k=k, X=len(X), ratios=ratios, cW=cW, xs=xs)


if __name__ == '__main__':
    names = ['3x+1', '3x-1', '3x+5', '5x+1', 'K7', 'core13', 'core135', 'core57',
             'core157', 'core357', 'core17', 'coreW', 'split5_3', 'split5_1', 'm3_b']
    print('%-9s %-6s %-6s %-7s %-8s %-3s %-9s %-4s %s' % ('system', 'x*', 'lamC', 'lamW', 'kappa',
                                                     '|W|', 'q,k (e=80)', '|X|', 'min lift ratio (e=100..300): pos/neg'))
    for nm in names:
        r = run(nm)
        mp = min(x[2] for x in r['ratios'])
        mn = min(x[3] for x in r['ratios'])
        print('%-9s %-6s %-6s %-7s %-8.4f %-3d %-9s %-4d %.4f / %.4f' % (
            nm, str(r['xs']), str(r['lamC']), str(r['lamW']), r['kappa'], r['lenW'],
            '%d,%d' % (r['q'], r['k']), r['X'], mp, mn))
    window_count_check()
    print('Lemma R window count ceil(n/floor(delta n)) <= 2/delta + 1: checked')
    for (b, xs, n0, nm) in [(-1, 1, 5, '3x-1 cycle 5,7,10'), (-1, 1, 17, '3x-1 cycle from 17'),
                            (1, -1, -5, '3x+1 cycle -5,-7,-10'), (1, -1, -17, '3x+1 cycle from -17')]:
        yy, EE = cycle_check(b, xs, n0)
        print('%-22s satisfies (H0)-(H4) from |y_0| = %s with E = %d divisions (60 laps)' % (nm, yy, EE))
    if FAIL:
        print('FAILURES', FAIL)
        sys.exit(1)
    print('all checks passed')
