# Referee 1: round 4, lens "integrality"

Scope: everything in this folder, read against round3/README.md and
round3/accel/trichotomy.md. I did not edit any prover file and did not commit.
My own check is `referee1_check.py`. I wrote it from scratch: it imports no
prover module and uses exact integers and Fractions throughout. It has 58
checks, including negative controls.

    python3 referee1_check.py            # N = 2*10^6, about 15 s
    python3 referee1_check.py 10000000   # N = 10^7, about 25 s; ALL PASS

I confirmed that the script can fail. A copy with two planted errors (the
second sf3_13 cycle dropped, and a wrong X_fail) exits 1 with three FAILs.

## Headline

**No type-(c) system is claimed as settled, and none is settled.** The README
says plainly that the hard criterion of the round was not met. The folder's
labels agree with that: GLOBAL is OPEN for K7, for G3 and for all 8 cores. So
there is no claimed new proof method for type (c) to attack. The rest of this
report checks the claims that *are* made: three impossibility theorems, a
classical cycle-length bound applied to new maps, K7 excursion facts, and a
census.

The mathematics is correct. Every proof below was re-derived line by line, and
the numbers were reproduced independently. What needs repair is wording in a
few places:

1. an off-by-one in the definition of the lap count;
2. one heuristic sentence presented as a conclusion;
3. an over-broad "Consequence" of Theorem R;
4. a wrong analogy with dch_C27_2466.

## Prover's checks

| check | result |
|---|---|
| check_mixing.py | ALL PASS (0.1 s) |
| check_k7.py | ALL PASS (1.4 s) |
| check_cycles.py (Z0 = 10^9) | ALL PASS (23 s); the [C-neg] controls fire as stated |
| check_census.py | ALL PASS (24 s) |
| runs/results.txt, results_g3.txt | 28 + 4 jobs, all rc=0; together the slices cover 1..10^11 for every system |

I also recompiled `sfverify.c` and `g3verify.c` and re-ran the top slice
[10^11 − 10^7, 10^11] for all 8 systems: all rc=0. The negative control
(sf3_13 without (3 10 5 6)) gives "no drop for n=3", rc=1. I read the C code:
it uses 128-bit arithmetic, and the guard is checked after each step. Since
x <= 2^120 before a step, 3x+1 < 2^122, so no overflow can slip past. Every
failure mode exits non-zero.

## Verdicts

| claim | verdict |
|---|---|
| Hard criterion (type-(c) system settled) | not claimed; correctly reported as not met |
| Theorem M (1)–(3) | CONFIRMED_WITH_FIX |
| Theorem N̂ | CONFIRMED |
| Theorem R | CONFIRMED; its "Consequence" CONFIRMED_WITH_FIX |
| Theorem C | CONFIRMED (nit: Y = 0) |
| C1 (7 S-cores, K7) | CONFIRMED |
| C2 (G3) | CONFIRMED |
| G3 is type (c), not a disguised easy case | CONFIRMED (type); GLOBAL correctly OPEN |
| K1, K2 | CONFIRMED |
| K3 | CONFIRMED (nit on digits of δ1) |
| census counts and types | CONFIRMED_WITH_FIX (Type (b) "settled" not executed; "trivially divergent" unproved) |
| "only usable extra information is Archimedean size" (README item 1) | CONFIRMED_WITH_FIX (heuristic, relabel) |
| Connection with dch_C27_2466 (cycles.md, README) | WRONG as stated (fix below) |
| Novelty statements | CONFIRMED_WITH_FIX (one self-contradictory phrase) |

## Detailed findings

### Theorem M: CONFIRMED_WITH_FIX

I re-derived (1). On the lap cylinder, T^ℓ is affine with slope λ_C = U/p^E
and fixes x*. The cylinder of the walk C^d is x* + p^{K+dE}Z_p. On D_d,
v_p(x − x*) lies in [K+dE, K+(d+1)E). After multiplication by λ_C^d it lies in
[K, K+E), which is D_0. The map is bijective and scales Haar measure by p^{dE}.

I re-derived (2). Each closed walk π gives a full branch of measure
p^{−K−E(π)}. Conditioning on π, the image is uniform on [r0]_K, so the next
lap count is independent of the past.

(3) is Lemma 1 of round 3.

**Fix 1 (definition).** mixing.md says that n "follows d laps if its first dℓ
residues mod p^K are those of C^d". Read literally, this is off by one: it
ignores the last edge, which returns to r0. Counterexample for G3 (ℓ = 1):
n = 8 has residue 8 at time 0, so by the wording it follows one lap. But
G3(8) = 11 ≢ 8 (mod 9), and 8 ≢ −1 (mod 27), so 8 lies in D_0 by the formula
for D_d. Replace the wording with "its first dℓ *steps* follow the walk C^d
(the residues at times 0..dℓ)". With that wording D_d is as stated.
`check_mixing.py` already uses the correct convention (the cylinder
x* + p^{K+dE}), so only the text is affected. My check: [M-word].

**Fix 2 (nit).** In (3), "the proportion of n <= X" should be "the proportion
of n <= X *in [r0]_K*". Otherwise there is a missing factor p^{−K}.

**Independent test.** [M-iid] in my script works on all n ≡ 8 (mod 9) modulo
3^13. G3 consumes one ternary digit per step, so events are decided exactly by
these residues. The test checks that P(d2 = j | d1, return time) = (2/3)·3^{−j},
exactly, on all 165 decided events. This is a stronger statement than the
factorization of the (d1, d2) table: it also conditions on the return time.
[M-run] checks the affine run formula on D_d for d <= 8.

### Theorem N̂: CONFIRMED

I re-derived it. T̂ extends to Ẑ with the branch read from the Z_p coordinate.
Theorem N supplies infinitely many distinct expanding orbits y_d, so one of
them avoids the finitely many p-projections of E. Take z with p-component y
and arbitrary other components. The cylinder D_i ∋ z, a class mod p^a M',
contains the integers ≡ z (mod p^N M'). For large N these follow y long enough
that T^{j_i}(n) = λn + β with λ > 1.

The argument also covers certificates restricted to one residue class modulo
M' coprime to p. That is the relevant case for split_d-type invariants (n mod d
preserved). So the README's sentence is justified within the certificate
framework. Wording suggestion: say "cannot get past the wall *as part of a
cover/stopping-time certificate*". A global argument that uses a mod-q
invariant in some other way is not excluded by this theorem.

### Theorem R: CONFIRMED; "Consequence" CONFIRMED_WITH_FIX

I re-derived the proof, and it is correct:

* n_d is an integer, because p^{FE} ≡ 1 (mod b) and p^K c' ≡ a (mod b).
* v_p(n_d − x*) = K + dFE exactly, so d(n_d) = dF.
* b·R(n_d) + a = U^{dF} p^K c'.

Images of regular sets under rational relations are regular (Nivat). Affine
maps and division by a constant preserve p-automaticity. Cobham's theorem then
applies with p and U^F multiplicatively independent. I checked the n_d
identity exactly for F5 (p = 2, U = 5, x* = 1/3, F = 2, c' = 5) for d < 12
([R-nd]).

**Fix.** The theorem is about the run map R. mixing.md says no unit system with
an expanding cycle has a finite-transducer "*excursion* map", which is broader.
That holds for any excursion map that contains a full run. It does not hold
for first-return maps in general: the 3x+1 Syracuse map (the first return to
the odd class) *is* a rational relation in base 2. The README and mixing.md
should say "run map (or any excursion map that contains the full run along C)".
The conclusion that the automata route is closed is fine for the route the lens
proposed.

### Theorem C: CONFIRMED

I re-derived it line by line:

* The product identity is p^X/a^Y = Π(1 + v_t/(u_t n_t)). It is > 1 because
  the identity-step cycles are excluded.
* The product is <= exp(βγX/Z0).
* e^t <= 1 + (e−1)t < 1 + 2t on (0, 1].
* t < ln p gives p^{X−1} < a^Y, so X is the least such exponent. The
  hypotheses for p = 2 (X < Z0 ln 2/(βγ)) and p >= 3 (t <= 1 < ln 3) are
  right.

The constants are correct for both families:

* **S-family:** β = 1. γ = 1, because each odd step lands on an even number and
  is followed by a halving. c = 2.
* **G3:** v ∈ {0, 1, 2} for u = 1 and v = 1 for u = 4, so β = 2. P = X and
  γ = 1, so c = 4.

**Independent reproduction.** My scan (a full scan, not a sample, and starting
at Y = 0) gives the same (Y_fail, X_fail) for all four (Z0, p, a) cases:

| Z0 | p | a | (Y_fail, X_fail) |
|---|---|---|---|
| 10^9 | 2 | 3 | (15601, 24727) |
| 10^11 | 2 | 3 | (190537, 301994) |
| 10^9 | 3 | 4 | (25254, 31867) |
| 10^11 | 3 | 4 | (176251, 222404) |

At each Y_fail, X log p − Y log a is a small positive number below cX/Z0, as
it must be.

**Falsification tests** (point 3 of the brief). Theorem C must hold for every
real cycle of a map in its class. I tested it with Z0 = min(cycle) − 1 on all
815 cycles of 3x+k (k < 400, 3 ∤ k, with β = k/3 and c = 2k/3) and on the 5x+1
cycles with minima 1, 13 and 17: no violation. As a control, a constant c/8
that is too small is violated 750 times, so the test has teeth. On 3x+1 the
theorem gives only the classical Steiner/Eliahou-type bound, as the prover
says. It proves nothing false.

Nit: `cycle_bound.py` starts at Y = 1. The case Y = 0 forces X = 1, and then
(★) reads Z0(p − 1) < c, which is false. So Y = 0 is excluded, but the text
should say so in one line.

### C1 and C2: CONFIRMED

Strong induction from "every n <= Z0 off the listed cycles drops below itself"
is valid. The minimum of an unlisted cycle could never drop, so it would make
the verifier fail. The 10^11 runs are recorded, complete and reproducible
(I re-ran the top slices). Lengths:

* **C1:** X + odd steps >= X + Y >= 301994 + 190537 = 492531.
* **C2:** P = X >= 222404.
* **K7:** I checked K7(z) = (g(2z+1) − 1)/2 directly for z < 2·10^5 and also
  re-derived it by hand in all three residue cases. K7 cycles map to sf3_7
  cycles with z = (n−1)/2 >= 5·10^10, and the length (the number of odd
  elements) is >= Y >= 190537.

**Completeness of the cycle lists, by independent brute force.**

* Drop verification of all n <= 10^7 for the 7 S-cores and G3.
* An independent orbit enumeration that finds every cycle with minimum
  <= 3·10^5. It returns exactly the listed cycles: (1 2) or (1 4 2), plus
  (3 10 5 6) for sf3_13, and (1) for G3. The only cycle reached by K7 from
  z >= 1 is the fixed point 0.
* Controls: sf3_13 without (3 10 5 6) is rejected at n = 3. The core W
  (sf3_137) is rejected already at n = 7 by my 10^40 / 10^5-step cap. The
  prover quotes n = 15 as the escaping orbit; n = 7 hits my cap first, which is
  a property of the cap, not a contradiction.

Labels: the claim is "no other cycle below 10^11 and none shorter than ...".
It is not GLOBAL, and it is labelled correctly.

### G3: type (c) CONFIRMED; not a disguised easy case

I checked this independently on G_2 and G_3:

* −1 (8 mod 9) has a self-loop with multiplier 4/3.
* 1 has a self-loop with multiplier 1/3.
* They are mutually reachable, for example 1 → 7 → 6 → 8 → 2 → 1 mod 9.

So the SCC is not a single simple cycle: it is type (c). By Theorem N it has no
generalized certificate, and the prover's decide.py run says OBST. The
branches are integral, and v/u <= 2. The excursion form
3^k m − 1 ↦ 4^{k−1} m is a full-branch i.i.d. process with unbounded expanding
branches (my [M-iid] test). I see no hidden invariant that would make it easy,
and the folder correctly leaves GLOBAL OPEN (EVIDENCE to 10^11).

### K1–K3: CONFIRMED

* **K1.** I re-derived it: (3z+1)/2 = 3(z+1)/2 − 1 keeps z ≡ −1 mod 2^{i−1}.
  The last step (z−1)/4 applies to 2·3^{j−1}u − 1. Checked for all odd
  z < 2·10^5.
* **K2.** Both inequalities and their equality cases are correct. For j <= 4,
  u(2^{j+1} − 3^{j−1}) >= 3 > 1, so S(z) < z.
* **K3.** For each (j, v), u lies in one class mod 2^{v+1}, and the condition
  is linear in u. My exact partial sum is δ1 = 0.0362745023…, and the count
  below 2^22 gives 0.0362749.
  * Nit: "0.036275…" reads as a truncation, but the value is 0.0362745…; write
    "≈ 0.036275" or "0.0362745…".
  * The explicit rising families are correct. My 2-adic lift finds exactly one
    class mod 2^{7k+1} for each k <= 8. The k = 8 class has least member
    z = 77696884006113599. That there is exactly one class matches Theorem M.
  * The mean drift log 3 − 4 log 2 ≈ −1.674 is right. Under Haar measure, j and
    v are independent geometric with mean 2.

### Census: CONFIRMED_WITH_FIX

The four families add up to 324, 20736, 46656 and 46656 tables, which matches
18², 12⁴, 6⁶ and 6⁶. The c_mixed counts sum to 54105. The prover's
check_census re-derives the counts, the OBST assertion and the level-(m+1)
lift.

Fixes:

1. "Type (b) occurs only in F3m2 (36 tables, all settled by Theorem H)": no
   script runs Theorem H on these 36 tables (there is no `theorem_H` call in
   the folder). The hypotheses do hold: positivity, no division-free cycle,
   and, for unit u, "neutral" SCCs cannot occur. So the right label is
   "settled by Theorem H in principle; cycle lists not computed", or the
   theorem should be run.
2. "c_exp … which is trivially divergent" is asserted without proof. Orbits
   can leave the SCC. Either prove "some positive orbit diverges" or say "no
   cycle can be confined to the SCC's interior below a computable bound".

The orbit statistics are correctly labelled EVIDENCE.

### README item 1 / "Where the method stalled": CONFIRMED_WITH_FIX

"After them, the only usable extra information is the Archimedean size of an
integer" is not a consequence of M, N̂ and R. Those three theorems exclude
three specific proof shapes:

* arguments that use only cylinder or Haar-measure information;
* cover/stopping-time certificates over Ẑ;
* finite transducers for the run map.

They do not exclude, for example, global arguments that combine residues with
size, or invariants that are not cylinder covers. Relabel the sentence as the
lens's interpretation (HEURISTIC). The impossibility theorems themselves are
fine and are honestly described as impossibility statements.

### Connection with dch_C27_2466: WRONG as stated

This bears directly on the user's interest in the 2466-step certificate.
cycles.md says that the near-critical ratios that defeat (★) "are the same
objects" that give round 3's deep certificates, and that "in both cases the
cost is governed by how well log a/log p is approximated by rationals". That is
not accurate for dch_C27_2466:

* dch_C27_2466 is a *settled* mixed-multiplier table: multipliers 1, 2, 4 and 5
  on base 3, proved by a weighted potential. Its depth k* = 2466 is a finite,
  exactly computed quantity. It comes from one specific 11-step residue cycle
  with multiplier 80/81 = 2^4·5/3^4, whose mean log-multiplier is −0.001129 per
  step (round3/dichotomy/dch_C27_2466.md). It is a max-cycle-mean of a finite
  graph. There is no single ratio log a/log p and no sequence of rational
  approximations involved.
* In Theorem C, (Y_fail, X_fail) is governed by the continued-fraction
  convergents of log_2 3 (or log_3 4), and Y_fail grows without bound as Z0
  grows. At Z0 = 10^11, X log 2 − Y log 3 = 6.4·10^{−8} at Y_fail = 190537.

The common theme is a product of multipliers close to 1. That is a fair
analogy, but the two "costs" are different mathematical objects: one is a
fixed finite depth in a solved system, the other is an unbounded Diophantine
threshold for open cycle problems. **Fix:** rewrite as "a loose analogy: both
are governed by products of multipliers close to 1. For dch_C27_2466 this is
one finite residue cycle (80/81), and for Theorem C it is the convergents of
log_p a." The same applies to the README line "80/81 behind dch_C27_2466's
2466 steps". The 2466 figure is correct; the explanation attached to it is
what needs changing.

### Novelty and honesty

The statements are honest overall. Literature was not checked, and Theorem C is
correctly called classical (Steiner, Eliahou, Simons–de Weger). Theorem M is
called Terras/Lagarias-style, and Theorem R a direct application of Cobham.

One fix: cycles.md says the application "is new in the sense that nobody has
done it for these maps; literature novelty was not checked". The first half is
an unverified claim that contradicts the second. Write "not found in this
repository; literature not checked".

## needs_repair

Yes, for wording only. One sentence is WRONG (the dch_C27_2466 analogy), and
several statements need the fixes stated above: the lap-count off-by-one, the
"Archimedean size only" overreach, the scope of Theorem R's consequence, the
Type (b) "settled" label, and the "nobody has done it" phrase. No theorem, bound
or count changes. All proved results stand as CONFIRMED.
