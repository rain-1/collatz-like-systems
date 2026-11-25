#!/usr/bin/env python3
"""Exact checks for a conditional theorem about the 1932 Collatz orbit of 8.

This is NOT a proof of infinitude. It proves that the still-unproved
condition c_k <= 2k/5 for all k >= 500 is sufficient.
"""

from argparse import ArgumentParser


def G(n: int) -> int:
    q, r = divmod(n, 3)
    return (2*q, 4*q + 1, 4*q + 3)[r]


def trajectory_stats(start: int, steps: int):
    n, Q, D, S, zeros = start, 1, 1, 0, 0
    first_drift_failure = None
    first_carry_failure = None
    worst_density = (-1, None, None)
    for k in range(1, steps + 1):
        r = n % 3
        q, s = ((2, 0), (4, -1), (4, 1))[r]
        zeros += (r == 0)
        S = q*S + s*D
        Q *= q
        D *= 3
        n = (q*n + s)//3
        assert n*D == start*Q + S
        if first_drift_failure is None and Q <= D:
            first_drift_failure = (k, n)
        if first_carry_failure is None and S <= 0:
            first_carry_failure = (k, n)
        if k >= 500 and 5*zeros > 2*k:
            worst_density = (zeros/k, k, zeros)
    return dict(n=n, Q=Q, D=D, S=S, zeros=zeros,
                first_drift_failure=first_drift_failure,
                first_carry_failure=first_carry_failure,
                beyond_40_percent=worst_density)


def verify_finite_part():
    n, Q, D, S, zeros = 8, 1, 1, 0, 0
    for k in range(1, 501):
        r = n % 3
        q, s = ((2, 0), (4, -1), (4, 1))[r]
        zeros += (r == 0)
        S = q*S + s*D
        Q *= q
        D *= 3
        n = (q*n+s)//3
        assert n*D == 8*Q+S
        assert Q > D and S > 0
    assert zeros == 168
    assert 5*S > Q  # R_500 > 1/5
    print('Verified exactly: Q_k > 3^k and S_k > 0 for 1<=k<=500')
    print('c_500 =', zeros)
    print('R_500 =', S/Q)
    print('The remaining hypothesis c_k<=2k/5 for ALL k>=500 is unproved.')


if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('--steps', type=int, default=10000)
    args = p.parse_args()
    verify_finite_part()
    for start in [35, 89]:
        x = trajectory_stats(start, 20)
        print('Start', start, 'drift failure', x['first_drift_failure'],
              'carry failure', x['first_carry_failure'])
    x = trajectory_stats(8, args.steps)
    print('Orbit 8, steps', args.steps, 'zeros', x['zeros'],
          'density', x['zeros']/args.steps)
    print('Observed failures (finite check only):',
          x['first_drift_failure'], x['first_carry_failure'])
