# The 1x+d family (catalog par_1_1, par_1_5) on Z: complete cycles and basins for every d

Check: `check_split_family.py`, part D.

Map: `P_d(n) = n/2 (n even), n + d (n odd)` on Z, for odd d ≥ 1. This is par_1_d, and
also the 1x+1 map S′(x) = x/2, x+1 on (1/d)Z.

## Theorem D (PROVED, every odd d)

1. Every orbit on Z is eventually periodic.
2. The cycles on Z are {0} and exactly one cycle for each orbit of multiplication by
   2 on Z/d. That is Σ_{e | d} φ(e)/ord_e(2) positive cycles, and the orbit {0} gives
   the cycle (d, 2d).
3. **Basins.** n ≤ 0 with d | n reaches 0. Every other n reaches the unique cycle whose
   residues mod d form the ⟨2⟩-orbit of n mod d. So the basin is a congruence rule mod
   d, plus a sign condition on the multiples of d.

*Proof.* Fold each odd step into the halving after it: U(a) = a/2 for even a and
U(a) = (a + d)/2 for odd a. For 1 ≤ a ≤ d we get 1 ≤ U(a) ≤ d and U(a) ≡ 2^{-1}a
(mod d). Since [1, d] is a complete residue system, U restricted to [1, d] is the
permutation "multiply by 2^{-1}" of Z/d. Its cycles are the ⟨2⟩-orbits. Every P_d-cycle
through positive numbers is a U-cycle with the even intermediate values a + d inserted.

Any n ≥ 1 enters [1, d]: odd n > d gives (n + d)/2 < n, and even n > d halves.
[1, d] ∪ {even numbers ≤ 2d} is forward invariant. So the positive cycles are exactly
the U-cycles on [1, d], and n ≥ 1 reaches the cycle of its residue orbit. This holds
because P_d acts on residues as ×1 or ×2^{-1}, so the ⟨2⟩-orbit of n mod d is
invariant.

For n < 0: an odd n < −d gives n + d < 0 with |n + d| < |n|. An odd n ∈ [−d, −1] gives
n + d ∈ [0, d − 1], which is 0 iff n = −d. So every negative orbit becomes ≥ 0. It hits
0 iff it hits −d, which happens iff the orbit stays inside dZ_{≤0}: on dZ the map is
d·(1x+1), and 1x+1 sends negative integers to nonpositive ones and ends at 0. Residues
are invariant, so a negative non-multiple of d becomes positive in its own ⟨2⟩-orbit. ∎

Check D verifies, for every odd d ≤ 1001, that U permutes [1, d] as ×2^{-1}. For
d ≤ 101 it verifies the cycle count on Z against the ⟨2⟩-orbits, and the basin rule for
every |n| ≤ 3000.

Examples: par_1_1 has cycles {0} and (1 2). par_1_5 has {0}, (5 10) for residue 0, and
(1 6 3 8 4 2) for the units, since 2 generates (Z/5)^*.

**Tier and novelty.** Tier 1. This is surely folklore: U is the classical "x/2 or
(x+d)/2" permutation. Novelty not checked. It is recorded because it is the cleanest
member of the family. The same residue argument fails for the split map (Theorem P),
because the factor 3 merges orbits that hold more than one cycle.
