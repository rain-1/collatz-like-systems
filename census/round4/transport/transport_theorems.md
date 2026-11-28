# Transport of proof between table maps: what it can and cannot do

Lens "transport", round 4. Check: `check_transport.py` (exits 0). Labels: PROVED / EVIDENCE /
OPEN. "Novelty: not checked" applies to everything here unless said otherwise.

## 0. Setting

A *table map* T is a modulus Q and triples (u_r, v_r, w_r), r mod Q, acting by
T(n) = (u_r n + v_r)/w_r on n ≡ r (mod Q), with u_r ≥ 1, w_r ≥ 1, exact division on the whole
class, and T(N+) ⊆ N+. Multipliers need not be units; Q is arbitrary. A table is *unit p-adic*
if Q = p^m, w_r is a power of p and p ∤ u_r (the setting of `round3/accel/trichotomy.md`).

For a class X = {n ≥ 1 : n ≡ r_X (mod M_X)} (0 ≤ r_X < M_X) put h_X(z) = M_X z + r_X and
D_X = {z ≥ 0 : h_X(z) ≥ 1}. The *first return* is R_T^X(n) = T^{τ(n)}(n) with
τ(n) = min{t ≥ 1 : T^t(n) ∈ X}. It is *bounded* if τ ≤ τ_max on X. The *normal form* is
G_T^X = h_X^{-1} ∘ R_T^X ∘ h_X, a map on D_X.

**Lemma P (pieces). PROVED.** If R_T^X is bounded, then there is a modulus L and, for each class
c mod L, integers (A, B, D) such that G_T^X(z) = (A z + B)/D for every integer z ≡ c (mod L) with
h_X(z) ≥ 1. The *canonical form* of G_T^X is the least such L with its formulas.

*Proof.* `transport_lib.first_return` refines a class n ≡ c (mod Mod) until (i) the branch of T at
the current iterate F(n) = (a n + b)/d is constant on it, which holds iff Q divides the increment
a·Mod/d, and (ii) membership of F(n) in X is constant, iff M_X divides a·Mod/d. Then one step of T
is one affine formula on the whole class. The recursion stops on every class at the first return
(bounded by hypothesis), and the classes produced partition the start class. Conjugating by h_X
and merging classes with equal formulas gives the canonical form. ∎

Two systems are related by a **transport identity** when G_A^X and G_B^Y have the same canonical
form. Such an identity is a finite exact fact: two affine formulas that are equal as formulas
agree on every integer of the class. `check_transport.py` re-derives every identity used below
with a second, independent symbolic iterator.

## 1. Transport of GLOBAL

**Lemma S (sufficient classes). PROVED.** Let d be a prime with T(dn) = n for all n (a
*dilation*), if one exists. Let G ⊆ Z/M_X be the set of c with d^j c ≡ r_X (mod M_X) for some
j ≥ 0 (G = {r_X} if there is no dilation). Let M = lcm(Q, M_X, all w_r), and let Γ be the graph on
Z/M with an edge x → y whenever y ≡ T(x) (mod gcd(u_x M/w_x, M)). Suppose every strongly
connected component with an internal edge of Γ restricted to {x : x mod M_X ∉ G} is either
(i) *pure dilation*: every vertex has the branch n ↦ n/d, or (ii) *contracting*: every closed
walk in it has ∏u/∏w < 1. Then every positive orbit either is eventually periodic inside such a
contracting component, or meets a point c with c mod M_X ∈ G; in the second case d^j c ∈ X for
some j and T^j(d^j c) = c, so the orbit merges with an orbit starting in X.

*Proof.* T(x + Mt) = T(x) + (u M/w) t, so the residues mod M of an orbit form a walk in Γ. If the
orbit never meets G, the walk stays in the restricted graph and from some time on inside one of
its components. In a pure-dilation component, n would be divided by d forever, impossible for a
positive integer. In a contracting component, the potential of `dichotomy.md` Lemma 4 (its proof
uses only that every cycle of a finite graph has product < 1) gives c(x) > 0 with
c(y)u_x < c(x)w_x on every internal edge. With V(n) = c(n mod M)·n we get V(Tn) ≤ θV(n) + β with
θ < 1, so the orbit is bounded and eventually periodic. ∎

`transport_lib.sufficient` checks the hypothesis exactly (cycles of product exactly 1 are
excluded by inflating every multiplier by 1001/1000 before an exact Bellman-Ford; this can only
reject).

**Theorem E (transport). PROVED.** Let R_A^X and R_B^Y be bounded with G_A^X = G_B^Y =: G.

1. For z ∈ D_X ∩ D_Y, the A-orbit of h_X(z) is eventually periodic iff the B-orbit of h_Y(z) is.
2. Every A-orbit starting in X is eventually periodic iff every B-orbit starting in Y is.
3. If (A, X) and (B, Y) both satisfy Lemma S, then GLOBAL(A) ⇔ GLOBAL(B). If only (B, Y)
   does, then GLOBAL(A) ⇒ GLOBAL(B).
4. The A-cycles that meet X and the B-cycles that meet Y are both in bijection with the G-cycles
   in D_X, respectively D_Y, with equal multipliers ∏u/∏w. D_X and D_Y differ at most in the
   point z = 0, and only the G-cycle {0} (when G(0) = 0) can be unmatched.

*Proof.* (1) The A-orbit of n ∈ X is the R_A-orbit of n with gaps of at most τ_max steps, so it
is eventually periodic iff the R_A-orbit takes finitely many values; and h_X carries R_A-orbits
to G-orbits. The same holds for B. (2) D_X ⊆ {z ≥ 0} and G maps D_X into D_X. If D_Y = D_X ∪ {0},
then G(0) is either 0 (a fixed point) or a point of D_X, so the orbit of 0 is eventually periodic
whenever all orbits in D_X are. (3) Under Lemma S every orbit merges with an orbit from X or is
eventually periodic, and merging preserves eventual periodicity. (4) A cycle meeting X is one
R_A-cycle (its X-points in order), and the multiplier of one lap of R_A is the product over the
whole A-cycle. h_X is affine, so G has the same multiplier. ∎

## 2. Positive results of the search

**Proposition C (a normal form of 3x+1). PROVED.** Let C(n) = n/2 (n even), 3n+1 (n odd). On
the class n ≡ 2 (mod 3), with n = 3z + 2, the first return of C is bounded (≤ 3 steps) and

    G(z) = (3z+1)/2  (z odd),   3z/4  (z ≡ 0 mod 4),   (z−2)/4  (z ≡ 2 mod 4).

Equivalently, with y = z + 1 = (n+1)/3,

    G'(y) = 3y/2  (y even),   (3y+1)/4  (y ≡ 1 mod 4),   (y+1)/4  (y ≡ 3 mod 4).

Every positive C-orbit is eventually periodic iff every positive G'-orbit is. The C-cycles
meeting 2 (mod 3) correspond to the G'-cycles, and every C-cycle meets 2 (mod 3) (reason below;
corrected after REFEREE1); the trivial cycle (1 4 2) is the fixed point y = 1.

*Proof.* z odd: n odd, 3n+1 = 9z+7 is even, (9z+7)/2 ≡ 2 (mod 3), and its z-value is (3z+1)/2.
z ≡ 0 (mod 4): n/2 = 3(z/2)+1 is odd and ≡ 1 (mod 3); 3·that+1 = 9z/2+4 ≡ 1; halving gives
9z/4+2 ≡ 2 (mod 3), z-value 3z/4. z ≡ 2 (mod 4): n/2 = 3(z/2)+1 is even and ≡ 1; halving gives
(3z+2)/4 ≡ 2 (mod 3), z-value (z−2)/4. The intermediate values are ≢ 2 (mod 3), so these are
first returns. Lemma S holds for (C, 2 mod 3): the dilation is d = 2, G = {1, 2} mod 3, and the
only component outside it is the halving loop on 0 mod 3 (pure dilation). Theorem E. 

*Every C-cycle meets 2 (mod 3).* (The first version cited "Lemma S and bounded return" for this.
That was a wrong justification, as REFEREE1 pointed out: Lemma S only gives a point c with
c mod 3 ∈ {1, 2}, and for c ≡ 1 it says 2^j c ∈ X, which need not lie on the cycle. The correct
argument follows.) If n ≡ 0 (mod 3), then n/2 ≡ 0 (mod 3) is smaller when n is even, and
3n+1 ≡ 1 (mod 3) when n is odd; a cycle cannot consist of halvings only, so every cycle has a
point ≡ 1 or 2 (mod 3). If n ≡ 1 (mod 3) is even, then n ≡ 4 (mod 6) and n/2 ≡ 2 (mod 3). If
n ≡ 1 (mod 3) is odd, then n ≡ 1 (mod 6), 3n+1 ≡ 4 (mod 18), and the next step (3n+1)/2 ≡ 2
(mod 3). So every cycle point ≡ 1 (mod 3) is followed within two steps by a point ≡ 2 (mod 3)
of the same cycle. (`check_transport.py` part B2 checks these residue facts symbolically.) ∎

G' is a unit 2-adic table of type (c) (`unit_type` reports the self-loop 0 → 0 of multiplier
3/2 in the 4-node component {0, 1, 2, 3} mod 4; another expanding cycle in it is 2 → 1 → 2,
multiplier 9/8), and decide.py says OBST, as Theorem O2 below predicts. *Remark (interpretation,
not a proved statement):* its branch on even y is the "dressing" branch 3y/2 of
`accel/dressing.md`, but without any division by 3; the factors of 3 it creates are never
removed, and this seems to be why it stays a Collatz-hard map. Compare core W of
`accel/sfamily_obst.md` (z odd → (3z+1)/2, z ≡ 2 (4) → z/2, z ≡ 0 (4) → 3z/4, expected
divergent): G differs from W only on z ≡ 2 (mod 4), where W halves and G divides by 4.

**Theorem F (four more S-family members are exactly 3x+1). PROVED.** Let T_S be the S-family map
(even n → n/2; odd n → 3n+1 if n mod 16 ∈ S, else n+1) with S ∩ {3, 7, 11, 15} = {3, 7, 15} and
S ∩ {5, 13} = ∅ (so S = {3,7,15} ∪ S₀ with S₀ ⊆ {1, 9}: four sets). On X = {n ≡ 3 (mod 4)},
n = 4z + 3, the first return of T_S is bounded and equals G of Proposition C. Hence GLOBAL(T_S)
⇔ the 3x+1 conjecture (no divergent orbit) for these four sets, and the cycles correspond as in
Theorem E. All four are OBST and of type (c) (exact), and they are not the Corollary-C sets of
round 3 (which are S ⊇ {3,7,11,15}).

*Proof.* z odd: n ≡ 7, 15 (mod 16) ∈ S, 3n+1 = 12z+10, half 6z+5 ≡ 3 (mod 4): z-value (3z+1)/2.
z ≡ 0 (mod 4): n ≡ 3 (mod 16) ∈ S, 6z+5 ≡ 5 or 13 (mod 16) ∉ S, n+1 → 6z+6, half 3z+3 ≡ 3
(mod 4): z-value 3z/4. z ≡ 2 (mod 4): n ≡ 11 (mod 16) ∉ S, n+1 = 4z+4, two halvings give
z+1 ≡ 3 (mod 4): z-value (z−2)/4. Lemma S for (T_S, X): the dilation is 2, G = {3} mod 4; outside
it the only component with an internal edge is {1, 2} (S₀ ∌ 1) or {1, 2, 4} (1 ∈ S₀) mod 16,
which carries the cycle (1 2), multiplier 1/2, or (1 4 2), multiplier 3/4, and is contracting;
the rest is acyclic or pure dilation (checked exactly). Theorem E with Proposition C. ∎

Concretely: the T_S-orbits that never meet 3 (mod 4) are exactly those ending in (1 2) or
(1 4 2). Every other orbit is a 3x+1 orbit in disguise (n = 4z+3 ↔ 3z+2).

**Equivalence classes in the S-family (PROVED for every listed join; counts are exact for the
searched transport class, which includes the search cut-offs below).** `equiv.py` joins two
systems when an identity of Theorem E holds with Lemma S on both sides. Over all
2 + 16 + 256 + 65536 S-family tables with m ≤ 5, using single classes with
M ∈ {2,…,10, 12, 16, 18, 24, 27, 32} (library and m ≤ 4) and a light list (M ∈ {2, 3, 4, 6, 8, 9})
for m = 5, and with the search cut-offs of `equiv.py`: first-return time at most tmax = 24,
at most pmax = 20000 pieces, canonical modulus at most Lmax = 4096. A first return that exceeds
any of these cut-offs is treated as absent, so an identity that needs a longer return, more
pieces or a larger canonical modulus is not excluded by these counts (added after REFEREE1):

| population | distinct tables | nontrivial classes | members | type mix |
|---|---|---|---|---|
| library (census open + round-3 settled) | 83 | 3 | 8 | all type (c) |
| + S-family m = 4 | 328 | 3 | 12 | all type (c) |
| + S-family m = 5 | 65607 | 42 | 264 | all type (c) |

The Collatz class grows from {3x+1, 3n+3, 3n+9, sf3_37} to 20 members (the 4 of Theorem F and
12 at m = 5). The other 39 classes at m = 5 join members that differ only on classes inside a
contracting part (the 1 mod 8 classes, which the first return skips). This shrinks the family
but does not touch the 8 small cores: **no identity in the searched class joins two of the 8
cores of `accel/sfamily_obst.md`, or a core with 3x+1. PROVED as a finite statement for this
class, stated precisely (corrected after REFEREE1):** on single classes M ≤ 32, the 9 maps
have 34 first returns that come back within 24 steps (43 canonical maps counting the 9 maps
themselves), the count is still 34 with the time bound raised to 64 and the piece cap to 60000,
and these canonical maps are pairwise distinct between different systems (`check_transport.py`
parts F, F2). On the 2-power classes M = 2^s ≤ 32 the boundedness of the return is decided
exactly (part F2: the return to X = r mod 2^s is unbounded iff the residue graph at modulus
2^max(m, s) has a walk from an X-vertex into an infinite non-X walk, by Lemma 1 of
`dichotomy.md`; 16 bounded returns there), so on 2-power classes the statement is complete. On
classes with an odd factor a return that needs more than 64 steps is not excluded. Hence the
list of 8 cores is not shortened by this method.

No class mixes a CERT member with an OBST member, and no class contains a settled system of any
kind. (Corrected after REFEREE1; the first version said "this is forced by the theorems below",
which is overstated.) For CERT members and other plain-certificate systems it is forced by
Theorem O1. For Theorem-H systems it is forced by Theorem O2 only through p-adic classes; the
search set also contains classes mod 3, 5, 6, 7, 9, … for the 2-adic Theorem-H systems acc_h16
and acc_h32, where O2 says nothing (§5 lists this as OPEN). For the dressed, mixed and divergent
library systems no theorem here excludes a join. For those cases the statement is an observed
outcome of the search, not a consequence of the theorems.

## 3. Why transport cannot reach a settled system (the wall, extended)

**Lemma B (bounded excursions). PROVED.** Let B be a table map with a plain descent
certificate at some modulus M: B^{j(r)}(n) < n for n ≡ r (mod M), n > N₀, J = max j. Let
Λ = max u_r/w_r and K = max |v_r|. Then for every n ≥ 1, every value of the B-orbit of n is at
most (Λ + K)^J · max(n, ΛN₀ + K).

*Proof.* B(x) ≤ (Λ + K)x for x ≥ 1. While the current value x exceeds N₀, the orbit returns
below x within J steps and does not exceed (Λ+K)^J x in between; so the successive values at the
descents decrease. A value ≤ N₀ is followed by a value ≤ ΛN₀ + K, after which the same argument
applies. ∎

**Lemma R (realised growth). PROVED.** Let A be a unit p-adic table at modulus p^m and X a class
mod p^s q with p ∤ q. Suppose the residue graph G_K (K ≥ max(m, s)) has a walk P from a class
≡ r_X (mod p^s) to a vertex of a cycle C with multiplier λ_C > 1. Then for every d there is an
infinite progression of positive integers n ∈ X on which A^{|P|+d|C|}(n) = λ_P λ_C^d n + β_d.
So sup_t A^t(n)/n is unbounded on X.

*Proof.* Lemma 1 of `dichotomy.md` realises the walk P C^d by a progression a + p^E t; intersect
with n ≡ r_X (mod q) by CRT (p ∤ q); take n large. ∎

**Theorem O1 (no transport from certificate-settled systems). PROVED.** Let A, X be as in Lemma R
(in particular A is OBST; every type-(c) system qualifies with X = all integers, and with any X
whose p-part reaches the expanding cycle). Let B be any table map (any modulus, unit or not,
mixed or not) and h(z) = αz + β with α > 0. If, for some L, every A-orbit starting in X has, in
every window of L consecutive times, a value of the form h(b) with b in the B-orbit of
h^{-1}(start), then B has no plain descent certificate at any modulus.

This covers every identity of Theorem E in both directions (bounded returns give L = τ_max), and
every case where A is an induced map of B (L = 1: every A-value is a B-value).

*Proof.* By Lemma R, for every d there are arbitrarily large n ∈ X with
A^{t_d}(n) = λ_P λ_C^d n + β_d at the fixed time t_d = |P| + d|C|. (The first version spoke of
"a time of maximum", which need not exist if the orbit is unbounded; REFEREE1 suggested the fixed
time t_d, which only helps.) Within L steps after t_d there is a sampled value h(b) with b in the
B-orbit of z = h^{-1}(n). One step of A satisfies A(x) ≥ μx − K' (μ = min u_r/w_r, K' a constant),
so h(b) ≥ min(μ, 1)^L λ_P λ_C^d n − c_d with c_d depending on d but not on n. Hence
sup_b b ≥ (min(μ, 1)^L λ_P λ_C^d n − c_d − β)/α over the B-orbit of z = (n − β)/α. Lemma B bounds this
sup by C_B·max(z, N_B) with a constant C_B of B. Taking n → ∞ for fixed d gives
min(μ, 1)^L λ_P λ_C^d ≤ C_B for every d, impossible since λ_C > 1. ∎

So decide.py-CERT systems, all round-2/3 plain certificates, and the plain mixed-radix
certificates of `mixedbase` can never be the source of a transport to a unit p-adic table with an
expanding cycle reachable from X (Lemma R). Non-unit OBST targets, such as dressed maps, are not covered.

**Theorem O2 (no transport from Theorem-H systems through p-adic classes). PROVED.** Let A and B
be unit p-adic tables (same p), X and Y classes mod powers of p, R_A^X and R_B^Y bounded, and
G_A^X = G_B^Y. If A has a type-(c) component Σ in some G_K, K ≥ max(m, s), that contains a
vertex lying in X, then B has infinitely many expanding periodic orbits in Z_p; hence B is of
type (c) or critical (it has a division-free cycle). In either case B is not settled by
Theorem H or by a generalized certificate (Theorem N for type (c); the translation cycle makes
B OBST in the critical case). If B satisfies the standing hypothesis of `trichotomy.md` (no
division-free cycle), B is of type (c). (Statement corrected after REFEREE1: the first version
concluded "B is of type (c)" without the standing hypothesis.)

*Proof.* All return pieces are cylinders mod powers of p and the identity is between affine
formulas, so it extends to the closures: Ĝ = ĥ_X^{-1} R̂_A ĥ_X = ĥ_Y^{-1} R̂_B ĥ_Y on Z_p.
As in the proof of Theorem N, for a vertex x of Σ in X the closed walks C^d W through x (W a
detour through x) give infinitely many distinct periodic points of Â lying in X̄, with real
multipliers λ_C^d λ_W > 1. A periodic point in X̄ returns to X̄, so it is R̂_A-periodic with the
same multiplier; then ĥ_Y ĥ_X^{-1} of it is R̂_B-periodic, hence B̂-periodic, with the same
multiplier, and distinct R̂_A-orbits give distinct B̂-orbits (the Y-points of one B̂-cycle form
one R̂_B-cycle). Finally, if B satisfies the standing hypothesis of `trichotomy.md` (no
division-free cycle; otherwise B is OBST by a translation cycle anyway), an expanding periodic
orbit follows a closed walk with multiplier > 1 in some component; in a type-(a) component every
closed walk contracts, and in a type-(b) component the only point following the cycle forever is
its periodic point. So a table with no type-(c) component has only finitely many expanding
periodic orbits. ∎

**Corollary (where a transport proof of a type-(c) system can come from).** Combining O1, O2 and
Theorem N: a transport identity of the kinds above can settle an OBST unit system A only from a
source B whose orbits have unbounded excursion ratio sup_t B^t(n)/n and which is not certified
in any of the senses above. The candidates are (i) non-unit systems settled by run-accelerated
arguments (Farkas pairing family P(a, 1, x*), P(3, 2, x*)), (ii) dressed systems
(`accel/dressing.md`), (iii) systems with proved divergent orbits, (iv) Theorem-H systems reached
through a class X that is not a p-adic cylinder (O2 does not cover mod-q classes). Item (iii)
only transports divergence.

**Search of (i), (ii) and (iv) (EVIDENCE, exact per case).** `search_nonunit.py`: for 30 pairing
and dressed systems and all classes Y with M_Y = 2^i 3^j 5^k 7^l ≤ 144 (117,390 pairs), only 31
first returns are bounded and none is a unit p-adic table. All 31 are returns to the class
0 (mod M_Y). (Corrected after REFEREE1: the first version called all 31 "the scaling symmetries
x*Z (P2 of `pairing_family.md`)". That holds for the 24 returns of pairing systems; the other 7
are returns of dressed systems to qZ, still non-unit tables but not P2 symmetries; list in
`results/nonunit_144_breakdown.txt`, made by `nonunit_breakdown.py`.) `check_transport.py`
part G now re-runs both M_Y ≤ 48 and M_Y ≤ 144 (the latter takes about 7 s) and checks the
24 + 7 split. `equiv.py`: the Theorem-H systems acc_h9, acc_h16, acc_h32 have no
identity with any library or S-family system on the searched classes. The obstacle is structural: in a
Farkas or dressed system the branch depends on n mod a, and a first return can forget that only
if its excursions never meet an undetermined mod-a residue, which the up-run structure (P1 of
`pairing_family.md`) prevents after one block.

## 4. Invariants

A transport identity G_A^X = G_B^Y preserves, by Theorem E(4), the multipliers of the cycles
that meet the classes, and by O2 the real multipliers of the p-adic periodic orbits that meet
them. For the 8 cores no invariant is needed: their canonical first-return maps that return within
64 steps on classes M ≤ 32 are already pairwise distinct (parts F, F2; exact boundedness on
2-power classes). Cycle multipliers alone would not separate all of them: the
known cycles of sf3_7, sf3_57 and sf3_357 are all (1 2) with multiplier 1/2.

## 5. What stayed open

* The hard criterion of this round (settle a unit type-(c) system with a convergence proof) is
  **not met**. The positive output is Proposition C and Theorem F (new members of the Collatz
  class) and 39 further joins inside the S-family; all of them connect open systems to open
  systems.
* OPEN: whether some *unbounded* first return (infinitely many affine pieces) of a pairing or
  dressed system is conjugate to a unit type-(c) table. Theorem O1 does not exclude it (these
  sources have unbounded excursions), Theorem O2 does not apply (non-unit source). This is the
  only transport door left open by this note.
* OPEN: O2 for classes X that are not p-adic cylinders (mod q with p ∤ q). The search found no
  example linking a Theorem-H system this way.

## 6. Revision after REFEREE1

REFEREE1 found no mathematical error and asked for text repairs. All of them are made; nothing
above was upgraded except where a new exact check backs it.

| item | what was wrong | what changed |
|---|---|---|
| Prop C, "every C-cycle meets 2 mod 3" | WRONG justification ("by Lemma S and bounded return" does not imply it) | replaced by the direct two-step argument; residue facts checked in part B2 |
| Prop C, multiplier | "cycle of multiplier 9/8" while `unit_type` reports the loop 0 → 0 of 3/2 | both quoted |
| Prop C, "exactly why it stays Collatz-hard" | interpretation presented as fact | marked as a remark |
| §2 counts | search cut-offs not stated | tmax = 24, pmax = 20000, Lmax = 4096 stated |
| §2 "forced by the theorems" | overstated | split into O1 (certificates), O2 (p-adic classes of Theorem-H systems), observation (the rest) |
| 8 cores | "bounded" meant "returns within 24 steps" | stated as such; part F2 re-runs at 64 steps (still 34 returns) and decides boundedness exactly on 2-power classes |
| O1 proof | "time of maximum" may not exist | fixed time t_d = |P| + d|C| |
| O2 statement | conclusion "type (c)" needed the standing hypothesis | conclusion "type (c) or critical", hypothesis stated |
| non-unit search | all 31 called P2 symmetries | 24 pairing P2 symmetries + 7 dressed returns to qZ; check now reproduces M ≤ 144 |
| `transport_lib.sufficient` | docstring said "acyclic" | docstring describes the implemented full Lemma S |
