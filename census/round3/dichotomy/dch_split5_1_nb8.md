# dch_split5_1_nb8

**Rule.** even n -> n/2; n=1 mod 8 -> 5n+1; n=5 mod 8 -> 3n+1; n=3 mod 4 -> n+1.

As a table map (Q = 8): n mod 8 in {0,2,4,6} -> (n)/2; n mod 8 in {1} -> 5n+1; n mod 8 in {3,7} -> n+1; n mod 8 in {5} -> 3n+1.

**Question (GLOBAL).** Is every positive orbit eventually periodic, and what are the cycles?

**Answer.** Yes. There are exactly 1 cycle(s): (1 6 3 4 2).

**Status.** PROVED (Theorem 2 of dichotomy.md, with the integer certificate below). one-class neighbour of the open split5_1 (CLS-048).

## Proof

(H1), (H2) and (P) hold, so Theorem 1 of dichotomy.md applies. decide.py found integer weights c(r) for r mod 8 with c(s)·u_r < c(r)·w_r on every edge r → s of the residue graph. The weights have 60-bit size and are printed by `python3 decide.py --id dch_split5_1_nb8`. Each of the 12 edge inequalities is checked with integers, and the largest edge ratio is θ = 0.927557 < 1. By Theorem 2, V(n) = c(n mod 8)·n strictly decreases except on the finite set F = {n : V(Tn) ≥ V(n)}. F is contained in {n ≤ 12} (symbolic bounds N_r) and has 4 elements, the largest being 11. Every orbit meets F and every cycle meets F. Iterating each element of F until it repeats gives exactly the cycles listed above. ∎

## Difficulty

* The minimal stopping depth is **k\* = 5** (Theorem 3). Every plain descent certificate T^j(n) < n on residue classes needs some class with j ≥ 5, and one with max j = 5 exists. The minimal certificate has 12 leaves when residues mod 8 are distinguished.
* Witness for the lower bound: the progression n ≡ 1 (mod 32) (modulus has 6 bits). On it, T^i(n) ≥ n for every i < 5 at all large n. `check_systems.py` verifies this at n = a + M·10^12 by direct iteration.
* The reason is the max-mean cycle of the residue graph: length 5, multiplier 5/8 ≈ 0.625000, mean log-multiplier -0.094001 per step. It contracts, but only barely, so by Theorem 3(c) the depth is large. The a-priori depth bound from the potential is 23.
* A one-step weighted potential nevertheless proves GLOBAL, so on the census scale this is tier 2 (descent plus a finite table). The depth matters only for plain certificates. For comparison, the round-2 depth record desc_s32_max has k = 44.

**Novelty.** I know of no prior occurrence of this specific map; novelty was not checked beyond that. The census catalogue and round 2 do not contain it.

**Check.** `check_systems.py` (all systems, about 5 s).
