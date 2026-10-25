#!/bin/bash
# c19: replicate c16's invasion test (invade.py, unchanged) on fresh seeds; arm m8 = side-4 invader, m15 = side-11 neutral.
# usage: run_invasion.sh seed...   (run from research/alife with the labenv on PATH)
INV=collective/contrib/20261025T1415-c16-evoloop-invasion
OUT=$PWD/collective/contrib/20261025T1447-c19-review-evoloop/invasion
mkdir -p $OUT
cd $INV
for s in "$@"; do for m in 8 15; do python invade.py $s 20000 $m 40000 $OUT/inv_s${s}_m${m}.json; done; done
