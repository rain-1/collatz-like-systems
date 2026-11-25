"""Exact checks for the first descent and recovery bounds in split5_3_s27.md."""

from fractions import Fraction

from check_split5_3_cycles import log_bounds
from check_split5_3_runs import run_step


def verify_first_crossing_bound():
    two_lo, two_hi = log_bounds(3)
    ratio_lo, ratio_hi = log_bounds(9)
    beta_lo, beta_hi = ratio_lo / two_hi, ratio_hi / two_lo
    p, q = 186396751, 579001193
    assert 0 < q*beta_lo - p < q*beta_hi - p < Fraction(1, 24 * 10**9)
    assert 1/beta_lo < Fraction(311, 100)
    limit = 3 * 10**9
    k_max = Fraction(311, 100) * limit
    gap = (1 - k_max / (24 * 10**9)) / q
    assert 2**64 * gap / 2 > 3*limit
    assert Fraction(5, 4)**31 * (1 + Fraction(6, 2**64))**10 < 2**10
    extended_limit = 6 * 10**9
    extended_gap = (1 - Fraction(311, 100) * extended_limit / (24 * 10**9)) / q
    # For d <= 1/16, 1-exp(-d log 2) >= d*(log 2 - (log 2)^2/32).
    assert two_lo - two_hi**2 / 32 > Fraction(2, 3)
    assert 2**66 * Fraction(2, 3) * extended_gap > 3*extended_limit
    assert Fraction(2**66, 32) > 3*extended_limit


def bit_step(z, s):
    if z % 2:
        return (z + 3)//2, s
    if s:
        return 5*z//2, 0
    return z//2, 1


def verify_bit_map():
    for initial_s in (0, 1):
        words = set()
        length = 12
        for initial_z in range(4, 4 + 2**length):
            z, s = initial_z, initial_s
            last_exit = z << s
            word = 0
            for j in range(length):
                bit = z % 2
                word += bit << j
                z, s = bit_step(z, s)
                if bit:
                    assert z << s == run_step(last_exit)
                    last_exit = z << s
            words.add(word)
        assert len(words) == 2**length


def surviving_words(depth):
    """Count exact post-streak bit words with no smaller reached height."""
    counts = [1]
    for r in range(1, depth + 1):
        counts = [a+b for a, b in zip([0] + counts, counts + [0])]
        for ones in range(r + 1):
            extra, flag = divmod(r - ones, 2)
            if 5**(4*depth + extra) < 1 << (9*depth + r - flag):
                counts[ones] = 0
    return sum(counts)


def verify_actual_heights(depth):
    prefix_modulus = 512**depth
    low = 2**(12*depth)
    residue = -768 * pow(113, -1, prefix_modulus) % prefix_modulus
    count = 0
    for j in range(2**depth):
        start = low + residue + j*prefix_modulus
        z = start
        for _ in range(depth):
            assert z % 512 == 256
            z = run_step(z)
        flag = 0
        for _ in range(depth):
            z, flag = bit_step(z, flag)
            if z << flag < start:
                break
        else:
            count += 1
    assert count == surviving_words(depth)


if __name__ == "__main__":
    verify_first_crossing_bound()
    verify_bit_map()
    for d in range(2, 12):
        verify_actual_heights(d)
    for d in (32, 64, 128, 512):
        survivors = surviving_words(d)
        print(f"D={d}: {survivors} of 2^{d} remain above their start after D more bits "
              f"({survivors / 2**d:.9g} of the class)")
