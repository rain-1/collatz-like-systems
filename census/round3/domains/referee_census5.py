"""referee_census5.py -- full m = 5 Gaussian S-family census with the referee's
own builder (referee_check.gcert) and own obstruction search.  About 5-10 min.
Claim tested: CERT = 2277, OBST = 63259, UNK = 0, max certifiable |S| = 9."""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import referee_check as R
odd = sorted({R.gres((a, b), 5) for a in range(-8, 9) for b in range(-8, 9) if (a + b) % 2})
st = {'CERT': 0, 'OBST': 0, 'UNK': 0}
mx = 0
t0 = time.time()
for mask in range(2 ** 16):
    S = [odd[i] for i in range(16) if mask >> i & 1]
    if R.residue_graph_obstruction(5, S, 5) or R.residue_graph_obstruction(5, S, 7):
        st['OBST'] += 1
        continue
    lv = R.gcert(5, S, maxnodes=400000, maxK=60)
    if lv is None:
        st['UNK'] += 1
        print('UNK', mask, flush=True)
    else:
        st['CERT'] += 1
        mx = max(mx, len(S))
print(st, 'max|S| cert', mx, round(time.time() - t0), 's')
assert st == {'CERT': 2277, 'OBST': 63259, 'UNK': 0} and mx == 9
print('CENSUS5 OK')
