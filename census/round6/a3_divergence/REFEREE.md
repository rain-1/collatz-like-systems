# Referee report: divergent A3 orbit (README.md, 28 Nov 2026)

Independent referee pass. I re-derived each step by hand and wrote a fresh check,
`referee_check.py`, which does not import `a3.py`, `theta.py` or `check_a3_divergence.py`. I did
not edit the prover's files.

**Overall verdict: the theorem as stated is fully proved.** I found no mathematical error. Four
places need a sentence or a small correction (fixes F1 to F4 below). None of them changes a
statement.

## Item verdicts

### Step 1 (renormalisation): CONFIRMED

* *The first six branches depend only on g mod t^6.* Each branch sends coefficient index `i` of
  the input to output indices `>= i - 1`. Branch 1 gives `out_i = f_{i+1} + f_{i-1}`, and the
  others give `out_i = f_{i+1}`, plus a constant for branch 2. After `j` steps, index `>= 6`
  affects only indices `>= 6 - j`. The branch at step `j+1 <= 6` reads index 0 of `T^j g`, and
  `6 - j >= 1` for these steps. Correct.
* *Affine law on a cylinder.* By induction, `T^j(g + t^6 h) = T^j(g) + (1+t^2)^{a_j} t^{6-j} h`
  for `j <= 6`. The added term has zero constant term for `j < 6`, so the branch word is shared.
  For `j = 6` this gives `T^6(g + t^6 h) = T^6(g) + (1+t^2)^a h`. Correct. The check tests it
  directly on 3000 random pairs `(g, h)`.
* *Base cases.* `f_0 = 1+2t -> 2+2t^2 -> 1+2t`, which has period 2 and word 121212.
  `f_2 = 1 + 2t^2 + t^4 + t^5 + t^7` has word 102101 and is fixed by `T^6`. `f_1` has word 111111
  and `T^6 f_1 = f_s`. Branch 1 occurs 3, 6 and 3 times in the three words, and
  `(1+t^2)^3 = 1 + t^6` in characteristic 3. All verified.
* *The identity for all K.* Write `K = k_0 + sM`. Then
  `T^6 f_K = f_{Theta(k_0)} + G(t^6) M(t^6) q = f_{Theta(k_0) + GM}`, since `K -> K(t^6) q` is
  additive. The formulas give `Theta(k_0 + sM) = Theta(k_0) + GM`. The division by `s` is exact
  because the numerator has constant term `k_0 - 1 = 0` or `k_0 - k_0 = 0`. `K = 0` gives
  `Theta(0) = 0` and `f_0` is fixed. `k_0 = 0` with `K != 0` is covered by the same identity.
  Verified exhaustively on all 729 polynomials of degree `<= 5` (including 0), on 500 random K of
  degree 6 to 120, and on 200 random K with `k_0 = 0` or `k_0 = 2`. In each case the branch word
  and the exact equality `T^6(f_K) = f_{Theta(K)}` hold, and every division by `s` is asserted
  exact.

### Step 2 (degrees): CONFIRMED_WITH_FIX (F1)

`deg q = 7`, `deg c = 1`, and `K(t^6) q` has leading coefficient `2 lead(K)`, so
`deg f_K = 6 deg K + 7` for `K != 0`.

* For `k_0 = 1`, `(1+s)^2 K - 1` has degree `deg K + 2` and leading coefficient `lead(K)`. The
  `-1` touches only the constant term, which is not the leading term because `deg >= 2`. Dividing
  by `s` and adding 1 gives degree `deg K + 1 >= 1`. For `K = 1` this is `s`.
* For `k_0 in {0, 2}`, `(1+s)K - k_0` has degree `deg K + 1 >= 1`. Subtracting `k_0` cannot
  cancel the leading term. The result has degree `deg K` with the same leading coefficient. For
  the constant `K = 2`, `Theta(2) = 2s/s = 2`.

No cancellation is possible in either case. Verified on all deg `<= 5` and 500 random K,
including the leading coefficient. The check also verifies the one-step degree changes `-1, +1, -1`
for degree `>= 2`.

**F1.** The proof does not say that `Theta^n(1) != 0` for all `n`, which is needed for
`deg T^{6n} f = 6 D_n + 7`. It follows at once from the degree being non-decreasing from 0. Add
that sentence.

### Step 3 (the raising branch recurs): CONFIRMED_WITH_FIX (F2, F3)

* `N(K)_i = k_i + k_{i+1}`: correct. `N` is `Theta` on both non-raising branches, because the
  formula for `k_0 = 0` is the same formula. Verified.
* *N^n(K) is the polynomial part of (1+1/s)^n K.* This is true, but the README gives no reason
  (**F2**). If `X = P + R` with `R` in `s^{-1} F_3[s^{-1}]`, then `(1+1/s) R` has no polynomial
  part, so `pp((1+1/s) pp(X)) = pp((1+1/s) X)`. Induction finishes it. Verified on 300 random
  `(K, n)` with `n < 60`. The check also confirms the constant term against
  `sum_j C(n,j) k_j mod 3` computed by Lucas' theorem.
* `L = s + (1+s)^2 M`: correct, since `((1+s)^2 - 1)/s + 1 = 2 + s + 1 = s`.
* The first constant term is `CT[(1+s)^n s^{1-n}]`, the coefficient of `s^{n-1}` in `(1+s)^n`,
  which is `C(n, n-1) = n`. Correct.
* The second constant term: `(1+1/s)^n (1+s)^2 M = (1+s)^{n+2} s^{-n} M`. With `n + 2 = 3^m`,
  `(1+s)^{3^m} = 1 + s^{3^m}`, so this is `s^{2-3^m} M + s^2 M`. Its constant term is
  `M_{3^m - 2} + 0`, and `M_{3^m - 2} = 0` because `3^m - 2 > deg M`. Correct. The README omits
  the `s^2 M` part, which is trivially 0.
* `n = 3^m - 2 = 1 mod 3` needs `m >= 1`, and the README requires it. For `M = 0`, `m = 1` and
  `n = 1`, which gives `1 -> s -> 1+s`, raising again at step 2. Correct.
* *Off-by-one.* If the raising step happens at time `r`, then `L` is at time `r+1`. The `n`
  steps applied to `L, ..., N^{n-1} L` are those at times `r+1, ..., r+n`, and `N^n L` (time
  `r+n+1`) has constant term 1. The gap is therefore at most `n + 1 = 3^m - 1`, as claimed. If
  an earlier step among them raises, the gap is smaller. Correct. The check finds the bound
  **attained**: the maximum of gap/(3^m - 1) is exactly 1.000, both on 300 random raising starts
  and along the orbit of 1.
* Key lemma verified exhaustively for all `M` of degree `<= 6` (including `M = 0`) and on 300
  random `M` up to degree 40. A direct gap test from random raising starts `K = 1 + sM` also
  passes.

**Rate: CONFIRMED_WITH_FIX (F3).** At the step that raises the degree to `D`, `deg M = D - 2`.
For `D = 1` we have `M = 0`, so it should read `deg M <= D - 2`. The smallest `m >= 1` with
`3^m > D` satisfies `3^m <= 3D`, so the gap is at most `3D - 1`. With `r_1 = 0`, degree `D` is
reached by time `1 + sum_{j<D} (3j - 1) <= 3D(D+1)/2`. If `D` is the largest integer with
`3D(D+1)/2 <= n`, then `(D+2)^2 > (D+1)(D+2) > 2n/3`, which gives `D_n >= D > sqrt(2n/3) - 2`.
That last line is not written out in the README; adding it is recommended (part of F3). Verified
along 60000 Theta steps.

**Intermediate degrees: CONFIRMED.** For degree `>= 2` each step changes the degree by exactly
`+1, -1, -1` on branches 1, 0, 2. Inside a block the degrees follow the three words:
121212 gives `d, d+1, d, ...`; 102101 gives `d, d+1, d, d-1, d, d-1`; 111111 gives
`d, ..., d+5`. So the intermediate degrees lie in `[6D_n + 6, 6D_n + 12]`. The README's "within
6" is true, and the sharp statement is within 5, at most 1 below. Verified on the raw orbit.

### Remark: orbits that never raise are periodic from the start: CONFIRMED_WITH_FIX (F4)

`N` preserves degree and leading coefficient. On `V_d` (degree `<= d`) it is `I + shift`, which
is unipotent and therefore a bijection of a finite set. Every `N`-orbit is therefore purely
periodic, and its period divides a power of 3. An orbit of `Theta` that never takes `k_0 = 1` is
an `N`-orbit, so it is purely periodic. An orbit that takes the raising branch once takes it
infinitely often by Step 3, so its degree tends to infinity. The two-behaviour statement is
correct.

**F4.** "N is invertible on polynomials of a fixed degree" should add "and that set is finite",
because finiteness is what gives *pure* periodicity. Verified exhaustively for degree `<= 5`:
`N` is a bijection on each `V_d`. Of the 729 K, 8 have purely periodic non-raising orbits
(among them 0 and 2) and 721 raise.

### Honesty of status and remarks: CONFIRMED (minor nit)

* Calling the result PROVED is justified.
* "Numerically D_n is about n/3" is accurate: `D_n / n = 0.3316` at `n = 60000`.
* The characteristic-3 and "no integer analogue implied" remarks are appropriately hedged.
* The pointer to Q4b in `output/tex/stopping_time_applications.tex` (Theorem 2) exists.
* Nit: the Files section says the prover's random K have "degree up to 59". `randrange(8,60)`
  gives lengths 8 to 59, so the maximum degree is 58. The count of 3679 conjugacy cases includes
  duplicate trimmed tuples (3279 tuples over 2187 distinct K of degree `<= 6`, plus 400 random).
  Neither point is an error in the proof.
* Housekeeping, not for this folder: `../../round5/funcfield/README.md` still lists item U as
  EVIDENCE / OPEN. Once this result is accepted, the A3 part of U should point here.

## Checks run

* `python3 check_a3_divergence.py` (prover): **exit 0**, "CHECK passed". It covered 3679
  conjugacy cases, and the final degree of K after 60000 steps is 19896 (about 50 s).
* `python3 referee_check.py` (this referee, defaults 60000 raw A3 steps and 60000 Theta steps):
  **exit 0**, "REFEREE CHECK passed" (about 7 s). It checks:
  * Step 1: the seed is `f_1`; the identities `(1+t^2)^3 = 1+t^6` and `(1+t^2)^6 = (1+t^6)^2`;
    the three base cases; mod `t^6` dependence and the affine law on 3000 random pairs; the
    conjugacy and branch words on all 729 K of degree `<= 5`, 500 random K of degree 6 to 120,
    and 200 random K with `k_0` in {0, 2}.
  * Step 2: degrees and leading coefficients; the one-step degree changes.
  * Step 3: the formula for `N`; `N^n` equals the polynomial part (Lucas cross-check);
    `C(n, n-1) = n mod 3`; the formula for `L`; the key lemma on 2487 `M`; the gap from 300
    random raising starts (maximum ratio 1.000).
  * Remark: `N` is a bijection on `V_d` for `d <= 5`, and the periodic or raising dichotomy holds
    on all deg `<= 5`.
  * Raw orbit: 60000 direct A3 steps (10000 blocks) in exact numpy arithmetic mod 3. At every
    block it checks `T^{6n} f = f_{Theta^n(1)}` exactly, which implies degree `6 D_n + 7`. It
    also checks the branch word of every block against `k_0`, that block degrees never decrease,
    and that no intermediate degree is more than 1 below its block value. The final degree is
    19945, so `D_10000 = 3323`.
  * Theta orbit of 1: 60000 steps to final degree 19896. Every gap satisfies `<= 3^m - 1`
    (maximum ratio 1.000) and `<= 3D`, and `D_n >= sqrt(2n/3) - 2` holds for every `n`.
  * Mutation tests, all **detected**:
    * branch-1 multiplier `1+t` (81 failures);
    * `t^7` coefficient of `q` changed (54);
    * raising branch with `(1+s)^1` (27);
    * key lemma with `n = 3^m - 3` (486) or `n = 3^m - 1` (729);
    * raw orbit from a mutated seed (degree law fails).

    The script exits 1 if any mutation goes undetected.

## Fixes requested (all editorial)

* **F1** (Step 2): say that `Theta^n(1) != 0` because the degree never decreases from 0, so
  `deg T^{6n} f = 6 D_n + 7` applies for every `n`.
* **F2** (Step 3): add the one-line reason that `N^n(K)` is the polynomial part of
  `(1+1/s)^n K`: negative powers never feed back into the polynomial part.
* **F3** (Rate): change `deg M = D - 2` to `deg M <= D - 2` (since `M = 0` at `D = 1`), and
  write out the step from "degree D within 3D(D+1)/2 steps" to `D_n >= sqrt(2n/3) - 2`.
  Optionally note that the gap bound `3^m - 1` is attained.
* **F4** (Remark): add that `V_d` is finite, since that is what makes the orbits *purely*
  periodic.
* Optionally, sharpen "within 6" to "within 5, and at most 1 below `6 D_n + 7`", and correct
  "degree up to 59" to 58 in the Files section.
