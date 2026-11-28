# Referee 1 report: round 4, lens "transport"

Scope: `README.md` and `transport_theorems.md` in this folder, plus the code and result files they
cite. Context documents: `round3/README.md` and `round3/accel/trichotomy.md`. I did not edit any
of the prover's files and I made no commits.

My own check is `referee1_check.py`. It was written from scratch, uses exact int and Fraction
arithmetic, and does not import `transport_lib`, `equiv`, `check_transport` or `decide`. It reads
`library.py` only for the table data. It includes negative controls that must be rejected, and
it exits 1 on any failure.

* `python3 referee1_check.py`: about 3 s. `--big` raises the brute-force bounds and takes about 7 s. Both exit 0.
* The prover's `python3 check_transport.py` exits 0: "ALL CHECKS PASSED", 4857 join members, about 3 s.

## Headline

The round's hard criterion was to settle a unit type-(c) system with a convergence proof. **The
lens does not claim to meet it, and it does not meet it.** The README says so in its first lines,
and I agree. No system in this folder is claimed to be settled, so there is no cycle list to make
complete.

The positive results are these:

* two exact identities, Proposition C and Theorem F, that link open systems to 3x+1;
* a family of equivalence joins inside the S-family;
* two barrier theorems, O1 and O2, which say that bounded-return transport cannot start from a
  certificate-settled system and cannot cross p-adic classes out of a Theorem-H system.

I re-derived every proof by hand. I re-proved every recorded join with an independent engine and an
independent Lemma S checker. I found no mathematical error. Some labels and wordings claim more than
is proved; those are listed below.

## Verdicts

| # | claim | verdict |
|---|---|---|
| 1 | Lemma P (pieces) | CONFIRMED |
| 2 | Theorem E (transport of eventual periodicity, GLOBAL, cycles) | CONFIRMED |
| 3 | Lemma S (sufficient classes) | CONFIRMED (nit) |
| 4 | Proposition C (normal form G, G′ of 3x+1) | CONFIRMED_WITH_FIX |
| 5 | Theorem F (4 S-family sets are exactly 3x+1) | CONFIRMED |
| 6 | S-family equivalence classes (42 classes, 264 members, Collatz class of 20) | CONFIRMED_WITH_FIX |
| 7 | 8 cores pairwise not joined (43 bounded returns) | CONFIRMED_WITH_FIX |
| 8 | Lemma B, Lemma R | CONFIRMED |
| 9 | Theorem O1 | CONFIRMED as stated in transport_theorems.md; README row CONFIRMED_WITH_FIX |
| 10 | Theorem O2 | CONFIRMED_WITH_FIX |
| 11 | Non-unit search (EVIDENCE) | CONFIRMED_WITH_FIX |
| 12 | "Hard criterion not met", open door, honest limits | CONFIRMED |
| 13 | Labels and novelty statements | CONFIRMED_WITH_FIX (see 4, 6, 7, 9, 11) |

## Details

### 1. Lemma P
The branch of T is constant on the class n ≡ c (mod Mod) under F(n) = (an+b)/d iff Q divides
a·Mod/d. Membership in X is constant iff M_X divides it. Every piece is a residue class containing
infinitely many positive integers, so a bound on the return time over the positive part of X also
bounds the return time of every piece. CONFIRMED.

### 2. Theorem E
(1) and (2) hold: the A-orbit is the R_A-orbit with gaps of at most τ_max. For D_Y = D_X ∪ {0}, the
value G(0) is the z-value of a positive integer, so it is 0 or lies in D_X.

(3) holds in both the two-way and the one-way form. Lemma S on the B side alone gives
GLOBAL(A) ⇒ (all A-orbits from X) ⇒ (all B-orbits from Y) ⇒ GLOBAL(B).

(4) holds: the lap multiplier of R is the product over the whole cycle, and conjugating by an affine
map keeps the slope.

I checked (4) on Prop C. The Collatz cycle (4 2 1) has multiplier 3/4, and the G′ fixed point y = 1
uses the branch (3y+1)/4, which also has multiplier 3/4 (R6). CONFIRMED.

### 3. Lemma S
The proof is correct. A cycle of Γ carries the edge relation y ≡ T(x) (mod gcd(uM/w, M)), which
holds for every member of the class. A component made only of the dilation branch cannot hold a
positive orbit forever. In a contracting component, the potential gives V(Tn) ≤ θV(n) + β. The
merge step T^j(d^j c) = c uses only T(dn) = n.

I wrote my own implementation. It certifies a contracting component exactly by giving rational
potentials and a rational θ < 1, checked edge by edge. It agrees with `transport_lib.sufficient` on
every recorded join, 4857 members (R10).

It also rejects the two negative controls: (3x+1, X = 1 mod 4) and (3x+1, X = 0 mod 3). Both leave
an expanding loop outside the set G, and both are rejected.

A side note from one of my own first controls. (3x+1, X = 3 mod 4) is **accepted**, and that is
correct: outside 3 mod 4, every odd step is followed by at least two halvings.

Nit: the docstring of `transport_lib.sufficient` still says the restricted graph must be "acyclic".
The code implements the full Lemma S, with dilation and contracting components.

### 4. Proposition C
I re-derived all three branches with their residues mod 3, and the conjugation y = z+1 that gives
G′:

* z odd: 2 steps, result (3z+1)/2.
* z ≡ 0 (mod 4): 3 steps, result 3z/4.
* z ≡ 2 (mod 4): 3 steps, result (z−2)/4.

My checks agree:

* the own symbolic engine proves the identity, with maximum return time 3 (R1);
* brute force agrees for z < 4·10^5 (R2);
* the own Lemma S finds G = {1, 2} mod 3 and no contracting component; the only remaining component
  is the halving loop on 0 mod 3 (R3);
* G and G′ are unit 2-adic and of type (c) (R4).

**Fix.** The text says "every C-cycle meets 2 (mod 3), by Lemma S below and bounded return". That
does not follow. Lemma S gives a point c with c mod 3 ∈ G = {1, 2}, and G ≠ X. For c ≡ 1 (mod 3)
it only says that 2^j c ∈ X, and 2^j c need not lie on the cycle.

The statement is still true, for a direct reason. If n ≡ 1 (mod 3) and n is even, then
n/2 ≡ 2 (mod 3). If n is odd, then 3n+1 ≡ 4 (mod 6), so (3n+1)/2 ≡ 2 (mod 3). So every orbit
through 1 mod 3 reaches 2 mod 3 within two steps. Replace the cited reason with this one.

Nit: the text says G′ has a "cycle of multiplier 9/8 in a 4-node component". Such a cycle exists
(2 → 1 → 2). However, `unit_type` reports the self-loop 0 → 0, with multiplier 3/2, and my check
finds that loop as well. Both are correct; say "e.g." or quote the loop.

The heuristic sentence "which is exactly why it stays a Collatz-hard map" is interpretation, not a
proved statement. Mark it as a remark.

### 5. Theorem F
I re-derived the three cases. They take 2+2, 4 and 4 steps. The hypotheses 11 ∉ S and
5, 13 ∉ S are each used.

My checks:

* The own engine proves the identity for all four sets (maximum return time 4). It rejects five
  sets outside the hypotheses as controls (R1).
* Brute force agrees for z < 4·10^5 (R2).
* The own Lemma S finds the contracting component {1, 2}, or {1, 2, 4} when 1 ∈ S (R3).
* All four tables are of type (c), with the expanding cycle 3 → 10 → 13 → 14 → 7 → 6 of
  multiplier 9/8 inside a 10-node SCC, and they have no division-free cycle (R4).

**Cycle list, brute force over all starts n ≤ 10^6 (R5, `--big`).** The cycles are exactly
(1 2) or (1 4 2), and (3 10 5 6). Every orbit that avoids 3 mod 4 ends in (1 2) or (1 4 2).
(3 10 5 6) is the image of the Collatz cycle through n = 2 (z = 0).

"Exactly those ending in (1 2)/(1 4 2)" is also correct as a theorem. Once an orbit is in X, the
bounded return keeps it in X forever. CONFIRMED.

These are genuinely type-(c) systems, not disguised easy ones. However, they are settled only up to
3x+1, and the document labels them that way correctly: "PROVED (equivalence; GLOBAL OPEN)".

### 6. S-family equivalence classes
All 4857 join members in `equiv_{lib,sfam4,sfam5}.json` were re-proved with my own engine and my
own Lemma S (R10). The Collatz class has the claimed 20 members. Each of them, taken on its own, has
a **direct** identity with G and Lemma S on a single class (R7):

* 3 mod 4 for the S-family members;
* 2 mod 3, 6 mod 9 and 18 mod 27 for par_3_1, par_3_3 and par_3_9;
* 5 mod 6 for sf3_37.

The counts in the table (83 / 328 / 65607 distinct tables, 3 / 3 / 42 classes, 8 / 12 / 264
members) match the result files.

**Fixes.**

(a) The counts are "exact for the searched transport class". That class is also cut off by the
search parameters `tmax = 24`, `pmax = 20000` and `Lmax = 4096` in `equiv.py`. State these
parameters in §2 and in "Honest limits".

(b) "No class mixes a CERT member with an OBST member, and no class contains a settled system of
any kind. This is forced by the theorems below." This is overstated.

* O1 forces it for CERT and other plain-certificate systems.
* O2 forces it for Theorem-H systems through p-adic classes only. The search set FULL includes
  classes mod 3, 5, 6, 7, 9, … for the 2-adic Theorem-H systems acc_h16 and acc_h32, and for these
  O2 says nothing. The document itself lists this case as OPEN in §5.
* Nothing in §3 excludes joins with the dressed, mixed or divergent library systems.

For those cases the statement is an observed outcome of the search, not a consequence of the
theorems. Reword it as "forced by O1 for certificate systems and by O2 for p-adic classes of
Theorem-H systems; observed for the rest".

### 7. The 8 cores
The pairwise distinctness is confirmed. With my own engine I get 43 bounded canonical first returns,
counting the 9 maps themselves (M = 1), and no collision. I get the same 43 and no collision when I
raise the time bound from the prover's 24 to 64 and the piece cap to 60000 (R8).

**Fix.** "Only 43 of their first returns on classes M ≤ 32 are bounded" really means that the
return comes within 24 steps. A return that is undetected by the cutoff is not excluded by the
computation. Say "return within 24 steps (no further ones up to 64)". The "PROVED (finite)" label
then applies to that stated class.

### 8. Lemma B and Lemma R
Lemma B: B(x) ≤ (Λ+K)x for x ≥ 1. Every descent chain is bounded by (Λ+K)^J times its start, and
every start is at most max(n, ΛN₀+K). Correct.

Lemma R: the Markov property (M) of the unit table realises the walk P C^d on a cylinder, and the
CRT combines that cylinder with the class mod q. Correct. The prover's part D/E checks growth
witnesses for d ≤ 8 on all 42 open unit systems.

Lemma R also applies to type-(b) systems, which are OBST but settled by Theorem H. That is
consistent with O1: such a system can't be transported to or from a CERT system either.

### 9. Theorem O1
I re-derived the proof. In it, "time of maximum" is best replaced by the time |P| + d|C| itself,
because the orbit could be unbounded. That change only helps the argument. With h = h_X ∘ h_Y^{-1}
(so α = M_X/M_Y > 0), every identity of Theorem E fits the window hypothesis with L = τ_max.
CONFIRMED, as stated in `transport_theorems.md`, where A, X are taken as in Lemma R.

On the user's point of interest: the consequence for **dch_C27_2466**, the 2466-step certificate
system, holds. It is a unit 3-adic table: 3 | n → n/3, and the other classes use multipliers 1, 2,
4 and 5. It has a plain certificate. By Lemma B its orbits are linearly bounded, so it can't be a
transport source for any table with realised growth.

The Lemma B constant (Λ+K)^2466 is astronomically loose. The Lyapunov function of
`round3/dichotomy/dch_C27_2466.md` gives a far better linear bound, but the qualitative conclusion
is the same.

**Fix (README row).** The README writes "if A is OBST (e.g. type (c))". The theorem needs A to be a
**unit p-adic** table with an expanding cycle reachable from X (Lemma R), and that hypothesis is used
in an essential way. Non-unit OBST systems, such as the dressed maps of `accel/dressing.md`, need
not realise growth along their expanding p-adic point. Copy the precise hypothesis into the README.

### 10. Theorem O2
I re-derived the proof:

* The return pieces are p-adic cylinders, so the identity extends to Z_p.
* The C^d W periodic points in X̄ have slope λ_C^d λ_W > 1.
* The conjugation carries R̂_A-periodic points to R̂_B-periodic points with the same slope.
* Distinct R̂_A-orbits give distinct B̂-orbits.
* Type (a) and type (b) components carry only finitely many expanding periodic orbits.

**Fix.** The conclusion "hence B is of type (c)" needs the standing hypothesis for B, namely no
division-free cycle. The proof says so in a parenthesis ("otherwise B is OBST by a translation cycle
anyway"), but in that case B is "critical", not of type (c). Put the hypothesis into the statement,
or conclude "B is of type (c) or critical; in either case it is not settled by Theorem H or by a
generalized certificate".

### 11. Non-unit search (EVIDENCE)
My own engine, run on the prover's population, gives 31 bounded first returns at M_Y ≤ 144, with
tmax = 30 and a piece cap of 4000. All 31 are on classes 0 (mod M_Y), and none of them is a unit
p-adic table. This matches `results/nonunit_144.json`.

**Fix.** The text says "all of them the scaling symmetries x*Z (P2 of pairing_family.md)". That
holds for the 24 returns of the pairing systems. The other 7 are dressed systems returning to qZ;
these are still non-unit tables mod Q, but they are not P2 symmetries. Also, `check_transport.py`
part G re-runs only M ≤ 48. The 144 figure is a stored result, which the EVIDENCE label covers, but
the README should say which bound the check reproduces.

### 12. Hard criterion, open door, honest limits
The statements are accurate and do not overclaim. One point is right and I re-confirm it: fx10_64
and fx26_32 are unit type-(c) systems with proved divergent orbits. So type (c) blocks only proofs
of eventual periodicity, not proofs of divergence.

The "open door" (unbounded first returns of pairing or dressed systems) is correctly identified as
not covered by O1 or O2.

### Sanity: would the method prove something false or famous?
* Transport toward 3x+1 itself: among all classes 2 ≤ M ≤ 48, 3x+1 has only 4 bounded first
  returns. All 4 are unit 2-adic tables of type (c), and none is of type (a) or (b), which would
  "prove" Collatz (R9). This agrees with O1 and O2.
* The identity verifier rejects a perturbed G and rejects 5x+1 on 3 mod 4 (R9).
* Lemma S rejects the two expanding-outside cases (R3).
* No join involves a divergent system together with a system that has a proof of GLOBAL.

Nothing in the folder proves a false or famous statement.

### 13. Labels and novelty
"Novelty: not checked" is stated throughout, which is honest. Reformulations like Proposition C (3x+1
restricted to 2 mod 3) are classical in spirit, so a novelty claim would have needed a search; none
is made.

The PROVED, EVIDENCE and OPEN labels are correct, apart from the overstatements in items 4, 6(b), 7,
9 (README) and 11.

## Repair list (text only; no mathematics changes)
1. Prop C: replace "by Lemma S and bounded return" with the two-step argument for n ≡ 1 (mod 3).
   Fix the 9/8 versus 3/2 wording. Mark the "exactly why" sentence as a remark.
2. §2: state tmax = 24, pmax = 20000 and Lmax = 4096. Replace "forced by the theorems" with the
   precise split between O1, O2 and observation.
3. 8 cores: say "return within 24 steps (still 43 at 64, referee)".
4. README O1 row: replace "A is OBST" with "A unit p-adic with an expanding cycle reachable from X".
5. O2: add the standing hypothesis for B to the statement, or weaken the conclusion to "type (c) or
   critical".
6. Non-unit search: 24 pairing scaling symmetries plus 7 dressed returns to qZ. Say that the check
   reproduces M ≤ 48 and that 144 is a stored result.
7. Nit: update the stale docstring of `transport_lib.sufficient`.
