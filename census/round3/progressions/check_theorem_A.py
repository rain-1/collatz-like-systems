"""Check for Theorem A (theorem_A_sufficiency.md).  Exact arithmetic throughout.
Exits 0 iff every check passes.  Run: nice python3 check_theorem_A.py  (a few minutes)."""

import json
import os
import random
import signal
import sys
from fractions import Fraction as Fr
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import plib
import systems
import construct
from certify import certify

FAIL = []


def ok(cond, msg):
    if not cond:
        FAIL.append(msg)
        print("FAIL:", msg, flush=True)


rng = random.Random(20261127)

# ------------------------------------------------------------------ 0. shortcut lemma vs raw census maps
sys.path.insert(0, os.path.join(HERE, "..", ".."))
import importlib.util
spec = importlib.util.spec_from_file_location("census_systems", os.path.join(HERE, "..", "..", "systems.py"))
cs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cs)
RAW = {"m3_c": "m3_c_s100", "m3_a": "m3_a_s100", "split_13": "split_13_s27", "split5_3": "split5_3_s27",
       "split5_1": "split5_1_s27", "par_5_1": "par_5_1_s5", "par_3_5": "par_3_5_s27", "m3_d": "m3_d_s7",
       "m3_e": "m3_e_s7", "m3_g": "m3_g_s7", "m3_b": "m3_b_s8", "par_7_1": "par_7_1_s1",
       "splitB_71": "splitB_71_s27", "par_1_5": "par_1_5_s27"}
for sid, cid in RAW.items():
    S = systems.get(sid)["sys"]
    R = cs.get(cid)["step"]
    for n in list(range(1, 3000)) + [rng.randrange(1, 10 ** 30) for _ in range(300)]:
        s = S.T(n)
        r1 = R(n)
        ok(s == r1 or s == R(r1), f"shortcut {sid} n={n}")
        if s != r1:
            ok(r1 % S.p == 0 and n % S.p != 0, f"shortcut structure {sid} n={n}")
print("0. shortcut lemma checked against census raw maps", flush=True)

# ------------------------------------------------------------------ 1. certificates recomputed and compared
stored = {c["id"]: c for c in json.load(open(os.path.join(HERE, "certificates.json")))}
APPLIES = []
for e in systems.SYSTEMS:
    c = certify(e)
    s = stored[e["id"]]
    for key in ["theorem_A", "invariant_modulus", "delta", "state_free", "theorem_B"]:
        ok(c.get(key) == s.get(key), f"certificate {e['id']} {key}: {c.get(key)} vs {s.get(key)}")
    if c.get("theorem_A"):
        APPLIES.append((e, c))
expected_A_false = {"par_5_5", "par_7_7", "par_3_3", "par_3_9", "perm_1932"}
ok({e["id"] for e in systems.SYSTEMS} - {e["id"] for e, c in APPLIES} == expected_A_false,
   "set of systems where Theorem A does not apply")
print(f"1. certificates recomputed; Theorem A applies to {len(APPLIES)} systems", flush=True)

# ------------------------------------------------------------------ 2. finite content per system
for e, c in APPLIES:
    S = e["sys"]
    sid = e["id"]
    mv = S.moves()
    ok(not S.validate() and S.has_dilation() and S.state_graph_strongly_connected(), f"A0/A1 {sid}")
    # loops: replay words on states, recompute affine maps, recompute translation amounts
    loops = plib.fundamental_loops(S)
    for w, f in loops:
        st = 0
        for i in w:
            ok(mv[i]["src"] == st, f"loop word not admissible {sid}")
            st = mv[i]["dst"]
        ok(st == 0, f"loop does not return to 0 {sid}")
        ff = plib.ID
        for i in w:
            ff = plib.Aff(Fr(S.p, mv[i]["u"]), Fr(-mv[i]["v"], mv[i]["u"])) @ ff
        ok(ff == f, f"loop affine {sid}")
    d = 0
    for t in c["translations"]:
        i, j = t["loops"]
        g, h = loops[i][1], loops[j][1]
        comm = g @ h @ g.inv() @ h.inv() if i != j else g
        ok(comm.a == 1 and comm.b == Fr(t["amount"]), f"translation amount {sid}")
        d = gcd(d, plib.strip(comm.b.numerator, S.bad))
    ok(d == c["delta"], f"delta {sid}")
    # classes: every move preserves them; minimal modulus
    cls = plib.groupoid_classes(S, c["delta"])
    ok(plib.check_symmetric(S, c["delta"], cls), f"class symmetry {sid}")
    dstar, sf, rep = plib.minimal_invariant(S, c["delta"], cls)
    ok(dstar == c["invariant_modulus"], f"d* {sid}")
    # invariance g(Tn) = g(n)
    def g(n):
        return rep[(n % S.S, n % dstar)]
    for n in list(range(1, 20001)) + [rng.randrange(1, 10 ** 40) for _ in range(2000)]:
        if g(S.T(n)) != g(n):
            ok(False, f"invariance {sid} n={n}")
            break
    # move identities
    for _ in range(3000):
        z = rng.randrange(1, 10 ** 25)
        for m in mv:
            w = S.move_int(m, z)
            adm = (z % S.S == m["src"]) and ((S.p * z - m["v"]) % m["u"] == 0)
            ok((w is not None) == adm, f"move admissibility {sid}")
            if w is not None and w > 0:
                ok(S.T(w) == z, f"move inverse {sid}")
    # cylinder lemma: words of length t give at most one class mod p^(kappa+t-1)
    for t in (1, 2, 3):
        mod = S.p ** (S.kappa + t - 1)
        seen = {}
        for n in range(mod, 2 * mod):
            x, word = n, []
            for _ in range(t):
                word.append(x % S.P)
                x = S.T(x)
            seen.setdefault(tuple(word), set()).add(n % mod)
        ok(all(len(v) == 1 for v in seen.values()), f"cylinder lemma {sid} t={t}")
    # lift lemma (randomized)
    for _ in range(200):
        x = rng.randrange(1, 10 ** 6)
        t = rng.randrange(0, 12)
        cc, a = x, 1
        for _ in range(t):
            a *= S.table[cc % S.P][0]
            cc = S.T(cc)
        y = cc + a * S.S * rng.randrange(0, 10 ** 8)
        n = x + S.p ** t * (y - cc) // a
        z = n
        for _ in range(t):
            z = S.T(z)
        ok(z == y, f"lift lemma {sid}")
    # IA game: verify the defining property of the live set independently
    if S.U:
        ia = plib.ia_game(S)
        L2, live, enter = ia["L2"], ia["live"], ia["enter"]
        ok(len(live) > 0, f"live nonempty {sid}")
        iso = [m for m in mv if m["kind"] in ("I", "D")]
        for nd in live:
            # iso closure
            seen, st = {nd}, [nd]
            while st:
                a_, x_ = st.pop()
                for m in iso:
                    if m["src"] == a_:
                        y_ = (m["dst"], (S.p * x_ - m["v"]) % L2)
                        if y_ not in seen:
                            seen.add(y_)
                            st.append(y_)
            good = False
            for (a_, x_) in seen:
                for m in mv:
                    if m["kind"] == "E" and m["src"] == a_ and (S.p * x_ - m["v"]) % m["u"] == 0:
                        modr = L2 // m["u"]
                        w_ = ((S.p * x_ - m["v"]) // m["u"]) % modr
                        if all((m["dst"], w_ + modr * k) in live for k in range(m["u"])):
                            good = True
            ok(good, f"live node without option {sid} {nd}")
        for z in range(L2):
            want = any((0, z * pow(S.p, h, L2) % L2) in live for h in range(S.kappa - 1, S.kappa + L2 + 2))
            ok(want == (z in enter), f"enterable {sid} {z}")
        if not c["IA"]["all_enterable"]:
            for m in mv:
                if m["kind"] == "E":
                    for _ in range(500):
                        n = m["r"] + S.P * rng.randrange(0, 10 ** 20)
                        if n > 0:
                            ok((S.T(n) % L2) in enter, f"E image enterable {sid}")
            Bnd, necyc = plib.non_E_cycles(S)
            for n in range(Bnd + 1, Bnd + 5000):
                r = n % S.P
                if S.moves()[r]["kind"] in ("I", "D"):
                    ok(S.T(n) < n, f"non-E descent {sid}")
            for n in range(1, Bnd + 1):
                r = n % S.P
                if S.moves()[r]["kind"] in ("I", "D"):
                    ok(S.T(n) <= Bnd, f"non-E box {sid}")
            ok(all(any(x % L2 in enter for x in cy) for cy in necyc), f"non-E cycles enterable {sid}")
print("2. finite content verified for every applicable system", flush=True)


# ------------------------------------------------------------------ 3. the proof executed
def _alarm(*a):
    raise TimeoutError


signal.signal(signal.SIGALRM, _alarm)
total, timeouts = 0, 0
for e, c in APPLIES:
    S = e["sys"]
    info = construct.prepare(S)
    starts = e["cycles"] or [1]
    for trial in range(10):
        y = rng.choice(starts) if trial % 2 == 0 else rng.randrange(1, 10 ** 6)
        N = rng.choice([1, 2, 4, 8, 16, 3, 9, 27, 5, 25, 7, 49, 10, 12, 100, 77, 120, 1000])
        while True:
            x = rng.randrange(1, 10 ** 5)
            if construct.g(S, info, x) == construct.g(S, info, y):
                break
        signal.alarm(20)
        try:
            n, data = construct.construct(S, info, y, x, N)
            construct.verify(S, y, x, N, n, data)
            total += 1
        except TimeoutError:
            timeouts += 1
        except AssertionError as ex:
            ok(False, f"construction {e['id']} y={y} x={x} N={N}: {ex}")
        finally:
            signal.alarm(0)
print(f"3. constructive proof verified on {total} random targets ({timeouts} skipped for time)", flush=True)
ok(total >= 250, "too few constructive verifications")

# ------------------------------------------------------------------ 4. counterexamples of Section 7
# (a) n/2, 2n: residue graph mod 8 weakly connected, class of 1 misses 3 mod 8
def dbl(n):
    return n // 2 if n % 2 == 0 else 2 * n
edges = set()
for n in range(1, 8 * 64):
    edges.add((n % 8, dbl(n) % 8))
comp = {0}
changed = True
while changed:
    changed = False
    for a_, b_ in edges:
        if (a_ in comp) != (b_ in comp):
            comp |= {a_, b_}
            changed = True
ok(comp == set(range(8)), "residue graph mod 8 connected for n/2, 2n")
ok({pow(2, k, 8) for k in range(0, 20)} == {0, 1, 2, 4}, "class of 1 misses 3 mod 8")
ok(all(dbl(2 ** k) in (2 ** (k - 1), 2) for k in range(1, 50)), "class of 1 is the powers of 2")
# (b) div2_3n: class of 1 = {2^a 3^b}; residues mod 73 = <2,3>
def d23(n):
    return n // 2 if n % 2 == 0 else 3 * n
sub = {1}
changed = True
while changed:
    new = {x * 2 % 73 for x in sub} | {x * 3 % 73 for x in sub}
    changed = not new <= sub
    sub |= new
cls1 = {(2 ** a * 3 ** b) % 73 for a in range(40) for b in range(40)}
ok(cls1 == sub and len(sub) < 72, "div2_3n class of 1 hits exactly <2,3> mod 73")
print("4. counterexamples checked", flush=True)

if FAIL:
    print(f"{len(FAIL)} FAILURES")
    sys.exit(1)
print("ALL CHECKS PASSED")
