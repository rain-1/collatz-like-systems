"""Exact finite content of Theorems A and A' (A3 over F_3, Q4b over F_4).
* Chernoff bounds: P(b)^2 <= (8/9)^b (A3) and P(b)^3 <= (243/256)^b (Q4b), b <= 300, exact P(b).
* |W_L| = number of zero-slope words: brute force for L = 6 (both systems) against the closed
  forms C(L,L/2) 2^{L/2} and C(L,L/3) 3^{2L/3}, and the binomial inequality C(2N,N) >= 4^N/(2N+1).
* For L = 2*3^k, k <= 6: (2 sqrt 2)^L/(L(L+1)) - 1 exceeds X P(b) at b = K log_3 X for K = 2
  once k >= 5 (prints the margins; the proved bound is asymptotic, the data show the excess at D = 10), illustrating the failure of E_F.
Exits 1 on failure."""
import sys, itertools
from fractions import Fraction
from math import comb, log
from ffmap import load_spec, survivors_exact, step_law

fail = []
A3 = load_spec('specs/A3.txt'); Q4b = load_spec('specs/Q4b.txt')
P = survivors_exact(A3, 300)
for b in range(301):
    if P[b] ** 2 > Fraction(8, 9) ** b:
        fail.append(('A3 chernoff', b))
P4 = survivors_exact(Q4b, 300)
for b in range(301):
    if P4[b] ** 3 > Fraction(243, 256) ** b:
        fail.append(('Q4b chernoff', b))
for S, form in ((A3, comb(6, 3) * 2 ** 3), (Q4b, comb(6, 2) * 3 ** 4)):
    law = step_law(S)
    nb = len(law)
    cnt = sum(1 for w in itertools.product(range(nb), repeat=6) if sum(law[i][1] for i in w) == 0)
    if cnt != form:
        fail.append(('W_6 count', cnt, form))
for N in range(1, 400):
    if comb(2 * N, N) * (2 * N + 1) < 4 ** N:
        fail.append(('binomial', N))
for k in range(1, 7):
    L = 2 * 3 ** k
    lower = comb(L, L // 2) * 2 ** (L // 2) // (L * (L + 1)) - 1
    logX = L + 2
    b = 2 * logX
    # X P(b) <= 3^logX (8/9)^(b/2)
    upper_log3 = logX + (b / 2) * log(8 / 9, 3)
    print(f'k={k} L={L}: never-dropping lower bound 3^{log(lower, 3) if lower > 0 else float("-inf"):.2f}, '
          f'X P(2 log X) <= 3^{upper_log3:.2f}')
    if k >= 5 and log(lower, 3) <= upper_log3:
        fail.append(('margin', k))
if fail:
    print('FAIL', fail[:5]); sys.exit(1)
print('Theorem A checks passed')
