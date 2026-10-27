#!/bin/bash
# c53 review of 20261026T2103-c46-hunting-ecology-claim: fresh seed 8 at 256^2 (claim settings) and the predator-free twin;
# then the fuel-cut fork (fork_t 6000) with its fed twin at 128^2 (drive.py), seed 8
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
R=collective/contrib/20261027T0953-c53-review-hunting-ecology; W=collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py
python -m labkit.run $W --out $R/pack256 --seeds 8 --size 256 256 --frames 120 --lineage-k 5 --no-movie > $R/pack256.log 2>&1 &
( WORLD_P='{"pred_on":0}' python -m labkit.run $W --out $R/twin256 --seeds 8 --size 256 256 --frames 120 --lineage-k 5 --no-movie > $R/twin256.log 2>&1
  OMP_NUM_THREADS=1 WORLD_P='{"fork_t":6000}' python $R/drive.py $W $R/fork_s8 --T 8000 --seed 8 > $R/fork.log 2>&1 &
  OMP_NUM_THREADS=1 python $R/drive.py $W $R/fed_s8 --T 8000 --seed 8 > $R/fed.log 2>&1
  wait )
wait; echo ALLDONE
