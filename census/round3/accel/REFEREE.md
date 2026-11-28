# Referee report: round 3, lens "accel"

Referee files: `referee_check.py` (about 8 s, exits 0) and `referee_cycles_rest.py` (about 5 s,
exits 0). Both were written from scratch. They import nothing from `accel_lib.py`, `check_*.py` or
`descent_lib.py`. They import `systems.py` only to compare its step functions with the referee's
own implementations of the written rules ([DEF]).

The prover's checks were re-run:

| check | result | time |
|---|---|---|
| `check_trichotomy.py` | exit 0 | 12 s |
| `check_sfamily.py` | exit 0 | 35 s |
| `check_dressing.py` | exit 0 | 6 s |

## What the referee check does independently

* **[DEF] Map definitions.** Own implementations of acc_h32, acc_h16, acc_h9, the four dress_*
  maps and all 12 S-family maps were compared with `systems.py` on 1..10^5 and on 2000 random
  200-bit inputs. They agree. The .md rules, `systems.py` and the check scripts all define the
  same maps. The acc_h9 table was also checked by hand against "9q+r → …".
* **[H] Theorem H, re-implemented.**
  * The affine branches are derived from the step function itself, and affinity is checked on
    each class.
  * G_K is built, and the SCCs come from Kosaraju (the prover used Tarjan).
  * The contraction weights come from an *exact multiplicative Bellman–Ford in Fractions*: θ = 1 −
    2^−k, relaxing c(s) ← min(c(s), θ c(r)/q). This is a different construction from the prover's
    float potentials plus `limit_denominator`. The referee's certificates are θ = 15/16 for
    acc_h32/acc_h16 (n ≤ 432 and n ≤ 136) and θ = 3/4 for acc_h9 (n ≤ 9).
  * Type-(b) periodic points are checked to follow their cycle under the p-adic extension.
  * The run was repeated at the higher levels K = 7, 6, 4. The SCC types are unchanged (isolated
    cycle at −1), which illustrates level independence.
  * The cycle lists come out as {1,3,19}, {1,3} and {1,4,7}, as claimed.
* **[EV] Evidence only.** Every n ≤ 3·10^5, and 300 random inputs of 64 to 256 bits, reach the
  claimed cycles.
* **[N] Theorem N witnesses, rebuilt.** This was done for 3x+1, 5x+1, perm_1932, split5_3, sf3_137,
  sf3_7, sf3_13, and sf3_137 at level 6.
  * W is a BFS walk through an edge that is not in C.
  * Each y_d (d ≤ 12, and d ≤ 30 for sf3_13 with λ_C = 9/8) is verified to be a *genuine*
    periodic point of the p-adic extension: its rational orbit is computed and follows C^d W.
  * Also checked: the multiplier is λ_C^d λ_W, y_d ≡ x* mod p^{K+d v_C}, y_d is not on O(x*), the
    y_d are distinct, and they are expanding from some d₀ on.
* **[S] S-family, m = 2..5, all subsets.** No SCC of G_m is an expanding simple cycle. As a side
  check, the number of subsets with an expanding cycle already at level m is 2, 10 and 172 for
  m = 2, 3, 4. This equals the round-2 OBST counts.
* **[Z] Theorem Z and Corollary C.** Checked on random z of up to 300 bits.
* **[CYC] Cycles of period ≤ 26, all 12 systems, re-enumerated.** The referee uses a pruned DFS
  over closed walks with exact integer composition (3^a x + B)/2^b. The lists agree with the
  prover's table for every system.
* **[K] Theorem K.**
  * The run identity and the first-return identity are checked for 5 prime pairs and 3 maps g.
  * The cycles (1 2 3), (1 2), (1 6 9 3) and (1 6 3) are confirmed.
  * The first return of the catalog map div23_5n1 on 6-rough numbers equals ρ(5w+1).

## Line-by-line review and verdicts

### Theorem H: CONFIRMED_WITH_FIX
The proof is correct. The type-(b) case uses uniqueness of the point that follows a cycle with a
division, which is (M) with a unit multiplier. The type-(a) case uses the potential
V(Tn) ≤ θV(n) + β, which is valid because c(s)·q ≤ θ c(r) and **n > 0**.

**Fix (made explicit here).** The inequality c(s)·u n/w ≤ θ c(r) n needs n ≥ 0, so Theorem H
needs the hypothesis *T maps positive integers to positive integers*. Otherwise "every positive
orbit" is not controlled once the orbit leaves Z_{>0}. All maps in the folder satisfy this. The
statement should include the hypothesis.

Two small points need no change:
* The existence of rational weights in a contracting SCC follows by slack and perturbation.
* A contracting simple cycle needs no weights, because its unique p-adic point is x*.

### Theorem N: CONFIRMED
The steps are correct:
* W contains an edge outside C, so y_d ∉ O(x*).
* y_d → x* p-adically, so infinitely many distinct expanding periodic orbits exist and one avoids
  the finite E.
* Lemma B (round2/descent/lemmas.md, lines 55–61: the cycle lemma gives a point whose partial
  multipliers are all > 1) applies.
* The affine progression around y inside the open cylinder D_i contradicts descent.

The statement "includes accelerated certificates with symbolic run exponent" is an
interpretation. It is correct for certificates that exclude finitely many periodic orbits and use
locally constant (p-adic) stopping times. The prover says that is all it covers. Certificates
that use archimedean information (the size of n) are not excluded, and the prover says so.

### Theorem T (trichotomy, level independence): CONFIRMED
* (1) is the round-2 referee proposition.
* (2) "⇐" is correct: a point not in E eventually stays in a contracting SCC, and the slope
  bound (max c / min c)·θ^s gives descent on a cylinder.
* Level independence of type (c), going up: y_d ≡ x* mod p^{K'} puts y_d's cycle in the SCC of
  x*'s node.
* Going down is terse but correct.
* Type (b) also persists upward. Any K'-cycle in x*'s SCC projects to a power of C, and by (M)
  its point is x*. This is not written out, but the referee's level-K' runs confirm it on the
  examples.

### S-family barrier (m ≤ 5): CONFIRMED_WITH_FIX
The exhaustive computation is correct and was reproduced. The written inference "every OBST
member has an expanding cycle, so it is in a type-(c) SCC" skips one step.

**Fix.** An expanding periodic point found at any level K' projects to a closed walk in G_m with
multiplier > 1. That walk decomposes into simple cycles, and one of them is expanding. Its SCC is
neither contracting nor (by the scan) a simple cycle, so it is type (c).

For m ≤ 4 the referee also confirmed directly that all OBST members (2, 10 and 172) have an
expanding cycle at level m. The m = 5 count of 48880 is taken from round 2 (family_scan.out).

### Catalog barrier witnesses: CONFIRMED
* Rebuilt independently for 3x+1, 5x+1, perm_1932 and split5_3, with genuine-periodicity checks.
* The prover's exact check covers split5_1, m3_e, desc_m3_4n5 and desc_split7_1. Their tables
  were compared with the catalog rules (desc_m3_4n5: 3|n → n/3, 4n+5, 2n+2; m3_e: 7n+2, 7n+1;
  perm_1932: 2q, 4q+1, 4q+3).
* The "scan found no open type-(b) catalog system" is a computation in scratch, and it is
  labelled as such.

### Theorem Z: CONFIRMED (one-line identity; correctly presented as such)

### Corollary C: CONFIRMED
* The cases are checked by hand: z odd gives 3z+2 = 2T(z)+1; z even gives z+1 = 2T(z)+1.
* T_S^2 maps odd numbers to odd numbers.
* The cycle correspondence is z = 0 ↔ (1 2) and {1,2} ↔ (3 10 5 6).

### Theorem K (dressing): CONFIRMED_WITH_FIX
Parts (1), (2) and (3) are correct:
* (1) and (2): the run identity, and the same first return ρ(g(w)).
* (3): there is no descent certificate. For any fixed j, the class 0 mod M contains infinitely
  many n ≡ 0 mod p^{max(j,s)} M′ with D^j(n) = (q^e/p)^j n > n.

**Fix (wording).** The sentence "Hence the unit-multiplier hypothesis of Theorem N is necessary"
(README, dressing.md) overstates what dressing shows. Theorem N's *conclusion* is "no generalized
certificate". The dressed maps do not refute that conclusion: an analogous cover of Z_p × Z_q
would have to exclude all points with p-component 0, which is not a finite union of periodic
orbits, so D has no generalized certificate either. What dressing does show:
1. Graph-level free re-entry without (M) does not produce the realized walks C^d W, so the
   *mechanism* in the proof of N needs unit multipliers.
2. "No (generalized) certificate" does not imply "hard": D is settled while certificate-free, and
   certifiability is not invariant under first-return equivalence.

Suggested replacement: "the Markov property (M), and hence unit multipliers, is needed for the
type-(c) ⇒ infinitely many expanding periodic orbits mechanism; and absence of certificates does
not imply openness." The mathematics is unaffected.

### Exact short-cycle lists (12 S-family systems): CONFIRMED
The referee independently re-enumerated all 12 (period ≤ 26), and the lists agree with the table
in sfamily_obst.md. The method is complete: every integer cycle of period L gives a closed walk of
length L in G_m, and that walk has a unique periodic point.

### Systems

| id | verdict | notes |
|---|---|---|
| acc_h32 | CONFIRMED | The Theorem H certificate was re-derived independently (θ = 15/16, n ≤ 432), also at level 7. OBST confirmed (−1 ↦ −2 ↦ −1, multiplier 3/2). New (not in census/systems.py or round 2). Tier 2–3 is fair. The system is engineered, as stated. |
| acc_h16 | CONFIRMED | θ = 15/16, n ≤ 136, also at level 6. OBST confirmed. |
| acc_h9 | CONFIRMED | θ = 3/4, n ≤ 9. Easy, as labelled. By hand, {1,4,7,2,3,5} map into {1,4,7} at level 2, while 6 and 8 are reachable only from 0, 6 and 8. |
| dress_23_x1 | CONFIRMED | The complete proof is R(w) = ρ(w+1) ≤ (w+1)/2 < w for w > 1. It is tier 1, labelled easy, and honest. |
| dress_32_x1 | CONFIRMED | Same argument. Cycle (1 2). |
| dress_23_3x1 | CONFIRMED (equivalence; GLOBAL OPEN) | The first return is Syracuse on 6-rough numbers, and every odd orbit enters that set. |
| dress_23_5x1 | CONFIRMED (equivalence; GLOBAL OPEN) | U is literally the catalog div23_5n1, so this is a redressing of a catalog system, as stated. |
| sf2_3 / sf3_37 | CONFIRMED (equivalence; OPEN) | |
| sf2_13 / sf3_1357 | CONFIRMED (literally 3x+1) | |
| 8 new cores | status OPEN is honest | Partial results confirmed: Theorem N witnesses, cycles of period ≤ 26, z-forms (K7 and W checked by hand). The W drift and the 10^60 orbit are correctly labelled EVIDENCE. |

## Overclaim and novelty review

* Nothing labelled PROVED rests on simulation. Simulations are labelled evidence or consistency.
* The easy systems (acc_h9, dress_*_x1) are labelled easy. acc_h32 and acc_h16 really do need the
  machine-verified potential, and are honestly described as constructed by computer search.
* Novelty is "not checked" throughout, which is honest. The ingredients are standard (Markov
  partitions, max-mean cycles); the prover says so.
* The only overstatements are the two wording fixes above (the positivity hypothesis in H, and the
  "necessary" sentence for K), plus the missing projection step in the S-family barrier. None
  affects a result.

**Overall:** there is no GAP and no WRONG. needs_repair = false. The three CONFIRMED_WITH_FIX
items are small and are spelled out above.
