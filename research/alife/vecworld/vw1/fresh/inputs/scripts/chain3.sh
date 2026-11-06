#!/bin/bash
# re-run steering (same layout and keys: must reproduce steer.json numbers exactly) with the clean
# video-run selection, then the steer video, the visibility figure check and summary.json
cd /home/user/evalwork/vecworld/vw1/fresh/inputs/scripts
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"
PY="taskset -c 2 /home/user/evalwork/vecworld/vw1/.venv/bin/python -B"
cp ../results/steer.json ../results/steer_run1.json
$PY steer.py 40 16 > ../results/steer_rerun.log 2>&1; echo "EXIT $?" >> ../results/steer_rerun.log
$PY render_steer.py > ../results/render_steer.log 2>&1; echo "EXIT $?" >> ../results/render_steer.log
$PY make_summary.py > ../results/make_summary.log 2>&1; echo "EXIT $?" >> ../results/make_summary.log
