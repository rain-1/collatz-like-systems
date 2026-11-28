"""Minimum-size provable trap sets by exact branch and bound.

A set A is provable (types P0/P1) iff no homoclinic obstruction avoids it
(Theorems 2-4).  If A is H, the Theorem-4 witness has a finite residue set
W (orbit of x* plus the homoclinic path, mod 2^k) disjoint from A, and
every provable superset of A must contain an element of W.  Branching on
W is therefore complete; iterative deepening gives the minimum size and
all provable sets of that size (each verified by a full certificate in
check_minsize.py).
Usage: python3 minsize.py a k odd|all maxsize
"""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import traps_lib as L


def witness_set(T, A, k):
    r = L.scc_method(T, A, k, k)
    if r["ok"]:
        return None
    comp, pc = r["bad"][0]
    x, Lp, z, j, i = L.homoclinic_from_scc(T, A, k, k, r["adj"], comp)
    pts = L.orbit_q(T, x, Lp)
    y = z
    for _ in range(j):
        pts.append(y); y = T.step_q(y)
    return frozenset(L.res(p, k) for p in pts)


def min_sets(a, k, uni, maxsize, b=1):
    T = L.collatz_a(a, b=b)
    allowed = set(r for r in range(1 << k) if uni == "all" or r % 2)
    found = set()
    memo = {}

    def search(A, budget):
        key = (A, budget)
        if key in memo:
            return
        memo[key] = 1
        W = witness_set(T, set(A), k)
        if W is None:
            found.add(A)
            return
        if budget == 0:
            return
        for w in sorted(W & allowed):
            search(A | {w}, budget - 1)

    for size in range(0, maxsize + 1):
        memo.clear()
        search(frozenset(), size)
        if found:
            # keep only the minimum-size ones
            msz = min(len(s) for s in found)
            return msz, sorted(sorted(s) for s in found if len(s) == msz)
    return None, []


if __name__ == "__main__":
    a, k, uni, mx = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], int(sys.argv[4])
    t = time.time()
    sz, sets = min_sets(a, k, uni, mx)
    print(f"C{a} k={k} {uni}: min size {sz}, {len(sets)} sets, {time.time()-t:.1f}s")
    for s in sets[:10]:
        print("  ", s)
    fn = os.path.join(HERE, "results", f"minsize_C{a}_k{k}_{uni}.json")
    json.dump({"a": a, "k": k, "universe": uni, "min_size": sz, "sets": sets}, open(fn, "w"))
