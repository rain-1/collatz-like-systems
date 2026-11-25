"""Exact checks for the expanding-run map and its adjacent 5-smooth pairs."""

from math import gcd
from check_split5_3_range import step


def run_step(y):
    exponent = (y & -y).bit_length() - 1
    k, b = divmod(exponent, 2)
    u = y >> exponent
    return (5**k * u + 3) >> (1 - b)


def is_smooth(n):
    for prime in (2, 3, 5):
        while n % prime == 0:
            n //= prime
    return n == 1


def smooth_pairs():
    # Table 1 of von Känel and Matschke gives 17 primitive triples in total.
    # Exhibit all 17 to certify completeness without reading an external file.
    small = {i for i in range(1, 129) if is_smooth(i)}
    triples = {(a, b, a+b) for a in small for b in small
               if a <= b and gcd(a, b) == 1 and a+b in small}
    assert len(triples) == 17
    peaks = set()
    for a, b, _ in triples:
        for summand, other in ((a, b), (b, a)):
            if 3 % summand == 0:
                z = (3 // summand) * other
                if z % 2:
                    peaks.add(z)
    assert peaks == {1, 3, 5, 9, 15, 27, 45, 125}

    starts = set()
    for z in peaks:
        cofactor = z
        factor = 1
        while True:
            for y in (factor*cofactor, 2*factor*cofactor):
                if y >= 4:
                    starts.add(y)
            if cofactor % 5:
                break
            cofactor //= 5
            factor *= 4
    assert len(starts) == 25 and max(starts) == 250
    fixed = {4, 6, 8, 64, 128}
    for y in starts:
        assert is_smooth(y) and is_smooth(run_step(y))
        visited = set()
        while y not in visited:
            visited.add(y)
            y = run_step(y)
        assert y in fixed and run_step(y) == y
    return starts


def verify_run_map():
    inputs = list(range(4, 20000))
    inputs.extend(2**(2*k + b) * u for k in (8, 31, 100)
                  for b in (0, 1) for u in (1, 3, 17, 125))
    for y in inputs:
        x = y - 3
        while x % 4 == 1:
            x = step(step(step(x)))
        x = step(step(x)) if x % 2 else step(x)
        assert x + 3 == run_step(y)


def check_four_expansion_runs():
    for depth in (1, 2, 3, 12, 64, 256):
        modulus = 512**depth
        y = (-768 * pow(113, -1, modulus)) % modulus + modulus
        start = y
        for _ in range(depth):
            assert y % 512 == 256
            next_y = run_step(y)
            assert 512*next_y == 625*y + 768 and next_y > y
            y = next_y
        assert 113*y + 768 == (113*start + 768) // modulus * 625**depth


if __name__ == "__main__":
    verify_run_map()
    check_four_expansion_runs()
    starts = smooth_pairs()
    print("Exactly 25 adjacent 5-smooth starting values in shifted coordinates:")
    print(*sorted(starts))
