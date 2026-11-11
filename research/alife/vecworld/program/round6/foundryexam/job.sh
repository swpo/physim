#!/bin/bash
# job.sh -- the GPU job of study foundryexam (requests r6-foundryexam-NNN); also the CPU test (FX_SIZE=smoke).
# 1. presmoke: every stage once at the full job's array shapes, a few steps (exit non-zero within minutes on failure)
# 2. the full pass. Everything is written under $OUT (small files, all PUBLIC pilot material).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
PY=${PY:-python}
: "${OUT:?OUT not set}"
mkdir -p "$OUT"
export PYTHONDONTWRITEBYTECODE=1
SIZE=${FX_SIZE:-full}
HOURS=${FX_MAX_HOURS:-2.5}
ARMS=${FX_ARMS:-P,N30,N10}
P() { echo "$(date +%T) [job.sh] $*" | tee -a "$OUT/progress.txt"; }
echo "PILOT_NEVER_REUSE_AS_EXAM: the hidden worlds of this job are public pilot material" > "$OUT/progress.txt"
P "start, size $SIZE, arms $ARMS, max hours $HOURS, nproc $(nproc 2>/dev/null || echo ?)"
$PY -c 'import jax, numpy, platform; print("versions", platform.python_version(), jax.__version__, numpy.__version__, jax.devices(), jax.default_backend())' 2>&1 | tee -a "$OUT/progress.txt"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv >> "$OUT/progress.txt" 2>&1 || true
if [ "$SIZE" = "smoke" ]; then
  $PY -B run_fx.py --size smoke --cpu-ok --arms "$ARMS" --out "$OUT/smoke" --max-hours 1.0
  RC=$?
  P "smoke exit $RC"
  exit $RC
fi
$PY -B run_fx.py --size presmoke --arms P,N30 --out "$OUT/presmoke" --max-hours 0.4
RC=$?
P "presmoke exit $RC"
if [ $RC -ne 0 ]; then tail -40 "$OUT/presmoke/progress.txt"; exit 2; fi
$PY -B run_fx.py --size full --arms "$ARMS" --out "$OUT/full" --max-hours "$HOURS"
RC=$?
P "full exit $RC; OUT size $(du -sh "$OUT" | cut -f1)"
exit $RC
