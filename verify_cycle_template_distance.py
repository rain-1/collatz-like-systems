"""Lower bounds on edits between a cycle through 8 and a repeated binary word.

Use 1 for a multiple of 3 and 0 otherwise. The word is read in time order.
An edit here changes a single bit, without moving or inserting positions.
Endpoint data and the earlier proof that the two arcs are disjoint as sets
of step indices come from verify_long_orbit.cpp and verify_phase_bridge.py.
"""

from fractions import Fraction

from verify_phase_bridge import DEPTH, FIRST_FORWARD, HEIGHT


def bounds():
    backward = DEPTH + 17  # From B to 8, since G^17(243)=8.
    forward = FIRST_FORWARD  # From 8 to F.
    if not 0 < backward <= forward:
        raise ValueError("Expected the backward arc to be shorter")

    # On either arc the inputs are distinct integers >=8. Each local
    # logarithmic error has magnitude <= 1/((4*n-1)*ln(2)). For s
    # terms, summing the decreasing bound gives a base-2 error <=
    # 1/(31*ln(2)) + log2((4*s+27)/31)/4. The check below bounds this
    # by 2/31 + 27/4 < 7, since ln(2)>1/2.
    if 4 * forward + 27 >= 31 * (1 << 27):
        raise ValueError("The seven-bit logarithmic bound needs updating")

    # In s steps with c contraction bits, the height change is
    # s*(2-log2(3))-c+error. Both large endpoints have HEIGHT bits.
    # Therefore c_back - (backward/forward)*c_forward exceeds
    # (1+backward/forward)*(HEIGHT-4-7).
    factor = 1 + Fraction(backward, forward)
    for cap in (1000, 1_000_000, 100_000_000):
        # A template with p ones per h steps differs from s*p/h on a
        # window of length s by at most h/4, in either direction.
        difference = factor * (HEIGHT - 4 - 7 - Fraction(cap, 4))
        required = difference // 1 + 1
        print(f"Template period <= {cap:,}: at least {required:,} mismatches.")


if __name__ == "__main__":
    bounds()
