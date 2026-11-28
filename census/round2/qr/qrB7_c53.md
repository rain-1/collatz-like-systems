# qrB7_c53: two cycles in one coset; no congruence rule exists; a 20-state binary automaton decides the basin

Rule: n even -> n/2; n = 1 mod 4 -> (n + 35)/2; n = 3 mod 4 -> (n + 21)/2.
This is family B, T(n) = (n + q*c_{n mod 4})/2, with q = 7 and (c_0, c_1, c_2, c_3) = (0, 5, 0, 3).
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
