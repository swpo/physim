#!/bin/bash
# one heavy process at a time; OMP 1 thread; labkit FFT workers set to 1 inside rotdiv.py
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd "$(dirname "$0")"
PY=/home/user/physim/.venv/bin/python
for job in "5 0 0 base_s5" "6 0 0 base_s6" "5 30 0 r30_s5" "6 30 0 r30_s6" "5 45 0 r45_s5" "6 45 0 r45_s6" "5 0 1 iso_s5" "6 0 1 iso_s6"; do
  set -- $job
  [ -f out/$4.json ] && continue
  $PY rotdiv.py $1 $2 $3 192 6000 $4 >> out/queue1.log 2>&1
done
echo QUEUE1_DONE >> out/queue1.log
