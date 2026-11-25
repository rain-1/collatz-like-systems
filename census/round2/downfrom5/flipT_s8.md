# flipT_s8

**Rule.** P(n) = T(n)+1 if T(n) is odd and T(n)-1 if T(n) is even. Branch by branch: 3q -> 2q-1, 3q+1 -> 4q+2, 3q+2 -> 4q+4. |P - T| = 1 everywhere, and P is a permutation of Z_{>0}.

**Question (FATE).** What is the fate of the seed 8?

| answer | status | tier |
|---|---|---|
| equivalent to Collatz's 1932 orbit-of-8 problem | OPEN | 5 |

## Exact reduction (tier 1)

P(n) = T(n+3) - 3. Branch by branch:
- n = 3q: T(3q+3) - 3 = 2q - 1.
- n = 3q+1: T(3(q+1)+1) - 3 = 4q + 2.
- n = 3q+2: T(3(q+1)+2) - 3 = 4q + 4.

The set {1,2,3} is T-invariant (T: 1 -> 1, 2 -> 3, 3 -> 2), so Z_{>=4} is T-invariant. Hence n -> n+3 conjugates P on Z_{>0} to T on Z_{>=4}. Since T(8) = 11, P^k(8) = T^k(11) - 3. The P-orbit of 8 returns to 8 iff 11 is T-periodic, iff 8 is T-periodic (T is a bijection and T(8) = 11). That is exactly Collatz's 1932 question.

## Context: the constant family

Consider F(c0,c1,c2): n -> (2n+c0)/3, (4n+c1)/3, (4n+c2)/3 according to n mod 3. These are the maps with T's slopes and T's branch reading, and only the additive constants changed.

**Proposition.** The members of F that are bijections of Z_{>0} are exactly T (0,-1,1), perm_swap S (0,5,-5), flipT (-3,2,4) = T(n+3)-3, and (-3,8,-2) = S(n+3)-3.

*Proof.* The images are tails of the classes 2Z + c0/3, 4Z + (4+c1)/3 and 4Z + (8+c2)/3. A bijection needs the three classes to partition Z, and each tail to start at the least positive element of its class. If the 2-class is the evens, the start 2 + c0/3 must equal 2, so c0 = 0, and the two 4-classes are {1,3} in either order. If the 2-class is the odds, the start must be 1, so c0 = -3, and the 4-classes are {2,4} in either order. That gives four maps. By round 1, S is T acting on (1/5)Z.

So every bijective member is T itself, acting on a translate or rescaling of a lattice. In this family, bijectivity means "the 1932 problem". `check_flipT_s8.py` also confirms the list by brute force for |c_i| <= 32.

**Role.** This is the nearest unprovable neighbour of T at sup-distance 1. Compare swT3_9_15_s8, which is also at sup-distance 1 and is tier 1.

Check: `check_flipT_s8.py` (exit 0).

## Referee

**Verdict: OPEN, tier 5 (agreed), by an exact tier-1 reduction to Collatz's 1932 problem.**

I checked P(n) = T(n+3) - 3 branch by branch and numerically for n < 10^5. T permutes {1,2,3}, so Z≥4 is T-invariant, and P^k(8) = T^k(11) - 3. Since T(8) = 11, 8 is P-periodic iff it is T-periodic.

The bijective-members proposition has a valid general proof. Bijectivity requires the three image tails to tile Z>0 and to start at the least positive element of each class, which forces c0 = 0 or c0 = -3. The brute-force range |c| ≤ 32 is only a cross-check.
