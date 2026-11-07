#!/bin/bash
# Oracle branches from the 128^2 snapshots (ticks 100, 200, 300, 400): R = 3 fresh-noise replicates x 32 ticks.
export OMP_NUM_THREADS=1 XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"
PY="taskset -c 2 /home/user/evalwork/vecworld/vw1/.venv/bin/python -B run.py"
cd /home/user/evalwork/vecworld/program/track1/vortex128
for arm in sel neu; do ( time $PY branch $arm 3 32 ) >> results/branch128_$arm.log 2>&1 || exit 1; done
echo chain2 done
