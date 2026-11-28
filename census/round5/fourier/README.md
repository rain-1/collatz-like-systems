# Round 5, lens "Fourier and Diophantine formulation" (27 Nov 2026)

Status: written by one agent, refereed once (`REFEREE1.md`) and revised; the section "Revision after
REFEREE1" at the end lists every change; refereed a second time (`REFEREE2.md`, all proofs confirmed)
and revised for wording (section "Revision after REFEREE2"). Statements corrected in either revision are marked [revised] in place. Labels: PROVED (complete proof below, finite content
checked by `check_fourier.py`, which exits 0 and fails under mutation), EVIDENCE (numerics),
OPEN, CONJECTURE. Nothing here settles GLOBAL for any system.

**Outcome in one paragraph.** Conjecture E is a statement about the Fourier coefficients of
mu_b at the frequencies xi with v_p(xi) < m, where m = b - log_p X is the number of digits past
the horizon. That is an exact identity (F1). E at a bounded distance past the horizon is
equivalent to mu_b -> Lebesgue, i.e. to mu_b^(xi) -> 0 for each fixed xi (F2). Theorem U is a
transfer bound that holds uniformly in the depth. It turns a finite computation at depth L into
a statement about EVERY depth b >= L. For 3x+1 it proves that for every b >= 22 the number of
n < 2^(b-1) (resp. 2^(b-2), 2^(b-3)) that survive b halvings is within 19.5% (resp. 43.3%, 87.8%)
of the Haar prediction. [revised: the exact form U' improves this to 12.21% for b >= 16 and 28.44%,
46.60% for b >= 14, in integer arithmetic, and gives 28.79% (m = 1, b >= 17) and 77.22% (m = 2) for K7, and 68% (m = 1) for
split5_3 for b >= 16; see R-B.] This is a real statement 1 to 3 digits past the horizon, but a weak one. [revised:
the original sentence "trivial monotonicity gives bounds of the same size" is true only for m = 1; see R-B.]
On the negative side, [revised, see R-A] no argument that uses only the moduli |mu_b^(xi)| can ever
certify N(X, b) = 0, and the Fourier (L1) criterion needs X P(b) > 1/2 to certify anything. So no
Fourier-decay hypothesis of this type can give the minimal form M. Under the
numerically supported square-root hypothesis H, it gives E exactly up to b = log_p X / (1 - h/2),
short of the critical C* = 1/(1 - h). I also found an error in the lead's derivation of M from E: with
the additive error X^{eps}, the stated inference is invalid (section 6; [revised wording, see R-D]).
Numerically, the top-level coefficients do NOT decay with b. [revised, see R-E] For 3x+1 and K7 the
worst frequency of each 2-adic class is xi = +-2^v u^a modulo the period 2^{b-w} of |mu_b^|, with
|a - ((b - v) log_u 2 - 1)| <= 1, where u is the multiplier; for split5_3 this is not so. So a Tao-type uniform decay statement for the
survival-conditioned 2-adic Syracuse variable is false in the range tested.

## Results table

| id | statement | status |
|---|---|---|
| F1 | exact Fourier identity for N(k p^{b-m}, b) - X P(b); only frequencies with v_p(xi) < m enter | PROVED |
| F2 | E at bounded distance past the horizon <=> mu_b -> Leb weakly <=> mu_b^(xi) -> 0 for each fixed xi | PROVED |
| F3 | hypothesis H(eps) (L1 square-root cancellation) => E for b <= log_p X / (1 - (1/2 - 2 eps) h), every X [revised: eps margin and general X, R-C] | PROVED (conditional) |
| F4 | the Fourier L1 criterion has B_F >= (2/pi)(1/(2 X P(b)) - 1) [superseded by F4' for the consequence] | PROVED |
| F4' | translation bound: B_F >= 1/(X P(b)) - 1, and (1 + B_F) X P(b) >= 1 always (R-A) | PROVED |
| Mod | no property of the moduli \|mu_b^(xi)\| alone implies N(X, b) = 0 (or = 0 on any interval); so moduli-only Fourier arguments cannot give slope-sense M, nor E_0 for 3x+1 (R-A) | PROVED |
| T | transfer identity: survivors above a node r1 are an affine image u^{-1}(All(sigma,A) - c) of a finite set | PROVED, checked exactly |
| U | for all b >= L: \|mu_b^(xi)\| <= kappa_{L,v(xi)} and \|N/(XP) - 1\| <= D_{L,m,k} | PROVED |
| U-3x+1 | for every b >= 22: \|N(2^{b-m}, b) / (2^{b-m} P(b)) - 1\| <= 0.195, 0.433, 0.878 for m = 1, 2, 3 | PROVED (FFT in double precision); superseded by U' |
| U' | exact (integer) form of U(ii): 3x+1, every b >= 14: <= 213/1627 = 0.1310, 213/749 = 0.2844, 349/749 = 0.4660 (m = 1, 2, 3; k = 1); every b >= 16: m = 1 <= 129/1057 = 0.1221; same for 3x-1, 3x+5 (slope sense, b >= 14); K7: 19/52 = 0.3654 (b >= 16), 19/66 = 0.2879 and 61/79 = 0.7722 (m = 1, 2; b >= 17); split5_3, b >= 16: 17/25 = 0.68 (m = 1) (R-B) | PROVED (exact arithmetic) |
| Z | 3x+1: if no power of 3 is in [2^{b-1}, 2^b), then R_b = R_b + 2^{b-1}, all odd-frequency coefficients vanish, and N(2^{b-1}, b) = \|R_b\|/2 exactly | PROVED (a restatement of in-horizon data) |
| S | 3x+1: r = -sum_k 3^{-k} 2^{e_k} (mod 2^b) on R_b, so mu_b^ is the characteristic function of a survival-conditioned 2-adic Syracuse variable | PROVED |
| G | the derivation of M from E in CONJECTURE.md is invalid (E's inequality allows one never-dropping start per scale); E_0, stated for the actual-drop count, implies M (R-D) [revised wording] | PROVED (logic) |
| N1 | low Archimedean frequencies decay at the square-root rate: max_{1<=xi<=64} \|mu_b^\| / \|R_b\|^{-1/2} in [1.28, 3.11] (3x+1, b = 16..28) [revised: was "~1.5"] | EVIDENCE |
| N2 | top-level sup does not decay: max over odd xi stays about 0.05 for 3x+1 at b = 20..27 (0.0485 at b = 20; exactly 0 at the Proposition Z depths b = 22, 25) (random set: 0.021 at b = 20, 0.004 at b = 26); ratio to the random set 2.3 to 13 (3x+1), 1.3 to 3.8 (K7), 0.7 to 2.0 (split5_3) [revised: "10 to 50 times" was wrong] | EVIDENCE |
| N3 | 3x+1, K7: worst frequency of each class v_2 = v is xi = +-2^v u^a mod 2^{b-w} (w = 2, 5 the symmetry of R_b), \|a - ((b-v) log_u 2 - 1)\| <= 1; split5_3: WITHDRAWN (R-E) [revised] | EVIDENCE |
| N4 | H holds on the data: B_F(b, m) / (2^m \|R_b\|^{-1/2}) ~ 1.3-1.9 (3x+1), 2.5-3.3 (K7), 3.3-4.2 (split5_3), b = 18..26 | EVIDENCE |
| E | Conjecture E itself, and E_bdd (bounded distance past the horizon) | OPEN |

## Setting and notation

Base-2 table maps (split5_3, 3x+1, K7, defined exactly as in `../../round4/lead/survive.c`).
R_b is the set of residues r mod 2^b whose node in the digit tree (round 3, `density/theory.md`,
Lemma 1: a step is applied only when the known digits decide it) keeps slope U/2^h >= 1 after
every step. Here b counts DIGITS of the start. For 3x+1 digits and halvings coincide. For
split5_3 and K7 they differ by at most one pending digit. P(b) = |R_b|/2^b. N(X, b) = #{0 <= n < X :
n in R_b} is the slope-sense survivor count. For X <= 2^b each integer n < X is its own residue, so
for b > log_2 X this counts integers past their horizon. All theorems are about this slope-sense
count. The lead's data use the actual value (n dropped below itself). For +d systems the two
counts differ by the intercept term. I did not treat that difference.

mu_b is the uniform probability on {r/2^b : r in R_b} in R/Z,
mu_b^(xi) = |R_b|^{-1} sum_{r in R_b} e(xi r / 2^b). The integer frequency xi has 2-adic level
j = b - v_2(xi). Low Archimedean frequencies (small |xi|) are top-level (odd xi) or near-top-level
characters. That is how the p-adic and Archimedean structures meet.

## 1. The Fourier identity (F1, PROVED)

Let X = k p^{b-m} with 1 <= k <= p^m. With S^(xi) = sum_{r in R_b} e(-r xi/p^b) and
I^(xi) = sum_{0<=x<X} e(-x xi/p^b), Plancherel on Z/p^b gives

    N(X, b) - X P(b) = p^{-b} sum_{xi != 0, v_p(xi) < m} S^(xi) conj(I^(xi)),

because I^(xi) = 0 whenever v_p(xi) >= m: then e(-x xi/p^b) depends on x mod p^{b-v} with
b - v <= b - m, and [0, k p^{b-m}) runs through each such residue k p^{v-m} times (check [4]).
Dividing by X P(b) = X |R_b| / p^b:

    | N(X,b) / (X P(b)) - 1 |  <=  B_F(b, m) := X^{-1} sum_{xi != 0, v_p(xi) < m} |mu_b^(xi)| |I^(xi)|,

with |I^(xi)| = |sin(pi X xi/p^b) / sin(pi xi/p^b)|. So m digits past the horizon involve
exactly the frequencies of level > b - m, weighted by the Dirichlet kernel of length X.

## 2. Bounded distance past the horizon (F2, PROVED)

**Theorem F2.** For a fixed system the following are equivalent:
(a) for all fixed m >= 1 and 1 <= k <= p^m, N(k p^{b-m}, b) / (k p^{b-m} P(b)) -> 1 as b -> inf;
(b) mu_b -> Lebesgue weak-*; (c) mu_b^(xi) -> 0 for every fixed integer xi != 0.

*Proof.* N(k p^{b-m}, b) / (k p^{b-m} P(b)) = mu_b([0, k/p^m)) / (k/p^m). (a) => (b): (a) gives
mu_b(J) -> |J| for every interval J with endpoints in p^{-m}Z, for every m. A continuous f on
R/Z is uniformly within eps of a step function constant on the intervals of the grid p^{-m}Z
(uniform continuity), so lim sup |int f dmu_b - int f| <= 2 eps. (b) => (c): x -> e(xi x) is
continuous. (c) => (b): trigonometric polynomials are uniformly dense in C(R/Z) (Fejer), and
the coefficients are bounded by 1. (b) => (a): the boundary of [0, k/p^m) has Lebesgue measure 0
(portmanteau). ∎

So E_bdd, the weakest form of E that still says something past the horizon, is exactly
pointwise Fourier decay of mu_b. EVIDENCE N1: the low frequencies decay at the square-root rate
(table in section 5). E_bdd is OPEN for every system. Theorem U below gives bounded errors,
not errors tending to 0.

## 3. Conditional theorem and its ceiling (F3, F4)

**Hypothesis H(eps).** There are C and b_0 with B_F(b, m) <= C p^m |R_b|^{-1/2+eps} for all
b >= b_0 and 1 <= m <= b.

**Theorem F3 (PROVED, conditional).** Under H(eps), for X = p^{b-m},
|N(X,b)/(X P(b)) - 1| <= C p^{m} |R_b|^{-1/2+eps}. Since |R_b| = p^{h b + o(b)}
(round 3, Theorem 3 there), the error tends to 0 whenever m <= (1/2 - 2 eps) h b. Writing
log_p X = b - m, this is E for b <= log_p X / (1 - (1/2 - 2eps) h). *Proof:* F1. ∎
[revised: this version covers only X = p^{b-m}; the version for every X is F3' in R-C. The results
table previously said "(1/2 - eps)"; the correct margin is (1/2 - 2 eps), as here.]

Ranges: 3x+1 (h = 0.94996): b up to 1.90 log_2 X; split5_3 (h = 0.58068): up to 1.41 log_2 X.
The critical constants are C* = 19.98 and 2.385. H can therefore give E well past the horizon,
but it does not reach C*.

**Theorem F4 (PROVED; the ceiling of the method).** For every b, m and X = k p^{b-m}:

    B_F(b, m) >= (2/pi) (1/(2 X P(b)) - 1).

So B_F < 1 forces X P(b) > 1/(2 + pi) = 0.194. *Proof.* For 0 < |xi| <= Z := floor(p^b/(2X)) we have
|X xi/p^b| <= 1/2, so |sin(pi X xi/p^b)| >= 2 X |xi|/p^b and |sin(pi xi/p^b)| <= pi |xi|/p^b, hence
|I^(xi)| >= 2X/pi. These xi have |xi| < p^m, so v_p(xi) < m and they occur in B_F. Then
B_F >= (2/pi) sum_{0<|xi|<=Z} |mu_b^(xi)| >= (2/pi) sum_{0<|xi|<=Z} |mu_b^(xi)|^2, using |mu^| <= 1.
Fejer: F_Z(x) = sum_{|xi|<=Z} (1 - |xi|/(Z+1)) e(xi x) >= 0 and F_Z(0) = Z + 1, so
sum_{|xi|<=Z} |S^(xi)|^2 >= sum_{r,s in R_b} F_Z((r-s)/p^b) >= |R_b|(Z+1). Hence
sum_{0<|xi|<=Z} |mu_b^|^2 >= (Z+1)/|R_b| - 1 >= p^b/(2X|R_b|) - 1 = 1/(2 X P(b)) - 1. ∎ (check [5])

Consequence: M and the "+o(1)" form E_0 of section 6 live where X P(b) -> 0. There every
bound obtained by putting absolute values on Fourier coefficients is >= 1. **No Fourier-decay
hypothesis used through absolute values can prove M.** A proof of M must use the signs (the
phases) of the coefficients, not their sizes. [revised: F4 does NOT prove this. F4 gives only
(1 + B_F) X P >= 1/pi + O(X P), which can be below 1 (0.33 at b = 16, m = 16 for 3x+1), so F4
leaves an N = 0 certificate possible. The consequence is true, and is proved in R-A by a
translation argument (F4' and Proposition Mod), which also covers smooth majorants.] For a random set of the same size the true error
is sqrt(X P(b)), so the phases carry the cancellation.

## 4. The transfer identity and the uniform bound (T, U, PROVED)

**Lemma T.** Let r1 mod p^j be a node that is alive after its decided steps, with x its value
at t = 0, U the product of multipliers (a unit), h the number of halvings, s = j - h,
sigma = (s, x mod p^s) its state, A = U/p^h >= 1. For z mod p^L let g_sigma(z) be the minimum
prefix slope of the decided steps from the value x mod p^s + p^s z with s + L known digits
(the starting value 1 included). Then for t < p^L:

    r1 + p^j t in R_{j+L}   <=>   z(t) := (U t + floor(x/p^s)) mod p^L  lies in  All(sigma, A) = { z : A g_sigma(z) >= 1 }.

*Proof.* The decided steps for n = r1 + p^j t are those for r1, because decidedness only grows
with the number of known digits. They take n to (U n + C)/p^h = x + U p^s t
= (x mod p^s) + p^s (U t + floor(x/p^s)). The later steps are decided by the s + L known digits of
this value, which are (x mod p^s) and z(t) mod p^L. They are exactly the steps in the definition
of g_sigma, with every slope multiplied by A. The earlier prefixes have slope >= 1 because r1
is alive. ∎ (check [2]: all r1, three systems, (j, L) in {(5,6), (8,6), (7,9)}.)

t -> z(t) is an affine bijection of Z/p^L (U is a unit). All(sigma, A) depends only on the
state and the threshold, so there are finitely many such sets for each L. As A runs over [1, inf)
they are the super-level sets {g_sigma >= gamma}.

**Theorem U.** Fix L. For every b >= L:

(i) for every xi with v = v_p(xi) < L: |mu_b^(xi)| <= kappa_{L,v}, the maximum over states sigma,
thresholds A >= 1 and c with v_p(c) = v of |sum_{z in All(sigma,A)} e(cz/p^L)| / |All(sigma,A)|;

(ii) for X = k p^{b-m} with m < L: |N(X,b)/(X P(b)) - 1| <= D_{L,m,k}, the maximum over the same
sets S = All(sigma, A) of
(p^m/(k p^L |S|)) sum_{v<m} < sorted |S^| on the class v_p = v , sorted |I_k^| on the class v_p = v >,
where I_k = [0, k p^{L-m}) in Z/p^L and both lists are sorted in decreasing order.

*Proof.* Write r in R_b as r1 + p^{b-L} t (j = b - L). By Lemma T,
sum_{r in R_b} e(xi r/p^b) = sum_{r1 alive} e(xi r1/p^b) sum_{z in All(r1)} e(xi U^{-1}(z - x')/p^L),
x' = floor(x/p^s). The inner sum has modulus |All^(xi U^{-1})| <= kappa |All(r1)|, and
v_p(xi U^{-1}) = v_p(xi). Summing, and using sum_{r1} |All(r1)| = |R_b|, gives (i). For (ii),
r < X iff t < k p^{L-m}. So N(X, b) = sum_{r1} #{z in All(r1) : U^{-1}(z - x') mod p^L in I_k}. The
deviation of each term from |All(r1)| k p^{-m} is, by Plancherel on Z/p^L,
p^{-L} sum_{xi != 0} All^(U^{-1} xi) conj(I_k^(xi)) times a phase. Only v_p(xi) < m survive
(annihilation). Multiplication by U^{-1} permutes each valuation class, so the rearrangement
inequality bounds the absolute sum by the sorted pairing. Sum over r1 and divide by
X P(b) = sum_{r1} |All(r1)| k p^{-m}. ∎

**Numbers** (`fourier_bound.py`; rearrangement bound, max over all states and thresholds):

| system | L | smallest set | kappa_{L,0} | D_{L,1} | D_{L,2} | D_{L,3} |
|---|---|---|---|---|---|---|
| 3x+1 | 16 | 2114 | 0.0872 | 0.379 | 0.857 | 1.72 |
| 3x+1 | 18 | 7495 | 0.0742 | 0.304 | 0.687 | 1.37 |
| 3x+1 | 20 | 27328 | 0.0650 | 0.242 | 0.545 | 1.11 |
| 3x+1 | 22 | 93222 | 0.0588 | **0.1948** | **0.4330** | **0.8777** |
| 3x+1 | 24 | 286581 | 0.0588 | 0.245 | | |
| K7 | 16 | 104 | 0.292 | 1.54 | 3.31 | 6.59 |
| K7 | 22 | 1966 | 0.187 | 0.999 | 2.10 | |
| split5_3 | 16 | 16 | 0.603 | 2.53 | 5.66 | 11.2 |
| split5_3 | 22 | 85 | 0.531 | 3.50 | | |

All entries are for k = 1. Every bound holds for all b >= L, so the best bound at depth b is the
minimum over L <= b. Consequence **U-3x+1**: for every b >= 22 and m = 1, 2, 3,
|N(2^{b-m}, b) / (2^{b-m} P(b)) - 1| <= 0.1948, 0.4330, 0.8777. Check [7] compares this with the
exact counts at b = 22, ..., 30 (`topdigits.txt`). The observed deviations are below 0.003.
Theorem U is valid but lossy by about two orders of magnitude.

**Honest assessment of U.** U does say something about integers past their horizon: m digits
past, uniformly in b, with an explicit error. But (1) the error does not tend to 0, and D does not
even decrease monotonically in L (L = 24 is worse than L = 22). (2) At a FIXED b the trivial
sandwich |R_b| - |R_{b-1}| <= N(2^{b-1}, b) <= |R_{b-1}| gives bounds of the same size: for 3x+1 at
b = 24 it gives [0.822, 1.178]. [revised: true for m = 1 only; for m = 2, 3 the sandwich is much
weaker than U' (up to 1.17 and 2.72 against 0.284 and 0.466), see R-B and `sandwich.txt`.] U's only advantage is uniformity in b, and the trivial sandwich
would be uniform too once P(b-1)/P(b) is bounded uniformly. (3) For split5_3 and K7 the allowed
sets at the accessible L are too small (85 and 1966 elements at L = 22). U gives nothing for
split5_3 (D_{22,1} = 3.5) and only the near-trivial D_{22,1} = 0.999 for K7. So U is a correct reduction of "bounded distance past the horizon, with bounded error"
to finite computations, but it does not prove anything that is not already nearly visible in
the in-horizon data. I do not claim it as a success of type (1) in substance. [revised after REFEREE2:
formally U, and its exact form U' (R-B), are type-(1) statements, beyond the horizon and uniform in b,
which is how R-B describes U'; "not in substance" means they are weak ones, with a bounded,
non-vanishing error over boundedly many digits.]

**Proposition Z (PROVED).** For 3x+1, if no power of 3 lies in [2^{b-1}, 2^b), then every node
alive after b - 1 halvings has slope 3^a/2^{b-1} >= 2. So both lifts survive, R_b = R_b + 2^{b-1},
mu_b^(xi) = 0 for all odd xi, and N(2^{b-1}, b) = |R_b|/2 exactly. This happens for about 37% of b
(b = 14, 17, 19, 22, 25, ...; check [6]). It is the clearest example of a "past the horizon"
statement that is really in-horizon.

## 5. Numerics (EVIDENCE)

Exact R_b from `rb.c`; FFTs in `spectrum.py`, `decay.py`, `profile.py`, `powers.py`, `l1test.py`.
Outputs: `spectrum_b24.txt`, `decay.txt`, `decay_c31_28.txt`, `profile_b26.txt`, `powers_b24.txt`, `l1test_b26.txt`, `l1_vs_b.txt`.

**Per-level maxima (b = 24).** At low levels j the coefficients are large (structure of Omega mod
p^j: level 1 or 2 has |mu^| = 1 for all three systems, since every survivor is odd, or 3 mod 4 for
split5_3). All levels sit above the Parseval floor |R_j|^{-1/2}. Selected values of max |mu^| at
level j (3x+1 / K7 / split5_3): j=8: 0.29 / 0.67 / 1.00; j=12: 0.125 / 0.45 / 0.71; j=16:
0.12 / 0.31 / 0.60; j=24: 0.056 / 0.18 / 0.17. Random set of equal size: 0.007 / 0.068 / 0.25.

**Top level and low frequencies against b** (`decay.txt`, 3x+1; similar for K7):

| b | \|R_b\| | max over odd xi | max over 1 <= xi <= 64 | \|R_b\|^{-1/2} | random, odd xi |
|---|---|---|---|---|---|
| 16 | 2114 | 0.0860 | 0.0278 | 0.0218 | 0.070 |
| 20 | 27328 | 0.0485 | 0.0099 | 0.0060 | 0.021 |
| 23 | 168807 | 0.0562 | 0.0051 | 0.0024 | 0.0098 |
| 24 | 286581 | 0.0563 | 0.0042 | 0.0019 | 0.0075 |
| 26 | 1037374 | 0.0525 | 0.0015 | 0.0010 | 0.0040 |
| 27 | 1762293 | 0.0541 (at xi = 3^15 exactly) | 0.0023 | 0.00075 | 0.0032 |
| 28 | 3524586 | 0 (Proposition Z) | 0.0011 | 0.00053 | 0.0023 |

At b = 14, 17, 19, 22, 25 the odd-frequency maximum is exactly 0 (Proposition Z).

* N1: the low Archimedean frequencies decay like |R_b|^{-1/2}, i.e. like 2^{-0.47 b} for 3x+1.
  That is square-root cancellation, slightly better than a random set. The dyadic profile
  (`profile_b26.txt`) is random-like up to |xi| ~ 2^7. Above that it grows with the level
  structure, because frequencies of level j have |xi| >= 2^{b-j}.
* N2/N3: the sup over top-level (odd) frequencies does not decay between b = 20 and 26. It is
  10 to 50 times the random baseline [WRONG, withdrawn: it is 10 to 50 times |R_b|^{-1/2}; against
  the random-set baseline the ratio is 2.3 to 13 for 3x+1, see R-E]. The maximisers are exactly
  xi = +-2^v 3^a (3x+1, K7) or +-2^v 5^a (split5_3) [revised: "exactly" means modulo the period
  2^{b-w} of |mu_b^|, with a small; this holds for 3x+1 and K7 and is WITHDRAWN for split5_3, R-E]. For 3x+1 at b = 24 the peak is at xi = 3^14 mod 2^22 = 588665. The
  profile over a (`powers_b24.txt`) peaks sharply at
  a = 13, 14 (v = 0), 13 (v = 1), 12 (v = 2), 11 (v = 4), i.e. a ~ (b - v) log_3 2 - 1.
  Mechanism (identity S): for r in R_b with A(r) odd steps, 3^A r + C(r) = 2^b x_b(r) with
  C(r) = sum_k 3^{A-k} 2^{e_k} a positive integer. So e(3^A r/2^b) = e(-C(r)/2^b), the
  ARCHIMEDEAN quantity C(r)/2^b = (3^A/2^b) sum_k 2^{e_k}/3^k. At xi = 3^A the 2-adic character
  becomes a real phase of a bounded-size real number, which is not equidistributed mod 1
  for the boundary survivors. This is the "middle digits of u^A s" structure of the lead's
  S-unit form, seen directly in the spectrum.
* N4: hypothesis H on the data (`l1test_b26.txt`, `l1_vs_b.txt`). B_F(b, m) roughly doubles with
  each m, and B_F/(2^m |R_b|^{-1/2}) = 1.54, 1.54, 1.35, 1.92, 1.84 for 3x+1 at b = 18, 20, 22,
  24, 26 (m = 6). The ratio is 2.5 to 3.3 for K7 and 3.3 to 4.2 for split5_3, with slow growth
  (consistent with |R_b|^{eps} or a log). At b = 26 the criterion certifies the 3x+1 count for
  m <= 9 (b = 1.53 log_2 X; B_F(9) = 0.87) and fails from m = 10 on. The actual deviation stays
  below 2.1% up to m = 12. This is the predicted ceiling 1/(1 - h/2) in action.

## 6. A gap in "E => M" (PROVED, logic) and the corrected form

E allows the additive error X^{eps(X)} >= 1. At b = K log_p X with K > C* the main term X P(b)
tends to 0, but the bound N(X, b) <= o(1) + X^{eps(X)} never forces N(X, b) = 0. So E is
compatible with one exceptional n per scale, and the claimed consequence "sigma(n) <= (C* + eps)
log_p n for all but finitely many n" does not follow. A form that does imply M:

**E_0.** For every K there is eps(X) -> 0 such that for b <= K log_p X,
N(X, b) <= (1 + eps) X P(b) + #{n < X : n in Exc} + eps(X), where Exc is the finite set of starts
that never drop (cycle minima of 3x-1, 3x+5, ...). [revised: here N MUST be the lead's actual-drop
count #{n <= X : sigma(n) >= b}, not the slope-sense count of the rest of this README; see R-D for
the corrected statement and why the slope-sense version does not give M.]

*E_0 => M.* Take a non-exceptional n with sigma(n) >= (C* + eta) log_p n. Apply E_0 at
X = n + 1 and b = ceil((C* + eta) log_p n). The left side minus #Exc counts n, so it is >= 1. The
right side minus #Exc is (1 + eps) X^{-eta(1-h) + o(1)} + eps(X) < 1 for large n. ∎
[revised] By Proposition Mod (R-A; not by F4, as first written), for 3x+1 E_0 is out of reach of
every argument that uses only the moduli of the Fourier coefficients of mu_b.

## 7. Literature: what is closest and why it does not apply

* **Tao, "Almost all orbits of the Collatz map attain almost bounded values"**, arXiv:1909.03562.
  Checked: the abstract says the proof rests on estimating the characteristic function of a
  skew random walk on a 3-adic cyclic group at high frequencies. From memory (not re-read): the
  key proposition bounds |E e(xi Syrac(Z/3^n)/3^n)| by O_A(n^{-A}) uniformly over xi not divisible
  by 3, for the unconditioned Syracuse variable with i.i.d. geometric exponents. Identity S is
  the 2-adic mirror: mu_b^ is the characteristic function of -sum_k 3^{-k} 2^{e_k} mod 2^b. Two
  differences. (a) Without conditioning, the 2-adic variable is EXACTLY uniform (Terras
  bijection), so all the content of E sits in the conditioning on survival, an event of
  probability 2^{-(1-h)b}. After exponential tilting the cost is polynomial. That is a plausible
  route to E_bdd: Tao-type decay at rate b^{-A}, A > 3/2, for the tilted variable restricted to
  the survival event would suffice for fixed xi. (b) But N2/N3 show that a statement UNIFORM in
  xi (Tao's form) is false here: the sup stays near 0.05. Any such route must treat the
  frequencies +-2^v 3^a separately.
* **Fourier decay for nonlinear Cantor sets.** Sahlsten-Stevens, "Fourier transform and
  expanding maps on Cantor sets", arXiv:2009.01703 (checked: polynomial decay of the Fourier
  transform of Gibbs measures for totally non-linear uniformly expanding maps on Cantor sets).
  Bourgain-Dyatlov (Patterson-Sullivan measures of convex cocompact Fuchsian groups, GAFA 2017)
  and J. Li (stationary measures and Gibbs measures, via spectral gaps and renewal): from memory.
  These are measures on R generated by REAL expanding maps, and non-linearity is what makes
  them decay. Our mu_b is the image of a p-adic Gibbs-type measure under the digit-reversal
  embedding Z/p^b -> [0,1). The dynamics that generates Omega acts on the LOW digits (p-adically),
  while the Fourier variable sees the HIGH digits. There is no real expanding map whose
  Gibbs measure is the limit of mu_b, so the hypotheses (C^2 non-linear real IFS) are not met.
  Moreover F2 shows the expected limit of mu_b is Lebesgue itself, not a fractal measure:
  the question is decay to the uniform measure, not Fourier dimension.
* **Furstenberg x2, x3 intersections** (Shmerkin; Wu; both Annals 189 (2019), checked): for
  p, q multiplicatively independent (log p / log q irrational), closed x p-invariant A and x q-invariant
  B in [0,1], and all real u != 0 and v, dim (uA + v) ∩ B <= max(0, dim A + dim B - 1). E is
  a "2-adic set seen through the real order" statement. But Omega is not invariant under a map
  of [0,1] (its natural invariance is under the 2-adic dynamics), and the theorem bounds the
  dimension of intersections, not the counts in short intervals at a fixed depth. Not applicable
  as stated. The heuristic that "x2-structure and x3-structure are independent" is the same
  philosophy as N3's u^a frequencies.
* **Mahler's question / intrinsic approximation on Cantor sets** (Bugeaud, Math. Ann. 2008;
  Fishman-Simmons, Proc. LMS 2014: from memory). These concern rationals close to the middle-third
  Cantor set in R. The lead's reformulation ("positive integers are badly approximable
  p-adically by Omega") is the p-adic analogue, with integers in place of rationals. The known
  results use the real self-similarity of the Cantor set. Omega's p-adic self-similarity is
  broken by the slope condition, so there is nothing to transfer.
* **Linear forms in logarithms, Subspace theorem, abc**: see `../../round4/lead/README.md`.
  Nothing to add, except that F4 is the Fourier-side version of their limitation.

## 8. What stayed open, and where it stalled

* E_bdd (F2(c): mu_b^(xi) -> 0 for fixed xi): OPEN for every system. The natural attack is
  Theorem U with the outer phases kept. Write sum_{r1} e(xi r1/p^b - xi U^{-1}x'/p^L) All^(xi U^{-1}).
  The triangle inequality over r1 is what loses: it caps U at kappa_L, which numerically does not
  tend to 0 (kappa_{L,0} = 0.087, 0.074, 0.065, 0.059, 0.059 for L = 16, 18, 20, 22, 24, flattening at the observed non-decaying sup 0.054-0.056). Cancellation among the r1
  requires equidistribution of the pairs (U(r1) mod p^L, x'(r1) mod p^L) over alive nodes. That is
  the same "value after the digits are used up is Haar-random" statement as E: circular.
* The square-root hypothesis H is supported numerically for b <= 26 but unproved. It gives at
  most b = log X/(1 - h/2) even if true (F3/F4).
* I did not prove G <=> E or any transfer between siblings.
* [revised: resolved by U', R-B, whose constants are exact rationals] The FFT-based numbers in Theorem U-3x+1 use double-precision FFTs (sizes up to 2^22, sets up to
  3e5 points). The rounding error is of order 1e-9 |S|, far below the margins, but it is a
  floating-point step: the bound is not certified in exact arithmetic.

## Files

* `rb.c` (compile: `gcc -O2 -o rb rb.c`): exact R_b bitmaps, top-digit histograms, local functions g_sigma.
* `check_fourier.py`: exact checks [1]-[7]; run with the venv python; about 3 s; exits 0.
* `check_revision.py` (revision): checks [A], [C], [B1]-[B5], [E], [N3]; about 1 min (`--full`: about 4 min on 12 cores; output `check_revision_full.txt`); exits 0.
* `exactD.c` (compile: `gcc -O2 -fopenmp -o exactD exactD.c`) and `exact_u.py SYS L M [all]` (revision):
  exact constants of Theorem U'. Outputs `exact_c31_L14.txt`, `exact_c31_L14_all.txt`, `exact_c31_L15.txt`,
  `exact_c31_L16.txt`, `exact_k7_L16.txt`, `exact_s53_L16.txt`, `exact_k7_L17.txt`, `exact_s53_L17.txt`.
* `sandwich.py` -> `sandwich.txt` (revision): the trivial sandwich against U'.
* `revision_n3.py` -> `revision_n3.txt` (revision): symmetry classes and discrete logs of the maximisers; exits 1 if the revised N3 fails.
* `REFEREE1.md`, `referee1_check.py`: the referee's report and independent checks (not mine).
* `fourier_bound.py SYS L M`: Theorem U numbers. Outputs `ub_*.txt`.
* `spectrum.py`, `decay.py`, `profile.py`, `powers.py`, `l1test.py`: EVIDENCE scripts.
* `topdigits.txt`, `spectrum_b24.txt`, `decay.txt`, `decay_c31_28.txt`, `profile_b26.txt`, `powers_b24.txt`, `l1test_b26.txt`, `l1_vs_b.txt`, `ub_*.txt`: outputs.

## Revision after REFEREE1

REFEREE1 (`REFEREE1.md`) confirmed F1, F2, T, U, Z, S and the F4 inequality. It asked for fixes A to E.
All five are made below. Two further errors that the referee did not list are also corrected here
(the "10 to 50 times" in N2, and N3 for split5_3). New checks are in `check_revision.py`, which exits
0 and can fail (check [B4] has a mutation that must produce violations; [B1] and [B2] are exact
equalities). Items marked [revised] earlier in this README point here.

### R-A. The translation bound and the moduli obstruction (fix A)

The consequence I drew from F4 ("no Fourier-decay hypothesis used through absolute values can prove
M") does not follow from F4. To certify N(X, b) = 0 one needs only (1 + B_F) X P(b) < 1, and F4 gives
(1 + B_F) X P >= 1/pi + O(X P), which can be below 1. For 3x+1 at b = 16, m = 16 it is 0.33 (check [A]).
The consequence is nevertheless true. Here is the proof.

**F4' (PROVED, translation bound).** Let R be a nonempty subset of Z/p^b, 1 <= X <= p^b, I = [0, X), and
N_t = #(R ∩ (t + I)) for t in Z/p^b. Then for every t

    |N_t - X|R|/p^b|  <=  E_abs := p^{-b} sum_{xi != 0} |S^(xi)| |I^(xi)|.

For X = k p^{b-m} we have E_abs = X P(b) B_F(b, m), so B_F >= 1/(X P(b)) - 1 and (1 + B_F) X P(b) >= 1.

*Proof.* The indicator of t + I has Fourier transform e(-t xi/p^b) I^(xi), so Plancherel gives
N_t - X|R|/p^b = p^{-b} sum_{xi != 0} S^(xi) conj(I^(xi)) e(t xi/p^b). Take absolute values. For
X = k p^{b-m} the terms with v_p(xi) >= m vanish (F1), so E_abs = X P B_F. Choose t = r0 in R. Then
0 in I gives r0 in t + I, so N_t >= 1 and X P B_F >= 1 - X P. ∎

F4' is stronger than F4 whenever either bound is positive. B_F < 1 now forces X P(b) > 1/2.

**Proposition Mod (PROVED).** Let Phi be any property of finite subsets of Z/p^b that depends only on
the function xi -> |S^(xi)|. If a nonempty R satisfies Phi, then for every r0 in R and every Y the
translate R'' = R - r0 + Y also satisfies Phi, and it contains Y. So for an interval J, no theorem of
the form "every R with Phi has R ∩ J = ∅" holds unless no nonempty set satisfies Phi. The same holds for every bound of the form
N <= sum_r phi(r) = |R| phi^(0)/p^b + p^{-b} sum_{xi != 0} S^(xi) conj(phi^(xi)) estimated by
|R| phi^(0)/p^b + p^{-b} sum |S^||phi^| with a majorant phi >= 1_J (sharp or smooth). That estimate depends
only on |S^|, so it also bounds the count for a translate of R that meets J, and therefore it is >= 1.

*Proof.* The Fourier transform of R - r0 + Y is e((r0 - Y) xi/p^b) S^(xi), which has the same modulus,
and R - r0 + Y contains Y. ∎

*What this does and does not say.*
(i) A proof of slope-sense M ("no n in [n0, X) lies in R_b for b >= C log X") needs R_b ∩ [n0, X) = ∅.
So it cannot come from any hypothesis on |mu_b^| alone, H included.
(ii) For 3x+1 the actual-drop count dominates the slope count: a slope >= 1 after every step and a
nonnegative intercept give T^t(n) >= n. Also 1 is not in R_b for b >= 2. So E_0 for 3x+1, which is
stated for the actual count in R-D, implies N_slope(X, b) <= (1 + eps) X P + eps(X) -> 0, i.e.
N_slope = 0 in that range. That is out of reach of moduli-only arguments. [revised after REFEREE2: the
earlier sentence "it is false as stated for K7, whose row (x-1)/4 has a negative intercept" was wrong
and is withdrawn.] (ii) also holds for K7, with b replaced by b - 1, by REFEREE2's lemma: write
x_t = sigma_t n + c_t. The three K7 maps send c to c/2, (3c+1)/2 and (c-1)/4, and each preserves
c >= -1/3, starting from c_0 = 0. So x_t >= sigma_t n - 1/3 > n - 1 whenever sigma_t >= 1, and since x_t
is an integer, x_t >= n. Hence slope survival over the decided steps implies actual survival, and b
digits cover at least b - 1 halvings. (REFEREE2's check [I] finds no drop among all 104 K7 slope
survivors at b = 16. REFEREE2 also remarks that the positive intercepts of split5_3 make the same
extension immediate there; I have not written that case out.)
(iii) Proposition Mod is not an obstruction to Fourier methods as such. It says that the phases of
the coefficients must enter, as first claimed. Proposition Z, for instance, uses exact vanishing, and
vanishing is a statement about moduli. But it gives counts equal to |R_b|/2, never zero.
Checks [A]: the three inequalities of F4' for 3x+1, K7, split5_3, 3x-1 and 3x+5 at b = 16, for all
X = 2^{b-m} and 20 random X each, with the maximum over translates computed exactly. Also: translates
have the same moduli.

### R-B. Exact constants: Theorem U' (fix B, extended)

**Theorem U' (PROVED).** Fix a system, a depth L and the group G generated by its multiplier mod p^L
(3 for 3x+1 and K7, 5 for split5_3; every node unit U is a power of it). Let

    D'_{L,m,k} = max over stuck states sigma, allowed sets S = All(sigma, A) other than the full set,
                 u in G and c in Z/p^L of  | #{t < k p^{L-m} : u t + c mod p^L in S} / (|S| k p^{-m}) - 1 |.

Then for every b >= L, 1 <= m <= L and 1 <= k <= p^m:
|N(k p^{b-m}, b) / (k p^{b-m} P(b)) - 1| <= D'_{L,m,k}.

*Proof.* Put j = b - L. Every r < p^b is r1 + p^j t with r1 < p^j and t < p^L. Since r1 < p^j, we have
r1 + p^j t < k p^{b-m} = k p^{L-m} p^j iff t < k p^{L-m}. Lemma T gives r1 + p^j t in R_b iff
(U t + x') mod p^L in All(r1), and nothing when r1 is dead. Hence
N(X, b) = sum_{r1 alive} #{t < k p^{L-m} : U t + x' in All(r1)} and |R_b| = sum_{r1 alive} |All(r1)|.
If All(r1) is the full set, its term equals |All(r1)| k p^{-m} exactly. Otherwise U mod p^L is in G,
so by the definition of D' the term differs from |All(r1)| k p^{-m} by at most D' |All(r1)| k p^{-m}.
Summing, |N - X P(b)| <= D' k p^{-m} |R_b| = D' X P(b). ∎

This is U(ii) with the Fourier step removed. The rearrangement bound D of U bounds the same per-node
quantity for every unit, so D' <= D (also checked by the referee, R3a). It requires the list of stuck
states. For 3x+1 the only stuck state is (0, 0). For K7 and split5_3 the stuck states are (0, 0) and
(1, 1): with s >= 2 known digits every row is decided, and with one known digit the row is decided
exactly when the digit is 0. Check [B5] confirms this for all nodes of depth <= 12. Lemma T itself is
check [2] of `check_fourier.py` and R2 of the referee.

*Computation* (`exactD.c`, integers only). As u runs over G, so does u^{-1}. Also
#{t < W : u t + c in S} = #(u^{-1} S ∩ [u^{-1} c, u^{-1} c + W)), and u^{-1} c runs over Z/p^L. So D' is the
maximum over w in G of the extreme window counts of wS, taken from prefix sums. Slopes are ranked
exactly with Fractions in `exact_u.py`. Check [B1] compares `exactD` with a direct brute-force
evaluation of the definition at L = 8 (3x+1 with all odd units and with <3>, and K7). The allowed
sets come from an independently written g. The agreement is exact.

| system | L (valid for b >= L) | units | D'_{L,1} | D'_{L,2} (k = 1, 3) | D'_{L,3} (k = 1, 3, 5, 7) |
|---|---|---|---|---|---|
| 3x+1 | 10 | all odd | 19/79 = 0.2405 | 31/71 = 0.4366, 31/213 | |
| 3x+1 | 12 | <3> and all odd | 63/367 = 0.1717 | 145/433 = 0.3349, 145/1299 | 249/433 = 0.5751, 0.2671, 0.1603, 0.0822 |
| 3x+1 | 14 | <3> and all odd | **213/1627 = 0.13092** | **213/749 = 0.28438**, 71/749 = 0.0948 | **349/749 = 0.46596**, 479/2247 = 0.2132, 479/3745 = 0.1279, 349/5243 = 0.0666 |
| 3x+1 | 15 | <3> | 213/1627 | same as L = 14 | same as L = 14 |
| 3x+1 | 16 | <3> | **129/1057 = 0.12205** | same as L = 14 | same as L = 14 |
| K7 | 16 | <3> | **19/52 = 0.3654** | 12/13 = 0.9231, 4/13 = 0.3077 | |
| split5_3 | 16 | <5> | **17/25 = 0.68** | 44/25 = 1.76, 44/75 = 0.5867 | |
| K7 | 17 | <3> | **19/66 = 0.2879** | **61/79 = 0.7722**, 61/237 = 0.2574 | |
| split5_3 | 17 | <5> | 17/25 = 0.68 | 44/25 = 1.76, 44/75 = 0.5867 | |

The L = 10, 12, 14 values agree with the referee's independent computation. Compared with the
floating-point rearrangement constants of U: 3x+1 0.1221 / 0.2844 / 0.4660 against 0.1948 / 0.4330 /
0.8777 (L = 22). K7 0.2879 (L = 17) against 0.999 (L = 22). split5_3 0.68 against 3.50. So U' gives a
non-trivial uniform bound for K7 and for split5_3 at m = 1, where U gave nothing. For 3x+1 the maximum at L = 14 is
attained on small high-threshold allowed sets (|S| = 1627 for m = 1, |S| = 2247 for m = 2, 3). I did not
investigate why D'_{L,2} and D'_{L,3} do not change between L = 14 and 16.

**Siblings.** For 3x+d the map x -> d x conjugates the slope dynamics: T_d(d x) = d T_1(x), and
multiplication by d preserves parity. So the allowed sets of 3x+d are d times those of 3x+1, and the
relevant units lie in d^{-1}<3>, which is contained in the odd units. The all-odd-unit constants at
L = 14 are the same fractions, so U' holds with the L = 14 constants for 3x-1 and 3x+5 (slope sense).
Check [B3] confirms this against exact counts for b = 14..21. The bound says nothing about cycles,
as it should. The actual-drop counts of 3x-1 and 3x+5 include their cycle minima, and U' is not a
statement about those.

*Checks.* [B2] recomputes the L = 14 fractions exactly. [B3] compares them with the exact counts of
3x+1 at b = 22..30 (`topdigits.txt`, all k/8) and of 3x+1, 3x-1, 3x+5 at b = 14..21. The largest
observed deviation is 0.146 D'. [B4] is node-level. At b = 24 = 14 + 10 every node deviation is
<= D'_{10}, and the worst node reaches 0.474 D'_{10}. A mutation to 0.4 D' produces 23 violations,
so the check can fail. [B5] compares the stored K7 and split5_3 constants with the exact counts at
b = 22..30. With `--full` it also recomputes them and the 3x+1 L = 16 constant.

**Against the trivial sandwich** (`sandwich.py`, exact). With rho = 2^m |R_{b-m}| / |R_b|, the sandwich
is R_b ∩ [0, 2^{b-m}) ⊂ R_{b-m}, and each other block holds at most |R_{b-m}| points. It certifies
|dev| <= (2^m - 1)(rho - 1) at a single b, and it needs |R_{b-m}| and |R_b| for that b. For 3x+1 and
b = 16..30 its maximum is 0.225 / 1.17 / 2.72 for m = 1 / 2 / 3. U' gives 0.1221 / 0.2844 / 0.4660 for
every b >= 16. For m = 1 the sandwich is better at some b: it is 0 at the Proposition Z depths and
about 0.10 at b = 20, 23, 26, 29. For m = 2, 3 U' is better at every b in the range, and U' alone is
uniform in b. My original assessment "the same size" was right only for m = 1.

*Is U' beyond the horizon?* Yes, by the same argument as for U. For n < 2^{b-m} the b-digit residue
of n ends in m zero digits, so membership in R_b depends on parities of iterates past n's own digits.
U' bounds their bias by a fixed constant, uniformly in b. It does not make the error tend to 0, and
it cannot reach m of order log X. It is a weak type-(1) statement, as before. Its improvement over
U is in the constants and in exactness, not in kind.

### R-C. F3 for every X, with consistent eps (fix C)

**Theorem F3' (PROVED, conditional on H(eps)).** Suppose B_F(b, m) <= C p^m |R_b|^{-1/2+eps} for all
b >= b_0 and 1 <= m <= b. Then for b >= b_0 and every 1 <= X <= p^b,

    |N(X, b) - X P(b)| <= C (p - 1)(log_p X + 1) |R_b|^{1/2 + eps},

hence |N(X,b)/(X P(b)) - 1| <= C (p-1)(log_p X + 1) p^{b - log_p X} |R_b|^{-1/2+eps}. Since
|R_b| = p^{h b + o(b)}, this tends to 0 for b <= log_p X / (1 - (1/2 - 2 eps) h): the exponent is
at most b(1 - (1/2 - eps) h) - log_p X + o(b) <= -eps h b + o(b), and the factor log_p X + 1 <= b + 1
is absorbed.

*Proof.* Write X = sum_{i=0}^{n} d_i p^i with digits d_i < p and n = floor(log_p X). Then [0, X) is the
disjoint union of sum_i d_i <= (p - 1)(n + 1) translates of the blocks [0, p^i). For a block with
i < b, F4' (the translation identity with |I^| invariant under translation) gives
|#(R_b ∩ block) - p^i P(b)| <= p^i P(b) B_F(b, b - i) <= p^i P(b) C p^{b-i} |R_b|^{-1/2+eps} = C |R_b|^{1/2+eps}.
A block with i = b occurs only when X = p^b, and its deviation is 0. Sum over the blocks. ∎

The results-table entry now has the margin (1/2 - 2 eps), and the ranges 1.90 log_2 X (3x+1) and 1.41
log_2 X (split5_3) are the eps -> 0 limits. Check [C] tests the block-decomposition inequality on 60
random X at b = 16. H itself is not proved. It is EVIDENCE (N4).

### R-D. G and E_0 (fix D)

*Wording.* "E does not imply M" is not a provable statement about a fixed system: if the Collatz
conjecture holds, M is true and every implication into it holds vacuously. What is proved is the
following. **The derivation of "sigma(n) <= (C* + eps) log_p n for all but finitely many n" from E in
CONJECTURE.md is invalid.** E's inequality |N - X P| <= eps X P + X^{eps(X)} allows N(X, b) up to
X^{eps(X)} >= 1 even where X P(b) -> 0. It is therefore consistent with a single never-dropping or
divergent start, and in fact with up to X^{eps(X)} exceptional starts below X.

*Corrected E_0 (stated for the actual-drop count).* Let N_act(X, b) = #{1 <= n <= X : sigma(n) >= b},
with sigma the number of halvings before the orbit first goes below n (infinite if it never does), as
in CONJECTURE.md. Let Exc be the set of n >= 1 that are the minimum of a periodic orbit. **E_0:** for
every K there is eps(X) -> 0 with N_act(X, b) <= (1 + eps(X)) X P(b) + #(Exc ∩ [1, X]) + eps(X) for all
b <= K log_p X. **M':** there is C with sigma(n) <= C log_p n for all large n not in Exc.

**E_0 => M' (PROVED).** Fix eta > 0 and K = C* + eta + 1. Suppose n >= p, n is not in Exc, and
sigma(n) >= b := ceil((C* + eta) log_p n). Note b <= K log_p n. Apply E_0 with X = n. Every element of
Exc ∩ [1, n] has sigma = infinity, and n is counted as well, so N_act(n, b) - #(Exc ∩ [1, n]) >= 1. On the
other side, P(b) = p^{-(1-h) b + o(b)} <= n^{-(1-h)(C* + eta) + o(1)} = n^{-1 - eta (1-h) + o(1)},
because (1 - h) C* = 1. So (1 + eps) n P(b) + eps(n) -> 0, which is < 1 for large n. Contradiction. So
sigma(n) < (C* + eta) log_p n for all large n not in Exc. ∎ If Exc is finite (one cycle for 3x+1,
three for 3x-1, several for 3x+5), M' is M away from finitely many n.

*Why the slope-sense count would not do.* Every theorem in this README is about the slope count
N(X, b) = #(R_b ∩ [0, X)). An n can survive in the actual sense without being in R_b: the intercepts
help it. And the cycle minima of 3x+5 are not slope-sense survivors. So a slope-sense E_0 bounds the
wrong quantity, and the argument above does not go through with it. This was the referee's point, and
I agree.

### R-E. N1, N2, N3 (fix E, plus two corrections of my own)

* **N1** [revised]. max_{1<=xi<=64} |mu_b^| / |R_b|^{-1/2} for 3x+1 lies in [1.28, 3.11] for b = 16..28. It
  is 2.57, 2.14, 2.35, 3.22 at b = 12..15. The old "~1.5" was too specific. The ratio wanders, with no
  clear trend, so "square-root rate up to a factor of about 3" is what the data support (check [E]).
* **N2** [corrected; not raised by the referee]. "10 to 50 times the random baseline" was WRONG. Those
  are the ratios to |R_b|^{-1/2}. Against the random-set top-level maximum the ratio is
  2.3, 3.9, 5.7, 7.5, 13.2 for 3x+1 at b = 20, 21, 23, 24, 26 (it grows, because the random baseline
  decays and the true sup does not), 1.3 to 3.8 for K7, and 0.7 to 2.0 for split5_3 (check [E]). The
  random baseline 0.004 quoted in the table is the b = 26 value (0.021 at b = 20). The qualitative
  claim, that the 3x+1 top-level sup does not decay while a random set's does, stands.
* **N3** [revised]. Every 3x+1 survivor is 3 mod 4. More generally R_b lies in a single class mod 2^w,
  with w = 2 (3x+1), 5 (K7), 8 (split5_3), and check [N3] confirms this exactly for b = 14..22. So
  |mu_b^(xi + 2^{b-w} d)| = |mu_b^(xi)|, and a printed maximiser such as 3^{3145742} is just one
  representative of the class of 3^{14} mod 2^{22}. Since every odd residue is +-u^a for some a, the
  claim "xi = +-2^v u^a" is vacuous unless a is small. Revised claim, from `revision_n3.py` (b = 20,
  22, 24, v = 0..4, one representative per class mod 2^{b-w}):
  - 3x+1 and K7: in all 29 cases with a nonzero maximum, the top frequency of the class v_2(xi) = v is
    +-2^v u^a modulo the full period 2^{b-w}, with |a - ((b - v) log_u 2 - 1)| <= 1. The class
    v = 0 of 3x+1 at b = 22 vanishes by Proposition Z. The next four frequencies typically agree with
    such a +-2^v u^{a'} only modulo 2^{b-w-v-1} (median deficit 1). EVIDENCE.
  - split5_3: WITHDRAWN. Only 1 of the 15 top maximisers is +-2^v 5^a with small a modulo the full
    period. The others agree with such a frequency only modulo 2^{b-w-v-d} with d = 1..8. At these
    depths |R_b| <= 270, and the spectrum is within a factor 2 of the random baseline (N2), so I see no
    arithmetic structure for split5_3.
  `revision_n3.py` exits 1 if either part of this claim fails.

### What did not change

E, E_bdd and H remain OPEN. The square-root hypothesis H is EVIDENCE only. The ceiling 1/(1 - h/2) of
F3 is unchanged. Theorem U' is the only proved statement that reaches past the horizon, and it does so
by a bounded number of digits with a bounded, non-vanishing error. The literature survey (section 7)
is unchanged. The referee found no misquotation, and every item quoted from memory is still flagged
as such.

## Revision after REFEREE2

REFEREE2 confirmed every PROVED item (needs_repair = false) and asked for two text fixes and two nits.
No proof and no PROVED statement was changed.

| referee item | action |
|---|---|
| Fix 1, R-A(ii): "false as stated for K7, whose row (x-1)/4 has a negative intercept" is wrong | Withdrawn. Replaced by REFEREE2's lemma (c >= -1/3 is preserved by the three K7 maps, so a slope >= 1 gives x_t >= n). (ii) now holds for K7 with b - 1 in place of b. The split5_3 extension is recorded as REFEREE2's remark, not written out. |
| Fix 2, section 7: Shmerkin-Wu quoted without hypotheses | Now states p, q multiplicatively independent (log p / log q irrational), u != 0, A x p-invariant and B x q-invariant. |
| Nit: "not a success of type (1) in substance" (section 4) versus "a weak type-(1) statement" (R-B) | One bracketed sentence in section 4 reconciles them: formally type (1), but weak. |
| Nit: N2 "stays about 0.05" for b = 20..27 | The row now gives 0.0485 at b = 20 and exactly 0 at b = 22, 25 (Proposition Z depths), as in `decay.txt`. |

REFEREE2's remark on H (at m = b it holds automatically, so H has content only for m < b) is not an
error and needed no change.
