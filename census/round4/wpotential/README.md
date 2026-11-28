# Round 4, lens "wpotential": weighted potentials against the homoclinic wall

**Outcome: no type-(c) system was settled.** What this folder contains is the second-best
outcome named in the task: a proved extension of the round-3 wall from cylinder certificates
to potentials, a second proved wall for digit-window potentials, and a precise list of what a
potential would need. The one class the walls do not reach (matrix interpretations of a
rewriting encoding) was searched with z3 for K7 and six other cores and gave nothing.

Agent-written; refereed once (REFEREE1.md) and revised (see "Revision after REFEREE1" below).
Novelty: not checked (no literature search).

## Results

| # | statement | status | where |
|---|---|---|---|
| S | A potential V ≥ 0 with V(Tn) ≤ V(n) − δ off a finite set F (or V into a well-order) proves GLOBAL, and every cycle meets F | PROVED | theory.md §1 |
| W | For any residue-class affine map (units not needed, mixed moduli allowed): a potential certificate is **not coarsely monotone** at any expanding periodic point. Coarsely monotone at x: on a small cylinder around x, n' ≥ ρn implies V(n') ≥ V(n) | PROVED | theory.md §2; data `check_wall.py [SHADOW]` |
| W1 | Type (c): the expanding periodic points are dense in the uncountable perfect set Λ_Σ, so a certificate fails coarse monotonicity on a dense subset of a Cantor set | PROVED | theory.md §2; `check_wall.py [DENSE]` |
| W2 | Classes **without counters** (residue weight × n + o(n), n^γ e^ψ with ψ locally bounded, mantissa factors with bounded ψ, c·(digit count) + bounded, and lexicographic / ordinal combinations): for unit-multiplier maps these certify exactly the CERT systems. **With counters** v_p(n − x_i) at finitely many points added: at most the systems whose expanding periodic points lie on finitely many orbits; this includes type (b) (acc_h16), never type (c). *Corrected after REFEREE1: the first version said the counter classes also certify only CERT systems, which was WRONG.* | PROVED | theory.md §2; `referee1_check.py [TYPEB]` |
| A | Sliding-window digit potentials V(n) = Σ_i f(n_i … n_{i+s−1}) + bounded boundary terms certify **no** 2-adic map that has a ×3 branch (s ≤ 10) or a ×5 branch (s ≤ 8) and an expanding periodic point. The descent condition forces f = constant + coboundary, so V = c·(digit count) + bounded | PROVED for those s (general s OPEN, EVIDENCE: rank pattern) | theory.md §3; `check_windows.py` |
| — | Type (c) of the 8 cores, K7 (z-form) and 3x+1 confirmed with round3/accel `barrier_witness`; decide.py gives OBST for the n-forms and 3x+1 | PROVED (re-check of round 3) | `check_wall.py [TYPE]` |
| — | mb_s3_27 (mixedbase blocked system): besides −5 → −7 → −10 (9/8) and the 11-cycle through −10138/139 (2187/2048), there are expanding rational periodic points that shadow the −5 cycle for 10, 20, 40 periods; Theorem W applies to all of them | PROVED for the exhibited points; infinitely many: OPEN (EVIDENCE) | `check_wall.py [MB]`, `scratch/mb_homoclinic.py` |
| — | Rewriting encodings of K7 and six cores (YAH style) are correct (they simulate the maps); natural matrix interpretations found by z3 remove only bookkeeping rules and K7's single instance `small1` (1 ↦ 0), never a rule acting on a residue class | encoding PROVED (finite parts checked); search EVIDENCE | srs.md; `check_srs.py` |
| — | Deterministic additive automata in general: pumping and a measure argument reduce the question to a rigidity lemma for ×3-invariant weightings of the automaton's bottom components | reduction sketched, not proved | theory.md §4 |

## What a potential would need (short form; details in theory.md §6)

1. It must assign smaller values to much larger integers inside arbitrarily small p-adic
   cylinders, at every expanding periodic point, hence on a dense subset of a Cantor set.
2. Its dependence on the high digits must not be additive over local windows: such sums are
   forced to be invariant under multiplication by 3 and collapse to c·(digit count).
3. It must carry itinerary information of depth about log n about the low digits, which a
   finite-state reader of the digits of n does not compute. Matrix interpretations of a
   rewriting system read intermediate mixed-radix words instead, which is why they are not
   excluded; none was found.

## Where the method stalled

* Every potential class here that reads the digits of n through local or residue information,
  without counters, is coarsely monotone everywhere once the descent condition is imposed
  (Corollary W2, Theorem A), so it is defeated by any expanding periodic point, not only by
  homoclinic ones. Counters at finitely many points escape this at finitely many orbits only
  (enough for type (b), never for type (c)). The window result even excludes
  the type-(b) systems that round 3 settles with Theorem H.
* For general deterministic automata the missing step is a rigidity lemma (theory.md §4):
  is a weighting of a strongly connected complete automaton whose cycle sums are invariant
  under ×3 necessarily a constant plus a coboundary? It is true for de Bruijn automata with
  s ≤ 10 (by computation). If it holds in general, deterministic additive automata are also
  walled off for every system whose Λ_Σ has interior (K7: Λ_Σ = Z_2).
* Matrix interpretations: search space too large for z3 at dimension ≥ 3 within the time
  limits; nothing that touches the arithmetic rules was oriented.

## Files

| file | content |
|---|---|
| theory.md | definitions, Lemma S, Theorem W, Corollaries W1, W2, Theorem A, the automaton reduction, feature list |
| srs.md | rewriting encodings and the matrix-interpretation search |
| wplib.py | system definitions (8 cores in n-form, K7 z-form, 3x+1, mb_s3_27), exact periodic-point tools |
| check_wall.py | [TYPE], [SHADOW], [DENSE], [MB] (about 45 s) |
| check_windows.py | [BIJ], [RANK], [ZERO] for Theorem A (about 5 s; needs numpy) |
| check_srs.py | [SEM], [SIM], [NF], [SIM-cores], [CHAIN] (about 1 s) |
| REFEREE1.md, referee1_check.py | referee report and the referee's independent check (about 1.5 min; includes [TYPEB], the acc_h16 counter certificate) |
| srs_lib.py, srs_cores.py | encodings and exact interpretation checker |
| mi_z3.py, mi_record.py, mi_chains.json | z3 search engine, the recorded cheap search and its chains |
| scratch/ | exploratory runs (z3 logs, homoclinic count for mb_s3_27); EVIDENCE only |

## Reproducing

The local virtual environment `.venv` has numpy, scipy and z3-solver (z3 is needed only for
`mi_record.py`). Run, from this folder:

    .venv/bin/python check_wall.py
    .venv/bin/python check_windows.py
    .venv/bin/python check_srs.py
    .venv/bin/python -I referee1_check.py

Each exits 0 when every claim passes.

## Revision after REFEREE1

The referee confirmed Lemma S, Theorem W, Corollary W1, Theorem A (for the stated (u, s)),
the type-(c) checks and the mb_s3_27 data. Every item flagged was handled as follows.

| item | referee verdict | what changed |
|---|---|---|
| W2b: "the W2 classes, counters included, exist only for CERT systems; they do not even reach type (b)" (theory.md §0, §2 "iff", README row W2) | WRONG | **Withdrawn.** The "iff CERT" now covers only the classes without counters. With finitely many counters the reach is at most the systems whose expanding periodic points lie on finitely many orbits: this includes type (b), never type (c). The referee's counter certificate for acc_h16 is written out as a Remark in theory.md §2 (PROVED, `referee1_check.py [TYPEB]`; the written potential was corrected after REFEREE2 to put φ = c(r)·n on the self-loop SCC {0} as well). The type-(c) conclusion (W2c) was CONFIRMED and is unchanged. |
| W2 item 2 | fix | ψ is now required to be *bounded* (also for mantissa factors). |
| W2 item 3 | fix | The unnecessary ratio hypothesis on g is dropped (ρ = 1 works). |
| W2 "only if" | fix | The division-free expanding cycle case is now handled: a whole residue class then diverges, so no certificate exists. |
| W2 item 5, "accelerated certificates along finitely many orbits are of this kind" | GAP (minor) | Relabelled as a heuristic remark, with no proof claimed. |
| theory.md §6.3, "the 2-adic conjugacy of 3x+1 is not computed by any finite automaton" | GAP | Relabelled as a heuristic (not proved, literature not checked). Nothing depends on it. |
| srs.md / README, "never a map rule" | fix | Qualified: K7's `small1` (LtR → LR, the instance 1 ↦ 0) is removed. No rule acting on a residue class was oriented. `check_srs.py` docstring and messages say "class map rules". |
| `check_wall.py [MB]` asserted only that −10 was found | fix | Now asserts exactly 16274 orbits and the exact expanding list {−10 (9/8), −10138/139 (period 11, 2187/2048)}. |
| docstrings: "Corollaries W1-W3", runtimes | fix | Now "W1, W2"; runtimes corrected (check_wall about 45 s, check_windows about 5 s, check_srs about 1 s). |

After the revision, `check_wall.py`, `check_windows.py`, `check_srs.py` and
`referee1_check.py` all exit 0. The headline is unchanged. No type-(c) system is settled. The
negative results (Theorems W, A; W1; W2 for the counter-free classes and for type (c)) stand.
One negative claim was too strong and is withdrawn (W2b).

## Revision after REFEREE2

REFEREE2 (`REFEREE2.md`) confirmed every claim and listed two text repairs. Neither changes a
headline. Both are made:

1. **Remark on acc_h16 (theory.md §2, labelled PROVED).** The written potential put φ = c(r)·n
   only on the 10-node SCC and φ = 0 on "transient nodes". But node 0 is a 1-node SCC with a
   self-loop (n ≡ 0 mod 16 ↦ n/2 can again be ≡ 0 mod 16), so with φ = 0 there V did not
   descend on n ≡ 0 (mod 32). The text now puts φ = c(r)·n on every contracting SCC with an
   internal edge (the 10-node SCC and the self-loop SCC {0}), and φ = 0 on the nodes 7, 8, 12,
   which have no internal edge. This is what `referee1_check.py [TYPEB]` already implements, so
   the check and the PROVED label stand. The README revision row above that cites the Remark
   now notes the correction.
2. **W2 "only if", division-free case (theory.md §2).** The text said the multiplier of a
   division-free cycle is > 1; it can be exactly 1 (e.g. n ≡ 1 (4) ↦ n + 4). The sentence now
   says the multiplier is ≥ 1: if it is > 1, or 1 with total shift > 0, every orbit of the class
   tends to ∞; if it is 1 with shift 0, every integer of the class is periodic; either way no
   certificate exists (Lemma S). The hypothesis now reads "a cycle with multiplier ≥ 1" in place
   of "an expanding cycle", and the division case notes that such a cycle is then expanding.

REFEREE2's optional README nit (labelling the §4 automaton consequence as resting on an
unproved sketch) is not applied here.
