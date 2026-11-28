# Referee report 1: round6/decide_wide

Referee 1. I read `README.md` and `theory.md`. For context I also read round3 `dichotomy.md`
(Lemmas 1-4, Theorem 1) and `accel/trichotomy.md` (Theorems H, N, Lemma L), and the round-4
type-(b) record (`round4/integrality/census_small.md`). I re-derived every PROVED statement
line by line. I wrote my own check, `referee1_check.py`, from scratch: its own graph, SCC,
max-mean and exact potential code, and a brute-force orbit tester. It does not import
`twlib.py`, `famscan` or the prover's checks. It imports `decide.py` only to cross-check one
k*, and `families.py` only to decode option menus. I ran the prover's checks on a scratch copy
of the folder, so none of the prover's files were rewritten.

## Checks run

| check | result |
|---|---|
| `check_theory.py` (round-4 venv) | exit 0, 90 s: Lemma S 2808 pairs, 10.6 M patterns, Theorem B 312 tables, 74 mixed tables |
| `check_harness.py` | exit 0, 117 s: 265 re-settled catalog tables, 10,734 type-(b) members, falsification tests |
| `check_famscan.py` | exit 0: 5400 members, 0 mismatches |
| `classify6.py check` | exit 0: 26,887 tables, 0 mismatches |
| `referee1_check.py` (own, `python3 -I`) | exit 0, about 25 s (`quick` argument: smaller N). Sections A-L below |

The run times are well under the README's "~5 min" and "~15 min". That is harmless.

`referee1_check.py` can fail, and it did. Its first version asserted Proposition 4 exactly as
stated, and it failed on 24,000 (table, level) pairs (see the Proposition 4 entry below). It
now asserts that the counterexample exists, and it checks the corrected statement. Section I
includes a wrong cycle list and a perturbed B2 that has to come out type (c). Both are
detected.

## Verdicts

| # | claim | verdict |
|---|---|---|
| 1 | Lemma 0 (over-approximation) | CONFIRMED |
| 2 | Theorem H' (any modulus, any multipliers, condition (D)) | CONFIRMED (nit) |
| 3 | Proposition Z | CONFIRMED |
| 4 | Proposition P (prime modulus) | CONFIRMED |
| 5 | Corollary P' | CONFIRMED |
| 6 | Lemma S, Theorem S (squarefree, level Q) | CONFIRMED_WITH_FIX (wording) |
| 7 | **Proposition 4 (modulus 4)** | **WRONG as stated; CONFIRMED_WITH_FIX once a hypothesis is added** |
| 8 | Theorem B(i), B2(u) | CONFIRMED |
| 9 | Theorem B(ii), Bp(u) | CONFIRMED (two slips in the text) |
| 10 | §4 type-(b)-by-modulus table | CONFIRMED_WITH_FIX |
| 11 | Theorem C6 | CONFIRMED |
| 12 | "div23 with 5n ± 1" (and the 5n+5 variant) | CONFIRMED |
| 13 | Q = 12 mixed type-(b) system, mixed examples, novelty remark | CONFIRMED |
| 14 | catalog sweep (244/256, 15/42, 0/226 open) | CONFIRMED_WITH_FIX (2 maps mislabelled) |
| 15 | 38 open census table maps all OBST and type (c) | CONFIRMED |
| 16 | coverage: 29 of 38 by class theorems, plus 3 at the base level | CONFIRMED |
| 17 | family scans (counts, CERT, type-(b) members) | CONFIRMED |
| 18 | `typeb_list.jsonl` (10,734 settled members) | CONFIRMED |
| 19 | 14 non-Markov mixedbase systems re-settled, open mixedbase ones not | CONFIRMED |
| 20 | exponents labelled EVIDENCE | CONFIRMED (label honest; not recomputed) |
| 21 | README headline on whole classes | CONFIRMED_WITH_FIX (overclaim for squarefree) |
| 22 | no open question settled; 3x+1 etc. not settled | CONFIRMED |

Because of item 7, **needs_repair = true**. Every application of Proposition 4 in the round
(split family with odd v, split5_1, split5_3, desc_split7_1, par_*) satisfies the missing
hypothesis, so no census conclusion changes. The statement, its proof, and two table rows do
need repair.

## Details

### 1. Lemma 0. CONFIRMED
T(r + Kt) = y0 + (uK/w)t needs w | uK, which follows from w | uQ and Q | K. The image lies in
y0 + gZ mod K. If w = 1 then g = K. Correct.

### 2. Theorem H'. CONFIRMED
*Type (b) part.* The residue of x mod K fixes the branch, because Q | K. So T^{jL}(m) = f^j(m)
also holds for non-Markov maps. The step v_p(f^j(m) − x*) ≥ min(0, v_p(x*)) holds because
f^j(m) is an integer. The valuation then drops by jδ, which forces m = x*. This needs only that
p is prime and that (D) holds. No unit hypothesis and no subgroup condition is used.

*Type (a) part.* This is round 3's argument. It uses x > 0 only to bound c(s)u x / w by
θ c(r) x. On N0 the case x = 0 is also fine.

*(H1)/(H2) imply (D).* This is right: v_p(U) = 0 for p | Q, and W > 1 is a product of divisors
of Q.

*Nit.* §0 leaves a single-cycle SCC with U = W > 1 without a type. It can occur only off
(H1)/(H2). The harness labels it 'b', and `padic_kill` then returns None, so Theorem H'
returns NONE. The code is safe. The text should say that (b) means U ≥ W and that (D)
excludes U = W, or classify U = W separately.

### 3. Proposition Z. CONFIRMED
The case A = 1, B < 0 contradicts (P), as stated.

### 4. Proposition P. CONFIRMED
Under (H1), a node with w = p has k = u and g = gcd(u, p) = 1, so it has all p successors,
itself included. That forces C = (r). Every other node then has w = 1 and avoids r, which gives
a division-free cycle on Z/p minus {r} (nonempty, since p ≥ 2). Own check: all successor
patterns for p = 2, 3, 5 (7776 at p = 5) and 20,000 random patterns each for p = 7 and 11.

Remark: the hypothesis "no division-free cycle" really is needed. At p = 2, with 0 → 3n/2 and
1 → n + 2, the SCC {0} is a type-(b) SCC next to a (z).

### 5. Corollary P'. CONFIRMED
It relies on round 3's Lemma L. Its proof in `trichotomy.md` is a two-line sketch, and it was
refereed there. I re-derived the "going up" step for an arbitrary expanding cycle C' at level
K. Its projection lies in a (c) SCC Σ of G_p. Take the periodic points of C'_proj^d W, with W
using an edge of Σ outside C'_proj. For large d they agree with x*(C') mod p^K, so they give a
second closed walk through C' at level K. So "no type (b) at any level" holds, not only "type
(c) at every level". Own check: 3x+1, m3_g, desc_m3_4n5 and perm_1932 are (c) with no (b) at
every level p^k ≤ 256.

### 6. Lemma S and Theorem S. CONFIRMED_WITH_FIX (wording)
Lemma S: CRT gives the unique successor divisible by q. S(s*(r)) = S(r) because
s* ≡ r q^{-1} (mod p) for p ≠ q. Injectivity holds as written. Own check: every squarefree
Q < 400 with at least two primes, under all rules q(S) when there are at most 7 support sets,
otherwise first, last and 20 random rules.

Theorem S at the pattern level: every single-cycle SCC of G_Q consists either of units only
or of non-units only (the s* cycle, which contracts). Checked exhaustively for Q = 6 and 10,
and on random patterns for Q = 14, 15, 21, 30, 35 and 42.

*Fix.* "In particular G_Q has no type-(b) SCC" holds only for SCCs that contain a division. A
unit self-loop such as 1 → 7n (Q = 6) is a single expanding cycle, which is (b) by the §0
definition and also (z). Say "no type-(b) SCC containing a division node", or "(z) takes
precedence".

### 7. Proposition 4. WRONG as stated; CONFIRMED_WITH_FIX
The statement has no "no division-free cycle" hypothesis. The proof dismisses even v with
"(if v is even there is a division-free cycle through the odd classes)" and then still
concludes "no type (b)". Counterexample (raw table mod 4, (H1), (H2), (P)):

    even n -> n/2;  n = 1 (mod 4) -> 3n + 2;  n = 3 (mod 4) -> 3n + 1.

Here 1 → 1 is a division-free loop. 3 → 2 and 2 → {1, 3}, but 1 never returns to 2. So {2, 3}
is an SCC consisting of the single cycle 2 → 3 → 2, with multiplier 3/2: a type-(b) SCC. The
step "both 1 and 3 return to 2" fails. The same thing happens with 1 → n, 1 → n + 4, and so on.
My check finds 1080 such (table, level) pairs at levels 4, 8 and 16. The prover's own
`check_theory.py` part 2 actually tests the corrected statement ("unless a division-free cycle
exists"), so the check is right and the theorem text is not.

**Fix.** Add the hypothesis "G_4 has no division-free cycle" (for example v1 and v3 odd), or
change the conclusion to "every type-(b) SCC coexists with a type-(z) SCC". With the
hypothesis, the proof as written is correct, and the "every level" extension via Lemma L also
holds. Own check: all 16 successor patterns, u ∈ {1, 3, 5, 7, 9, 27}, levels 4, 8 and 16. The
README sentence "Theorem H gives nothing for every raw table mod 4" is still true, because a
(z) SCC also blocks Theorem H'. But the README row "raw tables mod 4 … no type (b) at any
level" and the §4 row "4: no, at any level" must carry the same caveat. Nothing in the census
is affected: every split-family member used has odd v.

### 8. Theorem B(i). CONFIRMED
I re-derived G_8, the SCCs {0}, {3, 6} and {1, 2, 5}, x* = 3, and the return map
G(n) = (n+1)/2 or (n+5)/2. Own check for u ∈ {3, 5, 7, 9, 11, 13, 15, 21, 33, 63}:
- the types at levels 8, 16, 32 and 64 are exactly (a)/(b), and the (b) SCC is {3, 6} with
  U/W = u/2;
- brute force over every n ≤ 300,000 (u ≤ 7) or n ≤ 60,000 finds exactly the cycles (1 2),
  (3 6) and (5 10).

### 9. Theorem B(ii). CONFIRMED (two slips)
I re-derived the graph, the computation of F(q) (both cases b ≤ 1 and b ≥ 2), F(q) < q, x* = 1,
and positivity. Own check for p ∈ {3, 5, 7, 11}, nine values of u each: types (a)/(b) only at
p^2 and p^3 (and 81); the (b) SCC is {1, p} with multiplier u/p; brute force over n ≤ 60,000
finds exactly (1 p) and (2 2p).

*Slips.*
1. "only 0 and p lead to 1" should read "only p leads to 1; only 0 and 1 lead to p". My script
   asserts the predecessor sets. The conclusion is unaffected.
2. "Read at modulus p^m (m ≥ 3, or m ≥ 4 for p = 2)" is confusing. Bp already lives at p^2.
   Say "at every p^m with m ≥ 2 (odd p) or m ≥ 3 (p = 2)".

### 10. §4 table. CONFIRMED_WITH_FIX
1. Row Q = 4: add the division-free caveat (item 7).
2. The §2 scope remark and §4 say that with general branches type (b) occurs at
   "Q = 4, 6, 10, 15 (examples verified in `check_theory.py`)". `check_theory.py` part 4
   contains only Q = 6 and Q = 10 (I re-typed both with my own code: types ab, cycles (1 4)
   and (5), (10 15)). Q = 4 is true (my counterexample above). For Q = 15 there is no example
   anywhere in the folder, and a 400,000-member random search of mine found none. Supply an
   example or drop 15.
3. Prior art: type (b) at prime powers was already known in the repository. Round 3 had
   acc_h9, acc_h16 and acc_h32, and round 4 (`integrality/census_small.md`) had 36 type-(b)
   tables in F3m2, settled by Theorem H. What is new in Theorem B is an explicit infinite
   family with a *positive* expanding cycle for every u > p. The text should cite the earlier
   examples.

### 11. Theorem C6. CONFIRMED
I re-derived G_6 and checked that it depends only on (s1, s5). Own check: I enumerated the
simple cycles of all 36 graphs and evaluated exactly, for every u1, u5 < 60 prime to 6, whether
all of them contract. That agrees with every row of `out/classify6.md`. Both corollaries hold:
a certificate needs u ∈ {1, 5}, and (5, 5) is certifiable iff (s1, s5) = (0, 0). On 3000
random actual maps, my own SCC classification agrees with the table. The theorem rests on
round 3 Theorem 1, whose scope is mixed Q with (H1), (H2) and (P), and that is satisfied here.

### 12. "div23 with 5n ± 1". CONFIRMED
Own exact potential (type (a) at level 6). Brute force over n ≤ 2·10^6 finds the single cycle
(1 6 3), and decide.py gives k* = 4. The 5n+5 variant has the cycles (1 6 3) and (5 30 15).

### 13. Mixed type (b). CONFIRMED
For the Q = 12 example: types ab; the (b) SCC is {1, 2} with multiplier 11/2 and
x*(2) = −2/3; brute force over n ≤ 300,000 finds exactly (5 7 10). All 72 examples in
`typeb_mixed_examples.txt` (Q = 12, 20, 24, 28, 36) are Markov, have (a)/(b) types only and
satisfy (D) in my code.

The novelty remark ("first mixed-modulus system settled by an isolated expanding cycle, as far
as the files show") is consistent with what I found. The round-3/4 type-(b) systems are at 9,
16 and 32, and the catalog has no mixed (b).

### 14. Catalog sweep. CONFIRMED_WITH_FIX
From `catalog_rows.json` I reproduced 244 of 256 "yes" re-settled, 15 of 42 "no", and 0 of the
226 OPEN or OPEN-CLS rows. For a random sample of 40 of the 250 Theorem-H' GLOBAL records, the
listed cycle lists equal brute force (n ≤ 20,000), and my own types at the stated level contain
no (c).

*Fix.* "188 open round-folder maps are type (c)": two of them, zcore_3_7 (= zcore_K7) and
zcore_3_17, are N0 maps that were read on the positive integers. The harness reports
"positivity fails" and never classifies them. I checked that they satisfy (P) on N0 and are
type (c) at levels 4 and 16, so the conclusion holds. The harness output and the README count
should be fixed by re-running them with `zero=True`.

### 15. The 38 open census table maps. CONFIRMED
My code finds an exact type-(c) witness at the base level for all 224 analysable open records
(the remaining 2 are the zcore maps above). I wrote my own tables for split5_1, split5_3,
desc_split7_1, desc_m3_4n5, m3_b, m3_d, m3_g, div23_5n1, div23_7n1, div235_7n1, perm_1932 and
desc_s32_plus9. Each equals the extracted catalog table on n < 20,000. All twelve are (c),
with no (b), at every level tried: up to 576 for div23_*, 540 for div235_7n1, and 256 or 81
for the prime powers.

### 16. Coverage. CONFIRMED
My recount of the 38 OPEN-CLS tables: 26 by Proposition P (Q = 2 or 3, Markov, no
division-free cycle), 3 by Proposition 4 (raw, odd v), and 3 by Theorem S (base level only).
The 6 not covered are desc_s32_plus9, par_6_2, par_10_2, perm_1932inv, perm_c and perm_d. That
matches "29 + div23_5n1, div23_7n1, div235_7n1".

### 17. Family scans. CONFIRMED
- Every SUMMARY adds up, with FALLBACK = 0.
- The exhaustive totals equal the product sizes of `families.py`.
- Every CERT member has a known cycle count. Total CERT = 1,185,073, which matches "about
  1.19 M".
- `famscan.c` reviewed:
  - (z) is detected before anything else;
  - (b) and (c) are decided by exact big-integer U vs W;
  - (a) is decided by an integer potential checked in 128-bit arithmetic;
  - the exceptional set F = {V(Tn) ≥ V(n)} covers every cycle (at the V-minimum of a cycle,
    V(Tn) ≥ V(n));
  - the bound n ≤ c(s)v/(c(r)w − c(s)u) is right, and overflow is guarded.
- Own sample: 690 listed CERT/B members from all 18 files, classified by my own code. The CERT
  ones are all (a), and the famscan cycle count equals brute force (n ≤ 20,000). The B ones
  are (a)/(b) only.
- For the exhaustive files, 100 random *unlisted* members per family are (c) or divergent (z)
  in my code, as famscan claims.

### 18. `typeb_list.jsonl`. CONFIRMED
It has 10,734 lines, and the per-Q counts match the family table: 8621 at Q = 9 is
6272 + 2349, and so on. For a sample of 150, my own types are (a)/(b), the cycle lists equal
brute force over n ≤ 20,000, and x* agrees exactly. The prover's `check_harness.py` B checks
all of them.

### 19-22.
19. The non-Markov mixedbase re-settlements are covered by `check_harness.py` A and by my
    catalog sample.
20. The exponents are floats and are labelled EVIDENCE, which is honest.
21. **README lines 15-17** say Theorem H "is now proved to give nothing … for every raw
    full-division table with squarefree modulus". Theorem S is a level-Q statement. The same
    paragraph and "Honest limits" say so, but this sentence does not. Add "at level Q".
22. My code finds 3x+1, 3x−1, 5x+1 and 3x+5 type (c) at every level 2 to 512. No argument in the
    folder settles any type-(c) system, and none is claimed. Every newly settled system (B2,
    Bp, the Q = 12 system, the scan members, 5n ± 1) is (a)/(b) in my code, and none of the
    arguments would apply to 3x+1.

## Summary of required changes

1. Proposition 4: add "no division-free cycle" (or "(b) only next to (z)"), and correct the
   README row and the §4 row Q = 4 accordingly. (Substantive.)
2. README lines 15-17: "squarefree modulus" becomes "squarefree modulus, at level Q".
3. §2 and §4: give an example for Q = 15, or remove it; say which examples verify Q = 4.
4. zcore_3_7 and zcore_3_17: re-run on N0 and fix the "188 type (c)" count.
5. Nits: the U = W single-cycle case in §0; Theorem S "no type (b)" wording; Theorem B(ii)
   predecessor sentence and the m-range; cite the earlier type-(b) examples at 9, 16 and 32
   (round 3 acc_h*, round 4 F3m2).
