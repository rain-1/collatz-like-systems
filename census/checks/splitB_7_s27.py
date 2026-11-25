"""Check for splitB_7_s27: FATE by exact simulation (tier 0); GLOBAL via the descent
lemma (every odd image is divisible by 4) plus exhaustive cycle list on [1,7]."""
import sys
from _split_common import check_fate, check_descent
check_fate("splitB_7_s27", 13, 4)
check_descent("splitB_7_s27", 7, 1, 3)
print("PASS")
sys.exit(0)
