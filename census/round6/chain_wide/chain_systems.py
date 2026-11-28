"""Systems treated by the chain_wide lens, as exact residue tables
(table[r] = (u, v, w): n = r mod Q -> (u n + v)/w).

Named systems are copied from census/round3/density/systems.py (cross-checked
there against census/systems.py) and census/round3/accel/systems.py (S-family);
check_chain.py re-checks step agreement with those files.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(CENSUS, "round3", "density"))
from density_lib import TableMap  # noqa: E402


def par(a, d):
    return [(1, 0, 2), (a, d, 1)]


def split(a, d, b=1):
    return [(1, 0, 2), (a, d, 1), (1, 0, 2), (b, d, 1)]


def m3(a, c1, b, c2, w1=1, w2=1):
    return [(1, 0, 3), (a, c1, w1), (b, c2, w2)]


def s_table(m, S, d=1):
    Q = 2 ** m
    return [(1, 0, 2) if r % 2 == 0 else ((3, d, 1) if r in S else (1, d, 1))
            for r in range(Q)]


S_PLUS9 = (1, 3, 5, 7, 9, 11, 13, 15, 17, 21, 23, 25, 29)

NAMED = []   # (id, CLS / origin, Q, table, rule, kind)


def add(id, origin, Q, table, rule, kind="contracting"):
    NAMED.append(dict(id=id, origin=origin, T=TableMap(id, Q, table, rule=rule), rule=rule,
                      kind=kind))


for d, cls in [(1, "CLS-013"), (-1, "CLS-018"), (3, "CLS-014"), (5, "CLS-015"),
               (7, "CLS-016"), (9, "CLS-017"), (13, "CLS-011"), (17, "CLS-012")]:
    add("par_3_%s%d" % ("m" if d < 0 else "", abs(d)), cls, 2, par(3, d),
        "even n -> n/2; odd n -> 3n%+d" % d)
for S, name in [((7,), "sf3_7 (core K7)"), ((1, 7), "sf3_17"), ((5, 7), "sf3_57"),
                ((1, 5, 7), "sf3_157"), ((3, 5, 7), "sf3_357"), ((1, 3), "sf3_13"),
                ((1, 3, 5), "sf3_135")]:
    add(name.split()[0], "round3/accel " + name, 8, s_table(3, S),
        "even n -> n/2; odd n -> 3n+1 if n mod 8 in %s, else n+1" % (set(S),))
add("split5_1", "CLS-048/064", 4, split(5, 1), "even -> n/2; 1 mod 4 -> 5n+1; 3 mod 4 -> n+1")
add("split5_3", "CLS-049/065", 4, split(5, 3), "even -> n/2; 1 mod 4 -> 5n+3; 3 mod 4 -> n+3")
add("m3_b", "CLS-004/061", 3, m3(4, -1, 4, 1, 3, 3),
    "3|n -> n/3; 1 mod 3 -> (4n-1)/3; 2 mod 3 -> (4n+1)/3")
add("m3_d", "CLS-005/062", 3, m3(4, 2, 4, 1), "3|n -> n/3; 1 mod 3 -> 4n+2; 2 mod 3 -> 4n+1")
add("m3_g", "CLS-008/063", 3, m3(5, 1, 5, 2), "3|n -> n/3; 1 mod 3 -> 5n+1; 2 mod 3 -> 5n+2")
add("desc_split7_1", "CLS-053", 4, split(7, 1), "even -> n/2; 1 mod 4 -> 7n+1; 3 mod 4 -> n+1")
add("desc_m3_4n5", "CLS-051", 3, m3(4, 5, 2, 2), "3|n -> n/3; 1 mod 3 -> 4n+5; 2 mod 3 -> 2n+2")
add("desc_s32_plus9", "CLS-052", 32, s_table(5, S_PLUS9),
    "even -> n/2; odd -> 3n+1 if n mod 32 in S, else n+1 (S = all odd but 19,27,31)")
# expanding maps (mirror section)
add("par_5_1", "CLS-022/024", 2, par(5, 1), "even n -> n/2; odd n -> 5n+1", "expanding")
add("par_7_1", "CLS-032/034", 2, par(7, 1), "even n -> n/2; odd n -> 7n+1", "expanding")
add("sf3_137", "round3/accel core W", 8, s_table(3, (1, 3, 7)),
    "even n -> n/2; odd n -> 3n+1 if n mod 8 in {1,3,7}, else n+1", "expanding")

BY_ID = {s["id"]: s for s in NAMED}


# ------------------------------------------------------------- families ---

def family_S(m):
    """All S-family members: even -> n/2; odd -> 3n+1 if n mod 2^m in S else n+1."""
    odd = [r for r in range(2 ** m) if r % 2]
    out = []
    for mask in range(1 << len(odd)):
        S = tuple(r for i, r in enumerate(odd) if mask >> i & 1)
        out.append((S, TableMap("S%d_%s" % (m, "_".join(map(str, S))), 2 ** m, s_table(m, S))))
    return out


def family_split(alist=(3, 5, 7, 9), dlist=(1, 3, 5, 7, 9, 11, 13, 15)):
    """even -> n/2; 1 mod 4 -> a n + d; 3 mod 4 -> n + d (d odd)."""
    return [((a, d), TableMap("split%d_%d" % (a, d), 4, split(a, d))) for a in alist for d in dlist]


def family_m3(alist=(2, 4, 5, 7, 8), clist=range(0, 9)):
    """3|n -> n/3; 1 mod 3 -> a n + c1; 2 mod 3 -> a n + c2, c_i >= 0, with
    a n + c_i never divisible by 3 forced?  No: any c allowed (u = a prime to 3)."""
    out = []
    for a in alist:
        if a % 3 == 0:
            continue
        for c1 in clist:
            for c2 in clist:
                out.append(((a, c1, c2), TableMap("m3_%d_%d_%d" % (a, c1, c2), 3, m3(a, c1, a, c2))))
    return out
