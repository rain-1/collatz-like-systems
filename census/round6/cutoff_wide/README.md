# Round 6, lens `cutoff_wide`: the shift-and-subtract (S-unit) cutoff, ported and aimed at candidates

**Outcome: no system was settled.** Two general theorems were proved.

1. **Theorem W** (`theorem_W.md`): the whole-prefix cutoff of split5_3 holds for every path of
   two-prime affine steps whose events have bounded labels, bounded slope at events, at most J
   pieces with hereditary shift invariance or bounded period, and jumps of any size between
   pieces. Such a path has at most (1 + o(1)) log_p |y| divisions from a start y. It is
   instantiated for 13 census systems and families plus the three controls.
2. **Theorem P** (`theorem_P.md`): in every unit-multiplier system with a type-(c) component, the
   non-descending p-adic set has positive Hausdorff dimension. The rigid families covered by
   Lemma R's rotation families have only polynomially many words (Lemma Q). General (H4) shift
   pieces in block-word normal form have 2^{o(E)} words (Lemma Q', added after REFEREE1). So
   they are an exponentially small fraction. Conversely, dimension 0 holds exactly when there
   is no type-(c) component. Theorem H then settles the system, under its hypotheses: unit
   multipliers, the standing hypothesis, and that positive integers map to positive integers.

So the reduction asked for in part (2), "every long non-descending path is rigid", is false at the
cylinder level for every type-(c) system, for rigidity in block-word normal form (one expanding
cycle, distinct-label exits; Corollary P1). The same holds for the blocked mixed-base system
(Proposition B). No designed type-(c) table can have it in that normal form (that its
non-descending set cannot be countable is fully proved, since the dimension is positive). The
cutoff method therefore cannot be completed into a decision of any system in this class by a
cylinder-level rigidity reduction in block-word normal form. Rigidity for paths outside that
normal form (several expanding cycles, exits with coinciding labels, other decompositions) is not
covered. (Restriction added after REFEREE2.)
Arguments that use the integer start beyond its digit horizon are not excluded.

All work is agent-written. It was examined by two referees (REFEREE1.md, REFEREE2.md) and
repaired; see "Revision after REFEREE1" and "Revision after REFEREE2" below. Novelty was not checked, for Theorem W or for Theorem P.
Section 6 of `theorem_W.md` notes that the single-schedule form is probably a known
consequence of the p-adic Subspace Theorem. Theorem P is elementary, and for 3x+1 its
conclusion is presumably classical.

## Results

| system | technique | result | status |
|---|---|---|---|
| any two-prime affine path (H0-H4) | Theorem W (Evertse Thm 2, eq. (14), T = {p}) | E <= (1 + eta) log_p\|y\| for \|y\| >= y_*(eta, ...), ineffective; coefficient 1 sharp | PROVED (uses Evertse (14), verified against the scan by referee 1; (H0) and prefix-(H3) added after REFEREE1) |
| rotation schedules C^{k_i} X_{lambda_i}, equal-slope exits | Lemma R | satisfy (H4) with M(delta) = 2(2J+1)(1/delta + 2), gamma within [lambda_C^{-1}, lambda_C] | PROVED (window argument repaired after REFEREE1) |
| 3x+1 (Terras) | Theorem W instance | rigid paths around -1 (kappa = log2/log1.5 = 1.7095 per exit; 0.7095 per block "10") have <= (1+o(1)) log2 y halvings; no free labels exist on its near-critical schedule | PROVED; exact identity checks; lift ratios 0.98-1.00 (EVIDENCE) |
| 3x-1, 3x+5 (controls, extra cycles) | Theorem W instance | same around x* = 1 (a real positive cycle) and x* = -5. Expanding cycles such as 5, 7, 10 satisfy (H0)-(H4) from the bounded start \|y_0\| = 4. They are consistent with Theorem W only because y_* is ineffective, so nothing about cycles is claimed. (The earlier "cycles fail (H2)" is withdrawn.) | PROVED / checks |
| 5x+1 (control, divergence expected) | Theorem W instance | rigid paths around -1/3 (kappa = 0.7565) are short. No convergence claim; H = 1 | PROVED / checks |
| K7 and cores {5,7}, {1,5,7}, {3,5,7}, {1,7}, W | Theorem W instances | rigid paths around -1 are short | PROVED |
| cores S = {1,3}, {1,3,5} mod 8 (obstruction -5, slope 9/8) | Theorem W instance; Theorem P | rigid paths around -5 are short. Non-descending word count grows like p^{HE} with H = 0.428 and 0.359 base-2 digits per halving (H is the word-count exponent, an upper bound for dim_H), corrected after REFEREE1 (was 0.457, 0.376). These are the smallest among the type-(c) (open) unit-multiplier systems computed here and in round4/lundberg (that table also has acc_h16, type (b), with dimension 0). Explicit non-descending code {U, V}^* with dimension >= 0.020 and 0.011 | PROVED (P, W); H values EVIDENCE |
| split5_3, split5_1 | Theorem W instance; Theorem P | reproduces the repo cutoff for split5_3; H = 0.5807 and 0.9369 agree with rounds 3 and 4 | PROVED; H EVIDENCE |
| m3_b (p = 3, l = 2) | Theorem W instance; Theorem P | rigid paths around the fixed point 1 (lambda = 4/3, kappa = log3/log(4/3) = 3.8188 per exit) are short; H = 0.965 | PROVED; H EVIDENCE |
| mb_s3_27 (26 mod 27 -> (n+1)/27 on 3x+1) | skew product over Z/27 (Prop. B); Theorem W instance | never-blocked paths are Terras words times a Z/27 automaton. The cycle -5, -7, -10 has free re-entry (W = 010), giving a positive-dimension code (>= 1/84 in each class s = 0, 1 mod 3), so survivors are not rigid. The 9 classes s = 2 (mod 3) have no non-descending point (prefix slope < 1 within 3 steps). Rigid sub-families are short | PROVED (exact check); entropy fit 0.32 EVIDENCE |
| designed type-(c) tables with rigid re-entry (part 2c) | Theorem P + Lemmas Q, Q' | impossible at the cylinder level in the unit-multiplier class, for rigidity in block-word normal form (one expanding cycle, distinct-label exits); countable is impossible outright: type (c) gives 2^{E/e} non-descending words, rigid block-word families give poly(E) (Lemma R pieces) or 2^{o(E)} (general (H4) pieces) | PROVED |
| every open census system | all of the above | nothing settled | - |

## What the ineffective constant gives

Theorem W has the form "for all sufficiently large |y|", with no explicit threshold. It excludes
long rigid paths from large starts and nothing else.

* It does not exclude escaping orbits, because no theorem forces an escaping orbit to contain
  long rigid stretches.
* It says nothing about cycles. Expanding integer cycles *satisfy* (H0)-(H4) from bounded
  starts, and they are compatible with Theorem W only through the threshold y_*. So Theorem W
  cannot exclude any finite set of cycles. (Revision after REFEREE1: this line said cycles
  "fail (H2)". That is withdrawn. Only contracting cycles fail (H2).)
* It gives no explicit octave, so no finite computation can complement it.

Even if a full rigidity reduction were available, the ineffective constant would only give "no
escaping orbit". The cycle list would still need a separate argument.

## Files

| file | content | run time |
|---|---|---|
| `theorem_W.md` | general theorem, hypotheses and their roles, full proof, Evertse quotation, Lemma R, instance table, what is not ported | |
| `theorem_P.md` | Theorem P and its converse, Lemma Q, Corollary P1, Proposition B (mb_s3_27), entropy table | |
| `cwlib.py` | exact library: table systems, cylinder graphs, walk classes (CRT), cycle lemma, re-entry search | |
| `check_entropy_code.py` | for 15 systems: expanding cycle, rotation, re-entry, code {U, V} with all prefix slopes > 1, realizability by direct integer iteration, dimension bound | 1 s, exits 0 |
| `check_cutoff_instances.py` | for 15 systems: shifted forms, identity (1) on actual orbits, exact pairing decomposition, Lemma R exception bound (half-open form), lift ratios (EVIDENCE, asserted > 0.8); Lemma R window inequality; expanding cycles of 3x-1 and 3x+1 satisfy (H0)-(H4) from bounded starts | 4 s, exits 0 |
| `check_mb_s3_27.py` | skew-product lemma, CRT realizability, the code for the -5 cycle, entry words from every class s = 0, 1 (mod 3), descent of every class s = 2 (mod 3), rigid instance and identity, never-blocked counts | 1 s, exits 0 |
| `count_nondesc.py` | exact counts N(E) of non-descending cylinder words and the variational exponent H; `--check` compares the DP with direct residue enumeration (exits 0/1); `--hcheck` checks the stated H values against the variational minimum (grid [0, 12], minimizer interior) and the exact-count fit at E = 600 (exits 0/1); with an integer Emax it prints the table | <1 s (`--check`); about 10 s (`--hcheck`) |
| `REFEREE1.md`, `referee1_check.py` | referee report and the referee's independent check (not edited by me) | about 30 s |

Each check fails loudly (exit 1) if any exact assertion fails. The H values and the lift ratios are
floats and are labelled EVIDENCE.

## Honest limits

* **Evertse's statement.** I downloaded Evertse (1984) and extracted the text of Theorem 2, but
  my extraction could not read the displayed inequality (14). Referee 1 rendered pp. 226 and
  228 of the Numdam scan and confirmed the display as quoted: the hypothesis that every
  nonempty subsum is nonzero, C depending only on (epsilon, S, K, n), and the height
  max_k |x_k| for K = Q. The verification is the referee's, not mine. The theorem is used only
  with a bounded number of terms, so the constant is uniform.
* **What is ported.** Theorem W covers bounded-geometry pieces with bounded-ratio shifts, plus
  geometric pieces. The split5_3 results with unbounded rates, two-phase linking,
  complementary/multi-shift linked labels, the separation theorem and the free-label power bound
  are **not** re-proved in general here. They are only cited for split5_3.
* **Theorem P's dimension bounds are weak** (0.01 to 0.33). They only prove positivity. The
  realistic exponents H come from exact counts and a float variational formula (EVIDENCE).
* **Proposition B** handles only the never-blocked paths of mb_s3_27. This gives a lower bound for
  its non-descending set, which is all the negative answer needs.
* **No candidate is settled**, so no cycle lists are claimed.

## What stayed open

* Any rigidity reduction that uses the integer start beyond its digit horizon. By Corollary P1
  this is the only kind that could work, and it is the count-law problem (round4/lead, round5).
* Covering a positive fraction of the non-descending entropy of any system by an S-unit cutoff.
  The best proved linked-label families (split5_3 multi-shift) have exponent below 0.04 per
  division (log_2 3/(6T) = 0.0366 with T = 7.2126), against H >= 0.36 for the most rigid
  candidate computed (core S = {1,3,5} mod 8, H = 0.359).
* General-setting versions of the linked-label and free-label theorems (mechanical, not attempted).

## Revision after REFEREE1

The referee found no false settled claim. Nothing was settled, and nothing is settled now. The
referee did find one wrong number pair, one wrong explanation, two proof gaps and several
overstatements. Each item and how it was handled:

| referee item | verdict | action |
|---|---|---|
| Evertse Thm 2 (14) quoted "from memory" | CONFIRMED by referee from the scan | "from memory" removed; the verification is credited to the referee (theorem_W.md section 4, Honest limits) |
| Theorem W truncation step: e_max undefined, (H3) not hereditary | GAP | added (H0): e_j <= C, and (H3) for every prefix; truncation now argued hypothesis by hypothesis; checked that every instance satisfies both (theorem_W.md sections 2, 3, 6) |
| n_terms count | minor | corrected to 2J/delta short-piece singletons |
| Lemma R window count "<= 1/delta + 2" | WRONG step, conclusion survives | replaced by the half-open-arc argument: at most 2J + 1 exceptions per window, at most 2/delta + 1 windows; M(delta) unchanged. Check: window inequality exactly for delta = 1/5..1/40, and the sharper per-window bound on all instances |
| split5_3 kappa 6.2126 | WRONG number | corrected to 3.1063 (6.2126 = 2 kappa) |
| "cycles fail (H2)" | WRONG | **withdrawn** in README and theorem_W.md. Expanding cycles satisfy (H0)-(H4) from bounded starts; only y_* keeps them consistent with Theorem W, so it can exclude no finite set of cycles. New exact check `cycle_check` (3x-1: 5,7,10 and the 17-cycle; 3x+1: -5,-7,-10 and the -17 cycle) |
| H for core13, core135 (0.4565, 0.3755) | WRONG | **corrected** to 0.4281 and 0.3593 (crit 1.75, 1.56). Cause: theta grid stopped at 3. Grid now [0, 12] with an end-point guard; new `--hcheck` mode. No qualitative conclusion changes |
| Theorem P item 4 needs e <= 1 | GAP | restated for general e_max, with 2^{floor((E-1)/e*)} walks in intervals of p^{K+E+e_max-1}; proof now uses that division-free nodes have out-degree 1 |
| Corollary P1 counted only Lemma R families | overreach | new Lemma Q' (general (H4) shift pieces, 2^{o(E)} words, block-word normal form with distinct labels); Corollary P1 restricted to that normal form; caveat for coinciding labels stated |
| Proposition B "each 27-class" | WRONG | the referee's fix "each class != 26" is **also false**: the 8 further classes s = 2 (mod 3) have a prefix slope < 1 within 3 steps (exhaustive and direct check). Statement now: dimension >= 1/84 in each of the 18 classes s = 0, 1 (mod 3); entry words found by the check |
| README "Theorem H already settles" | missing hypotheses | Theorem H's hypotheses now stated |
| "cutoff cannot by itself decide any system" | overstated | now "cannot be completed by a cylinder-level rigidity reduction" |
| "escaping code / family" | misnomer | now "non-descending family"; nothing is shown to escape |
| "smallest in the census" | unsupported | restricted to systems computed here and in round4/lundberg |
| "below 0.03" | wrong number | now "below 0.04" (0.0366) |
| novelty caveat only for Theorem W | incomplete | extended to Theorem P (theorem_P.md, Novelty) |

All four of my checks exit 0 after the revision: `check_entropy_code.py`,
`check_cutoff_instances.py`, `check_mb_s3_27.py`, and `count_nondesc.py --check` and
`--hcheck`. The checks can fail, and both new ones were seen to fail on the old claims.
Running `--hcheck` with the old grid [0, 3] exits 1, because the end-point guard fires at
core13. The original Proposition B claim, an entry word from every class, failed the new
check on the 8 classes s = 2 (mod 3) other than 26. The referee's independent check
`referee1_check.py` also exits 0.

## Revision after REFEREE2

The second referee (`REFEREE2.md`, own check `referee2_check.py`) confirmed every proof and every
REFEREE1 repair except one leftover of REFEREE1 item 10 in the headline wording. Wording fixes
only; no mathematics, number or status changes.

| referee item | action |
|---|---|
| Headline overstates Corollary P1 (README "Outcome" paragraph; theorem_P.md introduction and the paragraphs after Corollary P1) | restriction added in all three places: rigidity is excluded **in block-word normal form (one expanding cycle, distinct-label exits)**, which is what Corollary P1 proves. "Countable is impossible" is fully proved by Theorem P and is now stated separately. Paths over several expanding cycles, exits with coinciding labels, or other decompositions are not covered. The part (2c) row of the results table carries the same restriction |
| H called the Hausdorff dimension (`count_nondesc.py` docstring, README core row) | H is now described as the growth exponent of the non-descending word count, N(E) ~ p^{HE}, an upper bound for dim_H (dim_H N_inf <= liminf log_p N(E)/E) |
| "smallest among ... round4/lundberg" | restricted to the type-(c) (open) systems; the lundberg table also contains acc_h16 (type (b), dimension 0) |
| mb_s3_27 "multipliers are not all units" (theorem_P.md, Proposition B) | corrected: 3, 1 and 1/27 are 2-adic units; the trichotomy does not apply because the branch condition is mod 27, not 2-adic |
