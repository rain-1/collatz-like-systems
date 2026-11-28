"""Small exact extensions of census/round2/automata/autolib.py."""
import os
import sys
from collections import deque

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "round2", "automata"))
import autolib  # noqa: E402,F401
from autolib import closure_violation, accepts, minimize, digits, check_fooling_set  # noqa: E402,F401


def meets_residues(dfa, M, residues):
    """Least-length accepted n with n mod M in `residues`, or None (exact BFS)."""
    b = dfa["base"]
    delta, acc = dfa["delta"], dfa["acc"]
    start = []
    seen = {}
    q = deque()
    for d in range(1, b):
        st = (delta[0][d], d % M)
        if st not in seen:
            seen[st] = d
            q.append(st)
    while q:
        st = q.popleft()
        s, r = st
        n = seen[st]
        if s in acc and r in residues:
            return n
        for d in range(b):
            nst = (delta[s][d], (r * b + d) % M)
            if nst not in seen:
                seen[nst] = n * b + d
                q.append(nst)
    return None


def dfa_from_predicate(base, pred_state):
    """Build a DFA from an explicit finite-state description.
    pred_state = (init, trans(state, digit) -> state, accept(state) -> bool),
    states hashable; explores reachable states from init after a nonzero
    first digit (the start state itself is init)."""
    init, trans, accept = pred_state
    ids = {init: 0}
    order = [init]
    delta = []
    i = 0
    while i < len(order):
        s = order[i]
        row = []
        for d in range(base):
            t = trans(s, d)
            if t not in ids:
                ids[t] = len(order)
                order.append(t)
            row.append(ids[t])
        delta.append(row)
        i += 1
    acc = {ids[s] for s in order if accept(s)}
    return dict(base=base, delta=delta, acc=acc)
