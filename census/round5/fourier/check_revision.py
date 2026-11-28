"""Checks for the "Revision after REFEREE1" section of README.md.  Exits 0 iff every check passes.
Run: <venv python> check_revision.py [--full]     (default about 1 min; --full adds the L = 16 constant, ~3 min more)

[A]  Translation bound (replaces the F4 consequence).  For X = 2^{b-m} (all m) and for random X, on R_b of
     split5_3, 3x+1, K7 (rb) and of 3x-1, 3x+5 (own slope-sense code):
       X P B_F >= max_t #(R_b cap (t + [0, X))) - X P,  B_F >= 1/(X P) - 1,  (1 + B_F) X P >= 1   (float, tol 1e-6;
       the max over translates is an exact integer).  Also: the translate R_b - min R_b has the same |S^| (float)
     and meets [0, 1).  And: the OLD derivation from F4 was insufficient: (1 + F4 floor) X P < 1 at b = 16, m = 16.
[C]  Base-2 decomposition used in the extended F3: |N(X,b) - X P| <= sum_{i: digit i of X is 1} 2^i P B_F(b, b - i)
     for 60 random X at b = 16 (float, tol 1e-6).
[B1] exactD (C, integers) agrees EXACTLY with a direct brute-force evaluation of the definition of D'_{L,m,k} at L = 8
     (3x+1 and K7, all odd units and the subgroup <3>), with the allowed sets built from an independent Python g.
[B2] exact constants D'_{14,m,k} (all odd units) equal the fractions quoted in README (213/1627, 213/749, 349/749, ...).
[B3] exact counts never exceed them: 3x+1 at b = 22..30 (topdigits.txt, all k/8), and 3x+1, 3x-1, 3x+5 at
     b = 14..21 (own masks), all m <= 3 and k (rational comparison).
[B4] node level, with mutation: at depth j = 14, L = 10 (b = 24) every alive node's deviation is <= D'_{10,m};
     with D' replaced by 0.4 D' some node must violate (so the check can fail; worst node is 0.474 D').
[B5] K7, split5_3: the only stuck node states are (0,0), (1,1) (all nodes, depth <= 12, exact); the stored exact
     constants D'_{16}, D'_{17} (exact_k7_L1[67].txt, exact_s53_L1[67].txt; L = 16 recomputed under --full) bound the exact counts of
     topdigits.txt (b = 22..30, m <= 2).
[E]  ratios quoted in README for N1 and N2, recomputed from decay.txt / decay_c31_28.txt.
[N3] R_b lies in one class mod 2^w (w = 2, 5, 8 for 3x+1, K7, split5_3; b = 14..22, exact), and
     |mu^(xi + 2^{b-w})| = |mu^(xi)| for all xi (b = 18, float).
"""
import sys, os, subprocess, math, tempfile
from fractions import Fraction
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import exact_u
FULL = "--full" in sys.argv
TMP = tempfile.mkdtemp(dir=os.environ.get("TMPDIR"))
FAIL = []
def ok(c, msg):
    if not c: FAIL.append(msg); print("  FAIL", msg)

def rb_mask(sys_, b):
    f = os.path.join(TMP, "bm.bin")
    subprocess.run([f"{HERE}/rb", "bitmap", str(sys_), str(b), f], check=True)
    m = np.fromfile(f, dtype=np.uint8).astype(bool); os.remove(f); return m

def own_mask(d, b):
    """slope-sense R_b for 3x+d, accelerated map T x = x/2 or (3x+d)/2; survive iff 3^{a_t} >= 2^t, t = 1..b."""
    OK = np.array([[3 ** a >= 2 ** t for t in range(b + 1)] for a in range(b + 1)])
    x = np.arange(1 << b, dtype=np.int64); a = np.zeros_like(x); alive = np.ones(len(x), dtype=bool)
    for t in range(1, b + 1):
        odd = (x & 1) == 1; x = np.where(odd, (3 * x + d) >> 1, x >> 1); a += odd; alive &= OK[a, t]
    return alive

def val2(N, b):
    xs = np.arange(N); v = np.zeros(N, dtype=np.int64); t = xs.copy(); t[0] = 1
    for _ in range(b):
        e = (t & 1) == 0; v[e] += 1; t[e] >>= 1
    v[0] = b; return v

def dir_abs(N, X, xs):
    xs = xs.astype(np.float64); return np.abs(np.sin(np.pi * X * xs / N) / np.sin(np.pi * xs / N))

def BF(mu, N, X, b):
    xs = np.arange(1, N); return float((mu[1:] * dir_abs(N, X, xs)).sum()) / X   # I^ vanishes where v >= m

# ------------------------------------------------------------------ [A]
print("[A] translation bound")
b = 16; N = 1 << b; rng = np.random.default_rng(1)
masks = {f"sys{s}": rb_mask(s, b) for s in (0, 1, 2)}
masks.update({f"3x{d:+d}": own_mask(d, b) for d in (-1, 5)})
ok(np.array_equal(masks["sys1"], own_mask(1, b)), "[A] rb and own mask disagree for 3x+1")
for name, M in masks.items():
    R = int(M.sum()); S = np.fft.fft(M.astype(np.float64)); mu = np.abs(S) / R
    cs = np.concatenate(([0], np.cumsum(np.concatenate((M, M)).astype(np.int64))))
    Xs = [1 << (b - m) for m in range(1, b + 1)] + [int(x) for x in rng.integers(1, N, 20)]
    for X in Xs:
        XP = X * R / N; B = BF(mu, N, X, b); maxtr = int((cs[X:X + N] - cs[:N]).max())
        ok(XP * B >= maxtr - XP - 1e-6, f"[A] {name} X={X}: X P B_F < max translate - X P")
        ok(B >= 1 / XP - 1 - 1e-6, f"[A] {name} X={X}: B_F < 1/(XP) - 1")
        ok((1 + B) * XP >= 1 - 1e-6, f"[A] {name} X={X}: (1 + B_F) X P < 1")
    r0 = int(np.nonzero(M)[0][0]); M2 = np.roll(M, -r0)
    ok(np.allclose(np.abs(np.fft.fft(M2.astype(np.float64))), np.abs(S), atol=1e-6) and M2[0],
       f"[A] {name}: translate has different moduli or misses 0")
M = masks["sys1"]; R = int(M.sum()); X = 1; XP = X * R / N
floor = (2 / math.pi) * (1 / (2 * XP) - 1)
print(f"  3x+1 b=16 m=16: X P = {XP:.5f}, (1 + F4 floor) X P = {(1 + floor) * XP:.4f} (< 1: F4 alone does not exclude"
      f" an N = 0 certificate); translation bound gives (1 + B_F) X P >= 1")
ok((1 + floor) * XP < 1, "[A] the old F4 consequence was not actually insufficient (expected < 1)")

# ------------------------------------------------------------------ [C]
print("[C] base-2 decomposition for general X")
mu = np.abs(np.fft.fft(M.astype(np.float64))) / R; P = R / N
BFi = {i: BF(mu, N, 1 << i, b) for i in range(b)}
for X in [int(x) for x in rng.integers(1, N, 60)]:
    dev = abs(int(M[:X].sum()) - X * P)
    bound = sum((1 << i) * P * BFi[i] for i in range(b) if (X >> i) & 1)
    ok(dev <= bound + 1e-6, f"[C] X={X}: {dev} > {bound}")

# ------------------------------------------------------------------ [B1]
print("[B1] exactD against a brute-force evaluation of the definition (L = 8)")
def g_pairs_c31(L):
    out = []
    for z in range(1 << L):
        x, a, best = z, 0, (0, 0)
        for t in range(1, L + 1):
            if x % 2: x = (3 * x + 1) // 2; a += 1
            else: x //= 2
            if Fraction(3 ** a, 2 ** t) < Fraction(3 ** best[0], 2 ** best[1]): best = (a, t)
        out.append(Fraction(3 ** best[0], 2 ** best[1]))
    return out
def brute(gvals, L, M_, units):
    """direct evaluation of the definition: max over S, u, c of |#{t < k 2^{L-M}: u t + c in S} 2^M - k|S|| / (k|S|)."""
    N_ = 1 << L; best = {}; t = np.arange(N_); c = np.arange(N_)
    g = np.array([float(x) for x in gvals]); levels = sorted(set(gvals))[1:]
    for gam in levels:                                     # all super-level sets except the full one
        inS = np.array([x >= gam for x in gvals]); sz = int(inS.sum())
        for u in units:
            hits = inS[(u * t[None, :] + c[:, None]) % N_]  # hits[c, t] = [u t + c in S]
            cs = np.cumsum(hits, axis=1)
            for k in range(1, 1 << M_):
                cnt = cs[:, k * (N_ >> M_) - 1]
                dev = Fraction(int(np.abs(cnt * (1 << M_) - k * sz).max()), k * sz)
                best[k] = max(best.get(k, Fraction(0)), dev)
    return best
L = 8; N8 = 1 << L
gv = g_pairs_c31(L)
U8, h8 = exact_u.gfun(1, L, 0, 0, TMP)
ok([Fraction(int(a), 1 << int(t)) for a, t in zip(U8, h8)] == gv, "[B1] rb gfun differs from independent g (3x+1)")
sub3 = sorted({pow(3, e, N8) for e in range(N8)})
for gen, units in ((0, list(range(1, N8, 2))), (3, sub3)):
    bf = brute(gv, L, 3, units)
    ex = exact_u.exact_D(1, L, 3, gen)
    ok(all(bf[k] == ex[k] for k in range(1, 8)), f"[B1] 3x+1 gen={gen}: exactD {ex} != brute {bf}")
# K7, both stuck states, through rb gfun ranks (brute force on the same g values)
bfk = {}
for (s, c0) in exact_u.STATES[2]:
    Uk, hk = exact_u.gfun(2, L, s, c0, TMP)
    gk = [Fraction(int(a), 1 << int(t)) for a, t in zip(Uk, hk)]
    for k, v in brute(gk, L, 3, sub3).items(): bfk[k] = max(bfk.get(k, Fraction(0)), v)
exk = exact_u.exact_D(2, L, 3, 3)
ok(all(bfk[k] == exk[k] for k in range(1, 8)), f"[B1] K7: exactD {exk} != brute {bfk}")
print("  agreement exact at L = 8")

# ------------------------------------------------------------------ [B2]
print("[B2] exact constants at L = 14 (all odd units)")
D14 = exact_u.exact_D(1, 14, 3, 0)
CLAIM14 = {4: Fraction(213, 1627), 2: Fraction(213, 749), 6: Fraction(71, 749), 1: Fraction(349, 749),
           3: Fraction(479, 2247), 5: Fraction(479, 3745), 7: Fraction(349, 5243)}
ok(D14 == CLAIM14, f"[B2] D'_14 = {D14} differs from README")
D14_3 = exact_u.exact_D(1, 14, 3, 3)
ok(D14_3 == D14, "[B2] subgroup <3> and all odd units disagree at L = 14")
if FULL:
    D16 = exact_u.exact_D(1, 16, 3, 3)
    ok(D16[4] == Fraction(129, 1057) and all(D16[k] == D14[k] for k in (1, 2, 3, 5, 6, 7)), f"[B2] D'_16 = {D16}")
    print("  L = 16 (<3>):", {k: str(v) for k, v in D16.items()})

# ------------------------------------------------------------------ [B3]
print("[B3] exact counts against D'_14")
worst = Fraction(0)
for ln in open(os.path.join(HERE, "topdigits.txt")):
    w = list(map(int, ln.split()))
    if w[0] != 1: continue
    bb, R, hist = w[1], w[2], w[3:]
    for k in range(1, 8):
        cnt = sum(hist[:k]); dev = Fraction(abs(cnt * 8 - k * R), k * R)
        ok(dev <= D14[k], f"[B3] 3x+1 b={bb} k/8={k}"); worst = max(worst, dev / D14[k])
for d in (1, -1, 5):
    for bb in range(14, 22):
        Mb = own_mask(d, bb); R = int(Mb.sum())
        for k in range(1, 8):
            cnt = int(Mb[: k << (bb - 3)].sum()); dev = Fraction(abs(cnt * 8 - k * R), k * R)
            ok(dev <= D14[k], f"[B3] 3x{d:+d} b={bb} k/8={k}"); worst = max(worst, dev / D14[k])
print(f"  largest observed deviation / D' = {float(worst):.3f}")

# ------------------------------------------------------------------ [B4]
print("[B4] node-level check (b = 24 = 14 + 10) with mutation")
D10 = exact_u.exact_D(1, 10, 3, 0)
M24 = own_mask(1, 24); j, L = 14, 10
lifts = M24.reshape(1 << L, 1 << j)          # lifts[t, r1] = [r1 + 2^j t in R_24]
size = lifts.sum(axis=0)
viol = {1.0: 0, 0.4: 0}; worstnode = Fraction(0)
for k in range(1, 8):
    cnt = lifts[: k << (L - 3)].sum(axis=0)
    for r1 in np.nonzero((size > 0) & (size < (1 << L)))[0]:
        dev = Fraction(abs(int(cnt[r1]) * 8 - k * int(size[r1])), k * int(size[r1]))
        worstnode = max(worstnode, dev / D10[k])
        for f in viol: viol[f] += dev > Fraction(f).limit_denominator(10) * D10[k]
ok(viol[1.0] == 0, f"[B4] {viol[1.0]} nodes exceed D'_10")
ok(viol[0.4] > 0, "[B4] mutation 0.4 D' produced no violation: check would be vacuous")
print(f"  worst node deviation / D'_10 = {float(worstnode):.3f}; violations of 0.4 D': {viol[0.4]}")

# ------------------------------------------------------------------ [B5]
print("[B5] K7 and split5_3: stuck states, and exact counts against D'_16")
TABLES = {0: (2, {0: (1, 0, 1), 2: (1, 0, 1), 1: (5, 3, 0), 3: (1, 3, 0)}),
          2: (2, {0: (1, 0, 1), 2: (1, 0, 1), 3: (3, 1, 1), 1: (1, -1, 2)})}
def stuck_state(sys_, x, s):
    kQ, rows = TABLES[sys_]
    while True:
        k = min(s, kQ); rs = {rows[r] for r in range(1 << kQ) if r % (1 << k) == x % (1 << k)}
        if len(rs) != 1: return (s, x % (1 << s))
        u, v, e = rs.pop(); x = (u * x + v) >> e; s -= e
for s_ in (0, 2):
    st = {stuck_state(s_, r, j) for j in range(0, 13) for r in range(1 << j)}
    ok(st == set(exact_u.STATES[s_]), f"[B5] sys {s_}: stuck states {st}")
def read_exact(fn):
    D = {}
    for ln in open(os.path.join(HERE, fn)):
        w = ln.split()
        if w and w[0] == "m":
            m, k = int(w[1]), int(w[3]); num, den = map(int, w[6].split("/")); D[(m, k)] = Fraction(num, den)
    return D
if FULL:
    for s_, fn in ((2, "exact_k7_L16.txt"), (0, "exact_s53_L16.txt")):
        ex = exact_u.exact_D(s_, 16, 2, exact_u.GEN[s_]); st = read_exact(fn)
        ok(all(ex[k << (2 - m)] == st[(m, k)] for (m, k) in st), f"[B5] recomputed {fn} differs")
for s_, fn in ((2, "exact_k7_L16.txt"), (0, "exact_s53_L16.txt"), (2, "exact_k7_L17.txt"), (0, "exact_s53_L17.txt")):
    D = read_exact(fn); wr = 0.0
    for ln in open(os.path.join(HERE, "topdigits.txt")):
        w = list(map(int, ln.split()))
        if w[0] != s_: continue
        R, hist = w[2], w[3:]
        for (m, k), Dv in D.items():
            cnt = sum(hist[: k << (3 - m)]); dev = Fraction(abs(cnt * (1 << m) - k * R), k * R)
            ok(dev <= Dv, f"[B5] sys {s_} b={w[1]} m={m} k={k}"); wr = max(wr, float(dev / Dv))
    print(f"  sys {s_}: constants {{{', '.join(f'{m}/{k}: {float(v):.4f}' for (m, k), v in D.items())}}}, "
          f"largest observed deviation / D' = {wr:.3f}")

# ------------------------------------------------------------------ [E]
print("[E] N1 / N2 ratios")
rows = {0: {}, 1: {}, 2: {}}
blk = [1, 2, 0]; lines = [l for l in open(os.path.join(HERE, "decay.txt")) if l.strip()]
for i, ln in enumerate(lines):
    w = ln.split(); sysb = blk[i // 15]
    rows[sysb][int(w[0])] = (int(w[1]), float(w[3]), float(w[9]), float(w[14]))
for ln in open(os.path.join(HERE, "decay_c31_28.txt")):
    w = ln.split(); rows[1][int(w[0])] = (int(w[1]), float(w[3]), float(w[9]), float(w[14]))
r1 = {bb: v[2] * math.sqrt(v[0]) for bb, v in rows[1].items()}
lo16 = min(r1[bb] for bb in range(16, 29)); hi16 = max(r1[bb] for bb in range(16, 29))
print(f"  N1 3x+1: max_(1<=xi<=64)|mu^| / |R_b|^(-1/2): b=16..28 range [{lo16:.2f}, {hi16:.2f}]; "
      f"b=12..15: {[round(r1[bb], 2) for bb in range(12, 16)]}")
ok(1.25 <= lo16 <= 1.30 and 3.05 <= hi16 <= 3.15, "[E] N1 range differs from README [1.27, 3.1]")
for s_, nm in ((1, "3x+1"), (2, "K7"), (0, "split5_3")):
    rat = {bb: v[1] / v[3] for bb, v in rows[s_].items() if 20 <= bb <= 26 and v[1] > 0}
    print(f"  N2 {nm}: top-level max / random-set top-level max, b=20..26 (Prop-Z zeros skipped): "
          + " ".join(f"{bb}:{x:.1f}" for bb, x in sorted(rat.items())))
    if s_ == 1: ok(2.2 <= min(rat.values()) and max(rat.values()) <= 13.5, "[E] N2 3x+1 ratio range")
    if s_ == 0: ok(min(rat.values()) < 1, "[E] split5_3 expected below the random baseline somewhere")

# ------------------------------------------------------------------ [N3]
print("[N3] one class mod 2^w and the frequency symmetry")
for s_, w in ((1, 2), (2, 5), (0, 8)):
    for bb in range(14, 23):
        r = np.nonzero(rb_mask(s_, bb))[0]
        ok(np.all((r - r[0]) % (1 << w) == 0) and not np.all((r - r[0]) % (1 << (w + 1)) == 0),
           f"[N3] sys {s_} b={bb}: R_b not in exactly one class mod 2^{w}")
    bb = 18; Mb = rb_mask(s_, bb); F = np.abs(np.fft.fft(Mb.astype(np.float64)))
    ok(np.allclose(F, np.roll(F, -(1 << (bb - w))), atol=1e-6), f"[N3] symmetry sys {s_}")

if FAIL:
    print(len(FAIL), "FAILURES"); sys.exit(1)
print("all revision checks passed"); sys.exit(0)
