# New uses of sufficiency: sparse sufficient sets, the combination question, permutations

Check: `check_sufficient_sets.py`.

A set S is *sufficient* for T if every merging class meets S. Then GLOBAL ⟺ every member of S is
eventually periodic (merging with an eventually periodic orbit makes an orbit eventually
periodic). For 3x+1, every arithmetic progression is sufficient by K. M. Monks, *The sufficiency
of arithmetic progressions for the 3x+1 Conjecture*, Proc. AMS 134 (2006) 2861–2872 (as cited in
the introduction of arXiv:1204.3904; PAMS article not read here), and Monks–Monks–Monks–Monks
(arXiv:1204.3904) construct sufficient sets of arbitrarily low density for 3x+1. §1 below is the
analogue for the other census maps.

## 1. One progression (PROVED, Theorem A.3)

For every system with "Theorem A = yes" in `applications_basins.md`, any progression meeting all
g-classes is sufficient; when the invariant is trivial, **every** progression is. Requested entries:

| entry | invariant | sufficient progressions |
|---|---|---|
| 5x+1 (CLS-022) | trivial | every progression, e.g. 1 mod 10^d for any single d |
| 7x+1 (CLS-032) | trivial | every progression |
| split5_1 (CLS-048) | trivial | every progression |
| split5_3 (CLS-049) | 3 ∣ n | every progression meeting both 3ℤ and its complement (e.g. 1 mod 10^d) |
| m3_b (CLS-004) | trivial | every progression |
| div23_5n1 (CLS-002) | – | not a p-shift map (two denominator primes 2 and 3): **OPEN** here |
| 1932 permutation (CLS-040) | – | exactly two: ℤ_{≥1} and 1 mod 2 (Proposition P0, §4); no progression with N ≥ 3 |

For div23_5n1 we have only EVIDENCE: every n ≤ 2·10^5 reaches (1 6 3) (consistent with the
census bound 2^46), so the single known basin meets every residue class modulo every N ≤ 81 we
tried. A proof of sufficiency would need a two-prime version of the lift lemma (an orbit need
not divide by 3 infinitely often), which we did not obtain.

## 2. A density-zero sufficient set (Theorem D, PROVED)

**Theorem D.** Let T satisfy Theorem A with a state-free invariant (d* coprime to p) and U ≠ ∅,
and put A_T = 2 log L_U (L_U = ∏_{ℓ∈U} ℓ^{max_r v_ℓ(u_r)}). Let k(n) = ⌊log log n / A_T⌋ (k(n) = 0
for n < 16) and

    S_T = { n ≥ 1 : n ≡ 1 (mod p^{k(n)}) } .

Then S_T has natural density 0 and every merging class meets S_T. Hence GLOBAL ⟺ every n ∈ S_T is
eventually periodic. For U = ∅ the same holds with k(n) = ⌊log n /(2 log p)⌋.

*Proof.* Density: k(n) is nondecreasing and unbounded. For each j, every member of S_T above
exp(exp(A_T j)) is ≡ 1 (mod p^j), so the upper density of S_T is at most p^{-j}; letting j → ∞
gives density 0.

Sufficiency. Fix a merging class H and its enterable point y0. For each k let x_k be the least
integer ≡ 1 (mod p^k) with g(x_k) = g(H); x_k ≤ p^k d* exists because p^k is coprime to d*.
Run the construction of Theorem A with x = x_k, N = p^k. Then Q = δ does not depend on k; the
entry point, h0, J_ℓ, the ball-growing words and the BFS word in 𝒢_δ do not depend on k except
through the target (state of c, c mod δ), which ranges over a finite set, so their total length
is ≤ C_1. The lift uses t ≤ k steps, a ≤ u_max^k, c = T^t(x_k) ≤ (u_max)^k p^k d* + C. The U-adic
precision required at the start is S_ℓ ≤ v_ℓ(a) + C_1 v_max ≤ k·max_r v_ℓ(u_r) + C_2. The
exponent h is the least solution ≥ h0 of congruences modulo lcm(ord_δ(p), ord_{ℓ^{S_ℓ}}(p)),
enlarged by at most C_3 + O(k) periods... more simply: h ≤ h0 + (C_4 + k)·lcm(...) with
lcm(...) ≤ C_5 ∏_ℓ ℓ^{S_ℓ} ≤ C_6 L_U^k. Every move multiplies by at most p, so the resulting
element n_k ∈ H ∩ (1 + p^k ℤ) satisfies

    n_k ≤ C_7 p^{k + C_1 + h} y0 ≤ exp(C_8 (k + 1) L_U^k).

Hence log log n_k ≤ k log L_U + log k + C_9 < A_T k for all k ≥ k_0(H), i.e. k(n_k) ≤ k, so
n_k ≡ 1 (mod p^{k(n_k)}) and n_k ∈ S_T. ∎ (For U = ∅ there is no U-adic precision; h is bounded
and n_k ≤ C p^{k}, giving the faster k(n).)

Applies to 5x+1, 7x+1, 9x+1, 3x+1, 3x−1, split5_1, split5_3 (1 mod 2^k meets both 3-classes),
desc_split7_1, desc_s32_plus9, m3_b, m3_d, m3_e, m3_g, desc_m3_4n5 and the 3x+d, 5x+d rows with
d* coprime to p. Example: for 5x+1, L_U = 5, so
S = {n : n ≡ 1 (mod 2^{⌊log log n / (2 log 5)⌋})} is a density-zero set on which eventual
periodicity is equivalent to GLOBAL(5x+1). Novelty: not checked (Monks et al. do low density for
3x+1; density zero for these maps we have not seen).

Honest caveat: the thinning is extremely slow. For 5x+1, A_T = 2 log 5 and S_T contains every
integer below exp(exp(A_T)) ≈ 10^{10.9}; only above 10^{271} must members be ≡ 1 (mod 4). The
statement is qualitative (density zero), not a practical reduction.

`check_sufficient_sets.py` runs the construction for k = 1..8 and prints log log n_k / k
(EVIDENCE that the constants are moderate; the proof does not depend on it).

## 3. Sufficiency plus descent on a progression: can it settle a system? (negative, PROVED in part)

**Lemma (combination, PROVED).** If every merging class meets P, and every n ∈ P with n > B has a
forward iterate in P that is smaller than n, then every merging class contains an element of
P ∩ [1, B]; so GLOBAL holds as soon as the finitely many members of P ∩ [1, B] are eventually
periodic. *Proof:* the least element of H ∩ P cannot exceed B. ∎

Can this settle a system that descent certificates cannot? We prove two obstructions for p-shift
maps and found no example; the question remains **OPEN** in general.

* **Cylinder certificates do not see good or U-adic conditions.** A finite descent (stopping time)
  certificate is a finite set of words W with a_W < p^{|W|} whose cylinders cover the inputs. If
  p ∤ N, every cylinder (a class mod p^m) meets P = x + Nℤ, and the inequality T^{|W|}(n) < n for
  large n in a cylinder depends only on (a_W, |W|). So a certificate valid on P is valid on ℕ. Thus
  combining sufficiency with a *cylinder* descent certificate on P gains nothing when p ∤ N.
* **Forward-invariant progressions are invariant classes.** If q is good and P = {n : n mod q ∈ A}
  with T(P) ⊆ P, then A is a union of g-classes mod q: the branch of n is independent of n mod q
  (CRT), so every φ_r(z) = (u_r z + v_r)/p maps A into A; φ_r is a bijection of the finite set
  Z/q, so φ_r(A) = A, hence A is invariant under every move and is a union of 𝒢_q-classes. So a
  forward-invariant good-modulus progression with descent settles exactly its own classes, as
  descent would.

What remains possible is descent *within* P (first returns to P decrease) for P with p | N or
with U-adic conditions (such forward-invariant sets exist: for 7x+1 the squares mod 7 are
forward-invariant, census CLS-033). Proving first-return descent is a statement about returns to
a p-adic cylinder, which is not a cylinder property; we found no system where it is provable
while plain descent fails. We report this honestly as not achieved.

## 4. The 1932 permutation (CLS-040): what replaces sufficiency

The map 3q→2q, 3q+1→4q+1, 3q+2→4q+3 is a 3-shift map T(n) = (u_r n + v_r)/3 with
(u, v) = (2, 0), (4, −1), (4, 1); it violates (A1). It is a bijection of the positive integers,
so merging classes are single orbits, and the conclusion of Theorem A fails: the cycle (1) is a
merging class meeting only the progressions that contain 1, although the residue graph is
strongly connected modulo every M (`../../lhf/perm-swap-c/CLS-038.md`), so the finest
finite-modulus invariant is trivial.

*Correction (REFEREE1, verdict WRONG).* The first version said "no sufficient progression can
exist". That is false: the odd numbers are a sufficient progression.

**Proposition P0 (PROVED).** For the 1932 map the sufficient progressions x + Nℤ (x, N ≥ 1) are
exactly ℤ_{≥1} (N = 1) and the odd numbers 1 + 2ℤ. In particular no progression with N ≥ 3 is
sufficient, and GLOBAL(1932) ⟺ every odd n has a periodic orbit.

*Proof.* 1 + 2ℤ is sufficient: T(3q+1) = 4q+1 and T(3q+2) = 4q+3 are odd. If the forward orbit
of n contained no odd number, then no orbit value is ≢ 0 (mod 3) (its image would be odd), so
every value is 3q with q ≥ 1 and the next is 2q < 3q: an infinite strictly decreasing sequence of
positive integers, impossible. So every forward orbit, hence every merging class, meets 1 + 2ℤ.
Conversely, a sufficient progression x + Nℤ must meet the cycles (1) and (2 3) (T(1) = 1,
T(2) = 3, T(3) = 2), so 1 ≡ x and (2 ≡ x or 3 ≡ x) (mod N); hence N | 1 or N | 2, and for N = 2
the progression is 1 + 2ℤ. ∎

The reduction to odd starts is trivial, so for this map sufficiency gives nothing beyond it; what
replaces sufficiency is a complexity statement:

**Proposition P (PROVED).** For a 3-shift map with κ = 1 and positive slopes, such as the 1932
map ((A1) is not needed), the forward orbit of n is eventually periodic iff for some k ≥ 1 it
meets at most k residue classes modulo 3^k. Equivalently, every infinite forward orbit of the 1932
map meets at least k + 1 classes modulo 3^k for every k. (The same holds for any prime p in place
of 3 when κ = 1.)

*Proof.* (⇐ for κ = 1.) Residues mod 3^k of the orbit points ↔ itinerary blocks of length k
(Lemma 1 of Theorem A: the class mod 3^k is determined by and determines the first k branch
symbols). Let c(j) be the number of distinct j-blocks occurring infinitely often in the
itinerary; c is nondecreasing and c(j) ≤ number of j-blocks occurring at all. If c(k) ≤ k then,
either c(1) = 1 (one symbol eventually: eventually periodic) or c(1) ≥ 2, and then strict
increase c(1) < c(2) < … < c(k) would give c(k) ≥ k + 1; so some j < k has c(j + 1) = c(j).
c(j+1) = c(j) means every j-block occurring infinitely often has a unique continuation among
(j+1)-blocks occurring infinitely often; beyond the last occurrence of the finitely many other
(j+1)-blocks the sequence is determined by its current j-block, so it is eventually periodic.
An eventually periodic itinerary with period word W (length L, product a = ∏u coprime to 3)
forces the orbit to be eventually periodic: on the cylinder T^L(n) − c* = (a/3^L)(n − c*) with c*
the rational fixed point; writing m = (3^L − a)(n_0 − c*) ∈ ℤ, integrality of all iterates gives
3^{Lj} | a^j m for all j, so m = 0 and n_0 = c* is periodic. (⇒) a finite orbit meets at most its
length many classes. For the bijective 1932 map eventually periodic = periodic. ∎

So for the 1932 map the replacement statement is a *complexity* statement (at least k + 1 classes
mod 3^k on every infinite orbit); the only sufficiency statement is the trivial one of
Proposition P0; and "every infinite orbit meets
every progression" is equivalent to "every infinite orbit has every finite word in its
itinerary", which we cannot prove. The census residue-graph result (G_M strongly connected for
every M, `../../lhf/perm-swap-c/CLS-038.md`) is the Ẑ-level counterpart: T extends to a
homeomorphism of Ẑ that is topologically transitive (any two clopen sets are connected by some
iterate), but this says nothing about the orbits of integers. Novelty: Proposition P is an
elementary combination of a Morse–Hedlund-type complexity argument with the cylinder lemma;
novelty not checked.
