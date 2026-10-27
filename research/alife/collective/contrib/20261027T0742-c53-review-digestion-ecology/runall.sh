#!/bin/bash
# c53 review of 20261027T0325-c52-digestion-ecology-claim: fresh seed 5 at 256^2 (claimed world, defaults) and the
# predator-free twin (pred_on 0) on the same seed; then the prey-removal fork (dfork_t 6000) and its fed twin at 128^2, seed 5
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
R=collective/contrib/20261027T0742-c53-review-digestion-ecology; W=collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py
python -m labkit.run $W --out $R/pack256 --seeds 5 --size 256 256 --frames 120 --no-movie > $R/pack256.log 2>&1 &
( WORLD_P='{"pred_on":0}' python -m labkit.run $W --out $R/twin256 --seeds 5 --size 256 256 --frames 120 --no-movie > $R/twin256.log 2>&1
  OMP_NUM_THREADS=1 WORLD_P='{"dfork_t":6000}' python $R/drive.py $W $R/dfork_s5 --T 8000 --seed 5 > $R/dfork.log 2>&1 &
  OMP_NUM_THREADS=1 python $R/drive.py $W $R/fed_s5 --T 8000 --seed 5 > $R/fed.log 2>&1
  wait )
wait
echo ALLDONE
