"""Run every check script of the divergence lens (default fast mode).  Exit 0 iff all pass.

check_theorem1_suffix.py   Theorem 1 (suffix maps)                 ~1 s
check_race_s21.py          race_s21 + Theorem 2 application        ~2 s
check_fx_5n1.py            fx10_64_s7, fx26_32_s7 (Lemmas A,F,I,P)  ~1 s
check_perm12_s7.py         perm12_s7                               ~1 s
check_c62_64_s27.py        c62_64_s27                              ~1 s
check_theorem4_precision.py Theorem 4 table, m = 5                 ~30 s
                           (python3 check_theorem4_precision.py --m 6,7,8 : ~1 h)
check_theorem5_precision3.py Theorem 5 table i <= 10, swT2_8_s8     ~60 s
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = ["check_theorem1_suffix.py", "check_race_s21.py", "check_fx_5n1.py",
           "check_perm12_s7.py", "check_c62_64_s27.py", "check_theorem4_precision.py",
           "check_theorem5_precision3.py"]


def main():
    bad = []
    for s in SCRIPTS:
        r = subprocess.run([sys.executable, os.path.join(HERE, s)], capture_output=True, text=True)
        status = "ok" if r.returncode == 0 else "FAIL"
        print(f"{s:34s} {status}")
        if r.returncode:
            print(r.stdout[-2000:], r.stderr[-2000:])
            bad.append(s)
    if bad:
        sys.exit(1)
    print("all checks passed")


if __name__ == "__main__":
    main()
