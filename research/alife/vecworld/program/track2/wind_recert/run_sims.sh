#!/bin/bash
# All simulations in sequence on core 0 (one heavy process at a time); logs in results/raw/*.log.
cd /home/user/evalwork/vecworld/program/track2/wind_recert || exit 1
export OMP_NUM_THREADS=1 XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"
PY="taskset -c 0 /home/user/evalwork/vecworld/vw1/.venv/bin/python -B"
for mode in viab oracle free prog; do
  if [ "$mode" = viab ] && [ -f results/raw/viab.npz ]; then continue; fi
  if [ "$mode" = oracle ] && [ -f results/raw/oracle.npz ]; then continue; fi
  $PY sim.py $mode > results/raw/sim_$mode.log 2>&1 || { echo "FAILED $mode"; exit 1; }
  echo "done $mode $(date +%T)"
done
