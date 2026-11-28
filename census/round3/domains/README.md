# Round 3, lens "domains": settled maps on larger domains, and Collatz maps on other rings

Every claim is labelled PROVED / PARTIAL / EVIDENCE / OPEN. All proofs and checks use
exact arithmetic (Python ints and Fractions). Floats appear only in the Karp search
for candidate obstructions, and every candidate is then re-verified exactly.

| file | content | check (runtime) |
|---|---|---|
| theorem_Z.md | Theorem Z (strict certificates are sign-blind), Proposition S (negative cycles are expanding, or degenerate with α = 1 and zero constants), every settled catalog map on all of Z | check_theorem_Z.py (3 s) |
| theorem_N.md | Theorem N: periodic points of positive full-branch block systems are necklaces (p-adic and number-field versions) | check_split_family.py N1–N3, check_rings.py |
| split_family.md | split_d / splitB_d for every odd d: cycles, negatives, the basin-periodicity criterion (Theorem P), exact catalog basins | check_split_family.py (15 s) |
| onexd.md | 1x+d for every odd d: cycles and basins on Z | check_split_family.py D |
| gaussian.md | Z[i]: unit multipliers, Theorem G (1x+c), Theorem PG, the norm-descent certificate census with obstructions, Gaussian 5x+1, the naive lift | check_gaussian.py (10 s), check_gcert.py (30 s) |
| rings.md | Z[ω], Z[√−2], Z[√2]: Theorem R, cycle lists, residue-orbit structure (≤ 2 per orbit proved for Z[√−2]) | check_rings.py (1 s) |
| systems.py | every map as a step function with an id | |
| gdescent.py, zdescent.py, gcert.py, rings.py | engines (Z-certificates with mixed modulus; π-adic norm-descent certificates; quadratic-order arithmetic) | |
| census_gauss.py | full m = 5 Gaussian S-family census (about 5 min; output in scratch/gscan_m5.out) | |

## General theorems

1. **Theorem Z (PROVED).** A descent certificate whose leaves all have slope P < L
   (strict) settles the map on all of Z. Every orbit enters an explicit finite set
   E_Z. **Proposition S:** for maps with positive slopes and nonnegative constants,
   every negative cycle is expanding (so it is exactly a Lemma-B obstruction), or has
   multiplier α = 1 with every constant along the cycle equal to 0. A strict
   certificate excludes negative cycles directly through E_Z (Theorem Z).
2. **Theorem N (PROVED).** For a full-branch block system over a complete DVR whose
   blocks are π-adically expanding: periodic points ↔ primitive necklaces, all of
   them rational. With archimedean contraction, every orbit in a lattice is
   eventually periodic and the cycle list is the set of necklaces with integral fixed
   point. With positive slopes and constants, every rational cycle is positive.
3. **Theorem S1/S2 (PROVED).** The whole split/splitB family is one 2-adic map S on
   (1/d)Z. Its cycles over Z_(2) ∩ Q are exactly the necklaces over
   {A_k, B_k : k ≥ 2}, with x_w = c_w/(2^K − 3^a) ∈ (0, 1]. There are no negative and
   no irrational 2-adic cycles. This gives a closed cycle-counting formula for every
   d. For 3 ∤ d, negative n reaches 0 iff d | n.
4. **Theorem P (PROVED).** The basin function of split_d is ultimately periodic iff
   every weak component of Z/d under ×2, ×3 carries exactly one cycle. That holds for
   185 of the 501 odd d ≤ 1001, and for no multiple of 3.
5. **Theorem D (PROVED, likely folklore).** 1x+d: cycles ↔ ⟨2⟩-orbits on Z/d, and the
   basin is that orbit (plus 0 for n ≤ 0 with d | n).
6. **Theorem G (PROVED).** Gaussian 1x+c (any odd c): GLOBAL yes. The class 0 mod c
   carries exactly {0} and {−ic, (1−i)c}. Every other ×π-orbit of Z[i]/(c) carries 1
   or 2 cycles (finite product-graph lemma). **Theorem PG:** for c a Gaussian prime,
   the basin is a congruence rule iff each unit orbit carries one cycle (fails for
   c = 3). The same bound "≤ 2 per orbit" holds in **Z[√−2]**, where the zero orbit
   carries only {0}.
7. **Theorem R (PROVED).** Unit-multiplier maps on Z[i], Z[ω], Z[√−2], Z[√2] all
   satisfy GLOBAL, with complete cycle lists from an explicit window.

## Systems settled (new domains or new maps)

| id | rule | question | answer | status | tier |
|---|---|---|---|---|---|
| desc_s32_max_Z | catalog desc_s32_max on Z | GLOBAL + cycles on Z | yes; cycles {0}, (1 4 2); no negative cycles | PROVED | 2 |
| desc_s32_d65_Z | catalog desc_s32_d65 on Z | same | yes; {0} + the 8 positive cycles | PROVED | 2 |
| desc_s8_35_Z, par_1_*, m3_a/c/f _Z | catalog on Z | same | yes; {0} + positive cycles (theorem_Z.md table) | PROVED | 1 |
| split_d_Z, splitB_d_Z (catalog d) | catalog on Z | same | yes; {0} + positive cycles; negative non-multiples of d become positive | PROVED | 1 |
| qr maps _Z (7 maps) | round-2 qr maps on Z | GLOBAL + basins on Z | yes; no negative cycles; negative multiples of q reach 0 in the A and C families; [qrB7 has a four-state split](../../round2/qr/qrB7_c53.md#exact-basins-on-negative-multiples-of-seven) | PROVED | 1 for descent |
| farkas2005_Z, farkas5m_Z, farkas_s27_Z | on Z | GLOBAL on Z | yes; cycles {0},{1} (farkas_s27: {−1},{0},{1}) | PROVED | 1 |
| yah_avoid15_Z | n≡1,5 (8) → 1, else 3x+1 | GLOBAL + basins on Z | cycles {0},{1},{−1,−2}; basin of {−1,−2} is exactly {−2^j} | PROVED | 1 |
| yah_avoid6_Z | n≡6 (8) → 1, else 3x+1 | GLOBAL on Z | every n ≠ 0 reaches (1 4 2); all negative 3x+1 cycles destroyed | PROVED | 1 |
| split_73, split_97, splitB_71 | catalog | BASIN | Legendre symbol (n/d) decides between the two unit cycles; d | n → d-cycle | PROVED (new) | 2 |
| split_13, split_7081 | catalog | BASIN a congruence rule? | no (Theorem P); exact basin OPEN | PARTIAL | — |
| M_d, all odd d | split map on (1/d)Z | cycles for every d | necklace formula; lists for d ≤ 401 recomputed | PROVED | 1 |
| G1_c (Z[i], z+c) | z/(1+i) or z+c | GLOBAL, cycles, basins | yes; Theorem G | PROVED | 2 |
| Gm1_1, Gmi_1 (Z[i]) | z/(1+i) or −z+1, −iz+1 | GLOBAL | every orbit reaches 0 | PROVED | 1 |
| Gi_1 (Z[i]) | iz+1 | cycles | {0}, {1,1+i}, {−i,2,1−i} | PROVED | 1 |
| GS5_deep (Z[i]) | (1+2i)z+1 on 5 classes mod (1+i)^5, else z+1 | GLOBAL | yes; only cycle {0}; certificate 965 leaves, k = 63 | PROVED | 2 |
| GS5_max (Z[i]) | 7 classes | GLOBAL | yes; {0}, {−i,1−i}; k = 52 | PROVED | 2 |
| GS5_9 (Z[i]) | 9 classes (maximum at m = 5) | GLOBAL | yes; {0} and an 18-cycle; k = 30 | PROVED | 2 |
| GS4_max (Z[i]) | 3 classes mod (1+i)^4 | GLOBAL | yes; {0}, {−i,1−i} | PROVED | 2 |
| E_f, E_w (Z[ω]) | m3_f analogue; ωz∓1 | GLOBAL + cycles | yes; lists in rings.md | PROVED | 1 |
| ZM2_1 (Z[√−2]) | z/√−2 or z+1 | GLOBAL | every element reaches 0 | PROVED (probably known, CNS) | 1 |
| ZP2_1 (Z[√2]) | z/√2 or z+1 | GLOBAL + cycles | {0}, {1+√2, 2+√2}, {1, 2, √2} | PROVED | 1 |
| G2_naive (Z[i]) | z/2 or z+1 | GLOBAL | **no**: Im z odd gives z, z+1, z+2, … | PROVED (trivial) | 1 |
| G5_1 (Z[i]) | (1+2i)z+1 always (Gaussian 5x+1) | GLOBAL | OPEN; no certificate exists (expanding fixed point z = i, exact); orbits of 1 and 3 grow (EVIDENCE) | OPEN | 5 |

**Gaussian S-family census** (z/(1+i); (1+2i)z+1 on S ⊂ odd classes mod (1+i)^m; else
z+1). Every subset is classified exactly, CERT or OBST, with no unknowns. m=3: 3/13.
m=4: 18/238. m=5: 2277/63259 (65536 subsets). The largest certifiable S has 9 of the
16 classes, and the deepest certificate has k = 63.

## Negative findings (proved)

* Leaves with slope exactly 1 (P = L, R < r), which round 2 allowed, are ascents in
  |n| on negatives. That is why Theorem Z needs strict leaves.
* farkas2005 and farkas5m have **no** certificate on Z. Their expanding fixed points are
  0 (multiplier 3/2) and 1 (multiplier 5/2), integer points. They are settled by
  extending the valuation-run proofs to |n|.
* For full-branch maps (§1–3 of gaussian.md, and S, 1x+d) no orbit can be proved
  divergent by a congruence trap or a periodic itinerary: a periodic itinerary pins the
  unique periodic π-adic point.
* split_13, split_7081, Gaussian 1x+3: the basins are provably not congruence rules.

## Open (sharp)

* Exact basins of split_13 and split_7081 (two cycles in one weak component). Are they
  k-automatic in some base? The qrA3_q17 Cobham argument needs f(pn) = f(n) for p
  independent of k, but only p = 2 is available, so bases that are powers of 2 stay
  open.
* Fate of negatives for split_d with 3 | d. Every negative orbit reaches 0 or becomes
  positive (proved), but which one is not classified.
* Bounds on cycles per ×π-orbit in Z[ω] and Z[√2] (data: ≤ 3); a quadruple product
  graph would decide it.
* Gaussian 5x+1 (G5_1), presumably as hard as 5x+1.

Novelty: not checked against the literature (no web search was done), apart from the
remarks in each file. Theorem D and the ZM2_1 complete-number-system statement are
probably known.

## Refereeing

Fixes applied from REFEREE.md (verdicts otherwise CONFIRMED; no check scripts changed):

* theorem_Z.md, Proposition S: "x < 0 forces α > 1" corrected to "α > 1, or α = 1 and every constant met along the cycle is 0", with the proof step and the counterexample n ↦ n/2 / 2n (negative cycle {−1, −2}, α = 1); noted that no application is affected (exclusions come from E_Z and β_w > 0).
* theorem_Z.md (Tier and novelty) and README.md (file table, general theorem 1): the "negative cycles = expanding cycles" summary narrowed to include the degenerate α = 1 case.
* gaussian.md, Theorem PG: replaced the false "translation by c generates Z[i]/m′" with the referee's π-twisted argument h(ρ) = h(ρ + π^{−j}c), giving invariance under the ideal (c, m′).
* gaussian.md, Theorem PG: periodicity hypothesis stated precisely (f(z) = f(z′) whenever z ≡ z′ mod P and z, z′ ∉ cZ[i]; no "ultimately").
