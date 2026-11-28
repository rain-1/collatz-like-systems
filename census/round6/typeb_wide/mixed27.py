"""mb_s3_27:  n = 26 (mod 27) -> (n+1)/27;  else even n -> n/2;  else n -> (3n+1)/2.

Search for exit words W giving homoclinic expanding periodic points y_d (one for every
d >= d0) that follow the ghost cycle C = (-5 -> -7 -> -10), word EEH, d times and then W.
See README section "Mixed base" for the proof; this file is the search plus exact checks.

Branches: D: (n+1)/27 if n = 26 mod 27; H: n/2 if n even (and n != 26 mod 27);
          E: (3n+1)/2 if n odd (and n != 26 mod 27).
"""
from fractions import Fraction as Fr
import itertools, sys

BR = {"D": (Fr(1, 27), Fr(1, 27)), "H": (Fr(1, 2), Fr(0)), "E": (Fr(3, 2), Fr(1, 2))}


def branch_of(x):
    """branch of a rational x with denominator prime to 6 (x mod 54 via inverses)."""
    a, b = x.numerator, x.denominator
    assert b % 2 and b % 3
    r27 = a * pow(b, -1, 27) % 27
    if r27 == 26:
        return "D"
    return "H" if (a * pow(b, -1, 2)) % 2 == 0 else "E"


def step(x):
    A, B = BR[branch_of(x)]
    return A * x + B


def compose(word):
    A, B = Fr(1), Fr(0)
    for c in word:
        a, b = BR[c]
        A, B = a * A, a * B + b
    return A, B


def vp(x, p):
    if x == 0:
        return 10 ** 9
    e, a, b = 0, x.numerator, x.denominator
    while a % p == 0:
        a //= p
        e += 1
    while b % p == 0:
        b //= p
        e -= 1
    return e


def padic_int(x, p, N):
    """residue of x mod p^N for x with v_p(x) >= 0"""
    a, b = x.numerator, x.denominator
    return a * pow(b, -1, p ** N) % p ** N


def follows_pair(word, x2, x3, N=60):
    """Does the pair (x2 in Q_2, x3 in Q_3) follow the word?  x2, x3 rationals used as
    approximations: the parity test uses x2 (2-adic), the mod-27 test uses x3 (3-adic).
    Both components are transported by the same affine maps."""
    for c in word:
        if vp(x2, 2) < 0 or vp(x3, 3) < 0:
            return False
        r27 = padic_int(x3, 3, 3)
        par = padic_int(x2, 2, 1)
        want = "D" if r27 == 26 else ("H" if par == 0 else "E")
        if want != c:
            return False
        A, B = BR[c]
        x2, x3 = A * x2 + B, A * x3 + B
    return True


C = "EEH"
AC, BC = compose(C)
assert AC == Fr(9, 8) and AC * (-5) + BC == -5


def search(maxlen=9):
    found = []
    for L in range(1, maxlen + 1):
        for w in itertools.product("DHE", repeat=L):
            W = "".join(w)
            A, B = compose(W)
            c = A * (-5) + B + 5
            if c == 0 or vp(c, 3) < 3:
                continue
            yinf = (-5 - B) / A          # 2-adic limit: W(yinf) = -5
            if vp(yinf, 2) < 0:
                continue
            if not follows_pair(W, yinf, Fr(-5)):
                continue
            found.append((W, A, c))
        if found:
            break
    return found


if __name__ == "__main__":
    for W, A, c in search():
        print(W, "A_W =", A, " c = W(-5)+5 =", c, " v2(c) =", vp(c, 2), " v3(c) =", vp(c, 3))


def y(d):
    """closed form of the homoclinic periodic point following C^d W, W = HEH"""
    return Fr(27 * 9 ** d, 8 ** (d + 1) - 3 * 9 ** d) - 5


def check(D=80):
    ok = True
    W = "HEH"
    AW, BW = compose(W)
    assert (AW, BW) == (Fr(3, 8), Fr(1, 4))
    seen = set()
    for d in range(D + 1):
        x = y(d)
        assert x.denominator % 2 and x.denominator % 3
        word, z = "", x
        for _ in range(3 * d + 3):
            word += branch_of(z)
            z = step(z)
        ok &= z == x and word == W + C * d
        lam = Fr(9, 8) ** d * AW
        ok &= (lam > 1) == (d >= 9)
        # orbit distinct from all previous ones and from the ghost cycle
        orb, z = set(), x
        for _ in range(3 * d + 3):
            orb.add(z)
            z = step(z)
        ok &= not (orb & seen) and not (orb & {Fr(-5), Fr(-7), Fr(-10)})
        seen |= orb
    print("[Y] y_d periodic with word W C^d, multiplier (9/8)^d 3/8 (> 1 iff d >= 9), "
          f"orbits pairwise distinct, d = 0..{D}:", ok)
    # integers near an expanding y_d rise: cycle lemma point, then T^j(n) > n
    allok = True
    for d in (9, 12, 20):
        x, L = y(d), 3 * d + 3
        pts, z = [], x
        for _ in range(L):
            pts.append(z)
            z = step(z)
        # cycle lemma: start where all partial multipliers exceed 1
        best = None
        for s in range(L):
            lam, good = Fr(1), True
            z = pts[s]
            for j in range(L):
                A, _ = BR[branch_of(z)]
                lam *= A
                z = step(z)
                if lam <= 1:
                    good = False
                    break
            if good:
                best = s
                break
        assert best is not None
        x0 = pts[best]
        N = 3 * L + 10
        M = 2 ** N * 3 ** N
        r = x0.numerator * pow(x0.denominator, -1, M) % M
        for k in range(1, 4):
            n = r + k * M
            z, rises = n, True
            for j in range(1, L + 1):
                z = (lambda t: (t + 1) // 27 if t % 27 == 26 else (t // 2 if t % 2 == 0 else (3 * t + 1) // 2))(z)
                if z <= n:
                    rises = False
            allok &= rises
    print("[R] integers n = y_d (mod 2^N 3^N) stay above n for a whole period (d = 9, 12, 20):", allok)
    return ok and allok


if __name__ == "__main__" and "check" in sys.argv:
    sys.exit(0 if check() else 1)
