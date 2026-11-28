# Round 6, lens typeb_wide: isolated expanding cycles (Theorem H), applied widely

28 November 2026. Written by one agent; refereed twice (REFEREE1.md, REFEREE2.md) and revised, see
"Revision after REFEREE1" and "Revision after REFEREE2" at the end. Every finite claim has an exact check
script that exits 0 and can fail (list at the end). Status labels: PROVED / EVIDENCE / OPEN.

## Outcome in one paragraph

**No open census entry is settled.** Every open table map is of type (c), as round 3 found,
so Theorem H cannot touch them; this round did not change that. What the round produced:
(1) Theorem H is now a mechanical proof generator with an independent verifier and a second,
ranking-function proof; (2) exhaustive type tables for 14 families (about 3.4 million
systems in Python, 2 x 4.3 billion in a C scan, 835,000 open-map neighbours) and SAT searches beyond them, with every
type-(b) member found settled (874 enumerated members, 2,030 SAT hits and 1,974 open-map
neighbours; 5,291 stored proof objects re-verified by an independent checker); (3) structural results: the minimal modulus of
type (b), a scaling conjugacy, a theorem giving every parity map an+d a provable neighbour
at modulus 8 that keeps its expanding cycle, Theorem-H neighbours closer than any
descent-certified neighbour for perm_1932inv, perm_c and par_5/7/9, and two corrections to
how the tail-exponent gap can be read; (4) for the blocked mixed system mb_s3_27 an explicit
infinite family of homoclinic expanding periodic points, which shows that it behaves like
type (c) in the sense of Theorem N: no certificate accelerated along finitely many orbits
exists. mb_s3_27 itself stays OPEN.

## Results table

| system / family | technique | result | status |
|---|---|---|---|
| any unit-multiplier table whose G_K has only (a)/(b) SCCs | Theorem H, mechanised (`tblib.prove_H`, `verify_H.py`) | proof object: SCC partition with levels, exact weights and search bound per type-(a) SCC, exact periodic orbit per simple SCC, complete cycle list; checked by a verifier that does not import the generator | PROVED (method) |
| same | counter potential V = (level, phi) (round-4 acc_h16 remark, generalised to every type-(b) cycle) | phi = l (v_p(n - x_i) + E_i) - i drops by >= 1 per step on a simple cycle; second proof, exact descent checked on sample orbits for 13 systems | PROVED (lemma), checked |
| S-family 3n+1 / n+1, m <= 6 (2^32 + 2^16 + ... members) | exhaustive SCC scan (Python m <= 5, C m = 6) | no type-(b) member. At m = 6, 34,560 members have an isolated expanding SCC; in every one it is {63, 62} (x* = -1), it is the only one, and the residue cycle of -5, -7, -10 lies in a type-(c) SCC (`check_iso63.py`, exact) | PROVED |
| S-family 3n+1 / n+1, m = 7, 8 | z3 (`sat_typeH.py`, SC = 2^22; complete for these moduli by the bound in `check_sat_precision.py`) | no type-(b) member | PROVED modulo the z3 UNSAT answer (no independent certificate) |
| S-family 5n+1 / n+1, m <= 6; 7n+1 / n+1, m <= 5 | exhaustive (m = 6 for 5n+1 in C) | no type-(b) member (5n+1, m = 6: 2,218,464 members with an isolated expanding SCC, all with a type-(c) SCC) | PROVED |
| same, 5n+1 m = 7; 7n+1 m = 6 | z3 (SC = 2^22, bound checked) | none | PROVED modulo z3 |
| SPLIT-type u n + d, u in {1,3,5}, common d in {1,3,5}, m <= 4 (m = 5 by z3 for d = 1, SC = 2^22, bound checked; d = 3, 5 at m = 5 by Proposition K) | exhaustive / z3 | none | PROVED (m <= 4), modulo z3 (m = 5) |
| base 3, B(Q, a, S): 3|n -> n/3, S -> a n + 1, else n + 1; Q = 9, 27; a in {2,4,5,7,8,10,11,13} | exhaustive (2.1 M systems) | none; CERT counts agree with round 3 | PROVED |
| base 3, divisions on units, D9 / D27 (u in {2,4,5}) | exhaustive / z3 (SC = 2^22, bound checked; the first run at SC = 4096 was not complete for D27) | none | PROVED / modulo z3 |
| shift family SH3: odd -> 3n+1 or n+d, d in {1,3,5,7} | exhaustive m <= 4, z3 m = 5 | m = 3: 2, m = 4: 358 type (b), all settled; m = 5: at least 2,000 (z3) | PROVED |
| shift family SH5 (5n+1 or n+d) | exhaustive m <= 4 | m = 3: 3, m = 4: 458, all settled | PROVED |
| base 3 C9 (8 branch choices per unit class mod 9) | exhaustive | 53 type (b), all settled | PROVED |
| base 3 C27 (same menu mod 27) | z3 | type (b) members exist (30 found, all settled) | PROVED (existence) |
| **sh8**: n/2 on evens; n = 1 (8) -> n+1; 3, 7 -> 3n+1; 5 -> n+5 | Theorem H | cycles (1 2), (5 10); isolated x* = -1; smallest modulus possible with n/2 on evens | PROVED |
| 5x+1 relative: n/2 on evens; n = 1, 5 (8) -> 5n+1; 3 -> n+3; 7 -> n+7 | Theorem H | cycles with minima 3 and 7; keeps 5x+1's expanding point -1/3, isolated | PROVED |
| c9b: base 3 mod 9 (see check_examples) | Theorem H | the expanding cycle is the positive cycle (1 3), multiplier 4/3, isolated; cycles (1 3), (2 5 6) | PROVED |
| minimal modulus (Prop. M) | shape enumeration | no type (b) at modulus p (any p; checked 2, 3, 5, 7); exists at 4 (general tables) and 9; with n/2 on every even class, not at 4, exists at 8 | PROVED |
| **Theorem P8**: parity map an+d (a >= 3 odd, d odd, a + d >= 1) with n = 4 (mod 8) -> n + 4 | round3/traps Corollary F1 extended to d >= 1 - a, plus the trivial dynamics on the trap; checked on 630 pairs | every positive orbit is eventually periodic; cycles (4 8) and (x*, 2x*) when x* = -d/(a-2) is a positive integer; type (b) with x* isolated | PROVED |
| open table maps: one-class modifications at Q p, Q p^2, Q p^3 (moduli up to 81; 304,296 tables) | exact classification + Theorem H | type-(b) neighbours exist for every par_* map at modulus 8 (par_3_* also at 16; par_5_*, par_7_*, par_9_1 have none at 16), split5_1 (mod 8, 16, 32); none for m3_*, perm_*, desc_*, split5_3 | PROVED (each neighbour settled) |
| open table maps: two-class modifications at moduli 4, 8, 9 (530,668 tables) | same | type-(b) neighbours for par_3_1, par_3_m1, par_5_1, par_7_1, par_9_1 (the only par maps run in two-class mode), perm_1932inv (68), perm_c (68), split5_1 (304), split5_3 (139), desc_m3_4n5 (33), desc_split7_1 (200); none for m3_b, m3_d, m3_e, m3_g, perm_1932, perm_b, perm_swap at 9 | PROVED |
| perm_1932inv, perm_c | two-class Theorem-H neighbours at modulus 8 | distance to provability at level 8 drops from 3 (descent, round 3) to at most 2 | PROVED |
| par_5_d, par_7_d, par_9_1 | Theorem P8 | distance at level 8 drops from 2 (par_5, par_7) and [2,4] (par_9_1) to 1 | PROVED |
| tail-exponent gap (round4/lundberg) | exact Collatz-Wielandt certificates | gap zero does NOT imply type (b): an S-family member at m = 6 has theta_1 = theta_run = log 2/log(3/2) and a type-(c) SCC; at the boundary of the standing hypothesis, gap zero with theta_1 > 0 and divergent orbits occurs (division-free translation class). Whether gap zero implies GLOBAL under the standing hypothesis is OPEN (an earlier sentence claiming it was WRONG and is withdrawn) | PROVED / OPEN |
| **mb_s3_27** (n = 26 mod 27 -> (n+1)/27; even n/2; odd (3n+1)/2) | homoclinic orbits, Theorem N transferred | y_d = 27·9^d/(8^{d+1} - 3·9^d) - 5 is a periodic point following the ghost cycle -5,-7,-10 d times, for every d >= 0, multiplier (9/8)^d·3/8 (> 1 for d >= 9). Hence no generalized (finitely-accelerated) certificate exists | PROVED; the system itself OPEN |
| every open census table map | Theorem H | not applicable: all are type (c) | (round 3 result, unchanged) |

## 1. Theorem H as a mechanical proof

`tblib.prove_H(p, m, table, K)` returns, or refuses with None, a proof object with:

* the table hypotheses (unit multipliers, w = p^e, exact divisibility on each class, and
  T(Z>0) in Z>0, checked at the least positive member of each class, which suffices because
  each branch is increasing);
* the SCCs of G_K with a **level** per SCC that drops strictly along every edge between SCCs;
* for each **simple-cycle SCC** (type (b), or a contracting simple cycle): the residue cycle,
  the exact composed map A x + B, and the exact periodic orbit x_0, ..., x_{l-1} (rationals
  with denominators prime to p), with x_i = node_i (mod p^K);
* for each **non-simple contracting SCC**: theta < 1 and positive rational weights c(r) with
  c(s) q <= theta c(r) on every internal edge, beta = max c(s) max(v, 0)/w, the bound
  Vmax = beta/(1 - theta) and the enumeration of the finitely many n with c(n mod p^K) n <= Vmax;
* the complete cycle list.

`verify_H.py` re-derives the graph from the table and checks all of it with integers and
Fractions only: the partition is exactly the SCC decomposition (each part strongly connected,
levels strictly drop between parts), the weight inequalities, the periodic orbits, the search
and the cycle list. It does not import the generator.

**The argument that the verifier certifies (PROVED).** Let n > 0. Levels never increase along
the orbit, so from some time on the residues stay in one SCC Sigma.
*Sigma a simple cycle with a division* (types (b) and contracting simple cycles alike): for n in
class node_i, T(n) - x_{i+1} = (u/w)(n - x_i) because T is affine on the class and
(u x_i + v)/w = x_{i+1}. Hence v_p(T(n) - x_{i+1}) = v_p(n - x_i) - e_i, and the counter
phi(n) = l (v_p(n - x_i) + E_i) - i (E_i = divisions on the cycle before position i) drops by
at least 1 at every step, while phi >= -l (as n = x_i mod p^K, v_p(n - x_i) >= K >= 0). So only
n = x_i can stay forever, and then x_i is a positive integer on a T-cycle. (This replaces the
nested-cylinder argument of round 3 by an explicit ranking function, and covers contracting
simple cycles too, without the real-distance argument.)
*Sigma contracting with weights*: V(n) = c(n mod p^K) n satisfies V(T n) <= theta V(n) + beta
while the orbit stays in Sigma (this uses n > 0), so V eventually stays below Vmax + 1, a finite
set. Every cycle lies in one SCC; the cycles in Sigma satisfy V <= Vmax at their maximum, and
are found by the enumeration. ∎

**Second proof: the counter potential (PROVED, generalising round4/wpotential theory.md, the
acc_h16 remark).** The lexicographic V(n) = (level, phi), with phi = c(r) n on contracting
SCCs, the counter above on simple-cycle SCCs and 0 on trivial SCCs, descends at every step off
a finite set: the level drops, or phi drops by 1 on a cycle, or phi(Tn) <= theta phi(n) + beta.
For acc_h16 this is exactly REFEREE1's certificate (counter 2 v_2(n+1) on node 15, here
l v_2(n - x_i) + ... with l = 2). `check_examples.py [CNT]` checks the descent exactly along
the orbits of n <= 3000 and of 300 random n < 2^200 for 13 systems. The lemma is a formal
identity; the sample check guards the implementation.

## 2. Systematic enumeration

`families.py` defines the families, `scan.py` classifies every member at level m (level m
suffices: type (c) is level independent, round3 trichotomy.md Lemma L, and the lift of an (a)
SCC contains only contracting cycles while the lift of an isolated expanding cycle is its
periodic point's residue cycle plus transient nodes), and settles every type-(b) member with
prove_H. Counts (verdicts: a = CERT, b = type (b), c = some type-(c) SCC, divfree = some
division-free cycle, the standing hypothesis fails):

| family | members | a | b | c | divfree |
|---|---|---|---|---|---|
| S3 (3n+1 / n+1), m = 2, 3, 4, 5 | 4, 16, 256, 65,536 | 2, 6, 84, 16,656 | 0 | 2, 10, 172, 48,880 | 0 |
| S3, m = 6 (C scan, `sbrute.c`) | 4,294,967,296 | | 0 | (34,560 have an isolated expanding SCC and a (c) SCC) | |
| S5 (5n+1 / n+1), m = 2..5 | 4 ... 65,536 | 1, 3, 22, 2,155 | 0 | 3, 13, 234, 63,381 | 0 |
| S5, m = 6 (C scan) | 4,294,967,296 | | 0 | (2,218,464 with isolated expanding SCC and a (c) SCC) | |
| S7 (7n+1 / n+1), m = 2..5 | 4 ... 65,536 | 1, 2, 17, 776 | 0 | 3, 14, 239, 64,760 | 0 |
| SPL_d (u in {1,3,5}, common +d), d = 1, 3, 5, m = 4 | 6,561 each | 506 | 0 | 6,055 | 0 |
| SH3 (3n+1 or n+1, n+3, n+5, n+7), m = 3, 4 | 625, 390,625 | 480, 295,200 | **2, 358** | 143, 95,067 | 0 |
| SH5 (5n+1 or n+d), m = 3, 4 | 625, 390,625 | 356, 193,632 | **3, 458** | 266, 196,535 | 0 |
| B9_a, a in {2,4,5,7,8,10,11,13} | 64 each | 24, 10, 8, 6, 6, 1, 1, 1 | 0 | | 40 for a = 2, 5, 8, 11 |
| B27_a, same a | 262,144 each | 57,816, 11,661, 4,364, 1,328, 1,074, 69, 76, 64 | 0 | rest | 165,376 (a = 2, 5, 11), 220,672 (a = 8) |
| C9 | 262,144 | 11,956 | **53** | 117,111 | 133,024 |
| D9 | 729 | 54 | 0 | 675 | 0 |

The CERT counts of S3, B27 and C9 equal round 3's (`check_scans.py [R3]`).

**What the table shows (EVIDENCE for a pattern, PROVED for each entry).** Type (b) appears
only when the non-expanding branches use **different shifts** (SH3, SH5, C9, C27). In every
family whose branches all have the same additive constant (S3, S5, S7, SPL, B9, B27) there is
no type-(b) member at any tested modulus, although isolated expanding SCCs do occur (from
m = 6 on in S3 and m = 5 in S5): they always come with a type-(c) SCC elsewhere. For the
3n+1 S-family at m = 6 this is now PROVED exactly (`check_iso63.py`, added after REFEREE1):
the 34,560 members with an isolated expanding SCC are exactly the members in which {63, 62}
is an SCC (an explicit enumeration of the latter gives 34,560, equal to the C-scan count of
the former); in each of them {63, 62} is the only isolated expanding SCC, the classes 59 and
57 of -5 and -7 lie in S, and the residue cycle 59, 50, 57, 44, 54 of the negative 3x+1
cycle -5, -7, -10 (multiplier 9/8) lies in an SCC that is not a simple cycle, which is
therefore of type (c). (In the first version this was stated without a check.) For S5 at
m = 6 the identity of the isolated SCCs and of the companion was not examined. *Conjecture CS (OPEN): a 2-adic table with n/2
on every even class and branches u_r n + d with one common d is never of type (b).* Proved
here only up to the moduli in the table.

**Proposition K (scaling conjugacy; PROVED; called "Proposition CS" in the first version).** For p not dividing d, x -> d x is a bijection of Z_p that
permutes the classes mod p^m and conjugates the branches u n + d (resp. n/p) to u n + 1 (resp.
n/p). So the cylinder graphs of the common-shift-d family and the common-shift-1 family are
isomorphic with the same multipliers, and the type counts agree. This is why SPL_d1, d3, d5
have identical rows. (The conjugacy is 2-adic only; it does not preserve the positive
integers, so it transfers types, not cycle lists.)

**Natural examples (all PROVED; `check_examples.py`, except the 5x+1 relative, which is checked in
`referee1_check.py` and `referee2_check.py`).**

* sh8 (mod 8): n/2 on evens; n = 1 -> n+1; n = 3, 7 -> 3n+1; n = 5 -> n+5. Cycles (1 2),
  (5 10). The SCC {7, 6} is the shadow of x* = -1 (multiplier 3/2), isolated because node 6's
  other successor 3 leads only into the contracting part. By Prop. M no table with n/2 on every
  even class has smaller modulus.
* sh16: 3n+1 on 5 of the 8 odd classes mod 16 (n+5 on 5, n+1 on 9, n+7 on 13); cycles (1 4 2),
  (5 10). sh32 (z3): 3n+1 only on 31 mod 32, cycles (1 2), (5 10).
* 5x+1 relative (mod 8): n/2 on evens; n = 1, 5 -> 5n+1; n = 3 -> n+3; n = 7 -> n+7. Keeps the
  5x+1 obstruction x* = -1/3 (multiplier 5/2) as an isolated cycle.
* c9a (base 3, mod 9): 3|n -> n/3; 1, 4 -> 5n+1; 2 -> 2n+1; 5 -> n+1; 7 -> 4n+1; 8 -> 2n-1;
  isolated x* = -1/2 (5/3); one cycle (2 5 6).
* c9b: 3|n -> n/3; 1 -> 4n-1; 2 -> 2n+1; 4, 7 -> 4n+1; 5 -> n+1; 8 -> 2n-1. Here the isolated
  expanding cycle is the positive cycle (1 3) itself (multiplier 4/3); cycles (1 3), (2 5 6).
  So "expanding" and "attracting nothing but itself" coexist for a genuine positive cycle.

## 3. Structural results

**Proposition M (minimal modulus; PROVED).** (i) No unit-multiplier table at modulus p (any
prime p) is of type (b). Proof: at modulus p a branch with a division has all p nodes as
successors. A simple-cycle SCC with a division is then a single node r with a self-loop, and no
other node may reach r; so every other node has e = 0, and their single successors form a
functional graph on the remaining nodes, which has a cycle, a division-free cycle. (ii) At
modulus 4 there are type-(b) tables (128 of the 2401 cylinder shapes), e.g. sh4:
n = 0, 1 (4) -> n+1, n = 2 -> (n+2)/2, n = 3 -> (3n+1)/2 (isolated x* = -1; cycles (2), (4 5 6)).
(iii) With n/2 on every even class, modulus 4 is impossible (0 of 49 shapes) and modulus 8 is
attained (sh8); with n/3 on every class 0 mod 3, modulus 3 is impossible by (i) and 9 is
attained (acc_h9). `shapes.py` checks (i) for p = 2, 3, 5, 7 and (ii), (iii) exhaustively. The
reduction to shapes: types depend only on, per class, the division exponent, the target
residue and the size of u; a shape admits type (b) iff it has no division-free cycle and a
simple-cycle SCC with a division containing a class whose u may be chosen (put u = 1 elsewhere,
which makes every other cycle contract, and u large on that cycle).

**Theorem P8 (PROVED).** Let a >= 3 and d be odd with a + d >= 1, and let
T(n) = n + 4 if n = 4 (mod 8), n/2 for other even n, a n + d for odd n. Then every positive
orbit is eventually periodic, and the cycles are (4 8) and, when x* = -d/(a-2) is a positive
integer, (x*, 2x*).
*Proof.* The set M4 of multiples of 4 is invariant (8 | n gives n/2 in M4; n = 4 mod 8 gives
n + 4 = 0 mod 8). On M4, n = 4k evolves as k -> k/2 (k even), k -> k+1 (k odd), which takes
every k >= 1 to the cycle k = 1, 2, i.e. n = 4, 8. If the orbit never meets M4, each even
iterate is 2 mod 4 and is halved once to an odd number, so from the first odd iterate n_0 on,
n_{j+1} = (a n_j + d)/2 with every n_j odd. Then n_j - x* = (a/2)^j (n_0 - x*), and since
x* has odd denominator a - 2, v_2(n_0 - x*) = j + v_2(n_j - x*) >= j for every j, so
n_0 = x*; then a x* + d = 2x*, which is 2 mod 4, and the orbit is the cycle (x*, 2x*). ∎
*Attribution (added after REFEREE1).* The core of this proof, that every orbit of
n/2 | an + b meets 4 mod 8 unless it is the rigid orbit of x* = -b/(a-2), forced by the
valuation drop, is round3/traps/family.md Corollary F1 (FAM_4mod8 in round3/traps/README.md),
stated there for odd b >= 1. P8 adds only two things: the range d >= 1 - a (which brings in
3x-1 and the other negative d), and the observation that redirecting 4 mod 8 to n + 4 makes
M4 a trap with trivial dynamics, so F1 becomes a Theorem-H-provable neighbour with the
expanding point kept. P8 is "F1 turned into a provable neighbour", not a new mechanism.
In cylinder terms: G_3 has the absorbing contracting SCC {0, 4} and one isolated expanding
2-cycle {x* mod 8, 2x* mod 8} with multiplier a/2; so T is of type (b), and Theorem H
reproduces the cycle list (`check_examples.py [P8]`, 630 pairs (a, d)). The proof is
elementary: the modification is a trap, and the part outside the trap is rigid (F1). It is stated
because it covers every open parity map (3x+1, 3x-1, 3x+d, 5x+d, 7x+d, 9x+1) at once and
keeps each one's expanding fixed point: -1 for 3x+1, -1/3 for 5x+1, -1/5 for 7x+1, -1/7 for
9x+1 (x* = -d/(a-2); the 2-cycles are (x*, 2x*), e.g. (-1/5, -2/5); corrected after REFEREE2, which
found -2/5 and -2/7 quoted, the even points 2x*), and the genuine cycle (1 2) for 3x-1. For par_5_d, par_7_d and par_9_1 this lowers the
level-8 distance to provability from 2 (round 3, descent) to 1.

**Open-map neighbours (PROVED for each neighbour, `mods.py`).** Menu per class: any branch
(u', v', p^e') with u' <= u a unit, e' <= 2, every target residue once, exact and positive
(damping, resets, shifts, extra divisions). Type-(b) counts / CERT counts:

| open map | one class at Q p^j | two classes at moduli 4, 8, 9 |
|---|---|---|
| par_3_d (all 8 open d) | 8: 2/9, 16: 11/0 | (par_3_1, par_3_m1) 4: 4/158, 8: 141/1781 |
| par_5_d (all 7), par_7_d, par_9_1 | 8: 2/0 | par_5_1 8: 159/353; par_7_1 8: 209/404; par_9_1 8: 261/159 |
| split5_1 | 8: 5/38, 16: 15/22, 32: 39/0 | 8: 304/2981 |
| split5_3 | 8: 0/37, 16: 0/95, 32: 0/221 | 8: 139/3011 |
| desc_split7_1 | 8: 0/51, 16: 0/119, 32: 0/94 | 8: 200/4621 |
| desc_m3_4n5 | 9: 0/34, 27: 0/28, 81: 0/0 | 9: 33/4434 |
| desc_s32_plus9 | 64: 0/868 | not run |
| perm_1932inv, perm_c | 8, 16, 32: 0/0 | 8: 68/0 each |
| perm_d | 16, 32, 64: 0/0 | not run |
| m3_b, m3_d, m3_e, m3_g, perm_1932, perm_b, perm_swap | 9, 27, 81: no type (b) | 9: no type (b) |

Representatives: 3x+1 with n = 4 (8) -> n+4 (P8); perm_1932inv with n = 2 (8) -> (n+2)/2 and
n = 6 (8) -> n - 4 (keeps the expanding fixed point 0 of 2q -> 3q, cycles with minima 1, 2);
perm_c with n = 1 (8) -> n+2, n = 7 (8) -> n-2 (x* = 0; cycles 1, 5); split5_3 with
n = 0 (8) -> (n+2)/2, n = 2 (8) -> n+1 (isolated x* = -5/3; cycles 3, 7). For perm_1932inv and
perm_c no one- or two-class modification at modulus 8 is CERT (round 3: distance 3), but 68
two-class modifications are type (b): Theorem H brings provable neighbours one class closer.
For the base-3 permutation family (perm_1932, perm_b, perm_swap) and the m3_* maps nothing
changes: no type-(b) neighbour at the tested moduli.

## 4. The tail-exponent gap (round4/lundberg Theorem 1)

Under the standing hypothesis, type (b) gives theta_1 = theta_run (lundberg Theorem 1(2)) and
GLOBAL (Theorem H), so a type-(b) system has gap zero and no divergent orbit. Two further
facts, both PROVED with exact certificates (`check_gap.py`; rho_S(t) <= 1 is certified by a
positive rational vector x with M^up x <= x, where M^up bounds M_t entrywise via exactly
checked rational powers, plus log-convexity of rho_S and rho_S(0) <= 1):

* **Gap zero does not imply type (b).** The S-family member with
  S = {3,7,15,23,31,35,39,41,47,51,55,57,59,63} (mod 64) has the isolated cycle {63, 62}
  (theta_C = log 2/log(3/2) = 1.7095) and a type-(c) SCC of 34 nodes with
  rho(665/389) = 0.847 < 1. So theta_1 = theta_C, and the expanding cycles of the (c) SCC have
  run exponent > theta_S >= theta_C, so theta_run = theta_C too: the gap is zero, yet no
  generalized certificate exists (Theorem N). The gap only sees re-entry at the minimising
  cycle.
* **Boundary of the standing hypothesis.** sh8 lifted to modulus 16 with n = 9 (16) -> n + 16:
  the class 9 mod 16 is a division-free self-loop, so every n = 9 mod 16 diverges linearly. Its
  block has rho = 1 for every theta, the rest is one isolated cycle (-1) plus contracting SCCs,
  so theta_1 = theta_run = 1.7095 > 0: gap zero with divergent orbits. With a division-free
  cycle of multiplier > 1 instead (e.g. n -> 3n + 2 on n = -1 mod 2^m), theta_1 = 0.

**Withdrawn (REFEREE1 item 15, WRONG).** The first version ended this section with "So 'gap
zero and theta_1 > 0 implies GLOBAL' holds exactly under the standing hypothesis". That was
not proved, and nothing here supports it: G1 above satisfies the standing hypothesis, has gap
zero and theta_1 > 0, and is of type (c); its GLOBAL status is unknown, and Theorems H and N
say it has no generalized certificate. Had the sentence been true it would settle G1 and
every type-(c) system whose minimising cycle is isolated. What is proved is only this:
* under the standing hypothesis, type (b) implies gap zero and GLOBAL (lundberg Theorem 1(2)
  and Theorem H);
* gap zero does not imply type (b) (G1);
* whether gap zero (with theta_1 > 0) implies GLOBAL under the standing hypothesis is OPEN;
* without the standing hypothesis, gap zero and theta_1 > 0 coexist with divergent orbits (G2).

## 5. Mixed base: the blocked system mb_s3_27

System: n = 26 (mod 27) -> (n+1)/27; else even n -> n/2; else n -> (3n+1)/2. Round 3 left it
open; the obstruction is the "ghost" cycle -5 -> -7 -> -10 (branch word EEH, multiplier 9/8).
round4/wpotential found two expanding rational cycles and expanding points for d = 10, 20, 40
and left open whether there are infinitely many. (A sibling folder, round6/blocked27, works on
the system's normal form.)

**Theorem Y (PROVED; `mixed27.py check`).** For every d >= 0 the rational
y_d = 27·9^d / (8^{d+1} - 3·9^d) - 5 (denominator prime to 6) is a periodic point of the map
extended to Z_(6), with branch word W C^d, W = HEH, C = EEH, period 3d + 3 and multiplier
(9/8)^d · 3/8, which is > 1 exactly for d >= 9.
*Proof.* Put s = y + 5. W is x -> (3x + 2)/8 on the branch level; W(-5) = -13/8, so
c := W(-5) + 5 = 27/8 and W(y) + 5 = (3/8) s + c. Along C, z -> (9z + 5)/8, i.e.
z + 5 -> (9/8)(z + 5). The fixed-point condition for the word W C^d is
(9/8)^d ((3/8) s + c) = s, i.e. s_d = c / ((8/9)^d - 3/8) = 27·9^d/(8^{d+1} - 3·9^d). One must
check that y_d really follows the word (the map is not Markov, so this is not automatic):
* the entry point z_0 = W(y_d) and the lap points z_j = C^j(z_0) satisfy
  z_j + 5 = (9/8)^j (8/9)^d s_d, so v_2(z_j + 5) = 3(d - j) + v_2(s_d) = 3(d - j) >= 3 and
  v_3(z_j + 5) = v_3(s_d) - 2(d - j) = 2j + 3 >= 3 for j < d (v_2(s_d) = 0, v_3(s_d) = 2d + 3,
  since 3·9^d is odd and v_3(8^{d+1} - 3·9^d) = 0). So z_j = -5 mod 8 and mod 27, which forces
  the three branches E, E, H (parities of -5, -7, -10, and residues 22, 20, 17 mod 27, none 26);
* at y_d itself: s_d = -9 (mod 2^{3d+3}), so y_d = -14 (mod 8), which gives the parities H, E, H
  of W (-14, -7, -10), and y_d = -5 (mod 27), whose W-images -5/2, -13/4 are not 26 mod 27.
Infinitely many of the orbits are distinct: O(y_d) avoids -5 (s_d != 0) and contains z_{d-1}
with v_3(z_{d-1} + 5) = 2d + 1, while a fixed finite orbit not containing -5 bounds
v_3(z + 5) on its points. (For d <= 80 the orbits are checked to be pairwise disjoint and to
avoid -5, -7, -10.) ∎

**Corollary (PROVED).** mb_s3_27 has no generalized certificate in the sense of Theorem N:
no cover of (Z_2 x Z_3) minus finitely many periodic orbits by cylinders with stopping times
j_i such that T^{j_i}(n) < n for almost all positive n in each cylinder. *Proof.* Theorem N's
argument transfers: the branch of x is decided by (x mod 2, x mod 27), the set of points that
follow a fixed word is open and closed in Z_2 x Z_3, and the integers are dense there. Take
d >= 9 with O(y_d) disjoint from the exceptional set (all but finitely many d qualify); by the
cycle lemma (Raney's lemma) some point y of O(y_d) has all partial multipliers > 1; for N large every integer
n = y (mod 2^N 3^N) lies in the cylinder D_i containing y and follows its word for j_i steps,
so T^{j_i}(n) = lambda n + beta with lambda > 1, which is > n for all large n in this
progression. ∎ `mixed27.py check [R]` exhibits integers n = y_d mod 2^N 3^N (d = 9, 12, 20)
that stay above n for a whole period.

**What this says about a "type (b)" notion for non-unit maps.** The natural definition
("every expanding periodic point of Z_(N) is isolated: no other expanding periodic orbits
accumulate on it") is exactly what Theorem N's argument needs, and mb_s3_27 violates it at
the ghost cycle, explicitly. So no type-(b)/Theorem-H-style argument can settle mb_s3_27;
it behaves like type (c) in the sense of Theorem N, with the 2-adic part of the dynamics a split map
with slope 9/8 (consistent with round6/blocked27). The system is **not settled**.

## Honest limits

* No open census question is settled. Theorem H applies to none of them, as round 3 said.
* The new settled systems are constructed or found by search; most are tier 2 (finite
  computation plus exact weights). Theorem P8 is elementary (a trap plus a rigid cycle).
* The z3 UNSAT answers (S3 at m = 7, 8; S5 at m = 7; S7 at m = 6; SPL at m = 5; D27) are not
  independently certified. The first version called the encoding "sound and complete"; that
  was too strong. It is sound for SAT answers (each hit is re-proved by prove_H and
  verify_H). It is complete only when the scale SC is large enough for the moduli at hand, and
  at the shipped SC = 4096 it was NOT complete for S3 m = 8 and D27 (REFEREE1 item 4; a
  contracting cycle could be wrongly excluded, an expanding one missed). After the revision
  SC = 2^22, `check_sat_precision.py` verifies the explicit completeness bound for every z3
  row (all count vectors of a simple cycle of length <= p^m, multiplier sign decided exactly),
  and every row was re-run at SC = 2^22 and is still UNSAT (out/sc22/). The encoding
  reproduces the exhaustive counts exactly where both exist (C9: 53, SH3 m = 3, 4: 2 and 358,
  D9 and S3 m <= 6: 0). Two encoding bugs found during the run (tails in the designated
  cycle; division-free C-cycles) only admitted spurious solutions, which prove_H rejected;
  UNSAT answers were unaffected, and the encoding was fixed and re-validated.
* The m = 6 C scans use floating-point Karp with a 1e-9 margin; check_scans.py [BRUTE] records
  why that is exact here (cycle means are bounded away from 0 by more than 2e-4).
* Conjecture CS (no type (b) with one common shift) is OPEN beyond the tested moduli.
* Literature novelty was not checked. External theorems used, all classical and quoted from
  memory via round4/lundberg, not re-checked at the source: Kingman's theorem that the
  spectral radius of a matrix whose entries are log-convex functions of a parameter is
  log-convex (used for theta -> log rho_S(theta) in section 4), and the Collatz-Wielandt
  bound (a nonnegative matrix M and a positive vector x with M x <= x give rho(M) <= 1),
  used for every rho_S(t) <= 1 certificate. (The first version said "no external theorem is
  used", which was inaccurate.) Theorem N and Theorem H are internal (round 3).

## Files

| file | content |
|---|---|
| tblib.py | classification (exact), prove_H, proof-object serialisation |
| verify_H.py | independent verifier of proof objects (exit 0 iff all verify) |
| families.py, scan.py | family definitions; exhaustive scan + settlement (data/scan_*.json, data/*_H.json) |
| sbrute.c, run_brute.sh | C scan of the S-family at m = 6 (out/brute/) |
| sat_typeH.py, sat_sfamily.py, sat_sfam_H.py, sat_family.py | z3 searches (out/sat*.txt, data/sat_*_H.json) |
| shapes.py | Proposition M |
| mods.py | one- and two-class neighbours of the open maps (data/mods_ONE_81.json, data/mods_TWO_9.json) |
| gap.py, check_gap.py | tail-exponent certificates (needs numpy: round4/wpotential/.venv) |
| mixed27.py | Theorem Y and its checks |
| check_examples.py | named systems, counter potential, Theorem P8, negative controls |
| check_scans.py | re-scan, round-3 cross-check, re-verification of all proof objects, C-scan summary |
| check_iso63.py | (revision) exact identification of the isolated SCC {63, 62} and the type-(c) companion for all 34,560 S3 m = 6 members |
| check_sat_precision.py | (revision) completeness bound of the z3 encoding at the chosen SC, for every z3 row; reproduces the SC = 4096 failures (out/sat_precision.txt) |
| check_sat_sc22.py | (revision) z3 at SC = 2^22 reproduces the exhaustive type-(b) counts (C9, SH3 m = 3, SH5 m = 3, D9); stored UNSAT re-runs out/sc22/ |
| referee1_check.py, REFEREE1.md | the referee's independent check and report |

## Reproducing

    python3 check_examples.py          # about 30 s
    python3 shapes.py                  # under 1 s
    python3 mixed27.py check           # under 1 s
    python3 check_scans.py             # a few minutes (add --full for all families)
    ../../round4/wpotential/.venv/bin/python check_gap.py
    python3 verify_H.py data/*_H.json  # re-verify stored proof objects
    python3 check_iso63.py             # about 5 s
    ../../round4/wpotential/.venv/bin/python check_sat_precision.py   # about 25 s
    ../../round4/wpotential/.venv/bin/python check_sat_sc22.py        # a few seconds
    python3 referee1_check.py          # the referee's check, about 1 minute

All exit 0. Rebuilding the data: `python3 scan.py <family>`, `python3 mods.py ONE 81`,
`python3 mods.py TWO 9 <prefixes>`, `./run_brute.sh` (about 35 minutes on 10 cores),
`sat_*.py` with the venv python.

## Revision after REFEREE1

REFEREE1.md confirmed every PROVED theorem (Theorem H as a proof object, the counter lemma,
Propositions M and K, Theorem P8, Theorem Y and its corollary, G1) and every recomputed count,
and raised one WRONG item, one attribution fix, one coverage fix, one completeness gap in the
z3 encoding, two unchecked sentences and nits. What was changed:

| referee item | what was wrong | repair | status now |
|---|---|---|---|
| 15 (WRONG) | §4 said "gap zero and theta_1 > 0 implies GLOBAL holds exactly under the standing hypothesis" | sentence withdrawn in §4 and replaced by the proved statements; the implication is listed as OPEN (G1 is a test case: standing hypothesis, gap zero, theta_1 > 0, type (c), status unknown) | withdrawn; OPEN |
| 10 (attribution) | Theorem P8 read as new | P8 now cites round3/traps/family.md Corollary F1 as its core and is presented as F1 extended to d >= 1 - a and turned into a Theorem-H-provable neighbour | PROVED, not new in mechanism |
| 11 (coverage) | results row said "every par_* map (mod 8, 16)" | reworded: every par_* map at 8; at 16 only par_3_* (par_5_1@16 is {divfree 40, c 840}) | corrected |
| 4 (z3 completeness) | "sound and complete" was false at SC = 4096 for S3 m = 8 and D27 | SC raised to 2^22 in `sat_typeH.py`; `check_sat_precision.py` checks the explicit bound for every z3 row over all count vectors of simple cycles (with the necessary realisability caps: Hall's condition per branch type, and #odd steps <= #halvings for the 2-adic rows), and reproduces the SC = 4096 failures (exactly S3 m = 8 and D27 with the caps; S3 m = 7 and S5 m = 7 also fail the crude bound without caps, but no realisable cycle violates it); all eight z3 rows re-run at 2^22, still UNSAT (out/sc22/); `check_sat_sc22.py` re-validates the SAT direction at the new scale (C9 53, SH3 m = 3 2, SH5 m = 3 3, D9 0) | PROVED modulo z3, with the completeness bound now checked |
| 3 (i), edit 6 | "{63, 62}" for all 34,560 members not established by a script | `check_iso63.py`: exact enumeration of the members in which {63, 62} is an SCC (7,740 closure configurations, 34,560 members) equals the C-scan count of members with any isolated expanding SCC, so the sets coincide; each member checked to have no other such SCC | PROVED (exact, no z3) |
| 3 (ii), edit 6 | "the companion (c) SCC always contains -5, -7, -10" was unchecked | same script: in all 34,560 members, 59 and 57 lie in S and the residue cycle 59, 50, 57, 44, 54 lies in a non-simple SCC | PROVED (S3, m = 6 only) |
| edit 5 | "No external theorem is used" | Kingman log-convexity and the Collatz-Wielandt bound now named in Honest limits (quoted from memory, via round4/lundberg) | corrected |
| nits | Proposition CS / Conjecture CS name clash; "B <= 64" in check_scans.py; "proves that it is the mixed-base analogue of type (c)" | renamed Proposition K; B <= 32; "behaves like type (c) in the sense of Theorem N" | corrected |

Nothing else changed: no count, cycle list or proof object was altered, and no open census
entry is settled.

## Revision after REFEREE2

REFEREE2.md re-derived every PROVED theorem, recomputed every count and confirmed that the
REFEREE1 repair is honest and complete (needs_repair: false). It listed four wording or number
fixes and some nits. All are made; no proof, count, cycle list or label changed.

| referee item | repair |
|---|---|
| 1 (numbers) | §3, P8 paragraph: the expanding fixed points of 7x+1 and 9x+1 were quoted as -2/5 and -2/7, which are the even points 2x* of the 2-cycles. Now -1/5 and -1/7 (x* = -d/(a-2)), with the 2-cycle (-1/5, -2/5) named |
| 2 (coverage) | results row for two-class modifications: "par_*" replaced by par_3_1, par_3_m1, par_5_1, par_7_1, par_9_1, the only par maps run in two-class mode (as the §3 table already said) |
| 3 (wording) | results row for SPLIT: m = 5 by z3 for d = 1 only; d = 3, 5 at m = 5 follow by Proposition K |
| 4 (attribution) | §2 "Natural examples": the 5x+1 relative is not in `check_examples.py`; it is now cited to `referee1_check.py` and `referee2_check.py` |
| 5 (nit) | `check_gap.py` docstring now states that t >= theta_C is chosen by a float comparison, with margin about 2.8e-7 for G1 (t = 665/389), and that it holds exactly (2^1054 <= 3^665) |
| nit (Theorem Y corollary) | the cycle lemma is now named (Raney's lemma) |
