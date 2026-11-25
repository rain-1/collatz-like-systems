# qrA3_q17 — no finite-state basin classifier in any integer base

**Theorem (CLS-057).** For every integer base $k\ge2$, no finite automaton reading the base-$k$ digits of a positive integer coprime to 17 can distinguish the cycles $(1,6,3)$ and $(5,13,10)$ reached under this map.

Write $f(n)=1$ if $n$ reaches 5, and $f(n)=0$ otherwise, with $f(0)=0$. Multiples of 17 are recognizable in every base by tracking the remainder. Therefore a classifier on the promised inputs would give a $k$-automaton for $f$. The proof below rules this out.

## Both basins occur in every progression containing a unit modulo 17

The map halves even inputs and takes an odd input $x$ to $(x+17c)/3$ with $c=x\bmod3$. For $x>17$ both branches decrease strictly. The interval $[1,17]$ is invariant and its cycle representatives are 1, 5 and 17. Each step preserves divisibility by 17 in both directions. Thus every unit eventually visits either 1 or 5.

First fix $Q$ coprime to 6. From either odd seed $b\in\{1,5\}$ we can produce arbitrarily large odd points of its basin congruent to either chosen $c\in\{1,5\}$ modulo $Q$. The maps $L(y)=3y$ and $R(y)=3y-34$ give odd predecessors whenever $y$ is odd and the result is positive. Modulo $Q$ they are permutations. Their finite semigroup contains their inverses, so it contains $R L^{-1}$, translation by $-34$. This translation reaches every residue in a fixed class modulo $\gcd(34,Q)$, which is either 1 or 17. In the latter case multiplication by 3 connects 1 and 5 since $3^5\equiv5\pmod{17}$. Hence some word in $L,R$ sends $b$ to $c$ modulo $Q$. Before applying the word, multiply $b$ by an arbitrarily large power of 3 congruent to 1 modulo $Q$. This keeps every intermediate input positive and gives arbitrarily large outputs. For $Q=1$ the empty word suffices.

Now let $x$ be any positive unit modulo 17 and let $M\ge1$. Follow $x$ to $c\in\{1,5\}$. Reverse this particular finite path. Its composite is $y\mapsto x+A(y-c)$, where $A$ is the product of its branch denominators. Indeed each reverse step is either $y\mapsto2y$ or $y\mapsto3y-17d$ with the original digit $d$. Starting with $y\equiv c\pmod2$ preserves the required parity at every intermediate step. The residue of $3y-17d$ modulo 3 is exactly $d$. For $y\ge c$ all intermediate values are positive.

Write $M=2^u3^vQ$ with $Q$ coprime to 6. From the basin of either seed choose a large odd $z\equiv c\pmod Q$ as above. Reversing one lap at $c$ sends an odd $z\ge c$ to $c+18(z-c)$, since each cycle has one halving and two divisions by 3. Reversing $t$ laps gives $y=c+18^t(z-c)$, still odd and in the chosen basin. Choose $t$ so that $2^u3^v\mid18^t$. Then $y\equiv c\pmod M$. Reversing the path from $x$ to $c$ gives $x+A(y-c)\equiv x\pmod M$ in the chosen basin. Taking $z$ arbitrarily large proves the assertion for both basins.

Consequently every section $g(n)=f(Dn+r)$ whose progression contains a unit modulo 17 fails to be ultimately periodic. Indeed, take an index $n_0$ with $Dn_0+r$ a positive unit. For every proposed period $P$, both labels occur arbitrarily far along the progression through $Dn_0+r$ of step $DP$. Ultimate periodicity would force a single label there.

## A finite kernel would force a periodic section

We have $f(2n)=f(3n)=f(n)$ for all $n$. Doubling simply inserts a halving step. For tripling, remove the common power of 2 from $n$ and $3n$, then observe that an odd multiple of 3 maps to its quotient by 3.

Suppose $f$ is $k$-automatic. Its $k$-kernel, consisting of the sequences $n\mapsto f(k^a n+r)$ for $0\le r<k^a$, is finite. Each member is itself $k$-automatic since its own $k$-kernel lies in the same finite set. Let $S$ consist of members admitting a representation whose progression contains a unit modulo 17. Every member of $S$ fails to be ultimately periodic by the preceding result. We use the standard finite-kernel characterization of automatic sequences. [Allouche and Shallit, *Automatic Sequences*](https://www.cambridge.org/core/books/automatic-sequences/B092437A099192BA22DE4CF638142558)

Choose $p=2$ unless $k$ is a power of 2, in which case choose $p=3$. Then $p$ and $k$ are multiplicatively independent. On $S$, give state $g$ a transition with digit $i$ to $n\mapsto g(pn+i)$ if that sequence belongs to $S$. These transitions are deterministic wherever defined.

**Every finite digit word can be read from some state in $S$.** Write its digits least significant first, let $e$ be its length, let $d$ be its value, and write $d_j=d\bmod p^j$ for the value of its first $j$ digits. Choose $D=k^a>2p^e$. There is a residue $0\le r<D$ with
$$
r\equiv-Dd\pmod{p^e},\qquad 17\nmid r.
$$
Indeed the least nonnegative solution and that solution plus $p^e$ both fit, and 17 cannot divide both. Start at $g(n)=f(Dn+r)$. After the first $j$ digits the section is
$$
g(p^j n+d_j)=f\bigl(p^j(Dn+r_j)\bigr)=f(Dn+r_j),
\qquad r_j=(Dd_j+r)/p^j.
$$
Here $r_j$ is an integer with $0\le r_j<D$. If $17\mid D$, then $17\nmid r_j$ because $17\nmid r$. If $17\nmid D$, every progression with step $D$ contains units. Thus every intermediate state lies in $S$, as required.

**Some state in $S$ can read every word.** Otherwise start with all states as possible starts. Pick one surviving start and append a word unreadable from its current state. This eliminates that start, and a start already eliminated cannot return. After at most $|S|$ such extensions the resulting word is unreadable from every start, contradicting the previous paragraph.

For this state, every iterated base-$p$ section belongs to the finite set $S$. It is therefore $p$-automatic as well as $k$-automatic. Cobham's theorem forces it to be ultimately periodic. This contradicts the progression result and proves the theorem. [Cobham, *On the base-dependence of sets of numbers recognizable by finite automata* (1969)](https://doi.org/10.1007/BF01746527)

## Round-two record (historical)

The original census established descent and nonperiodicity. Its open status and kernel measurements below predate the proof above.

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
