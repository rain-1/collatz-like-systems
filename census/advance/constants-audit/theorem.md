# constants-audit: replacing the linear-forms constants quoted from memory

**Status: PROVED.** Every result listed below now depends only on one transcendence bound: Laurent (2008), Corollary 2. I read that statement in the primary source. The rest is the proofs already in the census plus finite exact scans.

| Result | Constant used before | Verdict | New cutoff | Scan now covers |
|---|---|---|---|---|
| CLS-048 (split5_1, one-run) | LMN 1995 Cor. 2, k0 = 25000 | **VERIFIED** | k < 5868 | Y ≤ 5867 (old Y ≤ 24999 also suffices) |
| CLS-051 (m3_4n5, one-run) | LMN, k0 = 10800 | **VERIFIED** | k < 2715 | L ≤ 14001 |
| CLS-052 (s32_plus9, one-run) | LMN, k0 = 17100 | **VERIFIED** | k < 4774 | J ≤ 15389 |
| CLS-053 (split7_1, one-run) | LMN, k0 = 15100 | **VERIFIED** | k < 4739 | J ≤ 29904 |
| collatz3 Theorem 1C (CLS-011..018, 031; d ∈ {±1,3,5,7,9,13,17}) | Ellison (E) "K ≤ 27" / Rhin (R) "k ≤ 104", scan k ≤ 1000 | **CORRECTED** | k ≤ 4000 | scan extended to k ≤ 4001; same cycle lists |
| steiner_1cycle | Rhin H^-13.3, cutoff k ≤ 103 | **VERIFIED** (old scan k ≤ 10^4 is already enough) | k < 3997 | k < 3997 |
| perm1932_1cycle | Rhin H^-13.3, cutoff l ≤ 118, scan l ≤ 600 | **CORRECTED** | l < 4714 | scan extended to l < 4714; same 5 pairs, same 2 cycles |

"VERIFIED" means the old cutoff and scan remain valid once the consulted bound is used. In fact the consulted bound gives a smaller cutoff. "CORRECTED" means the consulted bound gives a larger cutoff than the old scan reached, so the scan was extended. No conclusion changed.

## 1. The consulted bound

**Source (read, primary).** M. Laurent, *Linear forms in two logarithms and interpolation determinants II*, Acta Arith. 133 (2008), 325–348, DOI 10.4064/aa133-4-3. I read pp. 325–328 of the IMPAN PDF. The statement is copied from there.

*Setting.* α1 and α2 are non-zero algebraic numbers, and Λ = b2 log α2 − b1 log α1 with b1, b2 positive integers. The paper assumes |α1|, |α2| ≥ 1 and sets D = [Q(α1,α2):Q]/[R(α1,α2):R]. It also sets

  b' = b1/(D log A2) + b2/(D log A1),

where A1, A2 > 1 are real numbers such that log Ai ≥ max{h(αi), |log αi|/D, 1/D}.

*Table 1 (C2 row).* m = 10, 12, …, 30 gives C2 = 25.2, 23.4, 22.1, 21.1, 20.3, 19.7, 19.2, 18.8, 18.4, 18.1, 17.9.

*Corollary 1* assumes that α1 and α2 are multiplicatively independent. *Corollary 2* adds "Suppose moreover that the numbers α1, α2, log α1, log α2 are real and positive." Its conclusion is

  log|Λ| ≥ −C2 D^4 (max{log b' + 0.38, m/D, 1})^2 log A1 log A2

for each pair (m, C2(m)) in Table 1.

*How I apply it.* I always take α1 = 2 and α2 = p, an odd prime (p = 3, 5 or 7). These are multiplicatively independent, real, and greater than 1, and their logarithms are positive. Then D = 1. h(2) = log 2 < 1, so log A1 = 1. Since log p ≥ 1, log A2 = log p. So b' = b1/log p + b2, where b1 is the exponent of 2 and b2 the exponent of p, both positive. This gives

  (L)  log|Λ| ≥ −C2 · max(log b' + 0.38, m)^2 · log p.

The check tries every m in Table 1 and keeps the smallest cutoff. In every case except CLS-053 that is m = 10 (C2 = 25.2); CLS-053 uses m = 12 (C2 = 23.4).

**Status of the constants quoted before.**
- *LMN 1995 Cor. 2* (log|Λ| ≥ −24.34 D^4 max(log b' + 0.14, 21/D, 1/2)^2 log A1 log A2). I could not get the primary source (J. Number Theory 55 (1995) 285–321). I did read a secondary quotation of it: arXiv:2208.05752, Théorème 2.5, which cites "[15], Corollary 2, p. 288". It has the same constant, the same max and the same b' convention as the census. The census results no longer need it, because (L) is stronger in this range and gives smaller cutoffs.
- *Ellison 1971 (E)* and *Rhin 1987 (R)*. Not consulted, and still unverified. I found no online copy. CLS-015's referee also notes that the H^(−13.3) form of (R) may be inexact: Simons–de Weger quote exp(−13.3(0.46057 + log H)). Neither is used any more.

## 2. An elementary lemma used three times

For x ∈ [0, 1] we have 1 − e^(−x) ≥ x − x²/2 ≥ x/2. Let A, B > 0 and Λ = log A − log B. Then |A − B| = max(A,B)(1 − e^(−|Λ|)). So either |Λ| ≥ 1 and |A − B| ≥ (1 − 1/e) max(A,B) > max(A,B)/2, or |Λ| < 1 and |A − B| ≥ max(A,B)|Λ|/2.

## 3. Cutoff method (same for all seven results)

Each census proof already gives an upper bound log|Λ| < U(k), where U is affine in k minus at most a log term. It also gives an affine bound b' ≤ a1 k + a0. Define

  G(k) = −U(k) − C2 · max(log(a1 k + a0) + 0.38, m)^2 · log p.

If G(k) > 0, (L) contradicts the upper bound, so no solution has that k. Let s be the slope of −U. G is piecewise differentiable, and on [k, ∞)

  G' ≥ s − [1/k] − 2 C2 log p · max(log(a1 k + a0) + 0.38, m)/k =: dG(k).

The bracketed term appears only in the one-run case. There −U contains −log(c1 k + c0), and c1/(c1 k + c0) ≤ 1/k. I also used a1/(a1 k + a0) ≤ 1/k, and the max-term has derivative 0 or 2u·u'. dG is nondecreasing: (log x + 0.38)/k decreases once a1 k + a0 > e^0.62, and m/k and 1/k decrease. So dG(k0) > 0 implies G is increasing on [k0, ∞). The check finds the least k0 with G(k0) ≥ 1 and dG(k0) ≥ 10^−4. It uses 60-digit `decimal` logs, so rounding is below 10^−50, far smaller than the margins. **So every solution has k < k0.**

## 4. The seven applications

**(c1) Steiner 1-cycles** (round2/literature/steiner_1cycle.md). The note proves 0 < Λ = (k+l) log 2 − k log 3 < 2^(1−k) and l ≤ k. Here b1 = k + l, b2 = k and p = 3, so b' ≤ k(2/log 3 + 1). With U = (1−k) log 2 this gives k0 = 3997 (m = 10). The note's exact scan, k ≤ 10^4 with l forced to be minimal, already covers this, and check.py repeats it for k < 3997: only (1,1). **VERIFIED.**

**(c2) perm1932 1-cycles** (round2/literature/perm1932_1cycle.md). For l ≥ 2 the note proves |Λ| < 2^(1−l), with Λ = (2k+l) log 2 − (k+l) log 3 and k ≤ 2l + 3. Its derivation uses the lemma of §2 with A = 3^(k+l) and B = 2^(2k+l). Here b1 = 2k + l and b2 = k + l, so b' ≤ (5l+6)/log 3 + 3l + 3. This gives **l0 = 4714**, far above the old 118, and the old scan stopped at l ≤ 600. So the scan is extended to l < 4714.

The scan is exact. For l ≤ 600 it tests every k ≤ 2l + 3. For l > 600 it uses R(k) = 3^(k+l)/2^(2k+l), which is strictly decreasing in k. Dividing |D| < 4^k by 4^k 2^l gives |R(k) − 1| < 2^(−l), which holds on an interval of k. The scan pins the left end ka exactly with integer comparisons, checking both up(ka) and ¬up(ka − 1). It then walks k upward while R(k) > 1 − 2^(−l), and tests |D| ≤ 4^k − 3^k exactly.

The candidate pairs are still exactly (1,1), (2,1), (3,2), (4,3) and (7,5). The note's e-enumeration plus simulation again gives only the cycles (2,3) and (4,5,7,9,6). **CORRECTED; conclusion unchanged.**

**(b) collatz3 Theorem 1C** (lhf/collatz3/CLS-011..018, 031). Part (ii) of the theorem proves 0 < |D| = |2^K − 3^k| ≤ |d|(2^l − 1) < |d| 2^l and K < k log2 3 + log2(|d| + 1). Apply §2 with A = 2^K:
- If |Λ| ≥ 1, then 2^K/2 < |d| 2^l, so 2^k < 2|d| ≤ 34 and k ≤ 5.
- Otherwise |Λ| < 2|d| 2^(−k) ≤ 34 · 2^(−k).

Here b1 = K, b2 = k and p = 3, so b' ≤ k(1/log 2 + 1) + log2(18)/log 3. This gives **k0 = 4001**, uniformly for |d| ≤ 17.

The old argument stopped at k ≤ 1000, which was enough only under the unverified (E)/(R). So the scan is extended to k ≤ 4001 for d ∈ {1, −1, 3, 5, 7, 9, 13, 17}. The scan is exact and uses only the proved condition 3^k/2^l ∈ (2^k − |d|, 2^k + |d|), which defines an interval of l found by integer comparisons. When 2^k ≤ |d| it falls back to l ≤ 4k + 8 + 2·bitlen|d|. That covers the proved bound K < k log2 3 + log2(|d| + 1) for d > 0, and K < k log2 3 for d < 0. Every solution is simulated. The lists are exactly the census lists:
- d=1: (1,1,1)
- d=−1: (1,0,1), (2,1,5)
- d=3: (1,1,3)
- d=5: (1,1,5), (1,2,1), (3,2,19)
- d=7: (1,1,7), (2,2,5)
- d=9: (1,1,9)
- d=13: (1,1,13), (1,3,1), (5,3,211)
- d=17: (1,1,17)

**CORRECTED: Theorem 1C is now unconditional.** The "conditional on (E)/(R)" in CLS-011..018 and 031 can be dropped.

**(a) One-run theorems CLS-048, 051, 052, 053** (lhf/mixed, onerun_lib.py). The notes prove 0 < Λ = X log P − Y log Q ≤ (c1 k + c0)/n0, n0 ≥ low(k), and Y ≤ c_hi k + c_hi0. They also give X ≤ Y log Q/log P + 1, which holds because Λ < log 2 for k ≥ k0. This is implied by G(k0) > 0, since that makes (c1 k + c0)/low(k) < e^(−2000).

Hence b' = e2/log p + ep. When P = 2 it is at most (1/log 2 + 1)(c_hi k + c_hi0) + 1/log p. When Q = 2 (CLS-051) it is at most (1 + log 2)/log p · (c_hi k + c_hi0) + 1.

For the slope of −U I use explicit lower bounds valid for k ≥ 3 (also spot-checked):
- floor((2^(k+1) − 1)/3) ≥ 2^(k+1)/6
- 3^k − 5 ≥ 3^k/2
- 2^(k+1) − 1 ≥ 2^k
- floor((2^(2k+1) − 1)/3) ≥ 4^k/3

The new cutoffs are 5868, 2715, 4774 and 4739, all below the census k0 = 25000, 10800, 17100 and 15100. The finite part (`onerun_lib.finite_part`, refereed, imported read-only) and the direct search were re-run with the new Ymax. Their survivor sets and n0 bounds are the census ones, and the one-run minima are again [(1,1)], [(16,1)], [] and []. **VERIFIED.** The census numbers F(k0) were computed with the LMN quote, which matches a secondary source. They are now unnecessary, because (L) from the primary source gives smaller cutoffs.

## 5. What is conditional

Nothing beyond Laurent 2008 Cor. 2, which I read in the primary source. The non-transcendence steps are the existing census proofs: the cycle equations, the bounds on b', the descent bounds and the finite-part logic of onerun_lib. Census referees confirmed them. I re-derived the inequalities quoted in §4 but did not re-referee those notes in full.

Literature I did not verify: LMN 1995 (secondary quote only), Ellison 1971 and Rhin 1987. None of them is used any more.

## 6. How to verify

`python3 census/advance/constants-audit/check.py` runs in about 2.5 s and exits 0 iff all of the following pass:
- the cutoff searches (all m in Table 1);
- the Steiner scan;
- the extended perm1932 scan with e-enumeration;
- the extended collatz3 scan for the 8 values of d, with simulation;
- the four one-run finite parts and direct searches.

## Referee (round 1)

**Verdict: CONFIRMED.** All seven verdicts (VERIFIED / CORRECTED) and all cutoffs stand. I found no mathematical gap. There are only presentation nits, listed below.

**Source check (done myself).** I downloaded the IMPAN PDF myself and read pp. 325–328: M. Laurent, *Linear forms in two logarithms and interpolation determinants II*, Acta Arith. 133.4 (2008) 325–348. The source agrees with the quotation in §1 on every point:
- The setting: Λ = b2 log α2 − b1 log α1 with b1, b2 positive integers, |α_i| ≥ 1 without loss of generality, and D = [Q(α1,α2):Q]/[R(α1,α2):R].
- The definition b' = b1/(D log A2) + b2/(D log A1), where A_i > 1 and log A_i ≥ max{h(α_i), |log α_i|/D, 1/D}.
- Table 1, C2 row: m = 10..30 gives 25.2, 23.4, 22.1, 21.1, 20.3, 19.7, 19.2, 18.8, 18.4, 18.1, 17.9.
- Corollary 1 assumes multiplicative independence. Corollary 2 adds "Suppose moreover that the numbers α1, α2, log α1, log α2 are real and positive" and concludes log|Λ| ≥ −C2 D^4 (max{log b' + 0.38, m/D, 1})^2 log A1 log A2.

The hypotheses hold in every application:
- α1 = 2 and α2 = p ∈ {3, 5, 7} are multiplicatively independent, real, and greater than 1.
- D = 1. log A1 = max(log 2, log 2, 1) = 1 and log A2 = log p ≥ 1.
- b1 is always the exponent of 2 and b2 the exponent of p, and both are ≥ 1 in the ranges where the bound is applied.

**Re-derived by hand.**
1. Steiner. I re-derived 0 < Λ < 2^(1−k), l ≤ k (including k = 1, 2), b' = (k+l)/log 3 + k ≤ k(2/log 3 + 1), and that only the least l can work.
2. perm1932. I re-derived the k-range k log(4/3) < l log(3/2) + log 2, so k ≤ 2l + 3. For l ≥ 2, min(|Λ|, 1) < 2^(1−l) gives |Λ| < 2^(1−l). I also checked b' = (2k+l)/log 3 + (k+l).
3. collatz3.
   - From (ii), 2^K min(|Λ|,1)/2 ≤ |D| < |d| 2^l. So either k ≤ 5 or |Λ| < 34·2^(−k).
   - b' = K/log 3 + k, with K < k log2 3 + log2 18 for d > 0 and K < k log2 3 for d < 0.
   - The case l = 0 is separate and correctly handled.
4. One-run results.
   - The b' bounds in both orientations: P = 2 for CLS-048/052/053 and Q = 2 for CLS-051, with b1 always the exponent of 2.
   - X ≤ Y log Q/log P + 1 needs Λ < log P. This is not circular: the upper bound Λ ≤ (c1 k + c0)/low(k) is proved without b', and G(k) > 0 forces it below e^(−2500).
   - The integer forms of low(k) ≥ exp(αk + β) for k ≥ 3.
   - The derivative bound. c0, a0 ≥ 0 give c1/(c1k+c0) ≤ 1/k and a1/(a1k+a0) ≤ 1/k. (log x + 0.38)/k decreases once log x + 0.38 ≥ 1, so dG is nondecreasing.
   - The binary search in check.py only needs some k0 that satisfies the test, and it asserts the test at the k0 it returns. Its minimality does not matter for soundness.

**Independent computation.** I wrote `referee_check.py` in this folder. It is my own code and imports neither check.py nor onerun_lib. It exits 0 in about 12 s.
- **Cutoffs.** Every cutoff was re-verified with my own G and derivative bound, using 50-digit Decimal and the C2 values entered as exact decimal strings: 3997, 4714, 4001, 5868, 2715, 4774 and 4739, with m = 12 for CLS-053.
- **Steiner.** Scanned every k < 3997 with a window of l around the forced value.
- **perm1932.** Scanned every l < 4714 and k ≤ 3l + 10 (wider than 2l + 3), filtered by an exact bit-length argument: |D| < 4^k requires bitlen(3^(k+l)) ∈ {2k+l, 2k+l+1}. The candidates are the same 5 pairs, and direct iteration of g from 2^l e finds the same 2 cycles.
- **collatz3.** Scanned every k ≤ 4001 and K in [bitlen(3^k) − 7, bitlen(3^k) + 6]. That window contains the range [B−5, B+4] that the proved bounds allow for |d| ≤ 17. Each solution was checked by simulating the parity vector. The lists are identical for all 8 values of d.
- **One-run finite parts.** I redid them by testing every admissible k, not just kmin and kmin+1, with an exact early exit justified by low(k+1) ≥ 2 low(k) and B(k+1) < 2B(k). The survivor counts are the same: 6, 26, 14 and 20. My n0 bounds are 213, 1849, 582 and 5500. A direct one-run search built from the T maps themselves, not from the prover's S, finds minima [1], [16], [] and [], matching the claims.

**Gaps / nits (none affects validity).**
1. *Labelling.* For perm1932 and collatz3, "CORRECTED" means "the old proof was conditional on an unverified constant; the scan is now extended to the cutoff the verified bound allows". It does not mean the old proof was shown wrong: under Rhin as quoted, l ≤ 118 and k ≤ 104 would still follow. The table wording "old scan too short" should be read in that sense.
2. *The census notes are not updated.* lhf/collatz3/CLS-0xx.md still says "conditional on (E)/(R)". lhf/mixed/*.md and the onerun_lib docstring still cite LMN 1995 with its F(k0) values. A pointer to this audit should be added there, which is outside this folder's write scope.
3. *Runtime claim.* theorem.md §6 says about 2.5 s. I measured 12.4 s wall time (3.9 s user) for check.py. This is well under the limit.
4. *Inherited steps.* The non-transcendence steps (1)–(3) of the one-run notes and (i)–(ii) of Theorem 1C are inherited from the census proofs and their earlier referees. I re-derived the inequalities this audit uses, but did not re-referee the step-fact lemmas beyond what the earlier referees confirmed. The direct searches above independently confirm the small cases.
5. *Literature not consulted.* LMN 1995, Ellison 1971 and Rhin 1987 remain unconsulted in primary form. The audit correctly no longer uses them.
