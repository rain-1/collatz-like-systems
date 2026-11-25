"""div235_7n1_s11: partial theorem (descent-tree exceptional set) + up-run witness.
Exit 0 iff the recorded certificate in partial_certs.json is reproduced exactly."""
from _partial_check import run

run("div235_7n1_s11", lambda K: 30**K - 1, range(1, 25), lambda K: 3*(K - 1))
