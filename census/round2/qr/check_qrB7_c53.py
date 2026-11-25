"""qrB7_c53: build the LSB-first basin automaton from the carry transducer, minimise it,
verify it, and verify the finite ingredients of the non-periodicity proof."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from qrlib import famB, cycles_in, basin_table, basin, subgroup

q, c1, c3 = 7, 5, 3
C = {1: c1, 3: c3}
T = famB(q, c1, c3)
BOX = q * max(c1, c3)                      # 35
ok = all(1 <= T(n) <= BOX for n in range(1, BOX + 1))
cyc = cycles_in(T, range(1, BOX + 1))
cid = basin_table(T, cyc)
mins = sorted(min(c) for c in cyc)
ok &= mins == [1, 3, 5, 7]
QR = {1, 2, 4}
assert subgroup([2], q) == QR
# class structure: 7|n -> {7,14}; QR -> 1; NQR -> 3 or 5 (two cycles in one coset)
for n in range(1, BOX + 1):
    b = basin(T, cid, n)
    if n % 7 == 0: ok &= b == 7
    elif n % 7 in QR: ok &= b == 1
    else: ok &= b in (3, 5)
ok &= (3 % 7 not in QR) and (5 % 7 not in QR) and 3 * pow(5, -1, 7) % 7 in QR  # same coset

# ---- transducer: state (s, b) means T^k(n) = 2*(n >> (k+1)) + b + s, b = bit k of n
def step(st, b2):
    s, b = st
    r = (2 * b2 + b + s) % 4
    add = q * C[r] if r % 2 else 0
    assert (b + s + add) % 2 == 0
    return ((b + s + add) // 2, b2)

START = "S"
trans, states, fr = {}, {START}, [START]
while fr:
    st = fr.pop()
    for bit in (0, 1):
        nt = (0, bit) if st == START else step(st, bit)
        trans[st, bit] = nt
        if nt not in states:
            states.add(nt); fr.append(nt)
def out(st):
    return None if st == START or st[0] + st[1] == 0 else basin(T, cid, st[0] + st[1])
ok &= all(st == START or st[0] + st[1] <= BOX + 1 for st in states)

# Moore minimisation
part = {s: out(s) for s in states}
while True:
    sig = {s: (part[s], part[trans[s, 0]], part[trans[s, 1]]) for s in states}
    ids = {}
    new = {s: ids.setdefault(sig[s], len(ids)) for s in states}
    if len(set(new.values())) == len(set(part.values())):
        part = new; break
    part = new
# canonical numbering by BFS from start
order, seen = [], {part[START]}
qu = [part[START]]
rep = {}
for s in states: rep.setdefault(part[s], s)
while qu:
    p = qu.pop(0); order.append(p)
    for bit in (0, 1):
        t = part[trans[rep[p], bit]]
        if t not in seen: seen.add(t); qu.append(t)
num = {p: i for i, p in enumerate(order)}
D = {num[p]: (num[part[trans[rep[p], 0]]], num[part[trans[rep[p], 1]]], out(rep[p])) for p in order}

def run_min(n):
    st = 0
    while n:
        st = D[st][n & 1]; n >>= 1
    return D[st][2]
for n in range(1, 1 << 18):
    if run_min(n) != basin(T, cid, n):
        print("FAIL dfa at", n); ok = False; break
# reading extra high zeros never changes the output (padding invariance), checked on the min DFA
ok &= all(D[s][2] is None or D[D[s][0]][2] == D[s][2] for s in D if s != 0)

print("minimal LSB-first DFA:", len(D), "states (state 0 = start; row: on0 on1 output)")
for s in sorted(D):
    print(f"  {s:2d}: {D[s][0]:2d} {D[s][1]:2d}  {D[s][2]}")
# non-periodicity witness: for each small modulus M, a pair n == n' (mod M) with basins 3 vs 5
for M in [7, 14, 28, 56, 7 * 3 * 5, 7 * 64 * 9]:
    found = False
    for n in range(1, 4000):
        if n % 7 in (3, 5, 6):
            b = basin(T, cid, n)
            for k in range(1, 40):
                if basin(T, cid, n + k * M) != b:
                    found = True; break
        if found: break
    ok &= found
print("qrB7_c53", "OK" if ok else "FAILED")
sys.exit(0 if ok else 1)
