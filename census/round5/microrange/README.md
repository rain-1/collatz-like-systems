# Round 5, lens "microrange": a rigorous step beyond the horizon in this census (27 Nov 2026)

Status: agent-written; refereed once (REFEREE1.md: mathematics confirmed, textual repairs requested), and revised after it (section 9); refereed a second time (REFEREE2.md: all proofs confirmed, wording fixes and one strengthening recommended), and revised after it (section 10). The title is scoped to this census: no literature search was done. Every claim is labelled PROVED / EVIDENCE / OPEN.
System: 3x+1 (Terras map), counting by the coefficient stopping time. Theorems R, D and D' hold
for every 3x+d with d odd; the numbers of C hold verbatim only for 3x-1 (section 6). split5_3 and K7 were not done (section 8).

## Results

| # | statement | status | check |
|---|---|---|---|
| R | **Reduction, uniform in the intercept.** For all m, j and every split depth j' with j <= j' <= m, the count N(2^m, m+j) lies in an interval [L, U]. L and U depend only on in-horizon data: the residues mod 2^{m-j'} and how many odd steps each has. No information about the integers' digits beyond the horizon is used. | PROVED | `check_exact.py` |
| C | **Certified instances.** For m = 100, 1000, 3000 and every j in 1..12 (j in {1,2,3,4,6,8,10,12} in `data/certified.txt`, j in {5,7,9,11} added after REFEREE1 in `data/certified_odd.txt`), and for every m in [35, 1000] with j = 4: N(2^m, m+j) = 2^m P(m+j)(1 + δ), with |δ| certified at most 3.2·10^-5 (j = 1; exact values 0, 3.18·10^-5, 1.83·10^-5 at m = 100, 1000, 3000) up to 0.0193 (j = 12), and at most 0.0062 for every m in [35,1000] at j = 4. The in-horizon sandwich only gives δ in about [-0.97, +0.69] at j = 12 and m = 100. | PROVED (exact integer computation) | `certify.py` |
| F | **Averaged discrepancy lemma.** For u uniform on a coset of <3> in (Z/2^K)^*, E_u max_B \|Φ(u,B) - Φ̄\| <= g_K sqrt(\|S\|(1 - \|S\|/2^K)), with g_K = 4(1 + 0.3466(K-1)). This holds for every set S. | PROVED; also checked exactly in 432 cases | `analytic.py` |
| P, M | Every threshold pattern that occurs has \|S\| >= #surv(K). #surv is supermultiplicative, and log2 #surv(K) >= (K - 2000) h0 for every K, with h0 = log2 #surv(2000)/2000 >= 0.9430. | PROVED | `analytic.py` |
| D | **Almost every octave, log log X digits beyond the horizon (τ-version, X = 2^m).** Fix η in (0, 3]. For large M, all but at most M^{1-η/3} of the m in [M, 2M) satisfy \|N(2^m, b) - 2^m P(b)\| <= 2 m^{-η/3} 2^m P(b) for every b with m < b <= m + (h0/2 - η) log2 m. Here h0 >= 0.9430 is the proved constant (not H(λ) = 0.94996), so h0/2 >= 0.4715. This is for the coefficient stopping time τ and for X a power of 2 only; it is not Conjecture E as stated (σ, all X). | PROVED | constants in `analytic.py` |
| D' | Explicit densities at K = 16 (Weyl). For example, the m with \|N(2^m, m+1)/2^mP(m+1) - 1\| > 0.05 have upper density <= 0.002, and for j = 2 and error 0.1 the bound is 0.002. | PROVED (exact computation + Weyl) | `analytic.py` |
| G | R, D and D' hold for 3x+d for every odd d (positive or negative); D' by the reflection identity of section 6. C holds verbatim for 3x-1 (the certificate equals that of 3x+1 exactly). For other d the method of C applies with the multiplier 3^A d^{-1}, and the numbers differ: they were computed after REFEREE1 only at m = 1000, j <= 8, K = 24 for d = 5, -3, 7 (`data/certified_siblings.txt`). The finitely many extra cycles of 3x-1 and 3x+5 do not affect any of this. *(Corrected after REFEREE1: the original row said "R, C, D and D' hold verbatim", which was wrong for C when d ≠ ±1.)* | PROVED | `check_exact.py` (3x-1, 3x+5 against brute force); `certify.py siblings` |
| O1 | **Why route (i) fails.** Only the multipliers 3^A with A in a window of about 0.63K consecutive integers matter: A is tied to the slope, and survivors sit near the critical slope. So "A is equidistributed mod 2^{2j-2} among survivors" (a local limit theorem) is false in the sense needed. | PROVED (one line, section 5) | |
| O2' | **All m, a fixed bound (added after REFEREE2, N2).** For every m >= 17 - j: \|N(2^m, m+j)/2^mP(m+j) - 1\| <= 129/1057 = 0.1221 (j = 1), 213/749 = 0.2844 (j = 2), 349/749 = 0.4660 (j = 3). Derivation in section 5. The bound does not tend to 0 | PROVED (Theorem R + Lemma P + exact computation at K = 16) | `allm_bound.py` |
| O2 | **All m, with error tending to 0:** OPEN. Bad multipliers exist (u near 3^{-i} 2-adically, for small i). An m whose window hits one gets only a weaker bound. There is no theorem saying that the windows of all large m avoid them. | OPEN; the bad multipliers are EVIDENCE | section 5 |
| σ | For 3x+1 (and 3x+d with d > 0) the lower bounds carry over to the integer stopping time σ, because σ >= τ. Not claimed for d < 0 (the proof uses c_i >= 0). For 1 <= n < 2^34 and m <= b <= m+8, the counts for σ and τ differ by exactly 1 (n = 1), except at m = b = 1 where they agree (with n = 0 counted, as in section 2, the difference is one larger, since σ(0) = ∞ and τ(0) = 1). | lower bound PROVED; upper bound EVIDENCE | brute force |
| LB | I know of no explicit family that beats σ(n) >= (log2 3 - o(1)) log2 n, the trivial family 2^k - 1 (a statement from memory; no literature search was done). D controls only O(log m) further digits, so it cannot change the constant. | OPEN (nothing new) | |

What is genuinely beyond the horizon. N(2^m, m+j) is decided by the parities of T^{m+1}(n), ..., T^{m+j}(n) for n < 2^m. These are not functions of n mod 2^m. Every earlier density result in the census (round 3 `density`, round 4 `lundberg` Corollary 2) stops at depth m. The concurrent round-5 lens `census/round5/fourier` (Theorems U and U') also proves an all-depth bound 1 to 3 digits past the horizon; its exact constants for 3x+1 coincide with the all-m bound O2' here (see section 10). Here they are controlled (τ-version, X = 2^m) for j up to (h0/2 - η) log2 m in almost every octave, and for every j <= 12 at the certified m. This is a real extension, but a small one: Conjecture E needs j up to a constant multiple of m.

## 1. Setting and notation

T(x) = x/2 for x even and (3x+1)/2 for x odd. A_i(n) is the number of odd values among n, T(n), ..., T^{i-1}(n). λ = log_3 2. amin(b) = ceil(bλ) is the least a with 3^a >= 2^b (bλ is irrational for b >= 1).

* F(n, b) = [A_i(n) >= amin(i) for 1 <= i <= b]. Equivalently, 3^{A_i}/2^i >= 1 at every step i <= b: n has not dropped in the coefficient sense within b steps. τ(n) = min{i : 3^{A_i} < 2^i} is the coefficient stopping time (Terras), and F(n,b) <=> τ(n) > b.
* N(m, b) = #{0 <= n < 2^m : F(n,b)}. #surv(b) = #{r mod 2^b : F(r,b)}, and P(b) = 2^{-b} #surv(b) is the Haar measure.
* Terras' identity (PROVED by induction on d, checked in `check_exact.py` part 2): n and n + 2^d s have the same first d parities, and T^d(r + 2^d s) = 3^{A_d(r)} s + T^d(r). Residues mod 2^d correspond bijectively to parity words of length d.
* In-horizon identity: N(m, b) = 2^{m-b} #surv(b) = 2^m P(b) for b <= m.
* Horizon: for b > m, F(n, b) depends on more of n's orbit than n mod 2^m fixes. N(m, m+j) is the object of Conjecture E. Conjecture E is phrased with σ; section 7 explains the relation.
* Cnt_d(A) = #{r mod 2^d : F(r,d), A_d(r) = A}, computed exactly by lattice-path dynamic programming (`microlib.cnt`).

Relation to 3x+1. Even "τ(n) <= C log n for all large n" would imply the Collatz conjecture (not immediately: τ(n) = i gives T^i(n) < n only via a Baker-type lower bound on 2^i - 3^{A_i}; this is unlabelled context, not used anywhere, and not proved here). Nothing here bounds τ(n) for an individual n. All statements are counts with relative errors, and they are consistent with any finite or density-zero set of exceptional n.

## 2. Theorem R (the reduction), PROVED

Fix m, j >= 1, j' with j <= j' <= m. Put d = m - j' and K = j + j'. For a depth-d survivor with A odd steps, set th_i = amin(d+i) - A for i = 1..K, and

    S = S_{d,A} = { x mod 2^K : A_i(x) >= th_i for i = 1..K }   (in-horizon: depends only on (d, A)),
    Φ(u, B) = #{ 0 <= s < 2^{j'} : (u s + B) mod 2^K ∈ S },   Φ̄ = 2^{j'} |S| / 2^K.

**Theorem R.**

    Σ_A Cnt_d(A) min_B Φ(3^A, B)  <=  N(m, m+j)  <=  Σ_A Cnt_d(A) max_B Φ(3^A, B),
    2^m P(m+j) = Σ_A Cnt_d(A) Φ̄,

where the min and max run over all B in Z/2^K, and 3^A is read mod 2^K. Consequently
|N(m,m+j) - 2^mP(m+j)| <= max_A r_A · 2^m P(m+j), with r_A = max_B |Φ(3^A,B) - Φ̄| / Φ̄, the maximum
taken over the A whose S is not all of Z/2^K.

*Proof.* (n = 0 is counted in N here but not by `brute`; this is harmless because 0 never survives step 1.) Write n < 2^m as n = r + 2^d s with r < 2^d and s < 2^{j'}. The first d steps of n are those of r, so F(n, m+j) requires F(r, d). Given that, put A = A_d(r) and x = T^d(n) = 3^A s + B_r with B_r = T^d(r). Then A_{d+i}(n) = A + A_i(x), so F(n, m+j) holds iff A_i(x) >= amin(d+i) - A for i <= K, i.e. iff x mod 2^K ∈ S_{d,A}. The parities of x for K steps depend only on x mod 2^K = (3^A s + B_r) mod 2^K. So the number of good s is exactly Φ(3^A mod 2^K, B_r mod 2^K). This lies between the min and the max over all B. Summing over r gives the two inequalities.

For the identity, replace s < 2^{j'} by s < 2^K. Then s ↦ 3^A s + B_r mod 2^K is a bijection, so the count becomes |S|. Summing over r gives #surv(m+j) = 2^{m+j} P(m+j) = Σ_r |S|. Dividing by 2^j gives 2^m P(m+j) = Σ_r Φ̄.

For the last line: the A with S = Z/2^K have Φ = Φ̄ = 2^{j'} for every B. For the rest, |Φ - Φ̄| <= r_A Φ̄, and Σ_r Φ̄ = 2^m P(m+j). ∎

Why this is not circular. The intercept B_r = T^d(r) is an integer whose low bits are exactly the beyond-horizon information we do not have. Routes that condition on B, or ask A to be independent of B's middle bits, need that information. Theorem R needs nothing about B: it asks that the line {3^A s + B : s < 2^{j'}} meet the in-horizon set S in the Haar proportion for every B. That is a finite statement about the multiplier 3^A mod 2^K and the set S. The top j' digits s of n carry j' bits. The theorem shows that, after multiplication by 3^A, they control j' + j digits of the continuation well enough for counting. This is the "middle digits of 5^A s + B" of CONJECTURE.md, made uniform in B.

Exact check (`check_exact.py`, exits 0; about 2 s). The checks compare Theorem R with brute-force counts: for 3x+1 every m in [16, 34], and for 3x-1 and 3x+5 every m in [16, 32], always with j = 1..8 and four split depths (1369 cases). In every case L <= N <= U, and Σ Cnt Φ̄ equals 2^m P(m+j) computed independently. The fast discrepancy code (digit-tree construction plus sliding window) is checked against the naive definition. At the median, the certified interval is 13 times narrower than the in-horizon sandwich.

## 3. Theorem C (certified instances), PROVED by exact computation

`certify.py` evaluates Theorem R in exact integer arithmetic. It uses Python big integers for Cnt_d and C for max_B and min_B over all 2^K intercepts. Output: `data/certified.txt`. "rel" is (bound - 2^mP(m+j))/2^mP(m+j). The in-horizon sandwich is [#{depth-m survivors whose level is so high that no continuation can die within j steps}, N(m,m)].

```
Table 1. Theorem R bounds, K = j + jp = 28. rel = (bound - 2^m P(m+j)) / 2^m P(m+j).
    m   j  jp    rel_lower    rel_upper     triv_lower   triv_upper   P(m+j)/P(m)
  100   1  27     +0.00000     +0.00000        +0.0000      +0.0000   1.0000
  100   2  26     -0.00050     +0.00067        -0.1957      +0.0652   0.9387
  100   3  25     -0.00054     +0.00075        -0.1957      +0.0652   0.9387
  100   4  24     -0.00145     +0.00138        -0.4412      +0.1210   0.8921
  100   6  22     -0.00360     +0.00267        -0.6335      +0.2262   0.8155
  100   8  20     -0.00759     +0.00625        -0.8772      +0.4331   0.6978
  100  10  18     -0.01083     +0.01048        -0.9366      +0.5240   0.6562
  100  12  16     -0.01923     +0.01878        -0.9679      +0.6875   0.5926
 1000   1  27     -0.00003     +0.00003        -0.0409      +0.0409   0.9607
 1000   2  26     -0.00007     +0.00007        -0.1752      +0.1169   0.8953
 1000   3  25     -0.00011     +0.00011        -0.1752      +0.1169   0.8953
 1000   4  24     -0.00020     +0.00020        -0.3667      +0.1693   0.8552
 1000   6  22     -0.00054     +0.00054        -0.5236      +0.2626   0.7920
 1000   8  20     -0.00116     +0.00121        -0.6640      +0.3253   0.7545
 1000  10  18     -0.00370     +0.00345        -0.8434      +0.4775   0.6768
 1000  12  16     -0.00930     +0.00885        -0.8970      +0.5458   0.6469
 3000   1  27     -0.00002     +0.00002        -0.0458      +0.0458   0.9562
 3000   2  26     -0.00007     +0.00007        -0.1845      +0.1273   0.8871
 3000   3  25     -0.00011     +0.00010        -0.1845      +0.1273   0.8871
 3000   4  24     -0.00021     +0.00020        -0.3704      +0.1820   0.8460
 3000   6  22     -0.00046     +0.00049        -0.5406      +0.2283   0.8141
 3000   8  20     -0.00134     +0.00134        -0.6656      +0.3144   0.7608
 3000  10  18     -0.00418     +0.00428        -0.8368      +0.4794   0.6759
 3000  12  16     -0.01022     +0.00964        -0.8900      +0.5504   0.6450
(718 s)

Table 2. every m in [35, 1000], j = 4, jp = 18 (K = 22): half-width of the certified interval
  median 0.00163, 90% 0.00265, max 0.00617 (at m = 290); in-horizon sandwich half-width there 0.3948
  ten worst m: 290 (0.0062), 751 (0.0055), 505 (0.0053), 289 (0.0053), 288 (0.0053), 321 (0.0052), 101 (0.0051), 504 (0.0050), 784 (0.0050), 594 (0.0047)
  smallest in-horizon sandwich half-width over the range: 0.2623
(32 s)
```

Table 1, missing rows (added after REFEREE1, `certify.py odd`, `data/certified_odd.txt`):

```
Table 1. Theorem R bounds, K = j + jp = 28. rel = (bound - 2^m P(m+j)) / 2^m P(m+j).
    m   j  jp    rel_lower    rel_upper     triv_lower   triv_upper   P(m+j)/P(m)
  100   5  23     -0.00322     +0.00235        -0.6335      +0.2262   0.8155
  100   7  21     -0.00523     +0.00402        -0.7848      +0.2997   0.7694
  100   9  19     -0.00832     +0.00714        -0.8772      +0.4331   0.6978
  100  11  17     -0.01527     +0.01559        -0.9679      +0.6875   0.5926
 1000   5  23     -0.00036     +0.00039        -0.5236      +0.2626   0.7920
 1000   7  21     -0.00084     +0.00097        -0.6640      +0.3253   0.7545
 1000   9  19     -0.00218     +0.00200        -0.7716      +0.3785   0.7254
 1000  11  17     -0.00505     +0.00505        -0.8434      +0.4775   0.6768
 3000   5  23     -0.00029     +0.00027        -0.3704      +0.1820   0.8460
 3000   7  21     -0.00095     +0.00097        -0.6656      +0.3144   0.7608
 3000   9  19     -0.00232     +0.00239        -0.7678      +0.3737   0.7280
 3000  11  17     -0.00603     +0.00589        -0.8368      +0.4794   0.6759
(326 s)
```

At m = 100, j = 1 the interval is exact: amin(101) = amin(100), so nothing can die at step 101, and both the sandwich and Theorem R are tight.

Reading the table. For m = 1000, N(2^1000, 1000+j) is certified to within about 1% of 2^1000 P(1000+j) for every j <= 12 (the odd j 5, 7, 9, 11 are in `data/certified_odd.txt`, computed after REFEREE1; before that, "every j <= 12" was claimed with only eight j computed). This is a statement about the parities of T^{1001}(n), ..., T^{1012}(n) for all n < 2^1000, which no in-horizon argument determines. As expected the precision decays slowly with j, because the line has 2^{j'} points that must stand in for 2^{j'+j} residues.

## 4. Theorem D (almost all octaves), PROVED

### Lemma F (averaged uniform discrepancy)

Let Q = 2^K, S ⊂ Z/Q, N = 2^{j'} with j' >= j = K - j' >= 1, and let c be odd. For u uniform on the coset c·<3> of (Z/Q)^*:

    E_u max_B |Φ(u,B) - Φ̄|  <=  g_K sqrt(|S| (1 - |S|/Q)),   g_K = 4(1 + (K-1) ln2/2) <= 4(1 + 0.3466(K-1)).

*Proof.* Write Ŝ(ξ) = Σ_{x∈S} e(-xξ/Q) and G(η) = Σ_{s<N} e(sη/Q). Fourier inversion gives Φ(u,B) = Q^{-1} Σ_ξ Ŝ(ξ) e(ξB/Q) G(uξ), and the ξ = 0 term is Φ̄. Hence, for every B,

    |Φ(u,B) - Φ̄| <= Q^{-1} Σ_{ξ≠0} |Ŝ(ξ)| |G(uξ)|.

The right side does not depend on B. If v2(ξ) >= j' then uξ = 2^{j'}η'' with η'' ≢ 0 mod 2^j, and G(uξ) is a sum over N/2^j full periods of a nontrivial character, which is 0. Otherwise write e = v2(ξ) < j' and L = K - e >= j+1 >= 2. As u runs over c<3>, uξ = 2^e·a, where a runs uniformly over a coset of the image H_L of <3> in (Z/2^L)^*. Here |H_L| >= 2^{L-2} (and = 2 for L = 2), so 2^L/|H_L| <= 4. Using |G(η)| <= 1/(2||η/Q||) and ||2^e a/Q|| = ||a/2^L||,

    E_u |G(uξ)| <= |H_L|^{-1} Σ_{a odd mod 2^L} 1/(2||a/2^L||) = (2^L/|H_L|) Σ_{b odd, b<2^{L-1}} 1/b
                <= 4 (1 + (L-1) ln2 / 2) <= g_K,

because 1/b <= (1/2)∫_{b-2}^b dx/x for odd b >= 3. Finally, Cauchy–Schwarz and Parseval (Σ_ξ |Ŝ|^2 = Q|S|) give Σ_{ξ≠0}|Ŝ(ξ)| <= sqrt((Q-1)(Q|S| - |S|^2)) <= Q sqrt(|S|(1 - |S|/Q)). ∎

Exact check: in 432 cases (K = 8..14, j = 1..3, threshold patterns of every slot, cosets 1, 5^{-1}, -1), the left side was computed exactly over all u and all B. The largest ratio of the left side to the right side was 0.064. So the lemma holds with a lot of room; its constants are not sharp. The B-free Fourier bound was also checked pointwise in floating point.

### Lemma P (the only patterns that occur are no harder than the root), PROVED

Write the depth-d survivors as slots: A = amin(d) + k, with k = 0, 1, .... Then th_i = amin(d+i) - A = ceil(φ + iλ), where φ = dλ - A = {dλ} - 1 - k < 0. (At d = 0 the formula is off by one, φ = -k, but th_i <= amin(i) still holds.) Hence th_i <= ceil(iλ) = amin(i), so S_{d,A} ⊇ S_root and |S_{d,A}| >= #surv(K). S is not all of Z/Q only if ceil(φ + Kλ) >= 1, i.e. k < Kλ - 1 + {dλ}. So at most n_s = floor(Kλ) + 1 slots matter. The pattern of slot k depends only on {dλ}, and it is constant between the breakpoints {1 - {iλ} : i <= K}. So there are at most K + 1 patterns per slot. (`analytic.py` checks th_i <= amin(i) for every slot pattern with K <= 24.)

### Lemma M, PROVED

#surv(a+b) >= #surv(a)·#surv(b): a concatenation of two surviving parity words survives, because A_i > iλ is additive. Put h0 := log2 #surv(2000)/2000 >= 0.9430. Iterating, log2 #surv(K) >= floor(K/2000)·2000 h0 >= (K - 2000) h0 for every K >= 1 (for K < 2000 the right side is negative and #surv(K) >= 1). This explicit bound, not the Fekete limit, is what Corollary D uses: sqrt(#surv(K)) >= c 2^{h0 K/2} with c = 2^{-1000 h0}. (Fekete gives lim = sup >= h0, but a lower bound on the limit alone does not bound each term; REFEREE1 pointed this out.) The true value is H(λ) = 0.94996 (Terras; round 3 `density` Theorem 3).

### Theorem D

Let ε > 0, j >= 1, K >= 2j, j' = K - j, q = 2^{K-2} <= M. Then

    #{ m ∈ [M, 2M) : |N(2^m, m+j) - 2^mP(m+j)| > ε 2^mP(m+j) }
        <=  2 n_s (λ + 3)(K+1) g_K 2^j M / (ε sqrt(#surv(K))).

*Proof.* By Theorem R the relative error at m is at most max over the nontrivial slots k of r_k(m) = r(3^{A_k} mod 2^K, pattern_k(m)), where A_k = amin(d) + k and d = m - j'. Let Bad_k be the set of a ∈ Z/q for which r(3^a, p) > ε for some pattern p of slot k.

By Markov's inequality, Lemma F (coset c = 1; u = 3^a is uniform on <3> when a is uniform mod q) and Lemma P (Φ̄ = 2^{-j}|S| and |S| >= #surv(K)), with at most K + 1 patterns per slot:

    |Bad_k|/q <= (K+1) g_K 2^j / (ε sqrt(#surv(K))).

As d runs through an interval of length M, A_k(d) = ceil(dλ) + k is nondecreasing. It takes each value at most twice (1/λ < 2) and covers an interval of at most Mλ + 2 integers. So at most 2((Mλ+2)/q + 1)|Bad_k| <= 2(Mλ + 3q)|Bad_k|/q values of d put slot k in Bad_k. Sum over the n_s slots and use q <= M. ∎

**Corollary D (the headline).** Take K = floor(log2 M) + 2 and ε = M^{-η/3}. By Lemma M, sqrt(#surv(K)) >= 2^{-1000 h0} 2^{h0 K/2} >= c M^{h0/2} with c = 2^{-1000 h0}, since 2^K > 2M. Summing the bound over j <= J with 2^J <= (2M)^{h0/2-η}, the number of bad m is at most C (log M)^3 M^{1-η}·M^{η/3} <= M^{1-η/3} for large M. On the remaining m, |N(2^m,b)/2^mP(b) - 1| <= M^{-η/3} <= 2m^{-η/3} for every b in (m, m + (h0/2 - η) log2 m]. The condition K >= 2j holds because j <= 0.48 log2 M. So **the τ-version of the count law holds for X = 2^m, for a density-one set of m, at every depth up to log2 X + (h0/2 - η) log2 log2 X**, with a power-saving error. ∎ This is not Conjecture E as stated: E uses σ and all X. For σ only the lower bound N_σ >= N_τ transfers (section 7). *(Corrected after REFEREE1: the original sentence said "the count law of Conjecture E holds ... up to log2 X + 0.47 log2 log2 X".)*

The explicit constants make the bound useful only from about M = 2^65 (j = 1, ε = 0.1; `analytic.py` part D). This is a theorem about the asymptotics, and the gap between m = 3000 and m = 2^65 is covered only m by m (any given m can be certified by `certify.py`).

**D' (explicit densities at K = 16), PROVED.** Weyl's theorem gives the joint equidistribution of (floor(dλ) mod q, {dλ}), via {dλ/q} with λ/q irrational. So the natural density of the m at which slot k is bad equals the product measure of the bad (a, {dλ}) set. `analytic.py` computes that set over all 2^14 multipliers and all 172 slot patterns. The thresholds and the bad-multiplier test are exact; the pattern representatives d are found by a floating-point search (tolerance 1e-9), the interval widths in {dλ} are floats, and intervals narrower than 1e-12 are dropped. The resulting error in each density is below 1e-9, so the printed digits are unaffected. Upper densities of {m : |N/2^mP - 1| > ε}:

| j | ε = 0.01 | 0.02 | 0.05 | 0.10 |
|---|---|---|---|---|
| 1 | 0.200 | 0.036 | 0.0020 | 0.0001 |
| 2 | (>1, vacuous) | 0.318 | 0.025 | 0.0020 |
| 4 | vacuous | vacuous | 0.82 | 0.136 |

These numbers are a union bound over the slots (each slot at its worst B). The actual errors are weighted averages over slots and are much smaller (section 3). The weights are in-horizon quantities, but I have no all-d theorem for them, so the density statements do not use them.

## 5. Route (i): what breaks, exactly, and the all-m question

**O1, PROVED.** Only depth-d survivors whose slope 3^A/2^d is below 2^K can die in the next K steps. For those, A ∈ [amin(d), amin(d+K)), which is at most ceil(Kλ)+1 consecutive integers. So, for any single m, the multipliers 3^A that Theorem R needs are about 0.63K consecutive powers of 3. They are not equidistributed mod 2^{2j-2} for any j >= 3. A local limit theorem for A among survivors (twisted transfer operator) describes how the weight spreads over this window. It cannot make 3^A equidistribute.

The dependence that breaks route (i) as proposed is the dependence of the level on A. Conditioning on the level fixes A. The randomness has to come from somewhere else:

* (a) the specific value of 3^A mod 2^K, which gives Theorem C, m by m;
* (b) the drift of the window with m, which gives Theorem D.

The second circularity (needing A to be independent of the middle bits of B) disappears once one bounds uniformly in B.

**Bad multipliers (EVIDENCE).** At K = 16 and j = 2, the worst multipliers for slot k are u = 3^a with a ≡ -(8-k) mod 2^{12} (for slot 0: r = 0.28 against a mean of 0.036). Next come a ≡ -18 mod 2^8 and similar. That is, the bad multipliers are 2-adically close to 3^{-i} for small i: after i forced odd steps, the line becomes nearly an interval. u = 1 itself is harmless (r = 0.016).

**O2' (all m, a fixed bound; added after REFEREE2, N2), PROVED.** Fix j and K, and let m >= K - j + 1, so that the split depth j' = K - j gives d = m - j' >= 1. By Theorem R the relative error at m is at most max_k r(3^{A_k} mod 2^K, pattern_k(m)) over the nontrivial slots k. Every multiplier 3^{A_k} mod 2^K lies in the finite group <3> (2^{K-2} elements), and by Lemma P every pattern is one of the finitely many slot patterns. So the maximum of r over all multipliers in <3> and all slot patterns bounds the error for every such m. At K = 16 (`allm_bound.py`, exact: integer max/min from `disc allu` over all 2^14 multipliers and all 172 slot patterns, ratios as fractions; the slot-pattern breakpoints are floats, but their minimum gap is 0.047, so no pattern is missed) this gives, for every m >= 17 - j,

| j | bound on \|N(2^m,m+j)/2^mP(m+j) - 1\| |
|---|---|
| 1 | 129/1057 = 0.1221 |
| 2 | 213/749 = 0.2844 |
| 3 | 349/749 = 0.4660 |

These are the values REFEREE2 reports (0.122, 0.284, 0.466). Larger K should improve them, but the bound never tends to 0 with m, so O2 below is unchanged.

**O2 (OPEN).** To have Theorem D for all large m (error tending to 0), one would need: for every large A, each of the 0.63K multipliers 3^{A+k} mod 2^K is good for some K <= c log m. A natural sharp hypothesis would be r(3^A) <= K^C 2^j (2^{μ(A)}/#surv(K))^{1/2} for the integer A (not its class mod q), where μ(A) = max_{|i| <= K, A+i ≠ 0} v2(A + i). (REFEREE1 noted that the first version defined μ on a mod q but then used v2 of the integer A; this is the intended reading.) It would give all m, because μ(A) <= log2 A + 1 < K once K > log2 m + 2. I did not test it beyond the K = 16 tables above, and I have no proof. This is where the argument stops: no available estimate controls the discrepancy of the specific dilations 3^A against a 2-adic Cantor set, only its average over A.

Route (ii) (Korobov sums of a^n mod prime powers) was not needed: Lemma F uses only the complete sum over the cyclic group, where Parseval is exact. Route (iii) (Kronecker discrepancy) is what Lemma F is, with the max over B absorbed by the B-free Fourier bound.

## 6. The siblings 3x+d (generalisation G), PROVED

Terras' identity holds for T_d(x) = (3x+d)/2 or x/2, for any odd d. Over Z_2, T_d(x) = d T_1(x/d), so the parity words of x under T_d are those of x/d under T_1 (checked in `check_exact.py` part 3). The survivor set is therefore dS, and Φ_d(u, B) = Φ_1(u d^{-1}, B d^{-1}). Theorem R holds with the multiplier 3^A d^{-1} (`microlib.bounds(..., dd=d)`). Lemma F holds for every coset, so Theorem D holds for every odd d. Checked against brute force for 3x-1 and 3x+5 (n < 2^32).

**Reflection identity (added after REFEREE1, PROVED).** With N = 2^{j'}, the substitution s ↦ N-1-s gives Φ(-u, B) = Φ(u, B - u(N-1)), so max_B Φ and min_B Φ are the same for u and -u. For K >= 3, <3> has index 2 in (Z/2^K)^* and does not contain -1, so (Z/2^K)^* = <3> ⊔ -<3> (for K <= 2 the group is <3> itself). Hence for every odd d, 3^A d^{-1} = ±3^{A+t} with t = t(d, K) independent of A, and:
* for 3x-1 (d^{-1} = -1, t = 0) the certificate of Theorem C is exactly the 3x+1 certificate (`certify.py siblings` checks this at m = 1000, K = 24, j <= 8);
* for every odd d the Weyl densities of D' are unchanged, because the bad set in (a, {dλ}) is shifted by t in the first coordinate, which preserves the product measure. So D' holds for every odd d with the same table.
* For other d the certificate of C must be recomputed: the shift t changes which 0.63K consecutive multipliers the window sees for a given m. At m = 1000, K = 24 (`data/certified_siblings.txt`) the certified half-widths for d = 5, -3, 7 are of the same order as for d = 1 but are different numbers (j = 8: 0.0050, 0.0049, 0.0054 against 0.0048; j = 2: 0.00029, 0.00024, 0.00018 against 0.00033). No sibling certificate at K = 28 or at m = 100 or 3000 was computed.

*(Corrected after REFEREE1: this section originally said that R, C, D and D' hold verbatim for every odd d. That was wrong for C when d ≠ ±1, and for D' the reason, the reflection identity, was missing.)*

The extra cycles of 3x-1 and 3x+5 are finitely many starts. They change counts by O(1), while 2^m P(m+j) grows like 2^{0.95m}. So nothing in R, C or D excludes or needs to exclude them. This is the expected behaviour of a sound argument.

## 7. Integer stopping time

The [subsequent transfer theorem](actual_counts.md) proves an upper as well as a lower
estimate for actual stopping-time counts, including odd negative d. The assessment
below records the original round-five result.

σ(n) = min{i : T^i(n) < n}. If 3^{A_i} >= 2^i then T^i(n) >= n, so σ >= τ. Here T^i(n) = (3^{A_i} n + c_i)/2^i with c_i >= 0, which holds for 3x+d with d > 0. Hence N_σ(2^m, b) >= N_τ(2^m, b), and every lower bound above holds for σ (PROVED for d > 0, in particular 3x+1; not claimed for d < 0, where c_i can be negative). For the upper bound one needs σ = τ for almost all of the counted n (Terras' coefficient stopping time conjecture is open). Brute force over 1 <= n < 2^34 (the convention of `brute`) shows N_σ - N_τ = 1 (only n = 1) for every m <= 34 and m <= b <= m+8, except m = b = 1 where the difference is 0 (EVIDENCE; `check_revision.py` part 3). With n = 0 counted, as in section 2, each difference is one larger, because σ(0) = ∞ while τ(0) = 1.

## 8. Honest limits

* The theorems are for 3x+1 and 3x+d. split5_3 (U/O digit states, multiplier 5) and K7 were not done. The proof of Lemma F needs only an odd multiplier group of bounded index, so I expect it to transfer. But the node bookkeeping (digits versus halvings, the O state where the multiplier is 2·5^A) has not been written or checked.
* Theorem D is "almost all m", for τ and X = 2^m only; for every m only the fixed bound O2' (j <= 3) is proved. Theorem C covers m <= 3000 (j = 4 all m in [35,1000]; every j <= 12 at three values), for 3x+1 and 3x-1; for d = 5, -3, 7 only m = 1000, j <= 8, K = 24. The all-m statement with error tending to 0 is OPEN (section 5).
* The depth gained is j <= (h0/2 - η) log2 m, h0/2 >= 0.4715: log log X digits, not a multiple of log X. The method is limited by having 2^{j'} line points for 2^{j'+j} residues, and by needing q = 2^{K-2} <= M for the averaging. Conjecture E (j up to Km) is untouched.
* The lower-bound question (explicit n with σ(n) >= c log2 n, c > log2 3) gained nothing.
* Quoted results: Terras' identity and Weyl's equidistribution theorem are standard and fully stated above. Fekete's lemma is standard. The value H(λ) = 0.94996 is quoted from round 3 and is not used in any proof (h0 is computed). No external number-theory constants are used.

## 9. Revision after REFEREE1

REFEREE1 confirmed every PROVED proof (R, F, P, M, D, D') and asked for textual repairs only. Each item, and what was done:

| referee item | action |
|---|---|
| C: "1 <= j <= 12" but j = 5, 7, 9, 11 were never computed | **Computed** (`certify.py odd`, 326 s, `data/certified_odd.txt`). All within the claimed range: largest half-width at j = 11 is 0.0156 (m = 100); every j <= 12 at m = 100, 1000, 3000 now has a certificate, max 0.0192 (j = 12, m = 100). The original claim was unsupported for those four j until now; it is now true as stated. |
| C: j = 1 constant "2·10^-5" | **Wrong, corrected** to 3.2·10^-5. Exact values 0, 3.184·10^-5, 1.832·10^-5 at m = 100, 1000, 3000 (`check_revision.py` part 6 recomputes them exactly). |
| M as used in D: Fekete gives a bound on the limit, not on each #surv(K) | **Gap closed**: log2 #surv(K) >= floor(K/2000)·2000 h0 >= (K-2000) h0 by supermultiplicativity, so c = 2^{-1000 h0} (section 4, Lemma M; checked for K <= 6000 in `check_revision.py` part 2, though the proof does not need the check). |
| D: "the count law of Conjecture E holds ... up to log2 X + 0.47 log2 log2 X" | **Overstated, withdrawn** and replaced by: the τ-version of the count law holds for X = 2^m, for a density-one set of m, up to depth log2 X + (h0/2 - η) log2 log2 X. Conjecture E (σ, all X) is not proved at any depth beyond the horizon; for σ only the lower bound transfers. The constant is h0/2 with h0 >= 0.9430 proved, not 0.47 or H(λ)/2. |
| G: "R, C, D and D' hold verbatim for every odd d" | **Wrong for C when d ≠ ±1, withdrawn.** Corrected statement: R, D, D' hold for every odd d (D' by the reflection identity, now proved in section 6); C holds verbatim for 3x-1; for other d the certificate must be recomputed with multiplier 3^A d^{-1}. Sibling certificates were computed at m = 1000, K = 24, j <= 8 for d = 5, -3, 7 (`data/certified_siblings.txt`); they differ from 3x+1. |
| σ: the proof of σ >= τ uses c_i >= 0 | **Scoped**: claimed for 3x+1 (and d > 0), explicitly not for d < 0. |
| σ data nit: at m = b = 1 the difference is 0 | **Corrected** (checked, `check_revision.py` part 3). |
| LB: "no explicit family beats ..." stated as fact from memory | **Reworded** to "I know of no explicit family ...", with "no literature search was done". |
| Title not scoped | **Scoped** to "in this census". Lemma F is a standard Fourier / Erdős–Turán type estimate and Theorem R is elementary; the contribution is their combination and the certified numbers. |
| P: d = 0 edge case (φ = -k) | Noted in Lemma P; the conclusion is unchanged. |
| D': floating-point pattern search in `analytic.py` | Described in section 4 (error below 1e-9; printed digits unaffected). Not converted to exact arithmetic. |
| O2: μ defined mod q but used on the integer A | Hypothesis restated with μ(A) for the integer A. Still OPEN and untested beyond K = 16. |
| n = 0 counted in N but not in `brute` | Noted in the proof of Theorem R (harmless). |

What did not change: no proof was altered except the explicit lower bound in Lemma M. What stayed open is unchanged: all m (O2), σ upper bound, split5_3 and K7, the lower-bound question, and Conjecture E itself. The method still stalls exactly at O2, where an all-m bound on the discrepancy of the specific dilations 3^A against the 2-adic survivor set would be needed, and at the depth limit j <= (h0/2) log2 m imposed by 2^{j'} line points standing in for 2^{j'+j} residues together with q = 2^{K-2} <= M.

## 10. Revision after REFEREE2

REFEREE2 confirmed every PROVED proof (needs_repair: false) and listed wording fixes plus one recommended strengthening. No proof was changed. Each item:

| referee item | action |
|---|---|
| C nit: "up to 0.019 (j = 12)", but the certified value is 0.01923 | Results row now says 0.0193. |
| D' wording: "These numbers use the worst slot" | Now "a union bound over the slots (each slot at its worst B)", which is what `analytic.py` computes (hence the j = 2, ε = 0.01 entry above 1). |
| N1 novelty: "a first rigorous step", and "every density result in the census stops at depth m" | "first" dropped from the title. The "genuinely beyond" paragraph now says "every earlier density result" and names the concurrent `census/round5/fourier` lens (Theorems U, U'), which also proves an all-depth bound 1 to 3 digits past the horizon. REFEREE2 quoted its original constants 0.195, 0.433, 0.878; its revised exact form U' gives 129/1057, 213/749, 349/749 for 3x+1, the same fractions as O2' below. |
| N2 (recommended strengthening): an explicit all-m bound from Theorem R and Lemma P | Added as O2' (Results table and section 5), with its derivation. I verified it with the folder's own code (`disc allu`, the slot-pattern enumeration of `analytic.py`) in the new script `allm_bound.py`: exactly 129/1057 = 0.1221, 213/749 = 0.2844, 349/749 = 0.4660 at j = 1, 2, 3, K = 16, for every m >= 17 - j. That agrees with REFEREE2's 0.122, 0.284, 0.466. O2 is restated as "all m with error tending to 0: OPEN". |
| N3: n = 0 in the σ data (σ(0) = ∞, τ(0) = 1) | The "differ by exactly 1" statements (σ row, section 7) now say n >= 1, the convention of `brute`, and note that counting n = 0 makes each difference one larger. |
| N4: unsourced "τ(n) <= C log n would imply Collatz" in section 1 | Now says this is not immediate: it needs a Baker-type lower bound on 2^i - 3^{A_i}. It is marked as unlabelled context that is not used anywhere. |

## Files

| file | content |
|---|---|
| `microlib.py` | exact routines: amin, Cnt_d (dynamic programming), thresholds, Theorem R bounds (`bounds_many`, `dd` for 3x+d) |
| `disc.c` | exact max_B/min_B Φ: digit-tree construction of S, sliding window over B; modes `batch`, `allu`, `naive` |
| `brute.c` | brute-force τ and σ counts for n < 2^M, 3x+d |
| `check_exact.py` | Theorem R checks against brute force, Terras identity, conjugacy, fast = naive (exits 0, about 2 s) |
| `certify.py` | Theorem C tables to `data/certified.txt` (exits 0; about 10-15 min; `quick` mode about 10 s); mode `odd` writes `data/certified_odd.txt` (j = 5, 7, 9, 11); mode `siblings` writes `data/certified_siblings.txt` (3x+d, d in {1, -1, 5, -3, 7}) |
| `check_revision.py` | exact checks for the repairs after REFEREE1: reflection identity and <3> ⊔ -<3> (with a mutation test), Lemma M explicit bound, σ - τ data, completeness and constants of the certified tables, sibling tables, the exact j = 1 constant (exits 0; about 2 min) |
| `allm_bound.py` | the all-m bound O2' at K = 16, j = 1..3, exact (exits 0 iff 129/1057, 213/749, 349/749 are reproduced; about 3 min; added after REFEREE2) |
| `REFEREE1.md`, `referee1_check.py` | the referee report and the referee's independent checker |
| `REFEREE2.md`, `referee2_check.py` | the second referee report and that referee's independent checker |
| `analytic.py` | Lemmas F, P, M exactly; Theorem D constants; D' densities (exits 0; about 5 min; numpy part needs `../../round4/wpotential/.venv/bin/python`) |
| `data/` | brute-force counts and certified tables |
