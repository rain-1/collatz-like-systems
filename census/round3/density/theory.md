# Density theorems for Markov table maps (round 3, lens "density")

This file holds every general statement of the lens with its proof. Per-system numbers are in
`results.md`; the machine-checked finite content is in `check_density.py` (exact) and
`evidence.py` (floating point, EVIDENCE only).

Status labels: **PROVED** = complete proof here plus exact check of all finite content.
**EVIDENCE** = numerical only.

---

## 0. Setting

A *table map* is `T(n) = (u_r n + v_r)/w_r` for `n ≡ r (mod Q)`, with integers `u_r ≥ 1`, `w_r ≥ 1`,
`w_r` a product of primes dividing `Q`, and `w_r | u_r n + v_r` for every `n ≡ r (mod Q)`. Write `P`
for the set of primes of `Q`. We assume `T` maps positive integers to positive integers (true for
every system treated). `u_r` may contain primes of `P` (e.g. `10n+2`).

Haar measure `μ` on `Ẑ_P = ∏_{p∈P} Z_p` gives the class `n ≡ r (mod M)` (M a `P`-number) mass `1/M`.

## 1. The adaptive digit tree and its state graph

A **node** is a tuple `(M, r, a, b, k)`, `M` a `P`-number, `0 ≤ r < M`, with the invariant

> `T^k(M t + r) = a t + b` for all integers `t ≥ 0`.

Its *real form* is `x = A n + B` with `A = a/M` (the **slope**) and `B = b − a r/M`; indeed
`a t + b = (a/M)(Mt + r) + b − ar/M`. The root is `(1, 0, 1, 0, 0)`: `A = 1`, `B = 0`.

The **state** of a node is `σ = (K, β)`, where `K` is the `P`-part of `a` and `β = b mod K`.
Write `a = K u₀` with `u₀` prime to `P`.

**Lemma 1 (faithful abstraction).**
1. *Deciding a branch depends only on σ.* For a `P`-number `N`, the values `a t + b` (`t ≥ 0`)
   meet exactly the residues `≡ β (mod gcd(K, N))` modulo `N` (because `u₀` is invertible modulo
   `N/gcd`). Hence all values of the node use one table row iff all `r' ≡ β (mod gcd(K, Q))` use
   one row, and then the division by `w` is exact for every `t` iff `w | K` (and `w | uβ + v`).
2. *Applying a decided branch* `x ↦ (ux+v)/w` gives the node `(M, r, ua/w, (ub+v)/w, k+1)`.
   Its state is a function of σ: the new `K' = P`-part of `uK/w`, and
   `(ub+v)/w mod K'` depends only on `ub + v mod wK' = u_P K`, where `u = u_P u₀'`,
   and `ub mod u_P K = u_P (u₀' b mod K)`. The real form changes by `A' = (u/w)A`,
   `B' = (uB + v)/w`.
3. *Splitting by a prime q ∈ P*: put `t = q t' + e`, `e = 0..q−1`. The children are
   `(qM, r + Me, qa, b + ae, k)` with states `(qK, β + K·(u₀ e mod q))`; `e ↦ u₀e mod q` is a
   bijection, so the q children are the q states `(qK, β + Kj)`, `j = 0..q−1`, each of Haar
   mass `μ(parent)/q`. Splitting does not change `(A, B)`.

The tree used everywhere: from a node, apply decided branches as long as possible; then split by
the first prime `q` (in a fixed order) with `v_q(K) < v_q(Q)`. By Lemma 1 the multiset of
children (state, slope factor `F`, intercept `G`, number of raw steps), where a child's real form
is `A_child = F·A`, `B_child = F·B + G`, depends only on the parent's state. Collecting these
gives a finite directed multigraph **G(T)** (when the breadth-first construction terminates; the
tool reports failure otherwise). Each state σ has a split prime `q(σ)` and exactly `q(σ)` out-edges.
**Single-prime maps** (`P = {p}`) have every `q = p`; then "depth j" = "class modulo `p^j`".
**Mixed-prime maps** (div23, div235) split by 2, 3 or 5 as needed; this is the right tree for
them: e.g. for `div23_5n1` the 5 states are `(1,0)`, `(2,1)`, `(3,1)`, `(3,2)`, `(6,·)` variants
built automatically (see `certificates.json`, field `states`).

`check_density.py [2]` builds the concrete integer tree to depth 12 (p=2), 8 (p=3) or 9 (mixed)
for every system and checks: the state, `A`, `B` predicted by G(T) equal the exact ones, and
`T^k(Mt+r) = at+b` at `t ∈ {0, 1, 7, 1000003, random 80-bit}`.

**Notation.** `G_max = max_e |G_e|`, `q_max = max q`. For real `s, γ` define the matrix

> `N_{s,γ}[σ, σ'] = Σ_{edges e: σ→σ'} q(σ)^{γ−1} F_e^s`.

`N_{0,0}` is the (stochastic) digit chain. `ρ(·)` is the spectral radius.

**Lemma 2 (supermartingale).** Let `w > 0` on states with `N_{s,γ} w ≤ w` entrywise. Put
`Φ(ν) = A_ν^s w(σ_ν) M_ν^γ`. For every finite cut `C` of the tree (a finite set of nodes meeting
each infinite path exactly once), `Σ_{ν∈C} μ(ν) Φ(ν) ≤ Φ(root) = w(σ_0)`.

*Proof.* Replacing a node ν by its q children changes the sum by
`μ(ν) A^s M^γ (Σ_e q^{γ−1} F_e^s w(σ_e) − w(σ_ν)) ≤ 0`, since a child has mass `μ(ν)/q`, slope
`A F_e`, modulus `qM`. Every finite cut is reached from `{root}` by finitely many replacements. ∎

**Lemma 3 (first crossing).** Along a path root = ν_0, ν_1, …, the real intercepts satisfy
`B_{l+1}/A_{l+1} = B_l/A_l + G_l / A_{l+1}`, `B_0 = 0`. If `A_l ≥ τ` for `1 ≤ l < i` and
`A_i < τ` then `|B_i| ≤ i G_max`.

*Proof.* `B_{l+1} = F_l B_l + G_l` and `A_{l+1} = F_l A_l`. So
`|B_i| ≤ A_i Σ_{l<i−1} G_max/A_{l+1} + |G_{i−1}| ≤ A_i (i−1) G_max/τ + G_max < i G_max`. ∎

**Lemma 4 (cuts at scale Y).** For `Y = 2^k` let `C_Y` be the set of nodes with `M ≥ Y` whose
parent has `M < Y` (or the root if `Y = 1`). Every positive integer lies in exactly one class of
`C_Y`; each `ν ∈ C_Y` has depth `≤ k` and `M_ν < q_max Y`; and each class of `C_Y` contains at
most one integer of `[Y, 2Y)`. (Depth `i` forces `M ≥ 2^i`, and the parent has `2^{i−1} ≤ M < 2^k`.)

---

## Theorem 1 (never-dropping starts; general, PROVED)

Let `H(X) = #{1 ≤ n ≤ X : T^k(n) ≥ n for all k ≥ 1}`. Suppose `s > 0`, `0 ≤ γ ≤ 1` and rational
`w > 0` satisfy `N_{s,γ} w ≤ w`. Put `θ = 1 − γ`, fix `c_* ∈ (0,1)` (we use 1/2), let `k_0` be the
least `k` with `(1−c_*) 2^m > m G_max` for all `m ≥ k`. Then for all `X ≥ 1`

> `H(X) ≤ 2^{k_0} + C_1 X^θ`,   `C_1 = w(σ_0) q_max^θ c_*^{−s} / w_min · 2^θ/(2^θ − 1)`.

Moreover every `n ≥ 2^{k_0}` outside the counted set drops below itself within the raw steps of
its cut node (`O(log n)` steps), and the Haar measure of the set of `P`-adic points whose slope
never falls below `c_*` is 0.

*Proof.* Fix a block `[Y, 2Y)`, `Y = 2^k`, `k ≥ k_0`, and `n` in it. Follow n's path to its cut
node in `C_Y` (Lemma 4). If some node on it has `A < c_*`, let `ν_i` be the first (i ≥ 1 since
`A_0 = 1`). By Lemma 3 `|B_i| ≤ i G_max ≤ k G_max`, so
`T^{k_i}(n) = A_i n + B_i < c_* n + k G_max ≤ n` because `(1−c_*) n ≥ (1−c_*) 2^k > k G_max`.
As `T^{k_i}(n) ≠ n`, `k_i ≥ 1`: n drops. Otherwise the cut node ν of n has `A_ν ≥ c_*`. By
Lemma 4 the number of such n is at most
`#{ν ∈ C_Y : A_ν ≥ c_*} ≤ Σ_{ν∈C_Y} (A_ν/c_*)^s ≤ Σ μ(ν)Φ(ν) · M_ν^{1−γ}/(c_*^s w_min)
≤ w(σ_0)(q_max Y)^θ /(c_*^s w_min)` by Lemma 2. Summing over `k_0 ≤ k ≤ log_2 X` (geometric
series with ratio `2^θ`) and adding `< 2^{k_0}` integers below `2^{k_0}` gives the bound. For the
Haar statement apply the same estimate to `μ` instead of counting: the measure of paths with
`A ≥ c_*` down to scale `Y` is `≤ w(σ_0) q_max^θ c_*^{−s} Y^{−γ}/w_min → 0`. ∎

**Corollary 1.1 (PROVED).** If GLOBAL fails, the least start whose orbit is not eventually periodic
is never-dropping; every cycle minimum is never-dropping; the tail minima of a divergent orbit are
never-dropping. Hence `#{cycles with minimum ≤ X} ≤ H(X) = O(X^θ)`.

## Theorem 2 (the optimal exponent and when it is < 1; PROVED)

Let `γ*(s) = sup{γ : ρ(N_{s,γ}) ≤ 1}` and `θ* = 1 − sup_{s>0} γ*(s)` (clipped to `[0,1]`).

(a) For every `θ > θ*` there is a certificate for Theorem 1 with exponent θ. So
`H(X) = O(X^{θ*+ε})` for all `ε > 0`.

(b) Suppose G(T) has exactly one closed (recurrent) class `C` (true for all systems here; checked by
`closed_classes`). Let `π` be its stationary law and
`Δ = Σ_σ π(σ) Σ_{e from σ} q(σ)^{−1} log F_e` (Lyapunov drift per digit),
`Λ = Σ_σ π(σ) log q(σ)`. Then **θ* < 1 iff Δ < 0.**

(c) For single-prime maps `N_{s,γ} = p^γ P_s` with `P_s = Σ p^{−1} F^s`, so
`θ* = 1 + min_{s>0} log_p ρ(P_s)`.

*Proof.* (a) `ρ(N_{s,γ'}) ≥ 2^{γ'−γ} ρ(N_{s,γ})` for `γ' > γ` (entrywise `q^{γ'−γ} ≥ 2^{γ'−γ}`), so
ρ is strictly increasing in γ. Pick `s` with `γ*(s) > 1 − θ`; at `γ = 1 − θ` we have
`ρ(N_{s,γ}) < 1`, so `w = Σ_k N^k 1 = (I − N)^{-1} 1 > 0` exists and `N w = w − 1 ≤ w`.

(b) **Kingman's convexity**: every entry of `N_{s,γ}` is a sum of `exp(affine(s,γ))`, hence
log-convex; sums and products of log-convex functions are log-convex, so every entry of `N^k` is,
and `log ρ = lim_k (1/k) log (1ᵀ N^k 1)` is a pointwise limit of convex functions, so
`f(s,γ) = log ρ(N_{s,γ})` is jointly convex. `f = max_D f_D` over the strongly connected
components D. At `(0,0)` the closed class has `ρ = 1` (stochastic, irreducible), every transient
component has `ρ < 1` (it leaks), so near `(0,0)` `f = f_C`, which is differentiable there (simple
Perron root) with gradient `(πN_s'1, πN_γ'1) = (Δ, Λ)`, `Λ > 0`.
If `Δ < 0` then `f(s,0) < 0` for small `s > 0`, so `γ*(s) > 0` and `θ* < 1`.
If `Δ ≥ 0` then for `s > 0, γ > 0`: `f(s,γ) ≥ f_C(s,γ) ≥ Δ s + Λ γ > 0` (a convex function lies
above its tangent plane), so `γ*(s) ≤ 0` for every `s > 0` and `θ* = 1`. (c) is immediate. ∎

`make_certificates.py` searches `s` in floating point, then certifies a rational `γ` just below
`γ*(s)`; `check_density.py [3]` verifies `N_{s,γ} w ≤ w` exactly, bounding each irrational power
`q^{γ−1}`, `F^s` above by a rational `y` with the exact integer test `y^b ≥ x^a` (exponent `a/b`).
The tool works for any table map whose graph is finite (`density_lib.best_certificate`).

**Remark (sanity check, CLS-013).** For `3x+1` (one state, `F ∈ {1/2, 3/2}`), (c) gives
`θ* = 1 + min_s log_2((2^{−s} + (3/2)^s)/2) = H(log_3 2) = 0.949955…` (binary entropy), which is the
classical Terras exponent for residues mod `2^k` with stopping time `> k` (as attributed in
Lagarias's 1985 survey to Terras 1976; recalled, not re-read). Our certified rational bound is
`θ ≤ 0.94996`. The 3n+d family (CLS-011…018, 031) has the same slopes, hence the same θ*.

## Theorem 3 (θ* is exactly the exponent of the method; single-prime maps; PROVED under (H))

Let `O_j(c_*)` be the number of depth-j nodes (classes mod `p^j`) whose slopes `A_i ≥ c_*` for every
`i ≤ j`, i.e. the classes the coefficient tree does *not* certify by a slope crossing. Hypothesis
(H): (part 1) the closed class C is reached from the root along a path whose partial products stay
≥ 1 and which can then be extended by a cycle of C with all partial products > 1; (part 2)
`ρ(P_s)` is attained on C for s near s*, i.e. `ρ(P_s) = ρ_C(P_s)` there (for instance, G(T) is
irreducible); and (part 3) `ρ(P_s)` has a minimiser `s* ∈ (0,∞)` such that the derivative of
`log ρ(P_s)` is `> 0` to the right of s* and tends to 0 as `s ↓ s*`. Then

> `lim_j (1/j) log_p O_j(c_*) = θ*`  for every `c_* ∈ (0, 1]`.

So the set of `n ∈ [p^j, p^{j+1})` not certified by slopes along the first j digits has size
`p^{jθ* + o(j)}` (each class mod `p^j` contains `p−1` of them): **no argument that only looks at the
coefficient tree to depth `log_p n` can beat θ*.**

*Proof.* Upper bound: the proof of Theorem 1 gives `O_j ≤ c_*^{−s} ρ(P_s)^j p^j w_0/w_min` for every
`s > 0`. Lower bound: take `s_1 > s*` close to `s*` with `μ_1 := (log ρ(P_s))'(s_1) > 0` small, `h`
the right Perron vector of `P_{s_1}` on C, `ρ_1 = ρ(P_{s_1})`. The tilted chain
`Q(e) = p^{−1} F_e^{s_1} h(dst)/(ρ_1 h(src))` is stochastic and irreducible on C, and for a path of
length m from σ, `p^{−m} = Q(path) ρ_1^m (h(σ)/h(end)) A^{−s_1}`. Under Q, `log A_m / m → μ_1 > 0`
a.s. (ergodic theorem; the mean increment of the tilted chain is `(log ρ)'(s_1)`), hence
`Q(inf_m log A_m ≥ −K) → 1` as `K → ∞` and `Q(log A_m ≤ (μ_1+ε)m) → 1`. By (H) a fixed prefix of
length `L_0` brings the slope to `≥ c_* e^K` without going below 1, landing in C. So for large j
`O_j ≥ p^{j} · p^{−L_0} · ½ ρ_1^{j−L_0} (h_min/h_max) e^{−s_1(μ_1+ε) j} · e^{−O(1)}`, i.e.
`liminf (1/j) log_p O_j ≥ 1 + log_p ρ_1 − s_1(μ_1+ε)/ln p`. Let `ε → 0`, `s_1 ↓ s*`
(`μ_1 → 0`, `ρ_1 → ρ_C(P_{s*})`): `liminf ≥ 1 + log_p ρ_C(P_{s*})`. Since the tilting is done only on
the closed class C, the Perron root here is that of C, and the argument by itself gives the lower
exponent `1 + min_s log_p ρ_C(P_s)`, while the upper bound uses ρ(P_s) of the whole graph. By (H)
part 2, `ρ(P_s) = ρ_C(P_s)` for s near s*, so `liminf ≥ 1 + log_p ρ(P_{s*}) = θ*`. (Without part 2, a
transient component with larger spectral radius at s* would break this equality.) ∎

**(H) parts 2 and 3 for irreducible graphs.** If G(T) is irreducible, part 2 is immediate, and
part 3 follows from part 1. Indeed, for an irreducible graph ρ(P_s) is a simple Perron root, so
`log ρ(P_s)` is analytic and convex in s. Its derivative at `s = 0` is `Δ < 0`. It tends to `+∞` as
`s → ∞`, because the exact pumping cycle of (H) part 1, of length L and slope product `Π > 1`, gives
`tr P_s^L ≥ p^{−L} Π^s`. Hence the set of minimisers of `log ρ(P_s)` is a nonempty compact interval
in `(0, ∞)`. Taking s* to be its right end, the derivative is `> 0` to the right of s* and tends to
0 as `s_1 ↓ s*`. That is all the proof uses; uniqueness of the minimiser is not needed.

(H) holds for every single-prime contracting system in `results.md` (17 maps). Part 1: they have a
self-loop or short cycle with factor > 1 at the root's class, checked exactly by `check_hypH.py`.
Parts 2 and 3: each of these graphs is irreducible (single-state graphs, plus split5_1, split5_3,
desc_s32_plus9 and desc_split7_1, which have 2–8 states and no transient states, by an exact SCC
computation in the referee's `referee_check.py` [R7]), so parts 2 and 3 follow from part 1 as above.
`evidence.py [E1]` shows the exact counts `O_j` approaching `θ*` (EVIDENCE for the rate).
Note: Theorem 3 is about the *method*. The true exponent of `H(X)` can be far smaller
(conjecturally `H(X) = O(1)` for 3x+1).

## Theorem 4 (Korec-type: almost all orbits go below `n^c`; PROVED)

Let `c_0 = 1 + Δ/Λ` (with Δ, Λ of Theorem 2(b)). If `Δ < 0` then for every `c ∈ (c_0, 1)`

> `#{n ≤ X : T^k(n) ≥ n^c for all k ≥ 1} = O(X^{θ_c})` with `θ_c < 1`,

where any `s > 0`, `γ ∈ [0,1]`, `w` with `N_{s,γ} w ≤ w` give `θ_c = 1 − γ + s(1 − c)`.

*Proof.* Block `[Y, 2Y)`, threshold `τ = (2Y)^{c−1}/2 ≤ n^{c−1}/2`. If n's path to its cut node has
a node with `A < τ`, the first one has `|B_i| ≤ k G_max` (Lemma 3) and
`T^{k_i}(n) < τ n + k G_max ≤ n^c/2 + k G_max < n^c` once `Y^c ≥ 2k G_max`. Otherwise the cut node
has `A ≥ τ`; their number is `≤ τ^{−s} Σ_{C_Y} A^s ≤ (w_0/w_min) q_max^{1−γ} 2^s (2Y)^{s(1−c)} Y^{1−γ}`.
Sum over blocks. Existence of `(s, γ)` with `θ_c < 1` for every `c > c_0`: with `f` as in Theorem 2,
along `(s, γ) = t(1, 1 − c + η)` we get `f = t(Δ + Λ(1−c+η)) + o(t) < 0` for small `t > 0` when
`η < c − c_0`, so `γ*(t) > t(1−c+η)` and `θ_c ≤ 1 − tη < 1`. ∎

For 3x+1, `c_0 = log_4 3 = 0.7925`, which is exactly Korec's 1994 threshold (as quoted in Tao,
*Almost all orbits of the Collatz map attain almost bounded values*, arXiv:1909.03562, intro; Korec's
paper itself not consulted). Theorem 4 is the extension of Korec's argument to every Markov table map. For the open census entries `c_0` ranges from 0.468 (desc_split7_1) to 0.977 (m3_g); a
certified `θ_c` at a sample `c` is in `results.md`.

**Proposition 4.2 (c_0 is sharp for the method; PROVED).** If `c < c_0` (`Δ < 0`), there are
`s < 0`, `γ` and `w` with `N_{s,γ} w ≤ w` and `η := γ + (c−1)s > 0`. Then for all large
`Y = 2^k`, all but `≤ (q_max w_0 q_max^{max(0,−γ)} 2^{−s}/w_min) Y^{1−η}` of the `n ∈ [Y, 2Y)` have
**every** tree value `x_i = T^{k_i}(n)` (nodes up to the cut) `≥ n^c`. So the depth-`log n` tree
certifies an iterate below `n^c` only for a density-zero set of n, for every `c < c_0`.

*Proof.* Call n exceptional if a node on its path has `A < 2Y^{c−1}`. At the first such node ν,
`Φ(ν) = A^s w M^γ ≥ 2^s Y^{(c−1)s} w_min min(1, (q_max Y)^γ)` (s < 0, `M < q_max Y`), so by Lemma 2
(stopping at those nodes or at the cut) their total mass is `≤ w_0 2^{−s} q_max^{max(0,−γ)}
Y^{−η}/w_min`, and the number of exceptional n is `≤ q_max Y` times that mass (each cut node has
mass `≥ 1/(q_max Y)`). For non-exceptional n all `A_l ≥ 2Y^{c−1} ≥ 2n^{c−1}`, so
`|B_i| ≤ A_i k G_max Y^{1−c}/2` (from `B_i/A_i = Σ G_l/A_{l+1}`), whence
`x_i ≥ A_i (n − kG_max Y^{1−c}/2) ≥ A_i n/2 ≥ n^c` once `Y^c ≥ k G_max`. Existence of `(s, γ)`:
put `s = −t`, `γ = t g` with `t > 0` small. Then `f(s, γ) = t(−Δ + Λ g) + o(t)` and
`η = t(g + 1 − c)`. Both `f < 0` and `η > 0` hold for small t iff `c − 1 < g < Δ/Λ`, and such g
exists iff `c < 1 + Δ/Λ = c_0`. (Here `g < 0`, so `γ < 0`.) ∎ The exact certificate for `c = c_0 − 0.02` (rounded) is checked.

## Theorem 5 (expanding maps: almost all orbits rise above `n^c`; PROVED)

If `Δ > 0` (so `c_0 = 1 + Δ/Λ > 1`), then for every `c ∈ (1, c_0)`:

> `#{n ≤ X : T^k(n) ≤ n^c for every k ≥ 0} = O(X^{θ_c})`, `θ_c < 1`.

This covers 5x+1 (`c_0 = log_2 5 /2 = 1.16096`, CLS-022/024 and the 5n+d family), 7x+1
(`c_0 = log_2 7/2 = 1.40368`, CLS-032/034), 9x+1 (`c_0 = log_2 3`, CLS-037), 10n+2, m3_e
(`c_0 = 1.18083`), and the permutations perm_1932, its inverse, perm_swap, perm_b, perm_c, perm_d
(`c_0 = 1.0516 … 1.161`).

*Proof.* Take `s' > 0`, `γ ∈ [0,1]`, `w` with `N_{−s',γ} w ≤ w`; put
`θ_1 = 1 − γ + s'(c − 1) < 1` and pick any `ε ∈ (0, 1)` with `ε ≤ (1 − θ_1)/s'`; the exponent is then `θ_c = max(θ_1, 1 − εs')` (equal to `θ_1` for `ε = (1−θ_1)/s'`; the check uses a 4-digit ε just below that). Block `[Y,2Y)`, n in it.
Exceptional sets: E1 = cut node has `A < τ' := 4(2Y)^{c−1}`; E2 = some node on the path has
`A < Y^{−ε}`. If n is in neither, `|B_cut| ≤ A_cut Σ_l G_max/A_{l+1} ≤ A_cut k G_max Y^ε`, so
`x_cut ≥ A_cut(n − kG_max Y^ε) ≥ A_cut n/2 ≥ 2(2Y)^{c−1} n > n^c` once `Y^{1−ε} ≥ 2kG_max`.
`|E1| ≤ τ'^{s'} Σ_{C_Y} A^{−s'} ≤ (w_0/w_min) q_max^{1−γ} 4^{s'} 2^{s'(c−1)} Y^{θ_1}` (Lemma 2 with
`s = −s'`). For E2, `N_{−s',0} w ≤ 2^{−γ} N_{−s',γ} w ≤ w`, so `A^{−s'} w(σ)` is a supermartingale
under μ; stopping at the first node with `A < Y^{−ε}` gives mass `≤ Y^{−εs'} w_0/w_min`, hence
`|E2| ≤ q_max Y · Y^{−εs'} w_0/w_min = q_max (w_0/w_min) Y^{1−εs'}`. Sum over blocks. Existence for every
`c < c_0` follows from Theorem 2's gradient as in Theorem 4 (now with `s < 0`). ∎

Note that signed intercepts (the permutations have negative `v`) are handled by E2.

## Theorem 6 (expanding maps: the early-drop density exists and is computable; PROVED)

Single-prime map with `Δ > 0` and all `G_e ≥ 0` (so `B ≥ 0` on every node). Let
`q = μ{paths whose slope is < 1 at some node}`, and
`D_early = {n : x_i(n) < n for some node i of depth ≤ ⌊log_p n⌋ on n's path}`. Then
**`D_early` has natural density exactly `q`**, and `D = {n : T^k(n) < n for some k}` has lower density
`≥ q`. Rigorous bounds (`check_density.py [6]`, depth 300, exact):

| map | q (density of starts dropping within log_p n tree steps) |
|---|---|
| 5n+d, any d>0 (par_5_*), 10n+2 | 0.823782 ≤ q ≤ 0.824073 (depth 300, checked); 0.823922 ≤ q ≤ 0.824002 (depth 400, make_certificates.py) |
| 7n+1, 7n+7 | 0.699249 (to 6 digits) |
| 9n+1 | 0.613870 |
| m3_e (3∣n→n/3, 7n+2, 7n+1) | 0.722567 – 0.722571 |

*Proof.* Upper: if `n ∈ [p^j, p^{j+1})` drops at a node `i ≤ j`, then `A_i n ≤ x_i < n`, so `A_i < 1`;
so n's depth-j class lies in `S_j`, the set of depth-j classes whose path has a slope `< 1`, and the
block contains at most `(p−1)#S_j = (p−1)p^j μ(S_j) ≤ (p−1)p^j q` such n. This bounds
`#(D_early ∩ [1,X])/X` only at block endpoints `X = p^{j+1}`; for X inside a block the classes of
`S_j` need not be equidistributed over `[p^j, X]`, and the trivial error `#S_j ≈ q p^j` is of the
order of X. So take `X ∈ [p^j, p^{j+1})` and fix L. Every element of `D_early ∩ [p^j, X]` lies in a
class of `S_j`, and we split `S_j` into two parts. The first part consists of the lifts of
`S_{j−L}`; membership in these depends only on n mod `p^{j−L}`, so on `[p^j, X]` they contain at
most `μ(S_{j−L})(X − p^j) + p^{j−L} ≤ q(X − p^j) + X p^{−L}` integers. The second part is
`S_j \ lift(S_{j−L})`, which contains at most `(p−1)p^j (μ(S_j) − μ(S_{j−L}))` integers of the
block; this is `o(p^j)` as `j → ∞`, because `μ(S_i) ↑ q`. Adding the full blocks below `p^j`
(at most `q p^j` elements by the endpoint bound) gives
`#(D_early ∩ [1,X]) ≤ q X + X p^{−L} + o(X)`, so `limsup_X #(D_early ∩ [1,X])/X ≤ q + p^{−L}` for
every L, hence `≤ q`. Lower: for each node ν
of depth `≤ L` that is the first on its path with `A_ν < 1`, every `n ≡ r_ν (mod M_ν)` with
`n > max(B_ν/(1−A_ν), p^L)` is in `D_early`; these progressions are disjoint with total density
`q_L → q`. Bounds: `q ≥ q_L` (exact enumeration of first crossings to depth L) and
`q ≤ q_L + Σ_{alive depth-L nodes} μ A^{s} w(σ)/w_min` for any `s < 0`, `w` with `N_{s,0} w ≤ w`
(optional stopping for the nonnegative supermartingale `A^s w`, which is `≥ w_min` once `A < 1`). ∎

## Proposition 7 (what the complementary statement would need; PROVED)

For any table map: if every positive orbit of T is eventually
periodic **and** T has only finitely many cycles, then `D` contains every `n` larger than the
largest cycle element, so `D` has density 1. Contrapositive: proving `upper density(D) < 1` for 5x+1
or 7x+1 would prove that 5x+1 (7x+1) has a divergent orbit or infinitely many cycles; neither is
known, and no 5x+1 orbit is known to be unbounded. So "the drop set has density < 1" is out of
reach of every density method here; Theorem 6 proves the strongest version available at depth
`log n`: the *early* drop set has density exactly `q < 1`. `evidence.py [E3]` shows the full drop set
in `[2^17, 2^18)` has proportion close to `q` (EVIDENCE that `density(D) = q`; conjecture).

## What "almost all" does not give (careful statements)

* "Almost every start drops below itself" (Theorem 1) does **not** imply "almost every orbit reaches
  a known cycle": the iterate below n is not a uniformly random integer, so the density-zero
  exceptional set could be hit by the orbits of a positive proportion of starts. Iterating
  Theorem 4 (`n → n^c → n^{c^2} …`) fails for the same reason. Proposition 4.2 shows the depth-log n
  tree cannot certify anything below `n^{c_0}` for almost all n, so any improvement (Tao 2019 style
  for 3x+1) needs information about the orbit beyond the first `log n` digits.
* Everything here is about densities. **No open GLOBAL question is settled.**
