#!/bin/bash
# job2.sh -- the second GPU job of study foundry (request r5-foundry-002); also the CPU test at tiny size
# (FOUNDRY_SIZE=tiny). Runs job2.py (arms late, enrich, cert, sigma010, sigma100). Everything is written
# under $OUT (small files). Exit code: 0 only if every arm finished.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
PY=${PY:-python}
: "${OUT:?OUT not set}"
mkdir -p "$OUT/logs"
export PYTHONDONTWRITEBYTECODE=1
export FOUNDRY_T_START=$(date +%s)
P() { echo "$(date +%T) [job2.sh] $*" | tee -a "$OUT/progress.txt"; }
P "start, size ${FOUNDRY_SIZE:-full}, nproc $(nproc 2>/dev/null || echo ?)"
$PY -c 'import jax, numpy, platform; print("versions", platform.python_version(), jax.__version__, numpy.__version__, jax.devices(), jax.default_backend())' 2>&1 | tee -a "$OUT/progress.txt"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv >> "$OUT/progress.txt" 2>&1 || true
FAIL=0
$PY -B job2.py > "$OUT/logs/job2.log" 2>&1
RC=$?
[ $RC -ne 0 ] && { P "job2.py exit $RC"; tail -30 "$OUT/logs/job2.log"; FAIL=1; }
P "OUT size $(du -sh "$OUT" | cut -f1); done, FAIL=$FAIL"
exit $FAIL
