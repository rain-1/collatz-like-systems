# Complete orbit and basin classification for qrB7_c53 on the integers

Rule: n even -> n/2; n = 1 mod 4 -> (n + 35)/2; n = 3 mod 4 -> (n + 21)/2.
This is family B, T(n) = (n + q*c_{n mod 4})/2, with q = 7 and (c_0, c_1, c_2, c_3) = (0, 5, 0, 3).

## Classification on all integers

**Theorem.** Every integer reaches exactly one of the following five cycles. Write $L(n)$ for the minimum of the cycle reached from $n$.

| $L(n)$ | Cycle in forward order | Which starts can reach it |
|---:|---|---|
| 0 | $(0)$ | Zero and some negative multiples of 7 |
| 1 | $(1,18,9,22,11,16,8,4,2)$ | Exactly $n\equiv1,2,4\pmod7$, of either sign |
| 3 | $(3,12,6)$ | Part of $n\equiv3,5,6\pmod7$, of either sign |
| 5 | $(5,20,10)$ | The rest of $n\equiv3,5,6\pmod7$, of either sign |
| 7 | $(7,14)$ | Every positive multiple of 7 and the remaining negative multiples of 7 |

The following binary rule decides **every** split in the table. For example $-21,-3,-9,-1,-7$ reach the cycles labelled $0,1,3,5,7$, respectively. Run the classifier with signed arguments, or omit the arguments to verify the theorem's finite calculations. [Classifier and exact checks](check_qrB7_signed.py)

**Why the list is exhaustive.** For $n<0$, $n<T(n)$, so after finitely many steps the orbit becomes nonnegative. For $n>35$, $0<T(n)<n$. The interval $[0,35]$ is forward invariant, and its cycle enumeration gives the five rows above. Every branch satisfies $2T(n)\equiv n\pmod7$. Multiplication by $2^{-1}$ partitions the residues into $\{0\},\{1,2,4\},\{3,5,6\}$. Positive integers stay positive. This proves all the residue and sign restrictions.

### A single binary classifier for either sign

Two halving identities account for the small number of states. For **all** integers $t$,
$$
L(2t)=L(t),\qquad L(4t+1)=L(t+9),\qquad L(4t+3)=L(t+6).
$$
For example $4t+1\to2t+18\to t+9$, and $4t+3\to2t+12\to t+6$.

Start with the unread integer $t=n$ in state $A_0$. Define $A_j(t)=L(t+j)$ and $B_j(t)=L(2(t+j)+1)$. While $t\notin\{0,-1\}$, read its low bit $b=t\bmod2$ and replace $t$ by $\lfloor t/2\rfloor$. With $j+b=2h+e$ and $e\in\{0,1\}$, update the state by this table.

| Current state | $e=0$ | $e=1$ |
|---|---|---|
| $A_j$ | $A_h$ | $B_h$ |
| $B_j$ | $A_{h+9}$ | $A_{h+6}$ |

Reading $b$ replaces the function $H$ by $t\mapsto H(2t+b)$. Substitution in the three identities gives exactly the displayed transitions. Thus the current function applied to the unread integer always equals $L(n)$. For a negative input, floor division leaves $-1$ when the finite digits have been consumed. This is the usual sign extension of binary integers.

The reachable states are precisely $A_0,\ldots,A_{12},B_0,\ldots,B_6$. The two rows show closure of this set, and breadth-first traversal from $A_0$ visits all 20. At termination use $z=t+j$ in state $A_j$, or $z=2(t+j)+1$ in state $B_j$. Return the entry for $z$ in this finite table, obtained from the cycles above.

| $z$ | $-1$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| $L(z)$ | 5 | 0 | 1 | 1 | 3 | 1 | 5 | 3 | 7 | 1 | 1 | 5 | 1 | 3 | 3 |

The classifier is minimal for this low-bit-first input convention with a terminal sign. For each reachable state $H$, form $(H(1),H(2),H(3),H(4),H(5))$. Direct evaluation gives 20 distinct tuples, as the checker verifies. Hence any two states can be distinguished by appending the digits of a positive integer from 1 to 5 and terminating with the positive sign. In particular, handling the negative inputs requires no additional states beyond the positive classifier.

### Natural densities of all five basins

On each half-line take cutoffs $1\le n\le X$ or $-X\le n\le-1$, dividing the count by $X$.

| Cycle minimum | Positive starts | Negative starts |
|---:|---:|---:|
| 0 | 0 | no density |
| 1 | $3/7$ | $3/7$ |
| 3 | no density | no density |
| 5 | no density | no density |
| 7 | $1/7$ | no density |

The densities that exist follow at once from the residue and sign rules. For the others, fix an integer $t$ and vary the low $k$ bits uniformly. This enumerates the block $[t2^k,(t+1)2^k)$ exactly, also for $t<0$. Each of the two transitions from a state then has probability $1/2$. If the resulting state is $H$, the output is $H(t)$.

The 19 states other than $A_0$ form a closed communicating class, as traversal of the transition table shows. It is aperiodic since $A_1$ has a self-loop. The initial state $A_0$ is transient since it leaves on a 1 and cannot be re-entered. Thus the state distribution tends to the unique stationary row. In order $A_0,\ldots,A_{12},B_0,\ldots,B_6$, the row has denominator 4599 and numerators
$$
(0,282,282,312,252,186,438,292,212,114,258,264,174,141,297,219,365,163,261,87).
$$
These sum to 4599, and the incoming weights on the two equally likely transitions give twice the weight at each destination. Summing weights over $H$ with $H(t)$ equal to the specified label gives the following limiting fractions, all in units of $1/4599$.

| Block high part $t$ | 0-basin | 1-basin | 3-basin | 5-basin | 7-basin |
|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 1971 | 1308 | 663 | 657 |
| 4 | 0 | 1971 | 990 | 981 | 657 |
| $-1$ | 282 | 1971 | 763 | 1208 | 375 |
| $-3$ | 312 | 1971 | 715 | 1256 | 345 |

If a basin had one-sided density $d$, its count up to $X$ on that side would equal $dX+o(X)$. Subtracting the counts at the two endpoints of any fixed-$t$ block on that side would then give $d2^k+o(2^k)$. The unequal entries between rows 0 and 4, and between rows $-1$ and $-3$, prove each nonexistence claim.

As a consequence the full signed basin function, with sign and magnitude encoded in any integer base $b\ge2$, is finite-state recognizable exactly for powers of two. Binary sign and magnitude can be converted to the convention above by complementing the bits and adding one with a single carry for a negative magnitude (then extending the sign); changing the reading direction preserves regularity. Grouping bits handles powers of two. In a multiplicatively independent base, even recognition of the positive 3-basin would force ultimate periodicity by Cobham's theorem, contradicting its absence of density. [Cobham (1969)](https://research.ibm.com/publications/on-the-base-dependence-of-sets-of-numbers-recognizable-by-finite-automata)

## Earlier classification on the positive integers

Question: BASIN.

| Question | Answer | Status | Tier |
|---|---|---|---|
| BASIN | 7 \| n -> (7 14). n a QR mod 7 (n = 1,2,4 mod 7) -> (1 18 9 22 11 16 8 4 2). n a non-residue mod 7 -> (3 12 6) or (5 20 10), as decided by the explicit 20-state LSB-first automaton below. No rule of the form "basin depends on n mod M" exists, for any M | PROVED | 3 |

## 1. Descent, cycles, coset invariant
If n <= 35 then T(n) <= 35, and if n > 35 then T(n) < n. Every odd branch adds a multiple
of 7 and halves, so T(n) = 4n (mod 7). Hence n mod 7 moves within its coset of <2> = {1,2,4},
the QR group. The table (check_qrB7_c53.py) finds exactly four cycles in [1,35]:
A = (1 18 9 22 11 16 8 4 2) among the QRs; (3 12 6) and (5 20 10), both non-residues;
and (7 14) among the multiples of 7. So the coset decides the basin except on the
non-residue coset, which holds two cycles. This is the first place where the coset invariant
stops determining the basin. In family B with c_i <= 5, q <= 17, this pattern (a unit coset
with >= 2 cycles) first occurs at q = 3 with c = (0,5,0,1); q = 7 is the smallest prime where
one coset is still decided by the Legendre symbol and the other is not.

## 2. No congruence classification exists (this is why tier 2 fails, and it is PROVED)
**Theorem.** There is no modulus P such that basin(n) depends only on n mod P.

*Proof.* Suppose basin(n) = f(n mod P), with P = 2^a m' and m' odd.
(i) T(2n) = n, so basin(2n) = basin(n). Let phi = ord_{m'}(2) and pick e with e*phi >= a.
    Then 2^{e*phi} n = 0 (mod 2^a) and = n (mod m'), so basin(n) = basin(2^{e*phi} n)
    = g(n mod m'), where g(x) := f(CRT(0, x)). From (i), g(2x) = g(x) for every x.
(ii) The numbers n = 1 (mod 4) cover every residue mod m' (gcd(4, m') = 1). For them,
    basin(n) = basin((n+35)/2), so g(x) = g((x+35)/2) = g(x+35) for every x, using
    g(y/2) = g(y). In the same way, n = 3 (mod 4) gives g(x) = g(x+21). Since
    7 = 3*21 - 2*35, g(x) = g(x+7).
(iii) If 7 does not divide m', translation by 7 is transitive on Z/m', so g is constant. That
    contradicts basin(1) != basin(7). If 7 | m', g(x) depends only on x mod 7 and is invariant
    under doubling. But 5 = 3*4 (mod 7), so g(5) = g(3), while basin(5) = (5 20 10) and
    basin(3) = (3 12 6). That is a contradiction. QED.

So no congruence invariant, however fine, decides the basin. A finite table cannot do it
either, because a "descent + finite table" proof of a classification rule needs the rule to
be stated by some finite data. The finest congruence data is the coset, and that has just
been shown insufficient. (The same argument works verbatim for any family-B map with
c_0 = c_2 = 0, gcd(c_1, c_3) = 1, and two cycles in one <2>-coset.)

## 3. The finite-state rule (tier-3 certificate)
**Carry transducer.** Write n in binary, b_0 the lowest bit. Claim: after k steps,
T^k(n) = 2*(n >> (k+1)) + b_k + s_k, where s_0 = 0 and

    r = (2 b_{k+1} + b_k + s_k) mod 4,
    s_{k+1} = (b_k + s_k + 7*c_r)/2      (c_r = 0, 5, 0, 3 for r = 0, 1, 2, 3).

*Proof by induction.* Put v = T^k(n) = 4*(n >> (k+2)) + 2b_{k+1} + b_k + s_k, so v = r (mod 4)
and T(v) = (v + 7c_r)/2 = 2*(n >> (k+2)) + b_{k+1} + (b_k + s_k + 7c_r)/2. The last fraction is
an integer, because c_r = r (mod 2) and 7 is odd. QED.

By induction s_k <= 36, so the state (s_k, b_k) ranges over a finite set. When the bits run
out (n >> (k+1) = 0), T^k(n) = b_k + s_k <= 37 is a small number, whose basin is read from
the table. Reading further leading zeros only applies more T-steps, so the output does not
depend on padding. The check builds this automaton (38 reachable states), minimizes it to 20
states by Moore's algorithm, and confirms it against direct iteration for all n < 2^18. The
table entries for all n are guaranteed by the proof above, not by that comparison.

Minimal automaton. Read n from its lowest bit; start in state 0; the output is the cycle
named by its minimum (1, 3, 5 or 7); "-" means n = 0.

    st: on0 on1 out     st: on0 on1 out
     0:   0   1  -      10:  16  13  5
     1:   2   3  1      11:   3  16  3
     2:   4   5  1      12:  17  11  1
     3:   6   7  3      13:   7  15  7
     4:   8   9  1      14:   9  18  1
     5:  10   6  5      15:  12  10  1
     6:  11  12  3      16:   5  14  5
     7:  13   8  7      17:   1  17  1
     8:  14   3  1      18:   3  19  3
     9:  15   4  1      19:  18   2  3

## Why tier 3 and not 2
Section 2 proves that no congruence invariant (tier-2 data) determines the basin. The
automaton is an explicit finite-state certificate in base 2, which is the tier-3 rubric item.
It is not tier 4: the certificate is small, and the correctness proof is the one-line carry
induction.

## Referee (round 2)
Verdict: CONFIRMED. Final tier: 3 (agreed).

Proof check. Descent and box [1,35] re-derived. The carry induction is correct: with v = 4(n>>(k+2)) + 2b_{k+1} + b_k + s_k, v mod 4 = r, and (b_k + s_k + 7c_r) is even because c_r = r (mod 2); s_{k+1} <= (1+36+35)/2 = 36. The automaton is therefore built from a proved identity over all states reachable from the start, so its correctness for every n follows from the induction, not from the 2^18 comparison. Independent test: referee re-implemented the carry recursion separately and compared to direct iteration of the systems.py step on 3000 random odd n up to 400 bits: 0 mismatches. check script re-run: exit 0.

Non-periodicity proof re-derived step by step and correct (g(2x)=g(x), g(x)=g(x+35), g(x)=g(x+21), 7 = 3*21 - 2*35, 5 = 3*4 mod 7). Strengthening: the same proof excludes ULTIMATE periodicity (basin(n) = f(n mod P) only for n >= N0): replace n by 2^{e*phi} n with e large, which is >= N0, and the argument goes through unchanged. So no congruence rule, even one valid only for large n, exists; tier 2 provably fails. Numerical witnesses at n ~ 10^6 for several moduli also found.

Tier: the 20-state automaton plus one-line carry induction is a genuine tier-3 certificate; nothing at tier 2 can work by the theorem above. Agreed.

## Exact basins on negative multiples of seven

**Theorem.** Write the starting integer as $n=-7u$ with $u\ge1$. Its orbit reaches either 0 or the cycle $(7,14)$. To decide which, start in state $A$ and read the binary digits of $u$ from least to most significant. Use the row for the current state and the column for the next bit. After the last bit, the final column gives the destination.

| State | Read 0 | Read 1 | Destination if finished |
|---|---|---|---|
| $A$ | $A$ | $B$ | 0 |
| $B$ | $C$ | $A$ | $(7,14)$ |
| $C$ | $D$ | $A$ | $(7,14)$ |
| $D$ | $C$ | $C$ | $(7,14)$ |

For example, $-7$ reaches 14 in one step. For $-21$ the bits of $u=3$ take the machine from $A$ through $B$ back to $A$, and indeed $-21\to0$. This resolves the basin question for negative multiples left open in the round-three integer-domain record.

**Proof of the rule.** Write $T(-7u)=-7F(u)$. Since $-7\equiv1\pmod4$, the induced map is $F(u)=u/2$ on evens, $(u-5)/2$ for $u\equiv1\pmod4$, and $(u-3)/2$ for $u\equiv3\pmod4$. Every positive input decreases strictly and has image at least $-2$. Zero is fixed and $-1,-2$ form a cycle. These are the two possible outcomes.

Let $b(u)=1$ if $F$ reaches 0, and 0 otherwise, with $b(-1)=b(-2)=0$. Halving and the two odd branches give, for $t\ge0$,
$$
b(2t)=b(t),\qquad b(4t+1)=b(t-1),\qquad b(4t+3)=b(t).
$$
For example, $4t+1\to2t-2\to t-1$. Interpret the four states as functions of the unread high digits $t$:
$$
A(t)=b(t),\quad B(t)=b(2t+1),\quad C(t)=b(t-1),\quad D(t)=b(2t-1).
$$
Reading a bit $e$ replaces the current function $H$ by $t\mapsto H(2t+e)$. The three identities give exactly the table, including $D(2t)=D(2t+1)=C(t)$ (at $t=0$ use $b(-1)=b(1)=0$). After the last bit, evaluate at $t=0$ to get $(1,0,0,0)$ in state order. This proves the rule for every input.

Four states are necessary in this digit order. All four are reachable, via the empty prefix, 1, 10, and 100 in reading order. Appending the digits of $t=1$ or $t=2$ distinguishes every pair. Their output pairs in state order are $(0,0),(1,1),(1,0),(0,1)$. Both distinguishing continuations end in a most significant 1, so the lower bound also holds for canonical binary inputs.

**Neither basin has a natural density among the negative multiples of seven.** To see how the proportion depends on the cutoff, fix a high part $t$ and let the low $k$ bits range uniformly. Those bits drive a four-state Markov chain with the two transitions in each row equally likely. The table makes the chain irreducible, and the self-loop at $A$ makes it aperiodic. Its unique stationary row is $(4,2,2,1)/9$, as direct multiplication shows. Consequently, in the block $t2^k\le u<(t+1)2^k$, the limiting fraction reaching 0 is
$$
\frac{4A(t)+2B(t)+2C(t)+D(t)}9.
$$
For $t=0,1,2$ the respective fractions are $4/9,4/9,3/9$. Thus the zero-basin fraction tends to $4/9$ below $2^k$ and to $11/27$ below $3\cdot2^k$. Omitting $u=0$ has no effect on either limit. Their difference, $1/27$, proves the assertion for the zero basin and its complement.

In particular there is no ultimately periodic rule, since every ultimately periodic set has a natural density. As sets of indices $u$, the basins are recognizable by a finite automaton in exactly the integer bases $2^a$, $a\ge1$. Grouping bits gives recognition in those bases. Every other integer base is multiplicatively independent of 2, so simultaneous recognition would imply ultimate periodicity by Cobham's theorem. Reversing digit order preserves regularity. [Cobham (1969)](https://research.ibm.com/publications/on-the-base-dependence-of-sets-of-numbers-recognizable-by-finite-automata) · [Exact checker](check_qrB7_negative.py)
