"""Mixed binary/ternary string rewriting encodings of 2-adic table maps, and
exact checking of natural matrix interpretations (rule-removal chains).

Symbols: 'L' (left end), 'R' (right end), binary digits 'f'=0, 't'=1,
ternary digits 'a'=0, 'b'=1, 'c'=2.  A word L d1 ... dk R has the Horner value
val = (((0*B1 + d1)*B2 + d2) ... ), B = 2 for f/t and 3 for a/b/c.

Value-preserving rules (any context):
  swaps   x e -> e' x'   (x binary, e ternary, 3x+e = 2e'+x')
  left    L a -> L,  L b -> L t,  L c -> L t f
Map rules: given per system (right-end windows).

Matrix interpretations: symbol -> (M, v), M in N^{dxd}, v in N^d, M[0][0] >= 1.
A word a1..ak is interpreted as f_{a1} o ... o f_{ak}.  A rule l -> r is weakly
decreasing if M_l >= M_r and v_l >= v_r entrywise, strictly if also v_l[0] > v_r[0].
(Endrullis-Waldmann-Zantema 2008; rule removal.)
"""
BIN = {'f': 0, 't': 1}
TER = {'a': 0, 'b': 1, 'c': 2}


def value(word):
    x = 0
    for s in word:
        if s in BIN:
            x = 2 * x + BIN[s]
        elif s in TER:
            x = 3 * x + TER[s]
    return x


def bits(z, width=None):
    s = bin(z)[2:] if z > 0 else ''
    if width is not None:
        s = s.rjust(width, '0')
        assert len(s) == width
    return ''.join('t' if ch == '1' else 'f' for ch in s)


def common_rules():
    rules = []
    for x, xv in BIN.items():
        for e, ev in TER.items():
            tot = 3 * xv + ev
            e2, x2 = divmod(tot, 2)
            rules.append(("swap_" + x + e, x + e, 'abc'[e2] + 'ft'[x2]))
    rules += [("left_a", "La", "L"), ("left_b", "Lb", "Lt"), ("left_c", "Lc", "Ltf")]
    return rules


# ---------------------------------------------------------------- exact MI
def mat_mul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))]
            for i in range(len(A))]


def compose(word, I, d):
    M = [[int(i == j) for j in range(d)] for i in range(d)]
    v = [0] * d
    for a in reversed(word):
        Ma, va = I[a]
        M = mat_mul(Ma, M)
        v = [sum(Ma[i][k] * v[k] for k in range(d)) + va[i] for i in range(d)]
    return M, v


def orient(rules, I, d):
    """(ok, strict names): ok iff every rule weakly decreases."""
    for a, (M, v) in I.items():
        assert M[0][0] >= 1 and min(min(r) for r in M) >= 0 and min(v) >= 0
    strict = []
    for name, l, r in rules:
        Ml, vl = compose(l, I, d)
        Mr, vr = compose(r, I, d)
        if any(Ml[i][j] < Mr[i][j] for i in range(d) for j in range(d)) or \
           any(vl[i] < vr[i] for i in range(d)):
            return False, []
        if vl[0] > vr[0]:
            strict.append(name)
    return True, strict


def verify_chain(rules, chain):
    remaining = list(rules)
    for d, I in chain:
        ok, strict = orient(remaining, I, d)
        assert ok and strict
        remaining = [x for x in remaining if x[0] not in strict]
    return remaining
