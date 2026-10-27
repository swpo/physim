#!/bin/bash
# c53 review of 20261026T1700-c43-cips-consumer: fresh seed 7 (claimed world, claim's settings), consumer-free twin (pred_on 0),
# and the prey-removal fork (tcut 3000) on the same seed
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2 NUMBA_NUM_THREADS=2
R=collective/contrib/20261027T0748-c53-review-cips-consumer; W=collective/contrib/20261026T1700-c43-cips-consumer/world.py
python -m labkit.run $W --out $R/pack --seeds 7 --frames 120 --lineage-k 5 --no-movie > $R/pack.log 2>&1 &
WORLD_P='{"pred_on":0}' python -m labkit.run $W --out $R/twin --seeds 7 --frames 120 --lineage-k 5 --no-movie > $R/twin.log 2>&1
WORLD_P='{"tcut":3000}' python -m labkit.run $W --out $R/efork --seeds 7 --frames 40 --lineage-k 5 --no-movie > $R/efork.log 2>&1
wait
echo ALLDONE
