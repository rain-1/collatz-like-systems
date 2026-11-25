# swT9_s8

**Rule.** Q(n) = sigma(T(n)), where T is the 1932 permutation and sigma swaps 9 <-> 10 (mod 18). So Q(n) = T(n)+1 if T(n) = 9 (mod 18), Q(n) = T(n)-1 if T(n) = 10 (mod 18), and Q(n) = T(n) otherwise. |Q - T| <= 1. Q is a permutation of Z_{>0}, affine on classes mod 27, with slopes 2/3 and 4/3.

**Question (FATE).** What is the fate of the seed 8?

| answer | status | tier |
|---|---|---|
| unknown: returns or infinite (never "other cycle") | OPEN | 5 |

## What is proved

Q is injective, so the orbit of 8 either returns to 8 or is infinite. If the orbit first met a cycle at y = Q^k(8) with 8 off that cycle, y would have two preimages.

## What was tried (all bounds exact, in `check_swT9_s8.py`)

- **Simulation.** No return within 1e5 steps (2e5 in exploration). This is evidence only.
- **Congruence certificates (tier 2).** For every K <= 150, and for K in {162, 216, 243, 288, 324}, the forward closure of Q(8) in the exact residue graph mod K contains 8. So no union of residue classes mod K separates. The residue-graph successor sets are computed exactly, piece by piece (Q is affine on classes mod 27).
- **Automata (tier 3).** No DFA certificate exists with at most 4 states in base 2 or at most 3 states in base 3, read MSD-first or LSD-first. A certificate here means: the accepted set excludes 8, contains Q(8), ..., Q^26(8), and is closed on [1, 3000]. Every candidate is refuted by an explicit n with n accepted and Q(n) rejected, so the non-existence at these sizes is a proof.
- **Why the tier-2 trick from swT9_15_s8 fails.** In swT9_15_s8 the two odd falling classes of R = T o sigma both land in 2 (mod 12), and the evens = 2 (mod 12) all rise. Here sigma touches only the class 9 (mod 18), so that trap is not closed. The rigorous statement is the exhaustive closure computation above.

**Why OPEN rather than "probably infinite".** The drift is (1/3)log(2/3) + (2/3)log(4/3) > 0, the same as T's, so most orbits are expected to escape. But the map differs from T only on T-values = 9, 10 (mod 18), and no certificate technique that works for nearby maps works here.

## Role in the chain

This is the nearest unprovable neighbour of the tier-2 system swT9_15_s8. Adding the single swap 15 <-> 16 (mod 18) gives a tier-2 congruence trap. Adding 3 <-> 4 as well gives tier 1 (monotone). Removing the swap gives T itself (tier 5). See swT9_15_s8.md for the full cube.

Check: `check_swT9_s8.py` (exit 0; verifies only the finite evidence).

## Referee

**Verdict: OPEN, tier 5 (agreed as OPEN; the tier-5 label is evidence-based, not a reduction).**

Q is injective, so Q cannot enter a cycle that avoids 8. That part is correct.

I tried to finish the problem with congruences on the conjugate R = T∘sigma_9, which is affine on classes mod 18 and has R^k(8) = sigma(Q^k(8)). `referee_swT9_separators.py` runs an exact residue-graph closure from R(8). It finds no separator for any K ≤ 2500, nor for any K = 2^a·3^b ≤ 20000. A Q-trap mod K gives an R-trap mod lcm(K, 18), so this extends the explorer's bound: there is no Q-separator for K ≤ 138, and none for any K whose lcm with 18 is at most 2500.

I found no reduction to T's 1932 problem either. So this is "no known technique", not "equivalent to a named open problem". Tiers 2 and 3 are excluded only up to the stated bounds.
