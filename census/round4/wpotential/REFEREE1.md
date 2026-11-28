# Referee 1 report: round 4, lens "wpotential"

Referee: independent (agent). Scope: everything in this folder: README.md, theory.md, srs.md,
the three check scripts, mi_chains.json and scratch/mb_homoclinic.py. Context read:
round3/README.md and round3/accel/trichotomy.md. I did not edit the prover's files and did not
commit anything.

My own check is `referee1_check.py`. I wrote it from scratch: it imports no prover or round-3
module, and it uses exact int and Fraction arithmetic everywhere except the rank computation,
which works modulo the prime 10^9+7. It exits 0, and its last run passed every check (about
1.5 min). Several checks are negative controls that would fail if the claim were false: a test
that must reject u = 3 at an even k, a rank that must come out 0 for u = 1, acc_h16 must come
out NOT type (c), and sf3_137 must show escaping orbits. I also ran the prover's scripts:
`check_wall.py`, `check_windows.py` and `check_srs.py` all exit 0 (ALL PASS).
`scratch/mb_homoclinic.py` reproduces the stated counts: 7 at d = 5, rising to 64 at d = 40.

## Headline

**No type-(c) system is claimed to be settled, and none is.** The README says this plainly in
its first line. So the round's main target, a new method that settles a type-(c) system, was
not met, and the folder does not pretend otherwise. What the folder does contain are negative
"wall" theorems, plus EVIDENCE from a matrix-interpretation search.

I re-derived the walls line by line, and they are sound:

* Lemma S;
* Theorem W;
* Corollary W1;
* Corollary W2, once it is restricted to the classes with E = ∅;
* Theorem A for the stated (u, s).

One sentence in the summary is false. theory.md §0 says that the W2 classes, *counters
included*, "exist only for CERT systems. They do not even reach type (b)." I constructed a
certificate in exactly that class (residue data, the counter v_2(n+1) at the single orbit
{−1, −2}, and a lexicographic tuple) for the type-(b) system acc_h16. Section [TYPEB] below
gives the proof, and `referee1_check.py [TYPEB]` checks it. The paper's own §2 states the
correct bound, so this is a repair to the summary, README row W2 and the §2 "iff" sentence, not
to a proof. Because it is a false statement, needs_repair = true.

## Verdicts

| # | claim | verdict |
|---|---|---|
| S | Lemma S (soundness of potential certificates; every cycle meets F) | CONFIRMED |
| W | Theorem W (a certificate is not CM at any expanding periodic point; any residue-class affine map) | CONFIRMED |
| W1 | Corollary W1 (type (c): Λ_Σ closed, perfect, uncountable; expanding periodic points dense; so B(V) is dense in Λ_Σ) | CONFIRMED |
| W2a | W2 items 1–4, 6 (E = ∅) are CM everywhere, so they certify exactly the CERT unit-multiplier systems | CONFIRMED_WITH_FIX (minor: item 2's ψ must be bounded; item 3's ratio hypothesis is unnecessary; "only if" also needs the division-free case, which is trivial) |
| W2b | §0 / README / §2: the classes *including counters* "only for CERT", "do not even reach type (b)", "certify exactly the CERT systems" | **WRONG** (counterexample acc_h16; fix below) |
| W2c | With finitely many counters, never a type-(c) system | CONFIRMED |
| A | Theorem A (window potentials collapse to c·len + bounded; u = 3, s ≤ 10; u = 5, s ≤ 8) | CONFIRMED |
| A-open | general s OPEN, rank pattern EVIDENCE | CONFIRMED (label correct) |
| TYPE | type (c) of the 8 cores, K7 z-form and 3x+1; OBST from decide.py | CONFIRMED (my own G_K and SCCs at K = m and m+2; 5x+1 also type (c); acc_h16 correctly not type (c)) |
| MB | mb_s3_27: cycle −5 → −7 → −10 (9/8); 16274 orbits of period ≤ 12, of which exactly two are expanding (−10 and −10138/139, 2187/2048); homoclinic points for d = 10, 20, 40; "infinitely many" OPEN | CONFIRMED (fix: check_wall.py does not assert the count or the expanding list) |
| SRS | encodings simulate the maps; chains verified; nothing arithmetic oriented | CONFIRMED_WITH_FIX ("never a map rule" needs a qualifier: K7's removed `small1`, LtR → LR, is the map step T(1) = 0) |
| §4 | automaton reduction | CONFIRMED as labelled ("sketch, not proved") |
| §6.3 | "the 2-adic conjugacy of 3x+1 is not computed by any finite automaton" | GAP (unlabelled and unproved; label it as a heuristic or conjecture, or cite a source) |
| N2 | "Accelerated certificates along finitely many orbits are of this kind" (W2 item 5) | GAP, minor (unproved identification; label it as a remark) |
| Novelty / labels | "Agent-written; not refereed. Novelty: not checked" | CONFIRMED (honest). Theorem W uses the same shadowing mechanism as round-2 Lemma B and round-3 Theorem N, and the README correctly calls it an extension of that wall |

## Line-by-line notes

### Lemma S
The proof is correct. The orbit meets the finite set F infinitely often, so some element of F
repeats. A cycle that missed F would be an orbit that avoids F forever. The well-order variant
is also correct. The remark that "steps to the cycle" is a tautological certificate is right
too: it needs only that F, the union of the cycles, is finite.

### Theorem W
I checked each step.

1. Shadowing. On the cylinder, T^i(n) − T̂^i(y) = λ_i (n − y) with λ_i > 0. The denominators of
   the reduced factors u_r/w_r divide Q. This follows from integrality on the whole class:
   w | uQ, so w/gcd(u, w) divides Q. So choosing M large enough keeps the branches for kL steps
   and gives n' ≡ y mod Q^N. For Q = 54 (mb_s3_27) the bookkeeping is done at each prime
   separately, and it works.
2. Growth. n' = λ^k n − (λ^k − 1)y ≥ 2ρn − O(1) ≥ ρn.
3. The orbit avoids F. The intermediate iterates tend to ∞ as n → ∞.
4. Contradiction. CM gives V(n') ≥ V(n), and descent gives V(n') ≤ V(n) − kLδ.

The proof is valid for any totally ordered strict order. `[SHADOW]` in my check rebuilds the
shadowing configuration independently: for x* and four points of C^d W in each of sf3_7,
sf3_137, sf3_13, K7z and 3x+1, it verifies the exact identity, growth ≥ 2, and that every
iterate stays above n/8. It also confirms that random c(r)·n potentials and bit length fail to
descend on every such segment.

### Corollary W1
* **(1) Closed, perfect, uncountable.** Points correspond injectively to infinite walks, and
  infinitely many divisions follow from the standing hypothesis. Perfectness holds because a
  type-(c) SCC is not a simple cycle, so some node has two internal out-edges.
* **(2) Density.** The closed walk π · path · C^d · path has multiplier > 1 for large d. By (M)
  it has a unique rational periodic point that agrees with x along π.
* **Checks.** `[DENSE]` (my own) builds these points for random walks of length 10, 20 and 40
  in K7z, sf3_13 and 3x+1. It verifies by direct iteration of T̂ that the point realises the
  walk residue by residue, returns to itself, and expands. `[TYPE]` confirms that G_2 of K7z is
  a single SCC, so Λ_Σ = Z_2.

### Corollary W2
* **Item 1.** The inequality c(7n'/8 − 9n/8) > 0 for n' ≥ 2n is correct.
* **Item 2.** It is correct when |ψ| ≤ B near x. The parenthetical "ψ a function of the real
  mantissa" must say *bounded* function. *Fix:* insert "bounded".
* **Item 3.** It is correct, but the ratio hypothesis is not needed: on a cylinder of depth ≥ K
  the residue factor is constant, so ρ = 1 already works.
* **Item 4.** It is correct. A ratio n'/n ≥ 2^{2B/c+1} gives a length difference of at least
  ⌊2B/c + 1⌋ > 2B/c.
* **Item 6.** It is correct.
* **"iff CERT".** The "only if" direction cites (M), which needs a division on the expanding
  cycle. A division-free cycle with u > 1, or with u = 1 and v ≠ 0, makes every integer of the
  class follow it forever. That gives a divergent progression or infinitely many cycles, so no
  certificate of any kind exists. Add that sentence.

**[TYPEB] counterexample to W2b.** Take acc_h16 (round 3, type (b), settled by Theorem H). Its
graph G_4 has SCCs of sizes 1, 1, 1, 1, 2 and 10. The 2-node SCC is the shadow {15, 14} of
x* = −1. Define a lexicographic pair V(n) = (lev, φ):

* lev is the DAG height of the SCC of n mod 16;
* φ = c(r)·n on the contracting SCC, with c from max-mean potentials and θ = 99/100, verified
  exactly;
* φ = 2·v_2(n+1) on node 15;
* φ = 2·v_2(n/2+1) + 1 on node 14;
* φ = 0 on transient nodes.

The descent argument:

* Node 15 → 14 sends n ↦ 3n + 1, and (3n+1)/2 + 1 = 3(n+1)/2, so φ drops from 2j to 2j − 1.
* Node 14 → 15 halves n, so φ drops from 2j − 1 to 2(j − 1).
* Leaving an SCC lowers lev.
* Inside the contracting SCC, V(Tn) ≤ θV(n) + β ≤ V(n) − 1/2 once V(n) is large.

So floor(2V), taken in N×N lexicographically, descends off a finite set. Every component is CM
off the orbit {−1, −2}: lev is locally constant, c(r)n is item 1, and the counter is item 5. So
this V lies in the class "counters at finitely many points + lexicographic combinations" of W2
and certifies a type-(b) system. The check confirms strict descent for all n < 3·10^5, except
for n < 165, which is below the proved bound of 2783. This is consistent with Theorem W, since
−1 ∈ B(V).

**Fix for W2b:**
* In theory.md §0, replace "exists only for CERT systems. They do not even reach type (b)." with
  "for the classes without counters (items 1–4, 6) exists only for CERT systems; with counters
  at finitely many points the reach is at most the systems whose expanding periodic points lie
  on finitely many orbits (this includes type (b), e.g. acc_h16), never type (c)".
* Restrict the "iff CERT" sentence in §2 in the same way.
* Change README row W2 to match.

### Theorem A
I checked all four steps.

* **Step 1 (pumping).** The carry c ∈ [0, u−1] can be reached by choosing β, because
  consecutive β change the low part by u·2^m < 2^{m+b}. Boundary terms, g, h (top digits are
  fixed for large M) and the shift by e all give an M-independent constant. `[PUMP]` (my own)
  verifies V(T n_M) − V(n_M) − MΦ(x) = const exactly for M = 4..9, for every closed walk with
  k ≤ 5, for the ×3 and ×5 branches with random f.
* **Step 2 (bijection).** For odd k, gcd(u, 2^k − 1) = 1 for u = 3 and 5. The words x = 0 and
  x = 2^k − 1 are fixed, and for every other x the carry is forced and lies in [0, u−1].
  `[BIJ]` re-verifies this for odd k ≤ 13, with a negative control at u = 3, k = 4.
* **Step 3.** The cyclic window count is right because k ≥ len(uh) + s, so no window wraps
  twice. `[STEP3]` verifies F(y) − F(x) = E_f(uh) − E_f(h) exactly.
* **Step 4 (rank).** The kernel contains the constants and coboundaries, which have dimension
  2^{s−1}. I verified exactly that these vectors lie in the kernel, and computed their rank. I
  recomputed the matrix rank modulo a different prime (10^9+7) and got 2^{s−1} for u = 3,
  s ≤ 10 and u = 5, s ≤ 8, with control rank 0 for u = 1. Rank mod p ≤ rank over Q, so the
  kernel is exactly constants plus coboundaries.
* **Conclusion.** The identity V_f = E_f + c₀(len + s − 1) − Σ_{i<0} f(window_i) is correct.
  Both cases c₀ > 0 (CM, then Theorem W) and c₀ = 0 (bounded V, long shadow segments) are
  handled.
* **Scope.** 5x+1 has the expanding point −1/3 with multiplier 5/2, which I checked. acc_h16
  and acc_h32 have the expanding point −1 under a ×3 branch. The S-family branch 3n+1 has
  e = 0, which the proof allows.

### Type (c) of the systems, and brute force
My own G_K, with K = m and K = m + 2, checks the following for all 8 cores (n-form), K7z, 3x+1
and 5x+1:

* the standing hypothesis holds, i.e. the division-free subgraph is acyclic;
* the residue cycle of x* is expanding;
* its SCC has more internal edges than nodes, so it is not a simple cycle.

None of these systems is a disguised type (a) or (b) case. Brute force to 2·10^5:

* sf3_7, sf3_17, sf3_57, sf3_157, sf3_357 and sf3_135 reach only the cycle through 1;
* sf3_13 reaches only the cycles through 1 and 3, which matches srs.md's stopping values;
* sf3_137 has orbits that escape 10^30. This matches round 3's "divergence expected", and it is
  why srs.md leaves sf3_137 out. Its seen cycles have minima 1, 3, 7 and 39.

### Test against false or famous statements
Every theorem here is negative: it says no certificate of the class exists. Each one applies to
3x+1 and to sf3_137 (expected divergent) just as it applies to the cores, which is the expected
behaviour. None of them can "prove" 3x+1. A positive claim would only come from a matrix
interpretation chain that removed every rule, and none was found. My one overreach finding is
W2b above, where a negative claim was too strong.

### srs.md
The swap, left-end and K7 rules are semantically correct; I re-derived each affine identity by
hand. I re-verified the K7 chain in mi_chains.json with my own composition code. The two strict
rules are `small1` (LtR → LR) and then `left_a`, and the remaining 11 rules match the table.
`small1` is the single map instance T(1) = 0, so "never a map rule" should say "never a map
rule except the single instance 1 ↦ 0". The z3 "unsat" and "unknown" results are correctly not
claimed.

## Minor fixes (non-blocking)
* `check_wall.py [MB]` prints the orbit count and the expanding list but only asserts that −10
  was found. Assert `len(rows) == 16274` and the exact expanding list, which my check confirms.
* The `check_wall.py` docstring says "Corollaries W1-W3", but there is no W3. The runtimes
  stated in the docstrings do not match the actual ones: check_windows takes about 5 s (the
  docstring says about 1 min) and check_srs takes about 1 s (the README and docstring say about
  1 min).
* theory.md §6.3: label as heuristic, or give a reference. (The parenthetical "for 3x+1 is not
  computed by any finite automaton" is not proved here.)
* W2 item 5: label "Accelerated certificates along finitely many orbits are of this kind" as a
  remark. Theorem N's certificates are covers with stopping times, not potentials.

## Reproduce
    .venv/bin/python -I referee1_check.py   # exits 0, ~1.5 min
    .venv/bin/python check_wall.py && .venv/bin/python check_windows.py && .venv/bin/python check_srs.py
