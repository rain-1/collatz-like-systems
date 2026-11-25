# m3_g_s7

Rule: 3|n -> n/3; n≡1 (mod 3) -> 5n+1; n≡2 (mod 3) -> 5n+2. Seed 7.
The image of a non-divisible n is ≡0 (mod 3), so the accelerated map is 3k+1 → 5k+2, 3k+2 → 5k+4, 3k → k.

| Question | Answer | Status | Tier |
|---|---|---|---|
| FATE | returns to seed (period 5) | PROVED | 0 |
| GLOBAL | unknown (conjecturally yes) | OPEN | 5 |

**Fate.** 7 → 36 → 12 → 4 → 21 → 7.

**Global: what was tried.**
- Simulation: every n < 2·10^5 reaches one of two cycles, {4,21,7,36,12} or {8,42,14,72,24}.
  The second is twice the first. That follows because f(2n) = 2f(n) whenever n ≢ 2 (mod 3), but it is not a
  global symmetry.
- Heuristic drift: (2/3)log(5/3) − (1/3)log 3 ≈ −0.026 per accelerated step. This is only barely contracting,
  so long excursions are expected (the baseline's step budget missed one small start for this reason).
- Descent plus a finite table fails. −1 is a 3-adic fixed point of n ↦ (5n+2)/3, so n = 3^j − 1 climbs for
  j steps.
- No invariant or conjugacy found.

Generic Collatz-type map, same shape as 3x+1. OPEN.

Check: `census/checks/m3_g_s7.py`.

## Referee

FATE confirmed, tier 0: I reproduced 7→36→12→4→21→7. GLOBAL open-agreed, tier 5.
The accelerated map is n/3 or ceil(5n/3). The drift of (2/3)ln(5/3)−(1/3)ln3 ≈ −0.026 is correct. A separate search over all n<3·10^6 finds only the cycles with min 4 and min 8. That search is weak evidence. Orbits run up to 19427 steps (n=2338156), and excursions reach about 2^184·n, as expected for drift this close to zero. The 3-adic fixed point −1 of (5n+2)/3 rules out a finite descent table. Because the drift is so close to zero, I would not be surprised by an unknown cycle or by a very slow orbit above 3·10^6. "Conjecturally yes" is plausible but held with less confidence than for m3_b and m3_d.
