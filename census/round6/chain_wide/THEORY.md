# One orbit: occupation bound, multiplier bound and chain theorem for a general table map

Round 6, lens "chain_wide". This file holds the general statements and their proofs. Per-system
constants are in `README.md` (tables) and `data/named.json`, `data/families.json`. The finite content
is checked by `check_chain.py` (exact) and `run_ranges.py` + `verify_range.c` (exact range
certificates).

Labels: **PROVED** = complete proof here plus exact check of all finite content. **EVIDENCE** =
numerical only. **OPEN** = not settled.

**Revised after REFEREE2** (see §9): a false clause in Corollary 5 is withdrawn, and Prop. 7's
"equivalent" is corrected to "implies".

**Revised after REFEREE1** (see §8 at the end for the list of changes). In short: the signed multiplier
constants were recomputed with the formula actually proved; a raw-time hypothesis (S1) for signed maps
was added; hypothesis (P) is now stated as "every `v_r ≥ 0`", which is what the raw-time arguments
use; core W does **not** satisfy (R), so only the update-time part of Prop. 7 applies to it (the
earlier text claimed more, and that claim is withdrawn); several wording fixes.

The two results being generalised are in `census/round2/rewriting/split5_3_s27.md`: the occupation
lemma with the multiplier bound ("How accurately the multipliers would track a divergent orbit") and
the chain theorem ("Arithmetic links between permanent survivors"). Here they are proved for every
single-prime table map with unit multipliers, a finite state graph G(T) and a certified negative
drift (and, for the chain theorem, hypotheses (P) and (R) below, or (S1) in the signed version), with
the exponent of the occupation bound equal to the
optimal moment exponent θ* of round 3 (`census/round3/density/theory.md`, Theorems 1 to 3).

---

## 0. Setting and hypotheses

A *single-prime table map* is `T(n) = (u_r n + v_r)/w_r` for `n ≡ r (mod Q)`, `Q = p^m`, with
integers `u_r ≥ 1`, `w_r` a power of the prime p, and `w_r | u_r n + v_r` on the whole class. We
assume T maps positive integers to positive integers, and that the multipliers are units
(`p ∤ u_r`). Units are used in Lemma 1 (the child digit is read off `y mod pK`), in the finiteness of
G(T) and in Corollary 3.1(ii) and Proposition 5.1. All systems treated have them (checked for the 26
named tables; in the families by construction: m3 skips `a ≡ 0 mod 3`, the S and split families have
odd u). [Revised after REFEREE1: the earlier text said units were not needed; that was wrong.]

We use the adaptive digit tree and its finite state graph **G(T)** from round 3
(`density/theory.md` §1, Lemma 1). Briefly: a node is `(M, r, a, b, k)` with
`T^k(Mt + r) = at + b` for all integers `t ≥ 0`; its state is `σ = (K, β)`, K the p-part of a and
`β = b mod K`; from a node one splits t by its next base-p digit and then applies every branch of T
that the residue information decides. Each split-plus-decided-steps is an **edge** of G(T), carrying
a slope factor `F_e` (product of the `u/w` of its raw steps), an intercept `G_e` (the real form
`x = An + B` changes by `A ← F_e A`, `B ← F_e B + G_e`) and a number of raw steps `steps_e ≥ 0`.
Each state has exactly p out-edges. Write `N_σ` for the number of states, `F_max = max_e F_e`,
`G⁺ = max(0, max_e G_e)`, `g = max_{e: G_e ≠ 0} |G_e|/F_e`.

Hypotheses (each statement lists which it uses):

* **(N) negative drift, certified.** There are rationals `s > 0`, `0 < γ ≤ 1` and a vector `w > 0`
  on states with `N_{s,γ} w ≤ w`, where `N_{s,γ}[σ,σ'] = Σ_{e: σ→σ'} p^{γ−1} F_e^s`. Put
  `θ = 1 − γ` and `W = Σ_σ w(σ)/w_min`. By round 3 Theorem 2 such certificates exist for every
  `θ > θ*` exactly when the Lyapunov drift Δ is negative; θ* is the exponent of the never-dropping
  set and equals its Hausdorff dimension (round 3 `deep/`, `density/`).
* **(P) positive constants.** Every `v_r ≥ 0`. Then `G_e ≥ 0` for every edge and every partial
  intercept inside an edge is ≥ 0, which is what the raw-time arguments use. [Revised after REFEREE1:
  the earlier text stated (P) as `G_e ≥ 0`, which is weaker than what the raw-time steps of Theorems 2
  and 4 use. Every system called "(P)" here has all `v_r ≥ 0`; `check_revision.py [R5]`.]
* **(S1) one constant per edge (signed maps only).** Every edge has at most one raw step with
  `v ≠ 0`. Steps with `v = 0` leave `Z = x/P` unchanged, so under (S1) the value of Z at a raw time
  inside an edge equals Z at one of the two updates bounding that edge. Holds for 3x−1 and m3_b
  (`check_revision.py [R2]`).
* **(R) raw prefixes.** Inside every edge, each intermediate raw prefix slope is at least
  `min(1, F_e)`. Checked exactly for every system (`chainlib.raw_prefix_ok`).

**Update chain of a start.** Fix a positive integer `x_0` and follow its path in the root tree:
nodes `ν_0, ν_1, …`. Node `ν_l` has a state `σ_l`, a value `y_l = T^{k_l}(x_0)` (an orbit value)
and a slope `P_l = F_{e_0}⋯F_{e_{l−1}}` (the product of the raw `u/w` up to raw time `k_l`). We call
l an *update*. Put `Z_l = y_l / P_l`.

For a state σ = (K, β), the **σ-tree** is the same adaptive tree started from the node
`(M, r, a, b) = (K, β, K, β)`: its integers are the `y ≡ β (mod K)`, its value is y itself, and its
depth-j nodes are the classes of y modulo `K p^j`.

## 1. Lemmas

**Lemma 1 (restart).** For all l, j ≥ 0 the nodes `ν_l, …, ν_{l+j}` are the path of the integer
`y_l` in the `σ_l`-tree: the states agree, `y_{l+j} = A y_l + B`, where `(A, B)` is the real form
of the depth-j node of the `σ_l`-tree containing `y_l`, and `A = P_{l+j}/P_l`.

*Proof.* At `ν_l = (M, r, a, b)` we have `x_0 = Mt + r` and `y_l = at + b`, `a = K u₀` with u₀
prime to p. The child taken is fixed by `t mod p`, equivalently (u₀ invertible mod p) by
`y_l mod pK`; in the `σ_l`-tree the child is fixed by the same residue of `y_l`. Which branches are
then decided, and their slopes and intercepts, depend only on the state (round 3 Lemma 1). Induct
on j. ∎ (Checked on random 160-bit starts for every system: `check_chain.py [2]`.)

**Lemma 2 (distinct pairs).** If the orbit of `x_0` is not eventually periodic, the pairs
`(σ_l, y_l)` are pairwise distinct, `y_l → ∞`, and `y_l ≡ β_{σ_l} (mod K_{σ_l})`.

*Proof.* Orbit values at different raw times differ (else the orbit is eventually periodic). Two
updates at the same raw time differ in the p-part K of their state, which grows by a factor p at each
split with no raw step. There are finitely many states, so only boundedly many updates share a raw
time, and raw time tends to infinity with l. Distinct orbit values of an integer sequence tend to
infinity. ∎

**Lemma 3 (moments).** Assume (N). For every state σ and j ≥ 0, summing over the `p^j` classes of
y modulo `K_σ p^j` (the depth-j nodes ν of the σ-tree),
`Σ_ν A_ν^s ≤ (w(σ)/w_min) p^{jθ}`.

*Proof.* Iterating `N_{s,γ} w ≤ w` j times gives `Σ_{paths} p^{j(γ−1)} A^s w(end) ≤ w(σ)`
(round 3 Lemma 2 from the root σ). Divide by `w_min p^{j(γ−1)}`. ∎

Consequently, if `X ≤ p^j`, each class modulo `K_σ p^j` contains at most one integer in `[1, X]`,
and summing Lemma 3 over the states,

  `M_s(X) := Σ_{pairs (σ,y) of the orbit, y ≤ X} A_j(σ, y)^s ≤ W p^{jθ}`,           (1)

where `A_j(σ, y)` is the slope of the depth-j node of the σ-tree containing y. For general j, each
class contains at most `X/p^j + 1` such integers and `M_s(X) ≤ W (X/p^j + 1) p^{jθ}`.

**Lemma 4 (two elementary inequalities).** For `u > 0`, `s > 0`: `log u ≤ u^s/(e s)`.
For `A > 0`, `B ≥ 0`, `y > 0`, `0 < c`: `A + B/y ≤ max(A, c)(1 + B/(c y))`. ∎ (The first: the
maximum of `log u / u^s` is `1/(es)`. The second: expand the right side.)

## 2. Occupation bound

Let `V(X)` be the number of updates l with `y_l ≤ X` on a non-eventually-periodic orbit (equivalently,
by Lemma 2, the number of distinct pairs (σ, y) with y ≤ X that occur).

**Theorem 1 (crude occupation bound). PROVED.** Assume (N) and that every `v_r ≥ 0` or not (signs
are allowed). For every X ≥ 2 and j ≥ 1,

  `V(X) ≤ W (X/p^j + 1) p^{jθ} + s e^{1/s} b_j N_σ (1 + ln X)`,   `b_j = G⁺ Σ_{i<j} F_max^i`.

With `φ = log_p F_max` and `j = ⌊κ log_p X⌋` for a fixed `0 < κ < min(1, 1/φ)` this is
`O(X^η (log X)^2)` with `η = max(1 − κ(1 − θ), κ φ) < 1`. Hence `Σ_l 1/y_l < ∞` and

  `E := Σ_l |log(1 + G_{e_l}/(F_{e_l} y_l))| = Σ_l |log Z_{l+1} − log Z_l| < ∞`.

*Proof.* Let `H(x) = log min(x, X)`. Fix j. Since `y_l → ∞` there is a last update `L_X` with
`y ≤ X`. For each residue ρ mod j, the sum of `H(y_{l+j}) − H(y_l)` over `l ≡ ρ`, `l ≤ L'` (with
`L' ≥ L_X` in the class) telescopes to `H(y_{L'+j}) − H(y_ρ) = log X − H(y_ρ) ≥ 0`. Terms with
`y_l > X` are `≤ 0`, so `Σ_{l: y_l ≤ X} (H(y_{l+j}) − H(y_l)) ≥ 0`. For `y_l ≤ X`, Lemma 1 gives
`y_{l+j} = A y_l + B` with `B ≤ b_j` (`B_0 = 0`, `B ← F B + G`), so by Lemma 4 with
`c = e^{−1/s}`:

  `H(y_{l+j}) − H(y_l) ≤ log(A + b_j/y_l) ≤ −1/s + e A^s / (e s) + b_j e^{1/s}/y_l`.

Summing over the `V(X)` updates with `y_l ≤ X` and multiplying by s:
`V(X) ≤ M_s(X) + s e^{1/s} b_j Σ 1/y_l`. The pairs with `y ≤ X` are distinct (Lemma 2), so the last
sum is at most `N_σ (1 + ln X)`. Insert (1) in its general form. For the exponent:
`(X/p^j + 1)p^{jθ} ≤ 2 p X^{1−κ(1−θ)}` and `b_j ≤ G⁺ j F_max^j ≤ G⁺ j X^{κφ}` (if `F_max ≥ 1`). Finally
`Σ_l 1/y_l ≤ Σ_k V(p^{k+1}) p^{−k} < ∞`, and `|log(1+u)| ≤ 2|u|` once `|u| ≤ 1/2`. ∎

**Theorem 2 (occupation bound with the optimal moment exponent). PROVED.** Under the hypotheses of
Theorem 1, for every X ≥ 1 and the orbit's total log error E,

  `V(X) ≤ W p^θ X^θ + s ⌈log_p X⌉ E`.

In particular `V(X) = O(X^θ)` for every certified θ, hence `V(X) ≤ X^{θ* + o(1)}`. With (R) and (P), the
number of raw times t with `T^t(x_0) ≤ X` is at most `R · V(X / c_raw)`, where R is the largest
number of raw steps in an edge and `c_raw = min(1, smallest non-final raw prefix slope in an edge)`.

*Proof.* Take `j = ⌈log_p X⌉`, so `X ≤ p^j ≤ pX`. As in Theorem 1, `0 ≤ Σ_{l: y_l≤X} log(y_{l+j}/y_l)`
(no capping needed above: `H(y_{l+j}) − H(y_l) ≤ log(y_{l+j}/y_l)` when `y_l ≤ X`). Now write exactly

  `log(y_{l+j}/y_l) = log A_l + log(Z_{l+j}/Z_l)`, `A_l = P_{l+j}/P_l`,

and `log A_l ≤ −1/s + A_l^s/s` (Lemma 4 with `u = e^{1/s} A_l`). [Typo `A_l^s` corrected after
REFEREE1.] Each update increment
`|log Z_{i+1} − log Z_i|` lies in at most j windows, so `Σ_l log(Z_{l+j}/Z_l) ≤ jE`. Summing,
`V(X)/s ≤ M_s(X)/s + jE`, and (1) gives `M_s(X) ≤ W p^{jθ} ≤ W p^θ X^θ`. For raw times: a raw time
inside the edge leaving update l has value at least `c_raw y_l` by (R) and positivity of the partial
intercepts; each update carries at most R raw times. ∎

Remark. Theorem 1 is needed only to know `E < ∞`; the bound then comes from Theorem 2. Without the
exact identity `log(y_{l+j}/y_l) = log A + log(Z_{l+j}/Z_l)` the intercepts would cost
`F_max^j = X^φ`, which exceeds `X^θ` for split5_1 (φ = 1.32), desc_split7_1 (φ = 0.81 > θ = 0.75)
and desc_s32_plus9 (φ = 1.17).

## 3. Multiplier bound and dichotomy

**Theorem 3 (multiplier bound). PROVED.** Assume (N). Suppose every value of a non-eventually-periodic
orbit is at least `p^{k_0}` (this holds whenever every `n < p^{k_0}` is verified to have an eventually
periodic orbit). Put

  `S_1 = Σ_{k≥k_0} p^{(k+1)θ − k} = p^θ p^{−k_0(1−θ)}/(1 − p^{−(1−θ)})`,
  `S_2 = Σ_{k≥k_0} (k+1) p^{−k}`.

with `g' = g` under (P) and `g' = 2g` otherwise (then also `g ≤ p^{k_0}/2` is required). If
`g' s S_2 < 1`, then `E ≤ E*(k_0) := g' W p^θ S_1 / (1 − g' s S_2)`. Consequently

  `1 ≤ x_t / (x_0 P_t) < e^{E*}` for every raw time t under (P),
  `e^{−E*} < y_l/(x_0 P_l) < e^{E*}` at every update l in general, and at every raw time under (S1),

where `P_t` is the product of the raw `u/w` up to time t. [Revised after REFEREE1: the signed
constants in `data/named.json` had used `g` instead of `g' = 2g` in the denominator and were about
1e-9 (relative) below the bound proved here; they were recomputed (`chainlib.multiplier_E(...,
factor=2)`). The signed raw-time claim now needs (S1).]

*Proof.* `E ≤ g' Σ_l 1/y_l` term by term (`log(1+u) ≤ u` for u ≥ 0; `|log(1+u)| ≤ 2|u|` for
`|u| ≤ 1/2`, and `|u| ≤ g/y_l ≤ g p^{−k_0}`). Group the pairs with `y_l ∈ [p^k, p^{k+1})`: at most
`V(p^{k+1})` of them, each with `1/y_l ≤ p^{−k}`. By Theorem 2,
`E ≤ g' Σ_{k≥k_0} p^{−k}(W p^θ p^{(k+1)θ} + s (k+1) E) = g' W p^θ S_1 + g' s S_2 E`. Since E is
finite (Theorem 1), solve for E. At updates, `Z_l/Z_0 = exp(Σ_{i<l} log(Z_{i+1}/Z_i))` with
`Z_0 = x_0`, so `|log(Z_l/Z_0)| ≤ E`; under (P) every term is ≥ 0. Raw times: under (P) every raw
step inside an edge multiplies Z by `1 + v/(u x) ≥ 1`, so the raw-time Z lies between `Z_l` and
`Z_{l+1}`; under (S1) it equals one of them. ∎

The constants `E*` are computed exactly (rational upper bounds for every irrational power) by
`chainlib.multiplier_E`, minimised over a grid of certificates s, and re-checked by
`check_chain.py [5]`. For split5_3 at `k_0 = 48` this gives `E* < 5.4·10⁻⁵`, sharper than the
repo's `log 1.000073 = 7.3·10⁻⁵` (which used s = 2 and exponent 0.585).

**Corollary 3.1 (dichotomy). PROVED.** Under (N): on a non-eventually-periodic orbit `P_t → ∞`. Under
(N) and (P): on an eventually periodic orbit the multiplier of each lap of the cycle is `< 1`, so
`P_t → 0`. With a negative constant the second half fails: 3x−1 has the cycles at 1, 5, 17 with lap
multipliers 3/2, 9/8, 2187/2048, all `> 1` (`check_chain.py [6]`); for those maps the dichotomy reads
"`P_t → ∞` iff the orbit is not eventually periodic, or it ends in a cycle with lap multiplier > 1".

*Proof.* `x_t → ∞` and `x_t/P_t` is bounded. On a cycle `x = λx + C` with `C ≥ 0` under (P). If
`C = 0` then `λ = 1`; with unit multipliers (`p ∤ u`) this forces every step of the cycle to have
`u = w = 1`, and `C = 0` then forces `v = 0`: a branch n ↦ n, which no system here has. So `C > 0`
and `λ < 1`. ∎

## 4. The chain theorem

**Theorem 4 (chain of permanent survivors). PROVED.** Assume (N), (P), (R), and let the orbit of
`x_0` be not eventually periodic. Let `ρ = F_max`. There are updates `t_0 < t_1 < …` (the successive
last minimisers of `P_l` over the tails `l > t_{i−1}`) such that, with `x_i := y_{t_i}`:

(a) **Permanent survival.** `P_l > P_{t_i}` for every update `l > t_i`; the raw multiplier from raw
time `k_{t_i}` never falls below 1; and every later raw value exceeds `x_i`. In particular
`x_i ∈ N^mult := {n ≥ 1 : every raw prefix multiplier of the orbit of n is ≥ 1}`, and
`N^mult ⊆ N_T := {n : T^k(n) ≥ n for all k}`. The `x_i` increase strictly.

(b) **Links.** The edge leaving `t_i` has `F > 1`, and `1 < r_i := P_{t_{i+1}}/P_{t_i} ≤ F` of that
edge `≤ ρ`. The last edge of the link with `F ≠ 1` (if the link has more than one edge with `F ≠ 1`)
has `F < 1`.
If the edge slopes other than 1 take exactly two values `ρ > 1 > κ` (multiplicatively independent),
a link with e contracting edges has exactly `a = ⌊e · log(1/κ)/log ρ⌋ + 1` expanding edges.

(c) **Strip.** `x_{i+1} = r_i x_i + C_i` with
`G_first r_i/F_first + [last ≠ first] G_last ≤ C_i ≤ Σ_{edges k of the link} G_k`.

(d) **Forced residues.** For every depth K, `x_i` lies in a class modulo `K_σ p^K` of the
`σ = σ_{t_i}` tree whose path has every prefix slope `> 1`. In particular the first
`k* = min{k : ρ^k κ_max > 1}` edges with `F ≠ 1` after `t_i` expand (`κ_max` = largest contracting
slope), and `x_i` lies in the union `U_K` of these classes; `README.md` lists the forced congruence
(the largest D with `U_K` inside one class mod `p^D`) and the "survivor mass" `Σ 1/M` over the classes
of all states. Root classes of different states can overlap, so this sum is **an upper bound** for
the Haar mass of `U_K`, not the mass itself. [Wording revised after REFEREE1.]

(e) **Count.** For every `Λ > 1`, every integer `k ≥ 0` with `ρ^k < Λ`, and every sufficiently large X,
the interval `[X, ΛX)` contains at least k of the `x_i`. In particular every B consecutive late
octaves `[2^m, 2^{m+B})` contain at least `A(B) := max{k : ρ^k < 2^B}` of them.

*Proof.* By Corollary 3.1, `P_l → ∞`, so for each i the minimum of `P_l` over `l > t_{i−1}` is
attained, at finitely many l; take the last. Then `P_l > P_{t_i}` for `l > t_i`.

(a) A raw time inside an edge leaving update `l ≥ t_i` has raw multiplier `P_l σ` with σ the raw
prefix slope; `σ ≥ 1` gives `≥ P_l ≥ P_{t_i}`, and `σ ≥ F_e` gives `≥ P_{l+1} > P_{t_i}`; (R) says one
of the two holds. The raw value there is `Z · (raw multiplier)` with Z nondecreasing under (P), so it
is `≥ Z_{t_i} P_{t_i} = x_i`, with equality impossible (distinct orbit values). The same argument
from the start n of any orbit shows `N^mult ⊆ N_T` under (P).

(b) `P_{t_i+1} > P_{t_i}` forces the first edge to have `F > 1`; `P_{t_{i+1}} ≤ P_{t_i + 1}` by
minimality. If the last edge `e` with `F_e ≠ 1` had `F_e > 1`, the update before it (later than
`t_i`) would have a smaller multiplier than `P_{t_{i+1}}`. Two slope values: `ρ^a κ^e ∈ (1, ρ]`
means `a ∈ (eL, eL + 1]`, `L = log(1/κ)/log ρ`; independence makes `eL` non-integral for `e ≥ 1`.

(c) Unroll `B ← F B + G` along the link: `C_i = Σ_k G_k P_{t_{i+1}}/P_{(end of k)}`. Every ratio is
in `(0, 1]` by minimality of `t_{i+1}`; for the first edge it equals `r_i/F_first`, for the last
it is 1; all terms are ≥ 0 by (P).

(d) By Lemma 1 the edges after `t_i` are the `σ_{t_i}`-tree path of `x_i`, whose prefix slopes are
the ratios `P_l/P_{t_i} > 1`. Before the first contracting edge the product is at most `ρ^k`, and
after it at most `ρ^k κ_max`.

(e) Z is nondecreasing and bounded (Theorem 3), so `Z_l → Z_∞ ∈ (0, ∞)`. Then
`x_{i+k}/x_i = (P_{t_{i+k}}/P_{t_i})(Z_{t_{i+k}}/Z_{t_i}) ≤ ρ^k Z_∞/Z_{t_i}`, and
`Z_∞/Z_{t_i} → 1`. For large X let i be the last index with `x_i < X`; then `x_{i+1}, …, x_{i+k}`
are `≥ X` and `x_{i+k} < X ρ^k Z_∞/Z_{t_i} < ΛX` once `Z_∞/Z_{t_i} < Λ/ρ^k`. ∎

**Signed version (m3_b, 3x−1). PROVED.** Assume (N), (R) and (S1) instead of (P). Then (a) holds
for the multiplier (so `x_i ∈ N^mult`), heights at raw times (by (S1); without (S1), at updates only)
satisfy `x_t ≥ x_i e^{−E_i}` with `E_i = Σ_{l ≥ t_i} |log Z_{l+1}/Z_l| → 0`
instead of `x_t > x_i`, and (b), (d), (e) hold unchanged (in (e) take i last with `x_i < X`; Z still
converges because `Σ |log Z_{l+1}/Z_l| < ∞`). (c) holds with `|G|` in the upper bound and without the
lower bound.

**Corollary 5 (window criterion). PROVED.** Assume (N) and (R), and (P) or the signed version. If for
some `B ≥ 1` there are infinitely many m with
`#(N^mult ∩ [2^m, 2^{m+B})) < A(B)`, then every positive orbit of T is eventually periodic. The same
holds with `N^mult` replaced by any superset: `N_T` (under (P)), the finite-depth multiplier survivors
`N_b` (survive the first b updates) for any `b = b(m)`, or their intersection with the forced class
of (d). This is a criterion for eventual periodicity only; it says nothing about which cycles occur. If
`A(B) = 0` (split5_1 and desc_s32_plus9 with B = 1) the hypothesis can never hold and the criterion is
vacuous; take B larger. In `N_b`, "survive" means: every raw prefix multiplier over the first b raw
steps is `≥ 1` (not `> 1`: the S-family has slope-1 raw steps). One may instead use "every
root-tree update multiplier over the first b updates is `≥ 1`", which the raw condition implies.
Either set contains every selected start, which is all the proof uses. [Revised after REFEREE1.]
[**Withdrawn after REFEREE2.** The REFEREE1 revision had added the clause "or equivalently for this
purpose every update multiplier over the first b updates is `> 1` (Theorem 4(a) gives strict
inequality at updates)". That clause is **false**. `N_b` is a set of starts n, so its updates are
those of the root tree of n, while Theorem 4(a) gives strict inequality at the updates of `x_0`'s
tree, which continue as the `σ_{t_i}`-tree of `x_i`, not the root tree of `x_i`. For split5_3 and the
S-family (sf3_*, desc_s32_plus9), the root edge (1,0) → digit 1 is a pure split with `F = 1` and no
raw step, so every odd start, including every selected start, has root-tree update multiplier
exactly 1. With the clause, `N_b = ∅` for b ≥ 1 and the corollary would "prove" GLOBAL for split5_3,
which is false as a deduction. The clause is replaced by the `≥ 1` version above
(`referee2_check.py [J]`).]

*Proof.* Theorem 4(a), (d), (e). ∎

## 5. What would be needed, and what the count law says

**Proposition 5.1 (what the chain structure implies). PROVED, but nearly tautological.** Assume
(N), (P), (R) and unit multipliers. [Revised after REFEREE1: earlier versions called this the "main
new point" and a "gap statement". Part 1 is just "N^mult ≠ ∅ ⇔ a divergent orbit exists", and part 2
is Theorem 4 restated. Its only content is the remark that the window criterion is a real target
only for finite-depth supersets.]

1. `N^mult` contains no start of an eventually periodic orbit (on such an orbit `P_t → 0`,
   Corollary 3.1). Hence `N^mult = ∅` if and only if every positive orbit is eventually periodic, and
   `N^mult ∩ [1, N_0) = ∅` whenever all `n < N_0` are verified.
2. If `N^mult ≠ ∅`, then for every B every sufficiently late window `[2^m, 2^{m+B})` contains at least
   `A(B)` members of `N^mult`, all in the forced classes of Theorem 4(d), all never-dropping, and
   linked in chains with ratios in `(1, ρ]` and the strips of Theorem 4(c).

So `N^mult` is either empty or has at least `log X/log ρ − O(1)` members below X, spread over every
late window. The counting function of `N^mult` is also `O(X^{θ*+ε})`, because under (P) it lies
inside `N_T`, the never-dropping set of round 3, Theorem 1. Part 1 shows that the
window criterion of Corollary 5 *for `N^mult` itself* is just a restatement of GLOBAL; its content is
in the computable supersets `N_b` (finite-depth survivors) and `N_T`, for which a count of
`A(B) − 1` in infinitely many windows is a genuinely weaker target than the count law.

*Proof.* 1: if `n ∈ N^mult` then `P_t ≥ 1` for all t, impossible when `P_t → 0`; conversely a
divergent orbit supplies the `x_i` of Theorem 4. 2: Theorem 4. With a negative constant, part 1 fails:
for 3x−1 the cycle point 1 lies in `N^mult` (its lap multiplier is 3/2). ∎


For each system the weakest counting statement of this kind that excludes escaping orbits is

  (W_B) `#(N^mult ∩ [2^m, 2^{m+B})) ≤ A(B) − 1` for infinitely many m (some fixed B),

or its finite-depth form with `N_{b(m)}`. What is known and expected:

* **Proved (round 3, Theorem 1).** `#(N_T ∩ [1, X]) = O(X^{θ*+ε})` (and `N^mult` likewise). This is
  `≈ 2^{θ* m}` per octave, exponentially more than `A(B)`.
* **Proved for 3x+d and split5_3 (round 5 microrange; split5_3 "Almost every octave").** In almost
  every octave, the number of finite-depth survivors follows the Haar prediction `2^m P(b)` up to depth
  `b = m + O(log m)` digits. There the prediction is `2^{θ* m + o(m)}`, again far above `A(B)`.
* **Count law (Conjecture E, `round4/lead/CONJECTURE.md`).** `#N_b ∩ [2^m, 2^{m+B}) ≈ 2^{m+B} P(b)`
  for `b ≤ K m`. Since `P(b) = p^{−(1−θ*) b + o(b)}`, the predicted count drops below `A(B)` at depth
  `b ≈ C* · m log_p 2` with `C* = 1/(1 − θ*)`. So (W_B) is implied by Conjecture E at depth factor `C*`
  (any `K > C*`), and it is far weaker than Conjecture E: it needs one upper bound in infinitely many
  windows, at one depth, with the constant `A(B) − 1` instead of an asymptotic.
* **Gap.** Proved depth factor 1 (in base-p digits per digit of n, τ-version, for a density-one set of m; round 5 microrange Corollary D); needed
  depth factor `C*`: 19.98 for 3x+d, 2.38 for split5_3, 3.98 for core K7, 15.84 for split5_1,
  4.06 for desc_split7_1, 3.98 for desc_m3_4n5, 28.42 for m3_b/m3_d, 1907 for m3_g.

Compared with the occupation bound: an escaping orbit has at least `log X / log ρ − O(1)` visits below
X (the selected starts), and at most `W p^θ X^θ + O(log X)` (Theorem 2). These do not meet; nothing
in this file excludes an escaping orbit.

## 6. Expanding maps: the mirror

Let the drift be positive (Δ > 0): 5x+1, 7x+1, core W (S-family `{1,3,7}` mod 8).

**Proposition 6 (no occupation mirror from moments). PROVED.** If `Δ > 0` then for every `s > 0`,
`γ > 0`, `ρ(N_{s,γ}) > 1`; so no certificate (N) exists, and every moment bound of the form (1)
has exponent `> 1`, worse than the trivial `V(X) ≤ N_σ X`. The negative-moment side cannot be used:
Lemma 4 (`log u ≤ u^s/(es)`) is false for `s < 0`.

*Proof.* `f(s, γ) = log ρ(N_{s,γ})` is jointly convex with gradient `(Δ, Λ)` at `(0, 0)` on the closed
class (round 3 Theorem 2(b)), so `f(s, γ) ≥ Δ s + Λ γ > 0`. ∎

**Proposition 7 (conditional chain). PROVED.** For any table map satisfying (P) and (R) (any drift),
and any orbit that is not eventually periodic and satisfies `Σ_t 1/x_t < ∞`, all conclusions of
Theorem 4 hold. Without (R), the update-time conclusions hold: `P_l > P_{t_i}` and `y_l > x_i` for
every update `l > t_i`, and (b)–(e); the raw-time part of (a) can fail. Under (P),
`Σ_t 1/x_t < ∞` implies `sup_t x_t/(x_0 P_t) < ∞`. [Revised after REFEREE2: the earlier text said
"is equivalent to"; only this direction is proved. REFEREE2 notes that for the three maps it is
applied to (5x+1, 7x+1, core W) every `v = 0` step is n/2, so halving chains give the converse; in
general the converse is not proved.]

*Proof.* The proof of Theorem 4 used (N) only through `E < ∞` (Theorem 1), and (R) only in the
raw-time part of (a). `log Z` is a sum of terms between `u/2` and `u`, `u = G/(F y)`, for large y. ∎

**Which expanding examples satisfy (R)** [revised after REFEREE1]. 5x+1 and 7x+1 satisfy (R). **Core
W (S-family `{1,3,7}` mod 8) does not**: the edge from state (4, 1) with residue 5 has raw prefix
slopes 1, 1/2, 3/2, 3/4, and 1/2 < 3/4 = min(1, F_e). A concrete raw drop: on the orbit of 15 the
update value 263 is the last multiplier minimum over a segment of 8000 updates, and the raw orbit
continues 263, 790, 395, 1186, 593, 1780, 890, 445, 446, 223, with raw multiplier 27/32 < 1 and
223 < 263 (`check_revision.py [R3]`). For core W only the update-time conclusions apply. The earlier
text applied Prop. 7 to core W without qualification; that is withdrawn.

So for an expanding map the chain is a *consequence* of divergence plus summability, not a tool: it
gives `A(B)` points of `N^mult` per B octaves, and `N^mult` there is expected to have positive density
(round 3 Theorem 6: the early-drop set has density about 0.82 for 5x+1, so about 18% of starts
survive the first `log n` digits). There is no contradiction to aim for, and no window criterion.

**Non-escaping orbits.** A non-eventually-periodic integer orbit always tends to infinity (Lemma 2),
so the only non-escaping orbits are eventually periodic, and on them `P_t → 0` (Corollary 3.1).
The time-reversed selection (successive last *maximisers* of `P`) exists on such an orbit, but the
height statement has no mirror: on a cycle Z grows by the factor `1/λ` every lap, so a multiplier
maximum need not be a height maximum. The usable statement about cycles is the classical one,
`log(1/λ) = Σ_{cycle} log(1 + G/(F y)) ≤ g L / m` for a cycle of L updates and minimum m (this is
what the repo's cycle-length bounds use). **No useful mirror** of the chain theorem for expanding
maps was found.

**EVIDENCE** (`evidence_expanding.py`, `data/evidence_expanding.out`): on orbit segments of 5x+1
(starts 7, 9; 6000 updates, values to 2^900), 7x+1 (start 3) and core W (start 15), Z is nondecreasing
(at updates; under (P) this is in fact a theorem, the script tests it in floating point),
`Σ 1/y` stays below 0.7, every link ratio of the selected multiplier minima is in `(1, ρ]`,
and the minimum number of selected starts per 10 octaves is exactly `A(10)` for 5x+1 (7) and 7x+1 (5),
and 20 ≥ A(10) = 17 for W. So the count in (e) is attained on these orbits.

## 7. Literature and novelty

* Lagarias, *The 3x+1 problem and its generalizations*, Amer. Math. Monthly 92 (1985); **checked in the
  scanned source** (pp. 11–16): Theorem F gives `|π*(x) − x| ≤ c_1 x^{1−η}`, `η ≈ 0.05004`, for the
  number of n ≤ x without finite stopping time; equation (2.32) deduces that for a divergent
  trajectory D, the set `U_D = {n ∈ D : T^k(n) > n for all k ≥ 1}` has `|U_D ∩ [1,x]| ≤ c_1 x^{1−η}`;
  (2.31) gives the liminf of the odd fraction. Theorem 2 here bounds **all** elements of a divergent
  trajectory below x by `C x^{θ}` with the same exponent `θ = 1 − η` up to the certificate's rounding
  (θ = 1082/1139 = 0.949956, versus 1 − 0.05004 = 0.94996), and with explicit constants. The
  multiplier bound and the chain theorem with `A(B) = max{k : (3/2)^k < 2^B}` for 3x+1 (at least one
  element of `N^mult` in every late octave of the shortcut map's chain) were not found in that survey.
  **Novelty: not checked** beyond that survey.
* Verified range for 3x+1: `2^68`, D. Barina, *Convergence verification of the Collatz problem*,
  J. Supercomputing (2021); **quoted from memory**, not checked. All constants are also given for the
  ranges verified here (`2^32`, exact, `verify_range.c`).

## 8. Revision after REFEREE1

Changes made in response to `REFEREE1.md`. All are checked by `check_revision.py` (exit 0).

1. **Signed multiplier constants (WRONG as computed, now fixed).** `chainlib.multiplier_E_signed`
   used `g` in the self-consistency factor instead of `g' = 2g`. The resulting values for 3x−1
   (24.07889438) and m3_b (50.73726249) were about 1e-9 below the bound that Theorem 3 proves, so they
   were not upper bounds. Recomputed with `g'` in both places: 3x−1 `E* = 24.07889444…`, m3_b
   `E* = 50.73726254…` at the 2^32 range; both are now at or above an independent 50-digit Decimal
   evaluation of the formula (`[R1]`). The headline values (24.1, 50.7) do not change.
2. **Signed raw-time statements.** Theorem 3 and the signed version of Theorem 4 bound Z at updates;
   at raw times inside an edge they need (S1). (S1) holds for both signed named systems (`[R2]`, plus an
   exact test that every raw-time Z on random orbits equals an update-time Z).
3. **(P) restated** as "every `v_r ≥ 0`", which the raw-time steps use. Every non-signed system and
   family member satisfies it (`[R5]`).
4. **Core W fails (R) (claim WITHDRAWN).** Prop. 7 is now stated with its update-time version, which
   is all that applies to core W. The concrete raw drop 263 → 223 is checked (`[R3]`).
5. **Families (coverage statement was WRONG).** 103 negative-drift family members had been dropped
   because the best certificate had `γ > 1`. Since `N_{s,1} = p^{1−γ}N_{s,γ} ≤ N_{s,γ}` entrywise, they
   satisfy (N) with `γ = 1`, `θ = 0`. `chainlib.certificate` now clips γ to 1 and re-checks the clipped
   inequality exactly. The families table now covers all 343 negative-drift members (see README); every
non-certified member has positive drift or a state-graph error. Of the 343, 63 have no edge with
`F > 1`; for them `P_l ≤ 1` and Corollary 3.1 excludes non-periodic orbits outright, so A(B) is not
defined (`chain_table.kstar` looped forever on them before; fixed).
6. **Wording.** Units are needed (§0); Theorem 2 typo `/s`; "edges with `F ≠ 1`" in 4(b), 4(d);
   "survivor mass" is an upper bound for the Haar mass; "survive" in `N_b` means `≥ 1` at raw steps;
   `A(B) = 0` makes Corollary 5 vacuous; Proposition 5.1 is no longer called the main new point.

## 9. Revision after REFEREE2

Changes made in response to `REFEREE2.md` (all proofs confirmed; text fixes only).

1. **Corollary 5: false clause WITHDRAWN.** The clause "or equivalently for this purpose every update
   multiplier over the first b updates is `> 1`", added in the REFEREE1 revision, is false: for
   split5_3 and the S-family every odd start has root-tree update multiplier exactly 1 (root edge
   (1,0) → (2,1) is a pure split with `F = 1`), so read literally the clause would make the criterion
   prove GLOBAL for split5_3. It is replaced by "every root-tree update multiplier over the first b
   updates is `≥ 1`", which the raw condition implies. The criterion itself is unchanged.
2. **Proposition 7:** "`Σ_t 1/x_t < ∞` is equivalent to `sup Z < ∞`" → "implies" (only ⇒ is proved).
3. README wording (positive-drift count 96, "GLOBAL by Cor. 3.1", certified θ for m3_g, range of the
   core multiplier constants); see the README.
