"""Check a binary finite-state certificate for nonreturn of 8 under G.

With a JSON file argument, read a deterministic automaton of the form
{"transitions": [[0, 1], [1, 0]], "accepting": [1]}.
State 0 is the initial state. Read the canonical binary digits of a positive
integer from most significant to least significant, including the leading 1.
Without an argument, verify the eight-state lower bound from orbit labels.
With --smt STATES, emit a finite sample-fitting problem in SMT-LIB format.
An unsatisfiable result excludes that size. A satisfying result still
requires the exhaustive closure check on the proposed automaton.
Use search_binary_invariant.py for synthesis and binary_prefix_bound.py for
the stronger state lower bound that also uses forward closure.
"""

from collections import deque
from itertools import combinations
import json
import sys
from time import monotonic


def orbit_step(n):
    q, r = divmod(n, 3)
    return (2 * q, 4 * q + 1, 4 * q + 3)[r]


def inverse_step(n):
    if n % 2 == 0:
        return 3 * n // 2
    return (3 * n + (1 if n % 4 == 1 else -1)) // 4


def binary_state(transitions, n):
    state = 0
    for digit in format(n, 'b'):
        state = transitions[state][int(digit)]
    return state


def closure_violation(transitions, accepting, deadline=None):
    """Return an edge leaving the accepted set, or None after exhaustive BFS."""
    state = lambda n: binary_state(transitions, n)
    if state(2) in accepting and state(3) not in accepting:
        return 2, 3  # The only nontrivial branch at q=0.

    # Coordinates are the states reached by q, 3q, 3q+1, and 3q+2.
    initial = tuple(state(n) for n in (1, 3, 4, 5))
    queue = deque([(initial, 1)])
    seen = {initial}
    while queue:
        if deadline is not None and monotonic() >= deadline:
            raise TimeoutError("closure check timed out")
        states, q = queue.popleft()
        base, *triple = states
        even, odd = transitions[base]
        images = (even, transitions[even][1], transitions[odd][1])
        for r in range(3):
            if triple[r] in accepting and images[r] not in accepting:
                source = 3 * q + r
                return source, orbit_step(source)

        # 3*(2q+b)+r = 2*(3q + floor((3b+r)/2)) + ((3b+r) mod 2).
        for bit in (0, 1):
            next_triple = []
            for r in range(3):
                offset, last_bit = divmod(3 * bit + r, 2)
                next_triple.append(transitions[triple[offset]][last_bit])
            successor = (transitions[base][bit], *next_triple)
            if successor not in seen:
                seen.add(successor)
                queue.append((successor, 2 * q + bit))
    return None


PREFIXES = (1, 2, 3, 4, 8, 10, 12, 37)


def orbit_labels():
    positive, negative = set(), set()
    f = b = 8
    for _ in range(300):
        f = orbit_step(f)
        positive.add(f)
        negative.add(b)
        b = inverse_step(b)
    assert positive.isdisjoint(negative)
    return {n: True for n in positive if n < 4096} | {
        n: False for n in negative if n < 4096
    }


def verify_state_lower_bound(samples):
    # For each prefix, store a binary suffix by its length and its value.
    # Length zero includes the empty suffix. Leading zeros of suffixes matter.
    labels = {p: {} for p in PREFIXES}
    for n, label in samples.items():
        for length in range(n.bit_length()):
            prefix, tail = divmod(n, 1 << length)
            if prefix in labels:
                labels[prefix][length, tail] = label
    for p, q in combinations(PREFIXES, 2):
        shared = labels[p].keys() & labels[q].keys()
        assert any(labels[p][w] != labels[q][w] for w in shared), (p, q)


def emit_sample_problem(count):
    samples = orbit_labels()
    verify_state_lower_bound(samples)
    if count < len(PREFIXES):
        print("(assert false)\n(check-sat)")
        return
    nodes = {n >> i for n in samples for i in range(n.bit_length())}
    states = range(count)

    def exactly_one(names):
        for name in names:
            print(f"(declare-const {name} Bool)")
        print(f"(assert (or {' '.join(names)}))")
        for left, right in combinations(names, 2):
            print(f"(assert (or (not {left}) (not {right})))")

    for i in states:
        print(f"(declare-const accept_{i} Bool)")
        for bit in (0, 1):
            exactly_one([f"edge_{i}_{bit}_{j}" for j in states])
    for n in sorted(nodes):
        exactly_one([f"node_{n}_{i}" for i in states])
    # The eight prefixes must occupy distinct states in any solution. Name
    # those states in this order. The initial state before the leading 1 is
    # left unconstrained, which only relaxes the sample-fitting problem.
    for i, n in enumerate(PREFIXES):
        print(f"(assert node_{n}_{i})")
    for n in sorted(nodes):
        for i in states:
            if n in samples:
                accept = f"accept_{i}" if samples[n] else f"(not accept_{i})"
                print(f"(assert (=> node_{n}_{i} {accept}))")
            if n > 1:
                for j in states:
                    print(f"(assert (=> (and node_{n//2}_{i} edge_{i}_{n%2}_{j}) node_{n}_{j}))")
    print("(check-sat)")


def main():
    if len(sys.argv) == 1:
        verify_state_lower_bound(orbit_labels())
        print("All 28 prefix pairs are distinguishable. At least eight states are required.")
        return 0
    if len(sys.argv) == 3 and sys.argv[1] == "--smt":
        emit_sample_problem(int(sys.argv[2]))
        return 0
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 verify_binary_invariant.py [candidate.json]")
    with open(sys.argv[1], encoding="utf-8") as f:
        candidate = json.load(f)
    transitions = candidate["transitions"]
    accepting = set(candidate["accepting"])
    states = range(len(transitions))
    if not transitions or any(len(row) != 2 for row in transitions):
        raise ValueError("Supply two transitions per state.")
    if any(type(i) is not int or i not in states for row in transitions for i in row):
        raise ValueError("Invalid transition state.")
    if any(type(i) is not int or i not in states for i in accepting):
        raise ValueError("Invalid accepting state.")
    if binary_state(transitions, 11) not in accepting or binary_state(transitions, 8) in accepting:
        print("Candidate must accept 11 and reject 8.")
        return 1
    violation = closure_violation(transitions, accepting)
    if violation is not None:
        print(f"Forward closure fails at {violation[0]} -> {violation[1]}.")
        return 1
    print("Verified: 11 is accepted, 8 is rejected, and the set is forward invariant.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
