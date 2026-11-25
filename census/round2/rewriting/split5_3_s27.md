# split5_3_s27: GLOBAL, partial result (round 2, rewriting lens)

Rule: even n -> n/2; n=1 mod 4 -> 5n+3; n=3 mod 4 -> n+3. Question: GLOBAL (is every orbit eventually periodic?). Known cycles: min 1 (length 4), min 3 (2), min 5 (5), min 61 (10), min 125 (11).

[Summary of the main results and the remaining open question](../../results/split5_3_s27.md#what-we-know-about-all-positive-starts)

| question | answer | status | tier |
|---|---|---|---|
| GLOBAL | unknown. Proved: a minimal counterexample, every new cycle's minimum and infinitely many points of every divergent orbit lie in an explicit set E of density 1.112e-06 | PARTIAL | 5 (partial statement: 2) |

## Method: machine-found descent tree (lib.descent_tree)

The tree explores residue classes n = Q t + r (t >= 0). Along a branch it carries the exact
affine image T^s(n) = A t + B, where A and B are integers. When the residue of A t + B modulo the
branching modulus is not fixed, it splits t. A class is *closed* as soon as A < Q. Then
T^s(n) < n for every t > t0 = (B - r)/(Q - A). The finitely many n with t <= t0 are simulated
directly; any n whose orbit fails to drop below n within 10^5 steps is recorded in a finite list S.
A class is *open* when one more split would push its modulus past the cap. The union E of the
open classes is the exceptional set.

**Theorem (partial).** Every n >= 1 with n not in E ∪ S has some iterate T^k(n) < n (k >= 1).
Consequences, all proved:
1. If GLOBAL fails, the least start n0 whose orbit is not eventually periodic lies in E. If n0 were
   outside E ∪ S, it would drop to some m < n0 whose orbit is eventually periodic, and then so is
   the orbit of n0. The points of S are periodic (the check verifies this).
2. Every cycle not on the listed cycles has its minimum in E, because a cycle minimum never drops
   below itself.
3. Every orbit that is not eventually periodic visits E infinitely often. Such an orbit takes no
   value twice, so it tends to infinity. It therefore has infinitely many *tail minima* x_k (x_k <= x_i
   for all i >= k), and none of them drops below itself.

**Why the table can never be completed (tier 2 provably fails).** The system has a p-adic point c
with infinite coefficient stopping time. For every K, the positive integers n_K in c's class modulo
p^K have stopping time at least L(K) → ∞ (witness below, checked for the listed K). So E is
nonempty at every modulus, and no finite descent table settles GLOBAL. This also rules out every
Lyapunov function of the form Φ(n) = n·w(n mod M) with positive weights. Strict decrease along an
up-run of length L gives T^L(n)/n < max w / min w, but T^L(n)/n grows without bound on the
witnesses.

**Blocking mechanism.** The descent proof fails at exactly two points. (a) The expanding branch has
an affine conjugacy x -> ρx (ρ > 1) on a p-adic neighbourhood of c, so up-runs have unbounded
length. (b) Re-entry is free: every m is the image of p·m under the division branch (p = 2 or 3). So a
value in the class of c to any prescribed depth can be entered from a value only p times larger. Any potential with a run-length weight Φ = n·λ^{ν(n)} (ν = depth
of n in c's neighbourhood) therefore fails at the re-entry step: the output m can have ν(m) as
large as log_p(m), and Φ(m)/Φ(n) is unbounded. To finish the proof you would have to show that
re-entry into deep neighbourhoods of c cannot happen often along a single orbit. That statement
about orbit statistics is the 3x+1 obstruction.

## Certificate for this system

- Modulus cap 4294967296: 4775 open classes and 6583 closed leaves. The exact density of E is
  4775/4294967296 ≈ 1.1118e-06. The small exceptions are S = [1, 3, 5, 61, 125], all periodic.
- How the density decays (cap: classes, density): 2^8: 1 class, 3.91e-3 | 2^12: 8, 1.95e-3 | 2^16: 16, 2.44e-4 | 2^20: 58, 5.53e-5 | 2^24: 340, 2.03e-5 | 2^28: 1340, 4.99e-6 | 2^32: 4775, 1.11e-6.
  The decay is slow and polynomial in the cap, and the class count keeps growing.
- Witness for "E is never empty": c = -3 in Z_2. For n = 5 mod 8 the steps 5n+3, /2, /2 give n' = (5n+3)/4 with n'+3 = (5/4)(n+3). n_K = 4^K - 3 makes K-1 such triples, each value above n_K, so its stopping time is >= 3(K-1). Checked for K = 1..32.

## Rewriting and potentials (lens b, c)
- (c) Bounded-weight potentials n·w(n mod M) are ruled out for every M (proof above). Run-length
  weighted potentials fail at the re-entry step (blocking mechanism (b) above).
- (b) This is the thinnest exceptional set in the batch: density 1.1e-6 at 2^32, with 4775 classes. The class count still grows by about 3.5x per 4 bits, so E is not a single p-adic point and no parametric closed-form family closes it. Rewriting was not attempted, because there are five cycles.

## What blocks a full proof
The descent tree closes every class except a closed p-adic set Ω that contains c. Ω has density
<= the tabulated values; that Ω has measure zero would follow from a Terras-type theorem and is not proved here. The
expanding branch generates c's up-runs, and the contracting branches generate the free re-entry. No
finite modulus, bounded potential or low-dimensional interpretation separates them.

## Tier
The partial theorem uses tier-2 machinery: a descent inequality plus a finite (machine-generated)
table. GLOBAL itself stays at tier 5 (OPEN). Tier 2 provably cannot settle it, because E is
nonempty at every modulus (witness).

Check: `check_split5_3_s27.py` reproduces E exactly (count, exact density, small list), checks that every
point of S is periodic and that the cycle minima lie in E ∪ S, and tests the witness bounds.

## Referee (round 2)
**Verdict.** GLOBAL: open-agreed, final tier 5. Partial theorem (E): confirmed, tier 2. I could not finish the proof. The open part is a 3x+1-type convergence problem, and no lower-tier method closes the class of the p-adic blocking point.

Independent tests (referee, scratchpad scripts ref1.py/cantor.py, not in repo):
- systems.py step agrees with the lib.py table for n < 20000.
- check_<id>.py rerun: exit 0, about 1 s.
- My own consistency test against the systems.py step function, with E rebuilt at a smaller cap: every n in [2, 6e4) outside E ∪ S drops below itself (10^6-step cap). So do 300 random 200-bit n outside E (2e4-step cap). Zero failures.
- I re-derived the closure logic of lib.descent_tree. A split by g = M/gcd(A,M) fixes the residue because A·g = lcm(A,M) ≡ 0 (mod M). A2 = uA/w is integral (asserted). A leaf closes when A2 < Q, which gives T^s(Qt+r) < Qt+r for t > (B2-r)/(Q-A2). Small t are simulated, and non-descenders are recorded in S and checked to be periodic. Consequences 1-3 (minimal counterexample, cycle minima, tail minima of divergent orbits) are correct.

Gap (repaired here). The .md derives "E is nonempty at every modulus" from the unbounded stopping time of the witnesses n_K. That inference is incomplete on its own: a closed leaf can contain a late-descending n among its finitely many simulated small t. Correct argument: c is a p-adic fixed point of the expanding block, and the tree branch through c has A/Q equal to the product of the branch slopes. Along that branch the product is >= 1 after every step, so the class of c never closes, at any cap. The other use of the witnesses, "no finite descent table", is valid by pigeonhole: finitely many classes, each with a bounded step count and finitely many exceptions, cannot contain infinitely many n_K with stopping time going to infinity.
Minor point: the lens says bounded-weight potentials are killed by free re-entry. The proof actually given kills them with the unbounded up-run ratio, not with re-entry.

**Referee upgrade (proved): E is not a single point, nor finitely many.** The .md offers the class growth only as evidence. Here is a proof.
- On odd values define two blocks:
  - A: n ≡ 5 (mod 8) gives 5n+3, then /2, /2, ending at (5n+3)/4. That value is odd, and the slope is 5/4.
  - B: n ≡ 3 (mod 4) gives n+3, then /2, ending at (n+3)/2. That value is odd, and the slope is 1/2.
- Realizability. On the class n = 8t+5, block A outputs 10t+7, whose residue mod 8 is 2t+7. On the class n = 4t+3, block B outputs 2t+3. So by fixing t modulo 4, the next value can be placed in any odd class mod 8. Every finite word in {A,B} is therefore realised by a residue class, and every infinite word by a unique 2-adic point. Distinct words give distinct points.
- Take infinite words over the two letters W1 = A^5 and W2 = A^4 B. Inside a block the running slope products are 5, 5/2, 5/4 for A, and 1, 1/2 for B. Every prefix of such a word therefore has slope product >= 1, because (5/4)^4/2 > 1. So the descent-tree branch of each such point never closes.
- The open classes at cap 2^K therefore contain at least 2^{floor(K/c)-O(1)} distinct classes, where c bounds the bits consumed per word; c = 15 is enough. The limit set Ω contains a Cantor set and is uncountable.
- Verified for 400 random words of 60 blocks with K = 400: every block condition holds, and the orbit stays above n.
- The same construction (two block words with all prefix products >= 1) applies to the other systems in this lens.

## Subsequent results: a power bound and a finite convergence certificate

The global eventual-periodicity question remains open.

### How many starts never drop?

Let $H(X)$ count the positive integers $n\le X$ for which $T^k(n)\ge n$ for every $k\ge1$. Then
\[
 H(X)=O\bigl(X^{\log_2(3/2)}\bigr),\qquad \log_2(3/2)=0.5849625\ldots .
\]
In particular the set of such starts has natural density zero. The bound counts starts that never drop below themselves. An orbit can drop below its start and still have unknown fate.

**Proof.** Read residues of the starting integer one binary digit at a time, beginning at the low end. In a class $n=2^j t+r$, keep a reached value $x=a t+b$. Use state U when $a$ is odd. In state O, $a$ is twice an odd number and $b$ is odd. Initially $x=n$ and the state is U. The next digit selects one of the two parities of $t$, with equal weight among extensions of the class.

| State | Branch after reading the bit | New reached value | Next state | Factor on real slope |
|---|---|---|---|---|
| U | $x$ even | $x/2$ | U | $1/2$ |
| U | $x$ odd | $x$ | O | $1$ |
| O | $x\equiv1\pmod4$ | $(5x+3)/4$ | U | $5/4$ |
| O | $x\equiv3\pmod4$ | $(x+3)/2$ | O | $1/2$ |

The U-to-O transition records parity and waits for the next bit. All other transitions follow the original map for one, two or three steps. To check the state types, put $t=2u+d$. In U the coefficient of $u$ before updating is twice an odd number. In O it is four times an odd number, and switching $d$ changes the reached residue by 2 modulo 4. These facts establish both the displayed transitions and their equal frequencies at every node.

Write the reached value as $x=A n+B$ on each class. Give U weight 1 and O weight $5/4$. Over the two children, the mean of $A^2$ times the state weight is exactly $3/4$ times its value at the parent. Indeed the two ratios before dividing by the old state weight have averages
\[
 \tfrac12(1/4+5/4)=3/4,\qquad
 \tfrac12(25/16+(1/4)(5/4))=(3/4)(5/4).
\]
By induction the mean of the weighted square over all $2^j$ classes is $(3/4)^j$. Since both state weights are at least one, at most $4(3/2)^j$ classes have $A\ge1/2$.

Every update has nonnegative intercept at most $3/2$ and slope at most $5/4$. Thus $0\le B\le6((5/4)^j-1)$. In $2^j\le n<2^{j+1}$ this is less than $n/2$ for $j\ge6$. If $A<1/2$, then $x<n$, certifying strict descent. There is exactly one start in this interval per residue modulo $2^j$, so at most $4(3/2)^j$ can fail to descend. Summing the geometric bound over the dyadic intervals proves the claim. The same squared-slope estimate implies that the set of infinite bit strings for which the slope never falls below one has binary Haar measure zero.

### Every positive start below 2^48 reaches a known cycle

The accompanying checker partitions $1\le n<2^{48}$ by the same low-bit transitions, retaining the exact integers in $n=Dt+r$, $x=at+b$. If $a<D$, every integer $t>(b-r)/(D-a)$ already gives $x<n$. The finitely many remaining inputs at that leaf are iterated individually until reaching a smaller positive integer or one of the five cycle representatives. Equal slopes with $b<r$ give descent for the entire class. At maximum depth, each class contains at most one input in range. Strong induction on the starting value now proves convergence throughout the range. The checker separately verifies the periods at the five representatives and requires all leaves together to cover exactly $2^{48}-1$ starts.

Run `python census/round2/rewriting/check_split5_3_range.py`. The exact run covered 281,474,976,710,655 starts with 7,574,751 tree nodes and 1,615,819 individual checks. The maximum number of additional raw steps in an individual check was 76.

### The rising family

For $n_K=4^K-3$, the first $K$ triples reach $5^K-3$, since the value after $i$ triples is $5^i4^{K-i}-3$, congruent to 1 modulo 4 for $i<K$. The proposed strict descent for every $K\ge2$ is false. For $K=3$ the entire cycle is
\[
61,308,154,77,388,194,97,488,244,122,61.
\]
Its minimum is 61. For $2\le K\le2000$, exact iteration from $5^K-3$ found descent below $4^K-3$ in every other case. This leaves open both the corresponding statement for all $K\ge4$ and the global eventual-periodicity question.

## Restrictions on every further positive cycle

**Theorem.** Any positive cycle other than the five already recorded has at least 1,936,274 applications of the expanding odd branch, at least 6,432,163 steps of the original map, and at least 101 separate runs of expansion. In particular the five known cycles exhaust the cycles with at most 100 expanding runs. The length bound uses elementary arithmetic and the finite convergence certificate. The bound on the number of runs also uses Matveev's theorem.

Use three blocks, each tracing actual steps of the map:
\[
 A(x)=(5x+3)/4\quad(x\equiv1\bmod4),\qquad
 B(x)=(x+3)/2\quad(x\equiv3\bmod4),\qquad E(x)=x/2\quad(2\mid x).
\]
In a further cycle every value is at least $m=\min(\text{cycle})\ge2^{48}$ by the preceding exact range certificate. Thus $A$ strictly increases, and $B,E$ strictly decrease. There must be both a rise and a fall. A $B$ step leaves its value odd, so between maximal runs of $A$ the contraction word has the form $E^h B^b$ with $h+b\ge1$. The minimum also occurs at a block boundary: intermediate raw values within $A$ or $B$ are larger than the block endpoint. Begin there, at the first step of an expanding run.

Let $r$ be the number of runs in a primitive period, $k_i$ their lengths, $K=\sum_i k_i$, and $L=2K+\sum_i(h_i+b_i)$. The raw period is $K+L+\sum_i b_i$. For a run $x\mapsto y=A^{k_i}(x)$, the ratio of $y/x$ to its slope $(5/4)^{k_i}$ is $(1+3/x)/(1+3/y)$. For a $B$ run taking $v$ to $w$, the ratio to its slope is $(1-3/v)/(1-3/w)$, by $B(v)-3=(v-3)/2$. Halvings have ratio exactly one. Multiplying around the cycle, using $m$ to bound each endpoint, gives
\[
 0<\delta=L\log2-K\log5
 \le r\log\frac{1+3/m}{1-3/m}<7r/m .
\]
For example $\log((1+t)/(1-t))\le 2t/(1-t^2)$ from its power series, with $t=3/m$. All logarithms in this proof are natural unless a base is shown.

**Length.** Put $\alpha=\log_2 5$. Since $r\le K$ and $\log2>2/3$,
\[
 \alpha<L/K<\alpha+11/2^{48}.
\]
This entire interval lies strictly between $4268621/1838395$ and $227268/97879$. Their cross-determinant is one. For neighbors $a/b<c/d$ with $bc-ad=1$ and $a/b<L/K<c/d$, the identity $K=b(cK-dL)+d(bL-aK)$ gives $K\ge b+d=1936274$, even for an unreduced $L/K$. Consequently $L\ge4495889$, proving the raw-period bound.

**Number of runs.** Suppose $r\le100$. Write $x_i$ for the start of run $i$, with $x_1=m$. Following $k_i$ expanding blocks requires $4^{k_i}\mid x_i+3$, since $A^{k_i}(x_i)+3=5^{k_i}(x_i+3)/4^{k_i}$. All intervening contractions decrease the value. Thus
\[
 4^{k_i}\le x_i+3\le(m+3)(5/4)^{k_1+\cdots+k_{i-1}}.
\]
Taking logs and summing the resulting geometric recursion for the partial sums of the $k_i$ gives
\[
 K\le \log(m+3)\frac{(\log_4 5)^r-1}{\log(5/4)}
 <5\cdot10^7\log(m+3).
\]
Here $\log_4 5<7/6$, $(7/6)^{100}<10^7$ and $\log(5/4)>1/5$.

For a first effective bound apply the positive-real form of Matveev's theorem to $\Gamma=5^K2^{-L}-1$. It is nonzero by prime factorization. The rational field has degree one. With two positive bases 5 and 2, logarithmic height parameters 2 and 1 suffice, and $\max(K,L)\le4K$ by the bound on $\delta$. The coefficient $1.4\cdot30^5\cdot2^{4.5}\cdot2$ is less than $2\cdot10^9$. It follows that
\[
 \exp[-2\cdot10^9(1+\log(4K))]<|\Gamma|=1-e^{-\delta}<700/m .
\]
See [Matveev, *An explicit lower bound for a homogeneous rational linear form in the logarithms of algebraic numbers II*](https://doi.org/10.1070/IM2000v064n06ABEH000314) and the [explicit real-field formulation](https://doi.org/10.1007/s00025-024-02156-w).

These two bounds imply $K<1.5\cdot10^{17}(1+\log(4K))$, hence $K<10^{20}$ by monotonicity of $x/(1+\log(4x))$ for $x\ge1$. To reduce this sufficiently, use the following two fractions in order:
\[
 \frac{992575246277942597707}{427478890695834754646},\qquad
 \frac{57567975761}{24793177656}.
\]
Each is a reduced fraction $P/Q$ with $|\alpha-P/Q|<1/Q^2$. If $0<K<Q/2$, then $LQ-KP$ is a nonzero integer, so $|L-K\alpha|>1/(2Q)$. In conjunction with $|L-K\alpha|<11r/m$ this yields $m<2200Q$. The first denominator exceeds $2\cdot10^{20}$ and gives $\log(m+3)<59$, hence $K<3\cdot10^9$. The second denominator now exceeds $2K$ and gives $m<54,544,990,843,200<2^{48}$, a contradiction.

The script `check_split5_3_cycles.py` checks all rational approximations using 64 terms of $\log((1+z)/(1-z))=2\sum_{j\ge0}z^{2j+1}/(2j+1)$ with $z=1/3$ for $\log2$ and $z=1/9$ for $\log(5/4)$. The first omitted term divided by $1-z^2$ bounds the tail. The earlier range checker supplies the lower bound on $m$.

### A smaller ancestor for infinitely many members of the rising family

For every positive $n\equiv311\pmod{625}$, set $u=(2n+3)/625$ and $z=256u-3$. Then $0<z<n$. For $0\le i\le4$, the reached value after $i$ blocks $A$ is $5^i4^{4-i}u-3$. For $i<4$ this is 1 modulo 4, so all four blocks are legal. They give $625u-3=2n$, which halves to $n$. Thus such an $n$ cannot be the least start failing to reach the five known cycles, or the least start with an infinite orbit. This is a statement about an ancestor; $n$ itself need not descend by this argument.

In particular it applies to $n=4^K-3$ for every $K\equiv53\pmod{250}$, since $4^{250}\equiv1\pmod{625}$ and $2\cdot4^{53}\equiv3\pmod{625}$. Whether every positive orbit is eventually periodic remains open.

## How accurately the multipliers would track a divergent orbit

Let $x_0,x_1,\ldots$ be a nonperiodic positive orbit of the original map (here and below, nonperiodic means *not eventually periodic*). Let $K_t$ count the $5x+3$ steps before time $t$, let $L_t$ count the halvings, and put $P_t=5^{K_t}/2^{L_t}$. Then for every $t$,
\[
 1\le \frac{x_t}{x_0 P_t}<1.000073.
\]
The quotient has a finite limit. In particular, for every positive start there is a dichotomy: $P_t\to0$ if the orbit is eventually periodic, and $P_t\to\infty$ otherwise.

The proof needs a count of *all visits* to small heights along a single nonperiodic orbit. The earlier count of starts that never fall below themselves does not give this directly. A related classical result on growth of divergent trajectories for the ordinary Collatz map is Theorem F in [Lagarias, *The 3x+1 problem and its generalizations*](https://web.williams.edu/Mathematics/sjmiller/public_html/355Sp24/addcomments/Lagarias_3x%2B1AndItsGeneralizations.pdf). Here the estimates use the branches of the present map.

**Occupation lemma.** In the two-state U/O evolution defined above, the total number $V(2^j)$ of visits with reached value at most $2^j$, along one nonperiodic orbit, satisfies
\[
 V(2^j)\log2\le \tfrac94(3/2)^j+24(5/4)^j(1+j\log2).
\]
In particular $V(2^j)<4(3/2)^j$ for $j\ge48$.

**Proof.** Start in U and advance exactly one binary update at a time. At a U-to-O update the reached integer stays fixed and the state changes. Every other update advances the original orbit. Thus each pair (state, reached integer) occurs at most once on a nonperiodic trajectory, and its integer values tend to infinity. From an O start use the odd inputs $x=2s+1$ with $s$ free. The same two-state transitions and slope moments apply, with initial weight $5/4$ and initial real slope one with respect to $x$.

Set $X=2^j$. For every pair with $1\le x\le X$ let $y=A x+B$ be the result after $j$ updates from that pair. U starts use at most one integer from each class modulo $2^j$. O starts use at most one odd integer from each class modulo $2^{j+1}$. Summing the weighted square identities from both initial states and dropping the final weights, which are at least one, gives
\[
 \sum_{(\mathrm{state},x):\,x\le X} A^2 \le (1+5/4)(3/2)^j .
\]
As before, $0\le B\le b=6(5/4)^j$.

Use the capped potential $H(x)=\log\min(x,X)$. An update window starting above $X$ contributes at most zero to $H(y)-H(x)$, even if the orbit subsequently re-enters the interval. For a window starting at $x\le X$, the inequality $2A\le e^{A^2}$ gives
\[
 H(y)-H(x)\le -\log2 + A^2+\log(1+2b/x).
\]
Sum these differences over consecutive window starts on the orbit. Along each time class modulo $j$ the sum telescopes, and its terminal term eventually equals $\log X$. The resulting sum is nonnegative once all visits below the cap have been included. Each starting pair occurs at most once. Using $\log(1+u)\le u$ and $\sum_{x\le X}1/x\le1+\log X$ for each of the two states proves the lemma for $j\ge1$. For the simplified bound use $2/3<\log2<7/10$. The quantity $24(5/6)^j(1+7j/10)$ is decreasing for $j\ge48$, and at 48 it is less than $4(2/3)-9/4$.

**Proof of the multiplier bound.** Every divergent orbit stays above the verified range $[1,2^{48}-1]$. Every odd value at which an odd raw step is taken occurs in state O, including when the run begins with U recording its parity. Summing reciprocals of just those odd values over all times, the occupation lemma gives
\[
 \sum_{x\text{ odd on orbit}}\frac1x
 \le\sum_{j\ge48}\frac{V(2^{j+1})}{2^j}
 <24(3/4)^{48}.
\]
This sum is over one trajectory, and all its terms occur once. Raw halving contributes no error to $\log(x_t/(x_0P_t))$. A $5x+3$ step contributes $\log(1+3/(5x))$, and an $x+3$ step contributes $\log(1+3/x)$. Both are positive and at most $3/x$. Hence the total log error on the entire orbit is bounded by $72(3/4)^{48}$. Its exponential is less than $1.000073$. Since $x_t\to\infty$ on a nonperiodic orbit, $P_t\to\infty$ there. On an eventually periodic orbit, every full lap has a positive additive correction and returns to its starting value, so the multiplier product per lap is strictly below one. This proves the dichotomy.

## A two-sided obstruction to bounded descent certificates

Use the accelerated blocks $A,B,E$ defined above and write $F$ for their deterministic map. For every fixed positive integer $D$ there exist arbitrarily large positive $n$ such that
\[
 F^j(n)\ne F^i(m)\qquad(0<m<n,\quad 0\le i,j\le D).
\]
Thus a certificate that always joins a start to a smaller positive start using boundedly many blocks on both paths cannot establish convergence. In fact, within $n\equiv-3\pmod{4^D}$, the lower relative density of starts with the displayed property exceeds $3/4$.

**Proof.** In the stated progression the first $D$ forward blocks are $A$. Use the shifted coordinate $z=x+3$. A forward $A$ multiplies $z$ by $5/4$. In the reverse direction the affine rules are
\[
 A^{-1}: z\mapsto 4z/5,\qquad E^{-1}:z\mapsto2z-3,\qquad B^{-1}:z\mapsto2z-6 .
\]
A putative merger follows $j$ forward blocks from $n$ and then an inverse word. Remove pairs consisting of a forward $A$ followed immediately by its inverse. With $h$ remaining doubling letters (either $E^{-1}$ or $B^{-1}$) and $a$ inverse $A$ letters, the net slope as a function of $n$ is $2^h(4/5)^{a-j}$. Slope one requires $h=0$ and $a=j$, giving the identity. For fixed $D$ there are only finitely many words. Each word with slope greater than one ends above $n$ for all sufficiently large $n$. It therefore suffices to bound the fraction of residues admitting a legal word whose net slope first crosses below one.

For $h=0$ this requires $A^{-1}$ at the initial start after cancellation, imposing $5\mid n+3$. Its fraction is $1/5$. If $h\ge1$, a reduced first-crossing inverse word starts with a doubling letter and ends with $A^{-1}$. Indeed, if any forward $A$ remains, the first inverse $A$ would cancel it. If none remains, an initial inverse $A$ already crosses below one. For a word ending at its first crossing write $a=j+b$, where $b$ is the least integer with $(5/4)^b>2^h$. Then $3h+1\le b\le4h$. Integrality of the endpoint restricts $n$ to at most one class modulo $5^b$: for two legal inputs their output difference is $2^h4^b(n-n')/5^b$. Modulo $4^D$ the restriction modulo $5^b$ has relative density $5^{-b}$ by coprimality.

We also need a bound on $j$ independent of $D$. For $j\ge1$, evaluate the inverse word on an auxiliary shifted input $z=0$ up to and including its $j$-th inverse $A$. The actual shifted input at the start of that word is $5^j(n+3)/4^j$, an integer divisible by $5^j$. The difference of the two evaluations remains integral through those first $j$ divisions by 5, since doubling never introduces a denominator. Legality of the original path thus gives integral auxiliary values throughout this prefix. The first doubling letter gives $-3$ or $-6$. Subsequent values are negative multiples of 3. Each further doubling letter increases the magnitude by a factor at most four, while each inverse $A$ multiplies it by $4/5$. At the end the magnitude is at least three. Consequently
\[
 3\le 6\cdot4^{h-1}(4/5)^j,\qquad j\le 7h ,
\]
where $(5/4)^7>4$. The bound also covers $j=0$.

For given $h,j$, the number of first-crossing words is at most $2^h\binom{j+b+h-2}{h-1}$, by choosing the remaining doubling positions between the fixed first and last letters and their types. A union bound through $h=20$, including the $h=0$ term, gives
\[
 \frac15+\sum_{h=1}^{20}\frac{2^h}{5^b}
   \sum_{j=0}^{7h}\binom{j+b+h-2}{h-1}<0.243692 .
\]
For $h\ge21$, the binomial coefficient is at most $\binom{12h}{h}\le(12e)^h$. The sum of the remaining bounds is at most
\[
 \frac15\sum_{h\ge21}(7h+1)(72/125)^h<0.000692 .
\]
Hence the total excluded fraction is less than $0.245$. For each fixed depth the actual union of congruence classes is finite; the infinite convergent series above only bounds its size uniformly. After removing the finitely many possible small inputs from the slope-greater-than-one paths, the claimed lower relative density follows.

For example, no smaller start merges with $4^{21}-3=4,398,046,511,101$ within 20 blocks on each side. Its own orbit nevertheless drops below its starting value at block 32, reaching $3,637,978,807,093$. The two-sided theorem concerns bounded local searches and supplies no positive divergent orbit. Both the numerical inequalities in the proofs and this particular example are checked by `check_split5_3_escape.py`.

**Orbit-wide inverse test.** If $n$ is the least start of an infinite orbit and $x_t=T^t(n)$, then for every $h,t\ge0$, with $a=v_5(2^h x_t+3)$,
\[
 2^h P_t(4/5)^a > 1/1.000073 .
\]
Indeed $z=(4/5)^a(2^h x_t+3)-3$ reaches $2^h x_t$ by $a$ legal expanding blocks and then reaches $x_t$ by halving. It is positive (for $a>0$ it is at least $4^a-3$). Thus $n\le z\le(4/5)^a2^h x_t$. The multiplier bound gives the inequality. This is a necessary condition at every later value of the least divergent orbit; the two-sided obstruction explains why any fixed-depth merger search still leaves arbitrarily large candidates.

## Arithmetic progressions and automaticity

Every orbit merges with the orbit of some member of $1\bmod 10^d$ for each $d\ge1$. More generally, divisibility by 3 is the only restriction on which arithmetic progressions a merging class meets. A finite-valued orbit-invariant label is automatic in some integer base exactly when it depends only on divisibility by 3. In particular the individual basins of $1,5,61,125$ are nonautomatic in every integer base. For each individual merging class and each compatible progression, the number of members up to $X$ is at least a positive constant times $X^{0.238298\ldots}$ for all sufficiently large $X$. The exponent is the positive root of $4^{-s}+(1024/5)^{-s}=1$. Global eventual periodicity remains open. [Proofs](split5_3_components.md) · [Exact finite checks](check_split5_3_components.py)

## A smaller start obtained by shortening the first expanding run

Let $n=4^K u-3$ with $K\ge2$, $u\ge1$, and put $Z=5^K u$. If $Z\equiv1\pmod8$, the strictly smaller positive start
\[
 m=2\cdot4^{K-1}u-3=(n-3)/2
\]
merges with $n$. In particular **every even $K\ge2$** in the family $4^K-3$ is excluded as a least counterexample.

Indeed, $K$ expanding blocks take $n$ to $Z-3$. The next two blocks are $E,B$, reaching $(Z+3)/4$. From $m$, the first $K-1$ expanding blocks reach $2\cdot5^{K-1}u-3$. This is 3 modulo 4, and $B$ takes it to $5^{K-1}u$. That value is 1 modulo 4 since $Z\equiv1\pmod4$. An $A$ block now gives the same $(Z+3)/4$. The merger uses $K+2$ and $K+1$ blocks respectively. For $u=1$, $5^K\equiv1\pmod8$ exactly when $K$ is even.

**Finite certificate for odd exponents as well.** For $K\ge3$, smaller merging starts exist for at least **46,055 of the 65,536 classes of $K$ modulo $2^{16}$** in the family $4^K-3$. All even classes are included, leaving 13,287 certified odd classes. To check a class, put $u=1$, and compare $n$ with the four possible starts $m=c4^{K-e}-3$ for $c\in\{1,2\}$ and $e\in\{1,2\}$. Each is positive and smaller. After $K$ and $K-e$ expanding blocks, respectively, the peaks are $Z-3$ and $cZ/5^e-3$.

Keep $Z$ as an indeterminate and retain its residue modulo $2^{18}$. Record every reached affine function $(aZ+b)/d$ along each peak's path, starting from the two peak formulas. The residue determines each next branch while enough bits remain. A halving or $B$ consumes one bit and $A$ consumes two. Stop when the remaining bits do not decide the next branch. Equality of two recorded rational affine functions certifies a merger for **every** exponent in the class. The residue of $5^K$ has period $2^{16}$ modulo $2^{18}$, verified by powering and checking its half-period. Enumerating one period gives the stated count. This certifies exclusion as a *least* counterexample. In general the smaller start could itself have unknown fate. [Exact symbolic checker](check_split5_3_rising.py)

The same certificate applies to arbitrary $u$. Write $K$ for the maximal integer with $4^K$ dividing $n+3$, so $u=(n+3)/4^K$ is 1, 2, or 3 modulo 4. For **each fixed $K\ge3$**, the exponent determines a permutation $u\mapsto5^K u$ of the cofactor residues modulo $2^{18}$ within each of these three types. Applying the four peak comparisons with $m=c4^{K-e}u-3$ certifies respectively 46,055, 36,699, and 36,757 residues. Thus **119,511 of the 196,608 possible cofactor residues** are excluded for every such initial run length, however large it is.

**A limitation of these four comparisons.** At $K=3$, the start 61 lies on its own cycle. Its four comparison starts are 13, 29, 1 and 5, which reach cycles 5, 1, 1 and 5 respectively. Consequently no fixed number of post-peak blocks with these four comparisons covers all sufficiently large $K$. To see this, fix a block budget $D$. The paths up to that depth depend on only finitely many low bits of $Z$. All $K$ sufficiently close to 3 modulo a suitable power of two reproduce the same branch choices. No pair of the corresponding affine functions can be identical, since its values at $Z=125$ would then meet. Each unequal pair agrees for at most one $Z$, and there are finitely many pairs. Thus arbitrarily large exponents survive this test. This argument concerns the four stated comparisons; others could still work.

## Extension of the range certificate to 64 bits

Every positive start below $2^{64}$ reaches one of the five recorded cycles. The compiled checker implements the affine residue partition and strong induction in the 48-bit proof. Node arithmetic uses unsigned 128-bit integers. At depth $j$, $a\le(5/2)^j$ and $b/a\le3j$ by the child formulas, so the numerators fit. Direct raw steps check for overflow. A leaf's number of represented positive starts is accumulated exactly, whether its proof uses uniform descent or direct iteration.

The run certified 18,446,744,073,709,551,615 starts in 3,191,342,737 tree nodes, with 579,402,090 individual checks and at most 99 extra raw steps. GCC and Clang gave identical full-range counts, including a Clang run instrumented to stop on unsigned arithmetic overflow. All four counts agree with the arbitrary-precision Python implementation at bit depths 1, 4, 8, 20, 32 and 48. [Compiled checker and build command](check_split5_3_range.cpp) · [Arbitrary-precision checker](check_split5_3_range.py)

**Consequences for cycles.** Any further cycle has at least **9,271,940,877 original steps** and **201 expanding runs**. For length, use the notation from the earlier cycle proof. Its slope inequality gives $\alpha<L/K<\alpha+11/2^{64}$ for $\alpha=\log_2 5$. This interval is strictly between the determinant-one neighbors
\[
 1344399137/579001193,\qquad 5136409418/2212131129 .
\]
Thus $K\ge2791132322$ and the raw period is at least $K+L\ge9271940877$.

For the run count, suppose $r\le200$ and let $m$ be the cycle minimum. The same run-length recursion gives $K<C\log(m+3)$ with $C=47\cdot10^{12}$, since $\log_4 5<1.161$, $1/\log(5/4)<5$, and $5(1.161)^{200}<C$. The Matveev bound used above gives $m<1400\exp(2\cdot10^9(1+\log(4K)))$, hence $\log(m+3)<3\cdot10^9(1+\log(4K))$. Monotonicity of $K/(1+\log(4K))$ gives $K<10^{25}$. [Matveev's theorem](https://www.mathnet.ru/eng/im314)

Use the following two reduced approximations $p/q$ in order:
\[
 \frac{116521770536551532152706941}{50183195075299715266313813},
 \qquad \frac{8009031126156845}{3449301958915901}.
\]
For the first, $|\alpha-p/q|<1/q^2$ and $2K<q$, so $|L-K\alpha|>1/(2q)$ by the determinant argument above. Since $|L-K\alpha|<2200/m$, this gives $m<4400q$ and $\log(m+3)<70$. Thus $K<70C$, less than the second denominator. For the second approximation $|\alpha-p/q|<1/(8q^2)$. The integer $Lq-Kp$ is nonzero, so $|L-K\alpha|>7/(8q)$ and $m<8\cdot2200q/7<2^{64}$. This contradicts the verified range. [Exact rational checks](check_split5_3_cycles.py)

**How long can both merger searches be forced to run?** For every integer $D\ge40$, consider the $4^D$ starts $n\equiv-3\pmod{4^D}$ in $[16^D,2\cdot16^D)$. For more than three quarters of them there is no merger with a smaller positive start when both paths have length at most $D$ blocks. In particular, along infinitely many inputs every such certificate needs more than $\lfloor(\log_2 n)/4\rfloor$ blocks on at least one side.

To make the earlier bounded-depth obstruction uniform in $D$, use its shifted coordinate $z=n+3$. After the forward $A$ blocks and an inverse word, write the result as $s z-e$. The error starts at zero, and each inverse letter increases it to at most $2e+6$. Hence $0\le e\le6(2^D-1)$. The slope $s=2^h(4/5)^{a-j}$ has denominator at most $5^D$ since $0\le a,j\le D$. If $s>1$, then $(s-1)z\ge16^D/5^D>6\cdot2^D$ for $D\ge40$. Such a word cannot end below the start. Slope one gives the identity as in the earlier proof.

For the remaining words count the earlier first-crossing congruences on this finite interval. Each congruence of mass $5^{-b}$ covers at most $4^D5^{-b}+1$ of the starts, by coprimality with $4^D$. The total mass is less than 0.245. There are fewer than $(D+1)3^{D+1}/2$ pairs of a forward prefix and an inverse word of length at most $D$, including any first-crossing prefix. The extra rounding loss as a fraction of the interval's starts is thus below $\tfrac32(D+1)(3/4)^D<0.005$ for $D\ge40$ (the expression decreases there). This proves the assertion.

A concrete example inside the verified range is $n=2^{64}-3$. No smaller start merges with it in at most 33 blocks on both sides. At depth 34 a merger exists, and $n$ itself first drops below its start at block 53. The even-exponent formula also gives the simple comparison start $2^{63}-3$, reaching the common value $(5^{32}+3)/4$ in 33 blocks to the original start's 34. [Exact checks of the merger depth and descent](check_split5_3_escape.py)

## One map for whole expanding runs

Use the shifted height $y=x+3\ge4$. Write $y=2^{2k+b}u$, where $u$ is odd and $b\in\{0,1\}$. Define
\[
 G(y)=2^{b-1}(5^k u+3)
     =\tfrac12(5/4)^k y+3\cdot2^{b-1}.
\]
This follows the original orbit for exactly $k$ expanding blocks and one further block. In shifted coordinates each expanding block replaces a multiple of 4 by $5y/4$. After $k$ such blocks the shifted value is $2^b5^ku$. For $b=0$ the original value is even, giving the shifted result $(5^ku+3)/2$. For $b=1$ the original value is 3 modulo 4, giving the shifted result $5^ku+3$. The formula also holds for $k=0$. Every step consumes at least one original step, and every finite expanding run ends, so eventual periodicity of $x$ is equivalent to eventual periodicity of $G$ at $y$.

**Fixed points.** The fixed point equation is
\[
 u(2\cdot4^k-5^k)=3.
\]
The parenthesis takes the values $1,3,7,3$ for $k=0,1,2,3$ and is negative thereafter. This gives exactly $y=4,6,8,64,128$ on the domain $y\ge4$. They represent the five known cycles. If $k\le3$, then $G(y)\le125y/128+3<y$ whenever $y>128$. Consequently the least divergent start, if it exists, must have $256\mid x+3$, and every divergent orbit visits such shifted multiples of 256 infinitely many times. In fact an upper bound of three on all sufficiently late expanding run lengths implies convergence to a known cycle, by descent into the verified finite range.

**A criterion for each individual orbit.** Say an integer is $S$-smooth if all its prime divisors belong to a specified finite set $S$. On a divergent orbit of $G$, for every fixed $S$ and every $h\ge1$, there are only finitely many pairs of $S$-smooth heights separated by between one and $h$ steps of $G$. Equivalently, if there are infinitely many $S$-smooth visits, the gaps between successive visits tend to infinity. An orbit is eventually periodic exactly when some finite $S$ and some $h$ give infinitely many such pairs.

Here is the stronger finiteness statement behind the criterion. For fixed $d\ge1$, only finitely many positive starting heights $y$ have both $y$ and $G^d(y)$ $S$-smooth, globally over all starts. Enlarge $S$ to include $2,3,5$. Write $y_i=G^i(y)$ and $y_{i+1}=a_i y_i+c_i$, with $a_i=(5/4)^{k_i}/2$ and $c_i\in\{3/2,3\}$. Iteration gives
\[
 1=\frac{y_0\prod_{i=0}^{d-1}a_i}{y_d}
    +\sum_{j=0}^{d-1}\frac{c_j\prod_{i=j+1}^{d-1}a_i}{y_d}.
\]
All $d+1$ summands are positive rational $S$-units. The nondegenerate unit-equation theorem gives finitely many ordered tuples of these summands, since their multiplicative group has finite rank and no nonempty subsum vanishes. In particular the last term $c_{d-1}/y_d$ takes finitely many values. Hence there are finitely many endpoints $y_d$. Each endpoint $w$ has finitely many predecessors: for each $b$ the positive odd integer $5^ku=2^{1-b}w-3$ allows only finitely many $k$. This proves finiteness of the initial heights as well. Taking $d=1,\ldots,h$ gives the orbit criterion because a nonperiodic orbit has distinct heights. Conversely a periodic tail has a finite set of prime divisors and gives adjacent pairs forever. [Evertse, Schlickewei and Schmidt, *Linear equations in variables which lie in a multiplicative group*](https://annals.math.princeton.edu/2002/155-3/p04)

**The explicit case $S=\{2,3,5\}$ and $d=1$.** Exactly 25 shifted starts have both $y$ and $G(y)$ 5-smooth. They are
\[
 4,5,6,8,9,10,12,15,18,24,27,30,36,45,54,64,72,80,90,100,125,128,160,200,250 .
\]
To prove completeness put $z=5^k u$. The conditions are exactly that $z$ and $z+3$ are 5-smooth and $z$ is odd. Dividing the triple $(z,3,z+3)$ by $\gcd(z,3)$ gives a primitive smooth triple. Table 1 of von Känel and Matschke gives exactly 17 primitive positive triples up to swapping the summands. The checker exhibits 17 using integers at most 128. Restoring the summand 3 and keeping odd $z$ gives $z\in\{1,3,5,9,15,27,45,125\}$. For each $0\le k\le v_5(z)$ and $b=0,1$, reconstruct $y=2^{2k+b}z/5^k$ and retain $y\ge4$. Every listed start reaches a fixed point by direct iteration. Conversely, all five fixed points are 5-smooth. Thus **a start reaches one of the five known cycles exactly when its compressed orbit contains one adjacent 5-smooth pair**. This equivalence does not establish that each orbit has such a pair. [Complete primitive triple counts, Table 1](https://bmatschke.github.io/solving-classical-diophantine-equations/) · [Exact checks](check_split5_3_runs.py)

For the earlier rising family $y=4^K$, $K\ge1$, the one-step classification says that $G(4^K)$ is 5-smooth exactly for $K=1,3$. More generally, for each fixed $h$ and finite $S$ containing 2, all sufficiently large $K$ have **no** $S$-smooth height among $G(4^K),\ldots,G^h(4^K)$. This follows from the global finiteness statement. It allows the required return time to grow with the starting value.

**Repeated growth with exactly four expansions per run.** Even after combining each full expanding run and its exit into one step, there is no fixed forward search depth that guarantees descent from every large start. In fact the number of consecutive initial steps of type $(k,b)=(4,0)$ is exactly
\[
 \left\lfloor\frac{v_2(113y+768)}{9}\right\rfloor.
\]
Indeed this branch requires $y\equiv256\pmod{512}$, equivalently $512\mid113y+768$. On the branch,
\[
 G(y)=(625y+768)/512>y,\qquad 113G(y)+768=\tfrac{625}{512}(113y+768).
\]
Each step therefore consumes exactly nine factors of 2 in the latter integer. For any prescribed $D$, choose $y\equiv-768/113\pmod{512^D}$, where division denotes the modular inverse. Infinitely many positive starting integers then increase through $D$ complete runs, each with precisely four expansions. Every individual start eventually leaves this repeated pattern because $113y+768$ is a positive integer. Thus even growth through many consecutive runs of moderate length supplies no counterexample. [Exact checks](check_split5_3_runs.py)

**A run-length inequality sufficient for the global question.** Let $k_i=\lfloor v_2(G^i(y))/2\rfloor$ and $K_t=\sum_{i=0}^{t-1}k_i$. Each compressed step has original-orbit multiplier $(5/4)^{k_i}/2$, including its exit block. At these times the earlier multiplier dichotomy therefore gives
\[
 K_t-\frac{\log 2}{\log(5/4)}t\longrightarrow
 \begin{cases}
 -\infty &\text{on an eventually periodic orbit},\\
 +\infty &\text{on a divergent orbit}.
 \end{cases}
\]
Thus to prove global eventual periodicity it suffices, for each positive start, to bound this difference above along an infinite subsequence. The coefficient is about 3.1063. A bound on the limiting average alone, with equality allowed, would leave the possibility of a positive excess tending to infinity sublinearly. Neither the smooth-pair theorem nor the finite-run identity proves the required subsequence bound.

## When the first drop in the multiplier gives actual descent

Let $y_0=x+3$, $y_i=G^i(y_0)$, $K_i=\sum_{j<i}k_j$ and $P_i=(5/4)^{K_i}/2^i$.

**Theorem.** For every $y_0\ge2^{64}$, through the first **3,000,000,000 complete runs**, the first $i$ with $P_i<1$ is exactly the first $i$ with $y_i<y_0$. If one event does not occur in that window, neither does the other.

The positive additive terms in $G$ give $y_i\ge P_i y_0$. Suppose $t$ is the first index with $P_t<1$. Writing $c_j=3\cdot2^{b_j-1}$ gives
\[
 y_t=P_t y_0+\sum_{j=0}^{t-1}c_jP_t/P_{j+1}\le P_t y_0+3t .
\]
The multiplier ratios up to the last term are less than one, since every earlier prefix has multiplier at least one. The last ratio is one. It therefore suffices to prove $y_0(1-P_t)>3t$.

Put $\beta=\log_2(5/4)$ and $d=t-\beta K_t$. At first crossing $P_{t-1}\ge1$ and a single run has slope at least $1/2$, so $0<d\le1$. Take $p=186396751$ and $q=579001193$. Rational bounds for the logarithms give $0<q\beta-p<1/(24\cdot10^9)$ and $1/\beta<3.11$. The integer $qt-pK_t=qd+(q\beta-p)K_t$ is positive. Thus
\[
 d>\frac{1-K_t/(24\cdot10^9)}q
\]
when $K_t>0$ (the weak inequality suffices also for $K_t=0$). For $t\le3\cdot10^9$ we have $K_t<3.11t$. By concavity on $[0,1]$, $1-2^{-d}\ge d/2$. The rational inequality
\[
 \frac{2^{64}}{2q}\left(1-\frac{3.11\cdot3}{24}\right)>9\cdot10^9
\]
finishes the proof. No bound on the time to a first crossing is assumed or obtained. The use of parity residue classes in classical coefficient stopping-time questions goes back to [Terras](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/en/publishing-house/journals-and-series/acta-arithmetica/all/30/3/101028/a-stopping-time-problem-on-the-positive-integers). [Exact rational checks](check_split5_3_recovery.py)

**Cycle consequence.** Every additional positive cycle must take **more than 30,900,000,000 original steps** per primitive period. Partition one original lap into the $A,B,E$ blocks beginning at an odd point. The intermediate states skipped by $A$ and $B$ are even, so the block partition returns to the initial odd point after traversing the lap once. Group each string of $A$ blocks with its next $B$ or $E$; at least one such exit exists since $A$ strictly increases. Rotate the resulting cyclic list to begin at the least shifted height among its run boundaries. All heights are at least $2^{64}$ by the range certificate. The lap multiplier is strictly below one, because the lap returns to its initial height with positive additive correction. If its number $t$ of compressed steps were at most three billion, the first-crossing theorem would force a smaller boundary height on the same lap.

For the total number $K$ of $A$ blocks, each ratio $y_{i+1}/y_i$ is at most its linear slope times $1+6/2^{64}$. If $K\le3.1t$ the product around the lap is strictly below one, by $(5/4)^{31}(1+6/2^{64})^{10}<2^{10}$. Hence $K>3.1t$. Each $A$ uses three original steps and each exit at least one, giving more than $10.3t$ original steps. The count $t$ includes exits preceded by zero expansions.

## Recovery after a prescribed stretch of growth

Encode the current shifted height as $y=2^s z$, with $s\in\{0,1\}$, initially $s=0$. Read a bit given by the parity of $z$. The update is
\[
 (z,s)\longmapsto
 \begin{cases}
 ((z+3)/2,s) & z\text{ odd},\\
 (z/2,1) & z\text{ even},\ s=0,\\
 (5z/2,0) & z\text{ even},\ s=1 .
 \end{cases}
\]
An odd bit ends one complete run. The first of a pair of even bits records a factor of two, leaving $2^sz$ unchanged, and the second performs one expanding block. The pending factor at a run boundary is retained. For either initial flag, words of $r$ bits correspond bijectively to residues of $z$ modulo $2^r$. Indeed, along a fixed prefix of length $j$ the affine image of $z=z_*+2^j v$ has odd coefficient in $v$. The two lifts modulo $2^{j+1}$ give opposite next bits.

Consider starts whose first $D$ runs are all $(k,b)=(4,0)$, so each increases height and their combined slope is $a^D$, where $a=625/512$. Take any interval of $2^{10D}$ consecutive shifted heights with lower endpoint greater than $6D\,2^{10D}$. It contains exactly $2^D$ such starts. For each of them, continue for $D$ more bits and stop at the first height strictly below its original start. For $D\ge2$ one example of a suitable lower endpoint is $2^{12D}$.

**Recovery law.** For every fixed $\epsilon>0$, the proportion of this class whose first descent occurs within $(0.342908285\ldots\ \pm\epsilon)D$ additional *complete runs* is $1-O_\epsilon(e^{-c_\epsilon D})$ for some $c_\epsilon>0$. The proportion still waiting at the end of the $D$ additional *bits* is
\[
 2^{-(0.03751708\ldots+o(1))D}.
\]
These are counts of ordinary positive integers on the stated finite intervals.

**Proof.** The prescribed prefix consumes $9D$ bits and ends with flag zero. The $D$ following bits run through all $2^D$ words exactly once by the bijection. If a prefix of $r$ further bits contains $h_r$ ones, the shifted height has slope relative to the original start
\[
 M_r=\frac{5^{4D+\lfloor(r-h_r)/2\rfloor}}{2^{9D+r-s_r}},
 \qquad s_r=(r-h_r)\bmod2 .
\]
Only an odd bit can lower this slope, so its first crossing is at a run boundary. The denominator divides $2^{10D}$. At a first crossing the affine correction is at most $6D$ by the argument above, since at most $2D$ complete runs have elapsed. The interval hypothesis then guarantees descent at exactly that crossing. This elementary denominator argument covers arbitrarily large $D$.

Put $g=\log a$, $v=\log(\sqrt5/2)$ and $w=\tfrac12\log5$. Then $\log M_r=gD+vr-wh_r-vs_r$. Outside an exponentially small fraction of binary words, $|h_r-r/2|\le\eta D$ simultaneously for all $r\le D$, for each fixed $\eta>0$. For example, for fair bits the moment generating function of $h_r-r/2$ is $(\cosh(\theta/2))^r\le e^{r\theta^2/8}$. Markov's inequality and a union bound give an exceptional fraction at most $2D e^{-2\eta^2 D}$. The log slope stays within $w\eta D+v$ of the line $gD-(w/2-v)r$. Its zero is at $r=0.685816570\ldots D$, strictly inside the observed interval. Taking $\eta$ sufficiently small forces the first crossing within any fixed relative tolerance of that time. The number of completed runs there is $h_r$, giving the constant $g/[2(w/2-v)]$ in the claim.

For the precise exponent of the surviving count, put $p_*=(g+v)/w=0.3864688385\ldots$. A survivor must have $h_D\le p_*D$. Conversely, take words with $m=\lfloor p_*D\rfloor-2$ ones for all sufficiently large $D$. At least $\binom{D}{m}/D$ of them satisfy $h_r\le rm/D$ at every prefix: rotate each word immediately after a maximum of $h_r-rm/D$ on its cyclic sequence of partial sums. For such a word $gD+vr-wrm/D$ is a line whose two endpoint values are $gD$ and at least $2w$. Both exceed $v$ for large $D$, so even the flag correction cannot cause descent. The survivor count is squeezed between $\binom{D}{m}/D$ and $\sum_{h\le p_*D}\binom{D}{h}$. Stirling's formula gives binary logarithm $D H_2(p_*)+O(\log D)$ for both bounds, where $H_2(p)=-p\log_2p-(1-p)\log_2(1-p)$. This gives the claimed exponent $1-H_2(p_*)$. Requiring the initial streak to end at exactly $D$ changes the concentration statement by at most a constant factor in the exceptional proportion since only one of the next 512 nine-bit words continues the streak.

A finite integer recurrence counts the survivors exactly. Start with one empty word. At each further bit, add the counts from the two possible previous one-counts, then zero out entries with $M_r<1$. For $D=64$ exactly 528,853,098,900,915,039 of $2^{64}$ words survive 64 additional bits (about 2.87%). At $D=512$ the fraction is about $1.01\cdot10^{-7}$. The remaining words have stayed above their starts throughout the window; their eventual fate is a separate question. [Exact enumeration and independent direct orbit checks](check_split5_3_recovery.py)

There is no upper bound depending on $D$ alone for the recovery time of every start that exits this streak at exactly $D$. For any $D,L\ge1$, prescribe the bit word $(0^8 1)^D(0^{10}1)^L$. The residue bijection gives one class modulo $2^{9D+11L}$. Its first $D$ runs have four expansions and its next $L$ have five. Each run strictly increases the shifted height. Both arbitrarily delayed recovery and the finite-interval concentration theorem therefore hold.

## How often a divergent orbit can return near the critical expansion count

Put $E_t=K_t-\kappa t$ with $\kappa=\log 2/\log(5/4)$, and $\alpha=\log_2(3/2)$. On any divergent orbit and for fixed $c\ge0$,
\[
 \#\{1\le t\le N:E_t\le c\log t\}
 =O_{y_0,c}\!\left(N^{\alpha c\log(5/4)}\right).
\]
Indeed the original height at a compressed boundary is $x_t=y_t-3\le 1.000073\,x_0P_t$ by the earlier multiplier bound, with $P_t=(5/4)^{E_t}$. All the times being counted therefore visit heights at most $1.000073\,x_0 N^{c\log(5/4)}$. Each run boundary is a distinct visit in the earlier U/O evolution: that evolution executes the same $A,B,E$ blocks with occasional parity-recording updates. Its occupation lemma bounds the total number of visits up to height $X$ by $O(X^\alpha)$, rounding $X$ up to a power of two. This proves the estimate.

For $c<1/(\alpha\log(5/4))=7.661038\ldots$, the displayed times have natural density zero on any divergent orbit. In particular **positive upper density of times with $K_t\le\kappa t+7\log t$ implies eventual periodicity**. The criterion allows an excess growing without bound. It does require a frequency of returns; a single unusually low prefix cannot establish it.

**A restriction at exactly the critical average.** For one starting integer let $p(m)$ count distinct length-$m$ words appearing anywhere in its bit sequence above. Every divergent orbit satisfies
\[
 \liminf_{m\to\infty}p(m)/m\ \ge\ 1/(2\log_2(\sqrt5/2))=\kappa .
\]
If $K_t/t\to\kappa$ on such an orbit, the stronger conclusion $p(m)/m\to\infty$ holds. Thus a divergent orbit with the critical limiting average cannot have linearly bounded word complexity, even if its expansion excess grows faster than $\log t$.

For the first claim put $w=5^{s/2}z$ and $\lambda=\sqrt5/2$. An even bit sends $w$ to $\lambda w$. An odd bit sends it to $(w+3\cdot5^{s/2})/2$. Hence $z_j\le w_j\le C\lambda^j$ with $C=\max(w_0,3\sqrt5)$. No pair $(z_j,s_j)$ repeats on a divergent orbit. A length-$m$ word and its initial flag specify the initial $z_j$ modulo $2^m$ by the residue bijection. Among positions $0\le j\le (m-\log_2 C)/\log_2\lambda$, all the $z_j$ are positive and at most $2^m$. Consequently a word can occur at most once per flag among these positions, proving the lower bound.

For the second claim, the number of bits consumed by $t$ complete runs is $B_t=2K_t+t+s_t$ since each pair of even bits accounts for one expansion, with $s_t$ the pending flag at the boundary. Thus $B_t/t\to1+2\kappa$. Squeezing each bit position between consecutive boundaries gives $h_j/j\to1/(1+2\kappa)$, where $h_j$ counts ones. For the $w$ evolution its slope product is $L_j=\lambda^j5^{-h_j/2}$. At this frequency $\log L_j=o(j)$. The additive terms are bounded, so iterating the affine updates gives
\[
 w_j\le L_j\left(w_0+3\sqrt5\sum_{i=1}^j L_i^{-1}\right)=\exp(o(j)).
\]
Indeed $\max_{i\le j}|\log L_i|=o(j)$. For any fixed $A>0$, eventually all $z_j$ with $j\le A m$ lie in $[1,2^m]$. The same residue argument now gives $2p(m)\ge\lfloor A m\rfloor+1$. Arbitrary $A$ proves the claim.

## An exact prefix criterion for all positive starts

Use the bit evolution above with initial state $(z,s)=(y,0)$, $y=x+3\ge4$. Write $h_j$ for the number of ones in its first $j$ bits, and put
\[
 \lambda=\sqrt5/2,\qquad p=\frac{\log(5/4)}{\log5}=0.1386468838\ldots .
\]

**Theorem.** Every positive orbit is eventually periodic if and only if **each** ordinary integer $y\ge4$ has **at least one** finite prefix with $h_j>pj$. This is an existential test at each start. The crossing may occur at a different time for every integer.

To prove it, use the weighted variable $w=5^{s/2}z$. Its bit multipliers are $\lambda$ at a zero and $1/2$ at a one, giving
\[
 L_j=\lambda^j5^{-h_j/2},\qquad L_j<1\ \Longleftrightarrow\ 5^{j-h_j}<4^j .
\]
At a bit boundary the actual shifted height is $w/\lambda^s$, so its linear multiplier from flag zero is $L_j/\lambda^s$. At complete-run boundaries this is precisely the run multiplier $P_t$. On every eventually periodic trajectory $P_t\to0$, hence some prefix crosses.

Conversely, on any divergent trajectory $P_t\to\infty$ by the multiplier theorem. Its sequence of run-boundary multipliers therefore attains an absolute minimum, say at time $t_0$, including time zero as a possibility. Restart the run map at the actual positive integer $y_{t_0}$, encoding it anew with flag zero. The subsequent complete-run multipliers are exactly $P_{t_0+t}/P_{t_0}\ge1$ because the run map depends only on the current height. Between these boundaries the actual multiplier only stays fixed or increases until the next exit bit. The weighted multiplier is at least the actual one. Thus this integer has $L_j\ge1$ for **every** prefix. Applying the argument on successive tails gives infinitely many distinct such integers on a divergent orbit. This proof permits the original start of a divergent orbit to have a crossing.

**How many starts survive a finite prefix test?** Let $A_m$ count the length-$m$ words satisfying $h_j\le pj$ for every $1\le j\le m$. Every interval of $2^m$ consecutive starting integers contains exactly $A_m$ survivors by the bit-to-residue bijection. With $H=H_2(p)=0.5806841231\ldots$,
\[
 A_m=\Theta\!\left(\frac{2^{Hm}}{m^{3/2}}\right).
\]
For example $A_{32}=6505$ and $A_{64}=660674068$. All tests of the threshold use integer powers. [Two independent exact count recurrences and direct residue checks](check_split5_3_prefix.py)

For the proof, let $B_m=\sum_{h\le pm}\binom mh$ count words satisfying the condition at the final bit only. For fair independent bits use walk increments $p$ at zero and $p-1$ at one. The nonnegative partial sum condition is exactly the prefix test. The Sparre Andersen identity, with its series variable rescaled by two to count words, gives the formal power series
\[
 1+\sum_{m\ge1} A_m z^m=\exp\left(\sum_{m\ge1}\frac{B_m}{m}z^m\right).
\]
This applies also without a symmetry assumption on the increments. In this case $p$ is irrational by unique factorization, so nonempty partial sums cannot tie zero. Logarithmic differentiation gives the independently checkable recurrence $m A_m=\sum_{j=1}^m B_j A_{m-j}$, with $A_0=1$. [Sparre Andersen, *On the fluctuations of sums of random variables II*](https://doi.org/10.7146/math.scand.a-10407)

Put $R=2^H$. Since $0<p<1/2$, consecutive binomial coefficients downwards from $\lfloor pm\rfloor$ decrease at least geometrically for large $m$. Stirling's bounds give $B_m=\Theta(R^m/\sqrt m)$, including the bounded effect of the floor. After substituting $z/R$, the exponent has coefficients $b_m=B_m/(mR^m)=\Theta(m^{-3/2})$. For $v_m=m^{-3/2}$, $m\ge1$, splitting the convolution at $m/2$ gives $(v*v)_m\le C v_m$ for a constant $C$ because $\sum v_m<\infty$. Consequently if $b_m\le C_1v_m$ then the $k$-fold convolution of $b$ is bounded by $C_1^k C^{k-1}v_m$. Summing with weights $1/k!$ proves the upper estimate for $A_m/R^m$. The linear term of the exponential gives the matching lower bound.

In particular, the number up to $X$ passing **forever** is $O(X^H/(\log X)^{3/2})$, by enclosing them in one full residue interval at $m=\lceil\log_2 X\rceil$. The matching lower bound above concerns passing $m$ bits only. Indeed every finite passing word is realized by arbitrarily large positive integers, but its extension by all zeros has a nonpositive rational starting value in the 2-adic encoding: the current $z$ must be zero after the word, and reversing the affine map $(a z_0+b)/2^m$ gives $z_0=-b/a$ with $a$ a nonnegative integral power of 5 and $b\ge0$.

The same count yields a sharp size for a finite **actual-height** test. In $2^m\le y<2^{m+1}$ the number that never fall below $y$ during their first $m$ bits is $\Theta(R^m/m^{3/2})$. For the lower bound prepend two zeros to any passing word of length $m-2$. These initial bits give weighted multiplier $\lambda^2$ and restore flag zero. Even after the flag correction, every subsequent actual linear multiplier is at least one. All additive terms are nonnegative. For the upper bound, while the height stays at least $y$, each one-bit update contributes to the actual-to-linear ratio a factor $1+3/z\le1+6/y$, and zero-bit updates are exact. Hence $L_j\ge(1+6/y)^{-m}\ge1/2$ for all $j\le m$ and all sufficiently large $m$. Prefixing seven zeros supplies $\lambda^7>2$ and turns the original word into a passing one, since the weighted multiplier depends only on the bit word. The count is therefore at most $A_{m+7}$. In particular the same big-O bound applies to the number of positive starts up to $X$ that never descend below themselves in the original map, by summing the dyadic bounds.

There is an explicit sufficient set of positive integers of this sparsity. On each dyadic interval $[2^m,2^{m+1})$ keep just the shifted starts passing $m$ bits. The set is computable from the interval index and the residue tree, contains exactly $A_m$ elements per interval, and contains every shifted start passing forever. Hence it would suffice to prove that each retained integer eventually crosses the prefix threshold. A fixed finite maximum depth cannot do this: for every $m$ there are positive multiples of $2^m$ whose first $m$ bits are all zero.

The corresponding infinite set in the 2-adic integers has Hausdorff dimension exactly $H$, with zero Hausdorff measure in dimension $H$. For the upper bound cover it by $A_m$ residue balls of diameter $2^{-m}$. For the lower bound concatenate arbitrary passing words of a fixed length $m$ indefinitely. Each entire word has nonnegative surplus $pm-h_m$, so all prefixes of a concatenation still pass. The residue bijection respects prefixes, giving $A_m$ disjoint children of relative diameter $2^{-m}$ at every level of this construction. Giving them equal mass shows dimension at least $\log_2 A_m/m$: a ball specified by $j$ bits has mass at most $A_m^{-\lfloor j/m\rfloor}$. Let $m$ tend to infinity. This describes the size of the full 2-adic set; the intersection with ordinary integers $y\ge4$ is the open question.

### Counting visits on one divergent orbit

In the weighted bit evolution, the number $V(X)$ of positions with $w\le X$ on any one divergent orbit satisfies
\[
 V(X)=O\!\left(\frac{X^H}{\sqrt{\log X}}\right).
\]
This estimate concerns visits on a single trajectory, including positions whose future prefixes have already crossed the barrier.

Here are the details. Take $m=\lceil\log_2 X\rceil$ and $X\ge4$. A length-$m$ window maps its initial value to $w'=Aw+B$, with $A=\lambda^m5^{-h/2}$ for a word having $h$ ones. Each additive term is at most $3\sqrt5/2$, and every one-step slope is at most $\lambda$. Hence $0\le B\le b=C\lambda^m$ for an absolute $C$. For the capped height $F(w)=\log\min(w,X)$, windows starting above $X$ have nonpositive increments. For $w\le X$,
\[
 F(w')-F(w)\le -1+(1+\log A)_++\log(1+e b/w),
\]
where $r_+=\max(0,r)$. This follows by bounding $A+b/w$ above by $\max(A,e^{-1})(1+e b/w)$. Sum over consecutive positions through a sufficiently late time. The increments telescope along each time class modulo $m$ and sum to a nonnegative number, since a divergent bit trajectory eventually stays above $X$. Indeed $y=2^sz$ advances through the original orbit with at most one consecutive waiting update, and $w=\lambda^s y$.

No integer pair $(z,s)$ can repeat on that trajectory. For each flag and each word, at most one start with $w\le X$ has that word, by $1\le z\le X\le2^m$ and the residue bijection. Thus the sum of the positive-part terms is bounded by
\[
 2\sum_{h=0}^m\binom mh\bigl(1+m\log\lambda-(h/2)\log5\bigr)_+
 =O(R^m/\sqrt m).
\]
The positive terms end at $h\le pm+2/\log5$. Moving down $j$ positions from that end increases the linear weight by $O(j+1)$ and decreases the binomial weight by a uniform geometric factor for large $m$. The remaining logarithmic errors sum to $O(b\log X)$ by $w\ge z$ and the harmonic sum for the two flags. Since $\lambda<R$, this too is $O(R^m/\sqrt m)$. Bringing the $-1$ terms to the other side gives the claim.

In particular write $c_*=1/(H\log(5/4))=7.71748346\ldots$. On every divergent orbit the fraction of run times $2\le t\le N$ with
\[
 K_t-\kappa t\le c_*\log t
\]
is $O_{y_0}(1/\sqrt{\log N})$. At a compressed boundary $w=\lambda^s y_t$ is at most a constant depending on the starting integer times $(5/4)^{K_t-\kappa t}$, by the earlier multiplier bound. Apply $V(X)$ with $X=C_{y_0}N^{1/H}$. More generally adding $d\log\log t$ to the threshold still gives density zero for every $d<c_*/2$, by the same substitution. Positive upper density of such returns therefore certifies eventual periodicity, including at the stated critical logarithmic coefficient.

### Verification through 66 bits

For **every** $1\le x<2^{66}$, the shifted start $y=x+3$ has a prefix with $5^{j-h_j}<4^j$ by bit 146. The bound 146 is attained, for example, at $y=19,469,588,806,135,160,832$. This counts the first crossing of the weighted bit multiplier. The example's actual shifted height first drops below its start one bit earlier.

The compiled prefix checker partitions $0\le y<2^{66}$ by consecutive low binary digits. At a node with $y=r+2^j t$, the current bit integer is $at+b$ with $a$ odd. The next two lifts give the two possible next bits. Once the threshold is crossed, the entire residue class is accounted for. At depth 66 there are exactly 2,150,900,120 passing residues (including zero), also given by the independent word recurrence. The checker continues each remaining positive in-domain representative exactly and includes $y=2^{66},2^{66}+1,2^{66}+2$ separately. The threshold table is built with integer powers and any unfinished trajectory triggers a failure. GCC and an unsigned-overflow-instrumented Clang build returned the same maximum. Direct Python iteration agreed with the search on smaller ranges and verified the 146-bit witness. [Compiled prefix checker](check_split5_3_prefix.cpp) · [Count recurrence](check_split5_3_prefix.py)

At the first weighted crossing the bit must be a one. It ends a run and its actual linear multiplier is $L_j/\lambda^s<1$. Some complete-run multiplier has therefore crossed below one by run 146. For $y\ge2^{64}$ the earlier three-billion-run theorem gives actual descent at the first such run. Together with the previous range and induction on $x$, **all 73,786,976,294,838,206,463 positive starts below $2^{66}$ reach a known cycle**. Independently, the original height-based residue verifier at depth 66 certified the same interval using 6,667,755,247 tree nodes and 1,887,286,712 individual checks (at most 117 extra raw steps). [Independent height verifier](check_split5_3_range.cpp)

With the range established, the earlier first-crossing argument extends to six billion complete runs for $y\ge2^{66}$. Retain its $d=t-\beta K_t$ and $q=579001193$. For $t\le6\cdot10^9$ the same rational bound gives $d\ge(1-3.11\cdot6/24)/q$. For $d\le1/16$ the quadratic Taylor bound gives $1-2^{-d}\ge d(\log 2-(\log 2)^2/32)>2d/3$. For $d>1/16$ the chord bound gives $1-2^{-d}>1/32$. In either case $2^{66}(1-2^{-d})>18\cdot10^9$. Thus the loss exceeds the $3t$ bound for the additive correction. As in the earlier cycle proof, any further positive cycle must have more than six billion complete runs and **more than 61,800,000,000 original steps**. [Exact rational checks](check_split5_3_recovery.py)

## The ordinary-integer obstruction

A finite parity word determines a residue modulo a power of two. To address its *infinite* extension, one can recover the unique 2-adic starting value directly. Take any infinite binary word $e_0,e_1,\ldots$ and set
\[
 a_j=\left\lfloor\frac{j-\sum_{i<j}e_i}{2}\right\rfloor,
 \qquad S_j=\sum_{i<j}\frac{e_i2^i}{5^{a_i}} .
\]
Here the initial flag is zero, and $a_j$ counts completed pairs of zero bits. If this word starts at $y$, induction on the bit updates gives
\[
 y+3S_j=\frac{2^j z_j}{5^{a_j}}.
\]
A one contributes the additive term $3/2$ to $z$ and leaves $a$ unchanged. A zero contributes no additive term. Since $5$ is odd, the right side tends to zero 2-adically for the 2-adic orbit. The prefix-to-residue bijection then identifies the unique starting value as $y=-3\lim_{\mathbb Q_2}S_j$. This is the split-map version of the inverse parity-series construction familiar for the ordinary Collatz map. [Bernstein and Lagarias, *The 3x+1 conjugacy map*](https://doi.org/10.4153/CJM-1996-060-x)

**A formulation independent of any size cutoff.** Global eventual periodicity is equivalent to the following arithmetic statement: for every binary word for which $S_j$ converges as a real series, its value $-3\lim_{\mathbb Q_2} S_j$ is outside the ordinary integers $y\ge4$. To check the equivalence, suppose this 2-adic value is such an integer, put $x_0=y-3$, and write $x_j=2^{s_j}z_j-3$ at bit time $j$. Its original-map multiplier is $P_j=2^{s_j}5^{a_j}/2^j$, including a factor of one at a waiting update. The finite identity reads $y+3S_j=(x_j+3)/P_j$. On a periodic tail the multipliers tend to zero along complete-run boundaries, forcing the nonnegative partial sums to be unbounded. On a divergent orbit the earlier multiplier theorem bounds $x_j/P_j$ and gives $P_j\to\infty$ at complete-run boundaries; between boundaries the multiplier only stays put or increases until the exit. The partial sums are therefore bounded and increasing. This proves both implications.

For an eventually periodic word whose real series converges, the value is the same rational in both completions. If there are finitely many ones this follows from the finite sum. Otherwise double a tail period if necessary so its zero count is even. Successive copies contribute a geometric series with rational ratio $2^d/5^a$, where $d$ is the period length and $a$ its number of zero pairs. The ratio is always contracting 2-adically and real convergence forces it to be less than one in the real absolute value. The geometric identity applies in both fields, giving $y\le0$. For an unrestricted aperiodic word, convergence in both fields supplies no identity equating their limits.

**An arithmetic test for some aperiodic words.** If a length-$m$ prefix is shared with a nonpositive rational $N/D$ in lowest terms with $D>0$ odd, then any ordinary positive integer $y$ realizing it must satisfy $2^m\mid Dy-N$. In particular $Dy+|N|\ge2^m$. A word with such completions satisfying $(D+|N|)/2^m\to0$ along a subsequence cannot come from a positive integer.

For example, suppose a word passes the prefix test forever and begins with $WW$ for arbitrarily long blocks $W$ having an even number of zeros. Repeat $W$ periodically instead. If $r=|W|$ and $a$ is half its zero count, its block sends $z$ to $(5^az+B)/2^r$ with $B\ge0$, restores the flag, and has $5^a>2^r$ by the prefix condition and unique factorization. Its 2-adic periodic completion starts at the nonpositive rational $-B/(5^a-2^r)$. Both numerator and denominator are $O((\sqrt5)^r)$: for a one at position $i$ its contribution to $B$ is $3\cdot 2^i 5^{a-a_i}$, and $a-a_i\le(r-i)/2$ since the block's total zero count is even and bit $i$ is a one. Summing the resulting geometric majorant proves the bound. The two paths agree for $2r$ bits, while $(\sqrt5)^r/2^{2r}\to0$. The arithmetic test excludes the original word even when its tail is aperiodic. The prefix inequality by itself does not give such repetitions or sufficiently small rational completions for a general word. This is where the argument stops.
