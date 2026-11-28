# Theorem P: free re-entry forces exponentially many non-descending words, so rigidity is not available at the cylinder level (proved in full for block-word normal form)

Round 6, lens `cutoff_wide`. Checks: `check_entropy_code.py` (Theorem P witnesses for 15
systems), `check_mb_s3_27.py` (Proposition B), `count_nondesc.py --check` (exact counts),
`count_nondesc.py --hcheck` (the H table, EVIDENCE).

**Revision after REFEREE1.** Changes in this file, all marked in place:

* Theorem P item 4: restated for steps that divide by more than p. The proof now handles a
  cut that falls after division-free steps.
* **New Lemma Q'**: general (H4) shift pieces give 2^{o(E)} words.
* Corollary P1 is restricted to the block-word normal form, where it now follows from Lemma Q
  (rotation pieces) and Lemma Q' (general shift pieces).
* Proposition B: "inside each 27-class" was false. The bound holds in the 18 classes
  s = 0, 1 (mod 3). The 9 classes s = 2 (mod 3) contain no non-descending point at all. This
  also corrects the referee's proposed wording "each class s != 26".
* **Corrected (it was WRONG):** the H values of core13 and core135. They are 0.4281 and 0.3593,
  not 0.4565 and 0.3755. The old minimization stopped at theta = 3.
* Wording: "escaping family" is replaced by "non-descending family". Nothing here escapes.
  "Smallest in the census" is restricted to the systems computed. 0.03 is replaced by 0.04.
  The novelty caveat now covers Theorem P.

**Revision after REFEREE2.** Wording only, marked in place:

* The headline sentences (introduction, and the paragraphs after Corollary P1) now carry the
  restriction that Corollary P1 actually proves: rigidity in block-word normal form (one
  expanding cycle, distinct-label exits). "Countable is impossible" is fully proved by Theorem P
  and is stated separately.
* Proposition B: the trichotomy does not apply to mb_s3_27 because its branch condition is mod
  27, not because of non-unit multipliers (3, 1, 1/27 are 2-adic units).
* "Smallest entropy" is restricted to the type-(c) (open) systems (acc_h16 in round4/lundberg is
  type (b), dimension 0).
* H is the growth exponent of the word count N(E), an upper bound for dim_H N_inf, not the
  dimension itself.

The aim of part (2) of the lens was to find systems, existing or designed, in which every long
non-descending path is rigid in the sense of Theorem W, and then to settle them. This file proves
that within the unit-multiplier class no type-(c) system has this property even at the level of
cylinder words, for rigidity in block-word normal form (one expanding cycle, distinct-label
exits; Corollary P1). It also proves the same for the blocked mixed-base candidate. The answer
to (2) is therefore **no** for every candidate at the cylinder level in that normal form, and an explicit uncountable
family of non-descending p-adic words is given. (Revision after REFEREE1: this sentence
called it an "escaping family". That was a misnomer: these are non-descending p-adic words,
and no integer orbit is shown to escape.)

Setting and the types (a), (b), (c) are as in round3/accel/trichotomy.md: a unit-multiplier
p-adic table map, its cylinder graph G_K, the Markov property (M), and the standing hypothesis
(every cycle of G_K divides). The **non-descending set** is

    N_inf = { x in Z_p : every prefix slope of the walk of x is >= 1 }.

## Theorem P. PROVED

**Theorem P.** Suppose some SCC of G_K is of type (c), containing an expanding cycle C. Then
there are two closed walks U != V of G_K at a common node r_0, of equal length, with the
following properties.

1. Every word in {U, V}^* has all its prefix slopes > 1, and so does every prefix of such a word.
2. The 2^n walks in {U, V}^n are distinct walks of the same length. They are followed by
   disjoint p-adic balls of radii p^{-K-e(w)}.
3. dim_H N_inf >= s > 0, where p^{-s e_U} + p^{-s e_V} = 1 and e_U, e_V are the division counts
   of U and V. In particular s >= log 2 / (max(e_U, e_V) log p).
4. Let e* = max(e_U, e_V) and let e_max be the largest division exponent of a single edge.
   Every interval of p^{K+E+e_max-1} consecutive integers contains at least
   2^{floor((E-1)/e*)} integers whose walks keep every prefix slope > 1 through at least E
   divisions. When e_max = 1, which holds for every census system used here, the interval
   length is p^{K+E}. (Revision after REFEREE1: the original statement had
   2^{floor(E/e*)} and cut "at the E-th division", which needs e <= 1 per step.)

*Proof.*

*Choosing r_0.* Let C have slope lambda_C > 1. By the cycle lemma there is a rotation of C
whose partial slopes, read from its first node r_0, are all > 1. Take the rotation that starts
right after the last minimum of the cyclic partial sums of log-slopes. Over one period every
later partial sum is strictly above that minimum, and after wrapping the total log lambda_C > 0
is added.

*Choosing W.* Since the SCC is of type (c), it contains an internal edge a -> b that is not an
edge of C (trichotomy.md, proof of Theorem N). Strong connectivity gives a closed walk W at r_0
through a -> b. Put W' = W^{|C|}, so that |W'| is a multiple of |C|. Let m = |W'|/|C|, and set

    U = C^D W',   V = C^{D+m}.

These have equal length. U != V because U uses the edge a -> b at a position where V uses an
edge of C.

*Prefix slopes.* The prefixes of V are C^j times a partial cycle; they have slope >= the minimum
partial slope of C, which is > 1. The prefixes of U are of that form, or
C^D times a prefix of W'. The latter have slope >= lambda_C^D min(1, minimum prefix slope of W'),
which is > 1 for D large. The full slope lambda_C^D lambda_{W'} is > 1 for D large.

A prefix of a word in {U, V}^* is a product of complete blocks, each of slope > 1, times a prefix
of one block, of slope > 1. This proves 1.

*Disjointness and dimension.* Blocks occupy the fixed positions [jL, (j+1)L), so two different
block sequences of the same length differ at some position. They are different walks of the same
length, and by (M) a point follows only one walk of each length. By (M) the set of points
following a walk with e divisions from r_0 is a ball of radius p^{-K-e}. So the points following
infinite words of {U, V}^omega form a Moran set with two pieces of ratios p^{-e_U} and p^{-e_V}
at each level.

Hausdorff dimension at least s follows from the mass distribution principle: give each block
choice the mass p^{-s e}. Every such point is in N_inf by 1. *Item 4 (revised after REFEREE1).* Put n = floor((E-1)/e*). Then n blocks carry at most
n e* <= E - 1 divisions. Extend each of the 2^n words of n blocks by further blocks, and cut
the result at the first step j with E_j >= E. That step comes after the n blocks, and
E <= E_j <= E - 1 + e_max.

Now take two distinct n-block words. Their walks agree up to some first differing edge. A
node whose branch does not divide has exactly one outgoing edge in G_K, since its successor
residue mod p^K is determined. So the first differing edge leaves a dividing node, and it lies
inside the first n blocks, hence before the cut. The cut walks are therefore distinct and
none is a prefix of another. By (M) each is followed by one residue class mod p^{K+E_j}, and
these classes are disjoint. Each class meets every interval of p^{K+E+e_max-1} consecutive
integers at least once, because E_j <= E + e_max - 1. By 1, every prefix slope along each walk
is > 1. ∎

**Converse.** If no SCC is of type (c), then N_inf is countable and dim_H N_inf = 0. PROVED.

*Proof.* A walk eventually stays in one SCC with an internal edge. If that SCC is of type (a), the
potential (★) of Theorem H gives prefix slopes <= const · theta^s -> 0, so the point is not in
N_inf. If it is of type (b), the point follows the cycle from some time t_0 on, so T^{t_0}(x) = x*
by (M). T has finitely many affine branches, so each x* has finitely many T^{t_0}-preimages.
The countable union over t_0 and the finitely many x* is countable. ∎

So **dim_H N_inf > 0 if and only if there is a type-(c) SCC**.

This converse is about the infinite set. At a finite depth E, a type-(b) system can still have
exponentially many non-descending words: a long run along x* can be followed by a long stretch
inside a contracting SCC.

## Lemma Q: rigid word families have polynomial size. PROVED

Fix the normal-form data of Lemma R (theorem_W.md, section 5): C, finitely many exit words
X_lambda, the rate kappa, and bounds J and B. Let R_E be the set of block words with at most E
divisions such that:

* the words split into at most J pieces;
* each piece is a rotation piece of Lemma R, with arbitrary t and c, w and Lambda having at most
  J arcs and |w| <= B, or a geometric piece of period at most B;
* jumps between pieces are arbitrary.

Then |R_E| <= (c E)^{c' J}, with c, c' depending only on (B, J, the number of exit words, C).

*Proof.* A block word is determined by the sequences (k_i) and (lambda_i). There are at most E
blocks, since every exit divides.

* Piece boundaries: at most (E + 1)^J choices.
* Jump k_u at the start of each piece: at most E + 1 values.
* Inside a rotation piece of length n with kappa fixed, (k_i) and (lambda_i) are determined by
  three things:
  1. the position of t among the n + 1 arcs cut out by the points {-kappa i};
  2. the position of each of the at most J arc endpoints of w and Lambda among the at most n + 1
     gaps between the phases phi_i;
  3. the values on the arcs.

  This gives at most (n + 1)^{J+1} (2B + 1)^J |X|^J choices.
* A geometric piece is determined by its period pattern, from a finite set.

Multiply the counts. ∎

## Lemma Q': general shift pieces give 2^{o(E)} words. PROVED (added after REFEREE1)

Lemma Q counts only the Lemma R normal form. Theorem W's (H4) shift pieces are more general.
This lemma counts them, in the same block-word setting.

**Setting.** Fix an expanding closed walk C at a node r_0 with e_C >= 1 (the standing
hypothesis). Fix exit walks X_1, ..., X_r at r_0. Each acts in y = n - x* as
y -> mu_X y + c_X, with c_X != 0 and e_X >= 1, and the labels c_X are **pairwise distinct**.
The slopes of the exits may differ. A block word is

    C^{k_1} X_1' C^{k_2} X_2' ... C^{k_n} X_n' C^{k_{n+1}},    X_i' in {X_1, ..., X_r}.

Its events are the exits, so N = n <= E. Let S_E = S_E(C_0, J, M) be the set of such words
with at most E divisions whose event data (c_i, A(i), E'(i)) satisfy (H4) of theorem_W.md
with constants (C_0, J, M).

**Lemma Q'.** For every delta in (0, 1/4),

    log |S_E| <= delta E log|Sigma| + c(delta) log(E + 2),

where |Sigma| <= r(2C_0 + 1), and c(delta) depends only on (delta, C_0, J, M(delta), r). In
particular |S_E| = 2^{o(E)}.

*Proof.* **The word is determined by its event data and k_{n+1}.** We have E'(1) = e_C k_1,
and for i >= 2

    E'(i) - E'(i-1) = e_{X_{i-1}'} + e_C k_i.

X_i' is read off from c_i, because the labels are distinct. Then k_i is recovered inductively
from the increments of E', using e_C >= 1. The final run k_{n+1} has at most E + 1 values.

**Symbols.** For i < n put sigma_i = (c_i, E'(i+1) - E'(i)). Together with E'(1) and
k_{n+1}, the sequence (sigma_i) determines the word. Inside a piece, bounded geometry (H4)
gives 0 <= E'(i+1) - E'(i) <= 2C_0, so sigma_i lies in an alphabet Sigma with
|Sigma| <= r(2C_0 + 1). The symbol that straddles a boundary between two pieces is free: it
encodes the jump, and it has at most r(E + 1) values.

**Count per piece.** Let I be a piece.

* A shift piece with |I| < 2/delta has at most |Sigma|^{2/delta} symbol strings.
* A shift piece with |I| >= 2/delta: apply (H4) with I' = I. This gives q <= delta|I| and a
  set X of at most M(delta) exceptional indices. Take i with i, i+1 not in X and with
  i+1+q in I. Then c_{i+q} = c_i, and

      E'(i+1+q) - E'(i+q) = (E'(i+1) + k_E) - (E'(i) + k_E) = E'(i+1) - E'(i),

  so sigma_{i+q} = sigma_i. The string on I is therefore determined by four things: q (at most
  |I| values), the first q symbols (at most |Sigma|^{delta|I|}), the set
  D = {i : sigma_{i+q} != sigma_i}, of size at most 2M(delta) (at most (|I| + 1)^{2M(delta)}
  choices), and the symbols sigma_{i+q} for i in D (at most |Sigma|^{2M(delta)}).
* A geometric piece of period pi <= C_0 has a constant vector
  (A(i+pi) - A(i), E'(i+pi) - E'(i)). So sigma is pi-periodic on it, with at most
  C_0 |Sigma|^{C_0} choices.

**Total.** Choose the piece boundaries (at most (E + 1)^J ways), the piece kinds (2^J), the J
boundary symbols, E'(1), k_{n+1}, and the strings on the pieces. Since sum |I| <= n <= E, the
product is at most

    |Sigma|^{delta E} · (E + 2)^{c(delta)}.

This proves the bound. Since delta is arbitrary, log|S_E| = o(E). ∎

Rotation pieces are shift pieces by Lemma R, so Lemma Q' contains Lemma Q up to the
polynomial-versus-subexponential bound.

*Caveat.* The distinct-label hypothesis matters. Suppose two different exit walks have the
same affine action in y. Theorem W treats them identically, and a family that chooses freely
between them has exponentially many words but rigid data. No census system has such a pair
among the exits used here: in each, the exits have distinct labels (`check_entropy_code.py`
and `check_cutoff_instances.py` use one exit word per system, and K7's two exits have labels 1
and 2). Such coincidences were not searched for in general.

**Corollary P1 (cylinder-level rigidity is impossible). PROVED.** (Restricted after REFEREE1.)
Take any unit-multiplier system with a type-(c) SCC, an expanding cycle C in it, and finitely
many exits with distinct labels as in Lemma Q'. The number of block words with at most
E + e_max divisions whose event data satisfy (H4) for fixed (C_0, J, M) is 2^{o(E)}, by
Lemma Q'. For Lemma R families it is (cE)^{c'J}, by Lemma Q. Theorem P item 4 gives at least
2^{floor((E-1)/e*)} distinct non-descending cylinder walks reaching E divisions. So the
fraction of those walks that are rigid in this sense is at most 2^{-E/e* + o(E)}, which tends
to 0 exponentially.

The original statement claimed this for "rigid in the sense of Theorem W" in general, but
counted only Lemma R families. It is now proved for the block-word normal form, with general
(H4) shift pieces and geometric pieces. Paths of Theorem W that do not have this normal form,
for example paths built over several expanding cycles or over exits with coinciding labels,
are not counted.

Hence no statement of the form "every non-descending word of length beyond L(y) is rigid in
block-word normal form (one expanding cycle, distinct-label exits)" holds for the p-adic walks.
(Restriction added after REFEREE2; rigidity in other decompositions is not covered.) A rigidity reduction would have to use the integer start itself beyond its
digit horizon, which is exactly the count-law problem (round4/lead/CONJECTURE.md).

If instead there is no type-(c) SCC, Theorem H already settles the system. This needs the
hypotheses of Theorem H: unit multipliers, the standing hypothesis (every cycle of G_K
divides), and that positive integers map to positive integers. So **within the unit-multiplier
class the cutoff theorem cannot be completed into a decision by a cylinder-level rigidity
reduction in block-word normal form.** Arguments that use the integer start beyond its digit
horizon are not excluded. Designing a type-(c) table whose non-descending set is countable, as
proposed in part (2c), is impossible (Theorem P: the dimension is positive). Designing one whose
non-descending set is rigid in block-word normal form (one expanding cycle, distinct-label exits)
is impossible by Corollary P1; rigidity in other decompositions is not excluded. (Restriction
added after REFEREE2.)

Each of these statements was checked for consistency with what is already known:

* trichotomy Theorem N: type (c) means infinitely many expanding periodic orbits, and Theorem P
  gives uncountably many non-descending points;
* lundberg Theorem 1: type (c) gives theta_1 < theta_run;
* the dimensions computed in rounds 3 and 4.

## Proposition B: the blocked mixed-base system. PROVED (exact finite check plus the argument below)

mb_s3_27: n = 26 (mod 27) -> (n+1)/27; else even n -> n/2; else (3n+1)/2. The trichotomy does
not apply because the branch condition is mod 27, not 2-adic. (Revised after REFEREE2: this said
"its multipliers are not all units", which is wrong; the 2-adic multipliers 3, 1 and 1/27 are all
2-adic units.)

*Skew-product lemma.* On n != 26 (mod 27), T(n) mod 27 = f(n mod 27, n mod 2), with f(s, 0) = s/2
and f(s, 1) = (3s+1)/2 in Z/27. Checked on all residues. Hence a Terras parity word b of length L
and an initial residue s are followed by **every** integer of one class mod 2^L · 27, provided the
f-path from s avoids 26. The 2-adic part is the Terras bijection, and CRT supplies the 27-part.

*Code.*

* C = 110 is the parity word of the cycle -5, -7, -10. Its f-states are 22, 20, 17, and its slope
  is 9/8.
* W = 010 is a word from state 22 back to state 22 that avoids 26 and is not a power of C.
* W' = W^3, D = 25, U = C^25 W', V = C^28, all of length 84 Terras steps.

Every prefix slope of U and V exceeds 1, and both return the fiber state to 22. Thus every word of
{U, V}^* is realized by a nonempty class mod 2^{84n} · 27, never meets the blocked class, and has
all prefix slopes > 1. The never-blocked part of the non-descending set therefore has 2-adic
dimension at least 1/84 inside each class s (mod 27) with s = 0 or 1 (mod 3), that is, in 18 of
the 27 classes. For each such s, `check_mb_s3_27.py` finds a parity word P of length at most 6
from s to state 22. P avoids 26 and has all prefix slopes > 1. Then P{U, V}^omega is realized
inside class s, and P only rescales.

**The other 9 classes, s = 2 (mod 3), contain no non-descending point, 26 included.**
(Revision after REFEREE1: the original said "inside each 27-class", and the referee proposed
"each class s != 26". Both are false.) An odd step maps a state s = 2 (mod 3) to another
state = 2 (mod 3), and from such a state at most two odd steps reach 26. An even step
multiplies the slope by 1/2, and a blocked step by 1/27. So some prefix slope is < 1 within 3
steps. This is checked exhaustively over (s, 3 parity bits) and on all integers |n| < 30000.
It is consistent with the cycle -5, -7, -10: -7 = 20 (mod 27), and the prefix slope from -7 is
3/4 after two steps. Exact counts of never-blocked non-descending words
of length j grow like 2^{0.32 j} (EVIDENCE, from exact integers at j = 120, 240).

So the only known obstruction of mb_s3_27, the cycle -5, -7, -10, comes with free re-entry, and
its non-descending set is not rigid. The cutoff applies only to the zero-entropy rigid
sub-families (Theorem W instance with W0 = 010, slope 3/8, kappa = 8.3274; exact identity check).

## Quantification for each candidate

The table gives the exponent of the number of non-descending words per division: exact integer
counts N(E) up to E = 300, the fitted exponent H_fit, and the variational value H. The floats are
EVIDENCE. The exact counts are verified against direct residue enumeration for small E by
`count_nondesc.py --check`.

* crit = 1/(1 - H) is the critical depth of the count law, in units of log_p y.
* Theorem P gives the rigorous lower bound s.
* Every rigid family has exponent 0 and Theorem W coefficient 1.

| system | H (exponent of the non-descending word count N(E) ~ p^{HE}; an upper bound for dim_H) | crit 1/(1-H) | Theorem P bound s | closest proved partial result |
|---|---|---|---|---|
| core S={1,3,5} mod 8 | 0.3593 (corrected; was 0.3755) | 1.56 | 0.0106 | Theorem W for rigid paths around -5 |
| core S={1,3} mod 8 | 0.4281 (corrected; was 0.4565) | 1.75 | 0.0200 | same |
| mb_s3_27 (never-blocked part) | >= 0.32 (fit, lower bound for full set) | - | 0.0119 | same, around -5 |
| split5_3 | 0.5807 | 2.38 | 0.0445 | repo: Theorem W, linked labels (coefficients 3/2, 2), free-label power bound |
| core {5,7} | 0.7193 | 3.56 | 0.0953 | Theorem W |
| K7 | 0.7491 | 3.99 | 0.0953 | Theorem W |
| cores {1,5,7}, {3,5,7}, {1,7} | 0.774, 0.788, 0.790 | 4.4-4.8 | 0.095-0.100 | Theorem W |
| split5_1 | 0.9369 | 15.8 | 0.1335 | Theorem W |
| 3x+1, 3x-1, 3x+5 | 0.9500 | 20.0 | 0.3333 | Theorem W |
| m3_b | 0.9648 | 28.4 | 0.3155 | Theorem W |
| 5x+1, core W | 1 (positive drift) | infinite | 0.5, 0.1667 | Theorem W (no convergence claim) |

**Corrected after REFEREE1.** The minimization in `count_nondesc.H_variational` ran over
theta in [0, 3] only. For core13 and core135 the minimizer lies at theta about 4.65 and 4.00,
so the old values 0.4565 and 0.3755 were s(3), not the minimum. The grid is now [0, 12], and
the run aborts if the minimizer sits at the grid end. The minimizers of all other systems are
below theta = 2.3. `count_nondesc.py --hcheck` checks each stated value against the minimum,
and checks the exact-count fit over E = 300..600. For example, the fit gives 0.4252 for core13
and 0.3564 for core135, slightly below H, as expected.

Among the type-(c) (open) unit-multiplier systems computed here and in the round4/lundberg
table, the cores S = {1,3} and {1,3,5} mod 8 have the smallest entropy. (Revised after REFEREE2:
the lundberg table also contains acc_h16, type (b), whose non-descending set has dimension 0.) This was not checked against the whole
census. The never-blocked part of mb_s3_27 has a lower fitted exponent, 0.32, but it is only a
lower bound for that system's full non-descending set. These cores also have the smallest gap
theta_run - theta_1 in round4/lundberg. Their non-descending words are the closest to rigid
among the systems computed, but their entropy is still 0.36 to 0.43 base-2 digits per
division. The explicit non-descending family {U, V}^* has 2^n members at 2-adic depth about 50n
(core13) or 94n (core135), and the actual non-descending family is much larger. (Revision
after REFEREE1: this paragraph said "escaping family". Nothing in it escapes.)

**The theorem that comes closest.** Theorem W covers bounded-complexity families only. Among the
split5_3 linked-label theorems (not ported here), the three-shift theorem covers 3^p words at
depth 6p blocks, an exponent of at most log2(3)/(6 T) per division. With the repo's
T = 2 kappa + 1 = 7.2126 this is 0.0366, so below 0.04. That is far below every H in the table. No proved cutoff covers a positive proportion of the entropy of any candidate.

## Novelty (added after REFEREE1)

Novelty was not checked for anything in this file. Theorem P and its converse are elementary:
Moran sets and the cycle lemma. For 3x+1, positive dimension of the 2-adic set with infinite
stopping time is presumably classical (Terras and Lagarias). Lemma Q and Lemma Q' are routine
counting.
