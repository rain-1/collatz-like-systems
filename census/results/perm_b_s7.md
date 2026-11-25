# perm_b_s7

Rule (B): 3q -> 4q; 3q+1 -> 4q+2; 3q+2 -> 2q+1. Seed 7.

| question | answer | status | tier |
|---|---|---|---|
| FATE | unknown (returns or infinite) | OPEN | 5 |
| GLOBAL | unknown | OPEN | 5 |

**Common facts (tier 1).** (i) The map is a bijection of the positive integers: each residue-class branch is an increasing affine bijection from its class onto one target class, and the target classes partition Z_{>0} (checked algebraically; spot-checked against an explicit inverse in the check script). (ii) For an injective map, fate (b) is impossible: if the orbit of x first meets a cycle C at y=T^k(x) with k>=1 and x not in C, then y has two distinct preimages (T^{k-1}(x) and its predecessor in C). So FATE is "returns" or "infinite". (iii) For a bijection, "every orbit eventually periodic" means "every orbit is a finite cycle".

**Exact conjugacy (tier 1).** B(n) = T(n+1) - 1, where T is the 1932 permutation. Proof: n=3q gives n+1=3q+1, T = 4q+1, minus 1 = 4q; n=3q+1 gives T(3q+2)-1 = 4q+2; n=3q+2 gives T(3(q+1))-1 = 2q+1. The shift n -> n+1 maps Z_{>0} onto Z_{>=2}, which is T-invariant (T bijective, T(1)=1). So B on Z_{>0} is isomorphic to T on Z_{>=2}, and the orbit of 7 under B is the orbit of 8 under T shifted by -1.

**FATE (OPEN, tier 5).** Equivalent to Collatz's 1932 orbit-of-8 problem. Everything listed for perm_1932_s8 applies verbatim.

**GLOBAL (OPEN, tier 5).** Equivalent to GLOBAL for T (T on {1} is trivially periodic).

Check: checks/perm_b_s7.py verifies the conjugacy on 1..2e5 and orbit agreement for 2e4 steps (exit 0).

## Referee

Independently re-checked against the catalog step functions (systems.py), not only the check script's own re-implementation: mutual inverses on 1..3e5 for T/T^{-1} and S/S^{-1}, B(n)=T(n+1)-1 on 1..3e5, S(5y)=5T(y) on 1..3e5, D injective on 1..8e4 with image covering 1..4e4. Bijectivity is re-derived by hand: the branch images are disjoint residue classes covering Z_{>0} (for D: 5Z from evens, 5q+1..5q+4 from odds). The injectivity argument ruling out fate (b) is correct.

Verdict: FATE open-agreed (tier 5), GLOBAL open-agreed (tier 5). The conjugacy B(n)=T(n+1)-1 was re-derived branch by branch. Z_{>=2} is T-invariant because T is a bijection with T(1)=1. So the orbit of 7 under B is the T-orbit of 8 minus 1, which is exactly the 1932 problem.
