# perm_suffix_a_s1

Rule: 2q -> 4q; 4q+1 -> 4q+2; 4q+3 -> 2q+1 (even n -> 2n, n=1 mod 4 -> n+1, n=3 mod 4 -> (n-1)/2)

| question | answer | status | tier |
|---|---|---|---|
| FATE (seed) | infinite (1 -> 2 -> 4 -> 8 -> ..., orbit = {1} u {2^k : k>=1}) | PROVED | 1 |
| GLOBAL | no | PROVED | 1 |

## Proof

Note: the step on n = 2q is 2n = 4q; the step on 4q+1 is n+1.

FATE (tier 1): f(1) = 2 (1 = 4*0+1). For even n, f(n) = 2n is even and > n. So by induction the orbit is 1, 2, 4, 8, ..., 2^k, ...: strictly increasing after the first step, hence all terms distinct and the orbit is infinite.

GLOBAL (tier 1): No. The orbit of 1 (or of any even number) is infinite by the same argument; every even start has an infinite, strictly increasing orbit.

## Check

checks/perm_suffix_a_s1.py verifies, with exact integer arithmetic, that the catalog step function agrees with the case formulas used above for all n < 200000, the monotonicity/closed-form facts on that range, and the seed orbit prefix. The proof itself is the algebra above; the check only guards against a mismatch between the catalog code and the stated rule.

## Referee

Verdict: FATE confirmed (tier 1), GLOBAL confirmed (tier 1). Code row r=0,2 is n -> 2n on all even n, so 1 -> 2 -> 4 -> ... strictly increasing. Check script re-run (OK); independent test of the key lemma over n < 10^5 also passed. The argument is pure algebra on the catalog code, so it does not depend on simulation, and it uses no injectivity assumption.
