"""Compare passing-word numerators with their exact octave grids for split5_3."""

from bisect import bisect_right
from collections import Counter, defaultdict

from check_split5_3_microrange import code, haar_counts, raw_passes


def passing_numerators(depth):
    modulus = 1 << depth
    groups = defaultdict(list)

    def visit(i, fives, flag, numerator):
        halvings = i - flag
        if halvings < depth and 5**fives < 1 << halvings:
            return
        if i == depth:
            groups[fives, flag].append(numerator % modulus)
            return
        visit(i + 1, fives, flag, numerator + (3 << i))
        visit(i + 1, fives + flag, 1 - flag, numerator * (5 if flag else 1))

    visit(0, 0, 0, 0)
    return groups


def check_octave(m, depth, print_gaps=False):
    size, modulus = 1 << m, 1 << depth
    assert 2 * size + 2 < modulus
    groups = passing_numerators(depth)
    total = sum(map(len, groups.values()))
    assert total == list(haar_counts(depth - 1))[-1]
    hits = []
    for fives in sorted({a for a, flag in groups}):
        factor = 5**fives
        inverse = pow(factor, -1, modulus)
        grid = sorted(-factor * y % modulus for y in range(size + 3, 2 * size + 3))
        gaps = [right - left for left, right in zip(grid, grid[1:])]
        gaps.append(modulus + grid[0] - grid[-1])
        gap_counts = Counter(gaps)
        assert len(gap_counts) <= 3 and sum(gaps) == modulus
        occupancy = Counter()
        for flag in (0, 1):
            for numerator in groups.get((fives, flag), ()):
                j = bisect_right(grid, numerator) - 1
                occupancy[gaps[j]] += 1
                if grid[j] == numerator:
                    y = -inverse * numerator % modulus
                    hits.append(y - 3)
                    assert code(y, depth)[-1][:2] == (fives, flag)
        if print_gaps:
            population = sum(occupancy.values())
            for gap, count in sorted(gap_counts.items()):
                expected = population * count * gap / modulus
                print(f"A={fives} gap={gap} intervals={count} "
                      f"observed={occupancy[gap]} uniform={expected:.1f}")

    direct = [n for n in range(size, 2 * size) if raw_passes(n, depth - 1)]
    assert sorted(hits) == direct
    print(f"m={m} D={depth} words={total} hits={direct} mean={total * size / modulus:.8g}")
    return direct


if __name__ == "__main__":
    for m in range(1, 17):
        depth = (12 * m + 4) // 5 + 1
        assert check_octave(m, depth, print_gaps=(m == 16)) == []

    calibration = check_octave(18, 26)
    assert calibration == [278525, 281853, 303101, 348157, 435197, 524285]
    for n in calibration:
        states = code(n + 3, 26)
        bits = [(n + 3) % 2] + [z % 2 for a, flag, z in states[:-1]]
        print(n, "".join(map(str, bits)), states[-1][:2])
    assert 5**31 < 2**72  # (5/4)^31 < 2^10
