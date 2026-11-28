#!/bin/bash
# Runs every family scan of families.FAMILIES in parallel (nice), writing out/fam_<name>.txt
cd "$(dirname "$0")"
PY=/home/riv/Code/collatz/census/round4/wpotential/.venv/bin/python
for line in $($PY -c "import families as F; print(' '.join(f'{n}:{m}:{c}' for n,m,c in F.FAMILIES))"); do
  IFS=: read name mode cnt <<< "$line"
  ( $PY -c "import families as F; Q,o=F.family('$name'); print(F.spec_text(Q,o,$mode,$cnt,12345),end='')" \
     | nice -n 15 ./famscan printcert > out/fam_$name.txt ) &
done
wait
