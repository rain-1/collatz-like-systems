# par_7_1_s1
Rule: even n -> n/2; odd n -> 7n+1. Seed 1.

## FATE: returns — PROVED (tier 0)
1 -> 8 -> 4 -> 2 -> 1. Period 4, preperiod 0. Check: census/checks/par_7_1_s1.py (exits 0).

## GLOBAL: unknown — OPEN (tier 5)
Every 7n+1 orbit eventually periodic? Open, and heuristically false (expected log-growth per odd
step log 7 - 2 log 2 > 0; the orbit of 3, see par_7_1_s3, appears to diverge). No divergent orbit
is proved for any map of this type, so "no" is unproven too. Descent arguments fail (average
multiplier > 1); a mod-7 invariant exists (odd steps land in 1 mod 7, halving multiplies by
4 mod 7) but it only constrains residues, not boundedness.

## Referee
FATE: confirmed (tier 0). 1->8->4->2->1. GLOBAL: open-agreed (tier 5). This is the 7n+1 eventual-periodicity problem. The mod-7 invariant constrains residues only.
