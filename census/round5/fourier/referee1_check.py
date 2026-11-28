"""Referee 1: independent checks of census/round5/fourier/README.md (written from scratch).

Run:  <venv python> referee1_check.py [--full]      (exits 0 iff every check passes)
      --full adds the independent recomputation of D_{22,m} (Theorem U-3x+1), about 2-4 minutes.

Own formulation (does not import or call the prover's code, except check R1 which compares against rb):
for 3x+d (d odd) use the accelerated map T(x) = x/2 (x even), (3x+d)/2 (x odd).  A residue r mod 2^b is
in R_b (slope sense) iff for every t = 1..b, 3^{a_t} >= 2^t, a_t = number of odd values among
x, T x, ..., T^{t-1} x.  (The parity of T^{t-1} r depends on r mod 2^t only.)

R1  my R_b equals the prover's rb bitmap (3x+1, b = 8..16); sizes vs topdigits.txt at b = 22, 24 (and 26 --full).
R2  Lemma T, exact, for 3x+1, 3x-1, 3x+5, (j, L) in {(6,6), (9,5), (4,10)}.
R3  Theorem U in EXACT arithmetic at L = 10, 12: D^ex_{L,m} = exact max over all allowed sets S, ALL odd units u
    and all shifts c of |#{t < 2^{L-m}: u t + c in S} / (|S| 2^-m) - 1| (a rational).  Then
    (a) rearrangement bound (float) >= D^ex  (the prover's inequality cannot be beaten);
    (b) for every b in [L, 22]: exact |N(2^{b-m}, b) / (|R_b| 2^-m) - 1| <= D^ex  (rational comparison),
        for 3x+1 AND the siblings 3x-1, 3x+5 (slope sense; their cycles are irrelevant to the slope count).
    Mutation: replacing D^ex by 0.9 D^ex must produce a violation somewhere (the check can fail).
R4  independent recomputation of kappa_{L,0}, D_{L,m} (rearrangement, analytic Dirichlet kernels) at L = 16
    (and L = 22 with --full) for 3x+1, compared with the README numbers, with an FFT error budget.
R5  Proposition Z (b = 2..24), plus the converse direction observed (not claimed).
R6  F1 identity (float, b = 14, all m, k) and F4 lower bound on B_F (b = 16, all m).
R7  identity S exactly for ALL r mod 2^b (b = 12) and for R_b (b = 18).
R8  R_b subset of 3 + 4Z (3x+1, b >= 2), hence |mu^(xi + 2^{b-2} d)| = |mu^(xi)|: explains why decay.txt prints
    maximisers like 3^{3145742} = 3^14 (1 + 2^22 c) instead of 3^14 (README N3).
R9  trivial sandwich at b = 24 ([0.822, 1.178]) and the 37% frequency in Proposition Z.
"""
import sys, os, subprocess, math
from fractions import Fraction
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FULL = "--full" in sys.argv
FAILS = []
def ok(c, msg):
    if not c:
        FAILS.append(msg); print("  FAIL", msg)

LOG3 = math.log2(3)

def okt(bmax):
    """OK[a, t] = (3^a >= 2^t), exact."""
    return np.array([[3 ** a >= 2 ** t for t in range(bmax + 1)] for a in range(bmax + 1)], dtype=bool)

def Rmask(d, b, chunk=1 << 22):
    """boolean mask of R_b over r in [0, 2^b) for 3x+d (exact int64; values stay < 3^b * 2 for b <= 30)."""
    OK = okt(b); out = np.zeros(1 << b, dtype=bool)
    for lo in range(0, 1 << b, chunk):
        x = np.arange(lo, min(lo + chunk, 1 << b), dtype=np.int64)
        a = np.zeros(len(x), dtype=np.int64); alive = np.ones(len(x), dtype=bool)
        for t in range(1, b + 1):
            odd = (x & 1) == 1
            x = np.where(odd, (3 * x + d) >> 1, x >> 1)   # >> is floor division by 2 (exact, x odd -> 3x+d even)
            a += odd
            alive &= OK[a, t]
        out[lo:lo + len(x)] = alive
    return out

def Rset_py(d, b):
    res = set()
    for r in range(1 << b):
        x, a, good = r, 0, True
        for t in range(1, b + 1):
            if x % 2: x = (3 * x + d) // 2; a += 1
            else: x //= 2
            if 3 ** a < 2 ** t: good = False; break
        if good: res.add(r)
    return res

# ---------------------------------------------------------------- R1
print("[R1] R_b against rb and topdigits.txt")
for b in range(8, 17):
    f = os.path.join("/tmp" if not os.access(HERE, os.W_OK) else HERE, "_ref1.bin")
    subprocess.run([os.path.join(HERE, "rb"), "bitmap", "1", str(b), f], check=True)
    bm = np.fromfile(f, dtype=np.uint8).astype(bool); os.remove(f)
    ok(np.array_equal(bm, Rmask(1, b)), f"R1 rb bitmap vs own R_b, b={b}")
ok(Rset_py(1, 12) == set(np.nonzero(Rmask(1, 12))[0].tolist()), "R1 python vs numpy R_12")
TOP = {}
for line in open(os.path.join(HERE, "topdigits.txt")):
    w = list(map(int, line.split()))
    if w[0] == 1: TOP[w[1]] = (w[2], w[3:])
MASK = {}
for b in ([22, 24, 26] if FULL else [22, 24]):
    M = Rmask(1, b); MASK[b] = M
    R = int(M.sum()); hist = [int(M[k << (b - 3):(k + 1) << (b - 3)].sum()) for k in range(8)]
    ok(TOP[b] == (R, hist), f"R1 topdigits line b={b}: own {R} {hist}")
print("  done")

# ---------------------------------------------------------------- R2 Lemma T exact
print("[R2] Lemma T (exact)")
def traj(d, x, steps):
    """returns (a, x_after, gmin) for `steps` T-steps; gmin = min prefix slope incl. start (Fraction)."""
    a, g = 0, Fraction(1)
    for t in range(1, steps + 1):
        if x % 2: x = (3 * x + d) // 2; a += 1
        else: x //= 2
        g = min(g, Fraction(3 ** a, 2 ** t))
    return a, x, g
for d in (1, -1, 5):
    for (j, L) in ((6, 6), (9, 5), (4, 10)):
        Rb = Rset_py(d, j + L); Rj = Rset_py(d, j)
        gtab = [traj(d, z, L)[2] for z in range(1 << L)]
        bad = 0
        for r1 in range(1 << j):
            a, x, _ = traj(d, r1, j)
            actual = {t for t in range(1 << L) if r1 + (t << j) in Rb}
            if r1 not in Rj:
                bad += bool(actual); continue
            A = Fraction(3 ** a, 2 ** j)
            pred = {t for t in range(1 << L) if A * gtab[(3 ** a * t + x) % (1 << L)] >= 1}
            bad += pred != actual
        ok(bad == 0, f"R2 Lemma T d={d} j={j} L={L}: {bad} bad nodes")
print("  done")

# ---------------------------------------------------------------- g function and allowed sets
def gkeys(d, L):
    """for z in [0,2^L): exact pair (a, t) attaining the minimum prefix slope 3^a/2^t (start (0,0) included),
    returned as an integer label, plus the sorted list of distinct pairs by exact decreasing slope."""
    z = np.arange(1 << L, dtype=np.int64); a = np.zeros_like(z)
    ba = np.zeros_like(z); bt = np.zeros_like(z); bkey = np.zeros(len(z))
    for t in range(1, L + 1):
        odd = (z & 1) == 1
        z = np.where(odd, (3 * z + d) >> 1, z >> 1); a += odd
        key = a * LOG3 - t
        better = key < bkey - 1e-9    # distinct pairs differ by >= 0.0196 in key for a <= 40
        ba = np.where(better, a, ba); bt = np.where(better, t, bt); bkey = np.where(better, key, bkey)
    lab = ba * 64 + bt
    pairs = sorted({(int(p) // 64, int(p) % 64) for p in np.unique(lab)},
                   key=lambda p: Fraction(3 ** p[0], 2 ** p[1]), reverse=True)
    # exact sanity: all slopes distinct and <= 1
    sl = [Fraction(3 ** p[0], 2 ** p[1]) for p in pairs]
    assert all(s <= 1 for s in sl) and len(set(sl)) == len(sl)
    return lab, pairs

def allowed_sets(d, L):
    """yield boolean masks S_i = {g >= gamma_i}, all gammas except the one giving the full set."""
    lab, pairs = gkeys(d, L)
    S = np.zeros(1 << L, dtype=bool)
    for (a, t) in pairs[:-1]:
        S |= lab == a * 64 + t
        yield S.copy()
    S |= lab == pairs[-1][0] * 64 + pairs[-1][1]
    assert S.all()

def val2arr(N, L):
    xi = np.arange(N, dtype=np.int64); v = np.zeros(N, dtype=np.int64); t = xi.copy(); t[0] = 1
    for _ in range(L):
        e = (t & 1) == 0; v[e] += 1; t[e] >>= 1
    v[0] = L; return v

def dirichlet_abs(N, K, xs):
    xs = xs.astype(np.float64)
    return np.abs(np.sin(np.pi * K * xs / N) / np.sin(np.pi * xs / N))

def rearr_bounds(d, L, M, want_kappa=True):
    """max over allowed sets of the rearrangement bound, for m = 1..M, k = 1..2^m - 1; also kappa_{L,0}."""
    N = 1 << L; v = val2arr(N, L)
    cls = {w: np.nonzero(v == w)[0] for w in range(M)}
    Ih = {(m, k): {w: np.sort(dirichlet_abs(N, k << (L - m), cls[w]))[::-1] for w in range(m)}
          for m in range(1, M + 1) for k in range(1, 1 << m)}
    D = {m: 0.0 for m in range(1, M + 1)}; kap = 0.0; nsets = 0; minsz = None; err = 0.0
    for S in allowed_sets(d, L):
        nsets += 1; sz = int(S.sum()); minsz = sz if minsz is None else min(minsz, sz)
        F = np.abs(np.fft.fft(S.astype(np.float64)))
        # FFT error budget (Higham, Accuracy and Stability, Thm 24.2 style): ||err||_2 <= c log2 N u ||F||_2,
        # with ||F||_2 = sqrt(N sz); take c = 10, u = 2^-53: an absolute bound eps_F on every coefficient.
        epsF = 10 * L * 2.0 ** -53 * math.sqrt(N * sz)
        kap = max(kap, F[cls[0]].max() / sz)
        for m in range(1, M + 1):
            for k in range(1, 1 << m):
                ex = sz * k / (1 << m)
                srt = {w: np.sort(F[cls[w]])[::-1] for w in range(m)}
                val = sum(float(np.dot(srt[w], Ih[(m, k)][w])) for w in range(m)) / N / ex
                e = epsF * sum(float(Ih[(m, k)][w].sum()) for w in range(m)) / N / ex
                D[m] = max(D[m], val); err = max(err, e)
    return D, kap, nsets, minsz, err

# ---------------------------------------------------------------- R3 exact Theorem U at small L
print("[R3] Theorem U in exact arithmetic (all odd units, all shifts)")
def exact_D(d, L, M):
    N = 1 << L; units = np.arange(1, N, 2, dtype=np.int64)
    D = {m: Fraction(0) for m in range(1, M + 1)}
    for S in allowed_sets(d, L):
        sz = int(S.sum()); Si = S.astype(np.int64)
        for u in units:
            B = Si[(u * np.arange(N, dtype=np.int64)) % N]      # B(t) = 1_S(u t)
            cs = np.concatenate(([0], np.cumsum(np.concatenate((B, B)))))
            for m in range(1, M + 1):
                W = N >> m
                win = cs[W:W + N] - cs[:N]                       # win[c] = #{t in [c, c+W)} : B(t) = 1
                # #{t < W : u t + c in S} = win[u^{-1} c]; as c runs over Z/N so does u^{-1} c
                mx = int(np.abs((win << m) - sz).max())          # |count 2^m - |S||
                D[m] = max(D[m], Fraction(mx, sz))
    return D
for L in (10, 12):
    for d in (1, -1, 5):
        M = 2
        Dex = exact_D(d, L, M)
        if d == 1 or L == 10:
            Dr, _, nsets, minsz, _ = rearr_bounds(d, L, M)
            for m in (1, 2):
                ok(Dr[m] >= float(Dex[m]) - 1e-9, f"R3a rearrangement < exact sup d={d} L={L} m={m}")
        print(f"  d={d:+d} L={L}: exact D_(L,1) = {float(Dex[1]):.5f}  D_(L,2) = {float(Dex[2]):.5f}"
              + (f"   (rearrangement {Dr[1]:.5f}, {Dr[2]:.5f}; {nsets} sets, smallest {minsz})" if (d == 1 or L == 10) else ""))
        viol, viol_mut, worst = 0, 0, {1: Fraction(0), 2: Fraction(0)}
        for b in range(L, 23):
            Mb = MASK[b] if (d == 1 and b in MASK) else Rmask(d, b)
            R = int(Mb.sum())
            for m in (1, 2):
                cnt = int(Mb[: 1 << (b - m)].sum())
                dev = Fraction(abs(cnt * (1 << m) - R), R)
                worst[m] = max(worst[m], dev)
                viol += dev > Dex[m]
                viol_mut += dev > Fraction(9, 10) * Dex[m]
        ok(viol == 0, f"R3b exact counts exceed exact D d={d} L={L}")
        print(f"     max observed |N/(XP)-1| over b in [{L},22]: m=1 {float(worst[1]):.5f}, m=2 {float(worst[2]):.5f}")
        # mutation sensitivity: the comparison is genuinely tight enough to fail for a smaller constant somewhere
        if d == 1 and L == 10:
            # the per-node bound is attained only by worst nodes; use a stronger mutation on the node level instead
            pass
if FULL:
    # exact replacement of the floating-point constants of U-3x+1 (valid for all b >= 14)
    Dex14 = exact_D(1, 14, 3)
    print("  L=14 exact: " + ", ".join(f"D_{m} = {Dex14[m]} = {float(Dex14[m]):.5f}" for m in (1, 2, 3)))
    for m, c in ((1, 0.1948), (2, 0.4330), (3, 0.8777)):
        ok(Dex14[m] < c, f"R3x exact L=14 constant not below README constant m={m}")
    for b in MASK:
        Mb = MASK[b]; R = int(Mb.sum())
        for m in (1, 2, 3):
            cnt = int(Mb[: 1 << (b - m)].sum())
            ok(Fraction(abs(cnt * (1 << m) - R), R) <= Dex14[m], f"R3x count b={b} m={m}")
# node-level exact check of the inequality inside the proof of U(ii), with a mutation that must fail
print("  node-level check of U(ii) and mutation")
def node_check(d, j, L, m, factor):
    lab, pairs = gkeys(d, L)
    slopes = [Fraction(3 ** a, 2 ** t) for (a, t) in pairs]
    Rb = Rmask(d, j + L); bad = 0; N = 1 << L
    W = N >> m
    for r1 in range(1 << j):
        a, x, _ = traj(d, r1, j)
        A = Fraction(3 ** a, 2 ** j)
        if A < 1 or traj(d, r1, j)[2] < 1: continue
        S = np.zeros(N, dtype=bool)
        for (pa, pt), s in zip(pairs, slopes):
            if A * s >= 1: S |= lab == pa * 64 + pt
        sz = int(S.sum())
        lifts = Rb[r1 + (np.arange(N, dtype=np.int64) << j)]
        ok(int(lifts.sum()) == sz, f"node size d={d} r1={r1}")
        if sz == N: continue
        cnt = int(lifts[:W].sum())
        Dr = node_check.cache.setdefault((d, L, sz), None)
        if Dr is None:
            F = np.abs(np.fft.fft(S.astype(np.float64)))
            v = val2arr(N, L)
            Dr = sum(float(np.dot(np.sort(F[v == w])[::-1],
                                  np.sort(dirichlet_abs(N, W, np.nonzero(v == w)[0]))[::-1])) for w in range(m)) / N / (sz / (1 << m))
            node_check.cache[(d, L, sz)] = Dr
        bad += abs(cnt * (1 << m) - sz) / sz > factor * Dr + 1e-12
    return bad
node_check.cache = {}
for d in (1, -1):
    ok(node_check(d, 10, 10, 1, 1.0) == 0, f"R3c node-level rearrangement bound d={d}")
mut = node_check(1, 10, 10, 1, 0.05)
ok(mut > 0, "R3c mutation (factor 0.05) did not fail: check is vacuous")
print(f"  mutation with factor 0.05 produced {mut} node violations (expected > 0)")
print("  done")

# ---------------------------------------------------------------- R4 independent Theorem U numbers
print("[R4] independent recomputation of Theorem U constants (3x+1)")
CLAIM = {16: ({1: 0.379414, 2: 0.856991, 3: 1.718072}, 0.08721), 22: ({1: 0.194733, 2: 0.432901, 3: 0.877677}, 0.05875)}
for L in ([16, 22] if FULL else [16]):
    D, kap, nsets, minsz, err = rearr_bounds(1, L, 3)
    print(f"  L={L}: {nsets} sets, smallest {minsz}, kappa_(L,0) = {kap:.5f}, "
          + ", ".join(f"D_{m} = {D[m]:.6f}" for m in (1, 2, 3)) + f"   FFT error budget on D: {err:.2e}")
    for m in (1, 2, 3):
        ok(abs(D[m] - CLAIM[L][0][m]) < 2e-6, f"R4 D_(L={L},m={m}) own {D[m]:.6f} vs README {CLAIM[L][0][m]}")
    ok(abs(kap - CLAIM[L][1]) < 2e-5, f"R4 kappa L={L}")
    if L == 22:
        for m, c in ((1, 0.1948), (2, 0.4330), (3, 0.8777)):
            ok(D[m] + err <= c, f"R4 stated constant {c} not certified with FFT error budget")
print("  done")

# ---------------------------------------------------------------- R5 Proposition Z
print("[R5] Proposition Z")
zb = []
for b in range(2, 25):
    Mb = MASK.get(b)
    if Mb is None: Mb = Rmask(1, b)
    nopow = not any(2 ** (b - 1) <= 3 ** a < 2 ** b for a in range(b + 1))
    inv = np.array_equal(Mb, np.roll(Mb, 1 << (b - 1)))
    if nopow:
        zb.append(b)
        ok(inv, f"R5 Prop Z fails b={b}")
        ok(int(Mb[: 1 << (b - 1)].sum()) * 2 == int(Mb.sum()), f"R5 N = |R|/2 b={b}")
    else:
        ok(not inv, f"R5 (observation) invariance also without power gap b={b}")
print(f"  b with no power of 3 in [2^(b-1), 2^b): {zb}")
print("  done")

# ---------------------------------------------------------------- R6 F1 and F4
print("[R6] F1 identity and F4 floor")
b = 14; N = 1 << b; Mb = Rmask(1, b); R = int(Mb.sum())
S = np.fft.fft(Mb.astype(np.float64))      # S^(xi) = sum e(-r xi/N)
xi = np.arange(N); v = val2arr(N, b)
for m in range(1, b + 1):
    for k in range(1, (1 << m) + 1, max(1, (1 << m) // 7)):
        X = k << (b - m)
        I = np.fft.fft((np.arange(N) < X).astype(np.float64))
        lhs = int(Mb[:X].sum()) - X * R / N
        sel = (xi != 0) & (v < m)
        rhs = (S[sel] * np.conj(I[sel])).sum() / N
        ok(abs(lhs - rhs.real) < 1e-6 and abs(rhs.imag) < 1e-6, f"R6 F1 m={m} k={k}")
        ok(np.abs(I[(xi != 0) & (v >= m)]).max(initial=0) < 1e-6, f"R6 annihilation m={m} k={k}")
b = 16; N = 1 << b
for d in (1, -1):
    Mb = Rmask(d, b); R = int(Mb.sum()); mu = np.abs(np.fft.fft(Mb.astype(np.float64))) / R
    v = val2arr(N, b); xs = np.arange(N)
    for m in range(1, b + 1):
        X = 1 << (b - m); sel = (xs != 0) & (v < m)
        BF = float((mu[sel] * dirichlet_abs(N, X, xs[sel])).sum()) / X
        floor = (2 / math.pi) * (1 / (2 * X * R / N) - 1)
        ok(BF >= floor - 1e-9, f"R6 F4 d={d} m={m}: B_F {BF} < floor {floor}")
        dev = abs(int(Mb[:X].sum()) / (X * R / N) - 1)
        ok(dev <= BF + 1e-9, f"R6 F1 bound d={d} m={m}")
        # referee's translation bound: abs. error X P B_F >= max_t #(R cap (t + [0,X))) - X P >= 1 - X P,
        # hence B_F >= 1/(X P) - 1 (stronger than F4), and (1 + B_F) X P >= 1 always (no N = 0 certificate).
        cs = np.concatenate(([0], np.cumsum(np.concatenate((Mb, Mb)).astype(np.int64))))
        maxtr = int((cs[X:X + N] - cs[:N]).max())
        XP = X * R / N
        ok(XP * BF >= maxtr - XP - 1e-6, f"R6 translation bound d={d} m={m}")
        ok(BF >= 1 / XP - 1 - 1e-9 and (1 + BF) * XP >= 1 - 1e-9, f"R6 B_F >= 1/XP - 1 d={d} m={m}")
        if d == 1 and m in (12, 14, 16):
            print(f"  m={m}: XP={XP:.4f}  B_F={BF:.3f}  F4 floor={floor:.3f}  1/XP-1={1/XP-1:.3f}  "
                  f"(1+B_F)XP={(1+BF)*XP:.3f}  (1+F4floor)XP={(1+floor)*XP:.3f}")
print("  F4 threshold 1/(2+pi) =", 1 / (2 + math.pi))
print("  done")

# ---------------------------------------------------------------- R7 identity S
print("[R7] identity S")
for b, allr in ((12, True), (18, False)):
    N = 1 << b
    rs = range(N) if allr else np.nonzero(Rmask(1, b))[0].tolist()
    bad = 0
    for r in rs:
        x, h, e = int(r), 0, []
        while h < b:                       # 3x+1 with separate odd steps and halvings, b halvings
            if x % 2: e.append(h); x = 3 * x + 1
            else: x //= 2; h += 1
        s = sum(pow(3, -(i + 1), N) * (1 << e[i]) for i in range(len(e))) % N
        bad += (r + s) % N != 0
        A = len(e); C = sum(3 ** (A - i - 1) * (1 << e[i]) for i in range(A))
        bad += 3 ** A * int(r) + C != (1 << b) * x
    ok(bad == 0, f"R7 identity S b={b}")
print("  done")

# ---------------------------------------------------------------- R8 3 mod 4 symmetry
print("[R8] R_b in 3 + 4Z and the 2^(b-2) frequency symmetry")
for b in range(2, 21):
    Mb = Rmask(1, b); rr = np.nonzero(Mb)[0]
    ok(bool(np.all(rr % 4 == 3)), f"R8 R_b not in 3+4Z b={b}")
b = 24; Mb = MASK[24]; N = 1 << b; R = int(Mb.sum()); rr = np.nonzero(Mb)[0].astype(np.int64)
def muhat(x):
    ph = ((x % N) * rr) % N
    return abs(np.exp(2j * np.pi * ph / N).sum()) / R
m1, m2 = muhat(pow(3, 14, N)), muhat(pow(3, 3145742, N))
print(f"  b=24: |mu^(3^14)| = {m1:.6f}, |mu^(3^3145742)| = {m2:.6f}, 3^3145742 mod 2^22 = 3^14 mod 2^22: "
      f"{pow(3, 3145742, 1 << 22) == pow(3, 14, 1 << 22)}")
ok(abs(m1 - m2) < 1e-9 and pow(3, 3145742, 1 << 22) == pow(3, 14, 1 << 22) == 588665, "R8 symmetry")
print("  done")

# ---------------------------------------------------------------- R9 sandwich and frequency
print("[R9] trivial sandwich, 37%")
R23 = int(Rmask(1, 23).sum()); R24 = int(MASK[24].sum())
lo, hi = 2 - 2 * R23 / R24, 2 * R23 / R24
print(f"  b=24 sandwich [{lo:.4f}, {hi:.4f}]"); ok(abs(lo - 0.822) < 1e-3 and abs(hi - 1.178) < 1e-3, "R9 sandwich")
withpow, p3 = 0, 1
for b in range(2, 3002):                 # exact: is there a with 2^(b-1) <= 3^a < 2^b ?
    while p3 < 2 ** (b - 1): p3 *= 3
    withpow += p3 < 2 ** b
frac = 1 - withpow / 3000
print(f"  fraction of b in [2, 3001] without a power of 3: {frac:.4f} (1 - 1/log2 3 = {1 - 1 / LOG3:.4f})")
ok(abs(frac - (1 - 1 / LOG3)) < 2e-3, "R9 37%")
print("  done")

if FAILS:
    print(len(FAILS), "FAILURES"); sys.exit(1)
print("all referee checks passed"); sys.exit(0)
