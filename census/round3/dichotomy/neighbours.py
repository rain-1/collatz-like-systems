#!/usr/bin/env python3
"""Application (3b): nearest provable neighbours of the open GLOBAL table maps.

For an open map T presented at modulus Q, lift it to Q' = Q*p (p = least prime of Q)
and modify the branch on one or two residue classes mod Q'.  Menu of replacement
branches for a class r with original branch (u, v, w):
  damp(u')  : (u', v, w) with 1 <= u' < u, gcd(u', Q') = 1, exact and positive;
  reset     : n -> floor(n/Q') + 1  (i.e. (1, Q'-r, Q') for r > 0, (1, 0, Q') for r = 0).
Every modified table is decided exactly by decide.py; CERT neighbours get their complete
cycle list and minimal stopping depth k*.

Distance to provability at level l (modulus Q_l = Q p^l):
  dist_l(T) = least |R| such that SOME admissible table agreeing with T off R is CERT.
  Lower bound (Proposition 6 in dichotomy.md): a family of pairwise vertex-disjoint
  cycles of G_{T,Q_l} with multiplier >= 1 must each be hit by R.
  Upper bound: a set R found by greedy search with the damp/reset menu.
Output: neighbours.out.  Runtime ~3-6 minutes.   Usage: python3 neighbours.py [maxlevel]
"""
import sys, os, math, itertools, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decide import (decide, residue_graph, karp_float, karp_np, cycle_multiplier,
                    translation_cycles, check_hypotheses)
from families import lift, rule_string
from open_tables import OPEN

HERE = os.path.dirname(os.path.abspath(__file__))


def least_prime(Q):
    p = 2
    while Q % p:
        p += 1
    return p


def menu(Q, r, br):
    u, v, w = br
    out = []
    for u2 in range(1, u):
        if math.gcd(u2, Q) != 1 or (u2 * r + v) % w:
            continue
        n0 = r if r else Q
        if (u2 * n0 + v) // w >= 1:
            out.append(("damp", (u2, v, w)))
    out.append(("reset", (1, (Q - r) if r else 0, Q)))
    return out


def find_bad_cycle(Q, tab, alive=None):
    """A cycle with multiplier >= 1 inside the alive node set (exact check), or None."""
    succ = residue_graph(Q, tab)
    if alive is not None:
        succ = [[s for s in succ[r] if s in alive] if r in alive else [] for r in range(Q)]
    # translation cycles
    for cyc, drift in translation_cycles(Q, tab):
        if alive is None or all(x in alive for x in cyc):
            return cyc
    # isolate nodes with no out-edges by giving them a hugely negative self-loop-free treatment
    nodes = [r for r in range(Q) if succ[r]]
    if not nodes:
        return None
    # prune nodes that cannot lie on a cycle (iteratively remove sinks)
    alive2 = set(nodes)
    changed = True
    while changed:
        changed = False
        for r in list(alive2):
            if not any(s in alive2 for s in succ[r]):
                alive2.discard(r)
                changed = True
    if not alive2:
        return None
    idx = sorted(alive2)
    pos = {r: i for i, r in enumerate(idx)}
    sub = [[pos[s] for s in succ[r] if s in alive2] for r in idx]
    subtab = [tab[r] for r in idx]
    mu, cyc = (karp_float if len(idx) <= 64 else karp_np)(len(idx), subtab, sub)
    if cyc is None:
        return None
    cyc = [idx[i] for i in cyc]
    U, W = cycle_multiplier(tab, cyc)
    return cyc if U >= W else None


def packing_lower_bound(Q, tab):
    alive = set(range(Q))
    packed = []
    while True:
        c = find_bad_cycle(Q, tab, alive)
        if c is None:
            return packed
        packed.append(c)
        alive -= set(c)


def mean_after(Q, tab):
    succ = residue_graph(Q, tab)
    if translation_cycles(Q, tab):
        return 1e9
    return (karp_float if Q <= 64 else karp_np)(Q, tab, succ)[0]


def greedy_upper(Q, tab):
    """Greedy: while OBST, modify one node of the offending cycle (best resulting mean)."""
    orig = list(tab)
    tab = list(tab)
    R = {}
    for _ in range(Q):
        res = decide(Q, tab, want_cycles=False, want_depth=False)
        if res["verdict"] == "CERT":
            break
        cyc = res["obst"]["cycle"]
        best = None
        for r in cyc:
            for name, br in menu(Q, r, tab[r]):
                t2 = list(tab)
                t2[r] = br
                try:
                    check_hypotheses(Q, t2)
                except AssertionError:
                    continue
                m = mean_after(Q, t2)
                key = (m, name != "damp")
                if best is None or key < best[0]:
                    best = (key, r, name, br)
        _, r, name, br = best
        R[r] = (name, br)
        tab[r] = br
    else:
        return None
    # prune
    for r in list(R):
        t2 = list(tab)
        t2[r] = orig[r]
        if decide(Q, t2, want_cycles=False, want_depth=False)["verdict"] == "CERT":
            tab = t2
            del R[r]
    return R


def neighbours(name, Q, tab, out):
    p = least_prime(Q)
    Q1 = Q * p
    base = lift(Q, tab, p)
    res0 = decide(Q, tab, want_cycles=False, want_depth=False)
    out(f"== {name}: Q={Q}, verdict {res0['verdict']}"
        + (f" ({res0['obst']['kind']}, cycle multiplier {res0['obst']['U']}/{res0['obst']['W']}"
           + (f", periodic point {res0['obst'].get('periodic_point')}" if 'periodic_point' in res0['obst'] else "")
           + ")" if res0['verdict'] == 'OBST' else ""))
    menus = {r: menu(Q1, r, base[r]) for r in range(Q1)}
    one, two = [], []
    n1 = n2 = 0
    for r in range(Q1):
        for nm, br in menus[r]:
            t = list(base)
            t[r] = br
            n1 += 1
            res = decide(Q1, t, want_cycles=False, want_depth=False)
            if res["verdict"] == "CERT":
                one.append(((r, nm, br),))
    for r1, r2 in itertools.combinations(range(Q1), 2):
        for (nm1, b1), (nm2, b2) in itertools.product(menus[r1], menus[r2]):
            t = list(base)
            t[r1] = b1
            t[r2] = b2
            n2 += 1
            res = decide(Q1, t, want_cycles=False, want_depth=False)
            if res["verdict"] == "CERT":
                two.append(((r1, nm1, b1), (r2, nm2, b2)))
    out(f"   level Q'={Q1}: one-class modifications CERT {len(one)}/{n1}; "
        f"two-class CERT {len(two)}/{n2}")
    recs = []
    for mods in one + two:
        t = list(base)
        for r, nm, br in mods:
            t[r] = br
        res = decide(Q1, t, cap=2 * 10 ** 6)
        cyc = res.get("cycles")
        rec = dict(entry=name, Q=Q1, mods=[(r, nm, list(br)) for r, nm, br in mods],
                   kstar=res["kstar"], ncycles=None if cyc is None else len(cyc),
                   cycles=None if cyc is None else [list(c) if len(c) <= 40 else list(c[:40]) + ["..."] for c in cyc],
                   Fsize=None if "F" not in res else len(res["F"]))
        recs.append(rec)
    for rec in sorted(recs, key=lambda x: -x["kstar"])[:4]:
        mins = None if rec["cycles"] is None else sorted(c[0] for c in rec["cycles"])
        out(f"   e.g. mods {rec['mods']}: k*={rec['kstar']}, |F|={rec['Fsize']}, cycle minima {mins}")
    return recs


if __name__ == "__main__":
    maxlev = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    f = open(os.path.join(HERE, "neighbours.out"), "w")
    allrecs = []

    def out(s):
        print(s)
        f.write(s + "\n")
        f.flush()

    for name, (Q, tab) in OPEN.items():
        t0 = time.time()
        allrecs += neighbours(name, Q, tab, out)
        # distance to provability at levels 1..maxlev (exact when lower == upper)
        from distance import implicit_hitting_set
        p = least_prime(Q)
        row = []
        for lev in range(1, maxlev + 1):
            Ql = Q * p ** lev
            if Ql > 256:
                break
            lo, up, R, nc, ex = implicit_hitting_set(Ql, lift(Q, tab, p ** lev), time_limit=30)
            row.append(f"{Ql}:{lo}" if ex else f"{Ql}:[{lo},{up if up is not None else '?'}]")
        out(f"   distance to provability dist_Q' (exact, or [lower,upper]): {', '.join(row)}"
            f"   [{time.time()-t0:.0f}s]")
    json.dump(allrecs, open(os.path.join(HERE, "scratch", "neighbours.json"), "w"))
