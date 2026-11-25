# qrA3_q17: two cycles in one coset with mixed multipliers {2,3}; no congruence rule (proved); finite-state rule OPEN

Rule: n even -> n/2; n odd -> (n + 17c)/3 with c = n mod 3.
Question: BASIN, in the strong form: give a finite-state (automatic) rule that decides whether n reaches (1 6 3) or (5 13 10), or prove that none exists.

| Question | Answer | Status | Tier |
|---|---|---|---|
| BASIN (finite-state rule) | Cycles are exactly (1 6 3), (5 13 10) and (17), all orbits reach them, and 17 \| n iff n reaches (17); all proved. No congruence rule separates (1 6 3) from (5 13 10) (proved). Whether some automaton in some base does is OPEN; the evidence says not in bases 2, 3, 6 | PARTIAL | 5 (nominal; see below) |

## Proved part
* **Descent and cycles.** Lemma CD (see qrA3_q23.md) with q = 17, M = {2,3}. The table gives exactly the cycles (1 6 3), (5 13 10) and (17).
* **Coset invariant is trivial.** 3 is a primitive root mod 17, so <2,3> = (Z/17)^*, and every unit lies in one coset. The coset invariant only separates multiples of 17, which reach 17, from units. This is the smallest prime q in family A3 where one coset holds two cycles. (The search over primes q < 200 lists 17, 53, 67, 71, 97, 107, 109, 157.)
* **Theorem (no congruence rule).** There is no P such that basin(n) depends only on n mod P.

  *Proof.* Suppose basin(n) = f(n mod P), with P = 2^a 3^b m' and gcd(m', 6) = 1.
  (i) T(2n) = n gives basin(2n) = basin(n). For odd n, 3n is odd and c = 0, so T(3n) = n and
      basin(3n) = basin(n).
  (ii) Taking 2^{e*ord(2)} n (with ord(2) the order of 2 mod 3^b m') gives
      basin(n) = F1(n mod 3^b m') for all n. Taking 3^{e*ord(3)} n (with ord(3) the order of
      3 mod 2^a m') gives basin(n) = F2(n mod 2^a, n mod m') for odd n.
  (iii) Let n, n' satisfy n = n' (mod m'). Replace each by an odd number with the same residue
      mod 3^b m', which by F1 has the same basin. By CRT pick an odd n'' with n'' = n (mod 3^b m')
      and n'' = n' (mod 2^max(a,1)). Then basin(n) = basin(n'') by F1, and
      basin(n'') = basin(n') by F2. So basin(n) = g(n mod m').
  (iv) g(2x) = g(x) and g(3x) = g(x), since odd n cover all residues mod m'. The numbers
      n = 1 (mod 6) have c = 1, and they cover all residues mod m'. They give
      g(x) = g((x+17)/3) = g(x+17).
  (v) If 17 does not divide m', g is constant, which contradicts basin(1) != basin(17). If
      17 | m', g depends only on x mod 17 and is invariant under multiplication by 3. But
      5 = 3^5 (mod 17), so g(5) = g(1). That contradicts basin(5) != basin(1). QED.

  The ingredients basin(2n) = basin(n) and basin(3n) = basin(n) (n odd) are one-line
  identities. The check also confirms them numerically to 2^20.

## Open part, and what was tried
* **Automaticity.** A set is k-automatic iff its k-kernel {n -> basin(k^e n + r)} is finite. The check, and a scratch run to 6*10^6, counts distinct kernel sequences on a window.
  * Base 2 gives 1, 2, 4, ..., 256 at levels 0..8. That is maximal: every new sequence is distinct.
  * Base 3 gives 1, 3, 9, ..., 243 (and 2187, then 6558 of 6561, on a larger run).
  * Base 6 gives 1, 6, 29, 65, 140, 329, 856.

  The growth does not saturate in any of these bases, which is strong evidence that the basin is not 2-, 3- or 6-automatic. This is evidence, not proof.
* **Why the qrB7_c53 method fails here.** With halving only, T is "drop the lowest bit, add a bounded carry", which is a finite transducer. Here the odd branch divides by 3 while the even branch divides by 2. Reading n in base 3 makes the odd branch a shift with carry, but halving in base 3 needs a carry from the top. That is the Collatz-type mixing of 2-adic and 3-adic digits, and it is exactly where finite-state certificates break down.
* **Cobham's theorem** (a set that is both 2- and 3-automatic is ultimately periodic) combines with the theorem above: the basin set is at most one of 2-automatic and 3-automatic. We could not exclude either one alone.
* Not tried: a proof of non-automaticity via the structure of kernels or via logic (Büchi arithmetic).

## Tier
Each individual n is decided by descent, so this is not a convergence problem. The hard part is
a closed classification rule. The negative half (no congruence rule) is proved at tier 2 level.
A finite-state rule, if one exists, would be tier 3. If none exists, the natural statement
("the basin is not k-automatic for any k") would need a substantial non-automaticity argument
(tier 4). We mark the question OPEN, with tier 5 as the nominal value of "unresolved". We do
not believe it is of Collatz difficulty.

## Referee (round 2)
Verdict: proved parts CONFIRMED; the finite-state question remains OPEN (agreed). Final tier: 5 (nominal "unresolved").

Proof check. Cycles, descent and the trivial coset invariant re-derived (3^5 = 243 = 5 mod 17 confirmed; 3 is a primitive root mod 17). The no-congruence theorem re-derived step by step; step (iii) needs n' to be replaced by an odd representative first (via F1), which the text does. Strengthening: like qrB7_c53, the argument also excludes ULTIMATE periodicity (multiply by a large power 2^{e*ord(2)} to land beyond N0), which is what the Cobham remark actually needs; with that, Cobham (1969) correctly gives: the basin is at most one of 2-, 3-automatic. Additional fact: basin(3n) = basin(n) holds for ALL n (for even n, 3n = 2^v * 3 * odd), so basin(n) = h(n') with n' the part of n coprime to 6. check script re-run: exit 0.

Attempts to finish (all failed):
* Invariance under x2 and x3 does not by itself force non-automaticity: S = {n : oddpart(n) = 1 or 3 mod 8} is 2-automatic, invariant under x2 and x3 (3 permutes {1,3} mod 8) and not ultimately periodic. So any non-automaticity proof must use the specific dynamics.
* Tested whether the basin restricted to n coprime to 102 is periodic mod M for M in {17*2^a*3^b : a<=11 or b<=7} and 17*5, 17*35, 17*5*7*11, 17*5*7*11*13, on n <= 2^21: tens of thousands of conflicts every time (no hidden congruence rule on the 6-free part).
* Kernel growth (explorer's data) is consistent with non-automaticity in bases 2, 3, 6, but is evidence only.
The question remains OPEN. We agree it is likely not Collatz-hard in the convergence sense (every n is decided by descent), but no technique at tiers 3-4 settled the classification question.
