"""Check for auto_sfx7_s17 (exact integers; exits 0 iff every part passes).

1. The seven rules define a permutation of the positive integers.
2. Closed form: for every binary word X (checked symbolically: the rules read
   at most 6 final bits, and each of the four words below ends in a matched
   suffix that lies inside the displayed part), X.10011 -> X.100010 ->
   X.10001 -> X.10100110 -> X10.10011.  Plus 17 -> 166 -> 83 = [10.10011].
3. Tier-2 certificate: A = {81,83,162,166,209,211} mod 256 is forward closed,
   17 is not in A, T(17) = 166 is in A.
4. No union of residue classes modulo any M < 256 is a certificate
   (exhaustive residue-graph reachability), so 256 is the least modulus.
5. Automata: an explicit 5-state certificate is verified exactly, and the
   complete backtracking search finds no certificate with <= 4 states.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from autolib import (suffix_branches, check_partition, make_step, certifies,
                     exhaust)
from systems import SFX7

br = suffix_branches(SFX7)
T = make_step(br)
check_partition(br)
check_partition([(v, s, u, r) for u, r, v, s in br])
print("1. permutation: ok")


def rewrite(word):
    """Apply the unique rule whose input suffix ends `word` (word long enough)."""
    hits = [(a, b) for a, b in SFX7 if word.endswith(a)]
    assert len(hits) == 1, (word, hits)
    a, b = hits[0]
    return word[:-len(a)] + b, a


# symbolic check: track which part of the word each rule consumes
w = "10011"
cycle = []
for _ in range(4):
    w2, a = rewrite(w)
    assert len(a) <= len(w), "rule would reach into the unknown prefix X"
    cycle.append(w2)
    w = w2
assert cycle == ["100010", "10001", "10100110", "1010011"], cycle
# the last word is "10" + "10011": one copy of V = "10" inserted after X
assert T(17) == 166 and T(166) == 83 and format(83, "b") == "10" + "10011"
# exhaustive confirmation on all prefixes X of length <= 14 (informative)
for X in range(1, 1 << 14):
    x = X * 32 + 0b10011
    y = T(T(T(T(x))))
    assert y == (X * 4 + 0b10) * 32 + 0b10011
print("2. closed form X10011 -> X1010011 (4 steps): ok")

A = {81, 83, 162, 166, 209, 211}
for r in A:
    for t in range(64):          # 64 = largest input modulus, so this is exhaustive
        assert T(r + 256 * t) % 256 in A, (r, t)
assert 17 % 256 not in A and T(17) % 256 in A
dA = dict(base=2, delta=[[(2 * r) % 256, (2 * r + 1) % 256] for r in range(256)], acc=A)
assert certifies(dA, br, 17) is None
print("3. congruence certificate mod 256 (6 classes): ok")


def periodic_certificate_exists(M):
    g = [set() for _ in range(M)]
    for n in range(1, 64 * M + 1):
        g[n % M].add(T(n) % M)
    start = T(17) % M
    seen, todo = {start}, [start]
    while todo:
        x = todo.pop()
        for y in g[x]:
            if y not in seen:
                seen.add(y)
                todo.append(y)
    return 17 % M not in seen


bad = [M for M in range(2, 256) if periodic_certificate_exists(M)]
assert bad == [], bad
assert periodic_certificate_exists(256)
print("4. no periodic certificate for any modulus M < 256: ok")

d5 = {"base": 2, "delta": [[1, 1], [2, 0], [3, 3], [1, 4], [4, 0]], "acc": {4}}
assert certifies(d5, br, 17) is None
fwd, x = [], 17
for _ in range(40):
    x = T(x)
    fwd.append(x)
Ti = make_step([(v, s, u, r) for u, r, v, s in br])
bwd, x = [], 17
for _ in range(40):
    x = Ti(x)
    bwd.append(x)
assert exhaust(2, br, 17, 4, 300, fwd, bwd) is None
print("5. 5-state automaton certificate verified; no certificate with <= 4 states: ok")
print("ALL OK")
