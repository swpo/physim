#!/bin/bash
# job.sh -- one GPU job of the round-5 study `bias2`: the worlds of $B5_PLAN, one after another.
#   B5_PLAN="world:sim_s:train_s:cert_s ..."   deadlines in seconds from that world's start: after sim_s the
#   simulation aborts, after train_s no new config starts, after cert_s no new certification starts.
# Per world:
# 1. csim.py: level-0 data on the GPU (float64, jax.vmap), kept on the pod ($B5_WORK, not returned)
# 2. ccert.py workers (CPU, one BLAS thread each) start and wait for latents
# 3. ctrain.py: hand designs, then the encoder grid on the GPU (float32); each frozen Phi encoded on the other half
# 4. ccombine.py: pooled halves, seed stability, windows -> $OUT/<world>/combined.json, table.txt
# Small results go to $OUT/<world>; the exit code is 0 only if every stage of every world succeeded.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
PY=${PY:-python}
export B5_OUT=${OUT:?OUT not set}
export B5_WORK=${B5_WORK:-${GPUJOB_DIR:-$HERE}/b5work}
PLAN=${B5_PLAN:?B5_PLAN not set}
JOBSTART=$(date +%s)
mkdir -p "$B5_WORK" "$B5_OUT"
NP=$(nproc 2>/dev/null || echo 8)
NW=$(( NP - 3 )); [ "$NW" -lt 1 ] && NW=1
[ -n "${B5_WORKERS:-}" ] && NW=$B5_WORKERS
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
P() { echo "$(date +%T) [job] $*" | tee -a "$B5_OUT/progress.txt"; }
P "plan $PLAN, nproc $NP, cert workers $NW, sim budget ${B5_SIM_BUDGET_S:-2400}s, tiny ${B5_TINY:-0}"
$PY -c 'import jax, numpy, scipy, platform; print("versions", platform.python_version(), jax.__version__, numpy.__version__, scipy.__version__, jax.devices())' 2>&1 | tee -a "$B5_OUT/progress.txt"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv >> "$B5_OUT/progress.txt" 2>&1 || true
free -g | head -2 >> "$B5_OUT/progress.txt" 2>&1 || true
df -h "$B5_WORK" | tail -1 >> "$B5_OUT/progress.txt" 2>&1 || true
FAIL=0
for ENTRY in $PLAN; do
  IFS=: read -r W SIM_S TRAIN_S CERT_S <<< "$ENTRY"
  export B5_WORLD=$W
  START=$(date +%s)
  export B5_SIM_DEADLINE=$((START + SIM_S)) B5_TRAIN_DEADLINE=$((START + TRAIN_S)) B5_CERT_DEADLINE=$((START + CERT_S))
  O="$B5_OUT/$W"
  mkdir -p "$O/logs"
  P "=== world $W: deadlines sim +${SIM_S}s train +${TRAIN_S}s cert +${CERT_S}s"
  WFAIL=0
  if ! $PY -B csim.py > "$O/logs/sim.log" 2>&1; then
    P "csim FAILED ($W)"; tail -30 "$O/logs/sim.log" | tee -a "$B5_OUT/progress.txt"; FAIL=1; rm -rf "$B5_WORK/$W"; continue
  fi
  WT=$(( B5_CERT_DEADLINE - $(date +%s) + 600 ))
  PIDS=()
  for i in $(seq 1 "$NW"); do
    JAX_PLATFORMS=cpu timeout "$WT" $PY -B ccert.py "$i" > "$O/logs/cert_$i.log" 2>&1 &
    PIDS+=($!)
  done
  $PY -B ctrain.py > "$O/logs/train.log" 2>&1 || { P "ctrain FAILED ($W)"; tail -30 "$O/logs/train.log" | tee -a "$B5_OUT/progress.txt"; WFAIL=1; }
  for p in "${PIDS[@]}"; do wait "$p" || { P "a cert worker exited non-zero ($p)"; WFAIL=1; }; done
  P "$W certification finished; $(ls "$B5_WORK/$W/cert"/*.json 2>/dev/null | wc -l) halves certified, $(ls "$B5_WORK/$W/lat"/*.ready 2>/dev/null | wc -l) left unclaimed"
  [ -s "$O/train_errors.txt" ] && { P "train errors:"; head -40 "$O/train_errors.txt" | tee -a "$B5_OUT/progress.txt"; WFAIL=1; }
  ls "$O"/cert_errors_*.txt >/dev/null 2>&1 && { P "cert errors:"; cat "$O"/cert_errors_*.txt | head -40 | tee -a "$B5_OUT/progress.txt"; WFAIL=1; }
  JAX_PLATFORMS=cpu OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 $PY -B ccombine.py > "$O/logs/combine.log" 2>&1 || { P "ccombine FAILED ($W)"; tail -30 "$O/logs/combine.log" | tee -a "$B5_OUT/progress.txt"; WFAIL=1; }
  rm -rf "$B5_WORK/$W/data"
  P "=== world $W done in $(( $(date +%s) - START ))s, FAIL=$WFAIL"
  [ "$WFAIL" -ne 0 ] && FAIL=1
done
P "OUT size $(du -sh "$B5_OUT" | cut -f1); elapsed $(( $(date +%s) - JOBSTART ))s; done, FAIL=$FAIL"
exit $FAIL
