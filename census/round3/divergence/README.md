# Round 3, lens "divergence": proving that orbits are infinite

This round proves that specific non-monotone orbits are infinite, develops a
theory of when automatic (regular-language) and congruence certificates exist,
and pushes as close as possible to 5x+1 and the 1932 map. All proofs are
agent-written. An independent agent referee has examined everything (REFEREE.md); nothing has had human review.

To check everything, run `python3 check.py`. It runs seven check scripts in
about 2 minutes, and all exit 0. The long table checks are
`check_theorem4_precision.py --m 6,7,8` (about 1 hour; run once, passed) and
`scratch/p3all.py 12` and `scratch/p3big.py 18 17` (minutes each).

## General theorems

| id | statement (short) | status | file |
|---|---|---|---|
| Theorem 1 | **b-suffix maps (non-injective allowed).** FATE is decidable. Every infinite orbit has a pump T^{t₀+kp}(s) = [P V^k Y₀] and a congruence-plus-finite cycle-free certificate. So automata never beat congruences in this class, and divergence there is tier 1. | PROVED | theorem1_suffix.md |
| Theorem 2 | **Quotient obstruction.** For b-automatic C, the sequence a ↦ C/b^a is eventually periodic. So a "fooling family" excludes b-automatic certificates of every size, and congruence certificates at every modulus. The family is: forced-in points b^{a_i}x_i on the orbit, and forced-out points b^{a_j}x_i whose orbits reach cycles. | PROVED | theorem2_quotient.md |
| Theorem 3 | **Ascent traps for non-injective maps.** Lemma A↑: a forward-closed union of classes whose closed walks all have slope product > 1, with offsets ≥ 0, contains no periodic point. Lemma F: forced falls. Lemma I: the itinerary mod K is not eventually periodic, so no affine pump on a residue class. Lemma B↑: contracting periodic points kill the witness. Exact integer witnesses. | PROVED | theorem3_ascent.md |
| Theorem 4 | **2-adic precision lemma.** For 2-adic maps with odd numerators and an acyclic no-halving graph, every congruence trap at any modulus 2^K contains a trap mod 2^m. This gives a finite test excluding certificates that are forward-closed unions of residue classes (not "minus a finite set") at every modulus 2^K. It yields a complete table for single-class changes of 5x+1 at moduli 32 … 256. | PROVED (lemma; "obstructed" entries are proofs) | theorem4_precision.md |
| Theorem 5 | **2·3-adic precision lemma for σ∘G** (G = 1932 map, σ a ±1 change mod 18). Separators at any modulus 2^i·3^j exist only if they exist in a finite "full-class graph" mod 2^i·9. | PROVED (lemma; tables are exact computations) | theorem5_precision3.md |

How these answer task (1), the existence and decision theory for automatic
certificates:

* **Certificates always exist and are periodic:** b-suffix maps (Theorem 1).
* **Certificates provably do not exist:**
  * in bases 2^j and 3^j at any size, for race-type maps (Theorem 2);
  * as forward-closed unions of residue classes at any modulus 2^K, for 2-adic
    odd-numerator maps passing the mod-2^m test (Theorem 4). This covers 17576
    of the 18048 single-class changes of 5x+1 at moduli 128 and 256 in the
    family studied;
  * as separators that are unions of residue classes at every modulus
    2^i 3^j with i ≤ 18, for swT9 (CLS-055) and the other open members of
    round 2's cube (Theorem 5).
  * Theorems 4 and 5 say nothing about "union of classes minus a finite set"
    certificates (the form used in Theorem 1(b)).
* **Automata strictly beat congruences:** race_s21. No congruence certificate
  exists at any modulus, yet a 2-state base-6 automaton works, and no base-2^j
  or base-3^j automaton of any size works.

## Systems

| id | rule | question | answer | status | tier |
|---|---|---|---|---|---|
| race_s21 | 5\|n: 6n/7 (7\|n) else 3n/5; 5∤n: 49n/6 (6\|n), 5n (n odd, 3\|n), n/2 (n even, 3∤n), n (gcd(n,30)=1) | GLOBAL; FATE of 21; certificate sizes | Cycles are exactly the fixed points gcd(n,30)=1. n diverges iff v₂ < v₃ + v₅. 21 diverges, passing 2^{2^k}3^{2^k+k+2}. Base 6: exactly 2 states (C = {v₂ < v₃}). Bases 2^j, 3^j: none of any size. No congruence certificate. Bases coprime to 6: open. | PROVED (other bases OPEN) | 1 for the dynamics; the certificate landscape is the point |
| fx10_64_s7 | 5x+1, but n ≡ 10 (mod 64) ↦ 5n+5 | FATE of 7; divergent classes | All of S = {10,20,21,42,53,55} mod 64 diverges, with infinitely many falls and an aperiodic itinerary. 7 enters S at step 12. S is the least congruence trap at every modulus 2^K. | PROVED | 2 |
| fx26_32_s7 | 5x+1, but n ≡ 26 (mod 32) ↦ 7n+1 | same | S = {5,10,20,21,23,26} mod 32 diverges (falls, aperiodic). 7 enters at step 5. Least trap. | PROVED | 2 |
| perm12_s7 | permutation: 0(6)↦2n−9, 1(6)↦4n+19, 2(6)↦(2n+8)/3, 4(6)↦2n−1, 5(6)↦(2n−7)/3, 3(12)↦(n+3)/3, 9(12)↦2n−7 | FATE of 7 | Infinite: separator {1,5,9,11} mod 12 (least modulus 12), infinitely many falls, 3-adically aperiodic itinerary. | PROVED | 2 |
| swT2_8_s8 | Q = σ∘G, σ swaps n↔n+1 for n ≡ 2, 8 (mod 18); \|Q−G\| ≤ 1 | FATE of 8 | Infinite: separator of 732 classes mod 2304. Least modulus 2^i3^j is exactly 2304; none for i ≤ 7 and any j. Aperiodic itinerary. | PROVED (falls: EVIDENCE) | 2 |
| c62_64_s27 | accelerated 3x+1 (average contraction), but n ≡ 62 (mod 64) ↦ 4n+5 | FATE of 27 | Infinite: 27 → 41 → 62 → 253, then T³(n) = 3n+6 on 253 mod 512, with a fall in every block. | PROVED | 1 (affine pump) |

Requested types, checked off:

* **Non-injective:** race_s21, fx10_64_s7, fx26_32_s7, c62_64_s27.
  c62_64_s27 contracts on average, and its proof is only tier 1. No aperiodic
  trap was found for average-contracting maps (EVIDENCE; c62_64_s27.md).
* **Permutation not in the catalog:** perm12_s7, a new shape. swT2_8_s8 is also
  new, but it belongs to round 2's family. Non-conjugacy is not proved.
* **Base 2 fails provably, another base works:** race_s21 (base 6, two states).
  Base 3 fails too. Theorem 2 explains why I found no "base 2 fails, base 3
  works" example of this kind: the fooling family uses unbounded v₂, which base
  3 cannot see either.

## Task (3): closest to 5x+1 and to the 1932 map

* **5x+1.** The finest single-class change found that settles a
  **non-monotone** infinite orbit of 7 has density 1/64: fx10_64_s7. Consider
  the family of one class mod 2^m with rule (a n + b)/d, a ∈ {1,3,5,7},
  d ∈ {1,2}, b < 8. At moduli 128 and 256, the precision lemma proves that
  every member with an acyclic no-halving graph has **no forward-closed union
  of residue classes as a certificate at any modulus**, for any seed. These are 5844 of 6016 and 11732
  of 12032 members. At modulus 128 the remaining members only give monotone
  traps for 7, at moduli up to 2^11 (EVIDENCE). Monotone (tier-1) divergence of
  7 can be forced at every density by placing the changed class on a
  no-halving loop the orbit visits. So density alone is not the right measure.
* **1932 map.**
  * swT2_8_s8 is a new two-swap neighbour (|Q − G| ≤ 1, the same density as
    round 2's swT9_15) with a proved infinite orbit of 8. Its least
    certificate modulus 2304 is 64 times round 2's.
  * Among the 138 swap sets with ≤ 2 pairs mod 18, the only separable ones for
    i ≤ 12 are {9,15}, {2,8} and {7,10}; the orbit under {7,10} appears
    monotone. No single swap is separable.
  * For swT9 (CLS-055) and the other open cube members, separators that are
    unions of residue classes are excluded at every modulus 2^i·3^j with
    i ≤ 18 (Theorem 5).
  * SAT found no automaton separator for swT9 with ≤ 9 states in base 2, nor
    with ≤ 8 states in bases 3, 6 or 12 (EVIDENCE; `scratch/sat_perm.py`,
    needs python-sat, which I ran from a private venv).

## What stayed open (precise)

* race_s21: automatic certificates in bases coprime to 6.
* fx10_64_s7 and fx26_32_s7, GLOBAL: does every orbit enter S or cycle? The
  2-adic expanding point −1 of (5n+1)/4 lies outside S. It blocks a
  capture-or-descend certificate.
* perm12_s7, GLOBAL: below 3000 the only periodic points are 8 and {21, 35}.
* An aperiodic non-monotone trap for an average-contracting map, or a proof
  that single-class changes of 3x+1 admit none.
* Theorem 5 for all i: strong connectivity of Γ_i for swT9. This would exclude
  congruence separators at every modulus 2^i 3^j for CLS-055.
* The 8 "open, no certificate" members at modulus 64 (theorem4_precision.md).

## Files

* `divlib.py`: RCWA maps, the exact residue graph, and the ascent, fall and
  aperiodicity witnesses.
* `suffix_maps.py`: Theorem 1's decision procedure and certificate verifier.
* `precision3.py`: the full-class graph of Theorem 5.
* `obstruction5.py`: Theorem 4's classification.
* `autoext.py`: product-automaton tests extending round 2's autolib.
* `race_common.py`: the race map.
* `satcert.py`: optional CEGAR SAT search (python-sat); no check depends on it.
* `systems.py`: every new map as a step function, with an exact RCWA form where
  available.
* One `.md` per theorem and per system, and the `check_*.py` scripts.
  `check.py` runs them all.
* `scratch/`: search scripts and raw outputs. These are evidence, not proofs.

**Literature.** Nothing was checked against the literature ("novelty not
checked"). Theorem 1 is the classical pumping argument for deterministic
suffix (pushdown) rewriting, and Lemma Q is a standard right-quotient fact.
Both are stated and proved here in the form used.

## Refereeing

An independent referee reviewed this folder (`REFEREE.md`, `referee_check.py`).
Nothing was found WRONG. Fixes applied from the report:

* theorem1_suffix.md: statement (c) and proof (c) now require h_{t₀} > ℓ for a pump witness (P nonempty, [P] ≥ 1).
* theorem3_ascent.md: Lemma I's "no formula T^h(x) = Ax + B along the orbit" narrowed to "itinerary mod K not eventually periodic, so no affine pump on a residue class".
* theorem4_precision.md: proof step 4 reworded to use Z_j itself at the first j with p_j < m, with p_j ≥ 0 because d | a·2^m.
* theorem4_precision.md: Corollary P and a new Scope paragraph say "no forward-closed union of residue classes", not "no congruence certificate"; finite-exception certificates are not covered.
* theorem5_precision3.md: scope remark added after Corollary P3 (pure unions of classes only, not separators with finite exceptions).
* README.md: Theorem 3, Theorem 4 and Theorem 5 statements and the task (1)/(3) bullets narrowed to the same scope.
