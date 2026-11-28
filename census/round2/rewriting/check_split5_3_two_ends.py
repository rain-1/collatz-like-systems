"""Verify the signed prefix/middle/suffix decomposition over exact integers."""

from collections import defaultdict

from check_split5_3_microrange import haar_counts, raw_passes


def segment(bits, flag):
    """Return (five-count, ending flag, affine numerator offset)."""
    count = offset = 0
    for i, bit in enumerate(bits):
        if bit:
            offset += 3 << i
        else:
            if flag:
                count += 1
                offset *= 5
            flag ^= 1
    return count, flag, offset


def bits_of(y, length):
    z, flag = y, 0
    word = []
    for _ in range(length):
        word.append(z % 2)
        if z % 2:
            z = (z + 3) // 2
        else:
            z = (5 if flag else 1) * z // 2
            flag ^= 1
    return tuple(word)


def inverse_residue(offset, count, modulus):
    return -offset * pow(5**count, -1, modulus) % modulus


def check_split(length, prefix_length, tail_length, survivors):
    modulus = 1 << length
    groups = defaultdict(dict)
    live_prefixes = defaultdict(set)
    for y, word in survivors:
        prefix = word[:prefix_length]
        middle = word[prefix_length:-tail_length]
        tail = word[-tail_length:]
        t = sum(prefix)
        live_prefixes[t].add(prefix)
        groups[t, middle].setdefault(prefix, {})[tail] = y

    # Root of unity in a finite field, so signed character comparisons are exact.
    prime = 998244353
    root = pow(3, (prime-1)//modulus, prime)
    for freq in (1, 2, 5, 10):
        def phase(i):
            return pow(root, freq*i, prime)
        total = 0
        for (t, middle), by_prefix in groups.items():
            assert set(by_prefix) == live_prefixes[t]
            first = next(iter(by_prefix))
            tails = by_prefix[first].keys()
            a, flag, _ = segment(first, 0)
            h = 5**a
            e, tail_flag, offset = segment(middle, flag)
            prefix_sum = 0
            for prefix, starts in by_prefix.items():
                assert starts.keys() == tails
                count, end, c = segment(prefix, 0)
                assert (count, end) == (a, flag) and 0 <= c <= 6*prefix_length*h
                u = inverse_residue(c, a, modulus)
                # u/Q = c (Q^-1 mod h)/h - c/(Q h) modulo one.
                assert (u*h - c*pow(modulus, -1, h)*modulus + c) % (modulus*h) == 0
                prefix_sum += phase(u)
            mid = inverse_residue(offset, e, modulus)
            mid = (mid << prefix_length)*pow(h, -1, modulus) % modulus
            tail_sum = 0
            for tail in tails:
                count, _, c = segment(tail, tail_flag)
                tail_residue = inverse_residue(c, count, 1 << tail_length)
                value = tail_residue*pow(5**(a+e), -1, 1 << tail_length)
                tail_sum += phase((value << (length-tail_length)) % modulus)
            total += prefix_sum * phase(mid) * tail_sum
        assert total % prime == sum(phase(y) for y, _ in survivors) % prime


if __name__ == "__main__":
    survivors = []
    for length, expected in enumerate(haar_counts(22), 1):
        if length < 6:
            continue
        modulus = 1 << length
        if length <= 16:
            candidates = range(modulus)
        else:
            candidates = [y + lift for y, _ in survivors for lift in (0, modulus//2)]
        survivors = [(y, bits_of(y, length)) for y in candidates
                     if raw_passes(4*modulus+y-3, length-1)]
        assert len(survivors) == expected
        for first, last in ((2, 2), (length//2, 2), (3, length//2)):
            check_split(length, first, last, survivors)
        print(f"{length} bits: {expected} residues, three splits, four exact characters")
