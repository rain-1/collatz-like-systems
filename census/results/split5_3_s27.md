# split5_3_s27

Rule: even n -> n/2; n=1 mod 4 -> 5n+3; n=3 mod 4 -> n+3. Seed 27.

| question | answer | status | tier |
|---|---|---|---|
| FATE | enters another cycle: 27 -> 30 -> 15 -> 18 -> 9 -> 48 -> 24 -> 12 -> 6, then the cycle 6 -> 3 -> 6 (preperiod 8, period 2) | PROVED | 0 |
| GLOBAL | unknown (expected yes) | OPEN | 5 |

## FATE
Exact simulation. 27 is not on the cycle {3,6}.

## What we know about all positive starts

Two questions remain open. Does every positive orbit eventually repeat? If so, are the five cycles with minima $1,3,5,61,125$ the only ones?

**Compressing a whole run identifies the five known cycles.** Set $y=n+3$ and write $y=2^{2k+b}u$ with $u$ odd and $b\in\{0,1\}$. Each expanding block multiplies $y$ by $5/4$. Taking all $k$ such blocks and the following exit gives one exact step

$$
G(y)=2^{b-1}(5^k u+3).
$$

Its fixed-point equation is $u(2\cdot4^k-5^k)=3$. The only solutions with $y\ge4$ are $4,6,8,64,128$, one for each known cycle. Any further cycle would have to visit at least two distinct heights under $G$. [Derivation and fixed-point proof](../round2/rewriting/split5_3_s27.md#one-map-for-whole-expanding-runs)

**Eventual periodicity is equivalent to a single prefix crossing at every start.** To generate the bits, start with $(z,s)=(n+3,0)$ and record the parity of $z$ at each step. On a one, replace $z$ by $(z+3)/2$. On a zero, replace it by $5^s z/2$ and toggle $s$. Write $h_j$ for the number of ones among the first $j$ bits. Then

$$
\text{every positive orbit is eventually periodic}
\quad\Longleftrightarrow\quad
\text{for every integer }y=n+3\ge4,\ \text{some }j\ge1\text{ satisfies }5^{j-h_j}<4^j.
$$

The quantifiers matter. A single crossing measures the linear multiplier and can occur before the height descends. The converse proof shows that on a divergent orbit the cumulative multiplier tends to infinity at run boundaries. Restarting at a boundary where it attains its minimum gives an actual positive start that never crosses. [Proof of both implications](../round2/rewriting/split5_3_s27.md#an-exact-prefix-criterion-for-all-positive-starts)

**The remaining obstruction is arithmetic.** Every length-$m$ parity word specifies one residue modulo $2^m$. For example, positive multiples of $2^m$ begin with $m$ zeros for every $m$, while the *infinite* all-zero word represents only $y=0$. In general every infinite word specifies a unique 2-adic integer. The global proof needs to exclude ordinary integers $y\ge4$ among the words that never cross. The proof excludes words that never cross and begin with $WW$ for arbitrarily long blocks $W$ having an even number of zeros. Repeating $W$ forever gives a nonpositive rational agreeing through $2|W|$ bits. Its numerator and denominator are small enough that a fixed positive integer cannot satisfy these congruences indefinitely. The argument leaves open the case of words without such repetitions. [Inverse series and rational approximation proof](../round2/rewriting/split5_3_s27.md#the-ordinary-integer-obstruction)

**Divisibility by 3 completely classifies the finite-state orbit labels.** Two starts merge if their forward orbits share a value. Every merging class has arbitrarily large members in every arithmetic progression containing an integer of its divisibility type modulo 3. A finite-valued function constant along orbits is computable by a finite automaton reading the digits in some integer base exactly when it depends only on divisibility by 3. In particular, membership in each individual basin through $1,5,61,125$ is nonautomatic in every base. [Progression theorem and automata proof](../round2/rewriting/split5_3_components.md)

The recorded computations certify that every positive $n<2^{66}$ reaches one of the five known cycles. The all-zero prefixes show that the first crossing can come arbitrarily late, so increasing the search depth still leaves infinitely many starts unresolved. [Range certificate and independent checkers](../round2/rewriting/split5_3_s27.md#verification-through-66-bits)

**A restriction at the proposed two-survivor depth.** Set $b=\lceil 2.4m\rceil$. For all sufficiently large $m$, no survivor starting in $[2^m,2^{m+1})$ has half of its first $b$ encoded bits covered by a fixed number of disjoint stretches of sublinear period. The proof bounds the two-adic cancellation in a sum of integers. The number of survivors with more varied bits remains open. [Theorem and proof](../round2/rewriting/split5_3_s27.md#a-restriction-on-survivors-at-the-two-survivor-depth)

## Original census investigation
Odd-to-odd map: n = 1 mod 4 -> (5n+3)/2^v with v >= 2 (5n+3 = 0 mod 4); n = 3 mod 4 -> (n+3)/2
(exactly one halving, since n+3 = 2 mod 4), which decreases n when n > 3.
- Heuristic drift: (1/2)(ln 5 - 3 ln 2) + (1/2)(-ln 2) = -0.58 < 0; convergence expected.
- The only growth is on n = 1 mod 4 with v = 2: n -> (5n+3)/4, i.e. n+3 -> (5/4)(n+3).
  For n = 4^(k+1) - 3 this happens k consecutive times, so the growth factor over a run is unbounded and
  descent plus a finite table (tier 2) provably fails, as does any bounded-weight residue Lyapunov
  function.
- No congruence invariant or conjugacy found; the map mixes residue classes like 3x+1.
- Evidence only: all starts 1..2·10^5 reach one of five cycles, minimum elements 1, 3, 5, 61, 125
  (peak about 4.7·10^6). No divergence observed.

Status: a generalized Collatz problem of the same nature as 3x+1; not literally equivalent to a
named open problem, and no standard tool (descent tables, automata, congruence invariants) applies.

Check: census/checks/split5_3_s27.py (seed fate; the up-run witnesses; evidence up to 10^5).

## Referee
Verdict: FATE confirmed (tier 0). GLOBAL open-agreed (tier 5).
- I re-ran the check (PASS). I verified by hand that n = 4^(k+1)-3 gives n+3 -> 5·4^k with v2 exactly 2
  and the image still 1 mod 4 for k steps, so the up-run witness is correct.
- Observation not in the claim: 3Z is invariant, and so is its complement, because each branch acts on
  n mod 3 as multiplication by 1 or 2. On 3Z the map is conjugate (n = 3m) to m=3 mod 4 -> 5m+1,
  m=1 mod 4 -> m+1, m even -> m/2. That is a Collatz-type map of the same kind (cycle {1,2} <-> {3,6}).
  So the problem splits into two invariant pieces, but neither piece becomes easier: each still mixes an
  expanding x5/4 branch with contracting branches over 2-adic residues.
- No congruence invariant, automaton or conjugacy that settles GLOBAL was found. I agree it is open.
