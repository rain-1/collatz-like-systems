# acc_h32: an OBST Collatz variant with an isolated expanding cycle (settled)

**Rule.** Even n → n/2. For odd n, look at n mod 32:
* n+1 if n ≡ 5, 9, 21, 25;
* n+9 if n ≡ 29;
* 3n+1 otherwise. That is the 11 classes 1, 3, 7, 11, 13, 15, 17, 19, 23, 27, 31.

**Question.** GLOBAL: is every positive orbit eventually periodic, and what is the complete cycle list?

**Answer (PROVED).** Yes. The cycles are exactly (1 4 2), (3 10 5 6) and (19 58 29 38).

**No descent certificate exists.** The 2-adic point −1 is fixed: −1 ≡ 31 (mod 32), and
−1 → 3(−1)+1 = −2 → −1. Its multiplier is 3/2. So Lemma B (round2/descent/lemmas.md) kills every
certificate. `check_trichotomy.py` verifies this with `verify_obstruction`, exactly.

**Proof.** Apply Theorem H of `trichotomy.md` at level K = 5. The SCCs of G_5 with internal edges are:

* {0}: self-loop 0 → 0, multiplier 1/2, contracting.
* {30, 31}: the cycle 31 → 30 → 31, multiplier 3/2. This is an **isolated expanding cycle**,
  type (b). Its periodic point is −1, which is not a positive integer.
* A 21-node SCC {1,2,3,4,5,6,8,9,10,11,13,17,18,19,20,21,22,25,26,27,29}. It is contracting:
  with θ = 843643/858949 and the rational weights c(r) printed by
  `accel_lib.theorem_H`, every internal edge satisfies `c(s)·q ≤ θ c(r)` exactly. The weights depend
  only on r mod 8: c = 1 on 4 and 0 (mod 8), 3 on 6, ≈ 1.612 on 2, ≈ 3.110 on 1 and 5, ≈ 5.013 on
  3 and 7.

The constant is β = 27. So every cycle inside the big SCC has all its points at
`n ≤ β/((1−θ)·min c) ≤ 1515`. Enumerating those points gives the three cycles listed above. ∎

**Why −1 is isolated.** The classes that reach 31 by halvings alone are
R₀ = {0, 16, 24, 28, 30, 31} (mod 32). The complement of R₀ is closed under halving: if e ∉ R₀ is
even, then e/2 and e/2 + 16 are ∉ R₀. The odd branches outside R₀ land at
1→4, 3→10, 7→22, 11→2, 13→8, 15→14, 17→20, 19→26, 23→6, 27→18 (3n+1),
5→6, 9→10, 21→22, 25→26 (n+1), and 29→6 (n+9). None of these is in R₀.

This is where the patches are forced. With 3n+1, the classes 5, 9 and 29 would land in R₀
(16, 28, 24), and with n+1 so would 29 (30). The classes 21 and 25 are patched only to make the
rest contracting. So an orbit leaves the shadow of −1 at most once and never returns.

**Tier.** 2–3 (SCC decomposition plus exactly verified weights). Novelty not checked.
**Check.** `check_trichotomy.py`.
