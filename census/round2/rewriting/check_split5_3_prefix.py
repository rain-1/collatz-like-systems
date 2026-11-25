"""Count exact parity-prefix candidates and cross-check the walk identity."""

from math import comb

from check_split5_3_recovery import bit_step


def count_words(limit):
    by_ones = [1]
    totals = [1]
    terminal_counts = [1]
    for length in range(1, limit + 1):
        # The allowed one-count increases by either zero or one at each bit.
        upper = len(by_ones) - 1
        if 5**(length - upper - 1) >= 4**length:
            upper += 1
        assert 5**(length - upper) >= 4**length
        assert 5**(length - upper - 1) < 4**length
        extended = [a+b for a, b in zip([0] + by_ones, by_ones + [0])]
        by_ones = extended[:upper + 1]
        totals.append(sum(by_ones))
        terminal_counts.append(sum(comb(length, k) for k in range(upper + 1)))
        assert length*totals[length] == sum(
            terminal_counts[j] * totals[length-j] for j in range(1, length+1)
        )
    return totals


def passes_prefix(y, bits):
    z, flag = y, 0
    even_bits = 0
    for j in range(1, bits+1):
        even_bits += int(z % 2 == 0)
        if 5**even_bits < 4**j:
            return False
        z, flag = bit_step(z, flag)
    return True


if __name__ == "__main__":
    totals = count_words(512)
    for length in range(2, 17):
        low = 1 << length
        observed = sum(passes_prefix(y, length) for y in range(low, 2*low))
        assert observed == totals[length]
    assert totals[66] == 2150900120
    witness = 19469588806135160832
    assert passes_prefix(witness, 145) and not passes_prefix(witness, 146)
    z, flag = witness, 0
    for length in range(1, 146):
        z, flag = bit_step(z, flag)
        assert ((z << flag) < witness) == (length == 145)
    for length in (16, 32, 64, 128, 512):
        print(f"{length} bits: {totals[length]:,} passing residue classes")
