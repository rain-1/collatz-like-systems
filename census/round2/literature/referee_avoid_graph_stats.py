import sys, math
import os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _avoid_common import graph_edges, max_cycle_mean
for K in [{0},{1},{2},{3},{4},{5},{6},{7},{1,5},{1,7},{5,7}]:
    row=[]
    for j in (3,5,7,8):
        M=2**j
        E=graph_edges(M,K)
        a=max_cycle_mean(E)
        E2=[e for e in E if e[0]!=M-1 and e[1]!=M-1]
        b=max_cycle_mean(E2) if E2 else None
        row.append((j,round(a,4),round(b,4)))
    print(sorted(K),row)
