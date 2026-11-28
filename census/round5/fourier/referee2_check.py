"""Referee 2: independent checks for census/round5/fourier (written from scratch; imports nothing of the prover's).

Run:  <venv python> referee2_check.py [--full]      exits 0 iff every check passes.

Own formulation.  For each system the node rule is simulated directly on x mod 2^s (s = known digits):
  3x+d (d = 1, -1, 5): accelerated, x even -> x/2, x odd -> (3x+d)/2; one digit per step; multiplier 3.
  K7:      x even -> x/2;  x = 3 mod 4 -> (3x+1)/2;  x = 1 mod 4 -> (x-1)/4 (2 digits); needs s >= 2 unless x even.
  split5_3: x even -> x/2;  x = 1 mod 4 -> 5x+3;  x = 3 mod 4 -> x+3 (0 digits); needs s >= 2 unless x even.
Slope U/2^h with U = u0^a; alive iff u0^a >= 2^h after every step (exact integer table).

[R]  own R_b against the prover's rb bitmaps (comparison only).
[T]  Lemma T exactly (Python ints) for 3x+1, K7, split5_3 at (j, L) = (7, 7), (9, 6).
[S]  stuck states of K7 / split5_3 are exactly (0,0), (1,1) at depths <= 14 (alive and dead nodes).
[D]  own exact D'_{L,m,k} (numpy integer prefix sums, Fractions): 3x+1 L = 10, 12 (all odd and <3>), L = 14 (<3>),
     compared with README fractions; K7 and split5_3 at L = 12 compared with the prover's exact_u.py at L = 12.
     --full: 3x+1 L = 14 all odd units, and L = 16 (<3>, m = 1 only).
[U]  Theorem U' against exact counts: 3x+1, 3x-1, 3x+5 (b = 14..24), K7 and split5_3 (b = 16..24), constants as
     quoted in README; reports the largest ratio deviation / D'.
[N]  node level: at b = j + L every alive non-full node's deviation <= D'_L (own D'); MUTATIONS that must fail:
     (a) 3x+1: 0.25 D'; (b) split5_3: D' computed with the trivial unit group {1} only (the max over units is needed).
[A]  F4' translation bound and Prop. Mod (float FFT, b = 14, five systems).
[Z]  Prop. Z exactly, b = 4..22.
[I]  slope survival => actual survival for 3x+1 and (referee's lemma) for K7, b = 16, over all slope survivors.
[W]  sandwich numbers in sandwich.txt recomputed for b = 16..24 from own |R_b|.
"""
import sys, os, subprocess, tempfile, math
from fractions import Fraction
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
FULL = "--full" in sys.argv
FAIL = []
def ok(c, msg):
    if not c: FAIL.append(msg); print("  FAIL", msg)
MULT = {"c1": 3, "cm1": 3, "c5": 3, "k7": 3, "s53": 5}

# ---------------------------------------------------------------- own node rule (vectorised, on x mod 2^s)
def step_arrays(sysn, x, s):
    """one decided step where possible. returns (newx, news, da, dh, decided) ; x is kept reduced mod 2^s."""
    even = (x & 1) == 0
    if sysn in ("c1", "cm1", "c5"):
        d = {"c1": 1, "cm1": -1, "c5": 5}[sysn]
        dec = s >= 1
        nx = np.where(even, x >> 1, (3 * x + d) >> 1)
        da = (~even).astype(np.int64); dh = np.ones_like(x); ds = np.ones_like(x)
    elif sysn == "k7":
        r4 = x & 3
        dec = (s >= 2) | ((s >= 1) & even)
        nx = np.where(even, x >> 1, np.where(r4 == 3, (3 * x + 1) >> 1, (x - 1) >> 2))
        da = (r4 == 3).astype(np.int64); dh = np.where(r4 == 1, 2, 1); ds = dh
    else:  # s53
        r4 = x & 3
        dec = (s >= 2) | ((s >= 1) & even)
        nx = np.where(even, x >> 1, np.where(r4 == 1, 5 * x + 3, x + 3))
        da = (r4 == 1).astype(np.int64); dh = even.astype(np.int64); ds = dh
    dec = dec & (s >= 1)
    ns = s - ds
    nx = np.where(ns > 0, nx & ((np.int64(1) << np.maximum(ns, 0)) - 1), 0)
    return nx, ns, da, dh, dec

def okt(u0, n=80):
    return np.array([[u0 ** a >= 2 ** h for h in range(n)] for a in range(n)])
OKT = {3: okt(3), 5: okt(5)}

def mask(sysn, b):
    N = 1 << b; x = np.arange(N, dtype=np.int64); s = np.full(N, b, dtype=np.int64)
    a = np.zeros(N, dtype=np.int64); h = np.zeros(N, dtype=np.int64)
    alive = np.ones(N, dtype=bool); act = np.ones(N, dtype=bool); T = OKT[MULT[sysn]]
    while act.any():
        idx = np.nonzero(act)[0]
        nx, ns, da, dh, dec = step_arrays(sysn, x[idx], s[idx])
        di = idx[dec]; x[di] = nx[dec]; s[di] = ns[dec]; a[di] += da[dec]; h[di] += dh[dec]
        alive[di] &= T[a[di], h[di]]
        act[idx[~dec]] = False; act[di] &= alive[di]
    return alive

def stuck_states(sysn, j):
    N = 1 << j; x = np.arange(N, dtype=np.int64); s = np.full(N, j, dtype=np.int64)
    act = np.ones(N, dtype=bool)
    while act.any():
        idx = np.nonzero(act)[0]
        nx, ns, da, dh, dec = step_arrays(sysn, x[idx], s[idx])
        di = idx[dec]; x[di] = nx[dec]; s[di] = ns[dec]; act[idx[~dec]] = False
    return {(int(si), int(xi)) for si, xi in zip(s, x)}

# exact ranking of slopes u0^a / 2^h
def rank_table(u0, n=80):
    pairs = [(a, h) for a in range(n) for h in range(n)]
    vals = sorted({Fraction(u0 ** a, 2 ** h) for a, h in pairs})
    pos = {v: i for i, v in enumerate(vals)}
    R = np.zeros((n, n), dtype=np.int64)
    for a, h in pairs: R[a, h] = pos[Fraction(u0 ** a, 2 ** h)]
    return R, vals

RT = {3: rank_table(3), 5: rank_table(5)}

def granks(sysn, L, s0, c0):
    """rank of g_sigma(z) = min prefix slope (incl. start 1) for value c0 + 2^s0 z with s0 + L known digits."""
    N = 1 << L; z = np.arange(N, dtype=np.int64); s = np.full(N, s0 + L, dtype=np.int64)
    x = (c0 + (z << s0)) & ((np.int64(1) << (s0 + L)) - 1)
    a = np.zeros(N, dtype=np.int64); h = np.zeros(N, dtype=np.int64)
    R, vals = RT[MULT[sysn]]; g = np.full(N, R[0, 0]); act = np.ones(N, dtype=bool)
    while act.any():
        idx = np.nonzero(act)[0]
        nx, ns, da, dh, dec = step_arrays(sysn, x[idx], s[idx])
        di = idx[dec]; x[di] = nx[dec]; s[di] = ns[dec]; a[di] += da[dec]; h[di] += dh[dec]
        g[di] = np.minimum(g[di], R[a[di], h[di]]); act[idx[~dec]] = False
    return g

STATES = {"c1": [(0, 0)], "cm1": [(0, 0)], "c5": [(0, 0)], "k7": [(0, 0), (1, 1)], "s53": [(0, 0), (1, 1)]}

def units(L, gen):
    N = 1 << L
    if gen == 0: return list(range(1, N, 2))
    out, u = [], 1
    while True:
        out.append(u); u = (u * gen) % N
        if u == 1: return out

def Dprime(rk, L, M, us, ks=None):
    """max over super-level sets S != full, u in us, shifts c of |#{t < kN/2^M : u t + c in S} 2^M - k|S|| / (k|S|).
    Implemented as: count of t < W with u t + c in S  =  #( S cap (u[0,W) + c) ); for each u build the indicator of
    u^{-1}... -- here directly: mark positions y = u^{-1} z for z in S (so u t + c in S  <=>  t + u^{-1}c in u^{-1}S)."""
    N = 1 << L; K = 1 << M; ks = ks or list(range(1, K))
    lev = np.unique(rk)[1:]
    sz = np.array([(rk >= q).sum() for q in lev], dtype=np.int64)
    best = {k: np.zeros(len(lev), dtype=np.int64) for k in ks}
    z = np.arange(N, dtype=np.int64)
    for u in us:
        uinv = pow(int(u), -1, N)
        R2 = np.empty(N, dtype=np.int64); R2[(uinv * z) % N] = rk          # R2[y] = rk[u y]
        ind = (R2[None, :] >= lev[:, None]).astype(np.int32)
        cs = np.zeros((len(lev), 2 * N + 1), dtype=np.int32)
        np.cumsum(np.concatenate((ind, ind), axis=1), axis=1, out=cs[:, 1:])
        for k in ks:
            W = (k * N) >> M
            cnt = cs[:, W:W + N] - cs[:, :N]
            d = np.maximum(cnt.max(1).astype(np.int64) * K - k * sz, k * sz - cnt.min(1).astype(np.int64) * K)
            best[k] = np.maximum(best[k], d)
    return {k: max(Fraction(int(best[k][i]), int(k * sz[i])) for i in range(len(lev))) for k in ks}

def Dsys(sysn, L, M, gen, ks=None):
    us = units(L, gen); out = {}
    for (s0, c0) in STATES[sysn]:
        for k, v in Dprime(granks(sysn, L, s0, c0), L, M, us, ks).items(): out[k] = max(out.get(k, Fraction(0)), v)
    return out

TMP = tempfile.mkdtemp(dir=os.environ.get("TMPDIR"))
def rb_mask(code, b):
    f = os.path.join(TMP, "bm.bin")
    subprocess.run([f"{HERE}/rb", "bitmap", str(code), str(b), f], check=True)
    m = np.fromfile(f, dtype=np.uint8).astype(bool); os.remove(f); return m

# ---------------------------------------------------------------- [R]
print("[R] own R_b vs prover's rb")
for sysn, code in (("s53", 0), ("c1", 1), ("k7", 2)):
    for b in (10, 15, 18):
        ok(np.array_equal(mask(sysn, b), rb_mask(code, b)), f"[R] {sysn} b={b}")

# ---------------------------------------------------------------- [T] Lemma T, Python ints
print("[T] Lemma T exactly")
def run_int(sysn, x, s):
    U0 = MULT[sysn]; a = h = 0; alive = True; gmin = Fraction(1)
    while s >= 1:
        if x % 2 == 0: x //= 2; s -= 1; h += 1
        elif sysn == "c1": x = (3 * x + 1) // 2; s -= 1; h += 1; a += 1
        elif s < 2: break
        elif sysn == "k7":
            if x % 4 == 3: x = (3 * x + 1) // 2; s -= 1; h += 1; a += 1
            else: x = (x - 1) // 4; s -= 2; h += 2
        else:
            if x % 4 == 1: x = 5 * x + 3; a += 1
            else: x = x + 3
        sl = Fraction(U0 ** a, 2 ** h); gmin = min(gmin, sl)
        if sl < 1: alive = False
    return alive, x, s, U0 ** a, h, gmin
for sysn in ("c1", "k7", "s53"):
    for (j, L) in ((7, 7), (9, 6)):
        Mb = mask(sysn, j + L); gc = {}
        for r1 in range(1 << j):
            # alive after the decided steps at depth j (stop at first death like the sets do)
            al, x, s, U, h, _ = run_int(sysn, r1, j)
            lifts = {t for t in range(1 << L) if Mb[r1 + (t << j)]}
            if not al: ok(not lifts, f"[T] {sysn} dead node {r1} has lifts"); continue
            key = (s, x % (1 << s))
            if key not in gc:
                gc[key] = [run_int(sysn, key[1] + (zz << s), s + L)[5] for zz in range(1 << L)]
            A = Fraction(U, 2 ** h)
            pred = {t for t in range(1 << L) if A * gc[key][(U * t + (x >> s)) % (1 << L)] >= 1}
            ok(pred == lifts, f"[T] {sysn} j={j} L={L} r1={r1}")

# ---------------------------------------------------------------- [S]
print("[S] stuck states")
for sysn in ("k7", "s53"):
    st = set()
    for j in range(0, 15): st |= stuck_states(sysn, j)
    ok(st == {(0, 0), (1, 1)}, f"[S] {sysn}: {st}")
ok(all(st == {(0, 0)} for st in [set().union(*[stuck_states("c1", j) for j in range(12)])]), "[S] 3x+1")

# ---------------------------------------------------------------- [D]
print("[D] exact constants D'")
F = Fraction
CL = {10: ({4: F(19, 79), 2: F(31, 71), 6: F(31, 213)}, 0),
      12: ({4: F(63, 367), 2: F(145, 433), 6: F(145, 1299), 1: F(249, 433)}, 0),
      14: ({4: F(213, 1627), 2: F(213, 749), 6: F(71, 749), 1: F(349, 749), 3: F(479, 2247), 5: F(479, 3745),
            7: F(349, 5243)}, 3)}
D = {}
for L in (10, 12):
    for gen in (0, 3):
        D[(L, gen)] = Dsys("c1", L, 3, gen)
        ok(all(D[(L, gen)][k] == v for k, v in CL[L][0].items()), f"[D] 3x+1 L={L} gen={gen}: {D[(L, gen)]}")
    ok(D[(L, 0)] == D[(L, 3)], f"[D] L={L}: <3> and all odd differ (README says same at 12)")
    print(f"  3x+1 L={L}:", {k: str(v) for k, v in D[(L, 0)].items()})
D[(14, 3)] = Dsys("c1", 14, 3, 3)
ok(all(D[(14, 3)][k] == v for k, v in CL[14][0].items()), f"[D] 3x+1 L=14 <3>: {D[(14, 3)]}")
print("  3x+1 L=14 <3>:", {k: str(v) for k, v in D[(14, 3)].items()})
if FULL:
    D[(14, 0)] = Dsys("c1", 14, 3, 0)
    ok(D[(14, 0)] == D[(14, 3)], "[D] L=14 all odd differs from <3>")
    d16 = Dsys("c1", 16, 1, 3)
    ok(d16[1] == F(129, 1057), f"[D] L=16 m=1: {d16}")
    print("  3x+1 L=16 m=1 <3>:", d16)
# K7 / split5_3 at L = 12, own vs prover's exact_u.py at the same L
PY = sys.executable
for sysn, code, gen in (("k7", 2, 3), ("s53", 0, 5)):
    mine = Dsys(sysn, 12, 2, gen)
    out = subprocess.run([PY, os.path.join(HERE, "exact_u.py"), str(code), "12", "2"], capture_output=True, text=True,
                         check=True).stdout.split("\n")
    theirs = {}
    for ln in out:
        w = ln.split()
        if w and w[0] == "m":
            m, kk = int(w[1]), int(w[3]); n_, d_ = map(int, w[6].split("/")); theirs[kk << (2 - m)] = F(n_, d_)
    ok(mine == theirs, f"[D] {sysn} L=12: mine {mine} vs exact_u {theirs}")
    print(f"  {sysn} L=12 <{gen}>: mine", {k: str(v) for k, v in mine.items()}, "| exact_u agrees:", mine == theirs)
    D[(sysn, 12)] = mine

# ---------------------------------------------------------------- [U]
print("[U] U' constants against exact counts")
QUOTED = {"c1": (14, CL[14][0], 3), "cm1": (14, CL[14][0], 3), "c5": (14, CL[14][0], 3),
          "k7": (17, {2: F(19, 66), 1: F(61, 79), 3: F(61, 237)}, 2),
          "s53": (16, {2: F(17, 25), 1: F(44, 25), 3: F(44, 75)}, 2)}
QUOTED16 = {"c1": {4: F(129, 1057)}, "k7": {2: F(19, 52), 1: F(12, 13), 3: F(4, 13)}}
BMAX = 24 if FULL else 22
Rsize = {}
for sysn, (L0, Dq, M) in QUOTED.items():
    worst = F(0)
    for b in range(min(L0, 16) if sysn in ("k7",) else L0, BMAX + 1):
        Mb = mask(sysn, b); R = int(Mb.sum()); Rsize[(sysn, b)] = R
        cum = np.concatenate(([0], np.cumsum(Mb.reshape(1 << M, -1).sum(1))))
        Duse = Dq if b >= L0 else QUOTED16[sysn]
        for k, Dv in Duse.items():
            dev = F(abs(int(cum[k]) * (1 << M) - k * R), k * R)
            ok(dev <= Dv, f"[U] {sysn} b={b} k/{1 << M}={k}: {float(dev):.4f} > {float(Dv):.4f}")
            worst = max(worst, dev / Dv)
        if sysn == "c1" and b >= 16:
            dev = F(abs(int(cum[4]) * 8 - 4 * R), 4 * R); ok(dev <= F(129, 1057), f"[U] c1 b={b} L16 const")
    print(f"  {sysn}: b = {L0}..{BMAX}, largest deviation / D' = {float(worst):.3f}")

# ---------------------------------------------------------------- [N]
print("[N] node level with mutations")
def node_check(sysn, j, L, M, Dl):
    """max over alive non-full nodes r1 at depth j and k of (deviation of the lift count in the top window) / D'_k."""
    Mb = mask(sysn, j + L); lifts = Mb.reshape(1 << L, 1 << j); size = lifts.sum(0)
    nodes = np.nonzero((size > 0) & (size < (1 << L)))[0]; worst = F(0)
    for k, Dv in Dl.items():
        cnt = lifts[: (k << L) >> M].sum(0).astype(np.int64)[nodes]; sz = size[nodes].astype(np.int64)
        dev = np.abs(cnt * (1 << M) - k * sz)
        worst = max(worst, max(F(int(d), int(k * z)) for d, z in zip(dev, sz)) / Dv)
    return worst
def D_units(sysn, L, M, us):
    out = {}
    for st_ in STATES[sysn]:
        for k, v in Dprime(granks(sysn, L, *st_), L, M, us).items(): out[k] = max(out.get(k, F(0)), v)
    return out
NODECASES = [("c1", 3, 12, 10, 3), ("k7", 3, 12, 10, 2), ("s53", 5, 12, 10, 2)]
if FULL: NODECASES += [("c1", 3, 14, 10, 3), ("k7", 3, 14, 10, 2)]
for sysn, gen, j, L, M in NODECASES:
    Dl = Dsys(sysn, L, M, gen); w = node_check(sysn, j, L, M, Dl)
    ok(w <= 1, f"[N] {sysn} j={j}: node deviation exceeds D' (ratio {float(w)})")
    D1 = D_units(sysn, L, M, [1]); w1 = node_check(sysn, j, L, M, D1)
    print(f"  {sysn} b={j + L} (j={j}, L={L}): worst node / D' = {float(w):.3f}; / D'(units {{1}} only) = {float(w1):.3f}")
    if sysn == "s53":   # mutation: dropping the max over units must break the bound here
        ok(w1 > 1, f"[N] mutation units={{1}} did not fail for s53 (ratio {float(w1)})")
    if sysn == "c1":    # mutation: a constant 0.25 D' must be violated
        ok(w > F(1, 4), f"[N] mutation 0.25 D' did not fail for c1 (ratio {float(w)})")

# ---------------------------------------------------------------- [A]
print("[A] F4' translation bound and Prop. Mod")
b = 14; N = 1 << b; rng = np.random.default_rng(7)
for sysn in ("c1", "cm1", "c5", "k7", "s53"):
    Mb = mask(sysn, b); R = int(Mb.sum()); S = np.fft.fft(Mb.astype(float))
    xs = np.arange(1, N).astype(float)
    cs = np.concatenate(([0], np.cumsum(np.concatenate((Mb, Mb)).astype(np.int64))))
    for X in [1 << (b - m) for m in range(1, b + 1)] + [int(v) for v in rng.integers(1, N, 15)]:
        I = np.abs(np.sin(np.pi * X * xs / N) / np.sin(np.pi * xs / N))
        Eabs = float((np.abs(S[1:]) * I).sum()) / N; XP = X * R / N
        Nt = cs[X:X + N] - cs[:N]
        ok(Eabs >= np.abs(Nt - XP).max() - 1e-7, f"[A] {sysn} X={X}")
        ok(Eabs + XP >= 1 - 1e-7, f"[A] {sysn} X={X} (1+B_F)XP<1")
    r0 = int(np.nonzero(Mb)[0][0]); Y = 12345 % N
    M2 = np.roll(Mb, Y - r0)
    ok(M2[Y] and np.allclose(np.abs(np.fft.fft(M2.astype(float))), np.abs(S), atol=1e-6), f"[A] Mod {sysn}")

# ---------------------------------------------------------------- [Z]
print("[Z] Proposition Z")
for b in range(4, 23):
    nopow = not any(2 ** (b - 1) <= 3 ** a < 2 ** b for a in range(b + 1))
    Mb = mask("c1", b); inv = np.array_equal(Mb, np.roll(Mb, 1 << (b - 1)))
    if nopow: ok(inv, f"[Z] b={b}")

# ---------------------------------------------------------------- [I]
print("[I] slope survival vs actual survival")
def actual_ok(sysn, n, b):
    """True iff the orbit of n stays >= n during the first b halvings."""
    x, h = n, 0
    while h < b:
        if x % 2 == 0: x //= 2; h += 1
        elif sysn == "c1": x = (3 * x + 1) // 2; h += 1
        elif x % 4 == 3: x = (3 * x + 1) // 2; h += 1
        else: x = (x - 1) // 4; h += 2
        if x < n: return False
    return True
b = 16; Mb = mask("c1", b)
ok(all(actual_ok("c1", n, b) for n in np.nonzero(Mb)[0].tolist()), "[I] 3x+1 slope survivor drops")
# K7: README R-A(ii) says the inclusion is "false as stated for K7" (negative intercept of (x-1)/4).  Referee's proof
# that it HOLDS: write x_t = sigma_t n + c_t; c -> c/2, (3c+1)/2, (c-1)/4 keep c >= -1/3 (c_0 = 0), so
# x_t >= sigma_t n - 1/3 > n - 1 whenever sigma_t >= 1, hence x_t >= n.  Check over the decided steps:
def k7_drop(n, b):
    x, s, a, h = n, b, 0, 0; drop = False
    while s >= 1:
        if x % 2 == 0: x //= 2; s -= 1; h += 1
        elif s < 2: break
        elif x % 4 == 3: x = (3 * x + 1) // 2; s -= 1; h += 1; a += 1
        else: x = (x - 1) // 4; s -= 2; h += 2
        if 3 ** a < 2 ** h: return None
        drop |= x < n
    return drop
Mk = mask("k7", b)
surv = [n for n in np.nonzero(Mk)[0].tolist() if n >= 1]
ok(all(k7_drop(n, b) is False for n in surv), "[I] a K7 slope survivor drops below itself, or own masks disagree")
print(f"  K7 b=16: all {len(surv)} slope survivors stay >= n over their decided steps (README R-A(ii) remark is wrong)")

# ---------------------------------------------------------------- [W]
print("[W] sandwich")
st = {}
for ln in open(os.path.join(HERE, "sandwich.txt")):
    w = ln.split()
    if w and w[0].isdigit(): st[int(w[0])] = list(map(float, w[1:4]))
for b in range(16, BMAX + 1):
    for m in (1, 2, 3):
        Rb = Rsize.get(("c1", b)) or int(mask("c1", b).sum())
        Rbm = Rsize.get(("c1", b - m)) or int(mask("c1", b - m).sum())
        rho = F((1 << m) * Rbm, Rb); val = float(((1 << m) - 1) * (rho - 1))
        ok(abs(val - st[b][m - 1]) < 1e-4, f"[W] b={b} m={m}: {val} vs {st[b][m - 1]}")

if FAIL:
    print(len(FAIL), "FAILURES"); sys.exit(1)
print("referee2: all checks passed"); sys.exit(0)
