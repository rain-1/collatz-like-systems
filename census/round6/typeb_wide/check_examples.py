"""Exact checks for the named type-(b) systems and the parity-map neighbour theorem (P8).

[H]   each named system: Theorem-H proof object built (tblib.prove_H) and re-checked by the
      independent verifier (verify_H.verify); cycle list equals the expected one.
[CNT] second proof (counter potential, round4/wpotential Remark generalised): the
      lexicographic V = (level, phi) with phi = c(r) n on contracting components,
      phi = l (v_p(n - x_i) + E_i) - i on simple-cycle components, 0 on trivial ones, is
      checked exactly to descend at every step of the orbits of n <= 3000 and of 300 random
      n < 2^200: level drops, or phi drops by >= 1 (cycle), or
      c(s) T(n) <= theta c(r) n + beta (contracting).
[EV]  consistency (EVIDENCE, not part of the proof): orbits of n <= 2*10^5 end in listed cycles.
[P8]  Theorem P8: for odd a in [3, 41] and odd d in [-41, 41] with a + d >= 1, the parity map
      an+d with n = 4 (mod 8) -> n+4 is of type (b), Theorem H applies, and its cycles are
      (4 8) plus (x*, 2x*) when x* = -d/(a-2) is a positive integer.
[NEG] controls: 3x+1, 3x-1, 3x+5, 5x+1 are of type (c) at levels 1..7 (prove_H refuses).
Exit 0 iff all pass.  Runtime about 2 minutes.
"""
import sys, os, random, math
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import tblib as TB
import verify_H as VH

OK = True


def claim(name, cond):
    global OK
    print(("PASS " if cond else "FAIL ") + name, flush=True)
    OK = OK and bool(cond)


H2 = (1, 0, 2)
H3 = (1, 0, 3)


def even_half(m, odd):
    return [H2 if r % 2 == 0 else odd.get(r, (3, 1, 1)) for r in range(2 ** m)]


NAMED = {
    # modulus 8, Collatz convention (n/2 on evens): the smallest possible (shapes.py [M3])
    "sh8": (2, 3, even_half(3, {1: (1, 1, 1), 5: (1, 5, 1)}), [[1, 2], [5, 10]]),
    "sh8b": (2, 3, even_half(3, {1: (1, 1, 1), 3: (1, 7, 1), 5: (1, 5, 1)}), [[1, 2], [5, 10]]),
    # modulus 4, general unit table (shapes.py [M2])
    "sh4": (2, 2, [(1, 1, 1), (1, 1, 1), (1, 2, 2), (3, 1, 2)], [[2], [4, 5, 6]]),
    # mod 16: 3n+1 on 5 of the 8 odd classes
    "sh16": (2, 4, even_half(4, {5: (1, 5, 1), 9: (1, 1, 1), 13: (1, 7, 1)}), [[1, 4, 2], [5, 10]]),
    # mod 32 (SAT search): 3n+1 only on 31 mod 32, isolated x* = -1
    "sh32": (2, 5, even_half(5, {**{r: (1, 1, 1) for r in (1, 3, 9, 25)},
                                   **{r: (1, 5, 1) for r in (5, 15, 21, 29)},
                                   **{r: (1, 3, 1) for r in (7, 17, 23)},
                                   **{r: (1, 7, 1) for r in (11, 13, 19, 27)}}), None),
    # base 3, mod 9 (C9 family): isolated expanding x* = -1/2 (5/3)
    "c9a": (3, 2, [H3, (5, 1, 1), (2, 1, 1), H3, (5, 1, 1), (1, 1, 1), H3, (4, 1, 1), (2, -1, 1)],
            [[2, 5, 6]]),
    # base 3, mod 9: the expanding cycle is the positive cycle (1 3), multiplier 4/3, isolated
    "c9b": (3, 2, [H3, (4, -1, 1), (2, 1, 1), H3, (4, 1, 1), (1, 1, 1), H3, (4, 1, 1), (2, -1, 1)],
            [[1, 3], [2, 5, 6]]),
    # round 3 references
    "acc_h16": (2, 4, even_half(4, {5: (1, 1, 1), 9: (1, 1, 1), 13: (1, 5, 1)}), [[1, 4, 2], [3, 10, 5, 6]]),
    "acc_h9": (3, 2, [H3, (2, 1, 3), (4, 4, 3), H3, (2, 4, 3), (4, 1, 3), H3, (2, 7, 3), (4, 1, 3)],
               [[1], [4], [7]]),
    # one-class neighbours of open maps (mods.py), Theorem P8 instances
    "3x+1#": (2, 3, [H2, (3, 1, 1), H2, (3, 1, 1), (1, 4, 1), (3, 1, 1), H2, (3, 1, 1)], [[4, 8]]),
    "3x-1#": (2, 3, [H2, (3, -1, 1), H2, (3, -1, 1), (1, 4, 1), (3, -1, 1), H2, (3, -1, 1)],
              [[1, 2], [4, 8]]),
    "5x+1#": (2, 3, [H2, (5, 1, 1), H2, (5, 1, 1), (1, 4, 1), (5, 1, 1), H2, (5, 1, 1)], [[4, 8]]),
    "split5_1#": (2, 3, [H2, (5, 1, 1), H2, (1, 1, 1), (1, 2, 1), (5, 1, 1), H2, (1, 1, 1)], [[3, 4, 6]]),
}


def lex_potential_check(name, p, m, tab, P, rnd):
    """[CNT]: exact descent of V = (level, phi) along sample orbits."""
    K = P["K"]
    PK, Q = p ** K, p ** m
    T = TB.step_fn(p, m, tab)
    comp_of, info = {}, {}
    for c in P["comps"]:
        for x in c["nodes"]:
            comp_of[x] = c["id"]
        info[c["id"]] = c
    pos = {}
    for c in P["comps"]:
        if "cycle" in c:
            L = len(c["cycle"])
            E = 0
            for i, x in enumerate(c["cycle"]):
                pos[x] = (i, E, L, c["xstar"][i])
                E += TB.val(tab[x % Q][2], p)[0]

    def V(n):
        r = n % PK
        c = info[comp_of[r]]
        if c["kind"] == "trivial":
            return c["level"], None, Fr(0)
        if "cycle" in c:
            i, E, L, x = pos[r]
            if Fr(n) == x:
                return c["level"], "fix", None
            d, a = Fr(n) - x, 0
            num, den = d.numerator, d.denominator
            while num % p == 0:
                num //= p
                a += 1
            return c["level"], "cyc", L * (a + E) - i
        return c["level"], "con", c["c"][r] * n

    starts = list(range(1, 3001)) + [rnd.getrandbits(200) + 1 for _ in range(300)]
    good = True
    for n in starts:
        for _ in range(4000):
            lv, kind, ph = V(n)
            if kind == "fix":
                break
            n2 = T(n)
            lv2, kind2, ph2 = V(n2)
            if lv2 < lv:
                pass
            elif lv2 > lv:
                good = False
            elif kind == "cyc":
                good &= kind2 in ("cyc", "fix") and (kind2 == "fix" or ph2 <= ph - 1)
            elif kind == "con":
                c = info[comp_of[n % PK]]
                good &= kind2 == "con" and ph2 <= c["theta"] * ph + c["beta"]
                if ph <= c["Vmax"]:
                    break            # inside the finite exceptional set: stop following
            else:
                good = False          # trivial component cannot keep its level
            n = n2
            if not good:
                break
        if not good:
            break
    claim(f"[CNT] {name}: lexicographic counter potential descends on sample orbits", good)


def evidence_cycles(name, p, m, tab, cycles, N=200000):
    T = TB.step_fn(p, m, tab)
    cyc_pts = {x: c[0] for c in cycles for x in c}
    fate = {}
    ok = True
    for n0 in range(1, N + 1):
        path, n = [], n0
        while n not in cyc_pts and n not in fate and len(path) < 10 ** 5:
            path.append(n)
            n = T(n)
        if len(path) >= 10 ** 5:
            ok = False
            break
        f = cyc_pts.get(n, fate.get(n))
        for x in path:
            fate[x] = f
    claim(f"[EV] {name}: all n <= {N} end in the listed cycles", ok)


def main():
    rnd = random.Random(2026)
    for name, (p, m, tab, expect) in NAMED.items():
        P = TB.prove_H(p, m, tab)
        claim(f"[H] {name} ({TB.fmt_rule(p, m, tab)}): type (b), Theorem H applies",
              P is not None and P["verdict"] == "b")
        if P is None:
            continue
        J = TB.to_json(P, name)
        try:
            VH.verify(J, quiet=True)
            v = True
        except AssertionError as ex:
            print(ex)
            v = False
        cyc = P["cycles"]
        xs = [str(c["xstar"][0]) for c in P["comps"] if c["kind"] == "b"]
        claim(f"[H] {name}: independent verifier accepts; cycles {cyc}; isolated expanding x*: {xs}",
              v and (expect is None or cyc == expect))
        lex_potential_check(name, p, m, tab, P, rnd)
        evidence_cycles(name, p, m, tab, cyc, N=50000 if p ** m > 16 else 200000)
    # [P8]
    bad = []
    count = 0
    for a in range(3, 42, 2):
        for d in range(-41, 42, 2):
            if a + d < 1:
                continue
            tab = [H2 if r % 2 == 0 else (a, d, 1) for r in range(8)]
            tab[4] = (1, 4, 1)
            P = TB.prove_H(2, 3, tab)
            xs = Fr(-d, a - 2)
            expect = [[4, 8]]
            if xs.denominator == 1 and xs > 0:
                x = int(xs)
                expect = sorted([[4, 8], [x, 2 * x]])
            count += 1
            if P is None or P["verdict"] != "b" or P["cycles"] != expect:
                bad.append((a, d))
    claim(f"[P8] parity maps an+d with n = 4 (8) -> n+4: {count} pairs (a, d), all type (b) "
          f"with the predicted cycles", not bad)
    # [NEG]
    neg = True
    for nm, tab in (("3x+1", [H2, (3, 1, 1)]), ("3x-1", [H2, (3, -1, 1)]), ("3x+5", [H2, (3, 5, 1)]),
                    ("5x+1", [H2, (5, 1, 1)])):
        for K in range(1, 8):
            cl = TB.classify(2, 1, tab, K)
            neg &= TB.verdict(cl) == "c" and TB.prove_H(2, 1, tab, K) is None
    claim("[NEG] 3x+1, 3x-1, 3x+5, 5x+1: type (c) at levels 1..7, Theorem H refuses", neg)
    print("ALL PASS" if OK else "SOME CHECK FAILED")
    sys.exit(0 if OK else 1)


if __name__ == "__main__":
    main()
