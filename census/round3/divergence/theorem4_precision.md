# Theorem 4: the precision lemma, and the finest modification of 5x+1 that this method settles

**Status.** The lemma is PROVED. The classification tables built on it are
exact computations, so each "obstructed" entry is a proof at every modulus. The
"open" entries are undecided, and the G1-cycle entries are covered only by a
bounded search (EVIDENCE).
Check: `check_theorem4_precision.py`. The default run (m ≤ 5) takes about 1
minute. `--m 6`, `--m 7` and `--m 8` reproduce the larger tables in about 4, 12 and
40 minutes; all three have been run and pass.
**Novelty:** not in the repo. The 2-adic precision bookkeeping is elementary;
literature novelty: not checked.

## Setting

T has modulus 2^m. On the class r it is T(n) = (a_r n + b_r)/d_r, where a_r is
**odd** and d_r is a power of 2. Every branch is then a 2-adic similarity: a
progression y + 2^p·(odd)·t is mapped to a progression y' + 2^{p − v₂(d)}·(odd)·t.
The 5x+1 map B(n) = n/2 | 5n+1, modified on any classes by rules with odd
numerators, is of this form. Let G1 be the subgraph of the residue graph mod 2^m
on the classes with d = 1 (no halving).

## Lemma P (precision)

Assume G1 is acyclic. Let U be a nonempty union of residue classes mod 2^K,
K ≥ m, with T(U) ⊆ U. Then U contains a full residue class Y mod 2^m.
Consequently U contains the forward closure of Y in the residue graph mod 2^m,
which is a nonempty forward-closed union of classes mod 2^m.

*Proof.*
1. Take a class Z₀ = {r + 2^K t : t ≥ t₀} ⊆ U.
2. Inductively, Z_j = T^j(Z₀) = {y_j + 2^{p_j} o_j t : t ≥ t₀}, with o_j odd and
   p₀ = K. While p_j ≥ m, all of Z_j lies in one class mod 2^m. So one branch
   applies to all of it, and Z_{j+1} = T(Z_j) has the same form with
   p_{j+1} = p_j − v₂(d).
3. A run of consecutive steps with d = 1 is a walk in G1. Since G1 is acyclic,
   such a run has fewer than 2^m steps, so p_j strictly decreases at least once
   every 2^m steps.
4. Hence there is a first j with p_j < m. Consider Z_j itself at this
   first j. It is a progression {y_j + 2^{p_j} o_j t : t ≥ t₀}, and this
   formula is valid because Z_{j−1} lay in one class mod 2^m (p_{j−1} ≥ m), so
   a single branch produced Z_j. Moreover p_j ≥ 0, because d divides a·2^m.
   Since Z_j ⊆ U and o_j is invertible mod 2^K, the residues of Z_j mod 2^K
   are all the classes ≡ y_j (mod 2^{p_j}).
5. U is a union of classes mod 2^K that contains Z_j, so U contains every
   positive integer ≡ y_j (mod 2^{p_j}). In particular U contains the full class
   Y = y_j mod 2^m.
6. For any edge Y → Y' of the residue graph mod 2^m, T(Y) is a progression with
   difference a·2^m/d. Its residues mod 2^K are all the classes
   ≡ T(y) (mod 2^{m − v₂(d)}). So U contains the full class Y'. Induct. ∎

## Corollary P (finite obstruction test)

Under the hypotheses of Lemma P, suppose every sink strongly connected
component of the residue graph mod 2^m contains the class of a periodic point
of T. Then **no forward-closed union of residue classes at any modulus 2^K is
cycle-free**. So no forward-closed union of residue classes (at any modulus
2^K) is a certificate of divergence, for any seed.

*Proof.* The closed set from Lemma P contains a sink component, hence a class
holding a periodic point, hence that periodic point. ∎

**Scope.** Lemma P and Corollary P concern certificates that are *pure*
forward-closed unions of residue classes mod 2^K. They say nothing about
certificates of the form "union of classes minus a finite set": the argument
only shows that U contains the class of a periodic point, and a finite
exception set could remove that point. Theorem 1(b) uses certificates of
exactly that modified form. Throughout this file, "obstructed" and "no
congruence certificate" mean "no forward-closed union of residue classes".

When G1 has a cycle, the classes on G1-cycles are mapped onto each other by
rising branches n ↦ an+b with d = 1, so they form a forward-closed set of
eventually monotone orbits. Traps through such classes give only monotone,
tier-1 divergence. Lemma P is not claimed in that case.

## Application: single-class modifications of 5x+1

Family F_m: change B on one class c mod 2^m to (a n + b)/d with
a ∈ {1,3,5,7}, d ∈ {1,2}, 0 ≤ b < 8 (integral on the class, positive). For each
member:

* **G1-cycle**: the lemma does not apply.
* **obstructed**: Corollary P applies. Periodic points are searched from starts
  below 200, but each one found is a genuine cycle, so the test is sound.
* **open**: some sink component has no known periodic point. For these we try
  Lemma A↑ (`theorem3_ascent.md`) on its lift to modulus 2^m, 2^{m+1} or
  2^{m+2}. "open-cert" means the sink is a proved cycle-free trap. "falls+aper"
  means Lemmas F and I also hold, so the orbits are non-monotone with aperiodic
  itineraries.

| m (modulus) | members | G1-cycle | obstructed (proved, all K) | open, no cert | open-cert | of which falls+aper | trap captures seed 7 |
|---|---|---|---|---|---|---|---|
| 5 (32) | 1504 | 76 | 1373 | 48 | 7 | 5 | 7 members: c = 5 with 3n+6, 7n+7 (falls+aper), (7n+7)/2 (aper only); c = 26 with 3n+6, 3n+7, 7n+1 (falls+aper), (3n+6)/2 (aper only) |
| 6 (64) | 3008 | 108 | 2891 | 8 | 1 | 1 | **10 ↦ 5n+5** (falls+aper) |
| 7 (128) | 6016 | 172 | 5844 | 0 | 0 | 0 | none |
| 8 (256) | 12032 | 300 | 11732 | 0 | 0 | 0 | none |

At m = 7 and m = 8, every member with acyclic G1 is obstructed at every modulus. For the
172 G1-cycle members, a search of seed-7 congruence traps at moduli
2^7 … 2^11 finds exactly one: c = 58, n ↦ 5n+3 (`scratch/g1cases.py`). For
each K it tests the least trap containing T(7). If that trap fails Lemma A↑,
so does every larger one. Least traps covering more than half of the classes
were skipped. It is monotone (falls fail),
because the orbit of 7 sits on the no-halving loop 58 → 293 → 1466 ≡ 58 (mod 128).
This part is EVIDENCE only. The same search at m = 6 finds 3 G1-cycle
members with seed-7 traps (c = 18 ↦ 5n+3, 46 ↦ 7n+7, 58 ↦ 5n+3), all monotone.

**Conclusion for task (3).** The finest single-class modification of 5x+1 in
these families that this method settles with a **non-monotone, aperiodic**
infinite orbit of 7 has density 1/64. That is fx10_64_s7: n ≡ 10 (mod 64) ↦ 5n+5.
At density 1/128 the method is provably obstructed for all members with acyclic
G1, and for the rest only monotone traps exist at moduli ≤ 2^11 (evidence).
Monotone (tier-1) divergence of 7 can be forced by modifications of every
density: put the modified class on a no-halving loop that the orbit of 7 visits,
as in 58 ↦ 5n+3 or 7n+15. Density is therefore not the right measure of
"closeness" for monotone examples. The meaningful measure here is the finest
class admitting a non-monotone trap.

**1932 map.** See `theorem5_precision3.md`. A mixed 2·3-adic version of
Lemma P (Lemma P3) reduces separators for every swap modification σ ∘ G at
any modulus 2^i 3^j to a finite graph mod 2^i·9. For swT9 (CLS-055) and the
other open swap sets this excludes separators that are pure unions of residue
classes at every modulus 2^i 3^j with i ≤ 18. The same test found a new settled two-swap system,
swT2_8_s8. Earlier, weaker evidence: bounded searches of single swaps
σ_{M,a} ∘ G (M ∈ {6, 12, 36, 54, 108}) and double swaps (M ∈ {36, 54}) found
no separators. SAT also found no base-2/3/6/12 automaton separator for swT9
with ≤ 9/8/8/8 states (`scratch/sat_perm.py`, needs python-sat; all
constraints are necessary).
