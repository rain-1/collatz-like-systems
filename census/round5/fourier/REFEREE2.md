# Referee 2 report: round 5, lens "Fourier and Diophantine formulation" (second pass, after the repair)

Referee: an independent agent, 27 Nov 2026. I did not edit any of the prover's files and I did not commit
anything. The only file I added is my own check script, `referee2_check.py`.

## How I checked

**My own script.** `referee2_check.py` was written from scratch and imports nothing from the prover. It
simulates the node rule for 3x+1, 3x-1, 3x+5, K7 and split5_3 directly on x mod 2^s, ranks slopes exactly
with Fractions, and computes the constants D' with integer prefix sums. It calls the prover's `rb` only in [R],
to compare bitmaps, and the prover's `exact_u.py` only in [D], to compare constants at L = 12.

- Default run: about 30 s, exits 0.
- `--full` run: also computes D'_{14} over all odd units, D'_{16,1} for 3x+1, exact counts up to b = 24, and
  node checks at b = 24. Its result is recorded at the end of this report.
- The script can fail. These conditions are required to hold, so a regression would trip them:
  - [N](a): the 3x+1 node deviations must exceed 0.25 D'.
  - [N](b): for split5_3 at b = 22, the constant computed with the unit group {1} instead of <5> must be
    violated. The observed ratio is 1.050. This shows that the maximum over units in U' does real work.
  - [D], [U] and [W] are exact equalities or inequalities against quoted numbers.
- An earlier draft of my mutations failed for the wrong reason: I had guessed that the worst node would reach
  0.5 D'. I replaced them with mutations that are known to bite. That was a defect in my script, not in the
  prover's work.

**The prover's checks.** I ran them all:

| script | exit code | time | notes |
|---|---|---|---|
| `check_fourier.py` | 0 | 2.2 s | |
| `check_revision.py` | 0 | about 1 min | output identical in substance to `check_revision_full.txt`, minus the `--full` items |
| `revision_n3.py` | 0 | | output byte-identical to `revision_n3.txt` |

## Were the REFEREE1 items resolved honestly?

| item | resolution | verdict |
|---|---|---|
| A (the F4 consequence) | F4' and Proposition Mod (R-A) replace the invalid derivation. Every place that drew the consequence from F4 now carries a [revised] pointer. | resolved |
| B (exact constants) | Theorem U' (R-B), with integer constants. | resolved, and extended to K7 and split5_3 |
| C (F3: consistent eps, general X) | F3' (R-C). The table now has (1/2 - 2 eps). | resolved |
| D (G and E_0) | E_0 is restated for the actual-drop count. The wording now says "the inference is invalid". | resolved |
| E (N1, N3) | N1 is now a range. N3 now notes the mod 2^{b-w} symmetry. | resolved |

The prover also found and corrected two errors that REFEREE1 had missed:

- N2 had said "10 to 50 times the random baseline". Those are ratios to |R_b|^{-1/2}. The correct ratios to the
  random baseline are 2.3 to 13.
- The N3 claim for split5_3 is withdrawn.

Both corrections are right; I checked them against `decay.txt` and `revision_n3.txt`. The revision log is
complete and candid.

## Verdicts

| id | verdict | note |
|---|---|---|
| F1 | CONFIRMED | Re-derived. Annihilation for v_p(xi) >= m is a full character sum. |
| F2 | CONFIRMED | Standard Weyl/portmanteau argument. No novelty is claimed. |
| F3 / F3' (conditional on H) | CONFIRMED | Re-derived the block decomposition, the per-block bound C\|R_b\|^{1/2+eps} and the exponent bound -eps h b + o(b). Remark below. |
| F4 | CONFIRMED | Jordan inequality, \|xi\| <= Z < p^m, Fejer kernel. Its consequence is correctly marked as superseded. |
| F4' | CONFIRMED | Choosing t in R_b gives N_t >= 1. [A] checks it on five systems at b = 14. |
| Mod | CONFIRMED_WITH_FIX | Correct. One side remark in (ii) is false. Fix 1. |
| T | CONFIRMED | Re-derived. [T] checks it exactly with Python integers for 3x+1, K7 and split5_3 at (j, L) = (7, 7) and (9, 6). |
| U | CONFIRMED | Unchanged since REFEREE1. |
| U' | CONFIRMED | See below. |
| U' siblings (3x-1, 3x+5, slope sense) | CONFIRMED | Proof by conjugation x -> dx. [U] checks exact counts for b = 14..22, with largest ratio 0.053 for 3x-1 and 0.146 for 3x+5. The theorem says nothing about cycles, so it proves nothing false. |
| Z | CONFIRMED | [Z] checks b = 4..22 exactly. It is honestly labelled as in-horizon. |
| S | CONFIRMED | Unchanged. |
| G ("the inference in CONJECTURE.md is invalid") | CONFIRMED | |
| E_0 => M' | CONFIRMED | Re-derived. Needs b <= K log n (n >= p), N_act - #Exc >= 1 and (1-h)C* = 1. The statement that the cycle minima of 3x+5 (1, 19, 23, ...) are not slope survivors is correct: 19 has slope 27/32 after one period. |
| sandwich comparison (R-B) | CONFIRMED | [W] recomputes `sandwich.txt` for b = 16..22 (24 under `--full`). "U' better for m = 2, 3 at every b" holds, narrowly at b = 20, m = 2 (0.2911 against 0.2844). |
| N1, N2, N4 (EVIDENCE) | CONFIRMED | They match the output files. |
| N3 (EVIDENCE) | CONFIRMED | I re-ran `revision_n3.py` and checked several (b, v) rows of a against (b - v) log_3 2 - 1 by hand. |
| Literature (section 7) | CONFIRMED_WITH_FIX | Shmerkin and Wu: hypotheses missing. Fix 2. |
| E, E_bdd, H | OPEN / EVIDENCE | Correctly labelled. |

### Theorem U' in detail

**The proof.** I re-derived it line by line:

1. Write r = r1 + p^j t with j = b - L. Then r < k p^{b-m} if and only if t < k p^{L-m}, because r1 < p^j.
2. Lemma T turns the condition on r1 + p^j t into a membership of U t + x' in an allowed set.
3. The unit U = u0^a lies in G.
4. Full sets contribute exactly their expected share. Every other node deviates by at most D' times its
   expected share.
5. Summing over nodes gives |N - X P(b)| <= D' X P(b).

There are no gaps.

**Stuck states.** For K7 and split5_3 the claim that the stuck states are exactly (0,0) and (1,1) holds in
general: with s >= 2 known digits every row is decided, and with s = 1 a row is decided only for an even
digit. [S] checks this at depth 14.

**The constants, recomputed independently in exact arithmetic ([D]):**

| system | L | units | agreement |
|---|---|---|---|
| 3x+1 | 10, 12 | all odd and <3> | every quoted fraction, e.g. 19/79, 31/71, 63/367, 145/433, 249/433 |
| 3x+1 | 14 | <3> | all seven fractions: 213/1627, 213/749, 71/749, 349/749, 479/2247, 479/3745, 349/5243 |
| K7 | 12 | <3> | identical to the prover's `exact_u.py` |
| split5_3 | 12 | <5> | identical to the prover's `exact_u.py` |
| 3x+1 | 14 (all odd units), 16 (m = 1) | | under `--full`, see the end of this report |

**What I did not recompute.** I did not recompute the K7 constants at L = 16, 17 or the split5_3 constants at
L = 16, 17: 19/52, 19/66, 61/79, 17/25. They rest on the prover's `exactD`. That program agrees exactly with a
brute-force evaluation at L = 8 ([B1]) and with my code at L = 12, and it bounds every exact count I computed:
the largest ratio is 0.096 for K7 and 0.256 for split5_3, for b up to 22.

**Node level ([N]).** At b = 22 every alive node that is not full satisfies the per-node bound. The worst ratios
are:

| system | worst ratio |
|---|---|
| 3x+1 | 0.290 |
| K7 | 0.208 |
| split5_3 | 0.938 |

**Is it beyond the horizon, and does it prove anything false?** Yes, it is beyond the horizon, by m digits.
For n < 2^{b-m}, membership in R_b depends on parities of iterates past n's own digits. The bound is a
worst case over all affine images U t + x', so it is not a restatement of in-horizon equidistribution.

It proves nothing false. The sibling bound holds for 3x-1 and 3x+5 and is consistent with their extra cycles,
because a cycle minimum contributes 1 out of |R_b|/2^m. Nothing famous follows from it.

The prover's own rating is accurate: the result is weak, with a bounded and non-vanishing error over
boundedly many digits.

**Labels.** The label "PROVED (exact arithmetic)" is justified.

### Remark on H (not an error)

At m = b, that is X = 1, hypothesis H holds automatically with C = 1 and eps = 0. By Cauchy-Schwarz and
Parseval, B_F(b, b) = sum_{xi != 0} |mu^| <= p^b |R_b|^{-1/2}. More generally,
B_F(b, m) <= p^{(b+m)/2} |R_b|^{-1/2}. So H has content only for m < b.

## Required or recommended fixes

Neither fix touches a PROVED statement or a proof.

**1. (R-A(ii), text.)** The sentence "It is false as stated for K7, whose row (x-1)/4 has a negative intercept"
is wrong if read as "slope survival does not imply actual survival for K7".

- *Lemma.* Write x_t = sigma_t n + c_t. The three maps send c to c/2, to (3c+1)/2 and to (c-1)/4, and each
  preserves the condition c >= -1/3, starting from c_0 = 0. So x_t >= sigma_t n - 1/3 > n - 1 whenever the
  slope sigma_t is at least 1. Since x_t is an integer, x_t >= n.
- *Consequence.* For K7, slope survival over the decided steps implies actual survival. With b digits that
  covers at least b - 1 halvings, so (ii) extends to K7 with b replaced by b - 1.
- *Check.* [I] tests all 104 slope survivors at b = 16 and finds no drop.
- *Fix.* Delete the sentence or replace it with this lemma. The positive intercepts of split5_3 make the same
  extension immediate there.

**2. (Section 7.)** The Shmerkin-Wu theorem is quoted without its hypotheses. It needs p and q multiplicatively
independent (log p / log q irrational) and u != 0. The item is labelled "checked", so these hypotheses should
be stated.

## Nits

- The old "Honest assessment" in section 4 says "I do not claim it as a success of type (1) in substance". R-B
  says "a weak type-(1) statement, as before". The two are compatible but read inconsistently. One sentence
  would reconcile them.
- In the results table, N2 says the top-level sup "stays about 0.05" for b = 20..27. It is exactly 0 at the
  Proposition Z depths 22 and 25, and 0.0485 at b = 20.

## Overall

All five REFEREE1 items were honestly resolved, and the prover's two self-corrections are right. Every PROVED
item survives a line-by-line re-derivation and independent exact computation. Fix 1 corrects a false side
remark that is not used in any proof, and fix 2 adds missing hypotheses to a literature quotation. No GAP or
WRONG remains in any PROVED claim, so needs_repair = false.

Nothing here proves E, E_bdd or GLOBAL, and the folder does not claim to.

## `--full` result

`referee2_check.py --full` exits 0 after 6 minutes. It adds the following results:

- D'_{14} over all odd units is identical to D'_{14} over <3>, for all seven fractions.
- D'_{16,1} = 129/1057 for 3x+1 over <3>. This is independent confirmation of the README's b >= 16 constant.
- The exact counts satisfy U' for b up to 24, for all five systems. The largest deviation ratios are
  unchanged: 0.053, 0.053, 0.146, 0.096 and 0.256.
- The node-level bound holds at b = 24 (j = 14, L = 10). The worst node reaches 0.474 D' for 3x+1, matching
  the prover's [B4], and 0.354 D' for K7.
