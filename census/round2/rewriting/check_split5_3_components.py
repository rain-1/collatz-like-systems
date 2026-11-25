"""Exact finite checks for the constructions in split5_3_components.md."""

from math import gcd, lcm

from check_split5_3_range import step


def order_of_two(modulus):
    order = 1
    while pow(2, order, modulus) != 1 % modulus:
        order += 1
    return order


def check_joint_residues():
    for modulus in (1, 3, 9, 11, 31, 101):
        order = order_of_two(modulus)
        depth = 1
        while order % 5 ** (depth + 1) == 0:
            depth += 1
        divisor = 5 ** (depth + 1)
        stride = lcm(order, 4 * 5**depth)
        for y in (1, 3, 61):
            initial = next(h for h in range(4 * 5**depth)
                           if (pow(2, h, divisor) * y + 12) % divisor == 0)
            residues = set()
            for index in range(1, 26):
                h = initial + stride * index
                power = y << h
                quotient, remainder = divmod(power + 12, divisor)
                assert remainder == 0
                w = 4**depth * quotient - 3
                residues.add((w % modulus, w % 25))
                for _ in range(depth):
                    assert w % 4 == 1
                    w = step(step(step(w)))
                assert w % 4 == 1 and step(w) == power
            assert len({r for r, t in residues}) == 1
            assert {t for r, t in residues} == set(range(25))


def check_residue_orbits():
    for modulus in range(1, 201, 2):
        if modulus % 5 == 0:
            continue
        inverse_five = pow(5, -1, modulus)
        for root in (1, 3):
            reached = {root % modulus}
            pending = list(reached)
            while pending:
                z = pending.pop()
                for value in (2*z - 3, (4*z - 3)*inverse_five):
                    residue = value % modulus
                    if residue not in reached:
                        reached.add(residue)
                        pending.append(residue)
            expected = {r for r in range(modulus)
                        if modulus % 3 or (r % 3 == 0) == (root % 3 == 0)}
            assert reached == expected


def check_binary_replay():
    for x in range(1, 129):
        for u in range(7):
            v, q = 2, 21
            modulus = 2**u * 5**v * q
            z, power_two, power_five = x, 1, 1
            raw_steps = 0
            for _ in range(u):
                if z % 4 == 1:
                    count, denominator = 3, 4
                    power_five *= 5
                elif z % 4 == 3:
                    count, denominator = 2, 2
                else:
                    count, denominator = 1, 2
                for _ in range(count):
                    z = step(z)
                raw_steps += count
                power_two *= denominator
            delta = 2 * 5**v * power_five * q
            w = x + power_two * delta // power_five
            assert (w - x) % modulus == 0
            for _ in range(raw_steps):
                w = step(w)
            assert w == z + delta


def next_odd(z):
    value = step(z)
    while value % 2 == 0:
        value //= 2
    return value


def check_tree():
    for root in (7, 9, 61):
        level = {root}
        visited = set(level)
        for _ in range(12):
            children = set()
            for z in level:
                b = 2*z - 3
                assert b > z and next_odd(b) == z
                if b % 5 == 0:
                    second = 2*b - 3
                    assert second > b and next_odd(second) == b
                    b = second
                a = next(((z << h) - 3) // 5 for h in range(3, 11)
                         if (z << h) % 5 == 3 and (z << h) % 25 != 3)
                assert z < a and 5*a < 1024*z and next_odd(a) == z
                assert b < 4*z and gcd(10, a*b) == 1
                children.update((a, b))
            assert len(children) == 2*len(level) and visited.isdisjoint(children)
            visited.update(children)
            level = children


def check_decimal_examples():
    for n, steps, root in ((6000001, 90, 1), (2000001, 76, 3),
                           (1000001, 66, 5), (27000001, 58, 61),
                           (18000001, 78, 125)):
        assert n % 10**6 == 1
        for _ in range(steps):
            assert n != root
            n = step(n)
        assert n == root


if __name__ == "__main__":
    check_joint_residues()
    check_residue_orbits()
    check_binary_replay()
    check_tree()
    check_decimal_examples()
    print("Verified joint residues, modular orbits, binary replay, inverse trees and decimal witnesses.")
