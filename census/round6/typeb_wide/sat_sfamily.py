"""SAT search for type-(b) SCCs in S-families at level m (search tool; results are
re-verified exactly by tblib.classify, see check_sfamily_sat.py).

Family F(a, d, m, S): even n -> n/2; odd n -> a n + d if n mod 2^m in S, else n + d.

We ask z3 for S and a simple cycle C of G_m with multiplier a^A / 2^B > 1 whose SCC is
exactly C.  The SCC condition is encoded by a closed set R: every exit edge of C lands
in R, R is closed under the edges of G_m, and R is disjoint from C.  (If such R exists,
nothing reachable from an exit returns to C, so the SCC of C is C.  Conversely, if the
SCC of C is C, the set of nodes reachable from exits is such an R.)  So UNSAT means:
no S gives an SCC of G_m that is an expanding simple cycle.

Usage: python sat_sfamily.py a d m [maxsol]
"""
import sys, math
import z3

a, d, m = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
maxsol = int(sys.argv[4]) if len(sys.argv) > 4 else 1
Q, H = 2 ** m, 2 ** (m - 1)
odd = [r for r in range(Q) if r % 2]
s = {r: z3.Bool(f"s{r}") for r in odd}
inC = [z3.Bool(f"c{r}") for r in range(Q)]
R = [z3.Bool(f"R{r}") for r in range(Q)]
hb = [z3.Bool(f"h{r}") for r in range(Q)]          # even node: True -> r/2 + H on C
root = [z3.Bool(f"root{r}") for r in range(Q)]
ordv = [z3.Int(f"o{r}") for r in range(Q)]
sol = z3.Solver()
sol.add(z3.PbEq([(x, 1) for x in root], 1))
for r in range(Q):
    sol.add(z3.Implies(root[r], inC[r]))
    sol.add(z3.Not(z3.And(R[r], inC[r])))
    sol.add(ordv[r] >= 0, ordv[r] < Q)
    if r % 2 == 0:
        t0, t1 = r // 2, r // 2 + H
        sol.add(z3.Implies(R[r], z3.And(R[t0], R[t1])))
        for hv, q, other in ((False, t0, t1), (True, t1, t0)):
            cond = z3.And(inC[r], hb[r] == hv)
            sol.add(z3.Implies(cond, z3.And(inC[q], z3.Or(root[q], ordv[q] > ordv[r]), R[other])))
    else:
        qa, q1 = (a * r + d) % Q, (r + d) % Q
        sol.add(z3.Implies(z3.And(R[r], s[r]), R[qa]))
        sol.add(z3.Implies(z3.And(R[r], z3.Not(s[r])), R[q1]))
        for sv, q in ((True, qa), (False, q1)):
            cond = z3.And(inC[r], s[r] == sv)
            sol.add(z3.Implies(cond, z3.And(inC[q], z3.Or(root[q], ordv[q] > ordv[r]))))
# multiplier a^A / 2^B > 1  <=>  A*log2(a) > B ; integer scaling, exactness re-checked later
L = math.log2(a)
A = z3.Sum([z3.If(z3.And(inC[r], s[r]), 1, 0) for r in odd])
B = z3.Sum([z3.If(inC[r], 1, 0) for r in range(Q) if r % 2 == 0])
SC = 10 ** 6
sol.add(A * int(round(L * SC)) > B * SC + 10)
nsol = 0
while nsol < maxsol and sol.check() == z3.sat:
    M = sol.model()
    S = sorted(r for r in odd if z3.is_true(M.eval(s[r], model_completion=True)))
    C = sorted(r for r in range(Q) if z3.is_true(M.eval(inC[r], model_completion=True)))
    print("SAT", dict(a=a, d=d, m=m, S=S, C=C), flush=True)
    nsol += 1
    sol.add(z3.Or([s[r] != M.eval(s[r], model_completion=True) for r in odd]))
if nsol == 0:
    print("UNSAT", dict(a=a, d=d, m=m))
