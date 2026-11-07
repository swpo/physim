#!/bin/bash
# Sequential post-pilot checks on core 3 (one heavy process at a time).
cd /home/user/evalwork/vecworld/program/track1/membrane_world
export OMP_NUM_THREADS=1 XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"
PY="taskset -c 3 /home/user/evalwork/vecworld/vw1/.venv/bin/python -B"
$PY check_repro.py 0.5 5000 1 > results/repro_dt0.5.log 2>&1 && echo "repro0.5 ok" || echo "repro0.5 FAILED"
$PY check_repro.py 1.0 5000 1 > results/repro_dt1.log 2>&1 && echo "repro1 ok" || echo "repro1 FAILED"
$PY dtcheck_tick.py 6 > results/dtcheck_tick.log 2>&1 && echo "dtcheck ok" || echo "dtcheck FAILED"
$PY probe_input.py 12 0.05 -0.03 5 30 > results/probe_input.log 2>&1 && echo "probe ok" || echo "probe FAILED"
$PY -m pytest -q -p no:cacheprovider test_membrane.py > results/tests.log 2>&1 && echo "tests ok" || echo "tests FAILED"
echo "checks done"
