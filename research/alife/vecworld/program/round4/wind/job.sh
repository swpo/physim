#!/bin/bash
# job.sh -- the GPU job of the round-4 wind certification (requests r4-wind-*.json).
# Order: runner check, F/M simulation, then the F/M analyses in the background while FM2 and P simulate,
# then the FM2 and P analyses; combine at the end. Everything is written under $OUT (small files) and
# $GPUJOB_DIR/w4work (simulation arrays, not returned). Exit code: 0 only if every step succeeded.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
cd "$HERE"
PY=${PY:-python}
export W4_OUT=${OUT:?OUT not set}
export W4_WORK=${W4_WORK:-${GPUJOB_DIR:-$HERE}/w4work}
mkdir -p "$W4_WORK" "$W4_OUT/logs"
NP=$(nproc 2>/dev/null || echo 8)
NT=$(( NP / 8 )); [ "$NT" -lt 1 ] && NT=1
export OMP_NUM_THREADS=$NT OPENBLAS_NUM_THREADS=$NT MKL_NUM_THREADS=$NT PYTHONDONTWRITEBYTECODE=1
TMO=${W4_TIMEOUT:-5100}                       # per analysis process (s)
P() { echo "$(date +%T) [job] $*" | tee -a "$W4_OUT/progress.txt"; }
P "nproc $NP, BLAS threads per process $NT, analysis timeout ${TMO}s"
$PY -c 'import jax, numpy, scipy, platform; print("versions", platform.python_version(), jax.__version__, numpy.__version__, scipy.__version__, jax.devices())' 2>&1 | tee -a "$W4_OUT/progress.txt"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv >> "$W4_OUT/progress.txt" 2>&1 || true
FAIL=0
$PY -B check4.py --burn > "$W4_OUT/logs/check4.log" 2>&1 || P "check4 reported a difference (non-fatal; logs/check4.log)"
$PY -B sim4.py fm > "$W4_OUT/logs/sim_fm.log" 2>&1 || { P "sim fm FAILED"; tail -20 "$W4_OUT/logs/sim_fm.log"; exit 1; }
declare -A PIDS
for S in F M; do for V in coarse objects; do
  timeout "$TMO" $PY -B clos4.py $S $V > "$W4_OUT/logs/clos_${S}_${V}.log" 2>&1 &
  PIDS[${S}_${V}]=$!
done; done
$PY -B sim4.py fm2 > "$W4_OUT/logs/sim_fm2.log" 2>&1 || { P "sim fm2 FAILED"; FAIL=1; }
if [ -f "$W4_WORK/FM2.npz" ]; then for S in F2 M2; do
  timeout "$TMO" $PY -B clos4.py $S objects --nolc > "$W4_OUT/logs/clos_${S}_objects.log" 2>&1 &
  PIDS[${S}_objects]=$!
done; fi
$PY -B sim4.py p > "$W4_OUT/logs/sim_p.log" 2>&1 || { P "sim p FAILED"; FAIL=1; }
if [ -f "$W4_WORK/P.npz" ]; then for V in coarse objects; do
  timeout "$TMO" $PY -B clos4.py P $V > "$W4_OUT/logs/clos_P_${V}.log" 2>&1 &
  PIDS[P_${V}]=$!
done; fi
for k in "${!PIDS[@]}"; do
  if wait "${PIDS[$k]}"; then P "clos4 $k ok"; else P "clos4 $k FAILED (exit $?)"; tail -5 "$W4_OUT/logs/clos_${k}.log" | tee -a "$W4_OUT/progress.txt"; FAIL=1; fi
done
$PY -B combine4.py > "$W4_OUT/logs/combine.log" 2>&1 || { P "combine FAILED"; FAIL=1; }
for f in FM.json FM2.json P.json; do [ -f "$W4_WORK/$f" ] && cp "$W4_WORK/$f" "$W4_OUT/sim_$f"; done
P "OUT size $(du -sh "$W4_OUT" | cut -f1); done, FAIL=$FAIL"
exit $FAIL
