# split5_3_s27

Rule: even n -> n/2; n=1 mod 4 -> 5n+3; n=3 mod 4 -> n+3. Seed 27.

| question | answer | status | tier |
|---|---|---|---|
| FATE | enters another cycle: 27 -> 30 -> 15 -> 18 -> 9 -> 48 -> 24 -> 12 -> 6, then the cycle 6 -> 3 -> 6 (preperiod 8, period 2) | PROVED | 0 |
| GLOBAL | unknown (expected yes) | OPEN | 5 |

## FATE
Exact simulation. 27 is not on the cycle {3,6}.

## GLOBAL: what was tried
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
