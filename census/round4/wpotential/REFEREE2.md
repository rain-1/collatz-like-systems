# Referee 2 report: round 4, lens "wpotential" (second pass, after the REFEREE1 repair)

Referee: independent agent. I did not edit any of the prover's files or REFEREE1's files, and I
committed nothing.

**What I read:** README.md, theory.md, srs.md, wplib.py, srs_lib.py, srs_cores.py,
mi_chains.json, the three check scripts, REFEREE1.md and referee1_check.py (the [TYPEB]
part), plus round3/README.md and round3/accel/trichotomy.md for context.

**My own check:** `referee2_check.py`, written from scratch.

* It imports nothing from the prover or from round 3. The only thing it reads is
  `mi_chains.json`, as data.
* All arithmetic is exact int or Fraction. The one exception is a rank computation modulo
  998244353, a different prime from the prover's 2^31 − 1 and REFEREE1's 10^9 + 7.
* It contains negative controls that must be rejected:
  * acc_h16 and a CERT system must not come out as type (c);
  * a contracting closed walk must be rejected;
  * u = 3 with k = 4 must break the bijection;
  * u = 1 must give rank 0;
  * a deliberately wrong rewriting rule must be rejected;
  * the acc_h16 potential as theory.md writes it must fail.
* Its first version did fail, on exactly that acc_h16 point (see Remark below).
* It now exits 0 in about 26 s:

      .venv/bin/python -I referee2_check.py        # ALL PASS, exit 0

**The prover's checks:** I ran all four, and each printed ALL PASS and exited 0.

| script | result |
|---|---|
| `check_wall.py` | ALL PASS, 42 s |
| `check_windows.py` | ALL PASS |
| `check_srs.py` | ALL PASS |
| `referee1_check.py` | ALL PASS |

## Headline

**No type-(c) system is claimed settled, and none is.** The README's first line says so. So
the round's main aim was not met, and the folder is honest about it. There is no positive
claim that could also prove 3x+1, so the "would it prove something false" test only applies
to the negative theorems.

I tested the negative theorems for over-reach:

* **Theorem W.** A settled type-(b) system (acc_h16) has a potential certificate, and that
  certificate is non-CM exactly at −1, as Theorem W requires.
* **Theorem A.** It needs an expanding periodic point. I built a CERT system with a ×3 branch:
  even n ↦ n/2, n ≡ 1 (4) ↦ (3n+1)/4, n ≡ 3 (4) ↦ (3n+3)/4. A width-1 window potential with a
  top-digit term, V = len − 1 + log₂(top8/128), certifies it. This is verified exactly for
  128 ≤ n < 4·10^5 ([CTRL-A]). So Theorem A does not over-reach, and its collapse
  "V = c₀·len + bounded" is consistent with this example.

Two statements still need a (small) repair, so needs_repair = true:

1. The acc_h16 counter certificate is labelled PROVED, but the potential written in
   theory.md does not descend.
2. One sentence in the division-free case of W2 is false.

Neither fix changes a headline.

## Verdicts

| # | claim | verdict |
|---|---|---|
| S | Lemma S (soundness; every cycle meets F; well-order variant) | CONFIRMED |
| W | Theorem W (any residue-class affine map: a certificate is not CM at any expanding periodic point) | CONFIRMED |
| W1 | Corollary W1 (type (c): Λ_Σ closed, perfect, uncountable; expanding periodic points dense) | CONFIRMED |
| W2a | Counter-free classes (items 1–4, 6) are CM everywhere, hence certify exactly the CERT systems | CONFIRMED_WITH_FIX (division-free sentence, see below) |
| W2b | With finitely many counters: reach ⊆ systems whose expanding periodic points lie on finitely many orbits; includes type (b), never type (c) | CONFIRMED (the REFEREE1 WRONG item is honestly withdrawn) |
| Rem | acc_h16 counter certificate (type (b) reached by item 5), labelled PROVED | CONFIRMED_WITH_FIX (φ must also be c(r)·n on the self-loop SCC {0}) |
| A | Theorem A (u = 3, s ≤ 10; u = 5, s ≤ 8) | CONFIRMED |
| A-open | general s OPEN, rank pattern EVIDENCE | CONFIRMED (label correct) |
| TYPE | type (c) of the 8 cores, K7 z-form, 3x+1 (and 5x+1) | CONFIRMED |
| BRUTE | stopping values / cycle lists used in srs.md | CONFIRMED to 10^6 |
| MB | mb_s3_27: −5 → −7 → −10 (9/8); 16274 orbits of period ≤ 12; exactly two expanding; homoclinic points d = 10, 20, 40; "infinitely many" OPEN | CONFIRMED |
| SRS | encodings simulate the maps; chains verified; no class map rule oriented (qualifier for `small1`) | CONFIRMED |
| §4 | automaton reduction, "sketch, not proved" | CONFIRMED as labelled (README nit below) |
| §6.3 | conjugacy not finite-state: now a heuristic | CONFIRMED (honestly relabelled) |
| Labels | "refereed once and revised", "Novelty: not checked", PROVED / EVIDENCE / OPEN usage | CONFIRMED, except the two fixes above |

## REFEREE1 items: were they honestly resolved?

| REFEREE1 item | status now |
|---|---|
| W2b WRONG (counters "do not reach type (b)") | Resolved. §0, §2 and README row W2 are corrected, the error is marked as withdrawn, and the counterexample is written out. |
| W2 item 2: ψ must be bounded | Resolved. |
| W2 item 3: the ratio hypothesis is unnecessary | Resolved (ρ = 1). |
| W2 "only if": division-free case | **Partly resolved.** The case was added, but its text says "Its multiplier is the product of the u's, which is > 1". REFEREE1 had written "u > 1, or u = 1 and v ≠ 0", and the u = 1 part was dropped. When every u is 1 the multiplier is exactly 1. See the fix below. |
| W2 item 5: "accelerated certificates are of this kind" | Resolved. It is now a heuristic remark. |
| §6.3 GAP | Resolved. It is now a heuristic, and nothing else depends on it. |
| srs "never a map rule" | Resolved. The qualifier for `small1` is in srs.md and the README, and check_srs now says "class map rules". |
| check_wall [MB] asserted too little | Resolved. Lines 167–169 now assert `len(rows) == 16274` and the exact expanding list. |
| Docstrings and runtimes | Resolved: W1, W2; about 45 s, 5 s and 1 s, which match my runs. |

## Line-by-line notes

### Lemma S, Theorem W, Corollary W1

I re-derived all three.

**Theorem W.** The shadowing step works as follows.

* On y + Q^M, every n follows y's branches for kL steps, provided M exceeds N plus the
  divisions plus m.
* T^i(n) = T̂^i(y) + λ_i(n − y) with λ_i > 0.
* n' = y + λ^k(n − y) ≥ ρn once λ^k > 2ρ and n is large.
* CM gives V(n') ≥ V(n), and kL descent steps give V(n') < V(n). This is a contradiction.

[SHADOW] checks this exactly for x* in sf3_7, sf3_13, sf3_137, K7z, 3x+1 and 5x+1, at
p-adic depth 20, with growth ≥ 2 and every iterate ≥ n/8.

**Corollary W1.**

* (1) The perfectness step is sound: a strongly connected SCC that is not a simple cycle has a
  node with two internal out-edges, and distinct edges have distinct targets mod p^K.
* (2) (M) of trichotomy.md gives a unique fixed point y = B/(1 − A) for every closed walk with
  a division, and its denominator is prime to p. With d copies of an expanding cycle the
  multiplier is > 1.
* [DENSE] builds 12 random walks of length 10, 20 and 40 in each of K7z, sf3_13 and 3x+1, at
  K = m + 1. My own G_K, closing paths and composition are used. Each walk is verified by
  iterating T̂ residue by residue: the point returns to itself and its multiplier is > 1.
* A contracting walk is correctly rejected.

### Corollary W2

**Items 1–4 and 6.** I re-checked each inequality.

* Item 1: c(7n'/8 − 9n/8) > 0.
* Item 2: n'^γ e^{−B} ≥ n^γ e^{B} for ρ = e^{2B/γ}.
* Item 3: ρ = 1.
* Item 4: ⌊2B/c + 1⌋ > 2B/c.
* Item 6: componentwise ≥ implies ≥ for lexicographic tuples.

All of these are correct.

**Item 5 off E.** This is correct, because v_p(n − x_i) is locally constant away from x_i.

**"Only if", the division-free case.** This case occurs only without the standing hypothesis.
The sentence "Its multiplier is the product of the u's, which is > 1" is false when every u on
the cycle is 1. [NEUTRAL] gives an example: n ≡ 1 (4) ↦ n + 4 is a division-free G_2
self-loop with multiplier exactly 1.

The conclusion still holds. On the class, T^ℓ(n) = n + V with p^K | V.

* If V > 0, every orbit diverges.
* If V = 0, every integer of the class is periodic, giving infinitely many cycles, which
  contradicts Lemma S.
* V < 0 is impossible for a map of Z_{>0} to itself.

**Fix:** replace "Its multiplier is the product of the u's, which is > 1, so all large integers
of that class have orbits tending to infinity" with:

> its multiplier is the product of the u's, which is ≥ 1. If it is > 1, or it is 1 and the
> total shift is > 0, every orbit of the class tends to ∞. If it is 1 with shift 0, every
> integer of the class is periodic. Either way no certificate exists (Lemma S).

Also note that a G_K cycle with multiplier exactly 1 is the only non-CERT case that is not
"expanding", so "suppose G_K has an expanding cycle" should read "a cycle with multiplier ≥ 1".

### Remark: the acc_h16 counter certificate (labelled PROVED)

theory.md defines φ = c(r)·n "on the contracting 10-node SCC" and φ = 0 "on transient
nodes". REFEREE1's prose said the same.

The trouble is node 0. My own G_4 has SCCs of sizes 1, 1, 1, 1, 2 and 10, as stated, but
**{0} is a 1-node SCC with a self-loop**: n ≡ 0 (16) ↦ n/2 can again be ≡ 0 (16). So node 0 is
a contracting SCC, not a transient node. With φ = 0 there, n ≡ 0 (32) keeps the same level
and the same φ (0 → 0), so V does not descend. This fails at infinitely many n. [TYPEB]
confirms it: the potential as written has 681 failures below 2·10^4, and every failure above
2400 is ≡ 0 (32).

REFEREE1's code (`referee1_check.py`, `contr = [i ... if internal[i] and i != shadow_c]`)
already puts c(r)·n on every contracting SCC with an internal edge. So the check is right and
only the prose is wrong.

With that repair, my independent reconstruction descends for all n < 3·10^5 except 57 values,
all below 510. That is under the proved threshold of 2369 (θ = 99/100, my own exact c(r)). The
counter identity 15 → 14 (φ: 2j → 2j − 1) is checked exactly.

**Fix:** in theory.md, replace "φ = c(r)·n on the contracting 10-node SCC" with:

> φ = c(r)·n on every contracting SCC with an internal edge (the 10-node SCC and the
> self-loop SCC {0})

and replace "φ = 0 on transient nodes" with:

> φ = 0 on the nodes 7, 8, 12, which have no internal edge

### Theorem A

I re-derived each step.

* **Step 1 (pumping).** The buffer reaches every carry when 2^b > u, and the boundary terms
  are independent of M. [PUMP] checks this on the 3x+1 branch with random f, s = 3 and every
  closed walk with k ≤ 5: the difference V(T n_M) − V(n_M) − MΦ is the same for M = 4..9.
* **Step 2 (bijection).** For x = 0 and x = 2^k − 1 only one carry works. For every other x,
  ux mod (2^k − 1) is nonzero, which forces y and c ∈ [0, u−1]. [BIJ] checks odd k ≤ 13, with
  the k = 4 control.
* **Step 3.** No window wraps twice because k ≥ len(uh) + s. [STEP3] checks both identities
  exactly.
* **Step 4.** My own matrix gives ranks 1, 2, 4, …, 512 for u = 3, s ≤ 10, and up to 128 for
  u = 5, s ≤ 8, modulo 998244353. The control u = 1 gives rank 0. I checked exactly, with
  integers, that the constants and the 2^{s−1} − 1 coboundary generators lie in the kernel,
  and that they span dimension 2^{s−1}. So the kernel over Q is exactly constants plus
  coboundaries.
* **Conclusion.** The identity V_f = E_f + c₀(len + s − 1) − Σ_{i<0} f(window_i) is correct.
  Both the c₀ > 0 case and the c₀ = 0 case are handled.

### Type (c), and the brute force

I built my own G_K, my own Tarjan SCCs and an exact potential test at K = m and K = m + 2 for
the 8 cores (n-form), K7z, 3x+1 and 5x+1. In each case:

* the standing hypothesis holds (the division-free subgraph is acyclic);
* the residue walk of x* is closed with an exact multiplier > 1 (3/2, 9/8 or 5/2);
* that walk lies in an SCC with more internal edges than nodes, so the SCC is type (c).

K7z's G_2 is one SCC. The controls also come out right: acc_h16 gives types {a, a, b} and no
type (c), and cert_ctrl comes out all-contracting. None of the cores is a disguised easy case.

Brute force over all starts:

* to 10^6, sf3_7, sf3_17, sf3_57, sf3_157, sf3_357 and sf3_135 reach only the cycle through 1;
* sf3_13 reaches only the cycles with minima 1 and 3;
* K7z reaches 0 from every z < 10^6;
* sf3_137 has 1408 starts below 2·10^4 that pass 10^30, and its cycle minima are 1, 3, 7 and
  39. This is consistent with it being left out of srs.md.

### mb_s3_27

My own Lyndon-word enumeration over the alphabet {E, O, Z} reproduces the prover's figures
exactly:

* exactly **16274** rational periodic orbits of period ≤ 12 with denominator prime to 6;
* exactly two of them expanding: the 3-cycle −5 → −7 → −10 (9/8), and an 11-cycle (2187/2048)
  that passes through −10138/139;
* expanding homoclinic points (OOE)^d·w for d = 10, 20 and 40, verified exactly.

"Infinitely many" is correctly labelled OPEN.

### srs.md

I wrote the K7 rules (13) and the core rules (21 or 22) myself and checked their semantics
with my own mixed-radix affine evaluator. Every rule either preserves the value in context or
applies T to the whole number, and the wrong control rule is rejected.

Every chain in mi_chains.json re-verifies with my own interpretation algebra. Each chain
removes exactly the rules the README lists:

* K7: `small1` and `left_a`;
* sf3_17, sf3_57, sf3_157 and sf3_357: `lead0`, `left_a` and the six p-increment rules;
* sf3_13 and sf3_135: `lead0` and `left_a`.

In every chain, all class map rules remain. The z3 "unsat" and "unknown" results are correctly
not claimed.

### Labels and novelty

* "Novelty: not checked (no literature search)" is honest.
* Theorem W is correctly presented as an extension of the round-3 shadowing wall (Theorem N /
  Lemma B).
* README nit (non-blocking): "Where the method stalled" says "If it holds in general,
  deterministic additive automata are also walled off …". That consequence rests on the §4
  sketch, which is not proved. Add "(by the sketch in theory.md §4, not proved)".

## Required repairs (all textual)

1. theory.md, Remark after W2 (and the README revision row that cites it): put φ = c(r)·n on
   the self-loop SCC {0} as well. The proof label PROVED is fine after this fix. The exact
   check, `referee1_check.py [TYPEB]`, already does this.
2. theory.md, the W2 "only if" division-free case: the multiplier is ≥ 1, not > 1. Handle
   multiplier 1 (shift > 0 diverges, shift 0 gives infinitely many cycles), and say "cycle with
   multiplier ≥ 1" in place of "expanding cycle".
3. Optional: the README §4 consequence label above.
