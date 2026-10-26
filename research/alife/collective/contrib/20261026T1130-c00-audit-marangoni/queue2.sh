#!/bin/bash
OUT=/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/nematic-marangoni
until grep -q ALLDONE $OUT/queue.log 2>/dev/null; do sleep 5; done
cd /home/user/physim/research/alife
echo "START res15_seed51 $(date +%T)" >> $OUT/queue.log
( time OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 /home/user/labenv/bin/python -m labkit.run $OUT/variants/active-nematic-marangoni-res15.py --out $OUT/controls/res15_seed51 --seeds 51 --size 192 192 --frames 120 --no-movie ) > $OUT/res15_seed51.log 2>&1
echo "DONE res15_seed51 $(date +%T)" >> $OUT/queue.log
