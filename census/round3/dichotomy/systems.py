"""Round 3, lens 'dichotomy': newly settled systems (same style as census/systems.py).

Every system is a table map: n = r (mod Q) -> (u n + v)/w with table[r] = (u, v, w).
Each was decided CERT by decide.py; GLOBAL holds and `cycles` is the COMPLETE list of
cycles (each written from its minimum).  `kstar` is the least step count of ANY plain
descent certificate (Theorem 3).  Verified by check_systems.py.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from families import s_family, base3_S, base3_table, rule_string

SYSTEMS = []


def mod_table(Q, table):
    def step(n):
        u, v, w = table[n % Q]
        x = u * n + v
        assert x % w == 0
        return x // w
    return step


def add(id, rule, Q, table, kstar, cycles, note=""):
    SYSTEMS.append(dict(id=id, question="GLOBAL", rule=rule, Q=Q, table=table,
                        step=mod_table(Q, table), seed=1, kstar=kstar,
                        cycles=None if cycles is None else [tuple(c) for c in cycles], note=note))


def D_table(Q, a, S):
    """2|n -> n/2; else 3|n -> n/3; else a n + 1 if n mod Q in S, else n + 1."""
    return [(1, 0, 2) if r % 2 == 0 else ((1, 0, 3) if r % 3 == 0 else
            ((a, 1, 1) if r in S else (1, 1, 1))) for r in range(Q)]


C8 = [(1, 1), (1, 2), (2, 1), (2, -1), (4, 1), (4, -1), (5, 1), (5, -1)]
U9 = [1, 2, 4, 5, 7, 8]

# ---- record depth: the deepest certificates found (deep.md)
S6 = {5, 7, 13, 23, 25, 31, 33, 35, 39, 47, 49, 51, 59, 61}
add("dch_S6_332", "even n -> n/2; odd n -> 3n+1 if n mod 64 in {5,7,13,23,25,31,33,35,39,47,49,51,59,61}, else n+1",
    64, s_family(6, S6), 332, [(1, 2)])

B81_2 = {2, 7, 14, 16, 19, 20, 23, 25, 28, 32, 34, 37, 38, 40, 41, 44, 47, 49, 50, 53, 55, 56,
         58, 59, 62, 67, 70, 71, 73, 77, 79}
add("dch_B81a2_655", "3|n -> n/3; n mod 81 in S -> 2n+1 (S = 31 classes, see table); other 3 not| n -> n+1",
    81, base3_S(81, 2, B81_2), 655, [(2, 5, 6), (22, 23, 47, 95, 191, 192, 64, 65, 66)])

B81_5 = {1, 2, 7, 8, 10, 11, 14, 22, 29, 31, 47, 55, 59, 61, 67, 70, 73, 76, 77, 79}
add("dch_B81a5_254", "3|n -> n/3; n mod 81 in S -> 5n+1 (S = 20 classes); other 3 not| n -> n+1",
    81, base3_S(81, 5, B81_5), 254,
    [(2, 11, 56, 57, 19, 20, 21, 7, 36, 12, 4, 5, 6), (8, 41, 42, 14, 71, 72, 24)])

B81_4 = {8, 14, 16, 17, 19, 25, 29, 32, 34, 35, 40, 53, 55, 59, 64, 70, 73, 74}
add("dch_B81a4_184", "3|n -> n/3; n mod 81 in S -> 4n+1 (S = 18 classes); other 3 not| n -> n+1",
    81, base3_S(81, 4, B81_4), 184, [(1, 2, 3)])

# ---- base-3 phase diagram (scan_base3.out)
add("dch_B27a5_66", "3|n -> n/3; n mod 27 in {2,4,16,17,23} -> 5n+1; other 3 not| n -> n+1",
    27, base3_S(27, 5, {2, 4, 16, 17, 23}), 66,
    [(1, 2, 11, 12, 4, 21, 7, 8, 9, 3), (28, 29, 146, 147, 49, 50, 251, 252, 84)])
add("dch_B27a8_65", "3|n -> n/3; n mod 27 in {7,8,14,17} -> 8n+1; other 3 not| n -> n+1",
    27, base3_S(27, 8, {7, 8, 14, 17}), 65,
    [(1, 2, 3), (7, 57, 19, 20, 21), (8, 65, 66, 22, 23, 24), (13, 14, 113, 114, 38, 39),
     (16, 17, 137, 138, 46, 47, 48)])
add("dch_B27a4_49", "3|n -> n/3; n mod 27 in {4,11,14,17,22} -> 4n+1; other 3 not| n -> n+1",
    27, base3_S(27, 4, {4, 11, 14, 17, 22}), 49, [(1, 2, 3)])
add("dch_B27a2_max14", "3|n -> n/3; n mod 27 in {1,2,4,5,7,10,11,13,14,17,19,20,22,25} -> 2n+1; other 3 not| n -> n+1",
    27, base3_S(27, 2, {1, 2, 4, 5, 7, 10, 11, 13, 14, 17, 19, 20, 22, 25}), 39, [(1, 3)],
    "2n+1 on 14 of the 18 unit classes mod 27 (maximum possible: no 15-set is certifiable)")
add("dch_C9_33", "3|n -> n/3; n=1,2,4,5,7,8 mod 9 -> 5n-1, 2n+1, 2n-1, n+1, 4n+1, 2n-1",
    9, base3_table(9, dict(zip(U9, [(5, -1), (2, 1), (2, -1), (1, 1), (4, 1), (2, -1)]))), 33, [(2, 5, 6)],
    "deepest certificate among all 8^6 mod-9 tables of family C9")
add("dch_C9_prod2500", "3|n -> n/3; n=1,2,4,5,7,8 mod 9 -> 5n+1, 5n-1, 4n-1, 5n+1, 5n+1, n+1",
    9, base3_table(9, dict(zip(U9, [(5, 1), (5, -1), (4, -1), (5, 1), (5, 1), (1, 1)]))), 6, [(1, 6, 2, 9, 3)],
    "largest product of multipliers (2500) among certifiable C9 tables (one of two tables attaining it)")

# ---- mixed modulus 36 (scan_mixed.out): neighbours of the open div23_5n1 / div23_7n1
add("dch_D36a5_8", "2|n -> n/2; else 3|n -> n/3; else 5n+1 if n mod 36 in {1,5,7,17,23,25,29,31}, else n+1",
    36, D_table(36, 5, {1, 5, 7, 17, 23, 25, 29, 31}), 27, [(1, 6, 3)],
    "5n+1 on 8 of the 12 unit classes mod 36 (maximum); open map div23_5n1 has all 12")
add("dch_D36a7_7", "2|n -> n/2; else 3|n -> n/3; else 7n+1 if n mod 36 in {5,11,13,23,25,29,31}, else n+1",
    36, D_table(36, 7, {5, 11, 13, 23, 25, 29, 31}), 15, [(1, 2)],
    "7n+1 on 7 of 12 unit classes mod 36 (maximum); open map div23_7n1 has all 12")
add("dch_D36a7_43", "2|n -> n/2; else 3|n -> n/3; else 7n+1 if n mod 36 in {1,31}, else n+1",
    36, D_table(36, 7, {1, 31}), 43, [(1, 8, 4, 2)], "deepest member of D(36,7)")

U27 = [r for r in range(27) if r % 3]
C27_REC = {1: (1, 1), 2: (2, -1), 4: (5, 1), 5: (2, 1), 7: (2, -1), 8: (2, -1), 10: (1, 1), 11: (4, -1),
           13: (2, -1), 14: (1, 1), 16: (1, 2), 17: (5, -1), 19: (1, 1), 20: (2, 1), 22: (5, 1),
           23: (1, 1), 25: (4, 1), 26: (1, 1)}
add("dch_C27_2466", "3|n -> n/3; n mod 27 = 1,10,14,19,23,26 -> n+1; 16 -> n+2; 5,20 -> 2n+1; "
    "2,7,8,13 -> 2n-1; 25 -> 4n+1; 11 -> 4n-1; 4,22 -> 5n+1; 17 -> 5n-1",
    27, base3_table(27, C27_REC), 2466, [(1, 2, 3), (5, 11, 43, 45, 15),
                                         (125, 624, 208, 209, 419, 420, 140, 281, 1123, 1125, 375)],
    "depth record: every plain descent certificate needs 2466 steps; near-critical cycle 80/81")

# ---- nearest provable neighbours of open entries (neighbours.out)
add("dch_split5_1_nb8", "even n -> n/2; n=1 mod 8 -> 5n+1; n=5 mod 8 -> 3n+1; n=3 mod 4 -> n+1",
    8, [(1, 0, 2), (5, 1, 1), (1, 0, 2), (1, 1, 1), (1, 0, 2), (3, 1, 1), (1, 0, 2), (1, 1, 1)],
    5, [(1, 6, 3, 4, 2)], "one-class neighbour of the open split5_1 (CLS-048)")
add("dch_div23_5n1_nb12", "2|n -> n/2; else 3|n -> n/3; else n+1 if n = 5, 11 mod 12, else 5n+1",
    12, D_table(12, 5, {1, 7}), 4, [(1, 6, 3)],
    "two-class neighbour of the open div23_5n1 (CLS-002): 5n+1 kept on n = 1, 7 mod 12")
add("dch_s32p9_nb64", "even n -> n/2 except n = 18 mod 64 -> (n+46)/64; odd n -> 3n+1 if n mod 32 in "
    "{1,3,5,7,9,11,15,17,21,23,25,29} and n != 13 mod 64, else n+1",
    64, [(1, 46, 64) if r == 18 else ((1, 1, 1) if r == 13 else t)
         for r, t in enumerate(s_family(6, {1, 3, 5, 7, 9, 11, 13, 15, 17, 21, 23, 25, 29}
                                       | {x + 32 for x in (1, 3, 5, 7, 9, 11, 13, 15, 17, 21, 23, 25, 29)}))],
    46, [(1, 4, 2), (7, 22, 11, 34, 17, 52, 26, 13, 14)],
    "two-class neighbour of the open desc_s32_plus9 (CLS-052)")

BY_ID = {s["id"]: s for s in SYSTEMS}
