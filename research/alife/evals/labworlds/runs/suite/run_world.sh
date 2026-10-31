#!/bin/bash
# One world's full suite (one heavy process), 8 members per control. usage: run_world.sh WORLD OUT
cd /tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/evalpilot/suite || exit 1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
P=/home/user/physim/.venv/bin/python
S=/home/user/swpo/residency-environments/scripts/physim/labworlds/labeval.py
start=$(date +%s)
$P $S run --world "$1" --out "$2" --members 8 > "$2_run.log" 2>&1 && echo "$1 OK" || echo "$1 FAILED"
echo "wall_s $(( $(date +%s) - start ))"
