"""Check a candidate potential on the 1932 Collatz permutation.

Let Z_t(n) count the multiples of 3 among the first t inputs. Give each
input deficit d=5 if divisible by 3 and d=-3 otherwise, so the deficit
over t steps is 8*Z_t-3*t. Let k be the number of ternary digits of n.
Define P(n) as the largest prefix deficit through k+1024 steps, including
the empty prefix. The proposed group potential is V=5*P/8. For n=3**a*u
with 3 not dividing u, P(n) is 5*a plus the largest prefix deficit from
2**a*u through digits_in_base_3(u)+1024 steps. Thus the first contraction
run is accounted for exactly.

The one-step inequality is P(n) >= d(n)+P(G(n)). A group with counts
(a,b) of divisible and nondivisible inputs has score 2*b-3*a. If the inequality
holds throughout the group, its score is at least V(next)-V(n)+(a+b)/8.
The constant 1024 was selected using an initial 50,000-step scan from 129.

Density bound. Write E(n)=max(0,d(n)+P(G(n))-P(n)). The next window ends
zero, one or two positions beyond the current end, since the ternary digit
length changes by at most one. Each position adds at most five deficit,
so E <= 10. For E>0, a prefix of length k+1025 or k+1026 must beat the
old maximum, which is nonnegative. Consequently 8*Z_k-3*k > -5*1026.
Over the complete residues mod 3**k the first k branch residues run over
all ternary words: lifting a start by 3**j changes its j-th iterate by a
power of 2, a unit mod 3. For z=33/32 the average of z**(8*Z_k-3*k)
is rho**k with rho=(2*z**(-3)+z**5)/3 < 1. Markov's inequality bounds
the number of possible exceptions in the k-digit shell by
z**(5*1026)*(3*rho)**k. Summing these bounds up to digits(X), and using
(3*rho)**1000 < 3**997, gives O(X**0.997) exceptions up to X.
This assertion concerns integer starts, not frequency along a single orbit.

Even exceptions can be tolerated: over T steps the original score is
at least (T + 5*(P(end)-P(start)) - 5*sum(E))/8. If fewer than a fixed
fraction below 1/50 of steps are exceptions along arbitrarily long
prefixes, the score is unbounded above, ruling out a cycle through 129.

First failure from 129. If t is its index, all prior signed defects
are <=0. Hence 8*Z_t-3*t <= P(129)-P(x_t) <=9. The preceding terms
are distinct: a whole cycle of nonpositive signed defects would have
Z/L <=3/8, whereas every good block from 129 strictly increases its
value (verify_good_block_induction.py). All terms are at least 8.
The exact growth factors are 2/3 or (4/3)*(1 +/- 1/(4*n)). The
loss from distinct n in [8,1023] is less than a factor four, because
(1-1/(4*n))**4 >= 1-1/n and the latter product is 7/1023.
For n >=1024 use at least 4095/4096 per step. Substitution gives
    x_t >= 129/(4*2**(9/8)) * ((4095/4096)*2**(13/8)/3)**t
        > 3**(t/40).
At a failure a newly exposed prefix strictly beats all prefix deficits
in the original window. Choose the first new strict record. Its length
is at least digits(x_t)+1025, and every nonempty suffix ending there
has strictly positive deficit by subtraction from the record. Thus this
one stretch has more than 3/8 multiples of 3 in every terminal segment.
"""

import argparse
from array import array
from collections import deque
from fractions import Fraction


PADDING = 1024


def check_counting_exponent():
    z = Fraction(33, 32)
    shell_factor = 2 / z**3 + z**5
    if not (1 < shell_factor and shell_factor**1000 < 3**997):
        raise AssertionError("Power bound on exceptional inputs failed")


def check_first_failure_constants():
    if 7 * 4**4 <= 1023 or 129**8 <= 4**8 * 2**9:
        raise AssertionError("Small-value growth allowance is insufficient")
    if 4095**40 * 2**65 <= 4096**40 * 3**41:
        raise AssertionError("Ternary digit growth bound failed")


def orbit_inputs(start):
    n = start
    digits = 1
    upper = 3
    while n >= upper:
        digits += 1
        upper *= 3
    while True:
        q, r = divmod(n, 3)
        yield digits, 5 if r == 0 else -3
        n = 2*q if r == 0 else 4*q + 2*r - 1
        if n >= upper:
            digits += 1
            upper *= 3
        elif 3*n < upper:
            digits -= 1
            upper //= 3


def check_interval(start, steps):
    inputs = orbit_inputs(start)
    prefix = array("q", [0])
    ends = array("Q")
    for i in range(steps + 1):
        digits, deficit = next(inputs)
        ends.append(i + digits + PADDING)
        prefix.append(prefix[-1] + deficit)
    while len(prefix) <= ends[-1]:
        _, deficit = next(inputs)
        prefix.append(prefix[-1] + deficit)

    # In absolute coordinates P(x_i) = max(prefix[i:end+1]) - prefix[i].
    # The signed one-step defect is the difference of adjacent window maxima.
    candidates = deque()
    right = -1
    previous_max = initial_value = first_failure = None
    failures = total_defect = 0
    for i, end in enumerate(ends):
        while right < end:
            right += 1
            while candidates and prefix[candidates[-1]] <= prefix[right]:
                candidates.pop()
            candidates.append(right)
        while candidates[0] < i:
            candidates.popleft()
        maximum = prefix[candidates[0]]
        if previous_max is None:
            initial_value = maximum
        elif maximum > previous_max:
            defect = maximum - previous_max
            if defect > 10:
                raise AssertionError("One-step defect exceeds the proved upper bound")
            if first_failure is None:
                first_failure = (i - 1, defect)
            failures += 1
            total_defect += defect
        previous_max = maximum
    return initial_value, failures, total_defect, first_failure


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--start", type=int, default=129)
    parser.add_argument("--steps", type=int, default=250_000)
    args = parser.parse_args()
    if args.start <= 0 or args.steps <= 0:
        parser.error("start and steps must be positive")
    check_counting_exponent()
    check_first_failure_constants()
    p, count, total, first = check_interval(args.start, args.steps)
    print(f"Start {args.start}, initial P = {p}, tested {args.steps} ordinary steps.")
    print(f"One-step failures: {count}. Sum of positive defects: {total}.")
    if first is not None:
        print(f"First failure at step {first[0]} with defect {first[1]}.")
