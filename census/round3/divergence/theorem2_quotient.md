# Theorem 2: the quotient obstruction to automatic certificates

**Status: PROVED** (a short automata argument, Myhill–Nerode style). It is
applied in `race_s21.md` and checked by `check_race_s21.py`.
**Novelty:** the lemma is a standard right-quotient finiteness fact for regular
languages. Its use here, to rule out automatic divergence certificates of every
size for a concrete Collatz-type map in bases 2 and 3 while base 6 works with 2
states, is new to the repo. Literature novelty: not checked.

## Lemma Q

Let C ⊆ Z_{>0} be b-automatic. That is, some DFA reads canonical base-b digits,
most significant first, and accepts exactly the members of C. For a ≥ 0 put

  C / b^a = { x ≥ 1 : b^a x ∈ C }.

Then the sequence a ↦ C/b^a is eventually periodic. In particular it takes only
finitely many distinct values (at most 2^k for a k-state DFA).

*Proof.* The canonical word of b^a x is word(x) 0^a. Let F_a = { q : δ(q, 0^a) ∈ F }.
Then x ∈ C/b^a iff δ(q₀, word(x)) ∈ F_a. Also F_{a+1} = { q : δ(q, 0) ∈ F_a } is a
function of F_a, so (F_a) is eventually periodic, and so is C/b^a. ∎

## Corollary Q (fooling families)

Suppose there are integers x_1, x_2, … ≥ 1 and exponents a_1 < a_2 < … such that

  b^{a_i} x_i ∈ C   and   b^{a_j} x_i ∉ C   for all j > i.

Then the sets C/b^{a_i} are pairwise distinct, so C is not b-automatic. The same
holds with "for all j < i" in place of "for all j > i".

## How it applies to divergence certificates

A divergence certificate C for (T, s) satisfies T(C) ⊆ C, T(s) ∈ C, and C has no
periodic point. So:

* **forced in:** every T^j(s), j ≥ 1, lies in C;
* **forced out:** every n whose orbit is eventually periodic lies outside C,
  because C is forward closed and would otherwise contain a periodic point.

For a separator (injective T, s ∉ C), "forced out" is the backward orbit of s.

So **if the orbit of s contains points b^{a_i} x_i, and the points b^{a_j} x_i
(j > i) reach cycles, then no b-automatic certificate of any size exists.** No
congruence certificate exists either, at any modulus, because periodic sets are
automatic in every base. The SAT lower bounds of round 2 only exclude certificates
up to a fixed size. Corollary Q excludes all sizes at once.

For b = p^j the hypothesis only needs v_p information. Write p^A y with
A = j⌊A/j⌋ + (A mod j) and absorb p^{A mod j} into y. So one family with
unbounded p-adic valuations rules out every base p, p², p³, ….

## What it does not cover

Lemma Q sees only one valuation direction, the trailing zeros. For bases
coprime to the valuations that drive the dynamics (base 5 or 7 for race_s21),
the lemma gives nothing. Those cases are recorded as OPEN in race_s21.md. A
Cobham-type argument might settle them, but I did not attempt it.
