#!/bin/bash
# job.sh -- the GPU job of study cards (requests r6-cards-*.json); also the CPU test at tiny size (CARDS_SIZE=tiny).
# Order: versions, job.py (presmoke of every program group at full shapes, then all runs by priority).
# Everything is written under $OUT (small files). Exit code: non-zero if the presmoke or any run failed.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
PY=${PY:-python}
: "${OUT:?OUT not set}"
mkdir -p "$OUT/logs"
export PYTHONDONTWRITEBYTECODE=1
export CARDS_T_START=$(date +%s)
P() { echo "$(date +%T) [job.sh] $*" | tee -a "$OUT/progress.txt"; }
P "PILOT_NEVER_REUSE_AS_EXAM start, size ${CARDS_SIZE:-full}, nproc $(nproc 2>/dev/null || echo ?)"
$PY -c 'import jax, numpy, platform; print("versions", platform.python_version(), jax.__version__, numpy.__version__, jax.devices(), jax.default_backend())' 2>&1 | tee -a "$OUT/progress.txt"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv >> "$OUT/progress.txt" 2>&1 || true
$PY -B job.py > "$OUT/logs/job.log" 2>&1
RC=$?
[ $RC -ne 0 ] && { P "job.py exit $RC"; tail -40 "$OUT/logs/job.log"; }
P "OUT size $(du -sh "$OUT" | cut -f1), largest file $(find "$OUT" -type f -printf '%s %p\n' | sort -n | tail -1); done, RC=$RC"
exit $RC
