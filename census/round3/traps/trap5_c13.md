# trap5_c13: 5x+1 whose only untrapped cycle is the 13-cycle

**System.** T(n) = 1 if n mod 32 ∈ A = {3, 5, 7, 15, 17, 23}. Otherwise T(n) = n/2 for even n and
5n + 1 for odd n.

**Question.** What is the exact set of eventual behaviours of 5x+1 orbits avoiding A?

**Answer.** Every 5x+1 trajectory either meets A or ends in the cycle
(13 66 33 166 83 416 208 104 52 26). The trivial cycle and the 17-cycle are trapped: 3 ∈ A, and
17 ∈ A. So under T, the only cycles are this 13-cycle and the cycle through 1
(1 → 6 → 3 → 1 → …, since 3 ∈ A sends 3 to 1). **PROVED** by a Theorem-2 certificate; tier 2.
Novelty not checked.

A is minimal: deleting any one residue gives an H set, so no SCC/descent certificate exists for it
at any modulus 2^m (check.py [2]). Ten minimal sets mod 32 isolate the 13-cycle in this way. They are
listed in results/census_C5_k5_odd.json.

## Certificate (level 5, B = 295)

* **Simple components:** (28, 30, 31), with lift −4 and multiplier 5/4; and (21, 10), with lift
  −1/3 and multiplier 5/2. These are the two expanding 2-adic cycles that avoid A.
* **Contracting component:** {0,1,2,4,6,8,11,12,13,16,19,20,22,24,26,27}. Its worst cycle is
  0 → 16 → 8 → 20 → 26 → 13 → 2 → 1 → 6 → 19 → 0, multiplier 125/128, lifting exactly to 416 on
  the 13-cycle. That is why the margin is thin.
* **Potential:** Q = 1024, P_5 = 2378, φ as printed by `traps_lib.finish_certificate`.
* **Trivial components:** 9, 14, 18, 25, 29.

By Theorem 2, every orbit avoiding A enters [1, 295]. Simulation of [1, 295] shows that the only
avoiding cycle is the 13-cycle.

**Check.** `check.py` [2] and [5]: the certificate is verified independently (verify.py); random
huge n are tested as evidence only.
