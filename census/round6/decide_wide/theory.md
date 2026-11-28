# Theory for the lens "decision procedure and trichotomy, applied to everything"

Round 6. Every statement is labelled PROVED, EVIDENCE or OPEN. Checks: `check_theory.py`
(Lemma S, Propositions P and 4, Theorem B, Theorem H' on mixed moduli), `check_harness.py`
(Theorem H' and decide.py against brute force on the catalog and on every type-(b) member).
External results used: round 3's dichotomy Theorem 1 (`round3/dichotomy/dichotomy.md`) and
Lemma L (level independence of type (c), `round3/accel/trichotomy.md`). Both are internal to
this repository and were refereed there. No external theorem (Evertse, Baker, ...) is used.

## 0. Setting

A *table map* is a modulus Q and, for each r mod Q, integers u_r >= 1, w_r >= 1, v_r with
w_r | u_r r + v_r and w_r | u_r Q, so that T(n) = (u_r n + v_r)/w_r is an integer for every
n = r (mod Q). (P) means T maps positive integers to positive integers (or N0 to N0 for the
three mixedbase maps stated on N0). (H1) is gcd(u_r, Q) = 1 and (H2) is w_r | Q; under both
the map is *Markov* in the sense of round 3.

For a multiple K of Q the *level-K graph* G_K has nodes r mod K. For n = r + K t,
T(n) = y0 + k t with y0 = (u r + v)/w and k = uK/w. Put g = gcd(k, K). The out-edges of r are
the residues y0 + g j mod K (j = 0, ..., K/g - 1), each labelled with the multiplier u/w.

**Lemma 0 (over-approximation). PROVED.** For every n >= 1 the residues T^t(n) mod K form a
walk of G_K. If w_r = 1, node r has exactly one out-edge, and every n = r (mod K) satisfies
T(n) = y0 (mod K).

*Proof.* T(r + Kt) = y0 + kt, and y0 + kt mod K lies in y0 + gZ. If w = 1 then k = uK and
g = K. ∎

Under (H1) and (H2), g = K/w and every edge is realised (round 3, dichotomy Lemma 1). Without
them the graph can have more edges than the map uses, so a statement proved from the graph
remains true, but the graph can miss structure the map has.

SCC types (round 3): an SCC with an internal edge is
**(a)** if every cycle in it has U < W (U, W the products of u and w along the cycle);
**(b)** if it is a single simple cycle with U > W;
**(c)** if it contains a cycle with U >= W and is not a single simple cycle;
**(z)** if it contains a *division-free* cycle (W = 1).
Types (z) and (c) can overlap; the harness reports (z) first. A unit self-loop or any other
division-free single cycle with U > 1 is both (b) and (z) by these words; (z) takes
precedence. (Revision after REFEREE1, nit.) A single-cycle SCC with U = W > 1 (a *neutral*
cycle with a division) belongs to none of (a), (b), (c) as defined. It cannot occur under
(H1) and (H2): there U is prime to Q and W > 1 is a product of divisors of Q, so U != W.
Off (H1)/(H2) the harness labels it 'b'; `padic_kill` then finds no prime with
v_p(W) > v_p(U) (because U = W), so condition (D) below fails and Theorem H' returns NONE.
So no conclusion is ever drawn from such an SCC. In Theorem H', "type (b)" means a single
simple cycle with U > W, and (D) excludes U = W anyway.

## 1. Theorem H' (isolated expanding cycles, any modulus, any multipliers). PROVED

**Theorem H'.** Let T be a table map satisfying (P), and K a multiple of Q. Suppose every SCC of
G_K with an internal edge is of type (a) or of type (b), and that each type-(b) cycle C satisfies

    (D)  some prime p has v_p(W_C) > v_p(U_C).

Then every positive orbit of T is eventually periodic. The complete list of cycles is: for
each type-(b) cycle C, the point x*_C = B/(W_C - U_C) of its lap map x -> (U_C x + B)/W_C if
x*_C is a positive integer whose orbit follows C; and, for each type-(a) SCC Σ, the cycles of the
orbits that start at the finitely many n with c(n mod K) n <= β_Σ/(1 - θ_Σ) (notation below).

Under (H1) and (H2), (D) holds for every cycle with W > 1: the primes of W divide Q, and U is
prime to Q. So Theorem H' contains round 3's Theorem H (prime-power moduli) and extends it to
mixed moduli (Q = 6, 10, 12, ...) and to maps with non-unit multipliers.

*Proof.* Fix n >= 1. By Lemma 0 its residue walk is a walk of G_K. The SCCs form a finite
acyclic order, so from some time t0 the walk stays in one SCC Σ, and Σ has an internal edge.

*Σ of type (b), cycle C of length L.* From time t0 on the walk follows C. Let m = T^{t0}(n) and
f(x) = (U x + B)/W the composition of the L branches along C (exact rationals, U = U_C,
W = W_C). Then T^{jL}(m) = f^j(m) for all j >= 0, and every f^j(m) is an integer. Since
U != W, f has the fixed point x* = B/(W - U), and f^j(m) - x* = (U/W)^j (m - x*). Take p as in
(D) and put δ = v_p(W) - v_p(U) >= 1. If m != x*, then

    v_p(f^j(m) - x*) = v_p(m - x*) - jδ  ->  -infinity.

But f^j(m) is an integer, so v_p(f^j(m) - x*) >= min(0, v_p(x*)), a bound independent of j.
Hence m = x*. So x* is a positive integer and the orbit of n is eventually periodic.

*Σ of type (a).* Every cycle of Σ has U < W. Let μ < 0 be the largest mean of log(u/w) over
cycles of Σ and fix θ with μ < log θ < 0. The longest-path potential for the edge weights
log(u/w) - log θ exists (no cycle has positive weight) and gives positive numbers c(r), r ∈ Σ,
with c(s) u_r <= θ c(r) w_r on every internal edge r -> s. The harness computes c in floating
point, rounds to rationals and verifies every inequality exactly. Put V(x) = c(x mod K) x. For
an internal step x -> (u x + v)/w with x >= 1:

    V(T x) = c(s)(u x + v)/w <= θ c(r) x + c(s) max(v, 0)/w <= θ V(x) + β,

where β = β_Σ is the maximum of c(s) max(v, 0)/w over internal edges. The first inequality
uses x > 0, which holds because of (P). Iterating, limsup V(T^t n) <= β/(1 - θ), so the orbit
eventually stays in the finite set {x : V(x) <= β/(1-θ) + 1} and is eventually periodic.

*Cycles.* A cycle of T is a closed walk, so it lies in one SCC. In a type-(b) SCC it is x*_C.
In a type-(a) SCC, apply the inequality at the point where V is largest: V_max <= θ V_max + β,
so every point of the cycle satisfies V <= β/(1 - θ). Enumerating those n and following their
orbits finds every such cycle. ∎

**Proposition Z (division-free cycles). PROVED.** Let C be a cycle of G_K with W_C = 1, lap
map x -> A x + B (A = U_C, B integer). Then every n = r0 (mod K), r0 ∈ C, follows C forever.
If A >= 2, or A = 1 and B > 0, every such n with A n + B > n has an infinite orbit. If A = 1 and
B = 0, every such n is periodic.

*Proof.* By Lemma 0 each node of C has one successor and the class maps into the next class, so
the whole class r0 follows C and T^L(n) = A n + B there. If A n + B > n then T^L(n) is again in
the class and larger, so the values T^{jL}(n) increase strictly and are all distinct. ∎

(A = 1 and B < 0 contradicts (P).) The harness reports such systems as DIVERGES with an exact
starting value; this re-settles, for example, par_3_2, par_5_2, div2_3n, div3_2n, up_qr7.

**What Theorem H' does not give.** Theorem N (no generalized certificate when type (c) occurs)
is proved in round 3 for prime-power Markov maps only. Its proof needs unique periodic points
for every closed walk, which fails for mixed moduli (a walk that divides only by 2 is not
contracting 3-adically) and for non-Markov maps (the graph over-approximates). For those
classes, a type-(c) SCC at level K is only a failure of this proof. I prove no barrier there,
and lifted levels can change the answer. That happens for the non-Markov mixedbase maps
mb_s3_3, mb_s5_5, ..., which are type (a) at level K = 2m although their natural 2-adic
reading has expanding branches (section 5).

## 2. Where type (b) cannot occur

**Proposition P (prime modulus). PROVED.** Let Q = p be prime and T satisfy (H1), (H2), so
w_r ∈ {1, p}. If G_p has no division-free cycle, then no SCC of G_p is of type (b).

*Proof.* Let C be a single-cycle SCC with U > W. Since G_p has no division-free cycle, C has a
node r with w_r = p, and r's successors are all residues mod p (g = K/w = 1), r itself
included. In a single-cycle SCC each node has exactly one internal out-edge, so C = (r) is the
self-loop. Every other residue s is a successor of r, so s must not reach r. Then no s != r has
w_s = p, because such an s would have r as a successor. So every s != r has w_s = 1 and its
single successor is again != r. That makes N = Z/p minus {r} closed under a function, and N
contains a cycle of w = 1 nodes, a division-free cycle. Contradiction. ∎

**Corollary P'. PROVED.** For a Markov table with prime modulus p and no division-free cycle,
Theorem H (and H') settles exactly the CERT systems: if some cycle of G_p expands, it lies in a
type-(c) SCC of G_p, so by Lemma L of round 3 there is a type-(c) SCC at every level p^k. By
Theorem N there is then no generalized certificate either.

*Proof.* If some cycle expands, its SCC is not of type (a) and, by Proposition P, not of type
(b); so it is of type (c). Lemma L (round 3, unit-multiplier p-adic systems, which is our
situation with m = 1) transports type (c) to every level. ∎

*Going up: no type (b) at any level p^k (added after REFEREE2).* Lemma L as written in round 3
says only that type (c) at one level gives type (c) at every level. The stronger statement used
in the README and in Proposition 4 ("no type (b) at any level") needs one more argument, which
REFEREE1 §5 sketched and REFEREE2 §5 completed. We state it for a Markov unit-multiplier table
read at a base level K0 = p^m (m = 1 here, K0 = 4 in Proposition 4) such that G_{K0} has no
division-free cycle and every SCC of G_{K0} containing an expanding cycle is of type (c). Let
k >= m and let C' be an expanding cycle of G_{p^k}. Then the SCC of C' is not a single simple
cycle; so G_{p^k} has no type-(b) SCC.

*Proof.* A division-free cycle at level p^k would project to a division-free closed walk at level
K0, hence to a division-free cycle there; so there is none. Let P be the projection of C' to
G_{K0}, a closed walk from the projection r of the start node of C'. P has the multiplier of C',
so it expands and lies in an SCC Σ of type (c); and P has at least one division. Let R be the
primitive root of P (P = R^j). Since Σ is not a single simple cycle, some node v of Σ has two
internal out-edges e1, e2. Going from r to v inside Σ, leaving by e1 or by e2, and returning to r
inside Σ gives two closed walks X1, X2 at r that agree up to v and then differ, so neither is a
prefix of the other. Powers of R are pairwise prefix-comparable, so at least one of X1, X2, call
it X, is not a power of R. (REFEREE1's version, "use an edge of Σ outside the projection of C'",
fails when P covers every edge of Σ; this choice of X avoids that.)

Let x* be the p-adic periodic point of C'; its level-K0 walk is P^∞, so it is also the periodic
point of P. For d >= 1 the closed walk P^d X has at least d divisions, so by (M) it has a unique
p-adic periodic point y_d, and y_d follows P^d first. Points following P^d lie in one ball of
radius at most p^{-m-d}, so y_d = x* (mod p^k) for d >= k. Fix such a d. The level-p^k orbit of
y_d is then a closed walk Y of G_{p^k} starting at the start node of C', and all its nodes lie in
the SCC of C'. Its projection to G_{K0} is (P^d X)^n for some n >= 1. If the SCC of C' were the
single cycle C', then Y would be a power of C' and its projection a power of R; but
(P^d X)^n = R^i forces P^d X to be a power of the primitive word R, hence X = R^{i'} for some i',
a contradiction. ∎

(REFEREE2's check, section C of `referee2_check.py`, finds no type (b) on 803 random lifted
(table, level) pairs with prime modulus and no division-free cycle, nor on 3x+1, 3x-1, 5x+1 and
desc_m3_4n5 at every level up to 256.)

Census systems covered by Corollary P' (Q = 2 or 3 after reduction to the minimal modulus):
every par_a_d with a odd and d odd (3x+1, 3x-1, 3x+5, ..., 5x+1, 7x+1, 9x+1), m3_b, m3_d,
m3_e, m3_g, perm_1932 (also as auto_1932, flipT, shiftT, perm1932_1cycle), perm_b, perm_swap,
desc_m3_4n5 and steiner_1cycle. Not covered: mahler and par_10_2, par_6_2 (multiplier not prime
to 2, so (H1) fails). For every covered map the isolated-cycle method gives nothing, at any
level. Round 3 found the same thing by a numerical scan for the open
entries; here it is a theorem for the whole class.

**Theorem S (squarefree modulus, full division). PROVED.** Let Q be squarefree. Suppose every
class r with gcd(r, Q) > 1 has the branch n -> n/q(r), where the prime q(r) | gcd(r, Q)
depends only on the set S(r) of primes of Q dividing r (for example the least such prime,
which is the census "2|n -> n/2; else 3|n -> n/3; ..." rule). Suppose every class prime to Q
has a branch (u, v, 1) with gcd(u, Q) = 1 (no division on units). Then every SCC of G_Q that
contains a cycle with U > W is of type (c) or contains a division-free cycle. In particular
G_Q has no type-(b) SCC that contains a division node (see the wording note below).

*Lemma S.* For a prime q | Q call r a q-node if gcd(r, Q) > 1 and q(r) = q. For a q-node r let
s*(r) be the successor of r that is divisible by q. Then r -> s*(r) is an edge of G_Q, s*(r) is a
q-node, and s* permutes the q-nodes.

*Proof of Lemma S.* The successors of r are the residues s with s = r/q (mod Q/q); since Q is
squarefree, gcd(q, Q/q) = 1, so by CRT exactly one successor has s = 0 (mod q). For a prime
p != q of Q, s*(r) = r q^{-1} (mod p), which is 0 iff r = 0 (mod p). So S(s*(r)) = S(r), hence
q(s*(r)) = q(r) = q. The map is injective: r mod p = q s*(r) mod p for p != q, and r = 0 mod q.
An injective self-map of a finite set is a permutation. ∎

*Proof of Theorem S.* Let C be a cycle with U > W in an SCC Σ. If C has no division, Σ contains
a division-free cycle. Otherwise C has a division node; units have w = 1, so that node is a
q-node r for some q. By Lemma S the orbit of r under s* is a closed walk Z through r using only
n -> n/q edges, with multiplier q^{-|Z|} < 1. So Z != C (C expands), both are cycles of Σ through
r, and Σ is not a single simple cycle. Since Σ contains the expanding cycle C, it is of type
(c). ∎

*Wording (revision after REFEREE1).* "No type-(b) SCC" in the statement means: no type-(b)
SCC that contains a division node. A division-free single cycle with U > 1 (for example a unit
self-loop 1 -> 7n at Q = 6) is (b) and (z) at the same time by the §0 words, and (z) takes
precedence; it is covered by the alternative "contains a division-free cycle" and makes the
class residue diverge (Proposition Z). Theorem H' never applies to a graph with such an SCC.

Scope. Theorem S is a statement at level Q. For Q prime it transfers to all levels (Corollary
P'). For composite squarefree Q (div23_5n1 at Q = 6, div235_7n1 at Q = 30, div23_7n1) level
independence of type (c) is not proved; the harness finds type (c) at every level up to 600
for the three census maps (EVIDENCE). The hypothesis "no division on units" is needed. With
general branches, type (b) does occur at Q = 6, 10 and 15: the Q = 6 and Q = 10 tables of
`check_theory.py` part 4, and the Q = 15 table E15 below (also in part 4).

*Revision after REFEREE1.* The first version claimed an example at Q = 15 that was nowhere in
the folder (the referee's 400,000-member random search found none). The claim is now backed by
this explicit table.

**Example E15 (type (b) at the squarefree modulus 15, general branches). PROVED.** On classes
mod 15: n = r (mod 15) with 3 | r -> (n + (15 - r) mod 15)/5 (so 0 -> n/5, 3 -> (n+12)/5,
6 -> (n+9)/5, 9 -> (n+6)/5, 12 -> (n+3)/5); n = 1 -> (7n - 1)/3; n = 2 -> n + 14; every other
r -> n + 15 - r. (H1), (H2), (P) hold. Every positive orbit reaches the fixed point 3, the
only cycle.

*Proof.* G_15: a node with w = 5 has the 5 successors y0 + 3j; for r ∈ R = {0, 3, 6, 9, 12},
y0 = (r + (15 - r) mod 15)/5 is 0 or 3, so the successors are exactly R. Node 1 has w = 3 and
y0 = 2, so its successors are 2, 7, 12. Node 2 -> 1. Every other node r goes to 0. So the SCCs
with an internal edge are R (strongly connected, every cycle has multiplier 5^{-k}: type (a))
and {1, 2} (the single cycle 1 -> 2 -> 1, multiplier 7/3: type (b), and (D) holds with p = 3).
7 and the other nodes are transient into R; nothing reaches 1 except 2, and nothing outside
{1, 2} reaches 2. The lap map of {1, 2} from class 1 is x -> (7x - 1)/3 + 14 = (7x + 41)/3,
with fixed point x* = -41/4, not an integer, so by Theorem H' no orbit stays in {1, 2}. In R,
T(n) = (n + 15 - r)/5 < n whenever 4n > 15 - r, i.e. for every n >= 4 in R; and n = 3 is
fixed. So every orbit in R falls to 3, which is the only cycle. ∎

**Proposition 4 (modulus 4). PROVED (corrected after REFEREE1).** Let Q = 4, even classes
n -> n/2, odd classes (u, v, 1) with u odd. Suppose G_4 has no division-free cycle (this holds,
for example, when both odd classes have odd v). Then no SCC of G_4 is of type (b), and by
the going-up argument after Corollary P' none is at any level 2^k. Without the hypothesis, G_4 can have a type-(b) SCC, but only
next to a division-free cycle, and then Theorem H' does not apply either (it requires every SCC
to be (a) or (b)). In both cases the whole split family SPLIT(a, b, d) (and par_*, split5_*,
desc_split7_1, all with odd v) is outside the reach of Theorem H.

*Withdrawn statement.* The first version had no hypothesis and claimed "no type (b)" for every
such table. That is WRONG. Referee 1's counterexample: even n -> n/2; n = 1 (mod 4) -> 3n + 2;
n = 3 (mod 4) -> 3n + 1. Here 1 -> 1 is a division-free loop (multiplier 3, so the class
1 mod 4 diverges by Proposition Z), 3 -> 2 and 2 -> {1, 3}, but 1 never returns to 2; so {2, 3}
is the single cycle 2 -> 3 -> 2 with multiplier 3/2, a type-(b) SCC. The old proof's step
"both 1 and 3 return to 2" fails there. Every census application (split family with odd v,
split5_1, split5_3, desc_split7_1, par_*) satisfies the hypothesis, so no census conclusion
changes. `check_theory.py` part 2 checks the corrected statement on all 16 successor patterns
and asserts that the counterexample is (b) next to (z).

*Proof.* Edges: 0 -> {0, 2}, 2 -> {1, 3}, and 1, 3 each have one successor t1, t3 mod 4.
Because there is no division-free cycle, the path from an odd node along odd nodes cannot
repeat, so within two steps it reaches an even node; from 0 the edge 0 -> 2 leads to 2. Hence
both 1 and 3 reach 2. An expanding cycle passes through an odd node (a cycle of even nodes
only divides), and from an odd node every path to an odd node again goes through 2 or stays on
odd nodes, which it cannot do forever; so the cycle passes through 2. Both 1 and 3 are
successors of 2 and both reach 2, so both lie in the SCC Σ of 2. Then 2 has two internal
out-edges in Σ (to 1 and to 3), whereas every node of a single-cycle SCC has exactly one. So Σ
is not a single simple cycle. ∎

*Every level.* A division-free cycle at level 2^k projects to one at level 4, so the hypothesis
holds at every level. An expanding cycle at level 2^k projects to an expanding cycle of G_4,
which lies in a type-(c) SCC by the proof above; the going-up argument after Corollary P'
(base level K0 = 4, added after REFEREE2) then gives a second closed walk through the lifted
cycle, so there is no type (b) at level 2^k. Without the hypothesis, the division-free cycle of G_4 lifts (the lifted walk of
w = 1 nodes is deterministic and stays over the cycle, so it closes up) to a division-free cycle
at every level 2^k, and Theorem H' fails at every level.

## 3. Where type (b) does occur

**Theorem B (explicit isolated expanding cycles). PROVED.**

(i) p = 2. For odd u >= 3 let B2(u) be: even n -> n/2; n = 1 (mod 8) -> n + 1;
n = 3 (mod 8) -> u(n - 3) + 6; n = 5 (mod 8) -> n + 5; n = 7 (mod 8) -> n + 3.
Then B2(u) has no descent certificate (the cycle (3 6) of positive integers expands with
multiplier u/2), and every positive orbit is eventually periodic with exactly the cycles
(1 2), (3 6), (5 10).

(ii) p an odd prime. For u > p with p ∤ u let Bp(u) be, on classes mod p^2: n = 0 (mod p) ->
n/p; n = 1 (mod p^2) -> u(n - 1) + p; every other unit n = s (mod p^2) -> n + v_s with
v_s ∈ {1, ..., p^2 - 1}, v_s = 2p - s (mod p^2). Then Bp(u) has no descent certificate (the
positive cycle (1 p) expands with multiplier u/p), and every positive orbit is eventually
periodic with exactly the cycles (1 p) and (2 2p).

Both are raw full-division tables in the sense of Theorem S, at the non-squarefree moduli 8 and
p^2. Read at every modulus p^m with m >= 2 (odd p) or m >= 3 (p = 2) they are members of the
same family there, so type (b) occurs at every prime power p^m except 2, 4 and p. (Wording
corrected after REFEREE1.)

*Prior art in this repository (added after REFEREE1).* Type (b) at prime powers was known
before this round: round 3 had acc_h9, acc_h16 and acc_h32 (`round3/accel/systems.py`, settled
by Theorem H), and round 4 (`round4/integrality/census_small.md`) found 36 type-(b) tables in
the family F3m2, also settled by Theorem H. What Theorem B adds is an explicit infinite family
with a *positive* expanding cycle for every u > p, with complete cycle lists.

*Proof of (ii).* Graph G_{p^2}: node 1 has the single successor p. Node p (branch n/p) has the
successors s = 1 (mod p): the node 1 and the units 1 + jp, j = 1..p-1. Every unit s != 1 goes to
2p (since s + v_s = 2p mod p^2, w = 1). Node 2p goes to the units = 2 (mod p). A multiple kp
with k != 0 mod p goes to the units = k (mod p); node 0 goes to the multiples of p. So the SCCs
with an internal edge are {0} (self-loop, multiplier 1/p), C = {1, p} (the single cycle
1 -> p -> 1, multiplier u/p > 1), and A = {2p} ∪ {units = 2 mod p} (every cycle alternates
w = 1, u = 1 and n/p, multiplier p^{-k}). Nothing in A or in the transient nodes reaches C:
only p leads to 1, and only 0 and 1 lead to p, and neither 0 nor p is reachable from A
(A's nodes go to 2p or to units = 2 mod p). (Sentence corrected after REFEREE1; the first
version said "only 0 and p lead to 1".) No division-free cycle exists,
because every unit goes to a multiple of p. So Theorem H' applies (Markov, (D) holds).

Cycles: in C, x* solves p x = u x + p - u, so x* = 1, and T(1) = p, T(p) = 1. In {0}: n -> n/p
decreases strictly, so there is no cycle. In A, write a unit n = 2 (mod p) as n = 2 + p q. Then
n + v_n = 2p + p^2 (floor(q/p) + [q mod p >= 2]) and the next point of A is 2 + p F(q) with
F(q) = floor(q/p) + [q mod p >= 2]. F(0) = 0 and F(q) < q for q >= 1. So the only cycle in A is
q = 0, which is (2 2p). Positivity: on the class 1 mod p^2, T(n) = u(n-1) + p >= p; on the other
units v_s >= 1. The expanding cycle C of G_{p^2} excludes every descent certificate (dichotomy
Theorem 1). ∎

*Proof of (i).* G_8: 1 -> 2, 5 -> 2, 7 -> 2, 3 -> 6 (since u·3 + 6 - 3u = 6), 2 -> {1, 5},
6 -> {3, 7}, 4 -> {2, 6}, 0 -> {0, 4}. SCCs: {0} (multiplier 1/2), {3, 6} (single cycle,
multiplier u/2 > 1; its exit 7 goes to 2, and 2 never reaches 3 or 6), {1, 2, 5} (cycles 2 -> 1
-> 2 and 2 -> 5 -> 2, multiplier 1/2 each). For n = 1 (mod 4) the return map to 1 mod 4 is
G(n) = (n + 1)/2 for n = 1 (mod 8) and (n + 5)/2 for n = 5 (mod 8). G(n) < n except at the fixed
points 1 and 5, so the cycles there are (1 2) and (5 10). In {3, 6}, x* = (6 - 3u)/(2 - u) = 3.
∎

The census has one open system blocked by a genuine expanding positive cycle: mb_pair_5_25p,
with the cycle (3 6). Theorem B shows that an expanding positive cycle is not a barrier in
itself. What blocks mb_pair_5_25p is that its cycle sits in a type-(c) component at every
level the harness tried (up to 500).

## 4. Classification of type (b) by modulus for raw full-division tables

Raw full-division tables: non-units -> n/q(r) (prime-support rule), units -> u n + v.

| modulus Q | type (b) possible? | status |
|---|---|---|
| p prime | no type (b) containing a division at level p (the division node 0 -> n/p has every residue as successor, so a single cycle through it is the contracting loop (0)); no type (b) at any level when G_p has no division-free cycle | PROVED (Proposition P + the going-up argument after Corollary P', added after REFEREE2; caveat made explicit after REFEREE1) |
| squarefree composite | no type (b) containing a division node, at level Q (a division-free (b) cycle is also (z)) | PROVED (Theorem S); other levels EVIDENCE |
| 4 | no, at any level, if G_4 has no division-free cycle (e.g. both odd v odd); otherwise (b) can occur, but only next to a (z) SCC, and Theorem H' does not apply | PROVED (Proposition 4, corrected after REFEREE1, + the going-up argument after Corollary P', added after REFEREE2) |
| p^m, m >= 2, p^m != 4 | yes, for every multiplier u > p with p ∤ u | PROVED (Theorem B) |
| mixed non-squarefree | examples found and exactly checked at Q = 12, 20, 24, 28, 36; none found at Q = 18 (15.7 million members of the M_18 family, exhaustive, plus 1.3 million random raw members), 40, 44, 45, 48, 50, 52, 54 (random samples) | examples PROVED; general case OPEN |

For general branches (units may divide too), Proposition P still holds at prime moduli, but
type (b) occurs at Q = 6, 10, 15 next to type (a) only (the Q = 6 and Q = 10 tables and E15 in
`check_theory.py` part 4, all settled by Theorem H'). At Q = 4 type (b) occurs already for a
raw table, the counterexample to the first Proposition 4, but only next to a (z) SCC
(`check_theory.py` part 2). (Corrected after REFEREE1: the first version listed Q = 15 with no
example and did not say which example verifies Q = 4.)

The multiplier side of the question: at prime powers every u > p occurs (Theorem B). Small
multipliers also work. The P5_2 scan (Q = 25, all u <= 4 < p) found 4 type-(b) members with
cycle multipliers 6/5 = 2·3/5, 9/5 and 12/5, each exactly checked and settled by Theorem H
(`out/typeb_list.jsonl`, family P5_2_u1234v12m). So the condition is on the cycle product,
not on single multipliers. A complete list of the (multiplier set, modulus) pairs for which type
(b) occurs is OPEN beyond the cases above.

## 6. Complete certificate classification of the div23 family mod 6

**Theorem C6. PROVED.** Let D6(u1, v1, u5, v5) be: 2|n -> n/2; else 3|n -> n/3;
n = 1 (mod 6) -> u1 n + v1; n = 5 (mod 6) -> u5 n + v5, with gcd(u1, 6) = gcd(u5, 6) = 1 and
(P). Put s1 = u1 + v1 mod 6 and s5 = 5 u5 + v5 mod 6. A descent certificate exists if and only
if the condition in the row (s1, s5) of `out/classify6.md` holds (36 rows; each is "never",
or a conjunction of at most three inequalities u1^a u5^b < 2^c 3^d). In particular:

* a certificate requires u1, u5 ∈ {1, 5}. So no member with a multiplier >= 7 (the 7n+1 maps)
  has one;
* u1 = u5 = 5 is certifiable exactly when (s1, s5) = (0, 0), that is v1 = 1 and v5 = 5 (mod 6).
  div23_5n1 itself has s5 = 2 and is not certifiable (known);
* when a certificate exists, every positive orbit is eventually periodic and decide.py lists the
  cycles.

*Proof.* (H1), (H2) hold with Q = 6. The graph G_6 is 0 -> {0, 3}, 2 -> {1, 4}, 4 -> {2, 5},
3 -> {1, 3, 5}, 1 -> s1, 5 -> s5, so it depends only on (s1, s5). By the dichotomy theorem
(round 3, Theorem 1) a certificate exists iff every cycle of G_6 has U < W. A closed walk's
multiplier is the product of the multipliers of the simple cycles it decomposes into, so it
suffices that every simple cycle contracts. `classify6.py` enumerates the simple cycles of the
36 graphs exactly. A cycle without a unit node contracts. A cycle through 1 or 5 has multiplier
u1^a u5^b / (2^c 3^d) with exponents read off the cycle. Division-free cycles (1 -> 1, 5 -> 5,
or 1 <-> 5) have multiplier >= 1 and exclude certificates (dichotomy Lemma 2/3). Of two
inequalities with the same (a, b), the one with the smaller divisor implies the other, so only
that one is kept. The two corollaries follow by reading the 36 rows. ∎

The check (`classify6.py check`) compares the table with decide.py on 26,887 members
(u ≤ 37, |v| ≤ 6): 0 mismatches.

New natural member: "div23 with 5n ± 1": 2|n -> n/2; else 3|n -> n/3; else 5n + 1 if
n = 1 (mod 6) and 5n - 1 if n = 5 (mod 6) (the multiple of 6 nearest to 5n). Row (0, 0); every
orbit reaches (1 6 3), k* = 4. The variant with 5n + 5 on n = 5 (mod 6) has the two cycles
(1 6 3) and (5 30 15). These are easy systems (tier 1-2). They show precisely which change to
div23_5n1's branch on 5 mod 6 makes it certifiable.

## 5. Non-Markov maps

For maps that violate (H1) (Farkas-type maps with a 3n+1 branch next to a division by 3), the
level-K graph only over-approximates, and refining K removes spurious edges. Theorem H' needs
no Markov property, so it applies. The harness re-settles 14 of the 23 round-3 mixedbase systems
(mb_s3_3, mb_s3_9, mb_s5_5, mb_s7_7, mb_t27, mb_t81, mb_t243, mb_t729, mb_f25, mb_f125, mb_s49,
mb_s343, mb_d23_30, mb_m3b_8) with all SCCs of type (a) at level 2m. That reproduces the round-3
mixed-radix engine by a different route. It does not settle mb_pair_* (type (c) at every level
tried, up to 576), farkas_s27 or farkas2005, which need the run-accelerated (pairing) argument
of round 3. It does not settle the open mb_s3_27, mb_pair_3_27m, mb_pair_5_25p either: type (c)
at every level tried. For mb_s3_27 the obstruction is visible: the 2-adic re-entry of 3x+1
survives because each 3n+1 step multiplies the 3-adic error by 3.
