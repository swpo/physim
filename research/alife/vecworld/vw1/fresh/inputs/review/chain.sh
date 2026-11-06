#!/bin/bash
cd /home/user/evalwork/vecworld/vw1/fresh/inputs/review
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"
PY="taskset -c 2 /home/user/evalwork/vecworld/vw1/.venv/bin/python -B"
( time $PY vis_rerun.py 13 14 6 ) > vis_rerun.log 2>&1; echo "EXIT $?" >> vis_rerun.log
( time $PY states_rerun.py 40 60 ) > states_rerun.log 2>&1; echo "EXIT $?" >> states_rerun.log
