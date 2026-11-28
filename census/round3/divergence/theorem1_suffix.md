# Theorem 1: suffix maps never need automata (non-injective version)

**Status: PROVED.** Check: `check_theorem1_suffix.py` (exit 0, about 2 s).
**Novelty:** the argument is the standard pumping argument for deterministic
suffix (equivalently pushdown) rewriting. Round 2 (`round2/automata/auto_sfx7_s17.md`)
proved the injective special case, citing `output/pdf/suffix_orbit_theorem.pdf`.
The non-injective statement and the cycle-free certificate are, to my knowledge,
not in the repo. Literature novelty: not checked.

## Setting

Fix a base b ≥ 2. A **b-suffix map** is a finite list of rules A_i → B_i, where
A_i and B_i are words over {0,…,b−1} and the A_i form a complete suffix code:
every left-infinite word has exactly one A_i as a suffix. Arithmetically the rule
reads n = b^|A| q + [A] ↦ b^|B| q + [B] for q ≥ 0. We also require that T maps
positive integers to positive integers. The B_i are arbitrary, so T may be
non-injective and non-surjective. Write ℓ = max |A_i|.

Examples are `perm_suffix_*` in the catalog, `auto_sfx7_*` from round 2, and the
binary maps "n even → n/2^k, n odd → 2^j n + c with c < 2^j".

A **divergence certificate** for (T, s) is a set C with T(C) ⊆ C, T(s) ∈ C, and
no T-periodic point in C. Such a C proves that the orbit of s is not eventually
periodic, so the orbit is infinite and unbounded. For non-injective maps this is
the right notion: a separator (s ∉ C) proves only that s does not return.

## Theorem 1

Let T be a b-suffix map and s ≥ 1. Exactly one of the following holds.

1. The orbit of s is eventually periodic.
2. There are t₀ ≥ 0, p ≥ 1, a nonempty word P with a nonzero first letter, words
   Y₀,…,Y_{p−1} of length ≥ ℓ, and a nonempty word V, such that
   * T^{t₀}(s) = [P Y₀], and
   * for every integer z ≥ 0 and 0 ≤ i < p,
     T(b^{|Y_i|} z + [Y_i]) = b^{|Y_{i+1}|} z + [Y_{i+1}], where Y_p := V Y₀.

In case 2:

* (a) T^{t₀ + kp}(s) = [P V^k Y₀] for all k ≥ 0. This is a strictly increasing
  subsequence, so the orbit is infinite and **tier 1 suffices**.
* (b) C = ⋃_{i<p} {b^{|Y_i|} z + [Y_i] : z ≥ 1} ∪ {T(s), …, T^{t₀}(s)} is a
  divergence certificate. It is a union of p residue classes modulo
  b^{max|Y_i|}, minus the p elements with z = 0, plus a finite set. So **a
  congruence-plus-finite certificate always exists**, and finite automata in
  base b (or any other base) add nothing for this class.
* (c) The dichotomy is decidable: simulate until a value repeats (case 1) or a
  pump witness (t₀, t₀+p) as below appears (case 2). A witness must have
  h_{t₀} > ℓ, so that P is nonempty and [P] ≥ 1. One of the two happens.

## Proof

Let w_t be the canonical base-b word of x_t = T^t(s), with h_t = |w_t|. A rule
reads at most the last ℓ letters. If |w| < ℓ, pad with leading zeros; the
arithmetic form handles this.

*Case 1 or unbounded heights.* If h_t does not tend to infinity, then some
height h occurs infinitely often. Only finitely many words have length h, so a
value repeats and the orbit is eventually periodic. So assume h_t → ∞.

*Future-minimum times.* Call t a future-minimum time if h_{t'} ≥ h_t for all
t' ≥ t. Since h_t → ∞, the minimum of h over [t, ∞) is attained, so
future-minimum times exist and form an infinite set with h → ∞ along it.

*Frozen prefix.* Let t be a future-minimum time with h_t > ℓ. Write
w_t = P Y with |Y| = ℓ; P is nonempty and starts with a nonzero letter. Claim:
for all t' ≥ t, w_{t'} = P Y_{t'} with |Y_{t'}| = h_{t'} − |P| ≥ ℓ, and the
sequence Y_{t'} does not depend on P. The proof is by induction. At time t',
the word has length ≥ h_t = |P| + ℓ, so the rule matched is determined by the
last ℓ letters, which lie inside Y_{t'}. Rewriting A ↦ B inside Y_{t'} gives
Y_{t'+1}, of length h_{t'+1} − |P| ≥ ℓ. The letters of P are never read or
written.

*Pumping.* There are infinitely many future-minimum times and only b^ℓ words of
length ℓ. So there are future-minimum times t₀ < t₁ with the same last-ℓ word Y
and h_{t₁} > h_{t₀}. The heights are not equal, because equal heights would give
w_{t₁} = w_{t₀} and an eventually periodic orbit. By the frozen prefix at t₀,
w_{t₁} = P V Y with V nonempty. Put p = t₁ − t₀ and Y_i = the suffix of
w_{t₀+i} after P (0 ≤ i < p). Each step from Y_i to Y_{i+1} rewrites inside
Y_i, which has length ≥ ℓ. So it is the same rewrite for every prefix, and
T(b^{|Y_i|} z + [Y_i]) = b^{|Y_{i+1}|} z + [Y_{i+1}] holds as an identity in z
(Y_p = V Y₀). This proves the dichotomy.

*(a)* Composing the p identities gives T^p(b^{|Y₀|} z + [Y₀]) =
b^{|Y₀|}(b^{|V|} z + [V]) + [Y₀]. Start from z = [P] and iterate. The map
z ↦ b^{|V|} z + [V] satisfies b^{|V|} z + [V] ≥ 2z > z for z ≥ 1.

*(b)* Let C_i = {b^{|Y_i|} z + [Y_i] : z ≥ 1}. The identities give T(C_i) ⊆ C_{i+1}
for i < p−1 and T(C_{p−1}) ⊆ C₀ with z ↦ b^{|V|} z + [V] ≥ 1. So
C' = ⋃ C_i is forward closed. Every x ∈ C' has the form T^i(b^{|Y₀|} z + [Y₀])
with z ≥ 1, up to renaming the starting index. Its T^p-iterates have strictly
increasing z, so its orbit is unbounded and x is not periodic. Adding the
finitely many points T(s), …, T^{t₀}(s) keeps the set forward closed, because
T^{t₀}(s) = [P Y₀] ∈ C₀. These points are not periodic either, since their orbits
reach C'. T(s) ∈ C holds when t₀ ≥ 1. When t₀ = 0, s ∈ C₀ and T(s) ∈ C₁.

*(c)* A pump witness (t₀, t₁) needs only these finite checks: h_{t₀} > ℓ, the
last ℓ letters agree, h_{t₁} > h_{t₀}, and h_{t'} ≥ h_{t₀} for t₀ ≤ t' ≤ t₁.
The condition h_{t₀} > ℓ is needed: it makes the prefix P nonempty, so
[P] ≥ 1. Without it, (a) can fail, for example when V consists only of zeros
and P is empty. (`suffix_maps.decide` enforces this as `len(w0) > ell`.) These suffice,
because the frozen-prefix argument used only the heights on [t₀, t₁], not
future-minimality. Future-minimality was needed only to show that a witness
exists. So the search "repeat, or witness" terminates. ∎

## Consequences and remarks

* **Separators.** For injective T and an infinite orbit, replace C' by
  T^{Np}(C'). Its elements have z ≥ b^N, so s ∉ T^{Np}(C') once N is large.
  This recovers round 2's tier collapse for suffix permutations.
* **Divergent set.** The divergent set of a b-suffix map contains a full
  residue class whenever it is nonempty: every pump witness gives the class C₀.
  So no b-suffix map has a "thin" divergent set. This is the reason the thin-set
  examples in this folder (race_s21) must use mixed slopes.
* **Where automata could help.** Theorem 1 shows that a finite automaton can be
  stronger than a congruence certificate only when the slopes are not all powers
  of b. The rest of this folder works in that regime: mixed slopes
  (fx10_64_s7, perm12_s7) and FRACTRAN-type maps (race_s21).

## Check (`check_theorem1_suffix.py`)

* 400 random b-suffix maps (b = 2, 3; non-injective allowed) × seeds 1..29. Each
  case is decided by the procedure (c). Every pump case has its certificate
  re-verified exactly: the symbolic rewrite of each Y_i, plus numeric identities
  at z ∈ {0, 1, 2, 12345, 10^30+7}. Every periodic case is confirmed by
  simulation.
* The round-2 permutation SFX7, seed 17, gives a pump. So does the explicit
  non-injective map below, whose certificate is printed.
