"""Round 4, lens 'wpotential': shared definitions.

Systems are unit-multiplier 2-adic table maps in the format of
round3/accel/accel_lib.py: (p, m, table) with table[r] = (u, v, w),
n = r (mod p^m) -> (u n + v)/w.  The mixed system mb_s3_27 is handled separately.
Everything used as proof data is exact (int / Fraction).
"""
import os
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
R3 = os.path.join(HERE, "..", "..", "round3")
sys.path.insert(0, os.path.join(R3, "accel"))
sys.path.insert(0, os.path.join(R3, "dichotomy"))
import accel_lib as AL      # noqa: E402
import decide as DEC        # noqa: E402


def s_table(m, S):
    return [(1, 0, 2) if r % 2 == 0 else ((3, 1, 1) if r in S else (1, 1, 1))
            for r in range(2 ** m)]


# the 8 open cores of round3/accel/sfamily_obst.md, in the n-form (S-family, m = 3)
CORES = {
    "sf3_7 (K7)": (7,), "sf3_17": (1, 7), "sf3_57": (5, 7), "sf3_157": (1, 5, 7),
    "sf3_357": (3, 5, 7), "sf3_137 (W)": (1, 3, 7), "sf3_13": (1, 3), "sf3_135": (1, 3, 5),
}
# expanding periodic point used by round 3 for each core
XSTAR = {"sf3_7 (K7)": Fraction(-1), "sf3_17": Fraction(-1), "sf3_57": Fraction(-1),
         "sf3_157": Fraction(-1), "sf3_357": Fraction(-1), "sf3_137 (W)": Fraction(-1),
         "sf3_13": Fraction(-5), "sf3_135": Fraction(-5)}

SYSTEMS = {}
for name, S in CORES.items():
    SYSTEMS[name] = dict(p=2, m=3, table=s_table(3, S), xstar=XSTAR[name], domain=1)
# K7 in its z-form: z even -> z/2; z = 3 (4) -> (3z+1)/2; z = 1 (4) -> (z-1)/4, z >= 0
SYSTEMS["K7 z-form"] = dict(p=2, m=2, table=[(1, 0, 2), (1, -1, 4), (1, 0, 2), (3, 1, 2)],
                            xstar=Fraction(-1), domain=0)
# 3x+1 itself (control)
SYSTEMS["3x+1"] = dict(p=2, m=1, table=[(1, 0, 2), (3, 1, 2)], xstar=Fraction(-1), domain=1)


def step_fn(sysd):
    p, m, t = sysd["p"], sysd["m"], sysd["table"]
    Q = p ** m

    def T(n):
        u, v, w = t[n % Q]
        x = u * n + v
        assert x % w == 0
        return x // w
    return T


def padic_res(x, p, K):
    x = Fraction(x)
    assert x.denominator % p != 0
    return (x.numerator * pow(x.denominator, -1, p ** K)) % p ** K


def rat_step(sysd, x):
    """T-hat on a rational p-adic integer x (exact)."""
    p, m, t = sysd["p"], sysd["m"], sysd["table"]
    u, v, w = t[padic_res(x, p, m)]
    return (u * Fraction(x) + v) / w, Fraction(u, w)


def periodic_data(sysd, y, maxlen=10 ** 4):
    """(L, lam, D, orbit, partial multipliers) for a rational periodic point y."""
    p = sysd["p"]
    x, lam, orb, parts, D = Fraction(y), Fraction(1), [], [], 0
    for _ in range(maxlen):
        orb.append(x)
        x, q = rat_step(sysd, x)
        lam *= q
        parts.append(lam)
        while q.denominator % p == 0:
            q *= p
            D += 1
        if x == y:
            return len(orb), lam, D, orb, parts
    raise AssertionError("not periodic")


# --------------------------------------------------------------- mixed system
def mb_s3_27(n):
    """round3/mixedbase: n = 26 (27) -> (n+1)/27; else even -> n/2; else (3n+1)/2."""
    if n % 27 == 26:
        return (n + 1) // 27
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2


def mb_rat_step(x):
    """mb_s3_27 on a rational in Z_(2) cap Z_(3) (denominator prime to 6)."""
    x = Fraction(x)
    assert x.denominator % 6 != 0 and x.denominator % 2 and x.denominator % 3
    r27 = padic_res(x, 3, 3)
    r2 = padic_res(x, 2, 1)
    if r27 == 26:
        return (x + 1) / 27, Fraction(1, 27)
    if r2 == 0:
        return x / 2, Fraction(1, 2)
    return (3 * x + 1) / 2, Fraction(3, 2)
