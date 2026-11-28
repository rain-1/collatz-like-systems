# Theorem 3: ascent traps (congruence certificates of divergence for non-injective maps)

**Status: PROVED.** These are the lemmas used by fx10_64_s7, fx26_32_s7 and
c62_64_s27. The engine is `divlib.py`, and each system's check script re-verifies
its witness exactly.
**Novelty:** this is the expanding counterpart of round 2's descent Lemma A/B
(`round2/descent/lemmas.md`). The itinerary lemma is the one in
`round2/downfrom5/swT9_15_s8.md`, re-proved below. The combination as a
cycle-free certificate for non-injective maps is, to my knowledge, new to the
repo. Literature novelty: not checked.

## Setting

T(n) = (a_r n + b_r)/d_r for n ≡ r (mod L), with a_r, d_r ≥ 1. On each class
the slope is λ_r = a_r/d_r and the offset β_r = b_r/d_r. For K a multiple of L,
the **residue graph mod K** has an edge u → v when T maps some (equivalently,
infinitely many) members of the class u mod K into the class v mod K. The
residues of T on the class u are exactly T(u₀) + gZ (mod K), where
g = gcd(a K/d, K) (divlib.images). A union U of classes mod K is forward closed
(T(U) ⊆ U) iff no edge leaves U. This is exact.

## Lemma A↑ (ascent)

Let U be a forward-closed union of classes mod K such that
(i) every closed walk of the residue graph inside U has slope product > 1, and
(ii) β_r ≥ 0 on every class of U.
Then U contains no periodic point. So every orbit that meets U is unbounded.

*Proof.* Take a cycle x₀ → x₁ → … → x_p = x₀ inside U. Its classes mod K form a
closed walk in U, because each x_{i+1} = T(x_i) gives an edge. Composing the
affine steps gives x₀ = A x₀ + B with A = ∏ λ > 1 by (i) and B ≥ 0 by (ii), since
B is a sum of products of the β's and λ's. Then (1 − A) x₀ = B ≥ 0 forces
x₀ ≤ 0, a contradiction. An eventually periodic orbit through U would contain a
cycle in U, because U is forward closed. ∎

**Exact witness.** Condition (i) involves logarithms. We certify it with
integers W_u ≤ N log₂ λ_u, each checked by 2^{W_u} d^N ≤ a^N (N = 64), and an
integer potential φ with S·W_u − 1 + φ(u) − φ(v) ≥ 0 on every edge u → v of U,
where S = |U| + 1. Summing over any closed walk of length ℓ gives
S·ΣW ≥ ℓ > 0, so ΣW ≥ 1 and ∏ λ ≥ 2^{1/N} > 1. The potential is found by
Bellman–Ford; `verify_ascent` re-checks the inequalities.

## Lemma F (forced falls)

Call a class a *fall class* if T(x) < x for every positive member x. If every
closed walk in U passes through a fall class, then every orbit in U has
infinitely many falls. It also has infinitely many rises, being unbounded.
Equivalently, the subgraph on non-fall classes is acyclic, which is checked by
DFS.

*Proof.* Any V+1 consecutive classes visited by the orbit (V = |U|) contain a
repetition, hence a closed sub-walk, hence a fall step. ∎

## Lemma I (aperiodic itinerary)

Suppose some prime p has v_p(∏ λ) ≤ −1 on every closed walk in U. Then an
infinite orbit in U has a non-eventually-periodic sequence of classes mod K.
In particular the orbit admits no affine pump on a residue class (a class mod
K on which some T^h acts as one affine map and which the orbit revisits
periodically), so the "monotone affine subsequence" tier-1 shortcut is
unavailable. What is proved is only that the itinerary mod K is not eventually
periodic.

*Proof.* Suppose the itinerary is eventually periodic with period word w.
Then x_{k+jh} − x* = A^j (x_k − x*), where A = ∏_w λ, v_p(A) = −e ≤ −1, and
x* = B/(1−A) is rational. The right side is nonzero (otherwise the orbit is
periodic) and has p-adic valuation −ej + const → −∞. The left side has valuation
≥ min(0, v_p(x*)). Contradiction. The witness is again a potential, for the
weights −(v_p(a) − v_p(d)) (`aperiodic_certificate`, `verify_aperiodic`). ∎

## Lemma B↑ (what kills an ascent witness)

Let ω be a periodic point (an integer, or a point of the K-adic completion) of
T with multiplier ∏ λ ≤ 1 over its period. If every class mod K visited by ω
lies in U, the classes of ω form a closed walk in U with product ≤ 1, so (i)
fails for U at modulus K. If ω is in the closure of U, this happens at every
finer modulus K'. In particular U must avoid every integer cycle: Lemma A↑ is
exact for real cycles. It can fail on U that are in fact cycle-free because of
2-adic contracting periodic points. That is the analogue of round 2's Lemma B.

## Relation to automata

Lemma A↑ certificates are congruence certificates (tier 2). Theorem 1 shows they
always suffice for b-suffix maps. Theorem 4 (`theorem4_precision.md`) shows that
for 2-adic maps with odd numerators, every congruence trap at any modulus
contains a trap at the map's own modulus. The race map (`race_s21.md`) is the
contrasting case: congruence traps do not exist at all, but a 2-state base-6
automaton works.
