#!/bin/sh
# exhaustive S-family scans at m = 6 (2^32 subsets each), 4096 slices, 10 in parallel
cd "$(dirname "$0")"
for a in 3 5; do
  seq 0 4095 | xargs -P 10 -I{} sh -c "nice ./sbrute $a 1 6 {} 4096 > out/brute/a${a}_m6_{}.txt"
done
