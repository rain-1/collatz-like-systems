# Referee 2: round 4, lens "integrality" (second pass, after the repair)

Scope: the whole folder, read against round3/README.md and
round3/accel/trichotomy.md, plus every REFEREE1 item. I did not edit any prover
file and did not commit. The one side effect was that running the prover's
`check_cycles.py` recompiled its own `sfverify_bin` and `g3verify_bin`, which
that script always does.

My check is `referee2_check.py`. I wrote it from scratch: it uses only the
standard library and imports neither the prover's modules nor
`referee1_check.py`. Claims are decided with exact integers and Fractions.
Floats appear only in Karp's max-mean-cycle search. There, every compared value
is far from 0 compared with float error, and each extremal cycle is
re-checked exactly.

    python3 referee2_check.py            # N = 10^6, about 17 s, ALL PASS
    python3 referee2_check.py 200000     # faster

**It can fail.** A copy with four planted errors exits 1 with exactly the
expected FAILs. The four errors are: sf3_13 without (3 10 5 6), a wrong
X_fail, a wrong 81/80 product, and (in an earlier run) a wrong census count.

I also wrote my own drop verifier in C, separate from the prover's.
`scratchpad/ref2/drop.c` uses uint64 with `__builtin_mul_overflow` and a step
cap, and has its own skip lists. It found:

* For all 8 systems (7 S-cores and G3), every n <= 4·10^9 off the listed cycles
  drops below itself (16 jobs, all rc = 0).
* The same holds on the top slice [9.98·10^10, 10^11].
* Negative controls: sf3_13 without its 4-cycle is rejected at n = 3. W is
  rejected at n = 7, which is on W's 9-cycle; see the note on REFEREE1 below.

## Headline

**No type-(c) system is claimed as settled, and none is.** The README still says
plainly that the round's hard criterion was not met. GLOBAL is OPEN for K7, G3
and all 8 cores. So there is no new type-(c) proof method to break. I
re-refereed what is claimed: three impossibility theorems (M, N̂, R), a
classical cycle-length bound (Theorem C) with two corollaries, K7 excursion
facts, and a census. All of it is correct, and all REFEREE1 items were resolved
honestly. Four small nits remain. None needs a repair.

## Prover's checks (re-run)

| check | result |
|---|---|
| check_mixing.py | ALL PASS (0.1 s) |
| check_k7.py | ALL PASS (1.3 s) |
| check_typeb.py | ALL PASS (8.5 s); 36 tables, cycle lists 18 × {1,2}, 12 × {1}, 6 × {2}; all at level K = 2 |
| check_census.py | ALL PASS (24 s) |
| check_cycles.py (Z0 = 10^9) | ALL PASS (19 s); [C-neg] fires |
| runs/results*.txt | 28 + 4 slices, all rc = 0; the 4 slices per system cover 1..10^11 exactly |

## REFEREE1 items: was each honestly resolved?

| REFEREE1 item | resolution | my check |
|---|---|---|
| dch_C27_2466 analogy WRONG | **Resolved.** Withdrawn in cycles.md and the README, and replaced by a correct "loose analogy" paragraph. I verified every fact in the new text independently (section below). | [2466-*] |
| lap-count off-by-one | Resolved. The definition is now in steps 0..dℓ, with the n = 8 example. | [M-def], [M-run], [R-nd] |
| proportion "in [r0]_K" | Resolved. | (text) |
| Theorem R "Consequence" too broad | Resolved. Narrowed to the run map and to excursion maps containing a full run; the Syracuse counterexample is stated. The README row matches. | (re-derived) |
| N̂ wording | Resolved ("as part of a cover/stopping-time certificate"). | (text) |
| "only Archimedean size is left" | Resolved. Labelled HEURISTIC in the README, mixing.md and cycles.md, with the three excluded proof shapes listed. | (text) |
| Type (b) "settled by Theorem H" not run | Resolved. `check_typeb.py` really calls `accel_lib.theorem_H` on all 36 tables. My independent typer finds exactly the same 36 tables, and my brute force reproduces every listed cycle list. | [census-F3m2], [typeb-set], [typeb-cyc] |
| c_exp "trivially divergent" | Withdrawn. Nothing is claimed about c_exp orbits. | (text) |
| Theorem C, Y = 0 | Resolved, and the argument is right: Z0(p^X − 1) < cX with p^X − 1 >= (p − 1)X gives Z0(p − 1) < c, which is false. My scan starts at Y = 0 and agrees. | [C-scan] |
| δ1 digits | Resolved (0.0362745…). | [K3-delta] = 0.0362745023 |
| "nobody has done it" | Withdrawn. | (text) |

**One correction to REFEREE1 itself (not the prover).** REFEREE1 said its
script rejects W (sf3_137) "already at n = 7", and that this was "a property of
the cap". That is wrong. n = 7 lies on W's known 9-cycle
(7 22 11 34 17 52 26 13 14), listed in round3 sfamily_obst.md, which REFEREE1
did not list. It is rejected for that reason. With all four known W cycles
listed (31 elements), the first rejected start is n = 15, exactly as the prover
says. [neg-drop] checks both statements.

## The 2466-step certificate (dch_C27_2466): what the revised text says, verified

The user is interested in this one, so I re-derived everything the revised
cycles.md and README say about it. I did not rely on round 3's scripts.

* **The rule.** The table covers each of the 27 residues exactly once. Its
  multipliers are 1, 2, 4 and 5, and the 3 | n classes go to n/3. So it is a
  unit-multiplier base-3 table, as stated. ([2466-rule])
* **Settled.** Every n <= 10^6 reaches one of exactly the three listed cycles:
  (1 2 3), (5 11 43 45 15) and the 11-cycle
  (125 624 208 209 419 420 140 281 1123 1125 375). ([2466-cyc])
* **80/81 is the max-mean cycle.** By Karp's algorithm on the mod-27 residue
  graph, the maximum cycle mean is −0.00112932, which equals ln(80/81)/11
  (agreement to 10^−12). It is negative, so every residue cycle contracts. That
  is row 1 of the trichotomy, which is why a descent certificate exists at all.
  ([2466-maxmean])
* **New observation.** The 80/81 residue cycle is exactly the residue pattern
  of the third integer cycle (125 … 375). Its multiplier is 5·2·2·4/3^4 = 80/81.
  The cycle identity from Theorem C holds on it exactly:

      Π (1 + v/(u n)) = 81/80

  ([2466-8081], [2466-id]). So there is one precise link between dch_C27_2466
  and this folder's Theorem C, beyond the "loose analogy" the prover now
  states. The barely contracting residue cycle carries a real integer cycle,
  whose small elements (125 to 1125) are what make the additive terms
  compensate the factor 80/81. It does not change the prover's corrected
  point: k* = 2466 is a fixed finite depth in a solved system, while Theorem C's
  threshold is an unbounded Diophantine one. The sentence could be added to
  cycles.md if the prover wants it. It is optional.
* **The witness for the lower bound.** I read a and M (1424 bits) from
  dch_C27_2466.md. At n = a + M·10^12, T^i(n) >= n for every 1 <= i < 2466.
  ([2466-wit]) I did not re-prove the matching upper bound (a certificate with
  max depth 2466) or the 60-bit potential; those are round-3 results refereed
  there.
* "Mean log-multiplier −0.001129 per step" is correct, as is "11-step".

## Verdicts and re-derivations

### Theorem M: CONFIRMED

I re-derived (1) to (3) line by line.

* **(1).** The cylinder of C^d is x* + p^{K+dE}Z_p. The map
  x ↦ x* + λ^d(x − x*) multiplies p-adic distance to x* by p^{dE}, so it sends
  D_d onto D_0 and scales Haar measure by p^{dE}.
* **(2).** Full branches follow from (M) applied step by step.
* **(3).** This is Lemma 1 of round 3.

My [M-full] test is stronger than a factorization check. On G3, for every
residue n ≡ 8 (mod 9) modulo 3^12, I took each of the 2585 first-return walks π
(as residue walks in G_2) that is decided at that precision. Each walk has
exactly 3^{10−E(π)} starting residues, and T^{|π|} maps them bijectively onto
all of [8]_2 mod 3^{12−E}. That is literally the full-branch property.
[M-run] checks R(n) = −1 + (4/3)^d (n+1) ∈ D_0 for d <= 8.

### Theorem N̂: CONFIRMED

I re-derived the proof. The one point that needs care is the choice of y. One
needs *all* partial multipliers along y's orbit to be > 1, because j_i is
arbitrary. Starting the expanding cycle at the right rotation (the cycle lemma)
gives λ_s > 1 for s < ℓ. Then λ_{qℓ+s} = λ_C^q λ_s > 1. Theorem N's
infinitely many expanding points avoid the finitely many p-projections of E.
The q-components of z are free. The scope sentence is now correct.

### Theorem R: CONFIRMED (Consequence now CONFIRMED)

The proof steps are each valid:

* n_d is an integer, and d(n_d) = dF.
* b R(n_d) + a = U^{dF} p^K c'.
* The definability steps in ⟨N, +, V_p⟩ go through.
* Rational transductions preserve regularity.
* Cobham's theorem applies: p is prime, p ∤ U and U >= 2, so p and U^F are
  multiplicatively independent.
* Y has gaps tending to infinity, so it is not ultimately periodic.

[R-nd] checks, for G3, that n_d = 3^{2+d} − 1 has lap count d and
R(n_d) = 9·4^d − 1 for d < 40.

Sanity check on 3x+1: the conclusion says the run map n = 2^k m − 1 ↦ 3^k m − 1
is not rational. That is consistent with the Syracuse map being rational,
because the Syracuse map does not contain the full run.

### Theorem C: CONFIRMED (one nit)

I re-derived it:

* The product identity holds.
* The product is > 1 unless every step is an identity step.
* The product is at most (1 + β/Z0)^{P_+} <= e^t, with t = βγX/Z0.
* e^t <= 1 + (e − 1)t < 1 + 2t on (0, 1].
* e^t < p gives minimality of X.

The constants are right for both families:

* **S-family:** β = 1. γ = 1, because every odd step lands on an even number.
* **G3:** v ∈ {0, 1, 2} for u = 1 and v = 1 for u = 4, so β = 2 and γ = 1.

My full scan from Y = 0, with my own code, reproduces all four (Y_fail, X_fail).
At Y_fail = 190537 one has 2^301994/3^190537 − 1 = 6.4508·10^−8.

**Falsification.** Theorem C holds on all 246 cycles of 3x+k (k < 400) that are
inside its range, with Z0 = min − 1. It also holds on the 5x+1 cycles 13 and
17. With c/8 it is violated 234 times, so the test has teeth.

**Literature calibration (new).** For 3x+1 with Z0 = 2^40:

* With its own constants (β = 1/3, γ = 1, c = 2/3), Theorem C gives only
  X_fail = 301994.
* Eliahou's sharper inequality, X ln 2 − Y ln 3 <= Y ln(1 + 1/(3Z0)), run
  through the same scan, reproduces his X = 17,087,915 exactly
  ([C-cal]).

So the scan is right, and Theorem C is weaker than Eliahou's inequality by one
convergent level. Two losses cause this: the bound P_+ <= X, and the factor 2
in e^t <= 1 + 2t.

**Nit 1.** cycles.md says Theorem C on 3x+1 "gives the known type of result
(Eliahou 1993: … 17,087,915 …)". That is true as to type, but a reader could
take it to reproduce that number. Suggested addition: "with these constants it
gives X >= 301994 at Z0 = 2^40; Eliahou's sharper form gives 17,087,915". This
does not affect C1 or C2, whose numbers are correct for the theorem as proved.

### C1, C2: CONFIRMED

* **Strong induction.** "Every n <= Z0 off the listed cycles drops below
  itself" implies that every n <= Z0 reaches a listed cycle. So no other cycle
  has an element <= Z0. All maps keep positive integers positive.
* **Lengths.** For C1, P = X + P_+ >= X + Y >= 492531. For C2, P = X >= 222404.
  The case X >= Z0 ln 2 (or X > Z0/2 for G3) trivially exceeds these bounds.
* **K7.** The length is P_+ >= Y. When X is outside the range, the identity
  still forces Y ≈ 0.63X, which is huge. z = (n−1)/2 >= 5·10^10.

Independent evidence for these claims:

* My C verifier to 4·10^9 and on the top slice below 10^11.
* My Python verifier to 10^6.
* Orbit enumeration from all n <= 3·10^5. It finds exactly the listed cycles
  for each of the 7 cores, only (1) for G3, and only (0) for K7.
* [type-K7] checks K7(z) = (g(2z+1) − 1)/2 for z < 2·10^5.

### G3 is type (c), not a disguised easy case: CONFIRMED

My own residue graph shows this:

* **Mod 9.** There is a single SCC of all 9 nodes. It has the loop 8 → 8 with
  multiplier 4/3 and the loop 1 → 1 with multiplier 1/3, and it is not a simple
  cycle.
* **Mod 27.** It is c_mixed again.

Because the expanding loop shares a component with contracting cycles, no
one-step weighted potential c(r)·n exists. That kind of potential is what
settles dch_C27_2466, and it needs every residue cycle to contract. Theorem N
excludes descent and accelerated certificates.

I re-derived the excursion form 3^k m − 1 ↦ 4^{k−1}m (k steps) by hand.
GLOBAL is correctly OPEN, with EVIDENCE to 10^11 (and mine to 4·10^9).

**Nit 2.** census_small.md calls log_3 4 "the integrality ceiling" for G3's
peak exponent. As proved, it is a ceiling for one run (t consecutive rising
steps need n ≡ −1 mod 3^{t+1}). It is not proved for a whole orbit with
several rising runs. The F3m2 bullet just above already says "per excursion",
so this needs only a word ("per-run ceiling").

### K1–K3: CONFIRMED

I re-derived each part:

* K1 (the j − 1 halvings keep z ≡ −1, then (z − 1)/4).
* Both K2 lines with their equality cases (u = 1, v = 1 iff j even).
* S < z for j <= 4.
* The class structure in K3 and δ1 = 0.0362745023.
* The rising families: exactly one class mod 2^{7k+1} for k = 1..3, matching
  measure 2^{−7} per excursion.
* The mean drift log 3 − 4 log 2 ≈ −1.674.

### Census: CONFIRMED

I wrote an independent enumerator and typer. It uses SCCs plus Karp on G_m;
neutral cycles cannot occur except division-free ones, and the families have
none. It reproduces the prover's counts exactly:

* **F2m2:** 86 / 54 / 0 / 168 / 16.
* **F3m2:** 20736 / 9200 / 36 / 16668 / 16.

I did not recount F2m3 or F3m2b myself; the prover's check_census re-derives
them. The orbit tables are correctly labelled EVIDENCE. The x* = 2 example,
n ≡ 2 (mod 9) → (4n − 2)/3, is in the F3m2 menu and is a fixed point.

### Labels, novelty, honesty: CONFIRMED (two nits)

The labels are honest. The hard criterion is "not met", and GLOBAL is OPEN
everywhere. Novelty is "not checked", with the classical sources named
(Steiner, Eliahou, Terras, Lagarias, Cobham).

**Nit 3.** The docstring of `check_cycles.py` says [C-bd] re-verifies the
inequality "for every Y < Y_fail". The code samples every ⌊Y_fail/2000⌋-th Y.
The printed label does say "sampled". The full scan in `cycle_bound.py`, and
mine, cover every Y, so nothing is unproved; only the docstring overstates.

**Nit 4.** README "Tests" quotes W's failure at n = 15. That is correct, but 15
is the least failing start only once all four known W cycles are listed. A
half-clause would help readers who rerun with a shorter list.

## Summary of verdicts

| claim | verdict |
|---|---|
| Hard criterion (type-(c) system settled) | not claimed; correctly reported as not met |
| Theorem M (1)–(3) | CONFIRMED |
| Theorem N̂ | CONFIRMED |
| Theorem R and its narrowed Consequence | CONFIRMED |
| Theorem C | CONFIRMED (nit 1: say it is weaker than Eliahou's form numerically) |
| C1 (7 S-cores, K7) | CONFIRMED |
| C2 (G3) | CONFIRMED |
| G3 type (c), not disguised easy; GLOBAL OPEN | CONFIRMED |
| K1–K3 | CONFIRMED |
| census counts / types; type (b) via Theorem H | CONFIRMED |
| revised dch_C27_2466 paragraph | CONFIRMED (all facts verified; optional added link: the 80/81 residue cycle is the integer cycle 125…375, identity product 81/80) |
| HEURISTIC relabel, c_exp withdrawal, novelty wording | CONFIRMED |
| REFEREE1 items | all honestly resolved |

## needs_repair

**No.** Every claim is CONFIRMED. The four nits (the Eliahou numbers, "per-run
ceiling", the check_cycles docstring, the W least start) are optional wording
improvements that change no statement's truth.
