#!/usr/bin/env python3
"""Task (1): enumerate small unit-multiplier tables and sort the type-(c)
ones by the structure of their excursion map.

Families (all exact; orbit statistics are EVIDENCE only):
  F2m2 : p=2, m=2, even n -> n/2; each odd class r mod 4 gets (u n + v)/w with
         u in {1,3,5}, w in {1,2,4}, v one of the two values of least |v| with
         w | u r + v (one positive, one negative).
  F2m3 : p=2, m=3, same with u in {1,3}.
  F3m2 : p=3, m=2, 3|n -> n/3; each unit class r mod 9 gets (u n + v)/3 with
         u in {1,2,4}, v one of the two values of least |v| (one positive, one
         negative) with 3 | u r + v.
  F3m2b: p=3, m=2, like F3m2 but u in {1,4,10} (multipliers = 1 mod 3; 10 = 1 mod 9).

Kept: tables with (P) (T(n) >= 1 for n >= 1), no division-free cycle.
Type: exact SCC classification of G_m (intlib.scc_types).  For every type (c)
table the decision procedure dichotomy/decide.py is run and must say OBST.

Usage: python3 census_small.py [family ...]   (default: all).  Writes enum_<fam>.json.
"""
import sys, os, json, itertools, math
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import intlib as IL


def two_vs(u, r, w):
    if w == 1:
        return [1, -1]
    v0 = (-u * r) % w
    assert v0 != 0          # r is a unit class
    return [v0, v0 - w]


def menu(p, r, us, ws):
    out = []
    for u in us:
        for w in ws:
            for v in two_vs(u, r, w):
                if v == 0 and w == 1:
                    continue
                out.append((u, v, w))
    return out


def division_free_cycle(p, m, table):
    Q = p ** m
    E = IL.AL.graph(p, m, table, m)
    nd = [r for r in range(Q) if table[r][2] == 1]
    S = set(nd)
    # DFS cycle detection in subgraph of non-dividing nodes
    color = {r: 0 for r in nd}

    def dfs(r):
        color[r] = 1
        for s, _ in E[r]:
            if s in S:
                if color[s] == 1:
                    return True
                if color[s] == 0 and dfs(s):
                    return True
        color[r] = 2
        return False
    return any(color[r] == 0 and dfs(r) for r in nd)


def family(name):
    if name == "F2m2":
        p, m, fixed = 2, 2, {0: (1, 0, 2), 2: (1, 0, 2)}
        free = [1, 3]
        menus = {r: menu(2, r, (1, 3, 5), (1, 2, 4)) for r in free}
    elif name == "F2m3":
        p, m = 2, 3
        fixed = {r: (1, 0, 2) for r in range(0, 8, 2)}
        free = [1, 3, 5, 7]
        menus = {r: menu(2, r, (1, 3), (1, 2, 4)) for r in free}
    elif name == "F3m2":
        p, m = 3, 2
        fixed = {r: (1, 0, 3) for r in range(0, 9, 3)}
        free = [r for r in range(9) if r % 3]
        menus = {r: menu(3, r, (1, 2, 4), (3,)) for r in free}
    elif name == "F3m2b":
        p, m = 3, 2
        fixed = {r: (1, 0, 3) for r in range(0, 9, 3)}
        free = [r for r in range(9) if r % 3]
        menus = {r: menu(3, r, (1, 4, 10), (3,)) for r in free}
    else:
        raise KeyError(name)
    for choice in itertools.product(*[menus[r] for r in free]):
        t = dict(fixed)
        t.update(zip(free, choice))
        yield p, m, [t[r] for r in range(p ** m)]


def vp(x, p):
    x = abs(x)
    if x == 0:
        return 99
    e = 0
    while x % p == 0:
        x //= p
        e += 1
    return e


def excursion_structure(p, m, table, comp):
    """Expanding self-loops (fixed points) inside the type-(c) SCC and their
    data: x*, multiplier u/w, s = v_p(u - 1) ('low digits of u^k fixed')."""
    Q = p ** m
    E = IL.AL.graph(p, m, table, m)
    S = set(comp["nodes"])
    fps = []
    for r in comp["nodes"]:
        u, v, w = table[r % Q]
        if Fraction(u, w) > 1 and any(s == r for s, _ in E[r]):
            x, lam = IL.periodic_point(p, m, table, m, [r])
            fps.append(dict(r=r, x=str(x), lam=str(lam), u=u, s=vp(u - 1, p)))
    return fps


def main():
    fams = sys.argv[1:] or ["F2m2", "F2m3", "F3m2", "F3m2b"]
    for fam in fams:
        counts = {}
        rows = []
        for p, m, table in family(fam):
            if not IL.positivity_ok(p, m, table):
                counts["fails (P)"] = counts.get("fails (P)", 0) + 1
                continue
            if division_free_cycle(p, m, table):
                counts["division-free cycle"] = counts.get("division-free cycle", 0) + 1
                continue
            kind, comps = IL.system_type(p, m, table)
            counts[kind] = counts.get(kind, 0) + 1
            if kind in ("c_mixed", "c_exp"):
                v = IL.decide_verdict(p, m, table)
                assert v == "OBST", (fam, table)
                cc = [c for c in comps if c["kind"] == kind][0]
                rows.append(dict(table=table, kind=kind,
                                 exp_cycle=cc["exp_cycle"], exp_lam=str(cc["exp_lam"]),
                                 con_cycle=cc.get("con_cycle"),
                                 con_lam=str(cc.get("con_lam")),
                                 fixed_points=excursion_structure(p, m, table, cc)))
        with open(os.path.join(HERE, "enum_%s.json" % fam), "w") as f:
            json.dump(dict(family=fam, counts=counts, typec=rows), f)
        print(fam, counts, flush=True)


if __name__ == "__main__":
    main()
