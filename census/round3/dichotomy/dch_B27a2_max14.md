# dch_B27a2_max14

**Rule.** 3|n -> n/3; n mod 27 in {1,2,4,5,7,10,11,13,14,17,19,20,22,25} -> 2n+1; other 3 not| n -> n+1.

As a table map (Q = 27): n mod 27 in {0,3,6,9,12,15,18,21,24} -> (n)/3; n mod 27 in {1,2,4,5,7,10,11,13,14,17,19,20,22,25} -> 2n+1; n mod 27 in {8,16,23,26} -> n+1.

**Question (GLOBAL).** Is every positive orbit eventually periodic, and what are the cycles?

**Answer.** Yes. There are exactly 1 cycle(s): (1 3).

**Status.** PROVED (Theorem 2 of dichotomy.md, with the integer certificate below). 2n+1 on 14 of the 18 unit classes mod 27 (maximum possible: no 15-set is certifiable).

## Proof

(H1), (H2) and (P) hold, so Theorem 1 of dichotomy.md applies. decide.py found integer weights c(r) for r mod 27 with c(s)·u_r < c(r)·w_r on every edge r → s of the residue graph. The weights have 60-bit size and are printed by `python3 decide.py --id dch_B27a2_max14`. Each of the 45 edge inequalities is checked with integers, and the largest edge ratio is θ = 0.981524 < 1. By Theorem 2, V(n) = c(n mod 27)·n strictly decreases except on the finite set F = {n : V(Tn) ≥ V(n)}. F is contained in {n ≤ 53} (symbolic bounds N_r) and has 22 elements, the largest being 53. Every orbit meets F and every cycle meets F. Iterating each element of F until it repeats gives exactly the cycles listed above. ∎

## Difficulty

* The minimal stopping depth is **k\* = 39** (Theorem 3). Every plain descent certificate T^j(n) < n on residue classes needs some class with j ≥ 39, and one with max j = 39 exists. The minimal certificate has 181 leaves when residues mod 27 are distinguished.
* Witness for the lower bound: the progression n ≡ 2719730 (mod 4782969) (modulus has 23 bits). On it, T^i(n) ≥ n for every i < 39 at all large n. `check_systems.py` verifies this at n = a + M·10^12 by direct iteration.
* The reason is the max-mean cycle of the residue graph: length 12, multiplier 64/81 ≈ 0.790123, mean log-multiplier -0.019631 per step. It contracts, but only barely, so by Theorem 3(c) the depth is large. The a-priori depth bound from the potential is 192.
* A one-step weighted potential nevertheless proves GLOBAL, so on the census scale this is tier 2 (descent plus a finite table). The depth matters only for plain certificates. For comparison, the round-2 depth record desc_s32_max has k = 44.

**Novelty.** I know of no prior occurrence of this specific map; novelty was not checked beyond that. The census catalogue and round 2 do not contain it.

**Check.** `check_systems.py` (all systems, about 5 s).
