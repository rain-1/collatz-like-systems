# perm_suffix_d_s1

Rule: 2q -> 8q; 4q+1 -> 2q+1; 8q+3 -> 4q+2; 8q+7 -> 8q+4 (even n -> 4n, ...)

| question | answer | status | tier |
|---|---|---|---|
| FATE (seed) | returns to seed (1 is a fixed point) | PROVED | 0 |
| GLOBAL | no | PROVED | 1 |

## Proof

Note: the step on n = 2q is 8q = 4n.

FATE (tier 0): 1 = 4*0+1 -> 2*0+1 = 1.

GLOBAL (tier 1): No. For even n, f(n) = 4n is even and > n, so every even start (e.g. 2 -> 8 -> 32 -> ...) has a strictly increasing, infinite orbit.

## Check

checks/perm_suffix_d_s1.py verifies, with exact integer arithmetic, that the catalog step function agrees with the case formulas used above for all n < 200000, the monotonicity/closed-form facts on that range, and the seed orbit prefix. The proof itself is the algebra above; the check only guards against a mismatch between the catalog code and the stated rule.

## Referee

Verdict: FATE confirmed (tier 0), GLOBAL confirmed (tier 1). Code: 1 -> (1+1)/2 = 1; even n -> 4n, strictly increasing and even. Check script re-run (OK); independent test of the key lemma over n < 10^5 also passed. The argument is pure algebra on the catalog code, so it does not depend on simulation, and it uses no injectivity assumption.
