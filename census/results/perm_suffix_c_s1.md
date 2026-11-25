# perm_suffix_c_s1

Rule: 4q -> 2q; 4q+2 -> 4q+3; 2q+1 -> 4q+1 (n=0 mod 4 -> n/2, n=2 mod 4 -> n+1, odd n -> 2n-1)

| question | answer | status | tier |
|---|---|---|---|
| FATE (seed) | returns to seed (1 is a fixed point) | PROVED | 0 |
| GLOBAL | no | PROVED | 1 |

## Proof

FATE (tier 0): 1 = 2*0+1 -> 4*0+1 = 1.

GLOBAL (tier 1): No. For odd n, f(n) = 2n-1 is odd, and 2n-1 > n whenever n > 1. So the orbit of any odd n >= 3 (e.g. 3, 5, 9, 17, ..., 2^k+1) is strictly increasing and infinite. In fact 1 is the only start with a periodic orbit: an even n halves while n = 0 mod 4 until it reaches some m = 2 mod 4, then goes to the odd number m+1 >= 3, whose orbit is infinite.

## Check

checks/perm_suffix_c_s1.py verifies, with exact integer arithmetic, that the catalog step function agrees with the case formulas used above for all n < 200000, the monotonicity/closed-form facts on that range, and the seed orbit prefix. The proof itself is the algebra above; the check only guards against a mismatch between the catalog code and the stated rule.

## Referee

Verdict: FATE confirmed (tier 0), GLOBAL confirmed (tier 1). Code: odd n -> 2n-1 (fixes 1, strictly increases for odd n>1). The extra remark also holds: an even start halves while 0 mod 4, reaches 4q+2, then goes to 4q+3 >= 3, so 1 is the only start with a periodic orbit. Check script re-run (OK); independent test of the key lemma over n < 10^5 also passed. The argument is pure algebra on the catalog code, so it does not depend on simulation, and it uses no injectivity assumption.
