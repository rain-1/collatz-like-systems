"""Exact checks for theory.md, Theorem W and Corollaries W1, W2.

[TYPE]  each of the 8 cores (n-form), K7 (z-form) and 3x+1: an expanding
        periodic point x* lies in an SCC of G_K that is not a simple cycle
        (type (c)), checked with round3/accel/accel_lib.barrier_witness; and
        round3/dichotomy/decide.py returns OBST (n-forms and 3x+1).
[SHADOW] for x* and for the homoclinic periodic points y_d of C^d W: an explicit
        large integer n = y (mod 2^(N+kD)) with T^(kL)(n) = y + lam^k (n - y),
        T^(kL)(n) = n = y (mod 2^N) and T^(kL)(n) >= 2n, every intermediate
        point > n/4.  This is the configuration used in the proof of Theorem W.
[DENSE] Corollary W1 for K7 (z-form) and sf3_13: for random walks of length t
        inside the type-(c) SCC, an expanding periodic point that follows the
        walk (so it lies in the walk's cylinder), t = 10, 20, 40.
[MB]    mixedbase blocked system mb_s3_27: the cycle -5 -> -7 -> -10 has
        multiplier 9/8; the shadow identity holds on Z_2 x Z_3 cylinders; and a
        complete enumeration of branch words of length <= 12 lists every rational
        periodic point of period <= 12 in Z_(2) cap Z_(3), with multipliers.
Exits 0 iff every claim passes.  Runtime: about 45 s.
"""
import random
from fractions import Fraction
from itertools import product
import wplib as W

AL, DEC = W.AL, W.DEC
ok = True


def claim(msg, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + msg, flush=True)
    ok = ok and bool(cond)


def shadow_check(name, sysd, y, N=24, H=10 ** 9 + 7):
    p = sysd["p"]
    T = W.step_fn(sysd)
    L, lam, D, orb, parts = W.periodic_data(sysd, y)
    if lam <= 1:
        return None
    k = 1
    while lam ** k < 4:
        k += 1
    M = N + k * D
    n = W.padic_res(y, p, M) + p ** M * H
    x, mn = n, n
    for _ in range(k * L):
        x = T(x)
        mn = min(mn, x)
    good = (Fraction(x) == y + lam ** k * (n - y)
            and (x - n) % p ** N == 0 and W.padic_res(y, p, N) == n % p ** N
            and x >= 2 * n and 4 * mn > n)
    return good, L, lam, k


# ------------------------------------------------------------------ [TYPE]
for name, s in W.SYSTEMS.items():
    p, m, t = s["p"], s["m"], s["table"]
    C, lamC, Wk, rows = AL.barrier_witness(p, m, t, m, s["xstar"], dmax=40)
    exp_rows = [(d, y, lam) for d, y, lam in rows if lam > 1]
    d0 = min(d for d, _, _ in exp_rows)
    claim(f"[TYPE] {name}: x* = {s['xstar']} has residue cycle {C} (lam {lamC}) in a non-simple SCC of G_{m}; "
          f"closed walk W = {Wk}; y_d expanding for all d >= {d0} (d <= 40)",
          lamC > 1 and all(lam > 1 for d, _, lam in rows if d >= d0))
    s["rows"] = rows
    if s["domain"] == 1:
        res = DEC.decide(p ** m, t, want_cycles=False, want_depth=False)
        claim(f"[TYPE] {name}: decide.py verdict {res['verdict']}", res["verdict"] == "OBST")

# ------------------------------------------------------------------ [SHADOW]
for name, s in W.SYSTEMS.items():
    pts = [s["xstar"]] + [y for d, y, lam in s["rows"] if lam > 1][:6]
    res = [shadow_check(name, s, y) for y in pts]
    claim(f"[SHADOW] {name}: {len(pts)} expanding periodic points "
          f"{[str(y) for y in pts[:4]]}...: exact shadow identities, growth >= 2, N = 24",
          all(r is not None and r[0] for r in res))

# ------------------------------------------------------------------ [DENSE]
rnd = random.Random(2026)
for name in ["K7 z-form", "sf3_13 "[:-1]]:
    s = W.SYSTEMS[name]
    p, m, t = s["p"], s["m"], s["table"]
    E = AL.graph(p, m, t, m)
    C, _ = AL.orbit_residues(s["xstar"], p, m, t, m)
    comp = next(c for c in AL.tarjan(list(range(p ** m)), E) if C[0] in c)
    cs = set(comp)
    allgood = True
    for tlen in (10, 20, 40):
        for trial in range(5):
            walk = [rnd.choice(comp)]
            for _ in range(tlen):
                walk.append(rnd.choice([b for b, _ in E[walk[-1]] if b in cs]))
            back = AL.bfs_path(E, cs, walk[-1], C[0])
            fwd = AL.bfs_path(E, cs, C[0], walk[0])
            for d in range(0, 400):
                P = walk + back[1:] + (C[1:] + [C[0]]) * d + fwd[1:]
                closed = P[:-1]
                A, B = AL.compose_along(p, m, t, m, closed)
                if A > 1:
                    break
            y, lam = AL.walk_point(p, m, t, m, closed)   # asserts: y follows `closed`
            allgood = allgood and lam > 1 and AL.padic_residue(y, p, m) == walk[0]
    claim(f"[DENSE] {name}: every sampled walk of length 10/20/40 in the type-(c) SCC is followed by "
          f"an expanding rational periodic point", allgood)

# ------------------------------------------------------------------ [MB]
y, lam, orb = Fraction(-5), Fraction(1), []
x = y
for _ in range(3):
    orb.append(x)
    x, q = W.mb_rat_step(x)
    lam *= q
claim(f"[MB] mb_s3_27: -5 -> -7 -> -10 -> -5 with multiplier {lam}", x == y and lam == Fraction(9, 8) and orb == [-5, -7, -10])
N = 20
allg = True
for k in (1, 2, 5, 10):
    Mod = 2 ** (N + 3 * k) * 3 ** N
    n = (-5) % Mod + Mod * (10 ** 6 + 3)
    z = n
    for _ in range(3 * k):
        z = W.mb_s3_27(z)
    allg = allg and Fraction(z) == -5 + Fraction(9, 8) ** k * (n + 5) and (z + 5) % (2 ** N * 3 ** N) == 0
claim("[MB] mb_s3_27: n = -5 (mod 2^(N+3k) 3^N) gives T^(3k) n + 5 = (9/8)^k (n + 5), still = -5 mod 6^N", allg)

BR = {"A": (Fraction(1), Fraction(1), Fraction(27)), "E": (Fraction(1), Fraction(0), Fraction(2)),
      "O": (Fraction(3), Fraction(1), Fraction(2))}
found = {}
for Lw in range(1, 13):
    for word in product("AEO", repeat=Lw):
        A, B = Fraction(1), Fraction(0)
        for b in word:
            u, v, w = BR[b]
            A, B = A * u / w, (u * B + v) / w
        if A == 1:
            continue
        xf = B / (1 - A)
        if xf.denominator % 2 == 0 or xf.denominator % 3 == 0:
            continue
        z, okw = xf, True
        for b in word:
            z2, q = W.mb_rat_step(z)
            u, v, w = BR[b]
            if z2 != (u * z + v) / w:
                okw = False
                break
            z = z2
        if okw and z == xf:
            orbit = [xf]
            z = xf
            for _ in range(Lw - 1):
                z = W.mb_rat_step(z)[0]
                orbit.append(z)
            key = min(orbit)
            per = len(set(orbit))
            if key not in found:
                found[key] = (per, A ** (per) if False else None, word)
# multipliers per primitive period
rows = []
for key, (per, _, word) in sorted(found.items()):
    z, lamz = key, Fraction(1)
    for _ in range(per):
        z, q = W.mb_rat_step(z)
        lamz *= q
    rows.append((key, per, lamz))
expanding = [(str(k), per, str(l)) for k, per, l in rows if l > 1]
print("  number of periodic orbits found:", len(rows))
claim(f"[MB] mb_s3_27: rational periodic orbits of period <= 12 in Z_(2) cap Z_(3): {len(rows)}; expanding: {expanding}",
      len(rows) == 16274
      and sorted(expanding) == sorted([('-10138/139', 11, '2187/2048'), ('-10', 3, '9/8')]))


# homoclinic expanding points of mb_s3_27: words (OOE)^d w, |w| <= 4
def mb_word_point(word):
    A, B = Fraction(1), Fraction(0)
    for b in word:
        u, v, w = BR[b]
        A, B = A * u / w, (u * B + v) / w
    if A == 1:
        return None
    xf = B / (1 - A)
    if xf.denominator % 2 == 0 or xf.denominator % 3 == 0:
        return None
    z = xf
    for b in word:
        u, v, w = BR[b]
        if W.mb_rat_step(z)[0] != (u * z + v) / w:
            return None
        z = (u * z + v) / w
    return (xf, A) if z == xf else None


hom = []
for d in (10, 20, 40):
    for Lw in range(1, 5):
        hit = None
        for wd in product("AEO", repeat=Lw):
            r = mb_word_point("OOE" * d + "".join(wd))
            if r and r[1] > 1 and r[0] not in (-5, -7, -10):
                hit = ("".join(wd), r)
                break
        if hit:
            break
    if hit is None:
        hom.append((d, None))
        continue
    wd, (y, lam) = hit
    word = "OOE" * d + wd
    a2 = sum(1 for b in word if b in "EO")          # divisions by 2
    a3 = sum(1 for b in word if b == "A")           # divisions by 27
    Nn, k = 15, 1
    while lam ** k < 4:
        k += 1
    Mod = 2 ** (Nn + k * a2) * 3 ** (Nn + 3 * k * a3)
    n = W.padic_res(y, 2, Nn + k * a2)
    # CRT with the 3-adic residue
    r3 = W.padic_res(y, 3, Nn + 3 * k * a3)
    m2, m3 = 2 ** (Nn + k * a2), 3 ** (Nn + 3 * k * a3)
    n = (n * m3 * pow(m3, -1, m2) + r3 * m2 * pow(m2, -1, m3)) % Mod + Mod * 1000003
    z = n
    for _ in range(k * len(word)):
        z = W.mb_s3_27(z)
    good = (Fraction(z) == y + lam ** k * (n - y) and z >= 2 * n
            and (Fraction(z) - y).numerator % 2 ** Nn == 0 and W.padic_res(y, 2, 3 * d) == (-5) % 2 ** (3 * d))
    hom.append((d, wd, good))
claim(f"[MB] mb_s3_27 homoclinic: for d = 10, 20, 40 an expanding rational periodic point following (-5,-7,-10)^d "
      f"then a short word; exact shadow identity on an integer progression: {hom}",
      all(len(h) == 3 and h[2] for h in hom))

print("ALL PASS" if ok else "SOME CHECK FAILED")
raise SystemExit(0 if ok else 1)
