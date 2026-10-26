#!/bin/bash
OUT=/tmp/claude-0/-home-user-physim/a7c2ec48-e3a6-5436-88da-a7523dbbe428/scratchpad/waudit/nematic-marangoni
CL=collective/contrib/20261026T0505-c34-nematic-marangoni/world.py
cd /home/user/physim/research/alife
run() { # name world outdir seed
  echo "START $1 $(date +%T)" >> $OUT/queue.log
  ( time OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2 PYTHONDONTWRITEBYTECODE=1 /home/user/labenv/bin/python -m labkit.run $2 --out $3 --seeds $4 --no-movie ) > $OUT/$1.log 2>&1
  echo "DONE $1 $(date +%T)" >> $OUT/queue.log
}
until grep -q DONE51 $OUT/queue.log 2>/dev/null; do sleep 5; done
run walloff_seed51 $OUT/variants/active-nematic-marangoni-walloff.py $OUT/controls/walloff_seed51 51
run rerun_seed52 $CL $OUT/rerun/seed52 52
run walloff_seed52 $OUT/variants/active-nematic-marangoni-walloff.py $OUT/controls/walloff_seed52 52
run chis0_seed51 $OUT/variants/active-nematic-marangoni-chis0.py $OUT/controls/chis0_seed51 51
run kappa0_seed51 $OUT/variants/active-nematic-marangoni-kappa0.py $OUT/controls/kappa0_seed51 51
echo ALLDONE >> $OUT/queue.log
