"""Check for auto_mix3_s7.

1. The five branches define a permutation of the positive integers.
2. Tier-1 proof: T(9*2^(k+1)) = 9*2^k for k >= 0 and 9 -> 14 -> 22 -> 16 -> 10 -> 7,
   so 7 has the infinite backward orbit 9*2^k (k >= 0) plus 5 more points.
   (The algebra: 6 | 9*2^(k+1), and 6|n -> n/2.)
3. The base-3 automaton certificate found by the CEGAR search (7 states) is
   verified exactly; its accepted set equals {n : 3 does not divide n} minus
   E = {5, 7, 8, 10, 14, 16, 22} (checked on n < 3^9); E contains the part
   {7, 10, 14, 16, 22} of the backward orbit of 7 prime to 3, plus 5 -> 8.
4. No base-3 certificate with <= 4 states (complete backtracking).
   (SAT, offline: none with <= 6 states; see the .md.)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from autolib import check_partition, make_step, certifies, accepts, exhaust
from systems import get

S = get("auto_mix3_s7")
br = S["branches"]
T = S["step"]
check_partition(br)
check_partition([(v, s, u, r) for u, r, v, s in br])
print("1. permutation: ok")

for k in range(0, 200):
    assert T(9 * 2 ** (k + 1)) == 9 * 2 ** k
chain = [9, 14, 22, 16, 10, 7]
assert all(T(a) == b for a, b in zip(chain, chain[1:]))
# formula check of the branch used on 9*2^(k+1): n = 6q, T = 3q = n/2
assert br[0] == (6, 0, 3, 0)
print("2. backward orbit of 7 contains 9*2^k for all k (infinite): ok")

d = {"base": 3, "delta": [[0, 1, 4], [6, 2, 6], [3, 5, 3], [3, 5, 5], [3, 6, 3],
                          [3, 5, 5], [3, 3, 5]], "acc": {1, 2, 4, 5}}
assert certifies(d, br, 7) is None
E = {5, 7, 8, 10, 14, 16, 22}
for n in range(1, 3 ** 9):
    assert accepts(d, n) == (n % 3 != 0 and n not in E), n
Ti = make_step([(v, s, u, r) for u, r, v, s in br])
b, x = [7], 7
for _ in range(60):
    x = Ti(x)
    b.append(x)
assert {n for n in b if n % 3} == {7, 10, 14, 16, 22}   # 5, 8 are extra, harmless
print("3. 7-state base-3 certificate = (3 does not divide n) minus E: ok")

f, x = [], 7
for _ in range(40):
    x = T(x)
    f.append(x)
assert exhaust(3, br, 7, 4, 400, f, b[1:40]) is None
print("4. no base-3 certificate with <= 4 states: ok")
# base-2 upper bound: {3 does not divide n} minus {7,10,14,16,22}, product automaton
E2 = {7, 10, 14, 16, 22}
trie, fin = [{}], set()
for n in E2:
    v = 0
    for c in format(n, "b"):
        dd = int(c)
        if dd not in trie[v]:
            trie[v][dd] = len(trie)
            trie.append({})
        v = trie[v][dd]
    fin.add(v)
idx, delta, todo = {(0, 0): 0}, [None], [(0, 0)]
while todo:
    st = todo.pop()
    r, v = st
    row = []
    for dd in (0, 1):
        t = ((2 * r + dd) % 3, trie[v].get(dd, -1) if v >= 0 else -1)
        if t not in idx:
            idx[t] = len(delta)
            delta.append(None)
            todo.append(t)
        row.append(idx[t])
    delta[idx[st]] = row
acc2 = {i for (r, v), i in idx.items() if r != 0 and not (v >= 0 and v in fin)}
from autolib import minimize
d2 = minimize(dict(base=2, delta=delta, acc=acc2))
assert certifies(d2, br, 7) is None
print(f"5. base-2 certificate with {len(d2['delta'])} states verified (SAT lower bound: >= 10)")
print("ALL OK")
