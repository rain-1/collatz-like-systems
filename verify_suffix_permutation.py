"""Verify an infinite orbit for a three-branch binary suffix permutation.

The rules replace 0 by 00, 01 by 10, and 11 by 1 at the right end
of a binary expansion. They define a permutation because the source and
target suffixes each partition the positive integers into three classes.
"""

from collections import deque

from verify_binary_invariant import binary_state


RULES = (("0", "00"), ("01", "10"), ("11", "1"))

# States track no 1 yet, one 1 with no trailing zeros yet, one 1 with
# trailing zeros, or at least two 1s. Only the third state accepts.
TRANSITIONS = ((0, 1), (2, 3), (2, 3), (3, 3))
ACCEPTING = {2}


def step(n):
    bits = format(n, "b")
    for source, target in RULES:
        if bits.zfill(len(source)).endswith(source):
            return int(bits[:-len(source)] + target, 2)
    raise AssertionError("No branch for the input")


def append_state(transitions, state, suffix):
    for bit in suffix:
        state = transitions[state][int(bit)]
    return state


def closure_violation(transitions, accepting):
    """Return a counterexample edge, or None after checking every quotient."""
    # At quotient zero only the positive inputs 1 and 3 apply. Canonical
    # representations omit the leading zero on the input suffix 01.
    for source in (1, 3):
        target = step(source)
        if (binary_state(transitions, source) in accepting
                and binary_state(transitions, target) not in accepting):
            return source, target

    first = binary_state(transitions, 1)
    queue = deque([(first, 1)])
    seen = {first}
    while queue:
        state, quotient = queue.popleft()
        for source, target in RULES:
            if (append_state(transitions, state, source) in accepting
                    and append_state(transitions, state, target) not in accepting):
                prefix = format(quotient, "b")
                return int(prefix + source, 2), int(prefix + target, 2)
        for bit, successor in enumerate(transitions[state]):
            if successor not in seen:
                seen.add(successor)
                queue.append((successor, 2 * quotient + bit))
    return None


def verify():
    start = 1
    if binary_state(TRANSITIONS, start) in ACCEPTING:
        raise AssertionError("The initial point must be rejected")
    if binary_state(TRANSITIONS, step(start)) not in ACCEPTING:
        raise AssertionError("The first image must be accepted")
    edge = closure_violation(TRANSITIONS, ACCEPTING)
    if edge is not None:
        raise AssertionError(f"Closure fails at {edge[0]} -> {edge[1]}")
    print("Verified a four-state binary certificate for the infinite orbit of 1.")


if __name__ == "__main__":
    verify()
