"""Archimedean profile of mu_b^: max |mu_b^(xi)| over dyadic ranges 2^i <= |xi| < 2^{i+1} (|xi| <= N/2),
in units of |R_b|^{-1/2}; same for a random set of equal size (EVIDENCE).  usage: python profile.py SYS b"""
import sys, os, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys_, b = int(sys.argv[1]), int(sys.argv[2]); N = 1 << b
f = os.path.join(HERE, f"_p{sys_}.bin"); subprocess.run([f"{HERE}/rb", "bitmap", str(sys_), str(b), f], check=True)
bm = np.fromfile(f, dtype=np.uint8).astype(np.float32); os.remove(f); R = float(bm.sum())
F = np.abs(np.fft.rfft(bm)) / R
rnd = np.zeros(N, dtype=np.float32); rnd[np.random.default_rng(3).choice(N, int(R), replace=False)] = 1
G = np.abs(np.fft.rfft(rnd)) / R
s = R ** 0.5
print(f"sys {sys_} b {b} |R_b| {int(R)}  (entries: max|mu^| * |R_b|^(1/2) on [2^i, 2^(i+1)); random set in brackets)")
print("  " + "  ".join(f"i={i}:{F[1<<i:2<<i].max()*s:.1f}[{G[1<<i:2<<i].max()*s:.1f}]" for i in range(b - 1)))
