"""shiftT_s8: J = 3q->2q+2, 3q+1->4q+1, 3q+2->4q+3, seed 8.  Tier 1:
J injective, 2 not in J(Z>0), J^6(2) = 8, so the orbit of 8 is infinite.
Also: census of the constant family F(c0,c1,c2) in a box (seed 8)."""
import sys
from _common import get, T
s = get("shiftT_s8"); J = s["step"]
ok = True
def claim(name, c):
    global ok
    print(("PASS " if c else "FAIL ") + name); ok = ok and c
claim("|J-T| <= 2, J=T off 3Z", all(J(n) - T(n) == (2 if n % 3 == 0 else 0) for n in range(1, 100001)))
claim("image classes: 3q (q>=1) -> evens >= 4; others -> 1,3 mod 4",
      all(J(3*q) == 2*q + 2 and J(3*q+1) % 4 == 1 and J(3*q+2) % 4 == 3 for q in range(1, 100000)))
claim("J injective on [1,2e5]", len({J(n) for n in range(1, 200001)}) == 200000)
claim("2 not in image (only evens come from 3q, and those are >= 4)", J(3) == 4)
chain = [2]
for _ in range(6): chain.append(J(chain[-1]))
claim("J-orbit of 2: 2,3,4,5,7,9,8", chain == [2, 3, 4, 5, 7, 9, 8])
x = 8; seen = {8}; good = True
for _ in range(20000):
    x = J(x); good &= x not in seen; seen.add(x)
claim("first 2e4 iterates of 8 distinct (consistent with proof)", good)

# box census of F(c0,c1,c2) for seed 8
def mk(c0, c1, c2):
    return lambda n: (2*n + c0)//3 if n % 3 == 0 else ((4*n + c1)//3 if n % 3 == 1 else (4*n + c2)//3)
def inverse_point(c, m):
    out = []
    for r, (a, cc) in enumerate([(2, c[0]), (4, c[1]), (4, c[2])]):
        x = 3*m - cc
        if x % a == 0 and x // a >= 1 and (x // a) % 3 == r: out.append(x // a)
    return out
inj_nonsurj = []
for c0 in range(-6, 13, 3):
    for c1 in range(-7, 12, 3):
        for c2 in range(-8, 12, 3):
            c = (c0, c1, c2); f = mk(*c)
            vals = [f(n) for n in range(1, 4000)]
            if min(vals) < 1 or len(set(vals)) < len(vals): continue
            gaps = [m for m in range(1, 50) if not inverse_point(c, m)]
            if not gaps: continue
            # backward chain from 8 must hit a gap
            x, k = 8, 0
            while k < 1000:
                pre = inverse_point(c, x)
                if not pre: break
                x = pre[0]; k += 1
                if x == 8: break
            kind = "gap" if (not inverse_point(c, x) and x in gaps) else ("cycle" if x == 8 else "?")
            inj_nonsurj.append((c, kind, k))
claim("box: 17 injective non-surjective members; seed 8 is periodic (tier 0) or on the orbit of a gap (tier 1)",
      len(inj_nonsurj) == 17 and all(t[1] in ("gap", "cycle") for t in inj_nonsurj))
print("  ", inj_nonsurj)
sys.exit(0 if ok else 1)
