# Referee 1 report: round 5, lens "microrange" (27 Nov 2026)

Referee: independent agent. Scope: `README.md` and all code in this folder, against
`census/round4/lead/CONJECTURE.md` (Conjecture E). The prover's files were not edited; their checks were
re-run on a scratch copy, with `disc` and `brute` recompiled from source.
My own checker is `referee1_check.py`. It was written from scratch, exits 1 on any failure, and includes
a mutation test that shows it can fail. Run it with
`../../round4/wpotential/.venv/bin/python referee1_check.py` (about 2.5 min).

## Summary

The mathematics holds. I re-derived every PROVED proof line by line and found no gap in R, F, P, M, D
or D'. The core results are genuinely beyond the horizon. N(2^m, m+j) is a count over the integers
n < 2^m, which is the same thing as the residues mod 2^{m+j} whose top j bits are zero. That is exactly
the object of Conjecture E at b = m+j, and it does not restate in-horizon equidistribution. The key
input is the interval structure of the top j' digits of n, made uniform in the unknown intercept.

The argument does not prove anything false or famous:
* It is consistent with the extra cycles of 3x-1 and 3x+5, which change counts by O(1).
* It gains only j <= 0.47 log2 m digits, and only for almost all octaves.
* It stops exactly where an all-m statement about specific dilations 3^A would be needed (O2).

Several statements in PROVED rows say more than was computed or proved, so textual repairs are needed:
* the j-range and the j = 1 constant in C;
* "verbatim" for C in G;
* the σ-versus-τ wording in Corollary D.

No mathematical repair is needed.

## Reproduction

| check | result |
|---|---|
| `check_exact.py` | exits 0 (1369 cases, 2 s) |
| `analytic.py` (venv) | exits 0: F in 432 cases, max ratio 0.0640; F' 0 violations; h0 >= 0.94300; D constants (M >= 2^65 for j = 1, ε = 0.1); D' table reproduced to all printed digits |
| `certify.py` (full, 13 min) | exits 0; `data/certified.txt` reproduced identically (apart from timing lines) |
| `referee1_check.py` (mine) | exits 0, with all parts below passing |

What `referee1_check.py` does, all exact unless stated:
* **T.** Terras' identity, including negative r and s and d in {1, -1, 5, -3, 7}, and the 3x+d conjugacy mod 2^14.
* **R.** Theorem R built from scratch, without the prover's conjugacy trick: survivor sets come from direct simulation of 3x+d, Cnt_d from enumerating residues, and Φ from cyclic window sums. There is also a numpy brute force of N(2^m, m+j). Tested on 324 cases: 3x+1, 3x-1 and 3x+5, m = 12..20, j in {1,2,3,5}, three split depths. In every case:
  * the middle step of the proof holds as an identity, N = Σ_r Φ(3^A, T^d(r) mod 2^K);
  * L <= N <= U holds;
  * Σ Cnt·|S|/2^j equals an independent dynamic-programming value of #surv(m+j)/2^j.

  The mutation multiplier 3^{A+1} breaks the identity in 286 of 324 cases, so the check can fail.
* **X.** At large m, my implementation reproduces README Table 2 at m = 290, 751 and 101 (half-widths 0.00617, 0.00547, 0.00514). At m = 1000 (j = 8, j' = 12) and for 3x-1 at m = 200, my (L, U, main) equal the prover's `microlib` values exactly, as integers and Fractions.
* **F.** Lemma F checked exactly on 162 cases with arbitrary sets S, because the lemma claims every S. The sets were random with densities 0.03, 0.3 and 0.7, an interval, a 2-adic ball and the root survivor set, with K = 8..10, j = 1..3 and cosets 1, -1, 5^{-1}. Max LHS/RHS is 0.072.
* **P.** Lemma P checked exactly for every depth d < ~6000 at K = 8, 16, 24. th_i <= amin(i) always. The number of nontrivial slots and the number of patterns per slot meet the bounds floor(Kλ)+1 and K+1 exactly, so both bounds are sharp.
* **M.** Supermultiplicativity holds (a, b < 70), and log2 #surv(2000)/2000 >= 0.94300.
* **S.** σ >= τ for every n < 2^20 under 3x+1.
* **G.** The coset question for the siblings (see G below). The reflection identity was verified exactly.
* **E.** The "bad multiplier" evidence: at K = 16, j = 2, slot 0, a ≡ -8 mod 2^12 gives r = 0.284, against pattern means of 0.013-0.037. This matches the README's 0.28 and 0.036.

## Verdicts

### R (reduction, uniform in the intercept): CONFIRMED

I re-derived the proof:
1. The split n = r + 2^d s, with d = m - j' and s < 2^{j'}, enumerates [0, 2^m) exactly.
2. The first d parities depend only on r.
3. T^d(n) = 3^A s + T^d(r), and A_{d+i}(n) = A + A_i(x).
4. K = j + j' steps after depth d reach depth m + j.
5. The parities of x over K steps depend on x mod 2^K.

So N = Σ_r Φ(3^A mod 2^K, T^d(r) mod 2^K). This is exact, and my R part confirms it as an identity, not
only as a bound. Taking min and max over B gives L and U.

The main identity uses the bijection s ↦ 3^A s + B mod 2^K. The error line follows because the trivial
A contribute zero error. Both L and U depend only on Cnt_d (depth d < m) and on S mod 2^K. These are
in-horizon data, and no information about B is used.

The "not circular" paragraph is correct. Note that n = 0 is included in the README's N but not in
`brute`. This is harmless because 0 never survives step 1.

### C (certified instances): CONFIRMED_WITH_FIX

The computation is exact and reproduced: Python integers for Cnt_d, and exact C for max/min over all
2^K intercepts. I checked the 64-bit arithmetic in `disc.c`. Values are kept mod 2^64, and the right
shifts lose one top bit per step; with K <= 31 this never reaches the parity bit. The `sufmax` shortcut
and the sliding update are also correct.

Two statements in the results row are not what was computed:
* **The j range.** The row says "1 <= j <= 12", but only j in {1, 2, 3, 4, 6, 8, 10, 12} were computed. j = 5, 7, 9, 11 are absent. Section 3's "for every j <= 12" at m = 1000 has the same problem. *Fix:* list the computed j, or run the missing four.
* **The j = 1 constant.** The row says "|δ| at most 2·10^-5 (j = 1)". The exact values are 0 at m = 100, 3.18·10^-5 at m = 1000 and 1.83·10^-5 at m = 3000. *Fix:* "at most 3.2·10^-5".

The m in [35, 1000] statement at j = 4 (at most 0.0062) and the sandwich comparison at j = 12, m = 100 are correct.

### F (averaged discrepancy lemma): CONFIRMED

I re-derived the proof:
* **Fourier inversion.** The ξ = 0 term is Φ̄.
* **Vanishing terms.** For v2(ξ) >= j', the term is zero because j' >= j makes N a multiple of the period 2^j.
* **The distribution of uξ.** For e < j', uξ/2^e mod 2^L is uniform on a coset of H_L, because reduction mod 2^L is a group homomorphism.
* **The index of H_L.** |H_L| = 2^{L-2} for L >= 3, and 2 for L = 2, so 2^L/|H_L| <= 4.
* **The bound on G.** |G| <= 1/(2||·||) follows from sin(πx) >= 2x.
* **The sum over odd a.** Each odd b < 2^{L-1} occurs twice, which gives the factor 2^L.
* **The harmonic sum.** Σ_{b odd < 2^{L-1}} 1/b <= 1 + (L-1)ln2/2. 0.3466 >= ln2/2 = 0.34657, and L <= K.
* **Parseval and Cauchy–Schwarz** finish the proof.

The lemma is true for every S, which my random-set check also confirms. It is a standard Erdős–Turán /
large-sieve-type estimate. It is correctly presented as a tool, not as a novelty.

### P (patterns no harder than the root) and M (supermultiplicativity): CONFIRMED, with one wording fix for M as used in D

**P.** th_i = ceil(φ + iλ) with φ = {dλ} - 1 - k < 0, so th_i <= ceil(iλ) = amin(i). The trivial-slot
criterion and the K+1 breakpoints are also correct. There is one edge case: at d = 0 the formula for φ
is off by 1 (φ = -k), but th_i <= amin(i) still holds. P is verified exactly for every d < ~6000.

**M.** Concatenating two surviving words survives, and h0 is computed. One step needs a fix. Corollary D
uses "sqrt(#surv(K)) >= c M^{h0/2}". That does not follow from "lim >= h0" as written: Fekete gives
an upper bound by the sup, not a lower bound at each K. It does follow from superadditivity directly:
log2 #surv(K) >= floor(K/2000) · 2000 h0 >= (K - 2000) h0, so c = 2^{-1000 h0} works.
*Fix:* state this one line.

### D (almost every octave, up to (h0/2 - η) log2 m extra digits): CONFIRMED_WITH_FIX (prose only)

I re-derived the proof:
* **The multipliers.** q = 2^{K-2} is the order of 3 mod 2^K, so a uniform mod q gives u uniform on <3>.
* **Markov's inequality.** It applies per pattern, with Φ̄ = |S|/2^j and |S| >= #surv(K). The union over K+1 patterns gives the bound on |Bad_k|/q.
* **Counting depths.** A_k(d) = ceil(dλ) + k is nondecreasing and takes each value at most twice, since 2λ > 1. Over d in an interval of length M it covers at most Mλ + 2 integers. This gives 2(Mλ + 3q)|Bad_k|/q.
* **Corollary D.** I checked it as follows:
  * K = floor(log2 M) + 2 gives q <= M.
  * 2^K > 2M, so 2^{h0 K/2} >= M^{h0/2}.
  * Σ_{j <= J} 2^j <= 2(2M)^{h0/2-η}.
  * The total is O((log M)^3 M^{1-2η/3}), which is at most M^{1-η/3}.
  * The range condition j <= (h0/2-η) log2 m <= J holds, and so does K >= 2j.
  * M^{-η/3} <= 2 m^{-η/3} for η <= 3.

The explicit constants (useful from M ≈ 2^65) are reproduced.

Two parts of the prose overstate the result:
* **σ versus τ.** The sentence "the count law of Conjecture E holds at every depth up to log2 X + 0.47 log2 log2 X" is not a statement of Conjecture E. E is phrased with σ and with N(X, b) for all X. D is for τ, at X = 2^m only, and for a density-one set of m. For σ only the lower bound transfers. *Fix:* "the τ-version of the count law holds for X = 2^m, for a density-one set of m". Also write (h0/2 - η) rather than 0.47.
* **The constant.** The headline should keep "(h0/2 - η)". It is h0 = 0.9430 that is proved, not H(λ) = 0.94996.

### D' (explicit densities at K = 16): CONFIRMED

Weyl applies to {dλ/q}, which encodes (floor(dλ) mod q, {dλ}) jointly and uniformly. The bad sets are
finite unions of point × interval, so they are Jordan measurable, and "upper density <=" is justified.
The table is reproduced.

There is a minor rigour note on how `analytic.py` handles patterns. It finds the representative d for
each pattern by a floating-point search with tolerance 1e-9, computes interval widths in floats, and
silently drops intervals narrower than 1e-12. The resulting error in the densities is below 10^-9, so the
printed 4-digit values are unaffected. The thresholds themselves are computed exactly.

### G (siblings 3x+d): CONFIRMED_WITH_FIX

**R and D.** R and D hold for every odd d. The conjugacy argument is correct, and my R part verifies
Theorem R for 3x-1 and 3x+5 by direct simulation of those maps, independent of the conjugacy.

**C does not hold "verbatim".** For d ≠ ±1 the multipliers are 3^A d^{-1}, so the certificates differ.
At m = 200, j = 3, j' = 12 the certified relative intervals are:

| map | certified interval |
|---|---|
| 3x+1 | [-0.0241, +0.0245] |
| 3x+5 | [-0.0182, +0.0165] |
| 3x-3 | [-0.0149, +0.0128] |
| 3x+7 | [-0.0102, +0.0084] |

No sibling certificate at m = 100/1000/3000 was ever computed.

**3x-1 and D' do hold verbatim, but for a reason the README does not give.** The reason is the reflection
s ↦ N-1-s, which gives Φ(-u, B) = Φ(u, B - u(N-1)), together with (Z/2^K)^* = <3> ⊔ -<3>. Every coset is
then <3> or -<3>, so:
* the max/min over B for multiplier ±3^{A+t} equal those for 3^{A+t};
* the 3x-1 certificate equals the 3x+1 certificate exactly (verified);
* the Weyl densities are invariant under the shift a ↦ a + t, so D' is the same for every odd d (verified at K = 12 for cosets 1, -1, 5^{-1}).

*Fix:* replace "R, C, D and D' hold verbatim" with "R, D and D' hold for every odd d (D' by the
reflection identity above), and C holds verbatim for 3x-1. For other d the method of C applies, but the
numbers must be recomputed with the multiplier 3^A d^{-1}."

The extra-cycle discussion is correct.

### O1 (why route (i) fails): CONFIRMED (a meta-statement)

The window of A's that can die has size at most floor(Kλ)+1. For one m, the 0.63K consecutive A cannot
equidistribute mod 2^{2j-2} when j >= 3. "False in the sense needed" is informal, but it is accurate.

### Bad multipliers (EVIDENCE): CONFIRMED as evidence

Reproduced: r = 0.284 against a mean of about 0.036.

### O2 (all m): OPEN, labelled honestly

The suggested hypothesis is loosely stated. μ(a) is defined for a mod q, but the argument then uses
v2 of the integer A. This does no harm, because the item is labelled OPEN.

### σ (stopping time σ): lower bound CONFIRMED_WITH_FIX (nit); upper bound EVIDENCE, CONFIRMED as evidence

The proof of σ >= τ uses T^i(n) = (3^{A_i} n + c_i)/2^i with c_i >= 0. That holds for 3x+d with d > 0,
not for 3x-1. The README states σ only for 3x+1, which is fine. It should say explicitly that the σ
lower bound is not claimed for d < 0.

Data nit: N_σ - N_τ = 1 for all m <= 34 and m <= b <= m+8, except m = b = 1, where the difference is 0.

### LB (lower-bound question): OPEN, labelled honestly; one wording fix

"No explicit family beats σ(n) >= (log2 3 - o(1)) log2 n" is a literature claim made from memory, with
no source and no search. The bound for 2^k - 1 itself is correct. *Fix:* "I know of no explicit family
that ...".

## Honesty of labels and novelty

The labels are mostly honest:
* The status line says "not refereed".
* The limits section is candid: log log X digits only, almost all m, split5_3 and K7 not done, Conjecture E untouched.
* The README correctly says that nothing bounds τ(n) for an individual n.
* No external number-theory constants are used. Weyl, Fekete and Terras are standard and are used within their exact statements.

The novelty claim "every density result in the census stops at depth m" is scoped to the census, which
is fine. The title, "a first rigorous step beyond the horizon", should also be scoped ("in this census"):
no literature search was done. Lemma F is a standard Fourier/Erdős–Turán argument, and Theorem R is
elementary. The value is in combining them and in the certified numbers.

The labelling problems that need repair are listed in the Summary. All three are textual.

## needs_repair: true

The repairs are textual only. No proof changes, except the one-line explicit lower bound in M.
