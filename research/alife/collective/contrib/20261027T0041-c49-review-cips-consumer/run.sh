#!/bin/bash
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
W=collective/contrib/20261026T1700-c43-cips-consumer/world.py; R=collective/contrib/20261027T0041-c49-review-cips-consumer
python -m labkit.run $W --out $R/rerun/seed7 --seeds 7 --frames 120 --lineage-k 5 --no-movie > $R/a.log 2>&1 &
WORLD_P='{"pred_on":0}' python -m labkit.run $W --out $R/twin_nocons/seed7 --seeds 7 --frames 120 --lineage-k 5 --no-movie > $R/b.log 2>&1
wait
WORLD_P='{"tcut":3000}' python -m labkit.run $W --out $R/efork_t3000/seed7 --seeds 7 --frames 40 --lineage-k 5 --no-movie > $R/c.log 2>&1
echo ALLDONE
