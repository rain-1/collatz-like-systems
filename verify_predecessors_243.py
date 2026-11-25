"""Check predecessors of 243 and a period lower bound for the orbit of 8.

Only integer arithmetic is used. The backward search tests inputs at depths
0 through DEPTH-1 and then records the bit length of the endpoint at DEPTH.
"""

from functools import lru_cache


DEPTH = 4_000_002
BACKWARD_BLOCK = 6
FORWARD_BLOCK = 8


def forward(n):
    q, r = divmod(n, 3)
    if r == 0:
        return 2 * q
    return 4 * q + 2 * r - 1


def backward(n):
    if n % 2 == 0:
        return 3 * (n >> 1)
    return (3 * n + (1 if n % 4 == 1 else -1)) >> 2


@lru_cache(maxsize=None)
def backward_block(low):
    # At most ten bits have been consumed before the sixth input, so all
    # six low-order residues modulo 64 are determined by the initial 16 bits.
    value = low
    bits_used = 0
    possible_multiple_of_64 = False
    for _ in range(BACKWARD_BLOCK):
        possible_multiple_of_64 |= value % 64 == 0
        bits_used += 1 + value % 2
        value = backward(value)
    offset = (value << bits_used) - 3**BACKWARD_BLOCK * low
    return bits_used, offset, possible_multiple_of_64


def check_predecessors():
    assert DEPTH % BACKWARD_BLOCK == 0
    n = 243
    smallest = (n, 0)
    powers_of_two = []
    for depth in range(0, DEPTH, BACKWARD_BLOCK):
        bits_used, offset, possible = backward_block(n & 65535)
        endpoint = (3**BACKWARD_BLOCK * n + offset) >> bits_used
        # Each inverse step gives at least n/2. When this cutoff holds,
        # every input exceeds 243, and a power of two must be a multiple of 64.
        if n.bit_length() <= BACKWARD_BLOCK + 8 or possible:
            value = n
            for j in range(BACKWARD_BLOCK):
                if value < smallest[0]:
                    smallest = (value, depth + j)
                if value & (value - 1) == 0:
                    powers_of_two.append((value, depth + j))
                value = backward(value)
            assert value == endpoint
        n = endpoint
    assert not powers_of_two
    assert smallest == (130, 7)
    return n.bit_length()


@lru_cache(maxsize=None)
def forward_block(low):
    value = low
    bits_added = 0
    for _ in range(FORWARD_BLOCK):
        bits_added += 1 + (value % 3 != 0)
        value = forward(value)
    return value, bits_added


def first_forward_index_with_bits(target):
    n, index = 8, 0
    modulus = 3**FORWARD_BLOCK
    while n.bit_length() < target:
        # G(n) <= 2n, so skip the block only if every state is too small.
        if n.bit_length() + FORWARD_BLOCK < target:
            q, r = divmod(n, modulus)
            value, bits_added = forward_block(r)
            n = (q << bits_added) + value
            index += FORWARD_BLOCK
        else:
            n = forward(n)
            index += 1
    return index


if __name__ == "__main__":
    value = 243
    for depth in range(1, 175):
        value = backward(value)
        if depth == 7:
            assert value == 130
        if depth < 174:
            assert value % 243
    assert value == 243 * 221
    value = 243
    for step in range(17):
        assert value != 8
        value = forward(value)
    assert value == 8
    bits = check_predecessors()
    first_index = first_forward_index_with_bits(bits)
    print("Backward endpoint bit length:", bits)
    print("First forward index from 8 reaching that bit length:", first_index)
    print("Lower bound for a finite period:", DEPTH + 17 + first_index)
