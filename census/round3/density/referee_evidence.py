"""REFEREE EVIDENCE (floating point / simulation only; proves nothing).
(a) 5x+1: proportion of n in [2^16, 2^17) dropping below n within 20000 steps
    (compare with q ~ 0.8240 and the prover's evidence.out).
(b) 5x+1: D_early proportion on [1, X] for X = 2^17 and X = 1.5 * 2^17
    (non-block endpoint), to illustrate the Theorem 6 partial-block repair.
D_early(n): some tree node of depth <= floor(log2 n) has value < n.  For the
5x+1 Terras tree (one state, F in {1/2, 5/2}) the node values after i digits
are the Terras iterates T^i(n) with T(n) = n/2 or (5n+1)/2.
Runtime: ~1 min.
"""


def terras(n):
    return n // 2 if n % 2 == 0 else (5 * n + 1) // 2


def drops(n, lim=20000):
    x = n
    for _ in range(lim):
        x = x // 2 if x % 2 == 0 else 5 * x + 1
        if x < n:
            return True
    return False


def early(n):
    j = n.bit_length() - 1
    x = n
    for _ in range(j):
        x = terras(x)
        if x < n:
            return True
    return False


lo, hi = 1 << 16, 1 << 17
print("(a) drop proportion [2^16,2^17):", sum(drops(n) for n in range(lo, hi)) / (hi - lo))
cnt = 0
X1, X2 = 1 << 17, 3 << 16
res = {}
for n in range(1, X2 + 1):
    cnt += early(n)
    if n in (X1, X2):
        res[n] = cnt / n
print("(b) D_early proportion up to 2^17: %.5f ; up to 1.5*2^17: %.5f" % (res[X1], res[X2]))
