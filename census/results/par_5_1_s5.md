# par_5_1_s5
Rule: even n -> n/2; odd n -> 5n+1. Seed 5.

| question | answer | status | tier |
|---|---|---|---|
| FATE | other cycle {13,66,33,166,83,416,208,104,52,26}, preperiod 1, period 10 | PROVED | 0 |
| GLOBAL | unknown (conjectured NO: orbit of 7 believed divergent) | OPEN | 5 |

## FATE (tier 0)
5 -> 26 -> 13 -> 66 -> 33 -> 166 -> 83 -> 416 -> 208 -> 104 -> 52 -> 26. Seed 5 not on the cycle.
Check: `checks/par_5_1_s5.py`.

## GLOBAL (OPEN)
This is the 5x+1 problem. Heuristically (expected log-growth per odd step log2(5) - 2 > 0) almost all
orbits diverge, so the expected answer is "no", but proving it requires exhibiting one provably
divergent orbit (e.g. 7), which is a well-known open problem; no integer is known to provably diverge.
Showing "yes" is also not possible by any known method. See par_5_1_s7.

## Referee
FATE: confirmed, tier 0 (independent re-simulation: 5 -> 26, then 10-cycle with minimum 13). GLOBAL: open-agreed, tier 5. This is literally the 5x+1 problem; NO would need a provably divergent orbit (none known), YES is believed false.
