# The split / splitB family on Z and on rationals with odd denominator

Check: `check_split_family.py` (N1–N4, P; about 15 s in total, including the 1x+d part).

## One map for the whole family

For odd d ≥ 1, let

  `M_d(n) = n/2 (n even);  3n + d (n·d ≡ 1 mod 4);  n + d (n·d ≡ 3 mod 4)`  on Z.

* d ≡ 1 (mod 4): M_d is catalog **split_d** (n ≡ 1 ↦ 3n+d, n ≡ 3 ↦ n+d).
* d ≡ 3 (mod 4): M_d is catalog **splitB_d** (n ≡ 1 ↦ n+d, n ≡ 3 ↦ 3n+d).

Put x = n/d. Then `M_d(n) = d·S(n/d)`, where S is the single 2-adic map

  `S(x) = x/2 (x even);  3x + 1 (x ≡ 1 mod 4);  x + 1 (x ≡ 3 mod 4)`  on Z_(2) ∩ Q.

This works because d^{-1} ≡ d (mod 4), so x ≡ n·d (mod 4). **The whole split/splitB
family on Z is the single map S on the lattices (1/d)Z, d odd.** These are the
rationals with a fixed odd denominator d that the lens asks about, and every d is
admissible. Round-2 Theorem 1 shows that S, together with 1x+1, is exactly the
certifiable part of the SPLIT(a, b, d) family.

## Theorem S1 (complete cycle classification, PROVED)

For every odd d ≥ 1:

1. Every M_d-orbit on Z is eventually periodic.
2. The cycles of M_d on Z are {0} together with one cycle for each primitive necklace w
   over {A_k, B_k : k ≥ 2} with d·x_w ∈ Z. Here x_w = c_w/(2^K − 3^a) (theorem_N.md).
   That cycle's odd points are d·x_{w′} for the rotations w′ of w. All of them lie in
   [1, d].
3. There are no negative cycles.

*Proof.* Theorem N applies to S (theorem_N.md, split instance) with λ = 3/4 and M = 1/4
(the block A_2), so part 4 gives 1 and 2. Part 3 of Theorem N gives
0 < x_w ≤ 1, so the odd points d·x_w lie in [1, d]. Item 3 follows from item 2. ∎

Check N3 recomputes the cycles of M_d by simulation from [−d, d] for every odd
d ≤ 401. It confirms that each cycle's word reproduces its odd points exactly by the
formula, and that every necklace with K ≤ 13 and d·x_w ∈ Z appears.

Equivalently, **the number of positive cycles of split_d / splitB_d equals the number of
primitive necklaces w with (2^K − 3^a)/gcd(c_w, 2^K − 3^a) dividing d.** This is a
Böhm–Sontacchi-type formula for the whole family, uniform in d. For example,
split_7081 has 10 positive cycles, with minima 1, 11, 41, 291, 485, 569, 713, 949,
2409 and 7081 (theorem_Z.md).

## Theorem S2 (negative integers, PROVED)

*Let d be odd with 3 ∤ d. A negative n reaches 0 iff d | n. Every other negative n
reaches a positive value after finitely many steps. If 3 | d, every negative orbit
still either reaches 0 or becomes positive.*

*Proof.* There are no negative cycles and every orbit is eventually periodic (S1), so a
negative orbit ends at 0 or becomes positive. In x = n/d, the exact denominator of x is
preserved by x/2 and x + 1. It is also preserved by 3x + 1 when 3 ∤ (denominator),
since gcd(3a + e, e) = gcd(3a, e). So with 3 ∤ d only x ∈ Z (that is d | n) can reach
0. Conversely, a negative integer x stays ≤ 0: if x ≡ 1 (mod 4) and x ≤ −3 then
3x + 1 ≤ −8, and if x ≡ 3 (mod 4) and x ≤ −1 then x + 1 ≤ 0. So it reaches 0. ∎

When 3 | d, −1/3 ↦ 0 also, and the basin of 0 among the negatives is more complicated.
For d = 3 every negative n reaches 0, because a negative third that is ≡ 3 (mod 4) is
≤ −5/3. For d = 9 the share is 2659 of the first 3000. This is EVIDENCE only and is not
classified.

Subsequent classification for $d=9$. The negative start $-u$ crosses into the positive cycle through 3 precisely when $u$ is generated from 1 or 5 by $u\mapsto2u$ and $u\mapsto4u+9$. Every other negative start reaches zero. [Proof and counting exponent, Theorem 3](../../../output/pdf/stopping_time_applications.pdf)

## Theorem P (when is the basin a congruence rule?, PROVED)

Let f(n) be the cycle reached by n ≥ 1 under M_d. Let 𝒢_d be the graph on Z/d with
edges ρ — 2ρ and ρ — 3ρ, and call its connected components the **weak components** of
Z/d. Since M_d acts on residues mod d as multiplication by 2^{-1}, 3 or 1, every orbit
stays in one weak component. Every component contains at least one cycle.

*Theorem P. f is ultimately periodic (f(n + P) = f(n) for some P ≥ 1 and all
n ≥ N_0) if and only if every weak component of Z/d contains exactly one cycle of M_d.
In that case f(n) = the unique cycle in the component of n mod d.*

*Proof.* "If": a component with exactly one cycle C receives every orbit that starts in
it, so f(n) = C depends only on n mod d.

"Only if": suppose f(n + P) = f(n) for n ≥ N_0. Write P = 2^u m′ with m′ odd.

* (i) f(2n) = f(n) for every n, since 2n ↦ n is one halving step.
* (ii) Choose e ≥ u with 2^e ≡ 1 (mod m′). If n, n′ ≥ N_0 and n ≡ n′ (mod m′), then
  2^e n ≡ 2^e n′ (mod P): both are 0 mod 2^u and both are ≡ n mod m′. So
  f(n) = f(2^e n) = f(2^e n′) = f(n′). Hence f(n) = h(n mod m′) for n ≥ N_0.
* (iii) For each residue ρ mod m′, CRT gives odd n ≥ N_0 with n ≡ ρ (mod m′) and
  n·d ≡ 3 (mod 4). For such n, f(n) = f(n + d), so h(ρ) = h(ρ + d). With n·d ≡ 1
  instead, h(ρ) = h(3ρ + d). With (i), h(ρ) = h(2ρ).
* (iv) Translation-invariance by d makes h a function h̄ of ρ mod g, where
  g = gcd(d, m′). Since g | d, h̄(3ρ) = h̄(ρ) and h̄(2ρ) = h̄(ρ). So h̄ is constant on the
  weak components of Z/g.
* (v) Reduction Z/d → Z/g maps edges to edges, so each weak component of Z/d lands
  inside one weak component of Z/g. Suppose a component K of Z/d contains two cycles
  C_1 ≠ C_2 with c_i ∈ C_i. Take j large. Then f(2^j c_i) = C_i, and 2^j c_1, 2^j c_2
  are ≥ N_0 with residues in the same component of Z/g. So
  C_1 = h̄(·) = C_2, a contradiction. ∎

The argument is the split-family analogue of the qrA3_q17 "no congruence rule" proof
(round2/qr/qrA3_q17.md). The difference is that S has no tripling identity
f(3n) = f(n); the translation identities f(n) = f(n + d) and f(n) = f(3n + d) take its
place.

**Data (check P).** For odd d ≤ 1001, the basin is a congruence rule for 185 of the 501
values. The values d ≤ 200 with a periodic basin are 1, 5, 7, 11, 17, 19, 23, 25, 35,
37, 41, 43, 47, 49, 53, 59, 71, 73, 77, 79, 83, 89, 95, 97, 101, 103, 107, 115, 121,
133, 137, 149, 151, 157, 163, 173, 175, 179, 181, 185, 191, 193, 197, 199. (Every
multiple of 3 fails. There d/3·{1,4,2} and d·{1,4,2} lie in the same component, which
contains 0.)

## The catalog members: exact basins (PROVED)

| catalog | d | positive cycles (minima) | weak components → cycles | basin rule |
|---|---|---|---|---|
| split_5 | 5 | 1, 5 | {0}→5, units→1 | 5 ∣ n → (5 20 10); else → (1 8 4 2). This is the round-1 rule. |
| splitB_7 | 7 | 1, 7 | {0}→7, units→1 | 7 ∣ n → 7-cycle; else → cycle of 1 (⟨2,3⟩ = (Z/7)^*) |
| split_73 | 73 | 3, 5, 73 | {0}, QR, NQR | 73 ∣ n → 73-cycle; (n/73) = +1 → cycle of 3 (length 12); (n/73) = −1 → cycle of 5 (length 28) |
| split_97 | 97 | 13, 33, 97 | {0}, QR, NQR | 97 ∣ n → 97-cycle; (n/97) = +1 → cycle of 33; (n/97) = −1 → cycle of 13 |
| splitB_71 | 71 | 1, 11, 71 | {0}, QR, NQR | 71 ∣ n → 71-cycle; (n/71) = +1 → cycle of 1 (length 20); (n/71) = −1 → cycle of 11 (length 18) |
| split_13 | 13 | 1, 5, 13 | {0}→13, units→{1, 5} | **no** congruence rule (Theorem P) |
| split_7081 | 73·97 | 10 cycles | 9 components, one holding 569 and 713 | **no** congruence rule (Theorem P) |

For 71, 73 and 97 the check confirms ⟨2, 3⟩ = the quadratic residues. That works because
2 and 3 are squares modulo these primes (p ≡ ±1 mod 8 and p ≡ ±1 mod 12). Each rule is
also confirmed on n ≤ 2·10^5, though by Theorem P the rule is already proved. On Z:
add "n ≤ 0, d ∣ n → 0" (Theorem S2). A negative non-multiple follows the same residue
rule, because it becomes positive inside its component.

## Status of each question

| question | status |
|---|---|
| all orbits of M_d on Z eventually periodic, every odd d | PROVED (tier 1) |
| complete cycle list for every d (necklace formula); lists for d ≤ 401 recomputed | PROVED |
| no negative cycles; fate of negatives for 3 ∤ d | PROVED |
| fate of negatives for 3 ∣ d | partly: they reach 0 or become positive (PROVED); which is EVIDENCE |
| basin a congruence rule ⇔ one cycle per weak component | PROVED |
| catalog d = 5, 7, 71, 73, 97 exact basins (Legendre symbol) | PROVED (new for 71, 73, 97) |
| split_13, split_7081 exact basins | OPEN. Not a congruence rule (PROVED). Whether some automaton decides them is open, as for qrA3_q17. The Cobham-type argument of qrA3_q17 needs f(pn) = f(n) for some p independent of the base. Here only p = 2 is available, so at best it would cover bases that are not powers of 2. Not attempted. |

Novelty: as far as I know the split family has not been studied outside this census.
Novelty not checked.
