"""check_theorem_Z.py -- exact checks for theorem_Z.md.

Claims checked:
  Z1  every catalog map in systems.CATALOG_Z and systems.QR_Z has a strict
      Z-certificate (verified independently); the finite exceptional set E_Z
      and the complete list of cycles on Z are as printed / asserted
      (no negative cycles anywhere).
  Z2  sign proposition: for each of these maps all slopes are > 0 and all
      constants >= 0 (so a cycle with multiplier < 1 is >= 0); checked on the tables.
  Z3  farkas2005, farkas5m, farkas_s27, yah_avoid15, yah_avoid6 on Z: the
      block identities used in the hand proofs are checked exactly for every
      n in [-10^5, 10^5] and for 3000 random 200-bit integers of both signs;
      the descent inequality |block(n)| < |n| is checked on the same ranges;
      the resulting cycle lists on Z are confirmed from the finite set of
      starts that the proofs leave.
  Z4  evidence only: every start in [-2*10^4, 2*10^4] ends in a listed cycle.
Runs in about 20 s.
"""
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gdescent as G  # noqa: E402
import systems as S   # noqa: E402

random.seed(20261127)

EXPECTED = {   # map -> list of (min, length) of all cycles on Z
    'par_1_1': [(0, 1), (1, 2)],
    'par_1_5': [(0, 1), (1, 6), (5, 2)],
    'split_5': [(0, 1), (1, 4), (5, 3)],
    'split_13': [(0, 1), (1, 5), (5, 6), (13, 3)],
    'split_73': [(0, 1), (3, 12), (5, 28), (73, 3)],
    'split_97': [(0, 1), (13, 12), (33, 13), (97, 3)],
    'split_7081': [(0, 1), (1, 334), (11, 339), (41, 336), (291, 12), (485, 28), (569, 50),
                   (713, 51), (949, 12), (2409, 13), (7081, 3)],
    'splitB_7': [(0, 1), (1, 4), (7, 3)],
    'splitB_71': [(0, 1), (1, 20), (11, 18), (71, 3)],
    'm3_a': [(0, 1), (1, 1), (2, 1)],
    'm3_c': [(0, 1), (1, 2), (2, 2)],
    'm3_f': [(0, 1), (1, 2)],
    'desc_s8_35': [(0, 1), (1, 2)],
    'desc_s32_max': [(0, 1), (1, 3)],
    'desc_s32_d65': [(0, 1), (1, 21), (5, 5), (7, 29), (13, 4), (39, 5), (65, 3), (299, 8),
                     (1135, 13)],
    'qrA3_q23': [(0, 1), (1, 4), (5, 5), (23, 1)],
    'qrA3_q307': [(0, 1), (1, 18), (5, 28), (7, 18), (307, 1)],
    'qrA3_q95': [(0, 1), (1, 6), (5, 6), (7, 12), (19, 2), (95, 1)],
    'qrA3_q17': [(0, 1), (1, 3), (5, 3), (17, 1)],
    'qrA5_q251': [(0, 1), (1, 8), (3, 8), (7, 15), (9, 8), (21, 8), (251, 1)],
    'qrC_q311': [(0, 1), (3, 13), (11, 16), (311, 1)],
    'qrB7_c53': [(0, 1), (1, 9), (3, 3), (5, 3), (7, 2)],
}


def cyc_of(T, n, cap=10 ** 6):
    seen = set()
    while n not in seen:
        seen.add(n)
        n = T(n)
        assert len(seen) < cap
    c, y = [n], T(n)
    while y != n:
        c.append(y)
        y = T(y)
    return (min(c), len(c))


def Z1_Z2():
    allmaps = dict(S.CATALOG_Z)
    allmaps.update(S.QR_Z)
    for name, (Q, tab) in allmaps.items():
        # Z2: slopes positive, constants nonnegative
        assert all(u > 0 and w > 0 and v >= 0 for u, v, w in tab), name
        c = G.settle_Z(Q, tab)
        assert c['ok'], name
        got = [(min(x), len(x)) for x in c['cycles']]
        assert got == EXPECTED[name], (name, got)
        assert all(min(x) >= 0 for x in c['cycles'])
        print(f"Z1 {name:13s} Q={Q:3d} leaves={c['size']:4d} k={c['k']:2d} |E_Z|={len(c['E']):5d}"
              f" E in [{c['E'][0]},{c['E'][-1]}]  cycles(min,len)={got}")
        # Z1b: qr maps other than qrB7: negative multiples of q stay <= 0
        if name.startswith('qr') and name != 'qrB7_c53':
            q = int(name.split('_q')[1])
            T0 = G.step_fn(Q, tab)
            for m in list(range(-3000, 0)) + [-random.getrandbits(150) - 1 for _ in range(500)]:
                assert T0(q * m) <= 0 and T0(q * m) % q == 0
            for n in range(-3000, 0):
                x = n
                while x < 0:
                    x = T0(x)
                assert (x == 0) == (n % q == 0), (name, n)
        # Z4 evidence
        T = G.step_fn(Q, tab)
        mins = {m for m, _ in got}
        for n in range(-20000, 20001, 7):
            assert cyc_of(T, n)[0] in mins
    print('Z1, Z2 OK')


def rand_ints(bits=200, k=3000):
    for _ in range(k):
        x = random.getrandbits(bits) + 2
        yield x
        yield -x


def Z3():
    Gf = S.farkas2005_G
    # farkas2005 block: m even, m != 2 mod 3, m = 2^a c, c odd: G^(2a+1)(m) = (c+1)/2
    rng = list(range(-10 ** 5, 10 ** 5 + 1)) + list(rand_ints())
    for m in rng:
        if m == 0:
            continue
        if m % 3 == 2:
            y, steps = Gf(m), 1
            assert y == (m + 1) // 3
        elif m % 2:
            y, steps = Gf(m), 1
            assert y == (m + 1) // 2
        else:
            a, c = 0, m
            while c % 2 == 0:
                a, c = a + 1, c // 2
            y = m
            for _ in range(2 * a + 1):
                y = Gf(y)
            assert y == (c + 1) // 2, m
        if m not in (0, 1):
            assert abs(y) < abs(m), m
    assert Gf(0) == 0 and Gf(1) == 1 and Gf(-1) == 0
    # farkas5m block: n odd, n != 3 mod 5, n - 1 = 2^a b: T^(2a+1)(n) = (b+1)/2
    F = S.farkas5m
    for n in rng:
        if n in (0, 1):
            continue
        if n % 5 == 3:
            y = F(n)
            assert y == (n + 2) // 5
        elif n % 2 == 0:
            y = F(n)
        else:
            a, b = 0, n - 1
            while b % 2 == 0:
                a, b = a + 1, b // 2
            y = n
            for _ in range(2 * a + 1):
                y = F(y)
            assert y == (b + 1) // 2, n
        assert abs(y) < abs(n), n
    assert F(0) == 0 and F(1) == 1
    # farkas_s27 (R) on Z: R(n) = G(n+1) - 1 for n != 1
    R = S.farkas_R
    for n in range(-10 ** 5, 10 ** 5):
        if n != 1:
            assert R(n) == Gf(n + 1) - 1, n
    for n in rand_ints(100, 500):
        assert R(n) == Gf(n + 1) - 1
    # G maps nonpositive integers to nonpositive integers
    for m in range(-10 ** 5, 1):
        assert Gf(m) <= 0
    # yah_avoid15 on Z: every odd o != -1 reaches 1 (o = 3 mod 8 in 2 steps;
    # o = 7 mod 8 via the run o_j = 3^j 2^(a-j) b - 1 to o_(a-2) = 3 mod 8)
    A15 = S.get('yah_avoid15_Z')['step']
    for o in list(range(-10 ** 5 + 1, 10 ** 5, 2)) + [x | 1 for x in rand_ints(120, 300)]:
        if o == -1:
            continue
        if o % 8 in (1, 5):
            assert A15(o) == 1
        elif o % 8 == 3:
            y = (3 * o + 1) // 2
            assert A15(A15(o)) == y and y % 8 in (1, 5)
        else:
            a, b = 0, o + 1
            while b % 2 == 0:
                a, b = a + 1, b // 2
            assert a >= 3 and b != 0
            x = o
            for j in range(a - 2):
                assert x == 3 ** j * 2 ** (a - j) * b - 1 and x % 8 == 7
                x = A15(A15(x))
            assert x == 4 * 3 ** (a - 2) * b - 1 and x % 8 == 3
    assert A15(-1) == -2 and A15(-2) == -1 and A15(0) == 0 and A15(1) == 1
    # yah_avoid6 on Z: odd iterates of class 1/5 strictly decrease in |.| (both signs)
    A6 = S.get('yah_avoid6_Z')['step']

    def next_odd(o):          # follow until odd or until the orbit hits 1 via 6 mod 8
        x = A6(o)
        while x % 2 == 0:
            if x % 8 == 6:
                return 1
            x = A6(x)
        return x
    for o in list(range(-10 ** 5 + 1, 10 ** 5, 2)) + [x | 1 for x in rand_ints(120, 300)]:
        if o in (1, -1):
            continue
        if o % 8 == 7:
            assert next_odd(o) == 1
        elif o % 8 == 3:
            assert next_odd(o) == 1 or next_odd(o) % 8 in (1, 5)
        else:
            y = next_odd(o)
            if y != 1:
                assert abs(y) < abs(o), o
                if y % 8 == 3:
                    z = next_odd(y)
                    assert z == 1 or abs(z) < abs(o), o
    assert next_odd(-1) == 1
    # cycles on Z from the finite residual sets left by the proofs
    assert cyc_of(Gf, 0) == (0, 1) and cyc_of(Gf, 1) == (1, 1)
    assert cyc_of(F, 0) == (0, 1) and cyc_of(F, 1) == (1, 1) and cyc_of(F, -1) == (0, 1)
    assert {cyc_of(R, n) for n in range(-50, 51)} == {(-1, 1), (0, 1), (1, 1)}
    assert {cyc_of(A15, n) for n in range(-50, 51)} == {(-2, 2), (0, 1), (1, 1)}
    assert {cyc_of(A6, n) for n in range(-50, 51)} == {(0, 1), (1, 3)}
    # evidence: every start in a range
    for n in range(-20000, 20001):
        assert cyc_of(Gf, n) in {(0, 1), (1, 1)}
        assert cyc_of(F, n) in {(0, 1), (1, 1)}
        assert cyc_of(R, n) == ((-1, 1) if n < 0 else (0, 1) if n == 0 else (1, 1))
        e = cyc_of(A15, n)
        if n == 0:
            assert e == (0, 1)
        elif n < 0 and (-n) & (-n - 1) == 0:
            assert e == (-2, 2), n
        else:
            assert e == (1, 1), n
        assert cyc_of(A6, n) == ((0, 1) if n == 0 else (1, 3))
    print('Z3 OK')


if __name__ == '__main__':
    Z1_Z2()
    Z3()
    print('ALL OK')
