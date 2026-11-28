# The Markov dichotomy for descent certificates

Lens "dichotomy", round 3. All statements are PROVED unless labelled otherwise.
The finite content of every statement is tested by `check_dichotomy.py`.

## 0. Setting

A **table map** is a modulus Q ≥ 1 together with integers (u_r, v_r, w_r) for each
residue r mod Q. It acts by

    T(n) = (u_r n + v_r) / w_r      for n ≡ r (mod Q).

Q is arbitrary: a prime power p^m, a mixed modulus such as 6 = 2·3 or 30, and so on.
We assume:

* **(H1)** u_r ≥ 1 and gcd(u_r, Q) = 1.
* **(H2)** w_r ≥ 1, w_r | Q, and w_r | u_r r + v_r.
* **(P)** T(n) ≥ 1 for every n ≥ 1. Since T is increasing on each class, it suffices
  to check the least positive n in each class.

By (H2), the division is exact on the whole class r + QZ, because w_r | Q. By (H1)
and w_r | Q, we also have gcd(u_r, w_r) = 1.

**Residue graph.** G_T has vertex set Z/Q and an edge r → s iff
s ≡ (u_r r + v_r)/w_r (mod Q/w_r). Vertex r has out-degree w_r. Every edge leaving r
carries the multiplier λ(r) = u_r/w_r. A walk π = (r_0, …, r_L) has multiplier
λ(π) = ∏_{i<L} λ(r_i). A **translation vertex** is one with u_r = w_r = 1.

**Certificate (round-2 definition).** A modulus M and a step count j(r) for each
residue r mod M such that T^{j(r)}(n) < n for all sufficiently large n ≡ r (mod M).

This setting is more general than round 2's lemmas.md in three ways. There, Q = p^m
with p ∈ {2, 3}. Lemma B there needs a p-adic periodic point. The referee
proposition there covers only p = 2, with even ↦ n/2 and odd branches dividing by 1.

## 1. The realisation lemma (Markov property)

**Lemma 1.** Assume (H1) and (H2). Let π = (r_0, …, r_L) be a sequence of residues,
and let N(π) be the set of n ≥ 1 with T^i(n) ≡ r_i (mod Q) for 0 ≤ i ≤ L.

1. If n follows π, then every consecutive pair (r_i, r_{i+1}) is an edge of G_T.
2. Conversely, if π is a walk of G_T, then N(π) = {a + M t : t ≥ 0} with
   M = Q·∏_{i<L} w_{r_i}. On N(π), T^L(n) = (U n + B)/W with U = ∏ u_{r_i} and
   W = ∏ w_{r_i}. In particular N(π) is infinite.

*Proof.* (1) Let n = r + Qz with r = r_i. Then T(n) = (u r + v)/w + (uQ/w)z, which is
≡ (u r + v)/w (mod Q/w).

(2) We use induction on L. Suppose N(π_{≤i}) = {a + M_i t} with M_i = Q W_i, where
W_i = ∏_{k<i} w_{r_k} and U_i = ∏_{k<i} u_{r_k}. Then T^i(a + M_i t) = Y + K t with
K = U_i M_i / W_i = U_i Q. One more step gives

    T^{i+1}(a + M_i t) = y_0 + (u K / w) t,    where y_0 = (u Y + v)/w.

Here u K / w = u U_i (Q/w). By (H1), gcd(u U_i, Q) = 1, so gcd(uK/w, Q) = Q/w. The
congruence y_0 + (uK/w) t ≡ r_{i+1} (mod Q) is therefore solvable iff
r_{i+1} ≡ y_0 (mod Q/w). Since Y ≡ r_i (mod Q), this says exactly that
r_i → r_{i+1} is an edge. When it is solvable, the solutions t form one class mod w,
so M_{i+1} = M_i w. ∎

This lemma is the only place where gcd(u_r, Q) = 1 is used; see §6. Every walk of
the finite graph G_T is realised by an infinite progression of positive integers,
so G_T describes the dynamics *exactly*. It is not merely an over-approximation.

## 2. Critical multipliers

**Lemma 2.** Assume (H1) and (H2).

* (a) A walk π has λ(π) = 1 iff every vertex on it except the last is a translation
  vertex.
* (b) A translation vertex has out-degree 1. If a cycle C consists of translation
  vertices, every n in the class of a vertex of C follows C forever, and T^{|C|}(n) =
  n + D with D = Σ_{r∈C} v_r.
* (c) Under (P), D ≥ 0 for every translation cycle.

*Proof.* (a) We have ∏u = ∏w. The left side is prime to Q. Every prime factor of the
right side divides Q. So both sides equal 1, and every factor is 1.

(b) w_r = 1 gives out-degree 1. Iterate it.

(c) If D < 0, then T^{k|C|}(n) = n + kD < 1 for large k, which contradicts (P). ∎

So **multiplier exactly 1 occurs only for translation cycles.** Under (P), these are
always obstructions (Lemma 3). This settles the critical case completely: no cycle
with multiplier 1 contracts.

## 3. Obstruction without periodic points

**Lemma 3.** Assume (H1), (H2) and (P). If G_T has a cycle C with λ(C) ≥ 1, then no
descent certificate exists.

*Proof.* Take a certificate (M, j(·)). Write M = M_1 M_2, where every prime of M_1
divides Q and gcd(M_2, Q) = 1. Fix s with M_1 | Q^s.

*Case λ(C) > 1.* By the cycle lemma, rotate C to start just after the last minimum
of its prefix products. Then every partial product along C^∞ is > 1. Let π_k = C^k.
By Lemma 1, N(π_k) is a progression a_k + M_k Z_{≥0} with M_k | M_{k+1}, and these
sets are nested. Their closures in the profinite completion Ẑ_Q = lim Z/Q^i are the
cosets a_k + M_k Ẑ_Q. These are nonempty, compact and nested, so they have a common
point y. (Here M_k | Q^{1+k|C|}, because each w | Q.)

Let r be the residue mod M with r ≡ y (mod M_1) and r ≡ 0 (mod M_2). Put j = j(r),
and take k with k|C| ≥ j. Consider the set of n with n ≡ y (mod lcm(M_1, M_k)) and
n ≡ r (mod M_2). By CRT it is an infinite progression, and it lies inside both the
class r mod M and N(π_k). On it, T^j(n) = (U_j n + B_j)/W_j with U_j/W_j > 1, because
this is a partial product of the rotated cycle. So T^j(n) > n for all large n in it,
which contradicts the certificate.

*Case λ(C) = 1.* By Lemma 2, C is a translation cycle with D ≥ 0. Rotate it to start
after the last minimum of its partial drifts. Then every partial drift is ≥ 0, and
every n in the start class r_0 mod Q satisfies T^j(n) ≥ n for all j. The class of M
that contains a residue ≡ r_0 (mod gcd(M, Q)) meets r_0 + QZ in an infinite
progression. That again contradicts the certificate. ∎

*What this changes.* Round-2 Lemma B needs a rational periodic point. When Q is
mixed (for example 6) and the cycle divides only by 2, the lap map is an isometry
in the 3-adic component and need not have a fixed point there. Lemma 3 needs only
compactness. `decide.py` still reports the rational periodic point B/(W − U)
whenever it lies in Ẑ_Q, and it verifies that point exactly.

## 4. Potentials

**Lemma 4.** If every cycle of G_T has λ < 1, then there are positive integers c(r)
with c(s) u_r < c(r) w_r for every edge r → s.

*Proof.* Let ρ = max over simple cycles C of λ(C)^{1/|C|}. This is a maximum over
finitely many values, so ρ < 1. Choose a rational γ with 1 < γ < 1/ρ. With the edge
weights γu/w, every cycle has product < 1. (Every closed walk splits into simple
cycles.)

Let g(r) be the maximum, over walks starting at r, of the product of γu/w along the
walk, with the empty walk counting as 1. This maximum is finite and attained on a
simple path: cutting out a cycle multiplies by a factor < 1, so it only increases the
product. So g(r) is rational. Prepending an edge gives g(r) ≥ γ (u_r/w_r) g(s) >
(u_r/w_r) g(s). Clear denominators to get integers. ∎

## 5. The theorems

**Theorem 1 (Markov dichotomy).** Assume (H1), (H2) and (P). The following are
equivalent:

* **(a)** a descent certificate exists;
* **(b)** every cycle of G_T has multiplier ∏u/∏w < 1;
* **(c)** there is an integer potential c with c(s) u_r < c(r) w_r on every edge;
* **(d)** a uniform certificate exists, with modulus Q^{k+1} and j ≡ k, where k is
  the least integer with (c_max/c_min) θ^k < 1 and θ = max_edges c(s)u/(c(r)w) < 1.

*Proof.* (b) ⇒ (c) is Lemma 4.

(c) ⇒ (d): For a walk of length k from r_0 to r_k, the product telescopes:
λ = [c(r_0)/c(r_k)] · ∏ [c(r_{i+1}) u_i / (c(r_i) w_i)] ≤ (c_max/c_min) θ^k < 1.
Each class mod Q^{k+1} lies inside a single N(π) for a walk π of length k. The
branches of the first k steps depend on r_0..r_{k−1}, and the modulus of that
progression is Q·∏_{i<k−1} w_i for the walk r_0..r_{k−1}, which divides Q^k. On N(π), T^k(n) = λ n + β with λ < 1.

(d) ⇒ (a) is trivial.

(a) ⇒ (b) is Lemma 3. ∎

Because certificate existence is a property of T alone, Theorem 1 gives the same
answer for every presentation of T. This includes the lifted table at modulus Qd,
as long as (H1) still holds there. *Lifting invariance* is checked in
`check_dichotomy.py`.

**Theorem 2 (GLOBAL, the exceptional set, and the complete cycle list).** Let c be a
potential as in (c), and put V(n) = c(n mod Q) n. For n ≡ r with T(n) ≡ s:

    V(Tn) < V(n)   ⇔   n (c(r) w_r − c(s) u_r) > c(s) v_r.

So the exceptional set F = {n ≥ 1 : V(Tn) ≥ V(n)} is contained in the set of
n ≡ r with n ≤ N_r, where N_r = max_{s∈succ(r)} ⌊c(s) v_r⁺ / (c(r)w_r − c(s)u_r)⌋.
Every orbit meets F. Otherwise V would decrease forever through positive integers.
Every cycle meets F, every orbit is eventually periodic, and **the cycles of T are
exactly the cycles reached from F.**

With g from Lemma 4 at parameter γ, we have c(r)w − c(s)u ≥ c(r) w (1 − 1/γ). This
gives the a-priori bound N_r ≤ (γ/(γ−1)) · (g_max/g_min) · v_r⁺/w_r, which depends
only on the graph and on v.

**Theorem 3 (exact depth).** Assume (b) holds. Call a walk *non-descending* if each
of its nonempty prefixes ρ has λ(ρ) > 1, or has λ(ρ) = 1 with translation drift ≥ 0.
By Lemma 2, λ(ρ) = 1 forces ρ to be a translation walk. Let Λ be the maximal length
of a non-descending walk. Then:

* (a) Λ < ∞, and **the least k over all plain descent certificates equals k\* = Λ + 1**.
* (b) k\* ≤ k_unif ≤ 1 + ⌊log(c_max/c_min) / log(1/θ)⌋ for every potential c.
* (c) In terms of the graph: let μ\* < 0 be the maximum cycle mean of log(u/w), and
  let σ be the span of the potential φ(r) = max over walks from r of
  Σ(log(u/w) − μ\*). Then k\* ≤ 1 + ⌊σ/|μ\*|⌋.

*Proof.* (a) Lower bound: let π be a non-descending walk of length Λ. For any
certificate (M, j), the infinite progression N(π) meets some class r mod M in an
infinite progression. On that progression, every i ≤ Λ has T^i(n) ≥ n for all large
n. So j(r) ≥ Λ + 1.

Upper bound: every walk of length Λ + 1 has a descending prefix. Close each walk at
its first descending prefix. That gives a certificate with modulus Q^{Λ+2} and
j ≤ Λ + 1.

(b) This follows from the bound in the proof of Theorem 1. Finiteness of Λ also
follows from it.

(c) Apply (b) with c = e^φ, which has θ = e^{μ\*}. ∎

For Q = p^m, round 2's engine (`descent_lib.certificate`, Lemma C) computes the same
k\* by splitting cylinders. Theorem 3 computes it **on the graph**, with states
(vertex, prefix multiplier), and this works for any Q. The two agree on all
p-power tables tested (`check_dichotomy.py`, part C). Theorem 3(c) explains why
deep certificates appear. They need a near-critical cycle (|μ\*| small) together
with a large potential span: for example, the 243/256 cycle of desc_s32_max, and
the 3^5·…/… cycles of the base-3 records in `deep.md`.

## 6. What fails without gcd(u_r, Q) = 1 (proved counterexample)

Take Q = 2, with even n ↦ n/2 and odd n ↦ 4n + 4. Then G_T has the edge 1 → 0 with
multiplier 4, and 0 → {0, 1} with multiplier 1/2. The cycle 1 → 0 → 1 has λ = 2 > 1.
But for odd n, T^4(n) = (n+1)/2 < n when n > 1, because 4n + 4 ↦ 2n + 2 ↦ n + 1 ↦
(n+1)/2. So a certificate exists (M = 2, j = (1, 4)), and the only cycle is
(1 8 4 2). Implication (a) ⇒ (b) fails.

The reason is that the image of the odd class is 8Z + 8, a proper sub-cylinder of
the even class, so Lemma 1 fails. The direction (c) ⇒ GLOBAL (Theorem 2) still holds
with the over-approximating residue graph, because Lemma 1(1) only needs H2. The
census maps with p | u (par_10_2, par_6_2) can be accelerated to equivalent maps
that satisfy (H1).

## 7. Distance to provability

**Definition 5.** For a table map T and a modulus Q' that is a multiple of Q, the
distance dist_{Q'}(T) is the least |R| over sets R ⊂ Z/Q' such that some table T'
satisfies (H1), (H2) and (P) at modulus Q', agrees with T off R, and is CERT.

**Proposition 6.** Suppose C_1, …, C_k are cycles of G_{T,Q'} with multiplier ≥ 1.
Then every admissible R must meet every C_i, so dist_{Q'}(T) ≥ the minimum hitting
set of {C_i}. In particular, dist_{Q'}(T) is at least the number of pairwise
vertex-disjoint such cycles.

*Proof.* Edges and multipliers at vertices outside R are unchanged. A cycle that
avoids R is therefore still a cycle of G_{T'}, with the same multiplier, so T' is
OBST by Theorem 1. ∎

For the upper bound, `distance.py` replaces the branch at each r ∈ R by the *reset*
n ↦ ⌊n/Q'⌋ + 1, which is (1, Q' − r, Q'), and runs an implicit-hitting-set loop. When
the reset table of a minimum hitting set is CERT, the distance is exact.

**Theorem 7 (3x+1 is exponentially far from provable, in class count).** Let T be
3x+1 (n/2 on even n, 3n+1 on odd n), presented at Q' = 2^m. Then dist_{2^m}(T) ≥
N(⌊m/2⌋), where N(L₀) is the number of primitive cyclic binary words of length
L ≤ L₀ that contain no two cyclically adjacent 1s and satisfy 3^a > 2^{L−a}, with a
the number of 1s.

*Proof.* Take such a word ω. By Lemma 1 at Q = 2, the sets N(ω^k) are progressions
with moduli 2^{1+k(L−a)}, where L − a ≥ 1. They are nested and their moduli tend to
∞, so the closures meet in exactly one point x_ω ∈ Z_2. Then T̂^L(x_ω) has the same
parity sequence, so it equals x_ω. Its period is L, because ω is primitive, and its
multiplier is 3^a/2^{L−a} > 1.

If x ≡ x' (mod 2^m), induction on the steps shows that the parity sequences of x and
x' agree until the m-th even step. So they agree on a prefix of length ≥ m. Now take
two points of these orbits with periods L, L' ≤ m/2. If they were congruent mod 2^m,
their periodic parity sequences would agree on ≥ m ≥ L + L' − gcd(L, L') positions.
By Fine–Wilf the sequences would then be equal, so the points would be equal.

Hence each orbit traces a simple cycle of G_{2^m}, and the cycles of different orbits
are vertex-disjoint. Proposition 6 finishes the proof. ∎

N(L₀) grows exponentially. Words with no "11" and a 1-frequency above
log 2/log 6 ≈ 0.387 have entropy ≈ 0.58 bit per symbol. So dist_{2^m}(3x+1) ≥
exp(Ω(m)). The exact values computed below are much larger than this bound.

| m | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| dist_{2^m}(3x+1) (`distance.py`; exact up to m=8, lower bounds after) | 1 | 1 | 1 | 2 | 2 | 4 | 5 | 8 | ≥ 10 | ≥ 16 | ≥ 19 |
| density dist/2^m | .50 | .25 | .125 | .125 | .0625 | .0625 | .039 | .031 | ≥ .0195 | ≥ .0156 | ≥ .0093 |

The m ≤ 7 values are re-verified in `check_dichotomy.py` (part H); m = 8 takes 25 s in `distance.py`. The m = 10, 11 bounds are packings of vertex-disjoint expanding cycles, re-verified in part H. The m = 9 bound is an exact minimum hitting set of 40 verified cycles (`distance.py`, 120 s). EVIDENCE only, and OPEN: does dist_{2^m}/2^m → 0? The density was non-increasing up to m = 8 (.5, .25, .125, .125, .0625, .0625, …), not strictly decreasing.

## 8. What is new compared with round 2

Round 2's lemmas.md has Lemmas A–D, the SPLIT/M3 theorems, and a referee proposition
that is stated with a proof sketch for p = 2, n/2 on even n, and w = 1 on odd n. The
following are new here:

1. The setting allows any modulus Q (mixed moduli included) and any w_r | Q. The
   hypothesis that makes the map Markov is isolated as (H1): gcd(u_r, Q) = 1. Its
   necessity is shown by the counterexample in §6.
2. Lemma 1 is a realisation lemma in the integers, with explicit moduli.
3. Lemma 3 is an obstruction that needs no periodic point. This matters for mixed
   moduli.
4. The critical case is classified exactly (Lemma 2). Multiplier 1 means a
   translation cycle, and under (P) that is always an obstruction.
5. Theorem 3 gives the exact certificate depth as a graph quantity, with bounds.
   Theorem 2 gives an explicit exceptional set.
6. Lifting invariance holds.
7. The decision procedure `decide.py` always terminates with an exactly verified
   answer, CERT or OBST. Round 2's family_scan had an UNKNOWN outcome; here it
   cannot occur.
8. Distance to provability, with Proposition 6 and Theorem 7.

**Literature.** I ran one web search. It found that the Markov chain on residue
classes for "relatively prime" generalized Syracuse maps goes back to Matthews and
Watts (Acta Arith. 43 (1984) 167–175; 45 (1985) 29–42). Their Markov chain is the
*random* walk on essentially the same residue graph. The deterministic statement here
is different: a certificate exists iff every cycle of that graph contracts. I did not
find it in that search, and novelty is otherwise not checked. An arXiv paper titled
"Loop Termination and Generalized Collatz Sequences" (arXiv:2605.15094) may be
related. I have not read it.
