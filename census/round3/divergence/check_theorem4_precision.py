"""Check for theorem4_precision.md.  Exit 0 on success.

 (A) Lemma P on random instances: random odd-numerator modifications of 5x+1
     with acyclic G1, random K, random start class: the forward closure mod 2^K
     contains every lift of a forward-closed set mod 2^m (illustration of the
     proved lemma; any failure would refute it).
 (B) The classification table of family F_m for m in {5} (default) or the
     values given with --m (6 and 7 take minutes).  Every 'obstructed' entry is
     re-derived (Corollary P: G1 acyclic + every sink SCC mod 2^m holds a
     periodic point, each periodic point verified as a genuine cycle), every
     'open-cert' entry carries an exactly verified ascent witness.
"""
import os
import random
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from obstruction5 import classify, B5, sink_sccs, g1_acyclic, sccs  # noqa: E402
from divlib import (modify, images, forward_closure, ascent_certificate, verify_ascent,  # noqa: E402
                    nonfall_subgraph_acyclic, aperiodic_certificate, verify_aperiodic)

EXPECT = {
    5: dict(members=1504, g1=76, obstructed=1373, open=55, opencert=7, falls_aper=5,
            seed7={(5, (3, 6, 1)): (True, True), (5, (7, 7, 1)): (True, True), (5, (7, 7, 2)): (False, True),
                   (26, (3, 6, 1)): (True, True), (26, (3, 7, 1)): (True, True), (26, (3, 6, 2)): (False, True),
                   (26, (7, 1, 1)): (True, True)}),
    6: dict(members=3008, g1=108, obstructed=2891, open=9, opencert=1, falls_aper=1,
            seed7={(10, (5, 5, 1)): (True, True)}),
    7: dict(members=6016, g1=172, obstructed=5844, open=0, opencert=0, falls_aper=0, seed7={}),
    8: dict(members=12032, g1=300, obstructed=11732, open=0, opencert=0, falls_aper=0, seed7={}),
}


def family(m):
    M = 2 ** m
    for c in range(M):
        for a in (1, 3, 5, 7):
            for d in (1, 2):
                for b in range(8):
                    c0 = c if c else M
                    if (a * c0 + b) % d or (a * M) % d or (a * c0 + b) // d < 1:
                        continue
                    if (a, b, d) == B5.rules[c % 2]:
                        continue
                    yield c, (a, b, d)


def part_A():
    rng = random.Random(4)
    tested = 0
    while tested < 300:
        m = rng.choice([3, 4])
        M = 2 ** m
        c = rng.randrange(M)
        a, d = rng.choice([1, 3, 5, 7]), rng.choice([1, 2, 4])
        b = rng.randrange(16)
        c0 = c if c else M
        if (a * c0 + b) % d or (a * M) % d or (a * c0 + b) // d < 1:
            continue
        T = modify(B5, M, {c: (a, b, d)})
        _, adj = sink_sccs(T, M)
        if not g1_acyclic(T, M, adj):
            continue
        K = 2 ** rng.randint(m, m + 4)
        r = rng.randrange(K)
        U = forward_closure(T, K, [r])
        full = [y for y in range(M) if all((y + M * j) in U for j in range(K // M))]
        assert full, (m, c, (a, b, d), K, r)
        Y = forward_closure(T, M, [full[0]])
        for y in Y:
            assert all((y + M * j) in U for j in range(K // M))
        tested += 1
    print("(A) precision lemma consistent on", tested, "random instances")


def part_B(m):
    M = 2 ** m
    cnt = Counter()
    seed7 = {}
    for c, rule in family(m):
        cnt["members"] += 1
        kind, T, extra = classify(m, c, rule, per_upto=200)
        if kind == "G1-cycle":
            cnt["g1"] += 1
            continue
        if kind == "obstructed":
            cnt["obstructed"] += 1
            # re-verify the periodic points that witness the obstruction
            sinks, _ = sink_sccs(T, M)
            pts = extra
            for cp in sinks:
                hit = [p for p in pts if p % M in set(cp)]
                assert hit
                p = hit[0]
                x = T(p)
                for _ in range(10 ** 5):
                    if x == p:
                        break
                    x = T(x)
                assert x == p
            continue
        cnt["open"] += 1
        got = False
        for cp in extra:
            for K in (M, 2 * M, 4 * M):
                U = [r for r in range(K) if r % M in set(cp)]
                cert = ascent_certificate(T, K, U)
                if cert:
                    break
            if not cert:
                continue
            verify_ascent(T, cert)
            got = True
            fa = nonfall_subgraph_acyclic(T, K, U)
            ap = aperiodic_certificate(T, K, U)
            if ap:
                verify_aperiodic(T, ap)
            x = 7
            for _ in range(3000):
                if x % M in set(cp):
                    seed7[(c, rule)] = (fa, ap is not None)
                    break
                x = T(x)
            if fa and ap:
                cnt["falls_aper"] += 1
        if got:
            cnt["opencert"] += 1
    exp = EXPECT[m]
    for k in ("members", "g1", "obstructed", "open", "opencert", "falls_aper"):
        assert cnt[k] == exp[k], (m, k, cnt[k], exp[k])
    assert seed7 == exp["seed7"], (m, seed7)
    print("(B) m=%d:" % m, dict(cnt), "seed-7 traps:", seed7)


def main():
    ms = [5]
    if "--m" in sys.argv:
        ms = [int(x) for x in sys.argv[sys.argv.index("--m") + 1].split(",")]
    part_A()
    for m in ms:
        part_B(m)
    print("OK")


if __name__ == "__main__":
    main()
