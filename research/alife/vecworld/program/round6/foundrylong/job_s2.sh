#!/bin/bash
# job_s2.sh -- the GPU job of study foundrylong, stage 2 (request r6-foundrylong-002); also the CPU test (FL_SIZE=smoke).
# 1. presmoke: 2 hidden worlds through every stage at the full job's fit shapes, and a speed guard that projects the
#    whole job from the measured fit speed (exit 4 before the full pass spends anything)
# 2. the full pass. Everything is written under $OUT (all PUBLIC pilot material).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
PY=${PY:-python}
: "${OUT:?OUT not set}"
mkdir -p "$OUT"
export PYTHONDONTWRITEBYTECODE=1
SIZE=${FL_SIZE:-full}
HOURS=${FL_MAX_HOURS:-2.9}          # for the whole of job_s2.sh (presmoke + full pass)
T_START=$(date +%s)
P() { echo "$(date +%T) [job_s2.sh] $*" | tee -a "$OUT/progress.txt"; }
echo "PILOT_NEVER_REUSE_AS_EXAM: the hidden worlds of this job are public pilot material" > "$OUT/progress.txt"
P "start, size $SIZE, max hours $HOURS, nproc $(nproc --all 2>/dev/null || echo ?)"
$PY -c 'import jax, numpy, platform; print("versions", platform.python_version(), jax.__version__, numpy.__version__, jax.devices(), jax.default_backend())' 2>&1 | tee -a "$OUT/progress.txt"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv >> "$OUT/progress.txt" 2>&1 || true
if [ "$SIZE" = "smoke" ]; then
  $PY -B run_fl2.py --size smoke --cpu-ok --out "$OUT/smoke" --max-hours 1.0
  RC=$?
  P "smoke exit $RC"
  exit $RC
fi
$PY -B run_fl2.py --size presmoke --out "$OUT/presmoke" --max-hours 0.5 --full-hours "$HOURS"
RC=$?
P "presmoke exit $RC"
if [ $RC -ne 0 ]; then tail -40 "$OUT/presmoke/progress.txt"; exit 2; fi   # 4 from run_fl2: too slow (shape_test.json)
rm -f "$OUT/presmoke/scores.npz" "$OUT/presmoke/w_fits.npz"                  # test material, not results
LEFT=$(awk -v h="$HOURS" -v t0="$T_START" -v t1="$(date +%s)" 'BEGIN { printf "%.3f", h - (t1 - t0) / 3600.0 }')
P "full pass: $LEFT h left of $HOURS"
$PY -B run_fl2.py --size full --out "$OUT/full" --max-hours "$LEFT"
RC=$?
P "full exit $RC; OUT size $(du -sh "$OUT" | cut -f1)"
exit $RC
