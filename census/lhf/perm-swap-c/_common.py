"""Shared exact-integer helpers for the perm-swap-c checks."""
import os, sys
from fractions import Fraction as Fr
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..")))
from systems import get  # noqa: E402

def T(n):  # 1932 permutation
    q, i = divmod(n, 3)
    return (2*q, 4*q+1, 4*q+3)[i]
def Tinv(n):
    if n % 2 == 0: return 3*(n//2)
    q, i = divmod(n, 4)
    return 3*q+1 if i == 1 else 3*q+2
def S(n):  # perm_swap
    q, i = divmod(n, 3)
    return (2*q, 4*q+3, 4*q+1)[i]
def C(n):  # perm_c = S^{-1}
    if n % 2 == 0: return 3*(n//2)
    q, i = divmod(n, 4)
    return 3*q+2 if i == 1 else 3*q+1
BRANCH = {"T": (T, 3), "Tinv": (Tinv, 4), "S": (S, 3), "C": (C, 4)}

def edges(F, B, M):
    """Complete edge list of the residue graph mod M: B*M consecutive inputs suffice
    because F(n + B*M) = F(n) + (slope)*M for every branch."""
    adj = [set() for _ in range(M)]
    for n in range(1, B*M + 1):
        adj[n % M].add(F(n) % M)
    return [sorted(a) for a in adj]

def scc(adj):
    """Iterative Tarjan; returns component id per vertex."""
    n = len(adj); index = [-1]*n; low = [0]*n; on = [False]*n
    st = []; comp = [-1]*n; c = 0; idx = 0
    for s in range(n):
        if index[s] != -1: continue
        work = [(s, 0)]
        index[s] = low[s] = idx; idx += 1; st.append(s); on[s] = True
        while work:
            v, i = work[-1]
            if i < len(adj[v]):
                work[-1] = (v, i+1); w = adj[v][i]
                if index[w] == -1:
                    index[w] = low[w] = idx; idx += 1; st.append(w); on[w] = True
                    work.append((w, 0))
                elif on[w]:
                    low[v] = min(low[v], index[w])
            else:
                work.pop()
                if work: low[work[-1][0]] = min(low[work[-1][0]], low[v])
                if low[v] == index[v]:
                    while True:
                        w = st.pop(); on[w] = False; comp[w] = c
                        if w == v: break
                    c += 1
    return comp
