"""Check the binomial orbit formulas by direct polynomial iteration over F_2."""

from polylib import T2, clmul, divmod2, subst2


def lift(f, m):
    return clmul(3 ^ (1 << m), subst2(f, m))


def quadratic_checkpoint(n):
    numerator = 1 ^ (6 << (3 * n))
    quotient, remainder = divmod2(numerator, 7)
    assert remainder == 0
    return quotient


def check_blocks():
    for m in range(2, 13):
        multiplier = 1 ^ (1 << m)
        for f in range(256):
            x = lift(f, m)
            bits = []
            for _ in range(m):
                bits.append(x & 1)
                x = T2(x, multiplier)
            assert bits == ([1, 1] + [0] * (m - 2) if f & 1 else [0] * m)
            assert x == lift(T2(f, 5), m)


def check_orbits():
    for m in (2, 3, 5, 6, 7, 11, 12):
        for twist in (1, 3, 13):
            multiplier = 1 ^ (1 << m)
            x = clmul(twist, lift(11, m))  # F_1 = 1 + u + u^3
            elapsed = 0
            for j in range(8):
                n = 1 << j
                target = 5 * m * (n - 1)
                for _ in range(target - elapsed):
                    # Use the sparsity of 1+t^m for the raw update.
                    x = ((x ^ (x << m) ^ twist) if x & 1 else x) >> 1
                elapsed = target
                assert x == clmul(twist, lift(quadratic_checkpoint(n), m))
                assert x.bit_length() - 1 == twist.bit_length() - 1 + m + 3 * m * n


if __name__ == "__main__":
    check_blocks()
    check_orbits()
    print("Verified 2,816 block identities and 168 exact orbit checkpoints.")
