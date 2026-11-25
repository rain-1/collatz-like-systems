"""Rule out short connections between the two recorded orbit-of-8 endpoints.

Reproduce the endpoint data with verify_long_orbit.cpp at depth 1000000000.
Let F be its forward endpoint, B its backward endpoint, and t the number
of intervening forward steps in a hypothetical least cycle. The prior
first-height bound gives t = L - (N+17+K) >= 0, since G^17(243)=8.

Write alpha=log2(3), beta=log2(B/F). Each step adds an integer minus
alpha to log2(n), plus an error of magnitude < 1/n: the correction is
zero or log2(1 +/- 1/(4n)), bounded by 1/((4n-1)*ln(2)).
If every intervening value is >=2^b and t<=T, the distance of q*beta
from an integer is therefore at most T*(abs(q*alpha-p)+q/2^b).
Two rational witnesses below contradict that inequality at different
time scales. Only exact integer and rational arithmetic is used.
"""

from fractions import Fraction

from verify_binary_invariant import orbit_step
from verify_pure_power_returns import log_bounds


DEPTH = 1_000_000_000
FIRST_FORWARD = 1_039_805_591
HEIGHT = 84_982_734
FORWARD_PREFIX = 0x995701407907FBD4DC57AA68CBC9C32C
BACKWARD_PREFIX = 0xC8E8CF870DA384721515EE105199BD1C


def normalized_log(prefix, log_two):
    """Bound log2(n) minus its integer part using its top 128 bits."""
    if prefix.bit_length() != 128:
        raise ValueError("Expected exactly 128 significant bits")
    scale = 1 << 127
    low, _ = log_bounds(Fraction(prefix, scale))
    _, high = log_bounds(Fraction(prefix + 1, scale))
    return low / log_two[1], high / log_two[0]


def verify_dip(alpha, beta, horizon, bits, p, q):
    low, high = (q * x for x in beta)
    floor = low // 1
    separation = min(low - floor, floor + 1 - high)
    drift = max(abs(q * x - p) for x in alpha)
    accumulated = horizon * (drift + Fraction(q, 1 << bits))
    if separation <= accumulated:
        raise AssertionError("The phase intervals do not exclude a high connection")
    print(f"Any connection of at most {horizon:,} steps visits an integer below 2^{bits}.")


def verify():
    n = 243
    for _ in range(17):
        n = orbit_step(n)
    if n != 8:
        raise AssertionError("Wrong offset for backward endpoint")

    log_two = log_bounds(2)
    log_three = log_bounds(3)
    alpha = log_three[0] / log_two[1], log_three[1] / log_two[0]
    f_low, f_high = normalized_log(FORWARD_PREFIX, log_two)
    b_low, b_high = normalized_log(BACKWARD_PREFIX, log_two)
    beta = b_low - f_high, b_high - f_low

    short_horizon = 400_000_000
    short_bits = 62
    verify_dip(alpha, beta, short_horizon, short_bits, 630_138_897, 397_573_379)
    verify_dip(alpha, beta, 10**15, 102, 766_512_153_894_657, 483_615_324_366_283)

    # Both endpoints are >= 2^(HEIGHT-1). Down to n<2^b, G(x)>=2x/3;
    # on the way back, G(x)+1 <= 4(x+1)/3 and n+1 <= 2^b.
    altitude = HEIGHT - 1 - short_bits
    # A whole block of contractions takes 3^j*u to 2^j*u, which is
    # >= (3^j*u)^rho for rho=log_3(2). All other steps increase n.
    # With <=30 contraction blocks the log2 height still exceeds 62.
    block_limit = 30
    if not (2**100 > 3**63 and
            (HEIGHT - 1)*63**block_limit > short_bits*100**block_limit):
        raise AssertionError("Contraction-block bound failed")
    # At least 31 contraction blocks require 30 intervening expansions.
    # Before the first dip n>=2^62, in particular n>=16. Each expansion
    # gains a factor >= (4*n-1)/(2*n) >= 63/32 over the baseline 2/3.
    extra_bits = 29
    if short_bits < 4 or 63**block_limit <= (1 << extra_bits)*32**block_limit:
        raise AssertionError("Expansion gain bound failed")
    down = (altitude + extra_bits) // (alpha[1] - 1) + 1
    # The upward inequality need not be strict, so round the lower bound up.
    up = -((-altitude) // (2 - alpha[0]))
    gap = min(short_horizon + 1, down + up)
    period = DEPTH + 17 + FIRST_FORWARD + gap
    print("Before the first short-connection dip there must be at least 31 contraction blocks.")
    print(f"At least {down:,} steps down and {up:,} back up in the short case.")
    print(f"Closing segment >= {gap:,} steps. Least period, if finite, >= {period:,}.")


if __name__ == "__main__":
    verify()
