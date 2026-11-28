# Referee report: round 3, lens "mixedbase"

Referee: independent adversarial verification. I changed none of the prover's files. My files are `referee_check.py` and this report.

## What I ran

* **The prover's checks.** All five exit 0: check_pairing_family.py (6 s), check_single_class.py (21 s), check_sparse.py (20 s), check_relatives.py (6 s), check_systems.py (<1 s).
* **`referee_check.py`.** Exits 0 and runs in about 13 s. It is written from scratch and imports nothing from mixedlib, pairlib, the check scripts or systems.py. Every map is re-typed from the rule text in the .md files.
  * **A.** My own mixed-radix descent engine and my own Lemma A' for all 16 certified systems. It checks that the leaves partition N0, re-tests each leaf identity on random 100-bit t, computes the exceptional set E and the complete cycle list. My leaf counts and maximum depths match the prover's exactly (for example mb_t729: 5417 leaves, depth 83; mb_d23_8: 93 leaves, depth 24). Every cycle list for a named system matches.
  * **B.** My own Lyndon-word enumeration of the expanding cycles of n ↦ (an+1)/2 | n/2 (my counts are larger, because I keep all cycles). Then my own exact hitting-set search, with superset reduction and a disjoint-packing bound. Every claimed minimum (2, 3, 4, 7 for 3^3..3^6; 2, 4 for 5^2, 5^3; 2, 5 for 7^2, 7^3) is confirmed as a lower bound, and every claimed R hits every cycle.
  * **C.** The S3 and S5 case analyses, re-run for every odd m ≤ 151 and every r, each with an explicit witness:
    * uncaught fixed points and cycles, checked exactly with rational residues;
    * Lemma-R runs, simulated on actual CRT-built integers for 29 steps, checking that they are never caught and that the identity T^i(n) − x* = (a/2)^i (n − x*) holds;
    * the D'' word U^{m−1}Q for m = 3, 9, 27, 81, with its fixed point verified exactly and multiplier > 1;
    * the cycles (−1 −2) and (−14/17 −7/17 −9/17).

    For S7 with m ≤ 199, my own enumeration of 7x+1 cycles leaves exactly (7, 4).
  * **D.** The pairing family:
    * the block lemma P1 on 74 058 instances, including 300-bit n, a ∈ {3, 5, 7, 9, 11, 15, 21}, K ≤ 4 and seven values of x*;
    * the P3 descent inequality on real orbits;
    * the cycle lists of the named systems;
    * the P5 obstruction cycles, checked exactly for a ≤ 39, K ≤ 6 (and a = 3, K ≤ 8), including that they are caught when K = 1 or (3, K ≤ 2).
  * **E.** Theorems D and M, with the repaired bound arguments below. The survivor lists are recomputed, and every survivor is certified with its true cycle list.
  * **F.** 200 random 400-bit starts for four systems (EVIDENCE only).

I re-derived every hand proof line by line: P1, P2, P3, P4, P5, the S3 sufficiency for m = 3 and 9, the S5 necessity case split including the Hull–Dobell single-cycle step and the Lemma D'' cylinder computation, and Lemmas A', B', C', R and D''. Notes on these are below.

## Verdicts

| claim | verdict |
|---|---|
| Pairing P1–P3 (block lemma, GLOBAL for K=1 and (3,2)) | CONFIRMED |
| Pairing P4–P5 (no plain / accelerated certificate) | CONFIRMED |
| S3 (single class, 3x+1) | CONFIRMED_WITH_FIX (wording) |
| S5 (single class, 5x+1) | CONFIRMED (the generalised "mechanism" sentence is overclaimed; see below) |
| S7 (m ≤ 199) — PARTIAL | CONFIRMED as PARTIAL |
| Minimal multi-class taming sets | CONFIRMED |
| Theorem D (div23_5n1 + one class) | **WRONG** in the sufficiency sub-claim, and a GAP in the necessity bound (repaired here) |
| Theorem M (m3_b + ≤ 2 classes) | **WRONG** in the q = 2 sub-claim, and a GAP in the necessity bound (repaired here) |
| Lemmas A', B', C', R, D'' | CONFIRMED |
| 16 certified systems (mb_s3_3, s3_9, s5_5, s7_7, t27, t81, t243, t729, f25, f125, s49, s343, d23_8, d23_4, d23_30, m3b_8) | CONFIRMED (my engine reproduces each certificate and cycle list) |
| mb_pair_3_9p, mb_pair_7_7m, mb_pair_5_5m | CONFIRMED |
| mb_pair_3_9m | CONFIRMED_WITH_FIX (wording: "no certificate of any kind") |
| OPEN entries (mb_s3_27, mb_pair_3_27m, mb_pair_5_25p) | correctly labelled OPEN / EVIDENCE; their obstructions are confirmed by P5 and S3 step 3 |

## Problems found

### 1. Theorem D, sufficiency: WRONG

relatives.md says: "Every pair in the list except 'first' (2,0) and (4,2) is certified. ... GLOBAL then holds with the single cycle (1 6 3)."

The certificates are right, but the cycle claim is false for 6 of the 16 pairs. These are the complete cycle lists from Lemma A' with my engine, each verified by hand:

| priority, (q, r) | true cycle list |
|---|---|
| first (2,1) | (1) |
| first (3,1) | (1), (5 26 13). Here 1 → (1+2)/3 = 1, and 5 → 26 → 13 → (13+2)/3 = 5. |
| first (5,1) | (1) |
| first (6,2) | (1 6 3), (5 26). Here 26 ≡ 2 (mod 6), so 26 → 30/6 = 5. |
| first (10,6) | (1 6). Here 6 → (6+4)/10 = 1. |
| last (2,1) | (1) |

The three named systems are unaffected: mb_d23_8, mb_d23_4 and mb_d23_30 all have only (1 6 3).

**Repair.** Replace the sentence with the table above, or with "GLOBAL holds; the cycle lists are as computed by check_relatives.py". check_relatives.py should then print and assert the cycle list of every survivor, not only "CERT".

### 2. Theorem D, necessity bound: GAP (repaired)

The bound argument "q divides the numerator of y − z for y on (−1 −4 −2) and z on the −42/13 cycle, hence q ≤ 45" is invalid when 13 | q. Then −42/13 is not in Z_13, and Lemma B' cannot use that cycle. The scan to q ≤ 3000 skips such cycles, which is sound for q ≤ 3000 but says nothing about q > 3000 with 13 | q.

**Repair, verified in referee_check E.** Use the integer expanding cycle (−84 −42 −21 −7 −34 −17), which has multiplier 25/24, instead of −42/13. Both cycles consist of integers, so they lie in every Z_q. Catching both with one class forces q | y − z ≠ 0, so q ≤ 83 for every q and either priority. My scan of q ≤ 83, using the refined criterion of item 3, returns exactly the claimed list.

### 3. Theorem M, necessity bound: GAP (repaired)

The step "the classes must catch (1/7, −1/7), so q | 6 or 8" is invalid when 7 | q, for the same reason as item 2.

**Repair, verified in referee_check E.**

1. *Refined Lemma B'.* Write q = q₁q₂, where q₂ collects the primes of q that divide the cycle's denominator. If no point of the cycle is ≡ ±1 (mod q₁), then integers n ≡ z (mod (3q₁)^N), with any residue mod q₂, follow the cycle uncaught for N steps. The argument of Lemma B' then goes through.
2. From the 1/7-cycle we get q = 7^e·q₁ with q₁ | 6 or q₁ | 8, so the primes of q lie in {2, 3, 7}.
3. The expanding cycle (7/25, 1/25, −7/25, −1/25) has denominator prime to 42, so q divides a numerator of z ∓ 1, which is at most 32.
4. My scan of q ≤ 32 returns exactly {3, 4, 6, 8}, as claimed.

### 4. Theorem M, one class q = 2: WRONG

The claim reads: "they are the odd numbers (q=2) or ... All of these are certified, with every orbit reaching 1."

m3_b with odd n → (n+1)/2 is certified (4 leaves), but it has the second cycle (2 3). Here 2 ≡ 2 (mod 3), so 2 → (8+1)/3 = 3, and 3 is odd, so 3 → (3+1)/2 = 2.

**Repair.** State its cycle list as (1), (2 3). The cases q = 3, 4, 6, 8 really do have only the cycle (1), and so does mb_m3b_8.

### 5. Wording overclaims (CONFIRMED_WITH_FIX, no mathematical error)

* **mb_pair_3_9m.** The JSON says "no certificate of any kind exists". P4 excludes only plain certificates. For (a, K) = (3, 2), the run-accelerated certificate exists: it is the P3 proof, and the prover's own pairlib check certifies it. It should read "no plain descent certificate exists".
* **single_class.md, after S3.** "The single classes that make 3x+1 provably GLOBAL are exactly ..." should be "the single classes known here to make 3x+1 provably GLOBAL". Other values of c, or non-descent arguments, are not excluded.
* **The "mechanism" sentence.** The JSON summary says the visit-every-residue mechanism is "proved never to be enough for a single class". That is proved only for a = 5 (all m, S5) and for a = 7 with m ≤ 199 (by enumeration). The general three-point "criterion" in single_class.md is a heuristic discussion, not a proof.
* **Linear residue-weighted potentials** (README, item 3; JSON "proved impossible for every open system"). The argument is plausible: chain V along an expanding cycle for many periods, with c(·) > 0 and bounded. But it is only sketched in one sentence and has no proof file or check. Label it as a sketch, or write it out with the positivity hypothesis on c.

### 6. Novelty and difficulty (honesty check)

* **mb_pair_5_5m** is the reflection n ↦ −n of the round-2 system farkas5m_s27 (= P(5,1,1)), restricted to n ≤ 0. Its proof is round 2's block argument verbatim. **mb_pair_7_7m** and the K = 1 family are the same routine argument. These are correct but only nominally new.
* mb_s3_3, mb_s3_9, mb_s5_5 and mb_s7_7 are one-line descents (tier 1). The prover labels them tier 1, which is honest.
* The genuinely substantive content is:
  * the K = 2 closed form for a = 3 (mb_pair_3_9m and mb_pair_3_9p), a system with no plain certificate;
  * the sharp obstructions P4 and P5;
  * the S3 and S5 classifications;
  * the multi-class tamings with proved minimality;
  * the necessity lists of Theorems D and M (after the repairs).
* The novelty statements ("novelty not checked"; K = 1, a = 3 is Farkas 2005) are honest. The K = 1 extension to general a is a routine generalisation of Farkas's and round 2's argument, and it should be described that way.

## Notes on the re-derivations (no action needed)

* **P1.** Uncaught: x_i ≡ x* (mod a) and r ≡ x*/2 (mod a), and these differ since gcd(a, x*) = 1. This is also valid for composite a. Caught: on the down-run z_k ≡ x*/2 (mod m) for k ≥ K. The step count j + 1 + q is correct.
* **P3.** The constants check out:
  * K = 1: (3|x*| + |n|)/4;
  * (3, 2) with ℓ = 0: (5|x*| + |n|)/8;
  * (3, 2) with ℓ = 1: (5|x*| + 3|n|)/4.

  The catch-branch bound uses |c| < (m−1)|n|. All are correct.
* **P5.** y − x*/2 = −a x*/(2(4−a)) and 2y − x*/2 = x*(4−3a)/(2(4−a)), with gcd(4−a, a) = gcd(4−3a, a) = 1. Near y and near 5x*, the accelerated map S is affine with slopes a/4 and 9/8 respectively, so Lemma B' applies to S.
* **S5, case m = 3^k.**
  * φ(z) = (5z+1)/2 satisfies 5/2 ≡ 1 (mod 3) and 1/2 ≢ 0 (mod 3), so it is a single 3^k-cycle.
  * The cylinder of U^{m−1}Q is B₂(x*, 2^{−(m−1)}) × (φ(r) + 3^k Z₃). The word map expands it onto Z₂ × Z₃, so Lemma D'' applies.
  * Verified exactly for k ≤ 4.
* **S5, case 3^k·5.** The cycle (−14/17, −7/17, −9/17) has multiplier 25/8 and no point ≡ −2 (mod 15). Verified.
* **Lemma B' / cycle lemma.** Rotating to a point with every prefix multiplier > 1 is the standard cycle lemma, and it extends to all j by periodicity. Correct.

## Repair instructions (summary)

1. **relatives.md, Theorem D(2).** Replace "GLOBAL then holds with the single cycle (1 6 3)" with the per-pair cycle lists: first (2,1), (5,1) → (1); first (3,1) → (1), (5 26 13); first (6,2) → (1 6 3), (5 26); first (10,6) → (1 6); last (2,1) → (1); all other certified pairs → (1 6 3). Make check_relatives.py print and assert these lists.
2. **relatives.md, Theorem D(1), bound.** Replace the −42/13 cycle in the bound with the integer cycle (−84 −42 −21 −7 −34 −17), giving q ≤ 83, or otherwise handle 13 | q. Make check_relatives.py assert the bound using the integer cycle.
3. **relatives.md, Theorem M, bound.** Add the refined Lemma B' (only the part of q prime to the cycle's denominator must match) and the second cycle (7/25, 1/25, −7/25, −1/25), giving q ≤ 32 when 7 | q. Make the check include this.
4. **relatives.md and the JSON, Theorem M, q = 2.** State the cycles (1) and (2 3) for m3_b + (odd → (n+1)/2). Do not say "every orbit reaches 1".
5. **Wording.**
   * mb_pair_3_9m: "no plain descent certificate". The accelerated one exists.
   * S3 "exactly": qualify it as "known here".
   * The "mechanism" claim: proved for a = 5, and for a = 7 with m ≤ 199 only.
   * Linear potentials: mark as a sketch, or write the proof out.
   * Note that mb_pair_5_5m is the reflection of farkas5m_s27.
