"""Second independent referee check (round-3 referee pass 2) for census/round3/polynomial.

Written from scratch; imports nothing from this folder except systems.py (whose step functions
are themselves tested against the written rules in part S).  Exact arithmetic only.
Runtime: about 1 minute.

  S   systems.py steps == rules as written (random inputs, deg <= 250)
  A   Theorem A: exhaustive functional graph, all odd h with deg h <= 7, all f with deg f <= 10
  B   Theorem B: brute-force periodic points over F_3 (deg<9), F_5 (deg<5), F_4 (deg<4, g1=w),
      F_7 (deg<7 sampled + count via Newton bijection), twists a=1,2
  C   Theorem C identity (random large), C1 for k<=8, Prop C' on random (m,h) satisfying (i),(ii);
      the 'special case' m=M^2,h=H^2 (violates (i), checked to hold anyway)
  D   every line certificate re-derived with a fresh Phi over F_p[X]; D2 symbolic for k<=5,
      D3 for k<=6; two-point D0, D4 checked by exact rational power-series simulation and by
      direct polynomial simulation; extra: 1+t^4, h=1 divergence via squared D0 orbit
  N1  s/L = 1/deg g on every polynomial cycle reached from all seeds deg<=9 (h=1)
"""
import random, sys, os
from math import comb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
random.seed(20261127)
FAILS = []


def check(cond, tag, msg=''):
    if not cond:
        FAILS.append((tag, msg))
        print('  FAIL', tag, msg)


# ---------------------------------------------------------------- F_2 as ints
def m2(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        b >>= 1
    return r


def d2(a, b):
    q, db = 0, b.bit_length()
    while a.bit_length() >= db:
        s = a.bit_length() - db
        q ^= 1 << s
        a ^= b << s
    return q, a


def p2(a, e):
    r = 1
    while e:
        if e & 1:
            r = m2(r, a)
        a = m2(a, a)
        e >>= 1
    return r


def sub2(a, N):
    r, i = 0, 0
    while a:
        if a & 1:
            r |= 1 << (i * N)
        a >>= 1
        i += 1
    return r


def T2(f, g, h):
    if f & 1:
        x = m2(g, f) ^ h
        assert x & 1 == 0
        return x >> 1
    return f >> 1


# ---------------------------------------------------------------- F_p as lists (low first)
def tr(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a


def addp(a, b, p):
    n = max(len(a), len(b))
    return tr([((a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)) % p for i in range(n)])


def mulp(a, b, p):
    if not a or not b:
        return []
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] = (r[i + j] + x * y) % p
    return tr(r)


def powp(a, e, p):
    r = [1]
    for _ in range(e):
        r = mulp(r, a, p)
    return r


def scp(c, a, p):
    return tr([(c * x) % p for x in a])


def subsp(a, N):
    if not a:
        return []
    r = [0] * ((len(a) - 1) * N + 1)
    for i, x in enumerate(a):
        r[i * N] = x
    return r


def divp(a, b, p):
    a = list(a)
    inv = pow(b[-1], p - 2, p)
    q = [0] * max(0, len(a) - len(b) + 1)
    while len(a) >= len(b) and a:
        c = a[-1] * inv % p
        s = len(a) - len(b)
        q[s] = c
        for i, y in enumerate(b):
            a[s + i] = (a[s + i] - c * y) % p
        a = tr(a)
    return tr(q), a


def Tp(f, g, h, p):
    if not f or f[0] == 0:
        return f[1:] if f else []
    x = addp(mulp(g, f, p), scp(-g[0] * f[0], h, p), p)
    assert x[0] == 0
    return x[1:]


# ================================================================ S
print('S: systems.py vs written rules')
import systems as SY
rules = {  # id: (p, g, h) as written in README / .md
    'p2_onept_h7': (2, [1, 1], [1, 1, 1]), 'p3_st': (3, [1, 1], [1]),
    'p2_t3': (2, [1, 0, 0, 1], [1]), 'p2_cube': (2, [1, 1, 1, 1], [1]),
    'p2_tri_k': (2, [1, 1, 0, 1], [1, 1, 1]), 'p2_crit': (2, [1, 1, 1], [1, 1, 1, 0, 0, 1]),
    'p2_ML': (2, [1, 0, 1], [1]), 'p3_a': (3, [2, 0, 1], [1, 1, 2]), 'p3_b': (3, [1, 1, 1], [1, 0, 1]),
    'p3_c': (3, [1, 0, 2], [1, 2, 2]), 'p3_d': (3, [2, 1, 2], [1, 0, 1]),
    'p2_sq111': (2, [1, 0, 1, 0, 1], [1, 1, 1, 0, 1]), 'p2_1034': (2, [1, 0, 0, 1, 1], [1, 1, 0, 1, 1]),
    'p2_nichols': (2, [1, 1, 1], [1]), 'p2_m3b_h1': (2, [1, 1, 0, 1], [1]), 'p2_m3c_h1': (2, [1, 0, 1, 1], [1])}
for S in SY.SYSTEMS:
    if S['step'] is None:
        continue
    check(S['id'] in rules, 'S', 'no written rule for ' + S['id'])
    p, g, h = rules[S['id']]
    for _ in range(300):
        d = random.randint(0, 250)
        f = tr([random.randrange(p) for _ in range(d + 1)])
        if p == 2:
            fi = sum(c << i for i, c in enumerate(f))
            exp = Tp(f, g, h, 2)
            got = S['step'](fi)
            check(got == sum(c << i for i, c in enumerate(exp)), 'S', S['id'])
        else:
            got = S['step'](tuple(f))
            check(tr(got) == Tp(f, g, h, p), 'S', S['id'])

# ================================================================ A
print('A: Theorem A exhaustive (deg h <= 7, deg f <= 10) and random large')


def ordt1(h):  # (a, k) with h = (1+t)^a k
    a = 0
    while True:
        q, r = d2(h, 3)
        if r:
            return a, h
        h, a = q, a + 1


def cycles_of(g, h, maxdeg):
    n = 1 << (maxdeg + 1)
    nxt = [T2(f, g, h) for f in range(n)]
    for f in range(n):
        assert nxt[f] < n
    state = [0] * n  # 0 unvisited 1 in progress 2 done
    oncyc = [False] * n
    for s in range(n):
        path = []
        x = s
        while state[x] == 0:
            state[x] = 1
            path.append(x)
            x = nxt[x]
        if state[x] == 1:
            i = path.index(x)
            for y in path[i:]:
                oncyc[y] = True
        for y in path:
            state[y] = 2
    return nxt, oncyc


nh = 0
for h in range(1, 1 << 8, 2):
    a, k = ordt1(h)
    dh = h.bit_length() - 1
    D = max(10, dh)
    nxt, oncyc = cycles_of(3, h, D)
    n = len(nxt)
    # (2)
    for f in range(n):
        check((d2(f, k)[1] == 0) == (d2(nxt[f], k)[1] == 0), 'A2', (h, f))
    cyc = [f for f in range(n) if oncyc[f]]
    # (5) cycles other than 0,h in degree < deg h and avoid multiples of k
    for f in cyc:
        if f not in (0, h):
            check(f.bit_length() - 1 < dh, 'A5deg', (h, f))
            check(d2(f, k)[1] != 0, 'A5k', (h, f))
    check(oncyc[0] and oncyc[h], 'A1fix', h)
    # (6)
    extra = [f for f in cyc if f not in (0, h)]
    check((not extra) == (k == 1), 'A6', (h, extra[:3]))
    # (3),(4),(7): fate of every f
    fate = {}
    for f in range(1, n):
        x, seen = f, 0
        while not oncyc[x]:
            x = nxt[x]
        # x on cycle: reaches {0,h}?
        reach = x in (0, h)
        check(reach == (d2(f, k)[1] == 0), 'A34', (h, f))
        if a == 0:
            check(x != 0, 'A7zero', (h, f))
            check((x == h) == (d2(f, h)[1] == 0), 'A7', (h, f))
    nh += 1
print('   %d twists h checked' % nh)
# random large (2),(7)
for _ in range(2000):
    h = random.getrandbits(random.randint(1, 30)) | 1
    a, k = ordt1(h)
    f = random.getrandbits(random.randint(1, 300))
    check((d2(f, k)[1] == 0) == (d2(T2(f, 3, h), k)[1] == 0), 'A2r')
    if a == 0:
        u = random.getrandbits(80) | 1
        x = m2(u, h)
        for _ in range(4000):
            if x == h:
                break
            x = T2(x, 3, h)
        check(x == h, 'A7r', (h, u))
# p2_onept_h7 explicit cycle list
nxt, oncyc = cycles_of(3, 7, 12)
check(sorted(f for f in range(len(nxt)) if oncyc[f]) == [0, 1, 2, 7], 'Ah7', 'cycle list')

# ================================================================ B
print('B: Theorem B brute force')


class GF:  # F_q, q = p or 4
    def __init__(self, q):
        self.q = q
        if q == 4:
            # elements 0..3 as bit pairs a+b w, w^2=w+1
            def mul(x, y):
                a0, a1, b0, b1 = x & 1, x >> 1, y & 1, y >> 1
                c0 = (a0 & b0) ^ (a1 & b1)
                c1 = (a0 & b1) ^ (a1 & b0) ^ (a1 & b1)
                return c0 | (c1 << 1)
            self.mul = mul
            self.add = lambda x, y: x ^ y
            self.neg = lambda x: x
            self.p = 2
        else:
            self.mul = lambda x, y: x * y % q
            self.add = lambda x, y: (x + y) % q
            self.neg = lambda x: (-x) % q
            self.p = q

    def pmul(self, a, b):
        if not a or not b:
            return []
        r = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            for j, y in enumerate(b):
                r[i + j] = self.add(r[i + j], self.mul(x, y))
        return tr(r)

    def padd(self, a, b):
        n = max(len(a), len(b))
        return tr([self.add(a[i] if i < len(a) else 0, b[i] if i < len(b) else 0) for i in range(n)])

    def step(self, f, g, H):
        if not f or f[0] == 0:
            return tuple(f[1:])
        c = self.neg(self.mul(g[0], f[0]))
        x = self.padd(self.pmul(g, list(f)), [self.mul(c, y) for y in H])
        assert not x or x[0] == 0
        return tuple(x[1:])


def all_polys(q, n):
    if n == 0:
        yield ()
        return
    for rest in all_polys(q, n - 1):
        for c in range(q):
            yield tr(rest + (c,)) if False else rest + (c,)


def periodic_set(K, g, H, n):
    pts = [tr(x) for x in all_polys(K.q, n)]
    pts = [tuple(x) for x in pts]
    S = set(pts)
    nxt = {}
    for x in S:
        y = K.step(list(x), g, H)
        nxt[x] = y
    # periodic: iterate image
    cur = set(S)
    while True:
        new = {nxt[x] for x in cur if nxt[x] in S}
        # restrict to closed part (bounded degree is invariant here)
        if new == cur:
            return cur, nxt
        cur = new


def newton(K, g0, g1, f, n):
    # v_n = sum C(n,i) g1^(n-i) g0^i a_i, via the operator recursion (no binomials): const of A^n f
    out = []
    x = list(f)
    for _ in range(n):
        out.append(x[0] if x else 0)
        # A x = g1 x + g0 Delta x
        dx = x[1:]
        x = K.padd([K.mul(g1, c) for c in x], [K.mul(g0, c) for c in dx])
    return out


cases = [(3, (1, 1), 2), (3, (2, 1), 2), (3, (1, 2), 2), (3, (2, 2), 2), (5, (1, 1), 1), (5, (2, 3), 1),
         (4, (1, 2), 2), (4, (3, 1), 2), (4, (1, 1), 2), (2, (1, 1), 4)]
for q, g, e in cases:
    K = GF(q)
    pe = K.p ** e
    g = list(g)
    per, nxt = periodic_set(K, g, [1], pe)
    nz = [x for x in per if any(x)]
    check(len(nz) == (q - 1) ** pe, 'Bcount', (q, g, len(nz)))
    for x in all_polys(q, pe):
        x = tuple(tr(x))
        v = newton(K, g[0], g[1], x, pe)
        isper = x in per
        if any(x):
            check(isper == all(c != 0 for c in v), 'Bcrit', (q, g, x))
    # period = least period of the extended Newton sequence
    for x in list(nz)[:200]:
        L, y = 1, nxt[x]
        while y != x:
            y, L = nxt[y], L + 1
        v = newton(K, g[0], g[1], x, 6 * pe * 3)
        lp = next(j for j in range(1, len(v)) if all(v[i] == v[i + j] for i in range(len(v) - j)))
        check(lp == L, 'Bper', (q, g, x, L, lp))
    print('   q=%d g=%s: %d nonzero periodic of deg<%d' % (q, g, len(nz), pe))
# twisted a = 1, 2 over F_3: periodic points of degree < 9+a are pi^a * (periodic of S_0, deg < 9)
K = GF(3)
for g in [(1, 1), (2, 1)]:
    g = list(g)
    inv = pow(g[0], 1, 3) if False else (1 if g[0] == 1 else 2)
    pi = [1, g[1] * inv % 3]
    per0, _ = periodic_set(K, g, [1], 6)
    for a in (1, 2):
        H = [1]
        for _ in range(a):
            H = K.pmul(H, pi)
        per, _ = periodic_set(K, g, H, 6 + a)
        exp = {tuple(K.pmul(H, list(u))) for u in per0}
        exp.add(())
        nzper = {x for x in per if any(x)}
        nzexp = {x for x in exp if any(x)}
        check(nzper == nzexp, 'Btw', (g, a, len(nzper), len(nzexp)))
# F_7 sampled: random nowhere-zero words of length 7 -> periodic, word with a zero -> not
K = GF(7)
for _ in range(200):
    g = [random.randint(1, 6), random.randint(1, 6)]
    # invert triangular map: choose coefficients a_n so that v_n = target
    w = [random.randint(1, 6) for _ in range(7)]
    zero = random.random() < 0.3
    if zero:
        w[random.randrange(7)] = 0
    a = []
    for n in range(7):
        s = sum(comb(n, i) * pow(g[1], n - i, 7) * pow(g[0], i, 7) * a[i] for i in range(n)) % 7
        a.append((w[n] - s) * pow(pow(g[0], n, 7), 5, 7) % 7)
    f = tuple(a)
    check(newton(K, g[0], g[1], f, 7) == w, 'B7newton')
    x, ok = f, True
    for j in range(7 * 6):
        x = K.step(list(x), g, [1])
    check((tuple(tr(x)) == tuple(tr(f))) == (not zero), 'B7per', (g, w))

# ================================================================ C
print('C: Theorem C, C1, Prop C\'')


def phi(M, u):
    return sub2(m2(M, u), 2)


def evod(a):
    e = o = 0
    i = 0
    while a:
        if a & 1:
            e |= 1 << i
        if a & 2:
            o |= 1 << i
        a >>= 2
        i += 1
    return e, o


for _ in range(400):
    M = random.getrandbits(random.randint(1, 9)) | 1
    if M == 1:
        M = 3
    m = sub2(M, 2) ^ 2
    u = random.getrandbits(random.randint(1, 400))
    lhs = T2(T2(phi(M, u), m, 1), m, 1)
    check(lhs == phi(M, T2(u, m, 1)), 'C', (M, u))
    if u:
        y = T2(phi(M, u), m, 1)
        check(evod(y)[1] != 0, 'Cnonsq', (M, u))
# C1: period of (1+t)^(2^(k+1)-2) under 1+t+t^2, h=1
for k in range(9):
    x0 = p2(3, 2 ** (k + 1) - 2)
    x, L = T2(x0, 7, 1), 1
    while x != x0 and L <= 2 ** (k + 3):
        x, L = T2(x, 7, 1), L + 1
    check(L == 2 ** (k + 2), 'C1', (k, L))
# Prop C': random (m,h) satisfying m(0)=h(0)=1, (i), (ii)
cnt = 0
while cnt < 300:
    me = random.getrandbits(random.randint(1, 8)) | 1
    mo = random.getrandbits(random.randint(1, 8))
    ho = random.getrandbits(random.randint(1, 8))
    if ((mo ^ ho) & 1) != 1:
        continue
    # (ii): he*(1+mo) = me*ho -> he = me*ho/(1+mo) must be polynomial with he(0)=1
    q, r = d2(m2(me, ho), mo ^ 1) if (mo ^ 1) else (None, 1)
    if r or q is None or not (q & 1):
        continue
    he = q
    m = sub2(me, 2) ^ (sub2(mo, 2) << 1)
    h = sub2(he, 2) ^ (sub2(ho, 2) << 1)
    hp = (m2(m2(mo ^ 1, ho), 1) << 1) ^ m2(me, he)
    hp = (m2(mo ^ 1, ho) << 1) ^ m2(me, he)
    for _ in range(5):
        A = random.getrandbits(random.randint(1, 200))
        check(T2(T2(sub2(A, 2), m, h), m, h) == sub2(T2(A, m, hp), 2), 'Cprime', (m, h, A))
    cnt += 1
# special case m=M^2, h=H^2: (i) fails (m_o = h_o = 0), identity still holds
for _ in range(300):
    M = random.getrandbits(random.randint(1, 8)) | 1
    H = random.getrandbits(random.randint(1, 8)) | 1
    F = random.getrandbits(random.randint(1, 200))
    check(T2(T2(sub2(F, 2), sub2(M, 2), sub2(H, 2)), sub2(M, 2), sub2(H, 2)) == sub2(T2(F, M, H), 2), 'Csq')

# ================================================================ D
print('D: line certificates (fresh Phi), two-point, direct simulation')


def Phi(P, g, p):
    lam = P[0] if P else 0
    R = addp(P, [(-lam) % p], p)
    v = next(i for i, c in enumerate(R) if c)
    R = R[v:]
    if lam:
        R = mulp(powp(g, v, p), R, p)
    return addp([lam], R, p), v


def line(g, h, P, p, kmax=60):
    Q, taus = list(P), []
    for _ in range(kmax):
        Q, v = Phi(Q, g, p)
        taus.append(v)
        b = 1
        while (len(P) - 1) * p ** b <= len(Q) - 1:
            if Q == subsp(P, p ** b):
                return len(taus), b, sum(taus)
            b += 1
    return None


def rho_fN(g, h, P, N, p):
    num = mulp(scp(g[0], h, p), subsp(P, N), p)
    den = addp(g, [0, p - 1], p)
    q, r = divp(num, den, p)
    return q if not r else None


LINE = [  # id, p, g, h, P, expected (k?, b, tau)
    ('p2_t3', 2, [1, 0, 0, 1], [1], [1, 0, 0, 0, 0, 0, 1, 0, 0, 1], 1, 18),
    ('p3_a', 3, [2, 0, 1], [1, 1, 2], [1, 0, 1], 1, 8),
    ('p3_b', 3, [1, 1, 1], [1, 0, 1], [0, 1, 1, 2], 1, 8),
    ('p3_c', 3, [1, 0, 2], [1, 2, 2], [1, 0, 1], 1, 8),
    ('p3_d', 3, [2, 1, 2], [1, 0, 1], [0, 1, 2, 2], 2, 32),
    ('p2_sq111', 2, [1, 0, 1, 0, 1], [1, 1, 1, 0, 1], [1, 1], None, 3),
    ('p2_1034', 2, [1, 0, 0, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1], None, 2),
]
for K_ in range(1, 6):
    Kk = 2 ** K_
    g = [1 if i in (0,) or comb(Kk + 1, i) % 2 else 0 for i in range(Kk + 2)]
    g = tr([comb(Kk + 1, i) % 2 for i in range(Kk + 2)])
    w = addp(g, [0, 1], 2)
    LINE.append(('p2_cube_k%d' % K_, 2, g, [1], w, K_, Kk * Kk + Kk))
for K_ in range(1, 7):
    Kk = 2 ** K_
    g = [0] * (Kk + 2)
    g[0] = g[1] = g[Kk + 1] = 1
    LINE.append(('p2_tri_k%d' % K_, 2, g, [1] * (Kk + 1), [1, 1], K_, 2))
for name, p, g, h, P, bexp, tauexp in LINE:
    r = line(g, h, P, p)
    check(r is not None, 'Dline', name)
    if r is None:
        continue
    k, b, tau = r
    check(tau == tauexp and (bexp is None or b == bexp), 'Dtau', (name, k, b, tau))
    # polynomiality for N = p^n: f_N = rho P(t^N); checked n=0..; rad criterion exact
    nsim = 0
    n = 0
    degs = []
    while True:
        N = p ** n
        f = rho_fN(g, h, P, N, p)
        check(f is not None, 'Dpoly', (name, N))
        f2 = rho_fN(g, h, P, N * p ** b, p)
        if len(f2) > 2500:
            break
        x = f
        if p == 2:
            xi = sum(c << i for i, c in enumerate(x))
            gi = sum(c << i for i, c in enumerate(g))
            hi = sum(c << i for i, c in enumerate(h))
            for _ in range(tau * N):
                xi = T2(xi, gi, hi)
            check(xi == sum(c << i for i, c in enumerate(f2)), 'Dsim', (name, N))
        else:
            for _ in range(tau * N):
                x = Tp(x, g, h, p)
            check(x == f2, 'Dsim', (name, N))
        degs.append(len(f) - 1)
        nsim += 1
        n += b
    check(all(degs[i] < degs[i + 1] for i in range(len(degs) - 1)), 'Ddeg', name)
    print('   %-12s k=%d b=%d tau=%d  sims=%d degs=%s' % (name, k, b, tau, nsim, degs[:5]))
# polynomiality for ALL N in p2_t3: 1+X^6+X^9 divisible by 1+X+X^3 in F_2[X]
check(d2(1 | (1 << 6) | (1 << 9), 0b1011)[1] == 0, 'D1fac')
# D2 polynomiality for all N: f_N = w^(N-1)  (rho = 1/w, P = w(X), Frobenius)
# p2_cube closed form k=1
for n in range(1, 8):
    x = 1
    for _ in range(6 * (2 ** n - 1)):
        x = T2(x, 0b1111, 1)
    check(x == p2(0b1101, 2 ** n - 1), 'D2closed', n)


# ---- two-point via exact rational power series over F_2 (num, den) with den(0)=1
def rnorm(a, b):
    def g2(x, y):
        while y:
            x, y = y, d2(x, y)[1]
        return x
    c = g2(a, b)
    return d2(a, c)[0], d2(b, c)[0]


def That(x, g, h):
    a, b = x
    if a & 1:
        a = m2(g, a) ^ m2(h, b)
    assert a & 1 == 0
    return rnorm(a >> 1, b)


def radd(x, y):
    return rnorm(m2(x[0], y[1]) ^ m2(y[0], x[1]), m2(x[1], y[1]))


def word(x, g, h, Lmax=40):
    w, y = '', x
    for L in range(1, Lmax):
        w += str(y[0] & 1)
        y = That(y, g, h)
        if y == x:
            return w
    return None


# D0: g=1+t^2, r=1/(1+t+t^2) word '1', c=1 word '10'
g = 0b101
r = (1, 0b111)
check(word(r, g, 1) == '1' and word((1, 1), g, 1) == '10', 'D0words')
# D4: g=1+t+t^2, r=1/(1+t)^2 word '1', c=1/(1+t+t^3) word '101'
check(word((1, 0b101), 0b111, 1) == '1' and word((1, 0b1011), 0b111, 1) == '101', 'D4words')


def series_u(c1, d, Q, N):
    acc = c1
    i = 0
    while Q:
        if Q & 1:
            acc = radd(acc, (m2(d[0], 1 << (i * N)), d[1]))
        Q >>= 1
        i += 1
    return acc


for (g, h, c1, c2, Q, tau, B, label) in [
        (0b101, 1, (1, 0b111), (1, 1), 0b1000, 5, 1, 'D0'),
        (0b111, 1, (1, 0b101), (1, 0b1011), 0b110, 4, 0b100111, 'D4')]:
    d = radd(c1, c2)
    for n in range(0, 7):
        N = 2 ** n
        u = series_u(c1, d, Q, N)
        x = u
        for _ in range(tau * N):
            x = That(x, g, h)
        check(x == series_u(c1, d, Q, 2 * N), label + 'series', N)
        # polynomial version for the twisted map T_{g,B}
        fN = m2(B, u[0])
        q_, rem = d2(fN, u[1])
        check(rem == 0, label + 'poly', N)
        fN = q_
        y = fN
        for _ in range(tau * N):
            y = T2(y, g, B)
        u2 = series_u(c1, d, Q, 2 * N)
        q2, rem2 = d2(m2(B, u2[0]), u2[1])
        check(rem2 == 0 and y == q2, label + 'sim', N)
    print('   %s two-point: series identity and polynomial simulation N=1..64 ok' % label)
# D4 polynomial formula and seed
for n in range(7):
    N = 2 ** n
    X = 1 << N
    fN = m2(0b1011, 1 ^ X ^ m2(X, X)) ^ m2(0b101, X ^ m2(X, X))
    u = series_u((1, 0b101), radd((1, 0b101), (1, 0b1011)), 0b110, N)
    check(fN == d2(m2(0b100111, u[0]), u[1])[0], 'D4formula', N)
    check(fN.bit_length() - 1 == 2 * N + 3, 'D4deg', N)
check(m2(0b1011, 0b111) ^ m2(0b101, 0b110) == 0b101111, 'D4seed')
# D0 untwisted: u_N polynomial for every N (t^{3N} = 1 mod 1+t+t^2 for all N): residues
check(d2(1 ^ m2(1 << 3, 0b110), 0b111)[1] == 0, 'D0polyN')
# EXTRA: g = 1+t^4, h = 1: squared D0 orbit, T^{10N}(u_N^2) = u_{2N}^2 (Prop C' square case)
for n in range(0, 6):
    N = 2 ** n
    u = d2(1 ^ m2(1 << (3 * N), 0b110), 0b111)[0]
    u2 = d2(1 ^ m2(1 << (6 * N), 0b110), 0b111)[0]
    x = sub2(u, 2)
    for _ in range(10 * N):
        x = T2(x, 0b10001, 1)
    check(x == sub2(u2, 2), 'D_t4', N)
print('   extra: 1+t^4, h=1 divergent orbit (squared Matthews-Leigh orbit) verified N=1..32')

# ================================================================ N1
print('N1: s/L = 1/deg g on polynomial cycles, h = 1')
for g in [0b111, 0b1011, 0b1101, 0b1001, 0b10011, 0b10101, 0b11111]:
    dg = g.bit_length() - 1
    seen_cyc = 0
    for f0 in range(1, 1 << 10):
        x, hist = f0, {}
        for i in range(3000):
            if x in hist:
                L = i - hist[x]
                y, s = x, 0
                for _ in range(L):
                    s += y & 1
                    y = T2(y, g, 1)
                if x:
                    check(s * dg == L, 'N1', (g, x, s, L))
                    seen_cyc += 1
                break
            hist[x] = i
            x = T2(x, g, 1)
            if x.bit_length() > 400:
                break
    print('   g=%s: %d seeds ended on nonzero cycles' % (bin(g), seen_cyc))

print('\nreferee_check2: %d failures' % len(FAILS))
sys.exit(1 if FAILS else 0)
