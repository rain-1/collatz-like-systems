# split5_3 and split5_1: a deep attack, and the exact size of the non-descending set for every split map

**Systems.** split5_3 = SPLIT(5,1,3) (CLS-049/065): even n -> n/2, n = 1 (mod 4) -> 5n+3,
n = 3 (mod 4) -> n+3. split5_1 = SPLIT(5,1,1) (CLS-048/064): the same with +1.

**Outcome in one paragraph.** GLOBAL for split5_3 and split5_1 is **not settled** (OPEN, tier 5).
What is new and proved here: (1) the exact place where the settled sibling breaks, within the
column d = 3: SPLIT(3,1,3) is already exactly equivalent to the Collatz no-divergence conjecture,
and the 3Z part of split5_3 is the new system SPLIT(1,5,1); (2) a **general theorem giving the
exact Hausdorff dimension of the non-descending 2-adic set Ω for every split map**, with closed
form H_2(1 - 2/log_2 c) for the "i.i.d. type" that contains split5_3, and a matching
counting theorem #{n <= X never below n} = O(X^{dim Ω}); (3) the numbers that separate the two
open maps: dim Ω = 0.580684... for split5_3 but dim Ω in [0.93627, 0.93686] for split5_1; (4) a
proof that every member with positive drift has Ω of positive Haar measure; (5) the precise
status of the lens questions (a)-(d).

| claim | statement | status |
|---|---|---|
| D3 | column d = 3: (1,1,3) descent; (3,1,3) <=> P1; (5,1,3) open; (7,1,3) = accelerated 7x+9 | PROVED (family.md) |
| Z3 | on 3Z, split5_3 is conjugate to SPLIT(1,5,1); GLOBAL(split5_3) => GLOBAL(SPLIT(1,5,1)); the same Ω-dimension 0.5807 | PROVED |
| Ω1 | for SPLIT(c,1,d), c = 1 mod 4, d = 3 mod 4 (and SPLIT(1,c,d), d = 1 mod 4), 5 <= c <= 13: dim_H Ω = H_2(1 - 2/log_2 c) exactly | PROVED |
| Ω2 | for every class-O member with negative drift, and for the positive-drift (3,7)/(7,3) rows: dim_H Ω = log_2 ρ_*, ρ_* = min_{θ>=0} ρ(M_θ) | PROVED (upper bound for every member; lower bound by an excursion/duality argument for T1, T2, T3 with negative drift; the (3,7)/(7,3) rows via Ω5) |
| Ω3 | rigorous two-sided numbers for every class-O type (table) | PROVED (exact rational checks) |
| Ω4 | #{n <= X : T^j(n) >= n for all j} = O(X^{log_2 ρ(θ)}) for every θ >= 0; in particular O(X^{0.5807}) for split5_3, O(X^{0.9369}) for split5_1 | PROVED |
| Ω5 | if the drift is positive (the (3,7) and (7,3) rows), Ω has positive Haar measure | PROVED |
| a-d | lens questions | see section 6: (a) no conjugacy or well-founded order found; (b) OPEN, reduced to a digit question; (c) bounded-depth ancestor search provably cannot exclude a positive density; (d) settled by Ω1 |

Check: `check_omega.py` (exact; runs in about a minute). Novelty: Ω1 for c = 5 restates, for the
descent-tree set, the round-2 dimension of the prefix-test set; the general theorem Ω2, the
split5_1 value and Ω4/Ω5 are new to this repository. The method (Chernoff upper bound, cycle
lemma and types for the lower bound) is standard large-deviation material; for the 3x+1 map the
same computation gives H_2(log 2/log 3) = 0.9500. Literature novelty not checked.

## 1. Coordinates (recap)

On odd values split5_3 has two blocks: A(x) = (5x+3)/4 for x = 1 (mod 4) (three raw steps) and
B(x) = (x+3)/2 for x = 3 (mod 4) (two raw steps, result odd). In N = x + 3 the A-block is
N -> (5/4) N. All of round2/rewriting/split5_3_s27.md applies; in particular every n < 2^66 reaches
one of the five cycles (minima 1, 3, 5, 61, 125).

## 2. The column d = 3 and the 3Z part (claims D3, Z3)

family.md, Theorem K: SPLIT(3,1,3) is conjugate on odd values to x -> x/2, (3x+3)/2 on x >= -1,
hence GLOBAL(SPLIT(3,1,3)) <=> GLOBAL(3n+3) <=> P1 (lhf/collatz3/CLS-014). SPLIT(7,1,3) is conjugate
to the accelerated 7x+9 map. So in the d = 3 column, multiplier 3 is exactly Collatz-hard,
multiplier 5 is split5_3.

**Z3.** 3Z is forward invariant (Lemma S of family.md) and n = 3m conjugates split5_3 on 3Z to
SPLIT(1,5,1): m even -> m/2, m = 1 (mod 4) -> m+1, m = 3 (mod 4) -> 5m+1 (3 = 3 mod 4 exchanges
the branches). Divisibility by 3 is invariant in both directions (each branch multiplies the
residue mod 3 by 1, 2 or 5). Therefore

    GLOBAL(split5_3) <=> GLOBAL(SPLIT(1,5,1)) and GLOBAL(split5_3 on 3 ∤ n).

SPLIT(1,5,1) has blocks (m+1)/2 (m = 1 mod 4, result odd) and (5m+1)/4 (m = 3 mod 4), the expanding
2-adic point is m = -1, and in the coordinate m + 1 the expanding block is again multiplication by
5/4. It is of the same "i.i.d. type" as split5_3 (section 3), with the same dim Ω. Its only cycle
found is {1, 2} (all starts <= 3000; EVIDENCE), which corresponds to the cycle {3, 6} of split5_3.

## 3. The exact dimension of Ω: the i.i.d. type (claim Ω1)

**Coding.** For any SPLIT(a,b,d), read the binary digits of the start n from the bottom. Keep a
state: U (the parity of the current value is not yet known) or O (the current value is odd, its
class mod 4 not yet known). In state U a digit decides the parity: even gives one halving (slope
1/2, stay in U), odd gives no step (slope 1, go to O). In state O a digit decides the class mod 4:
class 1 applies a n + d and v_a halvings (slope a/2^{v_a}), class 3 applies b n + d and v_b
halvings (slope b/2^{v_b}); the next state is U if the valuation used is 2 and O if it is 1 (by
Lemma V the output is then known to be odd). On n = 2^j t + r the reached value is α t + β with
α odd in state U and α = 2·odd, β odd in state O; this invariant is preserved by all four moves,
so **digit words of length j correspond bijectively to residues mod 2^j** and this is an isometry
between Z_2 and the digit-sequence space. (Same verification as in round 2 for split5_3; the
general case uses only Lemma V.)

Within a block the raw slopes are c, c/2, ..., c/2^v, all at least the block-end value, so the
**coefficient stopping time** of a 2-adic integer is infinite iff every digit-prefix slope product
P_j is >= 1. Define

    Ω = { ω in Z_2 : P_j(ω) >= 1 for all j }.

This is the limit set of the descent tree (round 2): the classes that never close.

**Theorem Ω1.** Let T = SPLIT(c,1,d) with c = 1 (mod 4), d = 3 (mod 4), or T = SPLIT(1,c,d) with
c = 1 (mod 4), d = 1 (mod 4), and 5 <= c <= 13. Put q_c = 1 - 2/log_2 c. Then

    dim_H Ω = H_2(q_c),   H_2(x) = -x log_2 x - (1-x) log_2(1-x).

Values: c = 5: 0.5806841231... (split5_3, SPLIT(1,5,1), SPLIT(5,1,7), ...); c = 9: 0.9499555...;
c = 13: 0.9952676... . (For c >= 17 the drift is positive and Ω has positive measure, Ω5.)

*Proof.* In both cases the O state has the self-loop of slope 1/2 (the branch with multiplier 1 and
valuation 1) and the return to U of slope c/4. Weight the states by w(U) = 1, w(O) = λ = √c/2 > 1
and put W_j = P_j w(state_j). Each digit multiplies W by λ or by 1/2: in U, odd gives 1·λ and even
gives 1/2; in O, the return gives (c/4)/λ = λ and the self-loop gives 1/2. Call a digit *bad* when
its factor is 1/2. The map ω -> (bad-indicator sequence) is again an isometry onto {0,1}^N (in each
state the two digit values give the two factors). With m_j bad digits among the first j,
log W_j = (j - m_j) log λ - m_j log 2, and W_j/λ <= P_j <= W_j. Let
Λ(κ) = {all j >= 1: (j - m_j) log λ - m_j log 2 >= κ}. Then Λ(log λ) ⊂ Ω ⊂ Λ(0).

Upper bound: Λ(0) is covered, for each m, by the cylinders of length m with m_m <= q_c m
(q_c = log λ / log(2λ) = 1 - 2/log_2 c), and Σ_{i <= qm} C(m,i) <= 2^{m H_2(q)} for q < 1/2
(from 1 >= Σ_{i<=qm} C(m,i) q^i (1-q)^{m-i} >= Σ_{i<=qm} C(m,i) 2^{-m H_2(q)}). So the
s-dimensional Hausdorff measure vanishes for s > H_2(q_c).

Lower bound: fix m and i < q_c m. Among the C(m,i) words with exactly i bad digits the total
surplus (m - i) log λ - i log 2 is positive (q_c is irrational, so i < q_c m is strict). By the cycle
lemma each such word has a rotation all of whose prefix surpluses are > 0, and a rotation class has
at most m members, so the set Y of length-m words with all prefix surpluses >= 0 has
|Y| >= C(m,i)/m >= 2^{m H_2(i/m)}/(m(m+1)). Every infinite concatenation 0 Y Y Y ... (one good
digit, then words of Y) has all prefix surpluses >= log λ, so it lies in Λ(log λ) ⊂ Ω. The uniform
mass on these concatenations gives each cylinder of length 1 + km mass |Y|^{-k}, so by the mass
distribution principle dim_H Ω >= log_2 |Y|/m. Let i/m -> q_c and m -> ∞. ∎

## 4. Every split map (claims Ω2, Ω3, Ω4)

For each member, let M_θ be the 2x2 matrix over {U, O} whose (s, t) entry is the sum of slope^θ
over the digit moves from s to t. Let ρ(θ) be its spectral radius and ρ_* = min_{θ >= 0} ρ(θ)
(ρ(0) = 2).

**Theorem Ω2 (upper bound, every member).** dim_H Ω <= log_2 ρ(θ) for every θ >= 0.

*Proof.* The number of length-m digit words with P_m >= 1 is at most Σ_words P_m^θ =
1_U^T M_θ^m 1 <= (max r / min r) ρ(θ)^m, where r > 0 is a Perron eigenvector (M_θ is irreducible:
U -> O -> U). Cover Ω by these cylinders. ∎

**Theorem Ω2' (lower bound, class O).** For every class-O member with negative drift, and for the
positive-drift members with (a,b) in {(3,7),(7,3)}, dim_H Ω = log_2 ρ_*. (In the table below these
are all the class-O types; the (3,7)/(7,3) rows are the only positive-drift class-O members in it.)

*Proof.* The class-O members are of three types: T1 (O has the self-loop of slope 1/2: section 3),
T2 (O has an expanding self-loop of slope s > 1 and returns to U with slope r), T3 (both O-moves
return to U, slopes α, β). Decompose a word starting in U into *excursions* from U: "even"
(length 1, slope 1/2), and "odd" (U -> O, then for T2 j self-loops and the return: length j + 2,
slope s^j r; for T3 one of the two returns: length 2, slope α or β). For T2 and T3 the slope product
along an excursion is monotone or rises then falls once, so its minimum is at one of the two
ends; hence **a word lies in the closure condition iff the excursion-end products are all >= 1**.
Let ρ(θ) solve the renewal equation F(θ, ρ) = Σ_e slope(e)^θ ρ^{-length(e)} = 1; expanding the
characteristic polynomial of M_θ shows this ρ is the Perron root (T3: ρ^2 - 2^{-θ}ρ - α^θ - β^θ = 0;
T2: ρ^2 - (2^{-θ} + s^θ)ρ + 2^{-θ}s^θ - r^θ = 0 with ρ > s^θ).

If the drift is negative, ρ(θ) attains its minimum at some θ_* > 0: log ρ is convex in θ,
its derivative at 0 is the drift (the mean log-slope under the stationary measure of the fair-digit
chain), and ρ(θ) -> ∞ as θ -> ∞ because every class-O type has a loop of slope > 1. Put
p_e = slope(e)^{θ_*} ρ_*^{-length(e)}, a probability distribution. Differentiating F(θ, ρ(θ)) = 1
at θ_* (where ρ' = 0) gives Σ p_e log slope(e) = 0, and then
-Σ p_e log p_e = (Σ p_e length(e)) log ρ_*. For T3 the alphabet has three letters. Choose counts
(n_0, n_α, n_β) proportional to p up to rounding with total log-slope > 0. The number of excursion
sequences with these counts is a multinomial coefficient. Its logarithm is R·H(counts/R) - O(log R),
where R is the number of excursions. By the cycle lemma at least a 1/R fraction of them have all
excursion-end partial sums > 0. These words have common length m = Σ counts·length and are loops
at U, so their infinite concatenations lie in Ω. As in section 3, dim_H Ω >= log_2(#)/m, and
log_2(#)/m -> log_2 ρ_* as R -> ∞. For T2 group the odd excursions by their total number N and the
total number J of self-loops. The count of sequences with n_0 even excursions, N odd ones and J
self-loops is C(n_0 + N, N)·C(J + N - 1, N - 1), and the total slope depends only on (n_0, N, J).
With frequencies n_0 : N : J = p_even : P_odd : P_odd·σ/(1 - σ), where σ = s^{θ_*}/ρ_* and
P_odd = Σ_j p_j, Stirling's formula gives the same exponent log ρ_*. We write this step out. Here
p_j = s^{jθ_*} r^{θ_*} ρ_*^{-(j+2)} is proportional to σ^j, so conditionally on an excursion being
odd, j is geometric: p_j/P_odd = (1 - σ)σ^j. Put R = n_0 + N and μ = J/N = σ/(1 - σ), so that
1/(1 + μ) = 1 - σ. By Stirling's formula, log C(n_0 + N, N) = R·H(p_even) + O(log R), where
H(p_even) = H_2(p_even) is the entropy of the choice even/odd, and
log C(J + N - 1, N - 1) = (J + N)·H_2(N/(J + N)) + O(log R) = N·(1 + μ)H_2(1/(1 + μ)) + O(log R)
= R·P_odd·H_geom + O(log R), where H_geom = H_2(σ)/(1 - σ) = (1 + μ)H_2(1/(1 + μ)) is the entropy
of the geometric distribution (1 - σ)σ^j. Hence

    log C(n_0 + N, N) + log C(J + N - 1, N - 1) = R·[H(p_even) + P_odd·H_geom] + O(log R),

and by the chain rule for entropy the bracket is exactly the entropy -Σ_e p_e log p_e of the
excursion distribution p (first the choice even/odd, then j given odd). By the identity derived
above, this entropy equals (Σ_e p_e length(e)) log ρ_*. Choose (n_0, N, J) proportional to
(p_even, P_odd, P_odd·σ/(1 - σ)) up to rounding with total log-slope > 0. The set of excursion
sequences with fixed (n_0, N, J) is closed under rotation, so by the cycle lemma at least a 1/R
fraction of them have all excursion-end partial sums > 0. Their common length is
m = n_0 + 2N + J = R·(Σ_e p_e length(e)) + O(1), so, as for T3, log_2(#)/m -> log_2 ρ_* as R -> ∞.
This proves equality for T2.

Positive drift. For the (3,7)/(7,3) rows the drift is positive, so (log ρ being convex with
derivative at 0 equal to the drift) ρ_* = ρ(0) = 2 and log_2 ρ_* = 1; Ω5 below shows that Ω has
positive Haar measure, so dim_H Ω = 1 = log_2 ρ_*. ∎

**Theorem Ω3 (certified numbers).** `check_omega.py` verifies, in exact rational arithmetic:
an upper bound ρ(p/q) <= μ via rational upper bounds for slope^{p/q} (u^q >= slope^p) and the 2x2
criterion μ >= M_UU, μ >= M_OO, (μ - M_UU)(μ - M_OO) >= M_UO M_OU; and a lower bound
log_2(⌊# / R⌋)/m with the exact multinomial counts above.

| type | members (examples) | O moves | drift/digit | dim_H Ω |
|---|---|---|---|---|
| T1, c = 5 | split5_3, SPLIT(5,1,7), SPLIT(1,5,1), SPLIT(1,5,9) | 1/2 self-loop, 5/4 return | -0.291 | 0.5806841231... = H_2(q_5) (exact) |
| T2 (5/2, 1/4) | split5_1, SPLIT(5,1,9), SPLIT(1,5,3) | 5/2 self-loop, 1/4 return | -0.291 | [0.936275, 0.936852] |
| T3 (7/4, 1/4) | SPLIT(7,1,1), SPLIT(1,7,3) | both return | -0.369 | [0.752601, 0.753484] |
| T3 (3/4, 5/4) | SPLIT(3,5,1), SPLIT(5,3,3) | both return | -0.242 | [0.662525, 0.663348] |
| T3 (5/4, 7/4) | SPLIT(5,7,3), SPLIT(7,5,1) | both return | -0.101 | [0.966468, 0.967365] |
| T2 (7/2, 3/4), (3/2, 7/4) | SPLIT(3,7,d), SPLIT(7,3,d) | expanding loop | +0.068 | 1, positive measure (Ω5) |

The SPLIT(3,5,1) upper value is the prover's certificate (θ = 2.295, U = 0.66334735...); it was
previously misquoted as 0.663347. The referee's independent certificate (θ = p/997) gives the
sharper upper bound 0.663345 (true log_2 ρ_* = 0.6633452).

The two open catalog maps differ sharply. Both have the same drift, but split5_1's non-descending
set is much fatter (dimension 0.937 against 0.581). This explains why the descent-tree and range
methods of earlier rounds went much further for split5_3: exceptional density 1.1e-6 at 2^32,
range 2^66, and 6.18e10 cycle steps, against split5_1's 2^46 range and 29 runs.

**Theorem Ω4 (counting non-descending starts).** For every SPLIT(a,b,d) and every θ >= 0,
#{1 <= n <= X : T^j(n) >= n for all j >= 0} = O(X^{log_2 ρ(θ)}).

*Proof.* Let 2^m <= n < 2^{m+1}. Each block multiplies a value x by its slope times
1 + d/(c x) <= 1 + d/x, and halvings are exact. If the orbit never goes below n, all block-start
values are >= n, so after at most m digits the actual value is at most
P_j n (1 + d/2^m)^m <= 2 P_j n once m >= m_0(d). Never going below n then forces P_j >= 1/2 for
j <= m. The number of length-m words with P_m >= 1/2 is at most 2^θ 1_U^T M_θ^m 1 = O(ρ(θ)^m), and
by the bijection each word is the residue of at most one n in [2^m, 2^{m+1}). Sum over m. ∎

For split5_3 this gives O(X^{0.58069}). That is between round 2's O(X^{0.585}) and its sharper
O(X^H/(log X)^{3/2}), and the method is uniform over the family. For split5_1 it gives
O(X^{0.93686}), which appears to be new.

**Theorem Ω5 (positive drift).** For the members with (a,b) in {(3,7),(7,3)} (type T2 with
s·r = 21/8 > 2), Ω has positive Haar measure, so dim_H Ω = 1.

*Proof.* Under Haar measure the digits are fair coins and the excursions are i.i.d. The log-slope
X of one excursion is -log 2 with probability 1/2 and J log s + log r otherwise, with J geometric
(P(J = j) = 2^{-j-1}, E J = 1). So E X = (1/2) log(sr/2) = (1/2) log(21/16) > 0 and X >= -log 2.
Choose θ > 0 with ψ(θ) = E e^{-θX} < 1, possible since ψ(0) = 1 and ψ'(0) < 0. Then
P(some partial sum <= -K) <= e^{-θK}/(1 - ψ(θ)) < 1 for large K. With probability > 0 the first
excursion has J so large that its log-slope exceeds K. After that, with positive probability, no
later partial sum falls by K. By the end-point property of excursions, all digit prefixes then have
P_j >= 1. ∎

This shows that Ω has positive measure. It does **not** show that any positive integer diverges.

## 5. What this says about GLOBAL for split5_3

* The descent method is blocked exactly on Ω, a set of dimension 0.5807 and measure 0. The
  integer question is whether Ω (shifted, in the y = n + 3 coordinate of round 2) contains a positive
  integer whose orbit never gets a crossing. Round 2 proved the equivalence of GLOBAL with "every
  integer y >= 4 eventually crosses" and verified all n < 2^66. Nothing here changes that status.
* Ω4 counts starts that never fall below themselves. A divergent orbit can contain only boundedly
  many such tail minima below any height X, at most O(X^{0.5807}) of them. This is the same
  obstruction as for every 3x+1-type problem: a density statement cannot exclude a single orbit.

## 6. The four lens questions

**(a) The induced map on (w, k).** With N = n + 3 = 4^k w (4 ∤ w), a run gives 5^k w and then one
exit block. This is round 2's map G(y) = 2^{b-1}(5^k u + 3), whose fixed points are exactly the
five known cycles (proved there). I found no well-founded order. A conjugacy to a known system is
excluded on all positive integers: an affine bijection of the positive integers is the identity
(lhf/mixed/CLS-049). An equivalence with a named problem is false within the parity family as far
as structure goes: no member of P or K has an Ω of the T1 type with c = 5. dim Ω is a
conjugacy-invariant of the 2-adic extensions, and the parity maps 3x+d, 5x+d, 7x+d have Ω of
dimension H_2(log 2/log 3) ≈ 0.9500, 1 (positive drift) and 1 respectively. So no affine 2-adic
conjugacy with them exists. (This last remark uses only that an affine 2-adic conjugacy is a
bi-Lipschitz map of Z_2 that preserves digit-prefix slopes up to a bounded factor. I state it as
EVIDENCE that no such reduction exists, not as a theorem about all possible reductions.)

**(b) The rising family 4^K - 3.** After K blocks the orbit is at 5^K - 3. Whether it later falls
below 4^K - 3 is decided by the binary digits of 5^K: in the (z, s) coding of round 2 the
digit walk of y = 5^K (started with linear multiplier (5/4)^K relative to 4^K) must lose a factor
(5/4)^K, which takes on the order of K digits. The low j digits of 5^K are periodic in K with period 2^{j-2}, so any finite digit
depth decides only finitely many residue classes of K. Round 2 proved that such class-wise
certificates cover 46,055 of the 65,536 classes mod 2^16 and cannot cover all large K. The
question is a statement about the 2-adic digit statistics of the powers of 5, of the same kind as
open questions on the digits of 2^n in base 3. **OPEN.** Verified for 4 <= K <= 2000 in round 2.

**(c) Ancestor arguments.** The minimal counterexample n_0 has no smaller ancestor. The simplest
instance: every n = 2 (mod 5) has the smaller ancestor (4n - 3)/5, which is 1 (mod 4) and has
5·((4n-3)/5) + 3 = 4n, then 2n, then n. So **n_0 ≢ 2 (mod 5)**, and more generally
5^a ∤ 2^h n_0 + 3 whenever (4/5)^a 2^h (n_0 + 3) < n_0 + 3 (round 2's mod-625 trick is h = 1,
a = 4). How thin can this make the candidate set? Round 2's two-sided theorem settles it for
bounded depth. For every D >= 40, more than three quarters of the starts n = -3 (mod 4^D) in
[16^D, 2·16^D) have no merger with a smaller start within D blocks on both sides. So **no
bounded-depth ancestor-plus-descent search can exclude more than a fraction 1/4 of the
non-descending candidates** in these progressions. That is the provable limit of approach (c).

**(d) The set Ω and its dimension.** Settled by Theorem Ω1: Ω is described exactly by the
weighted digit walk, and dim_H Ω = H_2(1 - 2/log_2 5) = 0.58068412319... .
