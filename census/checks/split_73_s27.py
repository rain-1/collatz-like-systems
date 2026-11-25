"""Check for split_73_s27: FATE by exact simulation (tier 0); GLOBAL via the descent
lemma (every odd image is divisible by 4) plus exhaustive cycle list on [1,73]."""
import sys
from _split_common import check_fate, check_descent
check_fate("split_73_s27", 8, 12)
check_descent("split_73_s27", 73, 3, 1)
print("PASS")
sys.exit(0)
