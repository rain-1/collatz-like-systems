"""Run every check in this folder; exit 0 iff all pass.  Total runtime about 1-2 minutes.

check_onept.py          Theorem A (F_2, g=1+t, all h)
check_snapptracy.py     Theorem B (degree-1 g over F_2, F_3, F_4, F_5)
check_frobenius.py      Theorem C, Proposition C', Corollary C1
check_divergence.py     all divergence certificates (D0-D6)
check_classification.py principles P1, P2, the degenerate lemma
"""
import subprocess, sys, os, time
here = os.path.dirname(os.path.abspath(__file__))
bad = 0
for name in ['check_onept.py', 'check_snapptracy.py', 'check_frobenius.py',
             'check_divergence.py', 'check_classification.py']:
    t = time.time()
    r = subprocess.run([sys.executable, os.path.join(here, name)], capture_output=True, text=True)
    print('%-26s exit %d  (%.0fs)  %s' % (name, r.returncode, time.time() - t,
                                         r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ''))
    bad += r.returncode != 0
sys.exit(1 if bad else 0)
