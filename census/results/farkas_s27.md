# farkas_s27

Rule: 1 -> 1; n = 1 mod 3 -> (n-1)/3; else n even -> n/2; else (n odd) -> (3n+1)/2. Seed 27.

| Question | Answer | Status | Tier |
|---|---|---|---|
| FATE | enters another cycle: the fixed point {1} (27 -> 41 -> 62 -> 31 -> 10 -> 3 -> 5 -> 8 -> 4 -> 1) | PROVED | 0 |
| GLOBAL | yes: every positive orbit reaches 1, and {1} is the only cycle | PROVED | 1 |

(This is not the published Farkas map, which has an (n+1)/2 branch. The argument below is for the rule as implemented in systems.py.)

## Proof of GLOBAL

Let n > 1. We show the orbit of n reaches a value < n, or reaches 1. Induction on n then gives that every orbit reaches 1. Since 1 is the only value that does not eventually move strictly below itself, no other cycle exists.

* n = 1 mod 3: n -> (n-1)/3 < n.
* n even, n != 1 mod 3: n -> n/2 < n.
* n odd, n != 1 mod 3. Write n + 1 = 2^a b with a >= 1 and b odd.
  1. Odd steps. If x is odd then (3x+1)/2 + 1 = 3(x+1)/2. Also (3x+1)/2 = 2 mod 3 for every x, because 3x+1 = 1 mod 3 and 2*2 = 1 mod 3. So the odd branch applies a times in a row: after the first step every value is 2 mod 3, so the n = 1 mod 3 rule never fires. The values run through 3^j 2^(a-j) b - 1, ending at 3^a b - 1, which is even and 2 mod 3.
  2. One halving gives z_a = (3^a b - 1)/2.
  3. For k >= 1, z_k = (3^k b - 1)/2 is 1 mod 3, since 3^k b - 1 = 2 mod 3. So the rule gives (z_k - 1)/3 = (3^(k-1) b - 1)/2 = z_(k-1). This repeats down to z_0 = (b-1)/2.

  So after exactly 2a+1 steps, n reaches (b-1)/2 = ((n+1)/2^a - 1)/2 < n. The orbit stops early only if it hits 1 first, which happens exactly when z_1 = (3b-1)/2 = 1, that is b = 1, and that already reaches 1. The value 0 is never produced: (b-1)/2 = 0 needs b = 1, and the orbit is already at 1 by then. The rule 1 -> 1 also blocks (1-1)/3.

Method: parity/valuation bookkeeping with an explicit closed formula for each odd block. That is elementary, so tier 1.

## Check

checks/farkas_s27.py simulates the seed with exact integers. As a sanity test it also checks the block formula for every odd n <= 10^6 and confirms that each 1 < n <= 10^6 descends. It passes.

## Referee
Verdict: FATE confirmed (tier 0), GLOBAL confirmed (tier 1).
I re-derived the block lemma. For odd x, x+1 -> 3(x+1)/2, so after j < a odd steps the value is 3^j 2^(a-j) b - 1. That value is odd, 2 mod 3 and not 1, so the odd branch keeps firing. At j = a the value is even and 2 mod 3, so it is halved. Then z_k = (3^k b - 1)/2 is 1 mod 3 (because 2^-1 = 2 mod 3) and maps to z_(k-1). The only z_k equal to 1 is z_1 with b = 1. The endpoint is (b-1)/2 <= (n-1)/4 < n. The other branches give values >= 1 and < n when n > 1, because n = 1 mod 3 with n > 1 forces n >= 4. Strong induction then gives convergence to 1 and rules out other cycles. No injectivity or open conjecture is used. checks/farkas_s27.py passes when re-run.
