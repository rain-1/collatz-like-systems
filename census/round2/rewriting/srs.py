"""Mixed-base string rewriting encodings and exact matrix-interpretation checking.

Family F(B; s1, s2):   3k -> k,   3k+1 -> B*k + s1,   3k+2 -> B*k + s2.

Word encoding (Horner, most significant first):  L d_1 ... d_m R  where each
digit symbol is ('t', r) with base 3 and value r in {0,1,2}, or ('b', d) with
base B and value d in {0..B-1}.  value(w d) = value(w)*base(d) + digit(d).

Rules (all strings over the alphabet, any position):
  tail rules, with a left context of h digit symbols x_1..x_h:
     x t0 R -> x R                  (3k   -> k)
     x t1 R -> x b_{s1} R          (3k+1 -> B k + s1)
     x t2 R -> x b_{s2} R          (3k+2 -> B k + s2)
  swap rules  t_r b_d -> b_q t_{r'}      where B*r + d = 3*q + r'
  left rules  L b_d -> L tern(d)          (ternary digits of d, no leading 0)

Simulation lemma (proved in the .md files): if n >= 3^h is written in ternary
without leading zeros, every maximal derivation from its word passes through the
ternary word of F(n) (all b-symbols must migrate to L before a tail rule can
fire again, and the swap / left rules preserve the value).  Hence if the SRS
is terminating, every F-orbit reaches a value < 3^h.

Matrix interpretations: symbol -> (M, v), M in N^{d x d}, v in N^d, M[0][0]>=1,
and a word a_1..a_k is interpreted as the composition f_{a_1} o ... o f_{a_k}.
For a rule l -> r:  weakly decreasing if M_l >= M_r and v_l >= v_r entrywise;
strictly decreasing if moreover v_l[0] > v_r[0].  Standard (Endrullis,
Waldmann, Zantema 2008): if all rules weakly decrease and the strict ones are
removed, termination of the remainder implies termination of the whole.
"""
from itertools import product

L, R = ('L',), ('R',)


def tern(d):
    if d == 0:
        return []
    out = []
    while d:
        out.append(('t', d % 3))
        d //= 3
    return out[::-1]


def family_srs(B, s1, s2, h=1):
    return family_srs2({1: (B, s1), 2: (B, s2)}, h)


def sym(base, d):
    return ('t', d) if base == 3 else ('b', d) if base == 4 else (f'b{base}', d)


def family_srs2(branches, h=1):
    """branches[r] = (B_r, s_r): 3k+r -> B_r*k + s_r for r = 1, 2 (3k -> k).
    Bases B_r must lie in {2, 4, 5, ...} (not 3)."""
    for B, s_ in branches.values():
        assert B != 3 and 0 <= s_ < B, "digit must be a proper base-B digit"
    bases = sorted({B for B, _ in branches.values()})
    digits = [('t', r) for r in range(3)] + [sym(B, d) for B in bases for d in range(B)]
    rules = []
    tails = {0: []}
    for r, (B, s_) in branches.items():
        tails[r] = [sym(B, s_)]
    for ctx in product(digits, repeat=h):
        ctx = list(ctx)
        for r in range(3):
            rules.append((f"tail{r}", ctx + [('t', r), R], ctx + tails[r] + [R]))
    for B in bases:
        for r in range(3):
            for d in range(B):
                q, rr = divmod(B * r + d, 3)
                rules.append((f"swap{B}_{r}{d}", [('t', r), sym(B, d)], [sym(B, q), ('t', rr)]))
        for d in range(B):
            rules.append((f"left{B}_{d}", [L, sym(B, d)], [L] + tern(d)))
    return rules


def alphabet(rules):
    s = set()
    for _, l, r in rules:
        s.update(l)
        s.update(r)
    return sorted(s)


# ------------------------------------------------------------ exact checking
def mat_mul(A, Bm):
    n, m, p = len(A), len(Bm), len(Bm[0])
    return [[sum(A[i][k] * Bm[k][j] for k in range(m)) for j in range(p)] for i in range(n)]


def compose(word, interp, d):
    M = [[int(i == j) for j in range(d)] for i in range(d)]
    v = [0] * d
    # f_{a1} o ... o f_{ak}: apply innermost (last) first
    for a in reversed(word):
        Ma, va = interp[a]
        # new(x) = Ma (M x + v) + va
        M = mat_mul(Ma, M)
        v = [sum(Ma[i][k] * v[k] for k in range(d)) + va[i] for i in range(d)]
    return M, v


def check_interp(rules, interp, d):
    """Return (ok, strict_rule_names). ok iff every rule weakly decreases and
    every symbol has M[0][0] >= 1 and nonnegative entries."""
    for a, (M, v) in interp.items():
        if M[0][0] < 1 or any(x < 0 for row in M for x in row) or any(x < 0 for x in v):
            return False, []
    strict = []
    for name, l, r in rules:
        Ml, vl = compose(l, interp, d)
        Mr, vr = compose(r, interp, d)
        if any(Ml[i][j] < Mr[i][j] for i in range(d) for j in range(d)):
            return False, []
        if any(vl[i] < vr[i] for i in range(d)):
            return False, []
        if vl[0] > vr[0]:
            strict.append(name)
    return True, strict


def verify_chain(rules, chain):
    """chain: list of (d, interp) applied in order; each must weakly orient the
    remaining rules and strictly orient at least one; the remaining set must
    end empty.  Returns the list of removed rule-name sets."""
    remaining = list(rules)
    removed = []
    for d, interp in chain:
        ok, strict = check_interp(remaining, interp, d)
        assert ok, "interpretation does not weakly orient the remaining rules"
        assert strict, "interpretation removes nothing"
        removed.append(sorted(set(strict)))
        remaining = [x for x in remaining if x[0] not in set(strict) or
                     not _rule_strict(x, interp, d)]
    return remaining, removed


def _rule_strict(rule, interp, d):
    _, l, r = rule
    return compose(l, interp, d)[1][0] > compose(r, interp, d)[1][0]
