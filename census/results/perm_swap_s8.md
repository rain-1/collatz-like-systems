# perm_swap_s8

Rule (S): 3q -> 2q; 3q+1 -> 4q+3; 3q+2 -> 4q+1. Seed 8.

| question | answer | status | tier |
|---|---|---|---|
| FATE | returns to seed (period 11) | PROVED | 0 |
| GLOBAL | unknown | OPEN | 5 |

**Common facts (tier 1).** (i) The map is a bijection of the positive integers: each residue-class branch is an increasing affine bijection from its class onto one target class, and the target classes partition Z_{>0} (checked algebraically; spot-checked against an explicit inverse in the check script). (ii) For an injective map, fate (b) is impossible: if the orbit of x first meets a cycle C at y=T^k(x) with k>=1 and x not in C, then y has two distinct preimages (T^{k-1}(x) and its predecessor in C). So FATE is "returns" or "infinite". (iii) For a bijection, "every orbit eventually periodic" means "every orbit is a finite cycle".

**FATE.** 8 -> 9 -> 6 -> 4 -> 7 -> 11 -> 13 -> 19 -> 27 -> 18 -> 12 -> 8.

**Structure (tier 1).** S(n) = 5 T(n/5), where T is the 1932 map extended to rationals with denominator prime to 3 (branch chosen by x mod 3): if x=n/5 then n = 2x mod 3, and the three branches match (n=0: 2n/3 = 5(2x/3); n=1 <-> x=2: (4n+5)/3 = 5(4x+1)/3; n=2 <-> x=1: (4n-5)/3 = 5(4x-1)/3). So S is T acting on (1/5)Z_{>0}. In particular the multiples of 5 are S-invariant and S(5y) = 5T(y) for integers y.

**GLOBAL (OPEN, tier 5).** "Yes" would imply the S-orbit of 40 = 5*(T-orbit of 8) is finite, i.e. it would settle Collatz's 1932 problem; so GLOBAL here contains that open problem. "No" would need a provably infinite S-orbit; none is known (S has the same drift as T, and 1929 of the first 2000 starts do not cycle within the baseline budget). Same tools fail as for T.

Check: checks/perm_swap_s8.py (cycle, bijectivity vs explicit inverse, S(n)=5T(n/5) on 1..2e4, S-orbit of 40 = 5*T-orbit of 8 for 2e4 steps; exit 0).

## Referee

Independently re-checked against the catalog step functions (systems.py), not only the check script's own re-implementation: mutual inverses on 1..3e5 for T/T^{-1} and S/S^{-1}, B(n)=T(n+1)-1 on 1..3e5, S(5y)=5T(y) on 1..3e5, D injective on 1..8e4 with image covering 1..4e4. Bijectivity is re-derived by hand: the branch images are disjoint residue classes covering Z_{>0} (for D: 5Z from evens, 5q+1..5q+4 from odds). The injectivity argument ruling out fate (b) is correct.

Verdict: FATE confirmed (tier 0). The 11-cycle was re-simulated. GLOBAL open-agreed (tier 5). S(n)=5T(n/5) re-derived by hand: n=5x gives n = 2x (mod 3), and all three branches match. So 5Z is S-invariant and S(5y)=5T(y), which makes the S-orbit of 40 five times the T-orbit of 8. GLOBAL therefore contains the 1932 problem.
