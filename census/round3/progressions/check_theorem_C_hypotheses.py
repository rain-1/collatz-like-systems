"""Round 3, lens 'progressions': two hypotheses of Theorem C that check_counting.py does not assert.

The proof of Theorem C starts by placing a vertex of the merging class H in a type progression
tau + W Z.  That step needs (1) the invariant g to be state-free (a function of n mod d* only) and
(2) gcd(W, d*) = 1.  Both are verified here for all 32 certified systems.  (Added after the second
referee's nit and a separate read of the proof.)
"""
import json, math, os, sys
here = os.path.dirname(os.path.abspath(__file__))
certs = {c["id"]: c for c in json.load(open(os.path.join(here, "certificates.json")))}
rows = json.load(open(os.path.join(here, "counting_results.json")))
assert len(rows) == 32
bad = []
for r in rows:
    c = certs[r["id"]]
    W, d = int(r["W"]), int(c["invariant_modulus"])
    ok = c["state_free"] is True and math.gcd(W, d) == 1 and c["theorem_A"] is True
    print(f"{r['id']:16s} W={W:<6d} d*={d:<6d} state_free={c['state_free']} gcd={math.gcd(W, d)}  {'ok' if ok else 'FAIL'}")
    if not ok:
        bad.append(r["id"])
if bad:
    print("FAILED:", bad); sys.exit(1)
print("all 32 systems: g state-free, gcd(W, d*) = 1, Theorem A hypotheses hold")
