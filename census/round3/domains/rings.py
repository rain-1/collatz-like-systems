"""Exact arithmetic in quadratic orders Z[theta], theta^2 = s*theta + t, and
Collatz-like maps on them that divide by a prime element pi.

Elements are pairs (a, b) meaning a + b*theta.  All arithmetic is in Python
ints.  Rings used here:
  GAUSS  Z[i]         theta = i,        theta^2 = -1          pi = 1 + i      (norm 2)
  EIS    Z[w]         theta = w,        w^2 = -1 - w           pi = 1 - w      (norm 3)
  ZM2    Z[sqrt(-2)]  theta = sqrt(-2), theta^2 = -2          pi = sqrt(-2)   (norm 2)
  ZP2    Z[sqrt(2)]   theta = sqrt(2),  theta^2 = 2           pi = sqrt(2)    (norm -2)
"""
from math import isqrt


class Ring:
    def __init__(self, name, s, t, pi, units):
        self.name, self.s, self.t, self.pi = name, s, t, pi
        self.units = units
        self.Npi = abs(self.norm(pi))
        self.imag = (s * s + 4 * t) < 0      # imaginary quadratic?

    # --- arithmetic -------------------------------------------------------
    def mul(self, x, y):
        a, b = x
        c, d = y
        return (a * c + b * d * self.t, a * d + b * c + b * d * self.s)

    def add(self, x, y):
        return (x[0] + y[0], x[1] + y[1])

    def neg(self, x):
        return (-x[0], -x[1])

    def conj(self, x):
        a, b = x
        return (a + b * self.s, -b)

    def norm(self, x):
        a, b = x
        return a * a + self.s * a * b - self.t * b * b

    def divides(self, d, x):
        """Exact test d | x in the order."""
        n = self.norm(d)
        y = self.mul(x, self.conj(d))
        return y[0] % n == 0 and y[1] % n == 0

    def div(self, x, d):
        n = self.norm(d)
        y = self.mul(x, self.conj(d))
        assert y[0] % n == 0 and y[1] % n == 0, (x, d)
        return (y[0] // n, y[1] // n)

    def residue_pi(self, x):
        """Residue of x modulo pi as an integer 0..Npi-1 (pi has prime norm
        and the order maps onto Z/Npi)."""
        for r in range(self.Npi):
            if self.divides(self.pi, (x[0] - r, x[1])):
                return r
        raise AssertionError

    def vpi(self, x, cap=10 ** 6):
        assert x != (0, 0)
        k = 0
        while self.divides(self.pi, x):
            x = self.div(x, self.pi)
            k += 1
        return k


GAUSS = Ring('Z[i]', 0, -1, (1, 1), [(1, 0), (0, 1), (-1, 0), (0, -1)])
EIS = Ring('Z[w]', -1, -1, (1, -1), [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)])
ZM2 = Ring('Z[sqrt-2]', 0, -2, (0, 1), [(1, 0), (-1, 0)])
ZP2 = Ring('Z[sqrt2]', 0, 2, (0, 1), None)   # infinitely many units


class PiMap:
    """T(z) = z/pi if pi | z; else u_r z + c_r where r = z mod pi (r != 0).
    branches: dict r -> (u_r, c_r) with pi | u_r r + c_r required."""
    def __init__(self, R, branches, name=''):
        self.R, self.br, self.name = R, branches, name
        for r, (u, c) in branches.items():
            assert R.divides(R.pi, R.add(R.mul(u, (r, 0)), c)), (r, u, c)

    def __call__(self, z):
        R = self.R
        if R.divides(R.pi, z):
            return R.div(z, R.pi)
        u, c = self.br[R.residue_pi(z)]
        return R.add(R.mul(u, z), c)


def orbit_to_cycle(T, z, cap=10 ** 6):
    seen = {}
    path = []
    while z not in seen:
        seen[z] = len(path)
        path.append(z)
        z = T(z)
        assert len(path) < cap, 'orbit too long'
    cyc = path[seen[z]:]
    k = cyc.index(min(cyc))
    return tuple(cyc[k:] + cyc[:k])


def window(T):
    """A finite box of ring elements that contains every odd (pi-free) element
    of every cycle except {0}, for maps whose odd branch multipliers are units
    of absolute value 1 in every embedding (Theorem N').  Uses the bound
    |sigma z| <= C_sigma/(|sigma pi| - 1); supersets are taken with exact
    integer comparisons."""
    R = T.R
    Cn = max(R.norm(c) for (u, c) in T.br.values())  # max |c|^2 (imag. case)
    out = []
    if R.imag:
        # |z|^2 <= Cn/(|pi|-1)^2 ; (|pi|-1)^2 >= 1/6 for |pi|^2 = 2, >= 1/2 for 3
        fac = 6 if R.Npi == 2 else 2
        B = fac * Cn
        # |a|,|b| bounded crudely: N(z) >= (|b|^2 * |disc|/4) and >= ... use box
        L = isqrt(4 * B) + 2
        for a in range(-L, L + 1):
            for b in range(-L, L + 1):
                if R.norm((a, b)) <= B:
                    out.append((a, b))
    else:
        # Z[sqrt2]: both embeddings, |a +- b sqrt2| <= C/(sqrt2-1) < 2.42 C
        C = max(max(abs(c[0] + c[1] * x) for x in (1.5, -1.5)) for (u, c) in T.br.values())
        Ce = max(abs(c[0]) + 2 * abs(c[1]) for (u, c) in T.br.values())  # >= |c0 +- c1 sqrt2|
        A = 3 * Ce
        for a in range(-A, A + 1):
            for b in range(-A, A + 1):
                # exact: |a + b sqrt2| <= A and |a - b sqrt2| <= A  <=> max(|a|+|b|sqrt2) <= A
                # <=> 2 b^2 <= (A - |a|)^2 with A >= |a|
                if abs(a) <= A and 2 * b * b <= (A - abs(a)) ** 2:
                    out.append((a, b))
    return out


def all_cycles(T):
    cycles = {orbit_to_cycle(T, (0, 0))}
    for z in window(T):
        cycles.add(orbit_to_cycle(T, z))
    return sorted(cycles, key=lambda c: (len(c), c))
