# Round 3, lens "progressions": the arithmetic progression technique as a general theory

The round-2 split5_3 note and the q-family theorem back-trace along inverse branches to steer
ancestors into any residue class. Here that technique becomes a theorem for a whole class of
maps (**p-shift maps**: T(n) = (u_r n + v_r)/p on n ≡ r mod p^κ, p prime, p ∤ u_r, with the
dilation T(pn) = n), with an algorithm that computes the exact invariant and outputs a checkable
proof object. It is then applied to every census system of that shape.

## Theorems

| # | statement (short) | status | file | check |
|---|---|---|---|---|
| A | Progression theorem: under (A0) connectivity, (A1) dilation, (IA) a finite "initial accessibility" game, every merging class (divergent ones included) meets every progression allowed by an explicit invariant g; g is the finest finite-modulus orbit invariant and is computed exactly (translations in the loop group ⇒ modulus δ; groupoid classes mod δ). The 3x+1 case is known (K. M. Monks, Proc. AMS 134 (2006) 2861–2872) | PROVED | `theorem_A_sufficiency.md` | `check_theorem_A.py` |
| A' | Counterexamples showing hypotheses matter (p ∣ u; no dilation, where the conclusion fails for the 1932 map; two denominator primes) | PROVED | same §7 | same |
| B | Complete list of automatic labels: with a state-free invariant and one expanding cycle, a finite-valued orbit-invariant label is automatic in some base ⟺ it is a function of g ⟺ periodic mod d*. Basins of cycles sharing a class are automatic in no base, and no automatic orbit-invariant label (and no ultimately periodic set) separates them; no automatic set at all separates them when the two basins exhaust their class (S2). The literal "no automaton separates" for open systems is withdrawn (REFEREE1 GAP) | PROVED (as restricted) | `theorem_B_automatic_labels.md` | `check_theorem_B.py` |
| C | Counting: every merging class has ≫ X^σ members in every compatible progression, σ certified exactly from a weighted ancestor tree; σ for 32 systems; split5_3 improved from 0.238 to 0.42; m3_a reaches 1 − ε. Lemma C2 had a GAP (construction length grows with the U-valuation; 13 systems affected); repaired by Lemma C2' (bounded valuation) + Lemma R (valuation reduction), checked exactly; all σ unchanged | PROVED after repair (heuristic limits: EVIDENCE) | `theorem_C_counting.md` | `check_counting.py` |
| D | Density-zero sufficient sets S_T = {n ≡ 1 mod p^{k(n)}}, k(n) = ⌊log log n / 2 log L_U⌋: GLOBAL ⟺ eventual periodicity on S_T (5x+1, 7x+1, split5_1, split5_3, m3_b, …) | PROVED (thins only above ~10^11) | `sufficient_sets.md` §2 | `check_sufficient_sets.py` |
| E | Combination with descent: lemma PROVED; obstruction: cylinder descent certificates on a progression with p ∤ N are global, forward-invariant good-modulus progressions are unions of g-classes; no system settled by the combination was found | PARTIAL (negative) / OPEN | `sufficient_sets.md` §3 | same |
| P0, P | 1932 permutation: the only sufficient progressions are ℤ_{≥1} and 1 mod 2 (every orbit contains an odd number; the cycles (1), (2 3) exclude every N ≥ 3). The first version's "no sufficient progression can exist" was WRONG and is withdrawn. Replacement statement: an orbit is infinite iff it meets ≥ k+1 classes mod 3^k for every k | PROVED | `sufficient_sets.md` §4 | same |

## Systems and newly settled basin questions

Full table: `applications_basins.md` (data: `certificates.json`, `counting_results.json`).

| system | GLOBAL | exact invariant g | answer to "is there a finite-state basin rule?" | new? |
|---|---|---|---|---|
| m3_a = m3_c | settled | trivial | no, for both cycles (1), (2); no automatic set separates them; each basin ≫ X^{1−ε} in every progression | **new** |
| desc_s32_d65 | settled | gcd(n, 65) | basin of 65 = 65ℤ exactly; the 7 other basins non-automatic | **new** |
| 5x+1 | open | trivial | no (cycles 1, 13, 17); GLOBAL ⟺ eventually-periodic set automatic | **new** |
| 3x−1 | open | trivial | no (1, 5, 17) | **new** |
| 3x+5 | open | 5 ∣ n | no for the 5 unit cycles; (5 20 10) automatic ⟺ Collatz | **new** |
| 3x+13 | open | 13 ∣ n | no (9 unit cycles) | **new** |
| 3x+17 | open | 17 ∣ n | no (1, 23) | **new** |
| 5x+3 | open | 3 ∣ n | no (3+4 cycles) | **new** |
| 5x+7 | open | 7 ∣ n | no (3+3 cycles) | **new** |
| 5x+11 | open | 11 ∣ n | no (3+2 cycles) | **new** |
| split5_1 | open | trivial | no (1, 13) | **new** |
| m3_d / m3_e / m3_g | open | trivial | no (two cycles each); for m3_e: the merging class of 7 and the basin of {1,9,3} are non-automatic and no automatic orbit-invariant label separates them | **new** (3) |
| desc_m3_4n5 | open | trivial | no (3 cycles) | **new** |
| 3x+1, 7x+1, split7_1, s32_plus9, m3_b | open | trivial | single known cycle: GLOBAL ∧ no other cycle ⟺ basin automatic | reformulation |
| split5_3 | open | 3 ∣ n | reproduces round 2 | – |
| split_5/13/73/97/7081, splitB_7/71, par_1_5 | settled | ⟨2,3⟩-classes mod d | reproduces census / concurrent lens `../deep` | – |
| qrB7_c53 | settled | squares mod 7 | invariant reproduced; Theorem B inapplicable (no expanding cycle), consistent with its known 20-state automaton | – |
| 5x+5, 7x+7, 3x+3, 3x+9 | open | – | (IA) fails; not covered | – |
| div23_5n1 | open | – | not a p-shift map; OPEN (evidence only) | – |

That is 15 newly answered basin/automaticity questions (counting m3_d, m3_e, m3_g separately).
"no" means: the basins are not automatic in any base and no automatic orbit-invariant label
separates them; for open systems this does not exclude a non-invariant automatic set that
separates the two basins while misbehaving on unknown orbits (Theorem B, separators).

## Files

* `plib.py` — exact core: p-shift maps, moves, loops, commutator translations, groupoid classes,
  minimal invariant, IA game, discrete logs.
* `systems.py` — the systems (census maps in shortcut form, raw rules recorded; cycles found by
  search where GLOBAL is open).
* `certify.py` — the algorithm of Theorem A; writes `certificates.json` (the proof objects).
* `construct.py` — the proof of Theorem A executed: builds an explicit merging start in any
  progression; `verify` replays it exactly.
* `counting.py`, `run_counting.py` — Theorem C certificates; writes `counting_results.json`.
* Theorem files and checks as in the tables. All checks are exact, exit 0, and run in a few
  minutes each with `nice python3 check_*.py`.

## Honest limits

* Theorem A needs the p-shift shape with a dilation branch; div23_5n1, the q-family (two
  denominators) and permutations are outside it (the q-family is covered by the earlier
  Theorem F of `../../lhf/q17-family/CLS-057.md`). Whether (IA) can be dropped is OPEN.
* Theorem B's base-p case needs a cycle with an expanding step; qrB7_c53 shows this is necessary.
* Theorem D is qualitative: S_T contains everything below about 10^{10.9} for 5x+1.
* No system was settled by "sufficiency + descent on a progression" (§3 of `sufficient_sets.md`).
* Novelty: the 3x+1 case of Theorem A (every arithmetic progression is sufficient) is
  K. M. Monks, *The sufficiency of arithmetic progressions for the 3x+1 Conjecture*, Proc. AMS 134
  (2006) 2861–2872 (citation and statement read in the introduction and bibliography of
  arXiv:1204.3904; the PAMS article itself not read). Monks–Monks–Monks–Monks (arXiv:1204.3904)
  give low-density sufficient sets for 3x+1. Everything else: novelty not checked.

## Revision after REFEREE1

* Theorem C: Lemma C2 restated for bounded U-valuation (C2'); new Lemma R reduces every vertex of
  the 13 affected systems to an ancestor of bounded valuation (exact check + enterability of all
  residues mod L2 in `check_counting.py`). Exponents unchanged and now proved.
* 1932 map: "no sufficient progression" withdrawn (WRONG); replaced by Proposition P0 (exactly
  ℤ and 1 mod 2), proved and checked in `check_sufficient_sets.py`.
* Theorem B: separator clause restricted to orbit-invariant labels / ultimately periodic sets,
  plus (S2) for classes exhausted by two basins; m3_e item 13 reworded.
* Theorem A item 3: example progression corrected (gcd(N, p^{κ−1}d*) = 1), tested on 33 systems.
* Lemma 5 ball-growing step expanded; Monks (2006) cited as the known 3x+1 case.

## Revision after REFEREE2

REFEREE2 confirmed every claim and found no new gap. Two small additions were made afterwards:
Theorem C now states the hypothesis that g is state-free (its proof uses it in the first step), and
`check_theorem_C_hypotheses.py` asserts state-freeness and gcd(W, d*) = 1 for all 32 systems
(REFEREE2's nit). No exponent changes.
