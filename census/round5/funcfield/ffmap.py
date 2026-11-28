"""Exact reference implementation of polynomial table maps over F_q (q = 2, 3, 4).

A polynomial is a tuple of coefficients (low degree first) with no trailing zeros.
F_4 = {0, 1, w, w^2} is coded 0, 1, 2, 3 with w^2 = w + 1 (addition = XOR of codes).
A system is (q, branches); a branch is (r, g, c): r a tuple of e digits (prefix code),
T(f) = g * (f - r) / t^e + c.
"""
from fractions import Fraction


def fadd(q, a, b):
    return (a ^ b) if q in (2, 4) else (a + b) % q


def fneg(q, a):
    return a if q in (2, 4) else (-a) % q


def fmul(q, a, b):
    if q == 4:
        if a == 0 or b == 0:
            return 0
        return ((a - 1 + b - 1) % 3) + 1
    return (a * b) % q


def trim(f):
    f = list(f)
    while f and f[-1] == 0:
        f.pop()
    return tuple(f)


def padd(q, f, g):
    n = max(len(f), len(g))
    return trim(fadd(q, f[i] if i < len(f) else 0, g[i] if i < len(g) else 0) for i in range(n))


def pneg(q, f):
    return tuple(fneg(q, a) for a in f)


def pmul(q, f, g):
    if not f or not g:
        return ()
    out = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        if a:
            for j, b in enumerate(g):
                out[i + j] = fadd(q, out[i + j], fmul(q, a, b))
    return trim(out)


def deg(f):
    return len(f) - 1 if f else -10**9


def branch_of(system, f):
    q, brs = system
    for i, (r, g, c) in enumerate(brs):
        if all((f[k] if k < len(f) else 0) == r[k] for k in range(len(r))):
            return i
    raise ValueError("incomplete prefix code")


def step(system, f):
    """Return (T(f), branch index, digits consumed)."""
    q, brs = system
    i = branch_of(system, f)
    r, g, c = brs[i]
    u = padd(q, f, pneg(q, trim(r)))
    e = len(r)
    assert all((u[k] if k < len(u) else 0) == 0 for k in range(e))
    u = u[e:] if len(u) > e else ()
    return padd(q, pmul(q, g, u), trim(c)), i, e


def sigma(system, f, cap):
    """Digits consumed up to the end of the first step with deg < deg f; cap+1 if none within cap."""
    d0 = deg(f)
    x, dig = f, 0
    while dig <= cap:
        x, i, e = step(system, x)
        dig += e
        if deg(x) < d0:
            return dig
    return cap + 1


def load_spec(path):
    q = None
    brs = []
    toks = []
    for line in open(path):
        line = line.split('#')[0]
        toks += line.split()
    k = 0
    while k < len(toks):
        if toks[k] == 'q':
            q = int(toks[k + 1]); k += 2
        elif toks[k] == 'B':
            e = int(toks[k + 1]); r = tuple(int(x) for x in toks[k + 2:k + 2 + e]); k += 2 + e
            assert toks[k] == 'G'; dg = int(toks[k + 1]); g = tuple(int(x) for x in toks[k + 2:k + 3 + dg]); k += 3 + dg
            assert toks[k] == 'C'; dc = int(toks[k + 1]); c = tuple(int(x) for x in toks[k + 2:k + 3 + dc]); k += 3 + dc
            brs.append((r, trim(g), c))
        else:
            raise ValueError(toks[k])
    return (q, brs)


def step_law(system):
    """i.i.d. step law under Haar measure: list of (probability, slope, digits)."""
    q, brs = system
    return [(Fraction(1, q ** len(r)), deg(trim(g)) - len(r), len(r)) for (r, g, c) in brs]


def survivors_exact(system, bmax):
    """P(b), b = 0..bmax, as exact Fractions: the Haar measure of the t-adic x such that every
    step ending at digit count <= b ends at height (cumulative slope) >= 0.
    Uses integer counts c[d][h] = q^d * (mass alive at a step end with d digits, height h)."""
    q = system[0]
    law = step_law(system)
    emax = max(e for _, _, e in law)
    c = [dict() for _ in range(bmax + emax + 1)]
    c[0][0] = 1
    for d in range(bmax + 1):
        for h, v in c[d].items():
            for (p, s, e) in law:
                nh = h + s
                if nh >= 0:
                    c[d + e][nh] = c[d + e].get(nh, 0) + v
    P = []
    for b in range(bmax + 1):
        tot = Fraction(0)
        for d in range(max(0, b - emax + 1), b + 1):
            m = sum(c[d].values())
            if m:
                tot += Fraction(m, q ** d) * sum(p for (p, s, e) in law if e > b - d)
        P.append(tot)
    return P
