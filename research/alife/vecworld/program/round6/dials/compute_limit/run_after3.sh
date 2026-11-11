#!/bin/bash
# After run_after2.sh: one more 64 px pool (also the re-check of the tracker overflow counters, now saved apart)
# and a second 128 px pool (8 members in all for the transfer table at a 4x-16x area ratio).
S=$1
PY="/home/user/evalwork/vecworld/vw1/.venv/bin/python -B"
HERE=$(cd "$(dirname "$0")" && pwd)
while ! grep -q ALL2_DONE $S/after2.log; do sleep 10; done
run() { # H B T seed
  f=$S/b$1_s$4.npz
  [ -f "$f" ] || OMP_NUM_THREADS=1 nice -n 10 $PY $HERE/run_boxes.py --H $1 --B $2 --T $3 --seed $4 --out $f | grep -v rollout
}
run 64 4 260 5
echo B64_S5_DONE
run 128 4 260 2
echo ALL3_DONE
