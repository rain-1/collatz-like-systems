"""z3 search for natural matrix interpretation chains (search engine only;
every result is re-verified exactly by srs_lib.verify_chain)."""
import sys, json, time
import z3
import srs_lib

W = 24


def sym_compose(word, I, d):
    M = [[z3.BitVecVal(int(i == j), W) for j in range(d)] for i in range(d)]
    v = [z3.BitVecVal(0, W) for _ in range(d)]
    for a in reversed(word):
        Ma, va = I[a]
        M = [[sum((Ma[i][k] * M[k][j] for k in range(1, d)), Ma[i][0] * M[0][j]) for j in range(d)] for i in range(d)]
        v = [sum((Ma[i][k] * v[k] for k in range(1, d)), Ma[i][0] * v[0]) + va[i] for i in range(d)]
    return M, v


def one_round(rules, d, maxe, timeout_ms, must=None, triangular=False):
    syms = sorted({s for _, l, r in rules for s in l + r})
    s = z3.SolverFor("QF_BV")
    s.set("timeout", timeout_ms)
    I = {}
    for a in syms:
        M = [[z3.BitVec(f"M_{a}_{i}_{j}", W) for j in range(d)] for i in range(d)]
        v = [z3.BitVec(f"v_{a}_{i}", W) for i in range(d)]
        for i in range(d):
            for j in range(d):
                s.add(z3.ULE(M[i][j], maxe))
                if triangular and j < i:
                    s.add(M[i][j] == 0)
        for x in v:
            s.add(z3.ULE(x, maxe))
        s.add(z3.UGE(M[0][0], 1))
        I[a] = (M, v)
    stricts = {}
    for name, l, r in rules:
        Ml, vl = sym_compose(l, I, d)
        Mr, vr = sym_compose(r, I, d)
        for i in range(d):
            for j in range(d):
                s.add(z3.UGE(Ml[i][j], Mr[i][j]))
            s.add(z3.UGE(vl[i], vr[i]))
        stricts[name] = z3.UGT(vl[0], vr[0])
    if must:
        for nm in must:
            s.add(stricts[nm])
    else:
        s.add(z3.Or(list(stricts.values())))
    res = s.check()
    if res != z3.sat:
        return None, str(res)
    m = s.model()
    out = {a: ([[m.eval(x, model_completion=True).as_long() for x in row] for row in M],
               [m.eval(x, model_completion=True).as_long() for x in v]) for a, (M, v) in I.items()}
    return out, "sat"


def search(rules, dims, maxe, timeout_ms=120000, rounds=40, triangular=False, log=sys.stderr):
    chain, remaining = [], list(rules)
    for _ in range(rounds):
        if not remaining:
            break
        found = None
        for d in dims:
            t0 = time.time()
            found, st = one_round(remaining, d, maxe, timeout_ms, triangular=triangular)
            print(f"  d={d} maxe={maxe} rules={len(remaining)}: {st} ({time.time()-t0:.1f}s)", file=log, flush=True)
            if found is not None:
                break
        if found is None:
            break
        ok, strict = srs_lib.orient(remaining, found, d)
        assert ok and strict
        print("   removed", strict, file=log, flush=True)
        chain.append((d, found))
        remaining = [x for x in remaining if x[0] not in strict]
    return chain, remaining
