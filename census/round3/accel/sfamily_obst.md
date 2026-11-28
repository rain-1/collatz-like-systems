# The 12 OBST members of the S-family (m = 2, 3): complete classification

Check: `check_sfamily.py` (exits 0, about 45 s). The barrier data are in `check_trichotomy.py`.

`T_S(n) = n/2` for even n; for odd n, `3n+1` if `n mod 2^m ∈ S`, else `n+1`. Round 2
(round2/descent/family_scan.out) proved that exactly 2 subsets at m = 2 and 10 at m = 3 have no
descent certificate (OBST).

## Theorem Z (the half-shift conjugacy). PROVED

For odd n write `n = 2z + 1` (z ≥ 0). Let `g_S(n)` be the next odd value of the T_S-orbit of n. Then

    (g_S(2z+1) − 1)/2 = G_S(z),   where   G_S(z) = (odd(3z+2) − 1)/2  if (2z+1) mod 2^m ∈ S,
                                           G_S(z) = (odd(z+1)  − 1)/2  otherwise,

and odd(x) is the odd part of x.

*Proof.* For n = 2z+1 we have 3n+1 = 2(3z+2) and n+1 = 2(z+1). Halving until the result is odd
gives `odd(3z+2)` and `odd(z+1)` respectively. ∎

The branch of `G_S` depends on z mod 2^{m−1}. So `G_S` is a "z-core" with these four branches:

| z mod 4 (n mod 8) | n ∈ S | n ∉ S |
|---|---|---|
| 0 (n ≡ 1) | `3z/4` | `z/2` |
| 1 (n ≡ 3) | `(3z+1)/2` | `(z−1)/4` |
| 2 (n ≡ 5) | `(odd(3s+2)−1)/2`, z = 4s+2 | `z/2` |
| 3 (n ≡ 7) | `(3z+1)/2` | `(odd(z+1)−1)/2` |

**Corollary C (two members are 3x+1 in disguise). PROVED** Let `S_C = {n ≡ 3 (mod 4)}`. That is
S = {3} for m = 2 and S = {3, 7} for m = 3. Then G_S = T, the 3x+1 map `T(z) = z/2` or
`(3z+1)/2`. More precisely, `T_S^2(2z+1) = 2T(z) + 1` for every z ≥ 0:
* if n ≡ 3 (mod 4), then (3n+1)/2 is odd;
* if n ≡ 1 (mod 4), then (n+1)/2 is odd.

So the odd numbers carry an exact copy of 3x+1. Even numbers halve to odd numbers. Hence:

* GLOBAL(T_{S_C}) ⇔ every 3x+1 orbit on z ≥ 0 is eventually periodic.
* The cycles correspond: z = 0 ↔ (1 2), and z ∈ (1 2) ↔ (3 10 5 6). "Only these two cycles" ⇔ the
  3x+1 conjecture.

Here n = 1 corresponds to z = 0 and n ∈ {3, 5} to z ∈ {1, 2}.

So the 12 OBST systems split as follows:

* **2 are literally 3x+1**: S = {1,3} mod 4, and S = {1,3,5,7} mod 8.
* **2 are 3x+1 via Corollary C**: S = {3} mod 4, and S = {3,7} mod 8. These are Collatz-equivalent
  (OPEN, tier 5).
* **8 are new Collatz-type cores**: perturbations of 3x+1 in the z-coordinate. Let
  D = S Δ S_C be the set of classes mod 8 where T_S differs from the S_C system. Then G_S differs
  from T exactly on the z-classes of D.

| system | S mod 8 | D = S Δ {3,7} | expanding obstruction | status | drift/odd step (EVIDENCE) | cycles of period ≤ 26 (PROVED, exact) |
|---|---|---|---|---|---|---|
| sf2_3 | {3,7} (m=2: {3}) | ∅ | −1, 3/2 | ≡ 3x+1 (Cor. C) | −0.140 | (1 2), (3 10 5 6) |
| sf2_13 | all (m=2) | {1,5} | −1, 3/2 | = 3x+1 | −0.281 | (1 4 2) |
| sf3_1357 | all | {1,5} | −1, 3/2 | = 3x+1 | −0.281 | (1 4 2) |
| sf3_37 | {3,7} | ∅ | −1, 3/2 | ≡ 3x+1 (Cor. C) | −0.140 | (1 2), (3 10 5 6) |
| sf3_7 | {7} | {3} | −1, 3/2 | new core K7, OPEN | −0.556 | (1 2) |
| sf3_17 | {1,7} | {1,3} | −1, 3/2 | new core, OPEN | −0.491 | (1 4 2) |
| sf3_57 | {5,7} | {3,5} | −1, 3/2 | new core, OPEN | −0.838 | (1 2) |
| sf3_157 | {1,5,7} | {1,3,5} | −1, 3/2 | new core, OPEN | −0.658 | (1 4 2) |
| sf3_357 | {3,5,7} | {5} | −1, 3/2 | new core, OPEN | −0.652 | (1 2) |
| sf3_137 | {1,3,7} | {1} | −1, 3/2 | new core W, OPEN (divergence expected) | **+0.046** | (1 4 2), (3 10 5 6), (7 22 … 14), (39 118 … 78) |
| sf3_13 | {1,3} | {1,7} | −5, 9/8 (period 5) | new core, OPEN | −0.826 | (1 4 2), (3 10 5 6) |
| sf3_135 | {1,3,5} | {1,5,7} | −5, 9/8 (period 5) | new core, OPEN | −0.919 | (1 4 2) |

Cycle lists of the form (1 2) mean the cycle 1 → 2 → 1 (n+1 branch). The long cycles of
sf3_137 are (7 22 11 34 17 52 26 13 14) and the 15-cycle through 39 (39 118 59 178 89 268 134 67
202 101 102 51 154 77 78). The exact enumeration covers every closed walk of length ≤ 26 in G_m
(`accel_lib.integer_cycles_upto`). Extending it to period ≤ 30 (`scratch`, about 75 s) gives the
same lists.

## What is proved about the 8 new cores

For each of the 8:

1. **Exact reformulation** (Theorem Z). Each one is the z-map in the table above. The two
   simplest are:
   * **K7** (S = {7}): `z even → z/2; z ≡ 3 (4) → (3z+1)/2; z ≡ 1 (4) → (z−1)/4`. This is 3x+1
     with the class 1 mod 4 short-circuited. In closed form along the expanding run,
     `2^j u − 1 ↦ (3^{j−1} u − 1)/2` (j ≥ 2), with gain ≈ 3^{j−1}/2^{j+1}. Only runs with j ≥ 5
     expand.
   * **W** (S = {1,3,7}): `z odd → (3z+1)/2; z ≡ 2 (4) → z/2; z ≡ 0 (4) → 3z/4`. Its odd-to-odd
     form is `o ↦ 3^{⌊(v−1)/2⌋} (3o+1)/2^v` with `v = v_2(3o+1)`. This is the Syracuse map in
     which, after the first halving, each further *pair* of halvings is replaced by a factor 3/4.
2. **No descent certificate** (round 2, Lemma B). **No generalized/accelerated certificate**
   (Theorem N): each has an expanding cycle in a type-(c) SCC. The exact witnesses y_d, d ≤ 24,
   are in `check_trichotomy.py`. The barrier is therefore not an artefact of plain descent:
   classes with a symbolic run exponent plus bounded lookahead cannot work either.
3. **All cycles of period ≤ 26 are known exactly** (table above). This is PROVED by exhaustive
   closed-walk enumeration.
4. **EVIDENCE.** Every n ≤ 10^5 reaches one of the listed cycles, except for sf3_137, where 1628 of
   the n ≤ 10^5 pass 10^60. The Monte-Carlo drift per odd step is negative for 7 of the cores and
   positive (+0.046) for W.

**Core problem W (new, sharply stated).** Is there a divergent W-orbit? Equivalently, a divergent
T_{{1,3,7}}-orbit. The first candidate is z = 7 (n = 15), whose orbit passes 10^60. The positive
drift (stationary Markov computation on odd classes mod 8:
`0.2·log(3/4) + 0.3·log(3/2) + 0.2·log(1/2) + 0.3·log(3/2) ≈ +0.047`) says GLOBAL should be
**false**. As with 5x+1, no orbit is provably divergent. The four cycles above are all the cycles
of period ≤ 26.

**Status.** All 8 are OPEN (tier 5). What blocks a proof is the free re-entry of Theorem N: from
every class of the big SCC, an orbit can return to the shadow of −1 (or −5) at any depth with
bounded loss. That is the 3x+1 obstruction. I found no conjugacy from any of the 8 to 3x+1 or to
each other. A conjugacy of the Corollary-C type would need G_S = T on all classes, which happens
only for D = ∅.

**Literature.** Corollary C is an elementary conjugacy of the kind used for 3x+1 variants in the
survey literature. I have not checked whether this particular S-family form appears in print, so
novelty is not checked. Cores K7 and W: novelty not checked.
