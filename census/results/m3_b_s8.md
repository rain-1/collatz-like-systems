# m3_b_s8

Rule: 3|n -> n/3; n≡1 (mod 3) -> (4n-1)/3; n≡2 (mod 3) -> (4n+1)/3. Seed 8.
In terms of k with n=3k+r: 3k → k, 3k+1 → 4k+1, 3k+2 → 4k+3.

| Question | Answer | Status | Tier |
|---|---|---|---|
| FATE | enters another cycle (fixed point 1) | PROVED | 0 |
| GLOBAL | unknown (conjecturally yes) | OPEN | 5 |

**Fate.** 8 → 11 → 15 → 5 → 7 → 9 → 3 → 1 → 1. Direct simulation.

**Global: what was tried.**
- Simulation: every n < 2·10^5 reaches 1. {1} is the only cycle found.
- Heuristic drift: residues mod 3 behave uniformly, so the mean log-growth per step is
  (2/3)log(4/3) − (1/3)log 3 ≈ −0.175 < 0. That predicts convergence, but it is a heuristic, not a proof.
- Descent plus a finite table fails. The expanding branch n ↦ (4n+1)/3 has the 3-adic fixed point −1,
  so n = 3^j − 1 rises for j consecutive steps (3^j−1 → 4·3^(j−1)−1 → …). No modulus 3^j has every class
  descending within a bounded number of steps.
- No mod-m invariant, no automaton and no conjugacy to a solved map was found. f is not odd-symmetric in a
  way that helps (f(−n) = −f(n) holds, but that only relates the positive and negative halves).

This is a generic three-branch Collatz-type map with contracting mean, which is the same shape as the 3x+1 problem.
Proving every orbit cycles would need a method that would also attack 3x+1. Not literally equivalent to Collatz.

Check (evidence + obstruction): `census/checks/m3_b_s8.py`; shared helpers in `census/checks/_m3_common.py`.

## Referee

FATE confirmed, tier 0: I reproduced 8→11→15→5→7→9→3→1 with a separate implementation. GLOBAL open-agreed, tier 5.
I checked the obstruction. -1 is a fixed point of n↦(4n+1)/3, so the 3-adic integer -1 has infinite coefficient stopping time. Any finite descent table, whatever its modulus, therefore has a class it cannot certify. The accelerated branches are n/3 and round(4n/3), with multipliers {1/3, 4/3, 4/3}. No affine conjugacy can send this to a solved map, because the multiplier sets differ.
I ran a separate search over all n<3·10^6. The only cycle is {1}. The longest orbit has 172 steps (n=736642), and the largest excursion is about 2^23·n. That growth is typical of a generic Collatz-type map and gives no sign of an invariant. I agree with the claim: proving GLOBAL needs a method that would also handle 3x+1.
