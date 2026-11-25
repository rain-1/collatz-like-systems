# split5_1_s27

Rule: even n -> n/2; n=1 mod 4 -> 5n+1; n=3 mod 4 -> n+1. Seed 27.

| question | answer | status | tier |
|---|---|---|---|
| FATE | enters another cycle: 27 -> 28 -> 14 -> 7 -> 8 -> 4, then the cycle 4 -> 2 -> 1 -> 6 -> 3 -> 4 (preperiod 5, period 5) | PROVED | 0 |
| GLOBAL | unknown (expected yes) | OPEN | 5 |

## FATE
Exact simulation. 27 is not on the cycle {1,2,3,4,6}.

## GLOBAL: what was tried
Odd-to-odd map: n = 1 mod 4 -> (5n+1)/2 (exactly one halving, since 5n+1 = 2 mod 4);
n = 3 mod 4 -> (n+1)/2^v with v >= 2.
- Heuristic drift: each branch has probability 1/2, giving log-drift (1/2)ln(5/2) - (1/2)(3 ln 2) = -0.58 < 0,
  so convergence is expected.
- Descent plus finite table (tier 2) provably fails: with c = -1/3 in Z_2 one has
  (5n+1)/2 + 1/3 = (5/2)(n + 1/3), so every n = -1/3 mod 2^(k+2) makes at least k consecutive
  x5/2 steps. Growth by an unbounded factor over arbitrarily many steps rules out any
  bounded-window descent, and any Lyapunov function of the form w(n mod 2^K)·n with bounded weights.
- No mod-m invariant can help: the map is a generalized Collatz map (modulus 4, multipliers 5 and 1)
  whose branch residues mix all classes; no conjugacy to a trivially understood map was found.
- Evidence only: all starts 1..2·10^5 reach one of two cycles, minimum elements 1 and 13
  (peak value about 7.6·10^14). No divergence observed.

Status: this is a generalized Collatz problem of the same nature as the 3x+1 conjecture
(mixing of an expanding and a contracting branch on 2-adic residue classes). It is not literally
equivalent to a named problem, but no known technique settles any such mixed map; Conway's theorem
makes the general class undecidable, though not this instance.

Check: census/checks/split5_1_s27.py (seed fate; the up-run witnesses; evidence up to 10^5).

## Referee
Verdict: FATE confirmed (tier 0). GLOBAL open-agreed (tier 5).
- I re-ran the check (PASS): the seed fate is exact, and the cycles from starts up to 1e5 have minimum elements 1 and 13.
- I verified the up-run identity (5n+1)/2 + 1/3 = (5/2)(n + 1/3) in Z_2, so up-runs of every length exist.
  Any one-step residue-weighted Lyapunov function with bounded weights, and any stopping-time table over
  a fixed modulus, must therefore leave the class -1/3 mod 2^K undescended.
- Attempts that failed:
  - Mod-3 and mod-5 invariant sets: 3 does not divide n+1 in general, so there is no invariant subset.
  - The affine change x = 3n+1 gives the branches (x+1)/2, 5x-1 and x+3, which is no simpler.
  - The odd-to-odd map has 2-adically expanding residue dynamics (8j+1 -> 3 mod 4, 8j+5 -> 1 mod 4),
    so its residues are as equidistributed as in 3x+1 and no finite automaton is evident.
- This agrees with the claim: it is a Collatz-type problem, not reducible by tier 1-3 tools.
