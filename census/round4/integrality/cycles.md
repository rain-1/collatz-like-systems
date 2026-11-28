# Cycle length from integrality: what real size gives that cylinders cannot

Lens "integrality", round 4. Check: `check_cycles.py` (exits 0). By default it
runs with Z0 = 10^9, in about 1 minute. `--full` runs Z0 = 10^11 in about
30 minutes on 11 cores. The 10^11 runs quoted below are recorded in
`runs/results.txt` and `runs/results_g3.txt`.

`mixing.md` excludes three proof shapes (cylinder/Haar arguments, certificates
over Ẑ, transducers for the run map). The Archimedean size of an integer is not
excluded by them; it is not the *only* remaining information (that earlier claim
was a heuristic and is withdrawn, see REFEREE1), but it is the one this lens
tried next. This file uses it for the cycle half of
GLOBAL. The argument is the classical one for 3x+1 (Steiner 1977, Eliahou 1993):
a cycle forces p^X/a^Y to be very close to 1. Applied to the open cores of
round 3, it replaces "no new cycle of period <= 26" (the exhaustive closed-walk
enumeration of sfamily_obst.md) by "no new cycle of length below about 5·10^5,
and none with an element <= 10^11". No cylinder argument can give a statement
about cycles of unbounded period in this form, because a cycle with all
elements large is p-adically invisible: it is one more periodic point y.

## Theorem C. PROVED

Let T be a table map on positive integers whose branches are
n ↦ (u n + v)/p^e with u ∈ {1, a} (a >= 2, p ∤ a) and 0 <= v <= β u. Let
n_0, …, n_{P−1} be a cycle of T, with X the total exponent of the divisions,
Y the number of steps with u = a, and P_+ the number of steps with v > 0.
Assume

* (H_γ) P_+ <= γ X;
* every element n_t > Z0;
* the cycle is not a cycle of identity steps (u = 1, v = 0, e = 0).

Put c = 2βγ. If X < Z0 ln 2/(βγ) (for p = 2) or X <= Z0/(βγ) (for p >= 3),
then X is the least integer with p^X > a^Y, and

    Z0 (p^X − a^Y) < c X a^Y.                                       (★)

*Proof.* T(n_t)/n_t = (u_t/p^{e_t})(1 + v_t/(u_t n_t)). The product over the
cycle is 1, so

    p^X / a^Y = Π_t (1 + v_t/(u_t n_t)).

Every factor is >= 1. If all were 1, every v_t would be 0, and then p^X = a^Y
forces X = Y = 0. That would make every step an identity step, which is
excluded. So the product is > 1. Each factor is at most 1 + β/Z0, and at most
P_+ factors exceed 1, so the product is at most (1 + β/Z0)^{P_+} <=
exp(βγX/Z0). Put t = βγX/Z0. If t <= 1 then e^t <= 1 + 2t, so
p^X/a^Y <= 1 + cX/Z0, which is (★) after multiplying by Z0 a^Y (it is strict
because e^t < 1 + 2t for 0 < t <= 1). If moreover e^t < p (which is the stated
bound on X), then p^{X−1}/a^Y < 1, so X is the least exponent with p^X > a^Y. ∎

The case Y = 0 (no a-step) is excluded directly, added after REFEREE1: then
X >= 1 and p^X >= 1 + (p − 1)X by Bernoulli, so (★) would give
(p − 1)X <= cX/Z0, i.e. Z0(p − 1) <= c, false for every Z0 used here
(c <= 4). So `cycle_bound.py` starts at Y = 1.
It loops over Y = 1, 2, … with X the least exponent with
p^X > a^Y. It returns the first Y for which (★) is *not* violated, called
(Y_fail, X_fail). For every smaller Y, (★) fails exactly (integer arithmetic),
so no cycle has that Y. Hence every cycle satisfying the hypotheses has
Y >= Y_fail and X >= X_fail.

**Corollary C1 (S-family cores).** Take T_S(n) = n/2 (n even), and for odd n
take 3n+1 if n mod 8 ∈ S, else n+1. Then a = 3, β = 1, and P_+ = (number of odd
steps) <= X, since every odd step lands on an even number, so γ = 1 and c = 2.
For each of the seven open cores

| core | S | listed cycles |
|---|---|---|
| sf3_7 (= K7) | {7} | (1 2) |
| sf3_17 | {1,7} | (1 4 2) |
| sf3_57 | {5,7} | (1 2) |
| sf3_157 | {1,5,7} | (1 4 2) |
| sf3_357 | {3,5,7} | (1 2) |
| sf3_13 | {1,3} | (1 4 2), (3 10 5 6) |
| sf3_135 | {1,3,5} | (1 4 2) |

the exact C program `sfverify.c` (unsigned 128-bit arithmetic with an
overflow guard) checked that every n <= Z0 = 10^11 not on a listed cycle drops
below itself. By strong induction, every n <= 10^11 reaches a listed cycle, so
no other cycle has an element <= 10^11. With Z0 = 10^11, cycle_bound gives
(Y_fail, X_fail) = (190537, 301994). The case X >= Z0 ln 2 needs no work. So:

**Every cycle of these seven cores other than the listed ones has all
elements > 10^11 and length P = X + (odd steps) >= X + Y >= 301994 + 190537 =
492531.** PROVED. Round 3 had: no other cycle of period <= 26.

For K7 itself: by Theorem Z of sfamily_obst.md, K7(z) = (g(2z+1) − 1)/2, where
g is the next odd value of the T_{{7}}-orbit. So one K7 step is one
odd-to-odd transition of sf3_7. K7 cycles on z >= 1 therefore correspond to
sf3_7 cycles other than (1 2), with z = (n−1)/2 running over the odd elements.
**Every K7 cycle other than the fixed point 0 has all elements >= 5·10^10 and
length (= number of odd elements of the sf3_7 cycle, which is >= Y) >= 190537.**
PROVED.

**Corollary C2 (the new core G3).** G3(n) = (4n+1)/3 if n ≡ 8 (mod 9), otherwise
⌈n/3⌉. Every step divides by 3, so P = X. Here a = 4 and v/u <= 2, so β = 2,
γ = 1 and c = 4. G3 is type (c) (its single SCC contains the expanding
fixed point −1, multiplier 4/3, and the contracting loop at 1) and
decide.py says OBST (`check_mixing.py` [type]). `g3verify.c` checked every
n <= Z0. With Z0 = 10^11, cycle_bound gives (176251, 222404), so **every G3
cycle other than the fixed point 1 has all elements > 10^11 and length
>= 222404.** PROVED (with the Z0 = 10^11 run; the default check proves the
Z0 = 10^9 version: length >= 31867).

**W is excluded.** For the core W (sf3_137) the verification hypothesis fails
at n = 15, whose orbit passes 10^60 (EVIDENCE, round 3). `check_cycles.py`
[C-neg] confirms that the verifier rejects it. It also rejects sf3_13 when the
second cycle (3 10 5 6) is left out. So the check can fail.

## Testing against 3x+1, and the limits

Theorem C applied to 3x+1 gives the known type of result (Eliahou 1993: any
nontrivial cycle has length >= 17,087,915 from verification up to about 2^40;
the bound now known is much larger). It says nothing about divergent orbits,
and neither does anything here. That is the honest limit: **the integrality
method settles the cycle half of GLOBAL only up to a length bound, and does not
touch the divergence half.** A divergent orbit is not a periodic point, and
the product identity has no analogue for it.

Why the bound is finite: with only continued-fraction information, (★) cannot
exclude Y near convergent denominators of log_p a once c X/Z0 exceeds
|p^X/a^Y − 1|. To exclude all cycles one would need either a lower bound for
|X log p − Y log a| that grows faster than Z0 can be raised (Baker-type bounds
give only a power of X, as for 3x+1), or a bound on Y in terms of the
elements. That is the same wall 3x+1 has for cycles.

## Connection with the near-critical depth records (corrected after REFEREE1)

The first version of this section said that the near-critical ratios defeating
(★) "are the same objects" as those behind round 3's deep certificates, and
that "in both cases the cost is governed by how well log a/log p is
approximated by rationals". **That was wrong for dch_C27_2466 and is
withdrawn.** The correct statement is only a loose analogy: both phenomena are
governed by products of multipliers close to 1, but they are different
mathematical objects.

* dch_C27_2466 (round3/dichotomy/dch_C27_2466.md) is a *settled*
  mixed-multiplier table on base 3 (multipliers 1, 2, 4, 5), proved by a
  one-step weighted potential. Its depth k* = 2466 is a fixed finite number:
  the minimal step count of a plain descent certificate. It comes from one
  specific 11-step contracting residue cycle with multiplier
  80/81 = 2^4·5/3^4 (mean log-multiplier −0.001129 per step), the max-mean
  cycle of a finite graph. No single ratio log a/log p and no sequence of
  rational approximations is involved.
* In Theorem C, (Y_fail, X_fail) is governed by the continued-fraction
  convergents of log_2 3 (or log_3 4), and Y_fail grows without bound with Z0
  (at Z0 = 10^11, X log 2 − Y log 3 ≈ 6.4·10^{−8} at Y_fail = 190537). It is
  an unbounded Diophantine threshold for an open cycle problem.

The 2466 figure itself is correct; only the explanation attached to it was
wrong.

## Novelty

The method is classical (Steiner, Eliahou, Simons–de Weger). Applying it to the
round-3 cores and to G3 was not found in this repository; literature not
checked. (The earlier phrase "nobody has done it for these maps" was an
unverified claim and is withdrawn.)
