"""Exact checks for theory.md, Theorem A (sliding-window potentials).

[BIJ]  For u = 3, 5 and odd k <= 13: the closed walks of length k of the
       LSB-first "multiply by u" transducer (carry states 0..u-1) are in
       bijection with binary words x of length k, each with output word
       y = u x - c (2^k - 1), and x -> y is a permutation of [0, 2^k).
       (So the sum over all closed walks of [F(y) - F(x)] is 0 for every
       window weight f.)
[RANK] For u = 3, window width s <= 10, and u = 5, s <= 8: the linear map
       f -> (E_f(u h) - E_f(h))_{1 <= h < 2^(s+2)} on R^(2^s) has rank
       exactly 2^(s-1) (computed modulo the prime 2^31 - 1; rank mod p is a
       lower bound for the rank over Q).  The kernel contains the constants
       and the coboundaries, a space of dimension 2^(s-1); hence the kernel is
       exactly that space, i.e. E_f(u h) = E_f(h) for all h forces E_f = 0.
[ZERO] For random f in constants + coboundaries, E_f(h) = 0 exactly for
       h < 2^12 (sanity check of the definition of E).
Exits 0 iff all pass.  Runtime: about 5 s.
"""
import random
import numpy as np

ok = True


def claim(msg, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + msg, flush=True)
    ok = ok and bool(cond)


# ------------------------------------------------------------------ [BIJ]
def transducer_closed_walks(u, k):
    out = {}
    for x in range(2 ** k):
        bitsx = [(x >> i) & 1 for i in range(k)]
        for c0 in range(u):
            c, ybits = c0, []
            for b in bitsx:
                t = u * b + c
                ybits.append(t & 1)
                c = t >> 1
            if c == c0:
                y = sum(bb << i for i, bb in enumerate(ybits))
                assert y == u * x + c0 - c0 * 2 ** k   # u x + c = y + 2^k c
                out.setdefault(x, []).append((c0, y))
    return out


for u in (3, 5):
    good = True
    for k in range(1, 14, 2):
        cw = transducer_closed_walks(u, k)
        ys = [v[0][1] for v in cw.values()]
        good = good and len(cw) == 2 ** k and all(len(v) == 1 for v in cw.values()) \
            and sorted(ys) == list(range(2 ** k))
    claim(f"[BIJ] u = {u}: closed walks of the x{u} transducer <-> words, x -> y a permutation (odd k <= 13)", good)

# ------------------------------------------------------------------ [RANK]
P = 2 ** 31 - 1


def E_row(h, s):
    """Coefficient vector of E_f(h) = sum over windows touching h of (f(w) - f(0^s))."""
    row = np.zeros(2 ** s, dtype=np.int64)
    L = h.bit_length()
    for i in range(-(s - 1), L):
        w = 0
        for j in range(s):
            pos = i + j
            if pos >= 0 and (h >> pos) & 1:
                w |= 1 << j
        row[w] += 1
        row[0] -= 1
    return row


def rank_modp(Mx):
    M = Mx % P
    rows, cols = M.shape
    r = 0
    for c in range(cols):
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0:
            continue
        piv = r + nz[0]
        if piv != r:
            M[[r, piv]] = M[[piv, r]]
        inv = pow(int(M[r, c]), P - 2, P)
        M[r] = (M[r] * inv) % P
        others = np.nonzero(M[:, c])[0]
        others = others[others != r]
        if len(others):
            fac = M[others, c].reshape(-1, 1)
            M[others] = (M[others] - (fac * M[r]) % P) % P
        r += 1
        if r == rows:
            break
    return r


for u, smax in ((3, 10), (5, 8)):
    for s in range(1, smax + 1):
        H = 2 ** (s + 2)
        Mx = np.array([E_row(u * h, s) - E_row(h, s) for h in range(1, H)], dtype=np.int64)
        rk = rank_modp(Mx)
        claim(f"[RANK] u = {u}, s = {s}: rank {rk} = 2^(s-1) = {2 ** (s - 1)}", rk == 2 ** (s - 1))

# ------------------------------------------------------------------ [ZERO]
rnd = random.Random(7)
good = True
for s in (1, 3, 6):
    for _ in range(5):
        c = rnd.randint(-9, 9)
        pi = [rnd.randint(-9, 9) for _ in range(2 ** (s - 1))]
        f = [c + pi[w >> 1] - pi[w & (2 ** (s - 1) - 1)] if s > 1 else c for w in range(2 ** s)]
        for h in range(1, 2 ** 12, 7):
            row = E_row(h, s)
            good = good and int(sum(int(a) * b for a, b in zip(row, f))) == 0
claim("[ZERO] E_f = 0 for f = constant + coboundary (random samples)", good)

print("ALL PASS" if ok else "SOME CHECK FAILED")
raise SystemExit(0 if ok else 1)
