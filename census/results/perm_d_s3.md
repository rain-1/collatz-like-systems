# perm_d_s3

Rule (D): 2q -> 5q; 8q+1 -> 5q+1; 8q+3 -> 5q+2; 8q+5 -> 5q+3; 8q+7 -> 5q+4. Seed 3.

| question | answer | status | tier |
|---|---|---|---|
| FATE | returns to seed (period 3) | PROVED | 0 |
| CYCLES with one strict local minimum | exactly the three cycles through 2, 6, and 26 | [PROVED](#all-positive-cycles-with-one-local-minimum) | 4 |
| GLOBAL | unknown | OPEN | 5 |

**Common facts (tier 1).** (i) The map is a bijection of the positive integers: each residue-class branch is an increasing affine bijection from its class onto one target class, and the target classes partition Z_{>0} (checked algebraically; spot-checked against an explicit inverse in the check script). (ii) For an injective map, fate (b) is impossible: if the orbit of x first meets a cycle C at y=T^k(x) with k>=1 and x not in C, then y has two distinct preimages (T^{k-1}(x) and its predecessor in C). So FATE is "returns" or "infinite". (iii) For a bijection, "every orbit eventually periodic" means "every orbit is a finite cycle". (Inverse: 5q -> 2q, 5q+r -> 8q+2r-1 for r=1..4.)

**FATE.** 3 -> 2 -> 5 -> 3.

**GLOBAL (OPEN, tier 5).** No proof either way. Heuristic drift (1/2)log(25/16) > 0 forward (and positive for D^{-1} too: (1/5)log(2/5)+(4/5)log(8/5) > 0), so most orbits are expected to be infinite; 1990 of the first 2000 starts do not cycle within the baseline budget. But proving any single orbit infinite is a problem of the same type as Collatz's 1932 orbit-of-8 question (a Collatz-type permutation with no known infinite orbit), and no conjugacy reducing D to a solved map was found. Its rational fixed points (0, -1, +-1/3, 1) do not give an embedding of T. Not known to be equivalent to a named problem; it is a direct analogue of the 1932 problem.

Check: checks/perm_d_s3.py (cycle and bijectivity vs explicit inverse; exit 0).

## Referee

Independently re-checked against the catalog step functions (systems.py), not only the check script's own re-implementation: mutual inverses on 1..3e5 for T/T^{-1} and S/S^{-1}, B(n)=T(n+1)-1 on 1..3e5, S(5y)=5T(y) on 1..3e5, D injective on 1..8e4 with image covering 1..4e4. Bijectivity is re-derived by hand: the branch images are disjoint residue classes covering Z_{>0} (for D: 5Z from evens, 5q+1..5q+4 from odds). The injectivity argument ruling out fate (b) is correct.

Verdict: FATE confirmed (tier 0). The 3-cycle 3->2->5->3 was re-simulated. GLOBAL open-agreed (tier 5). Observation: D(n)=5n/2 for even n and round(5n/8) for odd n, a direct analogue of T (2n/3 or round(4n/3)). Both drifts are re-derived as positive. Referee search (scratchpad dsep.py): the residue graph of D, and of D^{-1}, is strongly connected for every modulus M<=200, so no union of residue classes is forward-invariant and no congruence certificate of an infinite orbit exists at those moduli. A 'yes' answer has no known approach either. I agree it is an unsolved analogue of the 1932 problem. It is not known to be equivalent to it.

## All positive cycles with one local minimum

**Theorem (CLS-046, restricted question).** The positive cycles with exactly one strict local minimum, counted over their least period, are
$$
(2,5,3),\qquad (6,15,9),\qquad (26,65,41).
$$
The only positive fixed point is 1. Thus every further positive cycle must have at least two rising blocks. The existence of an infinite orbit remains open.

**The cycle equation.** Write an odd step as $(5n+s)/8$, with $s=3,1,-1,-3$ for $n=1,3,5,7\pmod8$, respectively. Every even step rises, and every odd step at $n>1$ falls. At the unique minimum of a nonconstant one-minimum cycle write $x=2^k u$, with $u$ odd. There are exactly $k\ge1$ rising steps, ending at $5^k u$, followed by $\ell\ge1$ odd steps returning to $x$. The error in each falling step relative to multiplication by $5/8$ is at most $3/8$. Earlier errors contract at every subsequent falling step, so
$$
\left|2^ku-(5/8)^\ell 5^ku\right|
\le \frac38\sum_{j=0}^{\ell-1}(5/8)^j=1-(5/8)^\ell.
$$
Put $a=k+3\ell$, $b=k+\ell$, and $R=5^b/2^a$. Clearing denominators and, separately, dividing by $2^ku$ gives
$$
u|2^a-5^b|\le 8^\ell-5^\ell,\qquad 0<|R-1|<2^{-k}.
$$
Prime factorization gives the strict lower inequality. In particular $R>1/2$. If $\ell\ge3k+2$, then $R\le[(5/2)(5/8)^3]^k(5/8)^2<1/2$. Hence $\ell<3k+2$ and $a,b<16k$.

**Bounding the exponents.** Matveev's explicit real-field bound applied to $5^b2^{-a}-1$ gives
$$
\log |R-1|>-2\cdot10^9(1+\log(16k)).
$$
Here the field degree is one, the height parameters for 5 and 2 are 2 and 1, and $1.4\cdot30^5\cdot2^{4.5}\cdot2<2\cdot10^9$. Combining the two bounds gives $k\log 2<2\cdot10^9(1+\log(16k))$. This fails at $k=10^{12}$ since $\log 2>1/2$ and $\log(16\cdot10^{12})<32$. The function $k/(1+\log(16k))$ is increasing for $k\ge1$, so $k<10^{12}$. [Matveev's theorem](https://doi.org/10.1070/IM2000v064n06ABEH000314) · [Explicit real-field form, Theorem 2](https://pure.mpg.de/pubman/item/item_3181483_3/component/file_3181485/Ddamulira-Luca_On%2Bthe%2Bx-coordinates%2Bof%2BPell%2Bequations_2020.pdf)

To reduce this bound, take $\alpha=\log_2 5$ and
$$
p/q=8009031126156845/3449301958915901.
$$
This fraction is reduced and $|\alpha-p/q|<1/q^2$. The checker certifies the inequality by enclosing $\log 2$ and $\log(5/4)$ between rational endpoints using the positive series for $2\operatorname{arctanh}z$ at $z=1/3,1/9$. Since $0<b<16\cdot10^{12}<q/2$, the integer $bp-aq$ is nonzero. Thus $|b\alpha-a|>1/(2q)$. Also $|\log R|<2|R-1|$ by the mean value theorem on $R>1/2$. Together these give
$$
\frac1{2q}<|b\alpha-a|=\frac{|\log R|}{\log 2}<4\cdot2^{-k},
\qquad 2^k<8q<2^{55}.
$$
Every possible cycle therefore has $1\le k\le54$.

**Exact enumeration.** For each such $k$ and $1\le\ell<3k+2$, compute $U=\lfloor(8^\ell-5^\ell)/|2^a-5^b|\rfloor$. The only pairs with $U\ge1$ are below. For each odd $1\le u\le U$, start at $2^ku$ and apply the catalog map, requiring the specified parities and return to the start.

| Rising steps $k$ | Falling steps $\ell$ | Upper bound $U$ | Odd $u$ passing the orbit check |
|---:|---:|---:|---|
| 1 | 2 | 13 | 1, 3, 13 |
| 2 | 4 | 4 | none |
| 3 | 6 | 1 | none |

These give exactly the cycles stated. The monotonicity of both branches away from 1 settles the fixed-point case. [Executable certificate](../lhf/perm-d/check_one_minimum.py)

**Relation to earlier work.** This map is $P(4,2,1,5)$ in Simons's notation. His Theorem 2 gives effective finiteness for each prescribed number of local minima in this family. The calculation here specializes that method to determine the actual list for one minimum. The earlier census enumeration covered arbitrary cycles of length at most 11. [Simons, *Cycles and divergent trajectories for a class of permutation sequences*](https://arxiv.org/abs/2205.10582) · [Earlier census proof](../lhf/perm-d/CLS-046.md)
