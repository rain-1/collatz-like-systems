"""Theorem Z machinery: a strict p-adic descent certificate settles the map on all of Z.

Reuses census/round2/descent/descent_lib.py (certificate engine, verifier).
All arithmetic exact (Python ints).
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'round2', 'descent'))
import descent_lib as DL  # noqa: E402


def strict(p, leaves):
    """True iff every leaf has P < p^K (no slope-1 leaves)."""
    return all(P < p ** K for K, r, j, P, R in leaves)


def z_exceptional(p, leaves):
    """All integers n (any sign) lying in a leaf class n = p^K t + r with
    |T^j(n)| >= |n|, i.e. |P t + R| >= |p^K t + r|.  For P < p^K this forces
    (p^K - P)|t| <= |R| + |r|, so the t-range is finite; we test each t exactly."""
    E = []
    for K, r, j, P, R in leaves:
        M = p ** K
        assert P < M
        B = (abs(R) + abs(r)) // (M - P)
        for t in range(-B - 1, B + 2):
            if abs(P * t + R) >= abs(M * t + r):
                E.append(M * t + r)
    return sorted(set(E))


def cycles_from(T, starts, cap=10 ** 7):
    """Simulate each start until a repeat; return the set of cycles (tuples
    rotated to start at their minimum)."""
    cycles = set()
    for e in starts:
        seen = set()
        x = e
        while x not in seen:
            seen.add(x)
            x = T(x)
            assert len(seen) < cap, e
        c = [x]
        y = T(x)
        while y != x:
            c.append(y)
            y = T(y)
        k = c.index(min(c))
        cycles.add(tuple(c[k:] + c[:k]))
    return cycles


def settle_on_Z(p, m, table, maxK=80):
    """Build + verify the minimal certificate, check strictness, return
    (certificate summary, E_Z, cycles on Z)."""
    c = DL.certificate(p, m, table, maxK=maxK)
    assert c['ok']
    DL.verify_certificate(p, m, table, c['leaves'])
    # verify affine forms also at negative t (the identity is polynomial in t,
    # but we re-test directly at several negative t as well)
    T = DL.step_fn(p, m, table)
    for K, r, j, P, R in c['leaves']:
        for t in (-1, -2, -3, -1000003):
            n = p ** K * t + r
            x = n
            for _ in range(j):
                x = T(x)
            assert x == P * t + R
    assert strict(p, c['leaves'])
    E = z_exceptional(p, c['leaves'])
    cyc = cycles_from(T, E)
    return c, E, cyc
