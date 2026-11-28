# Referee report: round 3, lens "divergence"

Referee: independent adversarial verification (agent). Date: 2026-11-27.
Files added by the referee: `REFEREE.md` (this file) and `referee_check.py`.
No prover file was modified.

## Summary

| claim | verdict |
|---|---|
| Theorem 1 (b-suffix maps) | CONFIRMED_WITH_FIX (wording in (c)) |
| Theorem 2 (Lemma Q / Corollary Q) | CONFIRMED (the base-2^j case is only sketched; the referee verified the inequalities) |
| Theorem 3 (Lemmas A↑, F, I, B↑) | CONFIRMED_WITH_FIX (one sentence in Lemma I is too strong) |
| Theorem 4 (Lemma P, Corollary P, 5x+1 tables m = 5..8) | CONFIRMED_WITH_FIX (proof step 4 wording; scope "union of classes") |
| Theorem 5 (Lemma P3, tables), PARTIAL | CONFIRMED (PARTIAL is the right label) |
| race_s21 | CONFIRMED |
| fx10_64_s7 | CONFIRMED |
| fx26_32_s7 | CONFIRMED |
| perm12_s7 | CONFIRMED |
| swT2_8_s8 | CONFIRMED |
| c62_64_s27 | CONFIRMED (tier 1, honestly labelled) |
| swT9_s8 side results (OPEN entry) | CONFIRMED (computational part, i ≤ 18); SAT part NOT_CHECKED |

Nothing is WRONG and nothing has a gap that needs repair. The fixes below are
wording or scope clarifications.

## Checks run

* `python3 check.py` (prover): exit 0 after 67 s. All seven sub-checks pass.
* `python3 referee_check.py --full` (referee, written from scratch; it imports
  no prover code): exit 0 after about 25 s. The default run (without
  `--full`) also exits 0 and takes a few seconds less. Section by section:
  * **R1 (race_s21).** The GLOBAL criterion v₂ < v₃ + v₅ holds on 24 500 inputs:
    1..20000, structured random 2^a3^b5^g7^e·m with exponents up to 50, and
    random 30-digit numbers. Each divergent input is followed through two
    exact rounds (c, e) → (c+1, 2e). Other checks: the fixed points are
    exactly gcd(n, 30) = 1; the closed form of the orbit of 21 for k ≤ 8; the
    base-6 set {v₂ < v₃} is closed and cycle-free (on 1..2·10^5 and 20 000
    structured inputs) and equals "last nonzero base-6 digit = 3"; the
    forced-out points 2^A 3^B (A ≥ B ≤ 44); and the fooling-family
    inequalities, including the base-2^j variant (j ≤ 6) that the .md only
    sketches.
  * **R2 (fx10_64_s7, fx26_32_s7).** The residue graphs are computed by brute
    force. All simple cycles of S are enumerated with exact Fraction
    products: each is > 1 and has v₂ ≤ −1. Also checked: offsets ≥ 0, the
    non-fall subgraph is acyclic, G1 is acyclic, S is the unique sink mod
    2^m, and the orbit of 7 enters S at the stated step. **The "least trap"
    claim was tested directly, without Lemma P**: at K = 2^{m+1} … 2^{m+4},
    every sink SCC of the brute-force residue graph mod K contains every
    lift of S. Random 25-digit members of S stay in S and grow.
  * **R3 (c62_64_s27).** The pump T³(n) = 3n + 6 holds on 253 (mod 512),
    including at 50-digit points. T^{3k}(253) = 3^k·256 − 3 for k < 40. U is
    closed, and its four simple cycles have products > 1.
  * **R4 (perm12_s7).** Integrality, positivity, injectivity on [1, 6·10^5)
    and surjectivity onto [1, 1.5·10^5). U = {1, 5, 9, 11} (mod 12) is closed
    (brute force). The non-fall classes 1 and 9 map only to 11. For every
    K < 12, the least closed set containing T(7) contains 7.
  * **R5 (swT2_8_s8).** The separator was recomputed by brute-force closure
    mod 2304, using an exact representative range (n mod lcm(54, 3K)
    determines Q(n) mod K). It has 732 classes and does not contain 8. It is
    closed on 12 lifts per class and on 20 000 random 30-digit lifts.
    **Least modulus, independently of Lemma P3:** for all 49 moduli
    2^i 3^j < 2304, the brute-force least trap containing Q(8) contains 8.
    The same holds for 13 further moduli with i ≤ 7 and j ≤ 6, up to 60 000.
  * **R6 (Theorem 5).** The referee built the full-class graph Γ_i in numpy
    and used "8 is reachable from every node", which is equivalent to "every
    sink component contains 8". G, {9}, {3}, {3,9} and {3,15} are obstructed
    at i = 18, so at every i ≤ 18 by the proved monotonicity; levels i < 12
    were also checked directly. The swap table up to i = 12 reproduces the
    claim: 138 sets, of which 68 return, 67 are obstructed, and the
    separable ones are {(9,15): i = 2, (7,10): i = 5, (2,8): i = 8}.
  * **R7 (Theorem 4 table).** The counts were recomputed from scratch for
    m = 5, 6, 7, 8 (members, G1-cycle, obstructed): (1504, 76, 1373),
    (3008, 108, 2891), (6016, 172, 5844), (12032, 300, 11732). Every
    obstruction witness was re-verified as a genuine cycle. For m = 7 and 8,
    obstructed = members − G1-cycle, so the claim "every acyclic-G1 member is
    obstructed" is confirmed. This takes seconds; the prover's code needed
    up to 40 minutes.
  * **R8 (Theorem 1).** On 300 random binary and ternary suffix maps (most
    non-injective) × 24 seeds, every orbit either repeats or yields a pump
    witness found by the referee's own search. Each witness's affine
    identities were checked at z = 0, 1 and a random 20-digit z.

## Per-claim notes

### Theorem 1: CONFIRMED_WITH_FIX
The argument is the classical pumping argument, re-derived line by line:

* The frozen prefix needs h_{t'} ≥ h_t, which makes q ≥ 1 and the
  concatenation canonical.
* Y_{t₁} = V Y₀ follows from equal last-ℓ words and strictly larger height.
* The identities hold for all z ≥ 0 because the rule is determined by
  n mod b^{|A|}.

**Fix (wording):** in (c), the witness must also require h_{t₀} > ℓ (so that P
is nonempty and [P] ≥ 1). Without it, (a) can fail (V all zeros with P empty).
`suffix_maps.decide` already enforces `len(w0) > ell`; only the text omits it.

The claim "automata never beat congruences in this class" is correct for
congruence-*plus/minus-finite* certificates, which is the form given in (b).
Novelty: the prover's statement that it is classical is honest.

### Theorem 2: CONFIRMED
The proof of Lemma Q is correct. F_{a+1} is a function of F_a, so the
sequence is eventually periodic. Corollary Q is correct in both the "j > i"
and "j < i" forms. For base 2^j, the md's "absorb p^{A mod j}" sketch works
after passing to a subsequence. The referee verified the required inequality
j⌊2^l/j⌋ + (2^k mod j) ≥ 2^k + k + 2 for l ≥ k + 2 and j ≤ 6.

### Theorem 3: CONFIRMED_WITH_FIX
Lemmas A↑, F, I and B↑ are correct. Lemma I's proof is correct: the left side
has valuation bounded below, the right side has valuation tending to −∞.

**Fix (overstatement):** the sentence "no formula T^h(x) = Ax + B can hold
along the orbit from some point on" is stronger than what is proved. What is
proved is that the itinerary mod K is not eventually periodic, which rules out
an affine pump on a residue class (the tier-1 shortcut). Restate it that way.

### Theorem 4: CONFIRMED_WITH_FIX
Lemma P is correct. Two points need fixing.

* **Step 4 wording.** "Take the step before it … some Z_j has p_j ≤ m" is
  muddled: the step before has p_{j−1} ≥ m. The correct statement is simpler.
  Z_j itself, at the first j with p_j < m, is a progression
  {y_j + 2^{p_j} o_j t} (its formula is valid because Z_{j−1} lay in one class
  mod 2^m). Also p_j ≥ 0, because d | a·2^m. Steps 5 and 6 then go through
  unchanged.
* **Scope.** Lemma P and Corollary P concern certificates that are *pure*
  forward-closed unions of residue classes mod 2^K. They say nothing about
  "union of classes minus a finite set" (the argument only shows that U
  contains the class of a periodic point, which a finite exception set could
  remove). Theorem 1(b) uses certificates of exactly that modified form. The
  README and theorem4_precision.md should say "no forward-closed union of
  residue classes", not "no congruence certificate".

The tables are confirmed exactly (R7). The G1-cycle and seed-7 statements at
m = 7 are labelled EVIDENCE, correctly. The referee did not re-run them.

### Theorem 5: CONFIRMED (PARTIAL is correct)
Lemma P3 was re-derived; all four steps are correct.

* The key residue fact in step 3: a progression with difference
  2^{i'}·9·u, where i' ≥ i, hits every class mod 2^i 3^j that is
  ≡ y (mod 2^i·9).
* The monotonicity argument is correct: edges project, and preimages of
  closed sets are closed.
* Corollary P3 is correct for pure unions of classes. The same scope remark
  as for Theorem 4 applies to "separator with finite exceptions".

The computational claims (i ≤ 18 for the cube members, the swap table for
i ≤ 12) were reproduced independently (R6). The claim "Γ_i strongly
connected for i ≤ 11" was not checked (NOT_CHECKED, minor). The SAT claims
are EVIDENCE and were not checked: python-sat is unavailable.

### race_s21: CONFIRMED
All phases were re-derived. Phase R gives (a+e, b+e+g, 0, 0). Phase S applies
S1 min(a, b) times. A round maps (c, e) to (c+1, 2e) in 2e + 2 steps, and the
value grows strictly. The divergence criterion is therefore a < b + g, and the
cycles are exactly the fixed points.

The base-6 certificate and its 2-state minimality are correct. The impossibility
in bases 2^j and 3^j covers finite modifications, because of automaticity.
Tier 1 is honestly stated.

### fx10_64_s7 and fx26_32_s7: CONFIRMED
* The graph tables in the .md were re-derived by hand and match.
* The simple cycles are as listed.
* The unique-sink and least-trap claims are confirmed both via Lemma P and
  directly (R2).
* GLOBAL is correctly left OPEN, and the n ≤ 20000 statistic is labelled
  EVIDENCE.

### perm12_s7: CONFIRMED
The bijection was proved by hand: each branch maps the k-th element of its
input class to the k-th element of its output class, and the output classes
partition Z_{>0}. The separator and minimality claims hold. "Not conjugate to
the catalog" rests only on the slope set, as the .md honestly says.

### swT2_8_s8: CONFIRMED
* The separator was verified independently (R5).
* The least modulus 2304 among 2^i 3^j was verified by brute force, without
  Lemma P3.
* "Infinitely many falls" is correctly labelled EVIDENCE.
* systems.py, precision3.make_sigma((2,8)) and the .md all define the same σ
  (up {2, 8}, down {3, 9}).

### c62_64_s27: CONFIRMED
The pump was verified by hand (253 → 768q+380 → 384q+190 ≡ 62 → 1536q+765),
and the average-contraction product 3^32·4 < 2^63 holds. The proof is tier 1
and labelled honestly.

## Novelty and overclaiming
* None of the systems appear in census/systems.py, round 2, or other round-3
  folders (grep).
* Every novelty statement says "not checked" and is honest.
* Nothing trivial is presented as deep: race_s21 and c62_64_s27 are flagged as
  tier-1 dynamics.
* The main overclaim risk is the phrase "no congruence certificate at any
  modulus" in Theorems 4 and 5, which should read "no forward-closed union of
  residue classes" (see above). race_s21's version of the phrase is fully
  justified, since automaticity covers finite modifications.
