"""After REFEREE1 item 3 / edit 6: which isolated expanding SCCs occur in the 3n+1 S-family
at m = 6, and what the companion type-(c) SCC contains.  Exact, no z3, no floats.

Family: even r -> r/2, r/2 + 32 (mod 64); odd r -> 3r + 1 if r in S, else r + 1.

Step 1 (exact enumeration).  {62, 63} is an SCC of G_6 iff 63 in S (63 -> 62; else 63 -> 0)
and the forward closure of 31 (the other successor of 62) avoids 62 and 63.  A depth-first
search over that closure, branching on S membership of each odd node when it is first
reached, lists every such S explicitly (unreached odd classes are free).
Step 2 (comparison with the C scan).  out/brute/a3_m6_*.txt: summed over all 4096 slices,
nb = number of S whose G_6 has an SCC that is an expanding simple cycle (exact verdict, see
check_scans.py [BRUTE]).  Every S of step 1 is such an S.  If the two numbers are equal,
the sets are equal: every member with an isolated expanding SCC has {62, 63} among them.
Step 3 (each member, exact).  For every S of step 1: Tarjan SCCs with integer data; the only
SCC that is a simple cycle with multiplier 3^A/2^B > 1 is {62, 63}; and the residue cycle of
the negative 3x+1 cycle -5 -> -14 -> -7 -> -20 -> -10 (nodes 59, 50, 57, 44, 54; multiplier
9/8) is present (59, 57 in S) and lies in an SCC that is not a simple cycle, which is
therefore of type (c).  Counts of members failing either statement are printed.
Exit 0 iff the step-2 equality holds and step 3 holds for every member.
"""
import os, glob, re, sys
sys.setrecursionlimit(10000)
HERE = os.path.dirname(os.path.abspath(__file__))
Q, H = 64, 32
ODD = list(range(1, Q, 2))


def succ(r, S):
    if r % 2 == 0:
        return [r // 2, r // 2 + H]
    return [(3 * r + 1) % Q] if r in S else [(r + 1) % Q]


def enumerate_members():
    out = []

    def dfs(stack, seen, assign):
        while stack:
            r = stack.pop()
            if r % 2 == 1 and r not in assign:
                for v in (True, False):
                    a2 = dict(assign); a2[r] = v
                    dfs(stack + [r], set(seen), a2)
                return
            for q in (succ(r, {x for x, v in assign.items() if v}) if r % 2 == 1 else succ(r, ())):
                if q in (62, 63):
                    return
                if q not in seen:
                    seen.add(q); stack.append(q)
        out.append(assign)

    dfs([31], {31}, {63: True})
    return out


def sccs(S):
    idx, low, on, st, comp = {}, {}, set(), [], {}
    cnt = [0]; nc = [0]

    def strong(v):
        idx[v] = low[v] = cnt[0]; cnt[0] += 1; st.append(v); on.add(v)
        for w in succ(v, S):
            if w not in idx:
                strong(w); low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], idx[w])
        if low[v] == idx[v]:
            while True:
                w = st.pop(); on.discard(w); comp[w] = nc[0]
                if w == v:
                    break
            nc[0] += 1
    for v in range(Q):
        if v not in idx:
            strong(v)
    return comp, nc[0]


def main():
    partial = enumerate_members()
    members = []
    for a in partial:
        free = [r for r in ODD if r not in a]
        base = {r for r, v in a.items() if v}
        for mask in range(2 ** len(free)):
            members.append(frozenset(base | {free[i] for i in range(len(free)) if mask >> i & 1}))
    n1 = len(members)
    distinct = len(set(members))
    nb = 0; nfiles = 0
    for f in glob.glob(os.path.join(HERE, "out", "brute", "a3_m6_*.txt")):
        mm = re.search(r"DONE a=3 d=1 m=6 slice=\d+/4096 nb=(\d+)", open(f).read())
        if mm:
            nb += int(mm.group(1)); nfiles += 1
    print(f"step 1: {len(partial)} closure configurations, {n1} members ({distinct} distinct) "
          f"with {{62, 63}} an SCC")
    print(f"step 2: C scan, {nfiles}/4096 slices, nb = {nb}")
    ok = n1 == distinct == nb and nfiles == 4096
    bad_other = bad_comp = 0
    ghost = [59, 50, 57, 44, 54]
    for S in members:
        comp, nc = sccs(S)
        nodes = {}
        for v, c in comp.items():
            nodes.setdefault(c, []).append(v)
        for c, vs in nodes.items():
            ned = sum(1 for v in vs for w in succ(v, S) if comp[w] == c)
            if ned == len(vs) and ned > 0:          # simple cycle (or self-loop)
                A = sum(1 for v in vs if v % 2 and v in S)
                B = sum(1 for v in vs if v % 2 == 0)
                if 3 ** A > 2 ** B and sorted(vs) != [62, 63]:
                    bad_other += 1
        present = 59 in S and 57 in S
        cg = comp[59]
        same = all(comp[g] == cg for g in ghost)
        vs = nodes[cg]
        ned = sum(1 for v in vs for w in succ(v, S) if comp[w] == cg)
        if not (present and same and ned > len(vs)):
            bad_comp += 1
    print(f"step 3: members with another expanding simple-cycle SCC: {bad_other}; members where "
          f"the -5,-7,-10 residue cycle is absent or in a simple-cycle SCC: {bad_comp}")
    ok = ok and bad_other == 0 and bad_comp == 0
    print("ALL PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


main()
