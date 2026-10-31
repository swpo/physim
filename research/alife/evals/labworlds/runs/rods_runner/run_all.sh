#!/bin/bash
# One process at a time; every arm saves its own npz and is skipped on re-run.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 TIMEFORMAT='%U user %S sys %R wall'
PY=/home/user/physim/.venv/bin/python
ARMS="truth:native pred:native pred:mar0 pred:passive pred:kappa0 pred:chis0"
for prog in "$@"; do
  extra=""
  [ "$prog" = "surf" ] && extra="pred:dthalf"
  { echo "run $prog"; time $PY rods_runner.py run --program "$prog" --arms $ARMS $extra >> out/run.log 2>&1; } 2>> out/cpu.log
done
