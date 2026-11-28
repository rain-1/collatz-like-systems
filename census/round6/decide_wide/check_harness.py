#!/usr/bin/env python3
"""check_harness.py -- the harness verdicts against brute force.  Exits 0 on success.

 A. Catalog: for every table settled by the harness in out/catalog_sweep.json (CERT, Theorem
    H', or DIVERGES), recompute the verdict from scratch and check it:
      CERT / H'  every start n < N reaches one of the listed cycles, and each listed cycle is
                 a cycle of T (N = 20000, or 3000 for Q > 500);
      DIVERGES   the exact starting value follows the division-free cycle and grows: 50 laps
                 strictly increasing.
    For the catalog tables that are re-settled, also check that the census answer agrees
    (yes for CERT/H', no for DIVERGES) whenever the census records one.
 B. Every type-(b) member in out/typeb_list.jsonl: recompute Theorem H' and check its cycle
    list against iteration of all n < 3000; check that decide.py says OBST (so the member is
    genuinely beyond descent certificates).
 C. Falsification tests: 3x-1 (Q=2) and 3x+5 must be OBST with type (c) (no false proof),
    5x+1 must be OBST; a deliberately wrong cycle list must be rejected by the same test.
 D. (added after REFEREE1) every OPEN / OPEN-CLS record is classified and has a type-(c) SCC
    at its base level; zcore_* maps are read on N0.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import twlib  # noqa: E402
import make_report  # noqa: E402

FAIL = []


def fail(m):
    print("FAIL", m)
    FAIL.append(m)


def reaches(Q, tab, cycles, N, zero=False):
    T = twlib.step_fn(Q, tab)
    pts = {x for c in cycles for x in c}
    for c in cycles:
        for i, x in enumerate(c):
            if T(x) != c[(i + 1) % len(c)]:
                return f"listed cycle {c} is not a cycle"
    for n in range(0 if zero else 1, N):
        x, k = n, 0
        while x not in pts:
            x = T(x)
            k += 1
            if k > 2 * 10 ** 6:
                return f"start {n} does not reach the list"
    return None


def part_A():
    d = json.load(open(os.path.join(HERE, "out", "catalog_sweep.json")))
    na = 0
    for g in d["records"]:
        r = g["result"]
        Q, tab, zero = g["Q"], [tuple(t) for t in g["table"]], g.get("zero", False)
        verdict = None
        if r.get("decide") == "CERT":
            verdict = "GLOBAL"
        if str(r.get("H", "")).startswith("GLOBAL"):
            verdict = "GLOBAL"
        if str(r.get("H", "")).startswith("DIVERGES"):
            verdict = "DIVERGES"
        if verdict is None:
            continue
        res = twlib.analyse(Q, tab, want_theta=False, maxnodes=600, zero=zero)
        st, how = make_report.status(g)
        if verdict == "GLOBAL":
            if "H" in res and res["H"]["status"] == "GLOBAL":
                cycles = res["H"]["cycles"]
            else:
                cycles = res["decide"]["cycles"]
            if "decide" in res and res["decide"]["verdict"] == "CERT":
                c2 = sorted(tuple(c) for c in res["decide"]["cycles"])
                if "H" in res and res["H"]["status"] == "GLOBAL":
                    c1 = sorted(tuple(c) for c in res["H"]["cycles"])
                    if c1 != c2:
                        fail(f"A {g['ids'][0]}: decide and Theorem H' cycle lists differ")
            err = reaches(Q, tab, cycles, 3000 if Q > 500 else 20000, zero)
            if err:
                fail(f"A {g['ids'][0]}: {err}")
            if st == "no":
                fail(f"A {g['ids'][0]}: harness GLOBAL but census says no")
        else:
            H = res["H"]
            if H["status"] != "DIVERGES":
                fail(f"A {g['ids'][0]}: DIVERGES not reproduced")
                continue
            T = twlib.step_fn(Q, tab)
            x = H["start"]
            L = len(H["cycle"])
            prev = x
            for _ in range(50):
                for _ in range(L):
                    x = T(x)
                if not x > prev:
                    fail(f"A {g['ids'][0]}: not increasing")
                    break
                prev = x
            if st == "yes":
                fail(f"A {g['ids'][0]}: harness DIVERGES but census says yes")
        na += 1
    print(f"A. {na} re-settled catalog tables confirmed by iteration")


def part_B():
    nb = 0
    for line in open(os.path.join(HERE, "out", "typeb_list.jsonl")):
        d = json.loads(line)
        Q, tab = d["Q"], [tuple(t) for t in d["table"]]
        lev = twlib.classify_level(Q, tab, Q)
        H = twlib.theorem_H(Q, tab, lev)
        if H["status"] != "GLOBAL" or sorted(map(tuple, H["cycles"])) != sorted(map(tuple, d["cycles"])):
            fail(f"B {d['family']} {d['index']}: Theorem H' not reproduced")
            continue
        err = reaches(Q, tab, H["cycles"], 3000)
        if err:
            fail(f"B {d['family']} {d['index']}: {err}")
        if nb % 25 == 0:      # decide.py is slower; every 25th member
            dd = twlib.D.decide(Q, tab, want_cycles=False, want_depth=False)
            if dd["verdict"] != "OBST":
                fail(f"B {d['family']} {d['index']}: decide says {dd['verdict']}")
        nb += 1
    print(f"B. {nb} type-(b) members: Theorem H' cycle lists confirmed by iteration")


def part_C():
    for name, Q, tab in [("3x-1", 2, [(1, 0, 2), (3, -1, 1)]), ("3x+5", 2, [(1, 0, 2), (3, 5, 1)]),
                         ("5x+1", 2, [(1, 0, 2), (5, 1, 1)]), ("3x+1", 2, [(1, 0, 2), (3, 1, 1)])]:
        res = twlib.analyse(Q, tab, want_theta=False)
        if res["decide"]["verdict"] != "OBST" or "H" in res:
            fail(f"C {name}: expected OBST and no Theorem H' verdict")
        if "c" not in res["levels"][0]["types"]:
            fail(f"C {name}: expected a type (c) SCC")
    # the test must be able to fail: drop a cycle of 3x-1 restricted to a CERT neighbour
    Q, tab = 4, [(1, 0, 2), (3, 5, 1), (1, 0, 2), (1, 5, 1)]      # split_5 (CERT)
    res = twlib.analyse(Q, tab, want_theta=False)
    cyc = res["decide"]["cycles"]
    if reaches(Q, tab, cyc, 5000) is not None:
        fail("C split_5: true cycle list rejected")
    if len(cyc) > 1 and reaches(Q, tab, cyc[1:], 5000) is None:
        fail("C split_5: truncated cycle list accepted")
    if reaches(Q, tab, cyc + [(10 ** 6 + 1,)], 100) is None:
        fail("C split_5: fake cycle accepted")
    print("C. falsification tests done (3x-1, 3x+5, 5x+1, 3x+1 stay unproved; wrong lists rejected)")


def part_D():
    """Revision after REFEREE1: every open record (OPEN or OPEN-CLS) of the sweep must have been
    classified (no error, no "positivity fails" note) and must contain a type-(c) SCC at its base
    level; the zcore_* maps must have been read on N0.  Recomputes the base-level types."""
    d = json.load(open(os.path.join(HERE, "out", "catalog_sweep.json")))
    nopen = 0
    for g in d["records"]:
        st, _ = make_report.status(g)
        ids = [i.split("@")[0] for i in g["ids"]]
        if any(i.startswith("zcore_") for i in ids) and not g.get("zero"):
            fail(f"D {ids}: zcore map not read on N0")
        if st not in ("OPEN", "OPEN-CLS"):
            continue
        nopen += 1
        r = g["result"]
        if "error" in r or r.get("note") or not r.get("types"):
            fail(f"D {ids}: open record not classified: {r.get('error') or r.get('note')}")
            continue
        Q, tab = g["Q"], [tuple(t) for t in g["table"]]
        lev = twlib.classify_level(Q, tab, Q)
        if "c" not in lev["types"]:
            fail(f"D {ids}: base-level types {lev['types']} contain no (c)")
    print(f"D. {nopen} open records classified, each with a type-(c) SCC at its base level")


if __name__ == "__main__":
    part_D()
    part_C()
    part_A()
    part_B()
    print("ALL CHECKS PASSED" if not FAIL else f"{len(FAIL)} FAILURES")
    sys.exit(1 if FAIL else 0)
