# split_5_s27

Rule: even n -> n/2; n=1 mod 4 -> 3n+5; n=3 mod 4 -> n+5. Seed 27.

| question | answer | status | tier |
|---|---|---|---|
| FATE | enters another cycle (preperiod 3, period 4, seed not in cycle) | PROVED | 0 |
| GLOBAL | yes: every positive orbit is eventually periodic; exactly 2 cycles, min elements [1, 5] | PROVED | 1 |

## FATE
Exact simulation: 27 reaches the cycle 8 -> 4 -> 2 -> 1 after 3 steps; 27 is not on it.

## GLOBAL (proof)
Let d = 5. For odd n the image is divisible by 4:
- n = 1 mod 4: 3n+5 = 3+1 = 0 mod 4 (d = 1 mod 4);
- n = 3 mod 4: n+5 = 3+1 = 0 mod 4.

So define the block map g(n) = n/2 (n even), g(n) = f(n)/4 (n odd; this is f applied 3 times).
Since both odd branches are at most 3n+d, g(n) <= (3n+d)/4 for odd n.
- If n > d: g(n) < n (even: n/2 < n; odd: (3n+d)/4 < n iff n > d).
- If n <= d: g(n) <= max(n/2, (3d+d)/4) <= d, and g(n) >= 1.

Hence the g-orbit of any n >= 1 strictly decreases until it enters [1, d] and then stays there.
The f-orbit visits only g-orbit points and their intermediate images f(n), f(n)/2 (all <= 4·max),
so it lives in a finite set and is eventually periodic. Every cycle meets [1, d], so enumerating
starts 1..d lists all cycles: min elements [1, 5].
Tier 1: a valuation (v2 >= 2) observation plus a linear descent inequality; the finite table is only
used to list the cycles, not to prove periodicity.

Check: census/checks/split_5_s27.py (verifies the residues, the descent on a window, the g-invariance of
[1, d] exhaustively, the cycle list, and the seed fate).

## Which cycle does each start reach?

The complete basin rule is divisibility by 5. Every positive multiple of 5 reaches
$5\to20\to10\to5$. Every other positive integer reaches $1\to8\to4\to2\to1$.
Indeed, modulo 5 the two odd branches act by multiplication by 3 and by 1,
and halving an even integer acts by the inverse of 2. Each multiplier is a
unit, so $5\mid T(n)$ if and only if $5\mid n$. The descent above forces every
orbit into one of the two cycles, and exactly one cycle has each divisibility type.

## Referee

Verdict: FATE confirmed (tier 0), GLOBAL confirmed (tier 1).
I re-derived the argument myself. Both odd images are 0 mod 4 (this is an exact residue identity). The block
map satisfies g(n) <= (3n+d)/4, which is < n for every n > d (no exceptions at small n), and g maps [1,d]
into itself. So every orbit lies in a finite set. The argument does not assume injectivity, and it does not
need the cycle enumeration to answer "yes"; the enumeration over [1,d] is complete only because every cycle
meets [1,d]. I re-ran the check script (PASS) and also spot-checked the residue and descent identity on
random 30-digit odd n.
