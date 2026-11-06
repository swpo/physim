#!/bin/bash
# (a)+(d) visibility over 32 states, its analysis, then (c) sensitivity (core 2, one process at a time)
cd /home/user/evalwork/vecworld/vw1/fresh/inputs/scripts
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"
PY="taskset -c 2 /home/user/evalwork/vecworld/vw1/.venv/bin/python -B"
$PY visibility.py 0 32 6 >> ../results/visibility.log 2>&1; echo "EXIT $?" >> ../results/visibility.log
$PY analyze_vis.py > ../results/analyze_vis.log 2>&1; echo "EXIT $?" >> ../results/analyze_vis.log
$PY sensitivity.py 0,1,2 > ../results/sensitivity.log 2>&1; echo "EXIT $?" >> ../results/sensitivity.log
$PY plot_sensitivity.py 0 > ../results/plot_sensitivity.log 2>&1; echo "EXIT $?" >> ../results/plot_sensitivity.log
