"""Verify a rational cycle matching 1,000 steps on each side of 8."""

from collatz_1932_periodic_approximations import (
    BRANCHES,
    backward_residues,
    coefficients,
    forward_residues,
    periodic_point,
)


def main():
    window = 1000
    prefix = forward_residues(8, window)
    suffix = backward_residues(8, window)
    word = prefix + [2] * 6531 + [0] * 4646 + suffix

    # The limiting affine map in the approximation argument fixes 8.
    # Bound its slope exactly, so its fixed point varies continuously.
    p, d, s = coefficients(prefix)
    q, h, b = coefficients(suffix)
    forward, rem = divmod(8 * p + s, d)
    assert rem == 0
    backward, rem = divmod(8 * h - b, q)
    assert rem == 0
    slope_num = p * q * backward
    slope_den = d * h * (forward + 1)
    assert 965 * slope_den < 1000 * slope_num < 966 * slope_den
    start = periodic_point(word)
    numerator, denominator = start.numerator, start.denominator
    assert 8005 * denominator < 1000 * numerator < 8006 * denominator
    assert denominator % 6 in (1, 5)

    # All iterates can be checked over the same denominator.
    current = numerator
    discrepancy = 0
    for index, residue in enumerate(word):
        assert index == 0 or current > numerator
        assert (current - residue * denominator) % 3 == 0
        multiplier, offset = BRANCHES[residue]
        current, remainder = divmod(multiplier * current + offset * denominator, 3)
        assert remainder == 0

        discrepancy += int(word[-1 - index] == 0) - int(residue == 0)
        if index + 1 < len(word):
            assert discrepancy > 0
    assert current == numerator and discrepancy == 0
    print(f"Least period {len(word)}. Unique minimum lies between 8.005 and 8.006.")
    print(f"Matched {window} forward and {window} backward residues of 8.")
    print(f"Positive discrepancy at all {len(word) - 1} proper cuts.")


if __name__ == "__main__":
    main()
