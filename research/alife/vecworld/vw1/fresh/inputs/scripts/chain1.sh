#!/bin/bash
# timing probes, steering, steer video (core 2, one process at a time)
cd /home/user/evalwork/vecworld/vw1/fresh/inputs/scripts
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"
PY="taskset -c 2 /home/user/evalwork/vecworld/vw1/.venv/bin/python -B"
$PY sens_timing.py 1 8 > ../results/sens_timing_N1.log 2>&1; echo "EXIT $?" >> ../results/sens_timing_N1.log
$PY sens_timing.py 4 8 > ../results/sens_timing_N4.log 2>&1; echo "EXIT $?" >> ../results/sens_timing_N4.log
$PY steer.py 40 16 > ../results/steer.log 2>&1; echo "EXIT $?" >> ../results/steer.log
$PY render_steer.py > ../results/render_steer.log 2>&1; echo "EXIT $?" >> ../results/render_steer.log
