# Round 4 (27 November 2026): four attempts at a new proof method

Round 3 proved that for unit-multiplier table maps with "free re-entry" (type (c): an
expanding residue cycle sharing a component with another cycle) no descent certificate and
no accelerated certificate exists. Round 4 asked four lenses for a NEW proof method that
settles at least one such system. Each lens was refereed twice.

**Result: no type-(c) system was settled.** All four lenses report the second-best
outcome: a proof that their method cannot work, with the exact reason. Positive
by-products are listed below. Everything is agent-written and agent-refereed; none has had
human review. `../round4_results.json` holds every prover claim and referee verdict.

## What each lens found

| Folder | Method tried | Why it fails (proved) | Positive results |
|---|---|---|---|
| `wpotential` | Lyapunov functions computed from all digits (residue weights, size, counters, digit windows, lexicographic and ordinal combinations) | Theorem W: a descending potential cannot be roughly monotone in size near any expanding periodic point, and in type (c) such points are dense in a Cantor set. Digit-window potentials collapse to "digit count plus bounded" (windows up to 10 for a x3 branch, 8 for x5) | counters at finitely many points do certify type-(b) systems (acc_h16) |
| `integrality` | finite digit expansions and real size; the map from one expanding run to the next | Theorem M: in every unit system the run-to-run process is full-branch and independent on finite windows, whatever the multiplier; other moduli do not help; the run map is never automatic | cycle bounds from the product identity: for K7 and the seven other S-cores every start up to 10^11 reaches a known cycle, and any unknown cycle has length at least 190,537 (K7) or 492,531; new base-3 core G3 |
| `transport` | exact conjugacy or first-return identity with an already settled system | Theorem O1: no system with realised growth can be transported from a plainly certified system; Theorem O2: bounded p-adic first returns preserve type (c) | four more S-family systems (mod 16) are exactly 3x+1; a 4-branch normal form equivalent to 3x+1; 42 transport classes among 264 S-family members; no identity joins any two of the 8 cores |
| `schema` | an open system as a limit of certifiable ones | Theorem B1: changing a type-(c) table near finitely many points leaves it type (c) (3x+1 cut at depth j is type (c) from j = 3, K7 from j = 6). Window approximants are certifiable for every N, but "every orbit eventually avoids the reset set" is equivalent to the conjecture for each N in [4, 26] | certificate depth records 41,362 (modulus 256), 133,534 (512) and 304,506 (1024), each with an integer witness (round 3 record: 2466); unbounded depth proved for a designed base-2 family, growing at least like Q^2 log Q; the distance of 3x+1 to a certifiable system, as a fraction of residues, tends to 0 |
| `lundberg` (written outside the loop, not refereed) | one exponent per system | does not settle anything | the trichotomy as a statement about two exponents; ranking of open systems by distance from the provable class |

## What is still not ruled out

1. **A size statement.** `schema/window.md` Theorem W4: if for some constant C no stretch
   of C log2 n or more consecutive steps in the 3x+1 orbit of n has more than 5/8 odd steps,
   then the 3x+1 conjecture follows. Numerically C near 20 fits. This is a statement about
   an orbit beyond the first log n digit steps, which is exactly where every method in the
   census stops.
2. **Matrix interpretations** of the digit-rewriting form (`wpotential/srs.md`): not covered
   by any wall; a z3 search at dimensions 2 to 4 oriented no rule that acts on a residue
   class (evidence only).
3. **Conjugacies with unbounded return time** to non-unit (Farkas-type) systems
   (`transport`).
4. **General additive automata**: reduced to an unproved rigidity lemma (`wpotential`).

## Reproducing

Each folder has `check_*.py` (prover) and `referee1_check.py`, `referee2_check.py`; all
exit 0. `schema/check_depth.py` takes about 11 minutes; the others a few minutes or less.
