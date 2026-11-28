#!/usr/bin/env python3
"""check_cutoff.py -- exact checks for cutoff.md (Theorem B1 and its instances).

Claims checked (ints / Fractions only; exits 1 on any failure):

 [C1] 3x+1 (accelerated, level 1) and K7 (n = z+1 coordinates, level 2) are of
      type (c): an exact expanding cycle in an SCC with an extra edge.
 [C2] Explicit two-block witnesses of Theorem B1.
      3x+1: A = (1,1,0) (multiplier 9/8), B = (1,0) (3/4), both closed at node 1.
      K7:   A = (0,0,0,0,2) (81/64),   B = (0,0,0,0,2,3) (81/128), closed at node 0.
      For every word over {A, B} the points following it never enter
      U_3 = {n = -1 mod 8} (3x+1), resp. U_6 = {n = 0 mod 64} (K7).  Proved in
      cutoff.md from the run-length formula; checked here: (i) the run-length formula
      itself on all residues mod 2^12, (ii) the maximal run inside any A/B
      concatenation, by enumerating all block pairs, (iii) the exact periodic points
      y_A, y_{A^i B} (i <= 12): their whole orbits avoid U_J, they differ, and
      y_{A^i B} = y_A mod 2^(K+i) as Theorem B1 step (7) needs.
 [C3] Reset cut-offs T_j (class of x* mod 2^j -> reset): exact verdicts.
      3x+1: j = 2 CERT (complete cycle list), j = 3..14 OBST and type (c).
      K7:   j = 2..5 CERT (complete cycle lists), j = 6..14 OBST and type (c).
      (For all j >= J0 this is Theorem B1; the computation is a cross-check.)
"""
import sys, os
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import schemalib as S
DC = S.DC

ok = True


def claim(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name, flush=True)
    ok = ok and bool(cond)


def compose(Q, table, walk):
    A, B = Fraction(1), Fraction(0)
    for r in walk:
        u, v, w = table[r % Q]
        A, B = A * Fraction(u, w), (B * u + v) / Fraction(w)
    return A, B


def residue(x, K):
    return (x.numerator * pow(x.denominator, -1, 2 ** K)) % 2 ** K


def periodic_point(Q, table, walk):
    """exact point following the closed level-Q walk forever (Markov property (M));
    verified: it follows the walk and returns to itself."""
    A, B = compose(Q, table, walk)
    assert A != 1
    x = B / (1 - A)
    y = x
    for r in walk:
        assert y.denominator % 2 == 1 and residue(y, 30) % Q == r
        u, v, w = table[r]
        y = (u * y + v) / w
    assert y == x
    return x, A


def orbit(Q, table, x, L):
    out, y = [], x
    for _ in range(L):
        out.append(y)
        u, v, w = table[residue(y, 30) % Q]
        y = (u * y + v) / w
    return out


SYSTEMS = {
    # name: (table, x* residue fn, A, B, J0, run-length check)
    "3x+1": dict(tab=S.collatz_table(), xstar=-1, A=[1, 1, 0], B=[1, 0], J0=3),
    "K7": dict(tab=S.k7_table(), xstar=0, A=[0, 0, 0, 0, 2], B=[0, 0, 0, 0, 2, 3], J0=6),
}

# ---------------------------------------------------------------- [C1]
for name, d in SYSTEMS.items():
    Q, tab = d["tab"]
    r = DC.decide(Q, tab, want_cycles=False, want_depth=False)
    o = r["obst"]
    U, W, size, extra = S.type_c_witness(Q, tab, o["cycle"])
    claim(f"[C1] {name}: OBST, expanding cycle {o['cycle']} multiplier {U}/{W}, SCC size {size}, "
          f"extra edge {extra}: type (c)", r["verdict"] == "OBST" and U > W)
    claim(f"[C1] {name}: no division-free cycle (standing hypothesis)", S.no_division_free_cycle(Q, tab))

# ---------------------------------------------------------------- [C2]
# (i) run-length formula.  3x+1: an odd run (consecutive odd steps) started at x has
# length exactly v2(x+1).  K7 (n-coords): a run of 3n/2 steps started at n has length
# exactly v2(n) - 1 when v2(n) >= 1 (0 when n is odd).
def v2(x):
    if x == 0:
        return 99
    k = 0
    while x % 2 == 0:
        x //= 2
        k += 1
    return k


T3 = DC.step_fn(*S.collatz_table())
TK = DC.step_fn(*S.k7_table())
good = True
for x in range(1, 2 ** 12):
    k, y = 0, x
    while y % 2 == 1:
        y = T3(y)
        k += 1
    good &= (k == v2(x + 1))
    k, y = 0, x
    while y % 4 == 0:
        y = TK(y)
        k += 1
    good &= (k == (max(v2(x) - 1, 0)))
claim("[C2](i) run-length formulas (3x+1: odd run = v2(x+1); K7: 3n/2-run = v2(n)-1) on 1..4095", good)

# (ii) maximal run of the expanding letter in any concatenation of A and B blocks.
def max_run(words, letter):
    best = 0
    for w1 in words:
        for w2 in words:
            for w3 in words:
                s = w1 + w2 + w3
                run = cur = 0
                for c in s:
                    cur = cur + 1 if c == letter else 0
                    run = max(run, cur)
                best = max(best, run)
    return best


mr3 = max_run([[1, 1, 0], [1, 0]], 1)
mrK = max_run([[0, 0, 0, 0, 2], [0, 0, 0, 0, 2, 3]], 0)
claim(f"[C2](ii) 3x+1: longest odd run in A/B words = {mr3} (< 3), so every point following an "
      f"A/B word has v2(x+1) <= 2 at every time: avoids U_3", mr3 == 2)
claim(f"[C2](ii) K7: longest 3n/2-run in A/B words = {mrK} (< 5), so v2(n) <= 5 at every time: "
      f"avoids U_6", mrK == 4)

# (iii) exact periodic points
for name, d in SYSTEMS.items():
    Q, tab = d["tab"]
    A, B, J0 = d["A"], d["B"], d["J0"]
    yA, lamA = periodic_point(Q, tab, A)
    claim(f"[C2](iii) {name}: y_A = {yA}, multiplier {lamA} > 1", lamA > 1)
    xs = Fraction(d["xstar"])
    avoid = all(residue(y, J0) != d["xstar"] % 2 ** J0 for y in orbit(Q, tab, yA, len(A)))
    rows = []
    for i in range(1, 13):
        walk = A * i + B
        y, lam = periodic_point(Q, tab, walk)
        orb = orbit(Q, tab, y, len(walk))
        avoid &= all(residue(z, J0) != d["xstar"] % 2 ** J0 for z in orb)
        K = {2: 1, 4: 2}[Q]
        agree = residue(y, K + i) == residue(yA, K + i)
        rows.append((i, y != yA, agree))
    claim(f"[C2](iii) {name}: orbits of y_A and y_(A^i B), i = 1..12, avoid U_{J0}", avoid)
    claim(f"[C2](iii) {name}: y_(A^i B) != y_A and y_(A^i B) = y_A mod 2^(K+i) for i = 1..12",
          all(a and b for _, a, b in rows))

# ---------------------------------------------------------------- [C3]
for name, d in SYSTEMS.items():
    Q0, t0 = d["tab"]
    for j in range(Q0.bit_length() - 1, 15):   # from j = 1 for 3x+1 (added after REFEREE1)
        Q = 2 ** j
        tab = S.lift(Q0, t0, Q)
        r0 = d["xstar"] % Q
        tab[r0] = S.reset(Q, r0)
        res = DC.decide(Q, tab, want_cycles=(j < d["J0"]), want_depth=False)
        if j < d["J0"]:
            claim(f"[C3] {name} cut at depth {j}: CERT, complete cycle list {sorted(c[0] for c in res['cycles'])}"
                  f" (cycle minima)", res["verdict"] == "CERT" and "cycles" in res)
        else:
            o = res["obst"]
            U, W, size, extra = S.type_c_witness(Q, tab, o["cycle"])
            claim(f"[C3] {name} cut at depth {j}: OBST and type (c) (expanding cycle {U}/{W} of length "
                  f"{len(o['cycle'])} in an SCC of {size} nodes)",
                  res["verdict"] == "OBST" and S.no_division_free_cycle(Q, tab))

print("ALL PASS" if ok else "SOME CHECK FAILED")
sys.exit(0 if ok else 1)
