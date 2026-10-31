#!/bin/bash
# Labkit packs (no dynamics noise: the claim's setting) for fresh seeds 3 and 4, T = 600 native time (120 frames of
# 5 native time), at a given dt and grid, then c34's own measures. One process at a time.
# usage: run_behav.sh DT N   (e.g. 0.05 128, 0.025 128)
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 TIMEFORMAT='%U user %S sys %R wall'
PY=/home/user/physim/research/alife/.labenv/bin/python
DT=$1; N=$2
DX=$($PY -c "print(128/$N)")
SPF=$($PY -c "print(int(round(5/$DT)))")
OUTD=$PWD/behav/dt${DT}_n${N}
W=/home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni/world.py
C=/home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni
mkdir -p "$OUTD"
cd /home/user/physim/research/alife
export WORLD_P="{\"dt\": $DT, \"dx\": $DX, \"noise_area\": $([ "$N" = 128 ] && echo false || echo true)}"
{ echo "behav dt $DT n $N"; time $PY -B -m labkit.run "$W" --out "$OUTD" --seeds 3 4 --frames 120 --spf "$SPF" --dt "$DT" --size "$N" "$N" --no-movie > "$OUTD/run.log" 2>&1; } 2>> "$OLDPWD/out/cpu.log"
for s in 3 4; do
  f="$OUTD/seed$s/frames.npz"
  { $PY -B "$C/swimdivide.py" "$f" "$W" 20
    $PY -B "$C/sd_individuals.py" "$f" 2,3 "$DX"
    $PY -B "$C/inherit.py" "$f" "$W" 3
    $PY -B "$C/speedstats.py" "$f" "$W"; } > "$OUTD/measures_seed$s.txt" 2>&1
done
