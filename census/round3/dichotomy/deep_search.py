#!/usr/bin/env python3
"""Application (3c): search for the deepest certificates (hardest settled systems).

Hill climbing on the minimal stopping depth k* (Theorem 3: the least k over ALL plain
descent certificates), over three families:
  S(m):     even -> n/2; odd n -> 3n+1 if n mod 2^m in S else n+1          (m = 6)
  B(81,a):  3|n -> n/3; n mod 81 in S -> a n + 1; other units -> n + 1      (a = 2, 4, 5, 8)
  C27:      3|n -> n/3; n = r mod 27 -> one of n+1, n+2, 2n+1, 2n-1, 4n+1, 4n-1, 5n+1, 5n-1
Every reported system is re-decided exactly (decide.py) with its complete cycle list.
Search only (random); the record systems are re-verified in check_deep.py.
Output appended to deep_search.out.  Runtime: ~budget seconds per family (default 150).
"""
import sys, os, random, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decide import decide, residue_graph, stopping_depth
from families import s_family, base3_S, base3_table

HERE = os.path.dirname(os.path.abspath(__file__))
C8 = [(1, 1), (1, 2), (2, 1), (2, -1), (4, 1), (4, -1), (5, 1), (5, -1)]


def kstar(Q, tab):
    res = decide(Q, tab, want_cycles=False, want_depth=False)
    if res["verdict"] != "CERT":
        return -1
    try:
        return stopping_depth(Q, tab, residue_graph(Q, tab), maxstates=300000)[0]
    except AssertionError:
        return -2


def climb(make, Q, nbits, nvals, budget, seed):
    rnd = random.Random(seed)
    best = (-1, None)
    t_end = time.time() + budget
    while time.time() < t_end:
        x = [rnd.randrange(nvals) for _ in range(nbits)]
        k = kstar(Q, make(x))
        if k < 0:
            # bias toward certifiable starts
            x = [0] * nbits
            k = kstar(Q, make(x))
        stale = 0
        while stale < 300 and time.time() < t_end:
            y = list(x)
            for _ in range(rnd.choice([1, 1, 2])):
                y[rnd.randrange(nbits)] = rnd.randrange(nvals)
            ky = kstar(Q, make(y))
            if ky >= k:
                stale = 0 if ky > k else stale + 1
                x, k = y, ky
            else:
                stale += 1
            if k > best[0]:
                best = (k, list(x))
    return best


def main(budget):
    out = open(os.path.join(HERE, "deep_search.out"), "a")

    def emit(s):
        print(s, flush=True)
        out.write(s + "\n")
        out.flush()

    # S(6)
    odd = list(range(1, 64, 2))
    mk = lambda x: s_family(6, {odd[i] for i in range(32) if x[i]})
    k, x = climb(mk, 64, 32, 2, budget, 1)
    emit(f"S(6): k*={k} S={[odd[i] for i in range(32) if x[i]]}")
    for a in (2, 4, 5, 8):
        units = [r for r in range(81) if r % 3]
        mk = lambda x, a=a: base3_S(81, a, {units[i] for i in range(54) if x[i]})
        k, x = climb(mk, 81, 54, 2, budget, a)
        emit(f"B(81,{a}): k*={k} S={[units[i] for i in range(54) if x[i]]}")
    units = [r for r in range(27) if r % 3]
    mk = lambda x: base3_table(27, {units[i]: C8[x[i]] for i in range(18)})
    k, x = climb(mk, 27, 18, 8, budget, 7)
    emit(f"C27: k*={k} maps={dict((units[i], C8[x[i]]) for i in range(18))}")


if __name__ == "__main__":
    main(float(sys.argv[1]) if len(sys.argv) > 1 else 150)
