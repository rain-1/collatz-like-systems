"""Verify extensions on the orbit of 8, using the saved long-orbit result.

Inputs at indices s,...,t-1 form the window [s,t). The long computation
in verify_long_orbit.cpp records the first forward index with 84,982,734
bits. This script checks the consequences of that checkpoint, without
rerunning the billion steps.
"""

from fractions import Fraction

from verify_binary_invariant import orbit_step
from verify_return_zero_counts import verify_cycle_cutoff


def verify_extensions():
    value, index = 8, 0
    for length in (12 * 2**j for j in range(9)):
        zeros = 0
        for _ in range(length):
            zeros += value % 3 == 0
            value = orbit_step(value)
        if 5 * zeros > 2 * length:
            raise AssertionError((index, length, zeros))
        print(f"[{index}, {index + length}): zero count {zeros} in {length} steps")
        index += length

    end, endpoint_bits = 1_039_805_591, 84_982_734
    latest_start = 100_000_000
    # G(n)+1 <= (4/3)(n+1), so x_s < 9*(4/3)**s.
    # On this orbit all n >= 8. At a nonzero residue G(n)/n <= 11/8.
    # With at least 2/5 zeros the product over m steps is bounded by
    # ((2/3)**2 * (11/8)**3)**(m/5) = (1331/1152)**(m/5).
    if 4**12 >= 2**5 * 3**12 or 1331**23 >= 2**5 * 1152**23:
        raise AssertionError("Growth factor bounds failed")
    # This exponent increases with s, so the latest start suffices.
    upper_bits = 4 + Fraction(5 * latest_start, 12) + Fraction(end - latest_start, 23)
    if upper_bits >= endpoint_bits - 1 or end - latest_start <= latest_start:
        raise AssertionError("Checkpoint cannot certify a longer good window")
    print(f"Given the recorded endpoint, every [s, {end}) with 0 <= s <= {latest_start} is below 40%.")


def verify_obstructions():
    verify_cycle_cutoff()
    length_floor = 2_039_805_608
    zero_fraction_floor = Fraction(415_037_498, 10**9)
    # On a cycle of negative total score, let M_i be the maximum score
    # over all prefixes starting at i, including the empty prefix. Then
    # M_i = max(0, a_i + M_{i+1}). The deficit M_i - a_i - M_{i+1}
    # is positive exactly at permanent obstructions and never exceeds 3.
    # Its sum along the cycle is 5*c - 2*L.
    count_floor = (5 * zero_fraction_floor - 2) * length_floor / 3
    print(f"A cycle through 8 would have at least {int(count_floor) + 1} permanent obstructions.")

    start = value = 111
    score = 0
    for _ in range(12):
        score += 2 - 5 * (value % 3 == 0)
        value = orbit_step(value)
        if score >= 0:
            raise AssertionError("Expected every nonempty prefix to be bad")
    if value != start or score != -1:
        raise AssertionError("Expected a negative-score cycle")
    print("At 111 on the period-12 orbit, every nonempty prefix exceeds 40%.")


if __name__ == "__main__":
    verify_extensions()
    verify_obstructions()
