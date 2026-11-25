"""Checks for the note output/pdf/binary_certificates_5np.pdf.

Map: T(n) = n/2 for even n, 5n+p for odd n, with p >= 1 coprime to 10.
The note proves that a binary finite automaton can certify nonreturn of a
seed coprime to 5 only when the orbit is eventually periodic. This script
tests the exact identities used there on finite ranges, then runs the 155
census cases (seed 27) much further than the census did.

Run: python3 verify_5np_binary_certificates.py [--odd-steps 100000]
"""
import argparse
import json
from fractions import Fraction


def T(n, p):
    return n // 2 if n % 2 == 0 else 5 * n + p


def check_mass_recursion(p, kmax=14):
    """a_k = 2 * density{n : T^k(n) odd} satisfies the renewal recursion and
    equals 2/3 + (1/3)(-1/2)^k."""
    a = [Fraction(1)]
    for k in range(1, kmax + 1):
        a.append(Fraction(1, 2 ** k)
                 + sum(Fraction(1, 2 ** j) * a[k - 1 - j] for j in range(1, k)))
    for k in range(kmax + 1):
        assert a[k] == Fraction(2, 3) + Fraction(1, 3) * Fraction(-1, 2) ** k
        assert a[k] >= Fraction(1, 2)
        # parity of T^k(n) depends only on n mod 2^(k+1)
        mod = 2 ** (k + 1)
        odd = 0
        for n in range(mod, 2 * mod):
            m = n
            for _ in range(k):
                m = T(m, p)
            odd += m % 2
            m2 = n + 7 * mod
            for _ in range(k):
                m2 = T(m2, p)
            assert m2 % 2 == m % 2
        assert 2 * Fraction(odd, mod) == a[k], (p, k)


def backward_chain(p, J, B):
    """For a unit class B mod 5^J (J >= 1) build J-1 backward odd steps
    through units. Returns (steps, E, slope5, const) with
    m = 5 * 2^E * q + const  and  T^steps(m) = 5^J q + B  for all q >= 0."""
    assert J >= 1 and B % 5 != 0
    # track m = c5 * q + c0 with c5 = 5^(J-i) * 2^E
    five, E, c0, steps = J, 0, B, 0
    for _ in range(J - 1):
        j = 1
        while True:
            num = 2 ** j * c0 - p
            if num > 0 and num % 5 == 0 and (five - 1 == 0 or (num // 5) % 5 != 0):
                break
            j += 1
        c0 = num // 5
        five -= 1
        E += j
        steps += j + 1
        assert c0 % 2 == 1 and c0 % 5 != 0
    return steps, E, c0


def check_backward_chains(p, Jmax=5):
    worst = 0
    for J in range(1, Jmax + 1):
        for B in range(5 ** J):
            if B % 5 == 0:
                continue
            steps, E, c0 = backward_chain(p, J, B)
            assert 0 < c0 < 5 * 2 ** E or J == 1
            worst = max(worst, E)
            for q in (0, 1, 2, 3, 4, 9, 23):
                m = 5 * 2 ** E * q + c0
                n = m
                for _ in range(steps):
                    assert n % 5 != 0  # the invariance relation is used on units only
                    n = T(n, p)
                assert n == 5 ** J * q + B
    return worst


def long_run(p, seed, odd_steps):
    """Follow odd terms only. Return (returned, cycled, bits, low_bits)."""
    n = seed
    low = None
    small_seen = {}
    for i in range(1, odd_steps + 1):
        n = 5 * n + p
        n >>= (n & -n).bit_length() - 1
        if n == seed:
            return True, True, n.bit_length(), None, i
        if n.bit_length() <= 64:
            if n in small_seen:
                return False, True, n.bit_length(), None, i
            small_seen[n] = i
        if i > odd_steps // 2:
            b = n.bit_length()
            low = b if low is None else min(low, b)
    return False, False, n.bit_length(), low, odd_steps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--odd-steps", type=int, default=100000)
    ap.add_argument("--census", default="output/certificate_search.json")
    args = ap.parse_args()

    for p in (1, 3, 7, 11, 13, 97, 997):
        check_mass_recursion(p, kmax=11)
        worst = check_backward_chains(p, Jmax=4)
        print(f"p={p}: mass recursion ok, backward chains ok (largest E {worst})")

    cases = json.load(open(args.census))["cases"]
    todo = [(c["p"], c["seed"]) for c in cases
            if c["system"] == "5n+p" and c["orbit"].get("stop")
            and not c["periodic_separator_exists"]]
    print(f"{len(todo)} unresolved census cases, {args.odd_steps} odd steps each")
    open_count, min_low = 0, None
    for p, seed in todo:
        returned, cycled, bits, low, i = long_run(p, seed, args.odd_steps)
        if cycled:
            print(f"  p={p}: {'RETURNS to seed' if returned else 'enters a cycle'}"
                  f" at odd step {i}")
        else:
            open_count += 1
            min_low = low if min_low is None else min(min_low, low)
    print(f"still unresolved: {open_count}; over those, every odd term in the "
          f"second half of the run has at least {min_low} bits")


if __name__ == "__main__":
    main()
