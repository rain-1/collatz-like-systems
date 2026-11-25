"""CLS-035 (7n+7). Computational part of CLS-035.md. Exact integers. Exit 0 iff all pass.
(i) step agrees with census; (ii) T(7m) = 7 U(m) (U = 7n+1 map) for m < 10^5 and T(n) in 7Z for odd n;
(iii) Theorem A' sanity: residue graph mod M (M even <= 1000): class of 7 reachable from every class;
(iv) cycles: via the conjugacy, the cycles with <= 1000 odd terms are 7*{U-cycles} = {7,56,28,14} only
     (U-part checked by the 7n+1 enumeration)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sevnine_lib as S
T, U = S.STEPS['P77'], S.STEPS['P7']
ok = S.run_standard('P77')
ok &= all(T(7 * m) == 7 * U(m) for m in range(1, 10 ** 5))
ok &= all(T(n) % 7 == 0 for n in range(1, 10 ** 5, 2))
found, X = S.cycles_up_to('P7', 1000)
ok &= found == [(1, 1)]
cyc = [7]
while True:
    cyc.append(T(cyc[-1]))
    if cyc[-1] == 7: break
ok &= cyc == [7, 56, 28, 14, 7]
print('7n+7 cycle through 7:', cyc[:-1], 'all checks:', ok)
sys.exit(0 if ok else 1)
