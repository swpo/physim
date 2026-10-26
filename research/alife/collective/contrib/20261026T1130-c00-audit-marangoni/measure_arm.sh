#!/bin/bash
# usage: measure_arm.sh <run dir relative to OUT> <world.py> <label> [rerun]
OUT=/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/nematic-marangoni
CD=/home/user/physim/research/alife/collective/contrib/20261026T0505-c34-nematic-marangoni
PY="env PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 /home/user/labenv/bin/python"
FR=$OUT/$1/frames.npz; W=$2; L=$3
cd /tmp
{
echo "##### $L ($1)"
$PY $OUT/measure_w.py $FR $W 3 2 --bands 1.5,3,6 --label "$L[own 1.5|3-6]" --json $OUT/w_results.jsonl
$PY $OUT/measure_w.py $FR $W 3 2 --bands 1.0,2,4 --label "$L[own 1|2-4]" --json $OUT/w_results.jsonl
echo "-- claim's sd_individuals.py (ch2 ring, ch3 cargo):"
$PY $CD/sd_individuals.py $FR 2,3
echo "-- claim's inherit.py (ch3):"
$PY $CD/inherit.py $FR $W 3
if [ -n "$4" ]; then echo "-- claim's swimdivide.py:"; $PY $CD/swimdivide.py $FR $W; fi
} 2>&1 | tee -a $OUT/measure_log.txt
