#!/bin/bash
# job.sh -- the GPU job of study foundry (requests r5-foundry-*.json); also the CPU test at tiny size
# (FOUNDRY_SIZE=tiny). Order: versions, quick family checks, job.py (checks, weight statistics, screen,
# selection, certification, controls, gliders reference). Everything is written under $OUT (small files).
# Exit code: 0 only if every step succeeded.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
PY=${PY:-python}
: "${OUT:?OUT not set}"
mkdir -p "$OUT/logs"
export PYTHONDONTWRITEBYTECODE=1
export FOUNDRY_T_START=$(date +%s)
P() { echo "$(date +%T) [job.sh] $*" | tee -a "$OUT/progress.txt"; }
P "start, size ${FOUNDRY_SIZE:-full}, nproc $(nproc 2>/dev/null || echo ?)"
$PY -c 'import jax, numpy, scipy, platform; print("versions", platform.python_version(), jax.__version__, numpy.__version__, scipy.__version__, jax.devices(), jax.default_backend())' 2>&1 | tee -a "$OUT/progress.txt"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv >> "$OUT/progress.txt" 2>&1 || true
FAIL=0
$PY -B check_tnca.py --quick --out "$OUT/checks_quick.json" > "$OUT/logs/check_tnca.log" 2>&1 \
  || { P "check_tnca reported a failure (logs/check_tnca.log)"; tail -5 "$OUT/logs/check_tnca.log" | tee -a "$OUT/progress.txt"; FAIL=1; }
P "check_tnca done"
$PY -B job.py > "$OUT/logs/job.log" 2>&1
RC=$?
[ $RC -ne 0 ] && { P "job.py exit $RC"; tail -30 "$OUT/logs/job.log"; FAIL=1; }
P "OUT size $(du -sh "$OUT" | cut -f1); done, FAIL=$FAIL"
exit $FAIL
