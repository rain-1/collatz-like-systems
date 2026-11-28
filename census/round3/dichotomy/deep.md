# Deepest certificates: the hardest settled systems (application 3c)

**Measure.** k\* is the least k such that a plain descent certificate (T^{j(r)}(n) < n on
residue classes) exists with every j ≤ k. Theorem 3 of dichotomy.md proves that k\* =
Λ + 1, where Λ is the length of the longest non-descending walk of the residue graph, so
k\* can be computed exactly on the graph. Round 2's cylinder engine computes the same number
on every p-power case tested (check_dichotomy.py part A, 71 random CERT tables, and
desc_s32_max: 44 = 44). For dch_S6_332 the engine independently gives k = 332, with
111849 leaves and modulus 2^181. For the deeper records the engine runs out of nodes: the
minimal certificate of dch_B81a2_655 has 3.9·10^8 leaves, and that of dch_C27_2466 has
1.3·10^20. Here the graph computation is the only way, and the lower bound is
cross-checked by an explicit integer witness.

The round-2 record was desc_s32_max, with k = 44.

| id | modulus | k\* | near-critical cycle of G_T (multiplier, length) | cycles of T |
|---|---|---|---|---|
| dch_C27_2466 | 27 | **2466** | 80/81 = 2^4·5/3^4, length 11 | (1 2 3), (5 11 43 45 15), (125 624 208 209 419 420 140 281 1123 1125 375) |
| dch_B81a2_655 | 81 | **655** | 2^11/3^7 = 2048/2187, length 24 | (2 5 6), (22 23 47 95 191 192 64 65 66) |
| dch_S6_332 | 64 | **332** | 3^5/2^8 = 243/256, length 15 | (1 2) |
| dch_B81a5_254 | 81 | 254 | 5^4/3^6 = 625/729, length 15 | (2 11 56 57 19 20 21 7 36 12 4 5 6), (8 41 42 14 71 72 24) |
| dch_B81a4_184 | 81 | 184 | 4^7/3^9 = 16384/19683, length 22 | (1 2 3) |
| dch_B27a5_66 | 27 | 66 | 25/27, length 9 | (1 2 11 12 4 21 7 8 9 3), (28 29 146 147 49 50 251 252 84) |
| dch_B27a8_65 | 27 | 65 | 8/9, length 7 | five cycles, minima 1, 7, 8, 13, 16 |
| dch_s32p9_nb64 | 64 | 46 | 243/256, length 13 | (1 4 2), (7 22 11 34 17 52 26 13 14) |
| dch_D36a7_43 | 36 (mixed) | 43 | 7/8, length 4 | (1 8 4 2) |
| dch_C9_33 | 9 | 33 | 2/3, length 3 (depth from a large potential span, not from near-criticality) | (2 5 6) |

The per-system files `<id>.md` give each system's max-mean cycle, its exact multiplier,
the potential and the witness progression. All entries are PROVED by `check_systems.py`,
which checks:

* GLOBAL, through an integer potential and the exceptional set;
* the complete cycle list;
* the exact k\*;
* a witness integer n with T^i(n) ≥ n for all i < k\* and T^{k\*}(n) < n.

## Why the depth explodes (Theorem 3(c))

k\* ≤ 1 + σ/|μ\*|, where μ\* is the maximum cycle mean of log(u/w) and σ is the span of the
critical potential. All the records have |μ\*| ≈ 10^{−3}:

* dch_C27_2466: μ\* = log(80/81)/11 ≈ −0.00113.
* dch_B81a2_655: μ\* = log(2048/2187)/24 ≈ −0.00274.
* dch_S6_332: μ\* = log(243/256)/15 ≈ −0.00347.

Near-critical cycles need a multiplier ∏u/∏w close to 1. In base 3 with multipliers
1, 2, 4, 5 available, 80/81 is reachable on an 11-cycle at modulus 27. In base 2 with
multiplier 3, the contracting ratios 3^a/2^b closest to 1 need ever longer cycles. Examples are 3^5/2^8 ≈ 0.949 (round 2, and dch_S6_332) and 3^41/2^65 ≈ 0.9886, so larger moduli are needed. More near-critical ratios should give unboundedly deep
certificates as the modulus grows. **Conjecture (EVIDENCE):** for the B(3^k, 2) and C(3^k)
families, sup k\* → ∞ as k → ∞. The mechanism is clear: the ratios 2^a 5^b / 3^c approach 1.
A proof needs an explicit family of tables realising such cycles while keeping every other
cycle contracting. That is OPEN.

**Unbounded depth is cheap with translations (PROVED, check_dichotomy.py part J).**
Take Q = 2^m, with n ↦ n/2 on even n, n ↦ n + 2 on odd n ≢ −1, and n ↦ (n+1)/2^m on n ≡ −1
(mod 2^m). This map has k\* = 2^{m−1}. The translation walk 1 → 3 → … → 2^m − 1 has
multiplier 1 and positive drift, so it is non-descending (Theorem 3). The only cycle is
(1 3 5 … 2^m − 1). So depth records mean something only *within* a family. In the records
above, translation chains have length ≤ 2 (n + 1 or n + 2 moves a unit mod 3 to a multiple
of 3 in at most two steps). Their depth comes from near-critical cycles.

**Depth is not difficulty.** Every one of these systems also has a *one-step* proof: a
weighted potential V(n) = c(n mod Q)·n together with a finite check of F, which has at most
332 elements. So depth measures the plain-certificate format, not the mathematics. This
sharpens round 2's remark: the census "tier 2 versus tier 3 by depth" distinction is
presentation-dependent. By Theorem 1, the Lyapunov form always exists when any certificate
exists.

## Search method

Hill climbing on k\* (`deep_search.py`, `scratch/deep2.py`), which is search only. Results:

* S(6): 332.
* S(7): 331, with 3n+1 on 41 of 64 odd classes, found in 240 s.
* B(81, a): 655, 184, 254 and 126 for a = 2, 4, 5, 8.
* C27: 2466.
* B(243, 2): 594, found in 240 s. This is below the Q = 81 record, so the search at larger Q is far from exhaustive.

These are lower bounds on the true maxima in each family. They are not claimed to be the
maxima.
