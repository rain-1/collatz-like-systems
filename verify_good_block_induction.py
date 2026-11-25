"""Arithmetic tests for induction by blocks with at most 2/5 zero residues.

Growth. Discard the cycles {1}, {2,3}, and {4,5,7,9,6}. On the remaining
positive integers set H(n)=n except for the three weights below. With
b=21/16, H(G(n))/H(n) is at least 2/3 at residue zero and at least b
otherwise. For unmodified edges this follows from (4n-1)/(3n) >= b at
n >= 16, and (4n+1)/(3n) > 4/3. Of the remaining inputs below 16 only
10 and 13 are 1 mod 3. The edges incident to the modified values are
exactly 11 -> 15 -> 10 -> 13 -> 17. Their ratios are checked below.
For a good block of length t the product is consequently at least
((2/3)**2 * b**3)**(t/5) = (1029/1024)**(t/5). Since H(n) <= n, any
good block starting at n >= 16 ends strictly above its starting value.

Limitation on inherited binary tests. Let P be an infinite regular set
of canonical binary strings. Suppose every member could take a good
jump of 1 to B steps back into P, for a fixed B. Then from every member
one could chain such jumps. The cumulative score (2 per nonmultiple of
3 and -3 per multiple) would be nonnegative at every selected endpoint.

To see why this fails, pump a cycle after the leading 1 in a sufficiently
long accepting path. P contains a family of strings u v**(2j) w with v
nonempty. In integer values the family is
    n_j = n_0 + D * (b**j - 1)/(b - 1),
where D=n_1-n_0 > 0 and b=2**(2*len(v)) is 1 mod 3. Denote the
geometric sum by U_j. Then v3(U_h)=v3(h) for h>0: if 3 does not
divide h, U_h is h mod 3; tripling h multiplies U_h by
1+b**h+b**(2*h), which is 3 mod 9. Differences U_i-U_j for i>j
equal b**j * U_(i-j). Thus U_j permutes the residues mod every 3**T.

Let K=v3(D). The family has the same first K branches as n_0. The
affine formula gives G**K(n_j)=G**K(n_0)+2**a*(D//3**K)*U_j,
where a counts the binary bits appended in those K steps. The
coefficient is a unit mod 3. For every T some j therefore makes
G**K(n_j) divisible by 3**T. All of the next T inputs are multiples
of 3. Initial score is at most 2*K, so the cumulative score at time
K+i is negative for floor(2*K/3) < i <= T. Choose T to give at
least B consecutive negative positions. No chain of good jumps of
length at most B can cross them. This excludes a bounded good-return
rule on P even if its choice of jumps uses the whole integer.
"""

from fractions import Fraction

from verify_binary_invariant import inverse_step, orbit_step


EXPANSION = Fraction(21, 16)
CONTRACTION = Fraction(2, 3)
WEIGHTS = {
    13: 17 / EXPANSION,
    10: 17 / EXPANSION**2,
    15: 17 / (CONTRACTION * EXPANSION**2),
}


def verify_growth():
    if any(value > n for n, value in WEIGHTS.items()):
        raise AssertionError("Modified weight exceeds the integer")
    if 4 - 3 * EXPANSION != Fraction(1, 16):
        raise AssertionError("Incorrect threshold on the ordinary residue-one branch")
    affected = set(WEIGHTS) | {inverse_step(n) for n in WEIGHTS}
    if affected != {10, 11, 13, 15}:
        raise AssertionError(affected)
    for n in affected:
        image = orbit_step(n)
        factor = EXPANSION if n % 3 else CONTRACTION
        if WEIGHTS.get(image, image) < factor * WEIGHTS.get(n, n):
            raise AssertionError((n, image))
    if CONTRACTION**2 * EXPANSION**3 != Fraction(1029, 1024):
        raise AssertionError("Incorrect block growth factor")
    print("Every good block from n >= 16 has endpoint/start >= (1029/1024)^(length/5).")


def verify_first_jumps():
    n = 129
    for expected_length, expected_zeros, expected_end in ((3, 1, 153), (5, 2, 161), (1, 0, 215)):
        start, zeros = n, 0
        for length in range(1, expected_length + 1):
            zeros += n % 3 == 0
            n = orbit_step(n)
            if 5 * zeros <= 2 * length:
                break
        if (length, zeros, n) != (expected_length, expected_zeros, expected_end):
            raise AssertionError((start, length, zeros, n))
        print(f"{start} -> {n} in {length} steps, zero count {zeros}")

    # The 12-step orbit of 111 repeats with negative score, so one lap
    # suffices to check that it has no good nonempty prefix.
    n, score = 111, 0
    for _ in range(12):
        score += 2 - 5 * (n % 3 == 0)
        n = orbit_step(n)
        if score >= 0:
            raise AssertionError("Unexpected good prefix at 111")
    if n != 111 or score != -1:
        raise AssertionError((n, score))
    print("111 has no good block.")


def verify_seed_class():
    # Three steps from 129+27*t land at 153+32*t with the same residues.
    # Since 3**8 is 1 mod 32, the images include every 3**(8*j+6).
    if 3**6 % 32 != 153 % 32 or 3**8 % 32 != 1:
        raise AssertionError("Incorrect power progression")
    for t in (0, 1, 18):
        value, residues = 129 + 27*t, []
        for _ in range(3):
            residues.append(value % 3)
            value = orbit_step(value)
        if residues != [0, 2, 1] or value != 153 + 32*t:
            raise AssertionError((t, residues, value))
    print("The same three-step rule takes 615 to 729, followed by six multiples of 3.")


if __name__ == "__main__":
    verify_growth()
    verify_first_jumps()
    verify_seed_class()
