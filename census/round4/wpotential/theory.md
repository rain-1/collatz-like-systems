# Weighted potentials and the homoclinic wall

Lens "wpotential", round 4. Checks: `check_wall.py` (Theorem W data, about 45 s),
`check_windows.py` (Theorem A data, about 5 s), `check_srs.py` (rewriting encodings, about
1 s). Revised after REFEREE1.md; every change is marked in place with "after REFEREE1".
Labels: PROVED, EVIDENCE, OPEN. Novelty: not checked (no literature search was done).

## 0. Summary

The goal was a proof method that gets past Theorem N of round 3. The idea of the lens was to
replace "a weight c(r) of the residue times n" by a potential V(n) that may read all the digits
of n. The outcome is a negative one, made precise:

* **Theorem W (PROVED).** A potential that is *coarsely monotone* at a point x of the p-adic
  (or profinite) integers cannot decrease along T near x if x is an expanding periodic point.
  "Coarsely monotone at x" means: on some small cylinder around x, a number that is much larger
  in the real sense never has a smaller potential. So a successful potential must break real
  monotonicity, at arbitrarily small scales, at *every* expanding periodic point. For a type-(c)
  system these points are dense in an uncountable Cantor set (Corollary W1).
* Consequence (Corollary W2, PROVED): for unit-multiplier systems, a certificate in the classes
  *without counters* (residue weight times n, plus any o(n) correction; n^γ times a locally
  bounded factor e^ψ; mantissa factors; c·(digit count) + bounded; lexicographic and ordinal
  combinations of these) exists **only for CERT systems**. With counters v_p(n − x_i) at
  finitely many points added, the reach is at most the systems whose expanding periodic points
  lie on finitely many orbits. This includes type (b) (for example acc_h16, see the Remark after
  Corollary W2), but never type (c).
  *[Corrected after REFEREE1. The first version said that these classes, counters included,
  "exist only for CERT systems" and "do not even reach type (b)". That was WRONG; the referee's
  counterexample is acc_h16.]*
* **Theorem A (PROVED for window width s ≤ 10 with a ×3 branch, s ≤ 8 with a ×5 branch).** A
  potential that sums a weight over all length-s windows of the binary digits of n (any
  weights, plus bounded boundary terms) is forced by the descent condition to have the form
  c·(number of digits) + (bounded), which is coarsely monotone. So digit-window weights cannot
  certify any 2-adic system with a ×3 or ×5 branch and an expanding periodic point: all 8 cores,
  3x+1, 5x+1, and also the type-(b) systems that Theorem H settles.
* The mixedbase blocked system mb_s3_27 (not unit-multiplier) has, besides the ghost cycle
  −5 → −7 → −10, expanding rational periodic points that follow that cycle for 10, 20 and 40
  periods (exact). Theorem W covers it: a potential must break monotonicity at all of them.
* Matrix interpretations of a mixed binary/ternary rewriting encoding (Yolcu-Aaronson-Heule
  style) are *not* covered by Theorems W or A. A z3 search found none for K7 or the other
  cores in the sizes tried (EVIDENCE only, see `srs.md`).

No type-(c) system was settled. Section 6 states what a potential would have to do.

## 1. Certificate class and soundness

Let T map Z_{>0} to itself (or Z_{≥0} to itself, as K7 does).

**Definition (potential certificate).** A triple (V, δ, F): V : Z_{>0} → R_{≥0}, a real
δ > 0 and a finite set F, such that V(T n) ≤ V(n) − δ for every n ∉ F. More generally V may
take values in any well-ordered set (ordinals, lexicographic tuples of naturals) with
V(T n) < V(n) for n ∉ F.

**Lemma S (soundness). PROVED.** If (V, δ, F) is a potential certificate, every orbit of T is
eventually periodic, and every cycle meets F. So the cycle list is the finite list of cycles
reached from F.

*Proof.* Take any n. If the orbit avoided F from time t on, V would decrease by at least δ at
each later step while staying ≥ 0, which is impossible. So the orbit meets F at some time t₁;
apply the same argument to T^{t₁+1}(n), and so on. The orbit meets the finite set F infinitely
often, so some element of F repeats, and from then on the orbit is periodic. A cycle that
missed F would be an orbit avoiding F forever. The well-ordered case is identical, because a
strictly decreasing sequence in a well-order is finite. ∎

The definition is too wide to be useful by itself: if GLOBAL holds, V(n) = (number of steps
until the orbit of n enters its cycle) is a certificate with F = the cycles. A certificate
class is a restriction on V that makes it checkable. Round 3's potentials V(n) = c(n mod Q)·n
are the simplest class. This lens asks which larger classes could reach type (c).

## 2. Theorem W: coarse monotonicity is the wall

Setting: a residue-class affine map. A modulus Q; for each residue r mod Q, integers
(u_r, v_r, w_r) with u_r, w_r ≥ 1 and T(n) = (u_r n + v_r)/w_r on n ≡ r. No unit hypothesis.
Let Ẑ_Q = lim Z/Q^k (for Q = p^m this is Z_p; for Q = 54 it is Z_2 × Z_3). A **cylinder** is a
set a + Q^N Ẑ_Q. Let T̂ be the extension of T to those points of Ẑ_Q where it is defined.

An **expanding periodic point** is a rational y in Ẑ_Q (denominator prime to Q) with
T̂^L(y) = y, whose composed branch along one period is x ↦ λx + β with λ > 1 (real). Because
T̂^L(y) = y, the identity T^L(n) − y = λ(n − y) holds for every integer n that follows the
same branches as y for L steps.

**Definition (coarse monotonicity).** V is *coarsely monotone (CM) at x ∈ Ẑ_Q* if there are
N, R and ρ ≥ 1 such that V(n') ≥ V(n) whenever n, n' are positive integers in the cylinder
x + Q^N Ẑ_Q with n ≥ R and n' ≥ ρn. Let B(V) be the set of points where V is not CM.

**Theorem W. PROVED.** Let T be a residue-class affine map, (V, δ, F) a potential
certificate for T (or V with values in a strict order and V(Tn) < V(n) off F). Then every
expanding periodic point y of T̂ lies in B(V).

*Proof.* Let y have period L and multiplier λ > 1. Suppose V is CM at y with constants N, R, ρ.
Choose k with λ^k > 2ρ. Let n run through the integers in a cylinder y + Q^M Ẑ_Q, where M is
large enough that every such n follows the branches of y for kL steps and that
T^{kL}(n) ≡ y (mod Q^N). Such an M exists: each step multiplies the difference n − y by
u_r/w_r, so after kL steps the difference has lost at most the factor ∏ w_r of divisibility,
and the branch at each step depends only on the class mod Q. Then for every such n:

* T^{kL}(n) = y + λ^k (n − y). This is ≥ ρn as soon as n is large, because λ^k > 2ρ.
* For 0 ≤ i < kL, T^i(n) = T̂^i(y) + λ_i (n − y) with λ_i > 0 the partial products, so
  T^i(n) → ∞ as n → ∞. For n large no T^i(n) lies in F.
* Both n and n' = T^{kL}(n) lie in y + Q^N Ẑ_Q.

So for one large n we have V(n') ≥ V(n) by CM, and V(n') < V(n) by applying the descent
condition kL times. Contradiction. ∎

Nothing in the proof uses units, the Markov property, or the residue graph. It uses only that
integers can shadow y for as long as we like while growing by a factor λ^k.

**Corollary W1 (type (c): the failure set is dense in a Cantor set). PROVED.** Let T be a
unit-multiplier p-adic table map with the standing hypothesis of trichotomy.md (every cycle of
G_K has a division), and let Σ be a type-(c) SCC of G_K. Let
Λ_Σ = {x ∈ Z_p : T̂^t(x) mod p^K ∈ Σ for all t ≥ 0}. Then

1. Λ_Σ is closed, perfect and uncountable;
2. the expanding periodic points in Λ_Σ are dense in Λ_Σ;
3. hence for every potential certificate V, B(V) ∩ Λ_Σ is dense in Λ_Σ.

*Proof.* (1) Closed: Λ_Σ is an intersection of closed (clopen) conditions. Infinite walks in
Σ starting at a node correspond to points: by the Markov property (M) every finite walk is
followed by a non-empty cylinder, and along an infinite walk the divisions are infinitely many
(standing hypothesis), so the nested cylinders shrink to one point. Two different walks from
the same node differ at some step in the target class mod p^K, so the points differ.
Uncountable and perfect: Σ is strongly connected and not a single simple cycle, so some node a
of Σ has two distinct out-edges inside Σ. Given x ∈ Λ_Σ and t, follow x's walk for t steps,
then a path in Σ to a, then either of the two edges, then any infinite continuation in Σ. This
gives two different infinite walks, hence two different points of Λ_Σ, in the cylinder of x of
depth t; at least one differs from x. Repeating the choice infinitely often gives 2^ℵ₀ walks.

(2) Let x ∈ Λ_Σ, t ≥ 0, π its walk of length t, C an expanding cycle of Σ through a node r.
Strong connectivity gives paths π_end ⇝ r and r ⇝ π_start in Σ. For d large, the closed walk
π · (π_end ⇝ r) · C^d · (r ⇝ π_start) has multiplier > 1, since each C contributes a factor
λ_C > 1 and the rest is fixed. By (M) it is followed by exactly one point y, which is
T̂-periodic, expanding, lies in Λ_Σ (its orbit only uses nodes of Σ) and agrees with x along
π, i.e. lies in x's cylinder of depth (number of divisions on π) + K. As t → ∞ these
cylinders shrink to x.

(3) Theorem W and (2). ∎

`check_wall.py [DENSE]` constructs these points exactly for random walks of length 10, 20, 40
in K7 (z-form) and sf3_13.

**Corollary W2 (classes that are CM, so certify only systems without expanding periodic
points). PROVED.** Each of the following V is CM at every point outside a finite union E of
periodic orbits (E = ∅ unless stated):

1. V(n) = c(n mod Q^K)·n + d(n mod Q^K) + o(n), c > 0 (round-3 potentials; any additive
   correction that is o(n) uniformly, e.g. any digit statistic of size O(log n)).
2. V(n) = n^γ·e^{ψ(n)} with γ > 0 and ψ bounded on a neighbourhood of each point (for example
   ψ continuous on Ẑ_Q, or ψ a *bounded* function of the real mantissa n/p^{⌊log_p n⌋}).
3. V(n) = g(n)·c(n mod Q^K) with g increasing and c > 0. (The first version also assumed
   g(ρt)/g(t) ≥ max c / min c; REFEREE1 noted that this is not needed, because c is constant
   on a cylinder of depth ≥ K, so ρ = 1 works.)
4. V(n) = c·(number of base-p digits of n) + β, with β bounded and c > 0 (Theorem A shows
   that window-additive potentials collapse to this form).
5. Counters at finitely many points: V(n) = Φ(n, n mod Q^K, v_p(n − x_1), …, v_p(n − x_r)) with
   Φ increasing in its first argument in the sense of 3; v_p(n − x_i) is locally constant away
   from x_i, so V is CM off E = {x_1, …, x_r} (and Theorem W applies to their orbits).
   *Remark (not proved; heuristic only):* accelerated certificates along finitely many orbits
   look like potentials of this kind. Theorem N's certificates are covers with stopping times,
   not potentials, and no translation between the two is proved here.
6. Lexicographic tuples, ordinal sums and finite sums of functions that are CM at x are CM at x
   (componentwise ≥ implies lexicographic ≥).

*Proof.* Each item is a direct check of the definition on a cylinder small enough that the
residue and counter values are constant (item 5 off E). Item 1: on such a cylinder c is a
constant c > 0 and d is a constant; take ρ = 2 and R so large that |o(m)| ≤ c·m/8 for m ≥ R.
Then for n ≥ R and n' ≥ 2n, V(n') − V(n) ≥ c n' − c n − c n/8 − c n'/8 = c(7n'/8 − 9n/8)
≥ c(14n/8 − 9n/8) > 0. Item 2: if |ψ| ≤ B near x, take ρ = e^{2B/γ}. Item 3: on a cylinder of
depth ≥ K the factor c is a constant c > 0, so n' ≥ n gives V(n') ≥ V(n); take ρ = 1.
Item 4: if |β| ≤ B, take ρ = 2^{2B/c + 1}; then n' ≥ ρn gives a digit count larger by at least
⌊2B/c + 1⌋ > 2B/c. Item 6: componentwise ≥ implies ≥ for lexicographic tuples, ordinal sums and
finite sums. Item 5 off E: on a small enough cylinder around x ∉ E every counter is constant,
so item 5 reduces to item 3. ∎

So for a unit-multiplier system, a certificate from the classes **without counters** (items
1–4 and 6 built from them) exists **iff** the system is CERT (every cycle of G_K contracts).
"If" is the round-3 potential c(r)·n (item 1). "Only if": suppose G_K has a cycle with multiplier ≥ 1.
If that cycle contains a division, it is expanding (a product of units over a positive power of p
is never 1), and (M) (Lemma D / trichotomy.md) gives an expanding periodic
point, and Theorem W gives a contradiction, since these classes are CM everywhere. If the cycle
has no division, every step is n ↦ un + v with u a unit, so the class mod p^K of T(n) depends
only on that of n, and every integer of the starting class follows the cycle forever. Its
multiplier is the product of the u's, which is ≥ 1. If it is > 1, or it is 1 and the total
shift is > 0, every orbit of the class tends to ∞. If it is 1 with shift 0, every integer of the
class is periodic. Either way no certificate of any kind exists (Lemma S). (Under the
standing hypothesis of trichotomy.md this case does not occur.) (The
division-free case was missing in the first version; REFEREE1 supplied it.)

With finitely many counters (item 5) the reach is at most the systems all of whose expanding
periodic points lie on finitely many orbits. It does include type-(b) systems (Remark below).
By Corollary W1 it never includes a type-(c) system, because there the expanding periodic
points are dense in an uncountable set. This is Theorem N restated for potentials.
*[Corrected after REFEREE1. The first version stated the "iff CERT" for all items, counters
included. That was WRONG; see the Remark.]*

**Remark (a counter certificate for a type-(b) system; REFEREE1's example). PROVED** (the
argument is the referee's, REFEREE1.md [TYPEB]; exact check: `referee1_check.py [TYPEB]`).
acc_h16 (round 3: even n → n/2; odd n: n + 1 if n ≡ 5, 9 (mod 16), n + 5 if n ≡ 13, else 3n + 1)
is type (b). Its graph G_4 has SCCs of sizes 1, 1, 1, 1, 2, 10; the 2-node SCC {15, 14} is the
shadow of x* = −1. Put V(n) = (lev, φ) in lexicographic order, where lev is the height of the
SCC of n mod 16 in the SCC DAG, φ = c(r)·n on every contracting SCC with an internal edge (the 10-node SCC and the
self-loop SCC {0}) (c from max-mean
potentials with θ = 99/100, verified exactly), φ = 2·v_2(n+1) on node 15,
φ = 2·v_2(n/2 + 1) + 1 on node 14, and φ = 0 on the nodes 7, 8, 12, which have no internal edge. Then:
* leaving an SCC lowers lev;
* 15 → 14 is n ↦ 3n + 1, and (3n+1)/2 + 1 = 3(n+1)/2, so φ goes from 2j to 2j − 1;
* 14 → 15 is n ↦ m = n/2, and φ goes from 2v_2(m+1) + 1 to 2v_2(m+1);
* inside a contracting SCC, φ(Tn) ≤ θφ(n) + β ≤ φ(n) − 1/2 once φ(n) is large.
So V descends in a well-order off a finite set, and Lemma S applies. Every component is CM off
the orbit {−1, −2}, consistent with Theorem W (−1 ∈ B(V)). So counters at finitely many points
do reach type (b).

**Mixed system mb_s3_27.** `n ≡ 26 (27) → (n+1)/27; else even → n/2; else (3n+1)/2`. Its
multipliers are not units at 54, so the trichotomy does not apply, but Theorem W does.
`check_wall.py [MB]` verifies exactly: the cycle −5 → −7 → −10 (multiplier 9/8) is shadowed by
integers n ≡ −5 (mod 2^{N+3k}3^N) with T^{3k}(n) + 5 = (9/8)^k (n + 5); an enumeration of all
branch words of length ≤ 12 finds 16274 rational periodic orbits in Z_(2) ∩ Z_(3), of which two
are expanding (−10 with 9/8 and the 11-cycle through −10138/139 with 2187/2048); and for
d = 10, 20, 40 there are expanding rational periodic points that follow the −5 cycle d times and
then a word of length 2 (EVIDENCE that there are infinitely many: the count of such points with
exit words of length ≤ 7 grows with d, 7 at d = 5 up to 64 at d = 40, `scratch/mb_homoclinic.py`).
So any potential for mb_s3_27 must fail CM at all these orbits. Whether there are infinitely
many is OPEN (not proved).

## 3. Theorem A: digit-window potentials collapse

Fix base 2 and a window width s ≥ 1. For n ≥ 1 with binary digits n_0 (lowest), n_1, …,
put n_i = 0 for i < 0 and i ≥ len(n). For f : {0,1}^s → R let

    V_f(n) = Σ_{i=0}^{len(n)−1} f(n_i, n_{i+1}, …, n_{i+s−1}).

A **window potential** is V = V_f + g(n mod 2^b) + h(top b digits of n), with g, h bounded
(any boundary convention differs from V_f by such terms). Such a V is a sliding-window
weighted automaton (a de Bruijn automaton with additive weights) and reads every digit of n.

**Theorem A. PROVED for (u, s) with u = 3, s ≤ 10 and u = 5, s ≤ 8.** Let T be a 2-adic table
map with a branch T(n) = (u n + v)/2^e on some class r mod 2^m, and with an expanding periodic
point. Then T has no potential certificate (V, δ, F) with V a window potential of width s.

The proof has four steps. Write c₀ = f(0^s) and, for a word h (an integer h ≥ 1),

    E_f(h) = Σ over the windows that touch the digits of h (positions −(s−1) … len(h)−1)
             of (f(window) − c₀).

For a cyclic binary word x of length k let F(x) be the sum of f over its k cyclic windows.

*Step 1 (pumping: Φ ≤ 0).* The LSB-first "multiply by u" transducer has carries 0 … u−1. Reading
the k bits of x from carry c it outputs k bits y and ends with carry c'; ux + c = y + 2^k c'. A
*closed walk* is a pair (x, c) with c' = c. Claim: for every closed walk, Φ(x) := F(y) − F(x) ≤ 0.
Take n_M = r + 2^m (β + 2^b X_M), where X_M is the word x repeated M times and the buffer β is
chosen so that the carry of u·n + v entering the block is c (any carry can be reached by
a few buffer digits). Then T(n_M) = (u n_M + v)/2^e has the digits of a fixed lower part, then
y repeated M times, then a fixed top part (the carry c flushed into zeros). Windows inside a
periodic stretch sum to the cyclic sums, so V(T n_M) − V(n_M) = M·Φ(x) + A with A independent of
M (the shift by e does not change sums). If Φ(x) > 0 then for large M, n_M ∉ F and
V(T n_M) > V(n_M) − δ, a contradiction.

*Step 2 (bijection: Φ = 0 at odd lengths).* Let k be odd and u ∈ {3, 5}, so gcd(u, 2^k − 1) = 1
(3 | 2^k − 1 iff k is even; 5 | 2^k − 1 iff 4 | k). For each word x ∈ [0, 2^k) there is exactly
one closed walk: c' = c means y = ux − c(2^k − 1) with 0 ≤ y ≤ 2^k − 1 and 0 ≤ c ≤ u − 1. For
x = 0 only c = 0 works (y = 0); for x = 2^k − 1 only c = u − 1 (y = 2^k − 1); for other x, ux is
not ≡ 0 mod 2^k − 1, so y must be the residue of ux in [1, 2^k − 2], which fixes c, and
0 ≤ c ≤ u − 1 holds. Hence x ↦ y is a permutation of [0, 2^k) (×u on Z/(2^k − 1) plus the two
fixed words). Summing, Σ_x Φ(x) = Σ_x F(y(x)) − Σ_x F(x) = 0, and with Step 1 every Φ(x) = 0.
(`check_windows.py [BIJ]` re-checks the bijection for odd k ≤ 13.)

*Step 3 (invariance).* For h ≥ 1 take k odd with k ≥ len(uh) + s and x = h padded with zeros.
Then ux < 2^k − 1, so c = 0 and y = uh padded. All windows of x that do not touch h are 0^s, so
F(x) = c₀k + E_f(h), and likewise F(y) = c₀k + E_f(uh). By Step 2, **E_f(uh) = E_f(h) for all
h ≥ 1.**

*Step 4 (rigidity, by computation).* The kernel of the linear map
f ↦ (E_f(uh) − E_f(h))_{1 ≤ h < 2^{s+2}} contains the constants and the coboundaries
f(w) = π(w_1…w_{s−1}) − π(w_0…w_{s−2}); together these span a space of dimension 2^{s−1}
(the coboundary map has kernel the constant π because the de Bruijn graph is strongly
connected; a nonzero constant is not a coboundary because its sum over the loop at 0^s is not
0). `check_windows.py [RANK]` computes the rank of the map modulo the prime 2^31 − 1 as exactly
2^{s−1} for u = 3, s ≤ 10 and u = 5, s ≤ 8. The rank over Q is at least the rank mod p, so the
kernel over Q has dimension ≤ 2^s − 2^{s−1}, and is therefore exactly constants + coboundaries.
For such f, E_f ≡ 0 (constants cancel by definition; coboundaries telescope to π(0^{s−1}) −
π(0^{s−1})).

*Conclusion.* Directly from the definitions,
V_f(n) = E_f(n) + c₀·(len(n) + s − 1) − Σ_{i=−(s−1)}^{−1} f(window_i(n)). With E_f ≡ 0 this is
c₀·len(n) + β(n), where β depends only on the lowest s − 1 digits. So
V = c₀·len(n) + (bounded). Since V ≥ 0, c₀ ≥ 0. If c₀ > 0, V is CM everywhere (Corollary W2.4)
and Theorem W gives a contradiction at the expanding periodic point. If c₀ = 0, V is bounded,
so every orbit segment avoiding F has length ≤ sup V/δ; but integers shadowing the expanding
periodic point for kL steps are arbitrarily large and avoid F along the whole segment. ∎

**Scope.** The theorem covers every OBST system of the S-family (3x+1 branch), all 8 cores,
K7 in its z-form (branch (3z+1)/2), 3x+1 and 5x+1 (×5, s ≤ 8). It also covers the type-(b)
systems acc_h16, acc_h32 that round 3 settles by Theorem H: no window potential proves them
either.

**OPEN.** Step 4 for all s. EVIDENCE: rank exactly 2^{s−1} for every s tested. A general proof
would need: a local, block-additive function E on Z_{>0} with E(2h) = E(h) = E(3h) vanishes.

## 4. What Theorem A says about automata in general (reduction; not a theorem)

A deterministic LSB-first automaton with additive weights reads n's digits and sums a weight
per transition. Window potentials are the case of a de Bruijn automaton. Counters (for example
"number of trailing 1s", which is what an accelerated certificate along −1 uses) are the case
of an automaton with a transient "alive" state and an absorbing "dead" state. The argument of
Theorem A goes through in part for any such automaton A:

* Step 1 (pumping) holds verbatim on the product of the ×u transducer with two copies of A (one
  reading n, one reading T(n)).
* In place of Step 2, the uniform measure gives: on the recurrent part of that product graph,
  every closed walk has Φ = 0, and all bottom SCCs of A have the same mean weight μ under
  uniformly random digits. (Sketch: multiplication by a unit preserves Haar measure, so both
  copies of A see i.i.d. uniform digits; the mean of Φ is then 0, and all closed walks have
  Φ ≤ 0.) We have not written this out in full; treat it as a sketch.
* Step 4 (rigidity) is what is missing: we do not know that a ×3-invariant weighting of a
  general bottom SCC is cohomologous to a constant.

If rigidity held for every bottom SCC, the same conclusion would follow for every system whose
type-(c) set Λ_Σ has non-empty interior (for K7, Λ_Σ = Z_2, since its level-2 graph is one SCC):
the alive part of A would have to contain a dense set of expanding periodic points, and the
set of points whose run never reaches a bottom SCC has empty interior. So the precise OPEN
question for deterministic additive automata is the rigidity lemma. Natural and arctic matrix
interpretations are not deterministic additive automata (they can count with polynomial growth
and take maxima), and they are not covered.

## 5. Tests against 3x+1 and known cycles

Consistency check of Theorem A (EVIDENCE, `scratch/lp_window.py`): an LP over the window
weights f (s = 2, 4, 6) asking for V(K7(z)) ≤ V(z) − 1 on 64 ≤ z < 20000 and V ≥ 0 is
infeasible, as the theorem predicts.

Every negative statement above also applies to 3x+1, which is the expected behaviour: the
theorems say what a class of proofs *cannot* do. No positive claim was made that would also
prove 3x+1. The z3 searches (srs.md) found no interpretation for any core, and the encoding
check confirms that the rewriting systems really simulate the maps (so a found interpretation
would have been a proof; none was found).

## 6. What a potential would need (the feature list)

1. **Non-monotone in size at every expanding periodic point** (Theorem W). On a type-(c) SCC
   this is a dense subset of an uncountable Cantor set (Corollary W1). So V must, inside
   arbitrarily small p-adic cylinders, assign *smaller* values to some *much larger* integers.
   Any V that is "residue information times an increasing function of size" fails.
2. **Not window-additive** (Theorem A). A potential that sums local digit weights is forced to
   be c·(digit count) + bounded, because the descent condition at a ×3 branch makes its window
   sums invariant under multiplication by 3. So the high digits must enter V non-additively:
   through products with polynomial growth (matrix interpretations), maxima, or long-range
   memory (an automaton whose bottom SCCs are not rigid, if such exist).
3. **Itinerary information at depth proportional to the digit count.** Along the shadow of an
   expanding point, V(n) must exceed the number of steps the orbit of n stays in the shadow,
   which is of order log n and is determined by the 2-adic itinerary of n. The map from digits
   to itineraries is the 2-adic conjugacy of the map. *Heuristic, not proved and not checked
   against the literature:* for 3x+1 this conjugacy should not be computable by a finite
   automaton reading the digits. (The first version stated this as a fact; REFEREE1 marked it
   GAP. It is now labelled a heuristic, and nothing else in this file depends on it.) If the
   heuristic is right, a successful V must encode itinerary-type information about the low
   digits that a finite-state reader of the digits cannot compute, while staying well-founded. Matrix interpretations of a rewriting encoding avoid this by
   reading the intermediate mixed-radix strings rather than the digits of n; that is why they
   remain the one class here that the wall does not cover.
