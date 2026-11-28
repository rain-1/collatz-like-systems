"""Check the all-starts height/slope certificate and the translated block reduction."""
from fractions import Fraction


def reciprocal_gap(depth):
    """Minimum of |1-2^j/3^a| for 1 <= j <= depth and 0 <= a <= j."""
    best, witness = Fraction(1), (1, 0)
    power = 1
    for a in range(1, depth + 1):
        power *= 3
        below = power.bit_length() - 1
        # On either side of 3^a the closest admissible 2^j is at a boundary.
        for j in {min(depth, below), min(depth, below + 1)}:
            if j >= a:
                gap = Fraction(abs(power - (1 << j)), power)
                if gap < best:
                    best, witness = gap, (j, a)
    return best, witness


def thresholds(depth):
    """Least a for which 3^a >= 2^j, using exact comparisons."""
    result = [0]
    a, power = 0, 1
    for j in range(1, depth + 1):
        if power < 1 << j:
            a += 1
            power *= 3
        result.append(a)
    return result


def first_disagreements(d, bound, limits):
    differing = []
    # Every positive even start drops by both tests at step one.
    for n in range(1, bound + 1, 2):
        x, odd = n, 0
        for j in range(1, len(limits)):
            if x & 1:
                x = (3*x + d) // 2
                odd += 1
            else:
                x //= 2
            height_drop = x < n
            slope_drop = odd < limits[j]
            if height_drop or slope_drop:
                if height_drop != slope_drop:
                    differing.append((n, j))
                break
    return differing


def prefix(x, steps, d, limits, odd=0, elapsed=0):
    for j in range(elapsed + 1, elapsed + steps + 1):
        if x & 1:
            odd += 1
            x = (3*x + d) // 2
        else:
            x //= 2
        if odd < limits[j]:
            return None
    return x, odd


def verify_translated_blocks():
    m, split, b = 6, 3, 8
    length, stride = 1 << m, 1 << split
    modulus = 1 << (b - split)
    limits = thresholds(b)
    for d in (-5, -1, 1, 3, 5):
        lower = upper = 0
        for r in range(stride):
            first = prefix(r, split, d, limits)
            if first is None:
                continue
            _, a = first
            continuation = [prefix(i, b-split, d, limits, a, split) is not None
                            for i in range(modulus)]
            sizes = [sum(continuation[(3**a * s + offset) % modulus]
                         for s in range(length // stride)) for offset in range(modulus)]
            lower += min(sizes)
            upper += max(sizes)
        # Every translate modulo 2^b, including blocks that wrap around.
        actual = [prefix(i, b, d, limits) is not None for i in range(1 << b)]
        for start in range(1 << b):
            count = sum(actual[(start+i) % (1 << b)] for i in range(length))
            assert lower <= count <= upper


def verify():
    verify_translated_blocks()
    depth = 3012
    gap, witness = reciprocal_gap(depth)
    assert witness == (1054, 665)
    cap = int(Fraction(depth, 3) / gap)
    assert cap == 22_999_481
    limits = thresholds(depth)
    print(f"All candidates lie below or at {cap:,}.", flush=True)
    for d in (1, -1):
        result = first_disagreements(d, cap, limits)
        print(f"d={d}: first disagreements (start, step) = {result}", flush=True)
        assert result == ([(1, 2)] if d == 1 else [])


if __name__ == "__main__":
    verify()
