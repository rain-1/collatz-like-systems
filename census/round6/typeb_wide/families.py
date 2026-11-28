"""Choice families scanned in this folder.  A family is (name, p, m, opts) with
opts[r] = list of allowed branches (u, v, w) on the class r mod p^m; its members are all
choices of one branch per class.  `members(fam)` iterates over (index, table)."""
import itertools

HALF = (1, 0, 2)
THIRD = (1, 0, 3)


def s_family(m, a, d=1):
    """even -> n/2; odd -> a n + d (n mod 2^m in S) or n + d."""
    return [[HALF] if r % 2 == 0 else [(1, d, 1), (a, d, 1)] for r in range(2 ** m)]


def shift_family(m, shifts=(1, 3, 5, 7), a=3):
    """even -> n/2; odd class -> a n + 1 or n + d for d in shifts (acc_h16/h32 live here)."""
    return [[HALF] if r % 2 == 0 else [(a, 1, 1)] + [(1, d, 1) for d in shifts]
            for r in range(2 ** m)]


def split_family(m, d, mults=(1, 3, 5)):
    """even -> n/2; odd class -> u n + d, u in mults (SPLIT(a,b,d) is m = 2)."""
    return [[HALF] if r % 2 == 0 else [(u, d, 1) for u in mults] for r in range(2 ** m)]


def base3_B(Q, a):
    """3|n -> n/3; S -> a n + 1; other units -> n + 1 (round-3 family B(Q, a, S))."""
    return [[THIRD] if r % 3 == 0 else [(1, 1, 1), (a, 1, 1)] for r in range(Q)]


C9_MAPS = [(1, 1, 1), (1, 2, 1), (2, 1, 1), (2, -1, 1), (4, 1, 1), (4, -1, 1), (5, 1, 1), (5, -1, 1)]


def base3_C9():
    """3|n -> n/3; each unit class mod 9 -> one of 8 maps (round-3 family C9)."""
    return [[THIRD] if r % 3 == 0 else list(C9_MAPS) for r in range(9)]


def base3_div(Q, mults=(2, 4, 5)):
    """3|n -> n/3; unit class r mod Q -> (u n + v)/3 with u in mults and v = the least
    |v| <= 2 making it exact (acc_h9 lives here): divisions also on the unit classes."""
    out = []
    for r in range(Q):
        if r % 3 == 0:
            out.append([THIRD])
            continue
        o = []
        for u in mults:
            for v in (1, 2, -1, -2, 4, 5, 7):
                if (u * r + v) % 3 == 0:
                    o.append((u, v, 3))
                    break
        out.append(o)
    return out


def n_members(opts):
    k = 1
    for o in opts:
        k *= len(o)
    return k


def table_at(opts, idx):
    tab = []
    for o in opts:
        k = len(o)
        tab.append(o[idx % k])
        idx //= k
    return tab


FAMILIES = {}
for m in (2, 3, 4, 5):
    for a in (3, 5, 7):
        FAMILIES[f"S{a}_m{m}"] = (2, m, s_family(m, a))
for m in (2, 3, 4):
    FAMILIES[f"SH3_m{m}"] = (2, m, shift_family(m))
for m in (2, 3, 4):
    for d in (1, 3, 5):
        FAMILIES[f"SPL_d{d}_m{m}"] = (2, m, split_family(m, d))
for Q, m in ((9, 2), (27, 3)):
    for a in (2, 4, 5, 7, 8, 10, 11, 13):
        FAMILIES[f"B{Q}_a{a}"] = (3, m, base3_B(Q, a))
FAMILIES["C9"] = (3, 2, base3_C9())
FAMILIES["D9"] = (3, 2, base3_div(9))
FAMILIES["D27"] = (3, 3, base3_div(27))
for m in (2, 3, 4):
    FAMILIES[f"SH5_m{m}"] = (2, m, shift_family(m, a=5))
FAMILIES["C27"] = (3, 3, [[THIRD] if r % 3 == 0 else list(C9_MAPS) for r in range(27)])  # SAT only
