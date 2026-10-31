#!/bin/bash
# Score queue, one process at a time. usage: q2.sh "cmd world level" ...   (cmd: score | null | det)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
PY=/home/user/physim/.venv/bin/python
S=/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/noise_intensity/scripts/nsweep.py
cd /tmp
for job in "$@"; do
  set -- $job
  echo "== $job $(date +%T)"
  $PY -W ignore $S $1 --world $2 --level $3
done
echo QDONE
