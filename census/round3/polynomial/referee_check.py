"""Independent referee check for census/round3/polynomial (round 3).

Written from scratch: it does NOT import polylib.py, certs.py or the prover's check scripts.
It imports systems.py only to compare the prover's step functions against the written rules
(the comparison is the test). All arithmetic is exact (Python ints as F_2 bit masks, lists
mod p, an explicit F_4 table). Runtime: about a minute.

Claims tested (labels as in REFEREE.md):
  S   systems.py step functions agree with the rules as written in the .md files
  A   Theorem A (onept.md): exhaustive + random large
  B   Theorem B (snapptracy.md): exhaustive over F_3, F_4, F_5 + random large Newton words
  C   Theorem C / Prop. C' / Cor. C1 (frobenius.md): random large, higher-degree (m,h)
  D   every divergence certificate re-derived with an independent renormalization map and
      re-simulated; general families p2_cube_k (k<=4) and p2_tri_k (k<=5)
  N1  s/L = 1/deg g on all polynomial cycles found exhaustively (h=1)
  P2  deg g <= 1 => bounded orbits (random, several F_p)
"""
import random, sys, os
from math import comb

random.seed(0xC011A72)
FAILS = []


def fail(tag, msg):
    FAILS.append((tag, msg))
    print('  FAIL [%s] %s' % (tag, msg))


# ------------------------------------------------------------------ F_2 arithmetic (ints)
def mul2(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        b >>= 1
    return r


def dm2(a, b):
    q = 0
    db = b.bit_length()
    while a.bit_length() >= db:
        s = a.bit_length() - db
        q |= 1 << s
        a ^= b << s
    return q, a


def pw2(a, e):
    r = 1
    for _ in range(e):
        r = mul2(r, a)
    return r


def sub2(a, N):  # a(t^N)
    r, i = 0, 0
    while a:
        if a & 1:
            r |= 1 << (i * N)
        a >>= 1
        i += 1
    return r


def deg(a):
    return a.bit_length() - 1


def step2(f, g, h):
    if not f & 1:
        return f >> 1
    v = mul2(g, f) ^ h
    assert not v & 1
    return v >> 1


def gcd2(a, b):
    while b:
        a, b = b, dm2(a, b)[1]
    return a


# ------------------------------------------------------------------ F_p lists (low first)
def tr(a, p):
    a = [x % p for x in a]
    while a and a[-1] == 0:
        a.pop()
    return a


def mulp(a, b, p):
    if not a or not b:
        return []
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                r[i + j] += x * y
    return tr(r, p)


def addp(a, b, p):
    n = max(len(a), len(b))
    return tr([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)], p)


def scal(c, a, p):
    return tr([c * x for x in a], p)


def subsp(a, N, p):
    if not a:
        return []
    r = [0] * ((len(a) - 1) * N + 1)
    for i, c in enumerate(a):
        r[i * N] = c
    return tr(r, p)


def stepp(f, g, h, p):
    if not f:
        return []
    c = f[0]
    if c == 0:
        return f[1:]
    v = addp(mulp(g, f, p), scal(-g[0] * c, h, p), p)
    assert not v or v[0] == 0
    return v[1:]


def divp(a, b, p):
    a = list(a)
    inv = pow(b[-1], p - 2, p)
    q = [0] * max(0, len(a) - len(b) + 1)
    while len(a) >= len(b) and a:
        c = a[-1] * inv % p
        k = len(a) - len(b)
        q[k] = c
        for i, y in enumerate(b):
            a[i + k] = (a[i + k] - c * y) % p
        a = tr(a, p)
    return tr(q, p), a


# ================================================================== S: systems.py vs rules
print('S: systems.py step functions vs written rules')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import systems  # noqa: E402

RULES2 = {  # id -> (g, h) as written in the .md / README odd-branch rule
    'p2_onept_h7': (0b11, 0b111), 'p2_t3': (0b1001, 1), 'p2_cube': (0b1111, 1),
    'p2_tri_k': (0b1011, 0b111), 'p2_crit': (0b111, 0b100111), 'p2_ML': (0b101, 1),
    'p2_sq111': (0b10101, 0b10111), 'p2_1034': (0b11001, 0b11011), 'p2_nichols': (0b111, 1),
    'p2_m3b_h1': (0b1011, 1), 'p2_m3c_h1': (0b1101, 1)}
RULESP = {'p3_a': ([2, 0, 1], [1, 1, 2]), 'p3_b': ([1, 1, 1], [1, 0, 1]),
          'p3_c': ([1, 0, 2], [1, 2, 2]), 'p3_d': ([2, 1, 2], [1, 0, 1]), 'p3_st': ([1, 1], [1])}
# sanity of the written constants: (1+t)^2(1+t+t^3) = 1+t+t^2+t^5 ; (1+t+t^2)^2 = 1+t^2+t^4
assert mul2(0b101, 0b1011) == 0b100111 and mul2(0b111, 0b111) == 0b10101
for S in systems.SYSTEMS:
    sid = S['id']
    if S['step'] is None:
        continue
    if sid in RULES2:
        g, h = RULES2[sid]
        for _ in range(3000):
            f = random.getrandbits(random.randint(0, 300))
            if S['step'](f) != step2(f, g, h):
                fail('S', sid)
                break
    elif sid in RULESP:
        g, h = RULESP[sid]
        for _ in range(1500):
            f = tr([random.randrange(3) for _ in range(random.randint(0, 80))], 3)
            if list(S['step'](tuple(f))) != stepp(f, g, h, 3):
                fail('S', sid)
                break
    else:
        fail('S', 'no written rule known for ' + sid)

# ================================================================== A: Theorem A
print('A: Theorem A, g = 1+t, all h')
G1 = 0b11


def split(h):
    a, k = 0, h
    while dm2(k, G1)[1] == 0:
        k = dm2(k, G1)[0]
        a += 1
    return a, k


# A(1),(2) random wide range
for _ in range(30000):
    h = random.getrandbits(random.randint(1, 60)) | 1
    f = random.getrandbits(random.randint(0, 400))
    a, k = split(h)
    Tf = step2(f, G1, h)
    if deg(Tf) > max(deg(f), deg(h) - 1):
        fail('A1', (f, h))
    if (dm2(f, k)[1] == 0) != (dm2(Tf, k)[1] == 0):
        fail('A2', (f, h))
# A(4) random large multiples of k reach {0,h}; A(3) random large non-multiples never do
for _ in range(400):
    h = random.getrandbits(random.randint(1, 12)) | 1
    a, k = split(h)
    u = random.getrandbits(random.randint(1, 120)) or 1
    for f, should in ((mul2(k, u), True), (mul2(k, u) ^ 1, None)):
        if f == 0:
            continue
        should = (dm2(f, k)[1] == 0)
        seen = set()
        x = f
        hit = False
        while x not in seen:
            seen.add(x)
            if x in (0, h):
                hit = True
            x = step2(x, G1, h)
        if hit != should:
            fail('A3/4', (f, h))
        if a == 0 and hit and x != h:
            fail('A7', (f, h))
# exhaustive: all h with h(0)=1, deg h <= 8; all f with deg f < 11
for dh in range(0, 9):
    for h in range((1 << dh) | 1, 1 << (dh + 1), 2) if dh else [1]:
        a, k = split(h)
        n = 1 << max(11, dh + 1)
        fate = {}
        cycles = []
        for f0 in range(n):
            path, idx, x = [], {}, f0
            while x not in fate and x not in idx:
                idx[x] = len(path)
                path.append(x)
                x = step2(x, G1, h)
            if x in idx:  # new cycle
                cyc = path[idx[x]:]
                cycles.append(cyc)
                for y in cyc:
                    fate[y] = ('0' if cyc == [0] else 'h' if cyc == [h] else 'c%d' % len(cycles))
            res = fate[x]
            for y in path:
                if y not in fate:
                    fate[y] = res
        extra = [c for c in cycles if c != [0] and c != [h]]
        for c in extra:
            if max(deg(y) for y in c) >= dh:
                fail('A5', (h, c))
            if any(dm2(y, k)[1] == 0 for y in c):
                fail('A5b', (h, c))
        if (len(extra) == 0) != (k == 1):
            fail('A6', h)
        for f in range(1, n):
            reach = fate[f] in ('0', 'h')
            if reach != (dm2(f, k)[1] == 0):
                fail('A3/4ex', (h, f))
            if a == 0 and ((fate[f] == 'h') != (dm2(f, h)[1] == 0) or fate[f] == '0'):
                fail('A7ex', (h, f))
# worked instance p2_onept_h7
hh = 0b111
assert step2(1, G1, hh) == 2 and step2(2, G1, hh) == 1 and step2(3, G1, hh) == 1

# ================================================================== B: Theorem B
print('B: Theorem B, degree-1 multipliers over F_3, F_4, F_5 (+ random large)')
F4M = [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]  # 2 = w, 3 = w+1 = w^2


class Fq:
    def __init__(s, q):
        s.q = q
        if q == 4:
            s.p = 2
            s.add = lambda a, b: a ^ b
            s.mul = lambda a, b: F4M[a][b]
            s.neg = lambda a: a
        else:
            s.p = q
            s.add = lambda a, b: (a + b) % q
            s.mul = lambda a, b: a * b % q
            s.neg = lambda a: -a % q
        s.inv = {a: [b for b in range(1, q) if s.mul(a, b) == 1][0] for a in range(1, q)}

    def pw(s, a, e):
        r = 1
        for _ in range(e):
            r = s.mul(r, a)
        return r

    def nat(s, n):  # integer n as field element
        r = 0
        for _ in range(n % s.p):
            r = s.add(r, 1)
        return r


def trq(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return tuple(a)


def Sq(K, g0, g1, f, h):
    if not f or f[0] == 0:
        return f[1:]
    c = f[0]
    r = [0] * (max(len(f) + 1, len(h)))
    for i, x in enumerate(f):
        r[i] = K.add(r[i], K.mul(g0, x))
        r[i + 1] = K.add(r[i + 1], K.mul(g1, x))
    gc = K.mul(g0, c)
    for i, x in enumerate(h):
        r[i] = K.add(r[i], K.neg(K.mul(gc, x)))
    assert r[0] == 0
    return trq(r[1:])


def newton(K, g0, g1, f, n_max):
    out = []
    for n in range(n_max):
        s = 0
        for i, a in enumerate(f[:n + 1]):
            s = K.add(s, K.mul(K.nat(comb(n, i)), K.mul(K.mul(K.pw(g1, n - i), K.pw(g0, i)), a)))
        out.append(s)
    return out


def from_word(K, g0, g1, v):
    """invert the triangular Newton map"""
    a = []
    for n, vn in enumerate(v):
        s = 0
        for i in range(n):
            s = K.add(s, K.mul(K.nat(comb(n, i)), K.mul(K.mul(K.pw(g1, n - i), K.pw(g0, i)), a[i])))
        a.append(K.mul(K.add(vn, K.neg(s)), K.inv[K.pw(g0, n)]))
    return trq(a)


import itertools  # noqa: E402
for q, P, gl in [(3, 9, [(1, 1), (2, 2), (1, 2)]), (4, 4, [(1, 1), (2, 3), (3, 1)]),
                 (5, 5, [(1, 1), (2, 4)]), (2, 16, [(1, 1)])]:
    K = Fq(q)
    for g0, g1 in gl:
        # brute-force periodic points in the S-closed set deg < P
        per = {}
        for co in itertools.product(range(q), repeat=P):
            f = trq(co)
            if not f:
                continue
            x, L = f, 0
            # periodic iff returns; degree never increases so the set is finite
            seen = set()
            while True:
                x = Sq(K, g0, g1, x, (1,))
                L += 1
                if x == f:
                    per[f] = L
                    break
                if x in seen or not x:
                    break
                seen.add(x)
                if L > q ** P:
                    break
        cnt = 0
        for co in itertools.product(range(q), repeat=P):
            f = trq(co)
            if not f:
                continue
            v = newton(K, g0, g1, f, P)
            crit = 0 not in v
            if crit != (f in per):
                fail('B2', (q, g0, g1, f))
            if crit:
                cnt += 1
                gam = K.pw(g1, P)
                vv = list(v)
                for j in range(P * (q - 1)):
                    vv.append(K.mul(gam, vv[j]))
                vv = vv[:P * (q - 1)]
                W = len(vv)
                lp = min(d for d in range(1, W + 1) if W % d == 0 and all(vv[i] == vv[(i + d) % W] for i in range(W)))
                if lp != per[f]:
                    fail('B3per', (q, g0, g1, f, lp, per[f]))
        if cnt != (q - 1) ** P:
            fail('B3count', (q, g0, g1, cnt))
        print('   q=%d g=%d+%dt deg<%d: %d periodic points = (q-1)^%d' % (q, g0, g1, P, cnt, P))
# random large: words of length p^e (27, 81, 125, 64) -> f; check S^{p^e} f = gamma f directly
for q, P in [(3, 27), (3, 81), (5, 25), (5, 125), (4, 16), (4, 64), (2, 128)]:
    K = Fq(q)
    for _ in range(6):
        g0, g1 = random.randrange(1, q), random.randrange(1, q)
        v = [random.randrange(1, q) for _ in range(P)]
        f = from_word(K, g0, g1, v)
        if newton(K, g0, g1, f, P) != v:
            fail('Binv', q)
        x = f
        for n in range(P):
            if not x or x[0] == 0:
                fail('B2big-branch', (q, n))
                break
            x = Sq(K, g0, g1, x, (1,))
        gam = K.pw(g1, P)
        if x != trq(tuple(K.mul(gam, c) for c in f)):
            fail('B2big', (q, P))
        # perturb one word letter to 0 -> must be non-periodic (reaches lower degree, never returns)
        j = random.randrange(P)
        v2 = list(v)
        v2[j] = 0
        f2 = from_word(K, g0, g1, v2)
        x = f2
        for n in range(j + 1):
            x = Sq(K, g0, g1, x, (1,))
        if len(x) >= len(f2) and f2:
            fail('B2zero', (q, P, j))
# B(4) twists a = 1, 2, 3 over F_3, F_5, F_4 (exhaustive small)
for q, P, a, g0, g1 in [(3, 3, 1, 2, 1), (3, 3, 2, 1, 2), (3, 3, 3, 2, 2), (5, 5, 1, 3, 2), (4, 4, 2, 2, 3), (4, 4, 1, 3, 3)]:
    K = Fq(q)
    pi = (1, K.mul(g1, K.inv[g0]))
    h = (1,)
    for _ in range(a):
        r = [0] * (len(h) + 1)
        for i, x in enumerate(h):
            r[i] = K.add(r[i], x)
            r[i + 1] = K.add(r[i + 1], K.mul(pi[1], x))
        h = trq(r)
    D = P + a
    pers = set()
    for co in itertools.product(range(q), repeat=D):
        f = trq(co)
        if not f:
            continue
        x = f
        for L in range(1, 4 * q ** 2 * P + 2):
            x = Sq(K, g0, g1, x, h)
            if x == f:
                pers.add(f)
                break
    # prediction
    pred = set()
    for co in itertools.product(range(q), repeat=P):
        u = trq(co)
        if u and 0 not in newton(K, g0, g1, u, P):
            r = [0] * (len(u) + len(h) - 1)
            for i, x in enumerate(u):
                for j, y in enumerate(h):
                    r[i + j] = K.add(r[i + j], K.mul(x, y))
            pred.add(trq(r))
    if pers != pred:
        fail('B4', (q, a, g0, g1, len(pers), len(pred)))
    # GLOBAL for twisted: random large f stays bounded (eventually periodic)
    for _ in range(50):
        f = trq([random.randrange(q) for _ in range(random.randint(1, 60))])
        mx = len(f)
        x = f
        for _ in range(2000):
            x = Sq(K, g0, g1, x, h)
            if len(x) > max(mx, len(h)):
                fail('B-global', q)
                break

# ================================================================== C: Theorem C
print('C: Frobenius self-conjugacy')


def sq(a):
    return sub2(a, 2)


def nonsquare(a):
    return any((a >> i) & 1 for i in range(1, a.bit_length(), 2))


for _ in range(300):
    M = random.getrandbits(random.randint(1, 10)) | 1
    if M == 1:
        M = 0b11
    m = sq(M) ^ 2
    for _ in range(40):
        u = random.getrandbits(random.randint(0, 500))
        phiu = sq(mul2(M, u))
        if step2(step2(phiu, m, 1), m, 1) != sq(mul2(M, step2(u, m, 1))):
            fail('C', (M, u))
        if u and not nonsquare(step2(phiu, m, 1)):
            fail('C-notimage', (M, u))
# period doubling on genuine cycles of several m = M^2 + t
for M in (0b11, 0b111, 0b101, 0b1011):
    m = sq(M) ^ 2
    for u0 in range(1, 1 << 8):
        x, L, seen = u0, 0, set()
        while x not in seen and len(seen) < 3000 and x.bit_length() < 60:
            seen.add(x)
            x = step2(x, m, 1)
        if x not in seen:
            continue  # no cycle found within the cap (orbit may diverge); skip
        # x is now on a cycle
        c0, L = x, 0
        while True:
            x = step2(x, m, 1)
            L += 1
            if x == c0:
                break
        y0 = sq(mul2(M, c0))
        y, L2 = y0, 0
        while True:
            y = step2(y, m, 1)
            L2 += 1
            if y == y0 or L2 > 2 * L + 1:
                break
        if L2 != 2 * L:
            fail('C-period', (M, c0, L, L2))
# Cor C1, k <= 11
for k in range(12):
    f0 = pw2(0b11, (1 << (k + 1)) - 2)
    x, L = f0, 0
    while True:
        x = step2(x, 0b111, 1)
        L += 1
        if x == f0 or L > 1 << (k + 3):
            break
    if L != 1 << (k + 2):
        fail('C1', k)


# Prop C': random (m,h) of larger degree built to satisfy (ii) (choose q, h_o=(1+m_o)q, h_e=m_e q)
def eo(a):
    e = o = 0
    i = 0
    while a:
        if a & 1:
            if i % 2 == 0:
                e |= 1 << (i // 2)
            else:
                o |= 1 << (i // 2)
        a >>= 1
        i += 1
    return e, o


def join(e, o):
    return sq(e) ^ (sq(o) << 1)


cnt = 0
while cnt < 400:
    me = random.getrandbits(random.randint(0, 8)) | 1
    mo = random.getrandbits(random.randint(0, 8))
    qq = random.getrandbits(random.randint(0, 6)) | 1
    ho, he = mul2(1 ^ mo, qq), mul2(me, qq)
    if ((mo & 1) ^ (ho & 1)) != 1 or (he & 1) != 1:
        continue
    m, h = join(me, mo), join(he, ho)
    hp = (mul2(1 ^ mo, ho) << 1) ^ mul2(me, he)
    cnt += 1
    for _ in range(20):
        A = random.getrandbits(random.randint(0, 200))
        if step2(step2(sq(A), m, h), m, h) != sq(step2(A, m, hp)):
            fail("C'", (m, h, A))

# ================================================================== D: certificates
print('D: divergence certificates (independent renormalization + simulation)')


def Phi(P, g, p):
    lam = P[0] if P else 0
    R = addp(P, [-lam], p)
    v = 0
    while R[v] == 0:
        v += 1
    R = R[v:]
    if lam:
        for _ in range(v):
            R = mulp(R, g, p)
    return addp([lam], R, p), v


def line_cert(g, h, P, p, maxk=40):
    Q = P
    taus = []
    for k in range(maxk):
        Q, v = Phi(Q, g, p)
        taus.append(v)
        for b in range(1, 7):
            if Q == subsp(P, p ** b, p):
                return k + 1, b, taus
    return None


def rho_fN(g, h, P, N, p):
    """rho P(t^N) with rho = g0 h/(g - t), returned as polynomial (or None if not)"""
    num = mulp(scal(g[0], h, p), subsp(P, N, p), p)
    den = addp(g, [0, -1], p)
    q, r = divp(num, den, p)
    return q if not r else None


def simulate(f, g, h, p, n):
    if p == 2:  # fast path via bit masks (step2 is cross-checked against stepp below)
        I = lambda a: sum(c << i for i, c in enumerate(a))
        x, gi, hi = I(f), I(g), I(h)
        for _ in range(n):
            x = step2(x, gi, hi)
        return [(x >> i) & 1 for i in range(x.bit_length())]
    x = f
    for _ in range(n):
        x = stepp(x, g, h, p)
    return x


for _ in range(2000):  # step2 == stepp over F_2
    g_ = tr([1] + [random.randrange(2) for _ in range(6)], 2)
    h_ = tr([1] + [random.randrange(2) for _ in range(6)], 2)
    f_ = tr([random.randrange(2) for _ in range(random.randint(0, 90))], 2)
    I = lambda a: sum(c << i for i, c in enumerate(a))
    if I(stepp(f_, g_, h_, 2)) != step2(I(f_), I(g_), I(h_)):
        fail('step2/stepp', 0)


LINE = [  # id, p, g, h, P, expected (b, tau) from the .md
    ('p2_t3', 2, [1, 0, 0, 1], [1], [1, 0, 0, 0, 0, 0, 1, 0, 0, 1], (1, 18)),
    ('p2_tri1', 2, [1, 1, 0, 1], [1, 1, 1], [1, 1], (1, 2)),
    ('p2_sq111', 2, [1, 0, 1, 0, 1], [1, 1, 1, 0, 1], [1, 1], (1, 3)),
    ('p2_1034', 2, [1, 0, 0, 1, 1], [1, 1, 0, 1, 1], [1, 1, 1], (1, 2)),
    ('p3_a', 3, [2, 0, 1], [1, 1, 2], [1, 0, 1], (1, 8)),
    ('p3_b', 3, [1, 1, 1], [1, 0, 1], [0, 1, 1, 2], (1, 8)),
    ('p3_c', 3, [1, 0, 2], [1, 2, 2], [1, 0, 1], (1, 8)),
    ('p3_d', 3, [2, 1, 2], [1, 0, 1], [0, 1, 2, 2], (2, 32)),
]
for k in range(1, 5):  # p2_cube_k
    K = 1 << k
    g = [comb(K + 1, i) % 2 for i in range(K + 2)]
    w = addp(g, [0, 1], 2)
    LINE.append(('p2_cube_k%d' % k, 2, g, [1], w, (k, K * K + K)))
for k in range(1, 6):  # p2_tri_k
    K = 1 << k
    g = [1, 1] + [0] * (K - 1) + [1]
    LINE.append(('p2_tri_k%d' % k, 2, g, [1] * (K + 1), [1, 1], (k, 2)))

for cid, p, g, h, P, (bexp, tauexp) in LINE:
    r = line_cert(g, h, P, p)
    if r is None:
        fail('D', cid + ' no self-similarity')
        continue
    k_, b, taus = r
    tau = sum(taus)
    if (b, tau) != (bexp, tauexp):
        fail('D', '%s b,tau = %s,%s expected %s,%s' % (cid, b, tau, bexp, tauexp))
    # polynomiality for every N = p^n: f_N = rho P(t^N); den(rho) radical divides P, check directly
    den = addp(g, [0, -1], p)
    num = scal(g[0], h, p)
    # reduce rho
    a, bb = num, den
    while bb:
        a, bb = bb, divp(a, bb, p)[1]
    gg = scal(pow(a[-1], p - 2, p), a, p)
    D = divp(den, gg, p)[0]
    # f_N polynomial <=> D | P(t^N); t^(p^n) mod D is eventually periodic in n: check all residues
    if len(D) > 1:
        Xs = []
        X = divp([0, 1], D, p)[1]
        while X not in Xs:
            Xs.append(X)
            X = divp(subsp(X, p, p), D, p)[1]  # X(t)^p = X(t^p) over F_p; reduce mod D
        for X in Xs:
            acc = []
            Xi = [1]
            for c in P:
                acc = addp(acc, scal(c, Xi, p), p)
                Xi = divp(mulp(Xi, X, p), D, p)[1]
            if divp(acc, D, p)[1]:
                fail('D-poly', cid)
    N = 1
    sims = 0
    while True:
        f, f2 = rho_fN(g, h, P, N, p), rho_fN(g, h, P, N * p ** b, p)
        if f is None or f2 is None:
            fail('D-poly2', (cid, N))
            break
        if len(f2) > (3000 if p == 2 else 1200):
            break
        if simulate(f, g, h, p, tau * N) != f2:
            fail('D-sim', (cid, N))
        if len(f2) <= len(f):
            fail('D-deg', cid)
        sims += 1
        N *= p ** b
    print('   %-12s b=%d tau=%2d  direct simulations %d' % (cid, b, tau, sims))
# specific claims in the text
f1 = rho_fN([1, 0, 0, 1], [1], [1, 0, 0, 0, 0, 0, 1, 0, 0, 1], 1, 2)
assert f1 == [1, 1, 1, 0, 1, 0, 1], f1  # 1+t+t^2+t^4+t^6
for n in range(6):
    if len(rho_fN([1, 0, 0, 1], [1], [1, 0, 0, 0, 0, 0, 1, 0, 0, 1], 2 ** n, 2)) - 1 != 9 * 2 ** n - 3:
        fail('D1deg', n)
# p2_cube k=1 closed form T^{6(2^n-1)}(1) = (1+t^2+t^3)^{2^n-1}
x = 1
for n in range(1, 8):
    for _ in range(6 * (2 ** (n - 1))):
        x = step2(x, 0b1111, 1)
    if x != pw2(0b1101, 2 ** n - 1):
        fail('D2closed', n)
# p2_tri_k all-ones form (h = C_k)
for k in (1, 2, 3):
    K = 1 << k
    g = 0b11 | (1 << (K + 1))
    h = (1 << (K + 1)) - 1
    N = 1
    while N * K < 2000:
        x = (1 << N) - 1
        for _ in range(2 * N):
            x = step2(x, g, h)
        if x != (1 << (K * N)) - 1:
            fail('D3ones', (k, N))
        N *= 2

# ---- two-point certificates, re-derived from scratch with rational power series over F_2
def rnorm(n, d):
    if n == 0:
        return (0, 1)
    c = gcd2(n, d)
    return (dm2(n, c)[0], dm2(d, c)[0])


def That(x, g, h=1):
    n, d = x
    assert d & 1
    if not n & 1:
        return rnorm(n, d << 1)
    return rnorm(mul2(g, n) ^ mul2(h, d), d << 1)


def radd(x, y):
    return rnorm(mul2(x[0], y[1]) ^ mul2(y[0], x[1]), mul2(x[1], y[1]))


def word_of(x, g, Lmax=50):
    w, y = '', x
    for _ in range(Lmax):
        w += '1' if y[0] & 1 else '0'
        y = That(y, g)
        if y == x:
            return w
    return None


# D0 Matthews-Leigh: r = 1/(1+t+t^2) fixed, 1 has word 10; u_N = r + t^{3N}(1+r)
g = 0b101
r = (1, 0b111)
assert word_of(r, g) == '1' and word_of((1, 1), g) == '10'
# D4 p2_crit: r = 1/(1+t)^2 (word 1), c = 1/(1+t+t^3) (word 101)
gc_ = 0b111
assert word_of((1, 0b101), gc_) == '1' and word_of((1, 0b1011), gc_) == '101'


def uN_ML(N):  # B = 1 : r + t^{3N}(1+r) must be a polynomial
    num = 1 ^ (mul2(1 << (3 * N), 0b110))  # (1 + t^{3N}(t+t^2)) / (1+t+t^2)
    q, rr = dm2(num, 0b111)
    return q if rr == 0 else None


N = 1
while N < 600:
    a, b2 = uN_ML(N), uN_ML(2 * N)
    if a is None or b2 is None:
        fail('D0poly', N)
        break
    x = a
    for _ in range(5 * N):
        x = step2(x, 0b101, 1)
    if x != b2:
        fail('D0sim', N)
    N *= 2
# also the residue argument for all N: t^{3N} = 1 mod 1+t+t^2 for all N  (t^3 = 1 there)
assert dm2((1 << 3) ^ 1, 0b111)[1] == 0


def fN_crit(N):
    X = 1 << N
    return mul2(0b1011, 1 ^ X ^ mul2(X, X)) ^ mul2(0b101, X ^ mul2(X, X))


assert fN_crit(1) == 0b101111
# B*u_N identity: B r = 1+t+t^3, B d = B(r + c) = (1+t+t^3) + (1+t)^2
N = 1
while N < 1200:
    x = fN_crit(N)
    for _ in range(4 * N):
        x = step2(x, 0b111, 0b100111)
    if x != fN_crit(2 * N):
        fail('D4sim', N)
    if deg(fN_crit(N)) != 2 * N + 3:
        fail('D4deg', N)
    N *= 2
# twist transfer R3 on random large k: T_{g,kh}(k u) = k T_{g,h}(u), F_2 and F_3
for _ in range(3000):
    g = random.getrandbits(random.randint(1, 8)) | 1
    h = random.getrandbits(random.randint(1, 8)) | 1
    k = random.getrandbits(random.randint(1, 30)) | 1
    u = random.getrandbits(random.randint(0, 200))
    if step2(mul2(k, u), g, mul2(k, h)) != mul2(k, step2(u, g, h)):
        fail('R3', (g, h, k, u))
for _ in range(1000):
    p = random.choice([3, 5])
    g = tr([random.randrange(1, p)] + [random.randrange(p) for _ in range(4)], p)
    h = tr([1] + [random.randrange(p) for _ in range(4)], p)
    k = tr([1] + [random.randrange(p) for _ in range(10)], p)
    u = tr([random.randrange(p) for _ in range(random.randint(0, 60))], p)
    if stepp(mulp(k, u, p), g, mulp(k, h, p), p) != mulp(k, stepp(u, g, h, p), p):
        fail('R3p', p)

# ================================================================== N1
print('N1: s/L = 1/deg g on polynomial cycles (h = 1)')
for g in [0b111, 0b1011, 0b1101, 0b1001, 0b1111, 0b10011, 0b11001, 0b10101]:
    dgr = deg(g)
    found = 0
    done = set()
    for f0 in range(1, 1 << 10):
        x, seen = f0, {}
        for i in range(400):
            if x in done or x.bit_length() > 40:
                break
            if x in seen:
                done.update(seen)
                c0 = x
                L = s = 0
                while True:
                    s += x & 1
                    x = step2(x, g, 1)
                    L += 1
                    if x == c0:
                        break
                if c0 and s * dgr != L:
                    fail('N1', (g, c0))
                found += c0 != 0
                break
            seen[x] = i
            x = step2(x, g, 1)
    print('   g=%s: %d starts ended on a nonzero cycle, all with s/L = 1/%d' % (bin(g), found, dgr))

# ================================================================== P2
print('P2: deg g <= 1 => deg T f <= max(deg f, deg h - 1)')
for _ in range(5000):
    p = random.choice([2, 3, 5, 7])
    g = tr([random.randrange(1, p), random.randrange(p)], p)
    h = tr([1] + [random.randrange(p) for _ in range(random.randint(0, 20))], p)
    f = tr([random.randrange(p) for _ in range(random.randint(0, 100))], p)
    if len(stepp(f, g, h, p)) > max(len(f), len(h) - 1):
        fail('P2', p)

print('\nreferee_check: %d failures' % len(FAILS))
sys.exit(1 if FAILS else 0)
