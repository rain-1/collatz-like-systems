# 9n+1: no cycle with at most 13 rising runs (so no circuit)

Targets: CLS-037 (GLOBAL) and CLS-036 (fate of 5) for the map `n even -> n/2, n odd -> 9n+1`.

Status: **PROVED**, with one literature constant (Laurent 2008, Corollary 2). I consulted that constant
in the original paper (see Section 5). Computation is used only after a proved reduction to a finite range.

## 1. Statement

Let `S(n) = (9n+1)/2` for odd `n` and `S(n) = n/2` for even `n`. This is the shortcut map: it merges each
odd step of the catalog map with the halving that must follow it. Positive cycles of the catalog map
correspond one to one with positive cycles of `S`: delete or reinsert the values `9x+1`. In a cycle of `S`,
a *rising run* is a maximal block of consecutive odd elements. Its first element is a *valley*. The valleys
are exactly the strict local minima of the cycle:
- An odd element preceded by an even one is below both neighbours.
- An odd element preceded by an odd one lies above its predecessor.
- An even element lies above its successor.

A run ends at the odd `x` with `S(x)` even, that is `4 | 9x+1`, that is `x ≡ 3 (mod 4)`.

**Theorem.** Every positive cycle of the 9n+1 map has at least **14** rising runs. Equivalently:
- it has at least 14 strict local minima under `S`;
- at least 14 of its odd terms are `≡ 3 (mod 4)`.

In particular, 9n+1 has **no circuit** (a cycle with exactly one local minimum), of any length.

Corollary (CLS-036/037). The orbit of 1 (and of 5) either is unbounded or ends in a cycle with at least
14 rising runs. Combined with the earlier census result, that cycle also has more than 1000 odd terms.

Relation to prior work in this repo: `census/lhf/seven-nine/CLS-037.md` proved the case of at most 7
runs, using Matveev's bound and a scan of odd minima below 762148. This note:
- replaces Matveev by Laurent's two-logarithm bound;
- uses the exact best-approximation bound `|kα−K| ≥ |q_nα−p_n|` for `k < q_{n+1}`, instead of `1/(2q)`;
- extends the result to 13 runs.

For `r ≤ 7`, the same pipeline gives the minimum bound 91495.

## 2. Notation and the two basic inequalities

Fix a positive cycle with `r` runs. Let its valleys be `x_0, …, x_{r−1}`, with `x_0 = m` the cycle minimum.
The minimum is odd, since an even value is followed by a smaller one, and it is preceded by an even value,
so it is a valley. Let:
- `a_i` be the number of odd elements in run `i`;
- `y_i` be its (even) peak;
- `d_i ≥ 1` be the number of halvings from `y_i` to the next valley.

Put `k = Σ a_i` (the number of odd terms) and `K = Σ (a_i + d_i)` (the number of halvings of the catalog map).
Put `α = log_2 9`.

**Run identity.** For odd `x`, `7S(x)+1 = (9/2)(7x+1)`. So `S^j(x) + 1/7 = (9/2)^j (x + 1/7)`, and `S^j(x)`
is odd iff `2^{j+1} | 7x+1`. Hence:
- `a_i = v_2(7x_i+1)`;
- `7y_i + 1 = (9/2)^{a_i}(7x_i+1)`;
- `y_i = 2^{d_i} x_{i+1}`.

In particular, for a circuit (`r = 1`) we get `m = (9^k − 2^k)/(7(2^K − 9^k))`.

**(A) Upper bound for the linear form.** Each odd step multiplies by `9 + 1/x`, each halving by `1/2`, and
the cycle closes. So `2^K = Π_{x odd in cycle} (9 + 1/x)`. Therefore
`δ := K log 2 − k log 9 = Σ log(1 + 1/(9x)) > 0`.

Inside run `i` the odd elements are `S^j(x_i)` for `0 ≤ j < a_i`, and `S^j(x_i) ≥ (9/2)^j x_i`. So run `i`
contributes less than `(1/(9x_i)) Σ_j (2/9)^j < 1/(7x_i)`. Since `x_i ≥ m`,

  `0 < δ < Σ_i 1/(7x_i) ≤ r/(7m)`.   (A)

Also `2^K ≤ 10^k`, so `K ≤ k log_2 10`.

**(B) Number of odd steps versus the minimum.** Put `h_i = log_2(7x_i+1)`. Then:
- `a_i = v_2(7x_i+1) ≤ h_i`;
- `h_{i+1} ≤ log_2(7y_i+1) = h_i + (α−1)a_i ≤ α h_i`.

So `h_i ≤ α^i h_0` and

  `k ≤ h_0 (α^r − 1)/(α − 1) =: C_r log_2(7m+1)`.   (B)

The constant `C_r` increases with `r`.

## 3. Step 1: a bound for k from linear forms in two logarithms

**Laurent (2008), Corollary 2** is stated with all hypotheses in Section 5. Apply it with:
- `α_1 = 3`, `b_1 = 2k`, `α_2 = 2`, `b_2 = K`, so `Λ = b_2 log α_2 − b_1 log α_1 = δ`;
- `D = 1`;
- `log A_1 = log 3` and `log A_2 = 1`. These satisfy `log A_i ≥ max{h(α_i), |log α_i|, 1}`, since `h(3) = log 3` and `h(2) = log 2`.

The hypotheses hold:
- 2 and 3 are real, positive, at least 1, with positive logarithms;
- they are multiplicatively independent;
- `b_1, b_2 ≥ 1`;
- `Λ ≠ 0` because `2^K ≠ 9^k`.

Then `b' = 2k + K/log 3 ≤ (2 + log 10/(log 2 log 3)) k < 5.03k`. With `(m, C_2) = (10, 25.2)`:

  `log δ ≥ −25.2 (max{log b' + 0.38, 10, 1})^2 log 3`.

Combining this with (A) for `r ≤ R`, and using `log_2(7m+1) ≤ 3 + log m / log 2`, (B) gives `k ≤ f(k)`, where

  `f(k) = C_R (3 + (log(R/7) + 25.2 log 3 · L(k)^2)/log 2)` and `L(k) = log(5.03k) + 0.38`.

This holds for `k ≥ K_0 := 2·10^12`, where `L(k) ≥ 10`.

For `L > 2`, the function `f(k)/k` decreases, because `d/dk[(A + B L^2)/k]` has the sign of `2BL − A − BL^2 < 0`.
The checker verifies `f(K_0) < K_0` exactly (for `R = 13`, `f(K_0) ≈ 5.7·10^10`). Hence **`k < 2·10^12`**.

## 4. Step 2: continued-fraction reduction, and Step 3: the exhaustive scan

**Lemma (best approximation).** Let `p_n/q_n` be the convergents of `α`, and suppose `0 < k < q_{n+1}`. Then
`|kα − K| ≥ |q_nα − p_n|` for every integer `K`.

*Proof.* Since `p_{n+1}q_n − p_nq_{n+1} = ±1`, we can write `(k, K) = u(q_n, p_n) + v(q_{n+1}, p_{n+1})` with
`u, v ∈ Z`.
- If `v = 0`, then `u = k/q_n ≥ 1`.
- If `v ≥ 1`, then `uq_n = k − vq_{n+1} < 0`.
- If `v ≤ −1`, then `uq_n > 0`.

So `u ≠ 0`, and `u, v` are never of the same strict sign. Since `q_nα − p_n` and `q_{n+1}α − p_{n+1}` have
opposite signs, the two terms of `kα − K = u(q_nα − p_n) + v(q_{n+1}α − p_{n+1})` have the same sign. Hence
`|kα − K| ≥ |u||q_nα − p_n| ≥ |q_nα − p_n|`. ∎

**The reduction loop.** Given a bound `k ≤ k_max`, take the least `n` with `q_{n+1} > k_max`. Then
`δ = log 2 · (K − kα) ≥ log 2 · |q_nα − p_n|`, and (A) gives `m < R/(7 log 2 |q_nα − p_n|)`. Next, (B) gives a
new `k_max = C_R · bitlength(7M+1)`. The loop is iterated while it improves.

The partial quotients of `α` come from a rational enclosure `[α_lo, α_hi]` of width below `10^{−60}`. Only
quotients shared by both endpoints are kept, so they are the true quotients. Every `|q_nα − p_n|` is bounded
below from the enclosure, after checking that its sign is certain.

For `R = 13` the loop runs as follows:
- `k < 2·10^12` gives `m < 7.8·10^12`;
- then `k ≤ 69175102` (using `q_{n+1} = 112822303`) gives `m < 352947866`;
- then `k ≤ 48121810` (using `q_n = 5390637` and `q_{n+1} = 53715833`) gives **`m < 152137747`**;
- the loop is then stable.

**Scan.** For every odd `m < 152137747`, the checker follows at most 13 runs from `m`, in closed form:
`x ↦ oddpart((9^a (7x+1)/2^a − 1)/7)` with `a = v_2(7x+1)`. It stops as soon as a valley is at most `m`. A
valley equal to `m` would be a cycle with at most 13 runs and minimum `m`. A valley below `m` shows that `m`
is not the minimum of any cycle through it.

Suppose a cycle with `r ≤ 13` runs and minimum `m` existed. Then `m < 152137747`. The valleys after `m` are
all above `m`, until the `r`-th one, which equals `m`. So the scan would report it. It reports nothing, and
the theorem follows. The closed-form run is cross-checked against step-by-step iteration of the catalog map
for all odd `x < 20001`.

## 5. Literature

Consulted:
- **Laurent's two-logarithm bound.** M. Laurent, *Linear forms in two logarithms and interpolation
  determinants II*, Acta Arith. 133 (2008), 325–348, **Corollary 2**, read from the IMPAN PDF.
  - Setting: `Λ = b_2 log α_2 − b_1 log α_1` with `b_1, b_2` positive integers and `|α_1|, |α_2| ≥ 1`.
  - Hypotheses: `α_1, α_2` multiplicatively independent; `α_1, α_2, log α_1, log α_2` real and positive.
  - Parameters: `D = [Q(α_1,α_2):Q]/[R(α_1,α_2):R]` and `b' = b_1/(D log A_2) + b_2/(D log A_1)`, where
    `A_i > 1` and `log A_i ≥ max{h(α_i), |log α_i|/D, 1/D}`.
  - Conclusion: `log|Λ| ≥ −C_2 D^4 (max{log b' + 0.38, m/D, 1})^2 log A_1 log A_2`, for each pair
    `(m, C_2(m))` in Table 1. That table includes `(10, 25.2)`, which is the pair used here.
  - Cross-check: the older Laurent–Mignotte–Nesterenko (1995) Corollaire 2, with
    `24.34 (max{log b' + 0.14, 21/D, 1/2})^2`, is quoted as Theorem 2.2 in Batte–Luca, arXiv:2412.12130. It
    would serve equally well, since only the order of magnitude of `K_0` matters.
- **Simons's method for generalized Syracuse maps.** J. L. Simons, *On the (non-)existence of m-cycles for
  generalized Syracuse sequences*, Acta Arith. 131 (2008), 217–254. Section 4 extends the Simons–de Weger
  m-cycle method to `px+q` with `p ≥ 5` prime. It uses the same ingredients:
  - an upper bound for `Λ` via `Σ 1/x_i`;
  - chaining of minima, of the form `x_{i+1} < b x_i^ρ`;
  - LMN Corollaire 2;
  - convergents (Lemma 9).

  It also assumes a computed lower bound `X_0 = 10^6` for the minima. As far as I could check, `p = 9` is not
  covered (it is not prime). The argument here is that method, specialized to `9x+1`. It is self-contained:
  the needed lower bound for minima comes from the scan.
- **Earlier circuit results.** Circuits for `3x+1` were excluded by Steiner (1977), and those for `3x+d` were
  studied by Belaga–Mignotte (1998). I did not consult those papers and do not rely on them.
- I found no published statement for 9n+1 itself. "No circuit for 9n+1" should be regarded as a routine
  instance of the method, not a new phenomenon.

## 6. Verification

`python3 census/advance/9n1-cycles/check.py` exits 0 and prints each step. The default `R = 13` takes about 70 s
on 12 cores.

The script:
1. Encloses `log 2`, `log 3` and `log(5/4)` by the atanh series with an explicit tail.
2. Computes the continued fraction of `α` exactly.
3. Checks `f(K_0) < K_0`.
4. Runs the reduction loop.
5. Scans all 76,068,873 odd candidates in parallel.

`python3 check.py R` runs the same certificate for other `R`. **`R = 14` was also run, and it passed.** The
log reads:
- LMN gives `k < 2·10^12`;
- with `q_n = 112822303` and `q_{n+1} = 397573379`, the bound is `m < 1188091035`;
- all 594,045,517 odd candidates were excluded through 14 runs;
- `PASS`, in 7m41s wall time on 12 cores under a load average of about 28.

So the theorem also holds with **15** in place of 14. This rests on that one longer run. The default check
certifies 14.

What is conditional: nothing beyond the correctness of the published constant in Laurent (2008), Corollary 2.

## Referee (round 1)

**Verdict: CONFIRMED.** The theorem holds as stated: every positive 9n+1 cycle has at least 14 rising runs, so there is no circuit. The 15-run version is also confirmed, by an independent run.

**Derivation re-checked by hand.**
- **Shortcut correspondence.** In the catalog map every odd term is followed by 9x+1, which is even. So deleting the 9x+1 values gives a bijection between positive cycles of the catalog map and positive cycles of S.
- **Valleys are exactly the strict S-local minima.** I checked the three neighbour cases.
- **Runs and residues mod 4.** A run ends at x ≡ 3 (mod 4), since S(x) is even iff 4 | 9x+1.
- **Definition of "local minimum".** Under the catalog map itself, every odd term is a local minimum, because it is preceded by 2x and followed by 9x+1. So a catalog-map "circuit" would have k = 1, which is trivially excluded. The S-based (Steiner) notion used here is the right one and is the stronger statement. No cases are silently excluded.
- **Run identity.** 7S(x)+1 = (9/2)(7x+1). Hence a_i = v_2(7x_i+1) ≥ 1 and 7y_i+1 = (9/2)^{a_i}(7x_i+1).
- **(A).** 2^K = Π(9+1/x) holds because the product of the ratios around the cycle is 1. Within a run, S^j(x) > (9/2)^j x. So run i contributes less than (1/(9x_i))·1/(1−2/9) = 1/(7x_i). Also K ≤ k log_2 10, since 9+1/x ≤ 10.
- **(B).** x_{i+1} ≤ y_i/2 < y_i, so h_{i+1} ≤ h_i + (α−1)a_i ≤ αh_i, and k = Σa_i ≤ Σh_i. This is correct.
- **Laurent step.** b' = 2k + K/log 3 ≤ (2 + log 10/(log 2 log 3))k ≈ 5.0237k. log_2(7m+1) ≤ 3 + log_2 m. The code bounds log(R/7) by R/7−1 when R ≥ 7, and by 0 when R < 7, so the constant A in f stays positive. Then d/dk[(A+BL²)/k] has the sign of BL(2−L) − A < 0 for L > 2, so f(k)/k is decreasing. f(K_0) is evaluated with an upper bound on L, and f is increasing in L, so the evaluation is safe.
- **Best-approximation lemma.** The proof is correct. When v ≠ 0, u has the opposite strict sign to v. θ_n and θ_{n+1} have opposite signs. The reduction m < R/(7 log 2 · |θ_n|) is applied with q_n ≤ k_max < q_{n+1}, and the last M printed comes from a valid k_max. So the loop's stopping rule is sound.
- **Scan logic.** In a cycle with r ≤ R runs and minimum m, the valleys x_1, …, x_{r−1} are distinct cycle elements other than m, so they are > m, and x_r = m. Stopping at the first valley ≤ m therefore never misses such a cycle. The prover's range is 1, 1000001, …, up to M_FINAL; all the start points are odd, so it covers every odd m < M_FINAL. I re-counted this: 76,068,873 = ⌊M/2⌋.

**Constant verified against the source.** I downloaded M. Laurent, *Linear forms in two logarithms and interpolation determinants II*, Acta Arith. 133 (2008) 325–348 (doi:10.4064/aa133-4-3) from impan.pl myself. Page 328, Corollary 2 reads: "Suppose moreover that the numbers α1, α2, log α1, log α2 are real and positive. Then log|Λ| ≥ −C2 D⁴ (max{log b' + 0.38, m/D, 1})² log A1 log A2 for each pair (m, C2(m)) from Table 1." The surrounding conditions are:
- "moreover" refers to Corollary 1's hypothesis that α1 and α2 are multiplicatively independent;
- Λ = b2 log α2 − b1 log α1, with b1 and b2 positive integers and |α_i| ≥ 1;
- D = [Q(α1,α2):Q]/[R(α1,α2):R];
- b' = b1/(D log A2) + b2/(D log A1), where A_i > 1 and log A_i ≥ max{h(α_i), |log α_i|/D, 1/D};
- Table 1 gives C2(10) = 25.2.

The prover's quotation is exact. The application also meets every condition:
- α1 = 3, α2 = 2, D = 1;
- log A1 = log 3 ≥ max{log 3, log 3, 1};
- log A2 = 1 ≥ max{log 2, log 2, 1};
- b1 = 2k ≥ 2 and b2 = K ≥ 1;
- Λ = δ ≠ 0.

I did not check the Simons (2008) coverage claim beyond its bibliographic data. Nothing in the proof depends on it.

**Independent computation.** The referee's code is in `referee/referee_check.py` and `referee/scan.c`. It does not reuse any code from check.py:
- logs come from `decimal` ln at 150 digits, widened by 10⁻¹⁴⁰;
- the continued fraction comes from interval endpoints (120 certified partial quotients);
- the scan is a C program that iterates the catalog map step by step;
- the 128-bit overflow cases are re-done in Python with big integers.

Results:
- **R = 13:** same chain as the prover, ending at m < 152137747. All 76,068,873 odd m are excluded; 705 of them overflowed and were re-done. PASS in 3 s. The prover's `check.py` also passed on re-run (exit 0, 53 s). My own smallest K_0 of the form c·10^e is 5·10^10, so 2·10^12 has a wide margin.
- **R = 14:** m < 1188091035, and all 594,045,517 odd m are excluded. PASS in 20 s. This confirms the prover's "15 runs" claim independently.
- **R = 15** (beyond the claim): m < 10122763217, and all 5,061,381,608 odd m are excluded. PASS in 3 m 13 s on 12 cores. So in fact **every positive 9n+1 cycle has at least 16 rising runs**. That is certified by the referee scan only, not by check.py. Run `python3 referee/referee_check.py 15` to reproduce it.

**Gap list.** There are no substantive gaps. Nits:
1. Section 6 says the default run takes about 70 s; the summary says 56 s. I measured 53 s. This is cosmetic.
2. Section 3 writes f with log(R/7) and calls the monotonicity argument complete. It needs A ≥ 0, which holds only because the code replaces log(R/7) by max(R/7−1, 0). The text should say this explicitly.
3. The step-by-step versus closed-form cross-check in check.py covers only odd x < 20001. The referee's step-by-step C scan over the full range now covers the closed form as well.
