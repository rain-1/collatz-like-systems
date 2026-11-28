# Theorem Z: settled catalog maps on all of Z

Check: `check_theorem_Z.py` (about 3 s; it exits 0).

## Setting

A residue-class affine map is given by a modulus Q ≥ 1 and a table
`n ≡ r (mod Q) ↦ (u_r n + v_r)/w_r`, with u_r, w_r > 0 and the division exact on the
whole class. The class is a set of integers of both signs, so the same table defines
T on all of Z. In this lens, "the map on Z" always means this table extension.

A **strict Z-certificate** is a finite partition of Z into classes `n = L t + r`
(0 ≤ r < L, t ∈ Z). For each class it gives a step count j ≥ 1 and integers P, R with
`T^j(L t + r) = P t + R` for **every** t ∈ Z, and with `0 < P < L`.

`gdescent.certificate` finds one by the minimal stopping-time tree of
`census/round2/descent/lemmas.md` (Lemma C). It splits t ↦ Qt′ + s while the branch of
`P t + R` is not constant in t, and it closes a node as soon as `P < L`. Unlike the
round-2 engine, it never closes on `P = L, R < r`. `gdescent.verify` checks
independently that the classes partition Z (Σ 1/L = 1 and the classes form a prefix
code), that `0 < P < L`, and that every affine form equals the true iterate at nine
values of t, of both signs and up to 10^15.

Validity for all t ∈ Z: along the path to a leaf every branch was chosen because
`P t + R mod Q` lies in one table row for every integer t. Exact divisibility
`w | uP` and `w | uR + v` was required for all t. So the identity is polynomial in t
and holds on all of Z, not only for t ≥ 0.

## Theorem Z

*If T has a strict Z-certificate, then every orbit of T on Z is eventually periodic.
Every orbit enters the finite set*

  `E_Z = { n = L t + r in a leaf : |P t + R| ≥ |L t + r| }`,

*and the cycles of T on Z are exactly the cycles reached from E_Z.*

*Proof.* In a leaf, |P t + R| ≥ |L t + r| forces `L|t| − |r| ≤ P|t| + |R|`, that is
`|t| ≤ (|R| + |r|)/(L − P)`. So E_Z is finite (`gdescent.exceptional_Z` enumerates the
t-range and tests each t exactly). Every n ∉ E_Z has an iterate T^j(n) with
|T^j(n)| < |n|. Starting from any n, repeat this while the current point lies outside
E_Z. The absolute values strictly decrease, so this stops after finitely many steps,
at a point of E_Z. The orbits of the finitely many points of E_Z are simulated until
they repeat, so every orbit is eventually periodic. A point of a cycle with minimal
|·| cannot have a later iterate of smaller absolute value, so it lies in E_Z. ∎

This is Lemma A of round 2 with n replaced by |n|. The one new point is that a
certificate whose leaves all satisfy P < L works on both sides of 0. A leaf with
`P = L, R < r` gives `T^j(n) = n − (r − R)`. That is a descent for n > 0 but an
*ascent* in |n| for n < 0, so such leaves are not allowed.

## Proposition S (sign of cycles)

*Suppose every branch has u > 0, w > 0 and v ≥ 0. Let x be a periodic point, in Z or in
any Z_(p) ∩ Q, with multiplier α (the product of the u/w around the cycle). Then
x(1 − α) = β ≥ 0. So x < 0 forces α > 1, or α = 1 and every constant met along the
cycle is 0 (so β = 0). In particular such a map has a negative integer cycle only if
that cycle is expanding or is a degenerate cycle with α = 1 and all constants along it
equal to 0. In the expanding case (Lemma B of round 2, together with α ≠ 1) no descent
certificate exists, not even on the positive integers; Lemma B does not apply to the
degenerate case.*

*Proof.* Composing affine maps with positive slopes and nonnegative constants gives
`T^L(x) = α x + β` with α > 0 and β ≥ 0, where β is a sum of the constants met along the
cycle, each multiplied by a positive factor. If x < 0, then x(1 − α) = β ≥ 0 gives
1 − α ≤ 0. Either α > 1, or α = 1 and then β = x · 0 = 0, which forces every constant
met along the cycle to be 0. ∎

The degenerate case does occur within the hypotheses: the map n ↦ n/2 (n even),
n ↦ 2n (n odd) has u > 0, w > 0, v = 0 and the negative cycle {−1, −2} with α = 1, which
is not expanding. No application in this folder is affected: every negative-cycle
exclusion in this file comes from E_Z directly (Theorem Z), not from Proposition S, and
for the split/necklace maps it comes from β_w > 0.

So for this class of maps, the "negative expanding cycles" that make many maps wild on
Z are exactly the obstructions to a certificate. For example, the 3x+1 cycles through −1,
−5 and −17 have multipliers 3/2, 3^2/2^3 and 3^7/2^11, all > 1. Conversely, every catalog map settled by
a certificate below has no negative cycle. Every map in the table has positive slopes
and nonnegative constants (check Z2).

## Results (all PROVED; check Z1)

The strict Z-certificate is found and verified, E_Z is enumerated, and the cycles are
computed from E_Z. A cycle is given as (minimum, length).

| map (catalog name) | leaves, k | E_Z | all cycles on Z |
|---|---|---|---|
| par_1_1 | 2, 2 | [0,1] | (0,1), (1,2) |
| par_1_5 | 2, 2 | [−1,5] | (0,1), (1,6), (5,2) |
| split_5 | 4, 3 | [−1,5] | (0,1), (1,4), (5,3) |
| split_13 | 4, 3 | [−1,13] | (0,1), (1,5), (5,6), (13,3) |
| split_73 | 4, 3 | [−21,73] | (0,1), (3,12), (5,28), (73,3) |
| split_97 | 4, 3 | [−29,97] | (0,1), (13,12), (33,13), (97,3) |
| split_7081 | 4, 3 | 4385 pts in [−2357,7081] | (0,1) and 10 positive cycles, minima 1, 11, 41, 291, 485, 569, 713, 949, 2409, 7081 |
| splitB_7 | 4, 3 | [−1,7] | (0,1), (1,4), (7,3) |
| splitB_71 | 4, 3 | [−23,71] | (0,1), (1,20), (11,18), (71,3) |
| m3_a | 3, 1 | [0,2] | (0,1), (1,1), (2,1) |
| m3_c | 3, 2 | [0,2] | (0,1), (1,2), (2,2) |
| m3_f | 3, 2 | [0,1] | (0,1), (1,2) |
| desc_s8_35 | 15, 6 | {0,1} | (0,1), (1,2) |
| desc_s32_max | 869, 44 | {0,1} | (0,1), (1,3) |
| desc_s32_d65 | 869, 44 | 73 pts in [−25,1519] | (0,1) and the 8 positive cycles of round 2 |
| qrA3_q23 | 6, 1 | [−7,23] | (0,1), (1,4), (5,5), (23,1) |
| qrA3_q307 | 6, 1 | [−149,307] | (0,1), (1,18), (5,28), (7,18), (307,1) |
| qrA3_q95 | 6, 1 | [−43,95] | (0,1), (1,6), (5,6), (7,12), (19,2), (95,1) |
| qrA3_q17 | 6, 1 | [−7,17] | (0,1), (1,3), (5,3), (17,1) |
| qrA5_q251 | 10, 1 | [−159,251] | (0,1), (1,8), (3,8), (7,15), (9,8), (21,8), (251,1) |
| qrC_q311 | 60, 1 | [−189,311] | (0,1), (3,13), (11,16), (311,1) |
| qrB7_c53 | 4, 1 | [−11,33] | (0,1), (1,9), (3,3), (5,3), (7,2) |

In every case: **there is no negative cycle and no divergent negative orbit. The
cycles on Z are the positive cycles plus the fixed point 0.** (The certificates for
desc_s32_* use Q = 32 splitting, so they have 869 leaves rather than the 144 of round
2. The depth k = 44 is the same.)

**Basins on Z for the qr maps (PROVED).** For the A-family maps (n + qc)/p and for
qrC, gcd(n, q) is invariant, as in Lemma CD. In those maps a negative multiple of q
stays ≤ 0. For odd n = qm with m ≤ −1, the digit c ∈ [0, p−1] satisfies p | m + c,
and m + c ≤ p − 2, so m + c ≤ 0 and (qm + qc)/p ≤ 0. Halving keeps the sign. (Check Z1b.) By Theorem Z it reaches 0. Every other negative n can never reach 0 (gcd
invariance). It has no negative cycle to enter, so it reaches a positive cycle in its
coset, and the round-2 coset rule applies verbatim. So for qrA3_q23, q307, q95, qrA5_q251
and qrC_q311, the round-2 basin theorems extend to Z with one change: **negative
multiples of q go to 0, not to q.** For qrB7_c53 the negative multiples of 7 split
between 0 and the cycle (7 14). On 7Z the map is 7·T₁ with T₁(m) = m/2, (m+5)/2 for
m ≡ 3, (m+3)/2 for m ≡ 1 (mod 4). The split has a minimal four-state binary
classifier on the index |n|/7. Neither basin has a natural density among negative
multiples of 7. [Classification and proof](../../round2/qr/qrB7_c53.md#exact-basins-on-negative-multiples-of-seven)

## Maps settled on the positives by an elementary block argument

These have no strict certificate on Z. farkas2005 has the expanding fixed point 0 of
m ↦ 3m/2. farkas5m has the expanding fixed point 1 (1 ↦ (5−3)/2, multiplier 5/2). The
round-2 hand proofs extend once n is replaced by |n|.

**farkas2005 on Z (PROVED).** G(m) = (m+1)/3 if m ≡ 2 (3); (m+1)/2 if m odd; 3m/2 if m
even. *Cycles on Z: {0}, {1}. Every m ≤ −1 reaches 0, and every m ≥ 1 reaches 1.*
Proof: (m+1)/3 and (m+1)/2 have absolute value < |m| for |m| ≥ 2, and G(−1) = 0. For
even m ≢ 2 (mod 3), write m = 2^a c with c odd. The valuation-run identity
G^{2a+1}(m) = (c+1)/2 of round 2 uses only congruences, so it holds for every sign
(check Z3, exactly on [−10^5, 10^5] and on random 200-bit integers). Also
|(c+1)/2| ≤ (|m|/2 + 1)/2 < |m| for |m| ≥ 2. G maps Z_{≤0} into itself, and G(0) = 0,
G(1) = 1.

**farkas5m on Z (PROVED).** *Cycles on Z: {0}, {1}. Every n ≤ −1 reaches 0, and every
n ≥ 1 reaches 1.* The block identity T^{2a+1}(n) = (b+1)/2 for odd n ≢ 3 (mod 5) with
n − 1 = 2^a b holds for all signs (check Z3). The bound |(b+1)/2| < |n| holds for
|n| ≥ 2. Also T(−1) = −4, T(−4) = −2, T(−2) = 0.

**farkas_s27 on Z (PROVED).** R(n) = G(n+1) − 1 for every n ≠ 1 (check Z3), and
R(1) = 1. *Cycles on Z: {−1}, {0}, {1}. n ≥ 1 reaches 1, n = 0 is fixed, and n ≤ −1
reaches −1.* For n ≤ −1, the G-orbit of m = n+1 ≤ 0 stays ≤ 0 and reaches 0, so it
never passes through m = 2.

**yah_avoid15 on Z (PROVED).** (n ≡ 1, 5 mod 8 ↦ 1, else Collatz.) *Cycles on Z: {0},
{1}, {−1, −2}. Basins: 0 ↦ 0; n = −2^j (j ≥ 0) ↦ {−1, −2}; every other integer ↦ 1.*
The round-2 proof only uses congruences. An odd o ≡ 3 (mod 8) reaches the class 1/5 in
two steps. An odd o ≡ 7 (mod 8) with o + 1 = 2^a b (b odd) runs through
o_j = 3^j 2^{a−j} b − 1 to o_{a−2} ≡ 3 (mod 8). This works for every sign provided
b ≠ 0, that is o ≠ −1. The only odd number never caught is −1, and its basin is
{−2^j}.

**yah_avoid6 on Z (PROVED).** (n ≡ 6 mod 8 ↦ 1.) *Cycles on Z: {0}, {1, 4, 2}. Every
n ≠ 0 reaches 1.* The round-2 odd-iterate descent holds with |·|. For negative o,
|3o+1| = 3|o| − 1, so the bounds (3|o|+1)/4, (3|o|+1)/8 and (9|o|+5)/16 all stay
below |o|, and o = −1 goes −1 ↦ −2 ≡ 6 ↦ 1 (check Z3). So the three negative 3x+1
cycles (−1, −2), (−5, …), (−17, …) are all destroyed by the class 6 mod 8. That is
special to class 6: for yah_avoid15 the cycle (−1, −2) survives.

**perm_flip** (2q+1 ↔ 2q+2) is a product of 2-cycles on Z, including {−1, 0}. This is
trivial.

## Tier and novelty

These are tier 1 (an inequality with a small finite table) or, for desc_s32_*, tier 2
(a certificate plus a table). The observation that strict certificates are sign-blind,
and that for nonnegative-constant maps negative cycles are expanding cycles (apart from
the degenerate case α = 1 with all constants along the cycle equal to 0), is elementary. Novelty not checked; it is likely folklore.
