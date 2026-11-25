"""Exact checks for the three conjugacies/inverse relations to the 1932 map T."""
import sys
from _lib import catalog, T, Tinv

N = 200000


def affine_branch_identity(lhs, rhs, mod):
    """lhs and rhs are both affine in q on each class n = mod*q + r (by their
    written rules).  Two affine functions of q that agree at q = 0, 1 agree for
    all q, so checking q in {0,1} per class is a proof; we also check more q."""
    for r in range(mod):
        for q in list(range(0, 2)) + list(range(2, 2000)):
            n = mod * q + r
            if n < 1:
                continue
            if lhs(n) != rhs(n):
                return False
    return True


def check_inverse():
    U = catalog("perm_1932inv_s8")["step"]
    Tc = catalog("perm_1932_s8")["step"]
    ok = all(Tc(n) == T(n) for n in range(1, N))
    ok &= all(U(n) == Tinv(n) for n in range(1, N))
    ok &= affine_branch_identity(lambda n: T(U(n)), lambda n: n, 4)
    ok &= affine_branch_identity(lambda n: U(T(n)), lambda n: n, 3)
    # forward U-orbit of 8 is the backward T-orbit of 8
    x = 8
    for _ in range(20000):
        y = U(x)
        if T(y) != x:
            return False
        x = y
        if x == 8:
            return False  # would be a return; not expected
    return ok


def check_perm_b():
    B = catalog("perm_b_s7")["step"]
    ok = affine_branch_identity(B, lambda n: T(n + 1) - 1, 3)
    ok &= all(B(n) == T(n + 1) - 1 for n in range(1, N))
    ok &= T(1) == 1 and all(T(n) >= 2 for n in range(2, N))
    x, y = 7, 8
    for _ in range(20000):
        x, y = B(x), T(y)
        if x != y - 1:
            return False
    return ok


def check_flipT():
    P = catalog("flipT_s8")["step"]
    ok = affine_branch_identity(P, lambda n: T(n + 3) - 3, 3)
    ok &= all(P(n) == T(n + 3) - 3 for n in range(1, N))
    ok &= (T(1), T(2), T(3)) == (1, 3, 2) and T(8) == 11
    x, y = 8, 11
    for _ in range(20000):
        x, y = P(x), T(y)
        if x != y - 3:
            return False
    return ok


if __name__ == "__main__":
    which = sys.argv[1]
    ok = {"inv": check_inverse, "b": check_perm_b, "flip": check_flipT}[which]()
    print(which, "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
