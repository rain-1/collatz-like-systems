# Round 5, lens "function fields": Conjecture E over F_q[t]

Outcome (success level 2): **the exact analogue of Conjecture E, and of its minimal form M, is
false** for three explicit polynomial systems with negative drift and free re-entry: A3 over
F_3, Q4b over F_4 and S2c over F_2. The proofs are complete and elementary. For S2c the proof is
new in this revision; before, it rested on a quoted method of types and a wrong constant. The
failure is beyond the horizon (`b = K log_q X`, `K > 1`). Inside the horizon the count law is
proved (per octave exactly, and cumulatively for `b <= log_q X - omega(X)`). The mechanism is
Frobenius acting on the TOP digits, and it needs no carries. Its integer counterpart, the
unit-denominator cycles `2^L - 3^a = ±1`, is elementary and finite. That is a finite subset of
Generalisation G's exceptions, not all of them. Generic (non-binomial) polynomial systems obey
the count law up to about twice the horizon in the tested range and then also break. That part
is EVIDENCE plus a heuristic. Refereed once (`REFEREE1.md`) and revised (see "Revision after
REFEREE1" below); a second referee (`REFEREE2.md`) confirmed all proofs and asked only for
wording fixes (see "Revision after REFEREE2"). Proofs: `theory.md`.

Subsequent results for U. A3 has a proved divergent orbit (`../../round6/a3_divergence/README.md`, refereed). Q4b has an explicit orbit whose degree after $j$ steps is at least $9+j/2$. This settles divergence for Q4b. The other candidates in U retain their original status. [Proof, Theorem 2](../../../output/pdf/stopping_time_applications.pdf)

## Setting

`T(f) = g_r (f - r)/t^{e_r} + c_r` on the cylinder `f = r mod t^{e_r}` of a prefix code of
digit strings. `t` plays the role of 2, `g_r` the role of 3 or 5, size = degree, digits =
coefficients. `sigma(f)` = digits consumed until the degree first goes below `deg f`.
`P(b)` = Haar measure of the points not dropped within `b` digits. `N(X, b)` counts
`deg f <= log_q X - 1` with `sigma(f) > b`. The horizon is `b = deg f`.

| id | field | branches | drift/digit | Haar `h` | type |
|---|---|---|---|---|---|
| A3 | F_3 | 0: f/t; 1: (1+t^2)(f-1)/t; 2: (f-2)/t+1 | -1/3 | log_3(2√2) = 0.9464 | binomial |
| Q4b | F_4 | 0: f/t; 1: (1+t^3)(f-1)/t; w: (f-w)/t+1; w²: (f-w²)/t | -1/4 | 0.9875 | binomial |
| S2c | F_2 | `0`: f/t; `10`: (1+t)^3(f-1)/t²+1; `11`: (1+t)(f-1-t)/t²+1 | -1/3 | 0.87585 (was 0.8703, wrong) | binomial |
| B3 | F_3 | as A3 with g_1 = 1+t+t^2 = (1-t)^2, twist 1; branch 2: 2(f-2)/t | -1/3 | 0.9464 | generic |
| G3 | F_3 | as B3 with g_1 = 1+t+2t^2 | -1/3 | 0.9464 | generic |
| S2 | F_2 | as S2c with `10 -> 1+t+t^3`, twist 0 | -1/3 | 0.87585 (was 0.8703, wrong) | generic |
| Q4 | F_4 | as Q4b with g_1 = 1+t+w t^3 | -1/4 | 0.9875 | generic |

Specs are in `specs/*.txt`. Each system has an expanding branch, every branch can follow every
other (free re-entry, type (c)), and the drift is negative.

## Results

| # | statement | status | file / check |
|---|---|---|---|
| H | Horizon lemma: `N_D(b) = (q-1) q^D P(b)` exactly for `D >= D_0` and `b + e_max - 1 <= D` (every in-horizon cell of all seven systems matches) | PROVED | theory §1; `analyse.py`, `check.py` |
| H' | Cumulative count: `0 <= N(X,b) - (X - q^B) P(b) <= Gamma (q-1) q^{b+2e-2} P(b) + q^{D_1}`, so E_F holds for `b <= log_q X - omega(X)` (all seven systems). New after REFEREE1 | PROVED | theory §1 (Lemmas S, B); `check_cumulative.py` |
| T | Lemma T: the top coefficients of `T^n f` (above degree `kappa + R`) are those of `G_w f/t^L`. The top digits depend only on the branch COUNTS | PROVED | theory §2; `check_topdigits.py` |
| T1 | Cycle inequality: a periodic `f` of degree `D` has `deg(t^L - G_w) <= L + kappa + R - D` (the analogue of `\|2^L - 3^a\| <= C L 2^L/n`) | PROVED | same |
| T2 | Frobenius sawtooth: with one non-constant multiplier, a cycle at degree `D` uses it `n_1` times with `nu p^{v_p(n_1)} >= D - kappa - R` | PROVED (the inequality). That the collapses in the cycle data come from T2 is EVIDENCE only; the earlier "explains" is withdrawn | same |
| F | Frobenius cycles: if `G_w = t^L + c`, then `-H_w/c` is a polynomial periodic point. This gives `>= \|W_L\|/L - 1` never-dropping polynomials of degree `<= L + kappa` | PROVED | theory §3; `check_frobenius_cycles.py` |
| A | A3: for `L = 2·3^k`, `X = 3^{L+2}` and every `b` (including infinity), `N(X,b) >= X^h/(9 log_3^2 X) - 1`, while `X P(b) <= X 3^{-(1-h)b}`. **E_F fails for every `K > 1`, M_F fails (infinitely many `sigma = infinity`)**. Inside the horizon E_F holds, per octave exactly (H) and cumulatively for `b <= log_q X - omega` (H'). The explicit bound beats `X P(2 log X)` from `L = 486` on; the enumeration shows the excess already at `D = 10` | PROVED | theory §3; `check_theoremA.py` |
| A' | the same for Q4b (`L = 3·2^k`, `h = 0.98747`) | PROVED | theory §3; `check_theoremA.py` |
| A'' | S2c (`L = 2^k >= 256`, `h = 1 + log_2 rho* = 0.875848`): `P(b) <= rho*^{b-1}` (optional stopping) and `N(2^{L+3}, infinity) >= 2^{hL-4}/(L(L+1)^2) - 1` (largest multinomial, elementary binomial bound, tilt identity). E_F fails for every `K > 1`, M_F fails. Replaces the quoted method of types and the withdrawn `h = 0.8703` and "`K >= 1.05` at `L = 2048`" | PROVED | theory §3; `check_s2c.py` |
| C | Corrected law: `N(X, b) <= C X^h` for all `X` and `b >= log_q X - e_max`, and `N(X, b) >= X^h/poly(log X)` along `X = q^{L+kappa+1}`; survivors stop thinning at the horizon. Upper bound now proved octave by octave | PROVED for A3, Q4b, S2c only; for general binomial systems it needs the type count `\|W_{L_k}\| = q^{hL_k + o(L_k)}` as a hypothesis | theory §3 |
| Z | Integer counterpart of F: `2^L - 3^a = ±1` holds exactly for `(L,a) = (1,0),(1,1),(2,1),(3,2)` (elementary, mod 3 / mod 4). These give the 3x+1 cycles {0}, {-1}, {1,2}, {-5,-7,-10} (and the d-multiples for 3x+d). This is a finite SUBSET of G's exceptions (G also has, e.g., the -17 cycle with denominator -139) | PROVED | theory §5; `check_integer_catalan.py` |
| G | Generic systems: count law within noise to `b ≈ 2D` (G3, S2), then excess from cycles; B3 deviates from `1.5D`; Q4 has a deficit at `2 to 6 D`; the number of cycles grows with `D` in a sawtooth at powers of `p` | EVIDENCE | `analyse.py`, `data/` |
| Gh | Heuristic: Frobenius-divisible counts make `t^L - G_w = Delta^{p^k}` with `deg Delta` fixed, giving about `q^{p^k(hM - deg Delta)}` cycles; E_F fails generically with a power-law excess; the critical constant `C* = 1/(1-h)` reappears | HEURISTIC / CONJECTURE | theory §4 |
| U | Orbits passing degree 4000 without repeating, despite negative drift (A3: orbit of 1+t+t^2+2t^4+2t^5+2t^7 grows at about 0.33 degrees per step; similar for B3, G3, S2c, Q4b); no certificate found | EVIDENCE / OPEN | `data/cyc/`, `scratch/certsearch.py` |

## Beyond-horizon data (D >= 8, cells with expected >= 5; exhaustive over all polynomials)

| system | `b/D` 1-1.5 | 1.5-2 | 2-3 | 3-4 | 4-6 | 6-10 |
|---|---|---|---|---|---|---|
| A3 (binomial) obs/exp | 1.060 | 1.75 | 4.45 | 16.1 | 82 | 1380 |
| Q4b (binomial) | 1.014 | 1.18 | 1.61 | 2.63 | 4.97 | 14.4 |
| S2c (binomial) | 1.016 | 1.84 | 7.58 | 72 | 654 | - |
| B3 | 1.002 | 1.062 | 1.54 | 2.81 | 9.8 | 132 |
| G3 | 1.0001 (χ²/cell 0.66) | 0.9995 (2.3) | 0.9955 (3.6) | 1.010 (23) | 1.73 | 16.9 |
| S2 | 0.9993 (0.78) | 1.005 (0.96) | 0.997 (6.3) | 1.11 (14) | 2.95 | - |
| Q4 | 1.0004 (0.38) | 1.0002 (1.2) | 0.947 | 0.865 | 0.83 | 1.00 |

Degree ranges: F_3 `D <= 16`, F_2 `D <= 24`, F_4 `D <= 12`. In every system the transient
survivors (`sigma` finite) fall BELOW the Haar prediction beyond about `2D`: cycles capture
orbits that Haar would let continue and then drop.

## What this says about the integer proof

1. The function-field failure does not come from the missing carries in the low digits:
   generic systems equidistribute fine to about `2D`. It comes from the top digits (Lemma T).
   With no carries the leading digits evolve on their own, by `G_w^*` in the pro-p group
   `1 + sF_q[[s]]`, where Frobenius gives exact or near returns (`u^{p^k} = 1 + O(s^{nu p^k})`).
   That produces cycles exponentially often (T1, F).
2. In `Z` the leading digits evolve by the real number `3^a/2^L`. Exact returns
   (`2^L - 3^a = ±1`) give only the four small cycles of (Z). A Baker-type bound
   (`|a log 3 - L log 2| >= L^{-C}`, quoted from memory) together with the cycle inequality forces
   every positive cycle with minimum `n` to have length `L >= c n^{1/(C+1)}`. So `Z` has no positive
   cycles of length `O(log n)`, unlike the cycles of length `L ≈ D` of A3. This does not show that `Z` has
   few cycles, nor that no other mechanism breaks E. (Revision after REFEREE1: this replaces "the
   cycle obstruction is provably absent in `Z`".)
3. REMARK (heuristic, theory §5; previously mislabelled as a proved obstruction): an argument
   that used only the cylinder structure, the affine form of the iterates, finite digit
   expansions with an exact size walk, and the Haar law of branches would also apply to A3,
   where E fails. This is not formalised, and the exact size walk does not hold in `Z`, so it
   is motivation only. It suggests, but does not prove, that a proof of E for integers would
   use an archimedean input (a Baker-type separation or the equidistribution of
   `a log_2 3 mod 1`) together with carries that bring this information down to the middle
   digits. In the integer case that is the step "middle digits of `3^A s` are generic". Its
   function-field version, "middle coefficients of `G_w f` are generic", is false whenever
   `G_w` is Frobenius-sparse.
4. Caution for the integer evidence: generic polynomial systems match Haar within noise up to
   `b ≈ 2D` and fail later. Agreement up to `b/m ≈ 3` in the integer tables is therefore
   compatible with a later failure in principle. In `Z` the specific mechanism found here is
   ruled out by (2).

## Honest limits / open

* The disproof covers binomial systems (an exact identity `G_w = t^L + c` for all zero-slope
  words of certain lengths). For generic systems the failure of E_F is EVIDENCE + HEURISTIC
  only. Exactly where it stalls: proving that `Delta^{p^k}` divides `H_w` for exponentially many
  Frobenius-divisible words. No structural reason was found, and the line-renormalization
  search found no certificate.
* No positive beyond-horizon theorem was found for any polynomial system. Proposition H' is strictly inside the horizon. The linear-algebra
  form (count = `#{w : H_w in t^b Poly + G_w Poly}`) reduces E_F to an equidistribution of
  `H_w mod G_w` that is as hard as the original.
* Possibly divergent orbits with negative drift (U) are OPEN. If proved, they would show GLOBAL
  failing for negative-drift free re-entry systems in characteristic p.
* Sizes: exhaustive enumeration up to `3^17`, `2^25`, `4^13` polynomials, cap 400 digits.
  "Never-dropping" means `sigma > 400`, and `survive_cyc.c` classifies these into cycles,
  preperiodic and unresolved (Brent's method, 2·10^6 steps or degree 4096).

## Files

* `theory.md`: definitions and all proofs.
* `ffmap.py`: exact reference arithmetic, exact `P(b)`.
* `survive.c`: exhaustive counts. `survive_cyc.c`: the same plus cycle classification and
  orbit tools. Build with `gcc -O2`.
* `analyse.py`: tables. `data/*.txt`: counts. `data/cyc/*.txt`: cycle classification.
* Checks (exact, each exits 0 and can fail): `check_frobenius_cycles.py`, `check_theoremA.py`,
  `check_topdigits.py` (about 5 min), `check_integer_catalan.py`, `check_s2c.py` (Theorem A''),
  `check_cumulative.py` (Proposition H', about 1 s); `check.py` runs all of them
  plus the horizon lemma. Run from this folder; `data/` must exist (rerun `survive` if not:
  `./survive specs/A3.txt 1 16 400 > data/A3.txt`, etc.).
* `scratch/`: exploration (cycle listing, sparse-orbit search, certificate search), EVIDENCE only.
  `scratch/check_run_r1.txt`: output of the full `check.py` run after the revision.
* `REFEREE1.md`, `referee1_check.py`: the referee's report and independent check (not edited).
  After this revision the two "REFUTED" lines it prints refer to the withdrawn S2c claims.

## Novelty and literature

Function-field analogues of 3x+1 are classical (quoted from memory, not re-checked: Hicks,
Mullen, Yucas and Zavislak, Amer. Math. Monthly 2008; Matthews and Leigh, J. Number Theory
1987). Theorem F (Frobenius periodic points) is very likely folklore. The new content is its
use, with the exact counts of Theorems A, A' and A'', against the count law E_F beyond the
horizon, and the exact in-horizon statements H and H'. No literature search was done.

## Revision after REFEREE1

Every GAP, WRONG and fix item in `REFEREE1.md`, and what was done:

| referee item | verdict | action |
|---|---|---|
| S2c `h = 0.8703` (README table, theory §3), and S2 | WRONG | Withdrawn. The correct value is `h = 0.875848` (saddle of `2 rho + lambda^2 + 1 = 4 lambda rho^2`, `lambda* = 1.6838`, `rho* = 0.91754`), so `C* = 8.055`. `analyse.py` now labels its finite-`b` value as a biased estimate |
| "`log_2 Z_L/L -> 0.8703`" | WRONG | Withdrawn; the limit is 0.875848, and the proved lower bound reaches 0.87584 at `L = 2^22` |
| "at `L = 2048` E_F fails for every `K >= 1.05`" | WRONG logic | Withdrawn. One `X` cannot falsify an asymptotic statement. As an illustration only, the proved bounds give the threshold `K > 1.083` at that `X` |
| S2c for all `K > 1` rests on a quoted method of types | GAP | Closed: Theorem A'' gives a complete elementary proof (optional stopping; largest multinomial; `C(n,k) >= 2^{nH}/(n+1)`; tilt identity `phi(theta*) = h`; Lipschitz approximation). `check_s2c.py` |
| "E_F holds exactly inside the horizon" | fix | True only per octave. New Proposition H' (with Lemmas S and B) gives the cumulative statement: E_F for `b <= log_q X - omega(X)`, error `O(q^{b - log_q X}) + O(1/G(D+1))`, checked on all 1337 data cells |
| Corrected law C, upper bound | GAP | Re-proved octave by octave. C is restricted to A3, Q4b and S2c. For general binomial systems the type count is stated as a needed hypothesis |
| H table omits `D >= D_0` | fix | Added |
| T2 "explains" the data sawtooth (G3 at `D = 10`) | loose | Withdrawn as an explanation; the data are stated as EVIDENCE consistent with T2, with the G3 boundary case spelled out |
| Z omits `(1,0)`, the cycle `{0}` | fix | Added; check updated |
| Z uses Mihailescu | fix | Replaced by the elementary mod 3 / mod 4 proof (theory §5) |
| "Catalan words = the finite set of exceptions G allows" | WRONG | Withdrawn. Correct: unit-denominator cycles are a finite SUBSET of G's exceptions. Counterexamples (-17 in 3x+1; 187 and 347 in 3x+5) are checked in `check_integer_catalan.py` |
| "provably absent in `Z`" | fix | Replaced by the precise Baker statement (no cycles of length `O(log n)`), with its limits |
| §5 obstruction "PROVED in the sense stated", bold "must" | GAP / mislabel | Relabelled REMARK (heuristic). Its incoherence (an exact size walk is false in `Z`) is stated |
| No novelty or literature sentence | fix | Added (theory §6, above) |

Unchanged and confirmed by the referee: H, T, T1, F, A, A', G (EVIDENCE), Gh (HEURISTIC), U
(EVIDENCE/OPEN).

## Revision after REFEREE2

`REFEREE2.md` confirms every PROVED item (verdict `needs_repair = false`) and lists five wording
fixes. All five are applied; no proof was changed.

| REFEREE2 item | action |
|---|---|
| B3 multiplier mislabelled `(1+t)^2` | Now `1+t+t^2 = (1-t)^2` (as in `specs/B3.txt`) in the system table and theory §4 |
| H' error term in the REFEREE1 revision table omits `O(1/G(D+1))` | Added: error `O(q^{b - log_q X}) + O(1/G(D+1))`, as in theory §1 |
| C slogan "every polynomial that survives its own digits survives forever" | Theory §3 now says: up to polynomial factors and along `X = q^{L+kappa+1}`, the number surviving their own digits and the number surviving forever agree (a statement about counts only) |
| Theory §4 "with the sawtooth of Corollary T2" | Now "consistent with Corollary T2" |
| Baker remark (README item 2, theory §5) | Now says "positive cycles" with minimum `n` |

Not changed: REFEREE2's side remark that the prover's script uses `D_0 = 2` for B3/G3 where the
definition gives `D_0 = 1`; the referee calls it harmless and checked H and H' with `D_0 = 1`,
and it is not listed as a fix.
