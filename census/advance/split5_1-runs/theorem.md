# split5_1 (CLS-048): convergence below 2^42, lower bounds on further cycles, and a density bound

**Map.** T(n) = n/2 for even n; 5n+1 for n ≡ 1 (mod 4); n+1 for n ≡ 3 (mod 4).
Known cycles: C1 = (1 6 3 4 2), and C13 with minimum 13 and period 35.

Earlier repo results: census/lhf/mixed/CLS-048.md shows that the only cycle with one expanding run is C1. census/round2/rewriting/split5_1_s27.md gives a descent-tree exceptional set.

## Statements

**Theorem A (range certificate).** Every integer 1 ≤ n < 2^42 eventually reaches C1 or C13.

**Theorem B (further cycles).** Let C be a positive T-cycle other than C1 and C13. Then
1. (unconditional) C has K ≥ 1,936,274 steps n → 5n+1 and L ≥ 4,495,889 halvings. In all it has at least 6,432,164 steps of T (at least 6,432,187 when part 2 is used).
2. (unconditional; uses Laurent's 2008 two-logarithm bound, quoted from the primary source below) C has more than **R = 23** expanding runs. Equivalently, C1 (1 run) and C13 (4 runs) are the only cycles with at most 23 runs.

**Theorem C (density).** Let H(X) be the number of n ≤ X such that T^k(n) ≥ n for every k ≥ 1. Then H(X) = O(X^0.9383). In particular these starts have natural density zero.

Here a *run* is a maximal cyclic block of consecutive A-steps of the odd-to-odd map S defined below. The bound R = 23 falls well short of the target R ≥ 100. Section B.4 explains why this method cannot reach R = 100.

## Notation and step facts

For odd x write A(x) = (5x+1)/2 when x ≡ 1 (mod 4). This takes 2 T-steps. Write B(v) = (v+1)/2^e with e = v_2(v+1) when v ≡ 3 (mod 4). This takes 1+e T-steps, and e ≥ 2. Let S be the map that sends an odd x to A(x) or B(x).

- (F1) For odd x, x ≡ 1 (mod 4) holds iff 4 | 3x+1. Also 3A(x)+1 = (5/2)(3x+1), and A(x) is odd.
- (F2) Each A-step lowers v_2(3x+1) by exactly 1. So a run of A-steps from x has exactly k = v_2(3x+1) − 1 steps, and it ends at a value y ≡ 3 (mod 4). In particular 2^{k+1} ≤ 3x+1.
- (F3) B(v) ≤ (v+1)/4. So v ≥ 4B(v) − 1 ≥ 3B(v).

The checker verifies (F1)–(F3) by brute force for odd x < 2·10^5. Each one is also a one-line congruence argument.

## A. Proof of Theorem A

**Residue tree.** A node (d, r, a, b) asserts that T^s(2^d t + r) = a t + b for all t ≥ 0, for some s ≥ 0. The root is (0, 0, 1, 0). Put t = 2u + g with g ∈ {0, 1}, and y = b + a g. The child value is then 2a u + y, and the child is chosen as follows:

| case | child | T-steps added |
|---|---|---|
| y even | (d+1, r+g2^d, a, y/2) | 1 |
| y odd, a odd | (d+1, r+g2^d, 2a, y) | 0 (the residue mod 4 is not yet known) |
| y odd, a even, y ≡ 1 mod 4 | (d+1, r+g2^d, 5a, (5y+1)/2) | 2 |
| y odd, a even, y ≡ 3 mod 4 | (d+1, r+g2^d, a, (y+1)/2) | 2 |

In the last two rows 2a ≡ 0 (mod 4), so every member of the child class has residue y mod 4. Together these rows give exact affine images of T-iterates. The checker confirms this on all 32,767 nodes of depth ≤ 14 and on 8 values of t per node.

A node is a **leaf** when one of three conditions holds:
- a < 2^d. Then a t + b < 2^d t + r for t > (b−r)/(2^d−a).
- a = 2^d and b < r. Then the class descends uniformly.
- d = 42.

At a leaf, the finitely many remaining n < 2^42 of the class are iterated directly from the reached value a t + b. The iteration stops when the value drops below n or hits a cycle minimum (1 or 13). Every leaf class therefore consists of starts that either drop below themselves or lie on a known cycle. The leaves partition [1, 2^42): the checker sums the covered counts to exactly 2^42 − 1.

Theorem A then follows by strong induction on n. The periods are checked: 1 has period 5 and 13 has period 35, each the minimum of its cycle.

**Computation.** `range.cpp` (128-bit integers, OpenMP) is compiled and run by check.py. In the measured run the tree had 24,979,688,741 nodes. Direct iteration handled 11,110,967,294 starts, each needing at most 747 extra T-steps. The run took about 280 s on 12 threads. Node arithmetic stays below 2^100. *Proof.* (i) The coefficient a is 1 until the first odd y at a node with a = 1, which doubles it to 2. After that a is even, and the four rules only keep a or multiply it by 5. So a ∈ {1} ∪ {2·5^j : j ≤ d−1}, hence a ≤ 2·5^41 < 2^97 at depth ≤ 42. (ii) Let ρ = b/a, with ρ = 0 at the root. In every rule y = b + ga ≤ (ρ+1)a, and the child ratio is y/(2a), (5y+1)/(10a) or (y+1)/(2a). Each is at most (ρ+1)/2 + 1/(2a) ≤ ρ/2 + 1, because a ≥ 1. By induction ρ ≤ 2 at every node. So b ≤ 2a < 2^98, y ≤ 3a, and 5y+1 < 2^100. Direct iteration happens only at leaves. A leaf with a < 2^d has a < 2^42 and t < 2^42, so a t + b < 2^99. A depth-cap leaf has t = 0 only. Later iterates go through step(), which throws an overflow exception above 2^125; none occurred. ∎ A separate Python loop iterates every n < 2^20 directly as an independent cross-check.

## B. Proof of Theorem B

Let C be a further cycle with minimum m. By Theorem A, every element of C is at least 2^42, so m ≥ 2^42. Pass to the odd elements and the map S. The minimum m is odd. It satisfies m ≡ 1 (mod 4), because n ≡ 3 gives (n+1)/2 < n. Its S-predecessor is a B-step, since A increases values. So m starts a run.

Write the cycle as r runs. Run i goes from x_i to y_i in k_i A-steps. The descent after run i consists of B-steps v → B(v) and ends at x_{i+1}, with x_1 = m. Put K = Σ k_i, and let L be the total number of halvings, which includes one inside each A. Put α = log_2 5.

**B.1 Linear form.** Let g(x) = (3x+1)/(3x). By (F1),

 A(x)/x = (5/2)·g(x)/g(A(x)),

so a run telescopes: y_i/x_i = (5/2)^{k_i} g(x_i)/g(y_i). Each B-step satisfies B(v)/v = 2^{−e}(1+1/v). Taking the product around the cycle gives

 δ := L log 2 − K log 5 = Σ_i [log g(x_i) − log g(y_i)] + Σ_B log(1 + 1/v).

Every term is positive, since y_i > x_i, so δ > 0. For the upper bound, use log g(x_i) ≤ 1/(3x_i). By (F3), the descent values before x_{i+1} are at least 3x_{i+1}, 9x_{i+1}, … when read backwards, so their terms sum to at most 1/(2x_{i+1}). Hence

 **0 < δ < (5/6)·r/m.**  (★)

**B.2 Length (part 1).** Since r ≤ K, (★) gives α < L/K < α + 5/(6·m·log 2) ≤ α + 5/(6·2^42·log 2). The checker computes, with exact Fractions and a rigorous enclosure of α, Stern–Brocot neighbours a/b = 4268621/1838395 and c/d = 227268/97879. They satisfy bc − ad = 1 and enclose that whole interval. Any L/K strictly between them satisfies K = b(cK − dL) + d(bL − aK), so K ≥ b + d = 1,936,274. Then L > Kα gives L ≥ 4,495,889. The number of T-steps is K + L + N_B, where N_B ≥ r ≥ 1 counts the n → n+1 steps (each run is followed by at least one). So there are at least 1,936,274 + 4,495,889 + 1 = **6,432,164** T-steps. No Baker bound is used in this part. Combined with part 2 (r ≥ 24), the count rises to at least 6,432,187.

**B.3 Runs (part 2).** Put G_i = log_2((3x_i+1)/2). By (F2), k_i ≤ G_i. By (F1), 3y_i+1 = (5/2)^{k_i}(3x_i+1). By (F3), 3x_{i+1}+1 ≤ (3y_i+7)/4 ≤ (3y_i+1)/2. Hence G_{i+1} ≤ G_i + (α−1)k_i − 1 < α G_i. This gives G_i ≤ α^{i−1} G_1 and

 K ≤ G_1 (α^r − 1)/(α − 1) ≤ C_R (1 + log m / log 2),  with C_R = (α^R − 1)/(α − 1) and r ≤ R.  (†)

*Baker stage.* Apply Laurent's two-logarithm bound (quoted below) to Λ = b_2 log α_2 − b_1 log α_1 with α_2 = 2, b_2 = L, α_1 = 5, b_1 = K, so Λ = δ > 0. The numbers 2 and 5 are multiplicatively independent, and 2, 5, log 2, log 5 are real and positive. K, L are positive integers. D = 1. Take log A_1 = log 5 ≥ max(h(5), log 5, 1) and log A_2 = 1 ≥ max(h(2), log 2, 1). Then b' = b_1/log A_2 + b_2/log A_1 = K + L/log 5. Since L < Kα + δ/log 2 and δ < 1, b' < K(1 + 1/log 2) + 1/(log 2 · log 5) < 2.443K + 1. With μ = log m, (★) gives, for each pair (m*, C_2) of Laurent's Table 1,

 μ < log(5R/6) + C_2·log 5·max(log b' + 0.38, m*, 1)^2 =: F(μ),

where b' is bounded through (†). The checker tries all eleven pairs. For R = 23 the best is (m*, C_2) = (30, 17.9), which gives μ_0 = 28525 with F(μ_0) < μ_0 and 2·17.9·log 5·Lg(μ_0) < μ_0, where Lg(μ) is the max(...) term. The bound for b' is affine in μ with a positive constant term, so dLg/dμ ≤ 1/μ, and F'(μ) ≤ 2c·Lg(μ)/μ with c = 17.9 log 5. Since Lg ≥ 30 > 1, Lg(μ)/μ is decreasing. Hence F'(μ) < 1 and F(μ) < μ for all μ ≥ μ_0, so m < e^{28525}.

*Continued-fraction stage.* **Lemma.** Suppose gcd(P, Q) = 1, |α − P/Q| < 1/Q^2 and 0 < K < Q/2. Then |L − Kα| > 1/(2Q). (Proof: LQ − KP ≠ 0, so |L − Kα| ≥ 1/Q − K/Q^2.) Combined with (★), this gives m < 5RQ/(3 log 2).

The stage alternates two bounds. Equation (†) bounds K by K_0 = C_R·log_2(2m). The lemma, applied to the first convergent P/Q of α with Q > 2K_0, then bounds m. All convergents are certified against a rational enclosure of α of width less than 10^-150. For R = 23 the bounds go e^{28525} → (Q = 23062019849360) m < 1.275·10^15 → (Q = 24793177656) m < 1.371·10^12 < 2^42. This contradicts m ≥ 2^42, so r ≥ 24. The checker finds the largest R that works. R = 24 fails.

**Source of the constant (primary source, consulted).** M. Laurent, *Linear forms in two logarithms and interpolation determinants II*, Acta Arithmetica 133.4 (2008), 325–348, Corollaries 1–2 and Table 1, p. 328. I downloaded the publisher's PDF (impan.pl) and read the statement. The setup on p. 326: α_1, α_2 are non-zero algebraic numbers, Λ = b_2 log α_2 − b_1 log α_1 with b_1, b_2 positive integers, and D = [Q(α_1, α_2) : Q]/[R(α_1, α_2) : R]. On p. 328, put b' = b_1/(D log A_2) + b_2/(D log A_1), where A_1, A_2 > 1 are real numbers with log A_i ≥ max{h(α_i), |log α_i|/D, 1/D}. Corollary 1 assumes α_1, α_2 are multiplicatively independent. Corollary 2 states: "Suppose moreover that the numbers α_1, α_2, log α_1, log α_2 are real and positive. Then

 log|Λ| ≥ −C_2 D^4 (max{log b' + 0.38, m/D, 1})^2 log A_1 log A_2

for each pair (m, C_2(m)) from Table 1." Table 1 gives, for m = 10, 12, …, 30, C_2 = 25.2, 23.4, 22.1, 21.1, 20.3, 19.7, 19.2, 18.8, 18.4, 18.1, 17.9. check.py hard-codes exactly this table. Part 2 of Theorem B therefore no longer rests on the secondary quotation of LMN 1995. For comparison, the LMN 1995 Cor. 2 constant (24.34, +0.14, 21/d), quoted in arXiv:2208.05752 and used in round 1, also gives R = 23.

**B.4 Why R stays small.** The recursion (†) is exponential in r with base α = log_2 5 ≈ 2.32. By comparison, split5_3 has base log_4 5 ≈ 1.16, which let GPT reach R = 100 there. Any reduction of this kind needs about m ≳ C_R log m. Each extra run therefore costs about log_2 α ≈ 1.2 bits of the range certificate. Reaching R = 100 would need a certificate near 2^125. A 2^40 certificate gives R = 19 (check.py 40). Getting past this barrier needs a non-exponential bound on Σ k_i in terms of r. A run i of length k_i needs 2^{k_i+1} | 3x_i+1, and chains of near-maximal runs are 2-adically consistent. So the extra gain must come from the cycle condition, not from the local structure.

## C. Proof of Theorem C

Use the residue tree of Section A without leaves, and write the reached value as x = A n + B, with A = a/2^d and B = b − A r. Every node is in one of three states:
- U: a is odd.
- O: a ≡ 2 (mod 4) and b is odd.
- E: a ≡ 2 (mod 4) and b is even.

The transitions follow from the table in Section A, and the checker verifies them on all nodes of depth ≤ 14.
- From U, the two children are U (×1/2) and O (×1).
- From O, they are O (×5/2, an A-step) and E (×1/2, x+1 then halve).
- From E, they are E (×1/2) and O (×1/2).

Take θ = 1/4, w_U = 1, w_O = 1, w_E = 0.783 and λ = 0.958. The checker verifies in exact rationals, using rational upper bounds for (5/2)^{1/4} and 2^{−1/4}, that at every node the average over the two children of A^θ·w(state) is at most λ times the parent's value. Summed over depth j, this gives Σ_classes A^θ w ≤ (2λ)^j.

**Descent at the first crossing.** The quantity B/A grows by 1/(5A_old) at an A-step, by 1/A_old at an x+1 step, and by 0 at a halving. Take the first depth i at which A < 1/2. All earlier slopes are at least 1/2, so B_i/A_i ≤ 2i and B_i < i. For n ∈ [2^j, 2^{j+1}) with i ≤ j, this gives x < n/2 + j ≤ n. So a start in [2^j, 2^{j+1}) that never drops below itself has A ≥ 1/2 at depth j in its own class, and each class at depth j contains exactly one integer of that interval. Hence the number of such starts is at most

 2^{1/4}(2λ)^j / 0.783,

and summing over j ≤ log_2 X gives H(X) = O(X^{log_2 1.916}) ⊂ O(X^{0.9383}). The checker verifies 1.916^{10000} < 2^{9383} exactly. The exponent could drop to about 0.937 by optimising θ ≈ 0.27.

## How to verify

`python3 census/advance/split5_1-runs/check.py [BITS]` (default 42). It runs parts [2]–[5] in about 1 s with exact Fractions. It then compiles and runs `range.cpp`, which takes about 5 minutes on 12 cores. It exits 0 iff every part passes. With `SKIP_RANGE=1` it skips the C++ certificate. With a smaller BITS, the R and S bounds are recomputed for the weaker range, for example R = 19 at 2^40.

## Status summary

- Theorem A: PROVED, by a computer certificate with a written reduction.
- Theorem B part 1 (length): PROVED, elementary. The unconditional T-step bound is 6,432,164 (corrected in round 2).
- Theorem B part 2 (R = 23): PROVED, using Laurent 2008 (Acta Arith. 133) Cor. 2, consulted in the primary source.
- Theorem C: PROVED.
- The aim of R ≥ 100 was NOT reached. Section B.4 explains the obstruction.

## Referee (round 1)

**Verdict: correct with one mislabelled number (a gap).** Theorems A and C, and the K and L bounds of B1, are proved. B2 (R = 23) is correct as a derivation but stays CONDITIONAL on the LMN constant. The T-step count stated in B1 is **not** unconditional, as explained below.

**What I re-derived by hand.**
- (F1)–(F3). The telescoping identity A(x)/x = (5/2)g(x)/g(A(x)).
- The cycle identity δ = L log 2 − K log 5 = Σ[log g(x_i) − log g(y_i)] + Σ_B log(1+1/v), using L = K + Σe and T-steps = K + L + N_B.
- The bound 0 < δ < (5/6)r/m. The descent terms satisfy v ≥ 3B(v), so they give a geometric tail of at most 1/(2x_{i+1}).
- The recursion G_{i+1} ≤ G_i + (α−1)k_i − 1. This uses x_{i+1} ≤ (y_i+1)/4 even across several B-steps, and (3y+7)/4 ≤ (3y+1)/2 for y ≥ 2.
- The Stern–Brocot argument, including that a non-reduced L/K only strengthens K ≥ b+d.
- The CF lemma, including LQ ≠ KP because gcd(P,Q) = 1 and 0 < K < Q.
- The Baker-stage monotonicity: Lg ≥ 21 makes Lg/μ decreasing, and dLg/dμ < 1/μ.
- The U/O/E transitions. In O both children have odd y, and the mod-4 residues of b and b+a differ by 2.
- The B/A increments 0, 1/(5A) and 1/A. B/A starts at 0, so B ≥ 0. The bound x < n/2 + j ≤ n needs 2^j ≥ 2j, which holds for j ≥ 1. Each depth-j class meets [2^j, 2^{j+1}) exactly once.

**Computations.**
- I ran `check.py` 42. It exited 0 in 4m05s on 12 threads, with covered = 2^42−1, direct = 11,110,967,294 and R = 23. Of the direct checks, 11,110,967,292 are depth-cap leaves, so the certificate largely brute-forces about 1.1e10 unclosed classes. That is valid, but closure seldom happens.
- `referee_lazy.cpp` is my own certificate with a different design. It is a lazy-split tree that applies T only when the needed residue is constant on the class, and it splits only otherwise. At 42 bits its coverage is exactly 2^42−1, in 1m46s. Its direct-start count is 11,110,967,294, identical to the prover's. Build it with `g++ -O2 -fopenmp referee_lazy.cpp -o lazy` and run `./lazy 42`.
- `referee_brute.c` iterates every n < 2^32 directly until the value drops below n or reaches 1 or 13. All starts were resolved.
- `referee_B.py` (`uv run --with mpmath==1.3.0 python referee_B.py`, 400 digits) recomputes everything for B independently.
  - It checks δ and the bound (★) on C1 and C13. C13 has K=9, L=21, 4 runs, δ≈0.0711 < 0.2564.
  - It checks the run recursion on random odd x of up to 200 bits.
  - It gives K_min = 1,936,274 with the same neighbours, and L_min = 4,495,889.
  - R = 22 and R = 23 succeed and R = 24 fails, through its own μ_0 and convergent chain. For R = 23 the chain is 38095 → Q=23062019849360 → Q=24793177656, ending at m < 1.371e12.
- `referee_C.py` checks the three supermartingale inequalities: O 0.95793 ≤ 0.958, E 0.74966 ≤ 0.75011, U 0.92045. It finds log_2 1.916 = 0.93810. It also brute-forces the counts of non-dropping starts in [2^j, 2^{j+1}) for j ≤ 18. Every count is 0 or 1, well under the bound.

**LMN constant.**
- I could not obtain the original JNT 55 (1995) paper either. Web searches did not find a full text.
- I downloaded arXiv:2208.05752 myself (Tiebekabe–Adonsou–Diouf, Théorème 2.5, attributed to "[15], Corollary 2, pp. 288"). Its statement matches the prover's transcription: −24.34 d^4 max(log b'+0.14, 21/d, 1/2)^2 log B_1 log B_2, with log B_i ≥ max(h(α_i), |log α_i|/d, 1/d) and b' = |b_1|/(d log B_2) + |b_2|/(d log B_1).
- That quotation leaves out "algebraic" and "b_i integers". Both hold here: 2 and 5 are rational, and K, L ≥ 1.
- The choice of parameters is right: d = 1, log B for 2 is 1, log B for 5 is log 5, and b' = K + L/log 5 < 2.443K + 1.
- B2 is therefore still CONDITIONAL on a secondary-source transcription, which is exactly how the prover labelled it.

**Gaps.**
1. *(Mislabelled conditional, theorem.md "Theorem B" item 1 and check.py part4 `raw = Kmin + Lmin + (R+1)`.)* The claim of "at least 6,432,187 T-steps" uses N_B ≥ r ≥ R+1 = 24, which comes from the conditional B2. The unconditional count is K + L + N_B ≥ 1,936,274 + 4,495,889 + 1 = **6,432,164**. It would be one more if the one-run exclusion in census/lhf/mixed/CLS-048.md were itself unconditional. That exclusion also cites LMN, so 6,432,164 stands. Fix: state 6,432,164 unconditionally, and 6,432,187 only under the LMN condition.
2. *(Source, not a math error.)* The LMN constant was checked only against the same secondary quotation. Nobody has consulted the primary source.
3. *(Cosmetic.)* The overflow remark "b ≤ 2a, ratio never exceeds 2" is not proved in the text. It is not load-bearing, because step() throws above 2^124 and no throw occurred. Also, the brief's goal R ≥ 100 was not reached. Section B.4 explains this honestly.

No small-n failures and no off-by-one errors in the leaves were found. In the leaf range lim = ⌊(b−r)/(M−a)⌋+1, the b < r case returns before the unsigned subtraction. No decisions depend on floating point: all decisions in check.py are exact Fractions.

## Repair

These changes answer the round-1 referee report.

1. **Mislabelled T-step count (gap 1).** The referee's objection is correct. Theorem B.1 now states ≥ 6,432,164 T-steps unconditionally (K + L + N_B with N_B ≥ r ≥ 1). The figure 6,432,187 is stated only together with part 2 (r ≥ 24). In check.py, part [4] now prints both values and returns the unconditional one.
2. **Source of the two-log constant (gap 2).** Round 1 used the LMN 1995 constant, known only through a secondary quotation. The Baker stage now uses **M. Laurent, Acta Arith. 133.4 (2008), Corollary 2 with Table 1**, which I read in the publisher's PDF. The full statement and hypotheses are quoted in B.3. All hypotheses hold: 2 and 5 are multiplicatively independent, they and their logs are real and positive, K and L are positive integers, and D = 1. The checker hard-codes Table 1 and takes the best pair. The result is μ_0 = 28525 (pair m = 30, C_2 = 17.9), then convergent denominators Q = 23062019849360 and Q = 24793177656, ending at m < 1.371·10^12 < 2^42. So R = 23 is unchanged and R = 24 still fails. Theorem B.2 is no longer conditional.
3. **Overflow remark (gap 3).** Section A now proves the range bounds: a ∈ {1} ∪ {2·5^j}, the ratio b/a ≤ 2 by induction, and every node quantity is below 2^100. range.cpp is unchanged.
4. **R ≥ 100 not reached.** Not fixed. R = 23 stands, and B.4 still explains the obstruction.

Verification after repair: `python3 check.py` (42 bits). Its output is recorded below.

```
[2] step facts for odd x < 2*10^5; residue tree transitions verified on 32767 nodes (depth <= 14)
[3] with m >= 2^42: every further cycle has more than R = 23 expanding runs
    stages: ('Baker (Laurent 2008, m=30)', 28525) q=23062019849360 -> m<1.275e+15 q=24793177656 -> m<1.371e+12
[4] every further cycle has K >= 1,936,274 expanding (5n+1) steps, L >= 4,495,889 halvings, and >= 6,432,164 steps of T (>= 6,432,187 using r >= 24 from [3])
[5] supermartingale inequalities hold with theta=1/4, 2*lambda = 1.916 < 2^0.9383; H(X) <= C X^0.9383
[1] range certificate: bits=42 covered=4398046511103 nodes=24979688741 direct=11110967294 depth-cap leaves=11110967292 max extra steps=747 (122s)
ALL CHECKS PASSED
```

Wall time 2m03s on 12 threads, exit code 0.

## Referee (round 2)

**Verdict: confirmed.** All three round-1 gaps are closed, and I found no new gap. Theorems A, B1 (K ≥ 1,936,274, L ≥ 4,495,889, ≥ 6,432,164 T-steps), B2 (R = 23, so ≥ 6,432,187 T-steps), and C (H(X) = O(X^0.9383)) are proved as stated. The brief's goal R ≥ 100 is not met, and the theorem says so.

**Round-1 gaps.**
1. *T-step count.* Closed. Theorem B item 1 and check.py part [4] now give 6,432,164 = K + L + 1 unconditionally. The figure 6,432,187 appears only together with r ≥ 24. I re-derived T-steps = 2K + Σ(1+e) = K + L + N_B, with N_B ≥ r because every run ends at a value ≡ 3 (mod 4).
2. *Source of the two-log constant.* Closed. I downloaded the paper myself from the impan.pl link on the mathdoc landing page (https://www.impan.pl/shop/en/publication/transaction/download/product/82485?download.pdf, md5 da9f293b…). It is M. Laurent, "Linear forms in two logarithms and interpolation determinants II", Acta Arith. 133.4 (2008) 325–348. From the text:
   - **p. 326.** α_1, α_2 are non-zero algebraic numbers. Λ = b_2 log α_2 − b_1 log α_1, with b_1, b_2 positive integers. D = [Q(α_1,α_2):Q]/[R(α_1,α_2):R].
   - **p. 328.** b' = b_1/(D log A_2) + b_2/(D log A_1), where A_i > 1 and log A_i ≥ max{h(α_i), |log α_i|/D, 1/D}.
   - **Corollary 1.** α_1, α_2 are multiplicatively independent.
   - **Corollary 2.** If moreover α_1, α_2, log α_1, log α_2 are real and positive, then log|Λ| ≥ −C_2 D^4 (max{log b' + 0.38, m/D, 1})^2 log A_1 log A_2.
   - **Table 1.** C_2 = 25.2, 23.4, 22.1, 21.1, 20.3, 19.7, 19.2, 18.8, 18.4, 18.1, 17.9 for m = 10, …, 30. This is exactly LAURENT_TABLE in check.py.

   The prover's application is correct. α_1 = 5 with b_1 = K and log A_1 = log 5 ≥ max(log 5, log 5, 1). α_2 = 2 with b_2 = L and log A_2 = 1 ≥ max(log 2, log 2, 1). D = 1 and Λ = δ > 0. The numbers are multiplicatively independent, and K, L ≥ 1. The bound b' = K + L/log 5 < (1 + 1/log 2)K + 1 holds, using L < Kα + δ/log 2 and δ < 1.
3. *Overflow remark.* Closed. The proof that a ∈ {1} ∪ {2·5^j : j ≤ d−1} and that ρ = b/a ≤ 2 (child ratio ≤ (ρ+1)/2 + 1/(2a) ≤ ρ/2 + 1) is correct. LIMIT in range.cpp is (2^128−1)/8 ≈ 2^125, which matches the text, and 5·LIMIT+1 < 2^128.

**What I re-derived by hand.**
- The product identity over the cycle, which gives δ = L log 2 − K log 5 > 0.
- The bound (★) δ < 5r/(6m): 1/(3m) from log g(x_i), plus the geometric tail 1/(2m) from v ≥ 3B(v).
- G_{i+1} ≤ G_i + (α−1)k_i − 1 < αG_i, and K ≤ G_1(α^r−1)/(α−1) with G_1 ≤ log_2(2m).
- The Baker-stage monotonicity. Lg ≥ 30 makes Lg/μ decreasing. The check at μ_0 uses upper bounds, so it carries over to the true F on [μ_0, ∞).
- The CF lemma, including that the |α − P/Q| < 1/Q² test at both enclosure endpoints covers the whole interval by convexity.
- The Stern–Brocot step, including Lmin = ⌊K_min·α_lo⌋ + 1 ≤ ⌊K_min α⌋ + 1, which is a valid but weaker bound.

No decision in check.py depends on floating point.

**Computations.**
- I ran `python3 check.py` (42 bits). It exited 0 in 1m58s with covered = 2^42−1, direct = 11,110,967,294 and R = 23.
- `ref2_B.py` is my own code. Run it with `uv run --with mpmath==1.3.0 python ref2_B.py`. It uses mpmath interval arithmetic at 300 digits and exact Fractions for the CF and Stern–Brocot steps. It applies Laurent Table 1 directly:
  - R = 23 gives μ_0 = 28975 from a coarser scan, then Q = 23062019849360 → m < 1.275e15, then Q = 24793177656 → m < 1.371e12 < 2^42.
  - R = 24 fails, stalling at Q = 149338067129 with m < 8.6e12.
  - K_min = 1,936,274 with neighbours 4268621/1838395 and 227268/97879. L_min = 4,495,889 and the T-step bound is 6,432,164. All match the prover.
- `ref2_brute.c` is my own code. It iterates every n < 2^31 directly, plus 10^7 random n in [2^31, 2^42). All of them drop below the start or reach 1 or 13. The random samples are only a sanity check, not a certificate.
- I re-ran the round-1 independent certificate `referee_lazy.cpp` at 42 bits: coverage_ok = 1, direct = 11,110,967,294, in 1m38s.

**Remaining remarks (not gaps).**
- The certificate for (A) closes few classes. About 1.1e10 depth-cap classes are brute-forced. This is valid.
- The goal R ≥ 100 is not reached. B.4 explains the exponential run recursion with base log_2 5, which is the honest limit of this method.
