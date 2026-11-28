"""Check for classification.md (principles P1, P2, the degenerate lemma, lemma N1).

 (P1/N1) exact degree identity deg T(f) = deg f + deg g - 1 in the nonzero branch when
         deg f + deg g > deg h; deg drop 1 in the zero branch  -- random, F_2 and F_3
 (P2)    deg g <= 1  =>  deg T(f) <= max(deg f, deg h - 1)        -- random, F_2, F_3, F_5
 (DEG)   degenerate F_2 multipliers g(0)=0, deg g <= 2: for every (g,h) with deg h <= 4 the
         claimed GLOBAL verdict is confirmed: 'true' cases by exhaustive check that every f of
         degree < 9 stays in the finite set {deg <= max(8, deg h) + 2} (so is eventually periodic);
         'false' cases by exhibiting an odd f whose degree increases at each of 200 steps.
"""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from polylib import Fp, Tp, T2, deg2, clmul

random.seed(3)
fails = 0
for p in (2, 3, 5):
    F = Fp(p)
    for _ in range(4000):
        dg = random.randint(0, 4)
        g = F.tr([random.randrange(1, p)] + [random.randrange(p) for _ in range(dg - 1)] +
                 ([random.randrange(1, p)] if dg >= 1 else []))
        h = F.tr([1] + [random.randrange(p) for _ in range(random.randint(0, 5))])
        f = F.tr([random.randrange(p) for _ in range(random.randint(0, 30))])
        if not f:
            continue
        Tf = Tp(F, f, g, h)
        df, dg_, dh = len(f) - 1, len(g) - 1, len(h) - 1
        dT = len(Tf) - 1
        if f[0] == 0:
            if dT != df - 1:
                fails += 1
        elif df + dg_ > dh and dT != df + dg_ - 1:
            fails += 1
        if dg_ <= 1 and dT > max(df, dh - 1):
            fails += 1
print('P1/P2 random: fails', fails)


def Tdeg(f, m, h):
    """F_2 map with m(0)=0 (no admissibility division on the odd branch): odd f -> (m f + h)/t"""
    if f & 1 == 0:
        return f >> 1
    v = clmul(m, f) ^ h
    assert v & 1 == 0
    return v >> 1


# degenerate: m = t*m1, h = t*h1 ; deg m <= 2  =>  m1 in {0, 1, t, 1+t}
verdict = {}
for m1 in (0, 1, 2, 3):
    for h1 in range(0, 1 << 4):
        m = m1 << 1
        h = h1 << 1
        if m1 & 1 and not h1 & 1:
            claim = (m1 == 1)           # g1(0)=1,h1(0)=0: true iff g1 = 1
        elif m1 == 2 and h1 & 1:
            claim = False
        else:
            claim = True
        if claim:
            B = max(8, deg2(h)) + 2   # intermediate (undivided) states may be 1-2 higher
            for f0 in range(1, 1 << 9):
                f = f0
                for _ in range(3000):
                    f = Tdeg(f, m, h)
                    if f.bit_length() - 1 > B:
                        fails += 1
                        break
        else:
            # find an odd f with strictly increasing degree for 200 steps
            ok = False
            for f0 in range(1, 1 << 8, 2):
                f = f0
                good = True
                for _ in range(200):
                    g_ = Tdeg(f, m, h)
                    if deg2(g_) <= deg2(f):
                        good = False
                        break
                    f = g_
                if good:
                    ok = True
                    break
            if not ok:
                fails += 1
        verdict[(m1, h1)] = claim
print('degenerate cases checked:', len(verdict), 'GLOBAL-false cases:',
      sorted(k for k, v in verdict.items() if not v)[:8], '... fails', fails)
sys.exit(1 if fails else 0)
