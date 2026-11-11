#!/bin/bash
# Study dialsA2 (round 6, dials): one process, presmoke at full shapes first (exit non-zero within minutes on a
# failure or if the measured rates cannot finish), then the full pass. $OUT is public.
set -uo pipefail
cd "$(dirname "$0")"
: "${OUT:?OUT is not set}"
: "${A2_MAX_HOURS:=3.6}"
python -c 'import jax, numpy, scipy; print("versions", jax.__version__, numpy.__version__, scipy.__version__, jax.devices())' || exit 1
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv || true
python -B run_a2.py --out "$OUT" --max-hours "$A2_MAX_HOURS" ${A2_EXTRA:-}
rc=$?
du -sh "$OUT" || true
find "$OUT" -type f -size +19M -print || true
exit $rc
