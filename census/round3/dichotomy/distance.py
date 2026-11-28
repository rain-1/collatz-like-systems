#!/usr/bin/env python3
"""Distance to provability (Definition 5 / Proposition 6 of dichotomy.md).

dist_Q'(T) = least |R|, R a set of residues mod Q', such that some admissible table
(H1, H2, P at modulus Q') that agrees with T off R is CERT.

* Lower bound (exact, any replacement branches): if C_1..C_k are cycles of G_{T,Q'} with
  multiplier >= 1, then R must meet every C_i (an untouched cycle keeps its edges and its
  multiplier, so it stays an obstruction).  Hence dist >= min hitting set of {C_i}.
* Upper bound: R with the 'reset' branch n -> floor(n/Q') + 1 on every r in R, verified
  CERT by decide.py.

`implicit_hitting_set` alternates: exact minimum hitting set of the cycles collected so
far (branch and bound) -> test the reset table -> if OBST, add the new bad cycles that
avoid R.  When the reset table of a minimum hitting set is CERT, lower = upper and the
distance is EXACT.
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decide import decide, residue_graph, check_hypotheses, cycle_multiplier
from neighbours import find_bad_cycle


def reset_branch(Q, r):
    return (1, (Q - r) if r else 0, Q)


def _reduce(sets):
    """Remove supersets (if C1 <= C2, hitting C1 hits C2)."""
    sets = sorted(set(sets), key=lambda b: bin(b).count("1"))
    keep = []
    for b in sets:
        if not any((k & b) == k for k in keep):
            keep.append(b)
    return keep


def min_hitting_sets(cycles, deadline=None, max_solutions=64):
    """All (up to max_solutions) minimum hitting sets, by branch and bound on bitmasks.
    Returns (size, list of solutions as sets)."""
    sets = _reduce([sum(1 << x for x in c) for c in cycles])
    best = [10 ** 9, []]

    def lb(rem):
        used, k = 0, 0
        for b in rem:                      # rem is sorted by size
            if not (b & used):
                used |= b
                k += 1
        return k

    def rec(chosen, rem):
        if deadline and time.time() > deadline:
            raise TimeoutError
        if not rem:
            if chosen.bit_count() < best[0]:
                best[0], best[1] = chosen.bit_count(), [chosen]
            elif chosen.bit_count() == best[0] and len(best[1]) < max_solutions \
                    and chosen not in best[1]:
                best[1].append(chosen)
            return
        if chosen.bit_count() + lb(rem) > best[0]:
            return
        c = rem[0]
        xs = [x for x in range(c.bit_length()) if c >> x & 1]
        freq = {x: sum(1 for d in rem if d >> x & 1) for x in xs}
        for x in sorted(xs, key=lambda y: -freq[y]):
            bx = 1 << x
            rec(chosen | bx, [d for d in rem if not (d & bx)])
    rec(0, sets)
    sols = [{x for x in range(b.bit_length()) if b >> x & 1} for b in best[1]]
    return best[0], sols


def implicit_hitting_set(Q, tab, max_rounds=200, time_limit=120):
    """Returns (lower, upper, R_upper, n_cycles, exact_flag)."""
    deadline = time.time() + time_limit
    cycles = []
    alive = set(range(Q))
    while True:                                   # initial packing
        c = find_bad_cycle(Q, tab, alive)
        if c is None:
            break
        cycles.append(frozenset(c))
        alive -= set(c)
    if not cycles:
        return 0, 0, set(), 0, True
    lower, upper, Rup = len(cycles), None, None
    for _ in range(max_rounds):
        try:
            size, sols = min_hitting_sets(cycles, deadline=deadline)
        except TimeoutError:
            break
        lower = max(lower, size)
        new = 0
        for R in sols:
            t = list(tab)
            for r in R:
                t[r] = reset_branch(Q, r)
            res = decide(Q, t, want_cycles=False, want_depth=False)
            if res["verdict"] == "CERT":
                upper, Rup = len(R), set(R)
                break
            alive = set(range(Q)) - set(R)
            while True:
                c = find_bad_cycle(Q, tab, alive)
                if c is None:
                    break
                cycles.append(frozenset(c))
                alive -= set(c)
                new += 1
            if new:
                break
            if time.time() > deadline:
                break
        if upper is not None or time.time() > deadline:
            break
        if new == 0:
            # every bad cycle of T meets each optimal R, but resets create new cycles:
            # greedy repair from the first optimal R (upper bound only)
            R = set(sols[0])
            t = list(tab)
            for r in R:
                t[r] = reset_branch(Q, r)
            for _ in range(Q):
                res = decide(Q, t, want_cycles=False, want_depth=False)
                if res["verdict"] == "CERT":
                    break
                x = next(y for y in res["obst"]["cycle"] if y not in R)
                R.add(x)
                t[x] = reset_branch(Q, x)
            upper, Rup = len(R), R
            break
    return lower, upper, Rup, len(cycles), (upper is not None and upper == lower)


if __name__ == "__main__":
    from families import lift, s_family
    from open_tables import OPEN
    maxQ = int(sys.argv[1]) if len(sys.argv) > 1 else 256
    out = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "distance.out"), "w")
    for name, (Q, tab) in OPEN.items():
        p = 2
        while Q % p:
            p += 1
        row = []
        d = p
        while Q * d <= maxQ:
            Ql = Q * d
            t0 = time.time()
            lo, up, R, nc, ex = implicit_hitting_set(Ql, lift(Q, tab, d), time_limit=60)
            row.append(f"Q'={Ql}: " + (f"{lo}" if ex else f"[{lo},{up}]")
                       + f" ({Ql and round(100*(lo if ex else lo)/Ql,1)}%)")
            d *= p
        s = f"{name}: " + "; ".join(row)
        print(s)
        out.write(s + "\n")
        out.flush()
