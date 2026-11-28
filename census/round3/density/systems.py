"""Round 3, lens "density": the maps treated here, as exact residue tables.

All of them are existing catalog entries (the density lens proves new
theorems about known open systems; it adds no new map).  Each entry gives
  id, CLS ids, the TableMap, and `step` (a Python step function).
The tables are checked against census/systems.py and
census/round2/descent/systems.py by check_density.py (step agreement on
1 <= n < 20000).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from density_lib import TableMap  # noqa: E402


def par(a, d):
    # even n -> n/2, odd n -> a n + d
    return [(1, 0, 2), (a, d, 1)]


def split(a, d, b=1):
    # even -> n/2; 1 mod 4 -> a n + d; 3 mod 4 -> b n + d
    return [(1, 0, 2), (a, d, 1), (1, 0, 2), (b, d, 1)]


def div_else(primes, a, d):
    Q = 1
    for p in primes:
        Q *= p
    t = []
    for r in range(Q):
        for p in primes:
            if r % p == 0:
                t.append((1, 0, p))
                break
        else:
            t.append((a, d, 1))
    return Q, t


def m3(a, c1, b, c2, w1=1, w2=1):
    return [(1, 0, 3), (a, c1, w1), (b, c2, w2)]


S_PLUS9 = (1, 3, 5, 7, 9, 11, 13, 15, 17, 21, 23, 25, 29)


def s_table(m, S, d=1):
    Q = 2 ** m
    return [(1, 0, 2) if r % 2 == 0 else ((3, d, 1) if r in S else (1, d, 1))
            for r in range(Q)]


SYSTEMS = []


def add(id, cls, catalog_id, Q, table, rule):
    T = TableMap(id, Q, table, rule=rule)
    SYSTEMS.append(dict(id=id, cls=cls, catalog=catalog_id, T=T, step=T.step, rule=rule))


Q6, D235 = None, None
q, t = div_else((2, 3, 5), 7, 1)
add("div235_7n1", "CLS-001/058", "div235_7n1_s11", q, t,
    "2|n -> n/2; else 3|n -> n/3; else 5|n -> n/5; else 7n+1")
q, t = div_else((2, 3), 5, 1)
add("div23_5n1", "CLS-002/059", "div23_5n1_s7", q, t,
    "2|n -> n/2; else 3|n -> n/3; else 5n+1")
q, t = div_else((2, 3), 7, 1)
add("div23_7n1", "CLS-003/060", "div23_7n1_s5", q, t,
    "2|n -> n/2; else 3|n -> n/3; else 7n+1")
add("m3_b", "CLS-004/061", "m3_b_s8", 3, m3(4, -1, 4, 1, 3, 3),
    "3|n -> n/3; 1 mod 3 -> (4n-1)/3; 2 mod 3 -> (4n+1)/3")
add("m3_d", "CLS-005/062", "m3_d_s7", 3, m3(4, 2, 4, 1),
    "3|n -> n/3; 1 mod 3 -> 4n+2; 2 mod 3 -> 4n+1")
add("m3_e", "CLS-006/007", "m3_e_s7", 3, m3(7, 2, 7, 1),
    "3|n -> n/3; 1 mod 3 -> 7n+2; 2 mod 3 -> 7n+1")
add("m3_g", "CLS-008/063", "m3_g_s7", 3, m3(5, 1, 5, 2),
    "3|n -> n/3; 1 mod 3 -> 5n+1; 2 mod 3 -> 5n+2")
for a, d, cls in [(3, 1, "CLS-013"), (3, -1, "CLS-018"), (3, 3, "CLS-014"),
                  (3, 5, "CLS-015"), (3, 7, "CLS-016"), (3, 9, "CLS-017"),
                  (3, 13, "CLS-011"), (3, 17, "CLS-012"),
                  (5, 1, "CLS-022/024"), (5, 3, "CLS-027"), (5, 5, "CLS-029"),
                  (5, 7, "CLS-030"), (5, 11, "CLS-020"), (5, 131, "CLS-021"),
                  (5, 353, "CLS-025"), (7, 1, "CLS-032/034"), (7, 7, "CLS-035"),
                  (9, 1, "CLS-037"), (6, 2, "CLS-031"), (10, 2, "CLS-010")]:
    tag = "par_%d_%s%d" % (a, "m" if d < 0 else "", abs(d))
    add(tag, cls, None, 2, par(a, d), "even n -> n/2; odd n -> %dn%+d" % (a, d))
add("split5_1", "CLS-048/064", "split5_1_s27", 4, split(5, 1),
    "even -> n/2; 1 mod 4 -> 5n+1; 3 mod 4 -> n+1")
add("split5_3", "CLS-049/065", "split5_3_s27", 4, split(5, 3),
    "even -> n/2; 1 mod 4 -> 5n+3; 3 mod 4 -> n+3")
add("desc_m3_4n5", "CLS-051", None, 3, m3(4, 5, 2, 2),
    "3|n -> n/3; 1 mod 3 -> 4n+5; 2 mod 3 -> 2n+2")
add("desc_s32_plus9", "CLS-052", None, 32, s_table(5, S_PLUS9),
    "even -> n/2; odd -> 3n+1 if n mod 32 in S, else n+1 (S = all odd but 19,27,31)")
add("desc_split7_1", "CLS-053", None, 4, split(7, 1),
    "even -> n/2; 1 mod 4 -> 7n+1; 3 mod 4 -> n+1")
# permutations (positive drift; treated by the expanding-side theorems)
add("perm_1932", "CLS-038/040", "perm_1932_s8", 3, [(2, 0, 3), (4, -1, 3), (4, 1, 3)],
    "3q->2q; 3q+1->4q+1; 3q+2->4q+3")
add("perm_1932inv", "CLS-042", "perm_1932inv_s8", 4,
    [(3, 0, 2), (3, 1, 4), (3, 0, 2), (3, -1, 4)], "2q->3q; 4q+1->3q+1; 4q+3->3q+2")
add("perm_swap", "CLS-047", "perm_swap_s8", 3, [(2, 0, 3), (4, 5, 3), (4, -5, 3)],
    "3q->2q; 3q+1->4q+3; 3q+2->4q+1")
add("perm_b", "CLS-044", "perm_b_s7", 3, [(4, 0, 3), (4, 2, 3), (2, -1, 3)],
    "3q->4q; 3q+1->4q+2; 3q+2->2q+1")
add("perm_c", "CLS-045", "perm_c_s8", 4, [(3, 0, 2), (3, 5, 4), (3, 0, 2), (3, -5, 4)],
    "2q->3q; 4q+1->3q+2; 4q+3->3q+1")
add("perm_d", "CLS-046", "perm_d_s3", 8,
    [(5, 0, 2), (5, 3, 8), (5, 0, 2), (5, 1, 8), (5, 0, 2), (5, -1, 8), (5, 0, 2), (5, -3, 8)],
    "2q->5q; 8q+1->5q+1; 8q+3->5q+2; 8q+5->5q+3; 8q+7->5q+4")

BY_ID = {s["id"]: s for s in SYSTEMS}


def get(id):
    return BY_ID[id]
