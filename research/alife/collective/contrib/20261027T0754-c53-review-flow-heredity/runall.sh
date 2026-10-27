#!/bin/bash
# c53 review of 20261027T0209-c49-thermals-flow-heredity: labkit re-run (eps 0.1, seed 21) and heredity.py (copied unchanged
# with world.py) on fresh seeds 21 and 22 for eps +0.1, -0.1 and 0
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=1 NUMBA_NUM_THREADS=1
R=collective/contrib/20261027T0754-c53-review-flow-heredity
WORLD_P='{"eps":0.1}' python -m labkit.run collective/contrib/20261027T0209-c49-thermals-flow-heredity/world.py --out $R/pack_eps0.1 --seeds 21 --frames 800 --spf 25 --no-movie > $R/pack.log 2>&1 &
cd $R
for sd in 21 22; do for e in 0.1 -0.1 0; do
  WORLD_P="{\"eps\":$e}" python heredity.py h_s${sd}_e$e $sd 800 > h_${sd}_$e.log 2>&1 &
  while [ $(jobs -r | wc -l) -ge 3 ]; do sleep 2; done
done; done
wait
echo ALLDONE
