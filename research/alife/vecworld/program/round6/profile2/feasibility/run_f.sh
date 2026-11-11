#!/bin/bash
# profile2 feasibility, candidate F (foundry hidden weights): every measurement of f_time.py, one process each, on 2 cores.
# Run from this folder:  bash run_f.sh  (writes raw/f_*.json and raw/f_log.txt)
set -u
cd "$(dirname "$0")"
PY=/home/user/evalwork/vecworld/vw1/.venv/bin/python
CORES=${CORES:-0,1}
export XLA_FLAGS="--xla_cpu_multi_thread_eigen=true intra_op_parallelism_threads=2"
mkdir -p raw
run() {
  local name=$1; shift
  echo "$(date -u +%H:%M:%S) start $name (cores $CORES, load $(cut -d' ' -f1-3 /proc/loadavg))" >> raw/f_log.txt
  taskset -c "$CORES" "$PY" -I -B f_time.py "$@" --out "raw/$name.json" > "raw/$name.stdout" 2>&1
  echo "$(date -u +%H:%M:%S) done  $name exit $?" >> raw/f_log.txt
}
run f_sim_B1 sim --B 1
run f_sim_B16 sim --B 16
run f_sim_B256 sim --B 256 --start-reps 0
run f_net_C48_b256 net --C 48 --batch 256
run f_net_C24_b256 net --C 24 --batch 256
run f_net_C48_b64 net --C 48 --batch 64
run f_plug_m256 plug --m 256
run f_fit_T32 fit --T 32
run f_sim_B64 sim --B 64 --start-reps 1
run f_fit_T48 fit --T 48 --reps 1
