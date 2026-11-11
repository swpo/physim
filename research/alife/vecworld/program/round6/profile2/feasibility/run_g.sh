#!/bin/bash
# profile2 feasibility, candidate G (gliders, hidden stress conversion): every measurement of g_time.py, one process
# each, on 2 cores. Run from this folder:  bash run_g.sh  (writes raw/g_*.json and raw/g_log.txt)
set -u
cd "$(dirname "$0")"
PY=/home/user/evalwork/vecworld/vw1/.venv/bin/python
CORES=${CORES:-0,1}
export XLA_FLAGS="--xla_cpu_multi_thread_eigen=true intra_op_parallelism_threads=2"
mkdir -p raw
run() {
  local name=$1; shift
  echo "$(date -u +%H:%M:%S) start $name (cores $CORES, load $(cut -d' ' -f1-3 /proc/loadavg))" >> raw/g_log.txt
  taskset -c "$CORES" "$PY" -I -B g_time.py "$@" --out "raw/$name.json" > "raw/$name.stdout" 2>&1
  echo "$(date -u +%H:%M:%S) done  $name exit $?" >> raw/g_log.txt
}
run g_sim_B1 sim --B 1 --T 16
run g_net_C48_b128 net --C 48 --batch 128
run g_net_C24_b128 net --C 24 --batch 128
run g_sim_B16 sim --B 16 --T 16 --start-reps 1
run g_sim_B64 sim --B 64 --T 4 --start-reps 0
# B = 256 only if B = 64 peaked under 2.5 GB (memory grows about linearly in B; this machine is shared)
if python3 -c "import json,sys; sys.exit(0 if json.load(open('raw/g_sim_B64.json'))['rss_mb_peak'] < 2500 else 1)" 2>/dev/null; then
  run g_sim_B256 sim --B 256 --T 2 --start-reps 0
else
  echo "$(date -u +%H:%M:%S) skipped g_sim_B256 (B = 64 peak memory >= 2.5 GB or missing)" >> raw/g_log.txt
fi
