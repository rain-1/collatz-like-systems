"""Plain simulation of every seed: the weakest tool. Writes baseline.json."""
import json
from systems import SYSTEMS

out = []
for s in SYSTEMS:
    step, seed = s["step"], s["seed"]
    for n in range(1, 3000):        # well-definedness on small inputs
        m = step(n)
        assert isinstance(m, int) and m >= 1, (s["id"], n, m)
    seen, n, i = {}, seed, 0
    while n not in seen and i < 20000 and n.bit_length() < 4000:
        seen[n] = i
        n = step(n)
        i += 1
    if n in seen:
        fate = "returns to seed" if seen[n] == 0 else "enters other cycle"
        rec = dict(fate=fate, preperiod=seen[n], period=i - seen[n])
    else:
        rec = dict(fate="unknown after simulation", steps=i, bits=n.bit_length())
    bad = 0
    for x in range(1, 2001):        # how many small starts fail to cycle quickly
        seen2, n, i = set(), x, 0
        while n not in seen2 and i < 3000 and n.bit_length() < 600:
            seen2.add(n); n = step(n); i += 1
        bad += n not in seen2
    rec.update(id=s["id"], family=s["family"], rule=s["rule"], seed=seed,
               small_starts_not_cycling=bad)
    out.append(rec)
    print(f"{s['id']:22s} {rec['fate']:26s} noncycling<=2000: {bad}")
json.dump(out, open("baseline.json", "w"), indent=1)
print(len(out), "systems")
