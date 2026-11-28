# Referee 2 report: round 6, lens `countlaw_wide` (second pass, after the REFEREE1 repair)

Referee 2 checked this independently. I read README.md, THEORY.md and REFEREE1.md line by line and compared
them with round3/README.md, round5/README.md (and round5/microrange/README.md, round5/fourier/README.md) and
round2/rewriting/split5_3_s27.md. I wrote my own check, `referee2_check.py`, from scratch:
* its own tables, re-inferred by exact affine fitting from the census rule strings;
* its own digit-tree engine, state DP and continuation sets;
* its own brackets, window extremes, U' constants, Diophantine scan, transfer matrices and (P) test.

Only section Z imports the prover's code or data, and only to compare numbers. I did not edit the prover's
files and did not commit.

## Verdict summary

**Nothing is settled, and the README says so correctly.** No system, and in particular no type-(c) system
or open census entry, is claimed settled. Part (2) of the brief (verify cycle lists, attack a settled
type-(c) claim, check whether the argument would also settle 3x+1) therefore has no target. As REFEREE1
noted, every theorem here holds with identical constants for 3x+1, 3x-1 and 3x+5, which have different
cycle sets. The theorems also hold for divergent-looking maps (5x+1, m3_e, W). So they cannot settle 3x+1
or any other system, and the text does not claim they do.

| claim | verdict |
|---|---|
| REFEREE1 items (12 repairs) | all honestly resolved (see below) |
| Lemma T_G / Theorem R_G | CONFIRMED |
| Lemma F_G and the values of ι | CONFIRMED |
| Lemma P_G and hypothesis (P) for all 23 systems | CONFIRMED |
| Theorem G1 | CONFIRMED |
| Corollary G1' (repaired bookkeeping) | CONFIRMED |
| Lemma X and "no exceptional octave for 18 <= m <= 3000" | CONFIRMED |
| Theorem G2 (conditional sketch on B2); split5_3 relabelled as imported from s27 | CONFIRMED as labelled |
| (B2) evidence | CONFIRMED as EVIDENCE |
| h, h_up, h0, α, H_2, c2, C* | CONFIRMED (all 23 recomputed) |
| h_* = h for single-state systems | CONFIRMED |
| h_* = h for split5_3 | CONFIRMED_WITH_FIX (cited from s27's coding; the present-coding proof is one line, given below) |
| C_G certified tables | CONFIRMED |
| U'_G constants | CONFIRMED (4 more systems recomputed exactly, plus brute force of the theorem on 4) |
| Hypothesis scan | CONFIRMED |
| GLOBAL section | CONFIRMED |
| Labels, coverage, novelty | CONFIRMED, with three nits (N1–N3) |

`needs_repair`: **no.** No mathematical error was found. The one fix (h_* = h for split5_3) is a matter of
citation, and the replacement argument is checked below. The nits are wording only.

## Runs

* **Prover's `check_all.py`** (numpy venv, parts 1–9): **ALL CHECKS PASSED**, exit 0, 12.0 min. It ran 1452 bracket cases, checked Lemma T_G on 582 nodes (the mutation broke 318 of them) and confirmed (P) and the (Pot) buffers. Part 9 reproduces round-5 3x+1 at m = 1000, K = 24, j = 1..8 to the printed 5 decimals. (Part 6 checks a buffer word from the root only; see the Fix below.)
* **`referee2_check.py`** (all sections A–K and Z): **ALL REFEREE-2 CHECKS PASSED**, exit 0 for every section, about 6 min in total. The sections:
  * **A.** All 23 tables re-inferred from the rule strings are identical to `cwlib.SYS`; I fit
    u/p^e and v on residue classes and checked exactness on negative members too. For each system,
    (SG), unit multipliers and H0 hold. My states1 sizes match the README `st` column:
    * K7: 2;
    * sf3_7: 3 (as "2 (3)");
    * desc_s32_plus9: 8;
    * every base-3 system: 1.
  * **B.** For every system, |R_b| counted node by node equals my state DP, up to b = 11 (p = 2) or
    b = 7 (p = 3). The 3x+1 values reproduce the known sequence (|R_14| = 734).
  * **C.** Theorem R_G on 92 random (system, m, j, K) cases over all 23 systems, against brute force:
    * L <= N(p^m, m+j) <= U holds in every case;
    * Σ|S_r| = |R_{m+j}| holds exactly;
    * Lemma T_G holds on 389 nodes, for every t < p^{K-j};
    * on 60 sets the window trick agrees with the literal max/min over all p^K intercepts B;
    * the mutation g^A -> g^{A+1} is detected 752 times.
  * **D.** Lemma X, my own exact scan:
    * It uses the rigorous criterion |g^A - p^E| p^{m-1} >= 3 t V max(g^A, p^E), from
      |log x| >= |x-1|/max(x,1), with my own τ0, t = τ0 b and b <= m + 2 log_p m + 1, together with the
      size test 8tV <= p^{m-1}.
    * For every one of the 23 systems, no octave 18 <= m <= 3000 is flagged.
    * The largest flagged octave is 16 (3x+5, desc_s32_plus9), and m <= 10 for p = 3. The prover's
      "only m <= 17" is consistent with this; its criterion is slightly more conservative.
    * On whole octaves, slope survival equals actual survival (T^i(n) >= n) for every n:
      * m = 18 (3x+5, K7, sf3_13, split5_3, desc_s32_plus9, desc_split7_1);
      * m = 11 (m3_b, desc_m3_4n5, m3_g);
      * at b = m and b = m + 3.
  * **E.** U'_G constants recomputed exactly with my own minimum-slope ranks and vectorised cyclic windows,
    for systems REFEREE1 did not recompute: m3_d (L = 9: 17/56, 29/56, 115/128), sf3_357 (L = 14: 9/41, 19/41, 7/9), split5_1 (L = 14: 89/569, 145/559, 143/375) and sf3_13 (L = 14: 1, 5/2, 5). All are identical to `data/everyoct.txt` and the README table. The theorem itself holds against brute force for
    K7 (L = 6), split5_3 (L = 6), m3_g (L = 4) and desc_s32_plus9 (L = 7), with b = L..L+3 and m = 1, 2, 3.
  * **F.** h, θ*, H_2, α (my own simple-cycle enumeration), c2 and C*, from my own transfer matrix. For all
    23 systems they agree with `data/constants_K1500.txt` (h to < 2·10⁻⁶, c2 to < 2·10⁻⁵).
    |R_K|^{1/K} <= p^{h + O(1/K)} holds at K = 60 / 40.
  * **G.** Hypothesis (P), my own computation at K0 = 40:
    * B is non-empty for exactly 6 systems: sf3_17, sf3_57, sf3_357, sf3_137 and sf3_13 (B = {(2,1)}),
      and desc_s32_plus9 (B = {(3,3), (4,3), (4,11)}). This matches the prover's lists.
    * Every B-state reaches G.
    * The only cycles in B are the self-loops of sf3_57 and sf3_357, and they contract strictly.
    * m_GG(K) >= 1 on [40, 80).
  * **H.** ι, from orders of g mod p^L (L <= 18, or 11 for p = 3): 2, 2, 4 for p = 2 with g = 3, 5, 7;
    2, 2, 1, 1 for p = 3 with g = 4, 7, 2, 5. The stated closed forms are correct.
  * **I.** Lemma F_G checked by exact enumeration on 28 random sets (7 pairs (p, g), all u ∈ H_K and all
    B). The largest ratio of left side to bound is 0.122.
  * **J.** h_* = h for split5_3 in the present coding (see "Fix" below). The exact potential and the buffer
    words from both states are verified.
  * **K.** Scan spot checks. The first empty R_b is as stated:
    * b = 2 for split_7081, split_5 and splitB_71;
    * b = 4 for desc_s8_35;
    * b = 30 for desc_s32_max and desc_s32_d65 (R_29 is non-empty);
    * b = 1 for m3_a and m3_c.

    3n+2 and 3n+4 have an infinite decided chain.
  * **Z.**
    * My brackets equal the prover's `cert.bracket` exactly, as integers (Lo, Up and Σ|S|), on 10 cases at
      m = 100 (K7, split5_3, m3_b, desc_s32_plus9, sf3_135; K = 9 to 14).
    * All 60 cells of the README C_G table agree with the K = 28 / K = 17 lines of
      `data/certified_*.txt`.
    * My U' constants equal `data/everyoct.txt` exactly.

## REFEREE1 items: were they honestly resolved?

| REFEREE1 item | status now |
|---|---|
| G1 "fully proved in that generality" | Fixed. The bottom line and table now say "for (SG) maps satisfying (F) and (P)". |
| G1' η bookkeeping | Fixed correctly. G1 is applied with η/2 on [M, 2M) and on [M-1, 2M-1). I checked that (h_*/2 - η/2) log_p(M-1) >= (h_*/2 - η) log_p M + 1 for large M. The exceptional set is 2M^{1-η/4} + O(log M), and the error is M^{-η/6}(p+1)/(p-1). |
| K1 note | Added (THEORY §3). |
| G2 "PROVED for split5_3" | Withdrawn and relabelled honestly, in the README row, THEORY §5 and Lemma B1. The bold c2 = 0.45992 is annotated "(= s27)". |
| B2 wording for m3_g, sf3_13, sf3_135 | Fixed. |
| GLOBAL "needs" (backwards) | Fixed in both files. It is now a sufficient route ("a counting proof along these lines would need ..."). |
| scan wording "empty from b = 1 to 30" | Fixed. I confirmed the exact first-empty depths, and the slope-certificate caveat is stated. |
| "least extrapolation anywhere in the census" | Fixed ("among the systems in this table"). |
| (F) "class mapped into itself" | Fixed: now a cycle of division-free decided steps. This is correct: s can only decrease, so an infinite chain is eventually division-free on finitely many (s, c), hence cyclic. |
| §5 notation k / ℓ | Fixed. |
| ι for m3_e | Added. |
| round-5 reproduction script | Added as part 9, which reads round5 `certified_siblings.txt` and compares j = 1..8. |

Nothing was silently dropped. The only status change is the one announced (G2 for split5_3).

## Proofs, line by line (second pass)

Throughout I paid attention to hypotheses that hold for 3x+1 but may fail on the new maps.

**T_G / R_G.**
* The reduction uses only that every multiplier is a p-adic unit. The value after the decided steps of
  r + p^d t is x_r + g^A p^s t; s = d - E because each division consumes one known digit.
* Exactness forces e <= s for a step decided at s < k (p^e | u p^s), so s never goes negative.
* Rows with u = 1 (n -> n+v, n -> (n-1)/4) are harmless: they contribute g^0.
* Negative v (3x-1, K7, m3_b) is harmless because floor division is used consistently.
* The shortcut "A >= amin(E + K + s + k + 1) ⇒ full" in `bracket_fast` is valid, since at most s + K
  divisions occur in K more digits.

CONFIRMED.

**F_G.**
* For e >= j, the additive order of uξ divides N, so G vanishes.
* For e < j, a = uξ/p^e ranges uniformly over a coset of H_L, because H_K -> H_L is a surjective
  homomorphism. This is the only place where the subgroup generated by the multipliers enters.
* The bound |H_L| >= φ(p^L)/ι brings in exactly the index. For g ≡ 1 mod 3 (m3_b, m3_d with g = 4; m3_e
  with g = 7) this index is 2, not 1, and it is used.
* The rest is Cauchy–Schwarz with Parseval.

CONFIRMED.

**P_G.**
* (a) Concatenation gives supermultiplicativity. Fekete then gives lim = sup.
* The explicit bound m(K) >= m(K0)^{⌊K/K0⌋-1} needs m >= 1 on [K0, 2K0). That follows from m >= 1 on
  [40, 80) by concatenation, which part 5 checks and I re-checked.
* (b) Deleting cycles inside B only raises later prefix slopes, and the cycle decomposition of a walk
  gives simple cycles. The "never enters G" case forces L >= cγ^{-K/|B|}.
* Only multi-state systems have B ≠ ∅, so this is the hypothesis that is new relative to 3x+1. I verified
  it independently for all 6 systems where it is non-trivial.

CONFIRMED.

**G1.** I re-derived every step:
* v = A - amin(E) ∈ [0, (K+k)λ + 1). Here s <= k-1 after the chain, so e* <= s + K < K + k.
* Δ_e(E) = ⌊eλ⌋ + [{Eλ} + {eλ} >= 1], which gives at most K + k + 1 patterns. E = 0 gives the top pattern.
* For fixed (σ, v), the octave m fixes both A and the pattern. So the count of bad octaves is a union over
  patterns, with no independence assumption.
* μ = ⌊1/λ⌋ + 1 covers λ < 1 (g = 5, 7 with p = 2: A can repeat) and λ > 1 (p = 3, g = 2).
* The number of states enters only through T_K.
* The constants are uniform: G_K, T_K, μ and λ depend only on the table. K1, h0 and K0 are fixed before M.
  The threshold "large M" depends on η but is effective in principle.
* The exponent is 1 - h0/2 + η/3 + h_*/2 - η <= 1 - 7η/12.

CONFIRMED.

**G1' and Lemma X.**
* I checked the identity T^i(n) = L_i(n + δ_i), δ_i = Σ v_l/(u_l L_l), symbolically.
* |δ_i| <= iV uses u_l >= 1 and L_l >= 1.
* The two inequalities hold: (1 + 3x)(1 - x) >= 1 for x <= 2/3, and e^{-3x}(1 + x) < 1 for x <= 1/8.
* H0 is needed exactly for slope-1 prefixes. It holds for all 23 systems: their slope-1 rows have v >= 0.
* In (ii), the three-points argument (two qualifying E differ by > M - C' log M, inside an interval of
  length M + O(log M)) is correct.

CONFIRMED.

**G2.**
* It is labelled as a sketch conditional on (B2). The constant formula reproduces s27's
  c_* = H/2 + H_2/log_2 5 = 0.459918; my value agrees.
* Step (3) needs <p> to have bounded index in (Z/g^A)^*. I checked this for the g used: index 1 for
  2 mod 3^A and 2 mod 5^A, 2 for 2 mod 7^A, and 2 for 3 mod 2^A. This is in line with the claim.
* Erdős–Turán is flagged as quoted from memory, and the form is correct.

CONFIRMED as labelled.

**h_* = h.**
* For single-state systems the Raney/types sketch is correct: G = {root}, m_GG = |R_K|, the rotation map
  is at most n-to-1, and the tilted type has entropy log ρ* because the mean is 0 at an interior θ*.
* This also upgrades the 3x+1 G1 constant to H(λ)/2 = 0.47498. See N1.

**Fix (h_* = h for split5_3).** THEORY §5 says that for split5_3 "h_* = h is the continuation-set bound of
`split5_3_s27.md`". That bound (s27, "Every continuation set ... has size at least c 2^{Hk}/k^{3/2}") is
stated in s27's (z, s) bit coding of y = n + 3. This is the same kind of coding transfer that REFEREE1
asked to be withdrawn for G2. But no transfer is needed: the present file's own (Pot) argument covers
split5_3 directly. In the present automaton:
* states1 = {(0,0), (1,1)};
* the digit moves are (0,0) -0-> (0,0) slope 1/2, (0,0) -1-> (1,1) slope 1, (1,1) -0-> (0,0) slope 5/4, and
  (1,1) -1-> (1,1) slope 1/2;
* with the potential φ(1,1) - φ(0,0) = -(1/2) log(5/4), the labels are {1/2, √5/2} from both states
  (Δ = (1/2) log(5/4));
* the intra-digit dip is 0 (no prefix inside a digit is below both of its endpoints);
* buffer words "1 0" from (0,0) and "0" from (1,1) both survive and reach slope 5/4 > √(5/4).

So Raney plus types gives m_GG(K) >= ρ*^K K^{-C} from both states of G = states1, and h_* = h. This is
verified exactly in `referee2_check.py` section J. Numerically, log_2 m_GG(K)/K is 0.490, 0.529, 0.552 and
0.564 at K = 100, 200, 400 and 800, rising towards h = 0.5807 at the expected (3/2) log K / K rate.

**Requested change:** replace the s27 citation by this argument, or by a sentence saying that the §5 (Pot)
sketch applies from every state of G, with buffer words from each state, and that part 6 should check
buffers from every state, not only from the root. The bold G1 constant 0.29034 for split5_3 then rests on
this file alone.

## Labels, coverage, novelty

**N1 (novelty statement, 3x+1 constant).** The README says "The 3x+1 constant 0.47498 is the round-5
H(λ)/2." Round 5 explicitly did not prove that constant: microrange/README.md Theorem D proves only
h0/2 >= 0.4715, and its revision table withdraws H(λ)/2. Here G1, together with "h_* = h PROVED for
single-state systems", gives depth (0.47498 - η) log_2 M for 3x+1. That is a (small) strengthening of
round-5 Theorem D, and the README should say so, rather than present 0.47498 as a round-5 number. The
proof it rests on is the Raney/types sketch in THEORY §5, which I confirm.

**N2 (B2 evidence).**
* For all 19 systems, the maximum of the normalised ratio over [100, 1200] occurs in the last third. So a
  slow upward drift is generic, not specific to m3_g.
* I extended three systems to n = 3000:
  * 3x+1 levels off at about 2.38 (2.338, 2.328, 2.391 and 2.382 at n = 600, 1200, 2000 and 3000);
  * K7 stays in [0.84, 1.06];
  * split5_3 oscillates in [0.60, 1.07].
* This supports the EVIDENCE label. I suggest one sentence noting the generic slow drift.

**N3 (external results list).** The THEORY.md header lists "Fekete's lemma, Erdős–Turán inequality
(Section 7, ...), unique factorization". Erdős–Turán is in Section 5. The list also omits Raney's cyclic
lemma, the method of types and the lifting-the-exponent facts, which the README lists correctly. Align the
two lists.

The remaining labels are fair:
* C_G is exact integer computation, and the README numbers match the data.
* U'_G is exact rationals.
* X is exact for m <= 3000.
* h is floating point, with a proved enclosure h0 <= h_* <= h <= h_up.
* "No literature search was done" is stated, and no novelty is claimed beyond porting.

The coverage statements match `hyp_scan.txt`:
* 23 systems in the tables;
* (P) holds for all of them;
* 6 have bad states;
* 19 have U' rows.

## Files

* `/home/riv/Code/collatz/census/round6/countlaw_wide/referee2_check.py`: sections A–K and Z. Run
  `python referee2_check.py [sections]`. It exits 0 iff all checks pass. It needs numpy, and section Z
  needs the prover's `cw` binary.
