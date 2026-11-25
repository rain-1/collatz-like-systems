"""div23_7n1_s5: partial theorem (descent-tree exceptional set) + up-run witness.
Exit 0 iff the recorded certificate in partial_certs.json is reproduced exactly."""
from _partial_check import run

run("div23_7n1_s5", lambda K: 6**K - 1, range(1, 33), lambda K: 3*(K - 1))
