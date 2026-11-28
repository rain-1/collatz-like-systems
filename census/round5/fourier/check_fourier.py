"""Exact checks for the finite content of README.md (pure Python integers; exits 0 iff all pass).

[1] Independent re-implementation of the node rule; it agrees with rb's bitmaps of R_b (b <= 14).
[2] Lemma T (transfer identity): for every node r1 mod 2^j alive at depth j and every L, the lifts
    r1 + 2^j t (t < 2^L) that lie in R_{j+L} are exactly those with  (U t + (x >> s)) mod 2^L  in
    All(sigma, A) = { z : A * g_sigma(z) >= 1 },  where sigma = (s, x mod 2^s), A = U / 2^h.
[3] 3x+1: every r in R_b satisfies r = -sum_k 3^{-k} 2^{e_k} (mod 2^b), e_k = halvings before odd step k.
[4] Annihilation: for v_2(xi) >= m the sum_{x < k 2^{L-m}} e(xi x / 2^L) vanishes, checked exactly by
    showing that x mod 2^{L - v_2(xi)} takes every value equally often.
[5] Fejer floor: sum_{0<|xi|<=Z} |mu^(xi)|^2 >= (Z+1)/|R| - 1 on the actual R_b (float, margin checked).
[6] 3x+1: if no power of 3 lies in [2^{b-1}, 2^b) then R_b = R_b + 2^{b-1} (b <= 16, exact sets).
[7] Bounded-beyond-horizon bound of Theorem U is consistent with exact counts (topdigits.txt).
"""
import os, sys, subprocess
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
FAIL = []
def ok(c, msg):
    if not c: FAIL.append(msg); print("FAIL", msg)

TABLES = {  # sys: (kQ, rows {residue mod 2^kQ: (u, v, e)})
    0: (2, {0: (1, 0, 1), 2: (1, 0, 1), 1: (5, 3, 0), 3: (1, 3, 0)}),
    1: (1, {0: (1, 0, 1), 1: (3, 1, 0)}),
    2: (2, {0: (1, 0, 1), 2: (1, 0, 1), 3: (3, 1, 1), 1: (1, -1, 2)}),
}
def decided(sys_, s, x):
    kQ, rows = TABLES[sys_]; k = min(s, kQ); Q = 1 << kQ
    rs = {rows[r] for r in range(Q) if r % (1 << k) == x % (1 << k)}
    return rs.pop() if len(rs) == 1 else None

def run(sys_, x, s, U=1, h=0, track=False):
    """apply decided steps; return (alive, x, s, U, h, gmin) with gmin the minimum prefix slope (Fraction)."""
    g = Fraction(1); alive = True
    while True:
        st = decided(sys_, s, x)
        if st is None: break
        u, v, e = st
        assert (u * x + v) % (1 << e) == 0
        x = (u * x + v) >> e; U *= u; h += e; s -= e
        sl = Fraction(U, 1 << h); g = min(g, sl)
        if sl < 1: alive = False
        if not alive and not track: break
    return alive, x, s, U, h, g

def Rset(sys_, b):
    return {r for r in range(1 << b) if run(sys_, r, b)[0]}

# [1]
for sys_ in (0, 1, 2):
    for b in (8, 11, 14):
        f = os.path.join(HERE, "_chk.bin")
        subprocess.run([f"{HERE}/rb", "bitmap", str(sys_), str(b), f], check=True)
        bm = open(f, "rb").read(); os.remove(f)
        ok({r for r in range(1 << b) if bm[r]} == Rset(sys_, b), f"[1] bitmap sys {sys_} b {b}")
print("[1] done")

# [2]
for sys_ in (0, 1, 2):
    for (j, L) in ((5, 6), (8, 6), (7, 9)):
        Rb = Rset(sys_, j + L); gcache = {}
        for r1 in range(1 << j):
            alive, x, s, U, h, _ = run(sys_, r1, j)
            lifts = {t for t in range(1 << L) if (r1 + (t << j)) in Rb}
            if not alive:
                ok(not lifts, f"[2] dead node has lifts sys {sys_} r1 {r1}"); continue
            sig = (s, x % (1 << s)); A = Fraction(U, 1 << h)
            if (sig, L) not in gcache:
                gcache[(sig, L)] = [run(sys_, sig[1] + (z << s), s + L, track=True)[5] for z in range(1 << L)]
            g = gcache[(sig, L)]
            pred = {t for t in range(1 << L) if A * g[(U * t + (x >> s)) % (1 << L)] >= 1}
            ok(pred == lifts, f"[2] transfer identity sys {sys_} j {j} L {L} r1 {r1}")
print("[2] done")

# [3]
for b in (10, 13, 16):
    N = 1 << b
    for r in Rset(1, b):
        x, s, k, e, h, S = r, b, 0, [], 0, 0
        while s >= 1:
            if x % 2: x = 3 * x + 1; k += 1; e.append(h)
            else: x //= 2; h += 1; s -= 1
        S = sum(pow(3, -(i + 1), N) * (1 << e[i]) for i in range(k)) % N
        ok((r + S) % N == 0, f"[3] syracuse identity b {b} r {r}")
print("[3] done")

# [4]
for L in (8, 10):
    for m in (1, 2, 3):
        for k in range(1, 1 << m):
            K = k << (L - m)
            for v in range(m, L):
                per = 1 << (L - v)
                cnt = [0] * per
                for x in range(K): cnt[x % per] += 1
                ok(len(set(cnt)) == 1, f"[4] annihilation L {L} m {m} k {k} v {v}")
print("[4] done")

# [5]
try:
    import numpy as np
    for sys_ in (0, 1, 2):
        b = 16; R = sorted(Rset(sys_, b)); N = 1 << b
        a = np.zeros(N); a[R] = 1; F = np.abs(np.fft.fft(a)) / len(R)
        for Z in (1, 10, 100, 1000, 10000):
            lhs = 2 * float((F[1:Z + 1] ** 2).sum())
            ok(lhs >= (Z + 1) / len(R) - 1 - 1e-9, f"[5] Fejer sys {sys_} Z {Z}")
    print("[5] done")
except ImportError:
    print("[5] skipped (numpy not available; run with the venv python)")

# [6]
for b in range(2, 17):
    nopow = not any((1 << (b - 1)) <= 3 ** a < (1 << b) for a in range(0, b + 1))
    if nopow:
        R = Rset(1, b)
        ok(R == {(r + (1 << (b - 1))) % (1 << b) for r in R}, f"[6] free top digit b {b}")
print("[6] done")

# [7] exact counts against the Theorem U bounds recorded in README (3x+1: L=22, D_1 <= 0.1948, D_2 <= 0.4330,
#     D_3 <= 0.8777; valid for b >= 22)
D = {1: 0.1948, 2: 0.4330, 3: 0.8777}
for line in open(os.path.join(HERE, "topdigits.txt")):
    sy, b, *rest = map(int, line.split())
    if sy != 1 or b < 22: continue
    R, hist = rest[0], rest[1:]
    for m in (1, 2, 3):
        cnt = sum(hist[: 1 << (3 - m)])
        ok(abs(cnt / (R / (1 << m)) - 1) <= D[m], f"[7] count vs bound b {b} m {m}")
print("[7] done")

if FAIL:
    print(len(FAIL), "failures"); sys.exit(1)
print("all checks passed"); sys.exit(0)
