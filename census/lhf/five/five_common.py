"""Shared exact-integer checks for the 5n+d family (census/lhf/five)."""
import os, sys, time
from fractions import Fraction
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, '..', '..')))
from systems import get  # noqa: E402

def U(m):            # 5x+1 map, also on rationals with odd denominator (parity of numerator)
    if isinstance(m, Fraction):
        return m / 2 if m.numerator % 2 == 0 else 5 * m + 1
    return m // 2 if m % 2 == 0 else 5 * m + 1

def T(d):
    return lambda n: n // 2 if n % 2 == 0 else 5 * n + d

FAIL = []
def ok(cond, msg):
    print(('PASS ' if cond else 'FAIL ') + msg)
    if not cond:
        FAIL.append(msg)

def check_system(key, d, mult=5):
    st = get(key)['step']
    ok(all(st(n) == (n // 2 if n % 2 == 0 else mult * n + d) for n in range(1, 20001)),
       f'{key}: systems.get step equals even n/2, odd {mult}n+{d} on 1..20000')

def check_dZ_conjugacy(d, M=100000):
    t = T(d)
    ok(all(t(d * m) == d * U(m) for m in range(1, M + 1)),
       f'T_{d}(d*m) = d*U(m) for m=1..{M} (dZ is invariant and conjugate to 5x+1)')

def check_rational_conjugacy(d, seed, steps=3000):
    t = T(d); n = seed; x = Fraction(seed, d)
    good = True
    for _ in range(steps):
        if Fraction(n, d) != x:
            good = False; break
        n, x = t(n), U(x)
    ok(good, f'orbit of {seed} under 5n+{d} = {d} * (5x+1 orbit of rational {seed}/{d}), {steps} steps')

def check_units_invariant(d, p, M=100000):
    t = T(d)
    ok(all(t(n) % p != 0 for n in range(1, M + 1) if n % p != 0),
       f'5n+{d}: n coprime to {p} => T(n) coprime to {p}, n<= {M}')

def check_first_odd_step_leaves_5Z(d, M=100000):
    t = T(d)
    ok(d % 5 != 0 and all(t(n) % 5 == d % 5 for n in range(1, M + 1, 2)),
       f'5n+{d}: every odd step lands in residue {d % 5} mod 5 (a unit), n<= {M}')

def orbit(f, s, k):
    out = [s]
    for _ in range(k):
        s = f(s); out.append(s)
    return out

def check_orbit_of_7_class(steps=20000):
    """CLS-009/013/015/017: all four seeds follow the 5x+1 orbit of 7."""
    u7 = orbit(U, 7, steps)
    ok(u7[:4] == [7, 36, 18, 9], '5x+1: 7 -> 36 -> 18 -> 9')
    # 10n+2 seed 7: delete the inserted terms 10n+2 after each odd term
    F = lambda n: n // 2 if n % 2 == 0 else 10 * n + 2
    f = orbit(F, 7, 2 * steps); red = [f[0]]
    i = 0
    while i < len(f) - 2:
        if f[i] % 2:
            ok_ = f[i + 1] == 2 * (5 * f[i] + 1) and f[i + 2] == 5 * f[i] + 1
            if not ok_:
                ok(False, '10n+2 double-step identity'); return
            red.append(f[i + 2]); i += 2
        else:
            red.append(f[i + 1]); i += 1
    ok(red[:steps // 2] == u7[:steps // 2], f'10n+2 orbit of 7 with inserted terms removed = 5x+1 orbit of 7 ({steps//2} terms)')
    # 5n+3 seed 27 = 3 * U-orbit of 9 = 3 * tail of orbit of 7
    o3 = orbit(T(3), 27, steps - 3)
    ok(o3 == [3 * v for v in u7[3:]], f'5n+3 orbit of 27 = 3 * (5x+1 orbit of 7 from step 3), {steps-3} steps')
    # 5n+5 seed 27 -> 140 = 5*28, 28 -> 14 -> 7
    o5 = orbit(T(5), 27, steps)
    ok(o5[1] == 140 and o5[3] == 35 and o5[3:] == [5 * v for v in u7[:steps - 2]],
       f'5n+5 orbit of 27: 27,140,70,35,... = 5 * (5x+1 orbit of 7) from step 3')

def finish(t0):
    dt = time.time() - t0
    print(f'time {dt:.1f}s')
    sys.exit(1 if FAIL else 0)
