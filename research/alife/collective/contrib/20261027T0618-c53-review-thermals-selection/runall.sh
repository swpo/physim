#!/bin/bash
# c53 review of 20261027T0222-c49-thermals-selection-claim: labkit re-runs of the claimed world (b favoured) on fresh seeds
# 21 22 and the neutral twin on the same seeds; heredity2.py (copied unchanged with world.py) on seeds 21 22 23, both arms
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1
R=collective/contrib/20261027T0618-c53-review-thermals-selection; W=collective/contrib/20261027T0222-c49-thermals-selection-claim/world.py
WORLD_P='{"eps":-0.1,"lab_mode":1,"mut_dt":25}' python -m labkit.run $W --out $R/pack_sel --seeds 21 22 --frames 1200 --spf 25 --no-movie > $R/sel.log 2>&1 &
WORLD_P='{"eps":0,"lab_mode":1,"mut_dt":25}' python -m labkit.run $W --out $R/pack_neutral --seeds 21 22 --frames 1200 --spf 25 --no-movie > $R/neu.log 2>&1 &
wait
cd $R
for sd in 21 22 23; do
  WORLD_P='{"eps":-0.1,"lab_mode":1,"mut_dt":25}' python heredity2.py m_s${sd}_e-0.1 $sd 1200 > h_${sd}_sel.log 2>&1 &
  WORLD_P='{"eps":0,"lab_mode":1,"mut_dt":25}' python heredity2.py m_s${sd}_e0 $sd 1200 > h_${sd}_neu.log 2>&1
  wait
done
echo ALLDONE
