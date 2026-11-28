"""Revision of N3 (README, "Revision after REFEREE1", item E).  EVIDENCE script, exact where stated.

(1) EXACT: for each system and b, the largest w such that R_b lies in ONE class mod 2^w.  Then
    mu_b^(xi + 2^{b-w} d) = e(d c / 2^w) mu_b^(xi) for that class c, so |mu_b^| is a function of xi mod 2^{b-w}
    and a printed maximiser is only a representative of its class mod 2^{b-w}.
(2) For each v = 0..4: the top 5 frequencies of the class v_2(xi) = v.  Each xi = 2^v eta (eta odd) is written
    as eta = +-u^a mod 2^{b-w-v} with a taken in the symmetric range (-ord/2, ord/2], ord = 2^{b-w-v-2}; this is
    always possible (every odd residue is +-u^a), so the content is whether |a| is SMALL (here: |a| <= b).
usage: python revision_n3.py   (writes nothing; output recorded in revision_n3.txt)
"""
import os, subprocess, tempfile, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
U = {0: 5, 1: 3, 2: 3}; NAME = {0: "split5_3", 1: "3x+1", 2: "K7"}

def Rmask(sys_, b):
    with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as t:
        f = os.path.join(t, "bm.bin")
        subprocess.run([f"{HERE}/rb", "bitmap", str(sys_), str(b), f], check=True)
        return np.fromfile(f, dtype=np.uint8).astype(bool)

def dlog_table(u, n):
    """inv[eta] = (sign, a) with eta = sign * u^a mod 2^n, a in [0, 2^{n-2})."""
    N = 1 << n; ordr = max(1, N >> 2)
    pw = np.empty(ordr, dtype=np.int64); x = 1
    for a in range(ordr): pw[a] = x; x = (x * u) % N
    A = np.full(N, -1, dtype=np.int64); S = np.zeros(N, dtype=np.int64)
    A[pw] = np.arange(ordr); S[pw] = 1
    neg = (-pw) % N; A[neg] = np.arange(ordr); S[neg] = -1
    return A, S, ordr

summary = {}; DEF = []; TOPA = []
for sys_ in (1, 2, 0):
    for b in (20, 22, 24):
        M = Rmask(sys_, b); r = np.nonzero(M)[0]; N = 1 << b
        w = 0
        while w < b and np.all((r - r[0]) % (1 << (w + 1)) == 0): w += 1
        mu = np.abs(np.fft.fft(M.astype(np.float64))) / len(r)
        xs = np.arange(N); v2 = np.zeros(N, dtype=np.int64); t = xs.copy(); t[0] = 1
        for _ in range(b):
            e = (t & 1) == 0; v2[e] += 1; t[e] >>= 1
        v2[0] = b                                   # xi = 0 is not a frequency of any class v < b
        print(f"{NAME[sys_]} b={b} |R_b|={len(r)}: R_b lies in one class mod 2^{w} (class {r[0] % (1 << w)}), "
              f"so |mu^| has period 2^{b - w} in xi")
        small = 0; tot = 0
        for v in range(5):
            n = b - w - v
            if n < 3: continue
            A, S, ordr = dlog_table(U[sys_], n)
            cls = np.nonzero((v2 == v) & (xs < (1 << (b - w))))[0]   # one representative per symmetry class
            top = cls[np.argsort(-mu[cls])[:5]]
            row = []
            for xi in top:
                eta = (int(xi) >> v) % (1 << n); a = int(A[eta]); s = int(S[eta])
                if a > ordr // 2: a -= ordr
                # agreement depth: largest n' <= n with eta = +-u^a' mod 2^n' for some |a'| <= b
                # (discrete logs are compatible with reduction: a' = a mod 2^(n'-2), symmetric representative)
                nd = n
                while nd > 3:
                    o = 1 << (nd - 2); ar = a % o
                    if ar > o // 2: ar -= o
                    if abs(ar) <= b: break
                    nd -= 1
                row.append(f"{mu[xi]:.4f}@xi={int(xi)}={'+' if s > 0 else '-'}2^{v}u^{a}[n-{n - nd}]")
                tot += 1; small += abs(a) <= b; DEF.append((sys_, b, v, rank_ := len(row), n - nd))
                if rank_ == 1 and mu[xi] > 1e-9:
                    pr = (b - v) * math.log(2) / math.log(U[sys_]) - 1
                    TOPA.append((sys_, b, v, n - nd, abs(abs(a) - pr) <= 1))
            pred = (b - v) * math.log(2) / math.log(U[sys_]) - 1
            print(f"   v={v}: top5 (distinct classes mod 2^(b-w)) " + "  ".join(row) + f"    [(b-v) log_u 2 - 1 = {pred:.1f}]")
        summary[(sys_, b)] = (small, tot)
print("[n-d] after a maximiser: it agrees with +-2^v u^a' (|a'| <= b) modulo 2^(b-w-v-d) but not modulo 2^(b-w-v-d+1)")
for sys_ in (1, 2, 0):
    first = [d for (s_, b, v, r, d) in DEF if s_ == sys_ and r == 1]
    rest = [d for (s_, b, v, r, d) in DEF if s_ == sys_ and r > 1]
    print(f"  {NAME[sys_]}: top maximiser per (b, v): deficits {first};  ranks 2-5: median deficit {sorted(rest)[len(rest)//2]}")
print("fraction of top-5 maximisers with |a| <= b:")
for k, (s, t) in summary.items(): print(f"  {NAME[k[0]]} b={k[1]}: {s}/{t}")

# claims of the revised N3 (exit 1 if they fail): for 3x+1 and K7 every nonzero top maximiser of each class v is
# +-2^v u^a modulo the full period with | |a| - ((b-v) log_u 2 - 1) | <= 1; for split5_3 this holds for at most 1 of 15
import sys
c = [t for t in TOPA if t[0] in (1, 2)]
good = all(t[3] == 0 and t[4] for t in c)
s53 = sum(1 for t in TOPA if t[0] == 0 and t[3] == 0)
print(f"3x+1/K7: {len(c)} nonzero top maximisers, all small-power: {good};  split5_3 small-power top maximisers: {s53}/15")
sys.exit(0 if good and s53 <= 1 else 1)
