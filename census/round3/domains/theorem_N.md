# Theorem N: cycles of positive full-branch maps are necklaces

Check: `check_split_family.py` (parts N1–N3, about 7 s) for the 2-adic and 3-adic
instances. `check_rings.py` covers the quadratic-order instances.

## Setting

Let F be a number field, π a prime of its ring of integers O, O_π the π-adic
completion, and |·|_π the π-adic absolute value. (For F = Q, π = p this is just Z_p.)
Let U ⊂ O_π be the units, U = O_π \ πO_π. A **full-branch block system** is a
countable family of affine maps `B_i(x) = α_i x + β_i` (α_i, β_i ∈ F, i ∈ I),
together with pairwise disjoint sets C_i ⊂ U, such that:

* (F1) `U \ X = ⊔_i C_i` for a finite exceptional set X;
* (F2) `B_i` maps `C_i` bijectively onto U;
* (F3) `|α_i|_π ≥ q > 1` for every i (automatic when α_i = u/π^k with u a unit and
  k ≥ 1).

The accelerated map is `G(x) = B_i(x)` for x ∈ C_i. A Collatz-type map T on O_π,
which divides by π on πO_π and applies the branch affine map on U, gives such a
system when "branch, then divide out all π" is the block B_i. Then C_i is the set where
exactly k factors π come out, and X is the set of points sent to 0.

## Theorem N

1. *For every finite word w = i_1 … i_n there is exactly one x_w ∈ C_{i_1} with
   G^n(x_w) = x_w and itinerary w. It is `x_w = β_w/(1 − α_w)` ∈ F, where
   `B_w = B_{i_n} ∘ … ∘ B_{i_1} = α_w x + β_w`.*
2. *Periodic points of G are exactly these x_w, and G-cycles correspond bijectively to
   primitive necklaces (primitive words up to rotation). The periodic points of T are
   0 (if T(0) = 0) together with the T-orbits of the x_w.*
3. *(Archimedean control.) Let σ be an embedding F → C with |σα_i| ≤ λ < 1 and
   |σβ_i| ≤ M for every i. Then |σ x_w| ≤ M/(1 − λ). If F = Q and every α_i > 0,
   β_i ≥ 0, then x_w ≥ 0, with equality only when β_w = 0.*
4. *(Integral models.) Let Λ be a lattice δ^{-1}O with π ∤ δ, and suppose T maps Λ into
   itself and every embedding σ satisfies the hypothesis of 3. Then every T-orbit in Λ
   is bounded in every embedding, so it is eventually periodic, and the cycles of T on
   Λ are {0} (when T(0) = 0) plus one cycle for each primitive necklace w with
   x_w ∈ Λ.*

*Proof.* (1) Let C_w be the set of x ∈ U whose G-itinerary starts with w. By (F2) and
induction on n, B_w maps C_w bijectively onto U: C_w = C_{i_1} ∩ B_{i_1}^{-1}(C_{w'})
with w = i_1 w′, and B_{i_1}: C_{i_1} → U is a bijection. Its inverse
B_w^{-1}: U → C_w ⊂ U is affine with π-adic Lipschitz constant |α_w|_π^{-1} ≤ q^{-n} < 1
by (F3). U is closed in the complete space O_π, so by Banach's fixed-point theorem
B_w^{-1} has a unique fixed point x_w ∈ U. It lies in C_w and has itinerary w.
Because |α_w|_π > 1 we have α_w ≠ 1, so the affine map B_w has exactly one fixed
point in F ⊗ Q_π, namely β_w/(1 − α_w). Any x ∈ C_w with G^n x = x is a fixed point of
B_w, so it is this point.

(2) A G-periodic x of period n has a well-defined itinerary w (by (F1), and a periodic
orbit avoids X because points of X leave U for good). Then x = x_w. Two distinct
primitive necklaces give distinct itineraries, and the itinerary is determined by x,
so they give distinct cycles. Rotations of w give the points of the same cycle. A
T-periodic point either meets U, and then its U-points form a G-cycle, or it never
meets U. In that case x ∈ π^n O_π for every n, so x = 0.

(3) Every B_i maps the closed disc |σz| ≤ M/(1 − λ) into itself:
|σB_i z| ≤ λ M/(1−λ) + M = M/(1−λ). So the fixed point of the contraction σB_w lies in
it. The sign statement holds because a composite of maps with positive slope and
nonnegative constant has the same form.

(4) Write a T-orbit as a sequence of blocks. Each block satisfies
|σ(next)| ≤ λ|σ(x)| + M in every embedding (the divisions by π contract), so every
orbit is bounded in the Minkowski embedding. Λ is discrete there, so the orbit is
finite, and T maps Λ to Λ, so the orbit is eventually periodic. The rest is (2). ∎

## Instances used in this folder

| map | p or π | blocks (k range) | X | where |
|---|---|---|---|---|
| split S (split_d, splitB_d) | 2 | A_k: (3x+1)/2^k on x≡1 (4), B_k: (x+1)/2^k on x≡3 (4), k ≥ 2 | {−1/3, −1} | split_family.md |
| 1x+1 (par_1_d) | 2 | (x+1)/2^k, k ≥ 1 | {−1} | onexd.md |
| m3_c, m3_a | 3 | (2x+1)/3^k on x≡1, (2x+2)/3^k on x≡2, k ≥ 1 | {−1/2, −1} | below |
| m3_f | 3 | (x+2)/3^k on x≡1, (x+1)/3^k on x≡2, k ≥ 1 | {−2, −1} | below |
| Gaussian u z + c, u a unit | 1+i | (uz+c)/π^k, k ≥ 1 | {−c/u} | gaussian.md |
| Eisenstein, Z[√−2], Z[√2] analogues | 1−ω, √−2, √2 | (uz+c)/π^k | {−c/u} | rings.md |

(F2) is checked at finite level for the 2- and 3-adic instances (check N1): the
cylinder of exact valuation k maps onto every unit class modulo p^N, with the right
multiplicity, for k ≤ 12 and N ≤ 8. It also follows by hand. Take x ≡ 1 (mod 4) with
v_2(3x+1) = k ≥ 2. The map x ↦ (3x+1)/2^k is a bijection Z_2 → Q_2. The preimage of
an odd u is x = (2^k u − 1)/3, which is ≡ −1/3 ≡ 1 (mod 4) automatically. The other
blocks work the same way.

**Corollary (split).** Every nonzero cycle of the split map S over Z_(2) ∩ Q is positive,
its odd points lie in (0, 1], and the cycles correspond bijectively to primitive
necklaces over {A_k, B_k : k ≥ 2}. For w with a A-letters and total exponent K,

  `x_w = c_w/(2^K − 3^a)`,  `c_w = Σ_j 3^{#A after j} · 2^{K before j}`.

The bound: 0 < x_w ≤ max_i β_i/(1−α_i) = max(1/(2^k−3), 1/(2^k−1)) = 1 (attained by
A_2, the cycle 1 → 4 → 2 → 1). There are no other 2-adic periodic points at all: no
irrational ones and no negative ones. Check N2 recomputes x_w exactly for all 1376
primitive necklaces with K ≤ 13 and confirms the itinerary and periodicity by exact
2-adic residue arithmetic on Fractions.

**Corollary (m3_a, m3_c, m3_f on (1/d)Z, 3 ∤ d).** These have the same shape (p = 3,
positive slopes 2/3^k or 1/3^k, positive constants). Every cycle on (1/d)Z other
than 0 is positive, cycles correspond to necklaces, and their odd points lie in
(0, max β/(1−α)] = (0, 1] for m3_c (A_1: (2x+1)/3, fixed point 1) and (0, 1] for m3_f
(fixed points of (x+2)/3 and (x+1)/3 are 1 and 1/2). On Z this recovers the Theorem Z
table: m3_c has cycles {0}, {1, 3}, {2, 6}, and m3_f has {0}, {1, 3}.

## Novelty

The block-system / necklace description of periodic points is standard symbolic
dynamics. For 3x+1 the formula x_w = c_w/(2^K − 3^a) is Böhm–Sontacchi (1978). That
nonnegative constants plus contracting blocks force every rational cycle to be
positive, and that the split family is exactly such a system, are as far as I know not
written down. Novelty not checked.
