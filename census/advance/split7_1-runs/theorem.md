# CLS-053 (desc_split7_1): range certificate to 2^50, cycles need at least 70 expanding runs, and a power bound for never-dropping starts

**Map.** T(n) = n/2 for even n, 7n+1 for n ≡ 1 (mod 4), and n+1 for n ≡ 3 (mod 4). The only known cycle is (1 8 4 2).
**Open question (GLOBAL).** Is every positive orbit eventually periodic? It stays open.

**Status: PROVED (three restricted results).** The only outside input is one published constant, a two-logarithm bound due to Laurent. I read it as restated in a 2026 arXiv paper and not in Laurent's original paper; see §2.4.

## Theorems

**Theorem 1 (range).** Every integer 1 ≤ n < 2^50 reaches the cycle (1 8 4 2).

**Theorem 2 (runs).** Let S be the odd-to-odd map: S(x) = (7x+1)/2^v for x ≡ 1 (mod 4) and S(x) = (x+1)/2^v for x ≡ 3 (mod 4), where v is the full 2-adic valuation. An odd x has S(x) > x exactly when x ≡ 5 (mod 8), and then S(x) = (7x+1)/4. Call such a step *expanding*. An *expanding run* is a maximal cyclic block of consecutive expanding S-steps in a cycle.

Every T-cycle other than (1 8 4 2) satisfies all of the following:
- its minimum is greater than 2^50;
- it has **at least 70 expanding runs**, so every cycle with at most 69 runs is (1 8 4 2);
- it has at least as many F-runs (runs of the block map F in §2.1) as expanding runs, so the F-run count is also at least 70.

This extends census/lhf/mixed/CLS-053.md, which excluded r = 1 only.

**Theorem 3 (density).** Let H(X) be the number of n ≤ X with T^k(n) ≥ n for every k ≥ 1. For X ≥ 1,

  H(X) ≤ (54/11) · X^{log₂(27/16)},  where log₂(27/16) = 0.75488…

So the never-dropping starts have natural density zero. The set of 2-adic integers whose slope never drops below 1/2 also has Haar measure zero.

---

## 1. Proof of Theorem 1 (exact residue tree)

The tree is ported from census/round2/rewriting/check_split5_3_range.py.

**Node data.** A node is a quadruple (d, r, a, b) of integers, d ≤ 50, with this invariant: for every n = 2^d·t + r with t ≥ 0, the number a·t + b equals T^k(n) for some k ≥ 0 that does not depend on t. The root is (0, 0, 1, 0).

**Children.** A child fixes one more bit of t. Write t = 2u + e with e ∈ {0, 1} and set y = b + e·a, so the reached value is 2a·u + y.
- **y even.** The value is even. Halve it: (a, y/2).
- **y odd, a odd.** The value is odd, but its residue mod 4 depends on u. Keep the value: (2a, y).
- **y odd, a even.** Then 2a ≡ 0 (mod 4), so the value is ≡ y (mod 4).
  - If y ≡ 1 (mod 4), take 7x+1, then /2, then /2. Both halvings are legal because 14a ≡ 0 (mod 4) and 4 | 7y+1. The new data is (7a/2, (7y+1)/4).
  - If y ≡ 3 (mod 4), take x+1, then /2, then /2. The new data is (a/2, (y+1)/4).

Induction shows that a is odd or twice an odd number, so every division above is exact.

**Leaves.** A node is a leaf when a < 2^d, or when a = 2^d and b < r, or when d = 50.
- If a ≤ 2^d and b < r, then a·t + b < n for all t.
- If a < 2^d, then a·t + b < n for every t > (b−r)/(2^d−a).
- Each remaining start n < 2^50 in a leaf is iterated directly until the value drops below n or equals 1.

A value below n is a positive iterate smaller than n. Strong induction on n then shows that n reaches (1 8 4 2).

**Coverage.** The leaves partition the positive integers below 2^50, and the program checks that the leaf counts sum to exactly 2^50 − 1.

**Arithmetic.** All arithmetic uses unsigned 128-bit integers. Every node asserts a, b < 2^100, and every raw step asserts no overflow.

**Run data.** 5,263,636,935 nodes and 1,976,164,335 direct simulations. The longest direct run had 177 extra raw steps. The run takes about 12 s on 12 cores.

**Cross-checks.** An independent pure-Python port certifies everything below 2^26, and spot-checks that a·t + b really is an iterate of n. A plain brute force checks that every n < 2^20 drops below itself.

## 2. Proof of Theorem 2

### 2.1 Setup

Let C be a T-cycle other than (1 8 4 2), and let m = min C.
- **m is odd.** If m were even, m/2 would be a smaller element of C.
- **m > 2^50.** If m < 2^50, Theorem 1 says m reaches (1 8 4 2). Since m is periodic, m would lie on that cycle, so C = (1 8 4 2).

The odd elements of C form an S-cycle with the same minimum m. Every value used below is ≥ m.

**Step facts (exact).**
- For odd x: x ≡ 5 (mod 8) ⇔ 8 | 3x+1. In that case S(x) = (7x+1)/4 is odd, S(x) > x, and 3S(x)+1 = (7/4)(3x+1).
- For x ≡ 1 (mod 8) (a *C-step*): S(x) = (7x+1)/2^v with v ≥ 3, so S(x) ≤ (7x+1)/8 < x when x > 1.
- For x ≡ 3 (mod 4) (a *B-step*): S(x) = (x+1)/2^v with v ≥ 2, so S(x) ≤ (x+1)/4 < x.

So S is increasing exactly on expanding steps. A cycle with no expanding step would be strictly decreasing, so C has r ≥ 1 runs.

The minimum m is preceded by a decrease and followed by an increase, so m starts a run. Label the runs cyclically from m: run i starts at x_i (x_1 = m), has length k_i, and ends at y_i = A^{k_i}(x_i), where A(x) = (7x+1)/4. After it comes a *gap* of s_i ≥ 1 contracting steps from y_i down to x_{i+1}.

**Comparison with F-runs.** Let F be the block map on all positive integers: x/2 for even x, (7x+1)/4 for x ≡ 1 (mod 4), (x+1)/4 for x ≡ 3 (mod 4). Every expanding run is contained in an F-run of A-blocks, and distinct runs lie in distinct F-runs. So the number of F-runs is at least r.

### 2.2 The cycle identity and its error

Count over one period of C:
- K = total number of 7x+1 steps (expanding plus C-steps);
- K_exp = Σ k_i;
- L = total number of halvings.

The ratios S(x)/x are:
- expanding step: (7/4)(1 + 1/(7x));
- C-step: 7·2^{−v}(1 + 1/(7x));
- B-step: 2^{−v}(1 + 1/x).

The product of these ratios around the cycle is 1. Hence

  δ := L log 2 − K log 7 = Σ_{7x+1 steps} log(1 + 1/(7x)) + Σ_{B-steps} log(1 + 1/x) > 0.

Use log(1+u) ≤ u to bound each piece.

- **Runs.** On run i the inputs satisfy A^j(x_i) ≥ (7/4)^j·x_i. So the run contributes at most Σ_j (4/7)^j/(7x_i) = 1/(3x_i) ≤ 1/(3m).
- **Gaps.** Write the gap as w_0 = y_i > w_1 > … > w_s = x_{i+1}, all ≥ m, and set c = (7m+1)/(7m−7). Each step satisfies err(w_j) ≤ c/w_{j+1} − c/w_j:
  - C-step: w' ≤ (7w+1)/8, and c/w' − c/w ≥ c(w−1)/(w(7w+1)) ≥ 1/(7w). The last inequality is equivalent to c ≥ (7w+1)/(7w−7), which holds because that bound decreases in w and w ≥ m.
  - B-step: w' ≤ (w+1)/4, and c/w' − c/w ≥ c(3w−1)/(w(w+1)) ≥ 1/w.

  The sum telescopes, so a gap contributes less than c/x_{i+1} ≤ c/m.

Adding up, with m > 2^50:

  **0 < δ < r(1/3 + c)/m < 1.34·r/m.**  (★)

Since δ < log 2, it follows that K log₂7 < L < K log₂7 + 1.

### 2.3 Length bounds in terms of m

**Run lengths.** A run of length k from x needs x, A(x), …, A^{k−1}(x) all ≡ 5 (mod 8). In terms of z = 3x+1, which A multiplies by 7/4, this means 2^{2k+1} | 3x+1. So 2·4^{k_i} ≤ 3x_i + 1.

**Growth between runs.** Gaps decrease, so x_{i+1} < y_i, and 3x_{i+1} + 1 < (7/4)^{k_i}(3x_i + 1). By induction, 3x_i + 1 ≤ (7/4)^{k_1+…+k_{i−1}}(3m+1).

**Bound on K_exp.** Taking logs gives k_i log 4 ≤ ℓ' + (k_1+…+k_{i−1}) log(7/4), where ℓ' = log(3m+1) − log 2. Solving this linear recursion, with ρ = log 7/log 4:

  K_exp ≤ ℓ'(ρ^r − 1)/log(7/4).

**Bound on contracting steps.** Every contracting step has ratio at most 7/8 (for B, (1/4)(1 + 1/x) ≤ 7/8 also holds). So 0 = Σ log(S(x)/x) ≤ K_exp log(7/4) − N_c log(8/7) + δ, where N_c is the number of contracting steps. Since log(7/4)/log(8/7) < 4.2:

  K ≤ K_exp + N_c ≤ 5.2·K_exp + 1.

### 2.4 The two-logarithm bound (quoted constant)

**What was read.** T. Miyazaki, R. Scott, R. Styer, *Handling some Diophantine equation via Euclidean algorithm and its application to purely exponential equations*, arXiv:2604.18991v2 (2026), Proposition 6.1. They state it as "a result of Laurent which is a particular case of [17, Corollary 2; (m, C₂) = (10, 25.2)]", where [17] is M. Laurent, *Linear forms in two logarithms and interpolation determinants II*, Acta Arith. 133 (2008), 325–348. I read the arXiv restatement and **not** Laurent's paper itself.

**Statement (verbatim content).** Let α₁, α₂ be positive rational numbers, both greater than 1 and multiplicatively independent. Let H_j ≥ max{h(α_j), log α_j, 1} for j = 1, 2. Then for all positive integers b₁, b₂,

  log|b₂ log α₂ − b₁ log α₁| > −25.2 · H₁H₂ · max{log b′ + 0.38, 10}²,  where b′ = b₁/H₂ + b₂/H₁.

**Parameters used.** α₁ = 2, α₂ = 7, H₁ = 1, and H₂ = 1.95 ≥ log 7 (checked exactly). Also b₁ = L, b₂ = K, so |Λ| = δ. Then b′ = L/1.95 + K < 2.442K + 0.52, using L < 2.81K + 1. Combining with (★) and μ = log m:

  μ < log(1.34r) + 49.14 · max{log(2.442K + 0.52) + 0.38, 10}²,  with K ≤ 5.2·(μ + 1.1 − log 2)·ρ^r/log(7/4) + 1.

Here log(3m+1) ≤ μ + 1.1 was used.

**Bound on μ.** Call the right-hand side g(μ). The program finds μ₁ with three properties: g(μ₁) < μ₁; the log term is ≥ 10, so it is the maximum; and 50.4·H₂·(log b′ + 0.38)/μ₁ < 1.

Write the log term as h = log(pμ + q) with p, q > 0. Then g′(μ) ≤ 50.4H₂(h + 0.38)/μ, and (h + 0.38)/μ decreases because h′μ ≤ 1 ≤ h + 0.38. So g′ < 1 on [μ₁, ∞), which gives g(μ) < μ there. Hence μ < μ₁. For r = 69 this gives μ₁ ≈ 71238; for r = 1 it gives 8104.

### 2.5 Farey reduction (elementary, exact)

Let α = log₂7. The program computes α as a rational interval of width below 10^{−100}, using the atanh series with directed dyadic rounding and explicit tail bounds.

**Lemma.** Suppose a/b < α < c/d with bc − ad = 1, and 1 ≤ K < b + d. If L/K > α, then L − Kα ≥ c − dα.

*Proof.* Put s = bL − aK and t = cK − dL. Then L = sc + ta and K = sd + tb. Since L/K > a/b, we get s ≥ 1. If t ≥ 1, then K ≥ b + d, which is excluded, so t ≤ 0. Therefore L − Kα = s(c − dα) + t(a − bα) ≥ c − dα, because a − bα < 0. ∎

**Iteration.** Start from a bound m < M_i. It gives log(3m+1) ≤ log(3M_i + 1) and hence K ≤ K_max. A Stern–Brocot walk finds neighbours with b + d > K_max. The lemma and (★) then give δ = log 2 · (L − Kα) ≥ log 2 · (c − dα), so m < M_{i+1} := 1.34r/(log 2 · (c − dα)).

**Result.** For every r = 1, …, 69, this reaches M ≤ 2^50 within two rounds. For r = 69 the bit-sizes go 61 → 50, and the final neighbours have b = 4109614612265 and d = 3188982970547. That contradicts m > 2^50, so no cycle has r ≤ 69. For r = 70 the iteration stalls at 2^58 with these constants. ∎

## 3. Proof of Theorem 3

Read the bits of n from the bottom, exactly as in §1 but without pruning. After j bits, every class n ≡ r (mod 2^j) carries a reached iterate x = A·n + B, where A is the real slope a/2^j.

**States and updates.** The state is U when a is odd and O when a is twice an odd number. Each bit causes one update:

| State | Case | Update | Next state |
|---|---|---|---|
| U | value even | A → A/2, B → B/2 | U |
| U | value odd | A, B unchanged | O |
| O | value ≡ 1 (mod 4) | A → 7A/4, B → (7B+1)/4 | U |
| O | value ≡ 3 (mod 4) | A → A/4, B → (B+1)/4 | U |

Each node has one child of each kind. The table is exactly the child rule of §1.

**Potential.** Give U weight 1 and O weight w = 32/27, and let λ = 27/32. The sum of A·W over the two children is at most 2λ times A·W at the parent:
- from U: A(1/2 + w) ≤ 2λA, since 1/2 + 32/27 = 1.685… ≤ 1.6875;
- from O: A(7/4 + 1/4) = 2A = 2λwA.

So Σ over the 2^j classes of A·W ≤ (27/16)^j. Both weights are ≥ 1, so

  #{classes with A ≥ 1/2} ≤ 2 Σ A·W ≤ 2(27/16)^j.

**Intercept.** B ≥ 0. Put β = B + 1/3. A 7-update multiplies β by 7/4. A halving sends β to β/2 + 1/6, the (x+1)/4 update sends it to β/4 + 1/2, and the odd-record update leaves it unchanged. Each of these keeps β ≤ c whenever c ≥ 2/3. Starting from β = 1/3, induction gives B + 1/3 ≤ (2/3)(7/4)^{#7}, and #7 ≤ j/2. Hence B < 2^{j−1} ≤ n/2 for j ≥ 1. The base cases are j = 1, 2, and stepping j → j+2 multiplies the left side by 7/4 and the right side by 4.

**Conclusion.** Take n ∈ [2^j, 2^{j+1}) with j ≥ 1. Such n has exactly one representative per class mod 2^j. If A < 1/2, then x < n/2 + n/2 = n, and x ≠ n forces k ≥ 1, so n drops. Hence at most 2(27/16)^j starts in [2^j, 2^{j+1}) never drop. This also holds for j = 0. Summing over j ≤ log₂X:

  H(X) < (32/11)(27/16)^{J+1} ≤ (54/11)·X^{log₂(27/16)}.

The same expectation bound shows that the 2-adic set where A_j ≥ 1/2 for all j has Haar measure at most 2(27/32)^j → 0. ∎

## What is conditional

- **Theorem 2 only:** it depends on the Laurent (2008) Corollary 2 constant (25.2, 0.38, 10), which I read through the restatement in arXiv:2604.18991, Prop. 6.1, not in the original paper.
- **Theorems 1 and 3:** unconditional.
- **GLOBAL:** still open. A divergent orbit, or a cycle with at least 70 runs and minimum above 2^50, is not excluded.

## How to verify

`python3 census/advance/split7_1-runs/check.py` exits 0 iff every check passes. It runs in about 45–70 s and needs g++ or clang++. It does the following:
- compiles and runs `range.cpp` at 2^26 and 2^50;
- runs the Python tree at 2^26 and the brute force below 2^20;
- checks every numeric inequality of §2 with rational intervals, runs the Laurent plus Farey argument for each r = 1..69, and reports that r = 70 fails;
- checks the Part 3 weight inequalities exactly, verifies the full tree to depth 18 exactly, and confirms the count bound by brute force for j ≤ 20.

Room to improve: the factor 5.2 in K ≤ 5.2·K_exp + 1 costs about 5 runs. With F-runs in place of S-runs, the same method gives roughly 74. Going to range 2^58 would give about 85–90, but the C++ tree takes several minutes there.

## Referee (round 1)

**Verdict: CONFIRMED.** All three theorems hold as stated. Theorem 2 can be upgraded from CONDITIONAL to unconditional, because the Laurent constant has now been checked against the original paper (details below).

### What the referee re-derived by hand
- **§1 tree invariant.** All four child rules were re-derived: halving; storing odd values with 2a; 7x+1,/2,/2 when y ≡ 1 (mod 4); x+1,/2,/2 when y ≡ 3 (mod 4).
  - a is always odd or twice an odd number.
  - The leaf tests hold: floor((b−r)/(M−a)) + 1 > (b−r)/(M−a).
  - Coverage is a partition. The strong-induction closure is valid.
- **range.cpp overflow.** The comment "a,b < 2^100 and t < 2^60 keep a·t+b < 2^127" is false as a general statement. The code is still safe: at a simulation leaf, either a < 2^depth (so a·t < 2^bits) or depth = bits (so t = 0). Raw steps are guarded. This is a cosmetic issue, not a bug.
- **§2.** Each item below was re-derived:
  - the step facts;
  - "m starts a run";
  - the error identity;
  - the run bound 1/(3x_i);
  - the telescoping gap bound with c = (7m+1)/(7m−7), for both the C-step and B-step inequalities;
  - 2^{2k+1} | 3x+1;
  - the linear recursion giving K_exp ≤ ℓ'(ρ^r − 1)/log(7/4);
  - N_c < 4.2·K_exp + 1, hence K ≤ 5.2·K_exp + 1;
  - the derivative and monotonicity argument for μ₁;
  - the one-sided Farey lemma, including s ≥ 1, t ≤ 0 and the sign of t(a − bα).

  F-runs ≥ r also holds. After an expanding run, the first contracting step is either a B-block or an A-block that lands on an even number, so the next F-step is a halving. Either way the F-run ends.
- **§3.** Re-derived:
  - the U/O transition table (an O node always has odd b, so its two children are ≡ 1 and ≡ 3 (mod 4));
  - the weights 91/54 ≤ 27/16 and 2 = 2λw;
  - the β = B + 1/3 invariant;
  - #7 ≤ ⌊j/2⌋;
  - B < 2^{j−1} ≤ n/2;
  - the final summation (32/11)(27/16)^{J+1} = (54/11)(27/16)^J ≤ (54/11)X^{log₂(27/16)}.

### Constant check (source consulted directly)
M. Laurent, *Linear forms in two logarithms and interpolation determinants II*, Acta Arith. 133.4 (2008), 325–348, p. 328.

**Setup.** Λ = b₂ log α₂ − b₁ log α₁, with b₁, b₂ positive integers. D = [Q(α₁,α₂):Q]/[R(α₁,α₂):R]. Also b′ = b₁/(D log A₂) + b₂/(D log A₁), where log A_i ≥ max{h(α_i), |log α_i|/D, 1/D}.

**Corollary 2.** Suppose α₁ and α₂ are multiplicatively independent, and moreover α₁, α₂, log α₁, log α₂ are real and positive. Then

  log|Λ| ≥ −C₂ D⁴ (max{log b′ + 0.38, m/D, 1})² log A₁ log A₂,

with (m, C₂) = (10, 25.2) from Table 1.

**Application.** With α₁ = 2, α₂ = 7, D = 1, log A₁ = 1 ≥ max(log 2, log 2, 1) and log A₂ = 1.95 ≥ log 7 = 1.9459…, this is exactly the form used in §2.4, with b₁ = L and b₂ = K. Every hypothesis holds. The prover's secondary quotation (arXiv:2604.18991v2, Prop. 6.1) agrees with the original. That restatement has a typo, "log α_i" for "log α_j", which does not matter here.

### Independent computation (referee's own code)
Command: `python3 referee_check.py`. It exits 0 and runs in about 2 minutes. It uses:
- **referee_range.cpp.** This is a different implementation of the residue tree, written from the definition of T. It applies raw T steps greedily whenever the parity or the residue mod 4 is determined, and starts from the 2^14 root classes. It certifies every 1 ≤ n < 2^50, with covered = 2^50 − 1 exactly, using 1.14e10 nodes and 4.27e9 direct simulations, in about 57 s. This confirms Theorem 1 independently of range.cpp.
- **Part 2 redone with different tools.** The referee used Python `decimal` at 250 digits with correctly rounded ln, and every decision has a margin of at least 1e-20.
  - The reduction uses continued-fraction convergents of log₂7 and the classical two-sided best-approximation lemma (|Kα − L| ≥ |q_kα − p_k| for 0 < K < q_{k+1}), not the one-sided Stern–Brocot lemma.
  - For every r = 1..69 it gives m < 2^50, a contradiction.
  - At r = 69: μ₁ ≈ 71234, and the bit history is 63 → 50.
  - It fails at r = 70, at 2^58, which matches the prover.
- **Brute force.** Every 2 ≤ n < 2^18 drops. The never-dropping count in [2^j, 2^{j+1}) is 0 for every 1 ≤ j ≤ 26; a start that does not drop within 2·10^4 steps would be counted, so the count errs on the high side. This sanity check is weak: Theorem 1 already gives H(X) = 1 for X < 2^50, so the bound is carried by the proof, not by the data.
- **Prover's checks.** check.py was re-run and exits 0 (22 PASS, about 38 s).

### Gap list (none fatal)
1. **Status label (fixed by this referee).** Theorem 2 was marked CONDITIONAL only because the constant was read secondhand. The original has now been consulted (see above), so Theorem 2 is unconditional.
2. **§2.3 wording.** "Every contracting step has ratio at most 7/8" is false for the full ratio of a C-step: (7x+1)/(8x) > 7/8. The displayed inequality 0 ≤ K_exp log(7/4) − N_c log(8/7) + δ is correct, because only the main terms 7·2^{−v} and 2^{−v} are bounded by 7/8 and the corrections are in δ. The parenthetical about (1/4)(1 + 1/x) is irrelevant. Suggest rewording.
3. **range.cpp comment.** The overflow comment is wrong (see above); the code is safe.
4. **"Independent" Python port.** check.py's pure-Python port uses the same algorithm as range.cpp and was written by the same author, so it is not independent. referee_range.cpp fills that role.
5. **Theorem 3 brute-force check.** The brute-force part of check.py's Part 3 is vacuous (every count is 0 or 1 by Theorem 1). This is harmless; the proof stands on its own.
