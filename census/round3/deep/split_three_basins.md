# Positive basins of the contracting split maps when the shift is divisible by three

For positive odd $d$, let $\Sigma_d$ halve an even positive integer $n$. For odd $n$, take the unique one of $n+d$ and $3n+d$ divisible by four. A basin is the set of positive starts reaching a specified cycle. This is the family denoted $\Sigma_d$ in the census. The question left at the end of the round-3 basin report concerns $3\mid d$. Eventual periodicity for this family was already known. [Original question and coprime-shift theorems](basins.md)

**The power-of-three case.** For every $a\ge1$, set $d=3^a$. There are exactly two positive cycles. In raw steps they are
$$
(d,4d,2d),\qquad (d/3,4d/3,2d/3).
$$
A finite automaton on the binary digits of the start distinguishes the two basins. The first has natural density one. If $E_a(X)$ counts starts at most $X$ reaching the second, then, with $\varphi=(1+\sqrt5)/2$,
$$
 E_a(X)=\Theta_a\!\left(X^{\log_2\varphi}(1+\log X)^{a-1}\right)
 \qquad (X\to\infty).
$$
For example, for $d=9$ the exceptional basin leading to $(3,12,6)$ has order $X^{0.69424\ldots}\log X$. The other starts reach $(9,36,18)$.

## The reduction

Combine an odd step and its two guaranteed halvings into one block. Denote the even block by $E$, the odd block using $n+d$ by $B$, and the odd block using $3n+d$ by $A$. For $n>d$ all three block outputs are strictly less than $n$. The interval $[1,d]$ is closed at block boundaries. Hence every positive orbit enters it and eventually cycles. Raw intermediate values can be recovered by restoring the two halvings.

Multiplying both parameter and input by an odd $s$ commutes with every raw step. At an $A$ block with current parameter $D=3D'$, one can therefore perform the following exact reduction:
$$
  \frac{3n+D}{4}=3\frac{n+D'}4.
$$
The quotient is a positive integer because the chosen branch was legal and 3 is odd. Continue with parameter $D'$ and height $(n+D')/4$, keeping the removed factor 3 as an overall scale. Blocks $E$ and $B$ leave the parameter in place. Thus, for $d=3^a u$, $3\nmid u$, after $a$ occurrences of $A$ the remaining dynamics is exactly $\Sigma_u$, scaled by $3^a$.

Here is also a rule for an individual start, with no automata terminology. While $3\mid D$, apply
$$
(D,n)\longmapsto
\begin{cases}
(D,n/2) & n\text{ even},\\
(D,(n+D)/4) & n\equiv-D\pmod4,\\
(D/3,(n+D/3)/4) & n\equiv D\pmod4 .
\end{cases}
$$
If the parameter reaches $u$, use the basin for $\Sigma_u$; if the pair repeats beforehand, the repeat gives the cycle. Multiply its heights by $d/D$ and restore intermediate raw steps. Only finitely many parameter drops are possible. At a fixed parameter $D$, each block starting above $D$ strictly decreases the height and blocks starting at most $D$ stay in that interval. Thus the rule terminates for every positive start. At $D=1$ the only cycle is $(1,4,2)$ by the descent into $[1,1]$.

## Which cycles can occur?

Write $d=3^a u$ with $u$ odd and coprime to 3. The cycles entirely in $3^a\mathbb N$ are precisely $3^a$ times the cycles of $\Sigma_u$. Every other cycle has a constant valuation $j=v_3(n)<a$. Indeed $E$ and $B$ preserve this valuation below $a$, while $A$ increases it, capped at $a$. Thus such a cycle uses only $E,B$.

The latter cycles have a finite description. In the auxiliary raw map $X_d$, which halves even inputs and adds $d$ at every odd input, take an orbit $K$ of multiplication by 2 on residues modulo $d$, represented in $[1,d]$ (represent zero by $d$). The corresponding raw cycle consists of $K$ and the values $r+d$ for odd $r\in K$. To see this, observe that after a halving in the cycle the value lies in $[1,d]$, and the successive halving outputs rotate through the residues by $2^{-1}$. Alternatively this is Theorem B1 of the census. Retain exactly the $K$ outside $3^a\mathbb N$ for which every odd $r\in K$ satisfies $r\equiv-d\pmod4$. Those and only those auxiliary cycles use legal $B$ steps throughout. This lists every positive cycle of $\Sigma_d$.

For $d=3^a$ and $j<a$, divide the valuation-$j$ layer by $3^j$ and put $k=a-j$. The units modulo $3^k$ form one orbit under doubling. Indeed $v_3(4^{3^i}-1)=i+1$ by induction on $i$ using the binomial expansion. Together with the order two of 2 modulo 3, this gives order $2\cdot3^{k-1}$ modulo $3^k$. When $k$ is even, the representative 1 forces an $A$ branch since $1\equiv 3^k\bmod4$. When $k$ is odd and at least three, the unit representative 7 forces $A$ since $7\equiv 3^k\bmod4$. Only $k=1$ survives. Its representatives are 1 and 2, giving the raw cycle $(1,4,2)$ at parameter 3. Rescaling gives the two cycles in the statement.

## A binary basin test

An integer set is binary automatic if a finite automaton recognizes its base-two representations. We describe a machine reading low digits first. Reversing a regular language gives the equivalent high-digits-first convention. [Background on automatic sequences](https://www.cambridge.org/core/books/automatic-sequences/B092437A099192BA22DE4CF638142558)

At a block boundary let $N$ be the unread binary suffix, considered as an integer. Store the current parameter $D=d/3^i$ and a carry $b$ so the current reduced height is $N+b$. Initially $D=d$, $b=0$. For $3\mid D$, read one bit $r$. If $r+b$ is even, consume that bit and replace $b$ by $(r+b)/2$. Otherwise read one more bit $t$, setting $v=r+2t+b$. If $v\equiv-D\bmod4$, keep $D$ and put $b=(v+D)/4$. In the other odd case put $b=(v+D/3)/4$ and replace $D$ by $D/3$. The identities follow by substituting $N=2N'+r$ or $N=4N'+r+2t$ in the reduction rule. The bound $0\le b\le d+1$ is invariant. A pending one-bit read adds only finitely many states.

At end of input the unread suffix is zero. Supply a zero bit to finish a pending pair if necessary. Each possible remaining state then represents a fixed bounded height, whose eventual cycle can be tabulated by the descent argument. If $D$ reaches 1 before the input ends, the final label is the original $d$-cycle independently of the unread digits. This constructs the claimed two-basin automaton, including an explicit output rule. Zero as a whole input is outside the domain.

**Extension to general $d=3^a u$.** Every cycle outside $3^a\mathbb N$ has a binary-automatic basin. Use the same machine and reject that cycle whenever $D$ reaches $u$ early. For a cycle $3^a C$ inside $3^a\mathbb N$, let $H=\langle2,3\rangle$ act on residues modulo $u$ by multiplication (use a single class for $u=1$).

- If $C$ is the only $\Sigma_u$ cycle in its $H$-class, its scaled basin is binary automatic. At an early stop with $D=u$, the $H$-class of the current reduced height equals that of the original input modulo $u$. This holds at each reduction because both 2 and 3 are units modulo $u$ and every current parameter is a multiple of $u$. Track the original residue, including all unread digits, in parallel modulo $u$ and return the class label. End-of-input cases before an early stop use the finite table above.
- If $C$ shares its $H$-class with a different $\Sigma_u$ cycle, its scaled basin is nonautomatic in every integer base. Restricting its indicator to $n=3^a m$ gives the indicator of the basin of $C$ in $\Sigma_u$, which is nonautomatic in every base by the census coprime-shift theorem B4. In any fixed base, multiplying an input by a fixed integer uses finite carry; thus if the scaled indicator were automatic, so would be this restriction. [Theorems B2–B4](basins.md)

This decides the automaticity question for each cycle at every odd shift. The positive result is binary automaticity; it does not require the basin to be a union of residue classes.

## Size of the smaller basin

We prove a slightly more general counting statement. Let $C$ be any cycle outside $3^a\mathbb N$, and let $j<a$ be its constant 3-adic valuation. Its basin up to $X$ has size
$$
 \Theta_{d,C}\!\left(X^{\log_2\varphi}(1+\log X)^j\right).
$$

Each reduced block consumes one bit for $E$ and two for $B,A$. For a word with total bit length $m$ and exactly $r$ marked $A$ blocks, its ordinary generating function in $m$ is
$$
 \frac{z^{2r}}{(1-z-z^2)^{r+1}}.
$$
Indeed its $r+1$ intervening strings are arbitrary over $E,B$. Its coefficient has order $\Theta_r((m+1)^r\varphi^m)$ as $m\to\infty$. For an elementary bound, the number of unmarked strings of length $l$ is $F_{l+1}\asymp\varphi^l$. Split $m-2r$ among $r+1$ nonnegative lengths and sum the products over the $\binom{m-r}{r}$ choices.

A start reaching $C$ uses at most $j$ marked $A$ blocks in its entire trajectory, since after $j+1$ such blocks every subsequent raw height is divisible by $3^{j+1}$. For starts below $2^m$, stop at the first block boundary consuming at least $m$ bits; its length is $m$ or $m+1$. Inverting a fixed word of length $h$ expresses its start as $2^h x-c$ with fixed integer $c$ and reduced endpoint $x$. Thus at most one start below $2^m$ realizes that word. Summing the coefficient bound for $0\le r\le j$ proves the upper estimate.

For the lower estimate choose a fixed $x>d$ in the basin of the scaled-down cycle $C/3^j$ at parameter $d/3^j$. One can take any cycle point in that scale and repeatedly double it. For every word of length $m$ with exactly $j$ marked blocks, start at $x$ and read the word backwards. At current parameter $D$, reverse $E$ by $x\mapsto2x$, reverse $B$ by $x\mapsto4x-D$, and reverse $A$ by $x\mapsto4x-D$ **and** $D\mapsto3D$. In the last case the predecessor is odd and congruent to $3D\bmod4$, precisely the legal $A$ class at the raised parameter. In the $B$ case it is congruent to $-D\bmod4$. All heights stay above the original $d$, since every parameter used is at most $d$. The starting values obtained are at most $2^m x_{\rm initial}$ and all reach $C$. Different words of the same bit length give different starts, because forward branch selection is deterministic and cumulative bit length is strictly increasing. Taking $m=\lfloor\log_2(X/x_{\rm initial})\rfloor$ proves the lower estimate. For $d=3^a$ the smaller cycle has $j=a-1$, as claimed.

**Verification and scope.** The accompanying checker compares the binary decision rule and the cycle construction against direct raw iteration and checks the inverse-word counts. The estimates above follow from the proof for unbounded $a$ and $X$. The general nonautomaticity conclusion uses the earlier coprime-shift theorem; the power-of-three result is elementary and independent of it. This resolves the positive basin question recorded for the contracting family. The split map called split5_3 has a different odd multiplier and its global question remains open. [Checker](check_split_three_basins.py)
