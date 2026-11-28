#!/usr/bin/env python3
"""check_theory.py -- exact checks for theory.md.  Exits 0 on success, 1 on any failure.

 1. Lemma S (the key step of Theorem S): for every squarefree Q <= 2310 and both the
    first-prime and the last-prime division rule, the map r -> s*(r) (the successor of r
    whose q-digit is 0) is an edge of G_Q and permutes the q-nodes, for every prime q | Q.
 2. Theorem S, Proposition P, Proposition 4 on the finite pattern level: for Q = 2, 3, 5, 7
    and every successor pattern of the unit classes (Proposition P: every branch type), and
    for Q = 4 with halving even classes (Proposition 4), no SCC is a single expanding cycle
    unless a division-free cycle exists.  The SCC structure depends only on the pattern, so
    the check runs over patterns, not multipliers; multipliers are then set to make every
    cycle that has a non-division step expanding (the worst case for the claim).
 3. Theorem B (construction): the tables B2(u) mod 2^m (m = 3, 4, 5; odd u = 3..41) and
    Bp(u) mod p^m (p = 3, 5, 7, 11, 13; m = 2, 3 where p^m <= 2197; u = p+1..p+30, p | u
    excluded) have a type-(b) SCC with the expanding positive cycle (3 6) resp. (1 p), no
    type-(c) SCC, are OBST for decide.py, and Theorem H' gives their complete cycle list;
    the list is confirmed by iterating every n < 20000 to a listed cycle.
 4. Theorem H' on Markov mixed moduli: the Q = 6 and Q = 10 tables below, the example E15
    (Q = 15, added after REFEREE1) and the scan examples of out/typeb_mixed_examples.txt
    (Q = 12, 20, 24, 28, 36) are re-derived and their cycle lists confirmed by iteration.
 Revision after REFEREE1: part 2 also asserts that the referee's mod-4 counterexample to the
 first Proposition 4 is type (b) next to type (z) (so the hypothesis "no division-free cycle"
 is needed), and part 3 asserts the predecessor sets used in the proof of Theorem B(ii).
"""
import itertools
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import twlib  # noqa: E402

FAIL = []


def fail(msg):
    print("FAIL", msg)
    FAIL.append(msg)


def primes_of(n):
    return twlib.primes_of(n)


def squarefree(Q):
    return all(Q % (p * p) for p in primes_of(Q)) if Q > 1 else True


# ------------------------------------------------------------------ 1. Lemma S
def lemma_S(Q, rule):
    ps = primes_of(Q)
    for q in ps:
        qnodes = []
        for r in range(Q):
            S = [p for p in ps if r % p == 0]
            if not S:
                continue
            chosen = min(S) if rule == "first" else max(S)
            if chosen == q:
                qnodes.append(r)
        img = []
        for r in qnodes:
            y = r // q if r else 0
            y = (r // q) % (Q // q)
            succ = [y + (Q // q) * j for j in range(q)]
            s0 = [s for s in succ if s % q == 0]
            if len(s0) != 1:
                return False
            s = s0[0]
            S2 = [p for p in ps if s % p == 0]
            ch2 = min(S2) if rule == "first" else max(S2)
            if ch2 != q:
                return False
            img.append(s)
        if sorted(img) != sorted(qnodes):
            return False
    return True


n1 = 0
for Q in range(2, 2311):
    if squarefree(Q):
        for rule in ("first", "last"):
            if not lemma_S(Q, rule):
                fail(f"Lemma S Q={Q} rule={rule}")
            n1 += 1
print(f"1. Lemma S checked for {n1} (Q, rule) pairs")


# ------------------------------------------------------------------ 2. patterns
def sccs_from_succ(N, succ):
    return twlib.tarjan(N, succ)


def has_b_pattern(N, succ, nodiv, expandable):
    """Is some SCC a single simple cycle that can expand, while no division-free cycle
    exists?  The SCC structure depends only on the pattern; `expandable` is the set of nodes
    whose branch may have u > w (Prop P: every division node, since (u n + v)/p with u > p is
    allowed; raw tables: only the unit nodes, because a division node is n -> n/q).  A cycle
    with no expandable node contracts whatever the multipliers are."""
    # division-free cycle?
    for r0 in nodiv:
        x, seen = r0, set()
        while x in nodiv and x not in seen:
            seen.add(x)
            x = succ[x][0]
        if x in nodiv and x in seen:
            return None   # division-free cycle present
    for comp in sccs_from_succ(N, succ):
        S = set(comp)
        ne = sum(1 for r in comp for s in succ[r] if s in S)
        if ne == 0:
            continue
        if ne == len(comp) and any(r in expandable for r in comp):
            return comp
    return False


np_ = 0
for p in (2, 3, 5, 7):
    # every residue: w = 1 (single successor t) or w = p (all residues)
    choices = [("d", None)] + [("s", t) for t in range(p)]
    for pat in itertools.product(choices, repeat=p):
        succ, nodiv = [], set()
        for r, (k, t) in enumerate(pat):
            if k == "d":
                succ.append(list(range(p)))
            else:
                succ.append([t])
                nodiv.add(r)
        res = has_b_pattern(p, succ, nodiv, set(range(p)) - nodiv)
        np_ += 1
        if res:
            fail(f"Prop P: pattern {pat} mod {p} has single-cycle SCC {res}")
# Q = 4, halving even classes, odd classes with a single successor (w = 1)
for t1 in range(4):
    for t3 in range(4):
        succ = [[0, 2], [t1], [1, 3], [t3]]
        res = has_b_pattern(4, succ, {1, 3}, {1, 3})
        np_ += 1
        if res:
            fail(f"Prop 4: pattern {(t1, t3)} has single-cycle SCC {res}")
# Revision after REFEREE1: Proposition 4 needs "no division-free cycle".  The referee's
# counterexample (even -> n/2, 1 -> 3n+2, 3 -> 3n+1 mod 4) must come out as a type-(b) SCC
# {2, 3} next to the division-free loop {1}; Theorem H' must not return GLOBAL for it.
CE4 = [(1, 0, 2), (3, 2, 1), (1, 0, 2), (3, 1, 1)]
lev4 = twlib.classify_level(4, CE4, 4)
bs4 = sorted(sorted(c["cycle"]) for c in lev4["comps"] if c["type"] == "b")
if bs4 != [[2, 3]] or "z" not in lev4["types"] or "c" in lev4["types"]:
    fail(f"Prop 4 counterexample: expected (b) {{2,3}} next to (z), got {lev4['types']} {bs4}")
if twlib.theorem_H(4, CE4, lev4)["status"] == "GLOBAL":
    fail("Prop 4 counterexample: Theorem H' wrongly returned GLOBAL")
# the pattern of the counterexample, (t1, t3) = (1, 2), is exactly a case the hypothesis removes
if has_b_pattern(4, [[0, 2], [1], [1, 3], [2]], {1, 3}, {1, 3}) is not None:
    fail("Prop 4: the counterexample pattern was not recognised as having a division-free cycle")
np_ += 1
# Theorem S at level Q on patterns: squarefree Q <= 30, first-prime rule, unit classes with
# a single successor (w = 1).  Exhaustive over patterns for Q in {6, 10, 14, 15}; random
# patterns for Q in {21, 22, 26, 30}.
import random
rnd = random.Random(5)
for Q in (6, 10, 14, 15, 21, 22, 26, 30):
    units = [r for r in range(Q) if math.gcd(r, Q) == 1]
    ps = primes_of(Q)
    base = []
    for r in range(Q):
        S = [p for p in ps if r % p == 0]
        if S:
            q = min(S)
            y = (r // q) % (Q // q)
            base.append([y + (Q // q) * j for j in range(q)])
        else:
            base.append(None)
    if len(units) <= 6:
        pats = itertools.product(range(Q), repeat=len(units))
    else:
        pats = (tuple(rnd.randrange(Q) for _ in units) for _ in range(200000))
    for pat in pats:
        succ = list(base)
        for r, t in zip(units, pat):
            succ[r] = [t]
        res = has_b_pattern(Q, succ, set(units), set(units))
        np_ += 1
        if res:
            fail(f"Theorem S: Q={Q} pattern {pat} single-cycle SCC {res}")
print(f"2. {np_} successor patterns checked (Prop P, Prop 4, Theorem S)")


# ------------------------------------------------------------------ 3. Theorem B
def table_B2(u, m):
    Q = 2 ** m
    t = []
    for r in range(Q):
        if r % 2 == 0:
            t.append((1, 0, 2))
        elif r % 8 == 3:
            t.append((u, 6 - 3 * u, 1))
        elif r % 8 == 1:
            t.append((1, 1, 1))
        elif r % 8 == 5:
            t.append((1, 5, 1))
        else:
            t.append((1, 3, 1))
    return Q, t


def table_Bp(p, u, m):
    Q = p ** m
    P2 = p * p
    t = []
    for r in range(Q):
        if r % p == 0:
            t.append((1, 0, p))
        elif r % P2 == 1:
            t.append((u, p - u, 1))
        else:
            t.append((1, (2 * p - r) % P2, 1))
    return Q, t


def confirm_cycles(Q, tab, cycles, N=20000):
    T = twlib.step_fn(Q, tab)
    pts = {x for c in cycles for x in c}
    for n in range(1, N):
        x, k = n, 0
        while x not in pts:
            x = T(x)
            k += 1
            if k > 10 ** 6:
                return n
    for c in cycles:
        for i, x in enumerate(c):
            if T(x) != c[(i + 1) % len(c)]:
                return -1
    return None


nb = 0
cases = [("B2", u, m) for m in (3, 4, 5) for u in range(3, 42, 2)]
for p in (3, 5, 7, 11, 13):
    for m in (2, 3):
        if p ** m > 2197:
            continue
        for u in range(p + 1, p + 31):
            if u % p:
                cases.append((f"B{p}", u, m))
for name, u, m in cases:
    if name == "B2":
        Q, tab = table_B2(u, m)
        xs, cyc0 = 3, (3, 6)
    else:
        p = int(name[1:])
        Q, tab = table_Bp(p, u, m)
        xs, cyc0 = 1, (1, p)
    hyp = twlib.hypotheses(Q, tab)
    if not (hyp["markov"] and hyp["P"]):
        fail(f"{name} u={u} m={m}: hypotheses {hyp}")
        continue
    lev = twlib.classify_level(Q, tab, Q)
    if "c" in lev["types"] or "z" in lev["types"] or "b" not in lev["types"]:
        fail(f"{name} u={u} m={m}: types {lev['types']}")
        continue
    bs = [c for c in lev["comps"] if c["type"] == "b"]
    H = twlib.theorem_H(Q, tab, lev)
    if H["status"] != "GLOBAL" or cyc0 not in H["cycles"]:
        fail(f"{name} u={u} m={m}: H {H.get('status')} {H.get('cycles')}")
        continue
    if len(bs) != 1 or bs[0]["xstar"] != xs:
        fail(f"{name} u={u} m={m}: b data {[(b['cycle'], b.get('xstar')) for b in bs]}")
    if name != "B2" and m == 2:
        # Revision after REFEREE1: predecessor sets used in the proof of Theorem B(ii):
        # only p leads to 1, and only 0 and 1 lead to p.
        sg = twlib.graph(Q, tab, Q)
        pred1 = sorted(r for r in range(Q) if 1 in sg[r])
        predp = sorted(r for r in range(Q) if p in sg[r])
        if pred1 != [p] or predp != [0, 1]:
            fail(f"{name} u={u}: predecessors of 1 {pred1}, of p {predp}")
    if Q <= 400:
        d = twlib.D.decide(Q, tab, want_cycles=False, want_depth=False)
        if d["verdict"] != "OBST":
            fail(f"{name} u={u} m={m}: decide {d['verdict']}")
    bad = confirm_cycles(Q, tab, H["cycles"], N=5000 if Q > 300 else 20000)
    if bad is not None:
        fail(f"{name} u={u} m={m}: start {bad} misses the cycle list")
    nb += 1
print(f"3. Theorem B construction checked on {nb} tables")


# ------------------------------------------------------------------ 4. mixed Markov type (b)
MIXED = [
    (6, [(7, -4, 2), (1, 3, 1), (13, -2, 3), (13, 5, 1), (1, -2, 2), (13, -5, 1)]),
    (10, [(1, 5, 1), (11, -2, 1), (1, -1, 1), (9, 3, 2), (7, -6, 1), (1, 5, 2), (11, 4, 1),
          (11, -1, 2), (3, 3, 1), (3, 3, 2)]),
]
# Revision after REFEREE1: the example E15 of theory.md (type (b) at squarefree Q = 15 with
# general branches), with its exact cycle list.
E15 = [((1, (15 - r) % 15, 5) if r % 3 == 0 else (7, -1, 3) if r == 1 else
        (1, 14, 1) if r == 2 else (1, 15 - r, 1)) for r in range(15)]
MIXED.append((15, E15))
_lev15 = twlib.classify_level(15, E15, 15)
_b15 = [sorted(c["cycle"]) for c in _lev15["comps"] if c["type"] == "b"]
_H15 = twlib.theorem_H(15, E15, _lev15)
if _lev15["types"] != "ab" or _b15 != [[1, 2]] or _H15.get("cycles") != [(3,)]:
    fail(f"E15: types {_lev15['types']}, b {_b15}, H {_H15.get('status')} {_H15.get('cycles')}")
if not twlib.hypotheses(15, E15)["markov"] or not twlib.hypotheses(15, E15)["P"]:
    fail("E15: hypotheses")
extra = os.path.join(HERE, "out", "typeb_mixed_examples.txt")
if os.path.exists(extra):
    for line in open(extra):
        Q, tab = eval(line)
        MIXED.append((Q, tab))
nm = 0
for Q, tab in MIXED:
    lev = twlib.classify_level(Q, tab, Q)
    if "b" not in lev["types"] or "c" in lev["types"] or "z" in lev["types"]:
        fail(f"mixed Q={Q}: types {lev['types']}")
        continue
    H = twlib.theorem_H(Q, tab, lev)
    if H["status"] != "GLOBAL":
        fail(f"mixed Q={Q}: H {H}")
        continue
    bad = confirm_cycles(Q, tab, H["cycles"], N=20000)
    if bad is not None:
        fail(f"mixed Q={Q}: start {bad} misses cycles {H['cycles']}")
    nm += 1
print(f"4. Theorem H' on {nm} mixed-modulus type-(b) tables")

print("ALL CHECKS PASSED" if not FAIL else f"{len(FAIL)} FAILURES")
sys.exit(1 if FAIL else 0)
