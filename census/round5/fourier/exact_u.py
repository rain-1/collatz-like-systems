"""Exact constants D'_{L,m,k} of Theorem U' (README, "Revision after REFEREE1", section R-B).

For system SYS and depth L: for every stuck node state sigma (as in fourier_bound.py), rb gfun gives per z < 2^L
the pair (U, h) attaining the minimum prefix slope g_sigma(z) = U / 2^h.  The distinct slopes are sorted
EXACTLY (Fractions), turned into integer ranks, and exactD (C, integer arithmetic only) computes

    D'_{L,m,k} = max over states sigma, allowed sets S = {g_sigma >= gamma} (not the full set),
                 units u in G, shifts c of  | #{t < k 2^{L-m} : u t + c mod 2^L in S} / (|S| k 2^{-m}) - 1 |

as an exact rational, for G = <u0 mod 2^L> (u0 = the system's multiplier: the only units that occur) and,
for comparison, G = all odd units (the referee's version).  No floating point enters the constants.

usage: python exact_u.py SYS L M [all]    (SYS: 0 split5_3, 1 3x+1, 2 K7)
prints one line per (m, k), m = 1..M, k odd or k = 1 (k even reduces to a smaller m), as "m k num/den float".
"""
import sys, os, subprocess, tempfile
from fractions import Fraction
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
STATES = {0: [(0, 0), (1, 1)], 1: [(0, 0)], 2: [(0, 0), (1, 1)]}
GEN = {0: 5, 1: 3, 2: 3}

def gfun(sys_, L, s, c0, tmp):
    f = os.path.join(tmp, f"gf_{sys_}_{L}_{s}_{c0}.bin")
    subprocess.run([f"{HERE}/rb", "gfun", str(sys_), str(L), str(s), str(c0), f], check=True)
    N = 1 << L; raw = open(f, "rb").read(); os.remove(f)
    return np.frombuffer(raw[:8 * N], dtype=np.uint64), np.frombuffer(raw[8 * N:], dtype=np.int32)

def ranks(U, h):
    pairs = sorted({(int(a), int(b)) for a, b in zip(U.tolist(), h.tolist())}, key=lambda p: Fraction(p[0], 1 << p[1]))
    sl = [Fraction(a, 1 << b) for a, b in pairs]
    assert len(set(sl)) == len(sl) and all(s <= 1 for s in sl) and sl[-1] == 1
    idx = {p: i for i, p in enumerate(pairs)}
    return np.array([idx[(int(a), int(b))] for a, b in zip(U.tolist(), h.tolist())], dtype=np.int32)

def exact_D(sys_, L, M, gen):
    best = {}
    with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as tmp:
        for (s, c0) in STATES[sys_]:
            U, h = gfun(sys_, L, s, c0, tmp)
            rk = ranks(U, h); f = os.path.join(tmp, "rk.bin"); rk.tofile(f)
            out = subprocess.run([f"{HERE}/exactD", f, str(L), str(M), str(gen)], check=True,
                                 capture_output=True, text=True).stdout.split("\n")
            for line in out[1:]:
                if not line.strip(): continue
                k, num, den = map(int, line.split()[:3])
                best[k] = max(best.get(k, Fraction(0)), Fraction(num, den))
    return best   # keyed by k over the grid 2^{-M}

if __name__ == "__main__":
    sys_, L, M = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    gen = 0 if (len(sys.argv) > 4 and sys.argv[4] == "all") else GEN[sys_]
    best = exact_D(sys_, L, M, gen)
    print(f"sys {sys_} L {L} M {M} units {'all odd' if gen == 0 else f'<{gen}>'}")
    for m in range(1, M + 1):
        for kk in range(1, 1 << m):
            if kk % 2 == 0: continue
            K = kk << (M - m); D = best[K]
            print(f"m {m} k {kk} D' = {D.numerator}/{D.denominator} = {float(D):.6f}")
