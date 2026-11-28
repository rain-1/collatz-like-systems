#!/usr/bin/env python3
"""Checks every system in systems.py (claims in systems.md / deep.md).  Exact; exits 0.

For each system:
 1. hypotheses (H1)(H2)(P); the step function equals the table on n < 5000.
 2. decide.py gives CERT; the integer potential c satisfies c(s)u < c(r)w on every edge
    (re-verified here); hence GLOBAL holds (Theorem 2).
 3. the exceptional set F is recomputed from the symbolic bounds N_r, and the cycles
    reached from F equal the stated COMPLETE list.
 4. k* (least step count over all plain certificates, Theorem 3) equals the stated value;
    lower-bound witness: a non-descending walk of length k*-1 is realised by a progression
    (Lemma 1) and a concrete large integer n in it has T^i(n) >= n for all i < k* and
    T^{k*}(n) < n, checked by direct iteration.
 5. consistency: every n <= 20000 reaches a listed cycle by direct simulation.
Runtime ~1 minute.
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from decide import (decide, check_hypotheses, residue_graph, verify_potential,
                    exceptional_set, cycles_from, deepest_walk, path_progression, step_fn)
import systems

for s in systems.SYSTEMS:
    Q, tab = s["Q"], s["table"]
    check_hypotheses(Q, tab)
    T = step_fn(Q, tab)
    for n in range(1, 5000):
        assert T(n) == s["step"](n)
    res = decide(Q, tab)
    assert res["verdict"] == "CERT", s["id"]
    succ = residue_graph(Q, tab)
    assert verify_potential(Q, tab, succ, res["weights"]) < 1
    F, bounds = exceptional_set(Q, tab, res["weights"])
    assert F == res["F"]
    cyc = cycles_from(Q, tab, F)
    assert sorted(cyc) == sorted(s["cycles"]), (s["id"], cyc)
    assert res["kstar"] == s["kstar"], (s["id"], res["kstar"])
    walk = deepest_walk(Q, tab, succ)
    assert len(walk) == s["kstar"]
    a, M, A, B, D = path_progression(Q, tab, walk)
    n = a + M * 10 ** 12
    x = n
    for i in range(1, s["kstar"]):
        x = T(x)
        assert x >= n, (s["id"], i)
    assert T(x) < n
    pts = {y for c in cyc for y in c}
    for n in range(1, 20001):
        x, k = n, 0
        while x not in pts:
            x = T(x)
            k += 1
            assert k < 10 ** 6
    print(f"{s['id']}: CERT, k*={s['kstar']}, |F|={len(F)}, cycles {len(cyc)} -- ok")
print("ALL OK")
