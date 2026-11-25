"""Referee's independent check for the automata lens (round 2).

Uses its own string-level suffix rewriter and its own map implementations,
cross-checked against systems.py step functions.  Exact integers.  Exit 0
iff every part passes.

R1. sfx7: string rewriter == systems step on 1..2^16; permutation on 1..2^14.
R2. sfx7 tier-1 lemma: T^4(32X+19) = 128X+83 = 4n+7 for every X >= 0
    (symbolic on the word X.10011, the rules read only the displayed bits,
    and also checked numerically for X < 2^14); T^2(17) = 83 = 32*2+19;
    hence T^(2+4k)(17) = (83+7/3)4^k - 7/3, strictly increasing.
R3. sfx7: the 6 classes mod 256 are closed (independent rewriter).
R4. far: T^44(2^21+5) = 17 and the backward closed form for i = 1..10.
R5. far: fooling-set lower bound I = 10 re-checked from raw orbit sets.
R6. sfx7: independent brute force over ALL 2-symbol DFAs with <= 4 states:
    none satisfies the necessary conditions (fwd orbit accepted, bwd orbit
    and 17 rejected, closure on 1..3000), so no certificate with <= 4 states.
R7. mix3: bijection, T(9*2^(k+1)) = 9*2^k for k < 300, 9->14->22->16->10->7.
R8. 1932: map = Collatz 1932 permutation; residue graph strongly connected
    for every modulus 2..300 (evidence for certificate_search_proofs.txt s5).
"""
import itertools
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from systems import get

RULES = [("00", "00"), ("001", "100110"), ("00101", "1110"), ("10", "1"),
         ("10101", "10110"), ("11", "010"), ("1101", "000110")]


def rw(word, rules=RULES):
    hits = [(a, b) for a, b in rules if word.endswith(a)]
    assert len(hits) == 1, word
    a, b = hits[0]
    return word[: len(word) - len(a)] + b, len(a)


def Ts(n):
    w = "0" * 8 + format(n, "b")          # leading zeros are harmless padding
    return int(rw(w)[0], 2)


S17 = get("auto_sfx7_s17")
T = S17["step"]
for n in range(1, 1 << 16):
    assert Ts(n) == T(n), n
img = {T(n) for n in range(1, 1 << 14)}
assert len(img) == (1 << 14) - 1
INV = [(b, a) for a, b in RULES]
for n in range(1, 1 << 14):
    assert T(int(rw("0" * 8 + format(n, "b"), INV)[0], 2)) == n
print("R1 ok")

w = "10011"
for _ in range(4):
    w, used = rw(w)
    assert used <= len(w)
assert w == "1010011"   # X.10011 -> X.10.10011, rules never touched X
for X in range(1 << 14):
    n = 32 * X + 19
    assert T(T(T(T(n)))) == 4 * n + 7 == 128 * X + 83
assert T(T(17)) == 83 and 83 % 32 == 19
x = 17
seq = [17]
for _ in range(2 + 4 * 60):
    x = T(x)
    seq.append(x)
for k in range(61):
    assert 3 * seq[2 + 4 * k] == 256 * 4 ** k - 7
print("R2 ok: T^4 = 4n+7 on 19 mod 32, T^2(17)=83")

A = {81, 83, 162, 166, 209, 211}
for r in A:
    for t in range(64):
        assert Ts(r + 256 * t) % 256 in A
print("R3 ok")

y = 2 ** 21 + 5
x = y
for _ in range(44):
    x = Ts(x)
assert x == 17
back = [17]
x = 17
for _ in range(44):
    x = int(rw("0" * 8 + format(x, "b"), INV)[0], 2)
    back.append(x)
for i in range(1, 11):
    assert back[4 * i + 4] == 2 ** (2 * i + 1) + 5
    assert back[4 * i + 5] == 2 ** (2 * i + 2) + 10 if 4 * i + 5 <= 44 else True
    assert back[4 * i + 6] == 2 ** (2 * i + 1) + 7 if 4 * i + 6 <= 44 else True
    assert back[4 * i + 7] == 2 ** (2 * i + 2) + 14 if 4 * i + 7 <= 44 else True
print("R4 ok")

fwd = set()
x = y
for _ in range(2000):
    x = T(x)
    fwd.add(x)
bwd = {y}
x = y
for _ in range(200):
    x = int(rw("0" * 8 + format(x, "b"), INV)[0], 2)
    bwd.add(x)
I = 10
for a in range(I):
    for b in range(a + 1, I):
        z = "0" * (2 * (I - 1 - b)) + "1110"
        assert int("1" + "0" * (2 * a) + z, 2) in fwd
        assert int("1" + "0" * (2 * b) + z, 2) in bwd
print("R5 ok")


def brute(k, Tm, seed, fwdpts, bwdpts, N):
    words = {}

    def run(delta, n):
        s = 0
        for c in format(n, "b"):
            s = delta[s][c == "1"]
        return s
    for flat in itertools.product(range(k), repeat=2 * k):
        delta = [flat[2 * i: 2 * i + 2] for i in range(k)]
        must1 = {run(delta, n) for n in fwdpts}
        must0 = {run(delta, n) for n in bwdpts}
        if must1 & must0:
            continue
        for mask in range(1 << k):
            acc = {i for i in range(k) if mask >> i & 1}
            if not must1 <= acc or acc & must0:
                continue
            if all(run(delta, Tm(n)) in acc for n in range(1, N)
                   if run(delta, n) in acc):
                return delta, acc
    return None


fw, x = [], 17
for _ in range(60):
    x = T(x)
    fw.append(x)
bw, x = [17], 17
for _ in range(60):
    x = int(rw("0" * 8 + format(x, "b"), INV)[0], 2)
    bw.append(x)
for k in range(1, 5):
    assert brute(k, T, 17, fw, bw, 3000) is None, k
print("R6 ok: no binary certificate with <= 4 states (independent brute force)")

M3 = get("auto_mix3_s7")
T3 = M3["step"]


def mix(n):
    if n % 6 == 0:
        return n // 2
    if n % 6 == 2:
        return (3 * n + 2) // 2
    if n % 12 == 4:
        return (3 * n - 8) // 4
    if n % 12 == 10:
        return (3 * n - 2) // 4
    return (3 * n + 1) // 2


for n in range(1, 200000):
    assert mix(n) == T3(n)
img = {mix(n) for n in range(1, 12 * 9 * 300)}
assert set(range(1, 300)) <= img
assert len({mix(n) for n in range(1, 50000)}) == 49999
for k in range(300):
    assert mix(9 * 2 ** (k + 1)) == 9 * 2 ** k
c = [9]
for _ in range(5):
    c.append(mix(c[-1]))
assert c == [9, 14, 22, 16, 10, 7]
print("R7 ok")

G = get("auto_1932_s8")["step"]
for n in range(1, 100000):
    e = {0: 2 * n // 3, 1: (4 * n - 1) // 3, 2: (4 * n + 1) // 3}[n % 3]
    assert G(n) == e
for M in range(2, 301):
    adj = [set() for _ in range(M)]
    for n in range(1, 3 * M + 1):
        adj[n % M].add(G(n) % M)
    radj = [set() for _ in range(M)]
    for a in range(M):
        for b in adj[a]:
            radj[b].add(a)
    for g in (adj, radj):
        seen, todo = {0}, [0]
        while todo:
            u = todo.pop()
            for v in g[u]:
                if v not in seen:
                    seen.add(v)
                    todo.append(v)
        assert len(seen) == M, M
print("R8 ok: 1932 residue graph strongly connected for M = 2..300")
print("ALL OK")
