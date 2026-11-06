#!/bin/bash
cd /home/user/evalwork/vecworld/vw1/fresh/inputs/scripts
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"
PY="taskset -c 2 /home/user/evalwork/vecworld/vw1/.venv/bin/python -B"
echo "restart $(date)" >> ../results/visibility.log
$PY visibility.py 0 32 6 >> ../results/visibility.log 2>&1; echo "EXIT $?" >> ../results/visibility.log
