"""The open GLOBAL entries of census/open_collatz_systems.txt that are table maps,
written as (Q, table) with table[r] = (u, v, w):  n = r (mod Q) -> (u n + v)/w.

Excluded (not table maps satisfying (H1)-(P), or not GLOBAL questions):
  CLS-009/010 par_10_2 and CLS-031 par_6_2: u even (H1 fails); the accelerated maps
     odd n -> (10n+2)/2 = 5n+1 and (6n+2)/2 = 3n+1 have the same orbits up to the
     inserted even term, so GLOBAL is equivalent to par_5_1 / par_3_1 (listed).
  CLS-056 yah_avoid57: constant branch (u = 0).   CLS-066 up_ct3: not a GLOBAL question.
  CLS-039/041/043/050/054/055 and the seed questions: FATE questions.
Every table below is checked against the census step functions in check_dichotomy.py.
"""


def par(a, d):
    return (2, [(1, 0, 2), (a, d, 1)])


def m3(a, c1, b, c2):
    return (3, [(1, 0, 3), (a, c1, 1), (b, c2, 1)])


def divchain(primes, a):
    Q = 1
    for p in primes:
        Q *= p
    tab = []
    for r in range(Q):
        for p in primes:
            if r % p == 0:
                tab.append((1, 0, p))
                break
        else:
            tab.append((a, 1, 1))
    return (Q, tab)


S0p9 = (1, 3, 5, 7, 9, 11, 13, 15, 17, 21, 23, 25, 29)

OPEN = {
    "m3_b (CLS-004/061)": (3, [(1, 0, 3), (4, -1, 3), (4, 1, 3)]),
    "m3_d (CLS-005/062)": m3(4, 2, 4, 1),
    "m3_e (CLS-007)": m3(7, 2, 7, 1),
    "m3_g (CLS-008/063)": m3(5, 1, 5, 2),
    "par_3_13 (CLS-011)": par(3, 13),
    "par_3_17 (CLS-012)": par(3, 17),
    "par_3_1 (CLS-013)": par(3, 1),
    "par_3_3 (CLS-014)": par(3, 3),
    "par_3_5 (CLS-015)": par(3, 5),
    "par_3_7 (CLS-016)": par(3, 7),
    "par_3_9 (CLS-017)": par(3, 9),
    "par_3_m1 (CLS-018)": par(3, -1),
    "par_5_11 (CLS-020)": par(5, 11),
    "par_5_131 (CLS-021)": par(5, 131),
    "par_5_1 (CLS-022/024)": par(5, 1),
    "par_5_353 (CLS-025)": par(5, 353),
    "par_5_3 (CLS-027)": par(5, 3),
    "par_5_5 (CLS-029)": par(5, 5),
    "par_5_7 (CLS-030)": par(5, 7),
    "par_7_1 (CLS-032/034)": par(7, 1),
    "par_7_7 (CLS-035)": par(7, 7),
    "par_9_1 (CLS-037)": par(9, 1),
    "perm_1932 (CLS-038/040)": (3, [(2, 0, 3), (4, -1, 3), (4, 1, 3)]),
    "perm_1932inv (CLS-042)": (4, [(3, 0, 2), (3, 1, 4), (3, 0, 2), (3, -1, 4)]),
    "perm_b (CLS-044)": (3, [(4, 0, 3), (4, 2, 3), (2, -1, 3)]),
    "perm_c (CLS-045)": (4, [(3, 0, 2), (3, 5, 4), (3, 0, 2), (3, -5, 4)]),
    "perm_d (CLS-046)": (8, [(5, 0, 2), (5, 3, 8), (5, 0, 2), (5, 1, 8),
                             (5, 0, 2), (5, -1, 8), (5, 0, 2), (5, -3, 8)]),
    "perm_swap (CLS-047)": (3, [(2, 0, 3), (4, 5, 3), (4, -5, 3)]),
    "split5_1 (CLS-048/064)": (4, [(1, 0, 2), (5, 1, 1), (1, 0, 2), (1, 1, 1)]),
    "split5_3 (CLS-049/065)": (4, [(1, 0, 2), (5, 3, 1), (1, 0, 2), (1, 3, 1)]),
    "desc_m3_4n5 (CLS-051)": m3(4, 5, 2, 2),
    "desc_s32_plus9 (CLS-052)": (32, [(1, 0, 2) if r % 2 == 0 else
                                      ((3, 1, 1) if r in S0p9 else (1, 1, 1)) for r in range(32)]),
    "desc_split7_1 (CLS-053)": (4, [(1, 0, 2), (7, 1, 1), (1, 0, 2), (1, 1, 1)]),
    "div23_5n1 (CLS-002/059)": divchain((2, 3), 5),
    "div23_7n1 (CLS-003/060)": divchain((2, 3), 7),
    "div235_7n1 (CLS-001/058)": divchain((2, 3, 5), 7),
}
