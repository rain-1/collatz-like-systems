"""m3_d_s7: partial theorem (descent-tree exceptional set) + up-run witness.
Exit 0 iff the recorded certificate in partial_certs.json is reproduced exactly."""
from _partial_check import run

run("m3_d_s7", lambda K: 3**K - 1, range(1, 41), lambda K: 2*K)
