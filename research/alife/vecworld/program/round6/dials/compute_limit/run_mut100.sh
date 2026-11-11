#!/bin/bash
# Pools at mut128 = 100 (declared, public): 64 px 12 members and 128 px 4 members, 300 ticks; then check_mut100.py.
# Waits for the full analysis first (one process at a time).
S=$1
PY="/home/user/evalwork/vecworld/vw1/.venv/bin/python -B"
HERE=$(cd "$(dirname "$0")" && pwd)
while ! grep -q "^EXIT" $S/analyse_full.log; do sleep 5; done
run() { # H B T seed
  f=$S/m100_b$1_s$4.npz
  [ -f "$f" ] || OMP_NUM_THREADS=1 nice -n 10 $PY $HERE/run_boxes.py --H $1 --B $2 --T $3 --seed $4 --mut128 100 --out $f | grep -v rollout
}
run 64 12 300 11
echo M100_64_DONE
run 128 4 300 11
echo M100_ALL_DONE
