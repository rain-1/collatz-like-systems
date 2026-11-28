# Referee report: round 3, lens "density"

Referee files (new; none of the prover's files were modified):
* `referee_check.py`: independent exact check, written from scratch. It imports nothing from
  `density_lib.py`, `check_density.py` or `make_certificates.py`. It reads `certificates.json` and
  uses `systems.py` only to compare step functions. **Exit 0, about 16 s.**
* `referee_evidence.py`: EVIDENCE only (simulation), about 1 min.

## 1. What I ran

| script | result |
|---|---|
| `check_density.py` (prover) | exit 0, ALL CHECKS PASSED, **179 s**. The docstring says "60–90 s"; the README says 3.5 min. It is over the 2-minute target, and the README says so. |
| `check_hypH.py` (prover) | exit 0, a few seconds |
| `referee_check.py` (referee) | exit 0, REFEREE CHECKS PASSED, 16 s |
| `referee_evidence.py` (referee) | EVIDENCE, see §4 |

What `referee_check.py` tests independently:
* **[R1]** I wrote 38 step functions from the rule text in the claims and README. They agree with the
  prover's tables on `1..30000` and on 300 random 120-bit inputs per map. The prover's
  `check_density.py [1]` also matches the tables against `census/systems.py` and the round-2
  descent catalog.
* **[R2]** My own state-graph builder uses a more liberal decision rule (`w | u·a`, where the prover
  uses `w | K`). It gives **the same state count, the same `G_max` and the same exact drift vector**
  for all 38 maps. I tested Lemma 1 ("children depend only on the state") directly: for every state,
  6 random representatives `(a, b) = (K·u0, β + K·m)` with `u0` up to 10^6 and `m` up to 10^12 give
  identical child multisets. I also checked faithful abstraction by iterating the map directly on
  25 random 150-bit `n` per map, to depth 40.
* **[R3]** I recomputed the exact stationary law, Δ and Λ, and confirmed that each graph has exactly
  one closed class. Every closed form for `c_0` in `results.md` matches to 1e-12. That covers all
  38 maps, including div235's `40165 ln7/(80330 ln2+27334 ln3+14445 ln5)`.
* **[R4]** Every certificate in `certificates.json` passes `N_{s,γ} w ≤ w` exactly. I checked this
  with my own rigorous upper bounds: binary-search integer k-th roots, 60-bit denominators, no
  floating point. I checked it with the prover's `w` and also with a `w` I built myself, so every
  claimed θ is reproducible. θ = 1 − γ + s(1 − c) is recomputed, and the parameter ranges each
  theorem needs are checked: `c_0 < c < 1` for Korec; `c < c_0` and `η > 0` for sharpness;
  `1 < c < c_0` for expanding maps.
* **[R5]** I tested the deterministic part of Theorems 1, 4 and 5 on random 200–400-bit `n`:
  * Theorem 1: a first crossing below 1/2 gives an actual iterate `< n` (direct iteration).
  * Theorem 4: a first crossing below τ gives an iterate `< n^c`, checked as the exact integer
    comparison `x^den < n^num`.
  * Theorem 5: a non-exceptional `n` gives an iterate `> n^c`.

  No counterexample was found. For some maps the Korec crossing at τ ≈ n^{c−1} was not reached at
  400 bits. That is expected, since θ_c is about 0.9996.
* **[R6]** I recomputed the Theorem 6 bounds with my own DP. At depth 300 they reproduce
  [0.823782, 0.824073] (5n+d, 10n+2), 0.699249 (7n+1, 7n+7), 0.613870 (9n+1) and
  [0.722567, 0.722571] (m3_e). At depth 400 I get **[0.823922, 0.824002]** for 5x+1. That
  confirms the narrower interval the prover quoted from `make_certificates.py`, which the prover's
  own check does not re-verify.
* **[R7]** For every contracting single-prime map with more than one state (split5_1, split5_3,
  desc_s32_plus9, desc_split7_1), the graph has **no transient states**: it is irreducible. The
  minimum of ρ(P_s) reproduces θ* = 0.93685, 0.58068, 0.56976 and 0.75348.

## 2. Line-by-line review of `theory.md`

**Lemma 1: CONFIRMED.** The residue-set argument (`u0` is a unit mod N/gcd) is right. The
state-transition computation for a decided row (`ub+v mod u_P K` depends only on β) is right. For a
split, the lifts form the set `{β + Kj}` (the multiset of children is a function of the state, though
the digit-to-child map depends on b mod qK); that is all the proof needs. The prover's decision
condition `w | K` is conservative but valid; with the liberal condition the graphs come out identical.

**Lemmas 2–4: CONFIRMED.** I re-derived each one:
* Lemma 2: the change at each replacement is ≤ 0.
* Lemma 3: `B_i/A_i = Σ G_l/A_{l+1}`, with the last term bounded using `A_i < τ`.
* Lemma 4: depth ≤ k, `M < q_max Y`, at most one integer of the block per class.

**Theorem 1: CONFIRMED.** I checked `k_0` (strict inequality `(1−c_*)n > kG_max`). I checked that
`k_i ≥ 1` because the value is not n. I checked the count bound via `μΦM^{1−γ} = A^s w` and the
geometric sum `2^θ/(2^θ−1)`. The Haar statement and Corollary 1.1 are right. Signed intercepts
(3n−1, m3_b) are covered because only `|G|` enters.

**Theorem 2: CONFIRMED.** I checked:
* the strict monotonicity in γ;
* the log-convexity (entries are sums of exponentials of affine functions);
* `f = max_D f_D`;
* that transient components have ρ < 1 at (0,0);
* the gradient (Δ, Λ) at a simple Perron root;
* the tangent-plane argument for Δ ≥ 0.

The "single closed class" hypothesis is verified for all maps ([R3]).

**Theorem 3: CONFIRMED_WITH_FIX.**
* *The proof silently uses a hypothesis that (H) does not state.* The upper bound uses ρ(P_s) of the
  **whole** graph. The lower bound tilts only on the closed class C (Perron vector "on C"). So the
  argument gives the lower exponent `1 + min_s log_p ρ_C(P_s)`. That equals θ* only if ρ(P_s) = ρ_C(P_s)
  near s*. A transient component with larger ρ at s* would break the equality as written.
* *Fix:* add to (H): "ρ(P_s) is attained on C for s near s*", for instance "G(T) is irreducible".
  This holds for all 17 maps Theorem 3 is applied to: single-state graphs, plus four 2–8-state graphs
  with no transient states ([R7], exact SCC computation).
* *The second half of (H) follows from the first, so the "numerical only" caveat can be dropped for
  these 17 maps.* For an irreducible graph, ρ(P_s) is a simple Perron root, so log ρ(P_s) is
  analytic and convex in s. Its derivative at s = 0 is Δ < 0. It tends to +∞ because the exact
  pumping cycle of (H) part 1 has product > 1, so `tr P_s^L ≥ p^{−L} Π^s`. So the set of minimisers
  is a nonempty compact interval in (0, ∞). Taking s* to be its right end, the derivative is > 0 to
  the right of s* and tends to 0 as s₁ ↓ s*. That is all the proof uses; uniqueness is not needed.
* The rest of the tilting argument is right: the identity `p^{−m} = Q·ρ₁^m·(h(σ)/h(end))·A^{−s₁}`,
  the a.s. positive drift, and the two probability estimates.

**Theorem 4: CONFIRMED.** I checked `τ ≤ n^{c−1}/2` on the block, the requirement `Y^c ≥ 2kG_max`,
and the count `τ^{−s} Σ A^s`. The existence argument along `t(1, 1−c+η)` gives `θ_c ≤ 1 − tη`.
c₀ = log₄3 for 3x+1 is the threshold Korec is credited with in Tao's arXiv:1909.03562 abstract and
introduction.

**Proposition 4.2: CONFIRMED.** At an exceptional node, γ < 0 gives `M^γ ≥ (q_max Y)^γ`. The bound
is `count ≤ q_max Y · mass`. On non-exceptional paths, `x_i ≥ A_i n/2 ≥ Y^{c−1} n ≥ n^c`. The window
`c−1 < g < Δ/Λ` is nonempty iff `c < c₀`.

**Theorem 5: CONFIRMED.** I checked:
* `N_{s,0} ≤ 2^{−γ} N_{s,γ}` for γ ≥ 0, which gives the E2 supermartingale;
* the E1 count;
* that `ε ≤ (1−θ₁)/s'` makes `θ_c = 1 − εs'`;
* that `x_cut ≥ 2(2Y)^{c−1}n > n^c`, using c > 1 and n < 2Y;
* that `g ∈ (c−1, Δ/Λ)` is positive, so γ ≥ 0.

Signed intercepts are fine, since only |B| is used. The closed-form c₀ values (log₄5, log₄7, log₂3,
(5/3)log₃2, (2/3)log₂3, (2/3)log₃7) are verified in [R3].

**Theorem 6: CONFIRMED_WITH_FIX.**
* *The upper-bound proof only covers block endpoints.* It shows that the block `[p^j, p^{j+1})`
  contains at most `(p−1)p^j q` elements of D_early. That bounds `#(D_early ∩ [1,X])/X` only at
  `X = p^{j+1}`. For X inside a block, the classes in S_j are not equidistributed over
  `[p^j, X]`; the trivial error is `#S_j ≈ q p^j`, which is of the order of X. So "natural density
  exactly q" is not yet proved.
* *Fix (complete):* for `X ∈ [p^j, p^{j+1})` and fixed L, split S_j into
  1. the lifts of S_{j−L}. These depend only on n mod p^{j−L}, so on `[p^j, X]` they number
     `≤ μ(S_{j−L})(X−p^j) + p^{j−L} ≤ q(X−p^j) + X p^{−L}`;
  2. `S_j \ lift(S_{j−L})`. This part has at most `(p−1)p^j (μ(S_j) − μ(S_{j−L}))` elements, and
     that is o(p^j) as j → ∞ because μ(S_i) ↑ q.

  Adding the full blocks below p^j gives `limsup ≤ q + p^{−L}` for every L, hence `≤ q`.
* The lower bound (a finite union of residue progressions of density q_L → q) is fine as written:
  the conditions are `B ≥ 0` (all `G_e ≥ 0`; `Gmin = 0` was checked for every map it is applied to)
  and `n > max(B/(1−A), p^L)`.
* The numerical bounds are reproduced exactly ([R6]).

**Proposition 7: CONFIRMED** (elementary). The first sentence of the statement in `theory.md`
contains an editing remnant ("For any table map with finitely many... precisely:"); it is cosmetic.

## 3. Per-system claims

All system claims are **density statements** about existing catalog entries. **No new system is
introduced and no GLOBAL question is settled.** The prover says so prominently and correctly.
Against the round-3 goal ("crack new systems"), this lens is a theory and tooling contribution, not
new settled systems.

| claim | verdict | note |
|---|---|---|
| div235_7n1 θ = 857/913, c₀ = 0.71732 | CONFIRMED | "method-optimal" here means the optimum over Theorem-1 certificates (Theorem 2a). Theorem 3 (exactness) is single-prime only and does not apply to mixed-prime maps. |
| div23_5n1 θ = 453/527, c₀ = 0.69135 | CONFIRMED | |
| div23_7n1 θ = 999/1000, c₀ = 0.95133 | CONFIRMED | |
| m3_b, m3_d θ = 521/540, c₀ = (4/3)log₃2 | CONFIRMED | |
| m3_g θ = 1906/1907, c₀ = (2/3)log₃5 | CONFIRMED | |
| 3n+d family, 6n+2: θ = 1082/1139, c₀ = log₄3 | CONFIRMED | This is a sanity check reproducing classical values (Terras exponent H(log₃2) = 0.949955; Korec). It is not new. |
| split5_1 994/1061; split5_3 457/787; desc_split7_1 703/933 ("the method's limit") | CONFIRMED (limit claim: with the Theorem 3 fix) | The graphs are irreducible, so Theorem 3 applies after the fix. |
| desc_m3_4n5 432/577; desc_s32_plus9 780/1369 | CONFIRMED | |
| 5n+d / 10n+2, 7n+1 / 7n+7, 9n+1, m3_e: rise threshold and q | CONFIRMED (q density: with the Theorem 6 fix) | The depth-400 interval [0.823922, 0.824002] is re-verified here. |
| perm_1932 family (Theorem 5 sample c) | CONFIRMED | |
| Conjecture: density(D) = q (EVIDENCE) | correctly labelled EVIDENCE | |

## 4. Evidence observations (referee_evidence.py)

* For 5x+1, the share of n in [2^16, 2^17) that drop within 20000 steps is 0.82304. The prover's
  evidence.out gives 0.82410 on [2^17, 2^18). Both are within about 1σ (σ ≈ 0.001) of
  q ∈ [0.82392, 0.82400]. This is consistent with the conjecture, and is EVIDENCE only.
* The D_early proportion up to 2^17 is 0.764, and up to 1.5·2^17 it is 0.767. It is still well below
  q: convergence is slow, since only crossings at depth ≤ 17 count. There is no conflict with
  Theorem 6.

## 5. Literature and novelty

The novelty statements are honest ("novelty not checked"; Terras, Matthews–Watts and Venturini are
marked as cited from memory). Referee caution:
* The *qualitative* statement of Theorem 1 for general maps (density-1 finite stopping time when the
  Markov drift is negative) is very likely classical, in the generalized-Collatz literature of
  Matthews–Watts (1984) and Venturini. The Theorem 1 summary should not suggest that this part is new.
* What is plausibly new is the explicit power-saving exponent for each catalog map, the optimality
  statement (Theorem 3), the general Korec-type and expanding-side thresholds (Theorems 4 and 5), and
  the exact certificates. I did not check this against the literature (no web search was done).

## 6. Recommended (non-blocking) edits for the prover

1. Theorem 3: add the irreducibility (C-dominance) hypothesis, and replace "second half of (H)
   checked numerically" with the convexity argument in §2.
2. Theorem 6: insert the partial-block argument from §2.
3. Fix the `check_density.py` docstring runtime (it says 60–90 s; the actual time is about 180 s).
4. Fix the stray text in the first line of Proposition 7.
