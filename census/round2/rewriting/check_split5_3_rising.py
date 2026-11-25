"""Certify smaller merging starts for classes of exponents in 4**K - 3."""

from math import gcd
from check_split5_3_escape import block
from check_split5_3_range import CYCLE_PERIODS, step


def affine_path(residue, bits, multiplier, denominator):
    """Peak (multiplier*Z - 3*denominator)/denominator, with Z known mod 2**bits."""
    modulus = 1 << bits
    x = (multiplier * residue * pow(denominator, -1, modulus) - 3) % modulus
    a, b, d = multiplier, -3 * denominator, denominator
    states = set()
    while True:
        divisor = gcd(gcd(a, b), d)
        states.add((a // divisor, b // divisor, d // divisor))
        if bits == 0 or (bits == 1 and x % 2):
            return states
        if x % 2 == 0:
            x //= 2
            d *= 2
            bits -= 1
        elif x % 4 == 1:
            x = (5*x + 3) // 4
            a, b, d = 5*a, 5*b + 3*d, 4*d
            bits -= 2
        else:
            x = (x + 3) // 2
            b, d = b + 3*d, 2*d
            bits -= 1


def verify_classes(bits):
    period = 1 << (bits - 2)
    modulus = 1 << bits
    assert pow(5, period, modulus) == 1 and pow(5, period // 2, modulus) != 1
    counts = [0, 0, 0]
    for kind in (1, 2, 3):
        for residue in range(kind, modulus, 4):
            target = affine_path(residue, bits, 1, 1)
            witness = any(target & affine_path(residue, bits, c, denominator)
                          for denominator in (5, 25) for c in (1, 2))
            counts[kind - 1] += witness
    print(f"{counts[0]:,} of {period:,} exponent classes have certified smaller starts.")
    print(f"For fixed run length, {sum(counts):,} of {3*period:,} cofactor residues are covered.")
    return counts


def check_even_formula():
    for k in range(2, 65):
        for u in range(1, 65):
            z = 5**k * u
            if z % 8 != 1:
                continue
            x, y = 4**k*u - 3, 2*4**(k-1)*u - 3
            assert 0 < y < x
            for _ in range(k + 2):
                x = block(x)
            for _ in range(k + 1):
                y = block(y)
            assert x == y == (z + 3)//4


if __name__ == "__main__":
    check_even_formula()
    for seed, root in ((61, 61), (13, 5), (29, 1), (1, 1), (5, 5)):
        value = seed
        for _ in range(100):
            if value in CYCLE_PERIODS:
                break
            value = step(value)
        assert value == root
    assert verify_classes(18) == [46055, 36699, 36757]
