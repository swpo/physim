#!/bin/bash
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
W=collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py; R=collective/contrib/20261027T0153-c49-review-hunting-ecology
python -m labkit.run $W --out $R/rerun256 --seeds 9 --size 256 256 --frames 120 --lineage-k 5 --no-movie > $R/a.log 2>&1 &
( WORLD_P='{"fork_t":6000}' python -m labkit.run $W --out $R/efork128 --seeds 9 --frames 70 --lineage-k 5 --no-movie > $R/c.log 2>&1
  python -m labkit.run $W --out $R/fed128 --seeds 9 --frames 70 --lineage-k 5 --no-movie > $R/d.log 2>&1 ) &
wait; echo ALLDONE
