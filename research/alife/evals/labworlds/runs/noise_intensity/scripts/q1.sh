#!/bin/bash
# Behaviour screen, one process at a time: PM seed 0 at levels 0 (pipeline check), 0.01, 0.03, 0.1; FV seed 3 at 0.003, 0.01, 0.03, 0.1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
PY=/home/user/physim/.venv/bin/python
LPY=/home/user/physim/research/alife/.labenv/bin/python
D=/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/noise_intensity
S=$D/scripts/nsweep.py
cd /tmp
run() { $PY -W ignore $S behav --world $1 --level $2 --seed $3 && $LPY -W ignore $D/scripts/behav_analyse.py $D/out/behav/$1/L$2_s$3; }
for job in "$@"; do run $job; done
echo QDONE
