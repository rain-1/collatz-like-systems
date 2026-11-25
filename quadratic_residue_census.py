"""Exact one-step Legendre-symbol census and forward-closure certificate search.

Run with --json PATH to export matrices, accepted label sets, seeds escaping
into those sets, and all cycles of the descending split family. Matrix rows
and columns are ordered -1, 0, +1. Counts are per complete input period.
"""

import argparse
import json
from functools import partial
from itertools import combinations
from math import isqrt
from pathlib import Path

from verify_binary_invariant import orbit_step
from verify_three_cycle_basins import step as split_step


LABELS = (-1, 0, 1)


def odd_affine(n, a, d):
    return a * n + d if n % 2 else n // 2


def characters(p):
    values = [-1] * p
    values[0] = 0
    for n in range(1, p):
        values[n * n % p] = 1
    return values


def census(step, p, period, chi):
    matrix = [[0] * 3 for _ in LABELS]
    first = {}
    for n in range(1, period + 1):
        source = chi[n % p]
        target = chi[step(n) % p]
        matrix[source + 1][target + 1] += 1
        first.setdefault((source, target), n)
    certificates = []
    for size in (1, 2):
        for accepted in combinations(LABELS, size):
            if any(i in accepted and j not in accepted for i, j in first):
                continue
            seeds = [n for (i, j), n in first.items() if i not in accepted and j in accepted]
            certificates.append(dict(accepted=accepted, entering_seed=min(seeds, default=None)))
    return dict(prime=p, input_period=period, matrix=matrix,
                character_conserved=all(i == j for i, j in first), certificates=certificates)


def split_cycles(p, chi):
    """Every odd orbit descends into [1,p]; its intervening even terms are <=4p there."""
    basin = {}
    cycles = []
    for start in range(1, p + 1, 2):
        path = {}
        n = start
        while n not in basin and n not in path:
            if not 1 <= n <= 4 * p:
                raise ArithmeticError(f"Bound failed at p={p}, n={n}")
            path[n] = len(path)
            n = split_step(n, p)
        if n in basin:
            root = basin[n]
        else:
            loop = list(path)[path[n]:]
            root = min(loop)
            cycles.append(dict(minimum=root, period=len(loop),
                               characters=sorted({chi[k % p] for k in loop})))
        basin.update(dict.fromkeys(path, root))
    return sorted(cycles, key=lambda item: item["minimum"])


def split_cosets(p):
    """Label each orbit of multiplication by 2 and 3 by its least residue."""
    labels = {0: 0}
    for root in range(1, p):
        if root in labels:
            continue
        labels[root] = root
        stack = [root]
        while stack:
            r = stack.pop()
            for s in (2 * r % p, 3 * r % p):
                if s not in labels:
                    labels[s] = root
                    stack.append(s)
    return labels


def orbit_sample(step, seed, limit):
    seen = {}
    n = seed
    while len(seen) < limit and n not in seen:
        seen[n] = len(seen)
        n = step(n)
    return list(seen), seen.get(n)


def run(limit, sample_limit):
    rows = {}
    for p in range(3, limit + 1, 2):
        if any(p % i == 0 for i in range(3, isqrt(p) + 1, 2)):
            continue
        chi = characters(p)
        systems = [
            ("1932 permutation", orbit_step, 3),
            ("3n+1", partial(odd_affine, a=3, d=1), 2),
            ("3n-1", partial(odd_affine, a=3, d=-1), 2),
            ("5n+1", partial(odd_affine, a=5, d=1), 2),
            ("3n+p", partial(odd_affine, a=3, d=p), 2),
            ("5n+p", partial(odd_affine, a=5, d=p), 2),
        ]
        if p % 4 == 1:
            systems.append(("split p", partial(split_step, d=p), 4))
        for name, step, branch_modulus in systems:
            row = census(step, p, branch_modulus * p, chi)
            seed = 8 if name == "1932 permutation" else 27
            trace, repeat = orbit_sample(step, seed, sample_limit)
            counts = [0, 0, 0]
            for n in trace:
                counts[chi[n % p] + 1] += 1
            row["sample"] = dict(seed=seed, distinct_terms=len(trace),
                                 next_repeats_index=repeat, character_counts=counts)
            if name == "split p":
                row["cycles"] = split_cycles(p, chi)
                cosets = split_cosets(p)
                for cycle in row["cycles"]:
                    cycle["coset"] = cosets[cycle["minimum"] % p]
                row["coset_count"] = len(set(cosets.values()))
            rows.setdefault(name, []).append(row)
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-prime", type=int, default=997)
    parser.add_argument("--orbit-terms", type=int, default=1000,
                        help="sample up to this many distinct terms per orbit")
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    if args.max_prime < 3 or args.orbit_terms < 1:
        parser.error("need --max-prime >= 3 and --orbit-terms >= 1")
    rows = run(args.max_prime, args.orbit_terms)
    print("system             primes   conserved   closed set   entering seed")
    for name, group in rows.items():
        conserved = sum(r["character_conserved"] for r in group)
        closed = sum(bool(r["certificates"]) for r in group)
        entered = sum(any(c["entering_seed"] is not None for c in r["certificates"]) for r in group)
        print(f"{name:18} {len(group):6} {conserved:11} {closed:12} {entered:15}")
    split = [r for r in rows.get("split p", []) if r["character_conserved"]]
    print("Split primes where the character determines the eventual cycle:",
          [r["prime"] for r in split if len(r["cycles"]) == 3])
    print("Conserved split primes with additional cycles:",
          [(r["prime"], len(r["cycles"])) for r in split if len(r["cycles"]) > 3])
    full = [r for r in rows.get("split p", []) if r["coset_count"] == len(r["cycles"])]
    print("Split systems with complete fixed-modulus basin certificates:", len(full))
    if args.json:
        args.json.write_text(json.dumps(dict(labels=LABELS, max_prime=args.max_prime,
                                             orbit_terms=args.orbit_terms, systems=rows),
                                        indent=2) + "\n")


if __name__ == "__main__":
    main()
