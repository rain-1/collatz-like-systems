"""SAT/SMT search for Theorem-H-provable systems with an isolated expanding cycle
inside a 'choice family' (search tool only; every hit is re-verified exactly by
tblib.prove_H and verify_H.py).

A choice family is (p, m, opts) with opts[r] a list of branches (u, v, w) allowed on the
class r mod p^m.  We look for a choice of branch per class, a set C of nodes carrying one selected
'C-edge' each (so the C-edges form disjoint simple cycles plus tails), one of these
cycles D with multiplier > 1, together with
  * integer levels L(r), non-increasing along every edge, equal along C-edges, and
    strictly decreasing along every other edge that leaves or enters a C-node;
  * integer potentials psi(r) with psi(s) - psi(r) <= -ceil(SC log2 q) - 1 on every
    edge r -> s (multiplier q) whose ends have equal level and which is not a C-edge.
Then every SCC other than C has only cycles with log2 multiplier <= -len/SC < 0 (type a)
and C is an SCC by itself (type b): all hypotheses of Theorem H except the standing
hypothesis and positivity, which prove_H checks.  Conversely every system whose SCCs are
of type (a) except one expanding simple cycle satisfies the constraints (levels = a
topological order of SCCs, psi from max-mean potentials) once SC is large enough.

API: search(p, m, opts, maxsol, fixed=None, extra=None) -> list of choice vectors.
"""
import math
import z3

SC = 2 ** 22   # raised from 4096 after REFEREE1 item 4; completeness bound: check_sat_precision.py


def succs(p, m, r, br):
    Q = p ** m
    u, v, w = br
    e = round(math.log(w, p)) if w > 1 else 0
    step = Q // w
    base = ((u * r + v) // w) % step
    return [base + i * step for i in range(w)], Fraction_log(u, w)


def Fraction_log(u, w):
    return math.log2(u) - math.log2(w)


def search(p, m, opts, maxsol=1, timeout_ms=600000, require_b=True, block_vars=None,
           verbose=False):
    Q = p ** m
    s = z3.Solver()
    s.set("timeout", timeout_ms)
    ch = [[z3.Bool(f"o{r}_{k}") for k in range(len(opts[r]))] for r in range(Q)]
    inC = [z3.Bool(f"c{r}") for r in range(Q)]
    inD = [z3.Bool(f"d{r}") for r in range(Q)]
    root = [z3.Bool(f"rt{r}") for r in range(Q)]
    od = [z3.Int(f"od{r}") for r in range(Q)]
    od2 = [z3.Int(f"oe{r}") for r in range(Q)]
    L = [z3.Int(f"L{r}") for r in range(Q)]
    psi = [z3.Int(f"psi{r}") for r in range(Q)]
    mult_terms = []
    into = [[] for _ in range(Q)]      # D-edges into q: (inD[r] and sel) with od[r] < od[q]
    for r in range(Q):
        s.add(z3.PbEq([(x, 1) for x in ch[r]], 1))
        s.add(L[r] >= 0, L[r] <= Q, od[r] >= 0, od[r] < Q)
        s.add(z3.Implies(inD[r], inC[r]))
        s.add(z3.Implies(root[r], inD[r]))
        for k, br in enumerate(opts[r]):
            ss, lq = succs(p, m, r, br)
            wq = math.ceil(SC * lq)
            mult_terms.append(z3.If(z3.And(inD[r], ch[r][k]), int(math.floor(SC * lq)), 0))
            sel = [z3.Bool(f"sel{r}_{k}_{i}") for i in range(len(ss))]
            on = z3.And(inC[r], ch[r][k])
            s.add(z3.Implies(on, z3.PbEq([(x, 1) for x in sel], 1)))
            s.add(z3.Implies(z3.Not(on), z3.And([z3.Not(x) for x in sel])))
            for i, q in enumerate(ss):
                cedge = sel[i]
                s.add(z3.Implies(cedge, z3.And(inC[q], L[q] == L[r])))
                if br[2] == 1:
                    # division-free C-edges raise od2, so every C-cycle contains a division
                    s.add(z3.Implies(cedge, od2[q] > od2[r]))
                s.add(z3.Implies(z3.And(cedge, inD[r]), z3.And(inD[q], z3.Or(root[q], od[q] > od[r]))))
                into[q].append(z3.And(cedge, inD[r], od[r] < od[q]))
                active = ch[r][k]
                # non-C edges
                nc = z3.And(active, z3.Not(cedge))
                s.add(z3.Implies(nc, L[q] <= L[r]))
                s.add(z3.Implies(z3.And(nc, z3.Or(inC[r], inC[q])), L[q] < L[r]))
                s.add(z3.Implies(z3.And(nc, L[q] == L[r]), psi[q] - psi[r] <= -wq - 1))
    # D is exactly the cycle through the root: every non-root D-node has a D-predecessor of
    # smaller order (so it is reached from the root; tails into the cycle are excluded)
    for q in range(Q):
        s.add(z3.Implies(z3.And(inD[q], z3.Not(root[q])), z3.Or(into[q]) if into[q] else False))
    if require_b:
        s.add(z3.PbEq([(x, 1) for x in root], 1))
        s.add(z3.Sum(mult_terms) > 0)
    else:
        s.add(z3.And([z3.Not(x) for x in inC]))
    sols = []
    while len(sols) < maxsol:
        res = s.check()
        if res != z3.sat:
            if verbose:
                print("solver:", res)
            break
        M = s.model()
        choice = []
        for r in range(Q):
            k = [k for k in range(len(opts[r])) if z3.is_true(M.eval(ch[r][k], model_completion=True))]
            choice.append(k[0])
        C = [r for r in range(Q) if z3.is_true(M.eval(inC[r], model_completion=True))]
        sols.append((choice, C))
        bv = block_vars if block_vars is not None else range(Q)
        s.add(z3.Or([z3.Not(ch[r][choice[r]]) for r in bv if len(opts[r]) > 1]))
    return sols, (res if len(sols) < maxsol else "maxsol")
