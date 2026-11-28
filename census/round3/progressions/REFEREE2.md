# REFEREE #2 report: lens "progressions" (after the REFEREE1 repairs)

Referee: independent referee #2 (adversarial verification, not new research). No prover file was
modified. My files: `REFEREE2.md` (this report) and `referee2_check.py` (an independent check
written from scratch; `nice python3 referee2_check.py` takes about 60 s and exits 0).

## What I ran

* The prover's five checks all exit 0 (`check_theorem_A.py` 110 s, `check_theorem_B.py`,
  `check_counting.py`, `check_sufficient_sets.py`, `check_applications.py`).
* **The prover's checks can fail.** I ran them on a copy in my scratchpad, never in the folder:
  - Raising split5_1's weighted σ to 0.80 in a copy of `counting_results.json` makes
    `check_counting.py` exit 1 with "FAIL: certificate split5_1 weighted".
  - Altering the 1932 table in a copy of `systems.py` makes `check_sufficient_sets.py` exit 1.
    This one fails by an exception, not by a FAIL line, which is acceptable.
* **`referee2_check.py`** does not use the prover's code for the maps, the tree children, the (W)
  inequality, the IA game or Lemma R. It reads only the certificate data (W, H, G, σ, weights)
  and compares against `plib`/`systems` where noted.
  1. It re-defines 18 maps from the raw census rules and derives the shortcut tables itself. It
     checks Lemma 0 (S(n) ∈ {R(n), R²(n)}) on 54 000 random n < 10^15 and finds that the maps and
     tables are identical to `systems.py`. The definitions in the .md files, `systems.py` and the
     checks agree.
  2. It re-implements the IA game from §4 of `theorem_A_sufficiency.md`. The live set and the
     enterable residues are identical to `plib.ia_game` for all 18 systems. Every residue mod L2
     is enterable in the 13 Lemma-R systems.
  3. **Lemma R** is re-derived with its own move search for each p-unit state. It confirms the
     table in §2 of `theorem_C_counting.md` row by row: V_R ≤ 1, h_max ≤ 4, and for d65 and
     plus9 the moves are I moves with h ∈ {0, 1, 4}. It also runs 12 800 random vertices with
     v_ℓ(z) up to 90. In each it checks exactly that c is an integer, a p-unit and positive, that
     S(c) = p^h z, that S^{h+1}(c) = z, that v_ℓ(c) = v_ℓ(v) − v_ℓ(u) ≤ V_R, that c ≤ p^{h+1} z,
     and that c is enterable.
     **Exhaustive counterexample hunt:** for every p-unit z ≤ 20 000 + max|v| with
     v_ℓ(z) > V_R, a direct search over all preimages (not using the table move) finds an
     ancestor of valuation ≤ V_R within h ≤ 4. The first run of this hunt reported 1 failure for
     split_97 and 37 for split_7081. All of them are small z with p·z ≤ v_r, where c = 4z − d ≤ 0.
     That is exactly the excluded range of Lemma R ("c > 0 once p^{h+1} z > v_r"), and Theorem C
     uses only large leaves. So these are not counterexamples. The check now restricts to p·z > v.
  4. The case split of Theorem C (case (a) bounded vs case (b) via Lemma R) independently gives
     19 and 13 systems, the same 13 as the prover. It also checks that gcd(W, d*) = 1 for all 32
     certificates, which the proof of Theorem C needs and `check_counting.py` does not check
     explicitly. It also checks that G consists of p-units.
  5. **(W) re-verified exactly** with an independent child enumeration, for 18 certificates
     (uniform and weighted) of m3_a, split5_1, desc_s32_d65, split_5, par_3_1, par_5_1, m3_e,
     split5_3 and desc_m3_4n5. The enumeration covers every lift ζ mod W·lcm(u), every
     (r, h ≤ H) passing the state and U-domain conditions with ρ > 1, and an exact replay
     S(c) = p^h z on a concrete large lift. Each q has an exact rational bound
     q^t ρ'^s ≤ 1 with ρ' = ρ·1001/1000. Every certificate holds, with a minimum slack ratio
     between 1.0017 and 1.0177. A negative control (split5_3 at σ = 0.6) fails as it should.
  6. m3_a σ → 1: exact certificates with ρ' = ρ (no ε factor) at σ = 99/100 (40 children, sum
     1.0096) and at σ = 999/1000 (400 children, sum 1.00096). It also checks on 2000 random z
     that there is exactly one child per h, that the child is a 3-unit, and that z < c < (3^{h+1}/2)z.
  7. 1932 map:
     - Every n ≤ 3·10^5 reaches an odd value, with exact descent on 3q.
     - Among all progressions with N ≤ 60, exactly (0 mod 1) and (1 mod 2) meet both (1) and (2 3).
     - Injectivity holds on [1, 3·10^5).
     - For 300 random period words W, the cylinder of W⁴ is a single class mod 3^{4L}. This is
       the Proposition P step.
  8. m3_a, (S1)/(S2) data: every n ≤ 2·10^5 reaches 1 or 2, and both basins occur in every class
     x mod q for q ≤ 60, beyond 10^5. This is EVIDENCE only, since the (S1) proof is via Theorem A.

## Verdicts

| claim | verdict | notes |
|---|---|---|
| Theorem A | CONFIRMED | REFEREE1's three fixes are all made. (1) Item 3 now reads gcd(N, p^{κ−1}d*) = 1. By CRT such a progression meets every residue mod p^{κ−1}d*, on which g depends, so it meets every g-class; correct. (2) §7 now cites P0. (3) Monks (2006) is cited, with an honest statement that the PAMS article was not read. The expanded Lemma 5 is correct: D/I words depend only on the state; for the E move the ball lies in or contains the domain coset; the image contains the centre's outcome set, so a live re-centring exists. The new remark that the ball radius depends on v_ℓ(y) is correct and is exactly what C2' needs. I did not re-derive Lemmas 1–4 and 6 line by line, since REFEREE1 did and they are unchanged; my IA game re-implementation agrees with plib on 18 systems. |
| Theorem A' (counterexamples) | CONFIRMED | The "no sufficiency statement" sentence is withdrawn. For the 1932 map the conclusion of Theorem A fails (the cycle (1) is a merging class missing most progressions, while the finest finite-modulus invariant is trivial per the cited census file). n/2–2n and div2_3n are unchanged. |
| Theorem B (1)⇔…⇔(4), (S1), (S2) | CONFIRMED | (S1): an ultimately periodic separator would contain large members of basin(C′) in n + qℤ, by Theorem A in the same g-class. (S2): A ∩ {g = γ} = basin(C) when the two basins exhaust the class; {g = γ} is periodic, hence automatic in every base, so A automatic implies basin(C) automatic, a contradiction. The literal open-system claim is withdrawn. For m3_a the exhaustion is elementary, not just cited: T(n) < n for n > 2, so the only cycles are (1) and (2). For desc_s32_d65 it rests on the refereed round-2 GLOBAL result. |
| Theorem C (32 exponents) | CONFIRMED | Lemma R is correct as stated. The proof is fine line by line: U = {ℓ} makes u_r a power of ℓ, and v_ℓ(u_r) ≤ v_ℓ(v_r) < v_ℓ(z) gives the U-domain condition; the state condition is p^h σ ≡ B_r(r) (mod p^{κ−1}); and v_ℓ(c) = v_ℓ(v_r) − v_ℓ(u_r). C2' is correct for bounded valuation: the initial ball is determined by z mod ∏ ℓ^{J_ℓ+V+1}. The proof of Theorem C correctly composes C1, R and C2': the extra iterate count h_max + 1 and the factor p^{h_max+1} only change constants, and multiplicity is ≤ J_V + h_max + 2. Its hypothesis "W coprime to d*" holds for all 32 certificates (checked here). All 13 case-(b) systems have every residue enterable (independent IA game). The (W) inequalities hold for the 18 certificates I re-verified, and the prover's check covers all 64 exactly. For m3_a, ≫ X^{1−ε} for every ε > 0 holds, with c(H, P) depending on ε. |
| Theorem D | CONFIRMED | Unchanged since REFEREE1. I re-read the bound: y0 is fixed per class and h ≤ C·k·L_U^k, so log log n_k ≤ k log L_U + log k + C < 2k log L_U for large k. |
| E (combination; obstructions) | CONFIRMED (PARTIAL, honestly labelled) | The combination lemma and both obstructions are correct. No system is claimed. |
| Proposition P0 (1932) | CONFIRMED | The proof is complete. Odd values are forced because a run of 3q values strictly decreases. Meeting (1) and (2 3) forces N \| 2. GLOBAL ⟺ every odd n periodic uses bijectivity correctly. |
| Proposition P (complexity) | CONFIRMED | Morse–Hedlund step: c(1) ≥ 2 plus strict increase gives c(k) ≥ k+1. Integrality step: 3^{Lj} \| a^j m with 3 ∤ a forces m = 0. The proof needs p ∤ u_r, which is part of the p-shift definition (the 1932 slopes are 2 and 4). |
| m3_a (=m3_c) | CONFIRMED | Trivial invariant, non-automatic basins, no automatic separator by (S2), and ≫ X^{1−ε} by case (b). |
| desc_s32_d65 | CONFIRMED | Basin of 65 = 65ℤ; seven non-automatic basins; (S2) for {1,7} and {5,1135}; σ = 0.772 via case (b). |
| 5x+1 | CONFIRMED | "Automatic iff everything" is correct because the set contains 1 and the invariant is trivial. |
| 3x−1 | CONFIRMED | |
| 3x+5 | CONFIRMED | (5 20 10) is automatic ⟺ basin = 5ℤ ⟺ Collatz, since 3x+5 on 5ℤ is conjugate to 3x+1. |
| 3x+13, 3x+17 | CONFIRMED | |
| 5x+3, 5x+7, 5x+11 | CONFIRMED | |
| split5_1 | CONFIRMED | X^0.692 is restored by case (b), Lemma R with c = 4z − 1. |
| m3_d, m3_e, m3_g, desc_m3_4n5 | CONFIRMED | The m3_e item 13 is now correctly restricted to merging classes and labels. |
| 3x+1, 7x+1, split7_1, desc_s32_plus9, m3_b | CONFIRMED | Reformulation via Theorem B; Monks is cited. |
| perm_1932 | CONFIRMED | The WRONG claim is withdrawn and replaced by P0 and P. |
| split5_3, split_d, splitB, par_1_5, qrB7_c53 | CONFIRMED | σ = 0.42 for split5_3 was re-verified independently (slack 1.0022). |
| div23_5n1 | CONFIRMED (EVIDENCE label is honest) | |

## Minor remarks (no repair required)

* Lemma R holds only for p^{h+1} z > v_r, and the text says so. My first hunt found exactly
  these small-z exceptions (split_97, split_7081), so the qualifier is load-bearing. It is
  already stated.
* `check_counting.py` does not assert gcd(W, d*) = 1, which the proof of Theorem C uses. It
  holds for all 32 certificates (checked in `referee2_check.py` §4). Adding the assert would make
  the check self-contained.
* The construct-based "ball words bounded" test in `check_counting.py` is an illustration, as the
  text says. The proof of C2' does not depend on it.
* Novelty: the Monks (2006) citation (Proc. AMS 134(10), 2861–2872) matches what I know of the
  paper's title and venue; I did not re-fetch it. All other novelty statements say "not checked"
  and claim nothing more.

## Overall

Every item REFEREE1 marked GAP or WRONG is repaired correctly:
* Theorem C by Lemma C2' and Lemma R;
* the 1932 claim by P0;
* the Theorem B separator clause by (S1) and (S2);
* the item-3 example;
* the Monks citation.

I found no new GAP or WRONG claim, and no counterexample on fresh inputs. needs_repair = false.
