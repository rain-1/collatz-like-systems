# par_5_1_s7
Rule: even n -> n/2; odd n -> 5n+1. Seed 7.

| question | answer | status | tier |
|---|---|---|---|
| FATE | unknown (apparently infinite) | OPEN | 5 |
| GLOBAL | unknown (conjectured NO) | OPEN | 5 |

## FATE (OPEN; this is the famous open question "does 7 diverge under 5x+1?")
7 -> 36 -> 18 -> 9 -> 46 -> 23 -> ... ; after 20000 steps the value has 2134 bits and no repeat occurred
(`checks/par_5_1_s7.py`). This is evidence only. The heuristic drift is positive (each odd step
multiplies by ~5, followed on average by 2 halvings: log2 5 - 2 > 0), but a proof of divergence would need
control of the 2-adic parity sequence of one specific orbit, which no known tool (congruence invariants,
finite automata, descent tables) provides; a proof that it cycles is impossible by simulation unless it
actually cycles. Note: the same orbit underlies par_5_3_s27 (3 x orbit of 9) and par_5_5_s27 (5 x orbit of 28 -> 14 -> 7).

## GLOBAL: as par_5_1_s5 — the 5x+1 problem, OPEN. A proof that 7 diverges would settle it as NO.

## Referee
FATE: open-agreed, tier 5. The script only simulates (2134 bits after 20000 steps), correctly presented as evidence, not proof. Divergence of 7 under 5x+1 is a known open problem; congruence/automaton arguments cannot control the parity sequence of one orbit. GLOBAL: open-agreed, tier 5.
