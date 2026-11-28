"""Round 3, lens "domains": the maps studied here, as exact step functions.

Two kinds of entries.

1. Catalog maps extended to all of Z (and to rationals with odd denominator
   d, which is the same as scaling the additive constants by d).  Each is
   given as a residue table (Q, table): n = r (mod Q) -> (u n + v)/w, which
   defines the map on every integer, negative ones included.
2. New maps on quadratic orders: Z[i], Z[w] (Eisenstein), Z[sqrt(-2)],
   Z[sqrt(2)], dividing by a prime element pi of norm 2 or 3
   (see rings.py for the arithmetic).

SYSTEMS is a list of dicts with id, domain, rule, step (a Python function on
the domain's elements), question.  get(id) returns one.
"""
import os
import sys
from fractions import Fraction
from math import lcm

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rings as RG  # noqa: E402

SYSTEMS = []


def add(id, domain, rule, step, question, **extra):
    d = dict(id=id, domain=domain, rule=rule, step=step, question=question)
    d.update(extra)
    SYSTEMS.append(d)


def table_step(Q, table):
    def T(n):
        u, v, w = table[n % Q]
        x = u * n + v
        assert x % w == 0
        return x // w
    return T


def table_from_step(T, Q, base=10 ** 6):
    """Read off the affine table of a map that is affine on classes mod Q
    (two sample points per class), then confirm it on 2Q*50 further points."""
    tab = []
    for r in range(Q):
        n0, n1 = r + Q * base, r + Q * (base + 1)
        s = Fraction(T(n1) - T(n0), Q)
        b = T(n0) - s * n0
        w = lcm(s.denominator, Fraction(b).denominator)
        tab.append((int(s * w), int(b * w), w))
    S = table_step(Q, tab)
    for n in range(1, 100 * Q):
        assert S(n) == T(n), n
    return tab


# ---------------------------------------------------------------------------
# 1. catalog maps on Z
# ---------------------------------------------------------------------------
def par1(d):
    return 2, [(1, 0, 2), (1, d, 1)]


def split_table(d):
    """The unified split map M_d: even n -> n/2; odd n -> 3n + d if n*d = 1
    (mod 4), n + d if n*d = 3 (mod 4).  For d = 1 (mod 4) this is catalog
    split_d, for d = 3 (mod 4) it is catalog splitB_d."""
    Q = 4
    tab = []
    for r in range(Q):
        if r % 2 == 0:
            tab.append((1, 0, 2))
        elif (r * d) % 4 == 1:
            tab.append((3, d, 1))
        else:
            tab.append((1, d, 1))
    return Q, tab


def s_table(m, S, d=1):
    return 2 ** m, [(1, 0, 2) if r % 2 == 0 else ((3, d, 1) if r in S else (1, d, 1))
                    for r in range(2 ** m)]


S0 = (1, 3, 5, 7, 11, 13, 15, 17, 21, 23, 25, 29)

CATALOG_Z = {
    'par_1_1': par1(1), 'par_1_5': par1(5),
    'split_5': split_table(5), 'split_13': split_table(13), 'split_73': split_table(73),
    'split_97': split_table(97), 'split_7081': split_table(7081),
    'splitB_7': split_table(7), 'splitB_71': split_table(71),
    'm3_a': (3, [(1, 0, 3), (2, 1, 3), (2, 2, 3)]),
    'm3_c': (3, [(1, 0, 3), (2, 1, 1), (2, 2, 1)]),
    'm3_f': (3, [(1, 0, 3), (1, 2, 1), (1, 1, 1)]),
    'desc_s8_35': s_table(3, (3, 5)),
    'desc_s32_max': s_table(5, S0),
    'desc_s32_d65': s_table(5, S0, 65),
}


def _qr_tables():
    here = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(here, '..', '..', 'round2', 'qr'))
    import qrlib
    return {
        'qrA3_q23': (6, table_from_step(qrlib.famA(23, 3), 6)),
        'qrA3_q307': (6, table_from_step(qrlib.famA(307, 3), 6)),
        'qrA3_q95': (6, table_from_step(qrlib.famA(95, 3), 6)),
        'qrA3_q17': (6, table_from_step(qrlib.famA(17, 3), 6)),
        'qrA5_q251': (10, table_from_step(qrlib.famA(251, 5), 10)),
        'qrC_q311': (60, table_from_step(qrlib.famC(311), 60)),
        'qrB7_c53': (4, table_from_step(qrlib.famB(7, 5, 3), 4)),
    }


QR_Z = _qr_tables()

for k, (Q, tab) in list(CATALOG_Z.items()) + list(QR_Z.items()):
    add(k + '_Z', 'Z', f'{k} extended to Z by its residue table mod {Q}',
        table_step(Q, tab), 'GLOBAL on Z + complete cycle list on Z', Q=Q, table=tab)


def farkas2005_G(m):
    if m % 3 == 2:
        return (m + 1) // 3
    if m % 2 == 1:
        return (m + 1) // 2
    return 3 * m // 2


def farkas5m(n):
    if n % 5 == 3:
        return (n + 2) // 5
    return n // 2 if n % 2 == 0 else (5 * n - 3) // 2


def farkas_R(n):           # catalog farkas_s27 extended to Z
    if n == 1:
        return 1
    if n % 3 == 1:
        return (n - 1) // 3
    return n // 2 if n % 2 == 0 else (3 * n + 1) // 2


def avoid(K):
    K = frozenset(K)

    def step(n):
        if n % 8 in K:
            return 1
        return n // 2 if n % 2 == 0 else 3 * n + 1
    return step


add('farkas2005_Z', 'Z', 'm=2 mod 3 -> (m+1)/3; else odd -> (m+1)/2; else 3m/2', farkas2005_G,
    'GLOBAL on Z')
add('farkas5m_Z', 'Z', 'n=3 mod 5 -> (n+2)/5; else even -> n/2; else (5n-3)/2', farkas5m,
    'GLOBAL on Z')
add('farkas_s27_Z', 'Z', '1->1; n=1 mod 3 -> (n-1)/3; else even -> n/2; else (3n+1)/2', farkas_R,
    'GLOBAL on Z')
add('yah_avoid15_Z', 'Z', 'n=1,5 mod 8 -> 1; else Collatz', avoid({1, 5}), 'GLOBAL + basins on Z')
add('yah_avoid6_Z', 'Z', 'n=6 mod 8 -> 1; else Collatz', avoid({6}), 'GLOBAL on Z')


# ---------------------------------------------------------------------------
# 1b. the split and 1x+d families on rationals with odd denominator d
#     (numerator form: x = n/d, so the map on n is M_d resp. P_d)
# ---------------------------------------------------------------------------
def M(d):
    Q, tab = split_table(d)
    return table_step(Q, tab)


def P(d):
    return table_step(2, [(1, 0, 2), (1, d, 1)])


for d in (1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27):
    add(f'M_{d}', 'Z (= split map on (1/d)Z)',
        f'even n -> n/2; odd n -> 3n+{d} if n*{d}=1 mod 4 else n+{d}', M(d),
        'complete cycle list on Z, basins, ultimately-periodic basin?')

# ---------------------------------------------------------------------------
# 2. quadratic orders
# ---------------------------------------------------------------------------
G, E, ZM, ZP = RG.GAUSS, RG.EIS, RG.ZM2, RG.ZP2


def gauss_1xc(c):
    return RG.PiMap(G, {1: ((1, 0), c)}, f'Z[i]: z/(1+i) if (1+i)|z else z+{c}')


def gauss_unit(u, c):
    return RG.PiMap(G, {1: (u, c)}, f'Z[i]: z/(1+i) if (1+i)|z else {u}*z+{c}')


add('G1_1', 'Z[i]', 'z/(1+i) if (1+i)|z, else z+1', gauss_1xc((1, 0)), 'GLOBAL, cycles, basins')
add('G1_3', 'Z[i]', 'z/(1+i) if (1+i)|z, else z+3', gauss_1xc((3, 0)), 'GLOBAL, cycles, basins')
add('G1_2p1i', 'Z[i]', 'z/(1+i) if (1+i)|z, else z+(2+i)', gauss_1xc((2, 1)), 'GLOBAL, cycles')
add('Gi_1', 'Z[i]', 'z/(1+i) if (1+i)|z, else i z+1', gauss_unit((0, 1), (1, 0)), 'GLOBAL, cycles')
add('Gm1_1', 'Z[i]', 'z/(1+i) if (1+i)|z, else -z+1', gauss_unit((-1, 0), (1, 0)), 'GLOBAL, cycles')
add('G5_1', 'Z[i]', 'z/(1+i) if (1+i)|z, else (1+2i)z+1', gauss_unit((1, 2), (1, 0)),
    'GLOBAL (Gaussian 5x+1)')
add('E_f', 'Z[w]', 'z/(1-w) if (1-w)|z; z+2 if z=1 mod (1-w); z+1 if z=2 mod (1-w)',
    RG.PiMap(E, {1: ((1, 0), (2, 0)), 2: ((1, 0), (1, 0))}), 'GLOBAL, cycles')
add('E_w', 'Z[w]', 'z/(1-w) if (1-w)|z; w z - 1 if z = 1 mod (1-w); w z + 1 if z = 2 mod (1-w)',
    RG.PiMap(E, {1: ((0, 1), (-1, 0)), 2: ((0, 1), (1, 0))}), 'GLOBAL, cycles')
add('ZM2_1', 'Z[sqrt-2]', 'z/sqrt(-2) if divisible, else z+1', RG.PiMap(ZM, {1: ((1, 0), (1, 0))}),
    'GLOBAL, cycles')
add('ZP2_1', 'Z[sqrt2]', 'z/sqrt(2) if divisible, else z+1', RG.PiMap(ZP, {1: ((1, 0), (1, 0))}),
    'GLOBAL, cycles')


def gauss_naive_x1(z):
    """Naive lift of the x+1 map to Z[i] dividing by the rational prime 2."""
    a, b = z
    if a % 2 == 0 and b % 2 == 0:
        return (a // 2, b // 2)
    return (a + 1, b)


add('G2_naive', 'Z[i]', 'z/2 if 2|z, else z+1', gauss_naive_x1, 'GLOBAL (fails)')

BY_ID = {s['id']: s for s in SYSTEMS}
assert len(BY_ID) == len(SYSTEMS)


def get(id):
    return BY_ID[id]


# ---------------------------------------------------------------------------
# 3. Gaussian S-family members settled by a norm-descent certificate
#    z/pi if pi | z;  (1+2i) z + 1 if z mod pi^5 in S;  z + 1 otherwise.
#    Residue of z = x + yi mod pi^5 = (4+4i): (x mod 4, (y + 4*floor(x/4)) mod 8).
# ---------------------------------------------------------------------------
def gauss_S(m, S):
    import gcert
    S = set(S)
    return gcert.GaussMap(G, m, lambda r: ((1, 2), (1, 0)) if r in S else ((1, 0), (1, 0)))


GS5_DEEP_S = [(0, 3), (0, 7), (1, 4), (2, 7), (3, 0)]
GS5_MAX_S = [(0, 3), (1, 4), (2, 1), (2, 3), (2, 5), (3, 0), (3, 2)]
GS5_9_S = [(0, 3), (0, 7), (1, 4), (1, 6), (2, 1), (2, 5), (3, 0), (3, 2), (3, 6)]
GS4_S = [(1, 2), (2, 1), (3, 2)]          # m = 4: residue (x mod 4, y mod 4)
add('GS5_deep', 'Z[i]', 'z/(1+i) if (1+i)|z; (1+2i)z+1 if z mod (1+i)^5 in ' + str(GS5_DEEP_S)
    + '; else z+1', gauss_S(5, GS5_DEEP_S), 'GLOBAL + cycles')
add('GS5_max', 'Z[i]', 'z/(1+i) if (1+i)|z; (1+2i)z+1 if z mod (1+i)^5 in ' + str(GS5_MAX_S)
    + '; else z+1', gauss_S(5, GS5_MAX_S), 'GLOBAL + cycles')
add('GS5_9', 'Z[i]', 'z/(1+i) if (1+i)|z; (1+2i)z+1 if z mod (1+i)^5 in ' + str(GS5_9_S)
    + '; else z+1', gauss_S(5, GS5_9_S), 'GLOBAL + cycles')
add('GS4_max', 'Z[i]', 'z/(1+i) if (1+i)|z; (1+2i)z+1 if z mod (1+i)^4 = 4 in ' + str(GS4_S)
    + '; else z+1', gauss_S(4, GS4_S), 'GLOBAL + cycles')
BY_ID = {s['id']: s for s in SYSTEMS}
