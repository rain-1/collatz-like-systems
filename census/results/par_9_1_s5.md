# par_9_1_s5
Rule: even n -> n/2; odd n -> 9n+1. Seed 5.

## FATE: unknown — OPEN (tier 5)
Note 1 -> 10 -> 5, so this is also the orbit of 1.
Tried:
- Simulation: 200000 steps, no repetition (strict record at step 199998, so preperiod + period >
  199998); size 79200 bits, matching the random-parity rate (1/3 log2 9 - 2/3 ~ 0.39 bits/step).
  Evidence only.
- Congruence separators: for every modulus M <= 3000 the forward closure of T(5) = 46 mod M in the
  residue graph contains 5 mod M. Mod 3 and mod 9 the odd step lands in 1 and halving (inverse 2 is
  a generator of the units mod 9) spreads over all units, so the quadratic-residue trick that works
  for 7n+1 (2 a square mod 7) fails here.
- No scaling conjugacy (gcd(5,1)=1 trivially; d = 1).
Reduces to: proving a specific 9n+1 orbit unbounded (or finding its cycle) — the same open type
as 5n+1 divergence. No named equivalence.
Check (evidence only): census/checks/par_9_1_s5.py.

## GLOBAL: unknown — OPEN (tier 5)
Every 9n+1 orbit eventually periodic? Open; heuristically false (log 9 - 2 log 2 > 0 per odd step,
and the orbit of 1 itself appears to diverge). No descent, invariant or automaton argument can give
"yes" against positive drift, and no divergence proof exists for "no".

## Referee
FATE: open-agreed (tier 5). Re-ran the check and an independent simulation (own step function, cross-checked against systems.get on n<5000). Reproduced 200000 steps without repetition, 79200 bits. Independent separator search over moduli 2..800 finds none. This agrees with the structural reason: the odd step gives 1 mod 9, halving multiplies by 5 = 2^{-1}, which generates (Z/9)^*, so every unit residue is reached. 1 -> 10 -> 5, so this is the 9n+1 orbit of 1. GLOBAL: open-agreed (tier 5). Positive drift (log 9 - 2 log 2 > 0) rules out descent, and 'no' needs a proved divergent orbit.
