#!/bin/bash
# profile2 feasibility, candidate F: the automaton in float32 (what an agent's own simulator may use; the hidden world
# stays float64). Run after run_f.sh and run_g.sh, from this folder: bash run_f32.sh
set -u
cd "$(dirname "$0")"
PY=/home/user/evalwork/vecworld/vw1/.venv/bin/python
CORES=${CORES:-0,1}
export XLA_FLAGS="--xla_cpu_multi_thread_eigen=true intra_op_parallelism_threads=2"
run() {
  local name=$1; shift
  echo "$(date -u +%H:%M:%S) start $name (cores $CORES, load $(cut -d' ' -f1-3 /proc/loadavg))" >> raw/f_log.txt
  taskset -c "$CORES" "$PY" -I -B f_time.py "$@" --out "raw/$name.json" > "raw/$name.stdout" 2>&1
  echo "$(date -u +%H:%M:%S) done  $name exit $?" >> raw/f_log.txt
}
run f_sim_B1_f32 sim --B 1 --f32 --start-reps 0
run f_sim_B16_f32 sim --B 16 --f32 --start-reps 0
run f_sim_B64_f32 sim --B 64 --f32 --start-reps 0
