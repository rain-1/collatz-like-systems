# Part B2: window approximants, an explicit certificate schema, and the exact reduction

Lens "schema", round 4. Revised after REFEREE1 (corrections are marked in place).
Checks: `check_window.py` (exits 0, about 2 minutes), and
`evidence_window.py` (EVIDENCE only). Library: `windowlib.py`.

Theorem B1 (cutoff.md) shows that approximants which change T only near finitely many
points are never certifiable when T is of type (c). The natural replacement removes
**high-multiplier windows** wherever they occur. These approximants are certifiable, they
agree with T on a set of density → 1, and they have a uniform certificate schema with N
as a symbolic parameter. This file then determines exactly what extra statement would turn
the family into a proof of T, and shows that the statement is the original problem.

## Definitions

Let T be a unit-multiplier table at modulus p^m, with branches (u, v, p^e). Fix a level
K ≥ m. The **window** of a residue r mod p^K is the sequence of steps i = 0, 1, … made
while the number D_i of divisions before step i satisfies D_i ≤ K − m. These steps are
the same for every integer of the class r + p^K Z. Let U_w(r) be the product of the u's
over the window, and D_w(r) its total division exponent; then K − m < D_w ≤ K − m + e_max.
For a rational δ ∈ (0, 1) put

    R_K(δ) = { r mod p^K : U_w(r) > p^{(1−δ) D_w(r)} },

the residues whose window has multiplier > p^{−δ D_w}. The **window approximant** T_K
agrees with T off R_K and is the reset n ↦ ⌊n/p^K⌋ + 1 on R_K.

## Theorem W1 (window approximants are certifiable). PROVED

Assume the standing hypothesis (no division-free cycle), (H1) to (P) for T, and
(1 − δ)(K − m + e_max) < K. The last condition holds for every K ≥ m when e_max ≤ m, as for
3x+1 and K7. Then every cycle of the residue graph of T_K contracts, so T_K has a descent
certificate and its complete cycle list is computable (dichotomy.md, Theorems 1 and 2).

*Proof.* The key fact: along any walk of the residue graph, the steps taken at the nodes
r_i, r_{i+1}, … coincide with the window of r_i for as long as that window lasts. This
holds because the walk is realised by integers (dichotomy.md, Lemma 1), and their window
steps are determined by r_i.

*Cycles avoiding R_K.* Take such a cycle and run it k times. Cut the resulting periodic
walk greedily into consecutive windows. Each full window satisfies U ≤ p^{(1−δ)D}. The
leftover at the end is a prefix of the window of some node x_j ∉ R_K, so it is controlled
by an *upper* bound: U_left ≤ U_w(x_j) ≤ p^{(1−δ)(K−m+e_max)}, a constant independent of k.
(The first version said "the leftover has U ≥ 1"; that is the wrong direction and is
corrected here after REFEREE1.) So U_cyc^k ≤ p^{(1−δ)(k D_cyc + K − m + e_max)} for
every k, which gives U_cyc ≤ p^{(1−δ)D_cyc}. The multiplier is then at most
p^{−δ D_cyc} < 1, since D_cyc ≥ 1.

*Cycles through R_K.* Cut the cycle at its reset nodes. A piece is a reset (multiplier
p^{−K}) followed by a path x_1 … x_s outside R_K. Cut that path greedily into windows.
Full windows contribute ≤ p^{−δD} ≤ 1. The final partial piece is a prefix of the window of
some x_j ∉ R_K, so its multiplier is at most its U, which is at most
U_w(x_j) ≤ p^{(1−δ)(K−m+e_max)}. Each piece therefore has multiplier
≤ p^{−K + (1−δ)(K−m+e_max)} < 1. ∎

**Density.** Under Haar measure, the window of a random residue is a Markov chain (each
division by p^e gives p^e equally likely continuations). So μ(R_K) is a large-deviation
probability, and it tends to 0 whenever δ is smaller than the typical log-contraction per
division. For 3x+1 this is exact. The map from residues mod 2^N to parity vectors of length
N is a bijection (Terras), so

    |R_N| = Σ_{k > 5N/8} C(N, k) ≤ 2^{N·H(5/8)},   H(5/8) = 0.9544,

with the threshold δ chosen so that R_N = {more than 5N/8 odd steps among the first N}.
(Note added in revision: this needs δ = 1 − (5/8) log₂3, which is irrational, while W1 was
stated for rational δ. Nothing depends on this: the proof of W1 uses δ only through the
inequalities U ≤ p^{(1−δ)D}, which make sense for real δ, and for 3x+1 the CERT property
of T_N is proved directly by the explicit potential of Theorem W2, with the odd-step count
as the threshold.)
The densities are 0.105 at N = 16, 1.7·10⁻³ at N = 128, and 3.4·10⁻¹⁶ at N = 1024
(`check_window.py` [W2d]). For K7 with δ = 1/5, the exact densities for K = 3..11 are
1/8, 1/8, 3/32, 9/64, 11/128, 25/256, 35/512, 11/128, 59/1024. They are not monotone, and
their decay is EVIDENCE only.

**Corollary W1′ (answers a round-3 OPEN question). PROVED.** dichotomy.md §7 asked
whether dist_{2^m}(3x+1)/2^m → 0. It does, exponentially: T_N is CERT, agrees with 3x+1
off R_N, and satisfies (H1), (H2), (P) at modulus 2^N. So

    dist_{2^N}(3x+1) ≤ Σ_{k>5N/8} C(N,k) ≤ 2^{N·H(5/8)},   H(5/8) = 0.95443… (so ≤ 2^{0.9545 N}).

Together with Theorem 7 there, the distance is exponential in N in both directions.

**Presentation (added after REFEREE1).** dichotomy.md §7 (Definition 5, Theorem 7 and its
table) is about the **non-accelerated** map T₀: n ↦ n/2 on even n, n ↦ 3n + 1 on odd n,
presented at modulus 2^m. The argument above was written for the accelerated map, and the
first version of `check_window.py` tested only that map. The corollary holds for T₀ as
well, and here is the direct proof. T₀ is a table at modulus 2 (m = 1) with e_max = 1.

* *Same R_N.* The window of r mod 2^N under T₀ consists of the steps made while at most
  N − 1 halvings have been done. An odd step (3n + 1, no division) is always followed by a
  halving, and a 3n + 1 step taken with D_i ≤ N − 1 is followed by a halving with the same
  D_i, so the window always ends right after the N-th halving: D_w = N. Grouping each
  3n + 1 with the following halving gives exactly the N steps of the accelerated map, so
  U_w = 3^k with k the number of odd steps among the first N accelerated steps. Hence the
  T₀-window set {r : k > 5N/8} is the accelerated R_N.
* *CERT.* Let T₀,N be T₀ off R_N and the reset on R_N. It satisfies (H1), (H2), (P) at
  modulus 2^N. Repeat the proof of W1 with "full window" meaning N halvings and k ≤ 5N/8
  odd steps, so a full window has multiplier ≤ 3^{5N/8}/2^N < 1. A cycle avoiding R_N, run
  j times and cut greedily, has multiplier^j ≤ 3^{5N/8}·(3^{5N/8}/2^N)^{(number of full
  windows)}; the number of full windows grows linearly in j, so the multiplier is < 1. A
  piece through a reset has multiplier ≤ 2^{−N}·3^{5N/8} < 1, since the leftover is a
  prefix of a window outside R_N and has U ≤ 3^{5N/8}. (Here δ plays no role; the
  threshold is the odd-step count, and no irrational δ is needed.)

So T₀,N is CERT, agrees with T₀ off R_N, and dist_{2^N}(T₀) ≤ |R_N|. `check_window.py`
[W1′p] verifies, for N = 4..10, that windowlib's generic window construction applied to
the T₀ table gives D_w = N and exactly the accelerated R_N, and that decide.py returns
CERT for T₀,N (REFEREE1 [R7] did the same with its own code and potential). This
bound is far from the exact values: for example |R_8| = 37 against dist = 8. With any
threshold below log 2/log 3 the method cannot give an exponent below
H(log 2/log 3) = 0.9499.

## Theorem W2 (an explicit certificate schema for 3x+1, all N ≥ 4). PROVED

Let γ = 161/160, so γ⁸·243 < 256. For r ∉ R_N with parity window b_0 … b_{N−1}, put

    c(r) = max_{0 ≤ s ≤ N−1} γ^s ∏_{i<s} q(b_i),    q(1) = 3/2, q(0) = 1/2,

and put c(r) = 1/2 on R_N. Then c(s)·u_r < c(r)·w_r on every edge of T_N, so V(n) =
c(n mod 2^N)·n is a Lyapunov function. The exceptional set satisfies

    F_N ⊂ [1, B_N],    B_N = ⌈(161/2)(3γ/2)^{⌊5N/8⌋}⌉ ≈ 80·2^{0.371 N}.

*Proof.* Let r ∉ R_N and r → r′. The window of r′ starts with b_1 … b_{N−1}.

* If r′ ∉ R_N, then q(b_0)c(r′) = γ^{−1} max_{1≤s≤N} γ^s ∏_{i<s} q(b_i). The terms with
  s ≤ N−1 are ≤ c(r). The term with s = N is ≤ γ^N (3^{5/8}/2)^N ≤ 1 ≤ c(r), because
  r ∉ R_N and γ⁸·243 < 256. So q(b_0)c(r′) ≤ c(r)/γ < c(r).
* If r′ ∈ R_N, then q(b_0)·1/2 ≤ 3/4 < 1 ≤ c(r).
* For a reset node, c(s)/2^N ≤ c_max/2^N < 1/2 = c(r), using
  c_max ≤ (3γ/2)^{⌊5N/8⌋} ≤ 2^{N−2}. The second inequality holds for every N ≥ 4, since
  (5/8)·log₂(483/320) = 0.371 < 1 − 2/N.

The bound on F_N comes from c(r) − (3/2)c(s) ≥ (1 − γ^{−1})c(r) on odd steps and from the
analogous estimate at the resets. ∎

The schema is uniform in N: the weights are an explicit formula in the residue's parity
vector. No search is needed, and the proof is the same for every N.
`check_window.py` [W2b] verifies every edge inequality exactly for N = 4..13 (all 2^N
nodes), and [W2c] has decide.py confirm CERT independently for N = 4..11.

## Theorem W3 (the exact reduction; the induction is empty). PROVED

1. For every N ≥ 4: if the 3x+1 orbit of n eventually avoids R_N, then it is eventually
   periodic, and it ends in a 3x+1 cycle that avoids R_N and has an element ≤ B_N.
2. For 4 ≤ N ≤ 26 the complete cycle list of T_N is {(1 2)} (`check_window.py` [W3]). So
   for each such N, **an orbit reaches (1 2) iff it eventually avoids R_N**.
3. Hence, for any single N in [4, 26]: the 3x+1 conjecture ⇔ every orbit eventually
   avoids R_N.

*Proof.* (1) From the time t₀ after which the orbit avoids R_N, it is a T_N-orbit, because
T_N = T off R_N. Apply Theorem W2: it reaches a T_N-cycle made of orbit points, so a cycle
avoiding R_N, and every T_N-cycle meets F_N. (2) An orbit that reaches (1 2) avoids R_N
from then on: the N-windows of (1 2) contain ⌈N/2⌉ ≤ 5N/8 odd steps for N ≥ 4. The
converse is (1) together with the computed cycle list. ∎

**This is where the limit method stalls, stated exactly.** Taking N → ∞ adds nothing. Each
single member T_N already reduces the conjecture to "every orbit eventually avoids R_N",
and these statements are equivalent to each other for all N in the verified range. The
"induction on N" has a trivial step and the whole problem as its base case. The same
happens for any approximant family: GLOBAL(T) ⇔ "every orbit eventually avoids the
modified set" as soon as the true cycles avoid it. This is a reformulation, not a proof.

## Theorem W4 (what extra statement would close the argument). PROVED

**(S_C)** For every n ≥ 2 and every N ≥ max(4, C log₂ n), no N consecutive steps of the
3x+1 orbit of n contain more than 5N/8 odd steps.

If (S_C) holds for some constant C, then every 3x+1 orbit reaches (1 2).

*Proof.* Let N = max(4, ⌈C log₂ n⌉). By (S_C) no orbit point lies in R_N, so the orbit is
a T_N-orbit. By Theorem W2 it ends in a cycle Z all of whose points avoid R_N. Let
x = min Z, L the period, and a the number of odd steps. Windows of length kL inside Z
(k large) have exactly ka odd steps, so (S_C) gives a ≤ 5L/8. The cycle identity
∏_{odd z∈Z} (3 + 1/z) = 2^L, together with z ≥ x, gives 2^L ≤ (3 + 1/x)^{5L/8}, that is,
(3 + 1/x)^5 ≥ 256. Since (3 + 1/31)^5 ≥ 256 > (3 + 1/32)^5, this forces x ≤ 31. The only
cycle with an element ≤ 31 is (1 2) ([W4]). ∎

(S_C) is a statement about sizes, not cylinders: it bounds the windows of an orbit by the
number of digits of its starting point. (The first version added "By Theorem B1 a
statement of this kind cannot be replaced by a cylinder statement". That is informal and
not proved: B1 concerns cut-offs near finitely many points, not all cylinder statements.
The sentence is withdrawn. What B1 does show is that no modification of 3x+1 near finitely
many points is certifiable, so the avoided set in any such reduction cannot be a
neighbourhood of finitely many points.) It is stronger than the conjecture: it implies
logarithmic bounds on stopping times, in the spirit of the Lagarias–Weiss heuristic. I
found no way to prove it, and I make no claim about it.

**EVIDENCE for (S_C)** (`evidence_window.py`). Let A(n) be the largest N for which the
orbit of n has an N-window with more than 5N/8 odd steps. For n ≤ 20000 the largest value
of A(n)/log₂ n is 13.25, at n = 27. For the known stopping-time record holders:
A(837799)/log₂ = 11.0, A(8400511)/log₂ = 14.2, A(63728127)/log₂ = 17.2, and
A(670617279)/log₂ = 15.1. So (S_C) is consistent with C ≈ 20 on this range.

## K7 and designed systems

K7's window approximants (δ = 1/5) are CERT for K = 3..11, and each has the single cycle
z = 0 (`check_window.py` [W1]). Theorems W1 and W3 transfer verbatim: K7's GLOBAL question
with cycle list {0} is equivalent to "every orbit eventually avoids R_K(1/5)" for each
checked K. A K7 analogue of W4 would need K7's cycle identity. I did not write it out.

**Designed type-(c) systems.** For any system, closing the argument means proving an
eventual-avoidance statement such as (S_C). By Theorem B1 this cannot be a statement about
cylinders near finitely many points, because the type-(c) re-entry orbits (−5 for 3x+1,
z = −49/17 for K7) produce high-multiplier windows a bounded distance from x\*. A designed
system would have to make high-multiplier windows provably impossible for small integers
over long stretches. Every design I considered either became type (a)/(b), so it no longer
qualifies, or left that statement as hard as (S_C). **No type-(c) system was settled.**
