"""Theorem U'_G (every octave, exact constants) for a general system.

For every b >= L and m = 1..M:  |N(p^{b-m}, b) / (p^{b-m} P(b)) - 1|  <=  D'_{L,m},
D'_{L,m} = max over node states sigma (reachable states and the root), non-full super-level sets
S = {g_sigma >= gamma}, units w in <g mod p^L> and windows [c, c + p^{L-m}) of | #(wS cap window) p^m / |S| - 1 |.
Exact: the slopes g^a/p^e are ranked with Fractions; cw uprime does integer arithmetic only.

usage: python everyoct.py SYSTEM L M      -> prints "m num/den float" and appends to data/everyoct.txt
"""
import os, sys, subprocess, tempfile
from fractions import Fraction
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cwlib import System
from cert import gfun


def ranks(S, a, e):
    pairs = sorted(set(zip(a.tolist(), e.tolist())), key=lambda t: Fraction(S.g ** t[0], S.p ** t[1]))
    sl = [Fraction(S.g ** x, S.p ** y) for x, y in pairs]
    assert len(set(sl)) == len(sl) and all(v <= 1 for v in sl)
    lut = {pq: i for i, pq in enumerate(pairs)}
    key = a * 4096 + e
    ukeys = np.unique(key)
    m = {int(k): lut[(int(k) // 4096, int(k) % 4096)] for k in ukeys}
    out = np.empty(len(a), dtype=np.int32)
    for k, r in m.items():
        out[key == k] = r
    return out


def uprime(S, L, M):
    best = {m: Fraction(0) for m in range(1, M + 1)}
    states = sorted(set(S.states1) | {S.root})
    with tempfile.TemporaryDirectory(dir=os.environ.get("TMPDIR")) as tmp:
        for st in states:
            a, e = gfun(S, st, L)
            rk = ranks(S, a, e)
            if rk.max() == 0:
                continue          # only one level: the full set
            f = os.path.join(tmp, "rk.bin")
            rk.tofile(f)
            out = subprocess.run([os.path.join(HERE, "cw"), "uprime", f, str(S.p), str(L), str(S.g), str(M)],
                                 check=True, capture_output=True, text=True).stdout.split("\n")
            for line in out[1:]:
                if line.strip():
                    m, n, d = map(int, line.split())
                    best[m] = max(best[m], Fraction(n, d))
    return best


if __name__ == "__main__":
    name, L, M = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    S = System(name)
    best = uprime(S, L, M)
    with open(os.path.join(HERE, "data", "everyoct.txt"), "a") as fo:
        for m in range(1, M + 1):
            D = best[m]
            line = f"{name} L={L} m={m} D'={D.numerator}/{D.denominator} = {float(D):.6f}  (every b >= {L})"
            print(line, flush=True)
            fo.write(line + "\n")
