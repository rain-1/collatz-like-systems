# Actual stopping-time counts on translated intervals

For any fixed odd integer $d$, put $T_d(x)=x/2$ at even integers and $(3x+d)/2$ at odd integers. Start at $n\ge1$. Let $x_i=T_d^i(n)$, let $a_i$ count the odd inputs in the first $i$ steps, and put $p_i=3^{a_i}/2^i$. Write $\sigma$ for the first $i\ge1$ with $x_i<n$, and $\tau$ for the first $i\ge1$ with $p_i<1$, with minimum of the empty set equal to infinity. For an interval $I$ of consecutive positive integers, let $N_\sigma(I,b)$ count $\sigma(n)>b$ and define $N_\tau$ likewise. Let $P(b)$ be the fraction of length-$b$ parity words with all prefix multipliers at least one. Every parity word represents one residue modulo $2^b$: the two lifts from depth $i$ have identical first $i$ parities and their $i$th iterates differ by $3^{a_i}$, which is odd.

**Index convention.** Survival through step $b$ means $\sigma>b$. A statement using $\sigma\ge b$ must use $P(b-1)$. Pairing $\sigma\ge b$ with $P(b)$, as in the original display of Conjecture E, fails at $b=1$: every positive start has $\sigma\ge1$, whereas $P(1)=1/2$. We study the intended count with matched indices below.

## A count law for actual heights

Write $\lambda=\log_3 2$ and $H=-\lambda\log_2\lambda-(1-\lambda)\log_2(1-\lambda)$, so $H/2=0.47497776\ldots$. **Theorem.** Fix $0<\eta<H/2$ and an odd $d$. For large $M$, apart from $O(M^{1-\eta/6})$ integer exponents $m\in[M,2M)$, the following holds simultaneously for every integer $2^m\le X<2^{m+1}$, **every interval $I$ of $X$ consecutive positive integers**, and every integer
$$
1\le b\le \log_2 X+(H/2-\eta)\log_2\log_2 X:
\qquad N_\sigma(I,b)=X P(b)\big(1+O_{d,\eta}(m^{-\eta/6})\big).
$$
In particular the prefix interval $[1,X]$ satisfies this part of Conjecture E. The exceptional indices are binary size exponents, not individual starting values. The proof uses the existing multiplier-discrepancy estimate in [the proof of Theorem D](README.md#theorem-d), in its uniform-in-intercept form.

### 1. Passing from the linear multiplier to the actual orbit

Put $p_0=1$. Dividing each affine update by its multiplier gives the exact identity
$$
\frac{x_j}{p_j}=n+\frac d3\sum_{0\le i<j,\ x_i\ {\rm odd}}\frac1{p_i}.
$$
If the two survival tests disagree by depth $b$, take $j$ to be the earlier of the two first drops. Then $j\le b$, all preceding $p_i\ge1$, and $x_j-n$ and $p_j-1$ give different answers to the strict drop test. In $(x_j-n)/p_j$, the additive term must therefore have magnitude at least $n|1-p_j^{-1}|$, even in the boundary case $x_j=n$. In particular,
$$
n\le \frac{|d|b}{3g_b},\qquad
g_b=\min_{1\le j\le b,\ 0\le a\le j}\left|1-2^j3^{-a}\right|>0. \tag{1}
$$
This applies to either sign of $d$. Matveev's bound for the two fixed rational bases $2,3$ gives $g_b\ge c(1+b)^{-C}$ for effective absolute $c,C>0$. Indeed $2^j3^{-a}-1$ is nonzero by unique factorization, the field degree and heights are fixed, and the maximum exponent is at most $b$. The case $a=0$ has gap at least one. It follows, uniformly in the interval, that
$$
 |N_\sigma(I,b)-N_\tau(I,b)|=O_d((1+b)^{C+1}). \tag{2}
$$
Thus on any range of depths where the predicted count dominates this polynomial, the two tests give equivalent relative asymptotics. At $b=O(\log X)$ the additive cost is polylogarithmic. This estimate alone does not control a predicted count of order one. Related bounds on discrepancies for the classical $d=1$ map appear in the work of Rozier and Terracol. [Matveev's estimate in Bugeaud, Mignotte and Siksek, Theorem 9.4](https://samirsiksek.github.io/siksek.github.io/papers/fibannalsfinal.pdf) · [Rozier and Terracol, Corollaries 4.4 and 5.4](https://arxiv.org/abs/2502.00948)

### 2. The same discrepancy estimate for translated blocks

Consider an interval of length $2^s$, initially at any integer offset. For $b\le s$ it contains complete periods of the coefficient survivor set, giving exactly $2^sP(b)$ coefficient survivors. For $b>s$ use the decomposition from Theorem R, writing $n=r+2^h v$, $0\le r<2^h$, at its chosen split depth $h\le s$. For each $r$, the available $v$ form **exactly $2^{s-h}$ consecutive integers**. Their first value $v_0$ may depend on both $r$ and the offset. The first $h$ parities depend only on $r$. If they contain $A$ odd steps, iteration gives
$$
 T_d^h(n)=3^A(v-v_0)+\big(T_d^h(r)+3^A v_0\big).
$$
Translation has changed only the intercept for this residue. The proof of Theorem D discards exponents for which the maximum relative discrepancy over intercepts, nontrivial odd-count slots and their threshold patterns exceeds its tolerance at any tested depth. The exponents retained by that proof therefore give the same relative bound **simultaneously at every offset**. For odd $d$ the continuation sets are the $d$-multiples of those for $d=1$ modulo the probing power of two. The same estimate applies on the multiplier coset $d^{-1}\langle3\rangle$, as in Theorem D's extension to odd $d$. [Theorem R and the coset discrepancy estimate](README.md#2-theorem-r-the-reduction-proved)

**The entropy constant in the dyadic estimate.** Here are the details of the averaged bound, replacing the earlier numerical lower bound on the survival exponent by $H$. Let $W_k$ be the number of surviving $k$-bit words. At least $\binom{k}{\lceil k\lambda\rceil}/k$ words survive. Indeed, for every word with exactly $\lceil k\lambda\rceil$ ones, sum its successive increments $e_i-\lambda$. The total is positive. Rotating just after a least partial sum (including the initial zero) makes all prefix sums nonnegative, and any surviving word has at most $k$ rotations. Stirling's formula therefore gives $W_k\gg 2^{Hk}/k^{3/2}$. The matching exponential upper bound follows by counting words with at least $\lceil k\lambda\rceil$ ones. In particular $P(b)=2^{-(1-H)b+o(b)}$.

For clarity, take $k=\lfloor\log_2 M\rfloor+2$, $Q=2^k$, $j=b-s>0$, and $h=s-(k-j)$ in the preceding decomposition. We need $2j\le k$. A prefix with $A$ ones survives a continuation precisely when its odd counts at lengths $i\le k$ are at least $\lceil(h+i)\lambda\rceil-A$. For each nontrivial slot $A=\lceil h\lambda\rceil+v$ there are at most $k+1$ such threshold patterns, by varying the fractional part of $h\lambda$ across the $k$ breakpoints. There are $O(k)$ nontrivial slots; larger $v$ accepts every continuation. Each continuation set $S\subseteq\mathbb Z/Q$ has at least $W_k$ elements, since its thresholds are at most $\lceil i\lambda\rceil$. For $d\ne1$ one can use the same sets after multiplying every continuation argument by $d^{-1}$ modulo $Q$: $T_d(dx)=dT_1(x)$ on the 2-adic integers.

For $N=2^{k-j}$, let $\Phi(u,B)=\sum_{t=0}^{N-1}1_S(ut+B)$ and $G(\xi)=\sum_{t=0}^{N-1}e^{2\pi\mathrm{i}t\xi/Q}$. The mean of $\Phi$ over $B$ is $|S|2^{-j}$. For $u$ uniform on $d^{-1}\langle3\rangle$ modulo $Q$, Fourier inversion and the triangle inequality give
$$
 \mathbb E_u\max_B |\Phi(u,B)-|S|2^{-j}|
 \le Q^{-1}\sum_{\xi\ne0}|\widehat {1_S}(\xi)|\,\mathbb E_u |G(u\xi)|
 \ll k\sqrt{|S|}.
$$
Indeed for a frequency of order $2^l$, the geometric sum vanishes when $2^l\mid N$. Otherwise its mean magnitude is $O(l)$ by summing $1/(2\|a/2^l\|)$ over odd residues $a$. The multiplier coset occupies at least a quarter of all residues at this level: for $l\ge3$ the order of $3$ is $2^{l-2}$, by $v_2(3^{2^t}-1)=t+2$ for $t\ge1$ (induction by squaring). Finally Cauchy–Schwarz and Parseval bound the sum of the Fourier magnitudes by $Q\sqrt{|S|}$.

As $s$ runs from $M$ to $2M-1$, each $A=\lceil h\lambda\rceil+v$ occurs at most twice, in an interval of length $O(M)$. Each exponent residue modulo $2^{k-2}\le M$ thus occurs $O(M/2^{k-2})$ times. Markov's inequality and the preceding Fourier estimate show that, after taking the union over slots and patterns, at most
$$
 O\!\left(\frac{M k^3 2^j}{\epsilon\sqrt{W_k}}\right)
$$
exponents $s$ have any relative discrepancy exceeding $\epsilon$. This event already takes the maximum over $B$. Outside it, summing over prefix residues gives the same relative error against $2^sP(b)$: the slot means sum to this quantity by counting all length-$b$ survivors and dividing by $2^j$. For $0<\theta<H/2$, sum the bound over $1\le j\le (H/2-\theta)\log_2(2M)$ and take $\epsilon=M^{-\theta/3}$. The entropy bound on $W_k$ leaves $O(M^{1-2\theta/3}(\log M)^{15/4})=O(M^{1-\theta/3})$ exceptions. This supplies the translated dyadic estimate with $H/2$.

### 3. Removing the restriction on interval length

Use the dyadic result with parameter $\eta/2$. Fix $L=\lfloor(\eta/4)\log_2 M\rfloor$ and put $s=m-L$. Discard the first $L$ possible $m$ and those for which $s$ is exceptional in $[M,2M)$. The number discarded is $O(M^{1-\eta/6})$. For every remaining $m$, the relative error on length-$2^s$ blocks is $O(M^{-\eta/6})$ through depth $s+(H/2-\eta/2)\log_2 s$. This covers the whole asserted range: $\log_2 X<m+1$, $\log_2 s=\log_2 m+o(1)$, and the loss $L+1$ is smaller than the margin $(\eta/2)\log_2 m$ for large $M$.

Tile $I$ from its left endpoint by whole blocks of length $2^s$. Sandwich its count between the counts of the union of whole blocks and that union extended by one further whole block. Since $2^s/X\le2^{-L}=O(M^{-\eta/4})$, this proves the stated relative estimate for $N_\tau$. Apply (2) once to $I$. To see that its error is negligible, the words 110 and 111 (1 denotes odd) both survive every prefix and finish above multiplier one. Concatenation and a final string of ones give $2^b P(b)\ge2^{\lfloor b/3\rfloor}$. Throughout this range $XP(b)\ge 2^{m/3-O(\log m)}$, which dominates every fixed power of $b=O(m)$. This proves the theorem.

## An exact check through 3,012 steps, for all positive starts

At $b=3012$ the minimum in (1) is attained at $(j,a)=(1054,665)$. Exact arithmetic gives $\lfloor b/(3g_b)\rfloor=22{,}999{,}481$. For each $a$ it suffices to test the admissible powers of two immediately below and above $3^a$, or the nearest allowed endpoint. The checker then iterates each odd start up to that bound until either test first drops or the depth is exhausted. Every even start drops by both tests at step one.

* For $3x+1$ the sole first disagreement is $n=1$ at step 2. Its orbit alternates between 1 and 2, so for $2\le b\le3012$ the actual count equals the coefficient count plus one if the interval contains 1.
* For $3x-1$ the two counts agree exactly on **every** interval through step 3012.

The depth includes every recorded finite instance of Theorem C at $m\le3000$ and $j\le12$. Its certified coefficient intervals therefore transfer exactly with the indicated correction. This finite certificate is deliberately self-contained; stronger classical-map computational information is already in Rozier and Terracol. [Exact checker](check_actual_transfer.py)

## Remaining question

By (2) and the entropy estimate, below any fixed depth $K\log_2 X$ with $K<1/(1-H)=19.9822\ldots$, relative asymptotics for the coefficient counts would suffice for actual counts: $XP(b)$ grows as a positive power of $X$ uniformly in that range. Proving those coefficient asymptotics is still open beyond the range of the theorem. Conjecture E asks for every size exponent and every depth up to $K\log_2 X$ for each fixed $K$, including the range where the expected count vanishes. The uniform-in-intercept average handles only most exponents, and the additive estimate (2) alone cannot resolve individual survivors at the critical depth. No global Collatz conclusion follows from the theorem.
