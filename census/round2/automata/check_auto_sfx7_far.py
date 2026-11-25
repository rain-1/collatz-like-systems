"""Check for auto_sfx7_far: seed y = 2^21 + 5 for the SFX7 permutation.

1. y lies on the backward orbit of 17: T^44(y) = 17 (and the closed form of
   that backward stretch: x_{-4i-4} = 2^(2i+1)+5, x_{-4i-5} = 2^(2i+2)+10,
   x_{-4i-6} = 2^(2i+1)+7, x_{-4i-7} = 2^(2i+2)+14, verified symbolically on
   words 1 0^m W).
2. Tier-2 certificate C = (6 classes mod 256) u {T(y), ..., T^44(y) = 17} is
   verified exactly (closure for all integers), y not in C, T(y) in C.
3. Fooling set: the 10 words 1 0^(2a), a = 0..9, are pairwise separated by
   suffixes 0^c 1110; one completion lies on the forward orbit of y (forced
   in), the other on its backward orbit (forced out).  Hence every
   certificate automaton has >= 10 states.
4. Upper bound: the exact-orbit automaton (suffix_orbit.exact_dfa), minimised,
   is a verified certificate; its size is printed.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..")))
from autolib import (suffix_branches, make_step, certifies, check_fooling_set,
                     minimize)
from systems import SFX7

br = suffix_branches(SFX7)
T = make_step(br)
Ti = make_step([(v, s, u, r) for u, r, v, s in br])
I = 10
y = 2 ** (2 * I + 1) + 5
J = 4 * I + 4

# 1. backward closed form, symbolically: words 1 0^m W, m >= 2
inv = [(b, a) for a, b in SFX7]


def rewrite(rules, word):
    hits = [(a, b) for a, b in rules if word.endswith(a)]
    assert len(hits) == 1
    a, b = hits[0]
    assert len(a) <= len(word)
    return word[:-len(a)] + b


# backward in time: 0^m 101 <- (T^-1) ... the inverse rules act on suffixes only;
# the four inverse steps from "00101" (= ...0^m 101 with m >= 2) give 0^m 1010,
# then 0^m 111, then 0^m 1110, then 0^(m+2) 101 -- checked on the visible part
w = "00101"
seq = []
for _ in range(4):
    w = rewrite(inv, w)
    seq.append(w)
assert seq == ["001010", "00111", "001110", "0000101"], seq
x = 17
for j in range(1, J + 1):
    x = Ti(x)
assert x == y
x = y
for _ in range(J):
    x = T(x)
assert x == 17
print("1. T^44(2^21+5) = 17; backward closed form: ok")

# 2. congruence + finite table certificate
A = {81, 83, 162, 166, 209, 211}
seg, x = [], y
for _ in range(J):
    x = T(x)
    seg.append(x)
trie, fin = [{}], set()
for n in seg:
    v = 0
    for c in format(n, "b"):
        d = int(c)
        if d not in trie[v]:
            trie[v][d] = len(trie)
            trie.append({})
        v = trie[v][d]
    fin.add(v)
idx, delta, acc, todo = {(0, 0): 0}, [None], set(), [(0, 0)]
while todo:
    s = todo.pop()
    r, v = s
    row = []
    for d in (0, 1):
        t = ((2 * r + d) % 256, trie[v].get(d, -1) if v >= 0 else -1)
        if t not in idx:
            idx[t] = len(delta)
            delta.append(None)
            todo.append(t)
        row.append(idx[t])
    delta[idx[s]] = row
for (r, v), i in idx.items():
    if r in A or (v >= 0 and v in fin and v != 0):
        acc.add(i)
dC = dict(base=2, delta=delta, acc=acc)
assert certifies(dC, br, y) is None
print("2. congruence(6 classes mod 256) + 44-element table certifies y: ok;",
      "minimal DFA of that set:", len(minimize(dC)["delta"]), "states")

# 3. fooling set
F, x = set(), y
for _ in range(J + 400):
    x = T(x)
    F.add(x)
B, x = {y}, y
for _ in range(400):
    x = Ti(x)
    B.add(x)
words = ["1" + "0" * (2 * a) for a in range(I)]
wit = {}
for a in range(I):
    for b in range(a + 1, I):
        wit[(a, b)] = ("0" * (2 * (I - 1 - b)) + "1110", 0)
assert check_fooling_set(2, words, wit, lambda n: n in F, lambda n: n in B) == I
print(f"3. fooling set of size {I}: every certificate has >= {I} states: ok")

# 4. exact-orbit automaton upper bound
from suffix_orbit import decompose, exact_dfa  # noqa: E402
stem, pump = decompose([list(r) for r in SFX7], T(y))
e = exact_dfa(stem, pump)
dE = minimize(dict(base=2, delta=e["transitions"], acc=set(e["accepting"])))
assert certifies(dE, br, y) is None
print(f"4. exact-orbit automaton, minimised: {len(dE['delta'])} states, verified: ok")
print("ALL OK")
