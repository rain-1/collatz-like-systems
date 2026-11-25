"""Check failures of the cofactor potential on paths that end at 129.

The short check uses exact integer iteration throughout. The long bound
uses the endpoint bit length and period lower bound in verify_long_orbit.cpp.
All logarithmic inequalities below use rational enclosures.
"""

from fractions import Fraction

from verify_binary_invariant import inverse_step, orbit_step
from verify_cofactor_potential import PADDING, check_interval
from verify_pure_power_returns import log_bounds


def nearest_failure():
    value = 129
    for _ in range(1089):
        value = inverse_step(value)
    successor = orbit_step(value)
    source_p, failures, total, first = check_interval(value, 1089)
    target_p, later_failures, _, _ = check_interval(successor, 1088)
    if (failures, total, first, later_failures) != (1, 5, (0, 5), 0):
        raise AssertionError("Failed to isolate the nearest exceptional predecessor")
    print(f"Depth 1089: {value} -> {successor}, P = {source_p} -> {target_p}.")
    print("Defect 5 there. All 1088 closer predecessor steps have zero positive defect.")


def long_arc_bound():
    value = 243
    for steps, expected in ((17, 8), (12, 129)):
        for _ in range(steps):
            value = orbit_step(value)
        if value != expected:
            raise AssertionError("Incorrect path from 243 to 129")

    # Recorded long verification: y=G**(-10**9)(243), with this bit length.
    bits = 84_982_734
    length = 10**9 + 17 + 12
    period_lower = 2_039_805_608
    if length >= period_lower:
        raise AssertionError("Distinctness is required for the logarithmic estimate")
    lo2, hi2 = log_bounds(2)
    lo3, hi3 = log_bounds(3)

    # log2(129/y) = (2-log2(3))*length - zeros + correction.
    # Only inputs 1 mod 3 lower the correction, and all inputs are distinct
    # and >=8. In natural logs their losses sum to at most
    # 1/39 + log(1+12*(length-1)/39)/12 by decreasing-sum integration.
    if 39 + 12*(length-1) >= 39*(1 << 30):
        raise AssertionError("The integral no longer fits the stated bound")
    if 1/(39*lo2) + Fraction(30, 12) >= 3:
        raise AssertionError("Logarithmic correction may exceed three bits")
    # log2(129)<8, log2(y)>=bits-1. The strict lower bound rounds up.
    zero_count = int((2 - hi3/lo2)*length + bits - 1 - 8 - 3) + 1
    max_digits = int(bits*hi2/lo3) + 1
    max_initial_p = 5*(max_digits + PADDING)
    final_p = check_interval(129, 1)[0]

    # Signed defects telescope. Dropping negative terms can only increase
    # the sum, and each positive defect contributes at most ten.
    min_total = 8*zero_count - 3*length + final_p - max_initial_p
    min_failures = (min_total + 9)//10
    print(f"Given the recorded endpoint and period bound, the last {length} steps to 129")
    print(f"include at least {zero_count} divisible inputs and {min_failures} potential failures.")


if __name__ == "__main__":
    nearest_failure()
    long_arc_bound()
