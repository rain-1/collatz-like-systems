# Referee 1 report: round6/cutoff_wide

Referee: independent agent (referee 1). I did not edit the prover's files. My own check is
`referee1_check.py`, written from scratch with no import of `cwlib`. It uses exact ints and
Fractions wherever a claim is exact. Run it with
`/home/riv/Code/collatz/census/round4/wpotential/.venv/bin/python referee1_check.py`. It takes
about 30 s, exits 0, and exits 1 on any failed assertion. It encodes the corrected values below,
so it would fail against the prover's H values for core13 and core135.

**Overall.** Nothing is claimed settled, and nothing is settled. The two general theorems hold
after small repairs. There is one numerical error in the EVIDENCE table (H for core13 and
core135). One stated explanation is false: "cycles fail (H2)". Several labels need tightening.
**needs_repair = true.**

## 0. Prover's checks (re-run)

| script | result |
|---|---|
| `check_entropy_code.py` | exit 0; table reproduced |
| `check_cutoff_instances.py` | exit 0; table reproduced |
| `check_mb_s3_27.py` | exit 0 (W = 010, D = 25, \|U\| = 84; growth fit 0.3245) |
| `count_nondesc.py --check` | exit 0 (DP = direct residue counts) |
| `count_nondesc.py 300` (run on a scratch copy) | reproduces the H_var column, **including the wrong core13/core135 values** (section 6) |

## 1. External theorem (Evertse 1984, Thm 2, eq. (14)): CONFIRMED, no longer "from memory"

I downloaded the Numdam PDF and rendered pp. 226 and 228 as images. The scanned display (14) reads

  (prod_{k=0}^n prod_{v in S} ||x_k||_v) prod_{v in T} ||x_0 + ... + x_n||_v
      >= C (prod_{v in T} max(||x_0||_v, ..., ||x_n||_v)) ||x||^{-eps}.

The hypothesis (13) says every nonempty subsum is nonzero, singletons included. C depends only on
(eps, S, K, n). By eq. (2) on p. 226, ||x|| = max_k |x_k| for K = Q. This is exactly the form
quoted in theorem_W.md section 4, with H(x) = max_k |x_k|. The "quoted from memory" caveat in
README "Honest limits" and theorem_W.md section 4 can be replaced by "verified against the scanned
p. 228". The theorem is ineffective (Subspace Theorem), as stated.

## 2. Theorem W: CONFIRMED_WITH_FIX

I re-derived Steps 1-4 line by line against the split5_3 original (split5_3_s27.md, "Large jumps
and stretches of consecutive exits"). The generalization replaces positivity of tau_i with
|tau_i| <= C. That is legitimate, because positivity was only used to bound absolute sizes.

These steps are verified:
* the pairing identity of Step 2. It is also checked exactly in `referee1_check.py` section D, on
  random two-piece rotation schedules with a jump, for 3x+1, core13 and m3_b (p = 3);
* tau_{i+q} = gamma^{-1} tau_i;
* the bound |1 - gamma| >= p^{-k_E} l^{-max(0,-k_A)}, also checked exactly;
* the geometric-piece sum (tau_first - g tau_last)/(1 - g), with g != 1 by unique factorization;
* protection of the leading term, and the deletion argument;
* the bookkeeping r(x_0)/|x_0|_p, which gives the factor |ZF|_p. It cancels as claimed: what
  remains is D_0 D_1 D_2 · num(F) · |y| |y|_l <= |y| p^{O(delta N)};
* the final inequality (3).

The identity (1) holds exactly on actual integer orbits (section D).

**Fix needed (truncation step).** The proof truncates "after the first step with E_j >= (1 +
eta/2) log_p|y|". It then uses (a) E <= (1 + eta/2) log_p|y| + e_max and (b) "Truncation keeps
(H1)-(H4)". The setting allows any e >= 0 per step, so e_max is undefined. (H3) is stated only for
the whole path (N <= C(E+1)), so it is not hereditary: a prefix could carry many division-free
events. Two hypotheses should be added:

* **(H0)** e_j <= C for every step;
* **(H3)** required for every prefix.

Both hold in every instance. Each exit divides, so N_j <= E_j. Steps are single cylinder-graph
edges or single blocks C, X, so e is bounded, and C^k is split into k copies of C. |A_j| = O(E_j)
because there is no division-free cycle. With these hypotheses the proof is correct.

Minor: n_terms should count J·(2/delta) short-piece singletons, not 2/delta. It stays bounded.

**Sharpness remark.** "Coefficient 1 sharp" is correct as stated. It needs the least lifts to be
unbounded, which holds because each integer follows one walk.

## 3. Lemma R: CONFIRMED_WITH_FIX

The algebra is right:
* K_{i+q} - K_i - k = floor(phi_i + eps) + w(phi_i + eps) - w(phi_i);
* gamma = lambda_C^{k - kappa q};
* k_E = e_C k + e_X q >= 1;
* bounded geometry holds.

The window count is wrong. With Q = floor(delta|I'|), the number of windows ceil(|I'|/Q) is not
<= 1/delta + 2. For example, delta = 1/6 and |I'| = 17 give 9 windows, against 8 (2122 cases are
listed in section E). The correct bound is 2/delta + 1, because Q >= delta|I'|/2 when delta|I'| >= 2.

The stated M(delta) = 2(2J+1)(1/delta + 2) still holds. Each exceptional set is a *half-open*
arc of length Delta: [1 - Delta, 1) or [0, Delta) for the floor, and [c - Delta, c) or
(c, c + Delta] for a cut. Q consecutive phases are pairwise at least Delta apart, so such an arc
holds at most 1 phase per window. This gives at most (2J+1)(2/delta + 1) <= 2(2J+1)(1/delta + 2).
Fix: replace "closed arc ... at most 2" and "<= 1/delta + 2 windows" with this argument. The
random tests in section D stay within both bounds (max 7 exceptions per piece).

## 4. Instances (13 systems + 3 controls): CONFIRMED_WITH_FIX

For all 15 table systems I recomputed, independently:
* x* (exact periodic rational);
* lambda_C;
* the existence of an off-cycle closed walk of G_m with the claimed W slope;
* kappa_W.

All match (section A). mb_s3_27 also matches: W0 = 010 has slope 3/8 and kappa = 8.3274.

* **Error.** The split5_3 row gives "exits y/2 + 3/2, y/2 + 3: kappa = 6.2126 (repo)". The exits
  have slope 1/2 and lambda_C = 5/4. So kappa = log 2/log(5/4) = 3.1063, which is the repo's
  kappa = 1/log_2 s (split5_3_s27.md line 810). The value 6.2126 is 2·kappa, and the repo's
  T = 2·kappa + 1 = 7.2126. Fix the number.
* The instances are genuine consequences of Theorem W (with the fix in section 2) plus Lemma R.
  None of them says anything about convergence. The 3x+1 instance does not settle 3x+1 and does
  not claim to. It excludes only one zero-entropy family from large starts.

## 5. "Cycles fail (H2)": WRONG as stated (README line 32 and "What the ineffective constant gives"; theorem_W.md section 6)

Expanding integer cycles *satisfy* (H1)-(H4). Section F checks this exactly:
* 3x-1: the cycles 5, 7, 10 and 17, ..., 34 around x* = 1;
* 3x+1: the cycles -5, -7, -10 and -17, ... around x* = -1.

Each, from its cycle-lemma rotation, is one geometric piece with one label. Its |tau_i| <= 0.47,
its shifted start |y_0| is 4 or 16, and E is unbounded. The identity (1) holds exactly.
(H2) fails only for *contracting* cycles. theorem_W.md line 166 says this correctly; README and
section 6 do not.

Theorem W remains consistent only because y_* is ineffective: it must exceed every such shifted
start. This is the real reason it "says nothing about cycles". The fix is to reword it: "expanding
integer cycles satisfy (H1)-(H4) from bounded starts. They are compatible with Theorem W only
through the threshold y_*, so Theorem W cannot exclude any finite set of cycles."

## 6. Entropy table: WRONG for core13 and core135, other values CONFIRMED (EVIDENCE)

`count_nondesc.H_variational` minimizes s(theta) over theta in [0, 3] only. For core13 and core135
the minimizer lies outside that range:

| system | stated H | true variational H | minimizer theta | own exact-count fit |
|---|---|---|---|---|
| core13 | 0.4565 | 0.4281 | 4.65 | 0.4252 (E = 300 to 600); 0.4271 (1200 to 2400) |
| core135 | 0.3755 | 0.3593 | 4.00 | 0.3564; 0.3582 |

The stated values are s(3), not the minimum. I confirmed this with both numpy and my own
power-iteration code. The prover's own H_fit (0.417, 0.347 at E = 300) already disagreed.

For every other system the minimizer is below theta = 1, and my fits agree with the stated values
within the usual finite-E offset. Those systems are 3x+1, split5_3, split5_1, m3_b, K7, core57,
core157, core357 and core17. For 5x+1 and coreW, H = 1.

Corrections:
* crit = 1/(1 - H) becomes 1.75 (core13) and 1.56 (core135);
* README line 35: "H = 0.428 and 0.359";
* README "What stayed open": "H >= 0.36", not 0.37;
* theorem_P.md quantification table.

The qualitative conclusions do not change. These two cores are still the lowest-entropy systems
computed, and H is still far above every proved cutoff family.

My own exact DP agrees with direct residue enumeration for E <= 11 (6 for p = 3) on 8 systems.

## 7. Theorem P: CONFIRMED (item 4 CONFIRMED_WITH_FIX)

* Type (c) gives an internal edge off C (trichotomy.md definitions).
* The cycle-lemma rotation is correct: start after the last minimum.
* The prefix-slope argument for {U, V}^* is correct.
* Distinct walks give disjoint balls, by (M).
* The mass-distribution argument for dim >= s is correct. In the ultrametric setting a ball meets
  at most one child chain.

I built the code independently for core13 and core135, with my own rotation, BFS re-entry and
minimal D. It gives the same |U|, eU/eV and s (0.0200 and 0.0106). Random {U, V}^5 words are
realized by integers, checked by direct iteration on three lifts each.

Item 4 cuts each walk "at its E-th division". That needs e_r <= 1 per step. Otherwise a step can
jump past E. All census systems here have e <= 1. Either state this, or say "at least E divisions,
interval length p^{K+E+e_max}".

Hypotheses are respected: Theorem P needs unit multipliers for (M) and the standing hypothesis.
Both are stated via trichotomy.md.

## 8. Converse (dim 0 iff no type (c)): CONFIRMED

In a type-(a) SCC the potential (★) bounds multipliers, so p-adic points need no positivity.
Type-(b) points are preimages of finitely many x* under injective affine branches.

README line 13-14 ("then Theorem H already settles the system") must add the hypotheses that
theorem_P.md states: positive integers map to positive integers, and the standing hypothesis.

## 9. Lemma Q: CONFIRMED

The counting is correct. A sanity check finds exactly n + 1 distinct one-piece rotation words for
the 3x+1 kappa (section H).

## 10. Corollary P1: CONFIRMED_WITH_FIX

The corollary claims the fraction of words that are "rigid in the sense of Theorem W, for any
fixed (J, B)" is at most (cE)^{c'J} 2^{-E/max e}. Lemma Q, however, counts only the Lemma R normal
form (rotation pieces and geometric pieces). Theorem W's (H4) shift pieces are more general.
README line 11 ("The rigid families covered by Theorem W have only polynomially many words") has
the same overreach.

There are two fixes:
1. Restrict the statement to Lemma R / Lemma Q families.
2. Add a short lemma for general (H4) shift pieces, giving 2^{o(E)} rather than poly(E). Sketch:
   given delta, a piece of length n is determined by
   * q <= delta n;
   * its first q symbols (c_i, A-increment, E'-increment), which come from a finite alphabet by
     bounded geometry;
   * at most M(delta) exceptional positions and values.

   That is at most exp(O(delta n) + O_delta(log n)) choices for every delta.

Either way the exponential-smallness conclusion survives.

## 11. Proposition B (mb_s3_27): CONFIRMED_WITH_FIX

These checks pass in section G, using my own code:
* the skew-product lemma, checked on all n in [-3000, 3000);
* C = 110 at states 22 -> 22 and W = 010 at 22 -> 22, both avoiding 26;
* U = C^25 (010)^3 and V = C^28 have length 84, all prefix slopes > 1, and D = 25 is minimal;
* random {U, V}^3 words are realized by integers that are never blocked.

The dimension bound 1/84 is correct.

**Fix.** "Dimension at least 1/84 inside each 27-class" is false for the class 26, which is blocked
at once. It is true for the other 26 classes, since every s != 26 reaches 22 avoiding 26 (checked).
Say "inside each class s != 26 (mod 27)".

The growth exponent 0.32 is labelled EVIDENCE, and the never-blocked count is a valid lower bound.

## 12. Labels, coverage and novelty

* "Outcome: no system was settled": CONFIRMED. No cycle lists are claimed, so no brute-force cycle
  verification is required. As a sanity check, every x* used is an exact periodic point of the
  stated slope.
* "The cutoff method cannot by itself decide any system in this class" (README line 19):
  overstated. What is proved is that a *cylinder-level* rigidity reduction is impossible
  (Corollary P1). Arguments that use the integer start are not excluded, as the README itself says
  in "What stayed open". Reword to "cannot be completed by a cylinder-level rigidity reduction".
* "Explicit escaping code / escaping family" (README line 35, theorem_P.md lines 10 and 190): a
  misnomer. {U, V}^* is a family of *non-descending* p-adic words. Nothing is shown to escape.
* "Smallest in the census" (README line 35): supported only among the systems computed here and in
  the round4/lundberg table. Say so.
* README "What stayed open" says the multi-shift exponent is "below 0.03 per division". With the
  repo's T = 2·kappa + 1 = 7.2126, log_2 3/(6T) = 0.0366. Say "below 0.04".
* Novelty: "not checked" is stated honestly. Theorem P and its converse are elementary. For 3x+1,
  positive dimension of the set of 2-adic points with infinite stopping time is presumably
  classical (Terras/Lagarias tail 2^{-0.05k}). The novelty caveat should cover Theorem P too, not
  only Theorem W.
* Instance rows marked "PROVED" depend on Evertse. That is now verified (section 1), so the label
  is acceptable.

## Verdicts

| claim | verdict |
|---|---|
| Evertse Thm 2 (14) as quoted | CONFIRMED (verified from the scan; drop "from memory") |
| Theorem W | CONFIRMED_WITH_FIX (add e_j <= C and hereditary (H3); n_terms count) |
| Lemma R | CONFIRMED_WITH_FIX (window count is 2/delta + 1; half-open arcs; stated M survives) |
| Instances (16 rows) | CONFIRMED_WITH_FIX (split5_3 kappa is 3.1063, not 6.2126) |
| "cycles fail (H2)" | WRONG (expanding cycles satisfy (H1)-(H4); only y_* excludes them) |
| Theorem P items 1-3 | CONFIRMED |
| Theorem P item 4 | CONFIRMED_WITH_FIX (needs e <= 1 per step) |
| Converse | CONFIRMED (README must add Theorem H's hypotheses) |
| Lemma Q | CONFIRMED |
| Corollary P1 / "Theorem W families are polynomial" | CONFIRMED_WITH_FIX (restrict to Lemma R families or prove 2^{o(E)}) |
| Proposition B | CONFIRMED_WITH_FIX ("each 27-class" -> "each class != 26") |
| H table, core13 / core135 | WRONG (0.428 / 0.359; theta grid truncated at 3) |
| H table, other systems | CONFIRMED (EVIDENCE) |
| "no system settled" | CONFIRMED |
| "cutoff cannot by itself decide any system" | CONFIRMED_WITH_FIX (cylinder-level only) |
| "escaping code", "smallest in census", "< 0.03" | CONFIRMED_WITH_FIX (wording and numbers) |
