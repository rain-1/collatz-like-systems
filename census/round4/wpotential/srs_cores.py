"""String-rewriting encodings of the S-family cores (n-form, m = 3), for the
matrix-interpretation search.  Same alphabet as srs_lib plus 'p' (x -> x+1).

Rules (besides srs_lib.common_rules):
  fR -> R                                   (even n -> n/2)
  B3(r) R -> ter(c0) B3(rem) R              (r in S:  8q+r -> 8(3q+c0)+rem = 3n+1)
  B3(r) R -> B3(r+1) R   (r < 7)            (r not in S: n+1)
  tttR -> p fffR         (r = 7 not in S)   (n+1 with carry)
  fp -> t, tp -> pf, ap -> b, bp -> c, cp -> pa, Lp -> Lt     (increment)
  Lf -> L                                   (strip leading zeros)
  small numbers: L t R (n = 1) is a normal form; L t t R (n = 3) is a normal form
  if 3 lies on a cycle, otherwise L t t R -> L <bits T(3)> R.
Termination of the SRS implies: every orbit reaches 1 (or 3).
"""
import srs_lib as S


def bits3(r):
    return S.bits(r, 3)


def core_rules(Sset, three_on_cycle):
    rules = [("even", "fR", "R"), ("lead0", "Lf", "L")]
    for r in range(1, 8, 2):
        if r in Sset:
            val = 3 * r + 1
            c0, rem = divmod(val, 8)
            rules.append((f"odd{r}", bits3(r) + "R", "abc"[c0] + bits3(rem) + "R"))
        elif r < 7:
            rules.append((f"inc{r}", bits3(r) + "R", bits3(r + 1) + "R"))
        else:
            rules.append(("inc7", "tttR", "pfffR"))
    rules += [("p_f", "fp", "t"), ("p_t", "tp", "pf"), ("p_a", "ap", "b"), ("p_b", "bp", "c"),
              ("p_c", "cp", "pa"), ("p_L", "Lp", "Lt")]
    if not three_on_cycle:
        T3 = 10 if 3 in Sset else 4
        rules.append(("small3", "LttR", "L" + S.bits(T3) + "R"))
    return rules + S.common_rules()
