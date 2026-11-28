# Theorem B: the complete list of automatic orbit-invariant labels

**Status: PROVED** (check: `check_theorem_B.py`).

A *label* is a function f from the positive integers to a finite set with f(T n) = f(n) for all
n (equivalently: constant on merging classes; the shortcut does not matter by Lemma 0 of
`theorem_A_sufficiency.md`). Basin indicators, "eventually periodic", "reaches cycle C" are
labels.

**Theorem B.** Let T be a p-shift map satisfying the hypotheses of Theorem A, whose invariant g
does not depend on the state (g(n) is a function of n mod d*, with gcd(d*, pU) = 1; checked by
`certify.py`), and which has a cycle whose lap uses a branch with u_r > 1. For a label f the
following are equivalent:

1. f is k-automatic for some integer base k ≥ 2;
2. f is constant on every g-class;
3. f is periodic with period d*;
4. f is k-automatic for every k ≥ 2.

In particular, if two cycles C ≠ C' have the same invariant, the basin of C is not k-automatic for
any k (this holds whether or not GLOBAL is known: the basin of a known cycle is a label), and no
orbit-invariant label that is automatic in some base separates the basins of C and C'.

*Separators (corrected after REFEREE1).* A *separator* is a set A ⊇ basin(C) with
A ∩ basin(C') = ∅; it need not be orbit-invariant, and in an open system it may take any value
on starts that reach neither cycle. What is proved about separators:

* **(S1) no ultimately periodic separator exists** (Theorem A alone): if A agreed with a
  periodic set mod q from some point on, pick n ∈ basin(C) beyond that point; the progression
  n + qℤ contains arbitrarily large members of basin(C') (Theorem A, same g-class), all in A.
* **(S2) if the two basins exhaust their g-class** C̄ (i.e. every n with g(n) = g(C) reaches C or
  C'; e.g. GLOBAL is settled and C, C' are the only cycles of that class), **no set automatic in
  any base separates them.** Proof: A ∩ {g = g(C)} = basin(C), since basin(C) ⊆ {g = g(C)} by
  Lemma 4' and the rest of the class lies in basin(C'). The class is periodic mod d*, hence
  automatic in every base, so if A were k-automatic, basin(C) would be k-automatic, contradicting
  the theorem.

For an open system where other orbits might exist, the statement "no automaton separates the
basins" in the literal set sense is **not** proved (the first version claimed it; REFEREE1
verdict GAP); only (S1) and the label statement above are.

(3)⇒(4)⇒(1) are trivial and (2)⇔(3) is the definition of g. The content is (1)⇒(2).

## Lemma B0 (kernel–Cobham with a dilation identity)

Let φ: N → Λ (finite), k0 ≥ 2 not a perfect power, and suppose φ is k0-automatic. Let P ≥ 2 be
multiplicatively independent of k0 and K = k0^e (e ≥ 0) with

    φ(P y) = φ(K y)   for all y ≥ 0.                                   (★)

Let C' be a nonempty union of residue classes modulo q' with gcd(q', P) = 1 such that
P y ∈ C' implies K y ∈ C'. Then some section n ↦ φ(D n + s) (D ≥ 1, 0 ≤ s) whose progression
contains a positive element of C' is ultimately periodic.

*Proof.* The k0-kernel 𝒦 = {n ↦ φ(k0^a n + r) : a ≥ 0, 0 ≤ r < k0^a} is finite. Let S ⊆ 𝒦
be the set of members having a representation whose progression k0^a n + r contains an element
of C'. Give S partial transitions: from ψ ∈ S, digit i ∈ [0, P) leads to n ↦ ψ(Pn + i) if that
sequence lies in S.

*Every base-P word is readable from some state of S.* Let the word have length E and value d
(least significant digit first); d_j = d mod P^j. Pick z_0 ∈ C' and D = k0^a ≥ P^E q'. Let
G = gcd(D, q') (coprime to P). By CRT choose 0 ≤ r < P^E G ≤ D with r ≡ −D d (mod P^E) and
r ≡ z_0 − D d (mod G). Then the progression D P^E n + (D d + r) contains numbers ≡ z_0 modulo
gcd(D P^E, q') = G, hence meets the class z_0 mod q', hence C'. Start at ψ_0(n) = φ(Dn + r)
(its progression contains that one). After j digits the section is
n ↦ φ(D P^j n + D d_j + r) = φ(P^j (D n + s_j)) with s_j = (D d_j + r)/P^j an integer in
[0, D). By (★) iterated (φ(P^j y) = φ(K^j y), induction using commutation of the dilations),
this equals φ(K^j D n + K^j s_j), a member of 𝒦 because K^j D is a power of k0 and
0 ≤ K^j s_j < K^j D. Its progression contains an element of C': the subprogression of
P^j(Dn + s_j) with n ≡ (d − d_j)/P^j (mod P^{E−j}) is D P^E n' + Dd + r, which contains some
P^j z ∈ C'; by the closure property K^j z ∈ C', and K^j z lies in the progression. So every
intermediate section is in S.

*Some state reads every word.* Otherwise every state has an unreadable word. Starting with all
states as candidates, repeatedly take a surviving candidate, look at the state it reaches after
the word built so far, and append a word unreadable from there; that candidate dies and dead
candidates stay dead. After at most |S| rounds no state reads the final word, contradicting the
previous paragraph.

Let ψ* read every word. Its P-kernel {n ↦ ψ*(P^j n + i)} lies in the finite S, so ψ* is
P-automatic; it is k0-automatic (its k0-kernel lies in 𝒦). By Cobham's theorem (stated for sets;
apply it to each level set of the finite-valued sequence) ψ* is ultimately periodic, and ψ* ∈ S.
[Cobham 1969, *On the base-dependence of sets of numbers recognizable by finite automata*,
Math. Systems Theory 3, doi:10.1007/BF01746527, as cited in `../../round2/qr/qrA3_q17.md`.] ∎

## Proof of (1)⇒(2)

Suppose f is k-automatic but takes two values on a g-class C̄ (a set of residues mod d*); write
C = {n ≥ 1 : n mod d* ∈ C̄}. Let k0 be the root of k (k = k0^m, k0 not a perfect power); f is
k0-automatic (automaticity depends only on the multiplicative class of the base).

*Non-periodicity.* There are merging classes H_1, H_2 ⊆ C with f(H_1) ≠ f(H_2). By Theorem A,
every progression containing an element of C contains arbitrarily large elements of both. Hence
for any affine section φ(n) = f(c + μ(Dn + s)) whose progression c + μ s + μ D N meets C, φ is not
ultimately periodic: if it were, with period P_0 from n_0, pick n_1 ≥ n_0 with
c + μ(D n_1 + s) ∈ C; the progression through it with step μ D P_0 meets C, so contains both labels
arbitrarily far out, but φ is constant along it.

*Case k0 ≠ p.* Take φ = f (φ(0) arbitrary), P = p, K = 1, C' = {z ≥ 0 : z mod d* ∈ C̄},
q' = d*. (★) is f(p y) = f(y), true because T(p y) = y (A1); y = 0 is trivial. P y ∈ C' ⇒
y ∈ C' since g(p y) = g(y). gcd(p, d*) = 1. p and k0 are multiplicatively independent because p
is prime and k0 ≠ p is not a perfect power. Lemma B0 yields an ultimately periodic section of f
along a progression meeting C — contradiction.

*Case k0 = p.* Let c be a point of a cycle whose lap (L steps, word W) has numerator product
a = ∏ u > 1, and μ = p^{κ−1}. By Lemma 1 of Theorem A the lap cylinder is c + p^{κ+L−1}Z and
T^L(c + μ p^L j) = c + μ a j for j ≥ 0 (all values ≥ the cycle values, so positive). Hence
φ(y) := f(c + μ y) satisfies φ(a y) = φ(p^L y) for y ≥ 0: (★) with P = a, K = p^L. φ is
p-automatic (an affine section of an automatic sequence). a > 1 is coprime to p, hence not a
power of p, hence multiplicatively independent of k0 = p. C' = {z ≥ 0 : c + μ z ∈ C} is a union of
classes mod d* (μ is a unit mod d*); gcd(a, d*) = 1 because the primes of a lie in U. If
a y ∈ C' then c + μ a y and c + μ p^L y lie on one orbit, so p^L y ∈ C'. C' ≠ ∅. Lemma B0
gives an ultimately periodic section φ(D n + s) = f(c + μ s + μ D n) along a progression meeting
C — contradiction. ∎

## Remarks

* The expanding-cycle hypothesis is needed for bases that are powers of p: qrB7_c53 (all u = 1)
  satisfies Theorem A with invariant 0 / squares / non-squares mod 7, two cycles share the
  non-square class, and both basins are dense in that class; yet the census proves the basin is
  decided by a 20-state binary automaton (`../../round2/qr/qrB7_c53.md`). So density of merging
  classes does not by itself rule out automaticity. Our proof fails exactly there: there is no
  second dilation.
* Theorem B contains Theorem 2 of `../../round2/rewriting/split5_3_components.md` (where
  g(4n) = g(5n) is our lap identity for the cycle through 1 shifted to its lap point) and the
  automaticity part of the q-family Theorem F is the analogous statement for a non-p-shift family.
* For an open system with a single known cycle (7x+1, 3x+1, split7_1, …) Theorem B gives the
  equivalence: the set of n reaching that cycle is automatic in some base ⟺ it is a union of
  g-classes; for one class: ⟺ every orbit reaches that cycle.

## Novelty

The kernel/Cobham argument is the one of `../../round2/qr/qrA3_q17.md` (adapted there from the
finite-kernel characterisation of automatic sequences, Allouche–Shallit). The general form
(★) with an arbitrary dilation pair (P, K) obtained from a cycle lap, and its combination with
the computed invariant of Theorem A for the whole p-shift class: novelty not checked.
