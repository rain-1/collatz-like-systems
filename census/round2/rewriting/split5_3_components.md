# Which arithmetic progressions meet an orbit of the split 5n+3 map?

Let $T$ halve even inputs, send $n\equiv1\pmod4$ to $5n+3$, and send $n\equiv3\pmod4$ to $n+3$. Work on positive integers. Say that two starts *merge* if some forward iterate of one equals some forward iterate of the other; zero iterates are allowed. This is an equivalence relation. Each step in either direction preserves divisibility by 3.

**Theorem 1.** For every $b,x,M\ge1$ with $3\mid b$ if and only if $3\mid x$, there are arbitrarily large $w\equiv x\pmod M$ whose orbits merge with that of $b$. Consequently the progressions meeting the merging class of $b$ are exactly those containing a positive integer of its divisibility type modulo 3.

In particular every merging class meets $1\bmod 10^d$ for every $d\ge1$, since this progression has members of both types. Eventual periodicity for all starts is equivalent to eventual periodicity on any one of these progressions. The point of intersection can be an ancestor off the forward orbit of $b$.

## Odd ancestors with prescribed residues

Write $A(x)=(5x+3)/4$ for the block at $x\equiv1\pmod4$ and $B(x)=(x+3)/2$ for the block at $x\equiv3\pmod4$. Both follow original steps. Every orbit visits an odd integer $y$ coprime to 5. Indeed, remove the initial powers of 2; if the resulting odd integer is a multiple of 5, its odd step gives a nonmultiple of 5, and halving preserves this property.

Fix $Q$ coprime to 10. Say a residue $r\bmod Q$ is *accessible at every power of 5* if for every $s\ge0$ and residue $t\bmod 5^s$ there are arbitrarily large odd ancestors of $y$ congruent to $r\bmod Q$ and $t\bmod 5^s$ simultaneously. We first construct one such $r$. This simultaneous condition matters because the orders of 2 modulo $Q$ and modulo $5^s$ can share large powers of 5.

Set $o=\operatorname{ord}_Q(2)$, taking $o=1$ when $Q=1$, and take $d\ge\max(1,v_5(o))$. The order of 2 modulo $5^i$ is $4\cdot5^{i-1}$ for $i\ge1$: its order modulo 5 is 4, and $v_5(2^{4\cdot5^j}-1)=1+j$ follows by binomial expansion from $2^4=1+3\cdot5$. In particular 2 generates all units modulo each power of 5.

Choose $h_0$ with $2^{h_0}y\equiv-12\pmod{5^{d+1}}$. For $h\ge2$ consider
\[
 w(h)=4^d\frac{2^h y+12}{5^{d+1}}-3 .
\]
Whenever the quotient is integral and $h$ sufficiently large, this is a positive odd ancestor. To verify the path, start with the ancestor $2^h y$, take the inverse odd branch to $(2^h y-3)/5$, then invert $A$ another $d$ times. The first inverse source is 1 modulo 4 since $h\ge2$. Each further inverse step multiplies the shifted coordinate $x+3$ by $4/5$ and again gives a source congruent to 1 modulo 4.

For any prescribed $t\bmod5^s$, solve
\[
 2^h y\equiv -12+5^{d+1}4^{-d}(t+3)\pmod{5^{d+1+s}} .
\]
The right side is a unit; the solutions give one class of exponents modulo $4\cdot5^{d+s}$ and agree with $h_0$ modulo $4\cdot5^d$. We may also impose $h\equiv h_0\pmod o$ by the generalized Chinese remainder theorem, since $\gcd(o,4\cdot5^{d+s})$ divides $4\cdot5^d$. Such exponents are arbitrarily large. Then $w(h)\equiv t\pmod{5^s}$ and its residue $r\bmod Q$ is independent of $t,s$, as $5$ is invertible modulo $Q$. This proves the initial accessibility claim.

From an accessible residue $r$, two maps give further accessible residues:
\[
 L(r)=2r-3,\qquad U(r)=(4r-3)/5\pmod Q.
\]
For odd ancestors $z$, $L(z)$ reverses $B$ and is positive for large $z$. To realize a target modulo $5^s$ after $U$, request $4z\equiv 5t+3\pmod{5^{s+1}}$ before it, so $U(z)$ is an actual positive inverse of $A$ and is odd. Both operations preserve the supply of arbitrarily large witnesses.

Modulo $Q$, $L,U$ are permutations. Their positive powers realize their inverses as permutations; every residue in their group orbit is therefore accessible. The maps $L U$ and $U L$ have the same slope and constants $-21/5$ and $-15/5$, respectively. Thus $(LU)(UL)^{-1}$ is translation by $-6/5$. Its orbits are precisely the classes modulo $\gcd(Q,6)=\gcd(Q,3)$. When $3\mid Q$, $L$ interchanges residues 1 and 2 modulo 3. It follows that all residues modulo $Q$ compatible with the type of $y$ are accessible.

## Restoring the binary part of the modulus

Write $M=2^u5^vQ$ with $\gcd(Q,10)=1$. From $x$ follow $u$ blocks chosen from $A,B,E$, where $E(x)=x/2$ for even $x$. Denote the endpoint by $c$, the product of their denominators by $2^l$, and the number of $A$ blocks by $k$. Then $l\ge u$. We can choose arbitrarily large ancestors $c'$ of $y$ such that
\[
 c'\equiv c\pmod{2\cdot5^{v+k}Q}.
\]
For odd $c$ this is the accessibility result. For even $c$, choose an odd ancestor congruent to $c/2$ modulo $5^{v+k}Q$ and double it. The relevant residues have the required type whenever $3\mid Q$.

Replay the path from $x$ to $c$ backward, starting at $c'\ge c$. At every stage the displacement from the old endpoint is nonnegative and even. A reversed $A$ consumes a factor of 5 from that displacement and multiplies it by 4. Reversed $B$ and $E$ multiply it by 2. There are enough factors of 5 for every division, and the even displacement preserves the parity needed for $B^{-1}$. The branch $A^{-1}(z)=(4z-3)/5$, whenever integral, gives the required residue 1 modulo 4. The resulting start
\[
 w=x+2^l(c'-c)/5^k
\]
lies in $x\bmod M$ and reaches $c'$. This proves Theorem 1.

## Finite automata for orbit-invariant labels

**Theorem 2.** Suppose $f$ takes finitely many values and $f(Tn)=f(n)$ for all $n>0$. It is automatic in some integer base if and only if it is constant on each of $3\mathbb N$ and its complement. Such labels are recognizable in every base by computing the remainder modulo 3.

Suppose $f$ takes different values at two starts of the same divisibility type $C$. By Theorem 1 any progression containing a member of $C$ contains arbitrarily large inputs of both labels. Its restriction of $f$ cannot even be ultimately periodic: restrict a proposed period $P$ in the progression index to the subprogression through that member, multiplying the step by $P$. This argument also works for the shifted label $g(n)=f(n-3)$ for $n\ge4$, since the shift preserves type and initial values can be assigned arbitrarily.

We use the finite-kernel criterion and Cobham's theorem. Recall that $\mathcal K_k(f)$ consists of the sequences $n\mapsto f(k^a n+r)$ for $0\le r<k^a$, $a\ge0$. It is finite precisely when $f$ is $k$-automatic, and all its members are then $k$-automatic. A finite set $S$ of such sequences carries partial digit transitions $h\mapsto (n\mapsto h(pn+i))$ when the new sequence belongs to $S$. If every finite base-$p$ word is readable from some start in $S$, some single start can read every word. Otherwise successively append a word that fails from the current state of one still-surviving start. After at most $|S|$ extensions no start survives. The state reading all words therefore has finite $p$-kernel. When $k,p$ are multiplicatively independent, Cobham implies that this state is ultimately periodic. [Cobham's theorem](https://research.ibm.com/publications/on-the-base-dependence-of-sets-of-numbers-recognizable-by-finite-automata)

First suppose $k$ is not a power of 2. Set $f(0)$ arbitrarily; $f(2n)=f(n)$ at every index. In its hypothetical finite $k$-kernel retain the states represented by progressions meeting $C$. Fix a binary word of length $e$ and value $d$, read low digit first. Choose a large $D=k^a$ and $0\le r<D$ with $r\equiv-Dd\pmod{2^e}$ and $r\equiv c_0\pmod3$, where $c_0=0$ for the multiples type and $1$ otherwise. These constraints are compatible. Write $d_j=d\bmod 2^j$. After $j$ digits, the section of $f(Dn+r)$ equals $f(Dn+s_j)$, where $s_j=(Dd_j+r)/2^j$ is an integer in $[0,D)$. If $3\mid D$ then $s_j\equiv 2^{-j}c_0\pmod3$; otherwise the progression meets every residue modulo 3. Every prefix stays in the retained states. The preceding digit argument with $p=2$ contradicts their failure of ultimate periodicity.

Now suppose $k$ is a power of 2. Automaticity in such a base is equivalent to binary automaticity by grouping binary digits. The fixed shift $g$ is binary automatic if $f$ is (subtracting a fixed integer in binary requires only finite carry information). The map gives the further identity
\[
 g(4n)=g(5n)\quad(n\ge0),
\]
because $4n-3$ reaches $5n-3$ by one $A$ block for $n\ge1$. For a base-5 word $d$ of length $e$, take $D=2^a>5^e$ and $0\le r<D$ with $r\equiv-Dd\pmod{5^e}$. For $d_j=d\bmod 5^j$ put $s_j=(Dd_j+r)/5^j\in[0,D)$. The section after $j$ digits is
\[
 g\bigl(5^j(Dn+s_j)\bigr)=g\bigl(4^j Dn+4^j s_j\bigr).
\]
The right side belongs to the original binary kernel since $4^jD$ is a power of 2. Every binary section has a step coprime to 3, so each progression meets $C$. The digit argument with $p=5$ again contradicts failure of ultimate periodicity. This proves Theorem 2.

**Consequences.** The four individual basins through $1,5,61,125$ are each nonautomatic in every integer base; their representatives are all coprime to 3. The basin of 3 is automatic exactly when it is all of $3\mathbb N$. The set of eventually periodic inputs contains a known representative of each type. Hence every positive orbit is eventually periodic if and only if that set is automatic in some integer base. The same equivalence holds separately for the stronger assertion that every input reaches one of the five known cycles, using the union of those five basins. The two assertions can differ if there are further cycles.

Theorem 1 is analogous to sufficiency of arithmetic progressions for the ordinary Collatz graph. Its two invariant types and the simultaneous residue construction above belong to this split map. Theorem 2 uses the kernel argument of the [q=17 note](../qr/qrA3_q17.md), with $g(4n)=g(5n)$ supplying the independent base in the binary case. [Monks et al., *Strongly sufficient sets and the distribution of arithmetic sequences in the 3x+1 graph*](https://arxiv.org/abs/1204.3904)

## How many members of a merging class lie in a progression?

**Theorem 3.** Let $H$ be any merging class and let $P$ be any arithmetic progression meeting its divisibility type. There is a constant $c(H,P)>0$ such that, for all sufficiently large $X$,
\[
 \#(H\cap P\cap[1,X])\ \ge\ c(H,P)X^\sigma,
 \qquad 4^{-\sigma}+(1024/5)^{-\sigma}=1 .
\]
Here $\sigma=0.238298\ldots$ is the unique positive root. This includes a hypothetical divergent class.

Choose an odd $y>3$ in $H$ coprime to 5, using Theorem 1. At every odd vertex $z\ge y$ coprime to 5 construct two children.

- Take $L(z)=2z-3$ if it is coprime to 5, and take $L(L(z))$ otherwise. In the latter case the second value is $-3$ modulo 5. Each $L$ step strictly increases its argument, reverses one step of the map from an odd value to the next odd value, and gives a predecessor congruent to 3 modulo 4. This child is smaller than $4z$.
- Among $3\le h\le10$, exactly two exponents, differing by 4, satisfy $2^hz\equiv3\pmod5$. The two integers $(2^hz-3)/5$ cannot both be multiples of 5, since $2^4-1=15$ is divisible by 5 exactly once. Choose the smaller exponent giving a unit modulo 5. Its predecessor $a=(2^hz-3)/5$ satisfies $z<a<(1024/5)z$, is 1 modulo 4, and has $z$ as its next odd iterate.

The resulting paths form a tree of distinct endpoints. Each expanded edge strictly increases at every odd step when read backwards. From an endpoint, the forward odd trajectory therefore determines its path up to its first visit to $y$. Reading that path backwards from $y$, the first predecessor modulo 4 identifies the child choice at each vertex. The length of the first kind of edge is determined by that vertex. This uniquely recovers the choices.

Assign weight $z^{-\sigma}$ to an endpoint. The combined child weight is at least the parent weight by the defining equation. For $R\ge y$, stop a path the first time it exceeds $R$. Strict increase of positive integers makes this a finite tree. Each leaf has weight at most $R^{-\sigma}$ and lies below $(1024/5)R$. Thus there are at least $(R/y)^\sigma$ distinct odd integers coprime to 5 in $H$ below $(1024/5)R$.

To transfer this count to a specified progression $P=x\bmod M$, we need uniform control of Theorem 1. Fix $x$ of the compatible type and its path to $c$ from that proof. There are constants $K,J$ depending only on $x,M$ such that every sufficiently large odd $z$ of that type coprime to 5 has an ancestor in $P$ of size at most $Kz$ reaching $z$ in at most $J$ original steps. The following bounds justify the uniformity.

1. Keep $Q,u,v,k,d,o$ fixed as in Theorem 1, choosing the least admissible $d$. Work backwards from the desired odd target residue ($c$ or $c/2$) modulo $Q$. From the initial accessible residue for $z$, a shortest word in $L,U$ reaching this target has length at most $Q-1$, because repeated residues can be deleted.
2. At the output of this word, prescribe the target modulo $5^{v+k}$. Pull this requirement backwards through the word. An $L$ uses the inverse of 2 at the same precision. A $U$ needs one additional factor of 5 in the input modulus. Thus the initial precision $s$ is at most $v+k+Q-1$.
3. For this initial prescription the Chinese remainder construction gives an exponent $2\le h\le 1+\operatorname{lcm}(o,4\cdot5^{d+s})$. The path for $w(h)$ and the word in $L,U$ now use a bounded number of original steps. The optional doubling and the replay of the fixed path from $x$ use a bounded number as well. All these inverse formulas have positive slope and fixed additive term once the branches and $h$ are specified. There are finitely many choices, so for sufficiently large $z$ every intermediate value is positive, the replay starts above $c$, and the final ancestor is at most $Kz$ for a common $K$.

Choose one such ancestor for each tree endpoint above the fixed lower threshold. A single output can represent at most $J+1$ endpoints, since each is among its first $J+1$ original iterates, counting time zero. Applying the tree count with $R=X/((1024/5)K)$ proves the claim.

The exponent measures a guaranteed supply of starts merging with an individual orbit. A bound of this size applies to each of the five known basins and would apply equally to another class. To prove global eventual periodicity by a counting contradiction one would need an incompatible upper bound on the number of starts in a divergent class. The earlier power bound counts only starts that never fall below their own initial value. An ancestor flowing into a divergent orbit can fall below its own start along the way, so that bound does not supply the needed comparison.

For a concrete example, the starts 6,000,001, 2,000,001, 1,000,001, 27,000,001, and 18,000,001 first hit the respective representatives 1, 3, 5, 61, and 125 after 90, 76, 66, 58, and 78 original steps. The accompanying checker verifies these orbits, joint residue control including modulus 101, the binary replay identity, and three inverse trees to depth 12. [Run the exact finite checks](check_split5_3_components.py)
