"""Verify three orbit constructions using complete arithmetic progressions."""

from argparse import ArgumentParser
from fractions import Fraction
from itertools import combinations
from math import gcd

from verify_binary_invariant import binary_state
from verify_suffix_permutation import append_state


SUFFIXES = (("1", "1100"), ("100", "1"), ("10", "10"),
            ("0000", "000"), ("1000", "0100"))
TRAILING_ZEROS = ((1, 0), (2, 0), (3, 0), (3, 0))
PARITY = ((0, 1), (0, 1))


def check_partition(classes):
    """Each pair (period, first term) describes a full positive residue class."""
    for period, first in classes:
        if not 1 <= first <= period:
            raise ValueError("Missing or invalid initial representative")
    for (a, x), (b, y) in combinations(classes, 2):
        if (x - y) % gcd(a, b) == 0:
            raise ValueError("Overlapping residue classes")
    # A disjoint union of periodic classes with density one covers every residue
    # modulo their common period.
    if sum(Fraction(1, a) for a, _ in classes) != 1:
        raise ValueError("Incomplete residue partition")


def check_permutation(rules):
    check_partition([source for source, _ in rules])
    check_partition([target for _, target in rules])


def step(rules, n):
    for (period, first), (new_period, new_first) in rules:
        quotient, residue = divmod(n - first, period)
        if residue == 0 and quotient >= 0:
            return new_period * quotient + new_first
    raise ValueError(f"No rule applies to {n}")


def check_seed(transitions, accepting, rules, seed):
    if (binary_state(transitions, seed) in accepting
            or binary_state(transitions, step(rules, seed)) not in accepting):
        raise ValueError("Certificate fails to separate the seed and its image")


def verify_suffixes():
    rules = []
    accepting = {0, 2}
    for source, target in SUFFIXES:
        a, b = 2 ** len(source), 2 ** len(target)
        x, y = int(source, 2), int(target, 2)
        # If the source suffix is all zeros, the first positive quotient is 1.
        first_quotient = int(x == 0)
        rules.append(((a, a * first_quotient + x), (b, b * first_quotient + y)))
        if x and (binary_state(TRAILING_ZEROS, x) in accepting
                  and binary_state(TRAILING_ZEROS, y) not in accepting):
            raise ValueError("Closure failed at quotient zero")
        for state in range(len(TRAILING_ZEROS)):
            if (append_state(TRAILING_ZEROS, state, source) in accepting
                    and append_state(TRAILING_ZEROS, state, target) not in accepting):
                raise ValueError("Closure failed for a positive prefix")
    check_permutation(rules)
    check_seed(TRAILING_ZEROS, accepting, rules, 8)


def family_rules(d, excursion):
    if excursion:
        rules = [((4, 4), (8, 6)), ((8, 2), (8, 2)),
                 ((4, 1), (4 * (d + 1), 4)), ((4, 3), (2, 1))]
        for r in range(1, d + 1):
            rules.append(((8 * d, 8 * r - 2), (4 * (d + 1), 4 * (r + 1))))
    else:
        rules = [((4, 1), (2 * (d + 1), 2)), ((4, 3), (2, 1))]
        for r in range(1, d + 1):
            rules.append(((2 * d, 2 * r), (2 * (d + 1), 2 * (r + 1))))
    return rules


def verify_family(d, excursion):
    rules = family_rules(d, excursion)
    check_permutation(rules)
    check_seed(PARITY, {0}, rules, 1)
    for (a, x), (b, y) in rules:
        # The two possible quotient parities cover the entire progression.
        for q in (0, 1):
            if (a * q + x) % 2 == 0 and (b * q + y) % 2:
                raise ValueError("An even input has an odd image")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--d", type=int, default=2, help="family parameter (at least 2)")
    args = parser.parse_args()
    if args.d < 2:
        parser.error("--d must be at least 2")
    verify_suffixes()
    print("Verified the suffix permutation and its four-state certificate at 8.")
    for excursion in (False, True):
        verify_family(args.d, excursion)
    print(f"Verified both permutations and their two-state certificates at 1 for d={args.d}.")
