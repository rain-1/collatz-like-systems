#!/usr/bin/env python3
"""Independent, reproducible finite checks for the original 1932 Collatz orbit of 8.

No part of this script proves that the orbit is infinite. Standard library only.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction
from pathlib import Path

Q_S = ((2, 0), (4, -1), (4, 1))


def G(n: int) -> int:
    assert n > 0
    q, r = divmod(n, 3)
    return (2*q, 4*q+1, 4*q+3)[r]


def inverse(n: int) -> int:
    assert n > 0
    if not n & 1:
        return 3*n//2
    return (3*n + (1 if n % 4 == 1 else -1))//4


def two_sided_discrepancy(steps: int):
    forward = backward = 8
    zeros = odd_back = 0
    minimum = None
    first_nonpositive = None
    sample_indices = {1, 10, 100, 1_000, 10_000, 100_000, 200_000, 300_000, steps}
    samples = {}
    classes = set()
    completed_3_9_at = None
    reached_start = None
    for k in range(1, steps+1):
        zeros += (forward % 3 == 0)
        odd_back += (backward % 2 == 1)
        forward = G(forward)
        backward = inverse(backward)
        discrepancy = k-zeros-odd_back
        minimum = discrepancy if minimum is None else min(minimum, discrepancy)
        if discrepancy <= 0 and first_nonpositive is None:
            first_nonpositive = k
        if forward == 8 and reached_start is None:
            reached_start = k
        if k in sample_indices:
            samples[str(k)] = dict(zeros=zeros, odd_backward=odd_back,
                                   discrepancy=discrepancy)
        if completed_3_9_at is None:
            classes.add(forward % 19683)
            if len(classes) == 19683:
                completed_3_9_at = k
    return dict(steps=steps, samples=samples, min_discrepancy=minimum,
                first_nonpositive_discrepancy=first_nonpositive,
                first_forward_return=reached_start, forward_bits=forward.bit_length(),
                backward_bits=backward.bit_length(),
                residue_classes_mod_19683=len(classes),
                full_residue_coverage_at_step=completed_3_9_at)


def coefficients(word):
    Q, D, S = 1, 1, 0
    for r in word:
        q, s = Q_S[r]
        S = q*S+s*D
        Q *= q
        D *= 3
    return Q, D, S


def rat_residue3(x):
    assert x.denominator % 3
    return x.numerator*pow(x.denominator, -1, 3) % 3


def validate_rational_cycle(word, x):
    start = x
    values = []
    for r in word:
        assert x > 0 and x.denominator % 6 in (1, 5)
        assert rat_residue3(x) == r, (x, r)
        values.append(x)
        q, s = Q_S[r]
        x = (q*x+s)/3
    assert x == start
    return dict(period=len(word), start=str(start), min_value=str(min(values)),
                residue_word=''.join(map(str,word)), positive=True)


def modular_graph_check(limit):
    # Each residue class a modulo m has all possible output residues already
    # represented by n=a+j*m, j=0,1,2 (with n>0), because G(n+3m)=G(n)+q_r*m.
    checked = 0
    for m in range(1, limit+1):
        adj = [set() for _ in range(m)]
        rev = [set() for _ in range(m)]
        for a in range(m):
            base = a if a else m
            for j in range(3):
                b = G(base+j*m)%m
                adj[a].add(b)
                rev[b].add(a)
        def count_reached(graph):
            seen = {0}
            todo = [0]
            while todo:
                a = todo.pop()
                for b in graph[a]:
                    if b not in seen:
                        seen.add(b)
                        todo.append(b)
            return len(seen)
        assert count_reached(adj) == m, (m, 'forward')
        assert count_reached(rev) == m, (m, 'reverse')
        checked += 1
    return {'checked_moduli': checked, 'all_strongly_connected': True}


def basic_exact_checks():
    for n in range(1, 30_001):
        assert inverse(G(n)) == n
        assert G(inverse(n)) == n
    assert [G(n) for n in (8,11,15,10,13,17)] == [11,15,10,13,17,23]
    for word, numerator, denominator in [
        ('220112022000', 220520, 7153),
        ('220112000', 3064, 3299),
    ]:
        w = tuple(map(int,word))
        Q, D, S = coefficients(w)
        x = Fraction(S, D-Q)
        assert x == Fraction(numerator, denominator)
        validate_rational_cycle(w, x)
    n, Q, D, S, zero = 8, 1, 1, 0, 0
    for k in range(1, 501):
        r = n % 3
        q, s = Q_S[r]
        zero += (r == 0)
        S = q*S+s*D
        Q *= q
        D *= 3
        n = (q*n+s)//3
        assert n*D == 8*Q+S
        assert Q > D and S > 0
    assert zero == 168 and 5*S > Q
    return {'inverse_checked_through': 30000, 'first_500_Q_gt_D': True,
            'first_500_S_positive': True, 'c_500': zero,
            'R_500_decimal': format(S/Q, '.16f'),
            'rational_cycles_verified': ['220112022000', '220112000']}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--steps', type=int, default=10_000)
    parser.add_argument('--scc-max', type=int, default=100)
    parser.add_argument('--json', type=Path, default=None)
    args=parser.parse_args()
    assert args.steps>=1 and args.scc_max>=1
    report={'notes':'FINITE VERIFICATION ONLY; NOT A PROOF OF INFINITE ORBIT',
            'basic':basic_exact_checks(),
            'two_sided':two_sided_discrepancy(args.steps),
            'modular_graphs':modular_graph_check(args.scc_max)}
    print(json.dumps(report, indent=2))
    if args.json:
        args.json.parent.mkdir(parents=True,exist_ok=True)
        args.json.write_text(json.dumps(report,indent=2)+'\n')

if __name__=='__main__':main()
