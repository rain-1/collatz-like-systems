"""CEGAR SAT search for minimal base-b DFA certificates of DIVERGENCE
(non-injective version).  Needs python-sat (optional; not used by the checks).

A divergence certificate for (T, s) is a set C with T(C) <= C, T(s) in C and
C containing no periodic point.  Necessary sample constraints:
  a(n) -> a(T n)            for sample n with T n in sample,
  a(T^j s) for j >= 1        (forced in: the orbit),
  not a(n) for n in `out`    (forced out: points whose orbit is periodic).
UNSAT at k is therefore a proof that no k-state certificate exists.
The candidate check is delegated to `exact_ok(dfa)`.
"""
import os
import sys
from itertools import count

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "round2", "automata"))
from autolib import digits  # noqa: E402


def build(base, k, sample, step, fin, fout):
    ids = count(1)
    t = [[[next(ids) for _ in range(k)] for _ in range(base)] for _ in range(k)]
    f = [next(ids) for _ in range(k)]
    cl = []
    for q in range(k):
        for c in range(base):
            cl.append([t[q][c][r] for r in range(k)])
            for r1 in range(k):
                for r2 in range(r1 + 1, k):
                    cl.append([-t[q][c][r1], -t[q][c][r2]])
    node = {}
    avar = {}

    def get(word):
        if word in node:
            return node[word]
        d = word[-1]
        v = [next(ids) for _ in range(k)]
        node[word] = v
        if len(word) == 1:
            for r in range(k):
                cl.append([-t[0][d][r], v[r]])
        else:
            par = get(word[:-1])
            for p in range(k):
                for r in range(k):
                    cl.append([-par[p], -t[p][d][r], v[r]])
        return v

    def A(n):
        if n in avar:
            return avar[n]
        x = get(tuple(digits(n, base)))
        a = next(ids)
        avar[n] = a
        for r in range(k):
            cl.append([-x[r], -f[r], a])
            cl.append([-x[r], f[r], -a])
        return a

    for n in sample:
        m = step(n)
        if m in sample:
            cl.append([-A(n), A(m)])
    for n in fin:
        cl.append([A(n)])
    for n in fout:
        cl.append([-A(n)])
    return cl, t, f


def search(base, step, sample, fin, fout, exact_ok, kmin=1, kmax=20, verbose=True, max_iter=400):
    from pysat.solvers import Cadical153
    sample = set(sample) | set(fin) | set(fout)
    for k in range(kmin, kmax + 1):
        it = 0
        while True:
            it += 1
            cl, t, f = build(base, k, sample, step, fin, fout)
            with Cadical153(bootstrap_with=cl) as s:
                if not s.solve():
                    if verbose:
                        print(f"k={k}: UNSAT (sample {len(sample)})", flush=True)
                    break
                m = set(v for v in s.get_model() if v > 0)
            delta = [[next(r for r in range(k) if t[q][c][r] in m) for c in range(base)] for q in range(k)]
            acc = {q for q in range(k) if f[q] in m}
            dfa = dict(base=base, delta=delta, acc=acc)
            bad = exact_ok(dfa)
            if bad is None:
                if verbose:
                    print(f"k={k}: FOUND {dfa}", flush=True)
                return k, dfa
            for x in bad:
                for _ in range(15):
                    sample.add(x)
                    x = step(x)
                sample.add(x)
            if it > max_iter:
                print("giving up at k", k)
                return None, None
    return None, None
