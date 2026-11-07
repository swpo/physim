#!/bin/bash
# After the main-arm rerun (level 2 v2): input probes, analysis, figure, tests. Core 3, one process at a time.
cd /home/user/evalwork/vecworld/program/track1/membrane_world
export OMP_NUM_THREADS=1 XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"
PY="taskset -c 3 /home/user/evalwork/vecworld/vw1/.venv/bin/python -B"
$PY probe_input.py 12 0.05 -0.03 5 30 > results/probe_input.log 2>&1 && echo "probe ok" || echo "probe FAILED"
$PY probe_input.py 16 0.03 -0.03 20 40 _long > results/probe_input_long.log 2>&1 && echo "probe long ok" || echo "probe long FAILED"
$PY analyse.py > results/analyse.log 2>&1 && echo "analyse ok" || echo "analyse FAILED"
$PY figure.py > results/figure.log 2>&1 && echo "figure ok" || echo "figure FAILED"
$PY -m pytest -q -p no:cacheprovider test_membrane.py > results/tests.log 2>&1 && echo "tests ok" || echo "tests FAILED"
echo "checks2 done"
