#!/bin/bash
# Pools of level-2 trajectories at three box sides (CPU, one process at a time, restart-safe: skips existing files).
# usage: run_pools.sh <scratch dir>
S=$1
PY="/home/user/evalwork/vecworld/vw1/.venv/bin/python -B"
HERE=$(cd "$(dirname "$0")" && pwd)
run() { # H B T seed
  f=$S/b$1_s$4.npz
  [ -f "$f" ] || OMP_NUM_THREADS=1 nice -n 10 $PY $HERE/run_boxes.py --H $1 --B $2 --T $3 --seed $4 --out $f | grep -v rollout
}
run 64 4 260 2
run 32 20 380 2
run 64 4 260 3
run 48 10 320 1
run 64 4 260 4
run 32 20 380 3
run 48 10 320 2
echo POOLS_DONE
