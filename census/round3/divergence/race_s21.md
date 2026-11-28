# race_s21: a "two-counter race" map

**Rule (non-injective; affine on each class mod 210).**

| condition | R(n) | effect on (a, b, g, e) = (v₂, v₃, v₅, v₇) |
|---|---|---|
| 5 \| n, 7 \| n | 6n/7 | (a+1, b+1, g, e−1) (R1, fall) |
| 5 \| n, 7 ∤ n | 3n/5 | (a, b+1, g−1, e) (R2, fall) |
| 5 ∤ n, 6 \| n | 49n/6 | (a−1, b−1, g, e+2) (S1, rise) |
| 5 ∤ n, n odd, 3 \| n | 5n | (a, b, g+1, e) (S2, rise) |
| 5 ∤ n, n even, 3 ∤ n | n/2 | (a−1, b, g, e) (S3, fall) |
| gcd(n, 30) = 1 | n | fixed point (S4) |

The cofactor m = n / (2^a 3^b 5^g 7^e) is never changed. R is not injective,
for example R(2) = 1 = R(1). It is a FRACTRAN-type ("residue-class-wise
linear") map with 5 as a phase flag and three counters a, b, e. No catalog entry
is of this type with these rules.

**Questions.** (i) GLOBAL: which orbits are eventually periodic, and what are
the cycles? (ii) FATE of 21. (iii) The certificate question for this lens: which
bases admit an automatic divergence certificate for 21, and of what size?

| question | answer | status | tier |
|---|---|---|---|
| cycles | exactly the fixed points n with gcd(n,30)=1 | PROVED | 1 |
| divergent set | D = {n : v₂(n) < v₃(n) + v₅(n)}; every other orbit reaches a fixed point | PROVED | 1 |
| FATE of 21 | infinite; R^{t_k}(21) = 2^{2^k} 3^{2^k+k+2}; falls in every round | PROVED | 1 |
| base-6 certificate | C = {v₂ < v₃} = "last nonzero base-6 digit is 3", minimum exactly 2 states | PROVED | — |
| bases 2^j and 3^j | no automatic certificate of any size; hence no congruence certificate at any modulus | PROVED | — |
| bases 5, 7, 10, … | not determined | OPEN | — |

The dynamics are tier 1, a counter-machine calculation. The point of the system
is the certificate landscape. It is the requested example where **base 2 fails
provably, for every automaton size, while another base works**, and where the
certificate is a two-counter comparison v₂ < v₃.

## (i) GLOBAL

Write n = 2^a 3^b 5^g 7^e m with gcd(m, 210) = 1.

*Phase R (5 | n).* R1 applies while 7 | n, then R2 applies while 5 | n. From
(a, b, g ≥ 1, e) this reaches (a+e, b+e+g, 0, 0) after e + g steps and enters
phase S.

*Phase S (5 ∤ n).* If a, b ≥ 1, S1 applies. It preserves b − a and lowers
min(a, b) by 1. After min(a, b) steps:

* a ≥ b: we reach (a−b, 0, 0, e+2b). Then S3 halves down to a = 0, and S4 fixes
  the result, n = 7^{e'} m, which is coprime to 30.
* a < b: we reach (0, c, 0, e') with c = b − a ≥ 1. This is a *round start*.

*Rounds.* From a round start (0, c, 0, e): S2 gives (0, c, 1, e), R1^e gives
(e, c+e, 1, 0), R2 gives (e, c+e+1, 0, 0), and S1^e gives (0, c+1, 0, 2e). This is
again a round start, reached after 2e + 2 steps. The value 3^c 7^e m becomes
3^{c+1} 7^{2e} m, which is strictly larger. So every orbit that reaches a round
start is unbounded.

Combining the phases: n diverges iff it reaches a round start, iff v₂ < v₃ (when
5 ∤ n), resp. v₂ < v₃ + v₅ (when 5 | n). Every other orbit ends at a fixed point
coprime to 30. A cycle cannot contain a round start, because values grow from
round to round. So the cycles are exactly the fixed points. ∎

## (ii) FATE of 21

21 = 3·7 is the round start (c, e) = (1, 1). Round k starts at 3^{1+k} 7^{2^k}.
After 2 + 2^k further steps it passes P_k = 2^{2^k} 3^{2^k+k+2} (the R2 exit).
So the orbit is infinite. It begins 21, 105, 90, 54, 441, 2205, 1890, 1620, 972, ….
Every round contains falls (R1, R2) and rises (S1, S2). Round lengths grow, so
the itinerary is not eventually periodic. The closed form makes the divergence
proof tier 1.

## (iii) Certificates

A divergence certificate is C with R(C) ⊆ C, R(21) ∈ C, and no periodic point in
C (see `theorem2_quotient.md`).

**Base 6, exactly 2 states.** Let C = {n : v₂(n) < v₃(n)}.

* *Closure.* Take n ∈ C, so b ≥ 1. R1 gives (a+1, b+1), R2 gives (a, b+1), S1
  gives (a−1, b−1), and S2 gives (0, b). S3 and S4 need b = 0, so they do not
  apply. Each image is in C.
* *No periodic point.* The periodic points are coprime to 3, and C requires
  b ≥ 1.
* *Contains R(21) = 105 = 3·5·7.* Indeed (a, b) = (0, 1).
* *Base-6 recognizer.* Write n = 6^k n' with 6 ∤ n'. Then
  v₂ < v₃ ⟺ (n' odd and 3 | n') ⟺ n' ≡ 3 (mod 6) ⟺ the last nonzero base-6 digit
  of n is 3. The DFA has states {0 = "last nonzero digit ≠ 3", 1 = "= 3"}.
  Digit 0 keeps the state, digit 3 goes to state 1, other digits go to state 0.
  It accepts state 1.
* *Minimal.* A 1-state DFA accepts everything, which includes the fixed point 1,
  or nothing, which excludes R(21). So the minimum is exactly 2.

The check verifies closure exactly over all n (autolib.closure_violation on the
210-branch table) and verifies that C has no member coprime to 30 (product
automaton with n mod 30).

**Bases 2^j and 3^j: none of any size.** Use Corollary Q.

* *Forced in:* P_k = 2^{2^k} · 3^{b_k} with b_k = 2^k + k + 2.
* *Forced out:* every 2^A 3^B with A ≥ B. Its orbit reaches the fixed point
  7^{2B}, so a certificate cannot contain it.
* *Base 2:* x_k = 3^{b_k} ∈ C/2^{2^k}. For j > k ≥ 2, 2^j ≥ 2^k + k + 2 = b_k, so
  2^{2^j} x_k is forced out and x_k ∉ C/2^{2^j}. The sets C/2^{2^k} (k ≥ 2) are
  pairwise distinct, so C is not 2-automatic. The same holds for 2^j, as in
  Theorem 2.
* *Base 3:* y_k = 2^{2^k} ∈ C/3^{b_k}. For j < k with k ≥ 3, b_j = 2^j + j + 2 ≤ 2^k,
  so 3^{b_j} y_k is forced out. The sets C/3^{b_k} are pairwise distinct, so C is
  not 3-automatic.

Periodic sets are automatic in every base. So **no union of residue classes, at
any modulus, is a divergence certificate for 21** (with any finite set added,
since a finite modification of an automatic set is still automatic).

**Other bases: OPEN.** For bases coprime to 6, Lemma Q gives nothing. A
certificate there would have to be non-periodic, by the corollary above.

## Why this is the expected picture

By Theorem 1, a base-b automaton beats a congruence only when the slopes are
not all powers of b. Here the dynamics are a race between the 2-adic and 3-adic
counters. The invariant "v₂ < v₃" is invisible to base 2 and base 3 separately:
each sees only one counter, as trailing zeros. Base 6 sees min(v₂, v₃) as
trailing zeros and the sign of v₂ − v₃ as the last nonzero digit. This is a
two-counter certificate in the sense of the task, and it happens to be
6-automatic.

**Novelty:** new system; FRACTRAN-type maps go back to Conway, but this map and
the certificate result are, to my knowledge, new. Literature novelty: not checked.

Check: `check_race_s21.py` (exit 0, about 2 s).
