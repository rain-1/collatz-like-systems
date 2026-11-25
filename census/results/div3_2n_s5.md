# div3_2n_s5

Rule: 3|n -> n/3; else 2n. Seed 5.

| Question | Answer | Status | Tier |
|---|---|---|---|
| FATE | infinite: 5 * 2^k | PROVED | 1 |
| GLOBAL | no: no positive orbit is eventually periodic | PROVED | 1 |

## Proof
Write n = 3^k m with 3 not dividing m. After k divisions the orbit reaches m. If 3 does not divide m, then 3 does not divide 2m either, so from then on the orbit is m * 2^j for j >= 0, which is strictly increasing and unbounded. Hence every positive orbit is infinite. For the seed: 5 -> 10 -> 20 -> ... = 5 * 2^k.

## Referee
Verdict: FATE confirmed (tier 1), GLOBAL confirmed (tier 1). The argument proves infinitude by strict monotonicity or an invariant (non-divisibility is preserved by the multiplier), not by simulation, and it holds for every n >= 1. No check script existed, so I verified it myself: the orbit formula holds for 60 steps and the step increases every n < 10^5 (for mahler).
