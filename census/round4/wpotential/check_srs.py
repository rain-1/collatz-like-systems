"""Exact checks for the string-rewriting encoding of K7 (srs.md).

[SEM]  every swap/left rule preserves the Horner value as an affine function of
       the context to its left (checked symbolically: both sides give the same
       map x -> a x + b), and the three map rules implement K7 on z >= 0:
       fR: 2y -> y;  ftR: 4y+1 -> y;  ttR -> ctR: 4y+3 -> 6y+5;  LtR -> LR: 1 -> 0.
[SIM]  the leftmost-ternary-first derivation from L bin(z) R passes through
       L bin(K7(z)) R (up to leading f's) and ends in LR, for every 1 <= z < 3000;
       the number of map-rule steps equals the K7 stopping time.
[NF]   every word L w R with w a nonempty binary word has a redex.
[SIM-cores] the encodings of six further cores (srs_cores.py) have value-correct
       rules and simulate T_S from n to 1 (or 3) for n < 2000.
[CHAIN] every chain stored in mi_chains.json (by mi_record.py) is re-verified
       exactly; the rule set it leaves contains every class map rule (every
       map rule except K7's single instance small1: 1 -> 0, which IS removed).
Exits 0 iff every claim passes.  Runtime: about 1 s.
"""
import json
import os
import srs_lib as S

ok = True


def claim(msg, cond):
    global ok
    print(("PASS " if cond else "FAIL ") + msg, flush=True)
    ok = ok and bool(cond)


K7_RULES = [("e0", "fR", "R"), ("e1", "ftR", "R"), ("e3", "ttR", "ctR"), ("small1", "LtR", "LR")]
RULES = K7_RULES + S.common_rules()


def affine(word):
    """word without L/R -> (a, b) with value(prefix + word) = a*value(prefix) + b."""
    a, b = 1, 0
    for ch in word:
        if ch == "p":
            b += 1
            continue
        base = 2 if ch in S.BIN else 3
        dig = S.BIN.get(ch, S.TER.get(ch))
        a, b = a * base, b * base + dig
    return a, b


def K7(z):
    if z % 2 == 0:
        return z // 2
    if z % 4 == 3:
        return (3 * z + 1) // 2
    return (z - 1) // 4


# [SEM]
good = True
for name, l, r in S.common_rules():
    if name.startswith("swap"):
        good = good and affine(l) == affine(r)
    else:   # left rules: L u -> L v means value(u) = value(v) from 0
        good = good and affine(l[1:])[1] == affine(r[1:])[1]
a0, b0 = affine("f"), affine("ft"), 
good = good and affine("f") == (2, 0) and affine("ft") == (4, 1)
good = good and affine("tt") == (4, 3) and affine("ct") == (6, 5)
good = good and all(K7(2 * y) == y and K7(4 * y + 1) == y and K7(4 * y + 3) == 6 * y + 5 for y in range(1000))
claim("[SEM] swap/left rules preserve values; map rules implement K7", good)


def derive(word, maxsteps=10 ** 7):
    """Strategy: if a ternary digit occurs, rewrite the leftmost one (swap or left
    rule); otherwise apply the map rule at R.  Returns list of values seen at
    all-binary words, and the final word."""
    vals, steps = [], 0
    while steps < maxsteps:
        steps += 1
        tpos = next((i for i, ch in enumerate(word) if ch in S.TER), None)
        if tpos is not None:
            for name, l, r in RULES:
                if (name.startswith("swap") or name.startswith("left")) and word.startswith(l, tpos - len(l) + 1):
                    i = tpos - len(l) + 1
                    word = word[:i] + r + word[i + len(l):]
                    break
            else:
                raise AssertionError(("stuck", word))
            continue
        vals.append(S.value(word))
        for name, l, r in K7_RULES:
            if word.endswith(l) and (name != "small1" or word == l):
                word = word[:len(word) - len(l)] + r
                break
        else:
            return vals, word
    raise AssertionError("too long")


good = True
for z in range(1, 3000):
    vals, nf = derive("L" + S.bits(z) + "R")
    orb = [z]
    while orb[-1] != 0:
        orb.append(K7(orb[-1]))
    good = good and vals == orb and nf == "LR"
claim("[SIM] canonical derivation from L bin(z) R follows the K7 orbit to 0 and ends in LR (z < 3000)", good)

good = True
for L in range(1, 12):
    for x in range(2 ** L):
        w = "L" + "".join("t" if (x >> (L - 1 - i)) & 1 else "f" for i in range(L)) + "R"
        has = any(l in w for _, l, _ in RULES)
        good = good and has
claim("[NF] every word L w R with w a nonempty binary word (length <= 11) has a redex", good)

# [CHAIN] (verified after the core encodings are defined, below)

# [SIM-cores] the encodings of six cores simulate T_S on n < 2000
import srs_cores as SC


def T_S(Sset, n):
    if n % 2 == 0:
        return n // 2
    return 3 * n + 1 if n % 8 in Sset else n + 1


def derive_general(rules, word, maxsteps=10 ** 7):
    maprules = [r for r in rules if r[1].endswith("R")]
    other = [r for r in rules if not r[1].endswith("R")]
    vals = []
    for _ in range(maxsteps):
        pos = next((i for i, ch in enumerate(word) if ch in "abcp"), None)
        if pos is None and word.startswith("Lf"):
            word = "L" + word[2:]
            continue
        if pos is not None:
            for name, l, r in other:
                i = pos - len(l) + 1
                if i >= 0 and word.startswith(l, i):
                    word = word[:i] + r + word[i + len(l):]
                    break
            else:
                raise AssertionError(("stuck", word))
            continue
        vals.append(S.value(word))
        for name, l, r in maprules:
            if word.endswith(l) and (not l.startswith("L") or word == l):
                word = word[:len(word) - len(l)] + r
                break
        else:
            return vals, word
    raise AssertionError("too long")


for nm, Sset, three in (("sf3_17", {1, 7}, False), ("sf3_57", {5, 7}, False), ("sf3_157", {1, 5, 7}, False),
                        ("sf3_357", {3, 5, 7}, False), ("sf3_13", {1, 3}, True), ("sf3_135", {1, 3, 5}, False)):
    rules = SC.core_rules(Sset, three)
    sem = all(affine(l) == affine(r) for name, l, r in rules if "R" not in l and "L" not in l)
    sem = sem and all(affine(l[1:])[1] == affine(r[1:])[1] for name, l, r in rules if l.startswith("L") and "R" not in l)
    for name, l, r in rules:
        if name.startswith(("odd", "inc")):
            for q in range(64):
                n = S.value("L" + S.bits(q) + l[:-1])
                a, b = affine(r[:-1])
                sem = sem and a * q + b == T_S(Sset, n)
    good = True
    stops = {1, 3} if three else {1}
    for n in range(1, 2000):
        vals, nf = derive_general(rules, "L" + S.bits(n) + "R")
        orb = [n]
        while orb[-1] not in stops:
            orb.append(T_S(Sset, orb[-1]))
        good = good and vals == orb and S.value(nf) in stops
    claim(f"[SIM-cores] {nm}: canonical derivation follows T_S from n to {sorted(stops)} (n < 2000)", good and sem)

# [CHAIN] re-verify every stored z3 chain exactly
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mi_chains.json")
data = json.load(open(p))
specs = {"K7": RULES}
for nm, Sset, three in (("sf3_17", {1, 7}, False), ("sf3_57", {5, 7}, False), ("sf3_157", {1, 5, 7}, False),
                        ("sf3_357", {3, 5, 7}, False), ("sf3_13", {1, 3}, True), ("sf3_135", {1, 3, 5}, False)):
    specs[nm] = SC.core_rules(Sset, three)
for nm, rec in data.items():
    chain = [(d, {a: (M, v) for a, (M, v) in I.items()}) for d, I in rec["chain"]]
    rem = S.verify_chain(specs[nm], chain)
    mapnames = {r[0] for r in specs[nm] if r[0].startswith(("e", "odd", "inc", "even"))}
    claim(f"[CHAIN] {nm}: stored chain of {len(chain)} interpretations verified exactly; "
          f"core left: {len(rem)} of {len(specs[nm])} rules, all class map rules among them",
          sorted(r[0] for r in rem) == sorted(rec["remaining"]) and mapnames <= {r[0] for r in rem})
print("ALL PASS" if ok else "SOME CHECK FAILED")
raise SystemExit(0 if ok else 1)
