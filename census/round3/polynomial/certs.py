"""Divergence certificates (data only).  Read by check_divergence.py and systems.py.

Polynomials over F_p are tuples low-first.  'kind':
  line     : P in F_p[X], Phi^k(P) = P(X^(p^b));  f_N = rho * P(t^N), rho = g(0) h /(g - t)
  twopoint : (F_2 only) periodic words w1 (start), w2; Q in F_2[X] with Q(0)=0;
             f_N = (c1 + Q(t^N)(c1+c2)) * B  where B = the declared twist (denominator)
See renormalization.md for the lemmas that turn a verified certificate into a proof.
"""
CERTS = [
    # ---------------------------------------------------------------- F_2, h = 1
    dict(id='p2_cube', p=2, g=(1, 1, 1, 1), h=(1,), kind='line', P=(1, 0, 1, 1), N0=1,
         note='g=(1+t)^3, h=1: T^{6N}(w^{N-1}) = w^{2N-1}, w=1+t^2+t^3; the orbit of 1 diverges'),
    dict(id='p2_cube5', p=2, g=(1, 1, 0, 0, 1, 1), h=(1,), kind='line', P=(1, 0, 0, 0, 1, 1), N0=1,
         note='g=(1+t)^5, h=1: P=w(X), w=t+g; T^{20N}(w^{N-1}) = w^{4N-1}; the orbit of 1 diverges'),
    dict(id='p2_cube9', p=2, g=(1, 1, 0, 0, 0, 0, 0, 0, 1, 1), h=(1,), kind='line',
         P=(1, 0, 0, 0, 0, 0, 0, 0, 1, 1), N0=1,
         note='g=(1+t)^9, h=1: P=w(X), w=t+g; T^{72N}(w^{N-1}) = w^{8N-1}; the orbit of 1 diverges'),
    dict(id='p2_ML', p=2, g=(1, 0, 1), h=(1,), kind='twopoint', w1='1', w2='10', Q=(0, 0, 0, 1), N0=1,
         note='g=1+t^2, h=1 (Matthews-Leigh 1987, re-proved): f_N = r + t^{3N}(1+r), r=1/(1+t+t^2)'),
    dict(id='p2_t3', p=2, g=(1, 0, 0, 1), h=(1,), kind='line', P=(1, 0, 0, 0, 0, 0, 1, 0, 0, 1), N0=1,
         note='g=1+t^3, h=1: f_N=(1+t^{6N}+t^{9N})/(1+t+t^3), T^{18N} f_N = f_{2N}; f_1 = 1+t+t^2+t^4+t^6'),
    # ---------------------------------------------------------------- F_2, twisted
    dict(id='p2_tri1', p=2, g=(1, 1, 0, 1), h=(1, 1, 1), kind='line', P=(1, 1), N0=1,
         note='g=1+t+t^3, h=1+t+t^2: f_N=(1+t)^{N-1}, T^{2N} f_N = f_{2N}'),
    dict(id='p2_tri2', p=2, g=(1, 1, 0, 0, 0, 1), h=(1, 1, 1, 1, 1), kind='line', P=(1, 1), N0=1,
         note='g=1+t+t^5, h=1+t+..+t^4: f_N=(1+t)^{N-1}, T^{2N} f_N = f_{4N}'),
    dict(id='p2_tri3', p=2, g=(1, 1) + (0,) * 7 + (1,), h=(1,) * 9, kind='line', P=(1, 1), N0=1,
         note='g=1+t+t^9, h=1+t+..+t^8: f_N=(1+t)^{N-1}, T^{2N} f_N = f_{8N}'),
    dict(id='p2_crit', p=2, g=(1, 1, 1), h=(1, 1, 1, 0, 0, 1), kind='twopoint', w1='1', w2='101',
         Q=(0, 1, 1), N0=1,
         note='g=1+t+t^2 (drift 0), h=(1+t)^2(1+t+t^3)=1+t+t^2+t^5: '
              'f_N=(1+t+t^3)(1+X+X^2)+(1+t)^2(X+X^2), X=t^N; T^{4N} f_N = f_{2N}'),
    dict(id='p2_sq111', p=2, g=(1, 0, 1, 0, 1), h=(1, 1, 1, 0, 1), kind='line', P=(1, 1), N0=1,
         note='g=(1+t+t^2)^2, h=t+g: line certificate P=1+X'),
    dict(id='p2_1034', p=2, g=(1, 0, 0, 1, 1), h=(1, 1, 0, 1, 1), kind='line', P=(1, 1, 1), N0=1,
         note='g=1+t^3+t^4, h=t+g: line certificate P=1+X+X^2'),
    # ---------------------------------------------------------------- F_3, twisted h=(g-t)/g(0)
    dict(id='p3_a', p=3, g=(2, 0, 1), h=(1, 1, 2), kind='line', P=(1, 0, 1), N0=1,
         note='F_3, g=2+t^2, h=1+t+2t^2: f_N = 1+t^{2N}, T^{8N} f_N = f_{3N}'),
    dict(id='p3_b', p=3, g=(1, 1, 1), h=(1, 0, 1), kind='line', P=(0, 1, 1, 2), N0=1,
         note='F_3, g=1+t+t^2, h=1+t^2: f_N = t^N+t^{2N}+2t^{3N}, T^{8N} f_N = f_{3N}'),
    dict(id='p3_c', p=3, g=(1, 0, 2), h=(1, 2, 2), kind='line', P=(1, 0, 1), N0=1,
         note='F_3, g=1+2t^2, h=1+2t+2t^2: f_N = 1+t^{2N}'),
    dict(id='p3_d', p=3, g=(2, 1, 2), h=(1, 0, 1), kind='line', P=(0, 1, 2, 2), N0=1,
         note='F_3, g=2+t+2t^2, h=1+t^2: f_N = t^N+2t^{2N}+2t^{3N}, renormalizes N -> 9N'),
]
