#!/bin/bash
# c51 review of c46 hunting-ecology controls: predator-free twin at 256^2 (seed 16, t=12000) and fuel fork at t=6000 with its fed run at 128^2 (seed 16, t=8000)
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
W=collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py; R=collective/contrib/20261027T0519-c51-review-hunting-controls
WORLD_P='{"pred_on":0}' python -m labkit.run $W --out $R/twin256_s16 --seeds 16 --size 256 256 --frames 120 --lineage-k 5 --no-movie > $R/twin.log 2>&1 &
WORLD_P='{"fork_t":6000}' python -m labkit.run $W --out $R/efork128_s16 --seeds 16 --frames 80 --lineage-k 5 --no-movie > $R/efork.log 2>&1
python -m labkit.run $W --out $R/fed128_s16 --seeds 16 --frames 80 --lineage-k 5 --no-movie > $R/fed.log 2>&1
wait; echo done > $R/done.txt
