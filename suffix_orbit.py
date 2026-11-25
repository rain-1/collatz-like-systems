"""Compute a finite cycle or the exact positive-time orbit of a binary suffix permutation.

Pass --rules a JSON file containing pairs of suffix strings, e.g.
[["0","00"],["01","10"],["11","1"]]. Each side must partition the
nonnegative integers and the rule for zero must fix zero.
"""

import argparse
from collections import defaultdict
import json
from pathlib import Path

from verify_binary_invariant import binary_state
from verify_more_certificates import SUFFIXES
from verify_suffix_permutation import append_state


def validate(rules):
    if not rules or any(not isinstance(pair, (list, tuple)) or len(pair) != 2
                        for pair in rules):
        raise ValueError("Expected nonempty pairs of suffix strings")
    for codes in zip(*rules):
        if any(not isinstance(s, str) or not s or set(s) - {"0", "1"} for s in codes):
            raise ValueError("Suffixes must be nonempty binary strings")
        ordered = sorted(s[::-1] for s in codes)
        if any(b.startswith(a) for a, b in zip(ordered, ordered[1:])):
            raise ValueError("Overlapping suffixes")
        width = max(map(len, codes))
        if sum(1 << (width - len(s)) for s in codes) != 1 << width:
            raise ValueError("Suffixes do not cover all inputs")
    if any(int(a, 2) == 0 and int(b, 2) != 0 for a, b in rules):
        raise ValueError("The permutation must fix zero")


def step(rules, n):
    for a, b in rules:
        q, r = divmod(n, 1 << len(a))
        if r == int(a, 2):
            return (q << len(b)) + int(b, 2)
    raise AssertionError("Missing rule")


def decompose(rules, first):
    """Visit until a repeat or a repeatable insertion is witnessed."""
    width = max(len(a) for a, _ in rules)
    mask = (1 << width) - 1
    trace = []
    seen = {}
    # Surviving indices have had no smaller bit length since their visit.
    minima = []
    by_suffix = defaultdict(list)
    n = first
    while n not in seen:
        height = n.bit_length()
        while minima and trace[minima[-1]].bit_length() > height:
            old = minima.pop()
            by_suffix[trace[old] & mask].pop()
        if height > width:
            candidates = by_suffix[n & mask]
            if candidates:
                i = candidates[0]
                base_height = trace[i].bit_length()
                if base_height < height:
                    prefix_length = base_height - width
                    current = format(n, "b")
                    prefix = current[:prefix_length]
                    insert = current[prefix_length:-width]
                    phases = [format(x, "b")[prefix_length:] for x in trace[i:]]
                    return trace[:i], (prefix, insert, phases)
            candidates.append(len(trace))
            minima.append(len(trace))
        seen[n] = len(trace)
        trace.append(n)
        n = step(rules, n)
    if seen[n] != 0:
        raise AssertionError("A permutation cannot have a transient before a cycle")
    return trace, None


def exact_dfa(stem, pump):
    """Determinize the union of the stem and the languages P V* U."""
    edges = [{}]
    accepting = set()

    def path(start, word, end=None):
        state = start
        for i, bit in enumerate(word):
            target = end if i + 1 == len(word) else None
            if target is None:
                target = len(edges)
                edges.append({})
            edges[state].setdefault(bit, set()).add(target)
            state = target
        return state

    for n in stem:
        accepting.add(path(0, format(n, "b")))
    prefix, insert, phases = pump
    hub = path(0, prefix)
    path(hub, insert, hub)
    for phase in phases:
        accepting.add(path(hub, phase))

    subsets = [frozenset({0})]
    indices = {subsets[0]: 0}
    transitions = []
    finals = []
    for index, states in enumerate(subsets):
        if states & accepting:
            finals.append(index)
        row = []
        for bit in "01":
            dest = frozenset(q for s in states for q in edges[s].get(bit, ()))
            if dest not in indices:
                indices[dest] = len(subsets)
                subsets.append(dest)
            row.append(indices[dest])
        transitions.append(row)
    return {"transitions": transitions, "accepting": finals}


def verify_certificate(rules, seed, dfa):
    transitions = dfa["transitions"]
    final = set(dfa["accepting"])
    if binary_state(transitions, seed) in final or binary_state(
            transitions, step(rules, seed)) not in final:
        raise ValueError("Seed separation failed")
    first = binary_state(transitions, 1)
    reachable = {first}
    todo = [first]
    while todo:
        for q in transitions[todo.pop()]:
            if q not in reachable:
                reachable.add(q)
                todo.append(q)
    for a, b in rules:
        x, y = int(a, 2), int(b, 2)
        if x and binary_state(transitions, x) in final and binary_state(transitions, y) not in final:
            raise ValueError("Closure failed at quotient zero")
        for q in reachable:
            if append_state(transitions, q, a) in final and append_state(transitions, q, b) not in final:
                raise ValueError("Closure failed at a positive quotient")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rules", type=Path, help="JSON suffix table (default: the five-rule example)")
    parser.add_argument("--seed", type=int, default=8)
    parser.add_argument("--output", type=Path, help="write the verified DFA for an infinite orbit")
    args = parser.parse_args()
    try:
        rules = json.loads(args.rules.read_text()) if args.rules else SUFFIXES
        validate(rules)
        if args.seed < 1:
            raise ValueError("The seed must be positive")
    except (ValueError, OSError, TypeError) as error:
        parser.error(str(error))

    stem, pump = decompose(rules, step(rules, args.seed))
    if pump is None:
        print(f"Finite cycle of exact period {len(stem)} through {args.seed}.")
        return
    prefix, insert, phases = pump
    print(f"Infinite orbit. First {len(stem)} positive-time iterates: {stem}")
    print(f"Then, for k = 0, 1, ... concatenate {prefix} + ({insert})^k + u")
    print(f"using these binary suffixes u in order: {', '.join(phases)}")
    dfa = exact_dfa(stem, pump)
    verify_certificate(rules, args.seed, dfa)
    print(f"Verified closure and seed separation for the {len(dfa['transitions'])}-state exact-orbit DFA.")
    if args.output:
        args.output.write_text(json.dumps(dfa, indent=2) + "\n")


if __name__ == "__main__":
    main()
