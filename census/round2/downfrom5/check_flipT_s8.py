"""flipT_s8: flipT(n) = T(n+3) - 3 (exact conjugacy to the 1932 map on Z_{>=4}).
Checks the conjugacy, the invariance of {1,2,3}, orbit correspondence, and
that among all (c0,c1,c2) maps n -> (2n+c0)/3, (4n+c1)/3, (4n+c2)/3 (by n mod 3)
the bijections of Z_{>0} are exactly T, S=perm_swap, flipT, S(n+3)-3."""
import sys
from _common import get, T, first_return
s = get("flipT_s8"); P = s["step"]
ok = True
def claim(name, c):
    global ok
    print(("PASS " if c else "FAIL ") + name); ok = ok and c
claim("flipT(n) = T(n+3)-3 on [1,3e5]", all(P(n) == T(n + 3) - 3 for n in range(1, 300001)))
claim("flipT = 3q->2q-1, 3q+1->4q+2, 3q+2->4q+4",
      all(P(3*q) == 2*q-1 and P(3*q+1) == 4*q+2 and P(3*q+2) == 4*q+4 for q in range(1, 100000)) and P(1) == 2 and P(2) == 4)
claim("T permutes {1,2,3}", sorted(T(n) for n in (1, 2, 3)) == [1, 2, 3])
x, y = 8, 11; good = True
for _ in range(20000):
    x, y = P(x), T(y)
    good &= (x == y - 3)
claim("flipT^k(8) = T^k(11) - 3 for k <= 2e4", good)
claim("T(8) = 11", T(8) == 11)
claim("no return to 8 in 1e5 steps (evidence only)", first_return(P, 8, 100000) is None)

# classification of bijective members of the constant family
def mk(c0, c1, c2):
    return lambda n: (2*n + c0)//3 if n % 3 == 0 else ((4*n + c1)//3 if n % 3 == 1 else (4*n + c2)//3)
bij = []
for c0 in range(-30, 31, 3):
    for c1 in range(-31, 32, 3):
        for c2 in range(-32, 33, 3):
            f = mk(c0, c1, c2)
            vals = [f(n) for n in range(1, 3001)]
            if min(vals) < 1 or len(set(vals)) < len(vals): continue
            if set(range(1, 1001)) <= set(vals): bij.append((c0, c1, c2))
claim("bijective members with |c|<=32: exactly T, S, flipT, S(n+3)-3",
      sorted(bij) == sorted([(0, -1, 1), (0, 5, -5), (-3, 2, 4), (-3, 8, -2)]))
print("  bijective:", bij)
sys.exit(0 if ok else 1)
