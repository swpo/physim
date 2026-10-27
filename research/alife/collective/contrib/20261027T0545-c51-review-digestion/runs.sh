#!/bin/bash
# c51 review of c52 digestion ecology: seed 5 at 256^2 (claimed world and pred_on 0 twin, t=12000, default K); then the prey-removal fork (dfork_t 6000) and its fed run at 128^2, t=8000
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
W=collective/contrib/20261027T0325-c52-digestion-ecology-claim/world.py; R=collective/contrib/20261027T0545-c51-review-digestion
python -m labkit.run $W --out $R/pack256_s5 --seeds 5 --size 256 256 --frames 120 --no-movie > $R/pack.log 2>&1 &
WORLD_P='{"pred_on":0}' python -m labkit.run $W --out $R/twin256_s5 --seeds 5 --size 256 256 --frames 120 --no-movie > $R/twin.log 2>&1
wait
WORLD_P='{"dfork_t":6000}' python -m labkit.run $W --out $R/dfork128_s5 --seeds 5 --size 128 128 --frames 80 --no-movie > $R/dfork.log 2>&1 &
python -m labkit.run $W --out $R/fed128_s5 --seeds 5 --size 128 128 --frames 80 --no-movie > $R/fed.log 2>&1
wait; echo done > $R/done.txt
