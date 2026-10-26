#!/bin/bash
# usage: measure_arm.sh <run dir relative to OUT> <world.py> <label> [dx]
OUT=/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/nematic-cargo
C=/home/user/physim/research/alife/collective/contrib/20261026T0405-c34-nematic-cargo
cd /tmp; export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1
PY=/home/user/labenv/bin/python
D=$OUT/$1
$PY $OUT/measure_w.py $D/frames.npz $2 --json $D/w_mine.json --label $3 --dx ${4:-1.0} > $D/w_mine.txt 2>&1
$PY $C/sd_individuals.py $D/frames.npz 2,3 ${4:-1.0} > $D/claim_sd.txt 2>&1
$PY $C/inherit.py $D/frames.npz $2 > $D/claim_inherit.txt 2>&1
grep -E "median_in_out:|share_ge2:|daughters_median|daughters_share_ge2:|ring_both|tracks_majority" $D/w_mine.txt; cat $D/claim_sd.txt $D/claim_inherit.txt | sed "s|$OUT/||"
