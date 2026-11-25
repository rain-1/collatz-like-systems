"""Prove that starts 1 <= n < 2**bits reach one of five recorded cycles."""

import argparse


CYCLE_PERIODS = {1: 4, 3: 2, 5: 5, 61: 10, 125: 11}


def step(n):
    if n % 2 == 0:
        return n // 2
    return 5 * n + 3 if n % 4 == 1 else n + 3


def verify(bits):
    if bits < 1:
        raise ValueError("bits must be positive")
    for root, period in CYCLE_PERIODS.items():
        value = root
        for index in range(1, period + 1):
            value = step(value)
            if (value == root) != (index == period):
                raise AssertionError((root, period, index))

    bound = 1 << bits
    # For n = modulus*t + residue, slope*t + offset is a reached value.
    pending = [(1, 0, 1, 0)]
    nodes = individually_checked = covered = max_extra_steps = 0
    while pending:
        modulus, residue, slope, offset = pending.pop()
        nodes += 1
        uniformly_smaller = slope == modulus and offset < residue
        if slope < modulus or uniformly_smaller or modulus == bound:
            stop = bound // modulus
            start = int(residue == 0)  # exclude n = 0
            covered += stop - start
            if uniformly_smaller:
                continue
            if slope < modulus:
                # All larger t already have slope*t+offset < modulus*t+residue.
                stop = min(stop, (offset - residue) // (modulus - slope) + 1)
            for t in range(start, stop):
                n = modulus * t + residue
                value = slope * t + offset
                individually_checked += 1
                extra_steps = 0
                while value >= n and value not in CYCLE_PERIODS:
                    value = step(value)
                    extra_steps += 1
                    if extra_steps > 100_000:
                        raise RuntimeError(f"unresolved start {n}")
                max_extra_steps = max(max_extra_steps, extra_steps)
            continue

        for digit in (0, 1):
            child_residue = residue + modulus * digit
            y = offset + slope * digit
            # At this child the reached value is 2*slope*u + y.
            if y % 2 == 0:
                next_slope, next_offset = slope, y // 2
            elif slope % 2:
                # Only parity is known. Read another bit before an odd step.
                next_slope, next_offset = 2 * slope, y
            elif y % 4 == 1:
                next_slope, next_offset = 5 * (slope // 2), (5 * y + 3) // 4
            else:
                next_slope, next_offset = slope, (y + 3) // 2
            pending.append((2 * modulus, child_residue, next_slope, next_offset))

    if covered != bound - 1:
        raise AssertionError(f"covered {covered} of {bound - 1}")
    print(f"{covered:,} starts certified, {nodes:,} tree nodes, "
          f"{individually_checked:,} individual checks, "
          f"at most {max_extra_steps} extra raw steps")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bits", type=int, nargs="?", default=48)
    verify(parser.parse_args().bits)
