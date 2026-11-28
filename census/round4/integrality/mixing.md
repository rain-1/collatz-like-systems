# Why fixing digits, other moduli and transducers do not get past the wall

Lens "integrality", round 4. Check: `check_mixing.py` (exits 0, under a second).

This file answers task (4) of the lens. The lens proposed three ways to beat
Theorem N (round3/accel/trichotomy.md): choose multipliers whose powers have
predictable low digits (u = 1 mod a high power of p), add information a p-adic
cylinder cannot see (congruences to other moduli), or treat the excursion map
as a finite-state transducer so that GLOBAL becomes an automata question. The
three theorems below show that none of these works, for every unit-multiplier
system with an expanding cycle in a type-(c) component. Each says exactly where
the idea fails. (HEURISTIC, revised after REFEREE1: the three theorems exclude
three specific proof shapes, namely arguments using only cylinder/Haar
information, cover/stopping-time certificates over Ẑ, and finite transducers
for the run map. They do not show that Archimedean size is the only remaining
information; global arguments that combine residues with size, or invariants
that are not cylinder covers, are not excluded. Size is the next thing this
lens tried, and `cycles.md` shows what it gives.)

Setting and notation are those of trichotomy.md: a unit-multiplier p-adic table
T(n) = (u_r n + v_r)/p^{e_r} on classes r mod p^m, the level-K cylinder graph
G_K (K >= m), and the Markov property (M): T maps every level-K cylinder
affinely and bijectively onto the union of its edge targets. For a closed walk
C of G_K through a node r0, write ℓ for its length, E for its number of
divisions (the sum of the e_r), U for the product of its u_r, and
λ_C = U/p^E for its multiplier. x* is its periodic point, a rational number in
Z_p. A point n of the cylinder [r0]_K "follows d laps" if its first dℓ *steps*
follow the walk C^d, i.e. its residues mod p^K at times 0, 1, …, dℓ are those
of C^d including the final return to r0 (corrected after REFEREE1: the earlier
wording "first dℓ residues" dropped the last edge; for G3, n = 8 has residue 8
at time 0 but G3(8) = 11 ≢ 8 mod 9, so it follows 0 laps). Its *lap count* d(n) is the largest such d (finite
unless n = x*). The *run map* is R(n) = T^{d(n)ℓ}(n).

## Theorem M (full-branch structure; low digits of u^k are irrelevant). PROVED

Let C be any closed walk with E >= 1 through r0.

1. For each d >= 0, the set D_d = {x in [r0]_K : d(x) = d} is
   {x : x = x* (mod p^{K+dE}), x ≠ x* (mod p^{K+(d+1)E})}. R restricted to D_d
   is the affine map x ↦ x* + λ_C^d (x − x*). It maps D_d bijectively onto
   D_0 = [r0]_K ∖ (x* + p^{K+E} Z_p) and multiplies Haar measure by p^{dE}.
   In particular, **for Haar-random x in D_d the post-run point R(x) is
   Haar-uniform on D_0, and this distribution does not depend on d or on any
   congruence property of U.**
2. Every closed walk π of G_K from r0 to r0 has a cylinder [π] that T^{|π|}
   maps affinely onto [r0]_K, multiplying Haar measure by p^{E(π)}. Hence the
   first-return map to [r0]_K is a *full-branch* map. Under normalized Haar
   measure on [r0]_K, the sequence of first-return words is i.i.d., with
   P(π) = p^{−E(π)}, conditioned on returning. So the sequence of lap counts
   d_1, d_2, … of successive runs is i.i.d.
3. (Positive integers.) For every finite sequence of closed walks π_1, …, π_k
   through r0, the positive integers whose orbit performs them in order form
   exactly one residue class mod p^{K + Σ E(π_i)} (Lemma 1 of
   round3/dichotomy/dichotomy.md). So the proportion of n <= X *in [r0]_K* doing this
   tends to Π p^{−E(π_i)}: on positive integers, every finite window of the excursion
   process has the i.i.d. law of part 2.

*Proof.* (1) If x follows one lap, T^ℓ is affine on the lap cylinder and fixes
x*, so T^ℓ(x) = x* + λ_C (x − x*). Iterating gives R. The cylinder of C^d is
x* + p^{K+dE} Z_p (by (M) it is a coset of p^{K+dE} Z_p, and it contains x*).
That gives the description of D_d. Since |λ_C^d|_p = p^{dE}, the map
x ↦ x* + λ_C^d(x − x*) sends x* + p^{K+dE} Z_p onto x* + p^K Z_p = [r0]_K and
x* + p^{K+(d+1)E} Z_p onto x* + p^{K+E} Z_p. So it sends the difference D_d onto
D_0 bijectively, and an affine map scales Haar measure by |λ_C^d|_p.

(2) This is (M) applied along π, step by step. Each step maps a cylinder onto
the union of its targets, and the cylinder of π is the set of points whose
images land in the prescribed targets. Full branches give independence: the
image of [π_1] under T^{|π_1|} is all of [r0]_K, with Haar measure scaled by a
constant, so the conditional law of the future given π_1 is the unconditional
one.

(3) Lemma 1 of dichotomy.md, applied to the concatenated walk. ∎

**What this says about the lens's idea.** Take u ≡ 1 (mod p^s), for example
p = 3 with u = 4 or 10, or p = 2 with u = 5. Then u^k m ≡ m (mod p^s), so the
low digits of the post-run value are predictable *given m*. But m is the free
part of n. Part 1 shows that the post-run value is uniform on its cylinder
whatever s is. Part 3 shows that every finite continuation is realized by a
progression of positive integers. The digits that decide the next excursion
are never controlled. This holds for every unit system, so there is no
counterexample family. What does break full branching is a non-unit
multiplier, which is exactly the mixed-base escape of round 3 (mixedbase,
dressing.md).

The "full copy of 3x+1-type digit mixing" is therefore this: the excursion
process of any type-(c) unit system is a full-branch Bernoulli process with
infinitely many branches C^d W (d >= 0). Their multipliers λ_C^d λ_W are
unbounded, and every finite word is realized by positive integers on one
residue class. 3x+1 at the point −1 has the same structure.

Checked exactly (`check_mixing.py`, [M-run], [M-walk], [M-iid]) for three
type-(c) systems with u = 3 (sf3_7 = K7), u = 4 ≡ 1 (mod 3) (G3 below) and
u = 5 ≡ 1 (mod 4) (F5 below). The runs were checked for d = 0..8, and 300 random
closed walks per system. The joint counts of (d_1, d_2) factor exactly, for
example 810, 270, 90 / 270, 90, 30 / 90, 30, 10 for G3.

* G3 (p = 3): n ≡ 8 (mod 9) → (4n+1)/3, otherwise n → ⌈n/3⌉.
* F5 (p = 2): even n → n/2, n ≡ 1 (mod 4) → n+1, n ≡ 3 (mod 4) → (5n−1)/2.
  The expanding fixed point is x* = 1/3, with multiplier 5/2.

## Theorem N̂ (other moduli do not help). PROVED

Let T be a unit-multiplier p-adic table (the branch depends only on n mod p^m).
Suppose some SCC of G_K is of type (c). Then there is no **profinite
generalized certificate**: a countable cover of Ẑ ∖ E by cylinders of Ẑ
(residue classes modulo arbitrary integers M), with step counts j_i, such that
T^{j_i}(n) < n for all but finitely many positive integers n in each cylinder,
where E is a finite union of periodic orbits of T̂ on Ẑ.

*Proof.* T extends continuously to Ẑ = Z_p × Π_{q≠p} Z_q. The branch is read
from the Z_p coordinate, and the division by p^e is invertible in each Z_q.
Theorem N's proof gives an expanding periodic point y in Z_p ∩ Q, outside a
neighbourhood of the p-components of E, with all partial multipliers > 1 along
its orbit. Note that y need not lie in Ẑ, since its denominator may contain
primes q ≠ p. Choose z in Ẑ with p-component y and arbitrary q-components, not
in E. Some cylinder D_i ∋ z, a class modulo M = p^a M' with p ∤ M', has step
count j_i. For N >= a, every positive integer n ≡ z (mod p^N M') lies in D_i.
These n are ≡ y (mod p^N), so for N large they follow y's orbit for more than
j_i steps, and T^{j_i}(n) = λ n + β with λ > 1. Infinitely many of them are
large, so T^{j_i}(n) > n for infinitely many n in D_i, a contradiction. ∎

So congruence information modulo primes other than p cannot get past the wall
*as part of a cover/stopping-time certificate*, as long as the branch is read
p-adically. (Scope stated after REFEREE1: a global argument that uses a mod-q
invariant in some other way is not excluded by this theorem.) The theorem also
covers certificates restricted to one residue class modulo M' coprime to p. Note that the split_d
invariants of round 3 (n mod d preserved) are of exactly this kind. Checked in
[Nhat]: for the expanding witnesses y_d of each example, integers n ≡ y_d
(mod p^N) with *arbitrary* residues mod 3^4·5^3·7^2 (p = 2) or 2^6·5^3·7^2
(p = 3) rise for three full laps.

## Theorem R (the run map is never automatic). PROVED (uses Cobham's theorem)

Let C be an expanding closed walk (U > p^E, E >= 1) of a unit-multiplier table.
Then the graph of the run map R, restricted to positive integers, is **not** a
p-automatic relation. More strongly, it is not a rational relation on base-p
digit strings (one that a finite two-tape automaton accepts, synchronously or
not).

*Proof.* Write x* = −a/b with b >= 1 and gcd(b, p) = 1. Let F be the order of
p^E modulo b. Pick an integer c' >= 1 with p ∤ c', c' ≡ a (mod b) when p^K ≡ 1
(mod b) holds, and in general with p^K c' ≡ a (mod b), so that
n_d = (p^{K + dFE} c' − a)/b is an integer for every d >= 0 (p^{FE} ≡ 1 mod b).
Then b n_d + a = p^{K+dFE} c' with p ∤ c', so n_d ≡ x* (mod p^{K+dFE}) and
n_d ≢ x* (mod p^{K+dFE+1}). Hence d(n_d) = dF, and by Theorem M(1),

    b R(n_d) + a = U^{dF} p^K c'.

The set X = {n_d : d >= 0} is p-automatic. It is first-order definable in
⟨N, +, V_p⟩ from the automatic set {p^{K+dFE} c'}, because n ↦ bn + a is
definable. Suppose the graph of R were rational. Then R(X) would be a regular
set of base-p representations, since rational transductions preserve
regularity. By definability again, Y = {U^{dF} : d >= 0} = {y : p^K c' y ∈ bR(X)+a}
would be p-automatic. Y is also U^F-automatic. Here p and U^F are
multiplicatively independent (p ∤ U and U >= 2), so by Cobham's theorem (1969)
Y is ultimately periodic. But Y is infinite and the gaps between its
consecutive elements tend to infinity, a contradiction. ∎

**Consequence** (scope corrected after REFEREE1). The lens hoped that GLOBAL
might become a decidable automata question for systems whose excursion map is a
finite-state transducer. By Theorem R, no unit system with an expanding cycle
has a rational *run map*, nor any rational excursion map that contains the full
run along C (whether the cycle is in a type-(b) or a type-(c) component). This
does NOT cover first-return maps in general: the 3x+1 Syracuse map (first
return to the odd class) is a rational relation in base 2. The earlier sentence
"no unit system with an expanding cycle has such an excursion map" was too
broad and is withdrawn in that form. T itself is always
automatic (it is affine on classes), but its iterate is not uniformly so, and
GLOBAL quantifies over unbounded iteration. The obstacle is the unbounded power
U^d: powers of a unit are not p-automatic.

## Testing against 3x+1

All three theorems apply to 3x+1 (p = 2, C = the fixed point −1 of
(3n+1)/2). They prove only impossibility statements, so they cannot prove
anything false about 3x+1, 5x+1 or systems with extra cycles. Theorem M(2) is
the classical fact that 3x+1 parity vectors are i.i.d. under 2-adic Haar
measure (Terras, Lagarias), restated for the first-return process of an
arbitrary unit system.

## Novelty

Not checked. Theorem M(2)–(3) is a direct consequence of the Markov property
and is standard in spirit (Terras 1976, Lagarias 1985). Theorem N̂ is a small
extension of round 3's Theorem N. Theorem R is a direct application of Cobham's
theorem. None of the three is deep; their use is to close off the three routes
the lens proposed, with exact reasons.
