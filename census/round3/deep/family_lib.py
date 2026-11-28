"""Classification of SPLIT(a,b,d) (see family.md).  Exact integer logic only;
the drift is floating point and used only as a heuristic label."""
import math
from math import gcd


def vals(a, b, d):
    va = 2 if (a + d) % 4 == 0 else 1
    vb = 2 if (3 * b + d) % 4 == 0 else 1
    return va, vb


def certifiable(a, b, d):
    va, vb = vals(a, b, d)
    return a < 2 ** va and b < 2 ** vb


def drift(a, b, d):
    """Mean log-slope per binary digit in the U/O coding (heuristic)."""
    va, vb = vals(a, b, d)
    pOU = 0.5 * (va == 2) + 0.5 * (vb == 2)
    piU = pOU / (0.5 + pOU)
    piO = 1 - piU
    return piU * 0.5 * math.log(0.5) + piO * 0.5 * (
        math.log(a / 2 ** va) + math.log(b / 2 ** vb))


def scale(a, b, d, e):
    """T restricted to eZ (e | d, e odd) is conjugate via n = e m to this member."""
    assert d % e == 0 and e % 2 == 1
    return (a, b, d // e) if e % 4 == 1 else (b, a, d // e)


def classify(a, b, d):
    """Return (cls, info).  cls in P, C, D, K, R, O."""
    va, vb = vals(a, b, d)
    if a == b:
        return 'P', f"parity map {a}n+{d}"
    if certifiable(a, b, d):
        return 'C', "descent (lemmas.md Thm 1)"
    if va == 1 and vb == 1:
        if min(a, b) >= 3:
            return 'D', "every odd value strictly increases"
        c = max(a, b)
        return 'K', f"conjugate to x->x/2,(%dx+%d)/2 on x>=%d" % (c, d * (c - 1) // 2, (1 - d) // 2)
    # reductions: e | gcd(d, a) with b-branch contracting, or e | gcd(d, b) with a contracting
    for (m, other, vo) in ((a, b, vb), (b, a, va)):
        e = gcd(d, m)
        if e > 1 and other < 2 ** vo:
            return 'R', scale(a, b, d, e)
    return 'O', f"drift {drift(a, b, d):+.3f}"


def canonical(a, b, d, depth=0):
    cls, info = classify(a, b, d)
    if cls == 'R' and depth < 10:
        return canonical(*info, depth=depth + 1)
    return (a, b, d), cls, info


if __name__ == '__main__':
    for a in (1, 3, 5, 7):
        for b in (1, 3, 5, 7):
            row = []
            for d in range(1, 16, 2):
                cls, info = classify(a, b, d)
                if cls == 'R':
                    c = canonical(a, b, d)
                    row.append(f"d{d}:R->{c[0]}{c[1]}")
                else:
                    row.append(f"d{d}:{cls}")
            print(a, b, ' '.join(row))
