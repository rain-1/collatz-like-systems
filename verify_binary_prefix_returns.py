"""Verify the exact return gaps for the binary prefix 1000 under G.

For each j, write n = 3**j * q + r. Then G**j(n) = 2**a * q + b
for some 0 <= b < 2**a. At j=0 this holds with a=b=0. For the
induction step write the old q as 3*q_new + d. Dividing the old
iterate by 3 leaves quotient 2**a * q_new + (2**a * d + b)//3.
The latter summand is below 2**a. G appends one or two bits to
that quotient, preserving the claimed form.

Thus if n//3**j >= 8, its first four bits are those of G**j(n).
When n >= 16*3**7, n and n//2 have identical four-bit prefixes at
each time j=0,...,7, since (n//2)//3**j = (n//3**j)//2 >= 8.
Repeated halving reduces all larger inputs to the finite check below.

On the prefix 1000, compare the normalized input with 2187/2048.
For n >= 16*3**7 the threshold, expressed at the scale of n//2,
is an integer because the leading power of two of n//2 is at least
2**14. Thus n and n//2 fall on the same side, including at equality.
The halving reduction also proves the threshold test, with the three
small exceptions verified below.

For j steps with z inputs divisible by 3, a = 2*j - z. If q > 0,
the output bit length is q.bit_length() + a. On prefix 1000 with
k = n.bit_length()-1, dividing by 243 puts n/243 in [2**(k-8),
2**(k-7)). For a seven-step return above the threshold, n/2187 is
in [2**(k-11), 2**(k-10)). Thus at large inputs the bit length
changes by 2-z or 3-z respectively. Small starts are checked directly.
"""

from verify_binary_invariant import orbit_step


def starts_with_1000(n):
    return n >= 8 and n >> (n.bit_length() - 4) == 8


def below_gap_threshold(n):
    leading_power = 1 << (n.bit_length() - 1)
    return 2048 * n < 2187 * leading_power


def verify():
    horizon = 7
    cutoff = 16 * 3**horizon
    misses = []
    gaps = set()
    exceptions = []
    for n in range(1, cutoff):
        value = n
        hits = []
        for j in range(horizon + 1):
            if starts_with_1000(value):
                hits.append(j)
            if j < horizon:
                value = orbit_step(value)
        if not hits or hits[0] >= horizon:
            misses.append(n)
        if hits and hits[0] == 0:
            if len(hits) < 2:
                raise AssertionError(f"No return within seven steps from {n}")
            gaps.add(hits[1])
            if (hits[1] == 5) != below_gap_threshold(n):
                exceptions.append((n, hits[1]))
            returned = n
            multiples = 0
            for _ in range(hits[1]):
                multiples += returned % 3 == 0
                returned = orbit_step(returned)
            change = returned.bit_length() - n.bit_length()
            if change != (hits[1] - 1) // 2 - multiples:
                raise AssertionError((n, returned, multiples))

    if misses != [1, 2, 3, 4, 5, 6, 7, 9] or gaps != {5, 7}:
        raise AssertionError((misses, gaps))
    if exceptions != [(17, 7), (34, 7), (273, 7)]:
        raise AssertionError(exceptions)
    value = 66
    cycle_visits = []
    for j in range(1, 13):
        value = orbit_step(value)
        if starts_with_1000(value):
            cycle_visits.append((j, value))
    if cycle_visits != [(5, 70), (12, 66)]:
        raise AssertionError(cycle_visits)
    print(f"Checked starts 1 through {cutoff - 1}. Halving covers every larger start.")
    print("Only 1, 2, 3, 4, 5, 6, 7, 9 miss prefix 1000 in the first seven terms.")
    print("The first return from prefix 1000 always takes five or seven steps.")
    print("Below normalized threshold 2187/2048 the gap is five, except at 17, 34, 273.")
    print("At or above the threshold the gap is seven.")
    print("Closed orbit example: 66 -> 70 in five steps, 70 -> 66 in seven.")
    print("Bit-length change per return: 2 - multiples of 3 (five steps), or 3 - multiples of 3 (seven steps).")


if __name__ == "__main__":
    verify()
