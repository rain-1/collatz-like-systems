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

## A restriction on survivors at the two-survivor depth

Let $2^m\le n<2^{m+1}$, $y=n+3$ and $b=\lceil 12m/5\rceil$. A survivor here is a start whose raw orbit has no value below $n$ through the first $b$ halvings. Use its first $b$ parity bits in the $(z,s)$ coding above. A word on an interval has period $d$ if bits at distance $d$ agree whenever both positions lie in that interval. Its length need not be a multiple of $d$.

**Theorem.** Fix a positive integer $R$ and any function $p(b)=o(b)$ taking positive integer values. Along any sequence of survivors with $m\to\infty$, the fraction of bits covered by at most $R$ disjoint intervals of period at most $p(b)$ has upper limit at most
$$
 1-\frac{7}{6\log_2 5}=0.4975440155\ldots .
$$
In particular, for all sufficiently large $m$, **zero** survivors at the requested depth have half their bits covered by such intervals. This includes constant expanding stretches and repetitions of short mixed patterns. The result gives no upper bound of two for the complementary class.

**The clock and the affine identity.** Index bit positions from zero. Write $A_j$ for the number of updates $z\mapsto5z/2$ in the first $j$ bits and $P_j=5^{A_j}/2^j$. At index $j$, $2^{s_j}z_j$ is the raw shifted height after $j-s_j$ halvings, at a block boundary. Indeed the first zero with flag zero waits, the next zero with flag one performs two halvings, and a one performs one halving with either flag. Thus a survivor satisfies $z_j\ge y/2$ at all $j\le b$. Iterating the three bit rules gives
$$
 z_j=P_j y\prod_{i<j:\,z_i\ {\rm odd}}(1+3/z_i),\qquad
 P_j\ge \tfrac12\exp(-6b/y)\ge \tfrac13
$$
for large $m$. This uses actual survival throughout, including when the flag is one.

For any consecutive block $[u,v)$ of length $\ell$, the affine update is
$$
 2^\ell z_v=5^{A_v-A_u}z_u+C_{u,v},\qquad
 C_{u,v}=3\sum_{u\le i<v:\,z_i\ {\rm odd}}2^{i-u}5^{A_v-A_{i+1}}.
$$
This nonnegative integer is at most $3\sqrt5\,\ell(\sqrt5)^\ell$. In a suffix each pair of zeros accounts for one factor of five, with at most one extra from its entry flag. Therefore $A_v-A_{i+1}\le(v-i)/2$ and each summand has the required bound. In the numerator $2^b z_b$ the block contributes $2^u5^{A_b-A_v}C_{u,v}$ in addition to the propagated starting term $5^{A_b}y$ and the contributions of the other blocks.

**An exact test for the remaining residue classes.** More generally, fix $K>0$ and allow any integer depth $1\le b\le Km$. For all sufficiently large $m$ and every start in the octave, actual survival through $b$ halvings is equivalent to
$$
 5^{A_j}\ge 2^{j-s_j}\quad\text{for every }0\le j\le b+1\text{ with }j-s_j\le b .
$$
The possible extra bit matters when the entry flag delays a halving. In a completed expanding block the raw slopes are $5,5/2,5/4$ relative to its input; a partial final expanding block cannot create a first drop. A nonexpanding odd block first adds 3 before its halving. Thus testing the completed bit boundaries detects every first drop of the raw multiplier. It detects every first drop of height as well. If all the tested slopes are at least one, the nonnegative additive corrections guarantee survival.

Conversely, at a boundary with $h=j-s_j\le b$ halvings the raw multiplier is $M=5^{A_j}/2^h$. If $M<1$, Matveev's bound for the fixed rational bases $5,2$ gives $1-M\ge c(1+b)^{-C}$ with absolute constants, since $A_j,h\le b+1$ and the two powers cannot agree here. If $A_j=0$, the gap is at least $1/2$. Under actual survival every preceding raw input is at least $n$. Each odd update with coefficient $a\in\{1,5\}$ contributes a factor $1+3/(ax)\le1+3/n$ relative to its linear part at input $x$. At most $b+1$ such updates precede the boundary since every odd update is followed by a halving. Its height divided by $n$ is therefore at most $M(1+3/n)^{b+1}<1$ for all large $m$, a contradiction. In particular the desired count at $b=\lceil2.4m\rceil$ equals exactly the number of passing word residues modulo $2^{b+1}$ whose shifted representative lies in $[2^m+3,2^{m+1}+3)$. This removes any additive approximation error at the scale of two survivors. [Matveev's theorem](https://www.mathnet.ru/eng/im314)

**Representing a periodic block by two terms.** In each proposed periodic interval with period $d$, take the longest initial segment consisting of whole repetitions of a word of length $2d$. Doubling the period restores the entry flag because this word has an even number of zeros. Discard fewer than $2d$ remaining bits into the unrestricted gaps. Empty periodic segments can be dropped. There are at most $R+1$ gaps of total length $L$, counting the discarded bits. The trimming changes the total coverage by $o(b)$.

One copy of the doubled word induces $z\mapsto\alpha z+\beta$, with $\alpha=5^a/2^{2d}\ne1$, $\beta=C/2^{2d}$, and $C$ as above. Put $c=\beta/(\alpha-1)=C/(5^a-2^{2d})$. Both numerator and denominator in lowest terms have magnitude at most $2^{O(d+1)}$. At the endpoints $u,v$ of the repeated segment,
$$
 \frac{z_v}{P_v}-\frac{z_u}{P_u}
   =c\left(\frac1{P_u}-\frac1{P_v}\right).
$$
Consequently the contribution to $2^b z_b$ is a pair of signed terms $c\,2^u5^{A_b-A_u}$ and $-c\,2^v5^{A_b-A_v}$. This holds also when $c=0$, in which case both terms can be omitted.

**The arithmetic estimate.** Write $r(x)=|x|\,|x|_2\,|x|_5$ for the part of a nonzero integer's magnitude coprime to 10, where $|p|_p=1/p$. Evertse's Theorem 2, equation (14), over the rationals with $S=\{\infty,2,5\}$ and $T=\{2\}$ gives the following. For a fixed number of nonzero integer summands $x_i$ with no nonempty vanishing subsum, and each $\epsilon>0$,
$$
 \left(\prod_i r(x_i)\right)\left|\sum_i x_i\right|_2
 \ \ge\ c_\epsilon\max_i |x_i|_2\,(\max_i |x_i|)^{-\epsilon}.
$$
The constant also depends on the number of terms. Only boundedly many choices for this number occur below. [Evertse, *On sums of S-units and linear recurrences*, p. 228](https://www.numdam.org/item/CM_1984__53_2_225_0.pdf)

Multiply the block decomposition by a common positive denominator $D$ of the periodic coefficients $c$. Since $R$ is fixed and $d\le p(b)=o(b)$, both $D$ and every $|Dc|+1$ are $2^{o(b)}$. The resulting integer sum equals $D2^bz_b$. Its leading term is $x_0=D5^{A_b}y$. All gap terms are nonnegative. After division by $D5^{A_b}$ the absolute sum of the signed periodic terms is at most $6\sum |c|=2^{o(b)}$, using $P_j\ge1/3$. Since $y\ge2^m$, no vanishing subsum contains $x_0$ for large $m$. Remove zero terms and successively delete any nonempty vanishing subsum until Evertse's hypothesis holds. The sum and its leading term are preserved.

The remaining terms have maximum magnitude at most $2^{O(b)}$, by their displayed formulas and $y<2^{m+1}+3$. Every $r(x_i)$ is at least one, so deletion can only decrease their product. The periodic terms contribute at most $2^{o(b)}$ to that product. The unrestricted terms contribute at most $2^{o(b)}(\sqrt5)^L$, by the bound for $C_{u,v}$ and the fixed number of gaps. The leading term contributes $r(D)r(y)$. On the other hand $|\sum x_i|_2\le |D|_2\,2^{-b}$ and $\max_i|x_i|_2\ge |D|_2|y|_2$. Cancelling $|D|_2$ and using $r(y)/|y|_2=y|y|_5\le y$ yields
$$
 b\le\log_2 y+L\log_2\sqrt5+O(\epsilon b)+o(b).
$$
The coefficient implicit in $O(\epsilon b)$ comes from the uniform height bound and is independent of $\epsilon$; the fixed Evertse constant contributes $o(b)$ for each $\epsilon$. Divide by $b$, pass to the limit, and let $\epsilon$ decrease to zero. Since $\log_2 y/b\to5/12$, the unrestricted fraction has lower limit at least $7/(6\log_2 5)$. This proves the theorem.

There is a quantitative consequence for the expanding bits themselves. The number of zeros among the first $b$ bits is $2A_b+s_b$. The exact multiplier test gives at least $2b/\log_2 5-O(1)$ zeros. After removing any fixed number of short-period intervals as in the theorem, the lower limit of the fraction of all $b$ positions still occupied by uncovered zeros is at least $2/\log_2 5-(1-7/(6\log_2 5))=0.3638\ldots$. A survivor would therefore need expansions distributed beyond its longest regular stretches.

**What remains.** The real growth condition allows extensive variation. For example, concatenate either of the eleven-bit blocks $0^{10}1$ and $0^9 1 0$ independently. Both restore flag zero, have terminal multiplier $5^5/2^{11}>1$, and maintain raw block-end multiplier at least one at all prefixes. For the second block the only contraction follows four complete expansions, with multiplier $(5/4)^4/2>1$ after the contraction. The intervening raw heights in an expanding or contracting block are at least the smaller endpoint, so each word is a legal survival pattern. Each specifies a residue modulo $2^b$ at length $b$ by the coding bijection.

For $b=11k$ there are $2^k$ of these words. At most $2^{k/2+o(b)}$ of them can have half their bits covered by at most $R$ intervals of period at most $p(b)=o(b)$. Indeed the interval endpoints, periods and period words have only $2^{o(b)}$ choices; the covered intervals determine at least $k/2-2R$ whole eleven-bit blocks. Thus many residue classes pass the multiplier test and escape the periodic-block restriction. Whether more than two surviving residues have representatives $y=n+3$ in the target octave for all sufficiently large $m$ remains undecided. There are arbitrarily large $m$ with $11\mid b$, for instance $m=55j$.

## Almost every octave beyond its binary length

Let $N_m(b)$ count actual survivors in $[2^m,2^{m+1})$ through $b$ halvings, including the height reached on the last halving. Let $P(b)$ be the Haar probability of survival for the raw linear multipliers on the same clock. Put $q=1-2/\log_2 5$ and $H=-q\log_2 q-(1-q)\log_2(1-q)=0.58068412\ldots$.

**Theorem.** Fix $0<\eta<H/2$. For large $M$, apart from $O_\eta(M^{1-\eta/3})$ integers $m\in[M,2M)$, simultaneously for all integers
$$
 1\le b\le m+(H/2-\eta)\log_2 m,\qquad
 N_m(b)=2^mP(b)\bigl(1+O_\eta(M^{-\eta/3})\bigr).
$$
This is an asymptotic count on actual integer octaves. The coefficient of the additional logarithmic term can be taken arbitrarily close to $0.29034206$. The two-survivor target has $b=\lceil2.4m\rceil$ and remains open. The proof adapts the averaged progression discrepancy argument for the $3x+d$ map to the two possible entry flags and to the pending last halving.

**Splitting the word.** By the exact multiplier test above, use $D=b+1$ bits, testing all raw slopes at bit boundaries except the last when its flag is zero. This equality with actual survival holds throughout the asserted range for all sufficiently large $m$. If $D\le m$, the octave contains whole periods of length $2^D$, giving equality with the Haar predictor. Otherwise set
$$
 j=D-m,\quad k=\lfloor\log_2 M\rfloor+2,\quad Q=2^k,\quad d=D-k=m+j-k.
$$
In our range $1\le j<k$ for large $M$. Write the shifted start $y=n+3=r+2^d t$ with $0\le r<2^d$. Each $r$ admits $2^{k-j}$ consecutive values of $t$ in the shifted octave. The first $d$ bits, their five-count $A=A_d$, and the end flag $s$ depend only on $r$. At this boundary $z_d=5^At+B_r$. Discard prefixes that have already dropped. For a remaining prefix let $S\subseteq\mathbb Z/Q$ be the set of continuation inputs $z_d\bmod Q$ that pass. Contributions from this residue are counts on a progression of length $2^{k-j}$, slope $5^A$, and arbitrary intercept.

**The possible continuation sets.** Write $L=\log_2 5$, $A=\lfloor d/L\rfloor+v$ and $\theta=\{d/L\}$. If the next $i$ bits, from entry flag $s$, use $a_i$ factors of five and end with flag $s_i$, their cumulative test is
$$
  v+a_i\ge\left\lceil \theta+(i-s_i)/L\right\rceil .
$$
Use every $1\le i<k$ and use $i=k$ precisely when $s_k=1$. For fixed $(s,v)$ there are $O(k)$ patterns as $\theta$ varies, since each $i-s_i\in[0,k]$ gives at most one interior breakpoint. Prefix survival gives $5^A\ge2^{d-s}$, so $v\ge-1$. If $A\ge(d+k)/L$ every continuation passes. Only $O(k)$ nontrivial slots $v$ need attention.

Every continuation set arising from a live prefix has size at least $c\,2^{Hk}/k^{3/2}$. To see this, let $\lambda=\sqrt5/2$. A zero bit has weighted multiplier $\lambda$ and a one has $1/2$. The unweighted multiplier of a continuation prefix is the corresponding product times $\lambda^{s-s_i}$, as follows from $2a_i=(\#\text{zeros})+s-s_i$. Begin with a zero, which creates a weighted buffer $\lambda$ and cannot lower the unweighted multiplier. For the remaining $k-1$ bits take words with exactly $\lfloor q(k-1)\rfloor$ ones whose partial weighted products are all at least one. Every word with this many ones has total weighted product at least one and some cyclic rotation with all prefix products at least one. Dividing the binomial count by $k-1$ and applying Stirling gives the bound. The initial buffer covers either flag, so all these words pass all the required tests. Distinct words from either fixed entry flag give distinct residues modulo $Q$ by the bit-coding bijection.

**Averaging the progression error.** For $N=2^{k-j}$, define $G(a)=\sum_{0\le t<N}\exp(2\pi iat/Q)$. For each fixed set $S$ above and uniform $u$ in the subgroup generated by $5\bmod Q$, Fourier inversion and Parseval give
$$
 \mathbb E_u\max_B\left|\sum_{0\le t<N}1_S(ut+B)-|S|2^{-j}\right|\ll k\sqrt{|S|}.
$$
Indeed, at a nonzero frequency of order $2^l$ the geometric sum vanishes if $2^l\mid N$. Otherwise $u$ times its odd numerator is uniform on a coset containing at least a quarter of the residues modulo $2^l$, since $5$ has order $2^{l-2}$ for $l\ge3$ (successive squaring gives $v_2(5^{2^t}-1)=t+2$). The mean of $|G|$ on the coset is $O(l)$ by the geometric-series bound and the harmonic sum over nonzero residues. Applying this frequency bound to the triangle inequality and then using $Q^{-1}\sum_\xi|\widehat{1_S}(\xi)|\le\sqrt{|S|}$ proves the estimate.

For fixed $j,v$, as $m$ runs through $[M,2M)$, each $A=\lfloor(m+j-k)/L\rfloor+v$ occurs at most three times, in an interval of length $O(M)$. Each exponent residue modulo $2^{k-2}\le M$ occurs $O(M/2^{k-2})$ times. For any fixed continuation pattern that is actually encountered on a live prefix, bound its bad exponents using the unrestricted average just derived. This avoids assuming independence of the threshold pattern and the multiplier. With relative tolerance $\epsilon=M^{-\eta/3}$, Markov's inequality and the union over the $O(k^2)$ choices of slots, patterns and flags discard at most
$$
 O\!\left( M k^{15/4}\,2^j\,2^{-Hk/2}/\epsilon\right)
$$
values of $m$. Sum this over $j\le1+(H/2-\eta)\log_2(2M)$ to obtain $O_\eta(M^{1-\eta/3})$ exceptions. For every other $m$, summing the relative estimates over the live prefix residues preserves the same tolerance. Their progression means add to $2^mP(b)$ because each such prefix has Haar mass $2^{-d}$ and conditional survival probability $|S|/2^k$. This proves the theorem.

**Haar probability at a pending halving.** In a fresh state the shifted input has unrestricted parity. An even-known state has one parity bit already fixed. Let $F_h,E_h$ be the surviving cylinder counts ending a completed block at halving $h$ in these states; the cylinder masses are respectively $2^{-h}$ and $2^{-(h+1)}$. Paths can also be halfway through a two-halving expansion. For $b\ge1$, the exact probability is
$$
 P(b)=\frac{2F_b+E_b+F_{b-1}+E_{b-1}}{2^{b+1}} .
$$
The last two terms arise by choosing the expansion from either state ending at $b-1$. Its conditional probability is $1/4$ or $1/2$, respectively, and its intermediate slope rises. The resulting $2^mP(\lceil12m/5\rceil)$ is $0.01416015625$ at $m=8$, $0.00171803$ at $32$, $0.000330225$ at $100$, and $8.18407\cdot10^{-10}$ at $2000$. These are model means, not observed octave counts. The checker compares the recurrence and bit-clock condition against raw multiplier iteration on complete residue systems through $b=13$, and checks the progression decomposition for both entry flags. [Exact probability and clock checker](check_split5_3_microrange.py)

### A limitation of taking absolute values in the exact Fourier count

The averaged estimate above controls a relative error while the predictor is large. At the two-survivor depth, even the *exact* Fourier magnitudes, multiplied by the exact interval kernel and then added in absolute value, give an upper bound tending to infinity. This assertion concerns the sharp interval and this particular use of the triangle inequality.

In fact let $G=\mathbb Z/Q$ be any finite cyclic group, $R\ne\varnothing$, $I=[0,X)$ with $X\le Q$, and $f(t)=|R\cap(t+I)|$. Along any sequence with $X\to\infty$ and $\mu=X|R|/Q\to0$, its Fourier algebra norm $M_f=\sum_{\xi}|\widehat f(\xi)|$ (normalized coefficients) tends to infinity. To see this, Sanders's quantitative idempotent theorem expresses the integer-valued $f$ as a sum of at most $L(M_f)$ signed subgroup-coset indicators, with $L$ bounded at each fixed norm bound, independently of $Q$. A subgroup coset in a cyclic group is one residue class modulo a divisor of $Q$. On any interval $J$ of consecutive residues its count differs from $|J|$ times its density by at most one. Choose $r\in R$ and take $J=r-I$. On every one of these $X$ translates $f\ge1$. Summing the signed decomposition on $J$ and subtracting the global mean forces $L(M_f)\ge X(1-\mu)$. The right side tends to infinity, proving the claim. [Sanders, *Bounds in Cohen's Idempotent Theorem*](https://arxiv.org/abs/1610.07092)

For the split map take $Q=2^{b+1}$, $X=2^m$ and $R$ the passing residues in shifted coordinates. The zero word gives a member of $R$. At $b=\lceil2.4m\rceil$, the prefix test at $j=b$ requires at most $qb+O(1)$ ones. The binomial bound thus gives $\mu\le2^{m-(1-H)b+o(b)}\to0$. The sharp interval kernel vanishes on nonzero frequencies of order dividing $X$, but all those zeros are already included in $M_f$. In the unnormalized transforms of $1_R,1_I$, the usual sum-of-absolute-values upper bound including the zero frequency equals $M_f=Q^{-1}\sum_\xi |\widehat{1_R}(\xi)\widehat{1_I}(\xi)|$. It eventually exceeds two on every subsequence. This leaves open methods exploiting phase cancellation at the specific octave, including methods that combine selected frequencies before estimating a remainder.

## Cancellation from both ends of a passing word

Write $q=1-2/\log_2 5$, $p=1-q$, $H=-p\log_2p-q\log_2q$ and $H_2=-\log_2(p^2+q^2)$. Here $H_2$ denotes the order-two Rényi entropy, and $H$ the binary Shannon entropy. Put
$$
 c_*=H/2+H_2/\log_2 5=0.45991803957\ldots .
$$

**Theorem.** Fix $0<\eta<c_*$. For all sufficiently large $M$, apart from $O_\eta(M^{1-\eta/4})$ integers $m\in[M,2M)$, the following holds simultaneously for every integer $1\le b\le m+(c_*-\eta)\log_2 m$:
$$
 N_m(b)=2^mP(b)\bigl(1+O_\eta(M^{-\eta/2})\bigr).
$$
$N_m$ counts actual survivors in the ordinary octave, on the halving clock of the preceding theorem. The extra term $H_2/\log_2 5$ comes from retaining the signs of the initial word phases while averaging the terminal word phases. No independence between the two averages is needed.

### Splitting the Fourier coefficient

Set $D=b+1$ and $Q=2^D$. A passing $D$-bit word obeys $5^{A_i}\ge2^{i-s_i}$ through $i<D$, and at $i=D$ when $s_D=1$. Let $W_D$ be the number of passing words and $\mu_D$ the uniform probability on their shifted starting residues $y/Q$ on the circle, with $0\le y<Q$. The coding bijection gives $P(b)=W_D/Q$. If a segment $w$ of length $l$ uses $a$ factors of five and ends at $z'$, write its affine update as $2^l z'=5^a z+C_w$ with $C_w\ge0$. On a fixed entry flag, put $r_w=-C_w/5^a$ in the rationals with odd denominator. For consecutive segments $u,v$, where $u$ uses $a$ factors of five,
$$
 r_{uv}=r_u+(2^{|u|}/5^a)r_v .
$$
In particular the starting residue is $r_w\bmod Q$. Use the convention $e_Q(x)=\exp(2\pi i(x\bmod Q)/Q)$ for such rational $x$.

Average over integer $D\in[M,3M]$, with fixed lengths $d=2\lfloor\log_5 M\rfloor$ at the beginning and $k=\lfloor\log_2 M\rfloor+2$ at the end. The intervening length is $D-d-k$. Group the initial words by their number $t$ of ones. In a group, the entry flag for the middle and $a=\lfloor(d-t)/2\rfloor$ are fixed. Let $V_t$ be the number of live initial words in this group, $p_{t,D}$ its probability under $\mu_D$, and
$$
 U_{t,D}(\xi)=V_t^{-1}\left|\sum_{u} e_Q(\xi r_u)\right|.
$$
Omit empty groups. Every initial word in a group admits exactly the same collection of middle and terminal words. For any fixed live prefix through time $D-k$, let $A=A_{D-k}$ and let $S\subseteq\mathbb Z/2^k$ be its accepted terminal residues, including the last-flag convention. Its normalized terminal factor has modulus
$$
 |S|^{-1}\left|\sum_{z\in S} e_{2^k}(\xi 5^{-A}z)\right|.
$$
Let $T_D(\xi)$ be the maximum over live prefixes. Grouping first by $t$ and then by the middle word, the concatenation identity factors each sum into the initial sum, one middle phase, and the terminal sum. Taking absolute values **after** the first and last sums gives
$$
 |\widehat\mu_D(\xi)|\le T_D(\xi)\sum_t p_{t,D}U_{t,D}(\xi). \tag{1}
$$
The weights here are the actual shares of completed passing words.

### The initial group weights

Write $B_n$ for the number of binary words whose every prefix has at most $q$ times its length in ones. The prefix-count theorem above gives $B_n\asymp 2^{Hn}(1+n)^{-3/2}$. Also $W_D\gg 2^{HD}D^{-3/2}$ by prefixing two zeros to such a word of length $D-2$. For a live initial word its weighted surplus $g=qd-t$ is nonnegative. Until position $D-1$ its remaining bits must stay above surplus $-g$ relative to their own start. This follows from the raw multiplier being at most the weighted multiplier.

To estimate the number of such continuations of length $n=D-d-1$, introduce $l=(d+2)^2$ artificial initial bits with exactly $u=\lfloor ql-g\rfloor$ ones (nonnegative for large $d$). At least $\binom lu/l$ of these words have nonnegative prefix surplus, by cyclic rotation, and they all end with surplus at least $g$. Prepending each to any allowed continuation produces a word counted by $B_{n+l}$. Stirling and Taylor's formula give, uniformly for $0\le g\le qd$,
$$
 \binom lu/l\gg l^{-3/2}2^{Hl-H'(q)g},\qquad H'(q)=\log_2(p/q),
$$
since $(g+1)^2/l=O(1)$. Divide the upper bound on $B_{n+l}$ by this lower bound, allow either final bit and normalize by $W_D$. Consequently for some absolute exponent $C$,
$$
 p_{t,D}\ll (1+d)^C V_t 2^{-Hd+H'(q)(qd-t)}
          =(1+d)^{O(1)}V_t p^{d-t}q^t. \tag{2}
$$

### Two second-moment estimates

All expectations below use the same uniform $D\in[M,3M]$. For the initial words, $C_u/5^a$ is the sum of $3\cdot 2^i/5^{A_i}$ over their one positions. The raw prefix test gives $2^i/5^{A_i}\le2$, hence $0\le C_u\le6d\,5^a$. The $C_u$ in a group are distinct: equal $C_u$ would give equal starting residues modulo $2^d$ and identical words. Each residue modulo $5^a$ thus occurs at most $6d+1$ times. With $h=5^a$ and $h>1$, reciprocity of inverses gives
$$
 e_Q(-\xi C_u/h)=e_h(\xi C_u Q^{-1})\exp(-2\pi i\xi C_u/(Qh)).
$$
For $1\le\xi\le M$ the last factor differs from one by $O(Md/2^M)$. Also $h\le M$. The quantities $Q^{-1}=2^{-D}$ run through the units modulo $h$ in complete periods with bounded relative frequency. Indeed $2$ has order four modulo five and $v_5(2^{4\cdot5^i}-1)=i+1$ by binomial expansion. After multiplying by $\xi$ the relevant modulus is $h'=h/\gcd(\xi,h)$. Each residue modulo $h'$ has multiplicity at most $(6d+1)5^{v_5(\xi)}$. Orthogonality over all characters modulo $h'$ bounds the mean square of the unnormalized sum by this multiplicity times $V_t$. Restriction to the units costs at most a constant. The same bound is trivial for $h'=1$ (including $h=1$). Thus
$$
 \mathbb E U_{t,D}(\xi)^2\ll (1+d)5^{v_5(\xi)}/V_t. \tag{3}
$$
The exponentially small reciprocity error is absorbed since $V_t\le2^d$.

For the terminal sets, the preceding one-ended proof gives three facts. Each has size $\gg2^{Hk}/k^{3/2}$. A non-full set has $A=\lfloor(D-k)/\log_2 5\rfloor+v$ for one of $O(k)$ slots $v$. For fixed slot and flag there are $O(k)$ threshold patterns as $D$ varies. A full set gives zero at $1\le\xi\le M<2^k$. In a fixed slot each exponent $A$ occurs at most three times, so its distribution modulo $2^{k-2}$ is bounded by a constant times uniform probability. For each pattern occurring on a live prefix, enlarge its average to all $D$ in the slot, without any condition on the pattern. If $e=v_2(\xi)$, then $5^{-A}$ times the odd part of $\xi$ ranges over a coset containing at least a quarter of all residues modulo $2^{k-e}$. The number of elements of $S$ in one residue modulo $2^{k-e}$ is at most $2^e$. Orthogonality gives mean square at most $O(2^e/|S|)$ for the normalized terminal sum. Bounding the squared maximum by the sum over the slots, flags and patterns gives
$$
 \mathbb E T_D(\xi)^2\ll (1+k)^{O(1)}2^{v_2(\xi)}2^{-Hk}. \tag{4}
$$

Apply Cauchy–Schwarz to $\mathbb E(U_{t,D}T_D)$ in (1), using the deterministic bound (2) on the weights. The remaining sum is bounded by
$$
 \sum_t p^{d-t}q^t\sqrt{V_t}
 \le\sqrt{d+1}\,(p^2+q^2)^{d/2},
$$
since $V_t\le\binom dt$. Equations (3) and (4), with the chosen $d,k$, now prove
$$
 \mathbb E|\widehat\mu_D(\xi)|\ll
 (\log M)^{O(1)} 2^{v_2(\xi)/2}5^{v_5(\xi)/2}M^{-c_*}
 \qquad(1\le\xi\le M). \tag{5}
$$

### Counting the ordinary octave

Apply the Erdős–Turán inequality with cutoff $\lfloor M^{3/4}\rfloor$ to the interval discrepancy $\Delta_D=\sup_J|\mu_D(J)-|J||$ on the circle. In the Fourier sum weighted by $1/\xi$, the valuation factors in (5) cost only $O(\log M)$: write $\xi=2^i5^j l$ with $\gcd(l,10)=1$ and sum the two geometric series and the harmonic sum over $l$. Since $3/4>c_*$,
$$
 \mathbb E\Delta_D\ll M^{-c_*}(\log M)^{O(1)}.
$$
[The Erdős–Turán inequality, Montgomery and Vaughan, Theorem F.4](https://personal.science.psu.edu/rcv4/571s25/montgomery-vaughanII.pdf)

Markov's inequality discards $O_\eta(M^{1-\eta/3}(\log M)^{O(1)})$ depths at tolerance $M^{-c_*+\eta/3}$. When $D>m$, the shifted octave represents the half-open interval beginning at $(2^m+3)/2^D$ of length $2^{m-D}$ on the circle. In the asserted range that length is $\gg_\eta M^{-c_*+\eta}$, so relative error is $O_\eta(M^{-2\eta/3})$ at a retained depth. Each discarded $D$ affects at most $O(\log M)$ exponents $m$ in the range; absorbing logarithms gives the theorem. For $D\le m$ there are whole periods. The earlier exact multiplier-to-height test applies to these octaves at all the depths used here.

The estimate controls all interval locations at the discrepancy step, including the specified ordinary octave. At $b=\lceil2.4m\rceil$ the corresponding length on the circle is exponentially small in $m$, while (5) yields polynomial accuracy in $m$. This is the remaining scale gap.

The checker reconstructs the signed decomposition for three initial/middle/terminal splits and four frequencies, including frequencies divisible by two and five. It evaluates the character identities in a prime field with a primitive $2^D$-th root, so equality is exact there. It enumerates raw passing residues directly through 16 bits and by both lifts of each passing parent through 23 bits, checking the count against the independent halving-clock recurrence at every depth. [Exact signed-sum checker](check_split5_3_two_ends.py)

## Arithmetic links between permanent survivors

Fable proposed studying consecutive survivors on the same orbit. An increase in height alone does not imply that the intervening multiplier exceeds one, because an exit adds a positive constant. Selecting minima of the *multipliers* gives both properties.

**Theorem.** Suppose a positive orbit escapes. Write $y=x+3$ for shifted height and $\alpha=\log_2(5/4)$. There is an infinite increasing sequence of shifted heights $y_i$ on this orbit with the following properties.

1. Each $y_i-3$ survives forever, both in height and in raw multiplier. Every $y_i$ is divisible by 256.
2. If the link $y_i\to y_{i+1}$ contains $e$ exits, its number of expanding blocks is exactly $a=\lfloor e/\alpha\rfloor+1$. Put $r_e=(5/4)^a2^{-e}$. For $e=0$ the next height is $5y_i/4$. For $e>0$ it satisfies
   $$
   r_e y_i+3/2\ \le\ y_{i+1}\ \le\ r_e y_i+3e.
   $$
3. For each fixed integer $L\ge1$, every sufficiently late interval $[2^m,2^{m+L})$ contains at least $\lfloor L/\alpha\rfloor$ of the selected **unshifted** starts. In particular every ten consecutive sufficiently late octaves contain at least 31 selected starts. At least one octave in each such window contains four.

**Proof.** At block boundaries the map in shifted coordinates has one expansion $y\mapsto5y/4$ when $4\mid y$, and two exits $y\mapsto y/2+\beta$. The exit constant is $3/2$ for odd $y$ and $3$ for $y\equiv2\pmod4$. Let $Y_t$ be the shifted height after $t$ blocks and $P_t$ the product of their linear slopes from time zero. Use the earlier multiplier theorem in “How accurately the multipliers would track a divergent orbit.” It gives $P_t\to\infty$ and bounds $(Y_t-3)/P_t$ on an escaping orbit. Thus $Z_t=Y_t/P_t$ is bounded and positive. It is also nondecreasing, since an exit adds $\beta/P_{t+1}$ to $Z_t$ and an expansion leaves it fixed. It follows that $Z_t$ converges to a positive finite limit.

Products at distinct boundaries differ: a nonempty segment with $a$ expansions and $e$ exits has multiplier $5^a/2^{2a+e}\ne1$. Take $t_0$ to be the unique minimizer of $P_t$ over all $t\ge0$, and recursively take $t_{i+1}$ to minimize $P_t$ over $t>t_i$. These minima exist because $P_t\to\infty$. Set $y_i=Y_{t_i}$. Every later block boundary has larger relative multiplier and larger shifted height. Inside an expanding block the raw slopes relative to its start are $5,5/2,5/4$, and inside a two-step exit they are $1,1/2$. The intermediate raw heights are at least the smaller endpoint. This proves permanent survival. The first exit after $t_i$ requires at least four preceding expansions, since $(5/4)^3/2<1$. Such an exit exists since $Y_{t_i}$ has finite 2-adic valuation. Four successive expansions require $4^4\mid y_i$.

The first block of the link must expand. Hence $1<P_{t_{i+1}}/P_{t_i}\le5/4$, by minimality on the tail containing $t_i+1$. Taking logarithms gives $0<a\alpha-e\le\alpha$, which fixes $a$. If $e>0$, the last block is an exit: otherwise its predecessor would have relative multiplier smaller than the minimum on this tail. For each exit ending at $j$ in the link, its contribution to $y_{i+1}-r_e y_i$ is $\beta_j P_{t_{i+1}}/P_j$. Each ratio is at most one, and the last equals one. This proves the strip bounds.

For the count, let $x_i=y_i-3$. Then $x_i/P_{t_i}$ also tends to the same positive limit. For fixed $k$ this gives $x_{i+k}/x_i\le(5/4)^k(1+o(1))$. With $k=\lfloor L/\alpha\rfloor$ one has $(5/4)^k<2^L$ by unique factorization. Choose the last $i$ with $x_i<2^m$. For large $m$, the next $k$ starts all lie in $[2^m,2^{m+L})$. For $L=10$, $31\alpha<10<32\alpha$. This proves the claim.

**A window criterion for global eventual periodicity.** At the usual target depth $b_j=\lceil12j/5\rceil$, let $N_j$ count survivors in octave $j$. It suffices to show $\sum_{j=m}^{m+9}N_j\le30$ for infinitely many $m$. More selectively it suffices to exclude a chain of 31 survivors in infinitely many such windows if successive members must obey the link conditions above (each member is tested at the depth of its own octave). For fixed $y_i$ and $e>0$ the strip contains at most $1+\lfloor(3e-3/2)/256\rfloor$ possible multiples of 256. No uniform upper bound on $e$ along these links is known here. These criteria concern eventual periodicity and do not enumerate cycles.

### Exact grid experiment

At bit depth $D=b+1$ put $Q=2^D$. A passing word with five-count $A$ and numerator $C$ represents the shifted residue $y\equiv-5^{-A}C\pmod Q$. For each $A$ form the sorted grid of $-5^Ay\bmod Q$ for $2^m+3\le y<2^{m+1}+3$. Count both equality with a grid point and occupancy of the half-open circular gaps between consecutive grid points. The uniform reference for a gap length $g$ occurring $k$ times in a class of $W$ words is $Wkg/Q$. Only equality counts as a hit.

At the target depths for $1\le m\le16$, every class has zero exact multiplier hits. At $m=16$, $D=40$, there are 126,604 passing words, and the uniform reference for *all* exact hits is 0.007546. For the largest class ($A=17$, 98,679 words), the three gap lengths in increasing order contain 12,529, 37,534 and 48,616 numerators. Their uniform references are 12,447.3, 37,581.6 and 48,650.1. Agreement in these coarse bins gives no bound on equality at the left endpoints.

As a positive control, $m=18,D=26$ gives six unshifted starts: 278525, 281853, 303101, 348157, 435197 and 524285. The checker emits their words and exit flags, verifies total class sizes against the separate halving-clock recurrence, and cross-checks every hit list against direct raw multiplier iteration on its octave. These finite statements test multipliers; the earlier equivalence with height survival is asymptotic. [Exact grid and direct-orbit checks](check_split5_3_grid.py)

**Scope of the Fourier obstruction.** The sharp-interval obstruction above is rigorous. The global Parseval identity in Fable's review does not by itself extend it to every smooth majorant. For example, in $\mathbb Z/Q$ take a subgroup $R$ of spacing $d\mid Q$, with even $X$ and $4X<d$. For cyclic distance $|t|_Q$, the triangular majorant
$$
g(t)=\tfrac43(1-|t|_Q/(2X))_+
$$
dominates an interval of length $X$ centered at zero and has nonnegative Fourier coefficients: it is a positive multiple of the autocorrelation of an interval of length $2X$. The subgroup indicator also has nonnegative Fourier coefficients. Consequently the absolute Fourier bound for $\sum_{r\in R}g(r-t)$ is its value at $t=0$, exactly $4/3$, uniformly in $Q$. Translating the majorant preserves this bound. One may take $Q=2^D$, $d=2^{\lfloor(1-H)D\rfloor}$ and $X=2^{\lfloor5D/12\rfloor}$ for large $D$, matching the exponential sizes of the problem. This example does not settle what majorants work for the actual passing residues. It identifies why mean square alone cannot rule them all out.

## How long can a link attain either endpoint of its sharp strip?

Take a finite block segment of the type between consecutive multiplier minima. Its full relative slope is $1<r\le s=5/4$, and every nonempty proper prefix has slope strictly greater than $r$. Suppose it has $e\ge1$ exits. Write $y$ for its starting shifted height, $y'$ for its endpoint, $R=y'-ry$, $\kappa=1/\log_2 s$, $a=\lfloor\kappa e\rfloor+1$, and $\ell=2a+e$ for its number of **raw halvings**. Let $\{u\}=u-\lfloor u\rfloor$.

**Sharp bounds.** For each $e$ the exact minimum and maximum possible corrections are
$$
L_e=3(1-2^{-e}),\qquad U_e=3\sum_{k=0}^{e-1}s^{-\{\kappa k\}}.
$$
Both occur at arbitrarily large positive integer starts, even with $256\mid y,y'$. The first $e$ for which $U_e-L_e\ge256$ is 97. Thus the enclosing interval alone always contains a multiple of 256 from that point onward. Attaining a particular value inside it requires a legal path.

Let $K_j$ be the cumulative number of expansions through exit $j$, and let its additive constant be $\beta_j\in\{3/2,3\}$. The last block must be an exit. The slope just after exit $j$ is $P_j=s^{K_j}2^{-j}$, giving $R=\sum_j\beta_j r/P_j$. For $1\le j<e$, $P_j>r$ implies
$$
b_j:=a-\lfloor\kappa(e-j)\rfloor\ \le K_j\le a .
$$
Set $b_e=a$. The upper choice $K_j=a$ for every $j$ and $\beta_j=3/2$ gives the minimum. The lower choice $K_j=b_j$ for every $j$ and $\beta_j=3$ gives the maximum since $s^{b_j}2^{-j}/r=s^{\{\kappa(e-j)\}}$. These choices are forced at equality. In the maximizing schedule there are four or five expansions up to the first exit and three or four between subsequent exits. In both schedules the first expansion has slope $s>r$ (equality would force $e=0$), and the proper interior slopes all exceed $r$.

For realizability, either prescribed word has affine formula $2^\ell y'=5^a y+C$ with integral $C$. Impose $5^a y+C\equiv0\pmod{2^{\ell+8}}$, a single class because $5^a$ is odd. Every intermediate quotient is integral: reducing the final numerator at any earlier denominator removes all subsequent additive terms and leaves an odd multiple of the earlier numerator. Integrality at an expansion forces its input to be divisible by four, and at an exit with $\beta=3/2$ it forces an odd input. An exit with $\beta=3$ also requires an even output. In the maximizing word this follows from the next expansion or from the terminal divisibility. The first four expansions give $256\mid y$. Finally $U_e-L_e$ increases strictly, since the increment in $U_e$ exceeds $12/5$ and the increment in $L_e$ is at most $3/4$ for $e\ge1$. The widths at 96 and 97 lie respectively in $(255,256)$ and $(258,259)$ by exact rational arithmetic. [Sharp-strip checker](check_split5_3_link_strip.py)

**A logarithmic cutoff.** At a minimizing link, $\ell\le(1+1/(2\kappa))\log_2 y$, since its first $a$ blocks expand and $4^a\mid y$. At a maximizing link starting at any sufficiently large positive integer,
$$
\ell\le 2\log_2 y+O(1).
$$
In particular neither extremizer can constitute a whole link of at least $\lceil12m/5\rceil$ halvings starting in a sufficiently large octave $2^m\le y-3<2^{m+1}$.

To see what limits the maximizing link, put $T=2\kappa+1$ and $d=\lceil(\log_2 y+4)/T\rceil$. The number of expansions in a run after the first exit is a difference of successive floors of $\kappa n$, read in reverse order. There are at most $d+1$ possible lists of $d$ such runs: the forward list is determined by the initial fractional part, partitioned by the $d$ cut points $\{-i\kappa\}$, $1\le i\le d$. Reversal preserves the bound. Each list has at least $\kappa d-1$ expansions by telescoping, hence consumes at least $Td-2$ raw halvings. Since all exit types are fixed, integrality at the end of a list specifies its initial height in one residue class modulo at least $2^{Td-2}$ (the modulus is $2^h$ for its integer halving count $h$).

Suppose $e\ge2d+2$. Consider the first $d+2$ post-exit heights and the $d$-run lists following them. All those heights lie between $y$ and $2y$ for sufficiently large $y$. Indeed $r\le P_j<sr\le s^2$ and $Y_j=P_j(y+\sum_{i\le j}\beta_i/P_i)\le s^2(y+3j)$ for $j\le d+2$. Two lists agree. Their starting heights are congruent modulo at least $4y$, hence equal. On an escaping orbit this already contradicts nonrepetition. For any positive orbit the intervening lap has $O(\log y)$ halvings and slope $M<1$, since its affine correction is positive. All its heights are at least $y$. Each exit increases height relative to its linear part by a factor at most $1+6/y$. Returning to the same height therefore requires $1-M=O((\log y)/y)$. The earlier two-logarithm bound gives $1-M\ge c(1+\log y)^{-C}$ for these unequal powers of 5 and 2, a contradiction for large $y$. Thus $e\le2d+1$ and $\ell=Te+O(1)$ proves the claim. [Matveev's logarithm bound](https://www.mathnet.ru/eng/im314)

**A deficit on any escaping orbit.** The same counting argument gives a quantitative statement for mixed links. Call exit $j$ exceptional if $K_j\ne b_j$ or $\beta_j\ne3$. Each costs at least $12/25$ in $U_e-R$: an extra expansion reduces its maximal summand by a factor at most $4/5$, and choosing $3/2$ instead of $3$ halves it. If $D$ exits are exceptional, with $d$ as above and $y$ sufficiently large, then
$$
D\ \ge\ \max\left(0,\frac{e-2d-1}{d+1}\right),\qquad U_e-R\ \ge\ \frac{12}{25}D.
$$
Indeed among the $e-d$ possible post-exit starting positions $j=1,\ldots,e-d$, at most $(d+1)D$ have an exceptional exit among $j,\ldots,j+d$ (the bound is trivial if $e\le d$). Each remaining position has $P_j\le s^2$ and one of the same $d+1$ following run lists with all exit constants fixed. On an escape the earlier raw multiplier bound restarted at $y-3$ gives $Y_j-3\le1.000073(y-3)P_j$. Hence all these heights are below $2y$, independently of $e$, and they are distinct. At most one position per list is possible, giving the assertion. This penalizes a link for following the maximizing schedule. It gives no logarithmic upper bound on the length of an unrestricted link.

**Finite-chain convention.** The raw halving count and the number of bits determining a labeled block word can differ. For example four expansions followed by the exit $Y\mapsto Y/2+3$ require $y\equiv512\pmod{1024}$: nine raw halvings, ten parity bits. Requiring $256\mid y'$ instead gives a single class modulo $2^{17}$, since the last bit already records evenness at the endpoint. Also a one-expansion finite link can start at $y=4$; the divisibility of every interior selected start uses the continuation through four expansions or a terminal divisibility condition. These endpoint conventions preserve Fable's finite-cylinder obstruction.

## A sharp cutoff for the single-departure families

Fable asked whether a single exceptional exit, or an expansion moved earlier and repaid later, can take a nearly maximizing link to $12m/5$ halvings. Both families have the sharper uniform asymptotic cutoff
$$
\ell\le (1+o(1))\log_2 y
\qquad(y\to\infty).
$$
Here $y$ is the initial shifted positive integer and $\ell$ is the number of raw halvings in the link. The exceptional exit can be anywhere. The two ends of the moved expansion can be arbitrarily far apart. The starting orbit need not escape.

**Theorem.** Retain $s=5/4$, $\kappa=1/\log_2 s$, $T=2\kappa+1$, $a=\lfloor\kappa e\rfloor+1$, $b_i=a-\lfloor\kappa(e-i)\rfloor$, and $\theta_i=\{\kappa(e-i)\}$ for exits $1\le i\le e$. Write $K_i=b_i+u_i$ for the actual cumulative expansion count and $\beta_i\in\{3/2,3\}$ for the exit constant. Fix $B,J\ge1$. Suppose $|u_i|\le B$. Partition the exit indices into at most $J$ consecutive intervals. On each, suppose the pair $(u_i,\beta_i)$ is a function of $\theta_i$ that is constant on each of at most $J$ arcs partitioning the circle. The cuts and the function may vary with the interval and the link. For every $\eta>0$, all sufficiently large positive starts of such links have $\ell<(1+\eta)\log_2 y$, uniformly for fixed $B,J$.

For one changed exit take $u_i=0$ and split off that exit as a singleton. Moving one expansion forward gives $u_i=1$ on the interval between the two changed runs and zero elsewhere. In both cases at most three index intervals with constant values suffice. The theorem also permits a positive proportion of changed exits, for instance when the choice of exit constant is determined by membership of $\theta_i$ in a single arc. The coefficient one is sharp for each of Fable's two families: for every sufficiently large $e$ choose an interior change. Each resulting legal schedule has positive lifts $2^{\ell+8}\le y<2^{\ell+9}$ by the terminal congruence construction above. In the moved-expansion example choose the change after the first exit and repay before the last; each gap between exits still has at least two expansions. In the changed-exit example the exit with constant $3/2$ needs only integrality. Thus the lifts may require $256\mid y'$ as well.

**1. A shift that almost preserves the schedule.** Suppose to the contrary that $\ell\ge(1+\eta)\log_2 y$ along an unbounded sequence of starts. Since $\ell=Te+O(1)$, we may use just the first
$$
N=\left\lfloor(1+\eta/2)\log_2 y/T\right\rfloor
$$
exits. Fix a small $0<\delta<1/4$, to be chosen below, and put $Q=\lfloor\delta N\rfloor$. Choose $1\le q\le Q$ minimizing $\|\kappa q\|$ (distance to the nearest integer), let $k$ be the nearest integer to $\kappa q$, and put $\Delta=\|\kappa q\|>0$. Define
$$
v_i=K_{i+q}-K_i-k,\qquad n=N-q,\qquad 1\le i\le n .
$$
Always $|v_i|\le 2B+1$. Away from at most $J-1$ index intervals of length at most $q$, $i,i+q$ are in the same piece of the partition. Their phases differ by a rotation of distance $\Delta$. The floor difference $b_{i+q}-b_i$ equals $k$ except on an arc of length $\Delta$, by subtracting $\kappa q$ inside the floor. Similarly a phase cut can change the pair of labels only on an arc of that length. Endpoints can be included in these exceptional arcs.

Any $Q$ consecutive phase points have pairwise circular distance at least $\Delta$, by the minimizing choice of $q$. A closed arc of length $\Delta$ contains at most two such points. Splitting the indices into blocks of $Q$ shows that outside the index intervals above,
$$
v_i=0\quad\text{and}\quad\beta_{i+q}=\beta_i
$$
except at $O_{J,\delta}(1)$ single indices. This bound is uniform in the phase and in the sizes of continued-fraction coefficients.

**2. Subtract the two affine trajectories.** Let $Y_i$ be the shifted integer height just after exit $i$, and put $Z_i=s^{-v_i}Y_{i+q}-Y_i$. The original link has $P_i=s^{K_i}2^{-i}=r s^{\theta_i+u_i}$ at these exits, where $1<r\le s$. Hence all $P_i$ and their reciprocals are bounded in terms of $B$. In particular $Y_i=P_i(y+\sum_{j\le i}\beta_j/P_j)\asymp_B y$ for $i\le N$. Subtracting the two recurrences gives the exact identity
$$
Z_i=(P_i/P_{i-1})Z_{i-1}+g_i,\qquad
g_i=s^{-v_i}\beta_{i+q}-\beta_i\qquad(2\le i\le n).
$$
The terms $g_i$ are bounded and vanish off the exceptional set in step 1. A fixed positive integer $D$ with prime factors only 2 and 5 clears the denominators of every $Z_i$ and $g_i$, because $v_i$ ranges over a fixed finite set.

The first term of the difference is large in the ordinary absolute value. Iterating from exit 1 to exit $1+q$ and using bounded slope ratios gives
$$
Z_1=(s^k2^{-q}-1)Y_1+O_B(q).
$$
The multiplier differs from one by unique factorization, and its denominator is at most $2^{2k+q}$, with $2k+q=Tq+O(1)$. Choose $\delta$ small enough that $TQ<\tfrac12\log_2 y$ for large $y$. It follows that $|Z_1|\gg_B\sqrt y\gg N$ and $|Z_1|\ll_B y$. This is the step that prevents subtraction from reducing the identity to a vanishing subsum.

**3. Use the binary divisibility of the difference.** Write $A_i=K_i-K_1$, $H_i=2A_i+i-1$. Thus $P_i/P_1=5^{A_i}/2^{H_i}$ and $H_v-H_u=T(v-u)+O_B(1)$. Clearing the accumulated denominators gives
$$
D2^{H_n}Z_n=x_0+\sum_{i=2}^n 2^{H_i}5^{A_n-A_i}Dg_i,
\qquad x_0=5^{A_n}DZ_1 .
$$
Group the exception intervals from step 1 into disjoint intervals and keep the other exceptional indices as singletons. There are $O_{J,\delta}(1)$ groups and the sum of their spans $v-u$ is at most $Jq$ (singletons cost zero). For a group $[u,v]$, factor its term as $2^{H_u}5^{A_n-A_v}C_{u,v}$. The remaining integer satisfies
$$
|C_{u,v}|\le C_B (v-u+1)2^{T(v-u)} .
$$
Indeed each inner factor is $2^{H_i-H_u}5^{A_v-A_i}$, and $5^{A_v-A_i}/2^{H_v-H_i}=P_v/P_i$ is bounded. After division by $5^{A_n}$ the sum of the absolute values of *all* correction terms is $O_B(N)$, since $2^{H_i}/5^{A_i}=P_1/P_i$. It is smaller than $|DZ_1|$. Delete zero terms and vanishing subsums until none remain. The leading term survives every deletion.

For clarity, put $r_{10}(x)=|x||x|_2|x|_5$. For the remaining integer terms, Evertse's Theorem 2, equation (14), with places $\{\infty,2,5\}$ and subset $\{2\}$ gives, for every $\rho>0$,
$$
\left(\prod_j r_{10}(x_j)\right)\left|\sum_jx_j\right|_2
\ge c\max_j|x_j|_2\,(\max_j |x_j|)^{-\rho}.
$$
Here the number of terms is bounded independently of $y$ for fixed $J,\delta$. The sum has 2-adic norm at most $2^{-H_n}$, and $\max_j|x_j|_2\ge|DZ_1|_2$. The leading factor divided by $|DZ_1|_2$ is at most $|DZ_1|\ll_B y$. Every other factor is at most $|C_{u,v}|$, and deletion only reduces their product. Every term has ordinary size at most $2^{O_B(N+\log_2 y)}$, with this height exponent independent of $\delta$ and $\rho$. Taking logarithms yields
$$
H_n\le\log_2 y+TJq+O_{B,J,\delta}(\log N)
     +O_B(\rho(N+\log_2 y))+O_{B,J,\delta,\rho}(1).
$$
But $H_n=T(N-q)+O_B(1)$. Choose $\delta$ still smaller if necessary so that $T(J+1)\delta N<(\eta/6)\log_2 y$, then choose $\rho$ so its contribution is below $(\eta/6)\log_2 y$. The remaining errors are $o(\log y)$. This contradicts the choice of $N$ and proves the theorem. [Evertse, p. 228, Theorem 2](https://www.numdam.org/item/CM_1984__53_2_225_0.pdf)

**Two extensions.** A concatenation of any fixed number of links from this theorem has the same cutoff. Indeed the proof uses only $K_i=\kappa i+O(1)$, the piecewise description relative to a common floor, and $\ell=Te+O(1)$. The surplus in $K_i-\kappa i$ accumulates by at most a constant per link. For total exit count $e$, a local floor $\lfloor\kappa(e_{\rm local}-i_{\rm local})\rfloor$ differs from $\lfloor\kappa(e-i)\rfloor$ by an integer constant and a step function of $\theta_i$ with at most one cut. The local phase is a translate of $\theta_i$, so its other cuts translate too. On each link this gives the required description with boundedly many cuts and bounded total offset. Links with no exits each add one expansion, which alters the bounded offsets or the terminal halving count by a bounded amount. The same argument applies if the last link is truncated, since its runs have bounded lengths. An unbounded number of links is a different case.

There is also a restriction on where irregular exits can occur. Keep $|u_i|\le B$, but allow arbitrary labels on at most $J$ extra index intervals containing $L$ exits in total. Assume the rest satisfies the theorem's schedule hypothesis, with $B,J$ fixed. Along any sequence with $\ell/\log_2 y\to c>1$ finite,
$$
\liminf L/e\ \ge\ 1-1/c .
$$
In particular the lower limit is at least $7/12$ at the $12m/5$ scale. To see this use $N=e$ in the proof. If either $i$ or $i+q$ is in an extra interval $[u,v]$, put the corresponding correction in the group $[u-q,v]$ clipped to the summation range. After taking unions, the sum of spans increases by at most $L+Jq$. All estimates on $P_i$, denominators and ordinary sizes still hold by the fixed bound on $u_i$. This adds at most $TL+TJq$ to the upper estimate for $H_n$. Divide by $Te$, let $y\to\infty$ and then let $\delta,\rho\downarrow0$ to get the claim. This bounds the lengths of intervals *covering* the irregularities when their number is fixed. It does not give that density for individual changed exits scattered over many intervals.

Unrestricted links can have unbounded displacements $K_i-b_i$ or schedules requiring more and more cuts. The argument gives an asymptotic exclusion for the stated families and supplies no numerical threshold octave. [Exact checks of the shifted identity and its support](check_split5_3_shifted_links.py)
