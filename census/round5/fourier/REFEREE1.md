# Referee 1 report: round 5, lens "Fourier and Diophantine formulation"

Referee: independent agent, 27 Nov 2026. I did not edit any of the prover's files.
My script: `referee1_check.py`, written from scratch. It uses its own formulation (the accelerated map
T(x) = x/2 or (3x+d)/2, with survival meaning 3^{a_t} >= 2^t for t = 1..b) and does not import the prover's
code. The only exception is check R1, which compares my R_b against the prover's `rb` bitmaps.
Run it with `<venv python> referee1_check.py`, which takes about 45 s. `--full` adds the L = 22 recomputation
and an exact L = 14 computation, about 9 min in total. It exits 0 iff every check passes. It can fail: check
R3c has a mutation that is required to fail, and it produces 39 violations.
Prover's checker: `check_fourier.py` exits 0 in 2.2 s. I mutated copies of it in my scratchpad. Setting
D_1 = 0.0001 makes [7] fail. Changing the 3x+1 row to 3x+3 makes [1] fail three times. So the checker can fail.
Note that [7] is only a consistency check, because the observed deviations are about 0.003 against a bound
of 0.19.

## Summary

The folder is careful and unusually honest. Each PROVED item survives a line-by-line re-derivation, and so do
the identities F1, Lemma T, Theorem U, Proposition Z, identity S, F2 and F3. Theorem U is the only claim that
controls integers beyond their horizon. I reproduced its 3x+1 constants independently to 6 digits:
D_{16,m} = 0.379414 / 0.856991 / 1.718072 and D_{22,m} = 0.194733 / 0.432901 / 0.877677, with
kappa_{22,0} = 0.05875. My FFT error budget on these is about 1e-11. I also proved a STRONGER, fully exact
version of the statement (see U below). The result really is beyond the horizon: it concerns the parity of
T^{b-1}(n) for n < 2^{b-1} on the boundary nodes. But it is only 1 to 3 digits beyond, and the prover says
so. It does not prove anything false. Its siblings 3x-1 and 3x+5 satisfy the same bound in the slope sense,
and nothing in the bound concerns cycles.

Problems that need repair:

1. **F4 consequence (substantive).** The inequality in F4 is correct, but it does not imply the headline
   consequence "no Fourier-decay hypothesis used through absolute values can prove M". To prove N = 0 one
   only needs N <= (1 + B_F) X P(b) < 1. F4 only gives (1 + B_F) X P >= 1/pi + O(X P), which can be below 1.
   Numerically, at b = 16 and m = 16, (1 + F4 floor) X P = 0.33. So an N = 0 certificate is not excluded by
   F4. The statement is nevertheless TRUE, by a one-line translation argument that also makes F4 stronger.
   This is fix (A) below.
2. **G / E_0 (substantive clarity).** All theorems in the folder use the slope-sense count. E_0 => M is valid
   only if E_0 is stated for the lead's ACTUAL-drop count. In the slope sense the argument breaks: an n that
   actually survives need not lie in R_b, and the cycle minima of 3x+5 are not slope-sense exceptions. Also,
   "E does not imply M" cannot be proved as a statement about a fixed system: if Collatz is true, the
   implication holds vacuously. What is proved is that the inference in CONJECTURE.md is invalid.
3. Smaller issues: the F3 constants are inconsistent (1/2 - eps in the table, 1/2 - 2eps in the text) and F3
   is proved only for X = p^{b-m}. The "~1.5" in N1 should be a range. N3 needs a note on the 2^{b-2} symmetry.
   I list these below.

## Verdicts

| id | verdict | note |
|---|---|---|
| F1 | CONFIRMED | re-derived; checked numerically for all m and several k at b = 14 (R6), annihilation exact |
| F2 | CONFIRMED | standard Weyl/portmanteau equivalence; correct; no novelty claimed |
| F3 | CONFIRMED_WITH_FIX | conditional, trivially from F1; make eps consistent; extend to general X (fix C) |
| F4 inequality | CONFIRMED | correct, but not sharp: the translation bound gives B_F >= 1/(X P) - 1, threshold 1/2 |
| F4 consequence ("no absolute-value Fourier argument proves M / E_0") | CONFIRMED_WITH_FIX | true, but F4 does not prove it; fix (A) does |
| T | CONFIRMED | re-derived; checked exactly with my own code for 3x+1, 3x-1, 3x+5 (R2) |
| U | CONFIRMED | proof re-derived (decidedness monotone, affine bijection, valuation classes permuted, rearrangement) |
| U-3x+1 | CONFIRMED (suggested upgrade) | constants reproduced independently; an exact L = 14 computation gives better constants with no floating point (fix B) |
| U for K7, split5_3 | CONFIRMED (not independently recomputed) | the numbers are >= 1 or 0.999, so they carry no content, as the prover says |
| Z | CONFIRMED | re-derived; my exact check for b = 2..24; the 37% frequency is right (0.369) |
| S | CONFIRMED | holds for EVERY r mod 2^b, not only on R_b (R7: all r at b = 12) |
| G (E as stated does not give M) | CONFIRMED_WITH_FIX | phrase as "the inference is invalid"; E even allows one divergent orbit |
| G (E_0 => M) | CONFIRMED_WITH_FIX | state E_0 for the actual-drop count N of CONJECTURE.md, not the slope-sense count |
| N1 | CONFIRMED_WITH_FIX | ratio max_{xi<=64}/|R_b|^{-1/2} is 1.3 to 3.1 in decay.txt, not "~1.5" |
| N2 | CONFIRMED | the random baseline 0.004 is for b = 26 only (0.021 at b = 20) |
| N3 | CONFIRMED_WITH_FIX | add the symmetry xi -> xi + 2^{b-2}d (R8); the printed exponents such as 3145742 are this symmetry |
| N4 | CONFIRMED | ratios recomputed from l1_vs_b.txt / l1test_b26.txt |
| E, E_bdd | OPEN (correctly labelled) | |

## Detailed comments

**F1.** Parseval on Z/p^b: N = p^{-b} sum_xi S^ conj(I^), where the xi = 0 term is X|R_b|/p^b. Take
xi != 0 with v_p(xi) >= m. Then x -> e(-x xi/p^b) has period p^{b-v}, and that period divides
X = k p^{b-m}. So I^(xi) is a full sum of a nontrivial character and equals 0. Dividing by
X P = X|R|/p^b gives B_F. Correct.

**F2.** Correct. Note that N/(XP) = mu_b([0, k/p^m))/(k/p^m). Standard; the prover claims no novelty.

**F3.** Under H(eps) the error is C p^{m - (1/2 - eps) h b + o(b)}. It tends to 0 for
m <= (1/2 - 2eps) h b, so the text is right and the table's "(1/2 - eps)" needs the same margin. F3 as written
covers only X = p^{b-m}. Fix C: write X in base p and split [0, X) into at most (p-1) log_p X translates of
[0, p^i). |I^| is invariant under translation, so H bounds each piece. The total relative error is
C (p-1) log_p X p^m |R_b|^{-1/2+eps}, and the same range of b follows. The ranges 1.90 log_2 X (3x+1) and
1.41 log_2 X (split5_3), and C* = 19.98 and 2.385, are arithmetically right.

**F4 and fix (A).** I re-derived the proof: the Jordan inequality, |xi| <= Z < p^m, the Fejer kernel, and
|mu^| <= 1. It is correct. One edge case: when X = 1 and p = 2, the frequencies +Z and -Z coincide mod p^b.
The inequality still holds there via plain Parseval. The consequence drawn from F4 needs a different argument:

> **Translation bound.** For every t, #(R_b ∩ (t + [0,X))) - X P = p^{-b} sum_{xi != 0} S^(xi) conj(I^(xi)) e(t xi/p^b),
> so X P B_F = p^{-b} sum_{xi != 0} |S^||I^| >= max_t #(R_b ∩ (t + [0,X))) - X P >= 1 - X P (take t in R_b).
> Hence B_F >= 1/(X P) - 1 (better than F4; B_F < 1 forces X P > 1/2), and (1 + B_F) X P >= 1 always.
> More generally, any bound sum_{r in R} phi(r) <= main + p^{-b} sum |S^||phi^| with phi >= 1_{[0,X)} is invariant
> under translating phi, so it is >= 1. Absolute values on the coefficients can never certify N = 0.

With (A), the sentence "No Fourier-decay hypothesis used through absolute values can prove M" and the remark
"E_0 is out of reach of every absolute-value Fourier argument" are proved. This includes smooth majorants,
not only the sharp cutoff. Check R6 verifies both bounds at b = 16 for 3x+1 and 3x-1, for all m.

**Lemma T and Theorem U.** I re-derived both line by line.

* The decided steps of r1 + p^j t are those of r1, because decidedness depends only on the low digits.
* The value after those steps is x + U p^s t.
* The remaining steps see (x mod p^s, z mod p^L), and their prefix slopes are A times those of g_sigma.
* For 3x+1 the only stuck state is (0,0). For K7 and split5_3 the stuck states are (0,0) and (1,1), as in
  `fourier_bound.py`.
* As A runs over [1, inf), All(sigma, A) runs over super-level sets of g, and the code enumerates all of them.
  It excludes only the full set, whose nonzero coefficients vanish.
* The deviations of the nodes add up. Multiplication by U^{-1} permutes each valuation class, so the
  rearrangement inequality applies.
* The normalisation sum_{r1} |All(r1)| k p^{-m} = X P(b) is correct.

My own implementation reproduces the README numbers to 6 digits at L = 16 and L = 22, with 94 and 170
allowed sets and smallest sets 2114 and 93222. The FFT error is far below the margins: my budget on D is
8e-12. So U-3x+1 as stated holds for every b >= 22.

**Fix (B) (an upgrade, not an error).** The rearrangement step loses roughly a factor of 2.5. The quantity
actually needed is the exact supremum over odd units u and shifts c of
|#{t < 2^{L-m} : u t + c in S}/(|S| 2^{-m}) - 1|. This is a rational number, and it is computable by sliding
window sums. Taking the sup over ALL odd units instead of the units 3^a only makes it larger, so it is still
a valid bound. Results:

| L | exact D_{L,1} | exact D_{L,2} | exact D_{L,3} | rearrangement D_{L,1}, D_{L,2} |
|---|---|---|---|---|
| 10 | 0.24051 | 0.43662 | | 0.61232, 1.31599 |
| 12 | 0.17166 | 0.33487 | | 0.40917, 0.90894 |
| 13 | 0.17166 | 0.33487 | 0.57506 | |
| 14 | **0.13092** = 213/1627 | **0.28438** = 213/749 | **0.46595** = 349/749 | |

So, in exact arithmetic with no floating point, for every b >= 14 and m = 1, 2, 3:
|N(2^{b-m}, b)/(2^{b-m} P(b)) - 1| <= 0.1310, 0.2844, 0.4660. This beats the README's L = 22 constants and
removes the "double precision" caveat. Check R3 verifies the exact constants for L = 10 and 12 against exact
counts for 3x+1, 3x-1 and 3x+5, for all b in [L, 22]. `--full` does the same for L = 14 against b = 22, 24, 26.
The sibling test shows nothing false: in the slope sense the three siblings have the same exact constants.
That is expected, because x -> d x conjugates 3x+1 to 3x+d, which maps the allowed sets to unit multiples.
The bound says nothing about cycles.

**Is U beyond the horizon?** Yes, and it is not a restatement of in-horizon equidistribution. For
n < 2^{b-1}, membership in R_b depends on the parity of T^{b-1}(n) whenever the node has slope A in [1, 2).
That parity is a digit past n's horizon. U bounds its bias uniformly in b. It is weak, and the prover's
"honest assessment" says so accurately: the trivial sandwich at b = 24 gives [0.822, 1.178] (R9), the error
does not tend to 0, and the method cannot reach K log X. I agree with the prover's own rating that U is not
a type-(1) success in substance.

**Z.** If 3^a >= 2^{b-1} and no power of 3 lies in [2^{b-1}, 2^b), then 3^a >= 2^b. So A >= 2, and both lifts
survive: the even lift has slope A/2 and the odd lift 3A/2. The rest follows. In my data the converse also
holds for b <= 24: whenever a power of 3 is present, the invariance fails. The README calls Z "really
in-horizon", which is an honest label.

**S.** Correct, and it holds for all r mod 2^b, not only on R_b. The claim that the unconditioned 2-adic
variable is exactly uniform follows from that.

**G.** E's additive term X^{eps(X)} >= 1 is consistent with N(X, b) = 1 for every b, i.e. with a single
never-dropping or divergent start. So the lead's "E => sigma(n) <= (C* + eps) log n for all but finitely many
n" is invalid. Suggested wording: "the stated derivation of M from E is invalid; E's inequality is consistent
with one divergent orbit". The proof that E_0 => M is right once N means the lead's actual-drop count. It
chooses X = n + 1 and b = ceil((C* + eta) log_p n) <= K log_p X, and uses X P(b) = n^{-eta(1-h) + o(1)}.

**Evidence items.** N2 and N4 match the output files. For N1, the ratios in decay.txt range from 1.27
(b = 16) to 3.1 (b = 27). For N3: every survivor of 3x+1 is 3 mod 4 (R8), so |mu^(xi + 2^{b-2}d)| = |mu^(xi)|.
The argmax printed in decay.txt is therefore an arbitrary representative. For example, 588665 = 3^14 mod 2^22
equals 3^{3145742} = 3^14 (1 + 2^22 c) mod 2^24, and |mu^| = 0.056246 at both (R8). The README's sentence
"exactly xi = ±2^v u^a" should say "up to this symmetry", i.e. xi ≡ ±2^v u^a mod 2^{b-2} with a small.
Without the restriction on a the statement is vacuous, because ±3^a covers all odd residues.

**Literature and labels.** External results that were only remembered are flagged as "from memory": Tao's
Prop. 1.17 form, Bourgain-Dyatlov, J. Li, Bugeaud, Fishman-Simmons. What is quoted agrees with my own
recollection. In particular Tao's bound is O_A(n^{-A}) for xi not divisible by 3, for Syrac(Z/3^n Z).
Shmerkin and Wu (Ann. of Math. 189, 2019) are stated correctly. None of these is used in a proof, so nothing
depends on an unchecked quotation. No novelty is overclaimed. The PROVED labels are justified, with fixes A
and C. Fix B is a recommended upgrade.

## Required fixes (needs_repair = true)

A. Replace the derivation of the "absolute values cannot prove M / E_0" consequence with the translation
   bound. Optionally state the improved F4: B_F >= 1/(X P) - 1.
B. (Recommended) Replace the U-3x+1 floating-point constants with the exact L = 14 constants 0.1310 / 0.2844 /
   0.4660, valid for b >= 14, or at least mention them.
C. F3: make eps consistent and add the base-p decomposition for general X.
D. G: state E_0 for the actual-drop count, and reword "E does not imply M" as "the inference is invalid".
E. N1: give the ratio range. N3: add the 2^{b-2} symmetry.
