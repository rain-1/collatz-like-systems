"""Round 3, lens "density": the state graph of a table map, the s-weighted
transfer matrices, and exact (rational) density certificates.

Everything that enters a proof is exact (Fractions / Python ints).  numpy is
used ONLY to *search* for parameters (s, gamma) and to propose a weight vector;
every proposed certificate is then re-verified in exact rational arithmetic
with rigorous rational upper bounds for the irrational powers F^s and q^gamma.

Objects
-------
TableMap(name, Q, table): T(n) = (u n + v)/w for n = r (mod Q), table[r] = (u, v, w),
    exact division on every class.  The branch is a function of n mod Q.

build_graph(T) -> Graph: the finite "state graph" of the adaptive digit tree
    (see theory.md, Section 1).  A state is (K, beta): the reached value of a
    tree node is a*t + b with a = K * (unit prime to Q) and b = beta (mod K).
    From a state we split t by one prime q (q children, Haar weight 1/q each)
    and then apply every branch of T that the new residue information decides.
    An edge records q, the slope factor F (product of u/w), the intercept G
    (B -> F*B + G for the real intercept B), and the number of raw T-steps.

certify(T, s, gamma, c) -> exact certificate that
    sum_{edges sigma->sigma'} q^(gamma-1) * F^s * w(sigma') <= w(sigma)   (all sigma)
    with rational w > 0.  This is the supermartingale inequality of Theorem 1.
"""
from fractions import Fraction as Fr
from math import gcd, log
import math
import itertools

# ----------------------------------------------------------------- the map ---


def factor_primes(Q):
    ps, q, x = [], 2, Q
    while q * q <= x:
        if x % q == 0:
            ps.append(q)
            while x % q == 0:
                x //= q
        q += 1
    if x > 1:
        ps.append(x)
    return ps


def vp(x, p):
    if x == 0:
        return 10 ** 9
    k = 0
    while x % p == 0:
        x //= p
        k += 1
    return k


class TableMap:
    def __init__(self, name, Q, table, primes=None, rule=""):
        self.name, self.Q, self.table, self.rule = name, Q, list(table), rule
        self.primes = primes or factor_primes(Q)
        assert len(self.table) == Q
        for r, (u, v, w) in enumerate(self.table):
            assert w > 0 and u > 0
            # exact division on the whole class r mod Q
            assert (u * Q) % w == 0 and (u * r + v) % w == 0, (name, r)
            # w must be a product of the primes of Q
            x = w
            for p in self.primes:
                while x % p == 0:
                    x //= p
            assert x == 1, (name, r, w)

    def step(self, n):
        u, v, w = self.table[n % self.Q]
        x = u * n + v
        assert x % w == 0
        return x // w


# -------------------------------------------------------------- the graph ---

class Edge:
    __slots__ = ("src", "dst", "q", "digit", "F", "G", "steps")

    def __init__(self, src, dst, q, digit, F, G, steps):
        self.src, self.dst, self.q, self.digit = src, dst, q, digit
        self.F, self.G, self.steps = F, G, steps


class Graph:
    pass


def _decide(T, K, beta):
    """Return the table row if every residue r mod Q compatible with
    x = beta (mod K) uses the same row and the division is exact on the whole
    class beta mod K; otherwise None."""
    g = gcd(K, T.Q)
    rows = {T.table[r] for r in range(beta % g, T.Q, g)}
    if len(rows) != 1:
        return None
    (u, v, w), = rows
    if K % w or (u * beta + v) % w:
        return None
    return (u, v, w)


def _process(T, K, beta, maxsteps=10000):
    """Apply every decided branch.  Returns (K, beta, F, G, steps)."""
    F, G, steps = Fr(1), Fr(0), 0
    seen = set()
    while True:
        row = _decide(T, K, beta)
        if row is None:
            return K, beta, F, G, steps
        if (K, beta) in seen:
            raise ValueError("branch loop without new information at %r" % ((K, beta),))
        seen.add((K, beta))
        u, v, w = row
        # a -> u a / w ; the Q-part of the new a
        K2 = K * u // w
        keep = 1
        for p in T.primes:
            keep *= p ** vp(K2, p)
        K2 = keep
        beta = ((u * beta + v) // w) % K2
        K = K2
        F = F * Fr(u, w)
        G = G * Fr(u, w) + Fr(v, w)
        steps += 1
        if steps > maxsteps:
            raise ValueError("too many steps")


def _split_prime(T, K, beta):
    for q in T.primes:
        if vp(K, q) < vp(T.Q, q):
            return q
    # the branch is decided but the division is not exact: refine by a prime of w
    for q in T.primes:
        return q


def build_graph(T, max_states=5000):
    K0, b0, F0, G0, st0 = _process(T, 1, 0)
    assert st0 == 0, "root applies a branch: trivial map"
    root = (K0, b0)
    states, index, edges = [root], {root: 0}, []
    i = 0
    while i < len(states):
        K, beta = states[i]
        q = _split_prime(T, K, beta)
        for j in range(q):
            K1, b1, F, G, st = _process(T, K * q, (beta + K * j) % (K * q))
            key = (K1, b1)
            if key not in index:
                index[key] = len(states)
                states.append(key)
                if len(states) > max_states:
                    raise ValueError("state graph too large")
            edges.append(Edge(i, index[key], q, j, F, G, st))
        i += 1
    g = Graph()
    g.T, g.states, g.index, g.edges = T, states, index, edges
    g.out = [[e for e in edges if e.src == k] for k in range(len(states))]
    g.qs = [g.out[k][0].q for k in range(len(states))]
    g.Gmax = max(abs(e.G) for e in edges)
    g.Gmin = min(e.G for e in edges)
    g.qmax = max(g.qs)
    return g


# --------------------------------------------- exact stationary statistics ---

def _solve_fr(A, b):
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        inv = 1 / M[c][c]
        M[c] = [x * inv for x in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [x - f * y for x, y in zip(M[r], M[c])]
    return [M[i][n] for i in range(n)]


def closed_classes(g):
    """Strongly connected components with no exit (recurrent classes)."""
    n = len(g.states)
    adj = [set(e.dst for e in g.out[k]) for k in range(n)]
    reach = []
    for k in range(n):
        seen, st = {k}, [k]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in seen:
                    seen.add(y)
                    st.append(y)
        reach.append(seen)
    comps = []
    done = set()
    for k in range(n):
        if k in done:
            continue
        comp = {j for j in reach[k] if k in reach[j]}
        done |= comp
        if reach[k] == comp:
            comps.append(sorted(comp))
    return comps


def stationary(g, comp):
    """Exact stationary distribution of the digit chain on a closed class."""
    idx = {s: i for i, s in enumerate(comp)}
    m = len(comp)
    P = [[Fr(0)] * m for _ in range(m)]
    for s in comp:
        for e in g.out[s]:
            P[idx[s]][idx[e.dst]] += Fr(1, e.q)
    # pi (P - I) = 0, sum pi = 1
    A = [[P[j][i] - (1 if i == j else 0) for j in range(m)] for i in range(m)]
    A[-1] = [Fr(1)] * m
    b = [Fr(0)] * (m - 1) + [Fr(1)]
    pi = _solve_fr(A, b)
    return {s: pi[idx[s]] for s in comp}


def log_vector(x, primes):
    """x rational -> exponent dict over primes (exact)."""
    num, den = x.numerator, x.denominator
    out = {}
    for p in primes:
        a, b = vp(num, p), vp(den, p)
        num //= p ** a
        den //= p ** b
        if a - b:
            out[p] = a - b
    assert num == 1 and den == 1, x
    return out


def drift(g, comp=None):
    """Exact Lyapunov data on a closed class:
    Delta = E_pi sum_e (1/q) log F_e  and  Lambda = E_pi log q, as exact
    rational combinations of log p.  Returns (Delta_vec, Lambda_vec, floats)."""
    if comp is None:
        cc = closed_classes(g)
        assert len(cc) == 1, "several closed classes"
        comp = cc[0]
    pi = stationary(g, comp)
    allp = set(g.T.primes)
    for e in g.edges:
        for x in (e.F.numerator, e.F.denominator):
            allp |= set(factor_primes(x)) if x > 1 else set()
    allp = sorted(allp)
    D, L = {p: Fr(0) for p in allp}, {p: Fr(0) for p in allp}
    for s in comp:
        for e in g.out[s]:
            for p, a in log_vector(e.F, allp).items():
                D[p] += pi[s] * Fr(1, e.q) * a
        L[g.qs[s]] += pi[s]
    Df = sum(float(a) * log(p) for p, a in D.items())
    Lf = sum(float(a) * log(p) for p, a in L.items())
    D = {p: a for p, a in D.items() if a}
    L = {p: a for p, a in L.items() if a}
    return D, L, Df, Lf


# ------------------------------------------------------ rigorous powers ---

def iroot_ceil(N, k):
    """Smallest integer r >= 0 with r^k >= N."""
    if N <= 0:
        return 0
    r = int(round(N ** (1.0 / k))) if N < 1 << 1000 else 1 << ((N.bit_length() + k - 1) // k)
    # Newton downwards from an upper bound
    if r ** k < N:
        r = 1 << ((N.bit_length() + k - 1) // k)
    while True:
        r2 = ((k - 1) * r + N // r ** (k - 1)) // k
        if r2 >= r:
            break
        r = r2
    while r ** k < N:
        r += 1
    while r > 0 and (r - 1) ** k >= N:
        r -= 1
    return r


def iroot_floor(N, k):
    r = iroot_ceil(N, k)
    return r if r ** k == N else r - 1


def _flog(x):
    x = Fr(x)
    return math.log(x.numerator) - math.log(x.denominator)


def upow(x, r, bits=36):
    """Rational U >= x^r for rational x > 0 and rational r (any sign).
    The candidate comes from floating point; the inequality U^b >= x^a
    (r = a/b) is then verified with exact integers, so U is rigorous."""
    x, r = Fr(x), Fr(r)
    if r < 0:
        x, r = 1 / x, -r
    if r == 0 or x == 1:
        return Fr(1)
    a, b = r.numerator, r.denominator
    f = math.exp(float(r) * _flog(x))
    y = Fr(f) * (1 + Fr(1, 1 << bits))
    while y.numerator ** b * x.denominator ** a < x.numerator ** a * y.denominator ** b:
        y *= 1 + Fr(1, 1 << (bits // 2))
    return y


def lpow(x, r, bits=36):
    """Rational L <= x^r (verified exactly as in upow)."""
    x, r = Fr(x), Fr(r)
    if r < 0:
        x, r = 1 / x, -r
    if r == 0 or x == 1:
        return Fr(1)
    a, b = r.numerator, r.denominator
    f = math.exp(float(r) * _flog(x))
    y = Fr(f) * (1 - Fr(1, 1 << bits))
    while y.numerator ** b * x.denominator ** a > x.numerator ** a * y.denominator ** b:
        y *= 1 - Fr(1, 1 << (bits // 2))
    return y


# ------------------------------------------- float search (heuristic only) ---

def _np():
    import numpy as np
    return np


def float_matrix(g, s, gamma):
    np = _np()
    n = len(g.states)
    N = np.zeros((n, n))
    for e in g.edges:
        N[e.src, e.dst] += float(e.q) ** (gamma - 1.0) * float(e.F) ** s
    return N


def rho(g, s, gamma):
    np = _np()
    ev = np.linalg.eigvals(float_matrix(g, s, gamma))
    return float(max(abs(ev)))


def gamma_star(g, s, lo=-60.0, hi=4.0, it=90):
    """sup{gamma : rho(N_{s,gamma}) <= 1} (rho is increasing in gamma)."""
    if rho(g, s, hi) <= 1:
        return hi
    if rho(g, s, lo) > 1:
        return lo
    for _ in range(it):
        mid = (lo + hi) / 2
        if rho(g, s, mid) <= 1:
            lo = mid
        else:
            hi = mid
    return lo


def optimize(g, c=1.0, sign=+1, smax=None):
    if smax is None:
        smax = 12.0 if sign > 0 else 4.0
    """Maximize phi(s) = gamma*(s) - s(1-c) over s with sign(s) = sign.
    phi is concave (theory.md, Lemma 3), so golden-section search is valid as
    a heuristic.  Returns (s, gamma*(s), theta = 1 - phi(s))."""
    f = lambda t: gamma_star(g, sign * t) - sign * t * (1 - c)
    a, b = 1e-6, smax
    gr = (5 ** 0.5 - 1) / 2
    x1, x2 = b - gr * (b - a), a + gr * (b - a)
    f1, f2 = f(x1), f(x2)
    for _ in range(70):
        if f1 < f2:
            a, x1, f1 = x1, x2, f2
            x2 = a + gr * (b - a)
            f2 = f(x2)
        else:
            b, x2, f2 = x2, x1, f1
            x1 = b - gr * (b - a)
            f1 = f(x1)
    t = (a + b) / 2
    return sign * t, gamma_star(g, sign * t), 1 - f(t)


# ------------------------------------------------- exact certificates ---

class Certificate:
    pass


def check_supermartingale(g, s, gamma, w, bits=36):
    """Exact check of  sum_e U(q^(gamma-1)) U(F^s) w(dst) <= w(src)  for all
    states.  Returns the worst ratio (as a Fraction) or None if it fails."""
    worst = Fr(0)
    cache = {}

    def U(x, r):
        k = (x, r)
        if k not in cache:
            cache[k] = upow(x, r, bits)
        return cache[k]
    for k in range(len(g.states)):
        tot = Fr(0)
        for e in g.out[k]:
            tot += U(Fr(e.q), gamma - 1) * U(e.F, s) * w[e.dst]
        ratio = tot / w[k]
        worst = max(worst, ratio)
        if tot > w[k]:
            return None
    return worst


def propose_weights(g, s, gamma, den=10 ** 9):
    """w = (I - N)^{-1} 1 for N = N_{s,gamma} (needs rho < 1), rationalised."""
    np = _np()
    N = float_matrix(g, float(s), float(gamma))
    n = len(g.states)
    w = np.linalg.solve(np.eye(n) - N, np.ones(n))
    if not all(x > 0 for x in w):
        return None
    m = max(w)
    return [Fr(float(x / m)).limit_denominator(den) for x in w]


def certify(g, s, gamma, bits=36):
    """Find rational w with the exact supermartingale inequality at (s, gamma).
    s, gamma are Fractions.  Raises if it cannot."""
    s, gamma = Fr(s), Fr(gamma)
    for slack in (0.0, 1e-9, 1e-7, 1e-5, 1e-4, 1e-3):
        w = propose_weights(g, float(s), float(gamma) + slack)
        if w is None:
            continue
        if min(w) <= 0:
            continue
        r = check_supermartingale(g, s, gamma, w, bits)
        if r is not None:
            C = Certificate()
            C.s, C.gamma, C.w, C.worst = s, gamma, w, r
            C.w0, C.wmin = w[0], min(w)
            return C
    raise ValueError("certificate failed at s=%s gamma=%s" % (s, gamma))


def simple_rational_in(lo, hi):
    """The rational with the smallest denominator in [lo, hi] (lo < hi floats)."""
    den = 1
    while True:
        num = math.floor(hi * den)
        if Fr(num, den) >= Fr(lo):
            return Fr(num, den)
        den += 1


def rational_below(x, den=10000):
    """A simple rational strictly below the float x."""
    f = Fr(int(x * den) - 1, den)
    return f


def best_certificate(g, c=Fr(1), sign=+1, den=200):
    """Search (float) the optimal s, then certify a rational gamma just below
    gamma*(s).  Returns (cert, theta_bar) with theta_bar = 1 - gamma + s(1-c)
    an exact rational upper bound for the exponent."""
    s_f, g_f, th_f = optimize(g, float(c), sign)
    s = Fr(s_f).limit_denominator(den)
    if s == 0:
        s = Fr(sign, den)
    gs = gamma_star(g, float(s))
    gamma = simple_rational_in(gs - 3e-6, gs - 2e-7)
    C = certify(g, s, gamma)
    C.c = Fr(c)
    C.theta = 1 - gamma + s * (1 - Fr(c))
    C.theta_float_opt = th_f
    C.s_float_opt = s_f
    return C


# ---------------------------------------------- explicit H(X) constants ---

def never_drop_constants(g, C, cth=Fr(1, 2)):
    """Theorem 1 constants: H(X) <= 2^k0 + C1 * X^theta for all X >= 1, where
    theta = 1 - gamma (C.c must be 1).  Returns (k0, C1) with C1 an exact
    rational upper bound."""
    assert C.c == 1 and 0 <= C.gamma <= 1 and C.s > 0
    th = C.theta
    k0 = 0
    while not ((1 - cth) * 2 ** k0 > k0 * g.Gmax and
               all((1 - cth) * 2 ** k > k * g.Gmax for k in range(k0, k0 + 200))):
        k0 += 1
    # (1-c)2^k > k Gmax is monotone once true for k >= k0 and 2^k grows faster;
    # the 200-step look-ahead plus monotonicity of 2^k / k for k >= 2 make it exact.
    Kc = C.w0 * upow(g.qmax, th) * upow(cth, -C.s) / C.wmin
    two_th_lo = lpow(2, th)
    C1 = Kc * upow(2, th) / (two_th_lo - 1)
    return k0, C1


# ------------------------------------------- concrete tree (verification) ---

def concrete_tree(g, depth, step=None):
    """Build the actual integer digit tree to the given depth and check that it
    follows the state graph exactly.  Yields nodes
    (depth, M, r, a, b, state, A, B, ksteps) where T^ksteps(M t + r) = a t + b
    for all t >= 0, A = a/M, B = b - a r / M."""
    T = g.T
    step = step or T.step
    root = (0, 1, 0, 1, 0, 0, Fr(1), Fr(0), 0)
    stack = [root]
    while stack:
        node = stack.pop()
        yield node
        d, M, r, a, b, st, A, B, ks = node
        if d == depth:
            continue
        K, beta = g.states[st]
        # invariant checks
        assert a % K == 0 and b % K == beta % K
        unit = a // K
        assert all(unit % p for p in T.primes)
        assert A == Fr(a, M) and B == b - Fr(a * r, M)
        for e in g.out[st]:
            q = e.q
            # digit j of the *graph* edge corresponds to value residue
            # beta + K j (mod qK); find the t-digit e_t with b + a e_t = beta + K j
            target = (beta + K * e.digit) % (K * q)
            et = next(x for x in range(q) if (b + a * x) % (K * q) == target)
            M2, r2 = M * q, r + M * et
            a2, b2 = a * q, b + a * et
            # apply the edge's branches with exact integers
            x_a, x_b = a2, b2
            for _ in range(e.steps):
                u, v, w = T.table[x_b % T.Q]
                assert (u * x_a) % w == 0 and (u * x_b + v) % w == 0
                x_a, x_b = u * x_a // w, (u * x_b + v) // w
            A2, B2 = A * e.F, B * e.F + e.G
            assert Fr(x_a, M2) == A2, (T.name, d)
            assert x_b - Fr(x_a * r2, M2) == B2
            stack.append((d + 1, M2, r2, x_a, x_b, e.dst, A2, B2, ks + e.steps))


def iterate(step, n, k):
    for _ in range(k):
        n = step(n)
    return n


# ------------------------------------------------------ paths of integers ---

def path_of(g, n, Y):
    """Follow the integer n down the concrete tree until the node modulus M is
    >= Y (the 'cut node' of Theorem 1).  Returns the list of nodes
    (depth, M, r, a, b, state, ksteps) from the root to the cut node."""
    T = g.T
    M, r, a, b, st, ks, d = 1, 0, 1, 0, 0, 0, 0
    out = [(0, M, r, a, b, st, ks)]
    while M < Y:
        K, beta = g.states[st]
        q = g.qs[st]
        et = ((n - r) // M) % q
        val = (b + a * et) % (K * q)
        j = ((val - beta) // K) % q
        e = g.out[st][j]
        assert e.digit == j
        M, r, a, b = M * q, r + M * et, a * q, b + a * et
        for _ in range(e.steps):
            u, v, w = T.table[b % T.Q]
            a, b = u * a // w, (u * b + v) // w
        st, ks, d = e.dst, ks + e.steps, d + 1
        out.append((d, M, r, a, b, st, ks))
    return out


# ------------------------------------------- exact walks on the slope ---

def _primes_of_F(g):
    ps = set(g.T.primes)
    for e in g.edges:
        for x in (e.F.numerator, e.F.denominator):
            if x > 1:
                ps |= set(factor_primes(x))
    return sorted(ps)


def _A_of(key, ps):
    num = den = 1
    for p, a in zip(ps, key):
        if a > 0:
            num *= p ** a
        elif a < 0:
            den *= p ** (-a)
    return num, den


def slope_walk(g, L, floor_num=1, floor_den=1):
    """Exact enumeration of the digit tree by (state, exponent vector of A),
    for a SINGLE-PRIME map (all q equal to p).  Paths are killed at the first
    node with A < floor (= floor_num/floor_den).  Returns
      killed[i] = number of depth-i nodes killed at depth i (first crossing),
      alive     = dict (state, exps) -> number of depth-L nodes never killed,
      alive_count[i] = number of alive depth-i nodes.
    Counts are integers; the Haar measure of a depth-i node is p^-i."""
    ps = _primes_of_F(g)
    p = g.qs[0]
    assert all(q == p for q in g.qs)
    ev = [(e.src, e.dst, tuple(log_vector(e.F, ps).get(x, 0) for x in ps)) for e in g.edges]
    cur = {(0, tuple(0 for _ in ps)): 1}
    killed, alive_count = [0], [1]
    for i in range(1, L + 1):
        nxt = {}
        k = 0
        for (st, ex), cnt in cur.items():
            for (s0, d0, dv) in ev:
                if s0 != st:
                    continue
                ex2 = tuple(a + b for a, b in zip(ex, dv))
                num, den = _A_of(ex2, ps)
                if num * floor_den < floor_num * den:
                    k += cnt
                else:
                    key = (d0, ex2)
                    nxt[key] = nxt.get(key, 0) + cnt
        cur = nxt
        killed.append(k)
        alive_count.append(sum(cur.values()))
    return killed, cur, alive_count, ps, p


def early_drop_bounds(g, L, s, w):
    """Rigorous bounds lo <= q <= hi for q = Haar measure of the paths whose
    slope ever falls below 1.  (s < 0, w) must satisfy the exact inequality
    sum_e (1/q) F^s w(dst) <= w(src) (checked here)."""
    s = Fr(s)
    assert s < 0
    # exact supermartingale check with gamma = 0
    assert check_supermartingale(g, s, Fr(0), w) is not None
    killed, alive, _, ps, p = slope_walk(g, L)
    lo = sum(Fr(k, p ** i) for i, k in enumerate(killed))
    wmin = min(w)
    tail = Fr(0)
    cache = {}
    for (st, ex), cnt in alive.items():
        if ex not in cache:
            num, den = _A_of(ex, ps)
            cache[ex] = upow(Fr(num, den), s)
        tail += cnt * cache[ex] * w[st]
    tail = tail / (p ** L * wmin)
    return lo, lo + tail
