# Referee 1 report: round 6, lens `countlaw_wide`

Referee 1 checked this independently. I read README.md and THEORY.md line by line and compared them with
round3/README.md, round5/README.md, round5/microrange and round2/rewriting/split5_3_s27.md. I wrote my own
check, `referee1_check.py`, from scratch: its own table inference from the census rule strings, its own
digit-tree engine, its own DP, brackets, U' constants and Diophantine scan. Only section Z imports the
prover's code, and only to compare numbers. I did not edit the prover's files and did not commit.

## Verdict summary

**Nothing is settled, and the README says so correctly.** No system, and in particular no type-(c) system,
is claimed settled. The theorems are counts with relative errors. They hold for 3x+1, 3x-1 and 3x+5 with
identical constants, and for expanding maps. So they cannot settle 3x+1 or any system, and they do not
claim to. Part (2) of the brief therefore has no target: there is no cycle list to verify.

| claim | verdict |
|---|---|
| Lemma T_G / Theorem R_G | CONFIRMED |
| Lemma F_G and the values of ι | CONFIRMED |
| Lemma P_G | CONFIRMED (for K >= K1; see note) |
| Theorem G1 | CONFIRMED (one wording fix) |
| Corollary G1' | CONFIRMED_WITH_FIX (bookkeeping of η) |
| Lemma X and the exceptional-octave table | CONFIRMED |
| Theorem G2, general (conditional on B2) | CONFIRMED as a conditional sketch |
| Theorem G2 "PROVED for split5_3" | CONFIRMED_WITH_FIX (relabel as imported from s27) |
| (B2) evidence | CONFIRMED as EVIDENCE, but weaker than stated for m3_g, sf3_13, sf3_135 |
| h, h_up, h0, α, H_2, c2, C* | CONFIRMED (all 23 systems recomputed) |
| h_* = h for single-state systems and split5_3 | CONFIRMED |
| C_G certified tables | CONFIRMED |
| U'_G constants | CONFIRMED (6 systems recomputed exactly) |
| Hypothesis scan | CONFIRMED_WITH_FIX (two wording errors) |
| GLOBAL section, "nothing settled" | CONFIRMED_WITH_FIX ("needs" is backwards) |

`needs_repair`: **yes**, for the relabelling and wording fixes below. No mathematical error was found.

## Runs

* Prover's `check_all.py` (numpy venv): **ALL CHECKS PASSED**, exit 0, 11.5 min. It found 1452 bracket
  cases, Lemma T_G exact on 582 nodes, and the mutation broke 318 of them. Lemma F_G largest ratio 0.118.
  (P) holds, the (Pot) buffers are exact, the octave table is as stated, and U' reproduces 3x+1.
  `data/log_check_378.txt` is an older log that records a failure of the mutation test. That test has since
  been fixed; the current run passes it.
* `referee1_check.py`: all sections A–H and Z pass.
  * **A.** Tables inferred from the census and round-4 rule strings agree with the prover's for all 23
    systems. The node rule agrees with an independent lift semantics (p^{k+1} lifts evolving in parallel)
    for every residue at b <= 9 (p = 2) or b <= 6 (p = 3). H0 holds and (F) holds everywhere.
  * **B.** h agrees to < 2·10⁻⁶ for all 23 systems; α, H_2 and c2 agree to 10⁻⁵. For split5_3, h equals
    the binary entropy H = 0.58068412 and c2 equals the closed form c_* = 0.45991804 of s27.
  * **C.** 44 random R_G cases on 11 systems against brute force, including 3x+5, perm_1932, m3_g and
    desc_m3_4n5. The bracket holds, the identity Σ|S| = |R_{m+j}| holds, and Lemma T_G holds node by node.
    The mutation g^{A+1} is detected.
  * **D.** The continuation set is determined by (σ, v, pattern), the Δ formula is exact, and the number
    of patterns is at most K + k + 1 (tested on 6 systems). Lemma P_G was tested numerically (see below).
  * **E.** ι closed forms checked for L <= 24 or 14. Lemma F_G checked exactly on random sets; largest
    ratio 0.10.
  * **F.** My own exact Diophantine scan uses the constant 3 of Lemma X and the rigorous bound
    |log x| >= |x-1|/max(x,1). It flags **no** octave in 18 <= m <= 3000 for any of the 23 systems. On
    whole octaves (m = 18 for p = 2, m = 11 for p = 3; b = m, m+2, m+4; 8 systems) slope survival and
    actual survival agree everywhere.
  * **G.** I recomputed U' exactly with my own minimum-slope function and window counts. The results are
    identical to the table: m3_b, desc_m3_4n5 and m3_g at L = 9; 3x+1, split5_3 and K7 at L = 14. I also
    checked Theorem U'_G itself against brute force (m3_b, L = 6, b = 6, 8, 10).
  * **H.** The scan spot check: the first empty R_b for split_7081, split_5, splitB_71, m3_a, m3_c,
    desc_s8_35 and desc_s32_max is as listed in `hyp_scan.txt`. The infinite chain of 3n+2 is confirmed.
  * **Z.** My grouped brackets at m = 100 (j = 1, 3) and m = 60 (j = 5) for K7, split5_3, sf3_57, m3_b
    and desc_s32_plus9 agree exactly, as integers, with the prover's `bracket` and `bracket_fast`.
* I reproduced the round-5 claim myself with the prover's `bracket_fast`: 3x+1, m = 1000, K = 24 gives
  j = 2: [-0.000327, +0.000294] and j = 8: [-0.004787, +0.004518]. These equal
  round5/microrange/data/certified_siblings.txt (d = 1). No script in the folder makes this comparison
  (nit: add one to `check_all.py`).

## Proofs, line by line

**T_G / R_G.** The derivation is correct. n = r + p^d t maps to x_r + g^A p^s t, and with Python floor
division this is valid for negative values too. Only the multiplier enters, and B ranges over everything.
Unit multipliers u_r = 1 cause no problem. I checked whether the 3x+d multiplier 3^A d^{-1} used in round 5
conflicts with this. It does not: in value coordinates the multiplier is g^A for every d. Round 5 used
different coordinates, which give a different but also valid bracket.

**F_G.** These steps are correct: G vanishes for v_p(ξ) >= j; reduction H_K → H_L is surjective; the
bound |G| <= 1/(2||x||); the harmonic sum is <= Q(1 + ln(Q/2)); and Cauchy–Schwarz with Parseval. The
closed forms for ι are the standard order formulas, and I verified them by computation. m3_e has ι = 2
(7 ≡ 1 mod 3); the README lists only 2 and 5 mod 3^k (nit).

**P_G.**
* (a) Supermultiplicativity is correct. If m_GG >= 1 on [40, 80), then m_GG >= 1 for all K >= 40, and
  h0(K0) → h_* as K0 grows. So the requirement "h0 >= h_* - η/6" in G1 is available, effectively.
* (b) The cycle-deletion argument is correct. Walks decompose into simple cycles, and the prover checks all
  edge-label choices exactly.
* G depends on K0 in principle. My G at K0 = 24 equals the prover's G at K0 = 1500 for every system I
  tested. **Note:** at small K the bound is not yet in force. For sf3_13, m_GG(K - r') = 0 for some
  K <= 10. For desc_s32_plus9, the minimum non-empty |S| stays at 2 for K = 6..10 and then starts to grow.
  This is consistent with "K >= K1" and is not an error. A sentence saying K1 can be about 10 to 15 here
  would help.

**G1.** I re-derived every step:
* the Δ formula (λ is irrational and E >= 1);
* the count of types;
* the Markov bound using a uniform mod q ⇒ g^a uniform on H_K;
* the union over patterns without an independence assumption;
* μ = ⌊1/λ⌋ + 1, which is 1 for λ > 1 (p = 3, g = 2);
* the final exponent 1 - 7η/12.

All are correct. The hypothesis gcd(a_r) = 1 is never used.

**Fix (wording):** the bottom line says G1 is "fully proved in that generality". It should say "for (SG)
maps satisfying (F) and (P)". (P) is a per-system check and not automatic.

**G1'.** Lemma X is correct as written. Each of these steps checks:
* the identity T^i(n) = L_i(n + δ_i);
* the three cases, including the inequality with tV/n <= 1/8;
* H0 for slope 1;
* the "at most two qualifying E" argument, using |g^A - p^E| >= 1.

**Fix:** applying G1 at m - 1 to depths up to m + c log M exceeds that octave's range by one digit. So
either η must shrink to η/2, which gives an exceptional set of M^{1-η/4}, or the depth must be
m - 1 + (h_*/2 - η) log_p M. This is cosmetic.

**G2, general.** The sketch follows s27's proof faithfully:
* the phase factorisation n ≡ y_r g^{-A} + p^d g^{-A} z;
* y_r = p^E c - C_r, with |C_r| <= tV g^A on live words;
* reciprocity, and the bounded index of <p> mod g^A for the g used;
* Cauchy–Schwarz with D-uniform weights;
* Erdős–Turán and Markov.

It is correctly labelled conditional on (B2). Two nits:
* In §5, k denotes both the table exponent (in |y_r| <= (τ0 dV + p^k) g^A, which must be the table k,
  otherwise the multiplicity would be about M) and the terminal length ⌊log_p M⌋ + 2. Rename one of them.
* Erdős–Turán is quoted from memory. The form used, 1/H + Σ_{ξ <= H} |μ̂(ξ)|/ξ with an absolute
  constant, is correct (Montgomery–Vaughan, as s27 cites).

**G2 "PROVED for split5_3": CONFIRMED_WITH_FIX.** The theorem and the constant 0.459918 are those of
split5_3_s27.md. I verified that the constant agrees with s27's closed form to 10⁻⁸. But the s27 theorem is
stated for a different counting set:
* shifted y = n + 3;
* the (z, s) bit coding;
* a halving clock with a pending-halving convention;
* actual survivors in [2^m, 2^{m+1}).

G2 here is stated for slope survivors N(2^m, b) in the digit tree of n. Lemma B1 also says that (B2) "is"
the s27 prefix-count theorem. In fact G2 uses only s27's weight bound (2) and its terminal-set bound. Both
must be carried from the s27 bit coding to this automaton, and that transfer is not written out. It is
plausible: the conjugacy n ↦ n + 3 is a 2-adic isometry, and split5_3 has (Pot), giving an i.i.d.
two-valued walk.

Fix: relabel as "PROVED in split5_3_s27.md (in its coding); the present formula reproduces the constant;
the translation to the present coding is routine but not written out". Alternatively, write the
translation.

**B2 evidence.** My own DP agrees with the prover's band. But "bounded" is a weak reading for three
systems:
* m3_g: the normalised ratio rises monotonically (3.81 → 5.10 over n = 100..600; local exponent 0.85
  between n = 300 and 600, not 1.5). θ* = 0.045, so the asymptotics are very slow.
* sf3_13 and sf3_135: large oscillations (θ* ≈ 4 to 4.6), with local exponents 1.05 and 0.90.

The README should say that for these the data neither confirm nor refute the n^{-3/2} exponent.

**h_* = h.** The Raney/types lower bound for (Pot) systems is a correct sketch, and the buffer words are
checked exactly. For split5_3 it is again imported from s27; (Pot) also covers it.

## Labels, coverage, novelty

1. **§7 and README "GLOBAL needs control out to C* log_p X digits" / "GLOBAL ... needs, at least, that no
   start ... survives b = C* log_p X digits".** This is backwards. Conjecture E at depth (C* + ε) log X is
   a *sufficient* route, given no new cycles. GLOBAL does not imply it: GLOBAL allows stopping times far
   longer than C* log n. Rephrase as "a counting proof of GLOBAL along these lines would need ...".
2. **Hypothesis scan wording.** The README says "R_b is empty from b = 1 to 30". The data say: empty for
   b >= 2 (split maps), b >= 1 (m3_a, m3_c), b >= 4 (desc_s8_35) and b >= 30 (desc_s32_max, d65). This
   is a *slope* descent certificate. It implies actual descent only for n large enough to absorb the
   additive constants, for example the +7081. Several of these maps have extra cycles.
3. **"Least extrapolation of Conjecture E anywhere in the census".** This holds only among the systems in
   the table. Mixed-prime and other excluded maps have no C* computed.
4. **"(F) fails exactly when some class is mapped into itself".** It fails exactly when there is a cycle of
   division-free decided steps among classes. The cycle need not have length 1.
5. The label for C_G, "PROVED (exact integer computation)", is fair. I verified the code paths (Python and C)
   against my own at small K; the K = 28 numbers in the README match `data/certified_*.txt`. The round-5
   reproduction claim is true (I reproduced it) but has no script.
6. The README says "No literature search was done". That is honest, and no novelty is claimed beyond
   porting.

## Files

* My check: `/home/riv/Code/collatz/census/round6/countlaw_wide/referee1_check.py` (sections A–H, Z; exit
  0 iff all checks pass; about 8 min in total; numpy/scipy venv).
