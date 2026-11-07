#!/bin/bash
# 128^2 main runs (6 seeds, ensemble seed 2, to tick 440 = t 2200), then the 64^2 per-area mutation runs.
export OMP_NUM_THREADS=1 XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"
PY="taskset -c 2 /home/user/evalwork/vecworld/vw1/.venv/bin/python -B run.py"
cd /home/user/evalwork/vecworld/program/track1/vortex128
for arm in sel neu; do ( time $PY main $arm 6 440 2 ) >> results/main128_$arm.log 2>&1 || exit 1; done
for arm in sel neu; do ( time $PY area64 $arm 4 500 0 200 ) >> results/area64_$arm.log 2>&1 || exit 1; done
echo chain1 done
