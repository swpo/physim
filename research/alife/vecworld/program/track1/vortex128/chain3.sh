#!/bin/bash
# Extras: 64^2 members 4..7 of ensemble(8, seed 0) at both mutation rates (per-area mut_dt 200, per-box mut_dt 50),
# then the 128^2 main runs resumed from tick 440 to tick 600 (t 3000).
export OMP_NUM_THREADS=1 XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"
PY="taskset -c 2 /home/user/evalwork/vecworld/vw1/.venv/bin/python -B run.py"
cd /home/user/evalwork/vecworld/program/track1/vortex128
for arm in sel neu; do ( time $PY area64x $arm 4 500 0 200 4 area64x ) >> results/area64x_$arm.log 2>&1 || exit 1; done
for arm in sel neu; do ( time $PY area64x $arm 4 500 0 50 4 box64x ) >> results/box64x_$arm.log 2>&1 || exit 1; done
for arm in sel neu; do ( time $PY main $arm 6 600 2 ) >> results/main128_$arm.log 2>&1 || exit 1; done
echo chain3 done
