#!/bin/bash
# job.sh -- the GPU job of the round-5 study `slots` (requests r5-slots-*.json).
# 1. ssim.py: level-0 gliders data + the tracker's tables and label maps on the GPU (float64), kept on the pod
# 2. scert.py workers (CPU, one thread each) start and wait for latents
# 3. strain.py: references, no-learning encoders, the learned slot encoders (float32, 4 replicas per config),
#    objective values on frozen readouts; every frozen Phi encoded on the other half -> latents
# 4. scombine.py: pooled halves, seed pairs -> $OUT/combined.json, table.txt
# Small results go to $OUT; the exit code is 0 only if every stage succeeded.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
PY=${PY:-python}
export S5_OUT=${OUT:?OUT not set}
export S5_WORK=${S5_WORK:-${GPUJOB_DIR:-$HERE}/s5work}
START=$(date +%s)
export S5_TRAIN_DEADLINE=$((START + ${S5_TRAIN_S:-5100}))
export S5_CERT_DEADLINE=$((START + ${S5_CERT_S:-6600}))
mkdir -p "$S5_WORK" "$S5_OUT/logs"
NP=$(nproc 2>/dev/null || echo 8)
NW=$(( NP - 3 )); [ "$NW" -lt 1 ] && NW=1
[ -n "${S5_WORKERS:-}" ] && NW=$S5_WORKERS
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1
P() { echo "$(date +%T) [job] $*" | tee -a "$S5_OUT/progress.txt"; }
P "nproc $NP, cert workers $NW, train deadline +${S5_TRAIN_S:-5100}s, cert deadline +${S5_CERT_S:-6600}s, size ${S5_SIZE:-full}"
$PY -c 'import jax, numpy, scipy, platform; print("versions", platform.python_version(), jax.__version__, numpy.__version__, scipy.__version__, jax.devices())' 2>&1 | tee -a "$S5_OUT/progress.txt"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv >> "$S5_OUT/progress.txt" 2>&1 || true
free -g | head -2 >> "$S5_OUT/progress.txt" 2>&1 || true
df -h "$S5_WORK" | tail -1 >> "$S5_OUT/progress.txt" 2>&1 || true
FAIL=0
$PY -B ssim.py > "$S5_OUT/logs/sim.log" 2>&1 || { P "ssim FAILED"; tail -30 "$S5_OUT/logs/sim.log" | tee -a "$S5_OUT/progress.txt"; exit 1; }
WT=$(( S5_CERT_DEADLINE - $(date +%s) + 900 ))
PIDS=()
for i in $(seq 1 "$NW"); do
  JAX_PLATFORMS=cpu CUDA_VISIBLE_DEVICES= timeout "$WT" $PY -B scert.py "$i" > "$S5_OUT/logs/cert_$i.log" 2>&1 &
  PIDS+=($!)
done
$PY -B strain.py > "$S5_OUT/logs/train.log" 2>&1 || { P "strain FAILED"; tail -30 "$S5_OUT/logs/train.log" | tee -a "$S5_OUT/progress.txt"; FAIL=1; }
for p in "${PIDS[@]}"; do wait "$p" || { P "a cert worker exited non-zero ($p)"; FAIL=1; }; done
P "certification finished; $(ls "$S5_WORK/cert"/*.json 2>/dev/null | wc -l) halves certified, $(ls "$S5_WORK/lat"/*.ready 2>/dev/null | wc -l) left unclaimed"
[ -s "$S5_OUT/train_errors.txt" ] && { P "train errors:"; head -40 "$S5_OUT/train_errors.txt" | tee -a "$S5_OUT/progress.txt"; FAIL=1; }
ls "$S5_OUT"/cert_errors_*.txt >/dev/null 2>&1 && { P "cert errors:"; cat "$S5_OUT"/cert_errors_*.txt | head -40 | tee -a "$S5_OUT/progress.txt"; FAIL=1; }
JAX_PLATFORMS=cpu CUDA_VISIBLE_DEVICES= OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 $PY -B scombine.py > "$S5_OUT/logs/combine.log" 2>&1 || { P "scombine FAILED"; tail -30 "$S5_OUT/logs/combine.log" | tee -a "$S5_OUT/progress.txt"; FAIL=1; }
cat "$S5_OUT/table.txt" >> "$S5_OUT/progress.txt" 2>/dev/null || true
P "OUT size $(du -sh "$S5_OUT" | cut -f1); elapsed $(( $(date +%s) - START ))s; done, FAIL=$FAIL"
exit $FAIL
