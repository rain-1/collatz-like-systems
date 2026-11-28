# Second referee report: round 3, lens "mixedbase" (after the repair pass)

Second independent referee. I did not modify any prover file or the first referee's files. My files are `referee2_check.py` and this report.

## What I ran

* **Prover's checks** (all exit 0): check_relatives.py (4 s), check_pairing_family.py (3 s), check_systems.py (<1 s), check_single_class.py (14 s), check_sparse.py (15 s). The first referee's referee_check.py also exits 0 (13 s).
* **`referee2_check.py`** (written from scratch; it imports nothing from mixedlib, pairlib, the check scripts, systems.py or referee_check.py; every map is re-typed from the rule text). It exits 0 in about 35 s.
  * **A. My own mixed-radix engine.** A node n = Mt + r, T^j(n) = Pt + Q steps only when every residue Q + Ps mod M0 uses the same row and the division is exact uniformly. Otherwise it splits t by the smallest prime of M0/gcd(P, M0). Lemma A' then does the following: checks the partition (total density 1, plus explicit disjointness when small); re-tests each leaf identity at t = 0, 1 and random 100-bit and 200-bit t, comparing against the step function written from the rule; and builds the exceptional set E and the complete cycle list. My leaf counts match the prover's exactly for every system, for example mb_t729 (5417 leaves, depth 83), mb_d23_8 (93), mb_d23_30 (12) and mb_m3b_8 (36).
  * **B. Theorem D.**
    * Own enumeration of the expanding rational cycles of div23_5n1 for all words up to length 11. It finds 11 cycles, as the prover says.
    * The cycles (−1 −4 −2) (multiplier 5/4) and (−84 −42 −21 −7 −34 −17) (multiplier 25/24) are verified exactly. I checked the difference bound max |y − z| = 83, and that A and B alone exclude every r for 84 ≤ q ≤ 600.
    * Own refined-Lemma-B' scan for q ≤ 83, under both priorities. It reproduces the claimed lists exactly.
    * **Every one of the 6952 excluded pairs gets an integer simulation of its witness.** Take n ≡ y₀ (mod (6q₁)^K) plus a random 64-bit multiple. It follows the base cycle for three periods through the *tamed* map without being caught, and T^L(n) = λn + μ > n holds exactly. This tests the refined lemma itself on real integers, including the cases where q shares a prime with the cycle denominator (13 | q).
    * Every survivor except first (2,0) and first (4,2) is certified, and its complete cycle list equals the repaired table in relatives.md. In particular: first (3,1) has (1) and (5 26 13); first (6,2) has (1 6 3) and (5 26); first (10,6) has (1 6); first (2,1), first (5,1) and last (2,1) have (1); all others have (1 6 3). first (2,0) and (4,2) do not terminate within budget, consistent with "open / unresolved". This is not a claim that no certificate exists.
    * I also checked the −42/13 cycle mentioned in the text: 5 steps, multiplier 25/12.
  * **C. Theorem M.**
    * Own enumeration of m3_b cycles (words up to length 11; 6148 cycles). It contains ±1, (1/7, −1/7) and (7/25, 1/25, −7/25, −1/25).
    * One class: the only class containing both 1 and −1 for q < 500 is (2,1). odd → (n+1)/2 is certified (4 leaves) with the cycles **(1), (2 3)**.
    * Two classes {1, −1} mod q: the scan over **3 ≤ q ≤ 400** against all 6148 cycles leaves exactly {3, 4, 6, 8}. All 394 exclusions are integer-simulated as above.
    * The bound argument itself (C1 with the refined lemma, or else C2) excludes every q from 33 to 2999. The numerators of y ∓ 1 on C2 are {18, 24, 26, 32}.
    * q = 3, 4, 6, 8 are certified, each with the single cycle (1). The mb_m3b_8 step function equals the rule text on 1..5000.
  * **D. The other 12 certified systems.** These are mb_s3_3, s3_9, s5_5, s7_7, t27, t81, t243, t729, f25, f125, s49 and s343. My engine reproduces each one, with identical leaf counts and depths and identical cycle lists. Minimality: my own cycle enumeration (all words, up to length 16 for a = 3 and up to 14 for a = 5, 7) and my own exact branching hitting-set search confirm every lower bound: 2/3/4/7 for 3^3..3^6, 2/4 for 5^2 and 5^3, and 2/5 for 7^2 and 7^3.
  * **E. EVIDENCE only.** 100 random 300-bit odd starts each, for mb_d23_30, first (3,1), mb_m3b_8, m3_b + odd class and mb_t729. All reach the listed cycles.

## Re-derivation of the repaired arguments

1. **Refined Lemma B' (lemmas.md).** Let q = q₁q₂, where q₂ carries the primes of the cycle denominator d. If no admissible y on the cycle has y mod q₁ ∈ R mod q₁, then integers n ≡ y₀ (mod (M_base·q₁)^K) have the following properties:
   * They have the base branch of the cycle point at every step, since the base branch depends only on n mod M_base.
   * They are never caught, since membership in the class needs n mod q₁ ∈ R mod q₁.
   * Each step divides by w | M_base, so K = (steps + 2) is enough precision.

   Their residue mod q₂ is irrelevant. Given a certificate (M', j(·)), choose its class compatibly with y₀ on the primes of M_base·q₁. CRT then gives infinitely many such n in one certificate class, with T^j(n) = λ_j n + β and λ_j > 1 (cycle lemma), which is a contradiction. The argument is sound, and my integer simulation tests exactly this.
2. **Theorem D(1).** Both cycles are integral, so they lie in Z_q for every q, and the plain Lemma B' applies to each. One residue r must equal some y mod q and some z mod q, so q | y − z ≠ 0 and q ≤ 83. Under "last" only 5n+1-branch points are admissible, which is a subset, so the bound still holds. The finite scan then decides each q ≤ 83. Sound.
3. **Theorem M.**
   * C1 = {±1/7} with the refined lemma: q₁ = q/7^e must divide 6 or 8 (from 1/7 − 1 = −6/7, 1/7 + 1 = 8/7, and the symmetric pair). So the primes of q lie in {2, 3, 7}.
   * C2 has denominator 25, prime to 42, so q itself divides a numerator in {18, 24, 26, 32}. Hence q ≤ 32.
   * I verified C2 by hand: 7/25 ≡ 1 (mod 3) maps to 1/25 ≡ 1, which maps to −7/25 ≡ 2, then to −1/25 ≡ 2, then back to 7/25. The multiplier is (4/3)^4.

   Sound.

## Verdicts

| claim | verdict |
|---|---|
| Pairing P1–P3 | CONFIRMED (unchanged since the first referee; prover check re-run; GLOBAL wording now accurate) |
| Pairing P4–P5 | CONFIRMED (unchanged; mb_pair_3_9m wording repaired to "no plain descent certificate") |
| S3 | CONFIRMED; wording nit below |
| S5 | CONFIRMED (the "mechanism" sentence is now restricted to a = 5, and a = 7 with m ≤ 199) |
| S7 (PARTIAL, m ≤ 199) | CONFIRMED as PARTIAL |
| Minimal multi-class taming sets | CONFIRMED (independent hitting-set lower bounds + certificates) |
| Theorem D (repaired) | CONFIRMED (bound, refined scan, all exclusions simulated, all cycle lists) |
| Theorem M (repaired) | CONFIRMED (bound, scan extended to 400, q = 2 cycles (1),(2 3), q = 3,4,6,8 cycle (1)); scope nit below |
| Lemmas A', B' (+ refined), C', R, D'' | CONFIRMED |
| 20 PROVED systems | CONFIRMED (the 16 certified ones re-certified by my engine; the 4 pairing systems by P3 and the prover/first-referee checks) |
| OPEN entries | correctly labelled |

## Nits (no repair required)

1. **single_class.md, line 35.** The parenthetical says "other values of c ... are not excluded". Read literally, this contradicts S3's "whatever c is" necessity. What is meant is that for (3,2) and (9,8) only c = 1 is certified. Suggested wording: "S3 excludes descent certificates for every other (m, r) and every c; for (3,2) and (9,8) only c = 1 is certified, and non-descent arguments are not excluded."
2. **Theorem M scope.** "Two classes mod q (q ≥ 3)" silently omits the degenerate q = 2 with R = {0, 1}, where the whole map is replaced by ⌈n/2⌉. That case is trivially certified with cycle (1). The README sentence "they must be the odd class (q = 2) or {1, −1} mod q" should say "two classes of one common modulus q". Classes with different moduli are not covered, and the text never claims they are.
3. **Leaf counts.** These depend on the engine. They agree with mine, but they are not part of any proof.
4. The run times in the README are slightly higher than measured here. This is harmless.

## Novelty

The novelty statements are honest. K = 1, a = 3 is attributed to Farkas 2005. mb_pair_5_5m is flagged as the reflection of round-2 farkas5m_s27. Everything else says "novelty not checked". I did no web search either.

## Overall

The repair addresses every item of REFEREE.md correctly. The repaired necessity bounds are sound, and the refined Lemma B' is now tested on real integers for every exclusion. The corrected cycle lists are exactly right. Nothing is overclaimed beyond the two wording nits above. No repair is needed.
