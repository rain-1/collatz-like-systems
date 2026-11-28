"""Library of table maps for the transport search.

Each entry: dict(id, Q, table, status, p, note)
  status in
    'open'          an open census entry or round-3 open core
    'cert'          settled by a plain descent certificate (decide.py CERT)
    'thmH'          settled by Theorem H (accel)
    'mixed'         settled mixed-base (non-unit) system (round 3 mixedbase, Farkas type)
    'dress'         settled by the dressing first-return argument (round 3 accel/dressing.md)
    'div'           has a proved divergent orbit (round 3 divergence)
    'random'        random unit-multiplier table (search population)
  p : the prime if the table is a unit-multiplier p-adic table at modulus p^m, else None.
Tables are checked against the round-3 step functions in check_library.py.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
R3 = os.path.join(HERE, '..', '..', 'round3')


def unit_prime(Q, table):
    """p if Q = p^m and every multiplier is u/p^e with p not dividing u; else None."""
    ps = [q for q in range(2, Q + 1) if Q % q == 0 and all(q % s for s in range(2, q))]
    if len(ps) != 1:
        return None
    p = ps[0]
    for (u, v, w) in table:
        if u % p == 0:
            return None
        x = w
        while x % p == 0:
            x //= p
        if x != 1:
            return None
    return p


def s_table(m, S):
    return [(1, 0, 2) if r % 2 == 0 else ((3, 1, 1) if r in S else (1, 1, 1))
            for r in range(2 ** m)]


def classes_table(m, R, a, b):
    """n = r (mod m), r in R -> (n + R[r])/m first; else even -> n/2; else (a n + b)/2."""
    Q = 2 * m if m % 2 else m
    t = []
    for r in range(Q):
        if r % m in R:
            t.append((1, R[r % m], m))
        elif r % 2 == 0:
            t.append((1, 0, 2))
        else:
            t.append((a, b, 2))
    return Q, t


def div23_plus_table(q, R, a=5):
    from math import gcd
    Q = q * 6 // gcd(q, 6)
    t = []
    for r in range(Q):
        if r % q in R:
            t.append((1, R[r % q], q))
        elif r % 2 == 0:
            t.append((1, 0, 2))
        elif r % 3 == 0:
            t.append((1, 0, 3))
        else:
            t.append((a, 1, 1))
    return Q, t


LIB = []


def add(id, Q, table, status, note=""):
    LIB.append(dict(id=id, Q=Q, table=list(table), status=status,
                    p=unit_prime(Q, table), note=note))


def build():
    if LIB:
        return LIB
    sys.path.insert(0, os.path.join(R3, 'dichotomy'))
    from open_tables import OPEN
    for k, (Q, t) in OPEN.items():
        add(k.split(' ')[0], Q, t, 'open', k)
    # S-family cores (accel/sfamily_obst.md); sf3_37 is 3x+1 in disguise, sf3_1357 is 3x+1
    for S in [(7,), (1, 7), (5, 7), (1, 5, 7), (3, 5, 7), (1, 3, 7), (1, 3), (1, 3, 5), (3, 7)]:
        add("sf3_" + "".join(map(str, S)), 8, s_table(3, S), 'open', "S-family core")
    # mixedbase open
    for sid, (m, R, a, b) in {"mb_pair_3_27m": (27, {13: -13}, 3, 1),
                              "mb_s3_27": (27, {26: 1}, 3, 1),
                              "mb_pair_5_25p": (25, {13: 12}, 5, -3)}.items():
        Q, t = classes_table(m, R, a, b)
        if sid == "mb_pair_3_27m":
            continue          # domain N0 (0 maps to 0 ... fine) but class 13 -> (n-13)/27 hits 0
        add(sid, Q, t, 'open', 'mixedbase open')
    Q, t = div23_plus_table(4, {2: 2})
    add("div23_5n1+2mod4", Q, t, 'open', 'mixedbase open (div23_5n1 + n=2 mod 4 -> (n+2)/4)')

    # ---- settled: dichotomy CERT systems
    from systems import SYSTEMS as DS
    for s in DS:
        add(s['id'], s['Q'], s['table'], 'cert')
    sys.path.pop(0)
    # ---- Theorem H (accel)
    acc_h32 = [(1, 0, 2) if r % 2 == 0 else ((1, 1, 1) if r in (5, 9, 21, 25) else
               ((1, 9, 1) if r == 29 else (3, 1, 1))) for r in range(32)]
    acc_h16 = [(1, 0, 2) if r % 2 == 0 else ((1, 1, 1) if r in (5, 9) else
               ((1, 5, 1) if r == 13 else (3, 1, 1))) for r in range(16)]
    acc_h9 = [(1, 0, 3), (2, 1, 3), (4, 4, 3), (1, 0, 3), (2, 4, 3), (4, 1, 3), (1, 0, 3),
              (2, 7, 3), (4, 1, 3)]
    add("acc_h32", 32, acc_h32, 'thmH')
    add("acc_h16", 16, acc_h16, 'thmH')
    add("acc_h9", 9, acc_h9, 'thmH')
    # ---- mixedbase settled
    for sid, (m, R, a, b) in {"mb_pair_3_9p": (9, {5: 4}, 3, -1),
                              "mb_s3_3": (3, {2: 1}, 3, 1), "mb_s3_9": (9, {8: 1}, 3, 1),
                              "mb_s5_5": (5, {3: 2}, 5, 1), "mb_s7_7": (7, {4: 3}, 7, 1),
                              "mb_t27": (27, {17: 10, 26: 1}, 3, 1),
                              "mb_f25": (25, {8: 17, 23: 2}, 5, 1),
                              "mb_s49": (49, {32: 17, 39: 10}, 7, 1)}.items():
        Q, t = classes_table(m, R, a, b)
        add(sid, Q, t, 'mixed')
    for sid, (q, R) in {"mb_d23_8": (8, {7: 1}), "mb_d23_4": (4, {3: 1}),
                        "mb_d23_30": (30, {26: 4})}.items():
        Q, t = div23_plus_table(q, R)
        add(sid, Q, t, 'mixed')
    # ---- dressing (accel/dressing.md), tables mod 6
    d23 = [(3, 0, 2) if r % 2 == 0 else ((1, 0, 3) if r % 3 == 0 else (1, 1, 1)) for r in range(6)]
    d32 = [(4, 0, 3) if r % 3 == 0 else ((1, 0, 2) if r % 2 == 0 else (1, 1, 1)) for r in range(6)]
    add("dress_23_x1", 6, d23, 'dress')
    add("dress_32_x1", 6, d32, 'dress')
    # ---- divergence (round 3): 5x+1 with one class modified
    fx10 = [(1, 0, 2) if r % 2 == 0 else (5, 1, 1) for r in range(64)]
    fx10[10] = (5, 5, 1)
    fx26 = [(1, 0, 2) if r % 2 == 0 else (5, 1, 1) for r in range(32)]
    fx26[26] = (7, 1, 1)
    add("fx10_64", 64, fx10, 'div')
    add("fx26_32", 32, fx26, 'div')
    return LIB


def by_id(i):
    for s in build():
        if s['id'] == i:
            return s
    raise KeyError(i)


if __name__ == "__main__":
    for s in build():
        print(f"{s['id']:24s} Q={s['Q']:4d} p={s['p']} {s['status']}")
