"""Fourier coefficients of mu_b = uniform measure on {r/2^b : r in R_b} (EVIDENCE; numpy FFT, double).

usage: python spectrum.py SYS b
Prints, per 2-adic level j = b - v_2(xi) of the frequency xi (mod 2^b):
  max |mu_b^(xi)| over that level, the arg max, and the Parseval floor |R_j|^{-1/2};
the same for a uniformly random subset of the same size (baseline);
the low Archimedean frequencies 1 <= xi <= 8 and the largest |mu^| among odd xi <= 2^12;
for the 12 largest coefficients at levels j >= b/2: the best rational approximation a/q (q <= 64) of xi/2^b.
"""
import sys, os, subprocess, numpy as np
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = {0: "split5_3", 1: "3x+1", 2: "K7"}

def bitmap(sys_, b):
    f = os.path.join(HERE, f"_bm_{sys_}_{b}.bin")
    subprocess.run([f"{HERE}/rb", "bitmap", str(sys_), str(b), f], check=True)
    a = np.fromfile(f, dtype=np.uint8); os.remove(f); return a

def val2(N, b):
    x = np.arange(N, dtype=np.int64); v = np.zeros(N, dtype=np.int64); v[0] = b
    t = x.copy(); m = t != 0
    for k in range(b):
        e = m & ((t >> k) & 1 == 0) & (v == k)
        v[e] += 1
    return v

def main():
    sys_, b = int(sys.argv[1]), int(sys.argv[2]); N = 1 << b
    bm = bitmap(sys_, b).astype(np.float64); R = int(bm.sum())
    F = np.abs(np.fft.fft(bm)) / R
    rng = np.random.default_rng(1)
    rnd = np.zeros(N); rnd[rng.choice(N, R, replace=False)] = 1.0
    G = np.abs(np.fft.fft(rnd)) / R
    v = val2(N, b)
    sizes = {}
    for j in range(1, b + 1):
        sizes[j] = int(subprocess.run([f"{HERE}/rb", "count", str(sys_), str(j), "1"], capture_output=True,
                                      text=True, check=True).stdout.split()[0])
    print(f"{NAMES[sys_]}  b={b}  |R_b|={R}  P(b)={R/N:.3e}")
    print(" level j  max|mu^|   argmax xi      floor|R_j|^-1/2   random-set max")
    for j in range(1, b + 1):
        idx = np.nonzero(v == b - j)[0]
        k = idx[np.argmax(F[idx])]
        print(f"  {j:3d}   {F[k]:.5f}   {k:>10d}     {sizes[j]**-0.5:.5f}         {G[idx].max():.5f}")
    print(" low frequencies xi=1..8:", " ".join(f"{F[x]:.4f}" for x in range(1, 9)))
    odd = np.arange(1, 1 << 12, 2)
    print(f" max over odd xi < 2^12: {F[odd].max():.5f} at xi={odd[np.argmax(F[odd])]};  random: {G[odd].max():.5f};"
          f"  R^-1/2 = {R**-0.5:.5f}")
    hi = np.nonzero(v <= b // 2)[0]
    top = hi[np.argsort(-F[hi])[:12]]
    print(" largest coefficients at levels j >= b/2 (xi, level, |mu^|, best a/q with q<=64, |xi/2^b - a/q|*2^b):")
    for x in top:
        xs = min(x, N - x)
        fr = Fraction(int(xs), N).limit_denominator(64)
        print(f"   xi={xs:>10d} j={b - v[x]:2d} |mu^|={F[x]:.5f}  a/q={fr}  dist*2^b={abs(xs - fr * N):.1f}")

if __name__ == "__main__":
    main()
