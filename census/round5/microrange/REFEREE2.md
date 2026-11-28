# Referee 2 report: round 5, lens "microrange" (second pass, after the REFEREE1 repair; 27 Nov 2026)

Referee: an independent agent. Scope: the revised `README.md`, all code and data in this folder, and
`REFEREE1.md`, read against `census/round4/lead/CONJECTURE.md` (Conjecture E). I did not edit the
prover's files. Their checks were re-run on a scratch copy, with `disc` and `brute` recompiled from
source and the brute-force data regenerated.

My own checker is `referee2_check.py`. I wrote it from scratch; it imports nothing from `microlib`, and
it exits 1 on any failure. Run it with:

    ../../round4/wpotential/.venv/bin/python referee2_check.py          (about 12 min)
    ../../round4/wpotential/.venv/bin/python referee2_check.py quick    (no K = 28 rows, about 3 min)

## Summary

The repair was honest, and every REFEREE1 item has been resolved:
* The four missing j were computed, and I reproduce them byte for byte.
* The j = 1 constant was corrected.
* The Lemma M gap was closed with a correct one-line argument.
* The overstatement in Corollary D was withdrawn.
* The siblings were rescoped, and the reflection identity, which was new, is proved correctly.

I re-derived every PROVED proof (R, F, P, M, D, D', the reflection identity, σ >= τ) line by line and
found no gap.

Every PROVED result is genuinely beyond the horizon. N(2^m, m+j) depends on the parities of
T^{m+1}(n), ..., T^{m+j}(n) for the integers n < 2^m. Equivalently, it counts the residues mod 2^{m+j}
whose top j bits are zero. These are not functions of n mod 2^m, and the in-horizon sandwich leaves
±40%.

No external theorem is quoted beyond its exact range:
* Weyl is applied to {dλ/q} with λ/q irrational.
* Terras' identity is proved.
* Fekete is no longer used for a per-K bound.
* H(λ) is quoted but used nowhere.

The argument is consistent with the extra cycles of 3x-1 and 3x+5, which change counts by O(1). It
proves nothing famous: it bounds counts only, gains O(log m) digits, and does so only for almost all
octaves.

What remains is minor: four wording points and one missed easy strengthening of O2 (section "New
items"). None of them is a GAP or WRONG.

## Reproduction

| check | result |
|---|---|
| `check_exact.py` (brute data regenerated from `brute.c`) | exits 0; 1369 cases; regenerated `brute34_3x1`, `brute32_3xm1`, `brute32_3xp5` identical to the shipped files |
| `check_revision.py` | exits 0 (parts 1-6; exact j = 1 half-widths 0, 3.184e-5, 1.832e-5) |
| `analytic.py` (venv) | exits 0; F 432 cases, max ratio 0.0640; h0 >= 0.94300; D constants; the D' table reproduced to all printed digits |
| `certify.py odd` | exits 0; output identical to `data/certified_odd.txt` (apart from the timing line) |
| `certify.py siblings` | exits 0; identical to `data/certified_siblings.txt`; d = -1 equals d = 1 exactly |
| `referee2_check.py` (mine, full) | exits 0, all parts pass |

What `referee2_check.py` does differently from the prover and from referee 1:
* **Survivor sets.** They come from direct numpy simulation of 3x+d itself, with no conjugacy x ↦ x/d. One array need(x) = max_i (amin(d+i) - A_i(x)) gives S_{d,A} = {need <= A} for every A at once.
* **max_B and min_B of Φ.** These are computed by permuting the indicator through y ↦ u·y and taking all cyclic window sums with a cumulative sum. There is no digit tree and no sliding update.
* **amin, Cnt_d and #surv** come from my own exact big-integer DP.

The parts of the checker:
* **B.** Tested on 180 cases: 3x+1, 3x-1, 3x+5 and 3x-3; m in {14, 17, 20}; j in {1, 2, 3, 4, 6}; up to three split depths. In every case L <= N <= U against a numpy brute force, and Σ Cnt·|S|/2^j = #surv(m+j)/2^j exactly. The middle step of the proof, N = Σ_r Φ(3^A, T^d(r) mod 2^K), holds as an exact identity in 12 cases. The mutated multiplier 3^{A+1} breaks it in 12 of 12 cases, so the check can fail.
* **T: certified rows.** Reproduced by my independent code, to the printed 5 decimals:
  * Table 2 at m = 290, 751, 594 and 784 (K = 22);
  * sibling rows at m = 1000, K = 24: d = 5 (j = 2, 8), d = -3 (j = 4), d = 7 (j = 2) and d = -1 (j = 8), all by direct simulation of 3x+d, which independently confirms the conjugacy claim;
  * the new K = 28 rows: m = 1000, j = 11 ([-0.005050, +0.005045]) and m = 100, j = 12 ([-0.019234, +0.018776]);
  * the exact j = 1 constants at m = 1000 and 3000: 3.1842e-5 and 1.8321e-5. Both are <= 3.2e-5, as now claimed.

  The 3x-1 certificate equals the 3x+1 certificate exactly, and the 3x+5 certificate differs from it.
* **M.** #surv(2000)^10000 >= 2^{18 860 000}, so h0 >= 0.9430; numerically h0 is in [0.94300, 0.94350]. Supermultiplicativity holds for a, b < 120. The explicit form #surv(K) >= #surv(2000)^{floor(K/2000)} holds for every K <= 4100.
* **P.** At K = 20, for every depth d < 5000: th_i <= amin(i), and at most 13 = floor(Kλ)+1 slots are nontrivial. The bound is attained.
* **F.** Lemma F checked exactly in 180 cases with arbitrary S: random sets of density 0.02, 0.5 and 0.9, a residue class mod 8, and a survivor set. The cosets were 1, -1, 7 and -5, so the nontrivial coset -<3> is included. Max LHS/RHS is 0.065.
* **R.** <3> has index 2 in the units mod 2^K and does not contain -1, for K = 3..20. The reflection identity holds exactly. The mutated shift B - uN breaks it 421 times.
* **S.** σ >= τ for every n < 2^24. N_σ - N_τ = 1 for m <= 24 and b in [m, m+8], except m = b = 1, where it is 0.
* **D' core.** My own pattern enumeration gives 172 nontrivial (slot, interval) patterns at K = 16, as in the README. For three of them, my max/min over all 2^14 multipliers equals `disc allu` row by row.

## REFEREE1 items: were they honestly resolved?

| REFEREE1 item | resolved? |
|---|---|
| C: j = 5, 7, 9, 11 missing | **Yes.** Computed. I reproduce `data/certified_odd.txt` identically, and my independent code reproduces the m = 1000, j = 11 row. |
| C: j = 1 constant 2·10^-5 | **Yes.** Now 3.2·10^-5. I confirm the exact values 3.184e-5 and 1.832e-5 independently. |
| M: per-K bound from Fekete | **Yes.** #surv(K) >= #surv(2000)^{floor(K/2000)} follows from supermultiplicativity (induction plus #surv >= 1). So sqrt(#surv(K)) >= 2^{-1000 h0} 2^{h0 K/2}, which is exactly what Corollary D uses. |
| D: "count law of Conjecture E holds" | **Yes.** Withdrawn in the Results row, in Corollary D and in the "genuinely beyond" paragraph. All three now say τ-version, X = 2^m, density one, (h0/2 - η). |
| G: "verbatim" | **Yes.** The reflection identity is proved correctly: s ↦ N-1-s maps the line for -u onto the line for u shifted by -u(N-1), and (Z/2^K)^* = <3> ⊔ -<3> for K >= 3. Sibling certificates were computed and reproduced. The README states exactly what was and was not computed (m = 1000, K = 24, j <= 8 only). |
| σ: c_i >= 0 | **Yes.** Scoped to d > 0. |
| σ data nit | **Yes.** I confirm it for n < 2^24. See the new nit N3 on n = 0. |
| LB wording | **Yes.** |
| title scope | **Partly.** "In this census" was added, but see the new item N1. |
| P at d = 0, D' floats, O2 μ, n = 0 | **Yes.** All noted. The D' float tolerance argument is adequate; the thresholds themselves are exact. |

The revision table in section 9 describes what happened accurately. It also admits that the
original "every j <= 12" claim was unsupported at the time it was made.

## Verdicts

### R (reduction, uniform in the intercept): CONFIRMED

I re-derived each step:
* n = r + 2^d s enumerates [0, 2^m) exactly.
* F(n, d) = F(r, d).
* T^d(n) = 3^A s + T^d(r), so A_{d+i}(n) = A + A_i(x).
* Survival to depth m+j holds iff x mod 2^K ∈ S_{d,A}, where K = j + j' covers exactly the steps d+1, ..., m+j.
* The main identity follows from the bijection s ↦ 3^A s + B mod 2^K (taking s < 2^K), divided by 2^j.
* The error line holds because Σ Cnt·r_A·Φ̄ <= max r_A · Σ Cnt·Φ̄.

L and U use only Cnt_d (d < m) and the in-horizon sets S mod 2^K; no information about B is used. My
checker confirms the identity exactly, not only the bounds, and it can fail.

### C (certified instances): CONFIRMED_WITH_FIX (nit)

The computation is exact. My code, which is structurally different, reproduces every row I tested,
including the post-REFEREE1 K = 28 rows.

*Nit:* the Results row says "|δ| certified at most ... up to 0.019 (j = 12)". The certified value
at j = 12, m = 100 is 0.01923 > 0.019. Section 9 correctly says 0.0192. Write 0.0193, or "about
0.019".

### F (averaged discrepancy lemma): CONFIRMED

I re-derived each step:
* Fourier inversion, with the ξ = 0 term equal to Φ̄.
* The terms with v2(ξ) >= j' vanish, because N = 2^{j'} is a multiple of the period 2^j.
* For e = v2(ξ) < j', uξ/2^e mod 2^L is uniform on a coset of H_L, and |H_L| >= 2^{L-2}.
* |G| <= 1/(2||·||).
* Each odd b < 2^{L-1} occurs twice, which gives the factor 2^L/|H_L| <= 4.
* The harmonic bound 1 + (L-1) ln2/2, with 0.3466 >= ln2/2.
* Cauchy–Schwarz and Parseval.

The lemma holds for every S and every coset, which is how D uses it for 3x+d. It is correctly
described as a standard Erdős–Turán / large-sieve-type estimate.

### P, M: CONFIRMED

**P.**
* th_i = ceil({dλ} - 1 - k + iλ) <= ceil(iλ), so S_{d,A} ⊇ S_root.
* A slot is nontrivial iff th_K >= 1. Because th_i is nondecreasing in i, this happens iff k < Kλ - 1 + {dλ}, which leaves at most floor(Kλ)+1 slots.
* There are at most K+1 patterns per slot.

**M.** The concatenation argument uses ceil(x) + ceil(y) >= ceil(x+y), and it is correct. The explicit
per-K bound is correct.

### D (almost every octave, (h0/2 - η) log2 m extra digits, τ-version, X = 2^m): CONFIRMED

I re-derived each step:
* q = 2^{K-2} is the order of 3.
* Markov's inequality is applied per pattern, with E r <= g_K 2^j / sqrt(|S|) <= g_K 2^j / sqrt(#surv(K)), and then a union over the K+1 patterns of a slot.
* A_k(d) = ceil(dλ) + k is nondecreasing, takes each value at most twice (2λ > 1), and covers <= Mλ+2 consecutive integers. This gives the count <= 2(Mλ+2+q)|Bad|/q <= 2(Mλ+3q)|Bad|/q.
* The sum runs over n_s slots, and q <= M.

I also checked the Corollary:
* K = floor(log2 M)+2 gives q <= M and 2^K > 2M.
* The Lemma M bound gives the M^{h0/2}.
* Σ_{j<=J} 2^j <= 2(2M)^{h0/2-η}.
* The total is O((log M)^3 M^{1-2η/3}) <= M^{1-η/3}.
* K >= 2j holds because 2j <= h0 log2(2M) < K.
* M^{-η/3} <= 2 m^{-η/3} for η <= 3.

The statement is now scoped correctly: τ, X = 2^m, density one, not Conjecture E.

### D' (explicit densities at K = 16): CONFIRMED_WITH_FIX (wording)

Weyl applies to {dλ/q}, which jointly encodes (floor(dλ) mod q, {dλ}). The bad sets are finite unions
of point × interval. The table is reproduced, and the per-pattern core is independently confirmed.

*Wording fix:* the README says "These numbers use the worst slot." `analytic.py` actually sums the
measure of the bad set over all slots and patterns (a union bound). That is why the j = 2, ε = 0.01
entry exceeds 1 (1.216). Write "These numbers are a union bound over the slots (each slot at its
worst B)".

The extension of D' to every odd d is correct. The multiplier ±3^{A+t} shifts the first coordinate
by t, which preserves the product measure, and the sign is absorbed by the reflection identity.

### G (siblings 3x+d): CONFIRMED

The claims are:
* R holds for every odd d. I verified it by direct simulation of 3x-1, 3x+5 and 3x-3.
* D holds for every odd d, because Lemma F holds for every coset.
* D' holds for every odd d, by the reflection identity.
* C holds verbatim for 3x-1; I verified the certificates are identical.

All four are correct. The sibling certificates are what the README says they are. The conjugacy
T_d(x) = d·T_1(x/d) is checked here independently of the prover's code.

The extra cycles are harmless in the right way: they are O(1) starts, against a main term of about
2^{0.95m}. A sound argument should be insensitive to them, and this one is.

### O1: CONFIRMED (meta-statement)

### Bad multipliers: CONFIRMED as EVIDENCE

REFEREE1 reproduced this. I did not reproduce it separately beyond confirming `disc allu` on three
K = 16 patterns.

### O2 (all m): label honest, but CONFIRMED_WITH_FIX (missed easy strengthening; see N2)

"Theorem D for all large m" (error tending to 0) is indeed open. The Results row "All m, not just
almost all: OPEN" reads as if nothing beyond the horizon were known for every m. Something is: see N2.

### σ: lower bound CONFIRMED; the upper-bound data is CONFIRMED as EVIDENCE (with nit N3)

### LB: OPEN, honest

### Relation to 3x+1 (section 1, unlabelled): nit N4

## New items in this pass

**N1 (novelty wording).** The title claims "a first rigorous step beyond the horizon in this census",
and the text says "every density result in the census stops at depth m". The concurrent round-5 lens
`census/round5/fourier` (Theorem U-3x+1, unrefereed) also claims a proved statement 1 to 3 digits past
the horizon, for every b >= 22. Its bounds are weak (19.5%, 43.3% and 87.8% at j = 1, 2, 3). I have not
refereed it. *Fix:* drop "first", or add a sentence that the fourier lens has a concurrent, weaker,
all-depth bound. This is a priority wording point, not a mathematical one.

**N2 (an all-m theorem that follows from the prover's own tools).** Theorem R and Lemma P already
give an explicit bound for every m, at fixed j:
* The relative error at m is at most max_k r(3^{A_k} mod 2^K, pattern_k(m)).
* Each multiplier lies in the finite group <3> mod 2^K, and each pattern lies in the finite list of slot patterns.
* So the maximum of r over all 2^{K-2} multipliers and all patterns bounds the error for every m >= K - j.

I computed this at K = 16 with `disc allu`, over the 172 patterns (pattern enumeration in floats, as in
`analytic.py`; the scratch script was not shipped). For every m >= 16:

| j | bound on \|N(2^m,m+j)/2^mP(m+j) - 1\| |
|---|---|
| 1 | 0.122 |
| 2 | 0.284 |
| 3 | 0.466 |

These already beat the fourier lens's 0.195, 0.433 and 0.878 at the same j, and larger K would improve
them.

*Fix (recommended, not required):* restate O2 as "all m with error tending to 0: OPEN". Then either add
this worst-case all-m bound as a PROVED item (with an exact pattern enumeration), or at least mention
that it exists. It makes the honest claim larger, not smaller.

**N3 (σ data and n = 0).** Section 2 counts n = 0 in N. But σ(0) = ∞ (T(0) = 0 is never below 0), while
τ(0) = 1. So under the README's own convention, N_σ - N_τ = 2 (n = 0 and n = 1), not 1. The "exactly 1"
statement in section 7 and in the σ row holds for the brute-force convention n >= 1. *Fix:* say "n >= 1"
there. This does not affect any theorem.

**N4 (section 1, "Even τ(n) <= C log n for all large n would imply the Collatz conjecture").** The
statement is true, but it is not immediate. Suppose τ(n) = i. Then T^i(n) = (3^A n + c_i)/2^i with
c_i <= i·3^A/2. To get T^i(n) < n, one needs (2^i - 3^A) n > c_i, which requires a lower bound
2^i - 3^A >= 2^i i^{-κ}. That is a Baker-type estimate on linear forms in logarithms. The README quotes
the statement without proof or source. It is unlabelled context and is used nowhere. *Fix:* phrase it
with σ, as CONJECTURE.md does, or add "(via a Baker-type bound on |2^i - 3^A|)".

## Honesty of labels and novelty

The labels are honest:
* The PROVED items are proved.
* C is labelled as an exact computation, and it is one.
* The EVIDENCE items (bad multipliers, the σ upper bound) and the OPEN items (O2, LB, Conjecture E itself) are labelled as such.
* The status line correctly says the document was refereed once and revised.
* The limits section is candid: log log X digits only, almost all m, τ only, X = 2^m only, and split5_3 and K7 not done.
* No external number-theory constant enters a proof.

The only novelty issue is N1.

## needs_repair: false

There is no GAP and no WRONG. The remaining fixes are wording: the C rounding nit, the D' "worst slot"
phrase, N1, N3 and N4. There is also one recommended strengthening (N2). None of them changes a proof
or a PROVED statement.
