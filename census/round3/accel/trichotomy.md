# The SCC trichotomy: when an expanding cycle is harmless, and when acceleration cannot work

Lens "accel", round 3. Check: `check_trichotomy.py` (exits 0, about 15 s). Library: `accel_lib.py`.

## Setting

A *unit-multiplier p-adic system* is a map `T(n) = (u_r n + v_r)/w_r` for `n ≡ r (mod p^m)`. Here
p is prime, `u_r ≥ 1` and `p ∤ u_r`, `w_r = p^{e_r}`, and `w_r | u_r n + v_r` on the whole class. It
has the usual continuous extension `T̂ : Z_p → Z_p`. This covers the S-family, the SPLIT and M3
families, 3x+1, 5x+1, 3x+k, the 1932 permutation, split5_1/5_3, m3_* and desc_* (see
"Catalog" below). It does not cover div23_*, farkas, or maps with even multipliers.

For K ≥ m, the **cylinder graph** `G_K` has the residues mod p^K as nodes. For each node r the step
`n ↦ (u n + v)/p^e` gives the p^e edges `r → s` with `s ≡ (u r + v)/p^e (mod p^{K−e})`. Every
edge carries the exact multiplier `u/p^e`.

**Markov property (M).** Because u is a p-adic unit, T̂ maps the cylinder `r + p^K Z_p` bijectively
and affinely onto `(u r + v)/p^e + p^{K−e} Z_p`, which is exactly the union of the edge targets. So
every finite walk in G_K is followed by a non-empty cylinder of points. Let a closed walk contain
at least one division, and write its composed map as `x ↦ A x + B`, with `|A|_p = p^{(number of
divisions)} > 1`. Then the walk is followed forever by **exactly one** point `x = B/(1 − A)`, and
that point is T̂-periodic with real multiplier A. (Lemma D of round2/descent/lemmas.md. The inverse
branch contracts the cylinder, so the nested intersection is a single point.)

**Standing hypothesis (no division-free cycle).** Every cycle of G_K contains an edge with e ≥ 1.
This rules out neutral cycles. Without it there are trivial divergent classes, such as odd
n ↦ 3n+2.

Every SCC (strongly connected component) of G_K with at least one internal edge is of exactly one
of three types:

* **(a) contracting**: every cycle in it has multiplier < 1;
* **(b) isolated expanding cycle**: the SCC is a single simple cycle with multiplier > 1;
* **(c) free re-entry**: the SCC contains a cycle with multiplier > 1 and at least one other cycle.

(A simple-cycle SCC with multiplier < 1 counts as (a).)

## Theorem H (isolated expanding cycles are harmless). PROVED

Assume the standing hypothesis, assume that T maps positive integers to positive integers, and
assume that, for some K ≥ m, every SCC of G_K is of type (a) or (b).
Then every positive orbit of T is eventually periodic. The complete cycle list is computable by a
finite search: the cycles inside type-(a) SCCs, plus those type-(b) periodic points x* that are
positive integers.

*Proof.* Let n be a positive integer. The residues `T^t(n) mod p^K` form an infinite walk in G_K.
The SCCs form a DAG, so the walk eventually stays inside one SCC Σ that has an internal edge.

* *Σ of type (b), cycle C.* From some time t₀ on, `T^{t₀}(n)` follows C forever. By (M), the only
  point of Z_p that does this is the periodic point x* of C. So `T^{t₀}(n) = x*`, x* is a positive
  integer, and the orbit is periodic from then on.
* *Σ of type (a).* Every cycle of Σ contracts, so the maximum cycle mean of `log(multiplier)` on Σ
  is some μ < 0. Fix a rational θ with `μ < log θ < 0`. Longest-path potentials for the edge
  weights `log q − log θ` exist, because no cycle has positive weight. They give positive rationals
  `c(r)` (r ∈ Σ) with

      c(s) · q ≤ θ · c(r)      for every internal edge r → s of Σ with multiplier q.      (★)

  These are found in floating point and then **verified exactly** with Fractions. Put
  `V(n) = c(n mod p^K) · n`. For an internal step `n ↦ (u n + v)/w` this gives
  `V(T n) ≤ θ V(n) + β`, where `β = max c(s)·max(v,0)/w`. This step uses n > 0: the inequality
  `c(s) · u n/w ≤ θ c(r) n` follows from (★) only when n ≥ 0. Because T maps positive integers to
  positive integers, every point of the orbit is positive, so the inequality applies at every
  step; without that hypothesis the orbit could leave Z_{>0} and would no longer be controlled.
  All maps in this folder satisfy the hypothesis. Once the orbit stays in Σ,
  `limsup V ≤ β/(1−θ)`. Only finitely many integers satisfy `V ≤ β/(1−θ) + 1`, so the orbit is
  eventually periodic.

Every cycle is a closed walk, so it lies inside one SCC. In a type-(b) SCC a cycle is the integer
point x*. In a type-(a) SCC, apply (★) at the point of the cycle where V is largest:
`V_max ≤ θ V_max + β`, so every point of the cycle has `V ≤ β/(1−θ)`. Enumerating those finitely
many n and following their orbits gives every cycle. ∎

`accel_lib.theorem_H` implements this proof exactly. It asserts the hypotheses and returns the
cycle list.

## Theorem N (acceleration barrier). PROVED

A **generalized certificate** for T is a countable cover of `Z_p ∖ E` by cylinders D_i, with step
counts j_i, such that `T^{j_i}(n) < n` for all but finitely many positive integers n ∈ D_i. Here E
is a union of **finitely many periodic orbits** of T̂.

Ordinary descent certificates are the case E = ∅ with a finite cover. *Accelerated certificates
along an expanding orbit O* are also of this form, with E = O. These are certificates that treat
the classes `n = x* + p^j u` for all j at once, with a symbolic exponent, and replace each run
along the shadow of x* by its closed form before continuing with a bounded lookahead.

**Theorem N.** Assume the standing hypothesis. If some SCC of some G_K is of type (c), then T has
no generalized certificate.

*Proof.* Let C (multiplier `λ_C > 1`, length ℓ, with v_C ≥ 1 divisions) be an expanding cycle in
an SCC Σ of type (c). Let r be a node of C.

Σ contains an internal edge a → b that is not an edge of C. (Σ is not a single simple cycle, and C
uses only ℓ edges.) Strong connectivity gives a closed walk `W = (r ⇝ a → b ⇝ r)` that is not a
power of C. For every d ≥ 0, the closed walk `C^d W` determines, by (M), a periodic point y_d.

* Its multiplier is `λ_C^d λ_W`, which is > 1 for all d ≥ d₀.
* y_d follows C for d·ℓ steps, so `y_d ≡ x* (mod p^{K + d v_C})`.
* y_d's orbit uses the edge a → b, so `y_d ∉ O(x*)`.

So the orbits O(y_d) come arbitrarily close to O(x*) without meeting it. A finite union of periodic
orbits disjoint from the closed set O(x*) has positive distance from it. Hence infinitely many of
the O(y_d) are distinct, and some expanding periodic orbit O(y) is disjoint from E.

By the cycle lemma (round2/descent Lemma B), there is a point y on that orbit all of whose partial
multipliers satisfy `λ_j(y) > 1`. This y lies in some D_i. Since T̂ is affine on cylinders, every
n ≡ y (mod p^N), for N large, lies in D_i and has `T^{j_i}(n) = λ_{j_i}(y) n + β`. That is > n for
all large n in this infinite progression, which contradicts the choice of D_i. ∎

**Equivalences (Lemma L, level independence).** Type (c) at one level implies type (c) at every
level ≥ m.

* Going up: for large d, the points y_d give closed walks through `x* mod p^{K'}` that differ from
  C's lift.
* Going down: the projection of `C^d W` is not a power of the projected C. If it were, by (M) its
  periodic point would follow C forever and so lie in O(x*).

So the trichotomy is a property of the system, not of the chosen level. Every type-(c) SCC
contains infinitely many expanding periodic orbits, accumulating at x*. This is the precise form
of the "free re-entry" mechanism of round2/rewriting/split5_3_s27.md.

## Theorem T (trichotomy). PROVED

Assume the standing hypothesis.

1. A plain descent certificate exists ⇔ every SCC is contracting. This is the referee
   proposition of round 2. The "⇐" direction is the potential of Theorem H on the whole graph. The
   "⇒" direction is Lemma B applied to any expanding cycle.
2. A generalized certificate exists ⇔ there is no type-(c) SCC.
   * "⇒" is Theorem N.
   * "⇐": let E be the finitely many orbits of type-(b) periodic points. Any x ∉ E eventually
     stays in a contracting SCC Σ, after t₀ steps say. By (★), after s further steps the slope of
     `T^{t₀+s}` on a small enough cylinder around x is at most
     `λ_{t₀}(x) · (max c/min c) · θ^s < 1`. So that cylinder descends.
3. If there is no type-(c) SCC, GLOBAL holds and the cycles are computable (Theorem H).

So, for unit-multiplier systems, *the boundary between "acceleration works" and "acceleration
cannot work" is exactly whether some expanding cycle shares its SCC with another cycle.*
Isolated expanding cycles are harmless. Non-isolated ones defeat every certificate that
accelerates along finitely many orbits and uses locally constant stopping times.

**What Theorem N does not say.** It does not say that type-(c) systems are unprovable. It only
excludes this whole class of local proofs. The proof uses the unit-multiplier hypothesis in an essential way:
`dressing.md` constructs systems with an expanding p-adic fixed point and free graph-level
re-entry that are nevertheless settled. Their multipliers are not units in the second prime, so
(M) fails and the walks `C^d W` are not realized.

## Applications

**S-family (PROVED, exhaustive).** `even n → n/2; odd n → 3n+1 if n mod 2^m ∈ S, else n+1`. For
m = 2, 3, 4, 5 and all 2 + 16 + 256 + 65536 subsets S, no SCC of G_m is an expanding simple cycle
(exact multiplier test `3^a < 2^b` on every simple-cycle SCC). Every OBST member has an expanding
cycle (round 2), that is, an expanding periodic point at some level K'. That periodic point
projects to a closed walk in G_m with multiplier > 1. A closed walk decomposes into simple cycles,
and its multiplier is the product of theirs, so one of those simple cycles is expanding. The SCC
containing it is not contracting, and by the scan it is not a single simple cycle, so it is of
type (c). (For m ≤ 4 the referee confirmed directly that all 2, 10 and 172 OBST members have an
expanding cycle already at level m; the m = 5 count 48880 is taken from round 2,
family_scan.out.) Hence **all 2 + 10 + 172 + 48880 OBST
members with m ≤ 5 admit no generalized (accelerated) certificate.** In this family the halving
nodes always let an orbit re-enter, so acceleration can never help.

For each of the 12 systems with m ≤ 3, the check exhibits the explicit witnesses `y_0 … y_24`:
exact rationals, all with multipliers `λ_C^d λ_W > 1` from the stated `d₀` on, and with
`y_d ≡ x* mod 2^{m+d}`.

**Catalog (PROVED for the listed systems).** The same exact witnesses are checked for 3x+1, 5x+1,
split5_1, split5_3, m3_e, the 1932 permutation, desc_m3_4n5 and desc_split7_1. A scan
(`scratch/catscan.py`, not a check) of every catalog system that is a unit-multiplier p-adic map
(p ∈ {2,3,5}, modulus ≤ 243) found no open system of type (b). So Theorem H settles no open
catalog system, and Theorem N applies to all of them.

**New systems settled by Theorem H (PROVED).** Each of these is OBST: it has an expanding p-adic
fixed point, verified exactly, so it has no descent certificate. Each is nevertheless settled.

| id | rule | cycles | notes |
|---|---|---|---|
| acc_h32 | even n→n/2; odd: n+1 if n≡5,9,21,25 (32); n+9 if n≡29 (32); else 3n+1 | (1 4 2), (3 10 5 6), (19 58 29 38) | 3n+1 on 11 of 16 odd classes; contracting SCC of 21 nodes, θ = 843643/858949, candidates n ≤ 1515 |
| acc_h16 | even n→n/2; odd: n+1 if n≡5,9 (16); n+5 if n≡13 (16); else 3n+1 | (1 4 2), (3 10 5 6) | 3n+1 on 5 of 8 odd classes; contracting SCC of 10 nodes |
| acc_h9 | 3q→q; 9q+r→6q+r (r=1,4,7); 9q+2→12q+4; 9q+5→12q+7; 9q+8→12q+11 | fixed points 1, 4, 7 | base 3, x* = −1 with multiplier 4/3; easy once the SCCs are drawn |

In each of these the exit classes from the shadow of x* = −1 were chosen so that no orbit can ever
return to the class of −1. For p = 2, the classes that can reach −1 by divisions alone are
`R₀ = {0, −1, −2, …, −2^{m−1}} mod 2^m`. Its complement is closed under halving. The odd branches
outside R₀ were chosen to land outside R₀, and the remaining part was then made contracting. The
systems were found by a randomized search (`scratch/hsearch2.py`, `scratch/h3s*.py`).

**Tier.** These are tier 2–3: a finite SCC computation plus exactly verified weights. No tier-0/1
argument exists, because they are OBST.

**Novelty.** Not checked (no literature search was done). The ingredients are standard: Markov
partitions, SCC decomposition and max-mean cycles. I am not aware of this trichotomy being stated
for Collatz-type maps.
