"""Check for fx10_64_s7.md and fx26_32_s7.md.  Exit 0 on success.

For each system (T = 5x+1 modified on one class):
 (1) T as an exact table: integrality on every class, agreement with the
     defining formula on 1..10^5 and random large n;
 (2) the trap S (union of classes mod 2^m) is forward closed (exact residue
     graph), the ascent witness (Lemma A-up) verifies exactly, offsets >= 0,
     the non-fall subgraph is acyclic (Lemma F) and the 2-adic aperiodicity
     witness verifies (Lemma I);
 (3) Lemma P hypotheses: all numerators odd, denominators powers of 2, G1
     acyclic; S is the unique sink SCC of the residue graph mod 2^m, so every
     forward-closed union of residue classes at any modulus 2^K contains S;
 (4) the orbit of 7 enters S at the stated step;
 (5) EVIDENCE only: every n <= 20000 either enters S within 5000 steps or
     reaches one of the listed cycles; random members of S grow.
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from systems import get  # noqa: E402
from divlib import (images, is_closed, ascent_certificate, verify_ascent, nonfall_subgraph_acyclic,  # noqa: E402
                    aperiodic_certificate, verify_aperiodic, vp)
from obstruction5 import sink_sccs, g1_acyclic  # noqa: E402

CASES = [
    dict(id="fx10_64_s7", m=6, c=10, f=lambda n: 5 * n + 5, S=[10, 20, 21, 42, 53, 55], enter=12,
         cycles=[1, 13, 17]),
    dict(id="fx26_32_s7", m=5, c=26, f=lambda n: 7 * n + 1, S=[5, 10, 20, 21, 23, 26], enter=5,
         cycles=[1, 17]),
]


def cycle_min(T, n, cap=5000, S=None, M=None):
    seen = {}
    x = n
    for i in range(cap):
        if S is not None and x % M in S:
            return "S"
        if x in seen:
            y, mn = x, x
            while True:
                y = T(y)
                mn = min(mn, y)
                if y == x:
                    return mn
        seen[x] = i
        x = T(x)
    return None


def main():
    rng = random.Random(5)
    for C in CASES:
        T = get(C["id"])["rcwa"]
        m, M = C["m"], 2 ** C["m"]
        T.check()
        # (1)
        def ref(n):
            if n % M == C["c"]:
                return C["f"](n)
            return n // 2 if n % 2 == 0 else 5 * n + 1
        for n in list(range(1, 100001)) + [rng.randrange(1, 10 ** 30) for _ in range(5000)]:
            assert T(n) == ref(n)
        # (2)
        S = C["S"]
        assert is_closed(T, M, S)
        cert = ascent_certificate(T, M, S)
        assert cert and verify_ascent(T, cert)
        assert nonfall_subgraph_acyclic(T, M, S)
        ap = aperiodic_certificate(T, M, S, 2)
        assert ap and verify_aperiodic(T, ap)
        # (3)
        for r in range(M):
            a, b, d = T.rules[r]
            assert a % 2 == 1 and d & (d - 1) == 0
        sinks, adj = sink_sccs(T, M)
        assert g1_acyclic(T, M, adj)
        assert [sorted(s) for s in sinks] == [sorted(S)], sinks
        # (4)
        x = 7
        for i in range(C["enter"]):
            assert x % M not in S
            x = T(x)
        assert x % M in S
        # (5) evidence
        Sset = set(S)
        outcome = {}
        for n in range(1, 20001):
            o = cycle_min(T, n, S=Sset, M=M)
            assert o is not None, n
            outcome[o] = outcome.get(o, 0) + 1
        assert set(outcome) <= {"S"} | set(C["cycles"]), outcome
        grow = 0
        for _ in range(200):
            n = rng.randrange(1, 10 ** 12)
            n = n - n % M + rng.choice(S)
            if n <= 0:
                continue
            y = n
            for _ in range(400):
                y = T(y)
                assert y % M in Sset
            grow += y > n
        assert grow == 200
        print(C["id"], "trap", S, "mod", M, "verified; orbit of 7 enters at step", C["enter"],
              "; n<=20000 outcomes:", outcome)
    print("OK")


if __name__ == "__main__":
    main()
