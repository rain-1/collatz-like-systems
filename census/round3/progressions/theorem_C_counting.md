# Theorem C: how many members of a merging class lie in a progression

**Status: PROVED** for every system in the table (exponent certificates verified in exact
rational arithmetic by `check_counting.py`; produced by `run_counting.py` into
`counting_results.json`). The heuristic exponents in §4 are **EVIDENCE** only.

*Revision after REFEREE1:* Lemma C2 had a GAP (unbounded U-valuation) affecting 13 systems. It is
repaired in §2 by Lemma C2' (bounded valuation) and Lemma R (valuation reduction), both proved
and checked exactly; all exponents keep their values.

## 1. The ancestor tree (Lemma C1)

Let T be a p-shift map with (A1) (notation of `theorem_A_sufficiency.md`). For a p-unit z and a
non-dilation move r and h ≥ 0 such that the move r is admissible at p^h z (state and U-domain
conditions, Lemma 3 there), put

    c_{r,h}(z) = P_r(p^h z) = (p^{h+1} z − v_r)/u_r .

Then T(c) = p^h z and h dilation steps lead to z, c ≡ r (mod p^κ) is a p-unit, and z is the p-free
part of T(c). So "z is the parent of c" defines a forest on p-units: the parent is unique.
We only use children with ρ_{r,h} := p^{h+1}/u_r > 1; for z ≥ Z0 := 1000·max|v_r| one has
z < c ≤ ρ' z with ρ' = ρ(1 + 1/1000).

A *type* is a residue mod W. For a lift ζ of a type (a residue mod W·lcm(u_r)) the admissible
pairs (r, h) and the child types c mod W are determined (c ≡ (p^{h+1}ζ − v)/u mod W since W·lcm(u)
absorbs the division). A certificate consists of a set G of types, a rational σ = s/t, positive
rational weights w_τ (τ ∈ G) and rationals q_{r,h} with q^t ρ'^s ≤ 1 (so q ≤ ρ'^{-σ}; this is an
exact rational inequality) such that for every lift ζ of every type in G

    Σ_{children (r,h) of ζ with type in G} w_{type(child)} q_{r,h}  ≥  w_{type(ζ)} .     (W)

**Lemma C1.** Given a certificate, every p-unit y ≥ Z0 of type in G has at least
(min w / max w)·(R/y)^σ distinct ancestors of type in G in (R, ρ'_max R], for every R ≥ y.

*Proof.* Expand the tree from y, expanding every vertex ≤ R (children of type in G only). Vertices
are distinct integers, so the expanded part is finite. Assign to a vertex z the mass w_τ z^{-σ}.
Since c ≤ ρ' z, w_child c^{-σ} ≥ w_child q z^{-σ}, and (W) shows that the total mass of the
children of an expanded vertex is at least its own. By induction the leaves (vertices > R, whose
parent is ≤ R, hence leaves lie in (R, ρ'_max R]) carry mass ≥ w_y y^{-σ}; each leaf carries mass
< max w · R^{-σ}. ∎

## 2. Transfer to a progression (Lemmas C2', R)

*Repair note (after REFEREE1).* The first version of Lemma C2 claimed that the construction of
Theorem A, run from a tree vertex z, depends only on z modulo one fixed modulus. That is false
for vertices of unbounded U-valuation: the initial ball of Lemma 5 is
p^{h0} z (1 + ∏ ℓ^{J_ℓ} Z_ℓ), of radius ℓ^{-(J_ℓ + v_ℓ(z))}, so the number of E moves (hence the
word, α_ω, K, J) grows with v_ℓ(z) (executed by `construct.py`; REFEREE1 §3). In 13 of the 32
certificates the good-type set G contains types τ with v_ℓ(τ) ≥ v_ℓ(W), i.e. vertices of every
large valuation. The lemma is now stated for bounded valuation (C2'), and Lemma R reduces every
vertex of those 13 systems to an ancestor of bounded valuation at bounded cost. All exponents in
§3 are restored with this repair; nothing in §3 changes.

Assume the hypotheses of Theorem A. Fix a progression P = x + NZ and a merging class H with
g(x) = g(H). A vertex is *enterable* if its residue mod L2 is enterable (§4 of
`theorem_A_sufficiency.md`).

**Lemma C2' (bounded valuation).** For every V ≥ 0 there are K_V, J_V, Z_V (depending on T, P, V)
such that every enterable z ∈ H with z ≥ Z_V and v_ℓ(z) ≤ V for all ℓ ∈ U has an ancestor
n(z) ∈ P with n(z) ≤ K_V z and T^j(n(z)) = z for some j ≤ J_V.

*Proof.* Run the construction of Theorem A with y := z (z is enterable, so k0 = 0). Every choice
in it is a function of a residue of z modulo one fixed modulus W_P(V):

* h0 depends on z mod L2;
* the initial ball p^{h0} z + ∏ ℓ^{J_ℓ + v_ℓ(z)} Z_ℓ is determined by z mod ∏ ℓ^{J_ℓ + V + 1}
  (this residue determines v_ℓ(z) ≤ V and the ball), so the ball-growing words, the live options
  and the re-centrings range over a finite set;
* the BFS word in 𝒢_Q depends on residues mod L2 and mod Q;
* the propagated U-adic target, and hence the exponent h (the least admissible solution ≥ h0 of
  an exact discrete-logarithm/CRT system), depends on z mod ∏ ℓ^{S_ℓ + V + 1} and mod Q, where
  S_ℓ is the (finite) precision of the target;
* the lift (t, c, a) depends only on x and N.

So for each of the finitely many classes ω mod W_P(V) there is a fixed word, a fixed h_ω and
therefore a fixed affine map n = α_ω z + β_ω with α_ω > 0. Take Z_V so large that all
intermediate values are positive and ≥ c for every ω (the replay step of the construction),
K_V = max α_ω + 1, J_V = max total length. ∎

**Lemma R (valuation reduction; for U = {ℓ}).** Suppose U = {ℓ} and that for every p-unit
state σ ∈ Σ there are h_σ ≥ 0 and a non-dilation move r_σ with

    v_{r} > 0,    u_{r} | v_{r},    p^{h_σ} σ ≡ B_{r}(r) (mod p^{κ−1})          (R)

(the last condition is the state condition of Lemma 3 at p^{h_σ} σ). Put
V_R = max_σ v_ℓ(v_{r_σ}). Then every p-unit z of state σ with v_ℓ(z) > V_R has the ancestor

    c = (p^{h+1} z − v_r)/u_r      (h = h_σ, r = r_σ)

with T(c) = p^h z (so T^{h+1}(c) = z), c a p-unit, v_ℓ(c) = v_ℓ(v_r) − v_ℓ(u_r) ≤ V_R, and
0 < c ≤ p^{h+1} z once p^{h+1} z > v_r.

*Proof.* The state of p^h z is p^h σ mod p^{κ−1}, so the state condition holds. Since U = {ℓ},
u_r is a power of ℓ, and v_ℓ(u_r) ≤ v_ℓ(v_r) ≤ V_R < v_ℓ(z); hence u_r divides p^{h+1} z and v_r,
so the U-domain condition u_r | p^{h+1} z − v_r holds. By Lemma 3 of Theorem A, c is an integer
with T(c) = p^h z and c ≡ r (mod p^κ), so c is a p-unit (r ≢ 0 mod p); h dilation steps lead
to z. Because v_ℓ(p^{h+1} z) = v_ℓ(z) > v_ℓ(v_r), v_ℓ(p^{h+1}z − v_r) = v_ℓ(v_r), so
v_ℓ(c) = v_ℓ(v_r) − v_ℓ(u_r). Finally v_r > 0 and u_r ≥ 1 give c < p^{h+1} z / u_r ≤ p^{h+1} z,
and c > 0 when p^{h+1} z > v_r. ∎

Condition (R) is a finite check. `check_counting.py` verifies it exactly for every p-unit state
of the 13 affected systems, with h_max = max h_σ ≤ 4 and V_R ≤ 1:

| systems | ℓ | (h, r, u_r, v_r) per p-unit state | V_R |
|---|---|---|---|
| m3_a, desc_m3_4n5 | 2 | (0, 2, 2, 2) | 1 |
| split_5/13/73/97/7081 | 3 | (1, 3, 1, d) | 0 |
| splitB_7, splitB_71 | 3 | (1, 1, 1, d) | 0 |
| split5_1, desc_split7_1 | 5, 7 | (1, 3, 1, 1) | 0 |
| desc_s32_d65, desc_s32_plus9 | 3 | an I move with h ∈ {0, 1, 4} (table printed by the check) | 0 |

For m3_a this is c = (3z − 2)/2 for 4 | z, which is odd. The check also verifies that in these
13 systems **every** residue mod L2 is enterable, so every ancestor c is enterable. Wide
randomized tests (vertices with v_ℓ(z) up to 59) confirm the conclusion of Lemma R, and the
construction executed from c = R(z) has a bounded number of IA ball words as v_ℓ(z) grows
(illustration, three systems).

**Theorem C.** Assume the hypotheses of Theorem A, that the invariant g is state-free (a function
of n mod d* alone), a certificate (W, G, σ, w) as in Lemma C1
with W a multiple of L2 coprime to the invariant modulus d* and G consisting of enterable types,
and either
(a) *bounded case:* v_ℓ(τ) < v_ℓ(W) for every τ ∈ G and ℓ ∈ U (or U = ∅), or
(b) *R case:* U = {ℓ}, condition (R) holds for every p-unit state, and every residue mod L2 is
enterable.
Then for every merging class H and every progression P = x + NZ with g(x) = g(H),

    #(H ∩ P ∩ [1, X]) ≥ c(H, P) X^σ     for all large X.

*Proof.* H contains a vertex of type in G: the progression τ + WZ, τ ∈ G, meets every invariant
class because g is state-free and W is coprime to d*, so Theorem A puts an element of H in it (it is a p-unit since
p | W and τ is a p-unit). Choose such a
y ∈ H, y ≥ Z0. By Lemma C1, for every R ≥ y there are ≥ c_1 (R/y)^σ leaves z ∈ (R, ρ'_max R], all
of type in G, all in H (ancestors of y).

To each leaf z assign a vertex c(z) of bounded valuation:
in case (a), c(z) = z, which has v_ℓ(z) = v_ℓ(type) ≤ V := max_{τ,ℓ} v_ℓ(τ) and is enterable
(its type is); in case (b), c(z) = z if v_ℓ(z) ≤ V_R, and otherwise the ancestor of Lemma R, so
v_ℓ(c(z)) ≤ V := V_R, c(z) is enterable (every residue is), T^{h+1}(c(z)) = z with h ≤ h_max,
and c(z) ≤ p^{h_max+1} z. In both cases c(z) ∈ H, c(z) → ∞ with z (c ≥ (pz − v_r)/u_r), and
T^i(c(z)) = z for some i ≤ h_max + 1 (i = 0 in case (a)).

Apply Lemma C2' with this V to c(z) (z large enough that c(z) ≥ Z_V): n(z) := n(c(z)) ∈ P ∩ H
with n(z) ≤ K_V c(z) ≤ K_V p^{h_max+1} z and T^{j}(n(z)) = z with j ≤ J_V + h_max + 1. Take
R = X/(K_V p^{h_max+1} ρ'_max); then n(z) ≤ X. A given n equals n(z) for at most J_V + h_max + 2
leaves z (each such z is one of its first J_V + h_max + 1 iterates). Hence
#(H ∩ P ∩ [1, X]) ≥ c_1 (R/y)^σ /(J_V + h_max + 2) ≫ X^σ. ∎

State-freeness of g and gcd(W, d*) = 1 are asserted for all 32 systems by
`check_theorem_C_hypotheses.py` (added after REFEREE2; the first version of the statement omitted
the state-free hypothesis, which the first step of the proof uses).
`check_counting.py` decides for each of the 32 certificates which case applies: 19 are in case
(a) (bounded G, or U = ∅) and 13 in case (b). So every σ in §3 is PROVED.

## 3. Results (σ from `counting_results.json`; "uniform": all weights 1; "weighted": type weights)

W = p^κ · L2 (types modulo W), children with h ≤ 16 (30 for 7x+1, 9x+1).

| system | σ uniform | σ weighted |
|---|---|---|
| m3_a (= m3_c) | 0.997 | 0.997 |
| qrB7_c53, par_1_5 | 0.998 | 0.998 |
| split_5, split_13, split_73, split_97, split_7081, splitB_7, splitB_71 | 0.692 | 0.974 |
| desc_s32_d65 | 0.399 | 0.772 |
| desc_s32_plus9 | 0.399 | 0.728 |
| desc_split7_1 | 0.692 | 0.821 |
| split5_1 | 0.692 | 0.692 |
| split5_3 | 0.155 | **0.420** |
| 3x+d (d = 1, −1, 5, 7, 13, 17) | 0.320 | 0.410 |
| 5x+d (d = 1, 3, 7, 11) | 0.103 | 0.198 |
| 7x+1 | 0.106 | 0.150 |
| 9x+1 | 0.067 | 0.115 |
| m3_b | 0.336 | 0.365 |
| m3_d | 0.154 | 0.308 |
| m3_e | 0.134 | 0.202 |
| m3_g | 0.184 | 0.278 |
| desc_m3_4n5 | 0.336 | 0.578 |

(Every row: certificate verified exactly. Rows m3_a, the split_d/splitB_d rows, desc_s32_d65,
desc_s32_plus9, desc_split7_1, split5_1 and desc_m3_4n5 use case (b) of Theorem C (Lemma R);
all other rows use case (a). REFEREE1 also re-certified four of them with G restricted to
bounded-valuation types, which gives smaller values (m3_a 0.377, split_5 0.878, split5_1 0.674,
desc_m3_4n5 0.546); Lemma R makes that restriction unnecessary.)

**Worked improvement.** For split5_3, `../../round2/rewriting/split5_3_components.md` Theorem 3
proves σ = 0.2383 (root of 4^{-σ} + (1024/5)^{-σ} = 1). The type-weighted certificate modulo
W = 100 proves σ = 21/50 = 0.42 for every merging class and every compatible progression.

**Pushing σ toward 1.** (PROVED) For m3_a the children of a 3-unit z are (3^{h+1} z − v)/2 for
every h ≥ 0 (exactly one of v = 1, 2 is admissible for each h, by parity) and all are 3-units; so
with H children Σ_{h<H} (3^{h+1}/2)^{-σ} ≥ 1 holds for σ = σ_H with σ_H → 1 (at σ = 1 the infinite
sum is exactly 1). Here no factor (1 + ε) is needed in ρ': since v ∈ {1, 2} is positive,
c = (3^{h+1}z − v)/2 < (3^{h+1}/2) z exactly, so Lemma C1 holds with ρ' = ρ for all z ≥ 1 (the
stored certificate σ = 99/100 uses ρ(1 + 1/1000) and is verified as is). m3_a is in case (b) of
Theorem C (Lemma R with c = (3z − 2)/2). Hence for m3_a: for every ε > 0, every merging class has ≫ X^{1−ε} members in
every progression — both basins (of 1 and of 2) are "almost full" in every progression, matching
their observed positive densities (≈0.70 and ≈0.30 below 2·10^4). The same argument gives σ → 1
for par_1_5 and qrB7_c53 (all children isometric). For maps with an expanding branch the worst
case of the U-domain condition (one admissible h per period) caps the uniform method.

## 4. When can σ reach 1? (EVIDENCE / heuristic)

For a parity map ax+1 treat the inverse tree as a branching random walk in log scale: z has the
child 2z (dilation) always and the child (2z − 1)/a with probability 1/a. The growth exponent of
the number of tree vertices below X is the smaller root γ of 2^{-γ} + (1/a)(a/2)^{γ} = 1 when this
equation has a root in (0, 1), and 1 otherwise:

| a | heuristic γ |
|---|---|
| 3 | 1 (no root below 1: the "Collatz" case) |
| 5 | 0.6509 |
| 7 | 0.3735 |
| 9 | 0.2581 |

So for 3x+1-type maps (negative drift) one expects merging classes of positive density and σ can
in principle be pushed toward 1 (Krasikov–Lagarias difference inequalities do this for 3x+1; we do
not quote their constants — not checked against the primary source); for 5x+1, 7x+1, 9x+1 no
lower bound can exceed γ < 1 if the heuristic is right, because merging classes are then
genuinely sparse. Numerically the 5x+1 basin of 1 has 256 members below 10^4 and 982 below 10^5
(log-slope 0.584; most starts are unresolved within 3000 steps), consistent with γ ≈ 0.65 and with
our proved σ = 0.198.

## Novelty

For 3x+1 the qualitative statement (every arithmetic progression is sufficient) is
K. M. Monks, *The sufficiency of arithmetic progressions for the 3x+1 Conjecture*, Proc. AMS 134
(2006) 2861–2872 (as cited in the introduction of arXiv:1204.3904; the PAMS article itself was
not read here, so no quantitative statement from it is quoted). Tree counting of this kind is classical for 3x+1 (Krasikov 1989, Applegate–Lagarias,
Krasikov–Lagarias; not re-read here, so no constants quoted). The generic exact certificate for
p-shift maps, the transfer to progressions with the merging-class invariant, and the numbers in
the table: novelty not checked.
