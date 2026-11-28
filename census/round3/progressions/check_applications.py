"""Check for applications_basins.md: the invariant table and the basin statements.
Exact; exits 0 iff all checks pass."""

import os
import sys
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plib
import systems
from certify import certify

FAIL = []


def ok(c, m):
    if not c:
        FAIL.append(m)
        print("FAIL:", m, flush=True)


# expected (d*, grouping of the listed cycles into classes) from the table in the .md file
EXPECTED = {
    "m3_a": (1, [[1, 2]]),
    "desc_s32_d65": (65, [[65], [1, 7], [5, 1135], [13, 39, 299]]),
    "qrB7_c53": (7, [[7], [1], [3, 5]]),
    "par_1_5": (5, [[5], [1]]),
    "split_5": (5, [[5], [1]]),
    "split_13": (13, [[13], [1, 5]]),
    "split_73": (73, [[3], [5], [73]]),
    "split_97": (97, [[13], [33], [97]]),
    "splitB_7": (7, [[1], [7]]),
    "splitB_71": (71, [[1], [11], [71]]),
    "par_3_1": (1, [[1]]),
    "par_3_m1": (1, [[1, 5, 17]]),
    "par_3_5": (5, [[5], [1, 19, 23, 187, 347]]),
    "par_3_7": (7, [[7], [5]]),
    "par_3_13": (13, [[13], [1, 131, 211, 227, 251, 259, 283, 287, 319]]),
    "par_3_17": (17, [[17], [1, 23]]),
    "par_5_1": (1, [[1, 13, 17]]),
    "par_5_3": (3, [[3, 39, 51], [1, 43, 53, 61]]),
    "par_5_7": (7, [[7, 91, 119], [1, 9, 57]]),
    "par_5_11": (11, [[11, 143, 187], [1, 141]]),
    "par_7_1": (1, [[1]]),
    "split5_1": (1, [[1, 13]]),
    "split5_3": (3, [[3], [1, 5, 61, 125]]),
    "m3_b": (1, [[1]]),
    "m3_d": (1, [[1, 7]]),
    "m3_e": (1, [[1, 4]]),
    "m3_g": (1, [[4, 8]]),
    "desc_m3_4n5": (1, [[1, 2, 16]]),
}
for sid, (dstar, groups) in EXPECTED.items():
    c = certify(systems.get(sid))
    ok(c["theorem_A"], f"Theorem A {sid}")
    ok(c["invariant_modulus"] == dstar, f"d* {sid}: {c['invariant_modulus']}")
    cls = {cy["rep"]: cy["cls"] for cy in c["cycles"]}
    got = {}
    for r, k in cls.items():
        got.setdefault(k, []).append(r)
    ok(sorted(sorted(v) for v in got.values()) == sorted(sorted(v) for v in groups),
       f"cycle grouping {sid}: {got}")
    if sid not in ("qrB7_c53", "par_1_5"):
        ok(c["theorem_B"], f"Theorem B {sid}")
    for cy in c["cycles"]:
        cyc = plib.cycle_of(systems.get(sid)["sys"], cy["rep"])
        ok(cyc is not None and cy["rep"] in cyc, f"cycle point {sid} {cy['rep']}")
print("table of invariants and cycle classes verified", flush=True)

# split_7081: 9 classes, 569 and 713 share, the others are alone
c = certify(systems.get("split_7081"))
ok(c["invariant_modulus"] == 7081 and len(c["classes"]) == 9, "split_7081 classes")
ok(list(c["shared_classes"].values()) == [[569, 713]], "split_7081 shared")

# desc_s32_d65: the invariant is gcd(n, 65)
S = systems.get("desc_s32_d65")["sys"]
c = certify(systems.get("desc_s32_d65"))
import construct
info = construct.prepare(S)
seen = {}
for n in range(1, 65 * 32 * 4):
    seen.setdefault(gcd(n, 65), set()).add(construct.g(S, info, n))
ok(all(len(v) == 1 for v in seen.values()) and len({min(v) for v in seen.values()}) == 4,
   "desc_s32_d65 invariant = gcd(n,65)")

# settled systems: completeness of cycles (descent for m3_a; census proofs elsewhere) and
# every start up to a bound reaches a listed cycle (consistency check)
S = systems.get("m3_a")["sys"]
for r in range(3):
    for k in range(0, 2000):
        n = 3 * k + r
        if n > 2:
            ok(S.T(n) < n, "m3_a descent")
for sid in ["m3_a", "desc_s32_d65", "split_13", "split_7081", "splitB_71"]:
    e = systems.get(sid)
    S = e["sys"]
    pts = set()
    for c0 in e["cycles"]:
        pts |= set(plib.cycle_of(S, c0))
    for n in range(1, 60001):
        x = n
        for _ in range(10000):
            if x in pts:
                break
            x = S.T(x)
        ok(x in pts, f"{sid}: {n} reaches a listed cycle")
print("settled systems: all starts <= 60000 reach listed cycles", flush=True)

if FAIL:
    print(len(FAIL), "FAILURES")
    sys.exit(1)
print("ALL CHECKS PASSED")
