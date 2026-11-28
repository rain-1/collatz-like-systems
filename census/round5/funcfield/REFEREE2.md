# Referee 2 report: round 5, lens "function fields" (`census/round5/funcfield/`)

Second pass, after the repair that answered `REFEREE1.md`. Scope: `README.md`, `theory.md`,
`specs/`, all check scripts, `REFEREE1.md`. I re-derived every PROVED item line by line, ran the
prover's `check.py`, and wrote a new independent check, `referee2_check.py`. It imports nothing
from the prover or from `referee1_check.py`. It has its own F_2/F_3/F_4 arithmetic, its own
encoding of the systems (compared against `specs/`), its own exact `P(b)` DP, its own
enumeration of `sigma`, and its own composition `G_w, H_w`. I did not edit the prover's files
and did not commit.

## Summary

All PROVED items now hold, including the two that were new in the repair: the elementary
Theorem A'' for S2c and Proposition H' with Lemmas S and B. The main result is correct and
complete: the exact function-field analogue of Conjecture E, and of its minimal form M, is
false for the binomial systems A3, Q4b and S2c. The failure really is beyond the horizon. It
holds at `b = K log_q X` for every `K > 1`, it comes from an exact algebraic identity
(Frobenius), and it is not a restatement of in-horizon equidistribution. Every REFEREE1 item was
resolved honestly. Withdrawn statements are named as withdrawn, not silently deleted.

Only cosmetic fixes remain:

* **B3 multiplier mislabelled.** The README table and theory §4 call it `(1+t)^2`. The spec and
  the data use `1 + t + t^2`, which over F_3 is `(1-t)^2 = (t+2)^2`, not `(1+t)^2 = 1 + 2t + t^2`.
  Theory §4's own argument, "`(t+2)^{2a}` would need ...", uses the correct factorisation.
* **README revision table, H' row.** The error is given as `O(q^{b - log_q X})`. The term
  `O(1/G(D+1))` from theory §1 is missing.
* **C slogan.** "Every polynomial that survives its own digits survives forever" holds only as a
  count, up to polynomial factors, and only along `X = q^{L+kappa+1}`. Read literally, it is
  false.
* **Theory §4.** "With the sawtooth of Corollary T2" is a leftover of the withdrawn "explains".
  It should say "consistent with T2".
* **README item 2 / theory §5 (Baker).** The cycle inequality `|2^L - 3^a| <= C L 2^L/n` as
  written is for positive cycles with minimum `n`. Say "positive cycles". The Baker exponent is
  correctly flagged as quoted from memory.

None of these affects a proof. Verdict: `needs_repair = false`. The fixes above are recommended
wording edits, not substantive repairs.

## REFEREE1 items: were they honestly resolved?

| REFEREE1 item | resolution | status |
|---|---|---|
| S2c `h = 0.8703` WRONG | Withdrawn. `h = 0.875848` from the saddle. I computed it independently by minimising the positive root `rho(lambda)` of `4 lambda rho^2 = 2 rho + lambda^2 + 1`. It agrees with the closed form `2 lambda = (lambda^2-1)^2` to 30 digits. `h = 0.87584821`, `C* = 8.0547`. I also reproduce the biased 0.8703 (raw `P(400)/P(360)`), and with the `b^{-3/2}` correction I get 0.87603 | resolved |
| "`log2 Z_L/L -> 0.8703`" WRONG | Withdrawn. The exact `Z_L` gives 0.8536, 0.8637, ..., 0.8748 for `L = 2^8 .. 2^13`, increasing toward 0.87585 | resolved |
| single-`X` "K >= 1.05" non sequitur | Withdrawn and relabelled an illustration. I recompute the threshold as 1.0823 (quoted 1.083). REFEREE1's 1.087 used `2 rho^{b-1}`, so the two differ only in the constant | resolved |
| S2c rests on a quoted method of types (GAP) | Closed by the elementary Theorem A''. Re-derived below | resolved |
| "E_F holds exactly inside the horizon" | Proposition H' (with Lemmas S and B). Re-derived below | resolved |
| C upper bound GAP | Re-proved octave by octave; scope restricted to A3, Q4b, S2c, with the general hypothesis stated | resolved |
| H omits `D >= D_0` | Added | resolved |
| T2 "explains" the sawtooth | Withdrawn in §2 and in the README. One leftover phrase in §4 (see fixes) | resolved (nit) |
| Z omits `(1,0)`; uses Mihailescu | `(1,0)` added. The elementary mod 3 / mod 4 proof is correct (re-derived) | resolved |
| "Catalan words = G's exceptions" WRONG | Withdrawn; restated as a finite subset. The -17, 187 and 347 counterexamples are checked (also independently by me, plus the 17-cycle of 3x-1) | resolved |
| "provably absent in Z" | Replaced by the precise "no cycles of length `O(log n)`" with stated limits | resolved |
| §5 obstruction "PROVED in the sense stated" | Relabelled REMARK (heuristic); the incoherence of ingredient (iii) is stated | resolved |
| novelty sentence | Added (§6); literature flagged as quoted from memory; no literature search, stated | resolved |

## Verdicts per claim

### H. Horizon lemma: CONFIRMED
Re-derived. Fact 1: the composition `H <- g_r H + t^E h_r`, the cylinder is one class mod
`t^L`, and cylinders are disjoint. Fact 2: the exact degree walk for `deg >= D_0`, which stays
valid while the orbit has not dropped, since the degree stays `>= D >= D_0`. The branch word up
to digit length `b + e - 1` is decided by `f mod t^{b+e-1}`, and that residue is free when
`b + e - 1 <= D`. My enumeration (A3 `D <= 9`, Q4b `<= 6`, S2c `<= 14`, G3 and B3 `<= 8`) gives
0 mismatches in 269 in-horizon cells. It gives 1420 differing beyond-horizon cells, so the test
discriminates. The prover's run gives 0 in all seven systems.
Remark: the prover's script computes `D_0 = 2` for B3/G3. The definition gives `D_0 = 1`
(`deg 0 = -infinity`). The larger value is harmless, and I checked H and H' with `D_0 = 1`.

### H'. Proposition H' (new): CONFIRMED (README wording nit)
Lemma S: with `tau` = first step with `E_tau >= m`, we have `E_tau <= m + e - 1`. `A ∩ B` lies
inside survival(`b`), because steps `k > tau` with `E_k <= b` have `E_k - E_tau <= b - m`. `A`
contains survival(`m+e-1`), and `B` has probability `P(b-m)` and is independent of `A` by the
strong Markov property. Correct. Lemma B: the block families (A3: `1·{0,2}`; Q4b:
`1·{0,w,w^2}^2`; S2c: `10·0`, `10·11`) have nonnegative prefix slopes. For S2c the bound
`P(j) >= c(n) 2^{-n}` for any `n >= j`, and propagation through `c(n) = c(n-3) + c(n-4)` with
`x^4 = x + 1`, are correct. Proposition: I checked each octave range. `D' < D_1` gives at most
`q^{D_1}`. For `D_1 <= D' < B`, `m' = D'+1-e < b` and `m' >= 0`. Lemma S applies with
`m = D'+2-2e >= 0` and gives `j = b - D' + 2e - 2`, and distinct `D'` give distinct `j`. For
`B <= D' <= D` the sum is exact. If `D_1 > B`, the overlap only weakens the upper bound, so it
is still valid. For the relative form, `X P(b) >= G(D+1)` because `b <= D+1`. My check: Lemma S
holds exactly for `b <= 150` (A3, Q4b, S2c). Lemma B holds exactly for `j <= 300`. Gamma comes
out as 2.6547, 2.3488 and 4.4456, which matches the quoted `<= 2.655, 2.349, 4.446`. The
two-sided bound holds on all 311 cells of my enumeration, while the naive equality
`N = X P(b)` fails on 60 of them. The prover's check passes on 1337 cells.
It is strictly inside the horizon, and the README says so.
Nit: the README revision table gives the error as `O(q^{b - log_q X})` and omits `O(1/G(D+1))`.

### T. Lemma T: CONFIRMED
`deg term_i = L + kappa + (S_n - S_i)` follows from `sum_{j>i} deg g = (S_n-S_i) + (L-E_i)` and
`deg h_r <= e_r + kappa`. I checked the affine form exactly and the degree bound on 150 random
`(f, n)` each for A3, Q4b, S2c and G3.

### T1. Cycle inequality: CONFIRMED
Immediate from T. My check verified it on all 138 distinct A3 cycles found by my enumeration.

### T2. Frobenius sawtooth: CONFIRMED (the inequality); data reading correctly EVIDENCE
`deg(t^L - G_w) < L` forces `G_w` to be monic of degree `L`, so `G_w^* = u^{n_1} = 1 + O(s^{D'})`.
`(u^{p^j})^m = 1 + m a^{p^j} s^{nu p^j} + ...` with `p ∤ m`, and `u != 1` because `g_1` is
non-constant with `g_1(0) != 0`. Correct. My check verified it on all 138 A3 cycles
(`nu = 2`, `p = 3`).

### F. Theorem F: CONFIRMED
Re-derived. `x_w` is periodic, the points are distinct by cylinder disjointness, and the
rotation after a minimum of `S_i` has nonnegative prefix slopes, so `R = 0` and
`deg <= L + kappa`. A cycle holds at most `n <= L` of the points, and at most one cycle is
`{0}`. Independent checks:
* S2c at `L = 16`: all 1330 zero-slope words (`= Z_16`) are Frobenius (`G_w = 1 + t^16`), each
  `x_w` is periodic with word `w`, and they form 136 distinct cycles (bound 82.1). The maximal
  minimum degree is 16 (`<= 18`), and these minimum points survive 300 digits.
* S2c at `L = 12`, which is not `2^k`: 90 zero-slope words are not Frobenius, as expected. So the
  test discriminates.
* Random zero-slope words at S2c `L = 32, 64`, A3 `L = 6, 18, 54` and Q4b `L = 6, 12, 24` are all
  Frobenius and periodic.
* A3 at `L = 6`: `|W_6| = 160` and 28 cycles (bound 25.7).

### A. Theorem A (A3): CONFIRMED
`|W_L| = C(L, L/2) 2^{L/2}`, `(1+t^2)^{3^k} = 1 + t^{2·3^k}`, `kappa = 1`. The constants are
correct: `9(L+2)^2 >= 8L(L+1)`. Chernoff at `lambda = sqrt 2` gives exactly `2 sqrt 2/3`. I
checked `P(b)^2 <= (8/9)^b` exactly for `b <= 300`. The bound is sharp up to a polynomial
factor: `P(300)^2/(8/9)^300 ≈ 3e-6`. The first crossing at `L = 486` is reproduced. The
statement is beyond the horizon (`K > 1`) and the threshold is right: at `K = 1` both sides are
`X^{h+o(1)}`.

### A'. Theorem A' (Q4b): CONFIRMED
`n_1 = L/3`, `C(L, L/3) >= (27/4)^{L/3}/(L+1)`, so `|W_L| >= 60.75^{L/3}/(L+1)`. Chernoff at
`lambda^3 = 3/2` gives `9/(8 lambda) = 3(3/2)^{2/3}/4`, and times 4 that is `60.75^{1/3}`. I
checked `P(b)^3 <= (243/256)^b` exactly for `b <= 300`.

### A''. Theorem A'' (S2c, new elementary proof): CONFIRMED
Line by line:
* Step law: `0` (`s=-1, e=1`, prob 1/2), `10` (`+1, 2`, 1/4), `11` (`-1, 2`, 1/4). The slopes
  follow from `deg (1+t)^3 = 3` and `deg(1+t) = 1`. `4 lambda rho^2 F = 2rho + lambda^2 + 1`.
  `dF/dlambda = 0` gives `rho = (lambda^2-1)/2`, and substituting gives `2 lambda = (lambda^2-1)^2`.
  Correct. This saddle is the true exponential rate: my check finds it independently as
  `min_lambda rho(lambda)`, and the `b^{-3/2}`-corrected empirical rate agrees to `1e-4`.
* (a) Optional stopping: `tau` = first step with `E_tau >= b-1`, so `tau <= b` is bounded and
  `E_tau ∈ {b-1, b}`. On survival `S_tau >= 0`, so `M_tau >= rho*^{-(b-1)}`. Correct. My check
  confirms it exactly against a rational `rho_lo < rho*` for `b <= 400` (maximal ratio 0.5), and
  the same inequality with `rho = 0.9` is refuted, so the check can fail.
* (b) The multinomial count `(2a)!/((a-beta)! a! beta!) = C(2a,a) C(a,beta)` is correct. `Z_L`
  agrees with brute force for `L <= 18`. `G_w = (1+t)^{3a+beta} = (1+t)^L = 1 + t^L` for
  `L = 2^k`, and `kappa = 2`, so `X = 2^{L+3}`. The binomial bound
  `C(n,k) >= 2^{nH(k/n)}/(n+1)` (largest term of the expansion of 1) is correct.
  Tilted law: `pi_r = P(r) lambda^{s_r} rho^{-e_r}`, the mean slope is 0, so `pi_10 = 1/2` and
  `theta* = 1/lambda*^2 = 0.352723`. `-log2 pi_r = e_r - s_r log2 lambda + e_r log2 rho` gives
  `H(pi) = E_pi[e] h`, and `H(pi) = 1 + H(theta)/2` and `E_pi[e] = (3+theta)/2` are correct
  (re-derived by hand). So `phi(theta*) = h`; my check agrees to 40 digits.
  Derivative: I re-derived `dg/dbeta = log2((1-theta)/theta) - (2 - log2(1-theta))/3`
  (using `da/dbeta = -1/3` and `dtheta/dbeta = (1 + theta/3)/a`). It is decreasing, with range
  `[-0.327, 0.384]` on `[0.3, 0.4]`, and 0 at `theta*`.
  The segment claim: `theta(beta* + delta)` has `d/dL` of sign `-delta`, so the endpoints move
  monotonically toward `theta*`. That makes the claim valid for every `L >= 256`, not only for
  the checked `L`. With `(2a+1)(a+1) <= (L+1)^2` the stated bound follows.
  My check: exact big-integer `Z_L (L+1)^2 >= 2^{hL-4}` for `L = 2^8 .. 2^13`, and the
  chosen-type term alone for `L = 2^8 .. 2^15`, with a large margin (the slack used is
  negative, i.e. the bound holds with 6 to 13 bits to spare).
* (c) `X P(b) <= 2^{L+3 - (1-h)(b-1)}`, and the exponent of the ratio is
  `(1-h)(K-1)L + O(log L)`. Correct. E_F requires `N <= eps XP + X^eps` with `eps -> 0`. Both
  terms are `o(N)` along `X = 2^{2^k+3}`, so E_F fails for each `K > 1`, and M_F fails.
* External theorems: none are used. Everything is elementary.

### C. Corrected law (A3, Q4b, S2c): CONFIRMED_WITH_FIX (wording only)
The proof is now octave by octave and is valid. For S2c: `2^{D'} rho*^{D'-2} = 2^{hD'} 2^{2(1-h)}
<= 4·2^{hD'}`, with `D' >= D_0 = 2`. My enumeration gives a bounded ratio
`N(X, D+1-e)/X^h` (A3 0.35 → 0.11; S2c 0.65 → 0.11; Q4b 0.25 → 0.16). The scope sentence
(general binomial systems need the type count as a hypothesis) is honest.
Fix: rephrase the slogan "every polynomial that survives its own digits survives forever"
as "the number surviving their own digits and the number surviving forever agree up to
polynomial factors along `X = q^{L+kappa+1}`".

### Z. Integer counterpart: CONFIRMED
The elementary proof is correct (re-derived both cases). My check finds no other solution of
`|2^L - 3^a| = 1` for `L < 400`. The cycles `{0}, {-1}, {1,2}, {-5,-7,-10}` and the d-multiples
are correct. "Finite subset of G's exceptions" is right: -17 (3x+1), 17 (3x-1), 187 and 347
(3x+5) all have non-unit denominators.

### README item 2 / theory §5 Baker remark: CONFIRMED_WITH_FIX (nit)
The bound is quoted from memory and flagged as such (Rhin ~13.3; not re-checked by me either).
The deduction `L >= c n^{1/(C'+1)}` is correct for positive cycles with minimum `n`, and the
limits are stated. Fix: say "positive cycles". This is far weaker than known cycle-length
bounds in the literature, but it is used only as a contrast, and the text does not overclaim.

### §5 REMARK: correctly labelled HEURISTIC now. No further issue.

### G (EVIDENCE), Gh (HEURISTIC/CONJECTURE), U (EVIDENCE/OPEN): CONFIRMED as labelled
My enumeration confirms that B3/G3 match Haar exactly in-horizon and differ beyond it. B3 is
not binomial: its multiplier is `(t-1)^2`, and `(t-1)^{2a}` is never a binomial. Fix: the label
`(1+t)^2` (README table, theory §4) should read `1+t+t^2 = (1-t)^2`. The §4 phrase "with the
sawtooth of Corollary T2" should read "consistent with T2".

## Sanity: does the method prove something false or famous?

* Integers: the integer form of Theorem F gives exactly the unit-denominator cycles (and their
  `d`-multiples for 3x-1 and 3x+5, checked). It does not produce the 17-cycle of 3x-1 or the
  187/347 cycles of 3x+5, and the text no longer claims it does. Nothing false follows.
* Function fields: Theorem F needs exponentially many Frobenius words. At non-Frobenius lengths
  (S2c `L = 12`) words fail, and for the generic B3/G3 no word is Frobenius. For the
  Hicks-Mullen-Yucas-Zavislak map (REFEREE1's control) there is only one zero-slope word per
  `L`. The method does not prove failure where none is expected.
* Nothing in A/A'/A''/F touches the integers, so no famous statement is implied. The README
  says this clearly (items 2 to 4).

## Labels and novelty

The labels are honest. PROVED is used only for complete proofs. The withdrawn claims are listed
with the reason they were withdrawn. The literature is flagged as quoted from memory, Theorem F
is called "very likely folklore", and the lack of a literature search is stated. The novelty
claim (the use of F against the count law beyond the horizon, plus H/H') is modest and fair.

## Reproduction

* `referee2_check.py` (mine): `cd census/round5/funcfield && <venv>/bin/python referee2_check.py`,
  about 50 s, exits 0. Sections 0-9 are listed in its docstring. Each section contains a
  deliberate discrimination test that would fail if the check were vacuous.
* Prover: `<venv>/bin/python check.py` (about 6 min). Result: all six scripts exit 0 and there are 0
  in-horizon mismatches in all seven systems; `check.py` exits 0 in 7 min 53 s.
