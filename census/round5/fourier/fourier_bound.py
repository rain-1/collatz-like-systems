"""Theorem U (uniform transfer bound), numerical part.

For a system, a depth L and every stuck node state sigma, rb gfun gives g(z) = minimum prefix slope of the
next L digits.  For a node with slope A >= 1 the allowed set is All(sigma,A) = {z : A g(z) >= 1}; as A runs
over [1, inf) these are the super-level sets S_gamma = {g >= gamma}, gamma a value of g in (0, 1].
For each such S and each m, k (1 <= k < 2^m) we bound

    sup over units u, shifts c of | #{z in S : u^{-1}(z - c) mod 2^L < k 2^{L-m}} / (|S| k 2^{-m}) - 1 |

by the rearrangement bound  (1/N) sum_{v<m} < |S^|_v sorted , |I_k^|_v sorted > / (|S| k 2^{-m})
(classes v = 2-adic valuation of the frequency; frequencies with v >= m annihilate I_k, checked).
A cheaper bound max|S^|_v * sum|I^|_v is used to screen; the rearrangement bound is computed for the
sets that the screen does not already certify below the running maximum.
Floating point (numpy FFT, double); the FFT error is below 1e-9 * |S| here, far below the margins.
usage: python fourier_bound.py SYS L M   ->  prints D_{L,m} for m = 1..M (max over states, sets, k)
"""
import sys, subprocess, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.environ.get("TMPDIR_FB", HERE)
STATES = {0: [(0, 0), (1, 1)], 1: [(0, 0)], 2: [(0, 0), (1, 1)]}

def gfun(sys_, L, s, c0):
    f = os.path.join(TMP, f"gf_{sys_}_{L}_{s}_{c0}.bin")
    subprocess.run([f"{HERE}/rb", "gfun", str(sys_), str(L), str(s), str(c0), f], check=True)
    N = 1 << L
    raw = open(f, "rb").read(); os.remove(f)
    U = np.frombuffer(raw[:8 * N], dtype=np.uint64); h = np.frombuffer(raw[8 * N:], dtype=np.int32)
    return U, h

def interval_hats(L, m):
    N = 1 << L; xi = np.arange(N); val = np.zeros(N, dtype=np.int64)
    t = xi.copy(); val[0] = L
    nz = t != 0
    vv = np.zeros(N, dtype=np.int64); tt = t.copy()
    while True:
        e = nz & (tt % 2 == 0)
        if not e.any(): break
        vv[e] += 1; tt[e] //= 2
    vv[0] = L
    out = {}
    for k in range(1, 1 << m):
        ind = np.zeros(N); ind[: k << (L - m)] = 1.0
        Ih = np.abs(np.fft.fft(ind))
        # check annihilation for v >= m (v < L)
        assert np.all(Ih[(vv >= m) & (vv < L)] < 1e-6 * N), "annihilation failed"
        out[k] = {v: np.sort(Ih[vv == v])[::-1] for v in range(m)}
    return vv, out

def main():
    sys_, L, M = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    N = 1 << L
    vv, Ihat = interval_hats(L, M)
    hats = {m: interval_hats(L, m)[1] for m in range(1, M + 1)}
    cls = {v: np.nonzero(vv == v)[0] for v in range(M)}
    D = {m: 0.0 for m in range(1, M + 1)}; worst = {m: None for m in range(1, M + 1)}
    minsize = None
    kap = {v: 0.0 for v in range(M)}
    for (s, c0) in STATES[sys_]:
        U, h = gfun(sys_, L, s, c0)
        key = np.log2(U.astype(np.float64)) - h            # log2 g(z) <= 0
        # exact grouping: pairs (U,h) are distinct iff ratios distinct (U a power of 3 or 5)
        order = np.argsort(-key, kind="stable")
        ks = key[order]
        # boundaries between distinct values (exact via (U,h) pairs)
        Uo, ho = U[order], h[order]
        brk = np.nonzero((Uo[1:] != Uo[:-1]) | (ho[1:] != ho[:-1]))[0] + 1
        ends = list(brk) + [N]
        # the smallest admissible set is {g >= 1} = {key == 0}; sets are prefixes order[:e] with key[e-1] <= 0
        for e in ends:
            if e == N: break          # full set: all nonzero coefficients vanish
            if ks[e - 1] > 1e-12: raise SystemExit("g > 1 found")
            S = np.zeros(N); S[order[:e]] = 1.0
            sz = e
            if minsize is None or sz < minsize[0]: minsize = (sz, s, c0)
            Sh = np.abs(np.fft.fft(S))
            for v in range(M):
                kap[v] = max(kap[v], Sh[cls[v]].max() / sz)
            for m in range(1, M + 1):
                for k in range(1, 1 << m):
                    expct = sz * k / (1 << m)
                    screen = sum(Sh[cls[v]].max() * hats[m][k][v].sum() for v in range(m)) / N / expct
                    if screen <= D[m]: continue
                    rb = sum(np.dot(np.sort(Sh[cls[v]])[::-1], hats[m][k][v]) for v in range(m)) / N / expct
                    if rb > D[m]: D[m] = rb; worst[m] = (s, c0, sz, k)
    print(f"sys {sys_} L {L}: smallest allowed set {minsize}")
    print("  kappa_(L,v) = max normalized |coefficient| at valuation v over all allowed sets:",
          " ".join(f"v={v}: {kap[v]:.5f}" for v in range(M)))
    for m in range(1, M + 1):
        print(f"  D_(L={L}, m={m}) <= {D[m]:.6f}   worst (state s, c0, |S|, k) = {worst[m]}")

if __name__ == "__main__":
    main()
