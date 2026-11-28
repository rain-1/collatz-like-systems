# Dressing: expanding fixed points whose runs are consumed by a second prime

Check: `check_dressing.py` (exits 0, about 5 s).

This file shows that the Markov property (M), and hence unit multipliers, is needed for the
mechanism "type (c) ⇒ infinitely many expanding periodic orbits" in the proof of Theorem N
(`trichotomy.md`), and that absence of certificates does not imply openness. It does not refute
the *conclusion* of Theorem N for non-unit systems: an analogous cover of Z_p × Z_q would have to
exclude all points with p-component 0, which is not a finite union of periodic orbits, so D has
no generalized certificate either. What dressing shows is (i) graph-level free re-entry without
(M) does not produce the realized walks C^d W, so the mechanism in the proof of N needs unit
multipliers; and (ii) "no (generalized) certificate" does not imply "hard": D is settled while
certificate-free, and certifiability is not invariant under first-return equivalence. It also gives a construction that turns *any* system of the div-form into one with no
descent certificate, without changing its answer.

## Definitions

Fix distinct primes p and q, and e ≥ 1 with `q^e > p`. Let g be any map from the positive
integers coprime to pq to the positive integers. Write ρ(x) for the pq-rough part
`x / (p^{v_p(x)} q^{v_q(x)})`.

* **Undressed map:** `U(x) = x/p` if p | x; `x/q` if p ∤ x and q | x; `g(x)` otherwise.
  For p = 2, q = 3 and g(x) = 5x+1 this is the catalog system div23_5n1.
* **Dressed map:** `D(x) = q^e x / p` if p | x; `x/q` if p ∤ x and q | x; `g(x)` otherwise.

## Theorem K. PROVED

1. **Run identity.** For `x = p^i q^k w` with w coprime to pq:
   * `D^{i+ei+k}(x) = w`, and the intermediate values are `q^{k+es} p^{i−s} w` (s ≤ i), followed by
     `q^{k+ei−s} w`;
   * `U^{i+k}(x) = w`.
2. **Same first return.** D and U have the same first-return map `R(w) = ρ(g(w))` on pq-rough
   numbers. Every orbit of either map meets a rough number within finitely many steps. Hence
   * GLOBAL(D) ⇔ GLOBAL(U) ⇔ every R-orbit is eventually periodic;
   * the cycles of D, the cycles of U and the cycles of R are in bijection, each cycle
     corresponding to the set of rough numbers on it.
3. **D never has a descent certificate**, whatever g is. Let M be any modulus, M = p^s M′ with
   p ∤ M′. For n ≡ 0 (mod p^N M′) with N ≥ s, we have `D^j(n) = (q^e/p)^j n > n` for every j ≤ N.
   So the class 0 mod M contains infinitely many n that do not descend within any prescribed
   number of steps. The p-adic point 0 is a fixed point with multiplier q^e/p > 1.

*Proof.* (1) While p | x, D multiplies by q^e/p, which removes one p and adds e factors q. Then
q | x and p ∤ x, so D divides by q until the value is rough. U does the same thing without adding
the q's.

(2) Between consecutive visits to rough numbers, both maps apply g once and then strip p and q
completely, by (1). The rest is bookkeeping. A D-orbit is eventually periodic iff the
subsequence of its rough points is, because D is deterministic and the gaps between rough points
are finite.

(3) This is the computation in (1) with w replaced by the whole number. CRT gives infinitely many
such n in every class 0 mod M. ∎

**Why this escapes Theorem N.** In D the expanding branch has multiplier q^e/p, which is not a unit
at q. So the image of a cylinder is not a union of cylinders: the q-adic depth is created, not
read off (the Markov property (M) fails). At the level of residue graphs the shadow of 0 is
re-entered freely, since g can land on any class mod p^a q^b. But the graph walks "C^d W" are not
realized by points: after a run of length d, the q-adic part is forced to depth e·d, and the
q-divisions consume exactly the gain. So *descent certifiability is not invariant under
first-return equivalence*, and the barrier of Theorem N depends on (M).

## Systems

| id | rule | question | answer | status |
|---|---|---|---|---|
| dress_23_x1 | 2∣x→3x/2; else 3∣x→x/3; else x+1 | GLOBAL | yes; only cycle (1 2 3) | PROVED (tier 1 given Thm K; OBST) |
| dress_32_x1 | 3∣x→4x/3; else 2∣x→x/2; else x+1 | GLOBAL | yes; only cycle (1 2) | PROVED (tier 1 given Thm K; OBST; base-3 expanding fixed point with multiplier 4/3) |
| dress_23_3x1 | 2∣x→3x/2; else 3∣x→x/3; else 3x+1 | GLOBAL | ⇔ the 3x+1 problem (R = Syracuse on numbers coprime to 6) | equivalence PROVED; GLOBAL OPEN |
| dress_23_5x1 | 2∣x→3x/2; else 3∣x→x/3; else 5x+1 | GLOBAL | ⇔ div23_5n1 (catalog, open); cycles in bijection, (1 6 9 3) ↔ (1 6 3) | equivalence PROVED; GLOBAL OPEN |

*dress_23_x1 and dress_32_x1.* Here `R(w) = ρ(w+1)`. For rough w ≥ 5, w+1 is even, so
`R(w) ≤ (w+1)/2 < w`, and R(1) = 1. Every R-orbit reaches 1, so by Theorem K(2) every D-orbit
reaches the D-cycle through 1: (1 2 3) for p = 2, and (1 2) for p = 3 (1 → 2 → 1). By Theorem
K(3) neither has a descent certificate.

These two systems are honestly easy *once the dressing is seen*. They are the minimal examples of
an OBST system with a harmless expanding fixed point and free graph-level re-entry.

*dress_23_3x1.* 3w+1 is never divisible by 3, so `R(w) = odd(3w+1)`, the Syracuse map restricted
to numbers coprime to 6. Every Syracuse orbit enters that set after one step. So GLOBAL(D) holds
iff every 3x+1 orbit is eventually periodic, and D's cycles correspond to those of 3x+1.

**Novelty.** Not checked. The construction resembles FRACTRAN-style prime bookkeeping (Conway),
but I have not seen it used to separate descent certifiability from the GLOBAL answer.
