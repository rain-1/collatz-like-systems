# perm_1932inv_s8

Rule (T^{-1}, inverse of the 1932 permutation): 2q -> 3q; 4q+1 -> 3q+1; 4q+3 -> 3q+2. Seed 8.

| question | answer | status | tier |
|---|---|---|---|
| FATE | unknown (returns or infinite) | OPEN | 5 |
| GLOBAL | unknown | OPEN | 5 |

**Common facts (tier 1).** (i) The map is a bijection of the positive integers: each residue-class branch is an increasing affine bijection from its class onto one target class, and the target classes partition Z_{>0} (checked algebraically; spot-checked against an explicit inverse in the check script). (ii) For an injective map, fate (b) is impossible: if the orbit of x first meets a cycle C at y=T^k(x) with k>=1 and x not in C, then y has two distinct preimages (T^{k-1}(x) and its predecessor in C). So FATE is "returns" or "infinite". (iii) For a bijection, "every orbit eventually periodic" means "every orbit is a finite cycle".

**Reduction (tier 1).** The map is exactly T^{-1} (compose branches: T(3q)=2q, T(3q+1)=4q+1, T(3q+2)=4q+3). For a bijection the forward orbit of x is a finite cycle iff the backward orbit is the same finite cycle. Hence FATE here is *equivalent* to the 1932 orbit-of-8 problem, and GLOBAL is equivalent to GLOBAL for T (same orbits as sets).

**FATE (OPEN, tier 5).** Equivalent to Collatz's 1932 question. Tried: simulation (no return in 1e5 steps, ~8800 bits); drift (1/2)log(9/8) > 0; periodic congruence separators for seed 8 under T^{-1}: none for M <= 150 (checks/perm_1932inv_s8.py). Same obstacles as perm_1932_s8.

**GLOBAL (OPEN, tier 5).** Same as for T.

Check: checks/perm_1932inv_s8.py (exit 0).

## Referee

Independently re-checked against the catalog step functions (systems.py), not only the check script's own re-implementation: mutual inverses on 1..3e5 for T/T^{-1} and S/S^{-1}, B(n)=T(n+1)-1 on 1..3e5, S(5y)=5T(y) on 1..3e5, D injective on 1..8e4 with image covering 1..4e4. Bijectivity is re-derived by hand: the branch images are disjoint residue classes covering Z_{>0} (for D: 5Z from evens, 5q+1..5q+4 from odds). The injectivity argument ruling out fate (b) is correct.

Verdict: FATE open-agreed (tier 5), GLOBAL open-agreed (tier 5). The branches were inverted by hand and match T^{-1}. Under a bijection, x is periodic for T exactly when it is periodic for T^{-1}, so FATE is equivalent to the 1932 problem. Backward drift (1/2)log(9/8) re-derived.
