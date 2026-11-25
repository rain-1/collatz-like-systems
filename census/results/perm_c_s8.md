# perm_c_s8

Rule: 2q -> 3q; 4q+1 -> 3q+2; 4q+3 -> 3q+1. Seed 8.

| question | answer | status | tier |
|---|---|---|---|
| FATE | returns to seed (period 11) | PROVED | 0 |
| GLOBAL | unknown | OPEN | 5 |

**Common facts (tier 1).** (i) The map is a bijection of the positive integers: each residue-class branch is an increasing affine bijection from its class onto one target class, and the target classes partition Z_{>0} (checked algebraically; spot-checked against an explicit inverse in the check script). (ii) For an injective map, fate (b) is impossible: if the orbit of x first meets a cycle C at y=T^k(x) with k>=1 and x not in C, then y has two distinct preimages (T^{k-1}(x) and its predecessor in C). So FATE is "returns" or "infinite". (iii) For a bijection, "every orbit eventually periodic" means "every orbit is a finite cycle".

**FATE.** 8 -> 12 -> 18 -> 27 -> 19 -> 13 -> 11 -> 7 -> 4 -> 6 -> 9 -> 8 (the perm_swap 11-cycle reversed).

**Structure (tier 1).** This map is S^{-1}, S = perm_swap (invert branches: S(3q)=2q, S(3q+1)=4q+3, S(3q+2)=4q+1). Hence its orbits are those of S, and on multiples of 5 it equals y -> 5T^{-1}(y/5).

**GLOBAL (OPEN, tier 5).** Equivalent to GLOBAL for perm_swap, which contains Collatz's 1932 orbit-of-8 problem (orbit of 40 here is 5 times the T^{-1}-orbit of 8).

Check: checks/perm_c_s8.py (exit 0).

## Referee

Independently re-checked against the catalog step functions (systems.py), not only the check script's own re-implementation: mutual inverses on 1..3e5 for T/T^{-1} and S/S^{-1}, B(n)=T(n+1)-1 on 1..3e5, S(5y)=5T(y) on 1..3e5, D injective on 1..8e4 with image covering 1..4e4. Bijectivity is re-derived by hand: the branch images are disjoint residue classes covering Z_{>0} (for D: 5Z from evens, 5q+1..5q+4 from odds). The injectivity argument ruling out fate (b) is correct.

Verdict: FATE confirmed (tier 0). The 11-cycle was re-simulated. GLOBAL open-agreed (tier 5). C = S^{-1} was verified both by hand and on 1..3e5. On 5Z, C(5y)=5T^{-1}(y), so the C-orbit of 40 is finite exactly when the T-orbit of 8 is.
