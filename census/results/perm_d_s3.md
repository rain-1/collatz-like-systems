# perm_d_s3

Rule (D): 2q -> 5q; 8q+1 -> 5q+1; 8q+3 -> 5q+2; 8q+5 -> 5q+3; 8q+7 -> 5q+4. Seed 3.

| question | answer | status | tier |
|---|---|---|---|
| FATE | returns to seed (period 3) | PROVED | 0 |
| GLOBAL | unknown | OPEN | 5 |

**Common facts (tier 1).** (i) The map is a bijection of the positive integers: each residue-class branch is an increasing affine bijection from its class onto one target class, and the target classes partition Z_{>0} (checked algebraically; spot-checked against an explicit inverse in the check script). (ii) For an injective map, fate (b) is impossible: if the orbit of x first meets a cycle C at y=T^k(x) with k>=1 and x not in C, then y has two distinct preimages (T^{k-1}(x) and its predecessor in C). So FATE is "returns" or "infinite". (iii) For a bijection, "every orbit eventually periodic" means "every orbit is a finite cycle". (Inverse: 5q -> 2q, 5q+r -> 8q+2r-1 for r=1..4.)

**FATE.** 3 -> 2 -> 5 -> 3.

**GLOBAL (OPEN, tier 5).** No proof either way. Heuristic drift (1/2)log(25/16) > 0 forward (and positive for D^{-1} too: (1/5)log(2/5)+(4/5)log(8/5) > 0), so most orbits are expected to be infinite; 1990 of the first 2000 starts do not cycle within the baseline budget. But proving any single orbit infinite is a problem of the same type as Collatz's 1932 orbit-of-8 question (a Collatz-type permutation with no known infinite orbit), and no conjugacy reducing D to a solved map was found. Its rational fixed points (0, -1, +-1/3, 1) do not give an embedding of T. Not known to be equivalent to a named problem; it is a direct analogue of the 1932 problem.

Check: checks/perm_d_s3.py (cycle and bijectivity vs explicit inverse; exit 0).

## Referee

Independently re-checked against the catalog step functions (systems.py), not only the check script's own re-implementation: mutual inverses on 1..3e5 for T/T^{-1} and S/S^{-1}, B(n)=T(n+1)-1 on 1..3e5, S(5y)=5T(y) on 1..3e5, D injective on 1..8e4 with image covering 1..4e4. Bijectivity is re-derived by hand: the branch images are disjoint residue classes covering Z_{>0} (for D: 5Z from evens, 5q+1..5q+4 from odds). The injectivity argument ruling out fate (b) is correct.

Verdict: FATE confirmed (tier 0). The 3-cycle 3->2->5->3 was re-simulated. GLOBAL open-agreed (tier 5). Observation: D(n)=5n/2 for even n and round(5n/8) for odd n, a direct analogue of T (2n/3 or round(4n/3)). Both drifts are re-derived as positive. Referee search (scratchpad dsep.py): the residue graph of D, and of D^{-1}, is strongly connected for every modulus M<=200, so no union of residue classes is forward-invariant and no congruence certificate of an infinite orbit exists at those moduli. A 'yes' answer has no known approach either. I agree it is an unsolved analogue of the 1932 problem. It is not known to be equivalent to it.
