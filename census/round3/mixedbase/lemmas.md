# Mixed-radix lemmas (lens "mixedbase", round 3)

These are the round-2 descent lemmas (census/round2/descent/lemmas.md), restated for maps whose branch depends on n modulo a number M0 with several prime factors (for example M0 = 2·27). Such a map is continuous on the product

    Z_S = prod_{p | M0} Z_p ,

and in general it is not continuous on any single Z_p. A one-prime engine cannot even state these maps. The proofs below are the round-2 proofs with "p-adic" replaced by "S-adic". I give them in full because everything in this folder rests on them.

**Setting.** A *table map* is (M0, table), with table[ρ] = (u, v, w) for ρ mod M0, meaning T(n) = (u n + v)/w for n ≡ ρ (mod M0). We require w | uρ+v and w | u·M0, so the division is exact on the whole class. The same formula, applied to the class of x mod M0, defines T̂ on Q ∩ Z_S, the rationals whose denominator is coprime to M0, and on Z_S itself. Over one step the multiplier is u/w.

## Lemma C' (the engine, and why it is complete)

`mixedlib.certificate` works with classes n = M t + r (t ≥ 0) and carries T^j(n) = P t + Q exactly. If every value P t + Q uses the same table row, with the division exact uniformly in t, it applies the step. Otherwise it splits t modulo the smallest prime dividing M0/gcd(P, M0). A class is closed at the first j ≥ 1 with P < M, or with P = M and Q < r.

*Completeness.* Suppose some certificate exists, that is, a modulus M' and step counts j(r') ≤ k with T^{j(r')}(n) < n for all large n ≡ r' (mod M'). While an engine node is open, we have P > M, or P = M and Q ≥ r. So T^j(n) ≥ n on that node for all large t, and this holds on every infinite sub-progression too. Every engine class meets some certificate class in an infinite progression (CRT). Hence no node can remain open beyond step k. Each step needs only a bounded amount of extra precision, so the search tree is finite and the engine terminates. Conversely, if the engine terminates, its leaves are a certificate. So:

> **the engine terminates ⇔ a descent certificate exists** (for any modulus).

`verify_certificate` re-checks a run independently:

* the digit paths form a full trie, so the leaf classes partition Z;
* each leaf's affine form is re-derived symbolically, asserting at every step that the branch is uniform on the class;
* T^j(M t + r) = P t + Q is checked numerically at several t, including random 80-bit t.

## Lemma A' (certificate ⇒ GLOBAL and the complete cycle list)

This is exactly round-2 Lemma A. For a leaf with P < M, T^j(n) < n once t > (Q − r)/(M − P). For a leaf with P = M and Q < r, it holds for every t. Let E be the finite set of positive n in the first kind of leaf with t ≤ ⌊(Q − r)/(M − P)⌋. Every positive n outside E has a smaller later iterate. Since T maps positive integers to positive integers, every orbit enters E. Therefore every orbit is eventually periodic, and the cycles are exactly the cycles reached from E (the minimum of a cycle cannot descend, so it lies in E). `mixedlib.prove_global` computes E and simulates it.

## Lemma B' (an expanding S-adic periodic point kills every certificate)

Let x ∈ Z_S be T̂-periodic with period L and multiplier λ > 1. In practice x is rational, with denominator coprime to M0, and `verify_periodic` checks it exactly. By the cycle lemma there is a point y on the orbit with λ_j(y) > 1 for every j ≥ 1. Take any certificate (M', j(·)) and write M' = M'_S·M'' with M'' coprime to M0. Choose a class r' ≡ y (mod M'_S), and put j = j(r'). Every integer n with n ≡ y (mod M0^N) follows the branches of y for j steps once N is large. By CRT, infinitely many such n lie in the class r' mod M'. On them T^j(n) = λ_j(y) n + β with λ_j(y) > 1, so T^j(n) > n for large n. This is a contradiction. ∎

The same argument works for the run-accelerated map S of pairlib.py (pairing_family.md). That map is affine on S-adic cylinders around any point other than x*, and its tail leaves claim S^{j+1}(n) < n for all large n in the leaf.

**Refined Lemma B' (added after refereeing).** Suppose a taming set is a union of classes mod q, and the base cycle above has denominator d. Write q = q₁q₂, where q₂ collects the primes of q dividing d. If no point y of the cycle (in a branch where the class applies) lies in the taming set mod q₁, then integers n ≡ y (mod (M0·q₁)^N), with any residue mod q₂, follow the base cycle uncaught for N steps, since every iterate already misses the taming classes mod q₁. The proof above then applies verbatim. So only the part of q prime to the cycle's denominator has to match. This is used in relatives.md (Theorems D and M).

## Lemma R (an unbounded uncaught run kills every certificate)

Suppose that for every N there are infinitely many n, forming an arithmetic progression of S-adic type, with T^i(n) = x* + λ^i (n − x*) for 1 ≤ i ≤ N, where λ > 1. Then no certificate exists: given (M', j(·)) with j(·) ≤ k, take N > k and intersect with a certificate class by CRT, exactly as in Lemma B'. No periodic point is needed. This is how the "δ ≡ 0" up-runs are used: an up-run whose residue never reaches the division class.

## Lemma D'' (fixed points of words, several primes)

Let f(y) = λ y + μ with λ, μ ∈ Q, and let C = Π_p C_p (p | M0) be a product of balls. Suppose that for each p, either

* |λ|_p > 1 and f(C_p) ⊇ C_p, or
* |λ|_p < 1 and f(C_p) ⊆ C_p.

Then the unique rational fixed point y* = μ/(1 − λ) lies in C.

*Proof.* In Q_p, an affine map with |λ|_p ≠ 1 has the unique fixed point y*. In the first case, f^{-1} maps C_p into C_p and contracts, so its fixed point, which is y*, lies in C_p. In the second case, f itself maps C_p into C_p and contracts. ∎

This is used to produce obstructions from a word: C is the set of S-adic points that follow the word.

## What the engine cannot see (and what replaces it)

* **Unbounded runs with an exact undo** (Farkas pairing). The expanding fixed point x* of the odd branch stays uncaught, so by Lemma B' no plain certificate exists. pairing_family.md handles this with a closed-form block lemma and a run-accelerated engine with "tail leaves".
* **Neutral or irrational obstructions.** If the engine does not terminate and no rational expanding periodic point is found, I report the system as UNRESOLVED BY THIS METHOD. I never report it as "no certificate" without a verified obstruction.
