# CLS-046 (perm_d): classification of the one-local-minimum cycles

**Map.** D(2q) = 5q, and D(8q+r) = 5q + (r+1)/2 for r = 1, 3, 5, 7. This is `perm_d_s3` in census/systems.py.
Equivalently:
- D(x) = 5x/2 for x even;
- D(x) = (5x + s)/8 for x odd, with s = 4 - (x mod 8), so s ∈ {3, 1, -1, -3}.

## Theorem

Let C be a cycle of D on the positive integers, read cyclically. Call x in C a *local minimum* if its predecessor and its successor in C are both larger than x.

1. {1} is a fixed point. It is the only cycle containing 1, and it has no local minimum.
2. Every other cycle has at least one local minimum. The number of local minima equals the number of maximal runs of even elements.
3. **The cycles with exactly one local minimum are exactly {2, 5, 3}, {6, 15, 9} and {26, 65, 41}.** Each has parity word E O O (k = 1, l = 2). Their minima are 2·e with e = 1, 3, 13.

Of the four short cycles found earlier, three are 1-cycles. The fourth, {1}, is the degenerate fixed point.

**Status: PROVED, with one caveat.** The proof uses the two-logarithm bound of Laurent, Mignotte and Nesterenko (Step 4). I read its statement in a secondary source that quotes it verbatim. I could not access the original paper. See *What is conditional* below.

## Proof

### Step 1: monotonicity and the shape of a cycle

- If x is even, D(x) = 5x/2 > x.
- If x is odd and x ≥ 3, D(x) ≤ (5x+3)/8 < x.
- D(1) = 1.

So no cycle other than {1} contains 1. Every other cycle contains both parities, because a cycle of a single parity would be strictly monotone.

A local minimum is exactly an element x_i with x_{i-1} odd and x_i even. Each maximal run of evens has exactly one such starting point, which gives parts 1 and 2. A cycle has exactly one local minimum exactly when its cyclic parity word is E^k O^l with k, l ≥ 1. Start the cycle at the minimum: x_0 is even, x_0, ..., x_{k-1} are even, and x_k, ..., x_{k+l-1} are odd. Then x_{k+l} = x_0.

### Step 2: the cycle equation (2-adic structure of the blocks)

**The rising block.** We have x_i = (5/2)^i x_0. Write x_0 = 2^a e with e odd. Then x_i = 5^i 2^{a-i} e. These are even for i < k and odd for i = k, so a = k. Hence

    x_0 = 2^k e (e odd),   x_k = 5^k e,   and min C = x_0 ≥ 2^k.

**The falling block.** We have x_{k+j+1} = (5 x_{k+j} + s_j)/8 with s_j ∈ {±1, ±3}. Induction gives

    8^l x_{k+l} = 5^l x_k + S,   S = Σ_{j<l} s_j 5^{l-1-j} 8^j,   |S| ≤ 3 (8^l - 5^l)/3 = 8^l - 5^l.

Substituting x_{k+l} = 2^k e and x_k = 5^k e gives

    e · Δ = S,   Δ := 2^{3l+k} - 5^{k+l} ≠ 0 (Δ is odd),   so   |Δ| ≤ e|Δ| ≤ 8^l - 5^l.   (★)

### Step 3: Λ is small, and l is tied to k

Put

    Λ := (k+l) log 5 - (3l+k) log 2 = k log(5/2) - l log(8/5).

- If Δ > 0, then by (★) 2^{3l+k} > 5^{k+l} > 2^{3l+k} - 8^l = 2^{3l+k}(1 - 2^{-k}). So 0 < -Λ < -log(1 - 2^{-k}) ≤ 2^{-k}/(1 - 2^{-k}) ≤ 2^{1-k}.
- If Δ < 0, then 0 < Λ < log(1 + 2^{-k}) < 2^{-k}.

In both cases

    |Λ| < 2^{1-k} ≤ 1.   (1)

From |k log(5/2) - l log(8/5)| < 1 we get

    |l - r k| < 1/log(8/5),   r = log(5/2)/log(8/5) = 1.94954...

In particular l < 1.949540 k + 2.127643.

### Step 4: the upper bound on k from a linear form in two logarithms

**Source.** Laurent, Mignotte and Nesterenko, *Formes linéaires en deux logarithmes et déterminants d'interpolation*, J. Number Theory 55 (1995), 285–321, Corollaire 2, p. 288.

The statement, as I consulted it (see *What is conditional*):
- Let α_1, α_2 be multiplicatively independent positive real algebraic numbers. Let d = [Q(α_1, α_2) : Q].
- Let B_1, B_2 be real numbers greater than 1 with log B_i ≥ max{h(α_i), |log α_i|/d, 1/d}.
- Let b' = |b_1|/(d log B_2) + |b_2|/(d log B_1), and Γ = b_1 log α_1 + b_2 log α_2.
- Then

      log|Γ| > -24.34 d^4 (max{log b' + 0.14, 21/d, 1/2})^2 log B_1 log B_2.

**Application.** Take:
- α_1 = 2 and α_2 = 5, which are multiplicatively independent; d = 1;
- b_1 = -(3l+k) and b_2 = k+l, so that Γ = Λ;
- log B_1 = max{log 2, log 2, 1} = 1 and log B_2 = log 5.

Then b' = (3l+k)/log 5 + (k+l). Step 3 gives b' < 7.204826 k + 6.093580. Combining with (1):

    (k-1) log 2 < 24.34 log 5 · max{log(7.204826 k + 6.093580) + 0.14, 21}^2.   (2)

Let G(k) be the left side of (2) minus its right side. We show G(k) > 0 for every k ≥ K_0 = 24925, which contradicts (2).

- **Region I: log(7.2048k + 6.09) + 0.14 ≤ 21.** The right side is the constant 24.34 · 441 · log 5 = 17275.610. The left side is increasing, and (K_0 - 1) log 2 = 17276.000 > 17275.610. (For comparison, G(24924) = -0.30 and G(24925) = +0.39.)
- **Region II: k ≥ k_1 = 159132686, where the maximum becomes log b' + 0.14.**
  - G(k_1) = 1.10 · 10^8 > 0.
  - G'(k) ≥ log 2 - 2 · 24.34 log 5 · (log(7.21k + 6.1) + 0.14)/k. This bound is increasing in k for k ≥ 3, because t/k is decreasing there. At k_1 it is 0.6931 > 0.
  - So G increases on [k_1, ∞).

**Hence k ≤ 24924, and by Step 3, l ≤ 1.94954 · 24924 + 2.13.**

### Step 5: the finite scan (exact integers)

For each 1 ≤ k ≤ 24924, let l_0 = round(r k) and take the window [max(1, l_0 - 4), l_0 + 4].

**The window is certified exactly.** Λ decreases strictly in l, by log(8/5) per step. The scan checks with integers that:
- 5^{k+l} ≥ 3 · 2^{3l+k} at l = l_0 - 5, when that is ≥ 1;
- 2^{3l+k} ≥ 3 · 5^{k+l} at l = l_0 + 5.

So every l outside the window has |Λ| ≥ log 3 > 1, which (1) excludes.

**Inside the window.** The scan tests (★) exactly:
- first the necessary condition |Δ| < 8^l, by bit operations;
- then |Δ| ≤ 8^l - 5^l.

The only pairs that survive are:

| (k, l) | Δ |
|---|---|
| (1, 2) | 3 |
| (2, 4) | 759 |
| (3, 6) | 144027 |

### Step 6: the e-enumeration

By (★), e ≤ (8^l - 5^l)/|Δ|. That gives e ≤ 13 for (1, 2), e ≤ 4 for (2, 4), and e ≤ 1 for (3, 6).

For every odd e in these ranges, the check simulates x_0 = 2^k e for k + l steps. It tests the parity word E^k O^l and the return to x_0. Exactly three cases succeed:
- (1, 2, e = 1): 2 → 5 → 3;
- (1, 2, e = 3): 6 → 15 → 9;
- (1, 2, e = 13): 26 → 65 → 41.

Every one-minimum cycle has the form of Steps 2 and 3 with k ≤ 24924. So this list is complete. ∎

## What is conditional

- **The constant 24.34 and the hypotheses of LMN 1995, Corollaire 2.** I could not open the original paper: Elsevier returned 403. I read the statement verbatim, with the hypotheses as quoted in Step 4, in a secondary source: Théorème 2.5 of arXiv:2208.05752, which cites "[15] Laurent, Mignotte, Nesterenko 1995, Corollary 2, pp. 288".
  - This is the same statement that census/lhf/mixed/CLS-048.md and CLS-053.md use.
  - I did not check it against the primary text.
  - The proof is otherwise complete. If a reader wants a fully primary-sourced proof, Step 4 is the one line to re-verify.
- **The cutoff has margin.** Even replacing 24.34 by 30 would only move K_0 to about 30700. The scan handles that easily: about 25 s for k ≤ 24924.

## Stretch goal (two local minima): not achieved

With two minima, the parity word is E^{k_1} O^{l_1} E^{k_2} O^{l_2}, and the analogue of (1) is

    |Λ| ≲ C (2^{-k_1} + 2^{-k_2}),   Λ = K log(5/2) - L log(8/5),   K = k_1 + k_2,   L = l_1 + l_2.

This decays only in min(k_1, k_2). A cycle with k_1 = 1 and K large is not controlled by a two-log bound alone. One needs a Simons–de Weger-type treatment: an exact two-block cycle equation in the free parameters, plus a reduction such as LLL or Baker–Davenport. I did not attempt it here.

## How to verify

    python3 census/advance/permd-1cycles/check.py

It runs in about 25 s and exits 0 iff all parts pass. It uses only exact integers, plus `decimal` at 60 digits for the logarithms in Step 4. Python's `Decimal.ln` and `Decimal.exp` are correctly rounded. Every margin in Step 4 is at least 0.3 in absolute value, far larger than the 1e-50 rounding error.

It checks:
1. that D agrees with systems.py on 1..10^5, and that the falling-block identity and |S| ≤ 8^l - 5^l hold on every falling block from an odd start < 4000;
2. the Step 4 constants: the bounds on l and b', Region I, and Region II with the derivative bound;
3. the certified exact scan of Step 5;
4. the e-enumeration of Step 6.

## Referee (round 1)

**Verdict: CONFIRMED.** The one-local-minimum classification holds. The only condition is the one the prover already declares: the LMN 1995 Corollaire 2 constant has not been checked against the primary text. I found no mathematical error.

**Re-derived independently**
- **Step 1.** For n ≥ 3 odd, D(n) ≤ (5n+3)/8 < n. A strict local minimum is exactly an even element whose predecessor is odd. This also holds for length-2 cycles, where the predecessor equals the successor. D is injective, so there are no ties. {1} has no local minimum.
- **Step 2.** The 2-adic argument gives a = k, so x_0 = 2^k e. The falling-block identity is 8^l y_l = 5^l y_0 + Σ s_j 5^{l-1-j} 8^j. I checked it by induction, and it also holds when 1 appears in the block. |S| ≤ 8^l − 5^l. Δ is odd, hence nonzero.
- **Step 3.** In both sign cases |Λ| < 2^{1−k}. At k = 1, −log(1/2) = 0.693 < 1, so the case holds.
- **Step 4.** I checked the assignment: b_1 = 3l+k goes with α_1 = 2 and log A_1 = 1, and b_2 = k+l goes with α_2 = 5 and log A_2 = log 5. So b' = (3l+k)/log 5 + (k+l), matching the convention of the sources. The cutoff (k−1) log 2 ≤ 24.34·441·log 5 gives k ≤ 24924, with margin 0.39. The constant 21 dominates while log b' + 0.14 < 21, which covers at least up to k = 10^8. Beyond 10^8, the right side divided by k decreases while the left side divided by k increases. The prover's derivative argument is also valid: t/k is decreasing and t > 1.
- **Steps 5 and 6.** The float l_0 only places the window. Both window edges are certified with integers, and Λ is strictly monotone in l. The e-bounds 13, 4 and 1 are correct.

**Independent computation.** I wrote `referee_check.py`, which shares no code with check.py. It exits 0 (ALL PASS) in about 260 s.
- **(A) Map and brute force.** D is rebuilt from the mod-8 table and matches systems.py on 1..50000. Orbits from n ≤ 20000 meet only the cycles {1}, {2,5,3}, {6,15,9} and {26,65,41}. In each, the number of minima equals the number of even runs.
- **(B) Cutoff.** I recomputed the cutoff in 80-digit Decimal.
- **(C) Scan.** An exact scan of all 1 ≤ k ≤ **31000** covers the case where 24.34 is replaced by 30, since that cutoff is about 30720. The window {l : 1/3 < 5^{k+l}/2^{3l+k} < 3} is found by walking outward to both sign changes. Survivors: (1,2), (2,4), (3,6) only.
- **(D) Solving for e.** I solved eΔ = S over all 4^l sign vectors, rather than enumerating e. Each solution was confirmed by simulation, including that the s-vector matches the actual residues. The solutions are exactly e = 1, 3, 13 for (k,l) = (1,2).

The prover's check.py also exits 0 here (90.6 s wall time).

**Literature constant.** The primary text was again unavailable: ScienceDirect returned 403 to both curl and WebFetch. I checked the statement in three independent secondary sources, and they agree on the 24.34 form:
1. arXiv:2208.05752, Théorème 2.5. It takes α_1, α_2 multiplicatively independent positive reals, log B_i ≥ max{h, |log α_i|/d, 1/d}, b' = |b_1|/(d log B_2) + |b_2|/(d log B_1), and gives log|Γ| > −24.34 d^4 (max{log b' + 0.14, 21/d, 1/2})^2 log B_1 log B_2.
2. H. Batte and F. Luca, arXiv:2412.12130, Theorem 2.2, which is "Corollary 2 in [LMN]". The form there is Λ = b_1 log γ_1 − b_2 log γ_2, where |γ_1|, |γ_2| ≥ 1 are real and multiplicatively independent, and b_1, b_2 are positive integers. The inequality is the same.
3. J. L. Simons, Acta Arith. 131.3 (2008), eq. (37), which quotes "Corollaire 2" of LMN. Simons applies it exactly to Λ = (K+L) log 2 − K log p.

All the hypotheses hold here: 2 and 5 are real, ≥ 1 and multiplicatively independent; b_1 and b_2 are positive integers; D = 1.

One further source, arXiv:2202.13182 Thm 2.1, quotes a different LMN variant: 30.9·max{log b', 21/D, 1/2}^2, with no +0.14. Under that variant the cutoff would be about k ≤ 31641, slightly beyond my 31000 scan. This does not affect the proof, which uses the 24.34 form confirmed above.

**Gap list (all minor; none invalidates the result)**
1. **Primary source.** LMN 1995 Corollaire 2 has still not been read in the primary source (J. Number Theory 55, 285–321). It is confirmed by three concordant secondary sources. The result is conditional on that.
2. **Status label.** The heading says "PROVED, with one caveat" while the claim JSON says CONDITIONAL. The heading should read "PROVED conditional on the LMN Cor. 2 constant (verified in three secondary sources)".
3. **Runtime.** The stated ~25 s runtime is machine-dependent; it measured 90 s here. This is still well under the limit.
4. **Region II comment in check.py.** The comment "(t1+1) covers t on [k1,k1+1)" is a loose justification. The real reason is that t/k is decreasing, so the bound at k_1 dominates every k ≥ k_1. The conclusion is unaffected.
5. **Stretch goal.** The two-minima case is honestly reported as not done. Nothing more is claimed.

## Addendum: unconditional via Laurent (2008)
`laurent_addendum.py` repeats Step 4 with Laurent, Acta Arith. 133 (2008), Corollary 2
(read in the primary source by the constants-audit cohort and its referee). The best row
(m=10, C2=25.2) gives k < 7431, inside the exact scan k <= 24924. The result therefore no
longer depends on the LMN 1995 constant and is unconditional.
