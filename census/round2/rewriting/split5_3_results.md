# Stopping times and cycles of the split $5n+3$ map

**Results and review record through `eab6fc9`, 28 November 2026**

For a positive integer $n$, define

$$
F(n)=
\begin{cases}
n/2 & n\equiv0\pmod2,\\
5n+3 & n\equiv1\pmod4,\\
n+3 & n\equiv3\pmod4 .
\end{cases}
$$

Every positive start below $2^{66}$ reaches one of five known cycles. Any further cycle has more than $61{,}800{,}000{,}000$ original steps. Whether every positive orbit eventually repeats is open. Whether the five cycles exhaust the positive cycles is also open. An escaping orbit would supply at least three starts in every sufficiently large dyadic interval whose heights never fall below their starting values. Thus a bound of two survivors, even at a finite depth and only in infinitely many such intervals, would settle eventual periodicity. The strongest general counting theorem reaches $m+O(\log m)$ halvings in almost every interval of width $2^m$. The proposed depth is $2.4m$.

This report gives the hypotheses, conclusions, checks and review history together. “Author proof” means that Codex supplied a mathematical argument in the repository. “Fable reviewed” means that Fable independently re-derived the specified argument, subject to the cited inputs. A checker certifies a finite computation or tests identified identities. The asymptotic theorems rest on the written arguments. The latest result, `eab6fc9`, has an author proof and finite checks. Fable has not independently refereed it. [Detailed derivations](split5_3_s27.md) · [Census entry](../../results/split5_3_s27.md)

## 1. Coordinates and the three clocks

Write $y=n+3$ and $s=5/4$. A complete **block** is one of the following exact segments of the original orbit.

| Input in shifted coordinates | Output | Original steps | Halvings |
|---|---|---:|---:|
| $4\mid y$ | $sy$ | 3 | 2 |
| $y$ odd | $y/2+3/2$ | 1 | 1 |
| $y\equiv2\pmod4$ | $y/2+3$ | 2 | 1 |

Call the first block an expansion and the other two exits. A **run** consists of all consecutive expansions and the next exit, allowing zero expansions. If $y=2^{2k+b}u$, with $u$ odd and $b\in\{0,1\}$, its exact run map is $G(y)=2^{b-1}(5^ku+3)$. At exit $i$, let $K_i$ count all expansions so far, $h_i=2K_i+i$ the raw halvings, $Y_i$ the shifted height, and $P_i=s^{K_i}2^{-i}$ the slope. With $Y_0=y$, $P_0=1$, the affine recurrence gives

$$
Y_i=P_i\left(y+\sum_{j=1}^i\frac{\beta_j}{P_j}\right),
\qquad \beta_j\in\{3/2,3\}.
\tag{1}
$$

For **bit time**, initialize $(z,f)=(y,0)$ and read the parity of $z$. A one sends $z\mapsto(z+3)/2$ and keeps the flag $f$. A zero sends $z\mapsto5^fz/2$ and toggles the flag. After $j$ bits the shifted block-boundary height is $2^{f_j}z_j$, with $j-f_j$ completed halvings. Writing $A_j$ for the number of zeros read with entry flag one, the raw multiplier there is $5^{A_j}/2^{j-f_j}$. For each entry flag, bit words of length $j$ are in bijection with residues of the initial $z\bmod 2^j$. The two lifts of any residue give opposite next parities because the numerator multiplier is odd. This distinction between bits, runs and halvings matters even in exact finite counts. [Bit and run checks](check_split5_3_recovery.py)

Throughout, set

$$
\kappa=1/\log_2s,\quad T=2\kappa+1,\quad \tau=1/T,\quad
q=1-2/\log_2 5,\quad H=H_{\rm bin}(q)=0.5806841231\ldots,
$$

where $H_{\rm bin}(u)=-u\log_2u-(1-u)\log_2(1-u)$. In this map $q=\tau$. The notation distinguishes a frequency of ones from the reciprocal number of halvings per near-critical run. Unsubscripted logarithms below are natural.

## 2. What is known for ordinary positive starts

| Result | Precise conclusion | Status, checker and review |
|---|---|---|
| Seed and cycles | The orbit of 27 first enters the cycle through 3 at 6 after eight steps. The cycle minima known on the positive integers are $1,3,5,61,125$. The fixed points of $G$ are exactly $4,6,8,64,128$, by the equation $u(2\cdot4^k-5^k)=3$. Every further cycle has more than one run-map height. | Exact. The original census referee confirmed the seed. Codex gave the fixed-point argument. [Seed checker](../../checks/split5_3_s27.py) · [Run checker](check_split5_3_runs.py) |
| Finite convergence | Every $1\le n<2^{66}$ reaches one of those cycles. Every corresponding $y$ crosses the weighted bit threshold of §3 by bit 146. The maximum 146 is attained at $y=19{,}469{,}588{,}806{,}135{,}160{,}832$. | Computational theorem. Independent height-based and weighted-prefix implementations cover the full range. The height verifier counted $2^{66}-1$ starts, 6,667,755,247 tree nodes and 1,887,286,712 individual checks. Archived runs, with no full-range rerun for this write-up. [Height verifier](check_split5_3_range.cpp) · [Prefix verifier](check_split5_3_prefix.cpp) |
| Necessary size of a further cycle | Its primitive period has at least 201 maximal **nonempty** expansion runs, more than six billion exits including those preceded by zero expansions, and more than $61{,}800{,}000{,}000$ original steps. For $y\ge2^{66}$ the first $P_i<1$ and first $Y_i<y$ coincide through six billion complete runs, including absence of both. The earlier version uses $y\ge2^{64}$ and three billion runs. | Author proof using the range certificate, rational separation and, for the 201 bound, Matveev. No separate Fable review recorded. [Cycle constants](check_split5_3_cycles.py) · [Crossing constants](check_split5_3_recovery.py) |
| Descent certificates | At modulus cap $2^{32}$, every start outside 4,775 open classes and the five cycle minima drops below itself. The classes have total density $4775/2^{32}$. The least escaping start, every unknown cycle minimum and infinitely many points on each escaping orbit must lie in these classes. No fixed finite table of bounded-time descent certificates suffices. The 2-adic branch through $-3$ never closes, and the limiting open set contains a Cantor set. | Finite certificate and structural proof confirmed by the round-2 referee, who supplied the Cantor construction. The starts $4^K-3$ grow for $K$ expansion blocks to $5^K-3$. These unbounded growth factors also rule out a strictly decreasing $n\,w(n\bmod M)$ with positive weights. [Round-2 referee record](split5_3_s27.md#referee-round-2) · [Checker](check_split5_3_s27.py) |
| Merging classes | Two starts merge if they have a common future value. Each class meets every progression containing an integer of its divisibility type modulo 3, and meets no incompatible progression. For each compatible class and progression the count up to $X$ is at least $cX^v$ for large $X$, where $c>0$ depends on both and $4^{-v}+(1024/5)^{-v}=1$. A finite-valued orbit-invariant function is automatic in some integer base exactly when it depends only on divisibility by 3. The individual basins of $1,5,61,125$ are nonautomatic in every base. On multiples of 3, $n=3u$ gives the conjugate map $u/2,u+1,5u+1$ on even, $1\bmod4,3\bmod4$ inputs respectively. | Repository proof. The original census referee recorded the conjugacy. The basin through 3 is automatic exactly when it equals all positive multiples of 3. No Fable review of the progression or automata proof recorded. [Proof](split5_3_components.md) · [Checker](check_split5_3_components.py) |
| Smaller ancestors | Every positive $n\equiv311\pmod{625}$ has a smaller ancestor. If $n=4^K u-3, K\ge2, 5^Ku\equiv1\pmod8$, then $(n-3)/2$ merges with $n$. For $u=1, K\ge3$, four symbolic comparisons certify 46,055 of 65,536 exponent residues modulo $2^{16}$, including every even exponent. For each fixed maximal $K\ge3$ they certify 119,511 of 196,608 cofactor residues modulo $2^{18}$ with $4\nmid u$. For any fixed post-peak depth arbitrarily large exponents evade those four comparisons. | Author proof and finite symbolic certificate. These eliminate possible *least* counterexamples. No Fable review recorded. [Rising-family checker](check_split5_3_rising.py) |
| Bounded local searches | For each fixed depth $D$ there are arbitrarily large starts for which no smaller start merges within $D$ blocks on both paths. For each fixed $D$ the lower relative density within $n\equiv-3\pmod{4^D}$ exceeds $3/4$. For $D\ge40$, more than three quarters of the $4^D$ starts congruent to $-3\bmod 4^D$ in $[16^D,2\cdot16^D)$ have this property. | Author proof and finite arithmetic checks. No Fable review recorded. [Merger checker](check_split5_3_escape.py) |
| Smooth heights | For fixed finite primes $S$ and fixed $d\ge1$, only finitely many $y\ge4$ have both $y,G^d(y)$ supported on $S$. Eventual periodicity of a given orbit is equivalent to infinitely many such pairs on it at bounded positive gaps for some finite $S$. For $S=\{2,3,5\}, d=1$, the possible $y$ are exactly $4,5,6,8,9,10,12,15,18,24,27,30,36,45,54,64,72,80,90,100,125,128,160,200,250$. All reach a known cycle. In particular $G(4^K)$ is 5-smooth exactly for $K=1,3$ among $K\ge1$. For fixed $h$ and $S$ containing 2, none of $G(4^K),\ldots,G^h(4^K)$ is $S$-smooth for all sufficiently large $K$. Encountering one adjacent 5-smooth pair is equivalent to reaching one of the five. | Author proof using the unit-equation finiteness theorem and a published enumeration. No Fable review recorded. [Smooth-pair checker](check_split5_3_runs.py) |
| Recovery after growth | The exact initial streak of runs with $(k,b)=(4,0)$ has length $\lfloor v_2(113y+768)/9\rfloor$. In each interval of $2^{10D}$ consecutive shifted starts above $6D2^{10D}$, precisely $2^D$ have at least $D$ such initial runs. Among these, the first descent takes $(g/(w-2v)\pm\epsilon)D$ additional runs outside a fraction $O_\epsilon(e^{-c_\epsilon D})$. The proportion surviving $D$ additional **bits** is $2^{-[1-H_{\rm bin}((g+v)/w)+o(1)]D}$, with $g=\log(625/512),v=\log(\sqrt5/2),w=(\log5)/2$. | Author proof, no Fable review recorded. The run-time coefficient is $0.342908\ldots$, the survival exponent $0.037517\ldots$. [Streak checker](check_split5_3_runs.py) · [Recovery checker](check_split5_3_recovery.py) |

In the rising family, the four-expansion ancestor also covers $K\equiv53\pmod{250}$. Exact iteration gave strict descent for every $2\le K\le2000$ except $K=3$. The assertion for every $K\ge4$ is open. [Rising-family record](split5_3_s27.md#the-rising-family)

The two range proofs allow strong induction on the starting integer. One partitions residue classes until every member drops or the remaining exceptions can be iterated individually. The other certifies a multiplier crossing, then uses the first-crossing theorem to turn it into actual descent above the previously verified range. To bound a further cycle, start a lap at its least run-boundary height. Its lap slope is strictly below one by $1$. A first slope crossing within the certified window would give a smaller height on that same lap. [Range and period proofs](split5_3_s27.md#verification-through-66-bits)

## 3. Equivalent global tests and counts up to the binary length

**Multipliers on an escaping orbit.** In the raw map put $M_t=5^{a_t}/2^{l_t}$, with $a_t$ expanding odd steps and $l_t$ halvings before time $t$. On every orbit that never repeats,

$$
1\le F^t(n)/(n M_t)<1.000073
$$

and the ratio has a finite limit. Thus $M_t\to\infty$ on escape and $M_t\to0$ on an eventually periodic orbit. At run boundaries $K_i-\kappa i$ tends respectively to $+\infty$ and $-\infty$. Every late expansion count at most three implies convergence to a known cycle. For the least escaping start $n$, every raw time $t$ and $h\ge0$ satisfy $2^h M_t(4/5)^{v_5(2^h F^t(n)+3)}>1/1.000073$. The multiplier estimate follows by bounding visits to small heights and summing the additive corrections. Fable read the occupation argument and accepted its logic as an input to the chain theorem. Fable did not re-derive its numerical constants. [Occupation and arithmetic checks](check_split5_3_escape.py) · [Derivation](split5_3_s27.md#how-accurately-the-multipliers-would-track-a-divergent-orbit)

**Prefix theorem.** Let $u_j$ be the number of ones in the first $j$ bits from $(y,0)$. Global eventual periodicity holds if and only if every ordinary $y\ge4$ has some $j\ge1$ with $u_j>qj$, equivalently $5^{j-u_j}<4^j$. Indeed, weighting the flag by using $w=5^{f/2}z$ gives bit multiplier $(\sqrt5/2)^j5^{-u_j/2}$. On a periodic tail the raw multiplier tends to zero. On an escape, restart at the least run-boundary multiplier on a tail. All future run multipliers from that integer are at least one, and the weighted bit multiplier stays at least one in between. This restarting step explains the universal quantifier over starts.

If $A_j$ counts words with $u_i\le qi$ at every $i\le j$, exactly $A_j$ integers pass in every interval of length $2^j$, and $A_j=\Theta(2^{Hj}j^{-3/2})$. In fact $A_0=1$ and $j A_j=\sum_{i=1}^j B_i A_{j-i}$, where $B_i=\sum_{k\le qi}\binom ik$. The infinite prefix set in $\mathbb Z_2$ has Hausdorff dimension $H$ and zero $H$-dimensional measure. For the actual-height test over the first $m$ bits the count in $2^m\le y<2^{m+1}$ is also $\Theta(2^{Hm}m^{-3/2})$. Consequently at most $O(X^H/(\log X)^{3/2})$ positive starts up to $X$ never descend below themselves. Author proof, with a separate round-3 derivation of the descent-tree dimension. The round-3 referee confirmed the split-map dimension specialization using **census/round3/deep/check_omega.py** and **referee_check.py**. Fable explicitly took the earlier prefix-count theorem as input in the two-ended review. [Count recurrences](check_split5_3_prefix.py) · [Prefix and dimension proof](split5_3_s27.md#an-exact-prefix-criterion-for-all-positive-starts)

The earlier two-state descent proof also gives an explicit estimate before optimizing the exponent. At each binary update of the unshifted map, state U reads parity and waits if the height is odd. State O resolves that odd branch, returning to U after $(5n+3)/4$ and remaining in O after $(n+3)/2$. An even input in U halves and remains in U. Along a nonrepeating orbit the count $V_U(2^j)$ of positions in either state with height at most $2^j$ satisfies

$$
V_U(2^j)\log2\le\tfrac94(3/2)^j+24(5/4)^j(1+j\log2).
$$

This is the occupation estimate used for the multiplier constant above. The corresponding elementary bound for starts that never descend is $O(X^{\log_2(3/2)})$, sharpened by the prefix theorem.

**Occupation and complexity.** On one escaping orbit the number of weighted bit positions with $w\le X$ is $O(X^H/\sqrt{\log X})$. At run times put $E_i=K_i-\kappa i$, $c_0=1/(H\log s)$. The fraction of $2\le i\le N$ with $E_i\le c_0\log i$ is $O_y(1/\sqrt{\log N})$, and remains of density zero with $d\log\log i$ added for any $d<c_0/2$. If $p(j)$ counts distinct length-$j$ factors of the bit word, escape requires $\liminf p(j)/j\ge\kappa$. If also $K_i/i\to\kappa$, then $p(j)/j\to\infty$. Author proofs. Fable’s limited review of the earlier occupation estimate is described above. [Occupation proof](split5_3_s27.md#counting-visits-on-one-divergent-orbit) · [Prefix checker](check_split5_3_prefix.py)

**Ordinary integers inside the 2-adic coding.** For an infinite word $e_0e_1\ldots$, define $a_i=\lfloor(i-\sum_{j<i}e_j)/2\rfloor$ and $S=\sum_{i\ge0}e_i2^i/5^{a_i}$. Its unique 2-adic start is $-3S$ in $\mathbb Q_2$. Global eventual periodicity is equivalent to excluding all ordinary $y\ge4$ from these values for words whose series also converges in the reals. Eventual periodicity of such a *word* gives the same rational sum in both completions and hence $y\le0$. More generally, agreement for $j$ bits with $N/D\le0$, $D>0$ odd, forces $Dy+|N|\ge2^j$. This excludes infinite passing words beginning with $WW$ for arbitrarily long $W$ having an even number of zeros. Author proof, no Fable review recorded for this equivalence. [Inverse series and arithmetic argument](split5_3_s27.md#the-ordinary-integer-obstruction) · [Bit checker](check_split5_3_prefix.py)

## 4. Actual stopping times and the two ends of a word

Let $N_m(b)$ count $2^m\le n<2^{m+1}$ whose raw orbit stays at least $n$ up to and including its $b$th halving. Let $P(b)$ be the probability of the corresponding **multiplier** test under uniform binary residues of the shifted start. Define $D=b+1$, $Q=2^D$. The cumulative count $N_{\le X}(b)$ uses $1\le n\le X$ instead. The following results use three different operations on the same words.

1. **Restarting at a tail minimum** (54ff27e). If one positive orbit escapes, then for every sufficiently large $X$ and every $b$, $N_{\le X}(b)\ge\kappa\log_2 X-O(1)$, with the constant depending on that orbit. Every sufficiently late octave contains at least three permanent survivors. To see this, take successive raw tail minima $n_i>3$. Each must expand first, since either other block would descend. Thus $n_{i+1}+3\le s(n_i+3)$. Counting minima gives the first inequality. Starting from the last minimum below $2^m$ gives the second because $s^3<2$. Consequently either $\liminf_m N_{\le2^m}(b_m)/m<\kappa$ or $N_m(b_m)\le2$ infinitely often suffices at **any** chosen depths $b_m$. Author proof, re-derived independently by Fable. No dedicated checker for the implication. [Tail-minimum proof](../../../output/tex/stopping_time_applications.tex)

2. **Testing a word exactly** (8830ba6). For every fixed $K>0$, all sufficiently large $m$, all integers $1\le b\le Km$ and all starts in the octave, actual survival is equivalent to

   $$
   5^{A_j}\ge2^{j-f_j}\qquad(0\le j\le b+1,\ j-f_j\le b).
   $$

   On a surviving path the relative correction to the raw slope is at most $(1+3/n)^{b+1}$. Matveev separates a slope below one from one by at least an inverse power of $1+b$. This exceeds the correction in a large octave. A partial final expansion cannot create a first drop. Independently of location, at $b=\lceil12m/5\rceil$ the following restriction applies to actual survivors in the octave. Fix $J\ge1$ and a positive integer function $p(b)=o(b)$. The upper limit of the fraction of the first $b$ bits covered by at most $J$ disjoint intervals of periods at most $p(b)$ is at most $1-7/(6\log_2 5)=0.4975440\ldots$. The lower limit of the fraction of all positions occupied by uncovered zeros is at least $2/\log_2 5-1+7/(6\log_2 5)$. Grouping a repeated affine block into two endpoint terms keeps the number of terms bounded in Evertse’s inequality. The unrestricted gaps pay for their total length. Author proofs. Fable discussed both reductions and explicitly left the Matveev and Evertse citations unchecked. No separate full referee sign-off on this commit. [Derivation](split5_3_s27.md#a-restriction-on-survivors-at-the-two-survivor-depth) · [Finite clock checks](check_split5_3_microrange.py)

3. **Counting residues in an ordinary octave** (d62a46f and f745a3bc). Put $H_2=-\log_2((1-q)^2+q^2)$ and $c_*=H/2+H_2/\log_2 5=0.45991803957\ldots$. For fixed $0<\eta<c_*$ and large $M$, all but $O_\eta(M^{1-\eta/4})$ integers $m\in[M,2M)$ satisfy, simultaneously for every integer $1\le b\le m+(c_*-\eta)\log_2 m$,

   $$
   N_m(b)=2^m P(b)\bigl(1+O_\eta(M^{-\eta/2})\bigr).
   $$

   When $D\le m$ the count is exactly the predictor for large $m$ by complete periods. The earlier one-ended result has coefficient $H/2$, exceptional count $O_\eta(M^{1-\eta/3})$ and relative error $O_\eta(M^{-\eta/3})$ for $0<\eta<H/2$. The additional $H_2/\log_2 5$ comes from retaining the signs of the initial phases. One averages a five-adic second moment at the beginning and a binary second moment at the end, combines them by Cauchy–Schwarz, and applies Erdős–Turán. This argument requires no independence between the two ends as depth varies. Fable reviewed the prefix-group weights, both second moments, their combination and the discrepancy argument of f745a3bc. The earlier prefix-count theorem and external citations were taken as inputs. The one-ended result has an author proof. [One-ended checker](check_split5_3_microrange.py) · [Two-ended checker](check_split5_3_two_ends.py) · [Two-ended proof](split5_3_s27.md#cancellation-from-both-ends-of-a-passing-word)

**Earlier uniform one-digit estimate.** In the round-5 digit-tree convention, let $R_j$ consist of raw input residues modulo $2^j$ whose slope stays at least one through every step decided by those $j$ digits. For every $j\ge16$, the number of these residues in $[0,2^{j-1})$ differs from $|R_j|/2$ by at most $(17/25)|R_j|/2$. Here the cutoff is the last decided step. The bound holds at every depth and has a fixed relative error. Round-5 Fourier Theorem U′ and its second project referee report give the proof and exact constant. The independent finite checker is **census/round5/fourier/referee2_check.py**.

**Finite evidence at the target.** At $D=40,m=16$ there are 126,604 passing words and zero shifted representatives in the octave. The exact uniform prediction is $126604/2^{24}=0.007546\ldots$. The same grid checker gives zero **multiplier** hits at target depths for $1\le m\le16$ and six hits at the shorter control depth $D=26,m=18$. Independently, Fable reported zero **actual-height** survivors for $7\le m\le35$ from the round-4 finite census, with one at $m=6$ (125). The archived actual-height checker **census/round4/lead/survive.c** tabulates $\sigma\ge j$ for the halving of first strict drop $\sigma$. Survival through $b$ uses column $j=b+1$. The corresponding $m=6,\ldots,35$ entries were checked against **s53.txt** for this report. Fable’s predictor used complete-block endpoint masses at depths $b,b-1$ to approximate the cutoff. The halving-clock recurrence also includes paths partway through their final expanding block, giving, for example, a predictor of $0.01416015625$ at $m=8$. The actual finite enumeration and the asymptotic ordinary-integer problem are separate statements. [Grid checker](check_split5_3_grid.py) · [Halving-clock recurrence](check_split5_3_microrange.py)

## 5. Links between consecutive permanent survivors

On a putative escape consider the product of block slopes at each boundary. It tends to infinity. Take the unique minimum on the whole tail, discard that boundary and everything before it, and repeat. Denote the successive shifted heights by $y,y',\ldots$. The ratios of products at distinct boundaries cannot be one, and (1) shows the ratio of height to slope is nondecreasing. Each selected start therefore survives forever in both height and raw slope. This selects a particular chain. Its finite segments can also occur on trajectories that eventually descend.

| Result | Statement | Status, review and checker |
|---|---|---|
| Chain theorem (04a59aa) | Each selected $y$ is divisible by 256. A link with $e$ exits has $a=\lfloor\kappa e\rfloor+1$ expansions, slope $r=s^a2^{-e}\in(1,s]$ and $h=2a+e$ halvings. For $e=0$ it is one expansion. For $e>0$ the link ends at an exit and $3/2\le y'-ry\le3e$. For each fixed $L\ge1$, every sufficiently late $[2^m,2^{m+L})$ contains at least $\lfloor\kappa L\rfloor$ selected **unshifted** starts. Thus $\sum_{j=m}^{m+9}N_j(\lceil12j/5\rceil)\le30$ infinitely often also suffices. | Codex proof, Fable re-derived all parts given the multiplier theorem. The first exit needs four expansions. The normalized height has a positive finite limit, giving the octave count. [Proof](split5_3_s27.md#arithmetic-links-between-permanent-survivors) · [Grid experiment](check_split5_3_grid.py) |
| Sharp strip (d2ff4f2) | For any finite link with $e\ge1$, require every nonempty proper prefix to have slope strictly greater than its terminal $1<r\le s$. The exact extrema of $R=y'-ry$ are $L_e=3(1-2^{-e})$ and $U_e=3\sum_{k=0}^{e-1}s^{-\{\kappa k\}}$. Both occur for arbitrarily large starts even with $256\mid y,y'$. The first $e$ with $U_e-L_e\ge256$ is 97. | Codex proof, Fable re-derived bounds, attaining schedules and lifts. [Sharp-strip checker](check_split5_3_link_strip.py) |
| Extremizers and departures (d2ff4f2) | Put $b_i=a-\lfloor\kappa(e-i)\rfloor$, $\theta_i=\{\kappa(e-i)\}$. The minimum forces $K_i=a,\ \beta_i=3/2$ at all exits, the maximum $K_i=b_i,\ \beta_i=3$. The former has $h\le(1+1/(2\kappa))\log_2 y$, the latter $h\le2\log_2 y+O(1)$. On escape let $d=\lceil(\log_2 y+4)/T\rceil$ and $D_0$ count exits deviating from the maximizing pair. For large $y$, $D_0\ge\max(0,(e-2d-1)/(d+1))$ and $U_e-R\ge(12/25)D_0$. | Codex proof, Fable reviewed the two cutoffs and deficit inequality. The next theorem sharpens the maximizing cutoff. [Strip and schedule checker](check_split5_3_link_strip.py) |

Here $\{x\}$ denotes fractional part. All strip claims follow from $R=\sum_i\beta_i r/P_i$ and $b_i\le K_i\le a$. Attaining the upper bound fixes a run schedule in which consecutive expansion counts differ according to an irrational rotation. The number of possible lists of $d$ successive ordinary runs on that schedule is $d+1$. Specifying the list and its labels forces the starting height into a binary residue class. This is the source of both the cutoff arguments and their limitations.

## 6. Which long links can be excluded?

The uniform cutoffs in this section apply to ordinary positive starts. They need no assumption that the orbit escapes. Throughout, “bounded” means bounded independently of the start and segment length.

**Bounded departures from the maximizing schedule (820585e).** Put $K_i=b_i+u_i$. Fix integers $B,J\ge1$. Suppose $|u_i|\le B$ and the exit indices split into at most $J$ consecutive pieces. On each piece $(u_i,\beta_i)$ must be constant on each of at most $J$ arcs of $\theta_i$. Then for each $\eta>0$, $h<(1+\eta)\log_2 y$ for all sufficiently large $y$. This includes changing one exit type, moving one expansion earlier and repaying it later, and concatenating a bounded number of such links, including a truncated final link. The leading coefficient one is sharp by integer lifts. If arbitrary labels are permitted on at most $J$ additional intervals covering $L$ exits, with the displacement still bounded, then $h/\log_2 y\to c>1$ finite implies $\liminf L/e\ge1-1/c$. At $c=12/5$ the fraction is $7/12$. This measures the length of an interval cover. Scattered individual defects need not have that density.

The proof translates a trajectory by an almost-return of the rotation. Away from the finitely many phase cuts its affine difference has zero forcing. Group the remaining corrections and apply Evertse to the resulting divisible integer sum. Codex proof. Fable independently reviewed the differences, nonvanishing condition, order of limits, sharpness and extensions. [Shifted-path checker](check_split5_3_shifted_links.py) · [Proof](split5_3_s27.md#a-sharp-cutoff-for-the-single-departure-families)

**Unbounded offsets and successive rates (a2dbef3).** Consider any path of complete blocks whose relative slope is at least one at *every* block boundary. Allow an ending partway through an expansion run. Suppose the exits split into at most $J$ pieces. On a piece of the first kind,

$$
K_i=c-\lfloor t-\omega i\rfloor+w_i,\qquad |w_i|\le B .
$$

Here $c\in\mathbb Z$, $t\in\mathbb R$, $\omega\ge0$ may change between pieces and have no size bounds. The pair $(w_i,\beta_i)$ is constant on each of at most $J$ arcs of $\{t-\omega i\}$. On a piece of the second kind $K_i$ is constant and the exits may take any legal labels. Again $h<(1+\eta)\log_2 y$ uniformly for sufficiently large $y$ with fixed $B,J,\eta>0$. This includes arbitrarily large initial or internal jumps and pieces shorter than the translating shift. The same cutoff allows a bounded number of additional pieces whose pairs (expansions since the preceding exit, exit type) have bounded period and bounded expansion counts. Their sums are geometric on residue classes within the period. On a constant-$K$ piece legality forces a string of $3/2$ exits followed by a string of $3$ exits. Translating the whole sum (1) retains the short pieces, and each constant-label string sums geometrically. Legal lifts with growing excursions attain limiting coefficient one.

In the near-critical version one may use a bounded number of cuts in each of two phases $\{t-\kappa i\}$, $\{t'-\omega i\}$ at the same site if $a\omega+b\kappa+c=0$ for bounded integers $a,b,c$ with $a\ne0$. Shifts divisible by $|a|$ control both displacements. Codex proved the whole-prefix and varying-rate results. Fable reviewed both, and supplied the bounded-relation extension, subsequently incorporated by Codex. Independent simultaneous phases with arbitrary labels remain outside this argument. [Excursion checker](check_split5_3_excursions.py) · [Proof](split5_3_s27.md#large-jumps-and-stretches-of-consecutive-exits)

## 7. The near-critical schedule with freely chosen exit types

For this section fix the length $e$ and the exact expansion schedule $K_i=b_i$ from §5. Write $\beta_i=3(1+\epsilon_i)/2$ with $\epsilon_i\in\{0,1\}$. Then $P_i=r s^{\theta_i}$ for $i\ge1$, $1\le P_i\le s^2$, $h_v-h_u=T(v-u)+O(1)$ and $h=h_e=Te+O(1)$. Every one of the $2^e$ words has arbitrarily large legal integer lifts, even with $256\mid Y_e$. The question concerns the *size* of those lifts.

**Forward coding, reverse coding and separation (517c32a).** The word gives $y\equiv-\sum_i\beta_i/P_i\pmod {2^h}$, reducing rationals of odd denominator in the binary residue ring. If two words first differ at exit $i$, their residues first differ at bit $h_i-1$, numbering from zero. Conversely, if $k_i=K_i-K_{i-1}$, then $2Y_i\equiv3(1+\epsilon_i)\pmod{5^{k_i}}$ determines the label already modulo 5 and $Y_{i-1}=4^{k_i}(2Y_i-3(1+\epsilon_i))/5^{k_i}$ determines the predecessor. Hence two distinct starts cannot merge at the same exit index. If distinct $y,z$ have labels agreeing on a union of at most $J$ intervals of total length $L$, then

$$
\log_2|y-z|\ge TL-o(e)
$$

uniformly for fixed $J$. One applies Evertse to the difference of (1), grouping the complementary gaps. In an interval of width $2^m$, $m<h$, at most $2^{m/T+O(1)}$ label words can occur, since only that many low-digit prefixes are possible. At $h=12m/5+O(1)$ the represented fraction is at most $2^{-7e/12+O(1)}$. For the successive prefixes of one infinite fair label string, let $y_e$ be the least positive lift with $256\mid Y_e$ on the length-$e$ schedule. Then $\log_2 y_e/h\to1$ almost surely by summability. Fable reviewed both decodings and the separation proof. [Decoding and separation checker](check_split5_3_free_labels.py) · [Proof](split5_3_s27.md#what-the-two-ends-determine-for-arbitrary-labels)

**Two complementary halves (517c32a).** For $e=2p$, choose a most frequent value $k$ of $K_{i+p}-K_i$ on $1\le i\le p$. Where the difference equals $k$, choose $\epsilon_i$ freely and put $\epsilon_{i+p}=1-\epsilon_i$. Elsewhere fix the pair to $(0,1)$. The resulting family contains at least $2^{p/2}$ words, which all satisfy $h\le(2+o(1))\log_2 y$. For infinitely many $p$ the same bound holds for all $2^p$ complementary words. Superposing the two halves makes their additive term constant on matched sites and a bounded phase function on the remaining sites in the first construction. At record denominators there are only boundedly many exceptional positions, so all first-half labels can be free. Fable reviewed the virtual recurrence, including its $9/2$ correction on matched sites. [Checker](check_split5_3_free_labels.py) · [Proof](split5_3_s27.md#complementary-labels-in-two-halves)

**Length with no label condition (93a20e4).** For some absolute $\sigma>0$, every such path has $e=O(y^{1-\sigma})$. One may take $\sigma=1/(B+1)$ when $B\ge2$ satisfies $\|j\kappa\|\gg j^{-B}$, with $\|\cdot\|$ distance to the nearest integer. With distinct post-exit heights, $e=O(y^\tau\log y)$. For every start the latter bound holds outside at most $O(\log(M+2))$ octaves among $m\le M$. Indeed $d=\lceil(\log_2 y+4)/T\rceil$ following runs have at most $(d+1)2^d$ labelled lists, and each determines its start modulo at least $4y$. An early repetition forces a periodic lap. If it has $p$ exits and $k$ expansions then $0<\kappa p-k\asymp p/y$. Repeating the lap forces an empty arc of the rotation, which bounds the length by $O(y/b)$ for $b$ the reduced denominator of $k/p$. Matveev bounds $b$ from below. Distinct exceptional scales $X=|\kappa-k/p|^{-1}$ grow beyond fourth powers for large $X$. Fable reviewed the distinct and repeated cases, including the exceptional-octave count. [Rotation and repeated-lap checker](check_split5_3_multishift.py) · [Proof](split5_3_s27.md#a-length-bound-allowing-every-exit-label)

**Several shifts and a sharp limitation of separation (93a20e4).** Take boundedly many shifts $0=q_0<\cdots<q_r<e$ and bounded nonzero integer coefficients $c_j$. For each $j$ choose $k_j$ from the two adjacent possible values of $K_{i+q_j}-K_i$ for $i\ge1$, with $k_0=0$. Put

$$
n_*=e-q_r,\quad v_{ij}=K_{i+q_j}-K_i-k_j,\quad
G_*=\sum_j c_j s^{k_j}2^{-q_j},\quad
b_i^*=\sum_j c_j s^{-v_{ij}}\beta_{i+q_j}.
$$

If $G_*\ne0$, $h\asymp\log_2 y$, and $b_i^*$ is piecewise constant on boundedly many time intervals and arcs of $\theta_i$ apart from boundedly many intervals of total length $L$ in $1\le i\le n_*$, then $T(n_*-L)\le\log_2 y+o(e)$. In particular $q_r+L\le(7/12-\eta)e$ excludes target depth for fixed $\eta>0$. For record denominators $p$ of $\|p\kappa\|$ there are $3^p$ words of length $6p$ with $h\le(3/2+o(1))\log_2 y$. Choose one of $100,010,001$ in each column $j,j+p,j+2p$, $1\le j\le p$, then repeat the three rows.

There is also an explicit family of $2^{(5/12)e-O(\log e)}$ binary words at target depth with *assigned* integers in one octave. They satisfy the first-differing-bit valuation and $\log_2|y-z|\ge TL-O((J+1)\log e)$ on unions of at most $J$ agreement intervals. Polynomial evaluation over a binary field supplies these assignments. They are examples for the coding inequalities alone. Fable previously gave a random-word example of every exponential rate below $5/24$ for the agreement condition. Fable reviewed the weighted-shift theorem, the three-shift example and the full-rate construction, taking Evertse as cited. [Multi-shift and code checker](check_split5_3_multishift.py) · [Proof](split5_3_s27.md#what-a-sum-of-several-shifted-paths-proves)

## 8. How many ordinary integers realize a list of runs?

**Status of eab6fc9. Codex supplied the proof and checker. Fable has not independently refereed this result.** This status applies to the discrepancy estimate, count law, target-depth corollary and path-length consequences below.

For $d\ge1$ let $\mathcal L_d$ consist of the $d+1$ expansion lists with $K_j=-\lfloor t-\kappa j\rfloor$, $0\le t<1$, $1\le j\le d$, $K_0=0$. A second convention adds one expansion to the first run. For either convention take one list $\ell$, write $h(\ell)=2K_d+d$, and let $N_I(\ell)$ count shifted starts in an interval $I$ following the list with any legal labels.

1. **Exact measure.** There are $3\cdot2^{d-1}$ legal residues modulo $2^{h(\ell)+1}$. The first $d-1$ labels are unrestricted. The final pair (exit constant, output parity) is $(3/2,0),(3/2,1)$ or $(3,0)$. Thus the exact full-period density is $(3/4)2^{d-h(\ell)}$. If $\Delta_d$ denotes the maximum circular interval discrepancy of the normalized residue measures over lists of both conventions, the proof gives $\mathbb E_{M\le d<2M}\Delta_d\ll M^{-\tau}(\log M)^{O(1)}$.
2. **Uniform interval count.** Fix $0<\eta<\tau$. Apart from $O_\eta(M^{1-\eta/4})$ exponents $m\in[M,2M)$, simultaneously for all lists of either convention with $Td\le m+(\tau-\eta)\log_2m$ and every interval of $X$ consecutive positive shifted integers, $2^m\le X<2^{m+1}$,

   $$
   N_I(\ell)=\tfrac34 X\,2^{d-h(\ell)}(1+O_\eta(M^{-\eta/2})).
   $$

   Within each convention the lists are disjoint as sets of starts, so their predictors add with the same relative error. To get the discrepancy, split off the first and last $\lfloor\tau\log_2 M\rfloor$ labels and average their Fourier factors over depths. The separation of head sums modulo powers of five and tail sums modulo powers of two is used only over complete periods.
3. **At the proposed depth.** Fix $\varepsilon>0$. For $Td_2=12m/5+O(1)$, on a density-one set of exponents the upper bound for a *single* target list is $O_\varepsilon(2^{\tau m}m^{-\tau(1-\tau)+\varepsilon})$. For the union of all lists under one convention multiply this bound by $O(m)$. This is obtained by counting a shorter prefix. It is an upper bound at target depth, while the asymptotic formula above holds at the shorter depth.
4. **Transfer to a path.** On the exact schedule of §7, if its post-exit heights are distinct, $e\le d+F(y,d)$ for every $d$, where $F$ counts heights in $[y,2y)$ following a list in $\mathcal L_d$ with arbitrary labels (for sufficiently large $y$). Fable supplied this transfer after reviewing 93a20e4. Codex then used $P_i=r s^{\theta_i}$ to localize the heights following each list to a shorter interval determined by its phase cell. With $m=\lfloor\log_2 y\rfloor$ this gives $e\ll y^\tau m^{1-\tau}$ for distinct heights in **every** octave. On a density-one set of exponents, **every** start on this schedule satisfies $e\ll_\varepsilon y^\tau m^{(1-\tau)^2+\varepsilon}$, including the repeated-height case by §7.

The checker verifies complete small residue systems, Fourier factorization in a prime field and phase localization on integer trajectories. In the single-list bound the saving is a power of $m$, with $\tau(1-\tau)=0.1194239\ldots$. The remaining factor $2^{\tau m}$ is a power of the starting height. [Family-count checker](check_split5_3_family_count.py) · [Author proof](split5_3_s27.md#a-typical-octave-count-for-freely-labelled-near-critical-runs)

## 9. External inputs and audit trail

The following four inputs are **cited, not re-verified**. Fable’s reviews concern deductions within the project. None constitutes independent verification of the external theorem statements, constants or bibliographic formulations. The checks run for this write-up concern the repository’s exact computations.

| External input | Form used here |
|---|---|
| Evertse, Theorem 2, equation (14), p. 228 | For a fixed number of nonzero integer terms $x_i$ having no nonempty vanishing subsum, set $r(x)=\lvert x\rvert\lvert x\rvert_2\lvert x\rvert_5$. For each $\epsilon>0$, $(\prod_i r(x_i))\lvert\sum_i x_i\rvert_2\gg_\epsilon\max_i\lvert x_i\rvert_2(\max_i\lvert x_i\rvert)^{-\epsilon}$, with dependence also on the number of terms. The real-place version controls the nonzero leading coefficient for signed virtual paths. [On sums of S-units and linear recurrences](https://www.numdam.org/item/CM_1984__53_2_225_0.pdf) |
| Matveev, linear forms in logarithms | Separation of distinct powers of 2 and 5. The cycle proof uses explicit constants. The asymptotic applications use an inverse-polynomial lower bound for the gap and a finite irrationality exponent for $\kappa$. [Matveev, 2000](https://doi.org/10.1070/IM2000v064n06ABEH000314) |
| Erdős–Turán discrepancy inequality | Bounds interval discrepancy by a reciprocal frequency cutoff and a weighted sum of absolute Fourier coefficients. Used after the signed decompositions and averaging in §§4 and 8. [Montgomery and Vaughan, Theorem F.4](https://personal.science.psu.edu/rcv4/571s25/montgomery-vaughanII.pdf) |
| Sanders, quantitative idempotent theorem | An integer-valued function on a finite cyclic group of bounded Fourier algebra norm has a decomposition into a bounded number of signed coset indicators, uniformly in group order. Used for the sharp-interval obstruction in §11. [Bounds in Cohen’s Idempotent Theorem](https://arxiv.org/abs/1610.07092) |

Earlier results also use the Sparre Andersen fluctuation identity for the prefix recurrence, the Evertse–Schlickewei–Schmidt finite-rank unit-equation theorem for smooth pairs, the enumeration of primitive smooth triples by von Känel and Matschke, and Cobham’s theorem and the finite-kernel criterion for automaticity. These inputs are likewise cited in the underlying proofs. [Sparre Andersen](https://doi.org/10.7146/math.scand.a-10407) · [Evertse–Schlickewei–Schmidt](https://annals.math.princeton.edu/2002/155-3/p04) · [Primitive triples, Table 1](https://bmatschke.github.io/solving-classical-diophantine-equations/) · [Automaticity argument](split5_3_components.md#finite-automata-for-orbit-invariant-labels)

The sharp-interval obstruction has an author proof from the cited Sanders theorem, with no dedicated checker. Fable reviewed its scope and corrected the claim about smooth majorants. The full-period limitation and the congruence in §11 come from Fable’s two-ends review and the Codex grid identity. The grid checker verifies finite instances.

The independent correspondence is identified below by its original filename in the local directory **census/round5/split5_3_target/**. The reports were uncommitted at the cutoff. Their verdicts and qualifications are reproduced here so that this record can be read from a clean checkout.

| Proof revision | Fable’s record | Scope |
|---|---|---|
| 54ff27e and 8830ba6 | REPORT_TO_CODEX.md | Re-derived raw tail minima. No independent external citation checks. |
| f745a3bc | REVIEW_TWO_ENDS.md | Reviewed the two-ended deduction. The earlier prefix count and both external Fourier references were taken as inputs. |
| 04a59aa | REVIEW_CHAIN.md | Reviewed the chain and window criterion given the multiplier theorem. Identified the finite-cylinder limitation. |
| d2ff4f2 | REVIEW_LINK_STRIP.md | Reviewed extremizers, realizability, cutoffs and deficit. Identified the distinct-futures limitation. |
| 820585e | REVIEW_SINGLE_DEPARTURE.md | Reviewed differencing, nondegeneracy, parameter limits, sharpness and the covering criterion. |
| a2dbef3 | REVIEW_EXCURSIONS.md | Reviewed whole-prefix and successive-rate proofs. Withdrew the proposed initial-offset penalty. |
| 517c32a | REVIEW_FREE_LABELS.md | Reviewed both decodings, separation and complementary halves. |
| 93a20e4 | REVIEW_FREE_LABELS_2.md | Reviewed distinct and repeated heights, weighted shifts, the three-shift example and the coding obstruction. Gave the distinct-height transfer. |
| eab6fc9 | No independent report | **Not independently refereed.** The preceding review predates the count law. |

For this write-up Codex reran all nine Python checkers identified by the suffixes **microrange, two_ends, grid, link_strip, shifted_links, excursions, free_labels, multishift, family_count** in this directory. All exited successfully. The two compiled full-range runs and Fable’s finite actual-height census are historical results.

## 10. Corrections that affect interpretation

- The original descent-tree argument needed the nonclosing branch through the 2-adic point $-3$. An arbitrarily late descent at an ordinary start alone still permits a small exceptional input at a closed leaf. Also, $4^K-3$ has an actual cycle minimum at $K=3$, so the proposed strict descent for every $K\ge2$ is false.
- At the halving cutoff one must inspect $b+1$ bits and test boundaries with $j-f_j\le b$. For finite links, four expansions followed by an exit of type 3 consume nine halvings but require ten parity bits. Asking that the terminal height be divisible by 256 gives a class modulo $2^{17}$. A finite one-expansion link can start at 4. Divisibility of the starts selected on an escape uses their continuation.
- For distinct block-boundary heights in $[y,4y)$, a common labelled future of $h\ge\log_2 y+2$ halvings would force congruence modulo $2^h\ge4y$ and hence equality. Fable observed that this pigeonhole argument therefore needs an independent upper bound on the number of possible futures. With one centrally placed departure the deficit bound in §5 alone permits $e\simeq2.4d$.
- The coarse strip of width $3e-3/2$ reaches width 256 at $e=86$. The sharp enclosing strip first does so at $e=97$. Width measures possible endpoint locations. It does not establish legality of each location.
- The sharp-interval Fourier obstruction in §11 was initially extrapolated to all smooth majorants. Fable withdrew that extrapolation after the subgroup counterexample. The $1.409m$ square-root scale has a different, conditional status.
- In the excursion proof, translating the *whole* prefix removes the proposed $(2+\log_2 s)u_1$ initial-offset penalty and the minimum-piece-length hypothesis. A geometrically summable ramp requires consecutive exits without intervening expansion. Two independent phases acting simultaneously have no proved general cutoff here.
- A virtual path requires control of the **weighted** corrections $b_i^*$ and a nonzero $G_*$. A relation on the unweighted bits cannot replace either hypothesis. In reverse construction a terminal exit of type 3 must have **even output**. For example, at $y=1024$ four formal expansions and that exit give the integer 1253, but the pre-exit input is 2500 and must expand again. This legality condition accounts for the factor $3/4$ in §8.
- Agreement inequalities constrain pairs of starts. Backwards uniqueness, or adding the endpoint of the same word, cannot by itself exclude a single small start. The elementary transfer in §8 requires distinct visited heights. The result there for every start in typical octaves also uses the separate repeated-height argument.

## 11. The open target and the three obstructions

**Open target.** Prove that for infinitely many integers $m$,

$$
N_m(\lceil12m/5\rceil)\le2 .
$$

By §4 this would prove eventual periodicity for **every** positive integer. A separate argument would be needed to show that the five known cycles exhaust the positive cycles. The Haar prediction at this depth is $2^{[1-(12/5)(1-H)]m+o(m)}\to0$. This is a statement about the mean over translations. The target concerns one prescribed interval of ordinary integers in each chosen octave. Even for the restricted family of §8 the present upper bound is a power of the height times powers of its logarithm. The unrestricted target remains open.

1. **Complete periods only reach logarithmically many extra halvings.** When depth varies over $M$ consecutive values, the two-ended argument completes periods in moduli of size $5^a$ for a head and $2^k$ for a tail. Their multiplicative periods have comparable orders up to constant factors, so this argument requires $5^a,2^k=O(M)$. It can exploit only $O(\log M)$ digits at the ends. Middle moduli at linear depth are exponentially larger. The discrepancy saving is therefore a power of $M$ whereas the target interval has normalized length $2^{m-D}=2^{-1.4m+O(1)}$. Finite chains have the same ordinary-digit limitation. A fixed legal labelled word with terminal $256\mid Y$ and $h$ halvings gives a residue modulo $2^{h+8}$, with exactly $2^{m-h-8}$ representatives in a full octave when $m\ge h+8$. Occurrence through that prefix does not make it a chain of infinite-tail minima.
2. **Taking absolute values loses the location of a sharp interval.** For nonempty $R\subset\mathbb Z/Q$, an interval $I$ of length $X$, and $f(t)=|R\cap(t+I)|$, the sum of the absolute normalized Fourier coefficients of $f$ tends to infinity whenever $X\to\infty$ and $X|R|/Q\to0$. Indeed, bounded norm would give a bounded signed-coset decomposition by Sanders. Each coset has discrepancy at most one on any interval. On $r-I$ for $r\in R$, $f$ is at least one throughout, so at least $X(1-X|R|/Q)$ cosets are needed. This proves a limitation for the sharp kernel. Under a generic square-root Fourier-size estimate, the relative-error calculation reaches only $b\sim m/(1-H/2)=1.409\ldots m$. The subgroup example shows where the argument for smooth majorants breaks down. For a subgroup of spacing greater than $4X$ a triangular majorant can have absolute bound $4/3$.
3. **The independent middle labels leave an ordinary-integer coincidence problem.** Put $b=\lceil12m/5\rceil$, $D=b+1$, $Q=2^D$. For a passing word $w$, write $2^D z_D=5^{A_D}y+C_w$, with $C_w=3\sum_{i<D:\,e_i=1}2^i5^{A_D-A_{i+1}}$. For fixed $A_D$, one must count exact coincidences between $C_w/Q\bmod1$ and the grid $\{-5^{A_D}y/Q\bmod1:2^m+3\le y<2^{m+1}+3\}$. In the near-critical family equation (1) gives the same issue as a subset sum. In base two it decodes forwards, in base five it decodes backwards, and over the reals it gives $U_e/2\le Y_e-r y\le U_e$. None provides a further constraint on freely chosen middle labels at the required size of $y$. Grouping a long irregular gap gives an integer whose part coprime to 10 can be its whole magnitude. Splitting it introduces a growing number of terms, for which the use of Evertse (14) here has no uniform bound. The full-rate coding example shows why pairwise separation cannot supply the missing estimate. No bound of two at the stated depth follows from these results.
