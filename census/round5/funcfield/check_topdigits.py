"""Exact check of Lemma T (top-digit decoupling) and its cycle corollaries on every cycle found
by exhaustive search in small degree, for several systems.

Lemma T: for any f and n steps with word w (L digits, cumulative slopes S_1..S_n),
    T^n f = (G_w f + H_w)/t^L,  deg H_w <= L + kappa + max_{1<=i<=n}(S_n - S_i).
Corollary T1: if f is periodic (period n), deg f = D, then
    deg(t^L - G_w) <= L + kappa + R - D,   R = max_{1<=i<=n}(S_n - S_i).
Corollary T2 (one non-constant multiplier g_1, u = g_1^*/g_1^*(0) = 1 + a s^nu + ...):
    if D' = D - kappa - R >= 1 then nu * p^{v_p(n_1)} >= D'.
The script finds every polynomial f with 1 <= deg f <= Dmax that is periodic (within a step
limit), recomputes w, G_w, H_w exactly and checks Lemma T, T1 and (where it applies) T2.
Exits 1 on any failure.
"""
import sys, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0] if '/' in __file__ else '.')
from ffmap import *
from check_frobenius_cycles import compose, kappa_of

FAIL = []


def periodic_word(S, f, limit):
    x, w = f, []
    for k in range(limit):
        x, i, e = step(S, x)
        w.append(i)
        if x == f:
            return tuple(w)
        if deg(x) > deg(f) + 60:
            return None
    return None


def vp(n, p):
    v = 0
    while n % p == 0 and n:
        n //= p
        v += 1
    return v


def nu_of(S):
    """For systems with exactly one branch of non-constant multiplier: (branch, nu)."""
    q, brs = S
    nc = [i for i, (r, g, c) in enumerate(brs) if deg(trim(g)) >= 1]
    if len(nc) != 1:
        return None
    g = trim(brs[nc[0]][1])
    rev = g[::-1]                       # g^*(s) coefficients, low first
    inv = [b for b in range(1, q) if fmul(q, b, rev[0]) == 1][0]
    u = [fmul(q, inv, a) for a in rev]  # u = g^*/g^*(0)
    nu = next(i for i in range(1, len(u)) if u[i])
    return nc[0], nu


def run(name, Dmax, limit=400):
    S = load_spec(f'specs/{name}.txt')
    q, brs = S
    p = 2 if q in (2, 4) else 3
    kap = kappa_of(S)
    nuinfo = nu_of(S)
    ncyc = 0
    seen = set()
    t2_checked = 0
    for D in range(1, Dmax + 1):
        for low in itertools.product(range(q), repeat=D):
            for lead in range(1, q):
                f = trim(low + (lead,))
                if f in seen:
                    continue
                w = periodic_word(S, f, limit)
                if w is None:
                    continue
                # mark cycle
                x = f
                for _ in w:
                    seen.add(x)
                    x = step(S, x)[0]
                ncyc += 1
                G, H, L = compose(S, w)
                # Lemma T: T^n f = (G f + H)/t^L
                num = padd(q, pmul(q, G, f), H)
                if any(num[:L]) or trim(num[L:]) != f:
                    FAIL.append(('affine form', name, f))
                slopes = [deg(trim(brs[i][1])) - len(brs[i][0]) for i in w]
                Sp = list(itertools.accumulate(slopes))
                R = max(Sp[-1] - Sp[i] for i in range(len(Sp)))
                if deg(H) > L + kap + R:
                    FAIL.append(('deg H bound', name, f, deg(H), L + kap + R))
                Delta = padd(q, (0,) * L + (1,), pneg(q, G))
                if deg(Delta) > L + kap + R - D:
                    FAIL.append(('T1', name, f))
                if nuinfo is not None:
                    b1, nu = nuinfo
                    Dp = D - kap - R
                    n1 = sum(1 for i in w if i == b1)
                    if Dp >= 1:
                        t2_checked += 1
                        if n1 == 0 or nu * p ** vp(n1, p) < Dp:
                            FAIL.append(('T2', name, f, n1, nu, Dp))
    print(f'{name}: cycles through degrees 1..{Dmax}: {ncyc}; Lemma T and T1 checked on all; '
          f'T2 applicable and checked on {t2_checked}')


if __name__ == '__main__':
    run('A3', 7)
    run('B3', 9)
    run('G3', 9)
    run('Q4', 6)
    run('Q4b', 5)
    run('S2', 16)
    run('S2c', 14)
    if FAIL:
        print('FAIL', FAIL[:10])
        sys.exit(1)
    print('all top-digit checks passed')
