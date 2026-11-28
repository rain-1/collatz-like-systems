# Referee 2 report: round 4, lens "transport" (second pass, after the REFEREE1 repair)

Scope: the whole folder (`README.md`, `transport_theorems.md`, code, `results/`), with context from
`round3/README.md` and `round3/accel/trichotomy.md`. I did not edit any of the prover's files and I
made no commits.

My own check is `referee2_check.py`. I wrote it from scratch, and it uses exact int and Fraction
arithmetic. It does not import `transport_lib`, `equiv`, `check_transport`, `referee1_check` or
`decide`. It reads `library.py` and `results/*.json` only as data. The tables that the theorems are
about (3x+1, G, G′, the S-family and dch_C27_2466) are rebuilt from their rules. To decide the sign
of a cycle it uses its own engine:

* an exact Karp maximum cycle mean, done multiplicatively and comparing r1^e2 with r2^e1;
* its own iterative Tarjan;
* its own cylinder graph, Lemma S and trichotomy type.

Run times and exit codes:

* `python3 referee2_check.py`: about 24 s, exit 0, "REFEREE2 CHECKS PASSED".
* Prover's `python3 check_transport.py`: about 10 s, exit 0, "ALL CHECKS PASSED".
* `python3 referee1_check.py`: exit 0.
* `python3 nonunit_breakdown.py`: exit 0, giving 24 pairing + 7 dressed.

I tested that my script can fail by injecting two faults:

* a perturbed G (constant −2 changed to +2 on z ≡ 2 mod 4);
* replacing core sf3_7 by sf3_37, which is 3x+1 in disguise.

Both runs failed: 8 failures in total, including "cores collide sf3_7 3x+1" and a count of 45
instead of 43.

## Headline

**The hard criterion of the round is not met, and the folder does not claim it is.** No
unit-multiplier type-(c) system is claimed to be settled. So there is no settled system whose type
needs re-checking, and no cycle list whose completeness needs proving as a settlement claim.

The positive content is of two kinds:

* Equivalences with 3x+1, correctly labelled "PROVED (equivalence; GLOBAL OPEN)". I checked
  independently that the systems involved really are type (c). They are not easy cases in disguise:
  each is exactly as hard as Collatz.
* Barrier theorems O1 and O2, which say that bounded-return transport cannot start from a
  certificate-settled system. O2 adds the same for a Theorem-H system through p-adic classes.

I re-derived every proof. I found no mathematical error. Every REFEREE1 item is honestly resolved
except for one residual sentence in the theorem file, a leftover of item 5, which is listed below.
There is also a new minor nit in the O1 proof.

## Verdicts

| # | claim | verdict |
|---|---|---|
| 1 | Lemma P | CONFIRMED |
| 2 | Theorem E | CONFIRMED |
| 3 | Lemma S | CONFIRMED |
| 4 | Proposition C (with the corrected cycle argument) | CONFIRMED |
| 5 | Theorem F, including cycle correspondence | CONFIRMED |
| 6 | S-family classes (42 / 264 / 20; cut-offs stated) | CONFIRMED |
| 7 | 8 cores not joined (34 + 9 = 43; exact on 2-power classes) | CONFIRMED |
| 8 | Lemma B, Lemma R | CONFIRMED |
| 9 | Theorem O1 | CONFIRMED_WITH_FIX (two wording fixes, no change to the result) |
| 10 | Theorem O2 ("type (c) or critical") | CONFIRMED |
| 11 | Non-unit search (EVIDENCE; 31 = 24 + 7) | CONFIRMED |
| 12 | Hard criterion not met; open door; honest limits | CONFIRMED |
| 13 | Labels and novelty | CONFIRMED |
| 14 | REFEREE1 repair list | 7 of 8 fully resolved; item 5 has one residual sentence (see 9) |

## Details

### 1–3. Lemma P, Theorem E, Lemma S

**Lemma P.** Refining until Q | a·Mod/d makes the branch constant, and M_X | a·Mod/d makes
membership in X constant. That is exactly the splitting rule of my engine, which works in a fresh
variable k with the value α k + β.

**Theorem E.**

* (1)–(3): I checked the boundary point. If r_X = 0 then D_X = {z ≥ 1}, otherwise D_X = {z ≥ 0}.
  G(0) is the z-value of a positive integer, so it lies in D_Y.
* (4): one lap of R is one lap of the cycle, and an affine conjugation keeps the slope.

**Lemma S.**

* The edge rule y ≡ T(x) (mod gcd(uM/w, M)) is a correct over-approximation, because
  T(x + Mt) = T(x) + (uM/w)t.
* An infinite walk ends in one SCC.
* A pure-dilation SCC cannot hold a positive orbit forever.
* A contracting SCC has a strict potential, which bounds the orbit.
* Merging uses only T(dn) = n.

My own Lemma S uses an exact Karp sign instead of the prover's 1001/1000 inflation. It agrees on
every one of the 4857 recorded join members. It rejects these controls:

* (3x+1, 1 mod 4);
* (3x+1, 0 mod 3);
* (5x+1, 3 mod 4);
* a table with a neutral loop (odd n → n+4, X = 1 mod 4).

It accepts (3x+1, 3 mod 4), which is correct.

### 4. Proposition C

I re-derived all three branches by hand. With n = 3z+2:

* **z odd:** 9z+7 ≡ 1 (mod 3), then (9z+7)/2 ≡ 2, giving (3z+1)/2 in 2 steps.
* **z ≡ 0 (mod 4):** 3z/2+1 is odd and ≡ 1, then 9z/2+4 ≡ 1, then 9z/4+2 ≡ 2, giving 3z/4 in
  3 steps.
* **z ≡ 2 (mod 4):** 3z/2+1 is even and ≡ 1, then (3z+2)/4 ≡ 2, giving (z−2)/4 in 3 steps.

With y = z+1 these become 3y/2, (3y+1)/4 and (y+1)/4.

My engine reproduces G exactly, with maximum return time 3. Brute force agrees for z < 2·10^5, and
the conjugation G′ = G(y−1)+1 holds for y < 10^5.

**The corrected argument "every C-cycle meets 2 mod 3" is right.** An odd n ≡ 0 (mod 3) goes to
1 (mod 3). An odd n ≡ 1 (mod 3) has n ≡ 1 (mod 6), so 3n+1 ≡ 4 (mod 18), and the next value
(3n+1)/2 ≡ 2 (mod 9). I also checked this by brute force for n < 3·10^5.

The old wrong justification is withdrawn openly.

**Types, with my own graph:**

* G and G′ are type (c), and so is 3x+1 itself.
* G′ has both quoted loops: 0 → 0 with multiplier 3/2, and 2 → 1 → 2 with multiplier 9/8.

**"Disguised easy case" test.** None. G′ is a conjugate of the Collatz first return, so it is
exactly as hard as Collatz.

My brute force sends every G′-orbit from y ≤ 10^6 to the fixed point 1, and finds no other cycle.
This is EVIDENCE only, and it is consistent with the claim that the G′-cycles correspond to the
C-cycles.

### 5. Theorem F

I re-derived the three cases (2+2, 4 and 4 steps). My engine reproduces G for the four sets, with
maximum return time 4. Brute force agrees for z < 10^5.

**The hypothesis is sharp.** Among all 256 subsets S at m = 4, exactly the four stated sets give G
on 3 mod 4. My check confirms that no fifth set does.

**Lemma S** gives the contracting component {1,2} when 1 ∉ S and {1,2,4} when 1 ∈ S. All four
tables are type (c).

**Cycle list, brute force over all starts n ≤ 10^6, for each of the four sets.** The cycles are
exactly:

* (1 2) or (1 4 2);
* (3 10 5 6).

For n < 2·10^4, an orbit ends in (3 10 5 6) if and only if it meets 3 mod 4. This agrees with the
statement "the orbits that never meet 3 mod 4 are exactly those ending in (1 2)/(1 4 2)", and that
statement is also correct as a theorem (bounded return keeps an X-orbit in X).

The label "PROVED (equivalence; GLOBAL OPEN)" is accurate.

### 6. S-family classes

I re-proved all 4857 join members with my own engine and my own Lemma S. Each sfam member was
rebuilt from its id, not read from the prover's population. The checks:

* Every library member of a class has status `open`.
* Every unit member is type (c).
* There are 42 classes with 264 members, and the Collatz class has 20 members.

The search cut-offs tmax = 24, pmax = 20000 and Lmax = 4096 are now stated in the theorem file and
in "Honest limits".

The split of the claim "no class contains a settled system" into three parts is now correct and
honest:

* forced by O1 for certificate systems;
* forced by O2 for p-adic classes of Theorem-H systems;
* observed for the rest.

### 7. Eight cores

My own engine finds 43 bounded canonical returns, counting the 9 maps, with no collision. That holds
at tmax = 24 and also at tmax = **80** with a piece cap of 100000. The prover went to 64, so this
extends REFEREE1's result.

I also wrote my own exact criterion for the 2-power classes 2^s ≤ 32. A return is unbounded iff an
X-vertex has an edge into a non-X vertex that can reach a non-X cycle. The criterion is sound: ⇐ by
the Markov property, which realises the walk into the cycle for every d; ⇒ by finiteness.

* It finds 16 bounded returns, the same as the prover.
* It agrees class by class with the search at tmax = 80.

The remaining limit, classes with an odd factor, is stated honestly.

### 8. Lemma B, Lemma R

**Lemma B** is correct: B(x) ≤ (Λ+K)x for x ≥ 1, values between descents stay at most (Λ+K)^J
times the current descent point, and a value ≤ N₀ is followed by a value ≤ ΛN₀ + K.

**Lemma R** is correct: Markov realisation of P C^d, plus CRT with q.

I also checked the exact witness for G′: on y = 2^{d+1}·7, the map G′^d multiplies by (3/2)^d, for
every d ≤ 29.

**dch_C27_2466** (the 2466-step certificate; the user's point of interest):

* I rebuilt it from the rule text, and it matches `library.py`.
* It is unit 3-adic, of type (a), with no division-free cycle.
* Its cylinder graph mod 27 has maximum cycle multiplier 80/81 on a cycle of length 11, which
  matches `dch_C27_2466.md`.
* All starts n ≤ 2·10^5 end in exactly the three cycles with minima 1, 5 and 125.
* max orbit / max(n, 2000) is at most 142.2, which shows the linear bound that Lemma B predicts.

So the README's use of it as an O1 example is right. It cannot be a transport source for any table
with realised growth, and a 2466-step depth does not change that: depth is irrelevant to Lemma B.

### 9. Theorem O1 — CONFIRMED_WITH_FIX

I re-derived the proof. With h = h_X ∘ h_Y^{-1}, so α = M_X/M_Y, an identity of Theorem E fits the
window hypothesis with L = τ_max. The fixed time t_d (the REFEREE1 fix) is used correctly.

**Falsification test (new).** If O1 were false, a certificate system could have a bounded first
return that is a unit table with an expanding cycle. I computed every bounded first return of every
library CERT system on all classes M ≤ 24.

* 32 of these returns are unit p-adic tables, and all 32 are type (a): no expanding cycle at all.
* One more return with canonical modulus > 512 was not typed.

So O1 is consistent with the data. Likewise:

* None of the 14 unit returns of Theorem-H systems to p-adic classes is type (c), which agrees
  with O2.
* None of the 220 distinct sufficient canonical returns of the library is shared between a settled
  and an unsettled or divergent system.

**Fixes (wording only):**

1. *Residual from REFEREE1 item 5.* `transport_theorems.md` line 220 still says certificate
   systems "can never be the source of a transport to an OBST system". The README was corrected,
   but this sentence was not. It should say "to a unit p-adic table with an expanding cycle
   reachable from X". Non-unit OBST targets, such as dressed maps, are not covered.
2. *New nit in the proof.* "h(b) ≥ μ^L λ_P λ_C^d n − c_d" is wrong as written when μ > 1, because
   the sampled time is t_d + i with i < L, not t_d + L. Use min(μ, 1)^L. The conclusion is
   unchanged.

**Optional strengthening, not required.** For a p-adic class X, Lemma S on (A, X) already forces
an expanding cycle of A to be reachable from X. If every vertex of the cycle were outside G, the
cycle would lie in a restricted SCC that is neither pure dilation nor contracting. A cycle vertex v
in G is reached from the X-vertex d^j v by j dilation steps. So in any transport that would *settle*
A (which needs Lemma S on the A side), the reachability hypothesis of O1 holds automatically. This
would make the Corollary in §3 sharper.

### 10. Theorem O2 — CONFIRMED

I re-derived the proof:

* The pieces are p-adic cylinders.
* Ĝ is defined on all of Z_p, because ĥ_X^{-1}(X̄) = Z_p.
* The periodic points from C^d W, with multiplier > 1, lie in X̄.
* R̂_A-periodic points map to R̂_B-periodic points, then to B̂-periodic points with the same slope.
* Distinct orbits stay distinct.

Under the standing hypothesis, a table with no type-(c) component has only finitely many expanding
periodic orbits. The conclusion "type (c) or critical" is the corrected and correct form. In a unit
table a cycle of multiplier exactly 1 is division-free, so the case split is complete.

### 11. Non-unit search — CONFIRMED (EVIDENCE)

`check_transport.py` part G now really re-runs M ≤ 144, giving 117,390 pairs, 31 bounded and
0 unit. `nonunit_breakdown.py` confirms the split into 24 pairing P2 symmetries and 7 dressed
returns to qZ, all to the class 0 (mod M_Y). The label EVIDENCE is right.

### 12–13. Outcome, limits, labels, novelty

* The README's first lines state that the hard criterion is not met.
* The open door is correctly identified as not covered by O1 or O2: unbounded first returns of
  pairing or dressed systems, and O2 for mod-q classes.
* The remark on fx10_64 and fx26_32 (type (c) with proved divergence) is correct and honest.

**Would the method prove something false or famous?**

* 3x+1 has only 4 bounded first returns on classes 2 ≤ M ≤ 64. All 4 are type (c), so none would
  "prove" Collatz.
* No join links a divergent system to a settled one.
* The identity engine rejects a perturbed G.
* The Theorem F hypothesis is sharp.

So nothing false is proved.

"Novelty: not checked" is stated throughout. Proposition C is a reformulation of 3x+1 in the
classical spirit and is not claimed to be new.

## Repair list

1. `transport_theorems.md` line 220: "to an OBST system" → "to a unit p-adic table with an
   expanding cycle reachable from X (Lemma R)". This finishes REFEREE1 item 5.
2. O1 proof: μ^L → min(μ, 1)^L.

Both are wording fixes and do not change any result. Strictly speaking, item 1 is a residual
overstatement of scope in a PROVED section, so I set needs_repair = true. The repair is a
one-sentence edit.
