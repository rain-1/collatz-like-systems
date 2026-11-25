# Lens "descent": shared definitions and lemmas

All systems here are maps `T(n) = (u_r n + v_r) / w_r` for `n ≡ r (mod Q)`,
with `Q = p^m` (p = 2 or 3), `w_r` a power of p, and exact division on the
whole class. Because the branch depends only on `n mod p^m` and the division
is exact on the class, the same formulas define a continuous extension
`T̂ : Z_p → Z_p`. Over one step the multiplier is `u_r / w_r`.

**Certificate (the task's definition).** A modulus M and, for each residue r
mod M, a step count `j(r) ≤ k` such that `T^{j(r)}(n) < n` for every
sufficiently large `n ≡ r (mod M)`.

## Lemma C (the minimal stopping-time certificate; how the engine works)

`descent_lib.certificate` works on classes `n = p^K t + r` (t ≥ 0). On such a
class it carries `T^j(n) = P t + R` exactly. If every value `P t + R` lies in
a single table row, it applies one step. If not, it splits t into p classes.
It closes a class at the first j ≥ 1 with `P < p^K`, or with `P = p^K` and
`R < r`.

* While a class is open, `P > p^K`, or `P = p^K` and `R ≥ r`. Then
  `T^j(n) ≥ n` for infinitely many n in the class (for P > p^K, all large
  ones). So no certificate can give that class, or any class containing it,
  a step count j at which the node was still open.
* Each p-adic integer x has a first descent time τ(x) ≤ ∞. Its leaf, if it
  has one, is closed exactly at τ(x). Suppose τ(x) < ∞ for every x. The
  closed cylinders then form an open cover of the compact space `Z_p`, so a
  finite subcover exists and the search terminates (König's lemma). The
  converse is Lemma B.
* **Lower bound on k.** Let the deepest leaf have j = k. Take any certificate
  and the class r mod M that contains integers 2-adically close to that
  leaf's points. At every j' < k this class contains infinitely many n with
  `T^{j'}(n) ≥ n`, by the first bullet. Hence **every certificate has k at
  least the k of the minimal stopping-time certificate.** I do *not* claim
  that the reported moduli are minimal. A coarser class with a single larger
  j is not excluded.

`verify_certificate` checks the output independently. The densities of the
leaves sum to 1, the leaves form a prefix code, and each stored affine form
equals the real iterate when tested at several t, including t = 1000003.

## Lemma A (certificate ⇒ GLOBAL and the complete cycle list)

Take a leaf with `P < M = p^K`. Then `T^j(n) < n` for all
`t > (R − r)/(M − P)`. Let E be the finite set of positive n that lie in a
leaf with `t ≤ ⌊(R − r)/(M − P)⌋`. Every positive n outside E has a later
iterate smaller than itself. Since T maps positive integers to positive
integers, iterating this from any n gives a strictly decreasing chain, and
the chain must enter E. So every orbit meets E, and the orbits from E can
be simulated until they repeat. Therefore every orbit is eventually
periodic. Also, the minimum of a cycle cannot descend, so it lies in E.
**The cycles are exactly the cycles reached from E**, which gives a complete
list.

## Lemma B (a growing p-adic periodic point kills every certificate)

Let `x* ∈ Z_p` be T̂-periodic with period L and multiplier
`λ = Π u/w > 1` over one period. Write the logs of the per-step multipliers
around the cycle as `s_1..s_L`, with positive sum. By the cycle lemma,
starting just after the *last* minimum of the prefix sums, every partial sum
of the periodic sequence is > 0. So there is a point y on the orbit with
`λ_j(y) > 1` for all j ≥ 1 (checked exactly by `verify_obstruction`).

Now take any certificate (M, j(·)) and write `M = p^s M'` with `p ∤ M'`.
Pick r with `r ≡ y (mod p^s)` and set `j = j(r)`. Since T̂ is affine on
cylinders, there is an N ≥ s such that every `n ≡ y (mod p^N)` follows the
same branches as y for j steps. By CRT the integers with `n ≡ y (mod p^N)`
and `n ≡ r (mod M')` form an infinite progression inside the class r mod M.
On this progression `T^j(n) = λ_j(y) n + β` with `λ_j(y) > 1`, so
`T^j(n) > n` for all large such n. This contradicts the certificate. ∎

The rational periodic points used below are found as the maximum-mean cycle
of a cylinder graph (Karp's algorithm, floating point, used only for the
search). Each one is then re-verified exactly with Fractions.

## Lemma D (full blocks have fixed points)

Let `B(x) = (a x + c)/p^v` be affine on a cylinder C ⊂ Z_p, with p ∤ a and
v ≥ 1, and suppose `B(C) ⊇ C`. Then `B^{-1}` maps C into C and contracts
by `p^{-v}`, so it has a fixed point in C. That point is B-periodic with
multiplier `a/p^v`.

## Theorem 1 (SPLIT family: the middle tier is empty)

Let `T(n) = n/2` for even n, `a n + d` for n ≡ 1 (mod 4), and `b n + d` for
n ≡ 3 (mod 4), with a, b, d odd and positive. Set `v_a = 1` if
a + d ≡ 2 (mod 4) and `v_a = 2` otherwise. Set `v_b = 1` if 3b + d ≡ 2
(mod 4) and `v_b = 2` otherwise. Then the following are equivalent:

* a descent certificate exists;
* `a < 2^{v_a}` and `b < 2^{v_b}`;
* one block suffices (k ≤ 3).

So the certifiable members are exactly (1,1,any d), (3,1,d ≡ 1 mod 4) and
(1,3,d ≡ 3 mod 4). All of them are tier 1.

*Proof.* On n ≡ 1 (mod 4), `v_2(a n + d) ≥ v_a`, because a n + d ≡ a + d
(mod 4). This gives `T^{1+v_a}(n) = (a n + d)/2^{v_a}`, which is < n for
large n when `a < 2^{v_a}`. The 3-class is the same. Conversely, suppose
`a > 2^{v_a}`. Let `x = d/(2^{v_a} − a)`. For v_a = 2 we have d ≡ −a, so
x ≡ −d·a ≡ a² ≡ 1 (mod 4). For v_a = 1 we have d ≡ 2 − a, so x ≡ 1. In both
cases `(a x + d)/2^{v_a} = x` is odd, so the halvings stop exactly there.
Then x is T̂-periodic with multiplier `a/2^{v_a} > 1`, and Lemma B applies.
For b: if v_b = 2 then d ≡ b, so x ≡ b/(−b) = −1 ≡ 3. If v_b = 1 then
x ≡ (2 + b)/(2 − b) ≡ 3 (mod 4) for both b ≡ 1 and b ≡ 3. ∎
`check_desc_split7_1.py` confirms this against the exhaustive engine for
all a, b ≤ 31 and d ∈ {1, 3, 5, 7} (1024 triples).

## Theorem 2 (M3 family: the middle tier is empty)

Let `T(n) = n/3` for 3 | n, `a n + c1` for n ≡ 1 (mod 3), and `b n + c2`
for n ≡ 2 (mod 3), with 3 ∤ ab. Because a and b are 3-adic units, class 1
maps onto the full class `i1 = a + c1 (mod 3)`, and class 2 maps onto
`i2 = 2b + c2`. A certificate exists iff
(i1, i2) = (0, 0) with a, b ≤ 2, or (2, 0) with ab ≤ 2 and b ≤ 2, or
(0, 1) with ab ≤ 2 and a ≤ 2. In each of those cases a block of at most
3 steps works.

*Proof.*
* If a nonzero class maps into a loop of nonzero classes (i1 = 1, i2 = 2,
  or 1 ↔ 2), then on that class `T^j(n) ≥ n` for all j, so no certificate
  exists.
* Otherwise each orbit passes through 0 within 2 steps, and the blocks
  1 → 0, 2 → 0, 1 → 2 → 0 and 2 → 1 → 0 are full (their image is Z_3).
  Lemma D then gives a periodic point with multiplier a/3, b/3 or ab/3.
  Any such multiplier > 1 kills certificates (Lemma B). If all of them are
  < 1, the block itself is the certificate. ∎

`check_desc_m3_4n5.py` confirms this against the engine for a, b in
{1, 2, 4, 5, 7, 8} and c1, c2 in 0..8 (2916 cases).

**Why round 1 was bimodal.** In both natural families the branch is chosen
by the same modulus the guaranteed division uses. Every block is then full,
so the symbolic dynamics is a full shift on blocks. The maximal Lyapunov
exponent is attained by a single block repeated, so "some certificate
exists" collapses to "a one-block certificate exists". A tier-2 middle
needs blocks whose image is a *proper* sub-cylinder. That happens when the
branch is chosen modulo 2^m but fewer than m halvings are guaranteed (for
example 3n+1 on a class mod 32 with exactly one halving). Those restrictions
turn the block dynamics into a subshift of finite type, where long
near-critical cycles appear.

## The S-family census (`family_scan.py`, output in `family_scan.out`)

`T_S(n) = n/2` for even n, `3n + 1` if `n mod 2^m ∈ S`, `n + 1` otherwise.
Every subset S was classified exactly as CERT (certificate found) or OBST
(verified growing 2-adic cycle). No case was left UNKNOWN for m ≤ 5.

| m | subsets | CERT  | OBST  | max \|S\| certifiable | number of sets of max size | deepest certificate (k steps, level K, classes) |
|---|---------|-------|-------|------------------------|----------------------------|-------------------------------------------------|
| 2 | 4       | 2     | 2     | 1 of 2                 | 1                          | S={1}: 3, 2, 3                                  |
| 3 | 16      | 6     | 10    | 2 of 4                 | 2                          | S={3,5}: 6, 4, 6                                |
| 4 | 256     | 84    | 172   | 6 of 8                 | 2                          | S={1,3,7,11,13}: 14, 10, 30                     |
| 5 | 65536   | 16656 | 48880 | 12 of 16               | 17                         | S={1,3,5,7,11,15,17,23,25,29}: 46, 30, 802      |

The exact rows for m = 4 and 5 are in `family_scan.out`. At m = 5 the
verified obstructions have periods 2, 5, 6, ..., 18, so the shortest
obstruction can be long. A greedy search at m = 6 (not exhaustive) found
S = {1,3,5,9,11,13,17,19,21,23,25,27,29,31,33,35,37,41,43,45,47,49,51,53,55,57,61}.
That is 27 of the 32 odd classes. Its certificate is small: level 10,
k = 13, 19 classes, and E = {1}. So by Lemma A every orbit of that map
reaches 1. The density of 3n+1 classes compatible with a certificate
therefore goes above 3/4, and certificate depth does not grow with density.

## Heuristic (evidence only)

`odd_markov_drift` gives the expected log growth per odd step when the
higher binary digits are uniformly random. It uses the Markov chain on odd
classes mod 2^m induced by "one odd step, then all halvings". It is used
only to show that the uncertifiable systems are *expected* to converge.

## Referee note (round 2)

**Proposition (referee).** Consider a map with even n ↦ n/2 and odd branches chosen mod 2^m. Let G_m be the mod-2^m transition graph: an odd r has the single edge to (u r + v) mod 2^m, and an even r has edges to r/2 and r/2 + 2^{m−1}. The following are equivalent:

1. a plain descent certificate exists;
2. every cycle of G_m has a product of multipliers < 1;
3. there is a one-step weighted potential V(n) = n·c(n mod 2^m).

**Proof sketch.**

* (2 ⇒ 3) Use longest-path weights, built exactly as in `referee_check.py`.
* (3 ⇒ global descent) This gives the conclusion of Lemma A, with a finite check up to an explicit bound B.
* (not 2 ⇒ no certificate) The 2-adic points that follow a graph cycle form a cylinder. The composed affine map sends that cylinder onto the starting class, so Lemma D gives a periodic point. That periodic point has the cycle's multiplier, and since 3^a = 2^b is impossible, that multiplier is > 1. Lemma B then applies.

**Computational check.** For all 256 subsets at m = 4, and for a random sample of 150 subsets at m = 5, certificate existence agreed with sign(max-mean of G_m) in every case.

**Consequences.**

* Certifiability in the S-family is decided by Karp's algorithm on 2^m nodes.
* The large k values (44, 46) are properties of the plain T^j(n) < n format, not of the difficulty of the problem. Each certifiable member also has a one-step proof with 2^m weights.
