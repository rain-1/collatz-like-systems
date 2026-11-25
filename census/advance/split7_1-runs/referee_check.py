#!/usr/bin/env python3
"""Referee (round 1) independent checks for CLS-053 (census/advance/split7_1-runs).

Written independently of check.py / range.cpp:
 (1) referee_range.cpp: a different residue-tree implementation (greedy raw T steps,
     root split at 2^14) certifying every 1 <= n < 2^50 drops below itself.
 (2) Part 2 redone with decimal (250 digits, correctly rounded ln, every decision checked with a margin of
     at least 1e-30 relative) and continued-fraction convergents of log_2 7 with the
     classical best-approximation lemma (|K a - L| >= |q_k a - p_k| for 0 < K < q_{k+1}),
     instead of the prover's one-sided Stern-Brocot lemma.
 (3) brute-force count of never-dropping starts in [2^j, 2^(j+1)) for j <= 26 (C).
Exit 0 iff all pass.
"""
import os, subprocess, sys, tempfile, shutil
import decimal
from decimal import Decimal as D, ROUND_FLOOR, ROUND_CEILING
decimal.getcontext().prec = 250


class _MP:
    """tiny shim: decimal (prec 250, correctly rounded ln) in place of mpmath"""
    class mp:
        dps = 250
    @staticmethod
    def mpf(x):
        return D(x)
    @staticmethod
    def log(x, base=None):
        x = D(x)
        return x.ln() if base is None else x.ln() / D(base).ln()
    @staticmethod
    def floor(x):
        return D(x).to_integral_value(rounding=ROUND_FLOOR)
    @staticmethod
    def ceil(x):
        return D(x).to_integral_value(rounding=ROUND_CEILING)


mp = _MP

HERE = os.path.dirname(os.path.abspath(__file__))
FAIL = []


def ok(c, m):
    print(("  PASS " if c else "  FAIL ") + m)
    if not c:
        FAIL.append(m)


def T(n):
    return n // 2 if n % 2 == 0 else (7 * n + 1 if n % 4 == 1 else n + 1)


def margin_lt(a, b, what):
    # decide a < b only with a clear margin
    assert b - a > mp.mpf(10) ** -30 * (abs(a) + abs(b) + 1), ("too close", what, a, b)
    return True


def part1():
    print("Referee part 1: independent residue tree to 2^50")
    ok([T(1), T(8), T(4), T(2)] == [8, 4, 2, 1], "(1 8 4 2) is a cycle")
    cxx = shutil.which("g++") or shutil.which("clang++")
    with tempfile.TemporaryDirectory() as td:
        exe = os.path.join(td, "rr")
        subprocess.run([cxx, "-O3", "-std=c++17", "-pthread", os.path.join(HERE, "referee_range.cpp"), "-o", exe], check=True)
        for b in (20, 50):
            res = subprocess.run([exe, str(b)], capture_output=True, text=True)
            print("   ", res.stdout.strip(), res.stderr.strip())
            ok(res.returncode == 0 and res.stdout.strip().endswith("OK"), "independent tree certifies 1 <= n < 2^%d" % b)
        # cross-check the small range by brute force
        good = True
        for n in range(2, 1 << 18):
            x, s = n, 0
            while x >= n:
                x = T(x); s += 1
                if s > 10 ** 5:
                    good = False; break
        ok(good, "brute force: every 2 <= n < 2^18 drops below itself")
        # part 3 brute force
        src = os.path.join(td, "nd.c")
        with open(src, "w") as f:
            f.write(r'''
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
int main(int c,char**v){int J=atoi(v[1]);
for(int j=0;j<=J;j++){uint64_t cnt=0;for(uint64_t n=1ULL<<j;n<(2ULL<<j);n++){
 unsigned __int128 x=n;int dropped=0;for(long k=0;k<20000;k++){
  if(x&1){ if(x>((unsigned __int128)1<<120)) break; x=((x&3)==1)?7*x+1:x+1;} else x>>=1;
  if(x<n){dropped=1;break;}}
 cnt+=!dropped;}
 printf("%d %llu\n",j,(unsigned long long)cnt);}return 0;}''')
        subprocess.run(["gcc", "-O2", src, "-o", os.path.join(td, "nd")], check=True)
        out = subprocess.run([os.path.join(td, "nd"), "26"], capture_output=True, text=True).stdout.split("\n")
        good = True
        for line in out:
            if not line.strip():
                continue
            j, cnt = map(int, line.split())
            good &= cnt <= 2 * mp.mpf(27) ** j / mp.mpf(16) ** j
            if j in (10, 20, 26):
                print("    j=%d never-dropping count %d  vs bound %.1f" % (j, cnt, float(2 * (27 / 16) ** j)))
        ok(good and len([l for l in out if l.strip()]) == 27,
           "brute force (non-drop = no drop in 2e4 steps, conservative): count <= 2(27/16)^j, j <= 26")


def convergents(alpha, upto):
    """continued fraction convergents p_k/q_k of alpha (needs alpha known far beyond q^2)."""
    a = []
    x = alpha
    p0, q0, p1, q1 = 1, 0, int(mp.floor(x)), 1
    res = [(p1, q1)]
    x = x - mp.floor(x)
    while q1 < upto:
        x = 1 / x
        ak = int(mp.floor(x))
        # guard: floor must be unambiguous
        assert x - ak > mp.mpf(10) ** -100 and ak + 1 - x > mp.mpf(10) ** -100
        x -= ak
        p0, q0, p1, q1 = p1, q1, ak * p1 + p0, ak * q1 + q0
        res.append((p1, q1))
    return res


def part2():
    print("Referee part 2: Laurent Cor. 2 + continued-fraction reduction, r = 1..69")
    l2, l7 = mp.log(2), mp.log(7)
    alpha = l7 / l2
    rho = l7 / mp.log(4)
    l74 = mp.log(mp.mpf(7) / 4)
    ok(l7 < mp.mpf('1.95'), "log 7 < 1.95 = log A2 ; log A1 = 1 >= max(h(2), log 2, 1)")
    ok(l74 / mp.log(mp.mpf(8) / 7) < mp.mpf('4.2'), "log(7/4)/log(8/7) < 4.2")
    m0 = mp.mpf(2) ** 50
    ok(mp.mpf(1) / 3 + (7 * m0 + 1) / (7 * m0 - 7) < mp.mpf('1.34'), "1/3 + c < 1.34")
    conv = convergents(alpha, 10 ** 40)
    C = mp.mpf('1.34')

    def kmax(logbound, r):
        return mp.mpf('5.2') * (logbound - l2) * rho ** r / l74 + 1

    allok = True
    for r in range(1, 71):
        # Laurent: mu < log(C r) + 25.2*1*1.95*max(log b' + 0.38, 10)^2,
        #   b' = L/1.95 + K <= (alpha K + 1)/1.95 + K
        def g(mu):
            K = kmax(mu + mp.mpf('1.1'), r)
            bp = (alpha * K + 1) / mp.mpf('1.95') + K
            lb = mp.log(bp) + mp.mpf('0.38')
            return mp.log(C * r) + mp.mpf('25.2') * mp.mpf('1.95') * max(lb, 10) ** 2, lb
        mu = mp.mpf(10) ** 7
        for _ in range(200):
            gv, lb = g(mu)
            new = gv * (1 + mp.mpf(10) ** -12) + 1
            if new >= mu:
                break
            mu = new
        gv, lb = g(mu)
        lmn_ok = gv < mu and lb > 10 and 2 * mp.mpf('25.2') * mp.mpf('1.95') * lb / mu < 1
        margin_lt(gv, mu, "g<mu")
        # reduction
        logb = mu + mp.mpf('1.1')
        M = None
        bits_hist = []
        for _ in range(10):
            K = kmax(logb, r)
            k = next(i for i in range(len(conv) - 1) if conv[i + 1][1] > K)
            p, q = conv[k]
            gap = abs(q * alpha - p)
            Mb = C * r / (l2 * gap)
            bits_hist.append(int(mp.ceil(mp.log(Mb, 2))))
            if Mb < m0 * (1 - mp.mpf(10) ** -20):
                M = Mb
                break
            nl = mp.log(3 * Mb + 1)
            if nl >= logb - mp.mpf(10) ** -20:
                break
            logb = nl
        passed = lmn_ok and M is not None
        if r <= 69:
            allok &= passed
        if r in (1, 50, 69, 70):
            print("    r=%d: mu1=%.1f, bit history %s -> %s" % (r, float(mu), bits_hist, "contradiction" if passed else "no contradiction"))
    ok(allok, "every r = 1..69 leads to m < 2^50 (contradiction with Theorem 1)")


if __name__ == "__main__":
    part1()
    part2()
    print("REFEREE CHECKS PASSED" if not FAIL else "REFEREE FAILED: %s" % FAIL)
    sys.exit(1 if FAIL else 0)
