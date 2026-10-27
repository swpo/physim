#!/bin/bash
# c51 review of c46 hunting ecology: fresh seed 13 at 256^2 with the predator-free twin, then the fuel fork at 128^2 (seed 13) with its fed twin
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
W=collective/contrib/20261026T2103-c46-hunting-ecology-claim/world.py; R=collective/contrib/20261027T0217-c51-review-hunting
python -m labkit.run $W --out $R/pack256 --seeds 13 --size 256 256 --frames 120 --lineage-k 5 --no-movie > $R/pack256.log 2>&1 &
WORLD_P='{"pred_on":0}' python -m labkit.run $W --out $R/twin256 --seeds 13 --size 256 256 --frames 120 --lineage-k 5 --no-movie > $R/twin256.log 2>&1
WORLD_P='{"fork_t":6000}' python -m labkit.run $W --out $R/efork128 --seeds 13 --frames 80 --lineage-k 5 --no-movie > $R/efork.log 2>&1
python -m labkit.run $W --out $R/fed128 --seeds 13 --frames 80 --lineage-k 5 --no-movie > $R/fed.log 2>&1
wait; echo done > $R/done.txt
