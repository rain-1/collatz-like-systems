#!/usr/bin/env python3
"""Checks for neighbours.md.  Exact; exits 0.  Runtime ~1.5 minutes.

 1. Every open table in open_tables.py equals the census step function (census/systems.py,
    or round2/descent/systems.py, or for the 12 remaining par_* entries the catalog rule text)
    on n < 3000, satisfies (H1)(H2)(P), and is OBST (with the stated obstruction multiplier).
 2. The numbers of CERT one-class / two-class modifications at Q' = Q p (menu damp/reset)
    equal the stated counts.
 3. The exact distances dist_{Q'} for Q' <= 64 marked exact in neighbours.md are re-derived:
    lower bound = exact minimum hitting set of verified bad cycles (Proposition 6), upper
    bound = a verified CERT reset table of that size.
"""
import sys, os, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from decide import decide, check_hypotheses, step_fn, cycle_multiplier
from families import lift
from open_tables import OPEN
from neighbours import menu, least_prime
from distance import implicit_hitting_set, reset_branch
import importlib.util
_sp = importlib.util.spec_from_file_location("census_systems", os.path.join(HERE, "..", "..", "systems.py"))
census = importlib.util.module_from_spec(_sp)
_sp.loader.exec_module(census)

CENSUS = {
    "m3_b (CLS-004/061)": "m3_b_s8", "m3_d (CLS-005/062)": "m3_d_s7", "m3_e (CLS-007)": "m3_e_s7",
    "m3_g (CLS-008/063)": "m3_g_s7", "par_3_13 (CLS-011)": "par_3_13_s27", "par_3_1 (CLS-013)": "par_3_1_s27",
    "par_3_m1 (CLS-018)": "par_3_m1_s27", "par_5_1 (CLS-022/024)": "par_5_1_s5",
    "par_7_1 (CLS-032/034)": "par_7_1_s1", "par_9_1 (CLS-037)": "par_9_1_s5",
    "perm_1932 (CLS-038/040)": "perm_1932_s8", "perm_1932inv (CLS-042)": "perm_1932inv_s8",
    "perm_b (CLS-044)": "perm_b_s7", "perm_c (CLS-045)": "perm_c_s8", "perm_d (CLS-046)": "perm_d_s3",
    "perm_swap (CLS-047)": "perm_swap_s8", "split5_1 (CLS-048/064)": "split5_1_s27",
    "split5_3 (CLS-049/065)": "split5_3_s27", "div23_5n1 (CLS-002/059)": "div23_5n1_s7",
    "div23_7n1 (CLS-003/060)": "div23_7n1_s5", "div235_7n1 (CLS-001/058)": "div235_7n1_s11",
}
for key, cid in CENSUS.items():
    Q, tab = OPEN[key]
    T, S = step_fn(Q, tab), census.get(cid)["step"]
    for n in range(1, 3000):
        assert T(n) == S(n), (key, n)
# the round-2 maps are compared with round2/descent/systems.py
sys.path.insert(0, os.path.join(HERE, "..", "..", "round2", "descent"))
spec = importlib.util.spec_from_file_location("r2sys", os.path.join(HERE, "..", "..", "round2", "descent", "systems.py"))
r2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r2)
r2by = {s["id"]: s for s in r2.SYSTEMS}
for key, cid in (("desc_m3_4n5 (CLS-051)", "desc_m3_4n5"), ("desc_s32_plus9 (CLS-052)", "desc_s32_plus9"),
                 ("desc_split7_1 (CLS-053)", "desc_split7_1")):
    Q, tab = OPEN[key]
    T = step_fn(Q, tab)
    for n in range(1, 3000):
        assert T(n) == r2by[cid]["step"](n), key
# the remaining parametric par_* entries have no census step function: compare them with the
# "Rule:" text of their entry in census/open_collatz_systems.txt (added after refereeing)
import re
CATALOG = open(os.path.join(HERE, "..", "..", "open_collatz_systems.txt")).read().splitlines()
rest = [k for k in OPEN if k not in CENSUS and k.startswith("par_")]
for key in rest:
    cls = key.split("(")[1].split("/")[0].rstrip(")")
    i = next(j for j, l in enumerate(CATALOG) if l.startswith(cls + " "))
    rule = CATALOG[i + 1].strip()
    m = re.fullmatch(r"Rule: even n -> n/2; odd n -> (\d+)n([+-]\d+)\.", rule)
    assert m, (key, rule)
    a, d = int(m.group(1)), int(m.group(2))
    Q, tab = OPEN[key]
    T = step_fn(Q, tab)
    for n in range(1, 3000):
        assert T(n) == (n // 2 if n % 2 == 0 else a * n + d), (key, n)
compared = len(CENSUS) + 3 + len(rest)
assert compared == len(OPEN) == 36, (compared, len(OPEN))
print("1a ok: tables match the census (%d census, 3 round-2, %d rule text)" % (len(CENSUS), len(rest)))

COUNTS = {}
for line in open(os.path.join(HERE, "neighbours.out")):
    if line.startswith("== "):
        cur = line[3:].split(":")[0]
    if "one-class modifications CERT" in line:
        a = line.split("CERT ")[1].split(";")[0]
        b = line.split("CERT ")[2].strip()
        COUNTS[cur] = (a, b)

for key, (Q, tab) in OPEN.items():
    check_hypotheses(Q, tab)
    res = decide(Q, tab, want_cycles=False, want_depth=False)
    assert res["verdict"] == "OBST" and res["obst"]["U"] > res["obst"]["W"]
    p = least_prime(Q)
    Q1 = Q * p
    base = lift(Q, tab, p)
    menus = {r: menu(Q1, r, base[r]) for r in range(Q1)}
    one = n1 = two = n2 = 0
    for r in range(Q1):
        for nm, br in menus[r]:
            t = list(base); t[r] = br; n1 += 1
            one += decide(Q1, t, want_cycles=False, want_depth=False)["verdict"] == "CERT"
    for r1, r2_ in itertools.combinations(range(Q1), 2):
        for (_, b1), (_, b2) in itertools.product(menus[r1], menus[r2_]):
            t = list(base); t[r1] = b1; t[r2_] = b2; n2 += 1
            two += decide(Q1, t, want_cycles=False, want_depth=False)["verdict"] == "CERT"
    assert COUNTS[key] == (f"{one}/{n1}", f"{two}/{n2}"), (key, one, n1, two, n2)
print("2 ok: neighbour counts")

EXACT = {"par_3_1 (CLS-013)": {4: 1, 8: 1, 16: 2, 32: 2},
         "par_5_1 (CLS-022/024)": {8: 2, 16: 3, 32: 4},
         "split5_1 (CLS-048/064)": {8: 1, 16: 1, 32: 2, 64: 3},
         "desc_m3_4n5 (CLS-051)": {9: 1, 27: 1},
         "m3_d (CLS-005/062)": {9: 2, 27: 3},
         "m3_b (CLS-004/061)": {9: 3, 27: 6},
         "perm_1932 (CLS-038/040)": {9: 4},
         "perm_1932inv (CLS-042)": {8: 3, 16: 5, 32: 7, 64: 11},
         "perm_d (CLS-046)": {16: 5, 32: 9},
         "div23_5n1 (CLS-002/059)": {12: 2, 24: 2, 48: 4}}
for key, d in EXACT.items():
    Q, tab = OPEN[key]
    for Ql, val in d.items():
        lo, up, R, nc, ex = implicit_hitting_set(Ql, lift(Q, tab, Ql // Q), time_limit=60)
        assert ex and lo == val, (key, Ql, lo, up)
        t = lift(Q, tab, Ql // Q)
        for r in R:
            t[r] = reset_branch(Ql, r)
        assert decide(Ql, t, want_cycles=False, want_depth=False)["verdict"] == "CERT"
print("3 ok: exact distances")
print("ALL OK")
