# dch_D36a7_7

**Rule.** 2|n -> n/2; else 3|n -> n/3; else 7n+1 if n mod 36 in {5,11,13,23,25,29,31}, else n+1.

As a table map (Q = 36): n mod 36 in {0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34} -> (n)/2; n mod 36 in {1,7,17,19,35} -> n+1; n mod 36 in {3,9,15,21,27,33} -> (n)/3; n mod 36 in {5,11,13,23,25,29,31} -> 7n+1.

**Question (GLOBAL).** Is every positive orbit eventually periodic, and what are the cycles?

**Answer.** Yes. There are exactly 1 cycle(s): (1 2).

**Status.** PROVED (Theorem 2 of dichotomy.md, with the integer certificate below). 7n+1 on 7 of 12 unit classes mod 36 (maximum); open map div23_7n1 has all 12.

## Proof

(H1), (H2) and (P) hold, so Theorem 1 of dichotomy.md applies. decide.py found integer weights c(r) for r mod 36 with c(s)·u_r < c(r)·w_r on every edge r → s of the residue graph. The weights have 60-bit size and are printed by `python3 decide.py --id dch_D36a7_7`. Each of the 66 edge inequalities is checked with integers, and the largest edge ratio is θ = 0.981714 < 1. By Theorem 2, V(n) = c(n mod 36)·n strictly decreases except on the finite set F = {n : V(Tn) ≥ V(n)}. F is contained in {n ≤ 53} (symbolic bounds N_r) and has 9 elements, the largest being 53. Every orbit meets F and every cycle meets F. Iterating each element of F until it repeats gives exactly the cycles listed above. ∎

## Difficulty

* The minimal stopping depth is **k\* = 15** (Theorem 3). Every plain descent certificate T^j(n) < n on residue classes needs some class with j ≥ 15, and one with max j = 15 exists. The minimal certificate has 139 leaves when residues mod 36 are distinguished.
* Witness for the lower bound: the progression n ≡ 20819 (mod 55296) (modulus has 16 bits). On it, T^i(n) ≥ n for every i < 15 at all large n. `check_systems.py` verifies this at n = a + M·10^12 by direct iteration.
* The reason is the max-mean cycle of the residue graph: length 10, multiplier 343/432 ≈ 0.793981, mean log-multiplier -0.023070 per step. It contracts, but only barely, so by Theorem 3(c) the depth is large. The a-priori depth bound from the potential is 152.
* A one-step weighted potential nevertheless proves GLOBAL, so on the census scale this is tier 2 (descent plus a finite table). The depth matters only for plain certificates. For comparison, the round-2 depth record desc_s32_max has k = 44.

**Novelty.** I know of no prior occurrence of this specific map; novelty was not checked beyond that. The census catalogue and round 2 do not contain it.

**Check.** `check_systems.py` (all systems, about 5 s).
