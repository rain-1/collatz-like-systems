# REFEREE #1 report: lens "progressions"

Referee check: `referee1_check.py` (written from scratch; `nice python3 referee1_check.py`, exit 0
in about 105 s; 92 fresh Theorem A constructions replayed with the referee's maps (39 skipped for
time), 102 random p-shift maps where Theorem A applies (292 constructions replayed), 253 (system, M)
invariant comparisons, no counterexample to Theorem A). Prover checks re-run: all five exit 0
(`check_theorem_A.py` 110 s, the others under 5 s). Mutation tests (run from a scratch wrapper,
no prover file touched): changing one branch of desc_s32_d65 makes `check_applications.py`
fail, and raising the stored split5_3 exponent to 1/2 makes `check_counting.py` fail. So the
prover's checks can fail.

## Verdicts

| claim | verdict |
|---|---|
| Theorem A (progression theorem, invariant g, algorithm) | **CONFIRMED_WITH_FIX** (wording and novelty only) |
| Theorem B, equivalence (1)–(4) for orbit-invariant labels | **CONFIRMED** |
| Theorem B, clause "no finite automaton in any base separates the basins of C and C′" (and §2(c), item 13 of `applications_basins.md`) | **GAP** (not proved for separators that are not orbit-invariant) |
| Theorem C (counting) | **GAP** in Lemma C2 for 13 of the 32 systems; the exponents of the other 19 stand |
| Theorem D (density-zero sufficient sets) | **CONFIRMED** |
| Combination with descent (PARTIAL) | **CONFIRMED** (honestly labelled) |
| Proposition P, complexity criterion | **CONFIRMED** |
| Proposition P / perm_1932, "no sufficient progression can exist" | **WRONG**: the odd numbers 1 + 2ℤ are a sufficient progression |
| m3_a / m3_c | invariant and non-automaticity CONFIRMED; "≫ X^{1−ε} in every progression" GAP (Theorem C) |
| desc_s32_d65 | **CONFIRMED** |
| par_5_1 | **CONFIRMED** |
| par_3_m1, par_3_5, par_3_13, par_3_17 | **CONFIRMED** |
| par_5_3, par_5_7, par_5_11 | **CONFIRMED** |
| split5_1 | non-automaticity and sufficiency CONFIRMED; "≫ X^{0.692}" GAP (Theorem C) |
| m3_d, m3_e, m3_g, desc_m3_4n5 | **CONFIRMED_WITH_FIX** (the m3_e sentence about the orbit of 7 must be reworded) |
| 3x+1, 7x+1, split7_1, desc_s32_plus9, m3_b | **CONFIRMED** |
| split5_3, split_d family, splitB, par_1_5, qrB7_c53 (reproductions) | **CONFIRMED** |
| div23_5n1 (OPEN, evidence only) | honest; evidence reproduced |

## 1. Theorem A

I re-derived Lemmas 0–6, the Entry argument and the proof. Points I checked in detail:

* **Lemma 4(a)** holds for good Q. My first version of the strong-connectivity test failed at
  moduli divisible by a prime of U (for 3x+1 mod 3, residue 0 is transient). That was a referee
  bug and does not touch the lemma, which is stated only for good Q. The corrected test passes at
  78 good moduli.
* **Lemma 5 (ball growing).** This is the delicate step. If some j_ℓ < v_ℓ(L2), the new ball no
  longer fixes a residue mod L2. The argument still works because only the centre needs a live
  option. D/I words depend only on the state. For an E move the ball either lies in the domain
  coset or contains it. The image ball contains the whole outcome set of the centre's option, so
  a live re-centre always exists, and every j_ℓ drops by v_ℓ(u_r) ≥ 1 because no move is mixed.
  The proof is correct, though it is terse at this point.
* **Lemma 2, the Theorem A proof, and item 2 (finest invariant).** Correct.
* **Independent test of item 2.** At 253 (system, M) pairs, including moduli divisible by p and
  by primes of U, the weak components of the residue graph mod M equal the claimed g-partition
  mod M. Weak components are the finest T-invariant function of n mod M by definition. I also ran
  150 random p-shift tables; where certify.py says Theorem A applies, no mismatch occurred.
* **Constructions.** Constructions on fresh moduli (2^11, 3^6, 5^4, 7^3, 31·32, …) were replayed
  with the referee's own maps, which were re-implemented from the census rule strings and
  cross-checked against `census/systems.py` and the round-2 `systems.py` files. All replays
  merged.

Fixes required (none changes the mathematics):

1. Item 3 gives "1 mod (p^{κ−1}·d*)·m" as an example of a progression meeting all g-classes. It
   meets only one g-class whenever there are several, because g is a function of n mod
   p^{κ−1}d*. Checked for split5_3 in section 10. Replace it with, for example, "1 mod N with
   gcd(N, d*) = 1, for a state-free invariant".
2. §7 says of the 1932 permutation that "no sufficiency statement can hold". This is false; see
   Proposition P below.
3. **Novelty.** The 3x+1 case of Theorem A (every arithmetic progression is sufficient) is a
   published theorem: K. M. Monks, *The sufficiency of arithmetic progressions for the 3x+1
   Conjecture*, Proc. AMS 134 (2006) 2861–2872, doi:10.1090/S0002-9939-06-08567-4. The
   introduction of arXiv:1204.3904 says "In [9], the third author shows that every arithmetic
   sequence is sufficient". Its Theorem 4.1 also gives a back-tracing length bounded in terms of
   the modulus only, which is relevant to Lemma C2. I read the arXiv text (ar5iv); the AMS page
   refused access, so I have not read the PAMS article itself. The novelty line must cite Monks
   (2006) as the known 3x+1 case, not only as "the circle of ideas".

## 2. Theorem B

**Lemma B0.** I re-derived it line by line:

* the CRT choice of r, with r < P^E·G ≤ D;
* that s_j is an integer in [0, D);
* the iterated identity (★) φ(P^j y) = φ(K^j y), using that the two dilations commute;
* that each section's progression meets C′ through the closure property;
* the "one state reads every word" argument;
* the application of Cobham's theorem.

All are correct. The case split k0 ≠ p / k0 = p and the lap identity are correct. I verified the
lap identity T^L(c + μp^L j) = c + μaj exactly for every listed shared-class cycle (section 3b).
The equivalence (1)–(4) for orbit-invariant labels is **CONFIRMED**.

**GAP: the separator clause.** The theorem statement and `applications_basins.md` §2(c) assert
that "no finite automaton in any base separates the basins of C and C′ (on any set of inputs
containing a g-class)". A separator is a set A ⊇ basin(C) with A ∩ basin(C′) = ∅. It is a label
only where every input lies in one of the two basins. For an open system (5x+1, 3x−1, 5x+3, …) a
separator may take any value on starts that reach neither cycle. Then (★) fails and Lemma B0
does not apply. The clause is proved only when the two basins exhaust the g-class, as in
settled systems with no third cycle in the class: m3_a, and desc_s32_d65 for the classes {1, 7}
and {5, 1135}.

Two narrower statements are proved:

* No periodic separator exists, by Theorem A alone.
* No automatic orbit-invariant label separates the two basins.

**m3_e (item 13 and the prover's summary).** The sentence "no congruence or automaton argument
can separate the orbit of 7 from {1,9,3}" is literally false. 7 lies on neither known cycle
(`census/lhf/results.json`). If the orbit of 7 does not reach {1,9,3}, the automatic set
ℕ ∖ {1,3,9} separates them. What is proved is this: the indicator of the merging class of 7, and
the basin of {1,9,3}, are not automatic in any base.

## 3. Theorem C: GAP in Lemma C2

Lemma C1 and the exact verification of (W) are correct. I re-verified (W) independently for
m3_a, split_5, split5_1 and desc_m3_4n5, with children enumerated from the referee's map on
actual integer lifts (section 7b).

**The gap.** Lemma C2 claims that "the ball centre and radius [depend] on z mod ∏ℓ^{J_ℓ+1}".
That is false. In Lemma 5 the initial ball p^{h0}z(1 + ∏ℓ^{J_ℓ}ℤ_ℓ) has radius
ℓ^{−(J_ℓ+v_ℓ(z))}, so the number of E moves needed grows with v_ℓ(z). Hence the word, α_ω, K and
J are not bounded on a type τ ∈ G with v_ℓ(τ) ≥ v_ℓ(W): such a type contains vertices of every
large ℓ-valuation. Executing `construct.py` shows this directly. For split5_1 and m3_a the
number of IA ball words grows with v_ℓ(z) = 0..6 (section 7a).

**Scope.** The certified G of the following 13 systems contains such types: m3_a, desc_s32_d65,
split_5, split_13, split_73, split_97, split_7081, splitB_7, splitB_71, split5_1, desc_split7_1,
desc_s32_plus9 and desc_m3_4n5. The claimed values 0.974 (split_d), 0.692 (split5_1), 0.772
(d65), 0.821, 0.728, 0.578, and the m3_a "σ → 1" statement, are therefore **not proved as
written**.

The other exponents stand: split5_3 0.42, 3x+d 0.41, 5x+d 0.198, 7x+1 0.15, 9x+1 0.115, m3_b,
m3_d, m3_e, m3_g, qrB7_c53 and par_1_5. Their G has no unbounded-valuation type.

**Repair route (checked in section 11, exact finite condition).** For every affected system and
every p-unit state σ there is a move r with v_r ≠ 0 and u_r | v_r, admissible at p^h z for a
fixed h, for every z of state σ with large U-valuation. The ancestor c = (p^{h+1}z − v_r)/u_r
then satisfies T(c) = p^h z, c ≤ p^{h+1}z, and v_ℓ(c) = v_ℓ(v_r) − v_ℓ(u_r), which is bounded
independently of z.

* For m3_a this is c = (3z − 2)/2 for even z, which is odd.
* In all 13 affected systems every residue mod L2 is enterable. I computed this with plib.ia_game
  in a one-off run; it is not part of `referee1_check.py`.
* Lemma C2 can therefore be applied to c instead of z. c has bounded valuation, so the residue
  data really is finite. This gives n(z) := n(c) ≤ K p^{h+1} z with multiplicity ≤ J + 2, and the
  same σ.

The prover must:

1. state Lemma C2 for vertices of bounded U-valuation, with W_P depending on that bound;
2. add this lemma ("R") with its proof and an exact check;
3. add enterability of the reduced vertices to the checks.

An alternative is to restrict G to types with v_ℓ(τ) < v_ℓ(W) and re-certify. Section 7b does
this for 4 systems: m3_a 0.377, split_5 0.878, split5_1 0.674, desc_m3_4n5 0.546. All are lower
than the claimed values, so lemma R (which keeps σ) is the better route.

## 4. Theorem D, the combination lemma, and Proposition P

**Theorem D: CONFIRMED.**

* Density 0: correct.
* Sufficiency: correct. y0 is fixed per class, so the valuation issue of §3 does not arise.
  log log n_k ≤ k log L_U + log k + C < 2k log L_U for large k.
* Thresholds: exp(exp(2 log 5)) = e^25 ≈ 10^{10.86} and e^{625} ≈ 10^{271.4}, both checked.
* Novelty statement: honest.

**Combination lemma and the two obstructions: CONFIRMED.**

* The cylinder argument is correct: a class mod p^m meets every progression with p ∤ N.
* The forward-invariant argument is correct: each φ_r is a bijection of ℤ/q, hence φ_r(A) = A.
* The PARTIAL / negative status is honest.

**Proposition P (complexity criterion): CONFIRMED.**

* I re-derived the Morse–Hedlund step: c(j+1) = c(j) forces unique continuations, hence an
  eventually periodic itinerary.
* The integrality step 3^{Lj} | a^j m ⇒ m = 0 is also correct.

**WRONG: "No sufficient progression can exist" for perm_1932.** The same claim appears in the
systems entry and in Theorem A §7. Counterexample: the progression 1 + 2ℤ is sufficient.

*Proof.* T(3q+1) = 4q+1 and T(3q+2) = 4q+3 are odd. T(3q) = 2q < 3q, so no orbit stays in the
branch r = 0 forever. Hence every forward orbit contains an odd number, and every merging class
meets 1 + 2ℤ. ∎

Moreover, the progressions that meet the cycles (1) and (2 3) are exactly ℤ_{≥1} and 1 + 2ℤ
(section 9 checks this for all N < 60; the general argument is two lines). So the sufficient
progressions of the 1932 map are exactly these two. The correct statement is: no progression
x mod N with N ≥ 3 is sufficient; 1 mod 2 is sufficient, but only trivially, since it gives no
reduction beyond "odd starts".

## 5. Systems

* **Maps.** Every prover table equals the referee's shortcut of the census rule: 6999 inputs per
  system, including random 40-digit inputs. The shortcut lemma S(n) ∈ {R(n), R²(n)} was checked.
* **Cycles.** All listed shared-class cycles are genuine, distinct, and share their g-class. Each
  shared-class system has an expanding cycle.
* **Quoted invariants.** gcd(n, 65); divisibility by d for 3x+5, 3x+13, 3x+17, 5x+3, 5x+7, 5x+11
  and split5_3; the trivial invariant on the 14 listed systems; squares mod 7 for qrB7_c53. All
  confirmed.
* **desc_s32_d65.** "Basin of 65 = 65ℤ" uses GLOBAL from `../../round2/descent/desc_s32_d65.md`
  (8 cycles, refereed) and the fact that 65 is alone in its class. Correct.
* **3x+5.** "Basin of (5 20 10) automatic ⟺ Collatz": correct, since on 5ℤ the map is 5·(3x+1).
* **Evidence (section 5).** Ancestor trees of the shared-class basins hit every compatible class
  mod 11, 16, 27, 32 and 49.
* **div23_5n1.** Every n ≤ 2·10^5 reaches (1 6 3). This is EVIDENCE only and is labelled as such.

## Repair list

1. Theorem C: fix Lemma C2 (bounded valuation) and add lemma R, or re-certify with
   valuation-bounded G. Until then, mark as GAP: the 13 affected exponents, the m3_a σ → 1
   claim, the split5_1 X^{0.692} claim, and the m3_a X^{1−ε} claim in `applications_basins.md`.
2. perm_1932 / Proposition P / Theorem A §7: replace "no sufficient progression can exist" with
   "the only sufficient progressions are ℤ_{≥1} and 1 mod 2", with the proof above.
3. Theorem B and `applications_basins.md` §2(c): restrict "no automaton separates" to
   orbit-invariant labels (or to settled classes exhausted by the two basins). Reword m3_e item 13
   and the summary sentence about the orbit of 7.
4. Theorem A item 3: fix the example progression.
5. Novelty (Theorem A, README, summary): cite K. M. Monks, Proc. AMS 134 (2006) 2861–2872 as the
   known 3x+1 case. Every-progression sufficiency for 3x+1 is not new.
