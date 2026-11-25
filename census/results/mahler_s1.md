# mahler_s1

Rule: n even -> 3n/2; n odd -> (3n+1)/2. In other words, f(n) = ceil(3n/2). Seed 1.

| Question | Answer | Status | Tier |
|---|---|---|---|
| FATE | infinite (1, 2, 3, 5, 8, 12, 18, 27, 41, ...) | PROVED | 1 |
| GLOBAL | no: no positive orbit is eventually periodic | PROVED | 1 |

## Proof
For n >= 1, f(n) = ceil(3n/2) >= 3n/2 > n. Every positive orbit is therefore strictly increasing, so all its terms are distinct and it is never eventually periodic. This covers the seed 1 in particular.

Monotonicity is all that is needed. The parity sequence of this orbit is linked to Mahler's 3/2 problem (Z-numbers), which is open, but neither question here depends on it.

## Referee
Verdict: FATE confirmed (tier 1), GLOBAL confirmed (tier 1). The argument proves infinitude by strict monotonicity or an invariant (non-divisibility is preserved by the multiplier), not by simulation, and it holds for every n >= 1. No check script existed, so I verified it myself: the orbit formula holds for 60 steps and the step increases every n < 10^5 (for mahler).
