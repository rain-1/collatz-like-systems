"""Exact arithmetic for polynomial Collatz maps over F_q[t] (round 3, lens `polynomial`).

Conventions
-----------
* Over F_2 a polynomial is a Python int used as a bit mask: bit i is the coefficient of t^i.
  So 0b1101 = 1 + t^2 + t^3.
* Over F_p (p prime) a polynomial is a tuple of ints in [0,p), low degree first, with no
  trailing zeros. () is the zero polynomial.
* A rational function is a pair (num, den) in lowest terms (den monic over F_p).
  A rational function with t not dividing den is an element of F_p[[t]] (a "rational
  power series"); its constant term is num(0)/den(0).

The polynomial Collatz map with multiplier g and twist h (h(0)=1, g(0) != 0) is
    T(f) = f/t                           if f(0) = 0,
    T(f) = (g f - g(0) f(0) h) / t       if f(0) != 0.
Over F_2 this is the usual  (g f + h)/t  for odd f.  T extends to F_p[[t]] by the same
formula ("T-hat").  Everything here is exact: no floating point is used anywhere.
"""
from fractions import Fraction  # noqa: F401  (kept for users of the module)

# ----------------------------------------------------------------------------- F_2 ints

def clmul(a, b):
    """carry-less product = product in F_2[t]"""
    if a.bit_length() < b.bit_length():
        a, b = b, a
    r = 0
    while b:
        if b & 1:
            r ^= a
        a <<= 1
        b >>= 1
    return r


def deg2(a):
    return a.bit_length() - 1


def divmod2(a, b):
    if b == 0:
        raise ZeroDivisionError
    q = 0
    db = b.bit_length()
    while a and a.bit_length() >= db:
        s = a.bit_length() - db
        q |= 1 << s
        a ^= b << s
    return q, a


def gcd2(a, b):
    while b:
        a, b = b, divmod2(a, b)[1]
    return a


def lcm2(a, b):
    return clmul(a, divmod2(b, gcd2(a, b))[0])


def pow2(a, e):
    r = 1
    while e:
        if e & 1:
            r = clmul(r, a)
        a = clmul(a, a)
        e >>= 1
    return r


def frob2(a, k=1):
    """a(t^(2^k)) = a(t)^(2^k)"""
    step = 1 << k
    r = 0
    i = 0
    while a:
        if a & 1:
            r |= 1 << (i * step)
        a >>= 1
        i += 1
    return r


def subst2(a, N):
    """a(t^N) for an arbitrary positive integer N"""
    r = 0
    i = 0
    while a:
        if a & 1:
            r |= 1 << (i * N)
        a >>= 1
        i += 1
    return r


def T2(f, m, h=1):
    """one step of the F_2 map: f/t if f(0)=0 else (m f + h)/t"""
    if f & 1 == 0:
        return f >> 1
    v = clmul(m, f) ^ h
    assert v & 1 == 0, "inadmissible: need h(0) = m(0) = 1"
    return v >> 1


def ps2(a, var='t'):
    if a == 0:
        return '0'
    out = []
    for i in range(deg2(a), -1, -1):
        if a >> i & 1:
            out.append('1' if i == 0 else (var if i == 1 else '%s^%d' % (var, i)))
    return '+'.join(out)


# ---- rational functions over F_2 (pairs of ints)

def rnorm2(x):
    n, d = x
    if d == 0:
        raise ZeroDivisionError
    if n == 0:
        return (0, 1)
    g = gcd2(n, d)
    return (divmod2(n, g)[0], divmod2(d, g)[0])


def radd2(x, y):
    return rnorm2((clmul(x[0], y[1]) ^ clmul(y[0], x[1]), clmul(x[1], y[1])))


def rmul2(x, y):
    return rnorm2((clmul(x[0], y[0]), clmul(x[1], y[1])))


def That2(x, m, h=1):
    """T-hat on a rational power series x = n/d (d(0) = 1)"""
    n, d = x
    assert d & 1, "not a power series"
    if n & 1 == 0:
        return rnorm2((n, d << 1))
    return rnorm2((clmul(m, n) ^ clmul(h, d), d << 1))


def periodic_point2(word, m, h=1):
    """the unique x in F_2[[t]] whose branch sequence is the periodic word (Terras bijection),
    returned as a reduced rational function.  T^L(x) = (A x + B)/t^L on the cylinder, so
    x = B / (t^L + A)."""
    A, B = 1, 0
    for k, c in enumerate(word):
        if c == '1':
            A = clmul(m, A)
            B = clmul(m, B) ^ (h << k)
    L = len(word)
    return rnorm2((B, (1 << L) ^ A))


def orbit_period2(x, m, h=1, cap=100000):
    """returns (L, s, word) if x is purely T-hat-periodic, else None"""
    seen = {}
    path = []
    y = x
    while y not in seen:
        if len(path) > cap:
            raise RuntimeError('cap')
        seen[y] = len(path)
        path.append(y)
        y = That2(y, m, h)
    if seen[y] != 0:
        return None
    word = ''.join('1' if z[0] & 1 else '0' for z in path)
    return (len(path), word.count('1'), word)


# ----------------------------------------------------------------------------- F_p tuples

class Fp:
    def __init__(s, p):
        s.p = p
        s.inv = [0] + [pow(i, p - 2, p) for i in range(1, p)]

    def tr(s, a):
        a = [x % s.p for x in a]
        while a and a[-1] == 0:
            a.pop()
        return tuple(a)

    def add(s, a, b):
        n = max(len(a), len(b))
        return s.tr([(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)])

    def sub(s, a, b):
        n = max(len(a), len(b))
        return s.tr([(a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0) for i in range(n)])

    def smul(s, c, a):
        return s.tr([c * x for x in a])

    def mul(s, a, b):
        if not a or not b:
            return ()
        r = [0] * (len(a) + len(b) - 1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    r[i + j] += x * y
        return s.tr(r)

    def pow(s, a, e):
        r = (1,)
        while e:
            if e & 1:
                r = s.mul(r, a)
            a = s.mul(a, a)
            e >>= 1
        return r

    def divmod(s, a, b):
        a = list(a)
        q = [0] * max(0, len(a) - len(b) + 1)
        ib = s.inv[b[-1]]
        while len(a) >= len(b) and a:
            c = a[-1] * ib % s.p
            k = len(a) - len(b)
            q[k] = c
            for i, y in enumerate(b):
                a[i + k] = (a[i + k] - c * y) % s.p
            a = list(s.tr(a))
        return s.tr(q), s.tr(a)

    def gcd(s, a, b):
        while b:
            a, b = b, s.divmod(a, b)[1]
        return a

    def subst(s, a, N):
        """a(t^N)"""
        if not a:
            return ()
        r = [0] * ((len(a) - 1) * N + 1)
        for i, c in enumerate(a):
            r[i * N] = c
        return s.tr(r)

    # rational functions
    def rnorm(s, x):
        n, d = x
        if not n:
            return ((), (1,))
        g = s.gcd(n, d)
        n = s.divmod(n, g)[0]
        d = s.divmod(d, g)[0]
        c = s.inv[d[-1]]
        return (s.smul(c, n), s.smul(c, d))

    def radd(s, x, y):
        return s.rnorm((s.add(s.mul(x[0], y[1]), s.mul(y[0], x[1])), s.mul(x[1], y[1])))

    def rsub(s, x, y):
        return s.rnorm((s.sub(s.mul(x[0], y[1]), s.mul(y[0], x[1])), s.mul(x[1], y[1])))

    def rmul(s, x, y):
        return s.rnorm((s.mul(x[0], y[0]), s.mul(x[1], y[1])))

    def const(s, x):
        n, d = x
        assert d and d[0] % s.p, "not a power series"
        return (n[0] if n else 0) * s.inv[d[0]] % s.p


def Tp(F, f, g, h):
    """one step of the F_p map on a polynomial tuple f"""
    if not f or f[0] == 0:
        return f[1:] if f else ()
    c = f[0]
    v = F.sub(F.mul(g, f), F.smul(g[0] * c, h))
    assert not v or v[0] == 0
    return v[1:]


def Thatp(F, x, g, h):
    n, d = x
    c = F.const(x)
    if c:
        n = F.sub(F.mul(g, n), F.smul(g[0] * c, F.mul(h, d)))
    return F.rnorm((n, F.mul(d, (0, 1))))


def psp(a, var='t'):
    if not a:
        return '0'
    out = []
    for i in range(len(a) - 1, -1, -1):
        c = a[i]
        if c:
            mon = '1' if i == 0 else (var if i == 1 else '%s^%d' % (var, i))
            out.append(mon if c == 1 else ('%d' % c if i == 0 else '%d%s' % (c, mon)))
    return '+'.join(out)


# ----------------------------------------------------------------------------- certificates

def line_renorm(F, g, P0, maxphases=200, maxb=4):
    """Line renormalization map on F_p[X] (Lemma R2 of renormalization.md):
         Phi(P) = l + g(X)^(v*[l != 0]) * (P - l)/X^v,   l = P(0), v = ord_X(P - l).
       Returns (k, b, taus) with Phi^k(P0) = P0(X^(p^b)) and taus the list of v's,
       or None.  Exact."""
    P = P0
    taus = []
    for k in range(1, maxphases + 1):
        l = P[0] if P else 0
        R = F.sub(P, (l,))
        if not R:
            return None
        v = 0
        while R[v] == 0:
            v += 1
        R = R[v:]
        if l:
            R = F.mul(F.pow(g, v), R)
        P = F.add((l,), R)
        taus.append(v)
        for b in range(1, maxb + 1):
            if P == F.subst(P0, F.p ** b):
                return (k, b, taus)
    return None


def rad_divides(F, w, P):
    """does every irreducible factor of w divide P ?  (checked as: w | P^deg(w), exact)"""
    e = max(1, len(w) - 1)
    return not F.divmod(F.pow(P, e), w)[1]
