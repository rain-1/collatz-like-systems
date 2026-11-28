# Theorem 5: a mixed 2·3-adic precision lemma for modifications of the 1932 map

**Status.** Lemma P3 is PROVED. The tables are exact computations, each a
proof for the moduli it covers.
Check: `check_theorem5_precision3.py` (about 1 min: Lemma P3 sanity, the swap
table for i ≤ 10, and swT2_8_s8). The runs for i ≤ 12 (all swap sets) and
i ≤ 18 (open cube members) are `scratch/p3all.py` and `scratch/p3big.py`, using
the same code (`precision3.py`).
**Novelty:** not in the repo. It complements the lhf result that the residue
graph of swT9 is strongly connected for moduli not divisible by 3. Literature
novelty: not checked.

## Setting

G(3q) = 2q, G(3q+1) = 4q+1, G(3q+2) = 4q+3 is Collatz's 1932 permutation.
σ(n) = n + δ(n mod 18) with δ ∈ {−1, 0, 1} and σ(Z_{>0}) ⊆ Z_{>0}. Examples are
the swaps σ_A of round 2 (`round2/downfrom5/systems.py`), which exchange n and
n+1 for n ≡ a (mod 18), a ∈ A, with a ≠ 0 so that 1 is not sent to 0.
Q = σ ∘ G. Each branch of G divides by 3 and multiplies by 2 or 4. So Q loses
one ternary digit of precision per step and gains one or two binary digits.

**The full-class graph Γ_i** has nodes Z/(2^i·9). Fix a node y. Its three
subclasses y + 2^i·9·k (mod 2^i·27), k = 0, 1, 2, each have a fixed G-branch.
On such a subclass, G(n) runs through a progression of difference a·2^i·9
(a ∈ {2, 4}), so G(n) mod 18 is fixed and σ acts as a fixed translation. Hence
Q maps the subclass into a single class y_k' mod 2^i·9. The edges are y → y_k'.

## Lemma P3

Let U be a nonempty union of residue classes mod 2^i·3^j (i, j ≥ 0) with
Q(U) ⊆ U. Then U contains a full class Y mod 2^i·9 together with every class
reachable from Y in Γ_i.

*Proof.*
1. *j ≤ 2.* Classes mod 2^i·3^j are unions of classes mod 2^i·9, so U is a union
   of full classes. Take a full class Y ⊆ U and an edge Y → Y'. Some subclass Z
   of Y has Q(Z) ⊆ Y'. U is a union of classes mod 2^i·3^j and contains a point
   of Y', so it contains the class of that point, which includes Y'.
2. *j ≥ 3, reaching precision 2.* Take a class Z₀ = {r + 2^i 3^j t} ⊆ U. While
   the 3-adic exponent of the difference is ≥ 3, the G-branch is fixed (n mod 3)
   and so is G(n) mod 18 (exponent ≥ 2 after the step). So Q maps the
   progression to a progression whose difference has 3-adic exponent one lower
   and 2-adic exponent one or two higher.
3. After j − 2 steps we get a progression {y + 2^{i'}·9·u·t} ⊆ U with i' ≥ i and
   u a unit. Its residues mod 2^i 3^j are all the classes ≡ y (mod 2^i·9), so U
   contains the full class Y = y mod 2^i·9.
4. *Edges.* For an edge Y → Y' via the subclass Z, Q(Z) is a progression of
   difference 2^{i+1 or i+2}·9 inside Y'. By the residue count of step 3, U
   contains all of Y'. Induct. ∎

**Corollary P3.** If every sink component of Γ_i contains the class of s, then
no union of residue classes mod 2^i·3^j, for any j, separates s: it would
contain the class of s, hence s.

**Scope.** Corollary P3 concerns separators that are *pure* unions of residue
classes. As for Theorem 4, it says nothing about a "separator with finite
exceptions" (a union of classes minus a finite set), since a finite exception
set could remove s itself. Below, "congruence separator" means a pure union of
residue classes.

**Monotonicity.** Projection mod 2^i·9 sends edges of Γ_{i+1} to edges of Γ_i.
Lifting the three subclasses shows the out-edges correspond, so the preimage of
a closed set is closed. So if level i is not obstructed, neither is level i+1.
Equivalently, obstruction at level I implies obstruction at every level ≤ I.

## Results (seed 8)

Swap sets A ⊆ {1, …, 17} with |A| ≤ 2, swapped pairs disjoint, 138 sets in all.

| outcome | sets |
|---|---|
| 8 is periodic (simulation, cap 3000) | 68 |
| obstructed at every level i ≤ 10 (check), and ≤ 12 (`scratch/p3all_12.txt`) | 67 |
| **not obstructed** | 3: (9, 15) from i = 2, (7, 10) from i = 5, (2, 8) from i = 8 |

For the three unobstructed sets, the closure of Q(8)'s class in Γ_i avoids 8,
which gives a separator mod 2^i·9:

* **(9, 15), modulus 36.** This recovers round 2's swT9_15_s8 certificate,
  a sanity check of the method.
* **(7, 10), modulus 288.** This is a new separator. The orbit of 8 shows no
  fall in 20000 steps, so it is probably eventually monotone. Not written up.
* **(2, 8), modulus 2304.** A new, non-monotone system: `swT2_8_s8.md`.

**Open cube members.** For G itself, {9} (swT9, CLS-055), {3}, {3, 9} and
{3, 15}, every sink component of Γ_i contains the class of 8, for every
i ≤ 18 (`scratch/p3big.txt`, `scratch/p3big18.txt`; Γ_18 has 2.4 million
nodes). For i ≤ 11, Γ_i is even strongly connected. So:

> **No union of residue classes modulo 2^i·3^j with i ≤ 18 and any j ≥ 0 is a
> separator for 8 under swT9 (CLS-055), nor under σ_{3}, σ_{3,9}, σ_{3,15}.**

Round 2 checked moduli ≤ 150, and lhf proved the case 3 ∤ K. Every 3-power is
now covered, for 2-parts up to 2^18. Moduli with prime factors ≥ 5 together with
3 | K are not covered.

## What would finish it

A proof that Γ_i is strongly connected for all i, for A = {9}, would exclude
congruence separators at every modulus 2^i 3^j for CLS-055. The obvious
induction fails. Γ_{i+1} → Γ_i has unique forward path lifting (the subclass
labels k correspond), but it is not a covering: two lifts can map to the same
node, because Q multiplies by 2 or 4. So strong connectivity needs a monodromy
argument on the added binary digit, through the constants that σ and the
3-adic branch choices contribute. I did not complete this; it is OPEN.
