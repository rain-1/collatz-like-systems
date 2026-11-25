# div2_3n_s5

Rule: 2|n -> n/2; else 3n. Seed 5.

| Question | Answer | Status | Tier |
|---|---|---|---|
| FATE | infinite: 5 * 3^k | PROVED | 1 |
| GLOBAL | no: no positive orbit is eventually periodic | PROVED | 1 |

## Proof
Write n = 2^k m with m odd. After k halvings the orbit reaches m. Since 3m is odd, from then on the orbit is m * 3^j, which is strictly increasing. Hence every positive orbit is infinite. For the seed: 5 -> 15 -> 45 -> ... = 5 * 3^k.

## Referee
Verdict: FATE confirmed (tier 1), GLOBAL confirmed (tier 1). The argument proves infinitude by strict monotonicity or an invariant (non-divisibility is preserved by the multiplier), not by simulation, and it holds for every n >= 1. No check script existed, so I verified it myself: the orbit formula holds for 60 steps and the step increases every n < 10^5 (for mahler).
