"""depthlib.py -- the designed family D(p, m, word, h) of depth.md (part A).

Table maps in the setting of round3/dichotomy (modulus Q = p^m, branch
n = r (mod Q) -> (u n + v)/w).  The residue graph is designed by hand:

  * a LOOP of L = len(word) residues l_0 -> l_1 -> ... -> l_{L-1} -> l_0.  Letter
    (u, e) at l_i means the branch n -> (u n + v)/p^e with v chosen so that
    T(l_i) = l_{i+1}.  e = 0: out-degree 1.  e = 1: out-degree p, the extra
    successors l_{i+1} + j Q/p (j = 1..p-1) lie in [Q/p, Q) and are RESETS.
  * a CHAIN e_1 -> ... -> e_h -> l_{i0} of residues with letter (uc, 0)
    (multiplier uc, out-degree 1).
  * every other residue r is a RESET:  n -> (n + Q - r)/Q  (u = 1, w = Q),
    i.e. n -> floor(n/Q) + 1; it has multiplier 1/Q and out-degree Q.

Loop and chain residues are distinct and lie in [2, Q/p); residue 1 is a reset,
so 1 -> 1.  Everything here is exact (ints / Fractions).
"""
from fractions import Fraction
import math


def christoffel(a, b):
    """Lower Christoffel word with a letters 'U' and b letters 'D' (gcd may be > 1:
    then it is the power of the primitive one).  Balanced: every two factors of the
    same length differ by at most one in their number of U's."""
    L = a + b
    w = []
    for i in range(L):
        # letter i is U iff floor((i+1) a / L) - floor(i a / L) == 1
        w.append('U' if ((i + 1) * a) // L - (i * a) // L == 1 else 'D')
    return w


def build(p, m, loop, h, uc, i0, loop_res=None, chain_res=None):
    """loop: list of letters (u, e); returns (Q, table, info)."""
    Q = p ** m
    L = len(loop)
    if loop_res is None:
        loop_res = list(range(2, 2 + L))
    if chain_res is None:
        chain_res = list(range(2 + L, 2 + L + h))
    allres = loop_res + chain_res
    assert len(set(allres)) == len(allres)
    assert all(2 <= r < Q // p for r in allres), "loop/chain must fit in [2, Q/p)"
    table = [None] * Q
    for i, (u, e) in enumerate(loop):
        r, s = loop_res[i], loop_res[(i + 1) % L]
        assert math.gcd(u, p) == 1 and e in (0, 1)
        w = p ** e
        table[r] = (u, w * s - u * r, w)
    for j in range(h):
        r = chain_res[j]
        s = chain_res[j + 1] if j + 1 < h else loop_res[i0]
        table[r] = (uc, s - uc * r, 1)
    for r in range(Q):
        if table[r] is None:
            table[r] = (1, (Q - r) % Q, Q)
    info = dict(Q=Q, L=L, h=h, i0=i0, loop_res=loop_res, chain_res=chain_res)
    return Q, table, info


def loop_mult(loop, p):
    U, D = 1, 0
    for (u, e) in loop:
        U *= u
        D += e
    return Fraction(U, p ** D)


def prefix_products(loop, p, i):
    """P_i(s) for s = 0..L: product of the letters i, i+1, ..., i+s-1 (cyclic)."""
    L = len(loop)
    out = [Fraction(1)]
    for s in range(L):
        u, e = loop[(i + s) % L]
        out.append(out[-1] * Fraction(u, p ** e))
    return out


def tstar(loop, p, i, G):
    """min { t >= 1 : G * P_i(t) < 1 } for the infinite periodic walk from rotation i.
    Uses P_i(kL + s) = lam^k P_i(s); exact.  Returns (t, k, s)."""
    L = len(loop)
    lam = loop_mult(loop, p)
    assert lam < 1
    P = prefix_products(loop, p, i)
    best = None
    for s in range(1, L + 1):
        x = G * P[s]
        # least k >= 0 with x * lam^k < 1.  Float guess, then exact repair.
        if x < 1:
            k = 0
        else:
            k = max(0, int(math.floor((math.log(x.numerator) - math.log(x.denominator))
                                      / -(math.log(lam.numerator) - math.log(lam.denominator)))) - 1)
            # exact repair
            while not (x * lam ** k < 1):
                k += 1
            while k > 0 and x * lam ** (k - 1) < 1:
                k -= 1
        t = k * L + s
        if best is None or t < best[0]:
            best = (t, k, s)
    return best


def tstar_big(loop, p, i, G):
    """Same value as tstar, for long loops / large k.  A guess is computed with
    80-digit decimal logarithms; the answer is then CERTIFIED with exact integers:
    (1) G * P_i(t) * ... < 1 at the returned t, and (2) for every s in 1..L the largest
    k with kL + s < t still has G * P_i(s) * lam^k > 1 (monotone in k), so no earlier
    t descends.  Only exact integer comparisons decide; the decimals only guess."""
    import decimal
    decimal.getcontext().prec = 80
    L = len(loop)
    lam = loop_mult(loop, p)
    assert lam < 1
    P = prefix_products(loop, p, i)
    ln = lambda fr: decimal.Decimal(fr.numerator).ln() - decimal.Decimal(fr.denominator).ln()
    llam = -ln(lam)
    best = None
    for s in range(1, L + 1):
        x = G * P[s]
        k = 0 if x < 1 else max(0, int(ln(x) / llam))
        t = k * L + s
        if best is None or t < best[0]:
            best = (t, k, s)
    # exact repair/certification
    cache = {}

    def lamk(k):
        if k not in cache:
            cache[k] = (lam.numerator ** k, lam.denominator ** k)
        return cache[k]

    def below(s, k):          # G P[s] lam^k < 1, exact
        x = G * P[s]
        A, B = lamk(k)
        return x.numerator * A < x.denominator * B

    while True:
        t, k, s = best
        if not below(s, k):                       # guess too early: move on
            best = None
            for s2 in range(1, L + 1):
                k2 = k if s2 > s else k + 1
                while not below(s2, k2):
                    k2 += 1
                t2 = k2 * L + s2
                if best is None or t2 < best[0]:
                    best = (t2, k2, s2)
            continue
        # minimality: every (s', k') with k'L + s' < t stays >= 1
        bad = None
        for s2 in range(1, L + 1):
            kmax = (t - 1 - s2) // L
            if kmax >= 0 and below(s2, kmax):
                bad = (kmax * L + s2, kmax, s2)
                break
        if bad is None:
            return best
        best = bad


def max_loop_walk_product(loop, p, i=None):
    """max over loop walks (from rotation i, or from any rotation) of any length >= 0
    of the product.  Since lam < 1, walks longer than L only lose: the max is over
    lengths 0..L-1."""
    L = len(loop)
    rots = range(L) if i is None else [i]
    best = Fraction(1)
    for j in rots:
        P = prefix_products(loop, p, j)
        best = max(best, max(P[:L]))
    return best


def exit_gain(loop, p, h, uc, i0):
    """G_exit = max product of a walk that starts at a chain or loop node and ends with a
    dividing loop step (after which a reset node can be entered).  Exact.  Walks longer
    than one lap only lose a factor lam < 1, so lengths <= L suffice."""
    L = len(loop)
    best = Fraction(0)
    starts = [(i, Fraction(1)) for i in range(L)] + \
             [(i0, Fraction(uc) ** j) for j in range(1, h + 1)]
    for i, G in starts:
        P = prefix_products(loop, p, i)
        for s in range(1, L + 1):
            if loop[(i + s - 1) % L][1] >= 1:
                best = max(best, G * P[s])
    return best


def predicted(p, m, loop, h, uc, i0):
    """Theorem A1 data: (CERT?, k* formula value, G_exit).  CERT <=> lam < 1 and
    G_exit < Q (Theorem A1(i))."""
    Q = p ** m
    Gstar = exit_gain(loop, p, h, uc, i0)
    cert = Gstar < Q and loop_mult(loop, p) < 1
    t_chain = h + tstar(loop, p, i0, Fraction(uc) ** h)[0]
    t_loop = max(tstar(loop, p, i, Fraction(1))[0] for i in range(len(loop)))
    return cert, max(t_chain, t_loop), Gstar


def predicted_big(p, m, loop, h, uc, i0):
    """predicted() with tstar_big (exact certification, faster for long loops)."""
    Q = p ** m
    Gstar = exit_gain(loop, p, h, uc, i0)
    cert = Gstar < Q and loop_mult(loop, p) < 1
    t_chain = h + tstar_big(loop, p, i0, Fraction(uc) ** h)[0]
    t_loop = max(tstar_big(loop, p, i, Fraction(1))[0] for i in range(len(loop)))
    return cert, max(t_chain, t_loop), Gstar
