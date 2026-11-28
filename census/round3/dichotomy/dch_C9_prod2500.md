# dch_C9_prod2500

**Rule.** 3|n -> n/3; n=1,2,4,5,7,8 mod 9 -> 5n+1, 5n-1, 4n-1, 5n+1, 5n+1, n+1.

As a table map (Q = 9): n mod 9 in {0,3,6} -> (n)/3; n mod 9 in {1,5,7} -> 5n+1; n mod 9 in {2} -> 5n-1; n mod 9 in {4} -> 4n-1; n mod 9 in {8} -> n+1.

**Question (GLOBAL).** Is every positive orbit eventually periodic, and what are the cycles?

**Answer.** Yes. There are exactly 1 cycle(s): (1 6 2 9 3).

**Status.** PROVED (Theorem 2 of dichotomy.md, with the integer certificate below). largest product of multipliers (2500) among certifiable C9 tables; it is one of two certifiable C9 tables attaining this maximum.

## Proof

(H1), (H2) and (P) hold, so Theorem 1 of dichotomy.md applies. decide.py found integer weights c(r) for r mod 9 with c(s)·u_r < c(r)·w_r on every edge r → s of the residue graph. The weights have 60-bit size and are printed by `python3 decide.py --id dch_C9_prod2500`. Each of the 15 edge inequalities is checked with integers, and the largest edge ratio is θ = 0.987888 < 1. By Theorem 2, V(n) = c(n mod 9)·n strictly decreases except on the finite set F = {n : V(Tn) ≥ V(n)}. F is contained in {n ≤ 81} (symbolic bounds N_r) and has 15 elements, the largest being 80. Every orbit meets F and every cycle meets F. Iterating each element of F until it repeats gives exactly the cycles listed above. ∎

## Difficulty

* The minimal stopping depth is **k\* = 6** (Theorem 3). Every plain descent certificate T^j(n) < n on residue classes needs some class with j ≥ 6, and one with max j = 6 exists. The minimal certificate has 27 leaves when residues mod 9 are distinguished.
* Witness for the lower bound: the progression n ≡ 19 (mod 81) (modulus has 7 bits). On it, T^i(n) ≥ n for every i < 6 at all large n. `check_systems.py` verifies this at n = a + M·10^12 by direct iteration.
* The reason is the max-mean cycle of the residue graph: length 6, multiplier 25/27 ≈ 0.925926, mean log-multiplier -0.012827 per step. It contracts, but only barely, so by Theorem 3(c) the depth is large. The a-priori depth bound from the potential is 178.
* A one-step weighted potential nevertheless proves GLOBAL, so on the census scale this is tier 2 (descent plus a finite table). The depth matters only for plain certificates. For comparison, the round-2 depth record desc_s32_max has k = 44.

**Novelty.** I know of no prior occurrence of this specific map; novelty was not checked beyond that. The census catalogue and round 2 do not contain it.

**Check.** `check_systems.py` (all systems, about 5 s).
