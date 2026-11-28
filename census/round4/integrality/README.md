# Round 4, lens "integrality"

**Verdict on the hard criterion: not met.** I did not settle any type-(c)
unit-multiplier system, whether one of the 8 cores, a census entry, or a new
design. What this folder contains:

1. **Second-best outcome (the wall extended to this lens's methods).** The lens
   proposed three routes past Theorem N: multipliers with predictable low
   digits, information a p-adic cylinder cannot see (other moduli), and
   excursion maps as finite-state transducers. Three theorems close all three,
   each with the exact reason (`mixing.md`). They exclude three specific proof
   shapes (cylinder/Haar arguments, cover/stopping-time certificates over Ẑ,
   finite transducers for the run map). The first version added "after them,
   the only usable extra information is the Archimedean size of an integer";
   that does not follow from the theorems and is now labelled HEURISTIC.
   Size is simply the next thing this lens tried.
2. **What size does give.** I proved an integrality (Steiner/Eliahou-type)
   theorem on cycles (`cycles.md`). For the 7 open S-family cores (including
   K7) and the new base-3 core G3, any cycle other than the known ones has all
   elements > 10^11 and length about 2·10^5 or more. Round 3 had period <= 26.
   The divergence half of GLOBAL is untouched.
3. Task (1): an exact census of four small families (54,105 c_mixed type-(c)
   tables), sorted by excursion structure (`census_small.md`). Task (3): K7's
   exact excursion map, the sharp excursion inequality, and the exact place
   where induction breaks (`k7.md`).

## Results

| id | statement | status | file / check |
|---|---|---|---|
| Theorem M | For any unit system and any closed walk C with a division: the run map sends each lap-count class D_d affinely onto the same set D_0, and the first-return map to a node is full-branch. So excursion data are i.i.d. under Haar measure, and every finite excursion word is realized by one residue class of positive integers. **u ≡ 1 mod p^s does not control the post-run digits.** This holds for every unit system, so there is no counterexample family. | PROVED | mixing.md / check_mixing.py |
| Theorem N̂ | Theorem N extends to covers by residue classes of *any* modulus (cylinders of Ẑ) when the branch is read p-adically. Congruences to other primes (split_d-type invariants) cannot get past the wall *as part of a cover/stopping-time certificate*; other global uses of a mod-q invariant are not excluded. | PROVED | mixing.md / check_mixing.py [Nhat] |
| Theorem R | For any unit system with an expanding cycle, the run map (or any excursion map containing the full run along C) is not a rational (finite-transducer) relation in base p. The reason is that the powers U^d are not p-automatic (Cobham). This closes the automata route the lens proposed; it does not say first-return maps are never rational (the 3x+1 Syracuse map is rational in base 2). | PROVED (cites Cobham 1969) | mixing.md |
| Theorem C | If a cycle of a map with multipliers in {1, a} has all elements > Z0, then 1 < p^X/a^Y <= 1 + cX/Z0. An exact search over Y gives a length bound. | PROVED | cycles.md / cycle_bound.py, check_cycles.py |
| C1 | sf3_7 (K7), sf3_17, sf3_57, sf3_157, sf3_357, sf3_13, sf3_135: every unlisted cycle has all elements > 10^11 and length >= 492531 (K7 in z-form: elements >= 5·10^10, length >= 190537) | PROVED (C verification to 10^11, runs/results.txt; default check proves the 10^9 version) | cycles.md |
| C2 | G3 (new core): every cycle other than 1 has all elements > 10^11 and length >= 222404 | PROVED (10^11 run, runs/results_g3.txt; default check: 10^9, length >= 31867) | cycles.md |
| K1–K2 | K7 excursion: 2^j u − 1 ↦ odd part of 3^{j−1}u − 1 ("3x+1 with one factor 3 removed per excursion"). Sharp bounds S(z) + 1/2 <= (3^{j−1}/2^{j+1})(z+1) and S(z) <= ((z+1)^{log_2 3} − 3)/6, both attained. | PROVED | k7.md / check_k7.py |
| K3 | Induction closes in one excursion off B1 ⊂ {z ≡ −1 mod 32}, density δ1 = 0.0362745…; for every k there are explicit z with k rising excursions | PROVED | k7.md / check_k7.py |
| census | F2m2, F2m3, F3m2, F3m2b: 168 / 6044 / 16668 / 31225 c_mixed tables, all OBST, sorted by (u, s = v_p(u−1), sign of x*) | PROVED (counts, types); orbit statistics EVIDENCE | census_small.md / check_census.py |
| type (b) | the 36 type-(b) tables of F3m2: Theorem H run, complete cycle lists ({1,2}: 18, {1}: 12, {2}: 6) | PROVED (not type (c)) | census_small.md / check_typeb.py, typeb_cycles.json |
| G3 | G3(n) = (4n+1)/3 if n ≡ 8 (mod 9), else ⌈n/3⌉. Type (c), OBST. Every n <= 10^11 reaches 1. | type: PROVED; GLOBAL: OPEN (EVIDENCE to 10^11) | census_small.md |
| K7, G3, all 8 cores | GLOBAL | OPEN | |

## Where the method stalled

* **Integrality as "n >= p^depth"** only caps the growth of one excursion, at
  z^{log_2 3}/6 for K7 and n^{log_3 4} for G3. Both caps are attained. It says
  nothing about how many rising excursions follow. Theorem M shows that the
  next excursion is independent of everything finite that came before.
* **Fixing digits** (u ≡ 1 mod p^s) fails because the free part m of n is
  uniform. Predictability of u^k m given m is useless when m is free (Theorem M).
* **Other moduli** fail because the expanding periodic points y_d live in Z_p,
  and integers near them can have any residue modulo anything coprime to p
  (Theorem N̂). A non-unit multiplier is what breaks this, which is the
  mixed-base escape round 3 already found.
* **Transducers** fail for the run map (and any excursion map containing a
  full run) because U^d for unbounded d is not automatic (Theorem R).
* **Real size via the cycle identity** works, but only for cycles, and only up
  to a length bound. The bound is set by the continued-fraction convergents
  of log_p a, and it grows without bound with Z0. (The first version called
  these "the same near-critical ratios" as the 80/81 cycle behind
  dch_C27_2466's 2466-step depth. That was wrong and is withdrawn; see the
  revision section.) A divergent orbit has no product identity, so this tool
  gives nothing on divergence.

I found no type-(c) system, natural or designed, where I could exclude
divergence. Every design I tried reduced to an avoidance or Mahler-type
problem of the same kind as 3x+1. Examples: a type-(c) SCC with a contracting
downstream part, where one must show that no positive integer stays in the SCC
forever. Another: n ↦ ⌈5n/4⌉ staying odd forever.

## Tests against 3x+1 and known cycles

* Theorems M, N̂ and R are impossibility statements. All of them hold for
  3x+1 and prove nothing about it.
* Theorem C on 3x+1 is the classical cycle-length bound and nothing more. The
  verifier fails, as it must, for sf3_13 when its second cycle (3 10 5 6) is
  left out, and for the core W at n = 15, whose orbit passes 10^60
  ([C-neg]).
* [M-iid] failed in a first draft because of a truncation bias in the counting,
  not because of the mathematics. The final check counts only events decided at
  the chosen precision, and the joint counts then factor exactly.

## Files

| file | content |
|---|---|
| mixing.md | Theorems M, N̂, R (task 4) |
| cycles.md | Theorem C and Corollaries C1, C2 |
| k7.md | K7 excursion map and inequality (task 3) |
| census_small.md | small type-(c) census, sorted; the core G3 (task 1) |
| intlib.py | exact SCC typing (a / b / c_mixed / c_exp) on top of round3 accel and dichotomy tools |
| census_small.py, analyze_census.py | enumeration and sorting; output enum_*.json, census_small_summary.json |
| cycle_bound.py | exact (Y_fail, X_fail) search for Theorem C |
| sfverify.c, g3verify.c | exact 128-bit "every n <= Z0 drops below itself" verifiers |
| runs/ | job list and outputs of the 10^11 runs |
| check_mixing.py, check_cycles.py, check_k7.py, check_census.py | checks; all exit 0 |
| check_typeb.py, typeb_cycles.json | Theorem H on the 36 type-(b) tables (added after REFEREE1) |
| REFEREE1.md, referee1_check.py | referee report and the referee's independent check (not edited) |

## Reproducing

    python3 check_mixing.py          # < 1 s
    python3 check_k7.py              # ~ 3 s
    python3 check_census.py          # ~ 1 min
    python3 check_typeb.py           # ~ 10 s
    python3 check_cycles.py          # ~ 1 min (Z0 = 10^9)
    python3 check_cycles.py --full   # ~ 30+ min on 11 cores (Z0 = 10^11)

## Novelty

Not checked by literature search. Theorem C is the classical Steiner/Eliahou
cycle argument, applied here to new maps. Theorem M is a restatement of the
Markov property in the style of Terras and Lagarias. Theorem R is an
application of Cobham's theorem. Theorem N̂ is a small extension of round 3's
Theorem N.

## Revision after REFEREE1

REFEREE1 confirmed every theorem, bound and count, and asked for wording
repairs. Nothing proved changed; one sentence was wrong and several were too
broad. Item by item:

| item | verdict | what was done |
|---|---|---|
| dch_C27_2466 analogy (cycles.md, README) | WRONG | **Withdrawn and rewritten.** The 2466-step depth of dch_C27_2466 is a fixed finite number in a *settled* base-3 table with multipliers 1, 2, 4, 5. It is the minimal depth of a plain descent certificate, forced by one 11-step contracting residue cycle with multiplier 80/81 = 2^4·5/3^4 (mean log-multiplier −0.001129 per step), the max-mean cycle of a finite graph. No ratio log a/log p and no rational approximation is involved. Theorem C's threshold (Y_fail, X_fail) is instead set by the convergents of log_2 3 or log_3 4 and grows without bound with Z0. The two share only the loose theme "a product of multipliers close to 1". The 2466 figure itself is correct. |
| lap count off by one (mixing.md) | fix | Definition now says the first dℓ *steps* follow C^d (residues at times 0..dℓ, including the return to r0). The checks already used the correct convention. |
| proportion in Theorem M(3) | nit | now "proportion of n <= X in [r0]_K". |
| Theorem R "Consequence" | fix | narrowed to the run map and to excursion maps containing a full run; the broader sentence is withdrawn, with the Syracuse map as the counterexample to the broad form. |
| Theorem N̂ wording | suggestion | now "cannot get past the wall as part of a cover/stopping-time certificate". |
| "only Archimedean size is left" (README, mixing.md, cycles.md) | fix | relabelled HEURISTIC in all three places, with the list of what the theorems actually exclude. |
| Type (b) "settled by Theorem H" | fix | Theorem H was not run before. It now is (`check_typeb.py`, exits 0, with a negative control): all 36 tables satisfy the hypotheses at level 2; cycle lists recorded. Status PROVED. |
| c_exp "trivially divergent" | fix | withdrawn; nothing is claimed about c_exp orbits. |
| Theorem C, Y = 0 | nit | one line added: Y = 0 gives Z0(p − 1) <= c, false. |
| δ1 digits (k7.md) | nit | 0.0362745… (exact partial sum 0.0362745023). |
| "nobody has done it" (cycles.md) | fix | withdrawn; now "not found in this repository; literature not checked". |

The verdict on the hard criterion is unchanged: no type-(c) system is settled
here. GLOBAL stays OPEN for K7, G3 and all 8 cores.
