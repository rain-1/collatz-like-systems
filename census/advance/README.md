# Cohort round (25–26 November 2026)

Seven prover/referee cohorts each targeted one exact theorem about an open entry in
`census/open_collatz_systems.txt`. In each cohort a prover wrote a proof and an
exact check. An independent referee re-derived the proof and wrote its own
check. If the referee found a gap, the prover got one repair round and a second
referee checked the repair. No open question was settled. Every result is a
strictly weaker, exact statement.

| Folder | Entry | Result | Review |
|---|---|---|---|
| `permd-1cycles` | CLS-046 | The cycles of perm_d with one local minimum are exactly {2,5,3}, {6,15,9}, {26,65,41} | confirmed; made unconditional by `laurent_addendum.py` (k < 7431, scan to 24924) |
| `split5_1-runs` | CLS-048 | Every start below 2^42 reaches a known cycle; any new cycle has more than 23 expanding runs and at least 6,432,164 steps; never-dropping starts number O(X^0.9383) | gap, repaired, confirmed |
| `split7_1-runs` | CLS-053 | Every start below 2^50 reaches (1 8 4 2); any other cycle has at least 70 expanding runs; never-dropping starts number O(X^0.7549) | confirmed |
| `9n1-cycles` | CLS-037 | 9n+1 has no circuit; every cycle has at least 14 rising runs | confirmed |
| `permswap-1cycles` | CLS-047 | Exactly five cycles with at most one block of multiples of 3 | confirmed |
| `swT9-connect` | CLS-055 | The residue graph is strongly connected at every modulus, so no congruence trap exists | confirmed |
| `constants-audit` | several | Earlier cycle results now rest only on Laurent 2008 Corollary 2, read in the primary source; two scans were extended, and no conclusion changed | confirmed |

**Transcendence input.** M. Laurent, *Linear forms in two logarithms and
interpolation determinants II*, Acta Arith. 133 (2008), 325–348, Corollary 2
with Table 1. Two agents read it in the IMPAN PDF. The older LMN 1995, Ellison
and Rhin constants are no longer used anywhere.

**Reproducing.** Run `python3 check.py` in each folder; the two `split*` folders
compile their `range.cpp` helper. `referee_*` files are the referees' independent
checks. `../advance_results.json` holds every prover claim and referee report.
