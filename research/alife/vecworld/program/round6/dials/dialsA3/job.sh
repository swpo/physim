#!/bin/bash
# Study dialsA3 (round 6, dials; the zero-point rerun of dialsA2): one process, presmoke at full shapes first (exit
# non-zero within minutes on a failure or if the measured rates cannot finish; exit 0 before the full pass if the
# declared presmoke stop rule fires, DECLARED A3-4), then the full pass. $OUT is public.
set -uo pipefail
cd "$(dirname "$0")"
: "${OUT:?OUT is not set}"
: "${A3_MAX_HOURS:=4.2}"
python -c 'import jax, numpy, scipy; print("versions", jax.__version__, numpy.__version__, scipy.__version__, jax.devices())' || exit 1
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv || true
python -B run_a3.py --out "$OUT" --max-hours "$A3_MAX_HOURS" ${A3_EXTRA:-}
rc=$?
du -sh "$OUT" || true
find "$OUT" -type f -size +19M -print || true
exit $rc
