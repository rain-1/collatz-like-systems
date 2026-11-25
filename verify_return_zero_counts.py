"""Check the cycle-frequency cutoff and the finite example for the orbit of 8.

The example of independent zero counts extends to arbitrary finite horizons.
Fix K initial residues from 8, take H > K, and put P = 3**H. For a block
n = P*2**s + r, 0 <= r < P, take s = P.bit_length() + 4. At time j <= H,
the leading four bits are those of n//3**j by the quotient identity in
verify_binary_prefix_returns.py. This quotient equals 3**(H-j)*2**s plus
an integer below P. The added bits lie below the top four, so the four
leading bits at every time, hence all the prefix visits, are common to
the block. To have both endpoints start with 1000, choose H such that
3**H starts with 1000. There are arbitrarily large such H since log2(3)
is irrational and its multiples are dense modulo one.

The residue words of length H label the residue classes modulo P bijectively:
three lifts of a class modulo 3**j change its j-th iterate in increments
of 2**a, a unit modulo 3. Thus exactly one lift realizes each next residue.
Restricting r to 8 modulo 3**K fixes the initial word. Among the remaining
H-K positions, precisely binom(H-K,z)*2**(H-K-z) words have z zeros.
At time H the bit-length change is 2*H - (P.bit_length()-1) - Z, where
Z counts all H inputs divisible by 3. For any fixed K, both signs occur
for sufficiently large H, even though all starts in the block share every
prefix visit. Their gap history need not be the gap history of 8.
"""

from collections import Counter
from fractions import Fraction
from math import comb

from verify_binary_prefix_returns import starts_with_1000
from verify_binary_invariant import orbit_step
from verify_pure_power_returns import log_bounds


def verify_cycle_cutoff():
    # This input is the period lower bound certified by verify_long_orbit.cpp.
    length = 2_039_805_608
    cutoff = Fraction(415_037_498, 10**9)
    log2_lower, _ = log_bounds(2)
    _, log3_upper = log_bounds(3)
    # Only n = 10,13,16,... can lower the logarithmic growth correction
    # on a cycle through 8. Their ordered losses are <= 1/(39+12*j).
    # At length L the mean of the first L such bounds is decreasing in L.
    # At the certified minimum, bound the sum by its first term plus the
    # integral and use log(1+12*(length-1)/39) < 30 log(2).
    if 39 + 12 * (length - 1) >= 39 * (1 << 30):
        raise AssertionError("The integral bound requires a larger exponent")
    loss_in_bits = Fraction(1, 39) / log2_lower + Fraction(30, 12)
    lower = 2 - log3_upper / log2_lower - loss_in_bits / length
    if lower <= cutoff:
        raise AssertionError("Cycle-frequency bound did not clear the cutoff")


def trace(n, steps):
    residues = []
    visits = []
    for j in range(steps + 1):
        if starts_with_1000(n):
            visits.append(j)
        if j < steps:
            residues.append(n % 3)
            n = orbit_step(n)
    return n, residues, visits


def verify_examples():
    reference = trace(8, 12)
    for start, end, zeros in (
        (8, 129, 1),
        (8_503_064, 134_217_857, 1),
        (8_854_928, 1_091_968, 8),
    ):
        value, residues, visits = trace(start, 12)
        if (value, residues.count(0), visits) != (end, zeros, [0, 5, 12]):
            raise AssertionError(start)
        if residues[:5] != reference[1][:5]:
            raise AssertionError("Initial residues do not match 8")
        change = end.bit_length() - start.bit_length()
        print(f"{start} -> {end}: gaps 5,7; zero count {zeros}; bit change {change:+d}")

    # In this block all starts have the same four leading bits at each time
    # through H. Select the starts sharing the first K residues of 8.
    horizon, shared = 12, 5
    power = 3**horizon
    base = power << (power.bit_length() + 4)
    counts = Counter()
    for offset in range(8, power, 3**shared):
        _, residues, visits = trace(base + offset, horizon)
        if residues[:shared] != reference[1][:shared] or visits != [0, 5, 12]:
            raise AssertionError(offset)
        counts[residues[shared:].count(0)] += 1
    remaining = horizon - shared
    expected = {z: comb(remaining, z) * 2**(remaining-z) for z in range(remaining+1)}
    if counts != expected:
        raise AssertionError(counts)
    print(f"All {sum(counts.values())} continuations have the exact binomial counts.")


if __name__ == "__main__":
    verify_cycle_cutoff()
    print("Given period >= 2039805608, a cycle through 8 has zero fraction > 0.415037498.")
    verify_examples()
