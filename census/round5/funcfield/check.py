"""Run every exact check of this folder; exits 0 iff all pass (about 6 minutes)."""
import subprocess, sys
ok = True
for s in ['check_frobenius_cycles.py', 'check_theoremA.py', 'check_integer_catalan.py', 'check_s2c.py',
          'check_cumulative.py', 'check_topdigits.py']:
    r = subprocess.run([sys.executable, s])
    print(s, 'exit', r.returncode)
    ok = ok and r.returncode == 0
# horizon lemma: analyse.py reports in-horizon mismatches; require 0
import analyse, io, contextlib
for n in ['A3', 'B3', 'G3', 'S2', 'S2c', 'Q4', 'Q4b']:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        analyse.table(n)
    line = [l for l in buf.getvalue().split('\n') if 'in-horizon' in l][0]
    good = line.strip().endswith(': 0')
    print(n, line.strip())
    ok = ok and good
sys.exit(0 if ok else 1)
