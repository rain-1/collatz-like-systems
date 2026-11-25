# m3_e_s7

Rule: 3|n -> n/3; n≡1 (mod 3) -> 7n+2; n≡2 (mod 3) -> 7n+1. Seed 7.
Non-divisible images are ≡0 (mod 3), so the accelerated map is 3k+1 → 7k+3, 3k+2 → 7k+5, 3k → k.

| Question | Answer | Status | Tier |
|---|---|---|---|
| FATE | unknown (conjecturally infinite) | OPEN | 5 |
| GLOBAL | unknown (conjecturally no) | OPEN | 5 |

**Evidence.** Known cycles are {1,9,3} and a 14-cycle through 4 (4,30,10,72,24,8,57,19,135,45,15,5,36,12).
The orbit of 7 runs 2·10^5 steps without meeting either cycle and reaches 34528 bits.
That is about 0.173 bits per step.

**Heuristic.** Mean log-growth per accelerated step is (2/3)log(7/3) − (1/3)log 3 ≈ +0.199 nats.
Each accelerated step takes 5/3 raw steps on average, which gives ≈0.172 bits per raw step and matches the
observed rate. So almost all orbits should diverge.

**Why OPEN.** Proving that any particular orbit is infinite would need control of the residue sequence mod 3
along the orbit for all time. That is the same obstruction as the 5x+1 divergence problem (Lagarias), where no
single orbit (e.g. of 7) is proved divergent. No monotone quantity, congruence trap or automaton forces
growth: every residue class mod 3^j contains numbers that descend (3^j·m → m). The same applies to
GLOBAL = "no", which needs one proven divergent orbit. Simulation is evidence, not proof.

Check (evidence only): `census/checks/m3_e_s7.py`.

## Referee

FATE open-agreed, tier 5. GLOBAL open-agreed, tier 5.
I checked the drift: +0.199 nats per accelerated step, or 0.172 bits per raw step. The check script reproduces the 2·10^5-step run (34528 bits, no known cycle hit). The expanding branches (7n+2)/3 and (7n+1)/3 have 3-adic fixed points −1/2 and −1/4. So n=(3^j−1)/2 climbs for j steps, but no positive integer climbs forever.
I tried to build a self-similar divergent family x(m)=α·7^m+β. It fails: for the orbit to move from x(m) to x(m+1), the 3-adic valuation of 7^m−1 would have to keep growing, and by LTE it is only v_3(m)+1. I found no automaton or congruence trap that forces growth. Proving that the orbit of 7 is infinite is of the same type as the open 5x+1 divergence problem. GLOBAL=no would need one orbit proven infinite, so it is equally open.
