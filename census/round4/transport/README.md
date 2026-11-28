# Round 4, lens "transport": moving proofs between table maps

Goal of the lens: settle a unit-multiplier system of type (c) (an expanding residue cycle that
shares a strongly connected component with another cycle, so Theorem N of
`round3/accel/trichotomy.md` excludes certificates) by an exact identity with a system that is
already settled.

**Outcome: the hard criterion was not met.** No unit type-(c) system was settled by a
convergence proof. What the lens produced:

1. a proved extension of the wall to transport proofs (Theorems O1, O2): an identity of the kinds
   searched can never carry a proof from a certificate-settled system (any modulus, unit or not)
   to a unit p-adic table with an expanding cycle reachable from the class (every type-(c)
   system qualifies), nor, through p-adic classes, from a Theorem-H system to a type-(c) one;
2. an exact searcher for transport identities and one positive structural result: a 4-branch
   normal form of 3x+1 (Proposition C) and four S-family members (m = 4) that are exactly 3x+1
   (Theorem F), plus 39 further equivalence classes inside the S-family at m = 5;
3. a precise statement of the one transport route these theorems leave open.

All labels below are exact. Novelty: not checked for anything in this folder.

## Results

| item | statement | status | where |
|---|---|---|---|
| Lemma P, Theorem E | a bounded first-return identity G_A^X = G_B^Y transports eventual periodicity and cycles (with multipliers) between the classes; with the sufficiency Lemma S it transports GLOBAL | PROVED | transport_theorems.md §0–1 |
| Lemma S | exact sufficient condition for "every orbit merges with an orbit from X or is eventually periodic in a contracting part" | PROVED | §1 |
| Proposition C | 3x+1 (n/2, 3n+1) on n ≡ 2 (mod 3), y = (n+1)/3: G'(y) = 3y/2 (y even), (3y+1)/4 (y ≡ 1 mod 4), (y+1)/4 (y ≡ 3 mod 4). Collatz ⇔ every G'-orbit eventually periodic; every 3x+1 cycle meets 2 mod 3 (justification corrected after REFEREE1). G' is unit 2-adic, type (c) (self-loop 0 → 0 of multiplier 3/2), decide.py OBST | PROVED (equivalence; GLOBAL OPEN) | §2 |
| Theorem F | S-family T_S with S ∩ {3,7,11,15} = {3,7,15} mod 16 and S ∩ {5,13} = ∅ (4 sets): first return to 3 mod 4 equals G; GLOBAL(T_S) ⇔ 3x+1 has no divergent orbit; all four OBST, type (c) | PROVED (equivalence; GLOBAL OPEN) | §2 |
| S-family classes | m ≤ 5: 42 transport classes with 264 members (the 3x+1 class has 20), counts exact for the searched class with cut-offs tmax = 24, pmax = 20000, Lmax = 4096; no class mixes types; no class contains a settled system (forced by O1 for certificate systems and by O2 for p-adic classes of Theorem-H systems; observed for the rest) | PROVED per join (finite) | results/equiv_*.json |
| 8 cores | no identity of the searched kind joins two of the 8 cores of accel/sfamily_obst.md or a core with 3x+1. On classes M ≤ 32 only 34 first returns come back within 24 steps (43 canonical maps with the 9 maps themselves), still 34 within 64 steps, and those are pairwise distinct. On 2-power classes boundedness is decided exactly; on classes with an odd factor a return longer than 64 steps is not excluded. A weak negative statement | PROVED (finite, for that stated class) | check parts F, F2 |
| Lemma B, Lemma R | a plain certificate bounds every orbit linearly; an OBST unit table has orbits with unbounded ratio max/start in every class reaching the expanding cycle | PROVED | §3 |
| **Theorem O1** | if A is a unit p-adic table with an expanding cycle reachable in its residue graph from the p-part of X (Lemma R; every type-(c) system qualifies with X = all integers; non-unit OBST systems such as dressed maps are NOT covered) and its orbits from X appear, through an affine h and with bounded gaps (or as a subsequence of every value), inside B-orbits, then B has no plain descent certificate at any modulus. So decide.py-CERT systems (dch_C27_2466 included), the plain mixed-radix certificates of mixedbase, and every other plain certificate can never be a transport source | PROVED | §3 |
| **Theorem O2** | p-adic bounded first-return identities between unit p-adic tables carry a type-(c) component that meets the class to infinitely many expanding periodic orbits of the target, so the target is type (c) or critical (type (c) under the standing no-division-free-cycle hypothesis): no transport from Theorem-H (type b) or certifiable systems | PROVED | §3 |
| non-unit sources | for 30 Farkas-pairing and dressed systems and 117,390 classes (M ≤ 144), only 31 first returns are bounded (within 30 steps, piece cap 4000): 24 scaling symmetries x*Z of pairing systems (P2) and 7 returns of dressed systems to qZ, all to 0 mod M_Y, none a unit p-adic table | EVIDENCE (exact per case) | search_nonunit.py, nonunit_breakdown.py, check part G (reproduces M ≤ 48 and M ≤ 144) |
| open door | an *unbounded* first return (infinitely many affine pieces) of a pairing or dressed system conjugate to a unit type-(c) table; O2 for classes mod q with p ∤ q | OPEN | §5 |

Two remarks that bear on the hard criterion:

* The 5x+1 modifications fx10_64 and fx26_32 of `round3/divergence` are unit 2-adic tables of
  type (c) (checked here with `unit_type`), and round 3 proved divergent orbits for them. So
  type (c) by itself does not block a *divergence* proof; the wall concerns proofs that every
  orbit is eventually periodic. This lens did not add new divergent systems.
* Corollary of O1 and O2: a transport proof of convergence for an OBST unit system needs a
  source whose orbits have unbounded excursion ratio and that is settled by something other
  than a certificate: a Farkas pairing system (run-accelerated block argument), a dressed
  system, or a Theorem-H system reached through a non-p-adic class. The search found none of
  these giving a unit table with bounded return times; the remaining possibility needs
  infinite-piece first returns, which the canonical-table method cannot represent.

## Where the method stalled, exactly

Bounded first returns of a unit p-adic table to a p-adic class are again unit p-adic tables,
and Theorem O2 shows they keep type (c). Moving to a class mod q (p ∤ q) breaks the p-adic
structure, but Theorem O1 still applies to any certificate-settled target. The only settled
systems with unbounded excursions that are not certificate-settled are non-unit (Farkas,
dressing). Their branch depends on n mod a, and after one up-run block the residue mod a is
fresh again (P1 of `round3/mixedbase/pairing_family.md`), so a first return either keeps the
mod-a dependence (not a unit table) or has unbounded return time (not a table at all). The search
confirms this in every case tried.

## Files

| file | content |
|---|---|
| transport_theorems.md | all definitions, statements and proofs |
| transport_lib.py | exact first-return pieces, canonical forms, Lemma S, exact trichotomy type |
| library.py | the systems: census open tables, the 8 cores, round-3 settled systems (CERT, Theorem H, mixedbase, dressing, divergence) |
| search.py | hash-join of canonical first returns (no sufficiency) |
| equiv.py | transport equivalence classes with Lemma S on both sides; one-way implications |
| analyze_classes.py | types of the members of each class |
| search_nonunit.py | first returns of settled non-unit systems, test for unit p-adic tables |
| nonunit_breakdown.py | lists the 31 bounded non-unit returns at M ≤ 144 by system (`results/nonunit_144_breakdown.txt`); exits 1 unless 24 pairing + 7 dressed, all to 0 mod M_Y |
| REFEREE1.md, referee1_check.py | referee report and the referee's independent check (not written by the prover) |
| check_transport.py | exact checks: independent identity verifier, Proposition C (with B2: every 3x+1 cycle meets 2 mod 3), Theorem F, all 4857 recorded join members, growth witnesses, core distinctness (F, and F2: exact boundedness on 2-power classes, re-run at 64 steps), non-unit search at M ≤ 48 and M ≤ 144; exits 0 (about 15 s) |
| results/ | search outputs (`equiv_lib.json`, `equiv_sfam4.json`, `equiv_sfam5.json`, `nonunit_*.json`, `search_*.json`) |

Reproduce: `nice python3 equiv.py sfam5` (about 100 s) regenerates the largest result file;
`python3 check_transport.py` re-verifies everything that the documents claim.

## Honest limits

* The transport class searched is narrow: single classes with M ∈ {2,…,10, 12, 16, 18, 24, 27, 32} (M ≤ 9 for the m = 5 tables),
  bounded first returns, affine conjugacies h(z) = Mz + r, and the cut-offs of `equiv.py`:
  return time ≤ 24, ≤ 20000 pieces, canonical modulus ≤ 4096. A return beyond a cut-off counts
  as absent. Identities between unions of classes,
  chains through intermediate maps not in the population, and unbounded first returns were not
  searched.
* Lemma S is only a sufficient condition. Several one-way implications (for example
  par_3_5 ⇒ par_3_1, perm_swap ⇒ perm_1932) are two-way equivalences in `census/lhf`, proved
  there by other arguments; the searcher simply could not prove the reverse direction.
* Theorem F and Proposition C relate open problems to open problems. The m = 5 classes mostly
  join tables that differ only on classes the first return never uses; they shrink the family
  but are close to trivial.
* Theorem O1 excludes plain certificates only. Run-accelerated certificates for non-unit
  targets are not excluded; that is the open door above.

## Revision after REFEREE1

REFEREE1 (`REFEREE1.md`) found no mathematical error; it confirmed every proof and every
recorded join with an independent engine. It listed seven text repairs. All are made, and two
checks were added. Explicit corrections and withdrawals:

1. **Proposition C, "every C-cycle meets 2 (mod 3)".** The cited reason ("by Lemma S and
   bounded return") was WRONG; the claim itself is true. The text now gives the direct argument
   (a point ≡ 1 mod 3 reaches 2 mod 3 within two steps; no cycle stays in 0 mod 3), and part B2
   of `check_transport.py` checks the residue facts. The 9/8 versus 3/2 wording is fixed (both
   loops are quoted), and "which is exactly why it stays Collatz-hard" is now marked as a remark.
2. **§2 counts.** The search cut-offs tmax = 24, pmax = 20000, Lmax = 4096 are now stated in the
   theorem file and in Honest limits.
3. **"No class contains a settled system … forced by the theorems."** WITHDRAWN as stated. It is
   forced by O1 for certificate systems and by O2 for p-adic classes of Theorem-H systems; for
   mod-q classes of acc_h16/acc_h32 and for the dressed, mixed and divergent library systems it
   is only an observed search outcome.
4. **8 cores.** "Bounded" meant "returns within 24 steps". Now stated as such. New part F2:
   the count stays 34 (43 with the maps) at 64 steps and piece cap 60000, with no collision, and
   on the 2-power classes boundedness is decided exactly by a residue-graph criterion (Lemma 1 of
   `dichotomy.md`), so on those classes the distinctness statement is complete.
5. **README O1 row.** "A is OBST" replaced by the actual hypothesis (unit p-adic table with an
   expanding cycle reachable from X). Non-unit OBST systems are not covered by O1.
   The O1 proof now uses the fixed time t_d = |P| + d|C| instead of "a time of maximum".
6. **O2.** The conclusion is now "type (c) or critical", and "type (c)" under the standing
   hypothesis (no division-free cycle), which is stated.
7. **Non-unit search.** "All 31 are scaling symmetries" was WRONG for 7 of them: 24 are P2
   scaling symmetries of pairing systems, 7 are returns of dressed systems to qZ. All 31 are
   returns to 0 mod M_Y and none is a unit table. `check_transport.py` part G now reproduces the
   M ≤ 144 result as well (about 7 s), and `nonunit_breakdown.py` checks the 24 + 7 split.
8. **Nit.** The docstring of `transport_lib.sufficient` now describes the implemented full
   Lemma S (dilation and contracting components), not "acyclic".

None of these changes the outcome: the hard criterion is still not met, and no system in this
folder is claimed to be settled. On the dch_C27_2466 question (the 2466-step certificate): it
remains a valid example for O1. It is a unit 3-adic table with a plain certificate, so by
Lemma B its orbits are linearly bounded and it cannot be a transport source for any table with
realised growth; the constant (Λ+K)^2466 of Lemma B is very loose, and the Lyapunov function of
`round3/dichotomy/dch_C27_2466.md` gives a much better linear bound, but the conclusion is the
same.

## Revision after REFEREE2

REFEREE2 (`REFEREE2.md`) confirmed every claim and listed two wording repairs to Theorem O1,
neither of which changes a result. Both are made:

1. **Residual from REFEREE1 item 5.** `transport_theorems.md`, the sentence after the O1 proof
   said certificate systems can never be a transport source "to an OBST system". It now says
   "to a unit p-adic table with an expanding cycle reachable from X (Lemma R)", and adds that
   non-unit OBST targets, such as dressed maps, are not covered.
2. **O1 proof.** The lower bound h(b) ≥ μ^L λ_P λ_C^d n − c_d was wrong as written when μ > 1,
   because the sampled time is t_d + i with i < L. All three occurrences now use min(μ, 1)^L.
   The conclusion is unchanged.

The optional strengthening REFEREE2 suggests (reachability is automatic in any transport that
would settle A) is not adopted here.
