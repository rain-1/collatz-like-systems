# A divergent orbit in the polynomial system A3, despite negative drift (28 Nov 2026)

Status: PROVED below; exact check `check_a3_divergence.py` exits 0. Written by Fable outside the
prover/referee loop. An independent referee confirmed the theorem (`REFEREE.md`, own script
`referee_check.py`, which also runs the raw A3 orbit for 60000 steps); its four editorial fixes are
applied below. Paper: `../../../output/tex/a3_divergent_orbit.tex`.
This settles the item "U" left open in `../../round5/funcfield` for A3. It is a statement about
a polynomial map over F_3, not about one of the 66 integer census entries.

## The system

A3 acts on F_3[t]: if f(0) = 0, f -> f/t; if f(0) = 1, f -> (1 + t^2)(f - 1)/t; if f(0) = 2,
f -> (f - 2)/t + 1. For large degree the three branches change the degree by -1, +1, -1, so
the mean drift under uniform constant terms is -1/3.

## Theorem

Let f = 1 + t + t^2 + 2t^4 + 2t^5 + 2t^7. Then deg T^n(f) -> infinity. More precisely
deg T^{6n}(f) = 6 D_n + 7 with D_n nondecreasing and D_n >= sqrt(2n/3) - 2, and every
intermediate degree is within 6 of these (the referee's run shows at most 1 below and 5 above). (Numerically D_n is about n/3.)

## Proof

Put s = t^6, c = 1 + 2t, q = 2t + t^2 + 2t^4 + 2t^5 + 2t^7, and for K in F_3[s] let
f_K = c + K(t^6) q. The seed is f_1.

**Step 1 (renormalisation).** T^6(f_K) = f_{Theta(K)} for every K, where with k_0 = K(0):

    k_0 = 1:        Theta(K) = ((1+s)^2 K - 1)/s + 1      (six steps of branch 1)
    k_0 = 0 or 2:   Theta(K) = ((1+s) K - k_0)/s           (branch words 121212 and 102101)

Proof. The first six branches of any g depend only on g mod t^6 (each step removes the constant
term, divides by t, and possibly multiplies by 1 + t^2 or adds 1; none of these lets a coefficient
of index >= 6 influence an index below 6 - j after j steps). On a set of polynomials with a common
branch word of length 6 containing a ones, T^6(g + t^6 h) = T^6(g) + (1 + t^2)^a h. Write
K = k_0 + s M. Then f_K = f_{k_0} + t^6 M(t^6) q and f_K = f_{k_0} mod t^6. The three constant
cases are finite computations: f_0 = 1 + 2t has word 121212 and T^6(f_0) = f_0; f_2 has word
102101 and T^6(f_2) = f_2; f_1 has word 111111 and T^6(f_1) = f_s. In characteristic 3,
(1 + t^2)^3 = 1 + s and (1 + t^2)^6 = (1 + s)^2. Hence T^6(f_K) = f_{Theta(k_0)} + G M(t^6) q
= f_{Theta(k_0) + G M} with G = (1+s)^2 or 1 + s, and Theta(k_0 + sM) = Theta(k_0) + G M by the
formulas. ∎

**Step 2 (degrees).** deg f_K = 6 deg K + 7 for K != 0. Theta raises the degree of K by exactly
one when k_0 = 1 and leaves it unchanged when k_0 is 0 or 2 (the leading coefficient of
(1+s)^e K is that of K). So D_n = deg Theta^n(1) is nondecreasing, and it tends to infinity if and
only if the branch k_0 = 1 is taken infinitely often. In particular Theta^n(1) is never 0 (its
degree never drops below 0), which the formula deg T^{6n}(f) = 6 D_n + 7 needs.

**Step 3 (the raising branch always recurs).** Let N(K) = ((1+s)K - k_0)/s, the map on both
non-raising branches. Its coefficients are N(K)_i = k_i + k_{i+1}, so N^n(K) is the polynomial
part of (1 + 1/s)^n K (multiplying by 1 + 1/s sends terms of negative degree to terms of negative
degree, so the discarded part never feeds back) and its constant term is the constant term of
(1 + 1/s)^n K(s).

Suppose a raising step is taken at some K = 1 + sM. Its image is

    L = ((1+s)^2 (1 + sM) - 1)/s + 1 = s + (1+s)^2 M.

Choose m >= 1 with 3^m - 2 > deg M and put n = 3^m - 2. If none of the next n steps from L is a
raising step, they are all N, and the constant term after them is

    CT[(1 + 1/s)^n s] + CT[(1 + s)^{n+2} s^{-n} M] = n + CT[(1 + s^{3^m}) s^{2 - 3^m} M] = n + 0,

because (1+s)^{3^m} = 1 + s^{3^m} in characteristic 3, the coefficient of s^{n-1} in (1+s)^n is n,
and M has no term of degree 3^m - 2. Now n = 3^m - 2 = 1 mod 3. So the constant term is 1 and
the next step is a raising step. Either way a raising step occurs within 3^m - 1 steps after the
previous one. The seed K = 1 starts with a raising step, so there are infinitely many. ∎

**Rate.** After the step that raises the degree to D, deg M <= D - 2 (M = 0 when D = 1) and the
least m with 3^m > D has 3^m <= 3D, so the next raising step comes within 3D - 1 steps. Reaching
degree D therefore takes at most 1 + 3(1 + ... + (D-1)) <= 3D^2/2 steps of Theta; so if
n >= 3D^2/2 then D_n >= D, which gives D_n >= sqrt(2n/3) - 1 >= sqrt(2n/3) - 2.

## Remarks

* The same proof shows more: every orbit of Theta that ever takes the raising branch diverges, and
  the others are periodic from the start (N is injective on the finite set of polynomials of a
  fixed degree, so its orbits there are purely periodic). So on
  the invariant family {f_K}, the map T^6 has exactly two behaviours.
* The mechanism is Frobenius, as in the round-5 disproof of the polynomial count law: (1 + t^2)^3
  is a polynomial in t^6, which makes the family {f_K} invariant, and (1 + s)^{3^m} = 1 + s^{3^m}
  forces the raising branch to recur.
* Negative mean drift therefore does not prevent divergence for polynomial Collatz-like maps.
  The integer analogue of this conclusion is not implied: the proof uses identities that have no
  counterpart with carries.
* The candidates B3, G3 and S2c of item U are not treated here. Q4b was settled separately
  (`../../../output/tex/stopping_time_applications.tex`, Theorem 2).

## Files

* `a3.py` — the map; `theta.py` — the renormalised map Theta.
* `check_a3_divergence.py` — exact check: the seed; T^6(f_K) = f_{Theta(K)} and the branch words
  for all K of degree at most 6 and 400 random K of degree up to 58; the degree statements; the
  key identity on 200 random M; and, along 60000 steps of the orbit of K = 1 (final degree
  19896), that every gap between raising steps obeys the proved bound.
