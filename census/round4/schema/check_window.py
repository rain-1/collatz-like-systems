#!/usr/bin/env python3
"""check_window.py -- exact checks for window.md (Theorems W1-W4).

 [W2a] gamma = 161/160 satisfies gamma^8 * 243 < 256 and 1 < gamma, and
       (3 gamma/2)^floor(5N/8) <= 2^(N-2) for 4 <= N <= 400 (the proof covers all N >= 4).
 [W2b] For N = 4..13: the explicit schema weights c_N (windowlib.schema_weights) satisfy
       c(s) u_r < c(r) w_r on EVERY edge of the window approximant T_N of 3x+1
       (all 2^N nodes, exact Fractions).
 [W2c] Independent cross-check: decide.py says CERT for T_N, N = 4..11.
 [W2d] |R_N| = sum_{k > 5N/8} C(N, k) for N = 1..18 (Terras bijection; direct count).
 [W3]  Complete cycle list of T_N for N = 4..26: only (1 2).  Every cycle meets
       F_N subset [1, B_N], B_N = ceil(161/2 * (3 gamma/2)^floor(5N/8)) (Theorem W2);
       all n <= B_N are iterated under T_N until they repeat.
 [W1]  K7 window approximants (delta = 1/5): decide.py says CERT for K = 3..11, with
       complete cycle lists; the Haar density |R_K|/2^K is printed (exact).
 [W1'p] (added after REFEREE1) Non-accelerated 3x+1 (n/2, 3n+1), the presentation of
       round3/dichotomy section 7: for N = 4..10 the generic window construction gives
       D_w = N, U_w = 3^k, and exactly the accelerated R_N; the approximant at 2^N
       (reset on R_N) is CERT by decide.py (which also checks (H1), (H2), (P)).
 [W4]  The finite facts used in Theorem W4: (3 + 1/31)^5 >= 256 > (3 + 1/32)^5, and the
       only 3x+1 cycle with an element <= 31 is (1 2).
"""
import sys, os, math
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import schemalib as S
import windowlib as W
DC = S.DC

ok = True


def claim(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name, flush=True)
    ok = ok and bool(cond)


g = Fraction(161, 160)
claim("[W2a] gamma = 161/160: gamma > 1 and gamma^8 * 243 < 256", g > 1 and g ** 8 * 243 < 256)
claim("[W2a] (3 gamma/2)^floor(5N/8) <= 2^(N-2) for N = 4..400",
      all((3 * g / 2) ** ((5 * N) // 8) <= 2 ** (N - 2) for N in range(4, 401)))

# ---------------------------------------------------------------- [W2b]
for N in range(4, 14):
    Q, tab, R = W.collatz_TN(N)
    c = W.schema_weights(N, g)
    succ = DC.residue_graph(Q, tab)
    good = True
    cmax = max(c)
    for r in range(Q):
        u, v, w = tab[r]
        if r in R:
            good &= cmax * u < c[r] * w          # all Q successors at once
        else:
            for s in succ[r]:
                good &= c[s] * u < c[r] * w
    claim(f"[W2b] N = {N}: schema potential verified on all edges of T_N "
          f"(|R_N| = {len(R)}, c_max = {float(cmax):.3f})", good)

# ---------------------------------------------------------------- [W2c]
for N in range(4, 12):
    Q, tab, R = W.collatz_TN(N)
    res = DC.decide(Q, tab, want_cycles=False, want_depth=False)
    claim(f"[W2c] N = {N}: decide.py verdict {res['verdict']}", res["verdict"] == "CERT")

# ---------------------------------------------------------------- [W2d]
good = True
for N in range(1, 19):
    cnt = sum(1 for r in range(2 ** N) if 8 * sum(W.parity_window(r, N)) > 5 * N)
    good &= cnt == sum(math.comb(N, k) for k in range(N + 1) if 8 * k > 5 * N)
claim("[W2d] |R_N| = sum_{8k > 5N} C(N,k) for N = 1..18", good)
for N in (16, 32, 64, 128, 256, 512, 1024):
    num = sum(math.comb(N, k) for k in range(N + 1) if 8 * k > 5 * N)
    print(f"      density |R_N|/2^N at N = {N}: {num / 2 ** N:.3e}")

# ---------------------------------------------------------------- [W3]
def make_TN(N):
    Q = 2 ** N
    cache = {}

    def inR(r):
        if r not in cache:
            cache[r] = 8 * sum(W.parity_window(r, N)) > 5 * N
        return cache[r]

    def T(n):
        r = n % Q
        if inR(r):
            return n // Q + 1
        return (3 * n + 1) // 2 if n % 2 else n // 2
    return T


for N in range(4, 27):
    B = math.ceil(Fraction(161, 2) * (3 * g / 2) ** ((5 * N) // 8))
    T = make_TN(N)
    owner, cycles = {}, []
    for n0 in range(1, B + 1):
        path, pos, x = [], {}, n0
        while x not in owner and x not in pos:
            pos[x] = len(path)
            path.append(x)
            x = T(x)
        if x in pos:
            cyc = path[pos[x]:]
            cycles.append(tuple(sorted(cyc)))
        for y in path:
            owner[y] = True
    claim(f"[W3] N = {N}: T_N cycles reached from [1, {B}]: {sorted(set(cycles))}",
          sorted(set(cycles)) == [(1, 2)])

# ---------------------------------------------------------------- [W1] K7
Q0, t0 = S.k7_table()
delta = Fraction(1, 5)
for K in range(3, 12):
    Q, tab, R = W.approximant(2, 2, t0, K, delta)
    res = DC.decide(Q, tab, want_depth=False)
    cyc = sorted(c[0] for c in res.get("cycles", []))
    claim(f"[W1] K7, delta = 1/5, K = {K}: |R_K|/2^K = {Fraction(len(R), Q)} = {len(R) / Q:.4f}; "
          f"{res['verdict']}; cycle minima {cyc}", res["verdict"] == "CERT" and "cycles" in res)

# ---------------------------------------------------------------- [W1'p]
plain = [(1, 0, 2), (3, 1, 1)]
for N in range(4, 11):
    Q = 2 ** N
    good, R = True, []
    for r in range(Q):
        es, U, Dw = W.window(2, 1, plain, N, r)
        k = 0
        while U % 3 == 0:
            U //= 3
            k += 1
        good &= Dw == N and U == 1
        if 8 * k > 5 * N:
            R.append(r)
    good &= set(R) == set(W.collatz_R(N))
    Rs = set(R)
    tab = [((1, (Q - r) % Q, Q) if r else (1, 0, Q)) if r in Rs else plain[r % 2] for r in range(Q)]
    res = DC.decide(Q, tab, want_cycles=False, want_depth=False)
    claim(f"[W1'p] N = {N}: plain-map windows have D_w = N and give the accelerated R_N "
          f"(|R_N| = {len(R)}); plain approximant: {res['verdict']}", good and res["verdict"] == "CERT")

# ---------------------------------------------------------------- [W4]
claim("[W4] (3 + 1/31)^5 >= 256 > (3 + 1/32)^5, so 3 + 1/x >= 2^(8/5) forces x <= 31",
      Fraction(94, 31) ** 5 >= 256 > Fraction(97, 32) ** 5)
T3 = DC.step_fn(2, [(1, 0, 2), (3, 1, 2)])
cyc = set()
for n0 in range(1, 32):
    seen, x = [], n0
    while x not in seen:
        seen.append(x)
        x = T3(x)
    cyc.add(tuple(sorted(seen[seen.index(x):])))
claim(f"[W4] the only 3x+1 cycle with an element <= 31 is {sorted(cyc)}", cyc == {(1, 2)})

print("ALL PASS" if ok else "SOME CHECK FAILED")
sys.exit(0 if ok else 1)
