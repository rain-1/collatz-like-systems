# Matrix interpretations of rewriting encodings (Yolcu-Aaronson-Heule style)

Files: `srs_lib.py` (encoding, exact checker), `srs_cores.py` (S-family cores),
`mi_z3.py` (z3 search engine), `mi_record.py` (re-runs the cheap search and stores the chains
in `mi_chains.json`), `check_srs.py` (exact checks). Long runs: `scratch/k7_*.out`,
`scratch/core_*.out`.

Status: **EVIDENCE only (negative).** No interpretation was found that removes any map rule,
except the single map instance `small1` (LtR → LR, i.e. K7(1) = 0), which removes one value
and no arithmetic. *(Qualifier added after REFEREE1; the first version said "never a map rule"
without this exception.)*

## Encoding

A number is written as a word `L d_1 … d_k R`, most significant digit first, where each digit is
binary (`f` = 0, `t` = 1) or ternary (`a`, `b`, `c` = 0, 1, 2) and the value is computed by
Horner's rule with base 2 or 3 per digit. For the cores also `p` (x ↦ x + 1).

* Value-preserving rules, any context: the six swaps `x e → e' x'` (binary then ternary to
  ternary then binary, 3x + e = 2e' + x'), the left rules `La → L`, `Lb → Lt`, `Lc → Ltf`, and
  for the cores the increment rules `fp → t`, `tp → pf`, `ap → b`, `bp → c`, `cp → pa`,
  `Lp → Lt`, and `Lf → L`.
* K7 (z-form, z ≥ 0): `fR → R` (2y ↦ y), `ftR → R` (4y+1 ↦ y), `ttR → ctR` (4y+3 ↦ 6y+5),
  `LtR → LR` (1 ↦ 0).
* Core with set S (n-form, mod 8): `fR → R`; for odd r, the window `B3(r) R` is replaced by the
  word of 3n+1 (r ∈ S) or n+1 (r ∉ S, carry through `p` when r = 7); `LtR` is a normal form
  (n = 1); `LttR` is a normal form for sf3_13 (where 3 lies on the cycle (3 10 5 6)) and is
  rewritten to T(3) otherwise.

**Lemma (simulation). PROVED (finite parts checked).** Every rule preserves the value or applies
the map to the suffix it touches (`check_srs.py [SEM]`, exact affine identities). Hence any
derivation from `L bin(z) R` passes through words whose values follow the orbit of z, and the
strategy "move the leftmost ternary or `p` symbol left until it is absorbed, then apply the map
rule" reaches `L bin(T z) R` after each map step. If the rewriting system terminates (on all
words), every orbit reaches the stopping values (0 for K7; 1, or 3 for sf3_13), so GLOBAL holds
with the known cycle list. `check_srs.py [SIM]`, `[SIM-cores]` confirm the simulation for
z < 3000 and n < 2000, and `[NF]` that every binary word has a redex.

A natural matrix interpretation (symbols ↦ affine maps with nonnegative integer matrices,
top-left entry ≥ 1) that weakly orients all rules and strictly orients some lets one delete the
strict rules (Endrullis-Waldmann-Zantema). A chain that deletes all rules proves termination.

## Search and outcome

z3 (bit-vectors, installed in the local `.venv`) was used as a search engine only. Every chain
it returns is re-verified exactly by `srs_lib.verify_chain`.

| encoding | rules | removable (dims ≤ 2, entries ≤ 7, triangular) | left over (the core) | longer runs |
|---|---|---|---|---|
| K7 | 13 | `small1`, `left_a` | the 3 class map rules `e0`, `e1`, `e3`, 6 swaps, `left_b`, `left_c` | d = 3 (entries ≤ 7, triangular) and d = 2 (entries ≤ 15, full): z3 `unknown` (timeout) after 500 s; the next calls (d = 4, resp. d = 3) were cut off by the 19-minute run limit |
| sf3_17, sf3_57, sf3_157, sf3_357, sf3_13, sf3_135 | 21 or 22 | `lead0`, `left_a`, some increment rules | every map rule, the swaps, `left_b`, `left_c` | d = 3 triangular, entries ≤ 7: z3 `unknown` (timeout) after 150 s on each core; scratch/core_*.out |

The exact list per encoding is in `mi_chains.json` and is checked by `check_srs.py [CHAIN]`.
"unsat" answers of z3 (for example dimension 2, entries ≤ 7, triangular, on each core) are not
re-checked and are not claimed as theorems; "unknown" means a timeout.

## Reading

The removable rules are the bookkeeping ones (leading zeros, absorbing the digit 0 at the left
end) and, for K7, the single instance `small1` (1 ↦ 0). No rule that acts on a whole residue
class (the map rules `e0`, `e1`, `e3` of K7 and the odd/even rules of the cores) was oriented. This matches round 2 (m3_b: no
interpretation of dimension ≤ 2, entries ≤ 3) and the YAH experience with 3x+1 itself. These
interpretations are the one class in this lens that Theorems W and A do not exclude (see
theory.md §4, §6), so the negative result here is only EVIDENCE about small sizes, not a wall.
