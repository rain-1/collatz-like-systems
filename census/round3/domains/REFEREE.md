# Referee report: round 3, lens "domains"

Referee: independent adversarial check. I did not modify any prover file. My files are
`referee_check.py` (parts RZ, RH, RQ, RS, RD, RG, RM, RC; about 10 s in total, exits 0) and `referee_census5.py` (the full m = 5 Gaussian census, 24 s).
Neither imports the prover's code. Map definitions are rebuilt from the written rules
and cross-checked against `census/systems.py`, `round2/descent/systems.py`,
`round2/literature/systems.py`, `round2/rewriting/systems.py` and `round2/qr/qrlib.py`.

## 1. Prover checks

All five prover check scripts exit 0: check_theorem_Z.py (3 s), check_split_family.py
(13 s), check_gaussian.py (15 s), check_gcert.py (34 s), check_rings.py (0.4 s). They
test real finite content (certificate verification, exact necklace fixed points,
product graphs, exact obstructions). Two limits:
* `gdescent.verify` and `gcert.verify` check affine forms at a few fixed t and test the
  partition by "measure 1 + no class contains another". That is adequate, because the
  tree construction already guarantees the partition. My check tests the partition and
  the forms on random integers (up to 10^30, and Gaussian integers up to 10^25).
* The m = 5 census row was produced by `census_gauss.py`, and its CERT cases were built
  but not re-verified by the prover. I re-ran the full census with my own builder and
  my own obstruction search (below), so the gap is closed.

## 2. Independent re-derivation and verdicts

### Theorem Z: CONFIRMED
The argument is Lemma A with |n|. Strict leaves 0 < P < L give |Pt+R| < |Lt+r| for
|t| > (|R|+|r|)/(L−P). The forms are polynomial identities in t because every branch
was fixed for all t ∈ Z, and the norm decreases strictly, so the iteration is
well-founded. The remark that P = L leaves ascend on negatives is correct.
My own strict-certificate builder (it splits by the deficient prime and requires
Q | P and w | uP) reproduces, for all 22 maps of the table, exactly the stated cycle
lists on Z. That includes split_7081 (minima 0, 1, 11, 41, 291, 485, 569, 713, 949,
2409, 7081) and desc_s32_d65 ({0} plus the 8 round-2 cycles (1,21), (5,5), (7,29),
(13,4), (39,5), (65,3), (299,8), (1135,13)). |E_Z| agrees wherever printed (4385 for
split_7081, 124 for qrC_q311, 20 for qrB7_c53). desc_s32_max has k = 44 in my tree
too. Every table has u, w > 0 and v ≥ 0.

### Proposition S: CONFIRMED_WITH_FIX
From x(1−α) = β ≥ 0 we get only that **x < 0 forces α > 1, or α = 1 and β = 0**. The
stated "x < 0 forces α > 1" is false in that degenerate case. Counterexample within
the hypotheses: n even ↦ n/2, n odd ↦ 2n (u > 0, w > 0, v = 0). It has the negative
cycle {−1, −2} with α = 1, which is not expanding, and Lemma B does not apply to it.
Fix: add "or α = 1 and every constant met along the cycle is 0". No application in the
folder is affected. Every negative-cycle exclusion in theorem_Z.md comes from E_Z
directly (Theorem Z), not from Prop. S, and for the split/necklace maps from β_w > 0.

### Hand-settled maps on Z (farkas2005, farkas5m, farkas_s27, yah_avoid15, yah_avoid6): CONFIRMED
I re-derived each argument. Checks, all exact on [−2·10^5, 2·10^5] and on 3000 random
300-bit integers:
* farkas2005: G^{2a+1}(m) = (c+1)/2, with |(c+1)/2| < |m|.
* farkas5m: T^{2a+1}(n) = (b+1)/2.
* farkas_s27: R(n) = G(n+1) − 1 for n ≠ 1.
* The one-step descents and sign preservation, and G(m) = 1 iff m ∈ {1, 2}. That last
  fact is needed for "n ≥ 1 reaches 1" in farkas_s27 and is only implicit in the text.
* yah_avoid15: I checked the run identity o_j = 3^j 2^{a−j} b − 1 for o ≡ 7 (mod 8),
  including negative b, and the basin {−2^j} of {−1, −2} on [−5000, 5000].
* yah_avoid6: I wrote my own symbolic |·|-descent on Z, with 18 leaves and the
  constant branch n ↦ 1 as a leaf, and simulated the exceptional range |n| ≤ 907.
  Every n ≠ 0 reaches 1.

### qr maps on Z: CONFIRMED as PARTIAL (the stated status)
* Cycle lists: confirmed (RZ).
* Invariance of gcd(n, q): checked.
* For the A-maps and qrC, negative multiples of q stay ≤ 0 and reach 0. The m + c ≤ 0
  argument is right.
* EVIDENCE that negatives follow the mod-q rule: for n ∈ [−3000, −1] with q ∤ n, n
  reaches the same cycle as n + 10^6 q.
* qrB7: −7 ↦ 14, so negative multiples of 7 do leave the nonpositive integers. The OPEN
  label is correct.

### Theorem N: CONFIRMED
* (F1)–(F3) hold for every instance used. A_k pulls back to x = (2^k u − 1)/3, which is
  ≡ 1 (mod 4) for k ≥ 2. B_k pulls back to 2^k u − 1, which is ≡ 3. The Gaussian and
  quadratic-order blocks pull back to (π^k w − c)/u, which is odd.
* Banach in U, the uniqueness of the affine fixed point, and the archimedean bound
  M/(1 − λ) are right (λ = 3/4, M = 1/4 for S, so x_w ∈ (0, 1]).
* Part 4 uses discreteness of the lattice under the Minkowski embedding; that is fine.
* Independent test: 400 random words over {A_k, B_k} (k ≤ 7, length ≤ 8). For each
  one, x_w ∈ (0, 1], and the exact 2-adic orbit of x_w follows the word with the right
  class and exact valuations, then returns.

### Theorem S1/S2: CONFIRMED
* M_d agrees with the catalog split_d and splitB_d maps on [−2000, 2000].
* For every odd d ≤ 301 I simulated a window of [−3d, 3d]. All nonzero cycles are
  positive, and their odd points lie in [1, d].
* S2: the denominator is preserved when 3 ∤ d (gcd(3a + e, e) = 1), and negative
  integers stay ≤ 0. I checked that for 3 ∤ d ≤ 301 and n ∈ [−6d, −1], n reaches 0
  iff d | n.

### Theorem P: CONFIRMED
Steps (i)–(v) re-derived. In Z, +d generates gZ/m′, so (iv) is right. The "if"
direction holds because M_d acts on residues by ×2^{−1}, ×3 or ×1. Recomputed
independently:
* **185 of the 501** odd d ≤ 1001 have one cycle per weak component, and none of them is
  a multiple of 3. The list for d ≤ 200 matches the one in split_family.md.
* For every good d ≤ 301 the basin follows the component, for positive n, for negative
  non-multiples of d, and for random 40-digit n.
* split_13 has cycles 1 and 5 in one component, and split_7081 has 569 and 713 in one
  component, so neither basin is a congruence rule.

### split_73, split_97, splitB_71 Legendre rules: CONFIRMED
* ⟨2, 3⟩ = the quadratic residues mod p, for each of the three primes.
* The rules are verified on n < 5·10^4, on 300 random 60-digit n, and on negatives:
  (n/73) = +1 gives the cycle of 3 and −1 the cycle of 5; for 97 they give 33 and 13;
  for 71 they give 1 and 11.

These follow from Theorem P, so they are proved.

### split_13 / split_7081 (PARTIAL): CONFIRMED
The negative statement ("no congruence rule") is proved. The exact basin is honestly
left OPEN.

### Theorem D (1x+d): CONFIRMED
* The cycle count equals the number of ⟨2⟩-orbits on Z/d.
* The basin rule (n ≤ 0 with d | n goes to 0; everything else goes to the cycle of its
  ⟨2⟩-orbit) is exact for every odd d < 100 and |n| ≤ 2000.

The result is folklore, as stated.

### Theorem G (Gaussian 1x+c): CONFIRMED
I re-derived the proof.
* V ≡ π^{−1}z (mod c), q_{n+1} = (q_n + e_1 − e_2)/π, and N(q) ≤ 5.
* e_1 + e_2 ≡ parity(q_12) because c is odd.
* An itinerary determines its point (digits of −z/c).

My own triple product graph has two labelled choices (e_1 = 0 or 1) per state and keeps
both labels. Its closed-walk part has 12 states, each with **exactly one** labelled
outgoing transition, forming two 6-cycles whose three parity words are rotations of
one another. That is what the proof needs.

Data for the 33 odd c with |Re c| ≤ 5 and 0 ≤ Im c ≤ 5:
* the zero class carries exactly {0} and {−ic, (1−i)c};
* every ×π-orbit carries 1 or 2 cycles;
* random z with coordinates up to 10^6 reach a cycle of their own orbit;
* for c = 3 there are two 12-cycles in the unit orbit.

### Theorem PG: CONFIRMED_WITH_FIX
1. **Wrong as written.** "If g = 1, translation by c generates Z[i]/m′" is false:
   Z[i]/m′ is not cyclic as an additive group (for example m′ = 3, where Z[i]/3 = F_9
   and Z·c has order 3).
   **Fix.** Combine the two invariances: h(ρ) = h(π^j ρ) = h(π^j ρ + c) = h(ρ + π^{−j}c).
   So h is invariant under translation by c·Z[π, π^{−1}] = c·Z[i] mod m′. That is the
   ideal (c, m′), which is everything when g = 1 and (c) when g = c. With this fix both
   cases go through as written.
2. **Hypothesis to make precise.** The hypothesis "f periodic modulo P" should be stated
   as: f(z) = f(z′) whenever z ≡ z′ (mod P) and z, z′ ∉ cZ[i]. Unlike Z, there is no
   "ultimately", and intermediate translates may fall into cZ[i].

### Z[√−2] "at most 2 cycles per orbit": CONFIRMED
* My own triple graph (z/√−2 = (b, −a/2)) has 24 states with unique transitions, forming
  6 cycles of length 4, each with rotated words.
* ZM2_1 has only the cycle {0}.
* The claim "2 occurs, e.g. c = 15" is data and I did not re-check it.

### Theorem R and the cycle lists (Gi_1, Gm1_1, Gmi_1, E_f, E_w, ZM2_1, ZP2_1): CONFIRMED
* The window bounds are correct: N(z) ≤ 6N(c) ⊇ |z| ≤ |c|/(√2 − 1); 2N(c) for Z[ω];
  |a| + |b|√2 ≤ B for Z[√2].
* My own arithmetic in each ring, with wide windows, gives exactly the stated lists:
  * Gi_1: {0}, {1, 1+i}, {−i, 2, 1−i}.
  * Gm1_1 and Gmi_1: {0} only.
  * E_f: {0}, {1+ω, 2+ω}, {2+2ω, 4+2ω}.
  * E_w: {0}, {−1, 1−ω, 1, −1+ω}.
  * ZP2_1: {0}, {1+√2, 2+√2}, {1, 2, √2}.

### Gaussian S-family census: CONFIRMED
`referee_census5.py` (own builder, own exact positive-cycle search in the residue graph
mod π^5 and π^7, with Lemma D for the full cylinders) gives:
* m = 5: **CERT 2277, OBST 63259, UNK 0, maximum certifiable |S| = 9**;
* m = 3: 3/13; m = 4: 18/238.

Every CERT case was rebuilt by my builder.

### GS5_deep, GS5_max, GS5_9, GS4_max: CONFIRMED
My own norm-descent trees are coarser than the prover's but have the same depth:

| system | leaves (mine / prover's) | K | k | \|E\| | cycles |
|---|---|---|---|---|---|
| GS5_deep | 1377 / 965 | 44 | 63 | 26 | {0} only |
| GS5_max | 735 / 666 | 37 | 52 | 189 | {0}, {−i, 1−i} |
| GS5_9 | 144 / 92 | 23 | 30 | 181 | {0} and an 18-cycle through −2−2i, i, 6, 4−4i |
| GS4_max | 14 / 12 | 7 | 10 | not compared | {0}, {−i, 1−i} |

* I compute E by exact integer bounds.
* The S residue convention in systems.py, (x mod 4, (y − 4⌊x/4⌋) mod 8) for π^5 = −4−4i,
  is correct, and all listed classes are odd.

### G5_1 (OPEN), G2_naive (PROVED, trivial), Bound in Z[ω] and Z[√2] (EVIDENCE): CONFIRMED as labelled
* G5_1: z = i is a fixed point of (1+2i)z + 1 followed by one division. Its multiplier
  √(5/2) > 1, so no certificate exists.
* G2_naive: an odd imaginary part is never cleared. It is correctly called trivial.

### Catalog-on-Z systems, M_d family, G1_c, Gm1_1/Gmi_1: CONFIRMED (see above)

## 3. Overclaiming and novelty
* The labels are honest. The prover itself flags the tier-1 / trivial items: 1x+d is
  folklore, G2_naive is trivial, and Theorem Z is elementary.
* The genuinely new content:
  * the uniform cycle formula for the split family;
  * Theorem P, with the Legendre rules for 71/73/97 and the proof that 13 and 7081 have
    no congruence rule;
  * Theorem G with its product-graph lemma;
  * the exactly classified Gaussian certificate census with four deep tier-2 systems.
* Novelty: ZM2_1 is the statement that base √−2 with digits {0, 1} is a canonical number
  system of Z[√−2]. That is a known CNS case: x² + 2 satisfies the classical quadratic
  CNS criterion (Kátai–Kovács; Gilbert), from memory and not re-checked. The prover's
  "probably known" is accurate. Nothing else was checked against the literature by me
  either.
* "Settled catalog maps on Z" is an extension of already-settled maps to a new domain,
  not new hard systems. It is presented as tier 1 / 2, which is fair.

## 4. Summary
No claim is WRONG and there is no GAP that affects a result. Two text fixes are needed:
Prop. S (the α = 1, β = 0 case) and Theorem PG (replace "translation by c generates
Z[i]/m′" with the π-twisted translation argument, and state the periodicity hypothesis
precisely). needs_repair = false. The fixes are wording, and the results stand.
