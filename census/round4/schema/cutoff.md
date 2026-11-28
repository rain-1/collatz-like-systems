# Part B1: cut-off approximants cannot reach a type-(c) system

Lens "schema", round 4. Revised after REFEREE1 (B1 itself was confirmed; only the
j ≤ 2 wording changed). Check: `check_cutoff.py` (exits 0, about 1 minute). Library:
`schemalib.py`.

The plan of task (B) was to approximate a type-(c) system T by systems T_j that agree
with T except on a cylinder of depth j around the expanding point, where the run is cut
off; to certify each T_j; and to pass to the limit. This file proves that the plan fails
at the first step. For large j **no** such T_j is certifiable, whatever is put on the
cut-off cylinder: T_j is again of type (c). The same holds for cut-offs around any finite
set of points. For K7 and for 3x+1 the threshold is computed exactly.

Setting and notation are those of `round3/accel/trichotomy.md`: a unit-multiplier p-adic
system (p, m, table) satisfying the standing hypothesis (every cycle of the cylinder graph
contains a division), the cylinder graphs G_K, the Markov property (M), and the types
(a), (b), (c) of an SCC.

## Theorem B1 (cut-offs inherit free re-entry). PROVED

Let T have a type-(c) SCC. Let F ⊂ Z_p be any finite set. Then there is J0 such that the
following holds for every J ≥ J0, every K′ ≥ J, and every unit-multiplier table T′ at
modulus p^{K′} that satisfies the standing hypothesis and agrees with T on each class mod
p^{K′} disjoint from U_J(F) = ∪_{f∈F} (f + p^J Z_p): **G_{K′}(T′) has an SCC of type (c).**
Consequently (Theorem N) T′ has no descent certificate and no generalized (accelerated)
certificate, and Theorem H does not apply to it.

The typical case is F = {x\*}, or F = O(x\*), for the expanding periodic point x\* of the
run. T′ is then "T with the run cut off at depth J", and the replacement dynamics on the
cut-off cylinder is arbitrary.

*Proof.*

**Step 1 (blocks).** Let Σ be a type-(c) SCC of G_K, C an expanding simple cycle in it
(ℓ edges, multiplier λ_C > 1), and r a node of C. As in the proof of Theorem N there is a
closed walk W at r inside Σ that is not a power of C. Write W = C^k W′, where W′ does not
begin with a full copy of C. W′ is a nonempty closed walk at r and not a power of C. Since
r occurs once on the simple cycle C, W′ also leaves C^∞ within its first ℓ edges.

For d ≥ 1 put A_d = C^d W′ and B_d = C^{d+1} W′. Then λ(A_d) = λ_C^d λ(W′) > 1 for all
d ≥ d0.

**Step 2 (the sets X_d).** Let Y_d be the set of x ∈ Z_p whose level-K walk is an infinite
concatenation of blocks A_d and B_d, and put X_d = ∪_{0 ≤ t < |B_d|} T̂^t(Y_d). Then:

* Y_d is closed. It is the intersection over n of the finite unions of cylinders whose
  walk prefix of length n extends to a concatenation; by König's lemma this is the set of
  points whose whole walk is a concatenation. So X_d is compact.
* T̂(X_d) ⊂ X_d, because after a full block a point of Y_d is again in Y_d.

Call a maximal factor of a walk that is also a factor of C^∞ a *C-stretch*. In a
concatenation, every block contributes one C-stretch that contains its C^d or C^{d+1}
part. That stretch has length between dℓ and (d+1)ℓ + |W′| + ℓ: it can extend at most
|W′| to the left, into the previous W′, and fewer than ℓ steps to the right, because W′
leaves C^∞ within its first ℓ edges. Every other C-stretch lies inside a single W′ and has
length ≤ |W′|. So for x ∈ X_d with dℓ > |W′|, the set of lengths > |W′| of C-stretches that
occur infinitely often in the walk of x is nonempty and contained in
I_d = [dℓ, (d+2)ℓ + |W′|]. If d′ ≥ d + 3 + |W′|/ℓ, then I_d and I_{d′} are disjoint, so
**X_d ∩ X_{d′} = ∅**. This gives infinitely many pairwise disjoint compact invariant sets.

**Step 3 (choice of d and J0).** F is finite, so it meets at most |F| of these pairwise
disjoint sets. Choose d ≥ d0 with dℓ > |W′| and X_d ∩ F = ∅. X_d is compact and F ∉ X_d,
so for each f ∈ F some ball f + p^{J_f} Z_p misses X_d. Put J0 = max_f J_f (and J0 ≥ K).
For J ≥ J0, X_d ∩ U_J(F) = ∅.

**Step 4 (T′ = T on X_d).** U_J(F) is a union of classes mod p^J, and K′ ≥ J. So every
class mod p^{K′} either lies in U_J(F) or is disjoint from it. Each x ∈ X_d lies in a class
disjoint from U_J(F), and there T′ has T's branch. So T̂′ = T̂ on X_d, and X_d is a
T̂′-invariant set carrying the same dynamics.

**Step 5 (two periodic orbits through one node).** Let y_A be the periodic point of the
closed level-K walk A_d, and y_i the periodic point of A_d^i B_d. Both exist and are unique
by (M), since every block contains a division. Both lie in X_d, so their orbits are
T̂′-orbits. Their residues mod p^{K′} trace closed walks Γ_A and Γ_i in G_{K′}(T′). The
points y_A and y_i follow the same level-K walk A_d^i, which has at least i divisions. So
y_i ≡ y_A (mod p^{K+i}), and for i ≥ K′ − K the two closed walks pass through the same
node z0 = y_A mod p^{K′}. Hence Γ_A and Γ_i lie in one SCC Σ′ of G_{K′}(T′). Γ_A has
multiplier λ(A_d) > 1. A closed walk splits into simple cycles, and its multiplier is
their product, so Σ′ contains an expanding simple cycle, and Σ′ is not of type (a).

**Step 6 (Σ′ is not a single simple cycle).** Suppose Σ′ were a single simple cycle Z.
Then Γ_A and Γ_i, both closed walks from z0 inside Σ′, are powers of Z, so y_A and y_i
both follow Z^∞ from z0. Z contains a division (standing hypothesis for T′), so by (M) at
most one point does this, and y_A = y_i. But their level-K walks differ. A_d^∞ and
(A_d^i B_d)^∞ agree up to position i|A_d| + dℓ. From there, B_d continues with a full
copy of C, while A_d starts W′, which leaves C^∞ within ℓ edges. A point determines its
walk, so this is a contradiction. Hence Σ′ has an expanding cycle and at least one other
cycle: it is of type (c). Theorem N applies to T′ because T′ satisfies the standing
hypothesis. ∎

**Remark (why this is the right negative statement).** Theorem N already says T has no
generalized certificate. Theorem B1 says more: no system that differs from T only near
finitely many points has one either. A family T_j that "converges to T" in the cylinder
sense is eventually of type (c), so it contains no certified member to take a limit of.
An approximant that is certifiable must modify T on a set that meets every one of the
disjoint invariant sets X_d. Such a set cannot shrink to finitely many points. Part B2
(window.md) builds approximants of exactly this kind.

## Instances: K7 and 3x+1, with exact thresholds

**3x+1** (accelerated, level 1; x\* = −1, multiplier 3/2). Take the blocks
A = (1, 1, 0), which is the cycle −5 → −7 → −10 with multiplier 9/8, and B = (1, 0), with
multiplier 3/4. Both are closed at node 1. An odd run (consecutive odd steps) started at x
has length exactly v₂(x+1). In any A/B concatenation the longest odd run is 2. So every
point of X has v₂(x+1) ≤ 2 at all times, which means X avoids U_3 = {x ≡ −1 mod 8}. The
argument of Steps 4 to 6 then applies with J0 = 3. So **every system that agrees with
3x+1 off the class −1 mod 2^j, for j ≥ 3, is of type (c)**. For j = 2, the reset cut-off
n ≡ 3 (mod 4) ↦ (n+1)/4 is CERT, with the single cycle (1 2). For j = 1 the reset
n odd ↦ (n+1)/2 is trivially CERT. So the reset cut-off of 3x+1 is CERT exactly for
j ≤ 2 (the first version of the README said "only for j = 2"; corrected after REFEREE1).

**K7** (z even ↦ z/2, z ≡ 3 (4) ↦ (3z+1)/2, z ≡ 1 (4) ↦ (z−1)/4; checked in the coordinate
n = z + 1, where x\* = 0 has multiplier 3/2). Take the blocks A = A⁴Q, that is
z ≡ −1 (mod 32) followed by four (3z+1)/2 steps and one (z−1)/4 step, with multiplier
(3/2)⁴/4 = 81/64 and periodic point z = −49/17; and B = A⁴QH, with multiplier 81/128. A
3z+1 run started at z has length v₂(z+1) − 1. In A/B words the longest run is 4, so
v₂(z+1) ≤ 5 at all times, and J0 = 6. So **every system that agrees with K7 off the class
z ≡ −1 (mod 2^j), for j ≥ 6, is of type (c)**. The reset cut-offs with j = 2, 3, 4, 5 are
CERT, and each has the single cycle z = 0 (n = 1). For example, K7 with z ≡ 31 (mod 32)
↦ (z+1)/32 − 1 is settled. These four are cheap neighbours, not claimed as interesting.

| system | cut-off depth j | verdict (decide.py, exact) | proof for all j |
|---|---|---|---|
| 3x+1 | 1, 2 | CERT; j = 1: cycle (1); j = 2: cycle (1 2) | – |
| 3x+1 | 3 … 14 | OBST, type (c) (SCC = the whole graph) | Theorem B1, J0 = 3 |
| K7 | 2, 3, 4, 5 | CERT, cycle z = 0 | – |
| K7 | 6 … 14 | OBST, type (c) | Theorem B1, J0 = 6 |

`check_cutoff.py` checks: the type-(c) witnesses of K7 and 3x+1 [C1]; the run-length
formulas on 1..4095, the maximal runs in A/B words, and the exact periodic points y_A,
y_{A^iB} (i ≤ 12), whose orbits avoid U_J, which differ, and which agree mod 2^{K+i} [C2];
and the verdicts in the table [C3].

## What this says about task (B)

The cut-off schema "T_j = T except on a depth-j cylinder around x\*" has certified
members only for j < J0, that is, for cut-offs that remove a fixed, non-shrinking set
(density 1/4 for 3x+1, ≥ 1/32 for K7). No induction on j is possible: from j = J0 on there
is no certificate to induct on. The obstruction is the same free re-entry as in Theorem N,
but now in a sharper form. The re-entry orbits y_A are expanding periodic orbits that stay
a bounded distance away from x\*, for example −5 for 3x+1 and −49/17 for K7. Cutting near
x\* never touches them.
