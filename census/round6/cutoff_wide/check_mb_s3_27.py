"""The blocked mixed-base system mb_s3_27 (round3/mixedbase):
    n = 26 (mod 27) -> (n+1)/27;  else n even -> n/2;  else (3n+1)/2.

Exact checks for Proposition B (theorem_P.md):
  (1) Skew-product lemma.  On n != 26 (mod 27) the map is the Terras map, and
      T(n) mod 27 is a function f(n mod 27, n mod 2).  Checked on all residues
      mod 54.
  (2) Hence a Terras parity word b_0..b_{L-1} and an initial residue s mod 27 whose
      f-path avoids 26 are followed by every integer in one class mod 2^L*27
      (CRT of the Terras class and s).  Checked by direct iteration on lifts.
  (3) Code: C = parity word 110 (the cycle -5,-7,-10, residues 22,20,17), a
      re-entry word W from state 22 back to 22 avoiding 26 that is not a power
      of C, W' = W^3, U = C^D W', V = C^(D+|W'|/3), with every prefix slope of U,
      V exceeding 1.  Every word in {U,V}^* then has all prefix slopes > 1 and
      avoids 26, so the non-descending set (slope sense) contains 2^n disjoint
      cylinders of 2-adic depth n|U| (with the fixed 27-class): positive entropy.
  (4) Rigid cutoff instance (Theorem W with primes {2,3}): the near-critical
      family C^{k_1} W0 C^{k_2} W0 ... with W0 a contracting re-entry word, exact
      whole-prefix identity on an actual orbit, and lift ratios (EVIDENCE).
  (5) Exact counts of non-descending, never-blocked words (lower bound for the
      non-descending count), and their growth (EVIDENCE).
Exits 0 iff all assertions hold.
"""
import sys
import random
from fractions import Fraction as F
from math import log
from decimal import Decimal, getcontext

getcontext().prec = 80
random.seed(2)
FAIL = []


def claim(name, cond):
    if not cond:
        FAIL.append(name)
        print('FAIL', name)


def T(n):
    if n % 27 == 26:
        return (n + 1) // 27
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2


INV2 = pow(2, -1, 27)


def f(s, b):
    return (s * INV2) % 27 if b == 0 else ((3 * s + 1) * INV2) % 27


# (1)
ok = True
for r in range(54 * 27):
    for t in range(3):
        n = r + 54 * 27 * t + 1000
        if n % 27 == 26:
            continue
        ok &= (T(n) % 27 == f(n % 27, n % 2))
claim('skew product lemma', ok)


def terras_class(bits):
    """residue mod 2^L of the Terras parity word (exact, by the bijection)."""
    # build n mod 2^j step by step: n = rho + 2^j z, track T^j(n) = (3^a n + B)/2^j
    rho, a, B = 0, 0, 0
    for j, b in enumerate(bits):
        # value (3^a n + B)/2^j mod 2 must equal b; n = rho + 2^j z
        val = (3 ** a * rho + B) >> j  # integer since 2^j | 3^a rho + B
        assert (3 ** a * rho + B) % (2 ** j) == 0
        if val % 2 != b:
            rho += 2 ** j  # flips the parity because 3^a is odd
        # apply step
        if b == 1:
            a, B = a + 1, 3 * B + 2 ** j
        # division by 2 is accounted by j increment
    return rho % 2 ** len(bits)


def word_class(bits, s0):
    L_ = len(bits)
    r2 = terras_class(bits)
    M2 = 2 ** L_
    # CRT with s0 mod 27
    n = (r2 + M2 * (((s0 - r2) * pow(M2, -1, 27)) % 27)) % (M2 * 27)
    return n, M2 * 27


def fpath_ok(bits, s0):
    s = s0
    for b in bits:
        if s == 26:
            return False, s
        s = f(s, b)
    return s != 26, s


def follows(n, bits):
    for b in bits:
        if n % 27 == 26 or n % 2 != b:
            return False
        n = T(n)
    return True


def prefix_slopes(bits):
    out, s = [], F(1)
    for b in bits:
        s *= F(3, 2) if b else F(1, 2)
        out.append(s)
    return out


C = [1, 1, 0]
claim('C cycle', fpath_ok(C, 22) == (True, 22) and follows(-5 + 27 * 2 ** 40 * 0, C) is not None)
claim('-5 is a cycle of T', T(T(T(-5))) == -5 and [T(-5), T(T(-5))] == [-7, -10])

# (2) random words
ok = True
for _ in range(200):
    L_ = random.randint(1, 40)
    bits = [random.randint(0, 1) for _ in range(L_)]
    s0 = random.randrange(27)
    good, _s = fpath_ok(bits, s0)
    if not good:
        continue
    n, M = word_class(bits, s0)
    for t in range(3):
        ok &= follows(n + M * t + M, bits)
claim('CRT class follows word', ok)

# (3) find W: BFS over parity words from state 22 back to 22, avoiding 26
best = None
for Lw in range(1, 16):
    for x in range(2 ** Lw):
        bits = [(x >> i) & 1 for i in range(Lw)]
        if Lw % 3 == 0 and bits == C * (Lw // 3):
            continue
        good, s = fpath_ok(bits, 22)
        if good and s == 22:
            best = bits
            break
    if best:
        break
W = best
claim('re-entry word found', W is not None)
Wp = W * 3
D = 0
while True:
    U = C * D + Wp
    V = C * (D + len(Wp) // 3)
    if all(s > 1 for s in prefix_slopes(U)) and all(s > 1 for s in prefix_slopes(V)):
        break
    D += 1
claim('U != V', U != V and len(U) == len(V))
claim('U,V avoid 26 and return to 22', fpath_ok(U, 22) == (True, 22) and fpath_ok(V, 22) == (True, 22))
ok = True
for _ in range(20):
    word = []
    for _ in range(5):
        word += random.choice([U, V])
    n, M = word_class(word, 22)
    ok &= follows(n + M, word) and all(s > 1 for s in prefix_slopes(word))
claim('concatenations realized and non-descending', ok)
eU, eV = len(U), len(V)  # one halving per Terras step
# Revision after REFEREE1 (section 11): the dimension bound holds inside each
# class s != 26 (mod 27), not inside class 26, which is blocked at once.  For
# each s != 26 find a parity word P from s to 22 that avoids 26 and has all
# prefix slopes > 1; then P {U,V}^omega is realized inside class s (CRT), and
# the dimension of that set equals that of {U,V}^omega (P only rescales).
from collections import deque
def entry_word(s0, maxlen=40):
    # BFS over (state, 3-exponent minus 2-exponent kept as slope); slopes > 1
    dq, seen = deque([(s0, F(1), [])]), set()
    while dq:
        s, sl, w = dq.popleft()
        if s == 22 and w:
            return w
        if s == 22 and not w:
            return []
        if len(w) >= maxlen:
            continue
        for b in (1, 0):
            if s == 26:
                continue
            t = f(s, b)
            sl2 = sl * (F(3, 2) if b else F(1, 2))
            if t == 26 or sl2 <= 1:
                continue
            key = (t, min(sl2, F(2 ** 8)))  # slopes >= 2^8 are interchangeable here
            if key in seen:
                continue
            seen.add(key)
            dq.append((t, sl2, w + [b]))
    return None
ok_entry = True
maxP = 0
for s0 in range(27):
    if s0 % 3 == 2:
        continue
    P = entry_word(s0)
    if P is None:
        ok_entry = False
        print('no entry word from', s0)
        continue
    maxP = max(maxP, len(P))
    good = fpath_ok(P, s0) == (True, 22) and all(x > 1 for x in prefix_slopes(P))
    # realized by an integer in class s0 that then follows U V U
    w = P + U + V + U
    n, Mod = word_class(w, s0)
    n += Mod * 7
    good &= n % 27 == s0 and follows(n, w)
    ok_entry &= good
claim('every class s = 0, 1 (mod 3) enters the code with slopes > 1', ok_entry)
# The referee's "every class s != 26" is too generous: the 9 classes
# s = 2 (mod 3) contain no point whose prefix slopes stay >= 1 for 3 steps.
# Odd steps keep s = 2 (mod 3) and reach 26 after at most 2 of them, an even
# step costs 1/2, a blocked step costs 1/27.  Exhaustive over the state s and
# the 3 parity bits (all realized by CRT; the blocked step overrides parity).
ok_desc = True
for s0 in range(2, 27, 3):
    for bits in range(8):
        s, sl, dead = s0, F(1), False
        for j in range(3):
            if s == 26:
                sl /= 27
            elif (bits >> j) & 1:
                sl *= F(3, 2)
                s = f(s, 1)
            else:
                sl *= F(1, 2)
                s = f(s, 0)
            if sl < 1:
                dead = True
                break
            if s == 26 and j == 2:
                pass
        ok_desc &= dead
claim('classes s = 2 (mod 3): a prefix slope < 1 within 3 steps', ok_desc)
# direct integer confirmation on a range
okd = True
for n in range(-30000, 30000):
    if n % 27 % 3 != 2:
        continue
    m, sl, dead = n, F(1), False
    for j in range(3):
        sl *= F(1, 27) if m % 27 == 26 else (F(3, 2) if m % 2 else F(1, 2))
        m = T(m)
        if sl < 1:
            dead = True
            break
    okd &= dead
claim('classes s = 2 (mod 3), direct integers |n| < 30000', okd)
print('entry words from every s = 0, 1 (mod 3) to state 22: found, max length', maxP)
print('classes s = 2 (mod 3), 26 included: every point has a prefix slope < 1 within 3 steps')

print('mb_s3_27: W =', ''.join(map(str, W)), ' D =', D, ' |U| = |V| =', len(U),
      ' dimension lower bound (2-adic) >= 1/%d = %.5f' % (len(U), 1 / len(U)))

# (4) rigid instance: contracting re-entry W0
cand = None
for Lw in range(1, 16):
    for x in range(2 ** Lw):
        bits = [(x >> i) & 1 for i in range(Lw)]
        if Lw % 3 == 0 and bits == C * (Lw // 3):
            continue
        good, s = fpath_ok(bits, 22)
        sl = prefix_slopes(bits)[-1]
        if good and s == 22 and sl < 1:
            cand = bits
            break
    if cand:
        break
W0 = cand
lamC, lamW = F(9, 8), prefix_slopes(W0)[-1]


def dlog(x):
    return Decimal(x.numerator).ln() - Decimal(x.denominator).ln()


kappa = -dlog(lamW) / dlog(lamC)


def sched(e):
    return [0] + [int((kappa * i).to_integral_value(rounding='ROUND_FLOOR')) + 1 for i in range(1, e + 1)]


def affine_bits(bits):
    A, B, Dd = 1, 0, 1
    for b in bits:
        if b:
            A, B, Dd = 3 * A, 3 * B + Dd, 2 * Dd
        else:
            Dd = 2 * Dd
    return lambda x: (A * x + B) / F(Dd)


TC, TW = affine_bits(C), affine_bits(W0)
xs = F(-5)
cW = TW(xs) - xs
claim('shifted C', TC(xs) == xs and TC(xs + 1) - xs == lamC)
claim('shifted W0', TW(xs + 1) - TW(xs) == lamW and cW != 0)
e = 60
Ks = sched(e)
word = []
for i in range(1, e + 1):
    word += C * (Ks[i] - Ks[i - 1]) + W0
claim('rigid word avoids 26', fpath_ok(word, 22)[0])
n, M = word_class(word, 22)
n += M
claim('integer follows rigid word', follows(n, word))
cur = n
for b in word:
    cur = T(cur)
P, taus, Ps = F(1), [], []
for i in range(1, e + 1):
    P *= lamC ** (Ks[i] - Ks[i - 1]) * lamW
    Ps.append(P)
    taus.append(cW / P)
claim('whole-prefix identity (mb_s3_27)', (F(n) - xs) + sum(taus) == (F(cur) - xs) / Ps[-1])
claim('prefix slopes >= 1', all(x >= 1 for x in Ps))
rat = []
for ee in (100, 200, 300):
    Ks = sched(ee)
    wd = []
    for i in range(1, ee + 1):
        wd += C * (Ks[i] - Ks[i - 1]) + W0
    n, M = word_class(wd, 22)
    h = len(wd)
    rp = log(n if n > 0 else n + M) / (h * log(2))
    rn = log(M - n) / (h * log(2))
    rat.append((ee, h, round(rp, 4), round(rn, 4)))
    claim('lift ratio', min(rp, rn) > 0.8)
print('rigid family: W0 =', ''.join(map(str, W0)), 'lambda_W0 =', lamW, 'kappa = %.5f' % float(kappa))
print('lift ratios log2|y|/h (e, h, pos, neg):', rat)

# (5) counts of never-blocked non-descending words: state (s, a) at depth j
layer = {(s, 0): 1 for s in range(27) if s != 26}
Ns = []
for j in range(1, 241):
    nxt = {}
    for (s, a), c in layer.items():
        for b in (0, 1):
            s2 = f(s, b)
            a2 = a + b
            if 3 ** a2 < 2 ** j:
                continue
            if s2 == 26:
                continue
            nxt[(s2, a2)] = nxt.get((s2, a2), 0) + c
    layer = nxt
    Ns.append(sum(layer.values()))
H = (log(Ns[239]) - log(Ns[119])) / (120 * log(2))
print('never-blocked non-descending words: N(120) = %.3e, N(240) = %.3e, growth exponent ~ %.4f'
      % (Ns[119], Ns[239], H))
claim('positive growth', Ns[239] > 2 ** 60 and Ns[239] > Ns[119] ** 1.5)

if FAIL:
    print('FAILURES', FAIL)
    sys.exit(1)
print('all checks passed')
