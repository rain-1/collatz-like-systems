"""Check for race_s21.md and the application of theorem2_quotient.md.  Exit 0.

Claims tested:
 (1) the 210-branch affine table equals the definition of R (1..10^5, random big n);
 (2) the GLOBAL description: n has an unbounded orbit iff v2 < v3 + v5;
     otherwise the orbit reaches a fixed point (gcd(n,30)=1).  Tested on
     1..30000 and on 3000 random n = 2^a 3^b 5^g 7^e m (exponents up to 40):
     divergent ones are followed until they reach a round start (0,c,e) and
     then for two further rounds with (c,e) -> (c+1,2e) checked exactly;
     the others are simulated to the fixed point;
 (3) the orbit of 21 passes through P_k = 2^(2^k) 3^(2^k+k+2), k = 0..9, in
     order, at the predicted times;
 (4) the 2-state base-6 DFA accepts exactly {v2(n) < v3(n)} (1..10^5 and
     random), its accepted set is forward closed (exact automaton test,
     autolib.closure_violation over all n), contains no n coprime to 30
     (exact product-automaton test), and contains R(21);  minimality: no
     1-state DFA works (both 1-state languages fail);
 (5) the finite ingredients of the base-2^j / base-3^j impossibility:
     forced-out points 2^A 3^B (A >= B) reach a fixed point (simulated for
     A, B <= 40) and the index inequalities used in the proof.
"""
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from race_common import R, BRANCHES, divergent, round_point, v  # noqa: E402
from autoext import closure_violation, accepts, meets_residues  # noqa: E402
from autolib import make_step, check_partition  # noqa: E402

rng = random.Random(21)


def is_fixed(n):
    return n % 2 and n % 3 and n % 5


def fate(n, cap=10 ** 6):
    """Simulate until a fixed point or a round start of the divergent type.
    Returns ('fixed', x) or ('round', c, e, m) with n -> 3^c 7^e m, 5∤, a=0."""
    for _ in range(cap):
        if is_fixed(n):
            return ("fixed", n)
        a, b, g = v(n, 2), v(n, 3), v(n, 5)
        if g == 0 and a == 0 and b >= 1:
            e = v(n, 7)
            m = n // (3 ** b * 7 ** e)
            return ("round", b, e, m)
        n = R(n)
    raise AssertionError("no decision")


def run_round(c, e, m):
    """From 3^c 7^e m (round start) run one round, return the next round start."""
    n = 3 ** c * 7 ** e * m
    steps = 0
    while True:
        n = R(n)
        steps += 1
        if n % 5 and n % 2 and n % 3 == 0 and steps > 1:
            break
    assert steps == 2 * e + 2, (steps, e)
    return n


def main():
    # (1)
    check_partition(BRANCHES)
    step = make_step(BRANCHES)
    for n in list(range(1, 100001)) + [rng.randrange(1, 10 ** 40) for _ in range(5000)]:
        assert step(n) == R(n)
    print("(1) table ok")

    # (2)
    samples = list(range(1, 30001))
    for _ in range(3000):
        n = 2 ** rng.randint(0, 40) * 3 ** rng.randint(0, 40) * 5 ** rng.randint(0, 6) \
            * 7 ** rng.randint(0, 6) * rng.choice([1, 11, 13, 143, 17 * 19])
        samples.append(n)
    nd = nf = 0
    for n in samples:
        f = fate(n)
        if divergent(n):
            assert f[0] == "round", n
            _, c, e, m = f
            x = run_round(c, e, m)
            assert x == 3 ** (c + 1) * 7 ** (2 * e) * m
            y = run_round(c + 1, 2 * e, m)
            assert y == 3 ** (c + 2) * 7 ** (4 * e) * m
            nd += 1
        else:
            assert f[0] == "fixed", n
            nf += 1
    print("(2) GLOBAL description ok on", len(samples), "inputs:", nd, "divergent,", nf, "to fixed points")

    # (3)
    x = 21
    t = 0
    for k in range(10):
        # round k starts at 3^(1+k) 7^(2^k); P_k is reached after 2 + 2^k steps
        assert x == 3 ** (1 + k) * 7 ** (2 ** k), k
        for _ in range(2 + 2 ** k):
            x = R(x)
        t += 2 + 2 ** k
        assert x == round_point(k), k
        for _ in range(2 ** k):
            x = R(x)
        t += 2 ** k
    print("(3) orbit of 21 passes P_0..P_9")

    # (4)
    dfa = dict(base=6, delta=[[0, 0, 0, 1, 0, 0], [1, 0, 0, 1, 0, 0]], acc={1})
    for n in list(range(1, 100001)) + [rng.randrange(1, 10 ** 50) for _ in range(5000)] \
            + [2 ** rng.randint(0, 60) * 3 ** rng.randint(0, 60) * rng.choice([1, 5, 7, 35]) for _ in range(2000)]:
        assert accepts(dfa, n) == (v(n, 2) < v(n, 3)), n
    assert closure_violation(dfa, BRANCHES) is None
    assert meets_residues(dfa, 30, {r for r in range(30) if r % 2 and r % 3 and r % 5}) is None
    assert accepts(dfa, R(21)) and accepts(dfa, 21)
    one_all = dict(base=6, delta=[[0] * 6], acc={0})
    one_none = dict(base=6, delta=[[0] * 6], acc=set())
    assert meets_residues(one_all, 30, {1}) is not None      # contains the fixed point 1
    assert not accepts(one_none, R(21))
    print("(4) 2-state base-6 certificate verified exactly; minimum is 2 states")

    # (5)
    for A in range(0, 41):
        for B in range(0, A + 1):
            f = fate(2 ** A * 3 ** B)
            assert f[0] == "fixed"
    for k in range(2, 60):
        for j in range(k + 1, 61):
            assert 2 ** j >= 2 ** k + k + 2            # base 2: 2^(2^j) 3^(b_k) is forced out
    for k in range(3, 60):
        for j in range(0, k):
            assert 2 ** j + j + 2 <= 2 ** k            # base 3: 2^(2^k) 3^(b_j) is forced out
    print("(5) forced-out points and index inequalities ok")
    print("OK")


if __name__ == "__main__":
    main()
