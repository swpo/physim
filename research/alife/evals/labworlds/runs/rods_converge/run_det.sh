#!/bin/bash
# deterministic screens, one process at a time
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 TIMEFORMAT='%U user %S sys %R wall'
PY=/home/user/physim/.venv/bin/python
for c in spread time "space --dt 0.025"; do
  { echo "det $c"; time $PY det.py $c > "out/det_${c%% *}.log" 2>&1; } 2>> out/cpu.log
done
