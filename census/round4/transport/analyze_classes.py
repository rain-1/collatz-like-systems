"""Summarize the transport-equivalence classes found by equiv.py: decide.py verdict and exact
trichotomy type of every member (consistency check of Theorems O1/O2: no class may mix CERT
and OBST members), and counts for the S-family.  usage: python3 analyze_classes.py results/equiv_X.json"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from transport_lib import unit_type, is_unit_padic
from equiv import population

def main(path):
    d = json.load(open(path))
    P = {s['id']: s for s in population(d['population'])}
    out = []
    for cl in d['classes']:
        row = []
        for i in cl:
            s = P[i]
            ty = unit_type(s['Q'], s['table'])['type'] if is_unit_padic(s['Q'], s['table']) else 'n/a'
            row.append((i, s['status'], ty))
        out.append(row)
    mixed = [r for r in out if len(set(x[2] for x in r)) > 1]
    print("classes", len(out), "members", sum(len(r) for r in out), "type-mixed classes", len(mixed))
    for r in mixed:
        print("  MIXED", r)
    from collections import Counter
    print(Counter(tuple(sorted(set(x[2] for x in r))) for r in out))
    fam = [r for r in out if all(x[1] == 'family' for x in r)]
    print("pure family classes", len(fam), "members", sum(len(r) for r in fam))
    json.dump(out, open(path.replace('.json', '_types.json'), 'w'), indent=0)

main(sys.argv[1])
