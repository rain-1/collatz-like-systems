# The split family SPLIT(a,b,d): a complete classification

**Map.** For odd positive integers a, b and d,

    SPLIT(a,b,d):  n even -> n/2;   n = 1 (mod 4) -> a n + d;   n = 3 (mod 4) -> b n + d.

Catalog members: split_d = SPLIT(3,1,d), splitB_d = SPLIT(1,3,d), split5_1 = SPLIT(5,1,1),
split5_3 = SPLIT(5,1,3), and the parity maps par_c_d = SPLIT(c,c,d).

**Question.** For each member: GLOBAL (is every positive orbit eventually periodic, and what are the
cycles?) or, where GLOBAL cannot be settled, the exact status (equivalent to a named problem,
provably divergent, or open).

**Answer.** Every member falls into exactly one of six classes, decided by the exact
congruence data (a mod 4, b mod 4, d mod 4), two size comparisons and, for classes R and O,
gcd(d, a) and gcd(d, b). The conditions are applied in the order listed, which is why each member
lies in exactly one class:

| class | condition | status | what is proved |
|---|---|---|---|
| P | a = b | catalog parity map an+d | not new |
| C | not P, and a < 2^{v_a}, b < 2^{v_b} | **GLOBAL yes**, every cycle meets [1,d] | lemmas.md Thm 1 (cited) plus Lemma C below |
| D | v_a = v_b = 1, min(a,b) >= 3 | **GLOBAL no: every orbit diverges, no cycles** | Theorem D (new, elementary) |
| K | v_a = v_b = 1, min(a,b) = 1 | **exactly conjugate to the accelerated parity map cx + d(c-1)/2**, c = max(a,b) | Theorem K (new) |
| R | not P,C,D,K; some e = gcd(d, a) > 1 with b-branch contracting (or a <-> b) | GLOBAL(T) <=> GLOBAL of a smaller-d member | Lemma R (new) |
| O | everything else | OPEN (Collatz-type) | drift sign, cycles found (EVIDENCE) |

Here v_a = 2 if a + d = 0 (mod 4) and v_a = 1 otherwise; v_b = 2 if 3b + d = 0 (mod 4) and
v_b = 1 otherwise.

Status: Theorems D, K and Lemmas C, R, S are **PROVED** (check: `check_family.py`). The O class is
OPEN; the drift figures are heuristics.

Novelty: Theorem D and Lemmas C, R, S are elementary and very likely folklore. Theorem K (the exact
conjugacy of SPLIT(1,3,1) with the 3x+1 map, and the general version) is new to this repository;
novelty in the literature not checked.

## Basic lemmas

**Lemma V (valuations).** Let n be odd. If n = 1 (mod 4) then a n + d = a + d (mod 4), so
2^{v_a} divides a n + d, and if v_a = 1 then v_2(a n + d) = 1 exactly, so (a n + d)/2 is odd.
The same holds for n = 3 (mod 4) with b n + d = 3b + d (mod 4) and v_b.

*Proof.* n = 1 + 4t gives a n + d = a + d + 4at; n = 3 + 4t gives b n + d = 3b + d + 4bt. ∎

Write S for the odd-to-odd map: S(n) is the first odd value after n on the orbit of an odd n.

**Lemma C (class C).** If a < 2^{v_a} and b < 2^{v_b}, then for every odd n > d the value S(n)
is less than n, and S maps the odd numbers of [1, d] into [1, d]. Hence every orbit enters [1, d]
and is eventually periodic, and every cycle has its minimum in [1, d].

*Proof.* In class C the pair (a, b) is (1,1), or (3,1) with d = 1 (mod 4), or (1,3) with
d = 3 (mod 4): indeed a < 2^{v_a} forces a = 1, or a = 3 with v_a = 2; similarly for b; and
(3,3) would need d = 1 and d = 3 (mod 4) at once. By Lemma V, S(n) <= (3n + d)/4 when a 3-branch
is used (it has v = 2) and S(n) <= (n + d)/2 for a 1-branch. Both are < n for n > d and <= d for
n <= d. A cycle's minimum is odd (an even value has the smaller value n/2 after it), so it lies in
[1, d]. ∎

This is the content of lemmas.md Theorem 1 (certificate <=> a < 2^{v_a} and b < 2^{v_b}); the
converse direction there (Lemma B obstruction) shows that no finite descent certificate exists
in all other classes.

**Lemma S (scaling).** Let e be odd and e | d. Then eZ is forward invariant, and on it
n = e m conjugates T to SPLIT(a, b, d/e) if e = 1 (mod 4) and to SPLIT(b, a, d/e) if
e = 3 (mod 4).

*Proof.* Halving and n -> c n + d preserve divisibility by the odd number e. For n = e m,
n = 1 (mod 4) iff m = e^{-1} = e (mod 4), and c e m + d = e (c m + d/e). ∎

**Lemma R (reduction).** Suppose e = gcd(d, a) > 1 and b < 2^{v_b}. Then every orbit of
T = SPLIT(a,b,d) either enters eZ or is eventually periodic. Hence GLOBAL(T) holds iff it holds for
SPLIT(a, b, d/e) (e = 1 mod 4) or SPLIT(b, a, d/e) (e = 3 mod 4), and the cycles of T are those of
the scaled member times e, together with the finitely many cycles avoiding eZ. The same holds with
the roles of a and b exchanged.

*Proof.* An a-step produces a n + d, a multiple of e. An orbit that never enters eZ therefore takes
only b-steps at odd values; by Lemma V each odd value n is followed by an odd value at most
(b n + d)/2^{v_b}, which is < n for n > d/(2^{v_b} - b). So the orbit is eventually bounded,
hence eventually periodic. Apply Lemma S. ∎

## Theorem D (provably divergent members)

**Theorem D.** If a + d = 2 and 3b + d = 2 (mod 4) (equivalently a + b = 0 and d = 2 - a
(mod 4)) and a, b >= 3, then every positive orbit of SPLIT(a,b,d) is unbounded and has no repeated
value. There are no cycles. GLOBAL fails at every start.

*Proof.* By Lemma V, for odd n, S(n) = (c n + d)/2 with c in {a, b}, and it is odd. Then
S(n) >= (3n + 1)/2 > n. Every orbit reaches an odd value after finitely many halvings and from then
on its odd values strictly increase, so it is unbounded and never repeats. ∎

In the table range (a, b <= 7, d <= 15) this covers the 16 members with {a,b} = {3,5} or {5,7}
and d = 2 - a (mod 4), e.g. SPLIT(3,5,3), SPLIT(5,3,1), SPLIT(5,7,1), SPLIT(7,5,3). Tier 1, easy.

## Theorem K (exact conjugacy with an accelerated parity map)

**Theorem K.** Suppose a + d = 2 and 3b + d = 2 (mod 4) and min(a, b) = 1; put c = max(a, b)
(then c = 3 mod 4). Define on odd n

    phi(n) = (n - d)/2,

a bijection from the odd positive integers onto the integers x >= (1-d)/2. Then

    phi(S(n)) = P_c(phi(n)),   P_c(x) = x/2 (x even),  (c x + d(c-1)/2)/2 (x odd),

and every step of S is exactly two steps of T. Consequently T is eventually periodic at n iff P_c
is eventually periodic at phi(n'), n' the first odd value of the orbit; T-cycles correspond
bijectively to P_c-cycles inside {x >= (1-d)/2}, with twice the length.

*Proof.* Case a = 1 (so c = b and d = 1 mod 4). For n = 1 (mod 4), n - d = 0 (mod 4), so
x = phi(n) is even, S(n) = (n + d)/2 and phi(S(n)) = (n - d)/4 = x/2. For n = 3 (mod 4),
n - d = 2 (mod 4), so x is odd; S(n) = (c n + d)/2 and, with n = 2x + d,
phi(S(n)) = (c n - d)/4 = (2cx + cd - d)/4 = (c x + d(c-1)/2)/2.
Case b = 1 (so c = a and d = 3 mod 4) is identical with the residues 1 and 3 exchanged.
By Lemma V both odd branches are followed by exactly one halving and an odd value. ∎

**Corollaries (exact equivalences).**

* SPLIT(1,3,1) is conjugate on odd values to the Collatz map C(x) = x/2, (3x+1)/2 on x >= 0
  (x = (n-1)/2). GLOBAL(SPLIT(1,3,1)) is **equivalent to the statement that no Collatz trajectory
  diverges** (P1 in lhf/collatz3), and the cycles of SPLIT(1,3,1) other than those through 1 and 3
  correspond exactly to nontrivial Collatz cycles.
* SPLIT(3,1,3) (the "split_3" sibling of split_5 and split5_3) is conjugate to the 3x+3 map
  x -> x/2, (3x+3)/2 on x >= -1. By lhf/collatz3/CLS-014, GLOBAL(3n+3) <=> P1. So
  **GLOBAL(split_3) <=> P1**: replacing d = 5 by d = 3 in the settled split_5 already gives a
  problem exactly as hard as the Collatz no-divergence conjecture.
* In general SPLIT(1,3,d) (d = 1 mod 4) and SPLIT(3,1,d) (d = 3 mod 4) are conjugate to the
  accelerated 3x+d map on x >= (1-d)/2; GLOBAL is equivalent to GLOBAL(par_3_d) (the finitely
  many x <= 0 stay in a finite set or rise into the positive range, which is checked for the table
  members). lhf/collatz3 reduces these further to P1 plus rational versions Q_e.
* SPLIT(1,7,d) (d = 1 mod 4) and SPLIT(7,1,d) (d = 3 mod 4) are conjugate to the accelerated
  7x + 3d map. These are expected divergent (drift +0.280 per bit) and open, like 7x+1.

Class K members in the table: (1,3,d) and (1,7,d) for d = 1 (mod 4); (3,1,d) and (7,1,d) for
d = 3 (mod 4): 16 members.

## Class O: what is left, and the heuristic

For the remaining 48 table members (after applying Lemma R to 8 more), the descent method is
provably blocked (lemmas.md Lemma B: an expanding 2-adic fixed point of the branch with
a > 2^{v_a} or b > 2^{v_b}), and none of the reductions above applies. In the U/O binary coding
(split5_3_deep.md, section 3) digits are fair coin flips and the mean log-slope per digit is

    drift = pi_U (1/2) log(1/2) + pi_O (1/2) (log(a/2^{v_a}) + log(b/2^{v_b})),

with pi_O the stationary probability of the 'odd' state. Negative drift: convergence expected;
positive drift: divergence of almost all orbits expected. Both are EVIDENCE only.

| (a,b) | v pattern | drift | members (d <= 15) | cycles found (min:length), starts <= 3000 |
|---|---|---|---|---|
| (5,1) | (2,1), d=3 mod 4 | -0.291 | d = 3, 7, 11 (and 15 -> R) | d=3: split5_3, 1:4 3:2 5:5 61:10 125:11; d=7: 1:11 7:2 9:7 25:8 |
| (5,1) | (1,2), d=1 mod 4 | -0.291 | d = 1, 9, 13 (5 -> R) | d=1: split5_1, 1:5 13:35 |
| (1,5) | both patterns | -0.291 | d = 1,3,7,9,11,13 | d=1: 1:2 only; d=3: 1:3 3:5 39:35 47:11 79:12 103:12 |
| (7,1) | (2,2), d=1 mod 4 | -0.369 | d = 1, 5, 9, 13 | d=1: 1:4 only; d=5: 1:7 5:4 9:9 |
| (1,7) | (2,2), d=3 mod 4 | -0.369 | d = 3, 11, 15 (7 -> R) | d=3: 1:3 3:4 |
| (3,5),(5,3) | (2,2) | -0.242 | (3,5,d), d=1 mod 4; (5,3,d), d=3 mod 4 | (5,3,3): 1:4 3:3 21:6 61:10 |
| (5,7),(7,5) | (2,2) | -0.101 | (5,7,d), d=3 mod 4; (7,5,d), d=1 mod 4 | (5,7,3): 1:4 3:4 5:18 61:10 181:68 |
| (3,7),(7,3) | mixed | +0.068 | all d | (3,7,1): 1:3 19:23 23:9 31:9 and about 20% of starts <= 3000 exceed 10^40 |

For O members with a prime p | d, p not dividing ab, divisibility by p is invariant in both
directions, and by Lemma S the subsystem on pZ is a smaller-d member. Example used in
split5_3_deep.md: on 3Z, split5_3 = SPLIT(5,1,3) is conjugate to SPLIT(1,5,1), so
GLOBAL(split5_3) implies GLOBAL(SPLIT(1,5,1)).

## Full table (a, b <= 7, d <= 15 odd; 128 members)

Rows (a,b), columns d = 1, 3, ..., 15. "R->(x,y,z)" gives the smaller member it reduces to (itself O).

| a b | 1 | 3 | 5 | 7 | 9 | 11 | 13 | 15 |
|---|---|---|---|---|---|---|---|---|
| 1 1 | P | P | P | P | P | P | P | P |
| 1 3 | K | C | K | C | K | C | K | C |
| 1 5 | O | O | R->(1,5,1) | O | O | O | O | R->(1,5,3) |
| 1 7 | K | O | K | R->(7,1,1) | K | O | K | O |
| 3 1 | C | K | C | K | C | K | C | K |
| 3 3 | P | P | P | P | P | P | P | P |
| 3 5 | O | D | R->(3,5,1) | D | O | D | O | D |
| 3 7 | O | O | O | O | O | O | O | O |
| 5 1 | O | O | R->(5,1,1) | O | O | O | O | R->(5,1,3) |
| 5 3 | D | O | D | O | D | O | D | R->(5,3,3) |
| 5 5 | P | P | P | P | P | P | P | P |
| 5 7 | D | O | D | O | D | O | D | O |
| 7 1 | O | K | O | K | O | K | O | K |
| 7 3 | O | O | O | R->(3,7,1) | O | O | O | O |
| 7 5 | O | D | O | D | O | D | O | D |
| 7 7 | P | P | P | P | P | P | P | P |

Counts: P 32, C 8, K 16, D 16, R 8, O 48. The table is produced by `family_lib.py` and verified
by `check_family.py`.

## Where "5 instead of 3" breaks the proof

The settled sibling split_5 = SPLIT(3,1,5) is in class C because 3 + 5 = 0 (mod 4) gives
v_a = 2 and 3 < 4. split5_3 = SPLIT(5,1,3) has v_a = 2 as well, but 5 > 4. That single inequality
is exactly the dividing line of lemmas.md Theorem 1, and beyond it no finite descent certificate
exists (the 2-adic point -3 is fixed by the block n -> (5n+3)/4 with multiplier 5/4). The
comparison inside the column d = 3 is sharper:

| member | class | status |
|---|---|---|
| SPLIT(1,1,3) | P / C | GLOBAL yes (descent) |
| SPLIT(3,1,3) = split_3 | K | GLOBAL <=> P1 (Collatz no-divergence), Theorem K |
| SPLIT(5,1,3) = split5_3 | O | open; see split5_3_deep.md |
| SPLIT(7,1,3) | K | conjugate to the accelerated 7x+9 map; expected divergent |

So in the d = 3 column the multiplier 3 is already exactly the Collatz problem; the multiplier 5
gives a problem not known to be equivalent to any parity map, with a much thinner exceptional set
than 3x+1-type problems (split5_3_deep.md).
