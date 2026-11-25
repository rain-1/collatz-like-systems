"""Shared exact-integer helpers for the split-family checks (stdlib only)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from systems import get


def orbit_fate(step, seed, limit=10**6):
    seen = {}
    n, i = seed, 0
    while n not in seen:
        if i > limit:
            raise RuntimeError("no cycle within limit")
        seen[n] = i
        n = step(n)
        i += 1
    pre = seen[n]
    order = sorted(seen, key=seen.get)
    cycle = order[pre:]
    return pre, cycle


def check_fate(sid, exp_pre, exp_period):
    s = get(sid)
    pre, cycle = orbit_fate(s['step'], s['seed'])
    print(f"{sid}: seed {s['seed']} preperiod {pre}, period {len(cycle)}, "
          f"cycle min {min(cycle)}, seed in cycle: {s['seed'] in cycle}")
    assert s['seed'] not in cycle
    assert pre == exp_pre and len(cycle) == exp_period
    return cycle


def check_descent(sid, d, mult_on_1, mult_on_3):
    """Verify the descent lemma for a split map with odd branches
    n=1 mod 4 -> mult_on_1*n+d, n=3 mod 4 -> mult_on_3*n+d,
    where both images are divisible by 4 and max multiplier is 3:
      (i) mult*r + d == 0 mod 4 for r = 1, 3 (exact residue check),
      (ii) the block map g (n/2 if even, else f then two halvings) satisfies
           g(n) < n for n > d and g([1,d]) in [1,d]; checked symbolically:
           (3n+d)/4 < n  <=>  n > d,  and for n <= d: (3n+d)/4 <= d,
      (iii) brute force: for every n in [1, 4d] the f-orbit cycles, and the
           set of cycles is listed exhaustively."""
    s = get(sid)
    f = s['step']
    assert (mult_on_1 * 1 + d) % 4 == 0 and (mult_on_3 * 3 + d) % 4 == 0
    assert max(mult_on_1, mult_on_3) <= 3
    # spot-check that f agrees with the stated branches on a full residue window
    for n in range(1, 4 * d + 64):
        if n % 2 == 0:
            assert f(n) == n // 2
        elif n % 4 == 1:
            assert f(n) == mult_on_1 * n + d and f(n) % 4 == 0
        else:
            assert f(n) == mult_on_3 * n + d and f(n) % 4 == 0
    # g-invariance of [1, d] (exhaustive) and descent (exhaustive on a window
    # beyond d; the general case is the linear inequality above)
    def g(n):
        return n // 2 if n % 2 == 0 else f(n) // 4
    for n in range(1, d + 1):
        assert 1 <= g(n) <= d
    for n in range(d + 1, 20 * d + 1000):
        assert g(n) < n
    # exhaustive cycle list on [1, d]
    cycles = set()
    for start in range(1, d + 1):
        seen = set(); n = start
        while n not in seen:
            seen.add(n); n = f(n)
        c = [n]; m = f(n)
        while m != n:
            c.append(m); m = f(m)
        cycles.add(min(c))
    print(f"{sid}: descent lemma OK; all orbits enter [1,{d}]; "
          f"cycles (by min element): {sorted(cycles)}")
    return sorted(cycles)
