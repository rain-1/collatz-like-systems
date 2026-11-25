"""swT9_15_s8: Q = sigma_{9,15} o T, seed 8.  Exact congruence certificate mod 36.
Exit 0 iff every computational claim in swT9_15_s8.md holds."""
import sys
from _common import get, T, sigma, residue_graph, closure, separates, \
    is_affine_on_classes, bijective_window
s = get("swT9_15_s8"); Q = s["step"]; sg = sigma(18, [9, 15])
ok = True
def claim(name, c):
    global ok
    print(("PASS " if c else "FAIL ") + name); ok = ok and c

claim("step = sigma(T(n)) and |Q-T|<=1 on [1,3e5]",
      all(Q(n) == sg(T(n)) and abs(Q(n) - T(n)) <= 1 for n in range(1, 300001)))
claim("sigma is an involution on [1,1e5]", all(sg(sg(n)) == n for n in range(1, 100001)))
claim("Q affine on classes mod 27", is_affine_on_classes(Q, 27))
claim("Q bijective on window", bijective_window(Q, 100000))
# certificate: S' = sigma(S), S = odd or 2 mod 12; membership depends on n mod 36
A = {x for x in range(36) if (sg(x + 36) % 2 == 1) or (sg(x + 36) % 12 == 2)}
claim("membership in S' is periodic mod 36 (checked on [1,1e5])",
      all(((n % 36) in A) == (sg(n) % 2 == 1 or sg(n) % 12 == 2) for n in range(1, 100001)))
succ = residue_graph(Q, 36, 27)
claim("S' forward closed under Q (exact residue graph mod 36)", all(succ[x] <= A for x in A))
claim("8 not in S', Q(8)=11 in S'", 8 % 36 not in A and Q(8) == 11 and 11 % 36 in A)
print("  |S' mod 36| =", len(A), sorted(A))
# minimality / lower-tier failures
claim("no separating union of classes mod K for K=1..35",
      not any(separates(Q, 27, 8, K) for K in range(1, 36)))
claim("no 2-adic separator mod 2^k, k<=10",
      not any(separates(Q, 27, 8, 2 ** k) for k in range(1, 11)))
claim("no 3-adic separator mod 3^k, k<=6",
      not any(separates(Q, 27, 8, 3 ** k) for k in range(1, 7)))
# the orbit is not monotone: falls keep occurring in the computed range
x = 8; falls = []; xs = [8]
for i in range(3000):
    y = Q(x)
    if y < x: falls.append(i)
    x = y; xs.append(x)
claim("orbit has falls (>= 300 in first 3000 steps, one after step 2950)",
      len(falls) >= 300 and falls[-1] > 2950)
print("  first terms:", xs[:16], " #falls:", len(falls), "last fall at step", falls[-1])
# rise-only cycle exists inside the trap (so congruences cannot force falls): Q(1)=1, 1 in S'
claim("Q(1)=1 and 1 in S' (rise self-loop in trap)", Q(1) == 1 and 1 in A)
sys.exit(0 if ok else 1)
