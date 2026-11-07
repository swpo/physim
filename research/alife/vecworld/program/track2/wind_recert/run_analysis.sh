#!/bin/bash
# All analyses in sequence on core 0 after run_sims.sh; logs in results/raw/an_*.log.
# usage: run_analysis.sh [jax]   (jax: only the optional JAX-predictor closure runs of F and M)
cd /home/user/evalwork/vecworld/program/track2/wind_recert || exit 1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
       XLA_FLAGS="--xla_cpu_multi_thread_eigen=false intra_op_parallelism_threads=1"
PY="taskset -c 0 /home/user/evalwork/vecworld/vw1/.venv/bin/python -B"
step() { echo "start $* $(date +%T)"; $PY "$@" > "results/raw/an_$(echo "$*" | tr ' -' '__').log" 2>&1 || { echo "FAILED $*"; exit 1; }; echo "done $* $(date +%T)"; }
if [ "$1" = jax ]; then
  for s in F M; do for v in objects coarse; do step closure_run.py $s $v --jax; done; done
else
  step viability_stats.py
  for s in F M P; do for v in coarse objects; do step closure_run.py $s $v; done; done
fi
step make_summary.py
