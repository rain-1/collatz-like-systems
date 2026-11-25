# farkas5m_s27 (NEW): a ×5 Farkas-type variant

Rule: n ≡ 3 (mod 5) -> (n+2)/5; otherwise even n -> n/2; otherwise (odd n) -> (5n-3)/2. Seed 27.
As a mod-10 table: residues 3 and 8 -> (n+2)/5; 0, 2, 4, 6 -> n/2; 1, 5, 7, 9 -> (5n-3)/2.

The map is built to sit next to split5_* and par_5_*. It has the same ×5/2 expanding branch, with up-runs
of unbounded length, together with a Farkas-type "undo" branch for multiplication by 5. Its 3x+1
analogue is the Farkas variant whose termination Yolcu, Aaronson and Heule proved automatically with
arctic matrix interpretations ("An automated approach to the Collatz conjecture", J. Automated
Reasoning 67 (2023), Sec. 4.2, arXiv:2105.14697). That paper also gives an inductive proof in the
manner of Farkas.

| question | answer | status | tier |
|---|---|---|---|
| FATE (seed 27) | reaches the fixed point 1: 27, 66, 33, 7, 16, 8, 2, 1 | PROVED | 0 |
| GLOBAL | yes: every orbit reaches 1, and {1} is the only cycle | PROVED | 1 (a finite table, tier 2, provably fails) |

## Proof of GLOBAL
T(1) = (5-3)/2 = 1. Let n > 1. We show that the orbit reaches a value m with 1 <= m < n. Strong
induction then gives that every orbit reaches 1, and that no other cycle exists.

- n ≡ 3 (mod 5): T(n) = (n+2)/5, which is < n and >= 1.
- n even, n ≢ 3 (mod 5): T(n) = n/2 < n.
- n odd, n ≢ 3 (mod 5), n >= 3. Write n - 1 = 2^a b with a >= 1 and b odd.
  1. *Up-run.* Put x_i = 5^i 2^(a-i) b + 1 for 0 <= i <= a, so x_0 = n. For 1 <= i < a, x_i is odd and
     x_i ≡ 1 (mod 5). Hence x_i is not caught by the first rule, and the odd rule applies:
     (5x_i - 3)/2 = 5^(i+1) 2^(a-i-1) b + 1 = x_(i+1). The same holds for i = 0 by hypothesis.
  2. x_a = 5^a b + 1 is even and ≡ 1 (mod 5), so it is halved: z_a = (5^a b + 1)/2.
  3. *Down-run.* For k >= 1 put z_k = (5^k b + 1)/2. Then z_k ≡ 1·2^(-1) ≡ 3 (mod 5), and
     (z_k + 2)/5 = (5^k b + 5)/10 = (5^(k-1) b + 1)/2 = z_(k-1).
  So T^(2a+1)(n) = z_0 = (b+1)/2. Also n = 2^a b + 1 >= 2b + 1 > (b+1)/2 >= 1. ∎

## Why tier 2 fails (proved)
Take n = 2^a b + 1 with b odd and n ≢ 3 (mod 5). This is a union of residue classes mod 5·2^(a+1). The a up-steps produce
x_1 < x_2 < ... < x_a, all > n. Then z_a, z_(a-1), ... stay above n while 5^k b/2 > 2^a b. So the
stopping time is at least a + 1 + (a - ⌈(a+1) log_5 2⌉), which is unbounded in a. No descent table
with a fixed modulus and a bounded number of steps closes every class.

The machine-generated descent tree (lib.descent_tree) shows the shape exactly. At modulus 5·2^K
the exceptional set consists of 8 classes, all ≡ 1 (mod 2^(K-2)), with density 8/(5·2^K), for every
K tested (6, 10, 14, 18). E shrinks to the single 2-adic point 1, crossed with residues mod 5, and
never becomes empty. This is the only system in our batch whose exceptional set is a single point.

## Tier and what this system shows about the boundary
Following the round-1 ruling on farkas_s27 (valuation bookkeeping plus a closed-form block = tier 1),
this is tier 1, even though the finite-table method of tier 2 provably fails. So the tier scale is
not nested: "tier 2 fails" does not imply "tier >= 3".

Lens observation (evidence, not a theorem). In every system we examined, an exceptional set that
shrinks to finitely many p-adic points went with an exact pairing like the one above: the up-run
conjugacy x -> ρx is undone step for step by a priority branch. That pairing is precisely what
the closed-form tier-1 proof uses. When the pairing is absent, E branches at every depth (the eight
OPEN systems here). We found no system in between, where E is thin enough for a parametric
certificate but no closed-form pairing exists.

Check: `check_farkas5m_s27.py` verifies the table against the direct definition, the seed, the block
identity T^(2a+1)(n) = (b+1)/2 for every eligible odd n <= 2·10^5, descent for every
1 < n <= 2·10^5, and the 8-class exceptional set at four moduli.

## Referee (round 2)
**Verdict.** GLOBAL: confirmed, final tier 1 (agreed). FATE(27): tier 0.
- I re-derived the proof line by line, including both cases:
  - For 1 <= i < a, x_i ≡ 1 (mod 5), and x_i is odd because a-i >= 1.
  - x_a is even and ≢ 3 (mod 5), so it is halved.
  - z_k ≡ 3 (mod 5), since 2·3 ≡ 1, so the priority branch applies.
  - The z_0 bound and the n = 3 edge case also check out.
- Independent test against the systems.py step:
  - the table agrees with the direct definition for n < 10^5;
  - the block identity T^(2a+1)(n) = (b+1)/2 holds for every eligible odd n < 3·10^5 and for 2000 random 300-bit n;
  - the seed path is as stated;
  - check_farkas5m_s27.py exits 0.
- No lower tier is possible: GLOBAL is universal, so simulation (tier 0) cannot settle it.
- Citation: Yolcu, Aaronson and Heule, "An Automated Approach to the Collatz Conjecture", J. Automated Reasoning 67, article 15 (2023), arXiv:2105.14697. The paper exists and treats "Farkas' variant". I did not verify the section number 4.2.
- Caveat: this is the ×5 analogue of round-1 farkas_s27 and uses the same pairing proof. It adds a calibration point, not a middle-tier system.
