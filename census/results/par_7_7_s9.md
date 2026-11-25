# par_7_7_s9
Rule: even n -> n/2; odd n -> 7n+7. Seed 9.

## FATE: other-cycle — PROVED (tier 0; tier 1 explanation)
Simulation: 9 -> 70 -> 35 -> 252 -> 126 -> 63 -> 448 -> 224 -> 112 -> 56 -> 28 -> 14 -> 7 -> 56.
Preperiod 9, period 4, cycle {7, 56, 28, 14}, not containing 9.
Structure: 7n+7 = 7(n+1), and T(7m) = 7*U(m) where U is the 7n+1 map; 70 = 7*10 and the U-orbit of
10 is 10 -> 5 -> 36 -> 18 -> 9 -> 64 -> ... -> 1 -> 8 -> 4 -> 2 -> 1, so the T-cycle is 7*{1,8,4,2}.
Check: census/checks/par_7_7_s9.py (exits 0).

## GLOBAL: unknown — OPEN (tier 5); exactly equivalent to GLOBAL for 7n+1 (equivalence tier 1)
Any positive orbit reaches an odd n by halving, then 7(n+1) in 7Z, and 7Z is forward-invariant
(halving preserves 7 | n, odd step gives a multiple of 7). On 7Z, T(7m) = 7 U(m) with U the 7n+1 map.
So "every T-orbit eventually periodic" iff "every 7n+1 orbit eventually periodic", which is open
(see par_7_1_s1 / par_7_1_s3; the 7n+1 orbit of 3, i.e. the T-orbit of 21, appears to diverge).

## Referee
FATE: confirmed (tier 0). Reproduced preperiod 9, cycle {7,56,28,14}. GLOBAL: open-agreed (tier 5). The equivalence is checked and correct (tier 1): every orbit hits an odd n, then 7(n+1) is in 7Z; 7Z is forward-invariant; T(7m)=7U(m) for all m>=1, so the T-orbits on 7Z are exactly 7 times all U-orbits. The question is therefore exactly GLOBAL for 7n+1, which is open.
