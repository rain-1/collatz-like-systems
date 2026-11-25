"""Verify the three exact basins of the modulo-four Collatz variant with d=73."""

from verify_binary_invariant import binary_state


D = 73
SQUARES = {i * i % D for i in range(1, D)}
# Each label is the least integer on the predicted cycle.
PERIODS = {3: 12, 5: 28, 73: 3}


def label(residue):
    if residue == 0:
        return 73
    return 3 if residue in SQUARES else 5


def step(n, d=D):
    if n % 2 == 0:
        return n // 2
    return 3 * n + d if n % 4 == 1 else n + d


def cycle(n):
    path = []
    offsets = {}
    while n not in offsets:
        if not 1 <= n <= 4 * D:
            raise AssertionError("Escape from the bounded odd-return calculation")
        offsets[n] = len(path)
        path.append(n)
        n = step(n)
    loop = path[offsets[n]:]
    first = loop.index(min(loop))
    return tuple(loop[first:] + loop[:first])


def verify():
    transitions = [[(2 * r + bit) % D for bit in (0, 1)] for r in range(D)]
    # Representatives modulo 4d determine both the branch and its output
    # modulo d, including on the halving branch.
    for n in range(1, 4 * D + 1):
        state = binary_state(transitions, n)
        if state != n % D or label(state) != label(step(n) % D):
            raise AssertionError(f"Failed residue certificate at {n}")

    # For an odd n>d the next odd is at most (3n+d)/4<n. For odd n<=d
    # the same bound is <=d. These starts therefore cover every orbit.
    loops = {}
    for n in range(1, D + 1, 2):
        loop = cycle(n)
        predicted = label(n % D)
        if (loop[0] != predicted or len(loop) != PERIODS[predicted]
                or loops.setdefault(predicted, loop) != loop):
            raise AssertionError(f"Wrong cycle for {n}")
    if loops.keys() != PERIODS.keys():
        raise AssertionError("A predicted cycle is missing")
    for first, loop in sorted(loops.items()):
        print(f"Cycle through {first}, period {len(loop)}: {list(loop)}")
    print("Verified every residue transition and all 37 odd starts in the bounded region.")


if __name__ == "__main__":
    verify()
