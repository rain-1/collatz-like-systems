"""twochanW_s8: permutation realising W(m) = T(m) (3|m), 3T(m) (3!|m) on the odd
numbers n = 2m-1, fed from the evens.  Seed 8."""
import sys
from math import gcd
from _common import get, T, residue_graph, is_affine_on_classes, bijective_window
s = get("twochanW_s8"); P = s["step"]
ok = True
def claim(name, c):
    global ok
    print(("PASS " if c else "FAIL ") + name); ok = ok and c
# branch table: (input modulus, residue, output modulus, output residue)
rows = [(6, 1, 24, 5), (6, 3, 24, 17), (6, 5, 4, 3), (4, 0, 2, 0), (8, 2, 12, 1), (8, 6, 12, 9)]
def first(m, r): return r if r > 0 else m
claim("each branch: k-th element of input class -> k-th element of output class",
      all(P(first(mi, ri) + mi * k) == first(mo, ro) + mo * k for mi, ri, mo, ro in rows for k in range(2000)))
def partition(cls):
    L = 1
    for m, _ in cls: L = L * m // gcd(L, m)
    return all(sum(1 for m, r in cls if x % m == r % m) == 1 for x in range(L))
claim("input classes partition Z", partition([(a, b) for a, b, _, _ in rows]))
claim("output classes partition Z", partition([(c, d) for _, _, c, d in rows]))
claim("bijective on window", bijective_window(P, 100000))
W = lambda m: T(m) if m % 3 == 0 else 3 * T(m)
claim("P(2m-1) = 2W(m)-1 for m <= 1e5", all(P(2*m - 1) == 2 * W(m) - 1 for m in range(1, 100001)))
def acc(f, m):   # first iterate (>=1 step) that is not a multiple of 3
    x = f(m)
    while x % 3 == 0: x = f(x)
    return x
claim("W_acc(m) = 2*T_acc(m) for 3!|m <= 1e5",
      all(acc(W, m) == 2 * acc(T, m) for m in range(1, 100001) if m % 3))
# certificate S = odd or 2 mod 4 or 4 mod 8 (union of classes mod 8); exact graph mod 24
Sres = {x for x in range(24) if x % 2 == 1 or x % 4 == 2 or x % 8 == 4}
claim("P affine on classes mod 24", is_affine_on_classes(P, 24))
succ = residue_graph(P, 24, 24)
claim("S closed under P (exact mod 24), 8 not in S, P(8)=4 in S",
      all(succ[x] <= Sres for x in Sres) and 8 % 24 not in Sres and P(8) == 4)
claim("odd numbers closed", all(succ[x] <= {y for y in range(24) if y % 2} for x in range(1, 24, 2)))
claim("rises on odds land in 5 mod 6 (forced fall next)",
      all(P(n) % 6 == 5 and P(n) > n for n in range(1, 60000) if n % 6 in (1, 3)))
claim("n = 5 mod 6 falls: P(n) = (2n-1)/3 < n", all(P(n) < n for n in range(5, 60000, 6)))
x = 8; xs = [8]
for _ in range(3000): x = P(x); xs.append(x)
signs = ''.join('R' if xs[i+1] > xs[i] else 'F' for i in range(3000))
claim("orbit prefix 8,4,2,1,5,3,17,11,7", xs[:9] == [8, 4, 2, 1, 5, 3, 17, 11, 7])
claim("no 'RR' after the odd channel is entered (step 3)", 'RR' not in signs[3:])
print("  sign word:", signs[:60])
sys.exit(0 if ok else 1)
