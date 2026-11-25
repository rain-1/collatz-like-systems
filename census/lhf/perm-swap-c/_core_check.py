"""Core exact checks shared by check_CLS-038/035/038.py."""
import itertools
from fractions import Fraction as Fr
from _common import get, T, Tinv, S, C, BRANCH, edges, scc

def agree(f, g, N):
    return all(f(n) == g(n) for n in range(1, N + 1))

def mutual_inverse(f, g, N):
    return all(g(f(n)) == n and f(g(n)) == n for n in range(1, N + 1))

def preserves5(F, N):
    return all((F(n) % 5 == 0) == (n % 5 == 0) for n in range(1, N + 1))

def residue_structure(name, MMAX):
    F, B = BRANCH[name]; bad = []
    for M in range(1, MMAX + 1):
        adj = edges(F, B, M); comp = scc(adj)
        crossing = any(comp[u] != comp[v] for u in range(M) for v in adj[u])
        if name in ("T", "Tinv") or M % 5:
            good = len(set(comp)) == 1
        else:
            good = len(set(comp)) == 2 and all((comp[r] == comp[0]) == (r % 5 == 0) for r in range(M))
        if crossing or not good: bad.append(M)
    return bad

def translation_identities():
    """A1 o A2^{-1} is translation by -2/3 (T) and by +10/3 (S), as rational affine maps."""
    ok = True
    for (A1, A2inv, d) in (
        (lambda c: (4*c - 1) / 3, lambda y: (3*y - 1) / 4, Fr(-2, 3)),   # T
        (lambda c: (4*c + 5) / 3, lambda y: (3*y + 5) / 4, Fr(10, 3)),   # S
    ):
        for y in (Fr(0), Fr(1), Fr(7, 5), Fr(-11, 2)):
            ok &= A1(A2inv(y)) == y + d
    # branch maps as affine maps of n: T(3q+i)=a q + b  <=>  A_i(n)=(a(n-i))/3+b
    for F, A in ((T, [lambda n: Fr(2*n, 3), lambda n: Fr(4*n - 1, 3), lambda n: Fr(4*n + 1, 3)]),
                 (S, [lambda n: Fr(2*n, 3), lambda n: Fr(4*n + 5, 3), lambda n: Fr(4*n - 5, 3)])):
        ok &= all(F(n) == A[n % 3](n) for n in range(1, 3000))
    # S(n) = 5 T(n/5) on rationals with denominator 5: compare via A-maps (branch by n mod 3)
    TA = [lambda x: 2*x/3, lambda x: (4*x - 1)/3, lambda x: (4*x + 1)/3]
    def Trat(x):  # x in Z_(3); branch by x mod 3
        r = (x.numerator * pow(x.denominator, -1, 3)) % 3
        return TA[r](x)
    ok &= all(S(n) == 5 * Trat(Fr(n, 5)) for n in range(1, 3000))
    return ok

def word_multipliers(maxlen=7):
    """Every branch word of length k>=1 has non-integer multiplier (2^h/3^k for T,S; 3^k/2^h, h>=k, for inverses)."""
    for k in range(1, maxlen + 1):
        for w in itertools.product((2, 4), repeat=k):
            a = Fr(1)
            for x in w: a *= Fr(x, 3)
            if a.denominator == 1 or (1 / a).denominator == 1: return False
    return True

def run(names, MMAX=300, label=""):
    s = {k: get(k)["step"] for k in ("perm_1932_s44", "perm_swap_s8", "perm_c_s8")}
    ok = agree(s["perm_1932_s44"], T, 100000) and agree(s["perm_swap_s8"], S, 100000) and agree(s["perm_c_s8"], C, 100000)
    ok &= mutual_inverse(T, Tinv, 100000) and mutual_inverse(S, C, 100000)
    ok &= preserves5(S, 100000) and preserves5(C, 100000)
    print(label, "step functions / inverses / 5Z-invariance:", ok)
    ti = translation_identities(); wm = word_multipliers()
    print(label, "translation & conjugacy identities:", ti, "| word multipliers non-integral:", wm)
    ok &= ti and wm
    for nm in names:
        bad = residue_structure(nm, MMAX)
        print(label, f"{nm}: moduli <= {MMAX} violating theorem structure: {bad}")
        ok &= not bad
    return ok
