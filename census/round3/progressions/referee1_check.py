"""Independent referee check (REFEREE #1) for the progressions lens.

Written from scratch: the raw maps are re-implemented here from the census rule strings, the
finite-level invariant is recomputed by a different method (weak components of the residue
transition graph modulo M, which is the finest T-invariant function of n mod M by definition),
ancestor trees are built with an independent inverse, and Theorem C certificates are re-verified
by an exact verifier written here.  The prover's code is imported ONLY (a) to read off the
claimed invariant g and the claimed certificates (the objects under test) and (b) to produce
constructions that are then replayed with the referee's own maps.

Exact integer / Fraction arithmetic in every check that supports a verdict.  Sections marked
EVIDENCE are simulations.  Exits 0 iff every check behaves as stated in REFEREE1.md (including the
expected detection of the Theorem C gap, which is asserted, not ignored).

Run: nice python3 referee1_check.py      (about 3-6 minutes)
"""

import math
import time
T0 = time.time()
import os
import random
import signal
import sys
from collections import deque
from fractions import Fraction as Fr
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

FAIL = []
rng = random.Random(9137)


def ok(c, m):
    if not c:
        FAIL.append(m)
        print("FAIL:", m, flush=True)


def vp(n, q):
    n, k = abs(n), 0
    if n == 0:
        return 10 ** 9
    while n % q == 0:
        n //= q
        k += 1
    return k


# =====================================================================================
# 1. Raw maps re-implemented from the census rule strings, and my own shortcut tables
# =====================================================================================
S0 = {1, 3, 5, 7, 11, 13, 15, 17, 21, 23, 25, 29}


def raw_parity(a, d):
    return lambda n: n // 2 if n % 2 == 0 else a * n + d


def raw_split(a, b, d):
    return lambda n: n // 2 if n % 2 == 0 else (a * n + d if n % 4 == 1 else b * n + d)


def raw_m3(a, c1, b, c2, div=False):
    # div=True: rule already divides by 3 (m3_a, m3_b)
    def f(n):
        if n % 3 == 0:
            return n // 3
        x = a * n + c1 if n % 3 == 1 else b * n + c2
        return x // 3 if div else x
    return f


def raw_s32(d, S):
    return lambda n: n // 2 if n % 2 == 0 else (3 * n + d if n % 32 in S else n + d)


RAW = {
    "m3_a": (raw_m3(2, 1, 2, 2, True), 3),
    "m3_c": (raw_m3(2, 1, 2, 2), 3),
    "desc_s32_d65": (raw_s32(65, S0), 2),
    "qrB7_c53": (lambda n: n // 2 if n % 2 == 0 else ((n + 35) // 2 if n % 4 == 1 else (n + 21) // 2), 2),
    "par_1_5": (raw_parity(1, 5), 2),
    "split5_1": (raw_split(5, 1, 1), 2),
    "split5_3": (raw_split(5, 1, 3), 2),
    "desc_split7_1": (raw_split(7, 1, 1), 2),
    "desc_s32_plus9": (raw_s32(1, S0 | {9}), 2),
    "m3_b": (raw_m3(4, -1, 4, 1, True), 3),
    "m3_d": (raw_m3(4, 2, 4, 1), 3),
    "m3_e": (raw_m3(7, 2, 7, 1), 3),
    "m3_g": (raw_m3(5, 1, 5, 2), 3),
    "desc_m3_4n5": (raw_m3(4, 5, 2, 2), 3),
    "perm_1932": (lambda n: 2 * (n // 3) if n % 3 == 0 else (4 * (n // 3) + 1 if n % 3 == 1 else 4 * (n // 3) + 3), 3),
}
for d in (5, 13, 73, 97, 7081):
    RAW[f"split_{d}"] = (raw_split(3, 1, d), 2)
for d in (7, 71):
    RAW[f"splitB_{d}"] = (raw_split(1, 3, d), 2)
for a, d in [(3, 1), (3, -1), (3, 5), (3, 7), (3, 13), (3, 17), (5, 1), (5, 3), (5, 5), (5, 7),
             (5, 11), (7, 1), (7, 7), (9, 1), (3, 3), (3, 9)]:
    RAW[f"par_{a}_{'m' if d < 0 else ''}{abs(d)}"] = (raw_parity(a, d), 2)


class Short:
    """Referee's own shortcut map: built from the raw map by sampling the branch affine maps."""

    def __init__(self, name, raw, p):
        self.name, self.raw, self.p = name, raw, p

    def T(self, n):
        x = self.raw(n)
        if n % self.p != 0 and x % self.p == 0 and self.name not in ("m3_a", "m3_b", "qrB7_c53", "perm_1932"):
            return x // self.p
        return x


import systems as PSYS   # prover's systems (objects under test)
import construct as PCON  # prover's construction (output replayed with the referee's maps)

MINE = {sid: Short(sid, *RAW[sid]) for sid in RAW}

# 1a. the prover's p-shift tables equal the referee's shortcut of the raw census rule
for e in PSYS.SYSTEMS:
    sid = e["id"]
    ok(sid in MINE, f"referee has a raw map for {sid}")
    S = e["sys"]
    M = MINE[sid]
    bad = 0
    for n in list(range(1, 5000)) + [rng.randrange(1, 10 ** 40) for _ in range(2000)]:
        if S.T(n) != M.T(n):
            bad += 1
    ok(bad == 0, f"prover table == referee shortcut of raw rule ({sid}), {bad} mismatches")
    # shortcut lemma: S(n) in {R(n), R(R(n))}
    R = RAW[sid][0]
    for n in range(1, 3000):
        s = S.T(n)
        ok(s == R(n) or s == R(R(n)), f"shortcut lemma {sid} {n}")
print("1. prover maps agree with referee re-implementations of the census rules", flush=True)

# 1b. cross-check the referee raw maps with the census/round-2 code where available
import importlib.util


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


CEN = load(os.path.join(HERE, "..", "..", "systems.py"), "cen_sys")
R2D = load(os.path.join(HERE, "..", "..", "round2", "descent", "systems.py"), "r2d_sys")
R2Q = load(os.path.join(HERE, "..", "..", "round2", "qr", "systems.py"), "r2q_sys")
PAIRS = [("m3_a", CEN, "m3_a_s100"), ("m3_c", CEN, "m3_c_s100"), ("m3_b", CEN, "m3_b_s8"),
         ("m3_d", CEN, "m3_d_s7"), ("m3_e", CEN, "m3_e_s7"), ("m3_g", CEN, "m3_g_s7"),
         ("split_7081", CEN, "split_7081_s27"), ("split_97", CEN, "split_97_s27"),
         ("splitB_7", CEN, "splitB_7_s27"), ("split5_3", CEN, "split5_3_s27"),
         ("par_5_11", CEN, "par_5_11_s27"), ("par_3_m1", CEN, "par_3_m1_s27"),
         ("perm_1932", CEN, "perm_1932_s8"),
         ("desc_s32_d65", R2D, "desc_s32_d65"), ("desc_s32_plus9", R2D, "desc_s32_plus9"),
         ("desc_split7_1", R2D, "desc_split7_1"), ("desc_m3_4n5", R2D, "desc_m3_4n5"),
         ("qrB7_c53", R2Q, "qrB7_c53")]
for sid, mod, cid in PAIRS:
    try:
        step = mod.get(cid)["step"]
    except Exception as ex:  # id missing in that file
        ok(False, f"census id {cid} not found: {ex}")
        continue
    R = RAW[sid][0]
    ok(all(step(n) == R(n) for n in range(1, 20000)), f"raw rule {sid} vs census {cid}")
print("1b. referee raw maps agree with census code", flush=True)


# =====================================================================================
# 2. Independent finite-level invariant: weak components of the residue graph mod M
# =====================================================================================
def residue_components(T, p, pk, M):
    """Weak components of the graph on Z/M with edges (n mod M) -> (T(n) mod M); n runs over a
    complete residue system modulo lcm(p^kappa, p*M) (T(n) mod M depends only on that)."""
    L = pk * p * M // gcd(pk, p * M)
    parent = list(range(M))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    out_edges = [set() for _ in range(M)]
    for n in range(L, 2 * L):
        a, b = n % M, T(n) % M
        out_edges[a].add(b)
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    comp = [find(a) for a in range(M)]
    return comp, out_edges


def strongly_closed(comp, out_edges, M):
    """True iff every weak component is strongly connected (reachability symmetric)."""
    for a in range(M):
        seen = {a}
        st = [a]
        while st:
            x = st.pop()
            for y in out_edges[x]:
                if y not in seen:
                    seen.add(y)
                    st.append(y)
        if any(comp[y] == comp[a] and y not in seen for y in range(M)):
            return False
    return True


def partition(labels):
    blocks = {}
    for i, l in enumerate(labels):
        blocks.setdefault(l, []).append(i)
    return sorted(tuple(b) for b in blocks.values())


ninv = 0
nstrong = [0]
for e in PSYS.SYSTEMS:
    sid = e["id"]
    S = e["sys"]
    if sid in ("perm_1932", "par_3_3", "par_3_9", "par_5_5", "par_7_7"):
        continue
    info = PCON.prepare(S)
    dstar = info["dstar"]
    base = S.S * dstar
    Ms = {base, base * S.p, base * S.p ** 2}
    for l in S.U:
        Ms |= {base * l, base * l * l}
    for q in (7, 11, 13):
        if base * q <= 60000:
            Ms.add(base * q)
    for M in sorted(Ms):
        if M > 120000 or M * S.P > 4 * 10 ** 6:
            continue
        comp, oe = residue_components(MINE[sid].T, S.p, S.P, M)
        claimed = [PCON.g(S, info, z if z > 0 else M) for z in range(M)]
        ok(partition(comp) == partition(claimed),
           f"finite-level invariant mod {M} of {sid}: {len(set(comp))} components vs {len(set(claimed))} g-classes")
        if M <= 3000 and all(M % q for q in S.bad):
            # Lemma 4(a) is a statement about GOOD moduli only (mod a prime of U, residues
            # divisible by it are transient, e.g. 3x+1 mod 3), so test strong connectivity there.
            ok(strongly_closed(comp, oe, M), f"weak components strongly connected {sid} mod {M}")
            nstrong[0] += 1
        ninv += 1
print(f"2. residue-graph components = claimed g-classes in {ninv} (system, M) pairs; "
      f"strong connectivity at {nstrong[0]} good moduli", flush=True)
ok(nstrong[0] >= 30, "enough good moduli for strong connectivity")

# 2b. the specific invariants quoted in the text
def classes_of(sid):
    S = PSYS.get(sid)["sys"]
    info = PCON.prepare(S)
    return S, info


S, info = classes_of("desc_s32_d65")
ok(info["dstar"] == 65, "d65 d* = 65")
for n in range(1, 20000):
    for m in range(1, 200):
        if gcd(n, 65) == gcd(m, 65):
            ok(PCON.g(S, info, n) == PCON.g(S, info, m), "d65: g = gcd(n,65)")
            break
gvals = {}
for n in range(1, 66 * 4):
    gvals.setdefault(gcd(n, 65), set()).add(PCON.g(S, info, n))
ok(all(len(v) == 1 for v in gvals.values()) and len({min(v) for v in gvals.values()}) == 4,
   "d65 invariant is exactly gcd(n,65) (4 classes)")
for sid, dd in [("par_3_5", 5), ("par_3_13", 13), ("par_3_17", 17), ("par_5_3", 3), ("par_5_7", 7),
                ("par_5_11", 11), ("split5_3", 3)]:
    S, info = classes_of(sid)
    ok(info["dstar"] == dd and len({PCON.g(S, info, n) for n in range(1, 4 * dd)}) == 2,
       f"{sid}: invariant is divisibility by {dd}")
for sid in ["m3_a", "par_3_1", "par_3_m1", "par_5_1", "par_7_1", "par_9_1", "split5_1", "desc_split7_1",
            "desc_s32_plus9", "m3_b", "m3_d", "m3_e", "m3_g", "desc_m3_4n5"]:
    S, info = classes_of(sid)
    ok(len({PCON.g(S, info, n) for n in range(1, 500)}) == 1, f"{sid}: trivial invariant")
S, info = classes_of("qrB7_c53")
sq = {1, 2, 4}
ok(all((PCON.g(S, info, n) == PCON.g(S, info, 1)) == (n % 7 in sq) for n in range(1, 2000)),
   "qrB7_c53: square class mod 7")
print("2b. quoted invariants confirmed", flush=True)


# =====================================================================================
# 3. Cycles and their classes (referee maps)
# =====================================================================================
def cyc(T, c, lim=10 ** 5):
    x, out = c, []
    for _ in range(lim):
        out.append(x)
        x = T(x)
        if x == c:
            return out
    return None


SHARED = {"desc_s32_d65": [[1, 7], [5, 1135], [13, 39, 299]], "m3_a": [[1, 2]], "par_5_1": [[1, 13, 17]],
          "par_3_m1": [[1, 5, 17]], "par_3_17": [[1, 23]], "split5_1": [[1, 13]], "m3_d": [[1, 7]],
          "m3_e": [[1, 4]], "m3_g": [[4, 8]], "desc_m3_4n5": [[1, 2, 16]], "par_5_3": [[3, 39, 51], [1, 43, 53, 61]],
          "par_5_7": [[7, 91, 119], [1, 9, 57]], "par_5_11": [[11, 143, 187], [1, 141]],
          "split_13": [[1, 5]], "split_7081": [[569, 713]], "par_3_5": [[1, 19, 23, 187, 347]],
          "par_3_13": [[1, 131, 211, 227, 251, 259, 283, 287, 319]]}
for sid, groups in SHARED.items():
    S, info = classes_of(sid)
    T = MINE[sid].T
    for grp in groups:
        cs = [cyc(T, c) for c in grp]
        ok(all(c is not None for c in cs), f"{sid}: listed points are periodic")
        ok(len({min(c) for c in cs}) == len(grp), f"{sid}: listed cycles distinct")
        ok(len({PCON.g(S, info, c) for c in grp}) == 1, f"{sid}: cycles {grp} share a class")
        # an expanding lap exists (numerator product > 1)
    # expanding cycle for Theorem B
    c0 = groups[0][0]
    cy = cyc(S.T, c0)
    a = 1
    for x in cy:
        a *= S.table[x % S.P][0]
    if sid not in ():
        ok(a > 1 or any(math.prod(S.table[x % S.P][0] for x in cyc(S.T, g2[0])) > 1 for g2 in groups),
           f"{sid}: expanding cycle present")
# m3_e: the 14-cycle through 4 in the raw map; {1, 9, 3}
ok(sorted(cyc(RAW["m3_e"][0], 1)) == [1, 3, 9], "m3_e raw cycle {1,9,3}")
ok(len(cyc(RAW["m3_e"][0], 4)) == 14, "m3_e raw 14-cycle through 4")
ok(sorted(cyc(RAW["m3_c"][0], 1)) == [1, 3] and sorted(cyc(RAW["m3_c"][0], 2)) == [2, 6], "m3_c raw cycles")
print("3. shared-class cycle data confirmed with referee maps", flush=True)

# 3b. lap identity T^L(c + mu p^L j) = c + mu a j (Theorem B, case k0 = p), referee maps
for sid, groups in SHARED.items():
    S = PSYS.get(sid)["sys"]
    T = MINE[sid].T
    for grp in groups:
        for c in grp:
            cy = cyc(S.T, c)
            L = len(cy)
            a = math.prod(S.table[x % S.P][0] for x in cy)
            if a == 1:
                continue
            mu = S.S
            for j in list(range(0, 50)) + [rng.randrange(1, 10 ** 25) for _ in range(50)]:
                z = c + mu * S.p ** L * j
                for _ in range(L):
                    z = T(z)
                ok(z == c + mu * a * j, f"lap identity {sid} c={c} j={j}")
print("3b. lap identities verified with referee maps", flush=True)


# =====================================================================================
# 4. Theorem A on fresh inputs: constructions replayed with the referee's maps
# =====================================================================================
def _alarm(*a):
    raise TimeoutError


signal.signal(signal.SIGALRM, _alarm)
FRESH_N = [2 ** 11, 3 ** 6, 5 ** 4, 7 ** 3, 11 * 13, 2 ** 5 * 3 ** 3 * 5 ** 2 * 11, 1001, 17 * 19, 4096 * 5,
           3 ** 4 * 7 ** 2, 2 ** 3 * 23, 31 * 32]
done, skipped = 0, 0
for e in PSYS.SYSTEMS:
    sid = e["id"]
    if sid in ("perm_1932", "par_3_3", "par_3_9", "par_5_5", "par_7_7"):
        continue
    S = e["sys"]
    info = PCON.prepare(S)
    T = MINE[sid].T
    for trial in range(4):
        y = rng.choice([rng.randrange(1, 10 ** 9), rng.choice(e["cycles"] or [1])])
        N = rng.choice(FRESH_N)
        x = None
        for _ in range(10000):
            xx = rng.randrange(1, 10 ** 7)
            if PCON.g(S, info, xx) == PCON.g(S, info, y):
                x = xx
                break
        if x is None:
            continue
        signal.alarm(4)
        try:
            n, data = PCON.construct(S, info, y, x, N)
            signal.alarm(0)
            # replay with the referee map: n = x mod N, and the forward orbits of n and y meet
            ok(n > 0 and (n - x) % N == 0, f"A: congruence {sid}")
            if data["steps_to_y0"] > 30000 or n.bit_length() > 100000:
                skipped += 1      # replay too long for the time budget (counted as skipped)
                continue
            signal.alarm(20)
            z = n
            for _ in range(data["steps_to_y0"]):
                z = T(z)
            w = y
            for _ in range(data["k0"]):
                w = T(w)
            ok(z == w, f"A: n merges with y ({sid}, y={y}, x={x}, N={N})")
            done += 1
        except TimeoutError:
            skipped += 1
        except AssertionError as ex:
            ok(False, f"A: construction failed {sid} y={y} x={x} N={N}: {ex}")
        finally:
            signal.alarm(0)
print(f"   [time {time.time()-T0:.0f}s]")
print(f"4. Theorem A constructions on fresh moduli replayed with referee maps: {done} ok, {skipped} timeouts", flush=True)
ok(done >= 40, "enough fresh constructions")


# =====================================================================================
# 5. EVIDENCE: independent inverse trees hit every compatible class mod fresh N
# =====================================================================================
def preimages(S, z):
    """All n >= 1 with T(n) = z, computed from the referee's map by solving u n + v = p z on each
    residue class (the coefficients (u, v) are read off from two evaluations of the referee map)."""
    if S.name not in _AFF:
        lst = []
        for r in range(S.P):
            n1 = r if r > 0 else S.P
            n2 = n1 + S.P
            t1, t2 = MINE[S.name].T(n1), MINE[S.name].T(n2)
            # T(n) = (A n + B)/S.P on the class: A = t2 - t1, B = S.P*t1 - A*n1
            A_ = t2 - t1
            B_ = S.P * t1 - A_ * n1
            lst.append((r, A_, B_))
        _AFF[S.name] = lst
    out = []
    for (r, A_, B_) in _AFF[S.name]:
        num = S.P * z - B_
        if num % A_ == 0:
            n = num // A_
            if n > 0 and n % S.P == r:
                out.append(n)
    return out


_AFF = {}


nev = 0
for sid, groups in [("desc_s32_d65", [[1, 7], [5, 1135], [13, 39, 299]]), ("m3_a", [[1, 2]]),
                    ("m3_e", [[1, 4]]), ("par_5_1", [[1, 13, 17]]), ("split5_1", [[1, 13]]),
                    ("par_3_m1", [[1, 5, 17]]), ("split_13", [[1, 5]])]:
    S, info = classes_of(sid)
    T = MINE[sid].T
    for grp in groups:
        for c in grp:
            cyset = set(cyc(T, c))
            B = 10 ** 9
            seen = set(cyset)
            dq = deque(cyset)
            while dq and len(seen) < 60000:
                z = dq.popleft()
                for n in preimages(S, z):
                    if n <= B and n not in seen:
                        seen.add(n)
                        dq.append(n)
            for N in (11, 16, 27, 32, 49):
                want = {r for r in range(N) for k in range(1, 400) if PCON.g(S, info, r + N * k) == PCON.g(S, info, c)}
                got = {n % N for n in seen}
                ok(want <= got, f"EVIDENCE {sid} basin of {c} misses compatible classes mod {N}: {sorted(want - got)[:5]}")
                ok(all(PCON.g(S, info, n) == PCON.g(S, info, c) for n in list(seen)[:3000]), f"basin inside class {sid}")
                nev += 1
print(f"   [time {time.time()-T0:.0f}s]")
print(f"5. EVIDENCE: {nev} (basin, N) pairs: every compatible class mod N hit by the ancestor tree", flush=True)


# =====================================================================================
# 6. Adversarial: random p-shift maps.  If Theorem A's hypotheses are certified, the residue
#    graph components mod M must coincide with the computed g (else Theorem A is wrong), and
#    the construction must succeed.
# =====================================================================================
import plib as PLIB
from certify import certify as PCERT

ntested, napplies = 0, 0
ncert_to = [0]
nrv = [0]
for trial in range(150):
    p = rng.choice([2, 2, 3, 5])
    kappa = rng.choice([1, 1, 2])
    if p == 5 and kappa == 2:
        kappa = 1
    P = p ** kappa
    ulist = rng.choice([[1, 3], [1, 3, 9], [1, 5], [1, 7], [3], [5], [1, 1, 3], [1, 25], [7], [3, 9]])
    if any(u % p == 0 for u in ulist):
        continue
    table = {}
    for r in range(P):
        if r % p == 0:
            table[r] = (1, 0)
        else:
            u = rng.choice(ulist)
            # v with p | u r + v, small, positive outputs
            cands = [v for v in range(-6, 40) if (u * r + v) % p == 0 and u * (r if r else P) + v > 0 and v != 0]
            if not cands:
                cands = [(-u * r) % p or p]
            table[r] = (u, rng.choice(cands))
    S = PLIB.PShift(f"rand{trial}", p, kappa, table)
    if S.validate():
        continue
    signal.alarm(8)
    try:
        c = PCERT(dict(sys=S, cycles=[]))
        signal.alarm(0)
    except (AssertionError, TimeoutError):
        signal.alarm(0)
        ncert_to[0] += 1
        continue
    ntested += 1
    if not c.get("theorem_A"):
        continue
    napplies += 1
    signal.alarm(8)
    try:
        info = PCON.prepare(S)
    except (TimeoutError, AssertionError):
        continue
    finally:
        signal.alarm(0)
    dstar = info["dstar"]
    base = S.S * dstar
    T = S.T   # random maps: the table is the definition
    for M in sorted({base, base * p, base * 7 if base * 7 < 5000 else base}):
        if M * P > 2 * 10 ** 6:
            continue
        signal.alarm(20)
        try:
            comp, oe = residue_components(T, p, P, M)
            claimed = [PCON.g(S, info, z if z > 0 else M) for z in range(M)]
            signal.alarm(0)
        except TimeoutError:
            continue
        finally:
            signal.alarm(0)
        claimed = [PCON.g(S, info, z if z > 0 else M) for z in range(M)]
        ok(partition(comp) == partition(claimed), f"random map {table} p={p}: invariant mismatch mod {M}")
    for _ in range(3):
        y = rng.randrange(1, 10 ** 6)
        N = rng.choice([8, 9, 25, 27, 49, 11, 64 * 3])
        signal.alarm(6)
        try:
            x = next((xx for xx in range(1, 10 ** 4) if PCON.g(S, info, xx) == PCON.g(S, info, y)), None)
            if x is None:
                continue
            n, data = PCON.construct(S, info, y, x, N)
            if data["steps_to_y0"] > 30000 or n.bit_length() > 100000:
                continue
            signal.alarm(10)
            PCON.verify(S, y, x, N, n, data)
            nrv[0] += 1
        except TimeoutError:
            pass
        except AssertionError as ex:
            ok(False, f"random map construction failed {table} p={p} k={kappa}: {ex}")
        finally:
            signal.alarm(0)
print(f"   [time {time.time()-T0:.0f}s]")
print(f"6. random p-shift maps ({ncert_to[0]} certify timeouts): {ntested} certified, Theorem A applies to {napplies}, {nrv[0]} constructions replayed; no counterexample", flush=True)
ok(napplies >= 12, "enough random maps where Theorem A applies")


# =====================================================================================
# 7. Theorem C: (a) the gap -- G contains types of unbounded U-valuation and the construction
#    length grows with the valuation; (b) exact re-verification of the repaired certificates.
# =====================================================================================
import json
import counting as PCNT

recs = {r["id"]: r for r in json.load(open(os.path.join(HERE, "counting_results.json")))}
AFFECTED = []
for sid, r in recs.items():
    S = PSYS.get(sid)["sys"]
    W = r["W"]
    G = r["G_weighted"] or r["G_uniform"]
    badt = [t for t in G if any(vp(t, l) >= vp(W, l) for l in S.U)]
    if badt:
        AFFECTED.append(sid)
ok(sorted(AFFECTED) == sorted(["m3_a", "desc_s32_d65", "split_5", "split_13", "split_73", "split_97",
                               "split_7081", "splitB_7", "splitB_71", "split5_1", "desc_split7_1",
                               "desc_s32_plus9", "desc_m3_4n5"]), f"affected systems {AFFECTED}")
print("7a. GAP detected: certificates whose good-type set G contains types of unbounded U-valuation:",
      AFFECTED, flush=True)
# construction length grows with v_l(z): word count is not bounded on such a type
for sid, l in [("split5_1", 5), ("m3_a", 2)]:
    S, info = classes_of(sid)
    lens = []
    for k in range(0, 7):
        z = next(l ** k * m for m in range(1, 1000) if (l ** k * m) % S.p and PCON.g(S, info, l ** k * m) == PCON.g(S, info, 1))
        n, data = PCON.construct(S, info, z, 1, 11 * 16)
        PCON.verify(S, z, 1, 11 * 16, n, data)
        lens.append(len(data["ball_words"]))
    ok(lens == sorted(lens) and lens[-1] - lens[0] >= 6, f"{sid}: ball words grow with valuation {lens}")
    print(f"   {sid}: number of IA ball words for v_{l}(z) = 0..6: {lens}", flush=True)


def my_verify(S, W, H, G, sigma, w, eps=Fr(1, 1000)):
    """Exact check of (W) with children enumerated by the referee's preimage function on an actual
    integer representative of each lift (not from the prover's table)."""
    Umax = 1
    for (u, v) in S.table.values():
        Umax = Umax * u // gcd(Umax, u)
    big = W * Umax
    s, t = sigma.numerator, sigma.denominator
    qc = {}

    def q_of(rho):
        if rho not in qc:
            x = float(rho) ** (-s / t)
            q = Fr(x).limit_denominator(10 ** 8) * Fr(99999, 100000)
            while q ** t * rho ** s > 1:
                q *= Fr(999, 1000)
            assert q ** t * rho ** s <= 1
            qc[rho] = q
        return qc[rho]
    for z0 in range(big):
        if z0 % S.p == 0 or z0 % W not in G:
            continue
        z = z0 + big * 10 ** 6          # a large representative of the lift
        tot = Fr(0)
        for h in range(H + 1):
            for c in preimages(S, S.p ** h * z):
                if c % S.p == 0:
                    continue          # the dilation preimage
                rho = Fr(c * 1, 1)  # placeholder
                # rho = p^(h+1)/u for the branch of c
                u = S.table[c % S.P][0]
                rho = Fr(S.p ** (h + 1), u)
                if rho <= 1:
                    continue
                assert S.T(c) == S.p ** h * z and z < c <= rho * (1 + eps) * z
                if c % W in G:
                    tot += w[c % W] * q_of(rho * (1 + eps))
        if tot < w[z0 % W]:
            return False
    return True


# repaired certificates: G restricted to valuation-determined types
REPAIRED = {}
for sid in ["m3_a", "split_5", "split5_1", "desc_m3_4n5"]:
    r = recs[sid]
    S = PSYS.get(sid)["sys"]
    W, H = r["W"], r["H"]
    rows, big = PCNT.child_table(S, W, H)
    ia = PLIB.ia_game(S)
    G = {z % W for z in rows if (z % W) % ia["L2"] in ia["enter"] and all(vp(z % W, l) < vp(W, l) for l in S.U)}
    while True:
        nG = {t for t in G if all(sum(1 for k in rows[z] if k[0] in G) >= 2 for z in rows if z % W == t)}
        if nG == G:
            break
        G = nG
    sig = PCNT.best_sigma(rows, W, G, True)
    sigma = Fr(int(sig * 1000) - 1, 1000)
    wf = PCNT.weights_for(rows, W, G, float(sigma))
    w = {t: Fr(wf[t]).limit_denominator(10 ** 6) for t in G}
    good = my_verify(S, W, H, G, sigma, w)
    ok(good, f"repaired certificate {sid} sigma={sigma}")
    # the original (unrestricted) certificate also passes the exact inequality: the gap is in C2
    Gw = set(r["G_weighted"])
    wo = {int(k): Fr(v) for k, v in r["weights"].items()}
    ok(my_verify(S, W, H, Gw, Fr(r["sigma_weighted"]), wo), f"original inequality {sid}")
    REPAIRED[sid] = str(sigma)
print(f"   [time {time.time()-T0:.0f}s]")
print("7b. exact (W) inequality re-verified independently; repaired sigma (valuation-bounded types):", REPAIRED,
      flush=True)

# m3_a valuation reduction: for 2-units-excluded types, one bounded step reaches a 2-unit
S = PSYS.get("m3_a")["sys"]
for z in [rng.randrange(1, 10 ** 15) * 4 for _ in range(2000)]:
    if z % 3 == 0:
        continue
    c = (3 * z - 2) // 2
    ok((3 * z - 2) % 2 == 0 and S.T(c) == z and c % 2 == 1 and c < 2 * z, "m3_a valuation reduction step")
print("7c. m3_a: every z with 4 | z has the ancestor (3z-2)/2 < 2z which is odd (repair route)", flush=True)


# =====================================================================================
# 8. Proposition P (1932) and Theorem D numbers
# =====================================================================================
T32 = RAW["perm_1932"][0]
for n in range(1, 3000):
    x, seen, orb = n, {}, []
    for i in range(3000):
        if x in seen:
            break
        seen[x] = i
        orb.append(x)
        x = T32(x)
    if x in seen and x == n:  # periodic
        ok(any(len({y % 3 ** k for y in orb}) <= k for k in range(1, len(orb) + 1)), "P: cycle meets <= k classes for some k")
    elif x not in seen:      # long orbit: EVIDENCE that it meets >= k+1 classes mod 3^k
        for k in range(1, 9):
            ok(len({y % 3 ** k for y in orb}) >= k + 1, f"P evidence n={n} k={k}")
# injectivity of the 1932 map on [1, 10^5] (bijection claim)
imgs = [T32(n) for n in range(1, 10 ** 5)]
ok(len(set(imgs)) == len(imgs), "1932 injective")
# Theorem D thresholds for 5x+1
A = 2 * math.log(5)
ok(abs(math.exp(A) / math.log(10) - 10.86) < 0.01 and abs(math.exp(2 * A) / math.log(10) - 271.4) < 0.1,
   "Theorem D thresholds")
print("8. Proposition P data and Theorem D thresholds confirmed", flush=True)

# =====================================================================================
# 9. WRONG: "no sufficient progression can exist" for perm_1932.  The odd numbers 1 + 2Z form
#    a sufficient progression.  Proof (exact, all n): T(3q+1) = 4q+1 and T(3q+2) = 4q+3 are odd;
#    T(3q) = 2q < 3q, so no orbit stays in the 0-mod-3 branch forever; hence every forward orbit
#    contains an odd number.  Finite content checked: the three branch identities, symbolically
#    (two-point affine check suffices) and on a wide sample; plus orbit search.
# =====================================================================================
for q in list(range(0, 2000)) + [rng.randrange(1, 10 ** 30) for _ in range(2000)]:
    ok(T32(3 * q + 1) % 2 == 1 and T32(3 * q + 2) % 2 == 1, "1932: nonzero branches give odd values")
    if q > 0:
        ok(T32(3 * q) == 2 * q and 2 * q < 3 * q, "1932: zero branch strictly decreases")
for n in range(1, 10 ** 5):
    x, k = n, 0
    while x % 2 == 0:
        x = T32(x)
        k += 1
    # n itself even: its forward orbit reaches an odd value after k <= log_{3/2} n steps
    ok(k <= 40, "1932 odd value reached quickly")
# the only sufficient progressions are N = 1 and 1 mod 2: cycle (1) forces x = 1 mod N, cycle (2 3)
# forces N | 1 or N | 2
ok(T32(1) == 1 and T32(2) == 3 and T32(3) == 2, "1932 cycles (1), (2 3)")
suff = [(x, N) for N in range(1, 60) for x in range(N) if all(any(c % N == x for c in cy) for cy in ([1], [2, 3]))]
ok(suff == [(0, 1), (1, 2)], f"progressions meeting the cycles (1) and (2 3): {suff}")
print(f"   [time {time.time()-T0:.0f}s]")
print("9. WRONG item: 1 mod 2 is a sufficient progression for perm_1932 (proved above)", flush=True)

# =====================================================================================
# 10. Theorem A item 3 example "1 mod (p^(kappa-1) d*) m" meets only ONE g-class (FIX needed when
#     there are several classes): e.g. split5_3 (d* = 3).
# =====================================================================================
S, info = classes_of("split5_3")
vals = {PCON.g(S, info, 1 + 3 * 7 * k) for k in range(0, 3000)}
ok(len(vals) == 1 and len({PCON.g(S, info, n) for n in range(1, 100)}) == 2,
   "item-3 example 1 mod d*m meets one class only")
print("10. Theorem A item 3 example meets only one g-class when there are several (wording fix)", flush=True)

# =====================================================================================
# 11. Theorem C repair lemma R (exact finite content).  For a type of unbounded U-valuation, a
#     vertex z with v_l(z) >= V (V > max v_l(v_r)) has, after a D-word of length < p^(kappa-1)
#     fixing the state, a move r with u_r | v_r (l-parts), v_r != 0, admissible at that state; the
#     ancestor P_r(p^h z) = (p^(h+1) z - v_r)/u_r then has v_l = v_l(v_r) - v_l(u_r), bounded
#     independently of z.  We check the finite condition for every state of every affected system.
# =====================================================================================
def hiv(S, st, e, j):
    """a p-unit z = st (mod p^(kappa-1)) with v_l(z) = e exactly... at least e for every l in U."""
    MU = math.prod(l ** e for l in S.U)
    t = (st * pow(MU, -1, S.S)) % S.S if S.S > 1 else 0
    return MU * (t + S.S * j)


for sid in AFFECTED:
    S = PSYS.get(sid)["sys"]
    mv = [m for m in S.moves() if m["kind"] != "D"]
    for st in range(S.S):
        if S.kappa > 1 and st % S.p == 0:
            continue          # tree vertices are p-units
        found = None
        for h in range(0, 2 * S.kappa + 2):
            for m in mv:
                if m["v"] == 0:
                    continue
                # admissibility at p^h z for z of state st and U-valuation >= 60: exact finite test
                zs = [hiv(S, st, 60, j) for j in (1, 2, 5)]
                if all((S.p ** h * z) % S.S == m["src"] and (S.p ** (h + 1) * z - m["v"]) % m["u"] == 0
                       for z in zs):
                    found = (h, m)
                    break
            if found:
                break
        ok(found is not None, f"repair lemma R: {sid} state {st}")
        if not found:
            continue
        h, m = found
        # exactness: state of p^h z depends only on z mod p^(kappa-1); U-domain condition for
        # v_l(z) >= v_l(u) is u | v_r: check that directly
        ok(all(vp(m["v"], l) >= vp(m["u"], l) for l in S.U) and m["v"] % m["u"] == 0, f"R: u | v ({sid})")
        for _ in range(100):
            e = rng.randrange(max(vp(m["v"], l) for l in S.U) + 1, 40)
            z = hiv(S, st, e, rng.randrange(1, 10 ** 6))
            if z % S.p == 0:
                continue
            c = (S.p ** (h + 1) * z - m["v"]) // m["u"]
            ok(S.T(c) == S.p ** h * z, f"R ancestor {sid}")
            ok(all(vp(c, l) == vp(m["v"], l) - vp(m["u"], l) for l in S.U), f"R valuation {sid}")
            ok(0 < c <= S.p ** (h + 1) * z, f"R size {sid}")
print("11. repair lemma R holds (exact finite condition) for every affected system:", AFFECTED, flush=True)

# 12. EVIDENCE for div23_5n1 claim (every n <= 2e5 reaches (1 6 3))
def d23(n):
    return n // 2 if n % 2 == 0 else (n // 3 if n % 3 == 0 else 5 * n + 1)
bad = 0
for n in range(1, 200001):
    x, s = n, 0
    while x not in (1, 6, 3) and s < 100000:
        x = d23(x)
        s += 1
    bad += x not in (1, 6, 3)
ok(bad == 0, f"div23_5n1 evidence: {bad} starts not reaching (1 6 3)")
print(f"   [time {time.time()-T0:.0f}s]")
print("12. EVIDENCE: div23_5n1 every n <= 2e5 reaches (1 6 3)", flush=True)

if FAIL:
    print(len(FAIL), "FAILURES")
    sys.exit(1)
print("ALL REFEREE CHECKS BEHAVED AS REPORTED (including the detected Theorem C gap)")
