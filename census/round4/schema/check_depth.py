#!/usr/bin/env python3
"""check_depth.py -- exact checks for depth.md (part A).

 [A1] Theorem A1 on 300 random members of D(2, m, word, h) (m = 4..7, random loop
      words with lam < 1, random h, i0, satisfying the CERT condition G_exit < Q):
      decide.py independently says CERT, its exact k* equals the formula of
      Theorem A1, and the complete cycle list is {(1), (the loop residues)}.
      Also 40 random members with G_exit >= Q are checked to be OBST (Theorem A1(i),
      'only if').
 [A2] Theorem A2: for the Christoffel loops of the table in depth.md, the lower bound
      k* >= h + 1 + q L, q = floor(h log3/|log lam|) (exact comparison; strengthened
      after REFEREE1 from h + L(q-1)) and the balance bound max factor product < 6.
 [A3] The best members found by search_depth.py, m = 4..9 (and best_member.py, m = 10):
      CERT condition and exact k* recomputed by the Theorem A1 formula; decide.py
      independently confirms CERT, the hypotheses and the complete cycle list (m <= 9).
 [A4] Integer witnesses (Theorem 3 lower bound of dichotomy.md) for the m = 7, 8 and 9
      members: the progression following the deepest walk is computed exactly
      (decide.path_progression), and n = a + M * 10^12 satisfies T^i(n) >= n for
      all 1 <= i < k* and T^{k*}(n) < n, by direct iteration.  This proves the LOWER
      bound k* >= value only (corrected after REFEREE1).
 [A5] Upper bound independent of Theorem A1, m = 4..8: decide.py's generic exact depth
      computation (Lambda + 1 over the residue graph) returns the same k*.
 [A3] also checks the lambda column of the records table in depth.md to 5 decimals.
"""
import sys, os, math, random, time
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "..", "round3", "dichotomy"))
import depthlib as D
import decide as DC

ok = True


def claim(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name, flush=True)
    ok = ok and bool(cond)


def chr_loop(a, b):
    return [(3, 0) if c == 'U' else (1, 1) for c in D.christoffel(a, b)]


# ---------------------------------------------------------------- [A1]
random.seed(20261127)
ncert = nobst = 0
good = True
while ncert < 300 or nobst < 40:
    m = random.randint(4, 7)
    Q = 2 ** m
    L = random.randint(1, min(20, Q // 2 - 3))
    loop = [random.choice([(3, 0), (1, 1)]) for _ in range(L)]
    if not any(e for _, e in loop) or D.loop_mult(loop, 2) >= 1:
        continue
    h = random.randint(0, min(6, Q // 2 - 2 - L))
    i0 = random.randrange(L)
    cert, k, G = D.predicted(2, m, loop, h, 3, i0)
    Qm, tab, info = D.build(2, m, loop, h, 3, i0)
    if cert and ncert < 300:
        res = DC.decide(Qm, tab)
        cyc = sorted(res.get("cycles", []))
        expect = sorted([(1,), tuple(sorted(info["loop_res"]))])
        # cycles are reported starting from the minimum; compare as sets
        got = sorted(tuple(sorted(c)) for c in cyc)
        good &= res["verdict"] == "CERT" and res["kstar"] == k and got == expect
        if not good:
            print("mismatch", m, loop, h, i0, res["verdict"], res.get("kstar"), k, got, expect)
            break
        ncert += 1
    elif not cert and nobst < 40:
        res = DC.decide(Qm, tab, want_cycles=False, want_depth=False)
        good &= res["verdict"] == "OBST"
        if not good:
            print("not OBST", m, loop, h, i0)
            break
        nobst += 1
claim(f"[A1] {ncert} random CERT members: decide.py CERT, k* = formula, cycles = {{(1), loop}}; "
      f"{nobst} members with G_exit >= Q are OBST", good)

# ---------------------------------------------------------------- [A2]
LOG3, LOG2 = math.log(3), math.log(2)
for (m, a, b) in [(6, 5, 8), (7, 17, 27), (8, 41, 65), (9, 94, 149)]:
    loop = chr_loop(a, b)
    L = a + b
    lam = D.loop_mult(loop, 2)
    Hmax = D.max_loop_walk_product(loop, 2)
    # detrended rotation i0: argmin over i of S(i) - (i/L) log lam, exact via 3^(L x) comparisons
    P = D.prefix_products(loop, 2, 0)
    i0 = min(range(L), key=lambda i: P[i] ** L / lam ** i)
    h = 0
    while 6 * 3 ** (h + 1) < 2 ** m and 2 + L + h + 1 < 2 ** (m - 1):
        h += 1
    cert, k, G = D.predicted(2, m, loop, h, 3, i0)
    mi0 = min(D.prefix_products(loop, 2, i0)[1:])
    # lower bound h + L (floor(h log3/|log lam|) - 1), floor computed exactly
    q = 0
    while Fraction(3) ** h * lam ** (q + 1) >= 1:
        q += 1
    lb = h + 1 + q * L
    claim(f"[A2] (a,b) = ({a},{b}), m = {m}: max factor product {float(Hmax):.3f} < 6, "
          f"min rotated prefix {float(mi0):.5f} >= lam = {float(lam):.5f}, h = {h}, CERT {cert}, "
          f"k* = {k} >= lower bound {lb}", Hmax < 6 and mi0 >= lam and cert and k >= lb)

# ---------------------------------------------------------------- [A3]
BEST = {4: (26, 1, 2, 2, 2), 5: (132, 3, 5, 4, 3), 6: (791, 5, 8, 11, 4), 7: (4335, 17, 27, 13, 5),
        8: (41362, 41, 65, 14, 5), 9: (133534, 94, 149, 16, 6)}
for m, (k, a, b, i0, h) in sorted(BEST.items()):
    cert, k2, G = D.predicted(2, m, chr_loop(a, b), h, 3, i0)
    claim(f"[A3] m = {m}: Christoffel({a},{b}), i0 = {i0}, h = {h}: CERT {cert}, k* = {k2}", cert and k2 == k)
    Qm, tab, info = D.build(2, m, chr_loop(a, b), h, 3, i0)
    res = DC.decide(Qm, tab, want_depth=False)       # checks (H1), (H2), (P) too
    got = sorted(tuple(sorted(c)) for c in res["cycles"])
    claim(f"[A3] m = {m}: decide.py independently: {res['verdict']}, no translation node, "
          f"complete cycle list = (1) and the {a + b}-cycle of loop residues",
          res["verdict"] == "CERT" and got == sorted([(1,), tuple(sorted(info["loop_res"]))])
          and not any(u == 1 and w == 1 for (u, v, w) in tab))

LAMBDA_TABLE = {4: (1, 2, "0.75000"), 5: (3, 5, "0.84375"), 6: (5, 8, "0.94922"),
                7: (17, 27, "0.96217"), 8: (41, 65, "0.98860"), 9: (94, 149, "0.99067"),
                10: (147, 233, "0.99274")}
good = True
for m, (a, b, txt) in LAMBDA_TABLE.items():
    lam = Fraction(3 ** a, 2 ** b)
    # exact rounding to 5 decimals: |lam - txt| <= 1/2 * 10^-5
    good &= abs(lam - Fraction(txt)) <= Fraction(1, 2 * 10 ** 5) and lam < 1
claim("[A3] lambda column of the depth.md records table correct to 5 decimals (m = 4..10)", good)

# m = 10 member: exact formula via the certified routine tstar_big (no witness: too large)
cert, k10, G10 = D.predicted_big(2, 10, chr_loop(147, 233), 6, 3, 17)
claim(f"[A3] m = 10: Christoffel(147,233), i0 = 17, h = 6: CERT {cert}, k* = {k10} (exact, tstar_big)",
      cert and k10 == 304506)

# ---------------------------------------------------------------- [A4]
for m in (7, 8, 9):
    k, a, b, i0, h = BEST[m]
    loop = chr_loop(a, b)
    Q, tab, info = D.build(2, m, loop, h, 3, i0)
    t, kk, s = D.tstar(loop, 2, i0, Fraction(3) ** h)
    assert h + t == k
    L = a + b
    nodes = info["chain_res"] + [info["loop_res"][(i0 + i) % L] for i in range(t)]
    assert len(nodes) == k            # Lambda + 1 nodes, Lambda = k - 1
    t0 = time.time()
    aa, M, A, B, Dd = DC.path_progression(Q, tab, nodes)
    n = aa + M * 10 ** 12
    T = DC.step_fn(Q, tab)
    x, good = n, True
    for i in range(1, k + 1):
        assert x % Q == (nodes[i - 1] if i - 1 < len(nodes) else x % Q)
        x = T(x)
        if i < k:
            if x < n:
                good = False
                break
    good &= x < n
    claim(f"[A4] m = {m}: witness n (modulus {M.bit_length()} bits) has T^i(n) >= n for i < {k} and "
          f"T^{k}(n) < n  ({time.time() - t0:.0f} s)", good)

# ---------------------------------------------------------------- [A5]
for m in (4, 5, 6, 7, 8):
    k, a, b, i0, h = BEST[m]
    Qm, tab, info = D.build(2, m, chr_loop(a, b), h, 3, i0)
    t0 = time.time()
    res = DC.decide(Qm, tab, want_cycles=False)
    claim(f"[A5] m = {m}: decide.py generic k* = {res.get('kstar')} equals {k} "
          f"(independent of Theorem A1; {time.time() - t0:.0f} s)",
          res["verdict"] == "CERT" and res.get("kstar") == k)

print("ALL PASS" if ok else "SOME CHECK FAILED")
sys.exit(0 if ok else 1)
