# Single taming classes for 3x+1, 5x+1 and 7x+1: complete classification

**Family.** Let m ≥ 3 be odd, r a residue mod m, c ≡ −r (mod m), and a ∈ {3, 5, 7}:

    T_{m,r,c}(n) = (n + c)/m      if n ≡ r (mod m)        (checked first)
                 = n/2            if n is even
                 = (a n + 1)/2    otherwise.

The odd branch has the 2-adic expanding fixed point x* = 1/(2 − a): −1 for a = 3, −1/3 for a = 5, and −1/5 for a = 7. The task asked when a single residue class (density 1/m) can tame the expansion. Below, "certificate" means a descent certificate of any modulus (lemmas.md). By Lemma C' this is the same as "the mixed-radix engine terminates", and by Lemma A' it implies GLOBAL.

## Theorem S3 (3x+1; PROVED)

A certificate for T_{m,r,c} (a = 3) exists only if (m, r) ∈ {(3, 2), (9, 8)}, whatever c is. For c = 1 both cases are certified, and GLOBAL holds with the single cycle (1 2).

The two settled systems are:

* **mb_s3_3**: n ≡ 2 (mod 3) → (n+1)/3; else even n → n/2; else (3n+1)/2.
* **mb_s3_9**: n ≡ 8 (mod 9) → (n+1)/9; else even n → n/2; else (3n+1)/2. The taming class has density 1/9.

*Proof of necessity.*

1. **r ≢ −1 (mod m).** Then −1 is odd, uncaught and T̂-fixed, since (3·(−1) + 1)/2 = −1, with multiplier 3/2. Lemma B' applies.
2. **r ≡ −1 and 3 ∤ m.** Take n ≡ −1 (mod 2^N) and n ≡ 0 (mod m). Then T^i(n) = −1 + (3/2)^i(n + 1) for i < N, because the values are odd and T^i(n) + 1 ≡ (3/2)^i (mod m) is a unit, so never ≡ 0. Lemma R applies.
3. **r ≡ −1, 3 | m, m ∉ {3, 9}.** The cycle (−5 −7 −10), with multiplier 9/8, is uncaught. Being caught would need m | 4, m | 6 or m | 9. Lemma B' applies.

*Proof of sufficiency (tier 1, by hand).*

* For m = 9: odd n ≢ 8 has x₁ = (3n+1)/2 and x₁ + 1 = 3(n+1)/2.
  * If 3 | n + 1, then x₁ is caught and T²(n) = (n+1)/6.
  * Otherwise x₁ ≡ 2 (mod 3), and either x₁ is even, giving T²(n) = (3n+1)/4, or x₂ + 1 = 9(n+1)/4 is caught, giving T³(n) = (n+1)/4.
* For m = 3: the analogous argument gives (n+1)/2.

The engine certificate (12 leaves, depth 3) confirms this. ∎

**So 1/9 is the sparsest single class that tames 3x+1 by a certificate.** Together with pairing_family.md, the single classes known here to make 3x+1 provably GLOBAL are the following. (This is not a classification of all provable single classes: S3 excludes descent certificates for every other (m, r), but other values of c or non-descent arguments are not excluded.)

* ±(n+1)-type classes, which are certifiable: (3, 2) and (9, 8);
* the Farkas pairing classes, which are not certifiable but are settled by a closed form: (3, 1) with c = −1, and (9, 4) with c = −4, on N0.

The density-1/27 analogues of both types carry explicit obstructions and are OPEN: (27, 26) is blocked by the cycle (−5 −7 −10), and (27, 13) by P5 of the pairing family.

## Theorem S5 (5x+1; PROVED)

A certificate for T_{m,r,c} (a = 5) exists only if (m, r) = (5, 3). For c = 2 it is certified, and GLOBAL holds with the single cycle (1 3). This system, **mb_s5_5**, is tier 1: an odd n ≢ 3 gives (5n+1)/2 ≡ 3 (mod 5), which is caught, and then (n+1)/2.

*Proof of necessity.* Write m = 3^k 5^l m'' with gcd(m'', 15) = 1, and x* = −1/3.

* **3 ∤ m.**
  * If 3r + 1 ≢ 0 (mod m), the fixed point x* (multiplier 5/2) is uncaught.
  * If 3r + 1 ≡ 0 and m'' > 1: start the run from n ≡ x* (mod 2^N) and n ≡ 0 (mod m). Then T^i(n) − x* = (5/2)^i(n − x*) is a unit mod m'', so it is never caught (Lemma R).
  * If m = 5^l: the cycle (−1 −2), with multiplier 5/4, must be caught. Combined with 3r ≡ −1 this forces l = 1 and r = 3.
* **3 | m and m'' > 1.** If r ≡ x* (mod m''), run from n ≡ 0 (mod m''). Otherwise run from n ≡ x* (mod m''). In both cases n ≡ x* (mod 2^N), and the run is never caught (Lemma R).
* **m = 3^k (l = 0).** On Z/3^k, the map φ(z) = (5z+1)/2 is one 3^k-cycle, because 5/2 ≡ 1 (mod 3) and 1/2 ≢ 0. Take the word U^{m−1}Q. Its cylinder C is (2-adic ball of radius 2^{−(m−1)} around x*) × (φ(r) + 3^k Z_3). The composed affine map sends C onto Z_2 × Z_3 and is expanding in both coordinates, so Lemma D'' gives a rational periodic point with multiplier (5/2)^{m−1}/m > 1 (for m = 3 it is 25/12).
* **m = 3^k 5^l with k, l ≥ 1.**
  * If r ≢ x* (mod 5^l): the run from n ≡ x* (mod 2^N · 5^l) is never caught.
  * Otherwise the cycle (−1 −2) must be caught. This forces l = 1 and r ≡ −2. Then the 3-cycle through −14/17 (word with multiplier 25/8) is uncaught, because none of its points is ≡ −2 (mod 15).

In every case Lemma B' or Lemma R excludes a certificate. ∎

## Theorem S7 (7x+1; PROVED for odd m ≤ 199)

For odd m ≤ 199, a certificate exists only for (m, r) = (7, 4). For c = 3 it is certified (**mb_s7_7**: n ≡ 4 (mod 7) → (n+3)/7; else even n → n/2; else (7n+1)/2), and GLOBAL holds with the single cycle (1 4). For every other (m, r) with m ≤ 199, some exactly verified expanding cycle of the plain map n ↦ (7n+1)/2, n/2 (Lyndon words of length ≤ 14) misses r mod m. That cycle is then uncaught (Lemma B').

A uniform proof for all m, in the style of S5, is routine but was not written out: S7 for m > 199 is EVIDENCE only.

## The mechanism, stated as a criterion (heuristic discussion; proved only where noted)

For a single class r mod m and the expanding odd branch U(y) = (a y + 1)/2, a certificate needs three things:

1. **x* must be caught**, if x* ∈ Z_m (that is, gcd(a − 2, m) = 1): r ≡ x* (mod m).
2. **Every up-run must be caught.** The run residues follow the affine map φ(z) = (a z + 1)/2 on Z/m. Every φ-orbit must hit r. With gcd(a(a−2), m) = 1 this is impossible: the orbits of x* and of the other points are disjoint. So some prime of m must divide a (runs collapse onto x* mod p^e) or a − 2 (φ is a translation-like single cycle mod p^e).
3. **The caught runs must still contract.** The worst run growth (a/2)^L/m must be < 1. This is what kills the a ≡ 2 (mod m) "every residue is visited" mechanism. For a = 5, m = 3 the run visits all residues mod 3 within 3 steps, but (5/2)²/3 = 25/12 > 1, and Lemma D'' turns this into a periodic point.

So the mechanism suggested in the task ("the run passes through every residue mod m within a bounded number of steps") does occur: it is condition 2 via a − 2. For a single class it is proved not to suffice for a = 5 (every odd m, S5, via Lemma D'') and for a = 7 with odd m ≤ 199 (S7, by exhaustive exact enumeration). For other a the three conditions above are a heuristic description, not a proof. Taming is possible only where the class sits on the x*-fiber and the run collapses p-adically within one or two steps.

## Tier, check and novelty

* The certifiable systems are tier 1.
* The necessity proofs are short exact obstructions (tier 2 content: finite witnesses).
* `check_single_class.py` (about 17 s) does the following:
  * for every odd m ≤ 301, every r, and two values of c, it builds and exactly verifies the witness of the proof (fixed point, run identity on CRT-constructed n, explicit cycle, or the Lemma D'' word);
  * it certifies the three positive cases and computes their cycles;
  * it confirms that the engine agrees with the classification for m ≤ 27;
  * it runs the a = 7 hitting-constraint classification for m ≤ 199.
* Novelty not checked. I know of no source that classifies single taming classes.
