"""m3_b_s8: partial theorem (descent-tree exceptional set) + up-run witness,
plus the rewriting-lens artefacts: the simulation lemma for the mixed base-3/4
SRS (sampled) and exact re-verification of the z3-found matrix-interpretation
chain stored in m3b_mi_chain.json (pure Python; z3 is not needed)."""
import json
import os
import sys
from _partial_check import run, HERE
from srs import family_srs, verify_chain, compose, check_interp, L, R

run("m3_b_s8", lambda K: 3**K - 1, range(1, 41), lambda K: K)


def T(n):
    r = n % 3
    return n // 3 if r == 0 else (4 * n - 1) // 3 if r == 1 else (4 * n + 1) // 3


def value(word):
    v = 0
    for a in word:
        if a in (L, R):
            continue
        v = v * (3 if a[0] == 't' else 4) + a[1]
    return v


def tern_word(n):
    ds = []
    while n:
        ds.append(('t', n % 3))
        n //= 3
    return [L] + ds[::-1] + [R]


rules = family_srs(4, 1, 3, h=1)
# Simulation lemma, sampled: from the ternary word of n >= 3, rewriting with the
# tail rule and then the swap/left rules (leftmost-first) reaches a pure ternary word of T(n).
for n in range(3, 3000):
    w = tern_word(n)
    first = True
    while True:
        # apply the first applicable rule, tail rules only at the very start
        done = False
        for name, l, r in rules:
            if name.startswith("tail") != first:
                continue
            for i in range(len(w) - len(l) + 1):
                if w[i:i + len(l)] == l:
                    w = w[:i] + r + w[i + len(l):]
                    done = True
                    break
            if done:
                break
        if first:
            assert done, n
            first = False
            continue
        if not done:
            break
    assert all(a[0] == 't' for a in w[1:-1]) and value(w) == T(n), n

# Exact re-verification of the partial matrix-interpretation chain.
chain_json = json.load(open(os.path.join(HERE, "m3b_mi_chain.json")))
chain = []
for d, items in chain_json["chain"]:
    interp = {tuple(a): (M, v) for a, M, v in items}
    chain.append((d, interp))
remaining = list(rules)
for d, interp in chain:
    ok, strict = check_interp(remaining, interp, d)
    assert ok and strict
    remaining = [x for x in remaining
                 if not compose(x[1], interp, d)[1][0] > compose(x[2], interp, d)[1][0]]
assert len(remaining) == chain_json["remaining"], len(remaining)
print(f"m3_b_s8 SRS: PASS simulation lemma for 3 <= n < 3000; MI chain removes "
      f"{len(rules) - len(remaining)} of {len(rules)} rules, {len(remaining)} remain (as recorded)")
