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
# Hard time bound: B5_JOB_HARD_S (seconds from the start of this script; set it below the runner's kill time
# max_hours x 3600 minus setup and collection). Every world's deadlines are clipped to it and every stage runs under
# `timeout`: csim to its deadline + 120 s, ctrain to the certification deadline, the workers to that + 240 s,
# ccombine to 420 s. So a world ends at most 700 s after its certification deadline, and the job before the bound.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
PY=${PY:-python}
export B5_OUT=${OUT:?OUT not set}
export B5_WORK=${B5_WORK:-${GPUJOB_DIR:-$HERE}/b5work}
PLAN=${B5_PLAN:?B5_PLAN not set}
JOBSTART=$(date +%s)
JOBEND=$(( JOBSTART + ${B5_JOB_HARD_S:-864000} ))
mkdir -p "$B5_WORK" "$B5_OUT"
NP=$(nproc 2>/dev/null || echo 8)
NW=$(( NP - 3 )); [ "$NW" -lt 1 ] && NW=1
[ -n "${B5_WORKERS:-}" ] && NW=$B5_WORKERS
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
P() { echo "$(date +%T) [job] $*" | tee -a "$B5_OUT/progress.txt"; }
P "plan $PLAN, nproc $NP, cert workers $NW, sim budget ${B5_SIM_BUDGET_S:-2400}s, hard end +${B5_JOB_HARD_S:-none}s, tiny ${B5_TINY:-0}"
$PY -c 'import jax, numpy, scipy, platform; print("versions", platform.python_version(), jax.__version__, numpy.__version__, scipy.__version__, jax.devices())' 2>&1 | tee -a "$B5_OUT/progress.txt"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv >> "$B5_OUT/progress.txt" 2>&1 || true
free -g | head -2 >> "$B5_OUT/progress.txt" 2>&1 || true
df -h "$B5_WORK" | tail -1 >> "$B5_OUT/progress.txt" 2>&1 || true
if [ "${B5_TINY:-0}" != 1 ] && [ "${B5_ALLOW_CPU:-0}" != 1 ]; then    # a GPU job without a GPU backend would only burn pod time
  $PY -c 'import jax, sys; sys.exit(0 if jax.default_backend() == "gpu" else 3)' || { P "jax.default_backend() is not gpu: abort"; exit 3; }
fi
FAIL=0
for ENTRY in $PLAN; do
  IFS=: read -r W SIM_S TRAIN_S CERT_S <<< "$ENTRY"
  export B5_WORLD=$W
  START=$(date +%s)
  CD=$(( START + CERT_S )); [ "$CD" -gt $(( JOBEND - 700 )) ] && CD=$(( JOBEND - 700 ))      # clip to the job's hard end
  TD=$(( START + TRAIN_S )); [ "$TD" -gt $(( CD - 240 )) ] && TD=$(( CD - 240 ))
  SD=$(( START + SIM_S )); [ "$SD" -gt $(( TD - 300 )) ] && SD=$(( TD - 300 ))
  if [ "$SD" -lt $(( START + 60 )) ]; then
    P "world $W SKIPPED: $(( JOBEND - START ))s left before the job's hard end"; FAIL=1; continue
  fi
  export B5_SIM_DEADLINE=$SD B5_TRAIN_DEADLINE=$TD B5_CERT_DEADLINE=$CD
  O="$B5_OUT/$W"
  mkdir -p "$O/logs"
  P "=== world $W: deadlines sim +$(( SD - START ))s train +$(( TD - START ))s cert +$(( CD - START ))s (plan $SIM_S/$TRAIN_S/$CERT_S)"
  WFAIL=0
  if ! timeout -k 10 $(( SD - START + 120 )) $PY -B csim.py > "$O/logs/sim.log" 2>&1; then
    P "csim FAILED ($W)"; tail -30 "$O/logs/sim.log" | tee -a "$B5_OUT/progress.txt"; FAIL=1; rm -rf "$B5_WORK/$W"; continue
  fi
  NOW=$(date +%s)
  WT=$(( CD - NOW + 240 ))
  PIDS=()
  for i in $(seq 1 "$NW"); do
    JAX_PLATFORMS=cpu timeout -k 10 "$WT" $PY -B ccert.py "$i" > "$O/logs/cert_$i.log" 2>&1 &
    PIDS+=($!)
  done
  timeout -k 10 $(( CD - NOW )) $PY -B ctrain.py > "$O/logs/train.log" 2>&1 || { P "ctrain FAILED ($W)"; tail -30 "$O/logs/train.log" | tee -a "$B5_OUT/progress.txt"; WFAIL=1; }
  mkdir -p "$B5_WORK/$W/lat" && touch "$B5_WORK/$W/lat/DONE"   # whatever ctrain's exit status (it may die at import): the workers must not poll to the deadline
  for p in "${PIDS[@]}"; do wait "$p" || { P "a cert worker exited non-zero ($p)"; WFAIL=1; }; done
  P "$W certification finished; $(ls "$B5_WORK/$W/cert"/*.json 2>/dev/null | wc -l) halves certified, $(ls "$B5_WORK/$W/lat"/*.ready 2>/dev/null | wc -l) left unclaimed"
  [ -s "$O/train_errors.txt" ] && { P "train errors:"; head -40 "$O/train_errors.txt" | tee -a "$B5_OUT/progress.txt"; WFAIL=1; }
  ls "$O"/cert_errors_*.txt >/dev/null 2>&1 && { P "cert errors:"; cat "$O"/cert_errors_*.txt | head -40 | tee -a "$B5_OUT/progress.txt"; WFAIL=1; }
  JAX_PLATFORMS=cpu OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 timeout -k 10 420 $PY -B ccombine.py > "$O/logs/combine.log" 2>&1 || { P "ccombine FAILED ($W)"; tail -30 "$O/logs/combine.log" | tee -a "$B5_OUT/progress.txt"; WFAIL=1; }
  rm -rf "$B5_WORK/$W/data"
  P "=== world $W done in $(( $(date +%s) - START ))s, FAIL=$WFAIL"
  [ "$WFAIL" -ne 0 ] && FAIL=1
done
P "OUT size $(du -sh "$B5_OUT" | cut -f1); elapsed $(( $(date +%s) - JOBSTART ))s; done, FAIL=$FAIL"
exit $FAIL
