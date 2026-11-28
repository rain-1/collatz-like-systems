"""b-suffix maps (possibly non-injective): the decision procedure of Theorem 1
(theorem1_suffix.md) and an exact verifier of the certificate it produces.

A b-suffix map is a list of rules (A, B) of digit strings over base b such that
the A's form a complete suffix code (every left-infinite word has exactly one
A as a suffix).  Arithmetically: n = b^|A| q + [A]  ->  b^|B| q + [B]  (q >= 0).
"""
import random

DIG = "0123456789abcdefghijklmnopqrstuvwxyz"


def val(w, b):
    return int(w, b) if w else 0


def word(n, b):
    s = ""
    while n:
        n, d = divmod(n, b)
        s = DIG[d] + s
    return s


class SuffixMap:
    def __init__(self, b, rules):
        self.b = b
        self.rules = rules
        self.ell = max(len(a) for a, _ in rules)
        self._check_code()

    def _check_code(self):
        # complete suffix code: every word of length ell has exactly one A as suffix
        b, ell = self.b, self.ell
        from itertools import product
        for tup in product(DIG[:b], repeat=ell):
            w = "".join(tup)
            hits = [a for a, _ in self.rules if w.endswith(a)]
            assert len(hits) == 1, (w, hits)
        # positivity
        for a, bb in self.rules:
            if a.strip("0") and not bb.strip("0"):
                raise ValueError("rule can send a positive integer to 0")

    def rule_for(self, w):
        """w: a word of length >= ell (may have leading zeros)."""
        for a, bb in self.rules:
            if w.endswith(a):
                return a, bb
        raise AssertionError

    def __call__(self, n):
        b = self.b
        w = word(n, b).rjust(self.ell, "0")
        a, bb = self.rule_for(w)
        q = (n - val(a, b)) // b ** len(a)
        return q * b ** len(bb) + val(bb, b)


def random_suffix_map(b, rng, splits=4, maxout=4):
    leaves = [""]
    for _ in range(splits):
        w = rng.choice(leaves)
        leaves.remove(w)
        leaves += [DIG[d] + w for d in range(b)]
    rules = []
    for a in leaves:
        while True:
            L = rng.randint(0, maxout)
            bb = "".join(rng.choice(DIG[:b]) for _ in range(L))
            if not (a.strip("0") and not bb.strip("0")):
                break
        rules.append((a, bb))
    return SuffixMap(b, rules)


def decide(T, s, maxsteps=5000):
    """Return ('periodic', t0, period) or ('pump', t, p, P, Ys, V) or ('unknown',)."""
    b, ell = T.b, T.ell
    seen = {}
    words = []
    n = s
    for t in range(maxsteps + 1):
        if n in seen:
            return ("periodic", seen[n], t - seen[n])
        seen[n] = t
        words.append(word(n, b))
        # pump search ending at t
        wt = words[t]
        if len(wt) > ell:
            Y = wt[-ell:]
            minh = len(wt)          # min height over (t0, t]
            for t0 in range(t - 1, -1, -1):
                w0 = words[t0]
                if len(w0) > ell and w0[-ell:] == Y and len(wt) > len(w0) and minh >= len(w0):
                    P = w0[:-ell]
                    assert wt.startswith(P)
                    V = wt[len(P):-ell]
                    Ys = [words[t0 + i][len(P):] for i in range(t - t0)]
                    return ("pump", t0, t - t0, P, Ys, V)
                minh = min(minh, len(w0))
        n = T(n)
    return ("unknown",)


def verify_pump_certificate(T, s, cert):
    """Exact check of the certificate C = U_i {b^|Y_i| z + [Y_i] : z >= 1}
    plus the finite orbit prefix.  Returns True or raises AssertionError.

    (1) the orbit of s reaches [P Y_0] at time t0, [P] >= 1;
    (2) for each i < p-1 the rule matched by Y_i (|Y_i| >= ell) rewrites Y_i
        into Y_{i+1}; for i = p-1 into V Y_0.  Because |Y_i| >= ell, the rule
        is the same for every prefix z, so this is a symbolic identity:
        T(b^|Y_i| z + [Y_i]) = b^|Y_{i+1}| z + [Y_{i+1}]  for all z >= 0;
    (3) hence T^p(b^|Y_0| z + [Y_0]) = b^|Y_0| (b^|V| z + [V]) + [Y_0], and
        b^|V| z + [V] > z for z >= 1, so no point of C is periodic.
    """
    _, t0, p, P, Ys, V = cert
    b, ell = T.b, T.ell
    assert P and P[0] != "0" and len(V) >= 1
    n = s
    for _ in range(t0):
        n = T(n)
    assert n == val(P + Ys[0], b)
    for i in range(p):
        Y = Ys[i]
        assert len(Y) >= ell
        a, bb = T.rule_for(Y)
        img = Y[:len(Y) - len(a)] + bb
        target = Ys[i + 1] if i + 1 < p else V + Ys[0]
        assert img == target, (i, Y, img, target)
        # numeric spot checks of the identity, including z = 0 and huge z
        for z in (0, 1, 2, 12345, 10 ** 30 + 7):
            x = z * b ** len(Y) + val(Y, b)
            assert T(x) == z * b ** len(target) + val(target, b)
    return True
