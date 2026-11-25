"""Optional SAT tools (need python-sat).  CEGAR search for minimal base-b DFA certificates of residue-class affine maps.

Sample constraints (necessary for every certificate):
  a(n) -> a(T n)   for sample n with T n also in sample
  not a(seed), a(T seed); forward orbit accepted, backward (given) rejected.
A solution is checked exactly with autolib.closure_violation; a counterexample
(x, T x) is added to the sample.  UNSAT at k is a proof that no k-state
certificate exists (all constraints are necessary).
"""
from itertools import count
from pysat.solvers import Cadical153
from autolib import digits, closure_violation, make_step, accepts


def build(base, k, sample, step, seed, fwd, bwd, symbreak=True):
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
    node = {(): None}   # prefix tuple -> var list
    avar = {}

    def get(word):
        if word in node and node[word] is not None:
            return node[word]
        if word == ():
            return None
        par = get(word[:-1])
        d = word[-1]
        v = [next(ids) for _ in range(k)]
        node[word] = v
        if par is None:
            for r in range(k):
                cl.append([-t[0][d][r], v[r]])
        else:
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
    cl.append([-A(seed)])
    cl.append([A(step(seed))])
    for n in fwd:
        cl.append([A(n)])
    for n in bwd:
        cl.append([-A(n)])
    if symbreak and k > 1:
        cl.append([t[0][1][0], t[0][1][1]])
    return cl, t, f


def search(base, branches, seed, fwd, bwd, kmin=1, kmax=12, N=2000, verbose=True, max_iter=200):
    step = make_step(branches)
    sample = set(range(1, N + 1)) | set(fwd) | set(bwd) | {seed, step(seed)}
    for k in range(kmin, kmax + 1):
        it = 0
        while True:
            it += 1
            cl, t, f = build(base, k, sample, step, seed, fwd, bwd)
            with Cadical153(bootstrap_with=cl) as s:
                ok = s.solve()
                if not ok:
                    if verbose:
                        print(f"k={k}: UNSAT (sample {len(sample)})", flush=True)
                    break
                m = set(v for v in s.get_model() if v > 0)
            delta = [[next(r for r in range(k) if t[q][c][r] in m) for c in range(base)] for q in range(k)]
            acc = {q for q in range(k) if f[q] in m}
            dfa = dict(base=base, delta=delta, acc=acc)
            v = closure_violation(dfa, branches)
            if v is None:
                if verbose:
                    print(f"k={k}: FOUND {dfa}", flush=True)
                return k, dfa
            x, y = v
            # add a few iterates of the counterexample
            for _ in range(20):
                sample.add(x)
                x = step(x)
            sample.add(x)
            if it > max_iter:
                print("giving up at k", k)
                return None, None
    return None, None
