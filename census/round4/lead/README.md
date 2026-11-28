# Following the size lead (27 Nov 2026)

Status: NOT RESOLVED. This note records how far the lead goes, with one exact reformulation,
one quantitative prediction that matches data, one exact formula, and the precise point where
known number theory stops. Written outside the prover/referee loop; not refereed.
Scripts: `stopping.py` (evidence, about 3 minutes), `check_log.py` (exact, exits 0).

## The lead

`../schema/window.md` Theorem W4: if no stretch of at least C log2 n consecutive steps of the
3x+1 orbit of n has more than 5/8 odd steps, then the 3x+1 conjecture holds. The same kind of
statement can be made for every system: "no positive integer keeps from dropping below itself
for more than C log n halvings".

## 1. Reformulation (PROVED, immediate from the Markov property)

Let Omega be the set of p-adic integers that never drop below themselves (round 3,
`../../round3/deep/split5_3_deep.md`), a Cantor set of Hausdorff dimension h < 1. The first b
halvings of the orbit of n depend only on n mod p^b. So

    n does not drop within b halvings   <=>   n is within p^{-b} of Omega, p-adically.

The lead for a given system is therefore: **every large positive integer n has p-adic distance
at least n^{-C} from Omega.** It is a Diophantine approximation statement: positive integers
are badly approximable by a nonlinear Cantor set.

## 2. The constant (EVIDENCE; heuristic derivation)

About p^{hb} residues mod p^b have not dropped after b halvings. If the unique residue of each
such class were a random number below p^b, the expected number of integers below X that survive
C log X halvings would be X^{1 - C(1-h)}. So the critical constant should be

    C* = 1/(1 - h).

| system | h (round 3) | predicted C* | largest observed (halvings to first drop)/log2 n, n < 3e6 |
|---|---|---|---|
| 3x+1 | 0.949955 | 19.98 | 11.1 and rising slowly (5.5, 8.6, 8.9, 9.3, 11.1 by octave) |
| split5_3 | 0.580684 | 2.385 | 1.84 (at n = 2^19 - 3) |
| split5_1 | about 0.9369 | 15.8 | not run |

This explains the value "C near 20" that the schema lens observed for 3x+1 (its 5/8 window
version gives 1/(1 - H(5/8)) = 21.9), and it predicts that split5_3 needs only C near 2.4. For
split5_3 the record holders are again the explicit integers 2^j - 3.

## 3. The explicit family, exactly (PROVED; `check_log.py`)

In the coordinate N = n + 3, split5_3 is: N = 0 mod 4 -> 5N/4; N = 2 mod 4 -> N/2 + 3;
N odd -> (N+3)/2. The start N = 4^k w runs to 5^k w, and the length of the NEXT run is the
2-adic valuation of 5^k w + b for a small integer b fixed by the few steps in between. For
b = 3 mod 4 and w = 1:

    v_2(5^k + b) = 2 + v_2(k - lambda_b),    lambda_b = log_5(-b)  (a 2-adic integer).

So after the big run from 4^k, a second long run happens exactly when k itself is 2-adically
close to one of the constants lambda_b. The map k -> 5^k is a 2-adic isometry up to a shift, so
the powers of 5 sit inside Z_2 exactly as the integers do. The question for the record holders
at size N is the same kind of question again for the exponent k, at size log N, with Omega
replaced by its image under the 2-adic logarithm. This is a restatement of what round 2 found
for the rising family; it does not close.

## 4. What number theory gives beyond the first log n digits, and where it stops

* **Linear forms in 2-adic logarithms** (Yu's theorem; quoted from memory, constants not
  checked): v_2(5^k w + b) <= C log(max(w, b)) log k. Consequence: after the run from 4^k w
  with w small, a run starting s steps later has length at most C (s + log w) log k. This is a
  rigorous statement about the orbit beyond the horizon, but the factor log k makes it too weak
  to force a drop: a drop needs about 0.32 k further halvings, and over that many steps the
  bound allows runs of length about k log k.
* **The Subspace Theorem** (S-unit sums with a bounded number of terms): after any FIXED number
  n of non-run steps, runs are at most epsilon k long, for all but finitely many k
  (ineffective). A drop needs n to grow like 0.32 k, and the theorem has nothing to say when the
  number of terms grows.
* **abc-type conjectures** do not help either, for the same reason: after t steps the orbit
  value is a sum of about t terms in powers of 2 and 5, and the conjectures control sums with
  boundedly many terms.

So the obstacle is specific: **S-unit sums in which the number of terms grows with the
exponents.** Controlling the 2-adic size of sum_j 3 * 5^{a_j} 2^{e_j} + 5^a N with t terms and
t proportional to the exponents is the missing theorem, for split5_3 exactly as for 3x+1.

## 5. Verdict

The lead is equivalent in strength to the open problems themselves (for 3x+1 it implies the
Collatz conjecture). I found no argument that proves it for any system, including split5_3
where the predicted constant is small and the margin is large. What is new here is the
reformulation as p-adic approximation of integers by Omega, the predicted constant 1/(1 - h)
and its agreement with data, and the identification of the exact number-theoretic statement
that is missing.
