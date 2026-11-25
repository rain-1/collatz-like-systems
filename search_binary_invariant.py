"""Synthesize a binary DFA certificate for the original Collatz orbit of 8.

Run: python3 search_binary_invariant.py --seconds 30
Requires the Z3 shared library. Each size has its own time budget (0 = unlimited).
Only a globally verified certificate is written to stdout or --output. Progress
goes to stderr. Exit 0 means verified, 1 means the requested range was excluded,
and 2 means at least one size was unresolved or an error occurred.
"""

import argparse
from contextlib import contextmanager
import ctypes
from ctypes.util import find_library
import json
import os
from pathlib import Path
import re
import sys
from tempfile import NamedTemporaryFile
from time import monotonic

from binary_prefix_bound import (
    DISTINCT_PREFIXES, EXTRA_MATCHES, MIN_STATES, extra_state_assignments, verify_state_bound,
)
from verify_binary_invariant import binary_state, closure_violation, orbit_labels, orbit_step


@contextmanager
def z3_session():
    """Keep declarations and assertions across SMT-LIB queries in libz3."""
    name = find_library("z3")
    if not name:
        raise RuntimeError("The Z3 shared library (libz3) is required.")
    lib = ctypes.CDLL(name)
    ptr, string = ctypes.c_void_p, ctypes.c_char_p
    for symbol, result, args in (
        ("Z3_mk_config", ptr, []), ("Z3_del_config", None, [ptr]),
        ("Z3_mk_context_rc", ptr, [ptr]), ("Z3_del_context", None, [ptr]),
        ("Z3_set_error_handler", None, [ptr, ptr]),
        ("Z3_eval_smtlib2_string", string, [ptr, string]),
    ):
        fn = getattr(lib, symbol)
        fn.argtypes, fn.restype = args, result
    config = lib.Z3_mk_config()
    context = lib.Z3_mk_context_rc(config)
    lib.Z3_del_config(config)
    lib.Z3_set_error_handler(context, None)

    def query(command):
        response = lib.Z3_eval_smtlib2_string(context, command.encode())
        if response is None:
            raise RuntimeError("Z3 returned no response.")
        text = response.decode().strip()
        if "(error " in text:
            raise RuntimeError(text)
        return text

    try:
        yield query
    finally:
        lib.Z3_del_context(context)


class DfaConstraints:
    """One finite Z3 datatype for states, with ground terms for visited prefixes."""

    def __init__(self, size, anchors):
        self.size = size
        self.anchors = anchors
        self.nodes = set()

    def machine(self):
        states = ' '.join(f"s{i}" for i in range(self.size))
        yield f"(declare-datatypes () ((State {states})))"
        yield "(declare-fun d0 (State) State)"
        yield "(declare-fun d1 (State) State)"
        yield "(declare-fun accept (State) Bool)"
        yield "(declare-const start State)"
        yield from self.words(self.anchors)
        for i, n in enumerate(self.anchors):
            yield f"(assert (= node_{n:x} s{i}))"
        if self.anchors == DISTINCT_PREFIXES:
            yield from self.words(EXTRA_MATCHES)
            cases = []
            for row in extra_state_assignments(self.size):
                equalities = (f"(= node_{p:x} s{i})" for p, i in zip(EXTRA_MATCHES, row))
                cases.append(f"(and {' '.join(equalities)})")
            yield f"(assert (or {' '.join(cases)}))" if cases else "(assert false)"
        for i in range(self.size):
            yield f"(define-fun accept_{i} () Bool (accept s{i}))"
            for bit in (0, 1):
                yield f"(define-fun edge_{i}_{bit} () State (d{bit} s{i}))"

    def words(self, numbers):
        fresh = set()
        for n in numbers:
            while n and n not in self.nodes and n not in fresh:
                fresh.add(n)
                n >>= 1
        for n in sorted(fresh):
            parent = "start" if n == 1 else f"node_{n//2:x}"
            yield f"(declare-const node_{n:x} State)"
            yield f"(assert (= node_{n:x} (d{n%2} {parent})))"
        self.nodes.update(fresh)

    def labels(self, samples):
        yield from self.words(samples)
        for n, accepted in samples.items():
            value = 'true' if accepted else 'false'
            yield f"(assert (= (accept node_{n:x}) {value}))"

    def implication(self, source, target):
        yield from self.words((source, target))
        yield f"(assert (=> (accept node_{source:x}) (accept node_{target:x})))"


def decode_machine(query, size):
    names = ["start"] + [f"accept_{i}" for i in range(size)]
    names += [f"edge_{i}_{bit}" for i in range(size) for bit in (0, 1)]
    response = query(f"(get-value ({' '.join(names)}))")
    values = dict(re.findall(r"\((\w+)\s+(true|false|s[0-9]+)\)", response))
    if set(values) != set(names):
        raise RuntimeError("Incomplete transition table in the solver response.")
    rows = [[int(values[f"edge_{i}_{bit}"][1:]) for bit in (0, 1)] for i in range(size)]
    # Solver state 0 is reached AFTER the leading 1. The file format instead
    # designates state 0 BEFORE that digit. Renumber without adding a state.
    start = int(values["start"][1:])
    order = [start] + [i for i in range(size) if i != start]
    new_index = {old: new for new, old in enumerate(order)}
    return {
        "transitions": [[new_index[j] for j in rows[i]] for i in order],
        "accepting": [new_index[i] for i in order if values[f"accept_{i}"] == "true"],
    }


def search_size(size, samples, labels, edges, seconds, anchors=DISTINCT_PREFIXES):
    """Refine labels and edges in place. Both are necessary at every state size."""
    start = monotonic()
    encoding = DfaConstraints(size, anchors)
    rounds = 0
    with z3_session() as query:
        query('\n'.join(encoding.machine()))
        query('\n'.join(encoding.labels(labels)))
        query('\n'.join(command for x, y in sorted(edges) for command in encoding.implication(x, y)))
        while True:
            if seconds:
                remaining = seconds - (monotonic() - start)
                if remaining <= 0:
                    return "timeout", rounds, None
                milliseconds = min(0xffffffff, max(1, int(remaining * 1000)))
                query(f"(set-option :timeout {milliseconds})")
            status = query("(check-sat)")
            if status == "unsat":
                return "excluded", rounds, None
            if status == "unknown":
                info = query("(get-info :reason-unknown)")
                reason = re.fullmatch(r'\(:reason-unknown\s+"([^"]*)"\)', info)
                return f"Z3: {reason[1] if reason else info}", rounds, None
            if status != "sat":
                raise RuntimeError(f"Unexpected solver response: {status}")
            rounds += 1
            candidate = decode_machine(query, size)
            transitions = candidate["transitions"]
            accepting = set(candidate["accepting"])

            def accepts(n):
                return binary_state(transitions, n) in accepting

            if any(accepts(n) != value for n, value in labels.items()):
                raise RuntimeError("Decoded model violates an asserted orbit label.")
            if any(accepts(x) and not accepts(y) for x, y in edges):
                raise RuntimeError("Decoded model violates a previous refinement.")
            try:
                failure = closure_violation(transitions, accepting, start + seconds if seconds else None)
            except TimeoutError:
                return "timeout in global checker", rounds, None
            if failure is None:
                if any(accepts(n) != value for n, value in samples.items()):
                    raise RuntimeError("Closure check disagrees with known orbit labels.")
                return "verified", rounds, candidate

            x, y = failure
            if y != orbit_step(x) or not accepts(x) or accepts(y):
                raise RuntimeError("Invalid closure counterexample.")
            edges.add(failure)
            # The implication is necessary even when neither endpoint has a
            # known label. Also supply a few forced orbit labels the model missed.
            missed = [n for n in sorted(samples) if accepts(n) != samples[n]][:6]
            new_labels = {n: samples[n] for n in missed}
            labels.update(new_labels)
            query('\n'.join(encoding.implication(x, y)))
            query('\n'.join(encoding.labels(new_labels)))
            if rounds <= 3 or rounds % 10 == 0:
                print(f"{size} states, candidate {rounds}: rejected edge {x} -> {y}",
                      file=sys.stderr, flush=True)


def save_certificate(path, candidate):
    content = json.dumps(candidate, indent=2) + "\n"
    if path is None:
        sys.stdout.write(content)
        return
    f = NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8")
    temp = Path(f.name)
    try:
        with f:
            f.write(content)
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--min-states", type=int, default=MIN_STATES)
    parser.add_argument("--max-states", type=int, help="default: same as --min-states")
    parser.add_argument("--seconds", type=int, default=30, help="per-size budget (0 = unlimited)")
    parser.add_argument("--seed-limit", type=int, default=96,
                        help="seed closure edges and known orbit labels through this integer")
    parser.add_argument("--output", type=Path, help="write verified JSON here instead of stdout")
    args = parser.parse_args()
    last = args.min_states if args.max_states is None else args.max_states
    if not 1 <= args.min_states <= last or args.seconds < 0 or args.seed_limit < 0:
        parser.error("invalid size range, time budget, or seed limit")
    samples = orbit_labels()
    labels = {n: expected for n, expected in samples.items()
              if n <= args.seed_limit or n in (8, 11)}
    edges = {(x, orbit_step(x)) for x in range(1, args.seed_limit + 1)}
    lower_bound = verify_state_bound()
    print(f"Prefix certificates: at least {lower_bound} states required.", file=sys.stderr, flush=True)
    unresolved = set()
    for size in range(args.min_states, last + 1):
        start = monotonic()
        if size < lower_bound:
            status, iterations, candidate = "excluded", 0, None
        else:
            status, iterations, candidate = search_size(size, samples, labels, edges, args.seconds)
        outcome = status if status in ("excluded", "verified") else f"unresolved ({status})"
        print(f"{size} states: {outcome}; {iterations} candidates, {monotonic()-start:.2f}s",
              file=sys.stderr, flush=True)
        if candidate is not None:
            save_certificate(args.output, candidate)
            return 0
        if status == "excluded":
            # Unreachable states can pad a smaller solution to this size.
            unresolved.clear()
        else:
            unresolved.add(size)
    if unresolved:
        sizes = ", ".join(str(n) for n in sorted(unresolved))
        print(f"No certificate found. Unresolved sizes: {sizes}.", file=sys.stderr)
        return 2
    print("All requested sizes excluded.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError, ValueError) as error:
        print(f"Search error: {error}", file=sys.stderr)
        sys.exit(2)
