"""Verify a lower bound on DFA size for the Collatz invariant search.

If two leading binary strings end at the same state, replacing either one
by the other preserves membership for every common suffix. A path from 11
to 8 using such replacements and forward G steps contradicts invariance.
Applying the same test with two proposed equalities rules out their joint
occurrence, even when neither equality alone has been ruled out.
All witnesses here use only positive integers at most 2**32.
"""

from itertools import combinations, product

from verify_binary_invariant import inverse_step, orbit_step


PREFIX_LIMIT = 1 << 20
DISTINCT_PREFIXES = (*range(1, 96), 97, 98, 99, 100, 102, 103, 104, 105, 107, 110, 111)
WITNESS_LIMITS = tuple(1 << bits for bits in (18, 20, 23, 25, 27, 30, 32))
# These are possible overlaps, not asserted equalities. All unlisted anchor
# matches are ruled out by single substitutions, and simultaneous matches of
# two different extra prefixes are ruled out by two substitutions together.
EXTRA_MATCHES = {
    101: (92, 97, 107), 106: (105, 110), 108: (99,),
    112: (110, 111), 114: (83, 111), 115: (103, 104, 110),
}
MIN_STATES = len(DISTINCT_PREFIXES) + len(EXTRA_MATCHES)


def incompatible(p, q, limit=PREFIX_LIMIT):
    return conflicting_matches(((p, q),), limit)


def conflicting_matches(matches, limit):
    """A meeting proves that the proposed state equalities cannot all hold."""
    frontiers = [{11}, {8}]
    seen = [{11}, {8}]
    substitutions = [(a, b, a.bit_length()) for p, q in matches for a, b in ((p, q), (q, p))]
    while frontiers[0] and frontiers[1]:
        direction = int(len(frontiers[0]) > len(frontiers[1]))
        advance = inverse_step if direction else orbit_step
        other = seen[1 - direction]
        visited = seen[direction]
        next_frontier = set()
        for n in frontiers[direction]:
            neighbors = [advance(n)]
            for old, new, bits in substitutions:
                suffix_bits = n.bit_length() - bits
                if suffix_bits >= 0 and n >> suffix_bits == old:
                    neighbors.append(n + ((new - old) << suffix_bits))
            for m in neighbors:
                if m in other:
                    return True
                if m <= limit and m not in visited:
                    visited.add(m)
                    next_frontier.add(m)
        frontiers[direction] = next_frontier
    return False


def verify_distinct_prefixes():
    for p, q in combinations(DISTINCT_PREFIXES, 2):
        # Try smaller graphs first. Only a successful meeting proves a conflict.
        if not any(incompatible(p, q, limit) for limit in WITNESS_LIMITS):
            raise RuntimeError(f"Missing prefix incompatibility witness for {p}, {q}.")
    return len(DISTINCT_PREFIXES)


def verify_overlap_bound():
    anchors = verify_distinct_prefixes()
    single_limits = tuple(1 << bits for bits in (17, 19, 21, 23, 25, 27, 30, 32))
    for p, allowed in EXTRA_MATCHES.items():
        for a in DISTINCT_PREFIXES:
            if a not in allowed and not any(incompatible(p, a, n) for n in single_limits):
                raise RuntimeError(f"Missing single-match witness for {p}, {a}.")
    for p, q in combinations(EXTRA_MATCHES, 2):
        if not any(incompatible(p, q, n) for n in single_limits):
            raise RuntimeError(f"Missing extra-prefix witness for {p}, {q}.")
        for a, b in product(EXTRA_MATCHES[p], EXTRA_MATCHES[q]):
            if a == b:  # p and q were just proved distinct.
                continue
            pair = ((p, a), (q, b))
            if not any(conflicting_matches(pair, 1 << bits) for bits in (13, 16, 19, 22)):
                raise RuntimeError(f"Missing simultaneous-match witness for {pair}.")
    return anchors + len(EXTRA_MATCHES) - 1


def verify_overlap_case(prefix, anchor):
    """Exclude one exact overlap, conditional on the previously checked bound."""
    if anchor not in EXTRA_MATCHES.get(prefix, ()):
        raise ValueError(f"Unknown overlap: {prefix}={anchor}")
    # With exactly one overlap the remaining prefixes name every one of the
    # 111 states. The probe must match at least one of these representatives.
    probe = 109 if (prefix, anchor) == (108, 99) else 96
    representatives = (*DISTINCT_PREFIXES, *(p for p in EXTRA_MATCHES if p != prefix))
    for other in representatives:
        matches = ((prefix, anchor), (probe, other))
        if not any(conflicting_matches(matches, 1 << bits) for bits in (12, 15, 18, 21)):
            raise RuntimeError(f"Missing case witness for {matches}.")
    return probe


def verify_state_bound(report=None):
    previous_bound = verify_overlap_bound()
    for prefix, allowed in EXTRA_MATCHES.items():
        for anchor in allowed:
            probe = verify_overlap_case(prefix, anchor)
            if report is not None:
                report(prefix, anchor, probe)
    return previous_bound + 1


def extra_state_assignments(size):
    """Name the fresh states in prefix order, leaving the anchor names fixed."""
    overlaps = ((p, a) for p, allowed in EXTRA_MATCHES.items() for a in allowed)
    for overlap in (None, *overlaps):
        fresh = len(DISTINCT_PREFIXES)
        row = []
        for p in EXTRA_MATCHES:
            if overlap is not None and overlap[0] == p:
                row.append(DISTINCT_PREFIXES.index(overlap[1]))
            else:
                row.append(fresh)
                fresh += 1
        if fresh <= size:
            yield row


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=int, nargs=2, metavar=("PREFIX", "ANCHOR"),
                        help="replay one overlap case after verifying its common premises")
    args = parser.parse_args()

    def report(prefix, anchor, probe):
        print(f"Overlap {prefix}={anchor}: excluded using probe {probe}.", flush=True)

    if args.case is not None:
        p, a = args.case
        if a not in EXTRA_MATCHES.get(p, ()):
            parser.error(f"Unknown overlap: {p}={a}")
        verify_overlap_bound()
        report(p, a, verify_overlap_case(p, a))
    else:
        count = verify_state_bound(report)
        print(f"At least {count} states are required.")
