# Census of trap sets for 3x+1, 5x+1 and 7x+1 (Corollary 5 applied exhaustively)

Status: **PROVED**, for every set in every census below. Each set is classified as either:

* **provable** (P0 or P1): a certificate is produced, and every *minimal* provable set's
  certificate is re-verified independently by verify.py; or
* **H**: a Theorem-4 homoclinic witness is produced and verified exactly.

By Corollary 5 these two cases are exhaustive, so **no set is left undecided**. `check.py` [2]
reproduces every census and also checks two things:

* minimality: removing any element of a minimal provable set gives H, with a verified witness;
* maximality: adding any residue to a maximal H set gives a provable set.

The maps are C_a(n) = n/2 (n even), a n + 1 (n odd). "Provable" for A means S(C_a, A): every
positive orbit meets A or ends in one of the listed cycles, and the cycle list comes with the
certificate. "H" means that no Theorem-2 SCC certificate and no avoider descent certificate
exists at any modulus 2^m. It does **not** mean that S(C_a, A) is false, and it does not exclude
other residue-based methods (for example YAH's rewriting/SAT encodings, non-power-of-2 moduli,
or potentials not of the form n·2^{φ(r)/Q}).

## Summary

| map | k | universe | subsets | provable | H | minimal provable | maximal H (frontier) | sizes of minimal provable |
|---|---|---|---|---|---|---|---|---|
| 3x+1 | 3 | all | 256 | 247 | 9 | 7 | 2 | 1–2 |
| 3x+1 | 4 | all | 65536 | 64405 | 1131 | 47 | 8 | 1–4 |
| 3x+1 | 5 | odd | 65536 | 41805 | 23731 | 76 | 35 | 3–7 |
| 5x+1 | 3 | all | 256 | 240 | 16 | 10 | 3 | 1–2 |
| 5x+1 | 4 | all | 65536 | 62752 | 2784 | 73 | 10 | 2–4 |
| 5x+1 | 5 | odd | 65536 | 20688 | 44848 | 115 | 36 | 5–8 |
| 7x+1 | 3 | all | 256 | 240 | 16 | 10 | 3 | 1–2 |
| 7x+1 | 4 | all | 65536 | 62602 | 2934 | 63 | 8 | 2–4 |
| 7x+1 | 5 | odd | 65536 | 15434 | 50102 | 89 | 25 | 5–8 |

Full lists are in `results/census_*.json`: minimal sets with B, cycle list, component types and
simple-cycle points; maximal H sets; and witnesses (x*, multiplier, z).

## 3x+1 mod 8: the YAH table is exactly the P/H boundary

* **Minimal provable (all residues):** {2} (P1), {3} (P1), {4} (P1), {6} (P0), {0,1} (P1),
  {1,5} (P1), {1,7} (P0). Only {6} and {1,7} are P0. The P1 sets' only expanding SCCs are the
  simple cycles of −1 (and 0).
* **Frontier (maximal H):** **{1}** and **{0,5,7}**.

So, for subsets of Z/8, the SCC/descent certificate method proves S(C, A) **iff A ⊄ {1} and A ⊄ {0,5,7}**.

* The 8 nonempty H sets are {1}, {0}, {5}, {7}, {0,5}, {0,7}, {5,7} and {0,5,7}.
* They include all the sets YAH list as open: {1}, {5}, {7}, {5,7} (the prize Conjectures
  4.11–4.14), and {0}, which YAH list as open but not as a numbered prize conjecture.
* The extra sets {0,5}, {0,7} and {0,5,7} are weaker cousins of those conjectures, and they are
  equally out of reach of the method.
* Counting note: the 490 minimal provable sets of the nine censuses include YAH's own proved
  mod-8 sets {2}, {3}, {4}, {6}, {1,5}, {1,7} (and {0,1}). Most of the 490 are routine instances
  of one method, not 490 independent new results; the new content is the method, the 5x+1 and
  7x+1 censuses, and the frontier description.

## 3x+1 mod 16 (all residues)

* **Minimal provable sets (47):**
  * size 1: {6}, {12};
  * size 2: {2,3}, {2,7}, {2,8}, {7,9}, {8,9}, {2,10}, {9,10}, {3,11}, {7,11}, {8,11},
    {10,11}, {2,14}, {9,14}, {11,14}, {2,15}, {9,15}, {11,15}. The last six of these are P0.
  * 20 triples and 8 quadruples: see the JSON.
* **Frontier (8 maximal H sets):**
  * {0,1,2,4,5,9,11}
  * {0,1,3,4,5,8,10,13,15}
  * {0,1,4,5,7,14,15}
  * {0,3,5,7,8,10,13,14,15}
  * {0,3,5,9}
  * {1,2,4,9,11,13}
  * {1,4,7,13,14,15}
  * {3,9,13}

**Relation to YAH.** Lift each open mod-8 set to mod 16; for example {5,7} becomes
{5,7,13,15}. Each lifted set lies in the following frontier sets:

| YAH set | frontier sets containing its lift |
|---|---|
| {5,7} (Conj. 4.14) | **only** F* = {0,3,5,7,8,10,13,14,15} |
| {7} | {0,1,4,5,7,14,15}, F*, {1,4,7,13,14,15} |
| {1} | {0,1,2,4,5,9,11}, {1,2,4,9,11,13} |
| {0}, {5} | {0,1,3,4,5,8,10,13,15}, F* |

So the statement

> every C-trajectory not reaching 1 meets 0, 3, 5, 7, 8, 10, 13, 14 or 15 (mod 16)

is the **weakest mod-16 weakening of the $500 Conjecture 4.14 that is still beyond every
SCC/descent certificate mod 2^m**. Adding any one of the residues 1, 2, 4, 6, 9, 11, 12 makes it provable with an explicit
certificate. Theorem E (entropy.md) bounds its possible counterexamples ≤ X by O(X^θ) with
θ < 1 (θ = 0.4057). F* has even residues, so this uses the remark in entropy.md that a
C-avoider is a T-avoider, together with the exact certificate λ < 2 in `check.py` [6].

## 3x+1 mod 32 (odd residues)

* 76 minimal provable sets: 9 of size 3, 23 of size 4 (14 of them P0), 19 of size 5, 21 of size
  6, 4 of size 7.
* The size-3 sets: {7,15,25}, {9,15,25}, {7,23,25}, {1,15,27}, {7,15,27}, {9,15,27}, {11,15,27},
  {7,23,27}, {11,23,27}.
* 35 frontier sets, with 7 to 12 residues each. Their Theorem-E exponents lie in
  [0.223, 0.613].

**Minimum size of a provable set of odd residues mod 2^k** (`minsize.py`, exact branch and
bound on witness sets; complete, because every provable superset must meet every witness set):

| k | 3 | 4 | 5 | 6 |
|---|---|---|---|---|
| min size | 1 ({3}) | 2 | 3 | 4 |
| density among odd classes | 1/4 | 1/4 | 3/16 | 1/8 |
| number of minimum sets | 1 | 5 | 9 | 5 |

The minimum sets mod 64 are {7,15,27,59}, {7,15,39,57}, {7,15,39,59}, {9,15,47,57} and
{9,15,47,59}. A pattern min size = k − 2 would give provable trap sets of density → 0. That is
EVIDENCE only (k ≤ 6). The mechanism visible in the data is to cut the 9/8 cycle of −5 (27 and 59
are ≡ −5 mod 32) and the −1 runs (7, 15) while keeping −1 simple. I have no proof for general k. For k = 7 the exact search did not finish within the compute
budget. A quick test found that no lift of a k = 6 minimum set plus one extra residue is provable
mod 128. So if the minimum size at k = 7 is 5, the minimum sets have a different shape; this is
EVIDENCE only.

## 5x+1 and 7x+1

There is no global conjecture to compare with here, since GLOBAL itself is hopeless. These
systems are new and settled:

* **5x+1, mod 8 (all residues).** Minimal provable sets: {4}, {6}, {0,1}, {0,2}, {1,3}, {2,3},
  {0,7}, {1,7}, {2,7}, {3,7}. Frontier: {0,3,5}, {1,2,5}, {5,7}.
* **7x+1, mod 8 (all residues).** Minimal provable sets: {2}, {4}, {0,5}, {1,5}, {0,6}, {1,6},
  {5,6}, {0,7}, {1,7}, {5,7}. Frontier: {0,1,3}, {3,5}, {3,6,7}.
* **mod 32, odd.**
  * No minimal provable set is P0. Every one of them **needs Theorem 2**: the expanding points
    −1/3 (5x+1) and −1/5 (7x+1) sit in simple components. This is task item (4) at scale.
  * For 5x+1, the certified cycle lists are: none, {(1 6 3 16 8 4 2)}, or
    {(13 66 33 166 83 416 208 104 52 26)}. Ten minimal sets leave only the 13-cycle (see
    trap5_c13.md).
  * For 7x+1, the cycle list is none or {(1 8 4 2)}.
  * The smallest are 5-element sets mod 32: 18 for 5x+1, 8 for 7x+1.

## Which expanding points drive the frontier

The witnesses' periodic points are:

* **3x+1:** −1 and −2 (3/2); the 9/8 cycle −5, −14, −7, −20, −10; the rational cycles −38/11,
  −46/11, −58/11, −19/11, −23/11 (27/16); −101/17 and −358/17 (81/64); −2683/139 (3^7/2^11).
* **5x+1:** −1/3 and −2/3 (5/2); −1 (5/4); −28/17, −9/17, −18/17 (25/8); −162/61 (125/64).
* **7x+1:** −1/5 and −2/5 (7/2); −4/3 (7/4); −36/41 (49/8); −67/327 and others (343/16).

All of them are negative rationals, as Theorem 2 forces for expanding cycles.
