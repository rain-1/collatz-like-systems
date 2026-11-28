"""Decay of the top-level and low-frequency Fourier coefficients of mu_b with b (EVIDENCE; numpy FFT).
usage: python decay.py SYS b0 b1.  Columns: b, |R_b|, max over odd xi, its xi written as +-u^a mod 2^b,
max over 1<=xi<=64 (Archimedean low frequencies), |R_b|^{-1/2}, random-set max over odd xi."""
import sys, os, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys_, b0, b1 = map(int, sys.argv[1:4]); u = 5 if sys_ == 0 else 3
rng = np.random.default_rng(7)
for b in range(b0, b1 + 1):
    N = 1 << b; f = os.path.join(HERE, f"_d{sys_}.bin")
    subprocess.run([f"{HERE}/rb", "bitmap", str(sys_), str(b), f], check=True)
    bm = np.fromfile(f, dtype=np.uint8).astype(np.float32); os.remove(f); R = float(bm.sum())
    F = np.abs(np.fft.rfft(bm)) / R  # xi in [0, N/2]; |mu^(-xi)| = |mu^(xi)|
    odd = F[1::2]; k = 2 * int(np.argmax(odd)) + 1
    # write k = +-u^a mod 2^b
    tgt = {k, (N - k) % N}; p = 1; a = None
    for e in range(N // 4 + 2):
        if p in tgt: a = e if p == k else -e; break
        p = p * u % N
    rnd = np.zeros(N, dtype=np.float32); rnd[rng.choice(N, int(R), replace=False)] = 1
    G = np.abs(np.fft.rfft(rnd)) / R
    print(f"{b:3d} {int(R):9d}  topmax {odd.max():.5f} at xi={k} = {'+' if a is not None and a >= 0 else '-'}u^{abs(a) if a is not None else '?'}"
          f"   low(1..64) {F[1:65].max():.5f}   R^-1/2 {R**-0.5:.5f}   random topmax {G[1::2].max():.5f}", flush=True)
