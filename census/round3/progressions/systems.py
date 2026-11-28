"""Systems for the progressions lens, written as p-shift maps (see plib.py).

Every census map below with a division branch n -> n/p on multiples of p is replaced by its
*shortcut*: the branch n -> u n + v (with p | u n + v) is merged with the division that follows
it, giving (u n + v)/p.  For the raw map R and its shortcut S one has S(n) in {R(n), R(R(n))}
and R(n) -> S(n) is a single R-step when R(n) = u n + v, so the two maps have the same merging
classes and the same cycles up to the inserted intermediate values (theorem_A_sufficiency.md,
Lemma 0).  The column `raw` records the census rule.

Fields: id, cls (census ids), source, raw, sys (plib.PShift), global_ ('settled' or 'open'),
cycles (representatives: the complete list when settled, the known ones when open),
cycles_note.
"""

from plib import PShift

SYSTEMS = []


def add(id, cls, source, raw, p, kappa, table, global_, cycles, cycles_note=""):
    SYSTEMS.append(dict(id=id, cls=cls, source=source, raw=raw,
                        sys=PShift(id, p, kappa, table), global_=global_,
                        cycles=cycles, cycles_note=cycles_note))


def parity(a, d):
    return {0: (1, 0), 1: (a, d)}


def split(a, b, d):
    """even -> n/2; 1 mod 4 -> a n + d; 3 mod 4 -> b n + d; shortcut by one halving."""
    return {0: (1, 0), 2: (1, 0), 1: (a, d), 3: (b, d)}


def m3(a, c1, b, c2):
    """3|n -> n/3; 1 mod 3 -> (a n + c1)/3; 2 mod 3 -> (b n + c2)/3."""
    return {0: (1, 0), 1: (a, c1), 2: (b, c2)}


def sfam(d, S):
    t = {}
    for r in range(32):
        t[r] = (1, 0) if r % 2 == 0 else ((3, d) if r in S else (1, d))
    return t


S0 = (1, 3, 5, 7, 11, 13, 15, 17, 21, 23, 25, 29)
C = "census/systems.py"
R2D = "census/round2/descent/systems.py"
R2Q = "census/round2/qr/systems.py"

# ---------------------------------------------------------------- settled GLOBAL, several cycles
add("m3_a", "m3_a_s100 (round 1); same merging classes as m3_c_s100", C,
    "3|n -> n/3; n=1 -> (2n+1)/3; n=2 -> (2n+2)/3", 3, 1, m3(2, 1, 2, 2),
    "settled", [1, 2], "complete: T(n) < n for n > 2 (census/results/m3_a_s100.md)")
add("m3_c", "m3_c_s100 (round 1)", C,
    "3|n -> n/3; n=1 -> 2n+1; n=2 -> 2n+2 (shortcut = m3_a)", 3, 1, m3(2, 1, 2, 2),
    "settled", [1, 2], "raw cycles (1 3), (2 6); complete (census/results/m3_c_s100.md)")
add("desc_s32_d65", "round 2 descent (CYCLES settled)", R2D,
    "even -> n/2; odd n -> 3n+65 if n mod 32 in S0, else n+65", 2, 5, sfam(65, S0),
    "settled", [1, 5, 7, 13, 39, 65, 299, 1135],
    "complete: census/round2/descent/desc_s32_d65.md")
add("qrB7_c53", "round 2 qr (BASIN settled there)", R2Q,
    "even -> n/2; 1 mod 4 -> (n+35)/2; 3 mod 4 -> (n+21)/2", 2, 2,
    {0: (1, 0), 2: (1, 0), 1: (1, 35), 3: (1, 21)}, "settled", [1, 3, 5, 7],
    "complete: census/round2/qr/qrB7_c53.md")
add("par_1_5", "par_1_5_s27", C, "even -> n/2; odd -> n+5", 2, 1, parity(1, 5),
    "settled", [1, 5], "complete: census/results/par_1_5_s27.md")
for d, cyc in [(5, [1, 5]), (13, [1, 5, 13]), (73, [3, 5, 73]), (97, [13, 33, 97]),
               (7081, [1, 11, 41, 291, 485, 569, 713, 949, 2409, 7081])]:
    add(f"split_{d}", f"split_{d}_s27", C, f"even -> n/2; 1 mod 4 -> 3n+{d}; 3 mod 4 -> n+{d}",
        2, 2, split(3, 1, d), "settled", cyc, f"complete: census/results/split_{d}_s27.md")
for d, cyc in [(7, [1, 7]), (71, [1, 11, 71])]:
    add(f"splitB_{d}", f"splitB_{d}_s27", C, f"even -> n/2; 1 mod 4 -> n+{d}; 3 mod 4 -> 3n+{d}",
        2, 2, split(1, 3, d), "settled", cyc, f"complete: census/results/splitB_{d}_s27.md")

# ---------------------------------------------------------------- open GLOBAL
for a, d, cls, cyc in [
        (3, 1, "CLS-013", [1]),
        (3, -1, "CLS-018", [1, 5, 17]),
        (3, 5, "CLS-015", [1, 5, 19, 23, 187, 347]),
        (3, 7, "CLS-016", [5, 7]),
        (3, 13, "CLS-011", [1, 13, 131, 211, 227, 251, 259, 283, 287, 319]),
        (3, 17, "CLS-012", [1, 17, 23]),
        (5, 1, "CLS-022/023/024", [1, 13, 17]),
        (5, 3, "CLS-026/027", [1, 3, 39, 43, 51, 53, 61]),
        (5, 5, "CLS-028/029", [5, 65, 85]),
        (5, 7, "CLS-030", [1, 7, 9, 57, 91, 119]),
        (5, 11, "CLS-019/020", [1, 11, 141, 143, 187]),
        (7, 1, "CLS-032/033/034", [1]),
        (7, 7, "CLS-035", [7]),
        (9, 1, "CLS-036/037", [])]:
    add(f"par_{a}_{'m' if d < 0 else ''}{abs(d)}", cls, C, f"even -> n/2; odd -> {a}n{d:+d}",
        2, 1, parity(a, d), "open", cyc, "cycle minima found by searching starts <= 3000; completeness open")
add("split5_1", "CLS-048/064", C, "even -> n/2; 1 mod 4 -> 5n+1; 3 mod 4 -> n+1",
    2, 2, split(5, 1, 1), "open", [1, 13], "known cycles; completeness open")
add("split5_3", "CLS-049/065", C, "even -> n/2; 1 mod 4 -> 5n+3; 3 mod 4 -> n+3",
    2, 2, split(5, 1, 3), "open", [1, 3, 5, 61, 125], "known cycles; completeness open")
add("desc_split7_1", "CLS-053", R2D, "even -> n/2; 1 mod 4 -> 7n+1; 3 mod 4 -> n+1",
    2, 2, split(7, 1, 1), "open", [1], "known cycles; completeness open")
add("desc_s32_plus9", "CLS-052", R2D,
    "even -> n/2; odd n -> 3n+1 if n mod 32 in S0+{9}, else n+1", 2, 5,
    sfam(1, S0 + (9,)), "open", [1], "known cycles; completeness open")
add("m3_b", "CLS-004/061", C, "3|n -> n/3; n=1 -> (4n-1)/3; n=2 -> (4n+1)/3",
    3, 1, m3(4, -1, 4, 1), "open", [1], "known cycles; completeness open")
add("m3_d", "CLS-005/062", C, "3|n -> n/3; n=1 -> 4n+2; n=2 -> 4n+1",
    3, 1, m3(4, 2, 4, 1), "open", [1, 7], "known cycles; completeness open")
add("m3_e", "CLS-006/007", C, "3|n -> n/3; n=1 -> 7n+2; n=2 -> 7n+1",
    3, 1, m3(7, 2, 7, 1), "open", [1, 4], "known cycles; completeness open")
add("m3_g", "CLS-008/063", C, "3|n -> n/3; n=1 -> 5n+1; n=2 -> 5n+2",
    3, 1, m3(5, 1, 5, 2), "open", [4, 8], "known cycles; completeness open")
add("desc_m3_4n5", "CLS-051", R2D, "3|n -> n/3; n=1 -> 4n+5; n=2 -> 2n+2",
    3, 1, m3(4, 5, 2, 2), "open", [1, 2, 16], "known cycles; completeness open")

# ---------------------------------------------------------------- outside the hypotheses
add("perm_1932", "CLS-038..042 (permutation)", C, "3q->2q; 3q+1->4q+1; 3q+2->4q+3",
    3, 1, {0: (2, 0), 1: (4, -1), 2: (4, 1)}, "open", [1, 2, 4, 44],
    "no dilation branch: hypothesis (A1) fails; orbits do not merge; the only sufficient "
    "progressions are Z>=1 and 1 mod 2 (sufficient_sets.md section 4)")
add("par_3_3", "CLS-014", C, "even -> n/2; odd -> 3n+3", 2, 1, parity(3, 3), "open", [3],
    "IA fails (every expanding image divisible by 3)")
add("par_3_9", "CLS-017", C, "even -> n/2; odd -> 3n+9", 2, 1, parity(3, 9), "open", [9],
    "IA fails (every expanding image divisible by 3)")

BY_ID = {s["id"]: s for s in SYSTEMS}


def get(id):
    return BY_ID[id]
