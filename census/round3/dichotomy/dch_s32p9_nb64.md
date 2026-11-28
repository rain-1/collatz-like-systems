# dch_s32p9_nb64

**Rule.** even n -> n/2 except n = 18 mod 64 -> (n+46)/64; odd n -> 3n+1 if n mod 32 in {1,3,5,7,9,11,15,17,21,23,25,29} and n != 13 mod 64, else n+1.

As a table map (Q = 64): n mod 64 in {0,2,4,6,8,10,12,14,16,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,58,60,62} -> (n)/2; n mod 64 in {1,3,5,7,9,11,15,17,21,23,25,29,33,35,37,39,41,43,45,47,49,53,55,57,61} -> 3n+1; n mod 64 in {13,19,27,31,51,59,63} -> n+1; n mod 64 in {18} -> (n+46)/64.

**Question (GLOBAL).** Is every positive orbit eventually periodic, and what are the cycles?

**Answer.** Yes. There are exactly 2 cycle(s): (1 4 2), (7 22 11 34 17 52 26 13 14).

**Status.** PROVED (Theorem 2 of dichotomy.md, with the integer certificate below). two-class neighbour of the open desc_s32_plus9 (CLS-052).

## Proof

(H1), (H2) and (P) hold, so Theorem 1 of dichotomy.md applies. decide.py found integer weights c(r) for r mod 64 with c(s)·u_r < c(r)·w_r on every edge r → s of the residue graph. The weights have 60-bit size and are printed by `python3 decide.py --id dch_s32p9_nb64`. Each of the 158 edge inequalities is checked with integers, and the largest edge ratio is θ = 0.996798 < 1. By Theorem 2, V(n) = c(n mod 64)·n strictly decreases except on the finite set F = {n : V(Tn) ≥ V(n)}. F is contained in {n ≤ 311} (symbolic bounds N_r) and has 74 elements, the largest being 307. Every orbit meets F and every cycle meets F. Iterating each element of F until it repeats gives exactly the cycles listed above. ∎

## Difficulty

* The minimal stopping depth is **k\* = 46** (Theorem 3). Every plain descent certificate T^j(n) < n on residue classes needs some class with j ≥ 46, and one with max j = 46 exists. The minimal certificate has 2282 leaves when residues mod 64 are distinguished.
* Witness for the lower bound: the progression n ≡ 1532013231 (mod 4294967296) (modulus has 33 bits). On it, T^i(n) ≥ n for every i < 46 at all large n. `check_systems.py` verifies this at n = a + M·10^12 by direct iteration.
* The reason is the max-mean cycle of the residue graph: length 13, multiplier 243/256 ≈ 0.949219, mean log-multiplier -0.004009 per step. It contracts, but only barely, so by Theorem 3(c) the depth is large. The a-priori depth bound from the potential is 729.
* A one-step weighted potential nevertheless proves GLOBAL, so on the census scale this is tier 2 (descent plus a finite table). The depth matters only for plain certificates. For comparison, the round-2 depth record desc_s32_max has k = 44.

**Novelty.** I know of no prior occurrence of this specific map; novelty was not checked beyond that. The census catalogue and round 2 do not contain it.

**Check.** `check_systems.py` (all systems, about 5 s).
