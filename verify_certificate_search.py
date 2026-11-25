"""Independently replay the graph, language, orbit and basin checks in a search file."""

from argparse import ArgumentParser
from collections import defaultdict, deque
from functools import lru_cache
import json
from pathlib import Path
import sys

from certificate_search import systems


def tarjan(graph):
    times = {}
    pending = []
    active = set()
    component = {}

    def visit(n):
        low = times[n] = len(times)
        active.add(n)
        pending.append(n)
        for v in graph[n]:
            if v not in times:
                low = min(low, visit(v))
            elif v in active:
                low = min(low, times[v])
        if low == times[n]:
            while True:
                v = pending.pop()
                active.remove(v)
                component[v] = n
                if v == n:
                    break
        return low

    for n in range(len(graph)):
        if n not in times:
            visit(n)
    return component


def verify_graphs(case, step, branches, bound):
    result = case["modular"]
    seed = case["seed"]
    moduli = set(range(1, bound + 1))
    if case["p"]:
        moduli.update(case["p"] * i for i in (1, 2, 4))
    proper, crossing, separated = [], [], []
    for m in sorted(moduli):
        graph = [set() for _ in range(m)]
        for u, r, v, s in branches:
            for q in range(m):
                graph[(u*q+r) % m].add((v*q+s) % m)
        ids = tarjan(graph)
        if len(set(ids.values())) > 1:
            proper.append(m)
        if any(ids[n] != ids[y] for n, row in enumerate(graph) for y in row):
            crossing.append(m)
        if ids[seed % m] != ids[step(seed) % m]:
            separated.append(m)
        w = result["seed_witness"]
        if w and w["modulus"] == m:
            accepted = set(w["accepted"])
            assert seed % m not in accepted and step(seed) % m in accepted
            assert all(graph[r] <= accepted for r in accepted)
    assert (proper, crossing, separated) == (
        result["proper_moduli"], result["one_way_moduli"], result["seed_moduli"])
    assert (result["seed_witness"]["modulus"] if separated else None) == next(iter(separated), None)
    if not separated:
        assert result["seed_witness"] is None
    assert not separated or case["periodic_separator_exists"]
    return len(moduli)


def read_state(rows, n):
    if n == 0:
        return len(rows)
    state = 0
    for digit in bin(n)[3:]:
        state = rows[state][int(digit)]
    return state


@lru_cache(maxsize=8192)
def branch_pairs(rows, branch):
    """All realizable pairs of endpoint states, independent of accepting masks."""
    u, r, v, s = branch
    trans = rows + ((len(rows), 0),)
    parents = defaultdict(list)
    offsets = {(r, s)}
    stack = [(r, s)]
    while stack:
        x, y = stack.pop()
        for b in (0, 1):
            left, right = x + u*b, y + v*b
            child = (left // 2, right // 2)
            parents[child].append(((x, y), left % 2, right % 2))
            if child not in offsets:
                offsets.add(child)
                stack.append(child)
    reached = {key: {(read_state(rows, key[0]), read_state(rows, key[1]))} for key in offsets}
    queue = deque((key, next(iter(pairs))) for key, pairs in reached.items())
    while queue:
        child, (i, j) = queue.popleft()
        for parent, b, c in parents[child]:
            pair = trans[i][b], trans[j][c]
            if pair not in reached[parent]:
                reached[parent].add(pair)
                queue.append((parent, pair))
    return reached[r, s]


def verify_languages(case, step, branches, machines, flags):
    sample = [(n, step(n)) for n in range(1, 257)]
    closed, separated = [], []
    for i, ((rows, mask), f) in enumerate(zip(machines, flags)):
        if any(f[n] and not f[y] for n, y in sample):
            continue
        if any(mask & (1 << x) and not mask & (1 << y)
               for b in branches for x, y in branch_pairs(rows, b)):
            continue
        closed.append(i)
        seed = case["seed"]
        if not mask & (1 << read_state(rows, seed)) and mask & (1 << read_state(rows, step(seed))):
            separated.append(i)
    assert case["binary"] == dict(closed_ids=closed, seed_ids=separated)


def verify_orbit(case, step, term_limit, bit_limit):
    orbit = case["orbit"]
    n = case["seed"]
    seen = set()
    for _ in range(orbit.get("terms_checked", len(orbit.get("terms", [])))):
        assert n not in seen and n.bit_length() <= bit_limit and len(seen) < term_limit
        if "terms" in orbit:
            assert orbit["terms"][len(seen)] == n
        seen.add(n)
        n = step(n)
    if "terms" in orbit:
        j = orbit["repeat_index"]
        assert 0 <= j < len(seen) and orbit["terms"][j] == n
        assert j or not (case["periodic_separator_exists"] or case["binary"]["seed_ids"])
    else:
        assert n not in seen and (len(seen) == term_limit or n.bit_length() > bit_limit)
        assert orbit["stop"] == ("bit limit" if n.bit_length() > bit_limit else "term limit")


def verify_periodic_witness(case, step, period):
    name, p, seed = case["system"], case["p"], case["seed"]
    expected = False
    if name not in ("1932", "split"):
        a = int(name[0])
        expected = seed % a == 0
        if p == a:
            expected = seed % a != 0 or seed % (a*a) == 0
    w = case["periodic_witness"]
    assert case["periodic_separator_exists"] == expected == (w is not None)
    if w is None:
        return

    def accepts(n):
        x, rem = divmod(n, w["scale"])
        return rem == 0 and ((x % w["prime"] == 0) == w["accept_multiples"]
                             or x % w["binary_divisor"] != 0)

    scale = a if p == a and seed % a == 0 else 1
    x = seed // scale
    assert (w["scale"], w["prime"], w["binary_divisor"], w["accept_multiples"]) == (
        scale, a, x & -x, p == a and scale == 1)
    assert w["modulus"] == w["scale"] * w["prime"] * w["binary_divisor"]
    assert not accepts(seed) and accepts(step(seed))
    if w["modulus"] <= 100000:
        assert all(not accepts(n) or accepts(step(n)) for n in range(1, period*w["modulus"]+1))


def verify_basins(case, step):
    p = case["p"]
    data = case["basins"]
    roots, ranks = data["odd_core_roots"], data["odd_steps_to_cycle"]
    assert len(roots) == len(ranks) == (p+1)//2
    claimed = {c["minimum"]: c for c in data["cycles"]}
    subgroup = {1}
    for a in (2, 3):
        previous = tuple(subgroup)
        power = a % p
        while power != 1:
            subgroup.update(k * power % p for k in previous)
            power = power * a % p
    on_cycle = set()
    seed_cycle = None
    for root, c in claimed.items():
        assert c["coset"] == min(root * h % p for h in subgroup)
        n = root
        for j in range(c["period"]):
            assert n >= root and (j == 0 or n != root)
            if n == case["seed"]:
                seed_cycle = root
            if n % 2:
                assert n not in on_cycle and n <= p and roots[n//2] == root
                on_cycle.add(n)
            n = step(n)
        assert n == root
    assert seed_cycle == data["seed_cycle"]
    for n in range(1, p+1, 2):
        y = step(n)
        while y % 2 == 0:
            y //= 2
        assert y <= p and roots[n//2] in claimed and roots[y//2] == roots[n//2]
        assert ranks[n//2] == (0 if n in on_cycle else 1+ranks[y//2])


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    d = json.loads(args.file.read_text())
    limit = d["max_prime"]
    sys.setrecursionlimit(max(2000, 2*max(4*limit, d["max_modulus"])))
    machines = [(tuple(map(tuple, m["transitions"])), m["accepting_mask"]) for m in d["machines"]]
    # Counts of nonconstant minimal languages with 1, 2 or 3 states, inclusive.
    assert len(machines) == len(set(machines)) == (0, 24, 1052)[d["max_binary_states_after_leading_one"]-1]
    states = {}
    flags = []
    for rows, mask in machines:
        if rows not in states:
            states[rows] = [read_state(rows, n) for n in range(limit+1401)]
        flags.append(bytearray((mask >> q) & 1 for q in states[rows]))
    total = 0
    for case, (name, p, step, period, branches) in zip(d["cases"], systems(limit), strict=True):
        assert (case["system"], case["p"]) == (name, p)
        total += verify_graphs(case, step, branches, d["max_modulus"])
        verify_languages(case, step, branches, machines, flags)
        verify_orbit(case, step, d["orbit_term_limit"], d["orbit_bit_limit"])
        verify_periodic_witness(case, step, period)
        if name == "split":
            verify_basins(case, step)
    print(f"Verified {total} graphs, {len(machines)} binary languages on each of "
          f"{len(d['cases'])} maps, all designated traces, and all split basin ranks.")


if __name__ == "__main__":
    main()
