"""swT9_s8: Q = sigma_{9} o T, seed 8.  OPEN.  Checks the finite evidence only:
no return in 1e5 steps; no separating union of residue classes mod K for every
K <= 150 and several larger K; no small binary/ternary DFA certificate."""
import sys, itertools
from _common import get, T, sigma, separates, is_affine_on_classes, bijective_window, first_return
s = get("swT9_s8"); Q = s["step"]; sg = sigma(18, [9])
ok = True
def claim(name, c):
    global ok
    print(("PASS " if c else "FAIL ") + name, flush=True); ok = ok and c
claim("step = sigma(T(n)), |Q-T|<=1 on [1,2e5]",
      all(Q(n) == sg(T(n)) and abs(Q(n) - T(n)) <= 1 for n in range(1, 200001)))
claim("Q affine on classes mod 27", is_affine_on_classes(Q, 27))
claim("Q bijective on window", bijective_window(Q, 50000))
claim("no return to 8 within 1e5 steps", first_return(Q, 8, 100000) is None)
bad = [K for K in list(range(1, 151)) + [162, 216, 243, 288, 324] if separates(Q, 27, 8, K)]
claim("no congruence separator mod K for K<=150 and K in {162,216,243,288,324}", not bad)

# small automata: canonical digits, MSD or LSD first; accepted set must
# reject 8, accept Q(8),...,Q^25(8), and be closed on [1,3000]
def digits(n, b, lsd):
    d = []
    while n: d.append(n % b); n //= b
    return d if lsd else d[::-1]
orbit = [Q(8)]
for _ in range(25): orbit.append(Q(orbit[-1]))
def dfa_found(b, lsd, S, N=3000):
    tests = list(range(1, N)); dg = {n: digits(n, b, lsd) for n in set(tests) | {Q(n) for n in tests} | set(orbit) | {8}}
    for delta in itertools.product(range(S), repeat=S * b):
        st = {}
        def run(n):
            if n not in st:
                q = 0
                for d in dg[n]: q = delta[q * b + d]
                st[n] = q
            return st[n]
        for acc in range(1, 2 ** S - 1):
            A = lambda n: (acc >> run(n)) & 1
            if A(8) or not all(A(x) for x in orbit): continue
            if all(not A(n) or A(Q(n)) for n in tests): return True
    return False
sizes = [(2, 4), (3, 3)]
claim("no DFA certificate up to (base, states) %s, MSD and LSD" % sizes,
      not any(dfa_found(b, lsd, S) for b, Smax in sizes for lsd in (False, True) for S in range(2, Smax + 1)))
sys.exit(0 if ok else 1)
