#!/bin/bash
# Ensembles one at a time: each argument is program:dt:n:seed. Saved arms are skipped on re-run.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 TIMEFORMAT='%U user %S sys %R wall'
PY=/home/user/physim/.venv/bin/python
for spec in "$@"; do
  IFS=: read prog dt n seed <<< "$spec"
  { echo "ens $spec" >&2; time $PY ens.py --program "$prog" --dt "$dt" --n "$n" --seed "$seed" >> out/ens.log 2>&1; } 2>> out/cpu.log
done
echo "batch done: $*" >> out/ens.log
