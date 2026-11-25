"""Search natural matrix interpretations with z3 (needs the z3-solver module).

Usage: python mi_search.py B s1 s2 h dim maxentry rounds [drop-rule-prefix ...]
Prints a JSON certificate chain (list of [dim, {symbol: [M, v]}]) if every rule is
removed, else reports the remaining rules.  Certificates are re-verified with the
exact checker in srs.py; z3 is only the search engine.
"""
import json
import sys
import z3
from srs import family_srs, family_srs2, alphabet, verify_chain, check_interp, _rule_strict


W = 28  # bit width; entries <= maxe and words of length <= 5 cannot overflow


def sym_compose(word, I, d):
    M = [[z3.BitVecVal(int(i == j), W) for j in range(d)] for i in range(d)]
    v = [z3.BitVecVal(0, W) for _ in range(d)]
    for a in reversed(word):
        Ma, va = I[a]
        M = [[sum((Ma[i][k] * M[k][j] for k in range(1, d)), Ma[i][0] * M[0][j])
              for j in range(d)] for i in range(d)]
        v = [sum((Ma[i][k] * v[k] for k in range(1, d)), Ma[i][0] * v[0]) + va[i]
             for i in range(d)]
    return M, v


def one_round(rules, d, maxe, timeout_ms=300000):
    syms = alphabet(rules)
    s = z3.SolverFor("QF_BV")
    s.set("timeout", timeout_ms)
    I = {}
    for a in syms:
        M = [[z3.BitVec(f"M_{a}_{i}_{j}", W) for j in range(d)] for i in range(d)]
        v = [z3.BitVec(f"v_{a}_{i}", W) for i in range(d)]
        for x in [x for row in M for x in row] + v:
            s.add(z3.ULE(x, maxe))
        s.add(z3.UGE(M[0][0], 1))
        I[a] = (M, v)
    stricts = []
    for name, l, r in rules:
        Ml, vl = sym_compose(l, I, d)
        Mr, vr = sym_compose(r, I, d)
        for i in range(d):
            for j in range(d):
                s.add(z3.UGE(Ml[i][j], Mr[i][j]))
            s.add(z3.UGE(vl[i], vr[i]))
        stricts.append(z3.UGT(vl[0], vr[0]))
    s.add(z3.Or(stricts))
    res = s.check()
    print(f"  round dim={d} maxe={maxe} rules={len(rules)}: {res}", file=sys.stderr, flush=True)
    if res != z3.sat:
        return None
    m = s.model()
    out = {}
    for a, (M, v) in I.items():
        out[a] = ([[m.eval(x, model_completion=True).as_long() for x in row] for row in M],
                  [m.eval(x, model_completion=True).as_long() for x in v])
    return out


def search(rules, dims=(1, 2), maxe=3, rounds=60, timeout_ms=300000):
    chain = []
    remaining = list(rules)
    for _ in range(rounds):
        if not remaining:
            break
        found = None
        for d in dims:
            found = one_round(remaining, d, maxe, timeout_ms)
            if found is not None:
                break
        if found is None:
            break
        ok, strict = check_interp(remaining, found, d)
        assert ok and strict
        chain.append((d, found))
        gone = [x for x in remaining if _rule_strict(x, found, d)]
        print("  removed:", [(x[0], x[1][0] if x[0].startswith("tail") else "") for x in gone],
              file=sys.stderr, flush=True)
        remaining = [x for x in remaining if not _rule_strict(x, found, d)]
    return chain, remaining


def to_json(chain):
    return [[d, [[list(a), M, v] for a, (M, v) in interp.items()]] for d, interp in chain]


if __name__ == "__main__":
    B1, s1, B2, s2, h = map(int, sys.argv[1:6])
    dims = tuple(int(x) for x in sys.argv[6].split(","))
    maxe = int(sys.argv[7])
    drop = sys.argv[8:]
    rules = [r for r in family_srs2({1: (B1, s1), 2: (B2, s2)}, h)
             if not any(r[0].startswith(p) for p in drop)]
    chain, remaining = search(rules, dims, maxe)
    if remaining:
        print("FAILED; remaining:", len(remaining), sorted({r[0] for r in remaining}))
        print("CHAIN", json.dumps(to_json(chain)))
    else:
        rem, removed = verify_chain(rules, chain)
        assert not rem
        print("PROVED", json.dumps(to_json(chain)))
