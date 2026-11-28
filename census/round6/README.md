# Round 6 (28 November 2026): applying the techniques widely

Each technique built in rounds 3 to 5 (and in the split5_3 work in
`../round2/rewriting/split5_3_s27.md`) had been used on one or two maps. Round 6 applied five of
them to every census system they fit and to broad families of new maps. Five lenses, each
refereed twice. `../round6_results.json` holds every claim and verdict. Agent-written and
agent-refereed; no human review; novelty mostly not checked.

**No open census question was settled.** The round's value is coverage, general theorems, and
two negative results that close off routes.

## Results by technique

| Folder | Technique | How widely applied | What it settled | Main new theorems |
|---|---|---|---|---|
| `decide_wide` | decision procedure, type (a)/(b)/(c), exponents | all 540 distinct table maps in the census catalogs; 18 new families, about 54 million tables (p = 2, 3, 5 and mixed moduli 6 to 36) | re-settles 244 of 256 known "yes" tables and 15 of 42 known "no" tables automatically; about 1.19 million certifiable tables with cycle counts (deepest certificate 2120 steps at modulus 27); 10,734 systems with an isolated expanding cycle, each with full cycle list; all 227 open table maps are type (c) | Theorem H' (isolated-cycle method for any modulus and multipliers); the isolated-cycle type cannot occur for prime-modulus Markov tables or for mod-4 tables without division-free cycles, which covers 29 of the 38 open census table maps; explicit infinite families B2(u), Bp(u) with an expanding positive cycle and complete cycle lists; complete classification of the div23 family mod 6 |
| `typeb_wide` | isolated expanding cycles (Theorem H) | S-family to m = 8 (exhaustive to m = 6, solver beyond), 5n+1 and 7n+1 analogues, base-3 families, split-type families, neighbours of open maps | a fully mechanical proof object for every system of this type; every par_* map has such neighbours at modulus 8 | where the type is impossible; an S-family member at m = 6 with exponent gap zero, type (c), status unknown (so "gap zero implies provable" is OPEN, and the claim was withdrawn) ; the blocked mixed-base system behaves like type (c) |
| `countlaw_wide` | count law beyond the digit horizon | general theorem for unit-multiplier maps whose multipliers generate a large enough group; constants for 23 systems; certified counts for 3; every-octave constants for 19 | nothing | one general theorem G1 (density-one octaves, depth log_p X + c log_p log_p X, c = h/2); for 3x+1 the constant improves to 0.47498; exact list of census maps where the hypotheses fail (mixed primes, non-unit multipliers, trivial multiplier group) |
| `chain_wide` | one-orbit occupation bound and chain theorem | 23 contracting systems, 3 expanding, 709 family members (343 with certified negative drift) | nothing | general occupation bound (visits below X at most X^{theta*}), multiplier bound with explicit constants, general chain theorem and window criterion: an escaping orbit forces at least A(B) survivors in every B octaves, with A(B) computed per system |
| `cutoff_wide` | shift-and-subtract cutoff with the S-unit theorem | general Theorem W for two-prime unit maps; 13 census systems and families plus controls | nothing | Theorem P: in every type-(c) system (in block-word normal form) and in the blocked mixed-base system there are exponentially many non-descending cylinder words, so no such system has only rigid survivors; expanding cycles satisfy all hypotheses of the cutoff theorem, so only its ineffective threshold separates them |
| `blocked27` (outside the loop, not refereed) | normal form of the blocked mixed-base system | one system | nothing | it is a split-type map with slope 9/8 on w = n + 5 = 0 mod 8 |

## The two negative results that matter

1. **The isolated-cycle method cannot reach the open entries.** It is now proved that this type
   does not occur at any level for prime-modulus Markov tables and for the mod-4 tables, which
   is where most open census maps live. Round 3 had only observed this by a scan.
2. **Designing a walled-off map whose survivors are all rigid is impossible at the level of
   residue classes.** Free re-entry always gives two different loops of the same length at a
   common node, hence exponentially many non-descending words (Theorem P). A proof that a
   particular integer cannot follow them still has to work beyond the start's own digits. This
   answers the "new maps designed to be rigid" idea in the negative.

## What the general theorems now say about a hypothetical escaping orbit

For any unit-multiplier map with negative drift (`chain_wide`): such an orbit visits at most
X^{theta*} values below X, its multipliers track its heights within an explicit constant, and its
successive multiplier minima never drop and are spaced so that every B octaves contain at least
A(B) of them. So escape is excluded as soon as some window count of survivors is below A(B)
infinitely often. The count law predicts this at depth factor C* = 1/(1 - theta*): 19.98 for
3x+d, 3.98 for K7, 2.38 for split5_3, and about 1.38 for the blocked mixed-base system (that
last value is a measurement from `blocked27`, not a refereed constant). What is proved
reaches depth factor 1 plus a multiple of log log X, for almost every octave.

## Reproducing

Each folder has check scripts and `referee1_check.py`, `referee2_check.py`; all exit 0. Some
need numpy: use `../round4/wpotential/.venv/bin/python`. `countlaw_wide/check_all.py` takes
about 12 minutes.
