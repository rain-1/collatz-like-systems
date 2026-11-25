# m3_d_s7

Rule: 3|n -> n/3; n≡1 (mod 3) -> 4n+2; n≡2 (mod 3) -> 4n+1. Seed 7.
The image of a non-divisible n is always ≡0 (mod 3), so the two-step map is 3k+1 → 4k+2, 3k+2 → 4k+3, plus 3k → k.

| Question | Answer | Status | Tier |
|---|---|---|---|
| FATE | returns to seed (period 16) | PROVED | 0 |
| GLOBAL | unknown (conjecturally yes) | OPEN | 5 |

**Fate.** 7 → 30 → 10 → 42 → 14 → 57 → 19 → 78 → 26 → 105 → 35 → 141 → 47 → 189 → 63 → 21 → 7.

**Global: what was tried.**
- Simulation: every n < 2·10^5 reaches one of two cycles, {1,6,2,9,3} or the 16-cycle through 7.
- Heuristic drift: (2/3)log(4/3) − (1/3)log 3 ≈ −0.175 per accelerated step, which predicts convergence.
- Descent plus a finite table fails. The branch n ↦ (4n+1)/3 fixes −1 3-adically, so n = 3^j − 1 climbs
  for j accelerated steps. No finite set of residue classes certifies descent.
- No congruence invariant, automaton or conjugacy found.

This is a generic Collatz-type map of 3x+1 shape. The global question is OPEN, with no reduction to a solved case.

Check: `census/checks/m3_d_s7.py`.

## Referee

FATE confirmed, tier 0: I reproduced the 16-cycle through 7 with a separate implementation. GLOBAL open-agreed, tier 5.
The accelerated map is n/3 if 3|n and ceil(4n/3) otherwise. The ceil(4n/3) branch is a Mahler/Z-number-type step. I checked the obstruction: -1 is fixed by (4n+1)/3, so no finite descent table exists. A separate search over all n<3·10^6 finds exactly the two cycles, min 1 (length 5) and min 7 (length 16). The longest orbit has 372 steps, and excursions reach about 2^20·n. I found no invariant or conjugacy.
