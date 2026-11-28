"""Round 3, lens `polynomial`: Collatz-like maps on F_q[t].

Every system is  T(f) = f/t if f(0) = 0,  (g f - g(0) f(0) h)/t otherwise
(over F_2: (g f + h)/t for odd f).  Polynomials over F_2 are ints (bit i = coeff of t^i);
over F_p they are tuples, low degree first.  `step` is an exact one-step function.

Each entry: id, field, rule, step, seed (a polynomial whose fate is part of the answer, or
None), question, answer, status, where (proof file), check (check script).
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from polylib import T2, Tp, Fp

SYSTEMS = []


def add(**kw):
    SYSTEMS.append(kw)


def f2map(g, h):
    return lambda f: T2(f, g, h)


def fpmap(p, g, h):
    F = Fp(p)
    g = F.tr(g)
    h = F.tr(h)
    return lambda f: Tp(F, F.tr(f), g, h)


def b(s):  # polynomial given high-degree-first as a binary string -> int
    return int(s, 2)


# ------------------------------------------------------------------ settled: GLOBAL true
add(id='p2_onept_h7', field='F2', rule='f/t ; ((1+t)f + 1+t+t^2)/t',
    step=f2map(0b11, 0b111), seed=None,
    question='GLOBAL with complete cycle list; BASIN of the fixed point h',
    answer='all orbits eventually periodic; cycles exactly {0}, {h}, {1,t}; f != 0 reaches h iff (1+t+t^2) | f, otherwise ends in {1,t}',
    status='PROVED', where='onept.md', check='check_onept.py')
add(id='p2_onept_family', field='F2', rule='f/t ; ((1+t)f + h)/t, any h with h(0)=1',
    step=None, seed=None,
    question='GLOBAL with cycle list, for every h',
    answer='GLOBAL true; with h=(1+t)^a k: k|f <=> k|T(f); nonzero f reaches {0,h} iff k|f; '
           'only cycles {0},{h} iff h=(1+t)^a; if (1+t) does not divide h, basin(h) = hF_2[t]\\{0}',
    status='PROVED', where='onept.md', check='check_onept.py')
add(id='p3_st', field='F3', rule='f/t ; ((1+t)f - f(0))/t  (Snapp-Tracy)',
    step=fpmap(3, (1, 1), (1,)), seed=None,
    question='GLOBAL with complete cycle list',
    answer='GLOBAL true; f != 0 periodic iff its Newton sequence sum_i C(n,i)a_i never vanishes; '
           'periodic points of degree < 3^e <-> nowhere-zero words of length 3^e (2^(3^e) of them), S = shift',
    status='PROVED', where='snapptracy.md', check='check_snapptracy.py')
add(id='p4_st', field='F4', rule='f/t ; ((1+t)f - f(0))/t over F_4',
    step=None, seed=None,
    question='GLOBAL with complete cycle list',
    answer='as p3_st with values in F_4^*: 3^(2^e) periodic points of degree < 2^e; e.g. 1+wt has period 2',
    status='PROVED', where='snapptracy.md', check='check_snapptracy.py')
add(id='pq_st_family', field='Fq', rule='f/t ; (g f - g0 f(0) (g/g0)^a)/t, deg g = 1',
    step=None, seed=None,
    question='GLOBAL with complete cycle list for every degree-1 g, every q, every a',
    answer='GLOBAL true; periodic points = (g/g0)^a * {u : v_n(u) = sum C(n,i) g1^(n-i) g0^i u_i never 0}',
    status='PROVED', where='snapptracy.md', check='check_snapptracy.py')

# ------------------------------------------------------------------ settled: GLOBAL false
add(id='p2_t3', field='F2', rule='f/t ; ((1+t^3)f + 1)/t',
    step=f2map(0b1001, 1), seed=b('1010111'),
    question='GLOBAL',
    answer='false: the orbit of 1+t+t^2+t^4+t^6 diverges; T^{18N}(f_N)=f_{2N}, f_N=(1+t+t^3)^{N-1}(1+X+X^2+X^4+X^6), X=t^N',
    status='PROVED', where='divergence.md#D1', check='check_divergence.py')
add(id='p2_cube', field='F2', rule='f/t ; ((1+t)^3 f + 1)/t',
    step=f2map(0b1111, 1), seed=1,
    question='FATE of 1 / GLOBAL',
    answer='false: T^{6(2^n-1)}(1) = (1+t^2+t^3)^{2^n-1}; the orbit of 1 diverges (probably known: Matthews)',
    status='PROVED', where='divergence.md#D2', check='check_divergence.py')
add(id='p2_cube_k', field='F2', rule='f/t ; ((1+t)^{2^k+1} f + 1)/t, k >= 1',
    step=None, seed=1,
    question='FATE of 1 / GLOBAL, for every k >= 1',
    answer='false for all k: T^{(4^k+2^k)N}(w^{N-1}) = w^{2^k N-1}, w = t+(1+t)^{2^k+1}; the orbit of 1 diverges',
    status='PROVED', where='divergence.md#D2', check='check_divergence.py (k=1,2,3)')
add(id='p2_tri_k', field='F2', rule='f/t ; ((1+t+t^{2^k+1})f + h)/t, C_k=1+..+t^{2^k} divides h',
    step=f2map(0b1011, 0b111), seed=0b11,
    question='GLOBAL (every k >= 1, every such h)',
    answer='false: f_N=(h/C_k)(1+t)^{N-1}, T^{2N} f_N = f_{2^k N}; for h=C_k the all-ones polynomials of length 2^n',
    status='PROVED', where='divergence.md#D3', check='check_divergence.py (k=1,2,3)')
add(id='p2_crit', field='F2', rule='f/t ; ((1+t+t^2)f + 1+t+t^2+t^5)/t',
    step=f2map(0b111, 0b100111), seed=0b101111,
    question='GLOBAL (zero average degree drift)',
    answer='false: f_N=(1+t+t^3)(1+X+X^2)+(1+t)^2(X+X^2), T^{4N}f_N=f_{2N}; seed f_1=1+t+t^2+t^3+t^5; '
           'also false for every multiple k*h, k(0)=1',
    status='PROVED', where='divergence.md#D4', check='check_divergence.py')
add(id='p2_ML', field='F2', rule='f/t ; ((1+t^2)f + h)/t, any h',
    step=f2map(0b101, 1), seed=0b1011,
    question='GLOBAL for every h',
    answer='false for every h (Matthews-Leigh 1987 for h=1, re-proved by two-point renormalization; all h by twist transfer)',
    status='PROVED (h=1 known)', where='divergence.md#D0', check='check_divergence.py')
add(id='p3_a', field='F3', rule='f/t ; ((2+t^2)f - 2f(0)(1+t+2t^2))/t',
    step=fpmap(3, (2, 0, 1), (1, 1, 2)), seed=(1, 0, 1),
    question='GLOBAL', answer='false: T^{8N}(1+t^{2N}) = 1+t^{6N} (N=3^n); the orbit of 1+t^2 diverges',
    status='PROVED', where='divergence.md#D5', check='check_divergence.py')
add(id='p3_b', field='F3', rule='f/t ; ((1+t+t^2)f - f(0)(1+t^2))/t',
    step=fpmap(3, (1, 1, 1), (1, 0, 1)), seed=(0, 1, 1, 2),
    question='GLOBAL', answer='false: f_N=t^N+t^{2N}+2t^{3N}, T^{8N} f_N = f_{3N}',
    status='PROVED', where='divergence.md#D5', check='check_divergence.py')
add(id='p3_c', field='F3', rule='f/t ; ((1+2t^2)f - f(0)(1+2t+2t^2))/t',
    step=fpmap(3, (1, 0, 2), (1, 2, 2)), seed=(1, 0, 1),
    question='GLOBAL', answer='false: f_N = 1+t^{2N}, T^{8N} f_N = f_{3N}',
    status='PROVED', where='divergence.md#D5', check='check_divergence.py')
add(id='p3_d', field='F3', rule='f/t ; ((2+t+2t^2)f - 2f(0)(1+t^2))/t',
    step=fpmap(3, (2, 1, 2), (1, 0, 1)), seed=(0, 1, 2, 2),
    question='GLOBAL', answer='false: f_N=t^N+2t^{2N}+2t^{3N}, T^{32N} f_N = f_{9N}',
    status='PROVED', where='divergence.md#D5', check='check_divergence.py')
add(id='p2_sq111', field='F2', rule='f/t ; ((1+t^2+t^4)f + 1+t+t^2+t^4)/t',
    step=f2map(0b10101, 0b10111), seed=0b11,
    question='GLOBAL', answer='false: line certificate P=1+X (f_N = 1+t^N), tau=3N',
    status='PROVED', where='divergence.md#D6', check='check_divergence.py')
add(id='p2_1034', field='F2', rule='f/t ; ((1+t^3+t^4)f + 1+t+t^3+t^4)/t',
    step=f2map(0b11001, 0b11011), seed=0b111,
    question='GLOBAL', answer='false: line certificate P=1+X+X^2 (f_N=1+t^N+t^{2N}), tau=2N',
    status='PROVED', where='divergence.md#D6', check='check_divergence.py')

# ------------------------------------------------------------------ structure / open
add(id='p2_nichols', field='F2', rule='f/t ; ((1+t+t^2)f + 1)/t',
    step=f2map(0b111, 1), seed=0b1000111,
    question='GLOBAL (Nichols 2016: is there a divergent orbit?)',
    answer='OPEN. Proved: T^2 o phi = phi o T with phi(u)=((1+t)u)^2, so (1+t)^{2^{k+1}-2} has period exactly 2^{k+2}: '
           'infinitely many cycles. Every certificate of the line/two-point type needs non-polynomial periodic points (N1); none found.',
    status='OPEN (PARTIAL: infinitely many cycles PROVED)', where='frobenius.md, classification.md',
    check='check_frobenius.py')
add(id='p2_m3b_h1', field='F2', rule='f/t ; ((1+t+t^3)f + 1)/t',
    step=f2map(0b1011, 1), seed=None, question='GLOBAL',
    answer='OPEN (divergence proved only for twists h in (1+t+t^2)F_2[t])', status='OPEN',
    where='classification.md', check=None)
add(id='p2_m3c_h1', field='F2', rule='f/t ; ((1+t^2+t^3)f + 1)/t',
    step=f2map(0b1101, 1), seed=None, question='GLOBAL',
    answer='OPEN (no certificate of any kind found)', status='OPEN', where='classification.md', check=None)
