#!/bin/bash
# c51 review of c43 cips-consumer: fresh seed 7 (seeds 5 and 6 blow up at frame 1) rerun, consumer-free twin seed 5, E fork at t=3000 seed 5
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
W=collective/contrib/20261026T1700-c43-cips-consumer/world.py; R=collective/contrib/20261027T0153-c51-review-cips-consumer
python -m labkit.run $W --out $R/rerun --seeds 7 --frames 120 --lineage-k 5 --no-movie > $R/rerun.log 2>&1 &
WORLD_P='{"pred_on":0}' python -m labkit.run $W --out $R/twin_nocons --seeds 7 --frames 120 --lineage-k 5 --no-movie > $R/twin.log 2>&1
WORLD_P='{"tcut":3000}' python -m labkit.run $W --out $R/efork --seeds 7 --frames 80 --lineage-k 5 --no-movie > $R/efork.log 2>&1
wait; echo RUNSDONE > $R/done.txt
