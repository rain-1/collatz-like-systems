"""Exact re-checks of the family tables (README "Results").

[SCAN]  re-runs the classification of every member of the small families (and, with
        --full, of all families in families.py except D27) and compares the verdict counts
        and the list of type-(b) members with data/scan_<family>.json.
[R3]    cross-check with round 3: CERT (= type a) counts of S3_m3..m5, C9 and B27_a* equal
        the numbers in round3/dichotomy/scan_base3.out and round3/README.md.
[PROOF] every stored Theorem-H proof object (data/*_H.json, data/mods_*.json) passes the
        independent verifier verify_H.py.
[BRUTE] the exhaustive C scans of the S-family at m = 6 (out/brute, run_brute.sh): all 4096
        slices finished for a = 3 and a = 5; no member is free of type (c) ("nH = 0") and
        no float verdict was within 1e-9 of 0 ("nunc = 0").  Exactness of the float verdict:
        a simple cycle of G_6 has at most 32 odd-class steps (A <= 32) and at most 32 halvings
        (B <= 32; corrected from a loose 'B <= 64' after REFEREE1), and min |A log 3 - B log 2|
        over 1 <= A <= 32, B <= 32 is > 0.013 (3^12/2^19), so
        every cycle mean of the a = 3 family differs from 0 by > 2e-4 (similarly for a = 5:
        min |A log 5 - B log 2| > 0.02 for A <= 32, from 5^3/2^7); float error is far below that.
Exit 0 iff all pass.  Default runtime about 1 minute; --full about 10 minutes.
"""
import sys, os, json, re, glob, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import families as FM
import scan as SC
import verify_H as VH

OK = True


def claim(name, cond):
    global OK
    print(("PASS " if cond else "FAIL ") + name, flush=True)
    OK = OK and bool(cond)


full = "--full" in sys.argv
for name, (p, m, opts) in FM.FAMILIES.items():
    N = FM.n_members(opts)
    if name in ("D27", "C27") or (N > 70000 and not full):
        continue
    fn = os.path.join(HERE, "data", f"scan_{name}.json")
    if not os.path.exists(fn):
        claim(f"[SCAN] {name}: stored result exists", False)
        continue
    st = json.load(open(fn))
    cnt, bs = {}, []
    for lo in range(0, N, SC.CHUNK):
        c, b = SC.work((name, lo, min(N, lo + SC.CHUNK)))
        for k, v in c.items():
            cnt[k] = cnt.get(k, 0) + v
        bs += b
    claim(f"[SCAN] {name}: {N} members, counts {cnt}, type (b) {len(bs)}",
          cnt == st["counts"] and sorted(bs)[:5000] == st["typeb_indices"])

# [R3]
r3 = open(os.path.join(HERE, "..", "..", "round3", "dichotomy", "scan_base3.out")).read()
for a in (2, 4, 5, 7, 8, 10, 11, 13):
    mm = re.findall(rf"B\(Q=27, a={a}\): \{{'CERT': (\d+)", r3)
    st = json.load(open(os.path.join(HERE, "data", f"scan_B27_a{a}.json")))
    claim(f"[R3] B27 a={a}: CERT count {st['counts'].get('a')} equals round 3 ({mm[-1] if mm else None})",
          mm and int(mm[-1]) == st["counts"].get("a"))
mm = re.findall(r"C9 \(8\^6 systems\): \{'CERT': (\d+)", r3)
st = json.load(open(os.path.join(HERE, "data", "scan_C9.json")))
claim(f"[R3] C9: CERT count {st['counts'].get('a')} equals round 3 ({mm[-1]})", int(mm[-1]) == st["counts"]["a"])
for m, obst in ((3, 10), (4, 172), (5, 48880)):
    st = json.load(open(os.path.join(HERE, "data", f"scan_S3_m{m}.json")))
    claim(f"[R3] S-family m={m}: {st['counts'].get('c')} type (c) = round-3 OBST count {obst}, "
          f"no type (b)", st["counts"].get("c") == obst and st["typeb"] == 0)

# [PROOF]
nobj = 0
bad = 0
for fn in sorted(glob.glob(os.path.join(HERE, "data", "*_H.json"))):
    for P in json.load(open(fn)):
        nobj += 1
        try:
            VH.verify(P, quiet=True)
        except AssertionError:
            bad += 1
for fn in sorted(glob.glob(os.path.join(HERE, "data", "mods_*.json"))):
    for name, R in json.load(open(fn)).items():
        for rec in R["typeb"]:
            nobj += 1
            try:
                VH.verify(rec["proof"], quiet=True)
                assert [c[0] for c in rec["proof"]["cycles"]] == rec["cycles"]
            except AssertionError:
                bad += 1
claim(f"[PROOF] {nobj} stored Theorem-H proof objects re-verified independently, failures {bad}",
      nobj > 0 and bad == 0)

# [BRUTE]
for a in (3, 5):
    files = glob.glob(os.path.join(HERE, "out", "brute", f"a{a}_m6_*.txt"))
    tot = dict(nb=0, nH=0, nunc=0)
    done = 0
    for f in files:
        for line in open(f):
            if line.startswith("DONE"):
                done += 1
                for k in tot:
                    tot[k] += int(re.search(rf" {k}=(\d+)", line).group(1))
    claim(f"[BRUTE] S-family a={a}, m=6: {done}/4096 slices, members with an isolated expanding "
          f"SCC {tot['nb']}, of which free of type (c) {tot['nH']}, near-zero verdicts {tot['nunc']}",
          done == 4096 and tot["nH"] == 0 and tot["nunc"] == 0)
mn3 = min(abs(A * math.log(3) - B * math.log(2)) for A in range(1, 33) for B in range(0, 65))
mn5 = min(abs(A * math.log(5) - B * math.log(2)) for A in range(1, 33) for B in range(0, 65))
claim(f"[BRUTE] separation: min |A log3 - B log2| = {mn3:.4f}, min |A log5 - B log2| = {mn5:.4f}",
      mn3 > 0.013 and mn5 > 0.02)
print("ALL PASS" if OK else "SOME CHECK FAILED")
sys.exit(0 if OK else 1)
