#!/bin/bash
# repeated division to 12000 t: isotropic stencil first, then the standard stencil; one process at a time
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$(dirname "$0")"
PY=/home/user/physim/.venv/bin/python
for job in "5 0 1 iso12_s5" "6 0 1 iso12_s6" "5 0 0 base12_s5" "6 0 0 base12_s6"; do
  set -- $job
  [ -f out/$4.json ] && continue
  $PY rotdiv.py $1 $2 $3 192 12000 $4 >> out/queue2.log 2>&1
done
echo QUEUE2_DONE >> out/queue2.log
