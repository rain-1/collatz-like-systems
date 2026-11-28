# The count law beyond the digit horizon for general table maps: statements and proofs

Round 6, lens `countlaw_wide`. Agent-written; examined by two referees (REFEREE1.md, REFEREE2.md) and
revised after each (the revisions are marked **[Rev]** and listed in Section 8, and **[Rev2]**, listed in
Section 9). Labels: PROVED, EVIDENCE, OPEN.
External results used: Fekete's lemma, Raney's cyclic lemma, the method of types, the Erdős–Turán
inequality (Section 5, quoted from memory, constant not needed), the lifting-the-exponent facts, unique
factorization. **[Rev2]** (the list previously said Section 7 for Erdős–Turán and omitted Raney's lemma, the
method of types and lifting the exponent; it now matches the README). Everything else is proved here or is a finite computation done by
`check_all.py` / `cert.py` / `everyoct.py`.

## 0. Setting

**Table map.** A prime p, an exponent k >= 1, Q = p^k, and for every residue r mod Q a row
(u_r, v_r, e_r) of integers with u_r >= 1, p ∤ u_r, e_r >= 0, and p^{e_r} | u_r n + v_r for every
n ≡ r (mod Q). The map is T(n) = (u_r n + v_r)/p^{e_r} for n ≡ r. (Exactness on the whole class forces
p^{e_r} | u_r Q, so e_r <= k.)

**Hypothesis (SG), single generator.** There is an integer g >= 2 with p ∤ g and integers a_r >= 0 with
u_r = g^{a_r} for every r, and gcd of the a_r is 1. (u_r = 1 is allowed.) Put λ = log p / log g; λ is
irrational (unique factorization: g^A = p^E forces A = E = 0).

**Digit tree** (round 3 `density/theory.md` Lemma 1; round 5 `fourier` Lemma T). With s known low
digits of the current value x, the next step is *decided* if every residue mod Q congruent to x mod
p^{min(s,k)} has the same row; it is then applied and consumes e digits (the result is known mod
p^{s-e}). A node state is σ = (s, c) with c = x mod p^s after all decided steps. Reading the next digit
of the start appends one digit to x (the value's next digit is an affine image of the start's next digit,
because the multiplier is a unit) and triggers a finite chain of decided steps.
**Hypothesis (F):** every such chain is finite. **[Rev]** It fails exactly when there is a cycle of
division-free decided steps among residue classes (a closed chain of classes, each step decided by the known
digits and consuming no digit); the cycle need not have length 1. The examples in the census have length 1
(odd n -> 3n+2, odd n -> 3n), and on such a class the orbit grows without bound. (The first version said
"some class is mapped into itself", which is the length-1 case only.)

After t decided steps the slope is g^{A_t}/p^{E_t}. A residue n mod p^b *survives b digits* if every
step decided by its b digits has g^{A_t} >= p^{E_t}. R_b is the set of survivors, P(b) = |R_b|/p^b, and
N(X, b) = #{0 <= n < X : n mod p^b ∈ R_b}. For b <= m one has N(p^m, b) = p^m P(b) exactly (in-horizon
identity). The *digit horizon* of X = p^m is b = m; this file is about b > m.

The **continuation set** of a node in state σ = (s, c) with slope L = g^A/p^E >= 1 is

    S_K(σ, L) = { z mod p^K : from the value c + p^s z (s+K known digits) every decided step
                  has L * (prefix slope) >= 1 }.

It depends only on σ and L. Let g_σ(z) be the minimum prefix slope (the start, slope 1, included); then
S_K(σ, L) = {z : L g_σ(z) >= 1}, a super-level set of g_σ.

**Automaton data.** states1 = states reachable from the root (0,0) in at least one digit. M(θ) is the
states1 × states1 matrix with entry Σ (g^a/p^e)^θ over the digits leading from σ to σ' (a, e the totals
of the chain). ρ(θ) is its spectral radius, ρ* = min_{θ >= 0} ρ(θ), attained at θ*, and
h := log_p ρ*. α is the maximum, over cycles of the automaton, of (number of factors g)/(number of digits).

## 1. Lemma T_G and Theorem R_G (reduction), PROVED

**Lemma T_G.** Let r be a node at depth d (r = n mod p^d) that survives d digits, in state σ = (s, c)
with A factors g and E divisions (E = d - s), and let x_r = (g^A r + C_r)/p^E be the integer value
after its decided steps. For every t >= 0 and K >= 1:

    r + p^d t survives d + K digits  <=>  z(t) := (g^A t + floor(x_r / p^s)) mod p^K  ∈  S_K(σ, g^A/p^E).

*Proof.* Decidedness only grows with the number of known digits, so the decided steps of r are decided,
with the same rows, for n = r + p^d t, and they take n to (g^A n + C_r)/p^E = x_r + g^A p^{d-E} t =
x_r + g^A p^s t. With d + K known digits of n, this value is known mod p^{s+K}; its low s digits are c and
its next K digits are z(t). The later steps are decided by exactly these digits, and they are the steps
in the definition of S_K, with every prefix slope multiplied by the node slope g^A/p^E. The earlier
prefixes have slope >= 1 because r survives. ∎ (This is round 5 `fourier` Lemma T in the present notation.)

**Theorem R_G.** Fix m, j >= 1 and K > j with d = m + j - K >= 0. For each surviving node r at depth d
let S_r = S_K(σ_r, g^{A_r}/p^{E_r}), u_r = g^{A_r} mod p^K, and

    Φ(u, B; S) = #{0 <= t < p^{K-j} : (u t + B) mod p^K ∈ S},   Φ̄(S) = p^{-j} |S|.

Then

    Σ_r min_B Φ(u_r, B; S_r)  <=  N(p^m, m+j)  <=  Σ_r max_B Φ(u_r, B; S_r),     Σ_r Φ̄(S_r) = p^m P(m+j),

with min and max over all B mod p^K. In particular |N(p^m, m+j) - p^m P(m+j)| <= max_r r(u_r, S_r) ·
p^m P(m+j), where r(u, S) = max_B |Φ(u,B;S) - Φ̄(S)| / Φ̄(S) over the r with S_r ≠ ∅.

*Proof.* Every n < p^m is r + p^d t with r < p^d and t < p^{m-d} = p^{K-j}. By Lemma T_G the number of
good t for a surviving r is Φ(u_r, floor(x_r/p^s) mod p^K; S_r), which lies between the min and the max
over B; non-surviving r contribute 0. For the identity let t run over all of Z/p^K: t -> u_r t + B is a
bijection, so the count is |S_r|, and Σ_r |S_r| = |R_{d+K}| = p^{m+j} P(m+j). Divide by p^j. ∎

No information about the digits of n beyond the horizon is used: B ranges over everything. The multiplier
u_r is the only arithmetic input. Checked against brute force in 1452 cases on 14 systems, and node by node on 582 nodes, and against the
round-5 `microrange` certificates for 3x+1 (identical numbers at m = 1000, K = 24, j = 2, 8)
(`check_all.py` part 3; a wrong multiplier g^{A+1} is detected).

## 2. Lemma F_G (averaged uniform discrepancy), PROVED

Let H_L be the image of <g> in (Z/p^L)^* and ι := sup_L [(Z/p^L)^* : H_L]. Then ι is finite: for p odd,
with o the order of g mod p and w = v_p(g^o - 1), ord_{p^L}(g) = o p^{max(0, L-w)} and the index is
((p-1)/o) p^{min(L,w)-1}; for p = 2 the index is 2^{v_2(g-1)-1} if g ≡ 1 (mod 4) and
2^{v_2(g^2-1)-2} if g ≡ 3 (mod 4) (L >= 3). These are the standard lifting-the-exponent facts; the
check verifies the closed forms and the stabilisation for L <= 20 for every g used.

**Lemma F_G.** Let Q = p^K, S ⊆ Z/Q, 1 <= j < K, N = p^{K-j}, and let u be uniform on H_K. Then

    E_u max_B |Φ(u,B;S) - N|S|/Q|  <=  G_K sqrt(|S| (1 - |S|/Q)),      (note N|S|/Q = Φ̄(S))
    G_K = ι (p/(p-1)) (1 + K ln p).

*Proof.* With Ŝ(ξ) = Σ_{x∈S} e(-xξ/Q) and G(η) = Σ_{t<N} e(tη/Q), Fourier inversion gives
Φ(u,B) = Q^{-1} Σ_ξ Ŝ(ξ) e(ξB/Q) G(uξ); the ξ = 0 term is N|S|/Q. So for every B,
|Φ - N|S|/Q| <= Q^{-1} Σ_{ξ≠0} |Ŝ(ξ)| |G(uξ)|, a bound free of B. Let e = v_p(ξ) < K. If e >= j, uξ has
additive order p^{K-e} dividing N, so G(uξ) = 0. If e < j, put L = K - e; then uξ = p^e a where a runs,
as u runs uniformly over H_K, uniformly over a coset of H_L in (Z/p^L)^* (reduction H_K -> H_L is a
surjective homomorphism). Using |G(p^e a)| <= 1/(2||a/p^L||),

    E|G| <= |H_L|^{-1} Σ_{a=1}^{p^L-1} 1/(2||a/p^L||) <= (ι/φ(p^L)) p^L (1 + ln(p^L/2)) <= G_K .

Finally Σ_{ξ≠0}|Ŝ| <= sqrt(Q-1) sqrt(Q|S| - |S|^2) <= Q sqrt(|S|(1-|S|/Q)) (Cauchy–Schwarz, Parseval). ∎

For p = 2, g = 3 this is the round-5 Lemma F with a slightly worse constant (that proof sums over odd a
only). Exact check on 30 random sets (`check_all.py` part 4): largest ratio left/right 0.08.

## 3. Lemma P_G (continuation sets are not small), PROVED under (P)

Let G ⊆ states1 be the largest set such that every σ ∈ G has a surviving K0-digit continuation from slope
1 that ends in a state of G (computed by fixed-point iteration), and B = states1 \ G. Put

    m_GG(K) = min_{σ ∈ G} #{ z ∈ S_K(σ, 1) whose path ends in G }.

**Hypothesis (P).** Every state of B reaches G, and either B carries no cycle (then r := longest path in B)
or every simple cycle in B has slope product < 1 (then r := |B|).

(a) m_GG is supermultiplicative: concatenating a G-ending survivor from σ with a G-ending survivor from its
end state (the end slope is >= 1) gives a G-ending survivor from σ, and the next digits of the value are a
bijective affine image of the next digits of the start. Hence h_* := lim (1/K) log_p m_GG(K) exists and
equals the supremum (Fekete). If m_GG(K) >= 1 for K0 <= K < 2K0 (checked), then
m_GG(K) >= m_GG(K0)^{⌊K/K0⌋-1} for all K >= K0, so log_p m_GG(K) >= h0 (K - 2K0) with
h0 = log_p m_GG(K0)/K0.

(b) **Lemma P_G.** For every σ ∈ states1, L >= 1 and K >= K1 (a constant), if S_K(σ, L) ≠ ∅ then
|S_K(σ, L)| >= min_{0 <= r' <= r} m_GG(K - r').

*Proof.* If σ ∈ G, S_K(σ,L) ⊇ S_K(σ,1). Let σ ∈ B and z ∈ S_K(σ, L) with path π. If π enters G at digit
r'', delete from its B-part every cycle; if B is acyclic nothing is deleted. Deleting a cycle with slope
product < 1 multiplies every later prefix slope by a factor > 1, so the shortened path still survives; it
has length r' <= r and ends in a G-state σ' with slope L' >= 1. Then S_K(σ, L) contains that path followed
by S_{K-r'}(σ', 1), which has at least m_GG(K - r') elements. If π never enters G (possible only if B has
cycles), π has at least K/|B| - 1 disjoint cycles in B, each of slope <= γ < 1, so survival forces
L >= c γ^{-K/|B|}; for K >= K1 this exceeds the threshold of a fixed path of length <= |B| from σ into G,
which therefore survives, and the first case applies. ∎

(P) holds for every system in the tables (`check_all.py` part 5); B is empty for most of them.

**[Rev] On K1.** The bound of (b) is asymptotic: it holds for K >= K1, and K1 is not small for every
system. The referee observed that for sf3_13, m_GG(K - r') = 0 for some K <= 10, and that for
desc_s32_plus9 the least non-empty |S_K(σ, L)| stays at 2 for K = 6..10 and grows only after that. So K1 can
be about 10 to 15 for these systems. This does not affect G1, G1' or G2, which use (b) only at
K = ⌊log_p M⌋ with M large. It does matter for small-K computations, which is why the certified tables (C_G)
and U'_G use the exact sets and not (b).

## 4. Theorem G1 (one-ended), PROVED

**Theorem G1.** Assume (SG), (F), (P). Let h_* be as in Section 3 (so h0 <= h_* <= h). Fix
0 < η < h_*/2. For all large M, all but at most M^{1-η/2} integers m ∈ [M, 2M) satisfy

    |N(p^m, b) - p^m P(b)|  <=  M^{-η/3} p^m P(b)     for every 1 <= b <= m + (h_*/2 - η) log_p M.

No drift hypothesis is needed; the statement is informative when h_* < 1 (negative drift), where
P(b) = p^{-(1-h)b + o(b)}.

*Proof.* For b <= m this is the in-horizon identity. Fix j >= 1, K = ⌊log_p M⌋ (so q := ord(g mod p^K)
<= p^K <= M), ε > 0, and let m ∈ [M, 2M), d = m + j - K. By Theorem R_G the relative error is at most
the max of r(u_r, S_r) over surviving nodes r at depth d with S_r ≠ ∅ and S_r ≠ Z/p^K.

*Types.* Let v = A_r - amin(E_r) (amin(E) = least A with g^A >= p^E; amin(E) = ⌈Eλ⌉ for E >= 1). If S_r is
not full then some z has A + a*(z) < amin(E + e*(z)) with e* <= K + k, so 0 <= v < V_K := (K+k)λ + 2.
S_r is {z : v + a*(z) >= amin(E + e*(z)) - amin(E)}, so it is determined by σ_r, v and the vector
Δ(E) = (amin(E+e) - amin(E))_{e <= K+k}. For E, e >= 1, Δ_e(E) = ⌊eλ⌋ + [{Eλ} + {eλ} >= 1] (all the
numbers involved are irrational), so Δ(E) takes at most K + k + 1 values as E varies. Hence the sets
that occur belong to at most T_K := |states1| · V_K · (K + k + 1) types τ = (σ, v, pattern), each with a
fixed set S_τ.

*Bad multipliers.* Let Bad_τ = {a mod q : r(g^a, S_τ) > ε}. As a is uniform mod q, g^a is uniform on
H_K, so by Markov's inequality and Lemmas F_G, P_G (with Φ̄ = p^{-j}|S_τ|):

    |Bad_τ| / q  <=  G_K p^j / (ε sqrt(m_P(K))),   m_P(K) := min_{r' <= r} m_GG(K - r').

*Counting octaves.* For fixed (σ, v), A = ⌈(m + j - K - s)λ⌉ + v is nondecreasing in m, takes each value
for at most μ := ⌊1/λ⌋ + 1 values of m, and ranges over an interval of length <= Mλ + 1. So at most
μ((Mλ + 1)/q + 1)|Bad_τ| <= μ(λ + 2)(M/q)|Bad_τ| values of m put a type-τ node on a bad multiplier.
(This is a union over all patterns of the slot; it does not assume that the pattern and the multiplier
are independent.) Summing over τ, the number of m ∈ [M,2M) that are bad for this j is at most

    T_K μ (λ + 2) G_K p^j M / (ε sqrt(m_P(K))).

For every other m, |N - p^m P(m+j)| <= Σ_r |Φ_r - Φ̄_r| <= ε Σ_r Φ̄_r = ε p^m P(m+j).

*Parameters.* Take h0 < h_* with h0 >= h_* - η/6 (possible by Fekete, with K0 large), ε = M^{-η/3},
and j <= J = ⌊(h_*/2 - η) log_p M⌋ (< K). By Section 3, sqrt(m_P(K)) >= c p^{h0 K/2} >= c' M^{h0/2}
(as p^K > M/p). Then the total over j <= J is at most
C (log M)^4 M^{1 - h0/2 + η/3} M^{h_*/2 - η} <= C (log M)^4 M^{1 - 7η/12} <= M^{1-η/2} for large M. ∎

**Corollary G1' (octaves and actual survival).** Assume also (H0): every row with a_r = e_r = 0 has
v_r >= 0. For all but 2M^{1-η/4} + O(log M) of the m ∈ [M, 2M), the number of n ∈ [p^{m-1}, p^m) with
T^i(n) >= n at every step decided by the b low digits of n equals (1 - 1/p) p^m P(b) (1 + O(M^{-η/6}))
for every b <= m + (h_*/2 - η) log_p M. **[Rev]** The exponents were M^{1-η/2} and M^{-η/3} in the first
version; see the bookkeeping note below.

**[Rev] Bookkeeping corrected.** The first version applied G1 at m - 1 to depths up to
m + (h_*/2 - η) log_p M, which is one digit more than G1 gives at m - 1. The corrected statement:
for all but 2M^{1-η/4} + O(log M) of the m ∈ [M, 2M), the octave count equals
(1 - 1/p) p^m P(b) (1 + O(M^{-η/6})) for every b <= m + (h_*/2 - η) log_p M.

*Proof.* Octave count = N(p^m, b) - N(p^{m-1}, b). Apply G1 with η/2 in place of η, on [M, 2M) and on
[M - 1, 2M - 1) (the proof of G1 is unchanged for an interval of length M starting at M - 1; only
M/q + O(1) enters). For large M, (h_*/2 - η/2) log_p(M - 1) >= (h_*/2 - η) log_p M + 1, so for m outside
both exceptional sets (at most 2M^{1-η/4} values) and b <= m + (h_*/2 - η) log_p M,

    |N(p^m, b) - p^m P(b)| <= M^{-η/6} p^m P(b),   |N(p^{m-1}, b) - p^{m-1} P(b)| <= M^{-η/6} p^{m-1} P(b),

and the difference is (1 - 1/p) p^m P(b) (1 + θ) with |θ| <= M^{-η/6} (p+1)/(p-1). It remains to show that
slope survival and actual survival agree on the octave outside O(log M) values of m: Lemma X. ∎

**Lemma X (exact survival test), PROVED.** Let V = max |v_r|, τ0 = max number of steps in one digit's
chain, and t <= τ0 b the number of decided steps. (i) If n >= 8tV and |log(g^{A_i}/p^{E_i})| >= 3tV/n for
every decided step i with (A_i, E_i) ≠ (0, 0), then for every i: [T^l(n) >= n for all l <= i] iff
[g^{A_l} >= p^{E_l} for all l <= i]. (ii) For c > 0 fixed, among m ∈ [M, 2M) at most O(log M) octaves
contain an n violating the hypothesis of (i) for some b <= m + c log_p m.

*Proof.* (i) Write L_l = g^{A_l}/p^{E_l} and y_l = T^l(n)/L_l. Then y_{l+1} = y_l + v_l/(u_l L_l), so
T^i(n) = L_i (n + δ_i) with δ_i = Σ_{l<i} v_l/(u_l L_l). Induct on i: if both conditions hold up to i - 1
then L_l >= 1 for l < i and |δ_i| <= iV <= tV. If L_i = 1 then A_i = E_i = 0 (unique factorization), all
rows so far have a = e = 0, δ_i >= 0 by (H0), and T^i(n) >= n: both conditions hold. If L_i >= exp(3tV/n)
then T^i(n) >= (1 + 3tV/n)(n - tV) >= n. If L_i <= exp(-3tV/n) <= 1 - 3tV/n + 4.5(tV/n)^2 then
T^i(n) <= L_i(n + tV) < n, using tV/n <= 1/8. In every case the two conditions agree at step i.
(ii) For n in octave m (n >= p^{m-1}) the hypothesis fails only if some pair (A, E) with E <= b and
(A, E) ≠ (0,0) has 0 < |A log g - E log p| < ε_m := 3τ0 bV p^{1-m}. Since |g^A - p^E| >= 1,
|A log g - E log p| >= 1/(2p^E) for E >= 1 (and >= log 2 when E = 0 < A), so E > m - C log m. If
(A1, E1) ≠ (A2, E2) both qualify, for octaves m1, m2 ∈ [M, 2M), then the difference satisfies
|ΔA log g - ΔE log p| < 2ε_M; ΔE = 0 or opposite signs are impossible (the left side would be >= log 2), so
1/(2p^{|ΔE|}) < 2ε_M and |ΔE| > M - C' log M. All qualifying E lie in an interval of length M + O(log M),
so there are at most two of them, each with a unique A, and each spoils only the octaves m with
E ∈ (m - C log m, m + c log m], that is O(log M) octaves. Finally n >= p^{m-1} >= 8tV for all large m. ∎

The exceptional octaves are computed exactly for m <= 3000 for every system (`check_all.py` part 7,
`data/exceptional_octaves.json`). Only octaves m <= 17 are flagged, all because of the size condition
n >= 8tV. No pair (A, E) with E <= 3000 + 2 log_p 3000 comes within the critical distance, so the
O(log M) Diophantine exceptions do not occur in this range. Brute force on whole octaves confirms that
slope and actual counts coincide in every unflagged octave tested.

## 5. Theorem G2 (two-ended), a conditional sketch under a ballot hypothesis

**[Rev] Status.** For every system, including split5_3, the argument below is a *proof sketch
conditional on (B2)*. For split5_3 the theorem itself is PROVED in `split5_3_s27.md`, in that file's own
coding; see Lemma B1 for exactly what is and is not transferred. The notation is also corrected: the
terminal length is now ℓ, and k means only the table exponent (Q = p^k).

Let ρ* = ρ(M(θ*)), and define the Rényi-2 rate of the tilted measure

    H_2 := 2h - log_p ρ(M(2θ*))      (the tilted weight of a d-digit word w is π_w = L_w^{θ*} ρ*^{-d}),

κ := 1/(α log_p g) and c_2 := min(1, h_*/2 + κ H_2/2).

**Hypothesis (B2), ballot asymptotics.** There are C, c > 0 such that for all states σ, slopes L >= 1 and
n >= 1: #S_n(σ, L) <= C (1 + log L)^c L^{θ*} ρ*^n n^{-3/2}, and |R_n| >= C^{-1} ρ*^n n^{-3/2}.

**Theorem G2.** Assume (SG), (F), (P), (B2) and θ* > 0. Fix 0 < η < c_2. For large M, all but
O(M^{1-η/4}) of m ∈ [M, 2M) satisfy N(p^m, b) = p^m P(b)(1 + O(M^{-η/2})) for every
b <= m + (c_2 - η) log_p M.

*Proof* (the argument of `round2/rewriting/split5_3_s27.md`, "Cancellation from both ends of a passing
word", in the present notation). Average over D ∈ [M, 3M], with initial length
d = ⌊(log_g M - C_0)/α⌋ (so g^{A} <= M for every live d-digit word, A <= αd + C_0) and terminal length
ℓ = ⌊log_p M⌋ + 2. Let μ_D be uniform on {n/p^D : n ∈ R_D}.

(1) *Splitting.* Group the surviving depth-d nodes by type γ = (σ, A). By Lemma T_G applied twice, every
n ∈ R_D above a node r of type γ is n ≡ y_r/g^A + p^d g^{-A}(z - …) with y_r = p^E c - C_r an integer,
and z running over the continuations of γ, which split further at depth D - ℓ into middle nodes ν and
terminal sets T(ν) = S_ℓ(σ_ν, L_ν). With T_D(ξ) the largest normalised terminal sum
|T(ν)|^{-1}|Σ_{w ∈ T(ν)} e(ξ g^{-A_ν} w/p^ℓ)| over surviving depth-(D-ℓ) nodes ν, and
U_γ(ξ) = V_γ^{-1}|Σ_{r ∈ γ} e_Q(ξ y_r/g^A)|,

    |μ̂_D(ξ)|  <=  T_D(ξ) Σ_γ p_γ U_γ(ξ),     p_γ = V_γ #S_{D-d}(γ) / |R_D|.

(2) *Weights.* By (B2), p_γ <= C (1+d)^{c'} V_γ π_γ with π_γ = L_γ^{θ*} ρ*^{-d}, uniformly in D.

(3) *Initial phases.* |y_r| <= (τ0 dV + p^k) g^A (k the table exponent), the y_r are distinct within a group, h := g^A <= M.
By reciprocity e_Q(ξy/h) = e(ξy/(hQ)) e_h(-ξ y Q̄_h), and as D runs over [M, 3M], Q̄_h = p^{-D} mod h runs
over the subgroup <p> of (Z/h)^* in complete periods (its order is < h <= M); <p> has index bounded in terms
of p and g only (same lifting-the-exponent argument as for ι). Orthogonality gives
E_D U_γ(ξ)^2 <= C (1 + d) gcd(ξ, g^∞) / V_γ.

(4) *Terminal sets.* For a fixed type of terminal set (state, slot, pattern as in the proof of G1), A mod q
is spread at most a bounded factor above uniform as D runs over [M, 3M]; if e = v_p(ξ) then
ξ g^{-A}/p^e runs over a coset of H_{ℓ-e}, and each class mod p^{ℓ-e} holds at most p^e points of T, so
E_D |T̂(ξ g^{-A})|^2/|T|^2 <= C p^e/|T|. Summing over the poly(ℓ) types and using Lemma P_G:
E_D T_D(ξ)^2 <= C (1 + ℓ)^{c} p^{v_p(ξ)} / m_P(ℓ).

(5) Cauchy–Schwarz over D in (1), then Σ_γ π_γ sqrt(V_γ) <= sqrt(#γ) (Σ_w π_w^2)^{1/2} and
Σ_{|w| = d} π_w^2 = (M(2θ*)^d 1)_root ρ*^{-2d} <= C d^c p^{-H_2 d}, give for 1 <= ξ <= M

    E_D |μ̂_D(ξ)|  <=  (log M)^{C} p^{v_p(ξ)/2} gcd(ξ, g^∞)^{1/2} M^{-κ H_2/2} M^{-h0/2},  h0 -> h_*.

(6) The Erdős–Turán inequality (quoted from memory: for a probability measure μ on R/Z and every integer
H >= 1, sup_J |μ(J) - |J|| <= C (1/H + Σ_{ξ=1}^{H} |μ̂(ξ)|/ξ) with an absolute constant C; I did not
check the source here, and only the existence of an absolute C is used. The referee confirms this form;
s27 cites it from Montgomery–Vaughan.) with H = ⌊M^{1-η/8}⌋, the
valuation factors costing O(log M), gives E_D Δ_D <= M^{-c_2 + η/8} (log M)^C. Markov discards
O(M^{1 - η/4}) depths; at a retained depth D the interval [0, p^m)/p^D has length p^{m-D} >= M^{-c_2+η},
so the relative error is O(M^{-η/2}). Each discarded D spoils O(log M) values of m. ∎

**Lemma B1 (when (B2) is known). [Rev: corrected.]** The first version said that for split5_3, (B2)
"is" the prefix-count theorem of `split5_3_s27.md`, and that G2 is therefore PROVED for split5_3. That
overstated what is written. What is true:

* `split5_3_s27.md` ("Cancellation from both ends of a passing word") PROVES a two-ended count law for
  split5_3 with constant c_* = 0.45991804..., but for its own counting set: the shifted variable
  y = n + 3, its (z, s) bit coding, a halving clock with a pending-halving convention, and actual survivors
  in [2^m, 2^{m+1}).
* The formula c_2 = min(1, h_*/2 + κ H_2/2) of this file, evaluated on the present automaton for split5_3,
  gives 0.459918 (`cwconst.py`, `data/constants_K1500.txt`), which agrees with s27's closed form
  0.45991804 to about 10^{-8} (checked in `referee1_check.py` section B).
* The proof of G2 above uses only two inputs from s27: the weight bound (its estimate (2)) and its
  terminal-set bound. These have to be carried from the s27 bit coding to the present digit automaton
  of n. That transfer is not written out here. It is plausible: n ↦ n + 3 is a 2-adic isometry, and
  split5_3 has (Pot), so the slope walk is an i.i.d. two-valued walk after relabelling. But it is not done.

So: **Theorem G2 for split5_3 is PROVED in `split5_3_s27.md`, in that file's coding. The present formula
reproduces its constant. The statement in the present coding (slope survivors N(2^m, b) in the digit tree
of n) is a routine-looking translation that is not written out, so in this file it has the same status as
for the other systems: a sketch conditional on (B2).** I did not prove (B2) for any system. For
single-state systems it is the classical ballot asymptotic for a walk with i.i.d. steps of finitely many
values and zero tilted drift, which I quote as known but have not written out. For multi-state systems I
know no reference.

Numerical EVIDENCE for (B2) (`evidence_b2.py`, `data/evidence_b2.txt`): the normalised ratio
log(|R_n| ρ*^{-n} n^{3/2}) stays in a band of width 0.25 to 1.7 for n in [100, 1200] for every
contracting system. **[Rev2]** For all 19 systems the maximum of the normalised ratio over [100, 1200]
occurs in the last third, so a slow upward drift is generic, not specific to m3_g (REFEREE2, N2; extended to
n = 3000, 3x+1 levels off at about 2.38, K7 stays in [0.84, 1.06] and split5_3 oscillates in [0.60, 1.07]).
**[Rev]** For three systems this reading is weak, and the data neither confirm nor
refute the exponent n^{-3/2}:
* m3_g: the ratio rises monotonically (3.81 at n = 100 to 5.48 at n = 1200; the last third alone is
  [5.27, 5.48]). The referee measured a local exponent of about 0.85, not 1.5, between n = 300 and 600.
  Here θ* = 0.045, so the asymptotic regime is reached very slowly, if at all in this range.
* sf3_13 and sf3_135: large oscillations (θ* about 4 to 4.6), with local exponents about 1.05 and 0.90
  (referee's measurement).

What is proved unconditionally for all systems with (Pot) (a per-state relabelling of the digits making
the log-slope a coboundary plus a function of the digit; `check_all.py` part 6) is the weaker lower bound
|R_n| >= ρ*^n n^{-C} (Raney's cyclic lemma on the relabelled i.i.d. walk, plus a buffer word, plus the
method of types). For single-state systems G = {root} and m_GG(K) = |R_K|, so this gives h_* = h. For
split5_3 the same (Pot) argument applies from every state of G, with a buffer word from each state (see
the paragraph after the proof sketch), so h_* = h is proved here too. **[Rev2]** (the first two versions
cited the continuation-set bound of `split5_3_s27.md` for this; that bound is stated in s27's (z, s) bit
coding of y = n + 3, so citing it is a coding transfer of the kind withdrawn for G2, and it is not needed.)
For the other multi-state systems
h_* = h is EVIDENCE only (h0 rises towards h as K0 grows, at the rate (3/2) log_p K0 / K0 expected from the
K^{-3/2} factor). None of this gives (B2), because the proof of G2 compares counts at depths differing by
O(log^2 M) and needs the exact n^{-3/2}.

*Proof sketch of the lower bound for (Pot) systems (PROVED; written out because it is used for h_* = h).*
Relabel the digits by π_σ so that the log-slope of a digit is f(label) + φ(σ') - φ(σ). Let Δ = max φ - min φ
and dip = the largest drop of the log-slope inside one digit's chain. Take a surviving buffer word w0 from
the root with log-slope >= Δ + dip (found and checked exactly, `check_all.py` part 6). For a label word u
whose f-prefix sums are all >= 0, w0 u survives (its log-slope never falls below that of w0 minus Δ + dip).
By Raney's lemma every label word with Σ f >= 0 has a cyclic rotation with all prefix sums >= 0, and
rotation is at most n-to-1, so |R_{n+|w0|}| >= n^{-1} #{u : Σ f(u) >= 0}. The tilted type q*_δ =
e^{θ* f(δ)}/ρ* has mean 0 and entropy log ρ*; a type with denominators n, mean >= 0 and all coordinates
within O(1/n) of q* exists, and its multinomial coefficient is >= (n+1)^{-p} ρ*^n e^{-O(log n)}.
For a multi-state G the same argument, run from each σ ∈ G with a surviving buffer word w0(σ) from σ that
ends in G, bounds m_GG(K) from below.

**[Rev2] h_* = h for split5_3 (from this file's (Pot) argument, following REFEREE2).** In the present
automaton states1 = G = {(0,0), (1,1)}, with digit moves (0,0) -0-> (0,0) slope 1/2, (0,0) -1-> (1,1)
slope 1, (1,1) -0-> (0,0) slope 5/4 and (1,1) -1-> (1,1) slope 1/2. With the potential
φ(1,1) - φ(0,0) = -(1/2) log(5/4) the relabelled slopes are {1/2, √5/2} from both states, so the label
walk is i.i.d., and Δ = (1/2) log(5/4). The intra-digit dip is 0 (no prefix inside a digit is below both
of its endpoints). The buffer words "1 0" from (0,0) and "0" from (1,1) both survive, end in G, and reach
slope 5/4 > √(5/4) = e^{Δ + dip}. So Raney's lemma plus types gives m_GG(K) >= ρ*^K K^{-C} from both
states of G, and h_* = h. This is checked exactly in `referee2_check.py` section J (the prover's
`check_all.py` part 6 checks a buffer word from the root only). Numerically log_2 m_GG(K)/K is 0.490,
0.529, 0.552 and 0.564 at K = 100, 200, 400, 800, rising towards h = 0.5807 at the expected
(3/2) log K / K rate (REFEREE2). The G1 constant 0.29034 for split5_3 therefore rests on this file alone.

## 6. Theorem U'_G (every octave, exact constants), PROVED

**Theorem U'_G.** Fix L. Let D'_{L,m} be the maximum, over states σ ∈ states1 ∪ {root}, non-full
super-level sets S of g_σ on Z/p^L, units w ∈ <g mod p^L> and windows I = [c, c + p^{L-m}), of
|#(wS ∩ I) p^m/|S| - 1|. Then for every b >= L and 1 <= m < L:

    |N(p^{b-m}, b) / (p^{b-m} P(b)) - 1|  <=  D'_{L,m}.

*Proof.* Split r ∈ R_b as r1 + p^{b-L} t (Lemma T_G with d = b - L, K = L). r < p^{b-m} iff
t < p^{L-m}. The good t for a surviving r1 are those with u t + B ∈ S_L(σ, g^A/p^E) =: S, i.e.
t ∈ u^{-1}(S - B) =: wS + c'; the count is #(wS ∩ [c, c + p^{L-m})) for some c, with w = u^{-1} ∈ <g>.
S is a super-level set of g_σ (or empty, contributing 0 to both sides, or full, contributing exactly).
So each r1 contributes |S| p^{-m}(1 + θ) with |θ| <= D'_{L,m}; and p^{b-m} P(b) = Σ_{r1} |S| p^{-m}. ∎

This is round 5 `fourier` Theorem U' (R-B) for a general table map. The constants are exact rationals
(slopes ranked with Fractions; window counts in integers, `cw uprime`); `check_all.py` part 8 checks the
C code against a naive evaluation and reproduces the round-5 constants 213/1627, 213/749, 349/749 for 3x+1.

## 7. What these theorems say about GLOBAL

None of them settles GLOBAL for any system. They count starts by the slope stopping time up to
b = log_p X + c log_p log_p X digits (G1, G2: almost every octave; U'_G: every octave, a fixed relative
error, m < L digits past the horizon).

**[Rev: corrected direction.]** The first version said that GLOBAL "needs, at least", that no start in a
large octave survives C* log_p X digits. That is backwards. GLOBAL does not imply it: GLOBAL allows
stopping times much longer than C* log n. The correct statement is the converse direction. A *counting
proof* of GLOBAL along these lines would need control out to depth C* log_p X, with C* = 1/(1 - h), the
depth where the prediction X P(b) falls below 1 (Conjecture E with exact constant; round 4
`lead/CONJECTURE.md`). Conjecture E at depth (C* + ε) log_p X, together with a proof that there are no
cycles beyond the known ones, would be a *sufficient* route to GLOBAL; it is not a necessary one. The
theorems here reach depth (1 + o(1)) log_p X, a factor C* short of that route, and they are consistent with any finite set of extra
cycles (3x-1, 3x+5 obey them with the same constants as 3x+1) and with divergent orbits (5x+1, m3_e and
the core W obey G1 with h = 1). For expanding systems (h = 1) P(b) tends to a positive limit and the
count law is an in-horizon statement in disguise; it implies nothing about divergence.

## 8. Revision after REFEREE1

REFEREE1 found no mathematical error and asked for relabelling and wording fixes. All are made above,
marked **[Rev]**:

1. G1 is proved for (SG) maps satisfying (F) and (P). (P) is a per-system check (`check_all.py` part 5),
   not automatic. This was a README wording issue; Section 4 already listed (P) among the hypotheses.
2. Corollary G1': the depth bookkeeping at m - 1 was off by one digit. Corrected by applying G1 with η/2.
   The exceptional set is now 2M^{1-η/4} + O(log M) and the error is O(M^{-η/6}).
3. Lemma P_G: added a note that K1 can be about 10 to 15 (sf3_13, desc_s32_plus9).
4. G2 for split5_3 is no longer called PROVED *here*. It is PROVED in `split5_3_s27.md` in that file's
   coding. The present formula reproduces the constant. The transfer to the present coding is not written
   out. Lemma B1 no longer says that (B2) "is" s27's prefix-count theorem.
5. (B2) evidence: m3_g, sf3_13 and sf3_135 are marked as not confirming the n^{-3/2} exponent.
6. Section 5 notation: the terminal length is now ℓ, and k is only the table exponent.
7. Section 7: "GLOBAL needs control out to C* log_p X" is withdrawn as backwards. It is replaced by
   "a counting proof along these lines would need ...", and Conjecture E is stated as a sufficient route.
8. (F): it fails exactly on a cycle of division-free decided steps, not only a class mapped into itself.
9. The round-5 reproduction for 3x+1 (m = 1000, K = 24, j = 1..8) is now an exact check, `check_all.py`
   part 9.

## 9. Revision after REFEREE2

REFEREE2 confirmed every proof and found no mathematical error. Its one fix and three nits are made above,
marked **[Rev2]**:

1. h_* = h for split5_3: the citation of the s27 continuation-set bound (stated in s27's coding) is
   replaced by this file's own (Pot)/Raney argument, run from both states of G with a buffer word from
   each (Section 5). The G1 constant 0.29034 for split5_3 now rests on this file alone.
2. N1 (README): the 3x+1 constant 0.47498 = H(λ)/2 is no longer presented as a round-5 number. Round 5
   proved only h0/2 >= 0.4715 and withdrew H(λ)/2; here G1 together with h_* = h for single-state systems
   gives it, a small strengthening of round-5 Theorem D.
3. N2: one sentence on the generic slow upward drift of the (B2) ratio (Section 5).
4. N3: the external-results list in the header now matches the README (Erdős–Turán is in Section 5;
   Raney's lemma, the method of types and lifting the exponent are listed).

