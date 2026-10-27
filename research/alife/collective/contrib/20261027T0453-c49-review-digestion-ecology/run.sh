#!/bin/bash
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
C=collective/contrib/20261027T0325-c52-digestion-ecology-claim; R=collective/contrib/20261027T0453-c49-review-digestion-ecology
python -m labkit.run $C/world.py --out $R/rerun256 --seeds 4 --size 256 256 --frames 120 --no-movie > $R/a.log 2>&1 &
( WORLD_P='{"dfork_t":6000}' python -m labkit.run $C/world.py --out $R/dfork128 --seeds 4 --frames 70 --no-movie > $R/b.log 2>&1
  python -m labkit.run $C/world.py --out $R/fed128 --seeds 4 --frames 70 --no-movie > $R/c.log 2>&1 ) &
wait; echo ALLDONE
