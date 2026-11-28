"""The non-descending 2-adic set Omega of SPLIT(a,b,d) (split5_3_deep.md, sections 3-4).

U/O coding: in state U the next bit decides the parity of the current value
(even: slope 1/2, stay U; odd: slope 1, go to O).  In state O the next bit decides the
class mod 4 (class 1: slope a/2^va, class 3: slope b/2^vb); the next state is U when
the guaranteed valuation is 2 and O when it is 1 (the output is then known to be odd).

Omega = set of 2-adic integers all of whose prefix slope products are >= 1.
Exact integer arithmetic for all counts; floats only for the displayed decimals.
"""
from fractions import Fraction
import math
from family_lib import vals


def transitions(a, b, d):
    va, vb = vals(a, b, d)
    # each transition: (from, to, (num_exp_a, num_exp_b, den_exp_2))
    return {
        'U': [('U', (0, 0, 1)), ('O', (0, 0, 0))],
        'O': [('U' if va == 2 else 'O', (1, 0, va)), ('U' if vb == 2 else 'O', (0, 1, vb))],
    }


def loop_count(a, b, d, m):
    """Exact number Z_m of words of length m from U to U whose prefix slope products are all >= 1.
    Slope = a^i b^k / 2^l; tracked exactly by (i,k,l)."""
    tr = transitions(a, b, d)
    cur = {('U', 0, 0, 0): 1}
    for _ in range(m):
        nxt = {}
        for (s, i, k, l), c in cur.items():
            for (t, (di, dk, dl)) in tr[s]:
                i2, k2, l2 = i + di, k + dk, l + dl
                if a ** i2 * b ** k2 >= 2 ** l2:
                    key = (t, i2, k2, l2)
                    nxt[key] = nxt.get(key, 0) + c
        # merge states with the same slope (needed only for speed when a or b is 1)
        cur = nxt
    return sum(c for (s, i, k, l), c in cur.items() if s == 'U')


def rho_float(a, b, d, th):
    va, vb = vals(a, b, d)
    tr = transitions(a, b, d)
    M = {('U', 'U'): 0.0, ('U', 'O'): 0.0, ('O', 'U'): 0.0, ('O', 'O'): 0.0}
    for s in 'UO':
        for (t, (di, dk, dl)) in tr[s]:
            M[(s, t)] += (a ** di * b ** dk / 2 ** dl) ** th
    al, be, ga, de = M[('U', 'U')], M[('U', 'O')], M[('O', 'U')], M[('O', 'O')]
    tr_ = al + de
    det = al * de - be * ga
    return (tr_ + math.sqrt(tr_ * tr_ - 4 * det)) / 2


def rho_min_float(a, b, d):
    lo, hi = 0.0, 8.0
    for _ in range(200):
        m1 = lo + (hi - lo) / 3
        m2 = hi - (hi - lo) / 3
        if rho_float(a, b, d, m1) < rho_float(a, b, d, m2):
            hi = m2
        else:
            lo = m1
    th = (lo + hi) / 2
    return th, rho_float(a, b, d, th)


def pow_upper(x, p, q, D=10 ** 12):
    """Rational u = k/D with u^q >= x^p (x a positive Fraction), close to x^(p/q)."""
    target = x ** p
    lo, hi = 0, D * 64
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if Fraction(mid, D) ** q >= target:
            hi = mid
        else:
            lo = mid
    return Fraction(hi, D)


def certify_upper(a, b, d, p, q, mu):
    """Exact check that rho(M_theta) <= mu for theta = p/q, using rational upper bounds of
    the entries (all entries are increasing in the base for fixed theta >= 0).
    For a nonnegative 2x2 matrix [[al,be],[ga,de]]: rho <= mu iff mu >= al, mu >= de and
    (mu-al)(mu-de) >= be*ga."""
    tr = transitions(a, b, d)
    E = {('U', 'U'): Fraction(0), ('U', 'O'): Fraction(0), ('O', 'U'): Fraction(0), ('O', 'O'): Fraction(0)}
    for s in 'UO':
        for (t, (di, dk, dl)) in tr[s]:
            base = Fraction(a ** di * b ** dk, 2 ** dl)
            E[(s, t)] += pow_upper(base, p, q)
    al, be, ga, de = E[('U', 'U')], E[('U', 'O')], E[('O', 'U')], E[('O', 'O')]
    return mu >= al and mu >= de and (mu - al) * (mu - de) >= be * ga


def H2(x):
    return 0.0 if x in (0, 1) else -x * math.log2(x) - (1 - x) * math.log2(1 - x)


# ---------------------------------------------------------------------------
# Excursion structure (split5_3_deep.md, section 4)

def otype(a, b, d):
    """'T1': O has a contracting self-loop of slope 1/2 (weighting makes the bits i.i.d.);
    'T2': O has an expanding self-loop (slope s > 1) and one return to U;
    'T3': both O-branches return to U."""
    va, vb = vals(a, b, d)
    if va == 2 and vb == 2:
        return 'T3', (Fraction(a, 4), Fraction(b, 4))
    if va == 1 and vb == 1:
        return None, None              # classes D/K, not O
    loop, ret = (Fraction(a, 2), Fraction(b, 4)) if va == 1 else (Fraction(b, 2), Fraction(a, 4))
    if loop < 1:
        return 'T1', (loop, ret)
    return 'T2', (loop, ret)


def lower_bound_counts(a, b, d, r):
    """Rigorous lower bound for dim Omega from exact excursion counts with r excursions.
    Returns (Fraction L, m, data) with dim >= L."""
    typ, (s1, s2) = otype(a, b, d)
    th, rho = rho_min_float(a, b, d)
    best = None
    if typ == 'T3':
        al, be = s1, s2
        p0 = 2 ** (-th) / rho
        pa = float(al) ** th / rho ** 2
        pb = float(be) ** th / rho ** 2
        base = (round(p0 * r), round(pa * r), round(pb * r))
        for dn0 in range(-40, 41):
            n0 = base[0] + dn0
            na, nb = base[1], base[2]
            if n0 < 0:
                continue
            fac = Fraction(1, 2) ** n0 * al ** na * be ** nb
            if fac <= 1:
                continue
            R = n0 + na + nb
            N = math.factorial(R) // (math.factorial(n0) * math.factorial(na) * math.factorial(nb))
            m = n0 + 2 * na + 2 * nb
            Z = N // R
            L = Fraction(Z.bit_length() - 1, m)
            if best is None or L > best[0]:
                best = (L, m, (n0, na, nb))
    elif typ == 'T2':
        loop, ret = s1, s2
        p0 = 2 ** (-th) / rho
        q = float(loop) ** th / rho
        Podd = float(ret) ** th / rho ** 2 / (1 - q)
        n0b = round(p0 / (p0 + Podd) * r)
        Nb = r - n0b
        Jb = round(Nb * q / (1 - q))
        for dn0 in range(-40, 41):
            n0 = n0b + dn0
            if n0 < 0:
                continue
            for dJ in (-2, 0, 2):
                J = Jb + dJ
                No = Nb
                fac = Fraction(1, 2) ** n0 * loop ** J * ret ** No
                if fac <= 1:
                    continue
                R = n0 + No
                N = math.comb(R, No) * math.comb(J + No - 1, No - 1)
                m = n0 + 2 * No + J
                Z = N // R
                L = Fraction(Z.bit_length() - 1, m)
                if best is None or L > best[0]:
                    best = (L, m, (n0, No, J))
    else:
        raise ValueError(typ)
    return best


def upper_bound_cert(a, b, d, digits=6):
    """Rational theta = p/q near theta* and rational mu with rho(M_theta) <= mu, verified exactly.
    Returns (p, q, mu); then dim Omega <= log2(mu)."""
    th, rho = rho_min_float(a, b, d)
    q = 1000
    p = round(th * q)
    mu = Fraction(math.ceil(rho * 10 ** digits * (1 + 1e-6)), 10 ** digits)
    assert certify_upper(a, b, d, p, q, mu)
    return p, q, mu
