# Conjecture E over F_q[t]: definitions, proofs, and where it breaks

Labels: PROVED (complete proof below, finite content checked by a script that exits 0 and can
fail), EVIDENCE (numerical), HEURISTIC, REMARK, CONJECTURE, OPEN. Refereed once (`REFEREE1.md`)
and revised. Every change made in response is marked "Revision after REFEREE1". Withdrawn
statements are named as withdrawn, not silently removed.

## 1. Setting and definitions

`q = p^f`, `F_q[[t]]` with Haar measure `mu`. A *system* is a complete prefix code of digit
strings `r` (branch `r` has length `e_r`), and for each branch a multiplier `g_r in F_q[t]` with
`g_r(0) != 0` and a twist `c_r in F_q[t]`:

    T(f) = g_r (f - r) / t^{e_r} + c_r        when f = r (mod t^{e_r})

(`r` read as a polynomial of degree `< e_r`). The role of 2 is played by `t`, the role of 3 or 5
by the multipliers, "size" is the degree, "digits" are coefficients. The slope of branch `r`
is `s_r = deg g_r - e_r`. For a branch word `w = (r_1, ..., r_n)` put `E_i = e_{r_1} + ... +
e_{r_i}`, `L(w) = E_n`, `S_i = s_{r_1} + ... + s_{r_i}`, `G_w = g_{r_1} ... g_{r_n}` and

    H_w = sum_{i=1..n} (g_{r_{i+1}} ... g_{r_n}) h_{r_i} t^{E_{i-1}},   h_r = t^{e_r} c_r - g_r r.

**Fact 1 (cylinders; PROVED).** The set `C_w` of `x in F_q[[t]]` whose first `n` branches are
`w` is the residue class `{x : G_w x + H_w = 0 mod t^L}` (`L = L(w)`), and on it
`T^n(x) = (G_w x + H_w)/t^L`, an affine bijection `C_w -> F_q[[t]]`. Distinct words of the same
digit length have disjoint cylinders. *Proof.* Induction on `n`: applying branch `r` to
`(Gx + H)/t^E` gives `(g_r G x + g_r H + t^E h_r)/t^{E+e_r}`. On the cylinder of `r`,
`x = r + t^e y` maps to `g_r y + c_r`, a bijection because `g_r` is a unit of `F_q[[t]]`. So
`C_w` is a class mod `t^L` of measure `q^{-L}`, it lies inside the class where the formula is
integral, which also has measure `q^{-L}`, so the two are equal. At the first place two words
differ, the same value takes different branches, so the cylinders are disjoint. ∎

Consequently, under Haar measure the branch sequence is i.i.d. with `P(r) = q^{-e_r}`. The
*drift* is `E[s]/E[e]` (per digit). All systems studied have negative drift and free re-entry:
an expanding branch (`s_r > 0`) whose fixed point lies in one strongly connected cylinder
component with contracting branches (for one-digit codes every branch may follow every branch).

**Fact 2 (exact degree walk; PROVED).** If `deg f >= e_r` and `deg f + s_r > deg c_r`, then
`deg T(f) = deg f + s_r` (`deg g_r(f - r) = deg g_r + deg f` since `deg r < e_r <= deg f`). Put
`D_0 = max_r max(e_r, deg c_r - s_r + 1)`. For `deg f >= D_0`, as long as the degree has not gone
below `deg f`, the degree after `i` steps is exactly `deg f + S_i`. There are no carries and no
error terms.

**Definitions.**

* `sigma(f)` = number of digits (divisions by `t`) consumed up to the end of the first step at
  which `deg T^k(f) < deg f`; `sigma(f) = infinity` if there is none.
* `P(b)` = `mu{x : S_k >= 0 at every step end with E_k <= b}`.
* `N_D(b) = #{f : deg f = D, sigma(f) > b}` (one "octave"), and with `X = q^{D+1}`,
  `N(X, b) = #{f != 0 : deg f <= D, sigma(f) > b}`.
* The horizon: a polynomial of degree `D` has `D + 1` digits. Beyond `b = D` the cylinder of
  `f` mod `t^b` is `f` itself followed by zeros.

**Horizon lemma (PROVED; `analyse.py` checks every in-horizon cell exactly).** If `D >= D_0` and
`b + e_max - 1 <= D`, then `N_D(b) = (q-1) q^D P(b)`. *Proof.* By Fact 2 and induction, for
`deg f = D` the event `sigma(f) > b` equals the event that the slope walk of the branch word
of `f` stays `>= 0` at every step end with `E_k <= b`. Those steps are decided by digits
`0 .. b + e_max - 2 <= D - 1` of `f`, which run over all `q^D` values independently of the
`q - 1` leading coefficients, and by Fact 1 the event is a union of cylinders of total measure
`P(b)`. ∎ (Every in-horizon cell of the seven systems, D <= 12 to 24, matches exactly.)

**Revision after REFEREE1: the cumulative count.** The horizon lemma is a statement about one
octave `N_D`. The cumulative count `N(X, b)` also contains the low octaves `D' < b + e_max - 1`,
which are beyond their own horizon. So the earlier sentence "E_F holds exactly inside the
horizon" was true only per octave. The following lemmas give the correct cumulative statement.

**Lemma S (supermultiplicativity; PROVED).** For `0 <= m <= b`, `P(b) >= P(m + e_max - 1) P(b - m)`.
*Proof.* Under Haar measure the branches are i.i.d. (Fact 1). Let `tau` be the first step with
`E_tau >= m`, so `E_tau <= m + e_max - 1`. Let `A = {S_k >= 0 for all k <= tau}`, which is
determined by the first `tau` steps, and
`B = {S_{tau+j} - S_tau >= 0 for all j with E_{tau+j} - E_tau <= b - m}`. If a step `k` has
`E_k <= b`, then either `k <= tau` (covered by `A`) or `k > tau` and `E_k - E_tau <= b - m`, so
`S_k = S_tau + (S_k - S_tau) >= 0` on `A ∩ B`. Hence `A ∩ B` is contained in the survival event
for `b`. `A` contains the survival event for `m + e_max - 1`, because every `k <= tau` has
`E_k <= m + e_max - 1`. By the strong Markov property `B` is independent of `A` and has
probability `P(b - m)`. ∎

**Lemma B (block growth; PROVED).** Put `G(j) = q^j P(j)`.
* Step law of A3 (shared by B3, G3: slopes `+1, -1, -1`, one digit each):
  `G(j) >= 2^{j/2}/3`.
* Step law of Q4b (shared by Q4: `+2, -1, -1, -1`): `G(j) >= 9^{j/3}/16`.
* Step law of S2c (shared by S2: `0` slope -1 with 1 digit; `10` slope +1 with 2 digits; `11`
  slope -1 with 2 digits): `G(j) >= c(n) 2^{j-n}` for every `n >= j`, where `c(n)` is the number
  of compositions of `n` into parts 3 and 4. So `G(j) >= alpha x^j / 8` with `x = 1.2207...`
  (`x^4 = x + 1`) and some `alpha > 0`.

*Proof.* Distinct words of the same digit length have disjoint cylinders of measure `q^{-length}`
(Fact 1), and `P` is nonincreasing. A3: the blocks "1 then 0 or 2" have prefix slopes `+1, 0`.
Any concatenation of `m` blocks survives `2m` digits, so `P(2m) >= 2^m 3^{-2m}`. Q4b: the blocks
"1 then two of `0, w, w^2`" (9 blocks of 3 digits) have prefix slopes `+2, +1, 0`. S2c: the
blocks `10·0` (3 digits) and `10·11` (4 digits) have prefix slopes `+1, 0`. A sequence of blocks
of total length `n >= j` survives `j` digits. For S2c, `c(n) = c(n-3) + c(n-4)`, so
`c(n) >= alpha x^n` on four consecutive values of `n` propagates to all larger `n`.
(`check_cumulative.py` also compares these bounds with the exact `P(j)`, `j <= 400`.) ∎

Consequently `Gamma := sum_{j >= 0} 1/G(j)` is finite. For these step laws it is at most
2.655 (A3), 2.349 (Q4b) and 4.446 (S2c), from the exact `P(j)` for `j <= 300` plus the block tail.

**Proposition H' (cumulative count inside the horizon; PROVED for all seven systems).** Let
`e = e_max`, `D_1 = max(D_0, 2e - 2)`, `D >= D_0`, `X = q^{D+1}`, `0 <= b <= D + 2 - e` and
`B = max(D_0, b + e - 1)`. Then

    0  <=  N(X, b) - (X - q^B) P(b)  <=  Gamma (q-1) q^{b + 2e - 2} P(b) + q^{D_1}.

So `N(X, b) = X P(b) (1 + O(q^{b - log_q X}) + O(1/G(D+1)))`. In particular, E_F (for the cumulative
count) holds uniformly for `b <= log_q X - omega(X)` for every function `omega -> infinity`,
with relative error `O(q^{-omega})`. At `b = log_q X - O(1)` the relative error is only `O(1)`.

*Proof.* By the horizon lemma the octaves `B <= D' <= D` contribute exactly
`sum (q-1) q^{D'} P(b) = (q^{D+1} - q^B) P(b)`. That gives the lower bound, since all other
terms are `>= 0`. The octaves `D' < D_1` contribute at most `q^{D_1}` polynomials. For
`D_1 <= D' < B` we have `m' := D' + 1 - e < b`. Monotonicity in `b` and the horizon lemma at
`m'` give `N_{D'}(b) <= N_{D'}(m') = (q-1) q^{D'} P(m')`. Lemma S with `m = m' - e + 1 >= 0`
gives `P(m') <= P(b)/P(j)` with `j = b - D' + 2e - 2 >= 0`. So
`N_{D'}(b) <= (q-1) q^{b + 2e - 2} P(b)/G(j)`. Distinct `D'` give distinct `j`, so the sum is at
most `Gamma (q-1) q^{b+2e-2} P(b)`. For the relative form, `q^B/X <= q^{b + e - 2 - D} + q^{D_0 - D - 1}`
and `X P(b) >= X P(D+1) = G(D+1) -> infinity` (Lemma B). ∎

`check_cumulative.py` verifies the two-sided inequality exactly on every cell `(D, b)` of the
exhaustive data of all seven systems (1337 cells). The observed relative error is about
`q^{b - D - 1}`, which comes from the missing low octaves, as the proof predicts.

**Conjecture E_F (the analogue of E).** For every `K` there is `eps(X) -> 0` with
`|N(X, b) - X P(b)| <= eps(X) X P(b) + X^{eps(X)}` for all `b <= K log_q X`.
**Minimal form M_F.** There is `C` with `sigma(f) <= C deg f` for all large `deg f`.

## 2. Lemma T: the top digits decouple (PROVED)

**Lemma T.** For every `f` and word `w` (the branch word of the first `n` steps of `f`),
`T^n f = (G_w f + H_w)/t^L` and

    deg H_w <= L + kappa + R,   kappa = max_r max(deg g_r - 1, deg c_r),
                                R = max_{1<=i<=n} (S_n - S_i)  (>= 0).

So every coefficient of `T^n f` in degree `> kappa + R` equals the corresponding coefficient of
`G_w f / t^L`. That is, **the top digits of the orbit depend only on the top digits of `f`
and on `G_w`, which depends only on how many times each branch was used.**

*Proof.* The term `i` of `H_w` has degree at most
`sum_{j>i} deg g_{r_j} + deg h_{r_i} + E_{i-1}`. Here `sum_{j>i} deg g_{r_j} = (S_n - S_i) +
(L - E_i)`, `E_{i-1} = E_i - e_{r_i}`, and `deg h_r - e_r <= max(deg g_r - 1, deg c_r)` because
`deg r <= e_r - 1`. ∎

**Corollary T1 (cycle inequality; PROVED).** If `f != 0` is periodic with period `n`, word `w`
and `deg f = D`, then

    deg(t^L - G_w) <= L + kappa + R - D.

*Proof.* `f = (G_w f + H_w)/t^L` gives `(t^L - G_w) f = H_w`; take degrees. ∎

This is the exact analogue of the classical integer cycle inequality: a 3x+1 cycle through `n`
of length `L` with `a` odd steps has `|2^L - 3^a| <= C L 2^L / n`. In `Z` Baker's theorem
gives `|2^L - 3^a| >= 2^L L^{-C}`, which forces `n <= L^{C+1}`. In `F_q[t]` nothing forbids
`deg(t^L - G_w)` from being far below `L`, and Frobenius makes it happen.

**Corollary T2 (Frobenius sawtooth; PROVED).** Suppose exactly one branch `b_1` has a
non-constant multiplier `g_1`. Let `g_1^*(s) = s^{deg g_1} g_1(1/s)` and `u = g_1^*/g_1^*(0) =
1 + a s^nu + O(s^{nu+1})` with `a != 0`. If a cycle point has degree `D` and
`D' = D - kappa - R >= 1`, then the number `n_1` of uses of `b_1` in one period satisfies

    nu * p^{v_p(n_1)} >= D'.

*Proof.* By T1 `deg(t^L - G_w) <= L - D' < L`, so `G_w` is monic of degree `L` and its next
`D' - 1` coefficients vanish: `G_w^*(s) = 1 + O(s^{D'})`. Since the other multipliers are
constants, `G_w^* = u^{n_1}` after normalising the constant to 1. Write `n_1 = p^j m`, `p` not
dividing `m`. In characteristic `p`, `u^{p^j} = 1 + a^{p^j} s^{nu p^j} + O(s^{(nu+1) p^j})`,
so `u^{n_1} = 1 + m a^{p^j} s^{nu p^j} + ...` with `m a^{p^j} != 0`. Hence
`ord_s(u^{n_1} - 1) = nu p^j >= D'`. ∎

So a cycle at degree `D` must use the expanding branch a multiple of `p^k` times with
`nu p^k >= D - kappa - R`. `check_topdigits.py` verifies Lemma T, T1 and, where it applies, T2
on every cycle found in small degree.

*Revision after REFEREE1 (the data interpretation is EVIDENCE, not a consequence of T2).*
Earlier text said that the cycle-count "sawtooth" (collapse at `D = 10` for `p = 3`, at `D = 17`
for `p = 2`) is explained by T2. That claim is withdrawn. The data are consistent with T2, but
T2 does not by itself explain them. Example: G3 has `nu = 1`, `kappa = 1` and `R = 0` at a cycle
minimum. There T2 allows `9 | n_1` at `D = 10` and requires `27 | n_1` only from `D = 11` on.
The data (`data/cyc/G3.txt`) nevertheless show 0 cycles at `D = 10` and 5 at `D = 11`. The
collapse sits in the boundary case `D' = nu p^k`, where equality would also need
`deg H_w = L + kappa` exactly. Why that boundary case is empty is not explained. EVIDENCE.

## 3. Theorem F: Frobenius cycles (PROVED)

Call `L` a **Frobenius length** for a word `w` if `G_w = t^L + c_w` with `c_w in F_q^*`. Let
`W_L` be the set of words of digit length `L` with this property. Such words have total slope
`S_n = 0`.

**Theorem F.** For `w in W_L`, `x_w := -c_w^{-1} H_w` is a polynomial with `x_w in C_w` and
`T^n x_w = x_w`. The points `x_w` (`w in W_L`) are pairwise distinct. If all prefix slopes of
`w` are `>= 0`, then `deg x_w <= L + kappa`. Every cycle through some `x_w` contains such a
point. Hence

    #{f != 0 : deg f <= L + kappa, sigma(f) = infinity}  >=  |W_L| / L - 1.

*Proof.* `G_w x_w + H_w = (t^L + c_w) x_w - c_w x_w = t^L x_w`, which is `0 mod t^L`, so
`x_w in C_w` (Fact 1), and `T^n x_w = t^L x_w / t^L = x_w`. Distinctness follows from the
disjointness of the cylinders. If all prefix slopes are `>= 0`, then `R = 0` in Lemma T, so
`deg x_w = deg H_w <= L + kappa`. A cyclic rotation `w'` of `w` has the same multiset of
branches, so `w' in W_L`. If the rotation starts right after a step where `S_i` is minimal,
all its prefix slopes are `>= 0`, and `x_{w'} = T^i(x_w)` lies on the same cycle. A cycle of
period dividing `n <= L` contains at most `L` of the points `x_w`, so there are at least
`|W_L|/L` distinct cycles. The point of least degree on a cycle never drops below its own
degree, so `sigma = infinity` there. Cycles are disjoint, and at most one of them is `{0}`. ∎

**Binomial systems.** Suppose every zero-slope word of digit length `L_k` lies in `W_{L_k}` for
an infinite sequence `L_k`. This happens when the non-constant multipliers are powers of one
binomial, as follows from `(t^m + c)^{p^k} = t^{m p^k} + c^{p^k}`. We call such systems
*binomial*. The three studied here are:

| system | field | branches (digit -> T) | slopes | Frobenius lengths | `W_L` |
|---|---|---|---|---|---|
| A3 | F_3 | 0: f/t; 1: (1+t^2)(f-1)/t; 2: (f-2)/t + 1 | -1, +1, -1 | `L = 2·3^k` | all zero-slope words: `C(L, L/2) 2^{L/2}` |
| Q4b | F_4 | 0: f/t; 1: (1+t^3)(f-1)/t; w: (f-w)/t + 1; w^2: (f-w^2)/t | -1, +2, -1, -1 | `L = 3·2^k` | all zero-slope words: `C(L, L/3) 3^{2L/3}` |
| S2c | F_2 | `0`: f/t; `10`: (1+t)^3(f-1)/t^2 + 1; `11`: (1+t)(f-1-t)/t^2 + 1 | -1, +1, -1 | `L = 2^k` | all zero-slope words of digit length `L` |

(For S2c: with `a` uses of `10` and `b` of `11`, `G_w = (1+t)^{3a+b}` and the digit length is
`n_0 + 2a + 2b = 3a + b` when the slope is zero, so `G_w = (1+t)^L = 1 + t^L` for `L = 2^k`.)

**Theorem A (E_F and M_F are false for A3; PROVED).** Let `L = 2·3^k`, `X = 3^{L+2}` and
`h = log_3(2 sqrt 2) = 0.94639...`. Then for every `b >= 0` (including `b = infinity`)

    N(X, b) >= (2 sqrt 2)^L / (L (L+1)) - 1  >=  X^h / (9 (log_3 X)^2) - 1,
    X P(b)  <=  X · 3^{-(1-h) b}.

Hence for every `K > 1` and `b = K log_3 X`, `N(X, b) / (X P(b)) >= X^{(K-1)(1-h)} / (9 (log_3
X)^2) - o(1) -> infinity`, and `N(X, b)` exceeds `X^{eps(X)}` for every `eps(X) -> 0`.
Conjecture E_F fails for every `K > 1` (asymptotically; with these explicit constants the lower
bound overtakes `X P(2 log_3 X)` from `L = 486` on, `check_theoremA.py`; the enumeration shows the
excess already at `D = 10`). Inside the horizon it holds: exactly per octave (horizon lemma), and
for the cumulative count for `b <= log_3 X - omega(X)`, `omega -> infinity` (Proposition H').
M_F fails: `sigma(f) = infinity` for polynomials of unbounded degree. (Revision after REFEREE1:
the earlier wording "holds exactly for `b` up to the horizon" was correct only per octave.)

*Proof.* A3 is one-digit, so `kappa = max(2 - 1, 0) = 1`. `|W_L| = C(2N, N) 2^N` with
`N = 3^k`, and `C(2N, N) >= 4^N/(2N + 1)`, so `|W_L| >= 8^N/(L + 1) = (2 sqrt 2)^L/(L + 1)`.
Theorem F gives the first bound, since `N(X, b) >= N(X, infinity)`. For `P(b)`: survival
forces `S_b >= 0`. The steps are i.i.d. `+1` with probability `1/3` and `-1` with probability
`2/3`. For `lambda >= 1`, `P(S_b >= 0) <= E[lambda^{S_b}] = (lambda/3 + 2/(3 lambda))^b`, and
`lambda = sqrt 2` gives `(2 sqrt 2/3)^b = 3^{-(1-h) b}`. ∎

**Theorem A' (Q4b; PROVED, same proof).** `L = 3·2^k`, `X = 4^{L+3}` (`kappa = 2`),
`|W_L| = C(L, L/3) 3^{2L/3} >= (27/4)^{L/3} 9^{L/3}/(L+1)`, that is `4^{hL}/(L+1)` with
`4^h = 60.75^{1/3}` (`h = 0.98747`). The Chernoff bound with `lambda^3 = 3/2` gives
`P(b) <= (3 (3/2)^{2/3}/4)^b = 4^{-(1-h) b}`. These two rates are the same number,
`3(3/2)^{2/3}/4 · 4 = 60.75^{1/3}`, so E_F fails for every `K > 1`.

(`analyse.py` prints a slightly lower empirical decay rate of `P(b)` for Q4b at `b = 400`; the
polynomial factor `b^{-3/2}` is still visible there. The exact Chernoff value above is the
asymptotic rate.)

**S2c. Revision after REFEREE1.** The earlier text here contained two errors, and both are
WITHDRAWN. (1) "The Haar rate is `h = 0.8703`" was wrong. 0.8703 is the finite-`b` estimate
`(P(400)/P(360))^{1/40}`, which is biased by the factor `b^{-3/2}`. The true rate is
`h = 0.875848`, so `C* = 1/(1-h) = 8.055` (not 7.70). The same correction applies to S2, which has
the same step law. The obs/exp tables used the exact `P(b)` and are unaffected. (2) "At
`L = 2048` E_F already fails for every `K >= 1.05`" was a non sequitur. E_F is asymptotic, and
one value of `X` cannot falsify it. As a numerical statement about that single `X`, the proved
bounds below give `N > X P(K log_2 X)` for `K > 1.083`. That is only an illustration. The
method of types, previously only quoted, is replaced by the following elementary proof.

**Theorem A'' (E_F and M_F are false for S2c; PROVED).** Let `lambda* = 1.683772...` be the root
`> 1` of `2 lambda = (lambda^2 - 1)^2`. Put `rho* = (lambda*^2 - 1)/2 = 0.917543...` and
`h = 1 + log_2 rho* = 0.875848...`. Then:

(a) `P(b) <= rho*^{b-1}` for all `b >= 1`;

(b) for `L = 2^k >= 256` and `X = 2^{L+3}`: `N(X, infinity) >= 2^{hL - 4} / (L (L+1)^2) - 1`;

(c) hence, for every `K > 1` and `b = K log_2 X`, `N(X, b) / (X P(b)) >= 2^{(1-h)(K-1) L - O(log L)}`,
which tends to infinity along `X = 2^{2^k + 3}`. So E_F fails for every `K > 1`, and M_F fails.

*Proof.* Write `F(lambda, rho) = E[lambda^{s} rho^{-e}] = (1/2) lambda^{-1} rho^{-1} +
(1/4) lambda rho^{-2} + (1/4) lambda^{-1} rho^{-2}` for the S2c step law (`0`: `s = -1, e = 1`, prob
1/2; `10`: `+1, 2`, prob 1/4; `11`: `-1, 2`, prob 1/4). Then `4 lambda rho^2 F = 2 rho + lambda^2 + 1`.
At `(lambda*, rho*)`: `2 rho* + lambda*^2 + 1 = 2 lambda*^2` and
`4 lambda* rho*^2 = lambda* (lambda*^2 - 1)^2 = 2 lambda*^2`, so `F = 1` exactly. Also
`4 lambda^2 rho^2 d F/d lambda = lambda^2 - 1 - 2 rho`, which vanishes at `(lambda*, rho*)`.

(a) `M_k = lambda*^{S_k} rho*^{-E_k}` is a product of i.i.d. factors of mean `F = 1`, hence a
positive martingale. Let `tau` be the first step with `E_tau >= b - 1`. Then `tau <= b` and
`b - 1 <= E_tau <= b`, so `E M_tau = 1` by optional stopping. On the survival event for `b`,
`S_tau >= 0` (because `E_tau <= b`), so `M_tau >= rho*^{-E_tau} >= rho*^{-(b-1)}`, using
`lambda* > 1` and `rho* < 1`. Markov's inequality gives `P(b) <= rho*^{b-1}`.

(b) *Counting.* A word with `n_0` uses of `0`, `a` of `10` and `beta` of `11` has slope
`a - n_0 - beta` and digit length `n_0 + 2a + 2beta`. With slope 0 this means `n_0 = a - beta`
and `L = 3a + beta`. The number of such words is `(2a)!/((a-beta)! a! beta!) = C(2a, a) C(a, beta)`,
so `Z_L = sum_{3a + beta = L, 0 <= beta <= a} C(2a, a) C(a, beta)`. For each of them
`G_w = (1+t)^{3a} (1+t)^{beta} = (1+t)^L = 1 + t^L` when `L = 2^k`. So `W_L` contains all
zero-slope words, and Theorem F (`kappa = 2`) gives `N(2^{L+3}, infinity) >= Z_L/L - 1`.
*Elementary bounds.* `C(n, k) >= 2^{n H(k/n)}/(n+1)`, where `H` is the binary entropy. (The
term `k` is the largest term of the binomial expansion of `(k/n + (n-k)/n)^n = 1`, and there are
`n + 1` terms.) In particular `C(2a, a) >= 4^a/(2a+1)`. Hence
`log_2 Z_L >= g(beta) - log_2((2a+1)(a+1))` for every admissible `beta`, where
`g(beta) = 2a + a H(beta/a)` and `a = (L - beta)/3` is regarded as a real function of `beta`.
*The type.* Let `pi_0 = 1/(2 lambda* rho*)`, `pi_10 = lambda*/(4 rho*^2)` and
`pi_11 = 1/(4 lambda* rho*^2)` (the tilted law). These sum to `F = 1`, and
`-pi_0 + pi_10 - pi_11 = lambda* dF/dlambda = 0`. So `pi_10 = 1/2`. Put
`theta* = pi_11/pi_10 = 0.352723...`, so `pi = ((1-theta*)/2, 1/2, theta*/2)`. Since
`-log_2 pi_r = e_r - s_r log_2 lambda* + e_r log_2 rho*`, we get
`H(pi) = E_pi[e] (1 + log_2 rho*) - E_pi[s] log_2 lambda* = E_pi[e] h`. Directly,
`H(pi) = 1 + H(theta*)/2` and `E_pi[e] = (3 + theta*)/2`. Therefore
`phi(theta*) := (2 + H(theta*))/(3 + theta*) = h`.
*Approximation.* Let `beta* = theta* L/(3 + theta*)`. Then `a* = (L - beta*)/3 = L/(3 + theta*)`,
`beta*/a* = theta*` and `g(beta*) = L phi(theta*) = hL`. Choose the integer `beta ≡ L (mod 3)`
nearest to `beta*`, so `|beta - beta*| <= 3/2`. We have `dg/dbeta = log_2((1-theta)/theta) -
(2 - log_2(1-theta))/3` with `theta = beta/a`. This is decreasing in `theta` and lies in
`[-0.33, 0.39]` for `theta in [0.3, 0.4]`. For `L >= 256` the whole segment `|beta - beta*| <= 2`
has `theta in [0.3, 0.4]`: at `L = 256` the endpoints are 0.324 and 0.382, and they move
monotonically toward `theta*` as `L` grows. So `g(beta) >= hL - 3/2·0.39 >= hL - 4`. With
`(2a+1)(a+1) <= (L+1)^2` this gives `Z_L >= 2^{hL-4}/(L+1)^2`, and (b) follows.

(c) `X P(b) <= 2^{L+3} rho*^{b-1} = 2^{L + 3 - (1-h)(b-1)}`, and
`N(X, b) >= N(X, infinity) >= 2^{hL - 4}/(L(L+1)^2) - 1`. With `b = K(L+3)` the exponent of the
ratio is `(h - 1)L + (1-h)K(L+3) - O(log L) = (1-h)(K-1)L + O(log L)`. Also
`N(X, infinity) >= X^{h - o(1)}`, which exceeds `X^{eps(X)}` for every `eps -> 0`. ∎

`check_s2c.py` checks the algebra to 50 digits, the tilt identity, `P(b) <= rho*^{b-1}` for
`b <= 400` (the maximal ratio is 0.5), the formula for `Z_L` against brute force (`L <= 16`), the
binomial bound exactly (`n <= 300`), the `theta`-segment and the bound in (b) for
`L = 2^8, ..., 2^22`, and the Lipschitz constant.

**Corrected law for binomial systems (PROVED for A3, Q4b, S2c; revised after REFEREE1).**
For every `X = q^{D+1}` with `D >= D_0` and every `b >= D + 1 - e_max`,

    N(X, b)  <=  C X^h,

and along `X = q^{L+kappa+1}` (`L` a Frobenius length as in Theorems A, A', A''), for all `b`,
`N(X, b) >= X^h/poly(log X)`. So survivors stop thinning at the horizon: up to polynomial
factors and along `X = q^{L+kappa+1}`, the number of polynomials surviving their own digits and
the number surviving forever agree. (This is a statement about counts only, not about individual
polynomials.)

*Proof of the upper bound.* (The earlier proof applied the horizon lemma to all octaves at once.
That is invalid for the low octaves. Here it is done octave by octave, as the referee suggested.)
For `D_0 <= D' <= D` we have `b >= D' + 1 - e`. The horizon lemma at `m' = D' + 1 - e` gives
`N_{D'}(b) <= (q-1) q^{D'} P(D' + 1 - e)`. For A3 and Q4b (`e = 1`), `P(m) <= q^{-(1-h)m}`
(Theorems A, A'), so the term is at most `(q-1) q^{hD'}`. For S2c (`e = 2`), `P(D' - 1) <= rho*^{D'-2}`
(Theorem A''(a)), so the term is at most `4 · 2^{hD'}`. Summing the geometric series over `D'`
gives `O(q^{hD}) = O(X^h)`, and the octaves `D' < D_0` add `O(1)`. The lower bound is Theorems
A, A', A''. ∎

*Scope.* For a general binomial system the same proof needs two inputs that are proved here only
for these three systems: an exponential Chernoff bound `P(b) <= C q^{-(1-h)b}` (true for any
finite step law by the same martingale, once `h` is defined as the saddle value), and
`|W_{L_k}| >= q^{h L_k - o(L_k)}`. The second is the same large-deviation (type) count as in
Theorem A''(b), and it also needs every zero-slope word of length `L_k` to be Frobenius. It is
not claimed in general.

## 4. Generic (non-binomial) systems: EVIDENCE and HEURISTIC

For B3 (`g_1 = 1+t+t^2 = (1-t)^2` over F_3), G3 (`g_1 = 1 + t + 2t^2`), S2 (`10 -> 1+t+t^3`) and
Q4 (`g_1 = 1 + t + w t^3`) no word has `G_w = t^L + c`. (B3: `(t+2)^{2a} = t^{2a} + c` would
need `2a` to be a power of 3.) Still:

* the count law holds within noise for `b <= 2D` (G3, S2: chi2/cell 0.7 to 2.3; Q4 up to
  `1.5D`) and then breaks: obs/exp is 1.01 to 1.11 at `3 to 4 D`, 1.7 to 3.0 at `4 to 6 D`, and 17
  at `6 to 10 D` (G3). B3 deviates from `1.5D`, Q4 shows a *deficit* (0.83 to 0.95) at
  `2 to 6 D`;
* every system has never-dropping polynomials whose number grows with `D`, consistent with
  Corollary T2 (a sawtooth). G3 has `0, 5, 15, 33, 62, 251, 784` distinct cycles with minimum at
  degree `D = 10..16`. Q4 has 3867 at `D = 12`. S2 has few (1 to 8 per degree; periods 4, 8,
  16, 32 steps, always powers of 2);
* every system except S2 has orbits that pass degree 4000 without repeating ("unresolved"),
  starting from sparse polynomials such as `1 + t^10` (B3). These are candidates for divergent
  orbits **despite negative drift**. No certificate was found: a line-renormalization search
  for A3 covered 12,446 of 927,866 candidate directions without success (`scratch/`). OPEN.

**HEURISTIC (corrected law, generic case).** If every count `n_r` is divisible by `p^k`, then
`G_w = Gamma(t)^{p^k}` and `t^L - G_w = Delta(t)^{p^k}`. Here `Delta` is a fixed polynomial of
degree `delta <= M - 1`, where `M = L/p^k`, and `Delta` is independent of `k` once the leading
coefficients multiply to 1. If `H_w` behaves randomly modulo `Delta^{p^k}`, the expected number
of polynomial periodic points is `q^{hL - delta p^k} = q^{p^k (hM - delta)}`. This is positive
whenever `delta < hM`, and in particular when `M < 1/(1-h) = C*`, the same critical constant
as in the integer heuristic. So generic function-field systems should also violate E_F, with
`N(X, infinity) = X^{c + o(1)}` along subsequences and `c` up to roughly `1/M_min - (1-h)`.
This is CONJECTURE. It is consistent with the data but not tested quantitatively.

## 5. The integer comparison (revised after REFEREE1)

* **Integer version of Theorem F (PROVED, `check_integer_catalan.py`).** For the accelerated
  map `x -> x/2` (`x` even), `(3x + d)/2` (`x` odd), a parity word of length `L` with `a` odd
  steps has the periodic point `x_w = d H_w/(2^L - 3^a)`. This is an integer for every word
  when `2^L - 3^a = ±1`. *Lemma.* With `L >= 1` and `a >= 0`, `2^L - 3^a = ±1` exactly for
  `(L, a) = (1, 0), (1, 1), (2, 1), (3, 2)`. *Proof (elementary; the earlier appeal to Mihailescu
  is unnecessary and is dropped).* Case `2^L - 3^a = 1`. If `a = 0` then `L = 1`. If `a >= 1`
  then `2^L ≡ 1 (mod 3)`, so `L = 2m` and `(2^m - 1)(2^m + 1) = 3^a`. Two powers of 3 that
  differ by 2 are 1 and 3, so `m = 1`, `(L, a) = (2, 1)`. Case `3^a - 2^L = 1`. If `L = 1` then
  `a = 1`. If `L >= 2` then `3^a ≡ 1 (mod 4)`, so `a = 2m` and `(3^m - 1)(3^m + 1) = 2^L`. Two
  powers of 2 that differ by 2 are 2 and 4, so `m = 1`, `(L, a) = (3, 2)`. ∎ These words give
  exactly the 3x+1 cycles `{0}` (from `(1, 0)`, omitted in the first version), `{-1}`, `{1, 2}`
  and `{-5, -7, -10}`, and their `d`-multiples for 3x+d.
* **WITHDRAWN: "this is the finite set of exceptions that Generalisation G allows".** That was
  wrong. G's exceptions include cycles whose denominator `2^L - 3^a` is not a unit. Examples:
  the 3x+1 cycle through -17 (`L = 11`, `a = 7`, `2^L - 3^a = -139`), and the 3x+5 cycles with
  minima 187 and 347 (`L = 27`, `a = 17`, `2^L - 3^a = 5077565`), which round 4 lists. The correct
  statement is that the unit-denominator (Frobenius-type) cycles of `Z` form a finite subset of
  G's exceptions (checked in `check_integer_catalan.py`).
* **What is provable in `Z` about this mechanism.** Exact returns (`|2^L - 3^a| = 1`) give only
  the cycles above. Near returns are limited by a Baker-type bound,
  `|L log 2 - a log 3| >= L^{-C}` for `L >= 2` with an absolute `C` (quoted from memory, e.g.
  Rhin's explicit exponent, about 13.3; not re-checked here). It gives `|2^L - 3^a| >= 2^L L^{-C'}`.
  Combined with the cycle inequality `|2^L - 3^a| <= C'' L 2^L / n` for a positive cycle with minimum `n`,
  this forces `L >= c n^{1/(C'+1)}`. So `Z` has no positive cycles of length `O(log n)` with minimum `n`,
  unlike the cycles of length `L ≈ D` of A3. This does NOT show that `Z` has few cycles, and it
  does NOT exclude other mechanisms that might break E. The first version's sentence "the cycle
  obstruction that kills E_F is provably absent in `Z`" is replaced by this precise statement.
* **Why E_F breaks (as analysed here).** The cause is not the absence of carries in the low
  digits. For generic polynomial systems the count law survives to about twice the horizon
  (EVIDENCE). The cause is Lemma T. Without carries the top digits evolve by multiplication by
  `G_w^*` in the pro-`p` group `1 + s F_q[[s]]`, and that group has Frobenius near-returns:
  `ord(u^{p^k} - 1) = nu p^k`. In `Z` the top digits evolve by the real number `3^a/2^L`, and
  carries couple them to the low digits.
* **REMARK (HEURISTIC, not a theorem; relabelled after REFEREE1, which correctly objected to
  "PROVED in the sense stated").** One would like to say: any argument for E that uses only
  (i) the cylinder/Terras structure, (ii) the affine form `(G_w x + H_w)/p^L` with `G_w`
  depending only on the branch counts, (iii) finite digit expansions with an exact size walk,
  and (iv) the i.i.d. Haar law of branches would also apply to A3, where E fails. This is not
  formalised. Moreover ingredient (iii) is false for the integer systems: the size walk in `Z`
  is only approximate, because of carries. So such an argument would not apply to `Z` at all,
  and the remark is not even internally coherent as a formal statement. It is offered only as
  motivation. The near-returns that break E_F live at the infinite place of `F_q(t)`, which is
  non-archimedean. This suggests that a proof of E for integers would have to use some
  archimedean property of the multipliers (a Baker-type lower bound for `|2^L - u^a|`, or the
  equidistribution of `a log_2 u mod 1`), together with carries that carry it down to the
  middle digits. No claim is made that such an input is necessary.

## 6. Literature and novelty (added after REFEREE1)

Function-field analogues of the 3x+1 map are classical (quoted from memory, not re-checked:
Hicks, Mullen, Yucas and Zavislak, Amer. Math. Monthly 2008, over `F_2[t]`, where every orbit
reaches 1; Matthews and Leigh, J. Number Theory 1987). The identity
`(t^m + c)^{p^k} = t^{m p^k} + c^{p^k}` and the resulting periodic points (Theorem F) are
standard and very likely folklore. The content new to this census is the use of Theorem F,
together with the counts of Theorems A, A' and A'', against the count law E_F beyond the
horizon, and the exact in-horizon statements (horizon lemma, Proposition H'). No literature
search was performed. The referee's control case, the Hicks et al. map, is binomial but has
no free re-entry with an expanding branch, and Theorem F yields only the fixed point 1 there.
That is consistent with the requirement of exponentially many zero-slope words.
