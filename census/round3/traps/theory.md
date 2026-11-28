# Theory: avoider graphs, SCC certificates and homoclinic obstructions

All statements here are PROVED. The finite content of every application is checked by
`check.py`, which runs in about 10 s. Novelty: Theorem 1 is close in spirit to the residue-graph
ranking method of Yolcu–Aaronson–Heule (arXiv:2105.14697, Prop. 4.7). That attribution comes
from `census/round2/literature/yah_avoid57.md`; I did not re-read the paper. I did not check the
novelty of Theorems 2–4 or Corollary 5. I know of no source for them.

## Setting

**The map T.** Fix β ≥ 1 and, for every residue i mod 2^β, a branch (a_i, b_i, e_i). The
branch data satisfy:

* a_i is odd and positive;
* e_i ≤ β;
* 2^{e_i} divides a_i·i + b_i.

For n ≡ i (mod 2^β), set T(n) = (a_i n + b_i)/2^{e_i}. The division is exact on the whole class.
T extends continuously to Z_2, and it acts on rationals with odd denominator. Examples:

* C_{a,b} has β = 1, with the branch (1, 0, 1) on evens and (a, b, 0) on odds.
* T_{a,b} is the shortcut map. Its odd branch is (a, b, 1).

We assume b_i ≥ 0, so T maps positive integers to positive integers. We also assume that every
cycle of the graphs below contains a step with e ≥ 1. This holds for C_{a,b} and T_{a,b}: an
odd step of C lands on an even residue, and the next step halves.

**The trap and the graph.** A trap set is a set A of residues mod 2^k. Let m ≥ m0 := max(k, β).
The avoider graph G_m^A is defined as follows:

* **Nodes:** the residues r mod 2^m with r mod 2^k ∉ A.
* **Edges:** r → s whenever some n ≡ r (mod 2^m) has T(n) ≡ s (mod 2^m). Equivalently, let i be
  the branch of r and set y = a_i r + b_i. Then s runs over the 2^{e_i} lifts of
  y/2^{e_i} mod 2^{m−e_i} that lie outside A.
* **Weight:** the edge carries the multiplier a_i/2^{e_i}. The multiplier of a closed walk is the
  product of the multipliers of its edges. It equals a^•/2^E with an odd numerator and E ≥ 1, so
  it is never 1. Every cycle is therefore either **expanding** (multiplier > 1) or
  **contracting** (multiplier < 1).

**The statement under study.**

**S(T, A).** Every positive orbit meets A (some iterate is ≡ an element of A mod 2^k), or is
eventually periodic. The cycles of the second kind form an explicit finite list.

For T = C_{3,1} with the list {(1 4 2)} (or no list, when A meets the trivial cycle), this is the
residue-avoidance question of YAH §4.5.

## Lemma 0 (lifting walks)

Let W = (r_0 → r_1 → … → r_ℓ) be a walk in G_m with E halvings in total. Then:

* the set Z_W of 2-adic x that follow W (x ≡ r_0 and T^j x ≡ r_j mod 2^m) is a cylinder of level
  m + E;
* T^ℓ maps Z_W affinely and bijectively onto the cylinder r_ℓ + 2^m Z_2, with multiplier
  (∏a)/2^E.

Consequently, a closed walk C at level m has exactly one 2-adic point x* that follows C forever
from r_0. That point is rational, satisfies T^ℓ x* = x*, and has the multiplier of C. Moreover,
x* is the only 2-adic point whose residue path is C^∞.

*Proof.* Induction on ℓ. One step on r + 2^{m+E'}Z_2 is affine with odd multiplier a and
division 2^e. Its image is a cylinder of level m + E' − e. Requiring the image to lie in the class
r_1 mod 2^m fixes e more bits, because each of the 2^e lifts is attained. Composing gives the
claim. For a closed walk, T^ℓ maps Z_C onto r_0 + 2^m Z_2 ⊇ Z_C, so T^{−ℓ} restricted to this
cylinder is a 2^{−E}-contraction of Z_C. It has a unique fixed point, and the fixed point of an
affine map with rational coefficients is rational. Any x that follows C^∞ lies in the nested
cylinders Z_{C^t}, whose levels go to infinity, so x = x*. ∎

`lift_cycle` and `lift_walk_to` in `traps_lib.py` compute these points exactly and re-verify
them by stepping with Fractions.

## Theorem 1 (pure potential; the dichotomy for descent certificates)

The following are equivalent:

* (a) every cycle of G_{m0}^A contracts;
* (b) every cycle of G_m^A contracts, for every m ≥ m0;
* (c) no 2-adic point that avoids A is T-periodic with multiplier > 1;
* (d) there is a finite descent certificate restricted to avoiders: a set of cylinders mod 2^K
  and step counts j, such that each cylinder either meets A within j steps, or satisfies
  T^j(n) < n for all large n in it and avoids A for those j steps.

If they hold, there are integers Q ≥ 1, P_a with a^Q < 2^{P_a} (or P_1 = 0), and φ on the nodes,
with

    φ(u) ≥ φ(v) + P_a − Q e + 1        for every edge u → v (branch (a, b, e)).        (*)

Choose B with (a(B+1) + |b|)^Q < 2 (a(B+1))^Q for every branch. Then every positive orbit that
avoids A enters [1, B]. So S(T, A) holds, and its cycle list is the list of cycles reached from
[1, B] that avoid A.

*Proof.*

* **(a) ⇔ (b) ⇔ (c).** An expanding cycle at any level lifts to an expanding periodic avoider
  (Lemma 0). Conversely, the residues of an expanding periodic avoider mod 2^m form an expanding
  closed walk at every level m ≥ m0.
* **(c) ⇒ (d).** By (b), the log-weights of walks of length ℓ are at most c_0 − δℓ for some
  δ > 0. So every avoider cylinder of depth ℓ > c_0/δ has λ_ℓ < 1. Every point of Z_2 either
  meets A or reaches such a depth, and König's lemma gives a finite cover.
* **not (c) ⇒ not (d).** This is Lemma B of `census/round2/descent/lemmas.md`. Points 2-adically
  close to the expanding periodic avoider y (taken at the start of a positive cyclic shift) avoid
  A and grow for any prescribed number of steps.
* **The potential (*).** Choose Q larger than 3/|μ|, where μ < 0 is the maximum mean log2-weight.
  Every cycle then has integer weight Σ(P_a − Qe + 1) ≤ 0, so a longest-path potential exists.
  This is found by Bellman–Ford and verified exactly.
* **The descent.** Put V(n) = n·2^{φ(n mod 2^m)/Q}. For one step n → T(n) along the edge u → v:

      V(Tn)/V(n) = (a/2^e)(1 + b/(an))·2^{(φ(v)−φ(u))/Q}
                 ≤ a·2^{−P_a/Q}·2^{−1/Q}(1 + |b|/(an))
                 ≤ κ := 2^{−1/Q}(1 + |b|/(a(B+1)))  < 1    for n > B.

  If an avoiding orbit stayed above B forever, V would tend to 0. But V ≥ n·2^{min φ/Q} >
  B·2^{min φ/Q} > 0, a contradiction. ∎

## Theorem 2 (SCC certificate: expanding cycles that are isolated)

Suppose every strongly connected component of G_m^A (m ≥ m0) is one of the following:

* **trivial:** no internal edge;
* **simple:** every node has exactly one internal out-edge, so the component is one cycle;
* **contracting:** every internal cycle contracts.

Then S(T, A) holds. Every positive orbit avoiding A enters [1, B], where B is defined as in
Theorem 1 from potentials on the contracting components only. Hence the cycle list consists of:

* the cycles reached from [1, B] that avoid A;
* the lifts x* of the simple components that are positive integers. No such lift is expanding:
  a positive integer cycle has multiplier < 1, because ∏(a + b/x_j)/2^E = 1.

**Proof.**

1. **Ranking the components.** The components are ranked in topological order. Along any path the
   rank never decreases, so every infinite path in G_m^A eventually stays in one component S.
2. **The residue path.** Let n be a positive integer whose orbit avoids A. Its residues mod 2^m
   form an infinite path in G_m^A.
3. **Case S simple.** The tail follows the cycle of S forever. By Lemma 0 the tail point equals
   x*, so it is a positive integer periodic point and is listed.
4. **Case S contracting.** Apply the potential argument of Theorem 1 on S alone. Only edges
   inside S are used from that time on. The orbit therefore drops to ≤ B, and its fate is the
   simulated fate of that value.
5. **Case S trivial.** A path cannot stay forever in a trivial component.

The verifier `verify.check_certificate` checks exactly what this proof uses:

* the edges are re-derived by brute force, independently of `traps_lib`;
* the rank condition holds on every edge;
* in a functional component each node has out-degree ≤ 1, and the exact lifts are listed;
* the potential inequalities (*) hold;
* the inequality defining B holds;
* the simulation of [1, B] gives the claimed cycles. ∎

The new content beyond Theorem 1 is the simple components. An expanding 2-adic cycle (for
example −1 under C, or −1/3 under C_5) is harmless when no avoider can leave its neighbourhood
and come back. The unbounded growth during a long run near x* does not matter. After the run the
orbit sits in a component of strictly larger rank, where the multiplicative potential decreases
regardless of the starting size. This answers task item (4): these are exactly the trap sets with
an expanding avoiding cycle that are nevertheless provable.

## Theorem 3 (homoclinic obstruction: no certificate at any level)

Let x* be a periodic avoider with period L and multiplier λ > 1. Suppose z is a 2-adic point
with the following properties:

* z ≡ x* (mod 2^{m0});
* z is not on the orbit of x*;
* the first j points of the orbit of z avoid A;
* T^j z = x*.

(Call this a *homoclinic avoider orbit*.) Then, for every m ≥ m0, the SCC of G_m^A that contains
the residue cycle of x* is neither simple nor contracting. So the hypothesis of Theorem 2 fails
at every level, and by Theorem 1 no avoider descent certificate exists.

*Proof.*

1. **The inverse branch.** Let D = x* + 2^{m0}Z_2. Points of D' = x* + 2^{m0+E}Z_2 follow the
   branches of x* for L steps and avoid A (the precision never drops below m0 ≥ k, β). T^L maps
   D' onto D affinely, so its inverse g: D → D' is a 2^{−E}-contraction fixing x*.
2. **Points close to x*.** Put z_t = g^t(z). Then z_t → x*, and T^{Lt} z_t = z, so the orbit of
   z_t avoids A forever (it ends on the cycle of x*). For t large, z_t ≡ x* mod 2^m. Its residue
   path therefore starts on the cycle of x* and ends on it, so the whole path lies in the SCC S
   of that cycle.
3. **S is not contracting.** S contains the expanding residue cycle of x*.
4. **S is not simple.** If S were simple, z_t would follow its cycle forever. By Lemma 0, z_t
   would then be a point of the orbit of x*, and so would z = T^{Lt} z_t. This is a
   contradiction. ∎

## Theorem 4 (a non-simple expanding SCC yields a homoclinic orbit)

Suppose that, at some level m, an SCC S of G_m^A is non-simple and contains an expanding cycle.
Then a homoclinic avoider orbit exists, and it can be computed (`homoclinic_from_scc`).

*Proof.*

1. **A simple expanding cycle.** Decompose an expanding closed walk into simple cycles. Since the
   log-weights add, some simple cycle C1 expands. Let r0 ∈ C1, and let x* be the lift of C1 from
   r0.
2. **Two closed walks.** S is strongly connected and not a single cycle, so some node u ∈ S has
   two internal out-edges u → v1 and u → v2. Take a path P from r0 to u and paths Q_i from v_i
   back to r0, all inside S. Set W_i = P·(u → v_i)·Q_i.
3. **The candidate points.** By Lemma 0 there is a unique w_i that follows W_i with
   T^{|W_i|} w_i = x*. Then w_i ≡ r0 ≡ x* (mod 2^m), and its orbit avoids A.
4. **One of them is off the orbit.** Suppose w_i lies on the orbit of x*. Since C1 is simple, r0
   occurs once per period, so w_i = x*. Then W_i is a prefix of the residue path C1^∞ of x*.
   W_1 and W_2 cannot both be prefixes of the same sequence, because they differ right after P.
   So some w_i is not on the orbit, and it is the required z. ∎

## Corollary 5 (the method is a decision procedure; the level does not matter)

**Lemma 6.** If the hypothesis of Theorem 2 holds at level m, it holds at every level m' ≥ m.

*Proof.* An SCC S' at level m' projects into an SCC S at level m.

* If S is contracting, so is S'.
* If S is simple, every closed walk in S' projects to a power of the cycle of S. By Lemma 0 it
  then lifts to the same x*. So S' consists of the residue cycle of x* mod 2^{m'}. An extra edge
  inside S' would give a closed walk with a different residue sequence that also lifts to x*,
  which is impossible. ∎

**Corollary 5.** Combining Theorem 2, Lemma 6, Theorem 4 and Theorem 3, the following are
equivalent:

* the hypothesis of Theorem 2 holds at some level;
* it holds at level m0 = max(k, β);
* there is no homoclinic avoider orbit.

Every trap set is therefore exactly one of:

* **P0** — no expanding avoiding cycle (Theorem 1);
* **P1** — expanding cycles exist, but they all sit in simple SCCs (Theorem 2);
* **H** — a homoclinic avoider orbit exists. No SCC certificate exists at any modulus, and no
  descent certificate exists.

The classification is decided at the single level m0, in time roughly linear in 2^{m0}.
Provability (P0 or P1) is monotone in A, because the graphs are node-deleted subgraphs.

**Consistency check against YAH (C = C_{3,1}, k = 3; check [1]).** The six sets {2}, {3}, {4},
{6}, {1,5} and {1,7}, which YAH report proved, are all P0 or P1. The five open sets {0}, {1},
{5}, {7} and {5,7} are all H; of these, {1}, {5}, {7} and {5,7} are their prize Conjectures
4.11–4.14, and {0} is listed as open but is not a numbered prize conjecture. The homoclinic witnesses are:

| set | x* (multiplier) | z |
|---|---|---|
| {7} | −20 (9/8) | −28 |
| {5,7} | −14 (9/8) | −58/3 |
| {1} | −1 (3/2) | −17/9 |
| {0} | −1 (3/2) | −35/27 |
| {5} | −2 (3/2) | −26/9 |

What this says is precise but limited: the open YAH problems are exactly the mod-8 instances
that lie beyond every SCC/descent certificate mod 2^m. It does **not** say that they are false
or undecidable, and it does not exclude other residue-based methods (for example YAH's
rewriting/SAT encodings, non-power-of-2 moduli, or potentials not of the form n·2^{φ(r)/Q}).

**Remark (what H means dynamically).** A homoclinic point z of the expanding (2-adically
repelling) periodic point x* produces, by the standard shadowing construction, avoiders that
follow x* for t_1 periods, then the excursion through z, then t_2 periods, and so on. So the
2-adic avoider set contains a horseshoe. An integer avoider can interleave runs near x*, each
with real growth λ^t, with contracting excursions. Controlling such interleavings is the 3x+1
difficulty itself. I have not proved that the horseshoe statement holds for every H set; it is
a remark, not a claim.
