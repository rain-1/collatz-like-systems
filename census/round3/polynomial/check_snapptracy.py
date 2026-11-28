"""Check for snapptracy.md (Theorem B: the map S(f) = f/t or ((1+t)f - f(0)h)/t over F_q,
h = (1+t)^a, q in {2,3,4,5}).

Claims tested exactly:
 (B1) deg S(f) <= deg f; the periodic points of S (h=1) are exactly 0 and the f whose
      Newton sequence v_n = sum_i C(n,i) a_i  (n = 0..p^e-1, p^e > deg f) never vanishes;
      exhaustive over all f of degree < p^e for (q,p^e) = (2,16),(3,9),(4,4),(5,5),(3,3),(4,8 partially)
 (B2) the period of a periodic f equals the least period of n -> v_n on Z/p^e
 (B3) count of periodic points of degree < p^e equals (q-1)^(p^e)
 (B4) twist h=(1+t)^a (a=1,2): periodic points are exactly (1+t)^a * (periodic points of S)
      (exhaustive over small degree)
F_4 = F_2[w]/(w^2+w+1) is implemented directly (elements 0,1,2=w,3=w+1).
"""
import sys, os, itertools
from math import comb
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class Field:
    def __init__(self, q):
        self.q = q
        if q in (2, 3, 5):
            self.p = q
            self.add = lambda a, b: (a + b) % q
            self.mul = lambda a, b: (a * b) % q
            self.neg = lambda a: (-a) % q
        elif q == 4:
            self.p = 2
            self.add = lambda a, b: a ^ b
            M = [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]
            self.mul = lambda a, b: M[a][b]
            self.neg = lambda a: a
        self.elems = list(range(q))

    def intmul(self, n, a):  # n * a for integer n
        r = 0
        for _ in range(n % self.p):
            r = self.add(r, a)
        return r


def trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return tuple(a)


G = (1, 1)   # the degree-1 multiplier g = g0 + g1 t (module-level, changed below)


def S(K, f, h):
    """f/t or (g f - g0 f(0) h)/t ; polynomials as tuples low-first"""
    if not f:
        return f
    c = f[0]
    if c == 0:
        return f[1:]
    g0, g1 = G
    n = max(len(f) + 1, len(h))
    r = [0] * n
    for i, x in enumerate(f):
        r[i] = K.add(r[i], K.mul(g0, x))
        r[i + 1] = K.add(r[i + 1], K.mul(g1, x))
    gc = K.mul(g0, c)
    for i, x in enumerate(h):
        r[i] = K.add(r[i], K.neg(K.mul(gc, x)))
    assert r[0] == 0
    return trim(r[1:])


def kpow(K, x, e):
    r = 1
    for _ in range(e):
        r = K.mul(r, x)
    return r


def newton(K, f, P):
    """v_n = sum_i C(n,i) g1^(n-i) g0^i a_i  (constant term of (g1 I + g0 Delta)^n f)"""
    g0, g1 = G
    out = []
    for n in range(P):
        s = 0
        for i, a in enumerate(f):
            if i > n:
                break
            s = K.add(s, K.intmul(comb(n, i), K.mul(K.mul(kpow(K, g1, n - i), kpow(K, g0, i)), a)))
        out.append(s)
    return out


def least_period(v):
    P = len(v)   # v is given on a full period window Z/P
    for d in range(1, P + 1):
        if P % d == 0 and all(v[i] == v[(i + d) % P] for i in range(P)):
            return d


def is_periodic(K, f, h, cap=10000):
    g = f
    for k in range(1, cap):
        g = S(K, g, h)
        if g == f:
            return k
        if len(g) > len(f) + len(h):
            return None
    return None


def periodic_points_bruteforce(K, D, h):
    """all f with deg f < D; S-closed set if D >= deg h; returns dict f -> period"""
    res = {}
    for coeffs in itertools.product(K.elems, repeat=D):
        f = trim(coeffs)
        # functional graph exploration
        seen = {}
        g = f
        k = 0
        while g not in seen:
            seen[g] = k
            g = S(K, g, h)
            k += 1
        if g == f:
            res[f] = k - seen[g]
    return res


def mulpoly(K, a, b):
    if not a or not b:
        return ()
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] = K.add(r[i + j], K.mul(x, y))
    return trim(r)


fails = 0
GLIST = {2: [(1, 1)], 3: [(1, 1), (1, 2), (2, 1), (2, 2)], 4: [(1, 1), (1, 2), (2, 3)], 5: [(1, 1), (2, 3), (3, 4)]}
for q, P in [(2, 16), (3, 9), (4, 4), (5, 5), (3, 3), (2, 8)]:
    K = Field(q)
    for G in GLIST[q]:
        per = periodic_points_bruteforce(K, P, (1,))
        count = 0
        # gamma = g1^(p^e); v_{n+P} = gamma v_n; full period divides P*ord(gamma) <= P*(q-1)
        for f, L in per.items():
            if not f:
                continue
            v = newton(K, f, P * (q - 1))
            if 0 in v:
                fails += 1
            if least_period(v) != L:
                fails += 1
            count += 1
        for coeffs in itertools.product(K.elems, repeat=P):
            f = trim(coeffs)
            if f and 0 not in newton(K, f, P) and f not in per:
                fails += 1
        if count != (q - 1) ** P:
            fails += 1
        print('q=%d g=%s p^e=%d: periodic points (nonzero) = %d, (q-1)^(p^e) = %d, fails so far %d'
              % (q, G, P, count, (q - 1) ** P, fails))

# B4 twist h = (g/g0)^a
for q, P, a, G in [(3, 3, 1, (1, 1)), (3, 3, 2, (1, 1)), (3, 3, 1, (2, 1)), (5, 5, 1, (1, 1)),
                   (4, 4, 2, (1, 1)), (4, 4, 1, (1, 2)), (2, 8, 3, (1, 1))]:
    K = Field(q)
    g0, g1 = G
    inv0 = [x for x in K.elems if K.mul(x, g0) == 1][0]
    base_h = (1, K.mul(g1, inv0))          # g/g0
    h = (1,)
    for _ in range(a):
        h = mulpoly(K, h, base_h)
    D = P + a
    per_tw = set(f for f in periodic_points_bruteforce(K, D, h) if f)
    base = set(f for f in periodic_points_bruteforce(K, P, (1,)) if f)
    pred = set(mulpoly(K, h, u) for u in base)
    pred = set(f for f in pred if len(f) <= D)
    if per_tw != pred:
        fails += 1
    print('twist q=%d g=%s a=%d: %d periodic points, equal to (g/g0)^a * base: %s'
          % (q, G, a, len(per_tw), per_tw == pred))
print('fails', fails)
sys.exit(1 if fails else 0)
