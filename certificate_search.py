"""Exhaust fixed-modulus graphs and small binary automata on the census systems."""

import argparse
from functools import partial
from itertools import product
import json
from math import isqrt
from pathlib import Path

from quadratic_residue_census import odd_affine, split_cosets
from verify_binary_invariant import orbit_step
from verify_three_cycle_basins import step as split_step


def systems(limit):
    # Each branch lists u,r,v,s for (u*q+r) -> (v*q+s), q >= 0.
    yield "1932", None, orbit_step, 3, [(3, 3, 2, 2), (3, 1, 4, 1), (3, 2, 4, 3)]
    primes = [p for p in range(3, limit + 1, 2)
              if all(p % d for d in range(3, isqrt(p) + 1, 2))]
    for name, a, offsets in (("3n+1", 3, [1]), ("3n-1", 3, [-1]), ("5n+1", 5, [1]),
                             ("3n+p", 3, primes), ("5n+p", 5, primes)):
        for d in offsets:
            yield name, d if name.endswith("p") else None, partial(odd_affine, a=a, d=d), 2, [
                (2, 2, 1, 1), (2, 1, 2 * a, a + d)]
    for p in primes:
        if p % 4 == 1:
            yield "split", p, partial(split_step, d=p), 4, [
                (2, 2, 1, 1), (4, 1, 12, 3 + p), (4, 3, 4, 3 + p)]


def components(graph):
    """Kosaraju components in topological order, with iterative DFS."""
    reverse = [[] for _ in graph]
    for r, row in enumerate(graph):
        for s in row:
            reverse[s].append(r)
    visited = set()
    order = []
    for start in range(len(graph)):
        if start in visited:
            continue
        stack = [(start, False)]
        while stack:
            r, finished = stack.pop()
            if finished:
                order.append(r)
            elif r not in visited:
                visited.add(r)
                stack.append((r, True))
                stack.extend((s, False) for s in graph[r] if s not in visited)
    labels = [-1] * len(graph)
    groups = []
    for r in reversed(order):
        if labels[r] >= 0:
            continue
        index = len(groups)
        group = []
        stack = [r]
        labels[r] = index
        while stack:
            v = stack.pop()
            group.append(v)
            for s in reverse[v]:
                if labels[s] < 0:
                    labels[s] = index
                    stack.append(s)
        groups.append(group)
    return labels, groups


def residue_graph(step, period, m):
    graph = [set() for _ in range(m)]
    for n in range(1, period * m + 1):
        graph[n % m].add(step(n) % m)
    return graph


def closed_from(graph, start):
    seen = {start}
    stack = [start]
    while stack:
        for s in graph[stack.pop()]:
            if s not in seen:
                seen.add(s)
                stack.append(s)
    return sorted(seen)


def modular_search(step, period, moduli, seed):
    proper, entering, separating = [], [], []
    witness = None
    for m in moduli:
        graph = residue_graph(step, period, m)
        labels, groups = components(graph)
        if len(groups) == 1:
            continue
        proper.append(m)
        if any(labels[r] != labels[s] for r, row in enumerate(graph) for s in row):
            entering.append(m)
        dest = step(seed) % m
        if labels[dest] != labels[seed % m]:
            separating.append(m)
            if witness is None:
                accepted = closed_from(graph, dest)
                lookup = set(accepted)
                assert seed % m not in lookup and all(graph[r] <= lookup for r in accepted)
                witness = dict(modulus=m, accepted=accepted)
    return dict(proper_moduli=proper, one_way_moduli=entering,
                seed_moduli=separating, seed_witness=witness)


def binary_languages(bound):
    """Minimal accessible machines, rooted after the mandatory leading 1."""
    for size in range(2, bound + 1):
        for flat in product(range(size), repeat=2 * size):
            seen = [0]
            for r in seen:
                for s in flat[2*r:2*r+2]:
                    if s not in seen:
                        seen.append(s)
            if seen != list(range(size)):
                continue
            rows = [flat[2*r:2*r+2] for r in range(size)]
            for mask in range(1, (1 << size) - 1):
                classes = [(mask >> r) & 1 for r in range(size)]
                while len(set(classes)) < size:
                    signatures = [(classes[r], classes[x], classes[y])
                                  for r, (x, y) in enumerate(rows)]
                    ids = {s: i for i, s in enumerate(dict.fromkeys(signatures))}
                    refined = [ids[s] for s in signatures]
                    if len(set(classes)) == len(ids):
                        break
                    classes = refined
                if len(set(classes)) == size:
                    yield rows, mask


class BinaryLanguage:
    def __init__(self, rows, mask, table_limit):
        self.rows = rows
        self.mask = mask
        # The extra state skips leading padding zeros and consumes the leading 1.
        self.transitions = rows + [(len(rows), 0)]
        self.states = [len(rows)]
        for n in range(1, table_limit + 1):
            self.states.append(self.transitions[self.states[n // 2]][n % 2])
        self.flags = bytearray((mask >> state) & 1 for state in self.states)
        self.preimage = [
            [sum(1 << i for i, row in enumerate(self.transitions) if m & (1 << row[b]))
             for m in range(1 << len(self.transitions))] for b in (0, 1)]

    def accepts(self, n):
        if n < len(self.flags):
            return bool(self.flags[n])
        state = 0
        for bit in format(n, "b")[1:]:
            state = self.rows[state][int(bit)]
        return bool(self.mask & (1 << state))

    def closed_on_branch(self, u, r, v, s):
        # Is there q >= 0 whose input is accepted and whose image is rejected?
        rejected = ((1 << len(self.transitions)) - 1) ^ self.mask
        initial = (r, s, self.mask, rejected)
        seen = {initial}
        stack = [initial]
        while stack:
            x, y, left, right = stack.pop()
            if left & (1 << self.states[x]) and right & (1 << self.states[y]):
                return False  # remaining quotient is zero
            for bit in (0, 1):
                a, b = x + bit*u, y + bit*v
                l = self.preimage[a % 2][left]
                h = self.preimage[b % 2][right]
                node = (a // 2, b // 2, l, h)
                if l and h and node not in seen:
                    seen.add(node)
                    stack.append(node)
        return True


def automaton_search(step, branches, machines, seed):
    # Finite examples only reject candidates. Every survivor receives a proof.
    sample = [(n, step(n)) for n in range(1, 257)]
    closed = []
    seed_ids = []
    for i, machine in enumerate(machines):
        f = machine.flags
        if any(f[n] and not f[y] for n, y in sample):
            continue
        if all(machine.closed_on_branch(*branch) for branch in branches):
            closed.append(i)
            if not machine.accepts(seed) and machine.accepts(step(seed)):
                seed_ids.append(i)
    return dict(closed_ids=closed, seed_ids=seed_ids)


def basin_certificate(p, seed):
    """A decreasing rank and cycle label for each odd state in the finite core."""
    roots = []
    distances = []
    odd_next = []
    for n in range(1, p + 1, 2):
        v = split_step(n, p)
        odd_next.append(v // (v & -v))
    memo = {}
    periods = {}
    seed_cycle = None
    for start in range(1, p + 1, 2):
        path = {}
        n = start
        while n not in memo and n not in path:
            path[n] = len(path)
            n = odd_next[n // 2]
        if n not in memo:
            cycle = list(path)[path[n]:]
            root = min(cycle)
            period = 0
            for k in cycle:
                image = split_step(k, p)
                period += (image & -image).bit_length()  # odd step plus all halvings
                if k == seed:
                    seed_cycle = root
                while image % 2 == 0:
                    if image == seed:
                        seed_cycle = root
                    image //= 2
            periods[root] = period
            memo.update({k: (root, 0) for k in cycle})
        for k in reversed(path):
            if k not in memo:
                root, dist = memo[odd_next[k // 2]]
                memo[k] = root, dist + 1
    for n in range(1, p + 1, 2):
        root, dist = memo[n]
        roots.append(root)
        distances.append(dist)
    labels = split_cosets(p)
    return dict(odd_core_roots=roots, odd_steps_to_cycle=distances, seed_cycle=seed_cycle,
                cycles=[dict(minimum=k, period=v, coset=labels[k % p])
                        for k, v in sorted(periods.items())])


def exact_trace(step, seed, term_limit, bit_limit):
    seen = {}
    n = seed
    while n not in seen and len(seen) < term_limit and n.bit_length() <= bit_limit:
        seen[n] = len(seen)
        n = step(n)
    if n in seen:
        return dict(terms=list(seen), repeat_index=seen[n])
    return dict(terms_checked=len(seen), stop="bit limit" if n.bit_length() > bit_limit
                else "term limit")


def periodic_separator(name, p, seed):
    """A witness at arbitrary modulus, or impossibility by the accompanying theorem."""
    if name in ("1932", "split"):
        return None
    a = int(name[0])
    scale = a if p == a and seed % a == 0 else 1
    x = seed // scale
    accept_multiples = p == a and scale == 1
    if (x % a == 0) == accept_multiples:
        return None
    power = x & -x
    return dict(modulus=scale*a*power, scale=scale, prime=a,
                accept_multiples=accept_multiples, binary_divisor=power)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-prime", type=int, default=997)
    parser.add_argument("--max-modulus", type=int, default=128)
    parser.add_argument("--dfa-states", type=int, choices=(1, 2, 3), default=3)
    parser.add_argument("--orbit-terms", type=int, default=10000)
    parser.add_argument("--orbit-bits", type=int, default=2048)
    parser.add_argument("--seed", type=int, help="override the designated seed for every map")
    parser.add_argument("--json", type=Path, required=True)
    args = parser.parse_args()
    if args.max_prime < 3 or args.max_modulus < 1:
        parser.error("limits require max-prime >= 3 and max-modulus >= 1")
    if min(args.orbit_bits, args.orbit_terms, args.seed or 1) <= 0 or args.seed == 0:
        parser.error("orbit limits and seeds must be positive")
    maps = list(systems(args.max_prime))
    machines = [BinaryLanguage(rows, mask, args.max_prime + 1400)
                for rows, mask in binary_languages(args.dfa_states)]
    cases = []
    for name, p, step, period, branches in maps:
        seed = args.seed or (8 if name == "1932" else 27)
        moduli = set(range(1, args.max_modulus + 1))
        if p is not None:
            moduli.update([p, 2*p, 4*p])
        witness = periodic_separator(name, p, seed)
        case = dict(system=name, p=p, seed=seed,
                    periodic_separator_exists=witness is not None, periodic_witness=witness,
                    modular=modular_search(step, period, sorted(moduli), seed),
                    binary=automaton_search(step, branches, machines, seed),
                    orbit=exact_trace(step, seed, args.orbit_terms, args.orbit_bits))
        if name == "split":
            case["basins"] = basin_certificate(p, seed)
        cases.append(case)
    result = dict(max_modulus=args.max_modulus, extra_parameter_moduli=["p", "2p", "4p"],
                  orbit_term_limit=args.orbit_terms, orbit_bit_limit=args.orbit_bits,
                  max_prime=args.max_prime, max_binary_states_after_leading_one=args.dfa_states,
                  machines=[dict(transitions=m.rows, accepting_mask=m.mask) for m in machines],
                  cases=cases)
    args.json.write_text(json.dumps(result, separators=(",", ":")) + "\n")
    print(f"{len(cases)} maps; {len(machines)} distinct nonconstant binary languages.")
    print("system       maps   modular hits   binary hits   nonreturn   return   unresolved")
    for name in dict.fromkeys(c["system"] for c in cases):
        group = [c for c in cases if c["system"] == name]
        returns = sum(c["orbit"].get("repeat_index") == 0
                      or c.get("basins", {}).get("seed_cycle") is not None for c in group)
        nonreturns = sum(bool(c["periodic_separator_exists"] or c["binary"]["seed_ids"]
                              or c["orbit"].get("repeat_index")
                              or ("basins" in c and c["basins"]["seed_cycle"] is None))
                         for c in group)
        print(f"{name:10} {len(group):6} {sum(bool(c['modular']['seed_moduli']) for c in group):14}"
              f" {sum(bool(c['binary']['seed_ids']) for c in group):13} {nonreturns:11}"
              f" {returns:8} {len(group)-nonreturns-returns:12}")


if __name__ == "__main__":
    main()
