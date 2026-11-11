#!/bin/bash
# Study A (round 6, dials): one process, presmoke at full shapes first (exit non-zero within minutes on a
# failure or if the measured rates cannot finish), then the full pass. $OUT is public.
set -euo pipefail
cd "$(dirname "$0")"
: "${OUT:?OUT is not set}"
: "${A_MAX_HOURS:=2.0}"
python -c 'import jax, numpy, scipy; print("versions", jax.__version__, numpy.__version__, scipy.__version__, jax.devices())'
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv || true
python -B run_a.py --out "$OUT" --max-hours "$A_MAX_HOURS" ${A_EXTRA:-}
rc=$?
du -sh "$OUT" || true
find "$OUT" -type f -size +19M -print || true
exit $rc
