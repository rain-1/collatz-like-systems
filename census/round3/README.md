# Round 3 (27 November 2026): new systems and the certificate wall

Ten prover lenses each built new Collatz-like systems or new theory, wrote
proofs with exact check scripts, and were then examined by an independent
referee who re-derived the proofs and wrote a separate check. Two lenses
needed a repair round, each confirmed by a second referee: `mixedbase` had two
false sub-claims, and `progressions` had a gap in its counting lemma, one
false sentence about the 1932 map and one overstated clause. The other
referees asked only for small fixes, which have been applied and are listed in
each folder's README under "Refereeing".

**None of the 66 open census questions was settled.** What the round produced
is (1) about a hundred individually named new systems with complete answers,
plus several exhaustively classified families, and (2) a sharp description,
reached independently by three lenses, of where every certificate-style proof
stops. All work is agent-written and agent-refereed; none has had human
review, and literature novelty was mostly not checked.

## The main theoretical result: a trichotomy

For a table map whose multipliers are units at the modulus prime (3x+1, 5x+1,
the split, m3 and desc families, the 1932 permutation), look at the strongly
connected components of the residue graph. Three lenses arrived at the same
statement from different directions (`accel/trichotomy.md` Theorems H, N, T;
`traps/theory.md` Theorems 1 to 4; `dichotomy/dichotomy.md` Theorem 1):

| Components of the residue graph | What can be proved | Tool |
|---|---|---|
| every cycle contracts | a descent certificate exists and gives the complete cycle list; conversely a certificate exists only in this case | `dichotomy/decide.py` (always answers, any modulus) |
| expanding cycles exist, but each is a component on its own | still provable: only the cycle's own periodic point can follow it forever | `accel/accel_lib.py`, `traps/` (case P1) |
| an expanding cycle shares a component with another cycle ("free re-entry", a homoclinic orbit) | no descent certificate and no accelerated certificate with symbolic run lengths exists, at any modulus | exact witnesses in `accel/check_trichotomy.py`, `traps/verify.py` |

The third row is a statement about what a class of proofs cannot do; it does
not say the systems are undecidable or false. Every open GLOBAL table map in
the census is in the third row (`dichotomy/neighbours.md`,
`accel/trichotomy.md` "Catalog"). In the family "3n+1 on a set S of odd
classes mod 2^m, else n+1" no member with m <= 5 is in the second row, so all
48,880 + 172 + 10 + 2 members without a descent certificate are behind the
same barrier.

Where the barrier does not apply is mixed-base maps, whose multipliers are not
units (Farkas-type maps that divide by 3 inside a 2-adic system). There
`mixedbase/` settles systems that provably have no plain descent certificate,
using run-accelerated certificates, and finds the first cases that resist
those too.

Cross-lens checks made while assembling this file:

* `deep/` and `density/` computed the split5_3 exponent independently
  (Hausdorff dimension 0.5806841; counting exponent 0.58069); likewise
  split5_1 (interval [0.936275, 0.936852]; 0.93685).
* `deep/`, `domains/` and `progressions/` each derived the invariant of the
  split_d family (the class of n mod d under multiplication by 2 and 3); they
  agree. Consequences: split_5, 73, 97, splitB_7, 71 have congruence basin
  rules; in split_13 (cycles 1, 5) and split_7081 (cycles 569, 713) two cycles
  share a class and their basins are automatic in no base.
* `mixedbase/` left "div23_5n1 plus n = 2 mod 4 -> (n+2)/4" unresolved (no
  certificate, no obstruction). `dichotomy/decide.py` resolves the certificate
  question: the residue cycle 1 -> 6 -> 5 -> 2 mod 12 has multiplier 25/16,
  and on n = 16381 mod 49152 one has T^4(n) = (25n+27)/16 > n (checked
  exactly). So no descent certificate exists. The reason `mixedbase` missed it
  is that the cycle has no periodic point 3-adically; the dichotomy proof does
  not need one. The system itself stays open.

## What each lens produced

| Folder | New settled systems | Theory | Still open there |
|---|---|---|---|
| `traps` | 6 named trap systems for 3x+1, 5x+1, 7x+1; two uniform families (every orbit of n/2, an+b meets 4 mod 8); 490 minimal provable trap sets mod 8, 16, 32 (some mod-8 ones already in Yolcu-Aaronson-Heule) | decision procedure for trap statements; O(X^theta) avoider counts | 130 maximal unprovable sets, including the YAH prize cases and F* = {0,3,5,7,8,10,13,14,15} mod 16 |
| `dichotomy` | 17 named systems (certificate depth up to 2466; previous record 44), one all-divergent table, 1330 provable neighbours of open entries | certificate exists iff all residue cycles contract, for mixed moduli too; "distance to provability" | all 36 open table maps have no descent certificate |
| `accel` | 5 systems with an expanding 2-adic or 3-adic cycle (`acc_h32`, `acc_h16` need the machine proof; three are easy) | Theorems H, N, T, K above | 8 new 3x+1-type cores; 4 of the 12 small obstructed systems are 3x+1 itself (exact conjugacy T_S^2(2z+1) = 2T(z)+1) |
| `mixedbase` | 20 Farkas-type systems for 3x+1, 5x+1, 7x+1 expansion, down to taming density 7/729; three provable relatives of div23_5n1 and one of m3_b | mixed-radix certificate engine; pairing family closed form; complete single-class classification | n = 26 mod 27 -> (n+1)/27 on top of 3x+1 (blocked by the cycle -5, -7, -10) |
| `polynomial` | 13 systems and 3 infinite families over F_2, F_3, F_4, most with a provably divergent orbit | Theorems A, B, C; Frobenius renormalization certificates | g = 1+t+t^2, h = 1 over F_2 (Nichols) |
| `domains` | every settled catalog map extended to all of Z; Gaussian, Eisenstein, Z[sqrt 2], Z[sqrt -2] systems with complete cycle lists | cycle formula for the whole split family; Legendre-symbol basin rules for split_73, 97, splitB_71 | Gaussian 5x+1 |
| `divergence` | 6 systems with a provably infinite non-monotone orbit, including 5x+1 changed on one class mod 64 and a new two-swap neighbour of the 1932 map | decidability for suffix maps; precision lemmas that exclude congruence certificates at every modulus | swT9 (CLS-055): no congruence separator at 2^i 3^j, i <= 18 |
| `density` | none (by design) | one moment method with exact certificates; exponents for every contracting open entry; for 5x+1, 7x+1, 9x+1 the exact density of starts that drop early (0.8238, 0.6992, 0.6139) | all GLOBAL questions |
| `deep` | split family table (128 members: 8 by descent, 16 divergent, 16 conjugate to parity maps, 48 open); basins of 1x+d and split_d | exact dimension of the non-descending set for every split map | split5_3, split5_1; the rising family 5^K - 3 |
| `progressions` | 15 basin questions answered (m3_a and desc_s32_d65 completely; for 5x+1, 3x-1, 3x+5, 3x+13, 3x+17, 5x+3, 5x+7, 5x+11, split5_1, m3_d, m3_e, m3_g, desc_m3_4n5: basins of known cycles are automatic in no base) | Theorem A: every merging class meets every progression allowed by an explicit computable invariant (3x+1 case is Monks 2006); Theorem B: complete list of automatic orbit-invariant labels; Theorem C: each merging class has at least X^sigma members in every allowed progression (split5_3: 0.42, was 0.238); 1932 map: only Z and 1 mod 2 are sufficient | whether the accessibility hypothesis (IA) can be dropped; no system settled by "sufficiency plus descent on one progression" |

`../round3_results.json` holds every prover claim and referee verdict.

## Second reading

After the agents finished, the proofs of the three hardest lenses were read
again line by line outside the prover/referee loop: `accel` Theorems H and N,
`deep` Theorems B1 to B4 and Omega-1, and `progressions` Theorem A and the
repaired Theorem C. They hold as written, with one addition: Theorem C needed
the hypothesis that the invariant is state-free, which is true for all 32
certified systems and is now stated and checked. Second attempts at the
recorded blocking points (core K7 in `accel`, the 26 mod 27 system in
`mixedbase`) ran into the same free re-entry obstruction and produced nothing
new.

## Reproducing

Each folder has `check*.py` scripts (prover) and `referee*_check.py` scripts
(referee); all exit 0. Most run in under a minute. `density/check_density.py`
takes about three minutes and `dichotomy/referee_b27.py` about four.
