"""Test of the Fourier (L1) criterion on the actual mu_b (EVIDENCE for hypothesis H_F; exact identity, double FFT).
For X = 2^(b-m):  N(X,b) - |R_b| 2^-m = (1/2^b) sum_{xi != 0, v_2(xi) < m} S^(xi) conj(I^(xi))   (Theorem F1)
so |relative deviation| <= B_F(m) := 2^m/2^b * sum_{v_2(xi)<m} |mu_b^(xi)| |I^(xi)|.
Prints, per m, the actual relative deviation and B_F(m); B_F < 1 means the Fourier criterion certifies the count.
usage: python l1test.py SYS b mmax"""
import sys, os, subprocess, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys_, b, mm = map(int, sys.argv[1:4]); N = 1 << b
f = os.path.join(HERE, f"_l{sys_}.bin"); subprocess.run([f"{HERE}/rb", "bitmap", str(sys_), str(b), f], check=True)
bm = np.fromfile(f, dtype=np.uint8); os.remove(f); R = int(bm.sum())
S = np.fft.fft(bm.astype(np.float64))
xi = np.arange(N, dtype=np.int64)
v = np.zeros(N, dtype=np.int8); t = xi.copy(); t[0] = 1
for k in range(b):
    e = (t & 1) == 0; v[e] += 1; t[e] >>= 1
v[0] = b
print(f"sys {sys_} b {b} |R_b| {R}")
for m in range(1, mm + 1):
    K = N >> m; x = xi[(v < m)]
    s = np.sin(np.pi * x / N); Ih = np.abs(np.sin(np.pi * K * x / N) / s)   # |Dirichlet kernel|
    BF = (1 << m) * np.sum(np.abs(S[x]) * Ih) / N / R
    actual = int(bm[:K].sum()) / (R / (1 << m)) - 1
    print(f"  m={m:2d}  X=2^{b-m}  expected {R/(1<<m):10.1f}  observed {int(bm[:K].sum()):9d}  rel.dev {actual:+.4f}   B_F {BF:.4f}")
