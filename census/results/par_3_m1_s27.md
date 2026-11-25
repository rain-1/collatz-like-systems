# par_3_m1_s27
Rule: even n -> n/2; odd n -> 3n-1. Seed 27.

| question | answer | status | tier |
|---|---|---|---|
| FATE | other-cycle (5,14,7,20,10) | PROVED | 0 |
| GLOBAL | unknown (conjecturally yes) | OPEN | 5 |

## FATE
27 -> 80 -> 40 -> 20 -> 10 -> 5 -> 14 -> 7 -> 20: enters the 5-cycle {20,10,5,14,7},
not containing 27.

## GLOBAL
n -> -n conjugates this map to 3x+1 on the negative integers. GLOBAL is therefore the
statement "no 3x+1 trajectory of a negative integer diverges", part of the 3x+1
conjecture on Z (Lagarias: cycles -1, -5, -17 only). Open; the same obstacles as
the positive Collatz problem apply (no known descent certificate, no finite-state
invariant). Known cycles on positives: {1,2}, {5,14,7,20,10}, {17,50,25,74,37,110,55,
164,82,41,122,61,182,91,272,136,68,34}.

Check: census/checks/par_3_m1_s27.py

## Referee
FATE: confirmed (tier 0). GLOBAL: open-agreed (tier 5).
An independent simulation gives a tail of 3 and the cycle {20,10,5,14,7}.
I verified the conjugacy -F(-n) = C(n) on negative n directly, with an assert over [-10^5, -1]. So GLOBAL is equivalent to "no 3x+1 trajectory of a negative integer diverges", which is open.
