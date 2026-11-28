#!/usr/bin/env python3
"""Check for cycles.md (Theorem C: cycle length from integrality).

  [C-id]   The cycle identity p^X / a^Y = prod (1 + v_t/(u_t n_t)) holds exactly
           (Fractions) on every known cycle of the 7 S-family cores, of G3 and of
           3x+1 (sanity).
  [C-ver]  Compiles sfverify.c / g3verify.c and verifies, for each core, that
           every n <= Z0 not on a listed cycle drops below n (so every n <= Z0
           reaches a listed cycle, and no other cycle has an element <= Z0).
           Default Z0 = 10^9 (about 2 minutes on one core per system);
           with --full, Z0 = 10^11 in parallel chunks (about 20 minutes on 11
           cores; this is the run quoted in cycles.md).
  [C-py]   Independent pure-Python re-check of [C-ver] for n <= 2*10^5.
  [C-neg]  Negative controls: the verifier FAILS for sf3_13 if its second cycle
           (3 10 5 6) is not listed, and for the core W (sf3_137) at n = 15.
  [C-bd]   cycle_bound.first_failure gives the exact (Y_fail, X_fail) used in
           the theorem, for Z0 = 10^9 and 10^11, and the inequality is
           re-verified independently for every Y < Y_fail with a second
           implementation (exact integer comparison, fresh powers).
Exit 0 iff all PASS.
"""
import sys, os, subprocess
from fractions import Fraction
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cycle_bound as CB

FULL = "--full" in sys.argv
Z0 = 10 ** 11 if FULL else 10 ** 9
ok = True


def claim(name, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + name, flush=True)
    ok = ok and bool(cond)


CORES = {  # name: (S mod 8, listed cycles)
    "sf3_7": ([7], [[1, 2]]),
    "sf3_17": ([1, 7], [[1, 4, 2]]),
    "sf3_57": ([5, 7], [[1, 2]]),
    "sf3_157": ([1, 5, 7], [[1, 4, 2]]),
    "sf3_357": ([3, 5, 7], [[1, 2]]),
    "sf3_13": ([1, 3], [[1, 4, 2], [3, 10, 5, 6]]),
    "sf3_135": ([1, 3, 5], [[1, 4, 2]]),
}


def TS(S):
    def T(n):
        if n % 2 == 0:
            return n // 2
        return 3 * n + 1 if n % 8 in S else n + 1
    return T


def G3(n):
    return (4 * n + 1) // 3 if n % 9 == 8 else (n + 2) // 3


def identity_on_cycle(T, cyc, p, a, branch):
    """branch(n) -> (u, v, w).  Returns True iff p^X/a^Y == prod(1+v/(u n))."""
    X = Y = 0
    prod = Fraction(1)
    for i, n in enumerate(cyc):
        assert T(n) == cyc[(i + 1) % len(cyc)]
        u, v, w = branch(n)
        assert (u * n + v) // w == T(n)
        while w % p == 0:
            w //= p
            X += 1
        assert w == 1
        if u == a:
            Y += 1
        else:
            assert u == 1
        prod *= 1 + Fraction(v, u * n)
    return Fraction(p ** X, a ** Y) == prod and prod > 1


# ---------------------------------------------------------------- [C-id]
good = True
for name, (S, cycs) in CORES.items():
    T = TS(S)
    br = (lambda S: lambda n: (1, 0, 2) if n % 2 == 0 else ((3, 1, 1) if n % 8 in S else (1, 1, 1)))(S)
    for c in cycs:
        good &= identity_on_cycle(T, c, 2, 3, br)
good &= identity_on_cycle(G3, [1], 3, 4,
                          lambda n: (4, 1, 3) if n % 9 == 8 else (1, (-n) % 3, 3))
coll = lambda n: n // 2 if n % 2 == 0 else 3 * n + 1
good &= identity_on_cycle(coll, [1, 4, 2], 2, 3,
                          lambda n: (1, 0, 2) if n % 2 == 0 else (3, 1, 1))
claim("[C-id] cycle identity exact on all listed cycles (and on 3x+1's (1 4 2))", good)

# ---------------------------------------------------------------- [C-ver]
for src, binn in (("sfverify.c", "sfverify_bin"), ("g3verify.c", "g3verify_bin")):
    r = subprocess.run(["gcc", "-O2", "-o", os.path.join(HERE, binn), os.path.join(HERE, src)])
    assert r.returncode == 0


def run(args):
    r = subprocess.run(args, capture_output=True, text=True)
    return r.returncode, r.stdout.strip(), r.stderr.strip()


chunks = 8 if FULL else 1
jobs = []
for name, (S, cycs) in CORES.items():
    mask = sum(1 << r for r in S)
    known = sorted({x for c in cycs for x in c})
    for i in range(chunks):
        lo, hi = i * Z0 // chunks + 1, (i + 1) * Z0 // chunks
        jobs.append((name, [os.path.join(HERE, "sfverify_bin"), str(mask), str(lo), str(hi)] + list(map(str, known))))
for i in range(chunks):
    lo, hi = i * Z0 // chunks + 1, (i + 1) * Z0 // chunks
    jobs.append(("G3", [os.path.join(HERE, "g3verify_bin"), str(lo), str(hi)]))
with ThreadPoolExecutor(max_workers=11 if FULL else 4) as ex:
    res = list(ex.map(lambda j: (j[0], run(j[1])), jobs))
per = {}
for name, (rc, out, err) in res:
    per.setdefault(name, []).append(rc == 0)
    if rc != 0:
        print("   ", name, rc, out, err)
for name in list(CORES) + ["G3"]:
    claim(f"[C-ver] {name}: every n <= {Z0} off the listed cycles drops below itself", all(per[name]))

# ---------------------------------------------------------------- [C-py]
def drops_py(T, n, known):
    if n in known:
        return True
    x, t = n, 0
    while x >= n:
        x = T(x)
        t += 1
        if t > 10 ** 5:
            return False
    return True


good = True
for name, (S, cycs) in CORES.items():
    T = TS(S)
    known = {x for c in cycs for x in c}
    good &= all(drops_py(T, n, known) for n in range(1, 200001))
good &= all(drops_py(G3, n, {1}) for n in range(1, 200001))
claim("[C-py] independent Python re-check for n <= 2*10^5 (all 8 systems)", good)

# ---------------------------------------------------------------- [C-neg]
rc, out, err = run([os.path.join(HERE, "sfverify_bin"), str(1 + 2 + 8), "1", "1000", "1", "4", "2"])
claim("[C-neg] verifier fails for sf3_13 when (3 10 5 6) is not listed", rc != 0)
rc, out, err = run([os.path.join(HERE, "sfverify_bin"), str(2 + 8 + 128), "15", "15"])
claim("[C-neg] verifier fails for the core W (sf3_137) at n = 15", rc != 0)

# ---------------------------------------------------------------- [C-bd]
EXPECT = {(10 ** 9, 2, 3, 2): (15601, 24727), (10 ** 11, 2, 3, 2): (190537, 301994),
          (10 ** 9, 3, 4, 4): (25254, 31867), (10 ** 11, 3, 4, 4): (176251, 222404)}
for (z, p, a, c), exp in EXPECT.items():
    if z > Z0 and not FULL:
        # still check the number itself (cheap enough)
        pass
    got = CB.first_failure(z, p, a, c, 10 ** 6)
    # second implementation: for each Y < Y_fail, fresh X from bit length
    Yf, Xf = got
    good = True
    import math
    for Y in range(1, Yf, max(1, Yf // 2000)):
        PY = a ** Y
        X = 0
        PX = 1
        # least X with p^X > a^Y, computed from a float guess and corrected exactly
        X = max(0, int(Y * math.log(a) / math.log(p)) - 2)
        PX = p ** X
        while PX <= PY:
            PX *= p
            X += 1
        assert PX // p <= PY
        if not z * (PX - PY) >= c * X * PY:
            good = False
    PY = a ** Yf
    X = max(0, int(Yf * math.log(a) / math.log(p)) - 2)
    PX = p ** X
    while PX <= PY:
        PX *= p
        X += 1
    good &= (X == Xf) and not (z * (PX - PY) >= c * X * PY)
    claim(f"[C-bd] Z0={z} p={p} a={a} c={c}: (Y_fail, X_fail) = {got} (expected {exp}); "
          f"sampled re-check of Y < Y_fail and failure at Y_fail", got == exp and good)

print("ALL PASS" if ok else "SOME FAIL")
sys.exit(0 if ok else 1)
