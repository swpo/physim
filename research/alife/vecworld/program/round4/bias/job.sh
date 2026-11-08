#!/bin/bash
# job.sh -- the GPU job of the round-4 study `bias` (requests r4-bias-*.json).
# 1. bsim.py: level-0 gliders data on the GPU (float64, jax.vmap), kept on the pod ($B4_WORK, not returned)
# 2. bcert.py workers (CPU, one BLAS thread each) start and wait for latents
# 3. btrain.py: the encoder grid on the GPU (float32), each frozen Phi encoded on the other half -> latents
# 4. bcombine.py: pooled halves, seed stability, windows -> $OUT/combined.json, table.txt
# Small results go to $OUT; the exit code is 0 only if every stage succeeded.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
PY=${PY:-python}
export B4_OUT=${OUT:?OUT not set}
export B4_WORK=${B4_WORK:-${GPUJOB_DIR:-$HERE}/b4work}
START=$(date +%s)
export B4_TRAIN_DEADLINE=$((START + ${B4_TRAIN_S:-7200}))
export B4_CERT_DEADLINE=$((START + ${B4_CERT_S:-9000}))
mkdir -p "$B4_WORK" "$B4_OUT/logs"
NP=$(nproc 2>/dev/null || echo 8)
NW=$(( NP - 3 )); [ "$NW" -lt 1 ] && NW=1
[ -n "${B4_WORKERS:-}" ] && NW=$B4_WORKERS
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
P() { echo "$(date +%T) [job] $*" | tee -a "$B4_OUT/progress.txt"; }
P "nproc $NP, cert workers $NW, train deadline +${B4_TRAIN_S:-7200}s, cert deadline +${B4_CERT_S:-9000}s, tiny ${B4_TINY:-0}"
$PY -c 'import jax, numpy, scipy, platform; print("versions", platform.python_version(), jax.__version__, numpy.__version__, scipy.__version__, jax.devices())' 2>&1 | tee -a "$B4_OUT/progress.txt"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv >> "$B4_OUT/progress.txt" 2>&1 || true
free -g | head -2 >> "$B4_OUT/progress.txt" 2>&1 || true
df -h "$B4_WORK" | tail -1 >> "$B4_OUT/progress.txt" 2>&1 || true
FAIL=0
$PY -B bsim.py > "$B4_OUT/logs/sim.log" 2>&1 || { P "bsim FAILED"; tail -30 "$B4_OUT/logs/sim.log" | tee -a "$B4_OUT/progress.txt"; exit 1; }
WT=$(( B4_CERT_DEADLINE - $(date +%s) + 600 ))
PIDS=()
for i in $(seq 1 "$NW"); do
  JAX_PLATFORMS=cpu timeout "$WT" $PY -B bcert.py "$i" > "$B4_OUT/logs/cert_$i.log" 2>&1 &
  PIDS+=($!)
done
$PY -B btrain.py > "$B4_OUT/logs/train.log" 2>&1 || { P "btrain FAILED"; tail -30 "$B4_OUT/logs/train.log" | tee -a "$B4_OUT/progress.txt"; FAIL=1; }
for p in "${PIDS[@]}"; do wait "$p" || { P "a cert worker exited non-zero ($p)"; FAIL=1; }; done
P "certification finished; $(ls "$B4_WORK/cert"/*.json 2>/dev/null | wc -l) halves certified, $(ls "$B4_WORK/lat"/*.ready 2>/dev/null | wc -l) left unclaimed"
[ -s "$B4_OUT/train_errors.txt" ] && { P "train errors:"; head -40 "$B4_OUT/train_errors.txt" | tee -a "$B4_OUT/progress.txt"; FAIL=1; }
ls "$B4_OUT"/cert_errors_*.txt >/dev/null 2>&1 && { P "cert errors:"; cat "$B4_OUT"/cert_errors_*.txt | head -40 | tee -a "$B4_OUT/progress.txt"; FAIL=1; }
JAX_PLATFORMS=cpu OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 $PY -B bcombine.py > "$B4_OUT/logs/combine.log" 2>&1 || { P "bcombine FAILED"; tail -30 "$B4_OUT/logs/combine.log" | tee -a "$B4_OUT/progress.txt"; FAIL=1; }
P "OUT size $(du -sh "$B4_OUT" | cut -f1); elapsed $(( $(date +%s) - START ))s; done, FAIL=$FAIL"
exit $FAIL
