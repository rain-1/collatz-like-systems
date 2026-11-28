"""|mu_b^(xi)| at xi = 2^v u^a mod 2^b (u = 3 for 3x+1 and K7, 5 for split5_3), b = 24 (EVIDENCE)."""
import sys, os, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys_, b = int(sys.argv[1]), int(sys.argv[2]); N = 1 << b; u = 5 if sys_ == 0 else 3
f = os.path.join(HERE, "_bm.bin"); subprocess.run([f"{HERE}/rb", "bitmap", str(sys_), str(b), f], check=True)
bm = np.fromfile(f, dtype=np.uint8).astype(float); os.remove(f); R = bm.sum()
F = np.abs(np.fft.fft(bm)) / R
for v in (0, 1, 2, 4):
    row = []
    for a in range(0, 31):
        row.append(F[(pow(u, a, N) << v) % N])
    best = int(np.argmax(row))
    lev = np.nonzero([(x >> v) & 1 for x in range(N)])  # unused
    print(f"v={v}: |mu^(2^v u^a)| a=0..30:", " ".join(f"{x:.3f}" for x in row), f"  argmax a={best}")
    print(f"      (max over all xi with v_2 = {v}: {F[np.arange(1 << v, N, 1 << (v + 1))].max():.4f})")
