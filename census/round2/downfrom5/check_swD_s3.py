"""swD_s3: P = sigma o D (D = round-1 perm_d), sigma swaps 3<->4, 11<->12, 14<->15 mod 20.
Seed 3.  Tier 2: the set {n != 3 mod 4} is P-closed, 3 is outside, P(3) = 2 inside."""
import sys
from _common import get, D, sigma, residue_graph, closure, separates, is_affine_on_classes, bijective_window
s = get("swD_s3"); P = s["step"]; sg = sigma(20, [3, 11, 14])
ok = True
def claim(name, c):
    global ok
    print(("PASS " if c else "FAIL ") + name); ok = ok and c
claim("step = sigma(D(n)), |P-D|<=1 on [1,2e5]",
      all(P(n) == sg(D(n)) and abs(P(n) - D(n)) <= 1 for n in range(1, 200001)))
claim("P affine on classes mod 32", is_affine_on_classes(P, 32))
claim("P bijective on window", bijective_window(P, 100000))
A = {0, 1, 2}
succ = residue_graph(P, 4, 32)
claim("{n != 3 mod 4} closed (exact residue graph mod 4)", all(succ[x] <= A for x in A))
claim("3 = 3 mod 4 and P(3) = 2", P(3) == 2)
claim("no separator for K = 1..3", not any(separates(P, 32, 3, K) for K in (1, 2, 3)))
claim("no 5-adic separator mod 5^k, k<=4", not any(separates(P, 32, 3, 5 ** k) for k in range(1, 5)))
x = 3; xs = [3]; falls = 0
for _ in range(3000):
    y = P(x); falls += y < x; x = y; xs.append(x)
claim("orbit not monotone: >= 300 falls in 3000 steps", falls >= 300)
print("  prefix:", xs[:14], "falls:", falls)
succ80 = residue_graph(P, 80, 32)
C80 = closure(succ80, P(3) % 80)
ev = {x for x in C80 if x % 2 == 0}
def has_cycle(nodes, g):
    indeg = {v: 0 for v in nodes}
    for v in nodes:
        for w in g[v]:
            if w in nodes: indeg[w] += 1
    q = [v for v in nodes if indeg[v] == 0]; c = 0
    while q:
        v = q.pop(); c += 1
        for w in g[v]:
            if w in nodes:
                indeg[w] -= 1
                if indeg[w] == 0: q.append(w)
    return c < len(nodes)
claim("evens rise (P(n) > n, n even <= 1e5)", all(P(n) > n for n in range(2, 100001, 2)))
claim("rise-only (even) cycle inside the mod-80 trap: falls are not congruence-forced", has_cycle(ev, succ80))
sys.exit(0 if ok else 1)
