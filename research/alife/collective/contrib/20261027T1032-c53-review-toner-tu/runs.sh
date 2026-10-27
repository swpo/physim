#!/bin/bash
# c53 review of 20261027T0210-c51-toner-tu-eaters-fronts: motile (v0 0.25, defaults) and the v0=0 twin on fresh seeds 5 and 6,
# plus the motile world at half the world step (dt 0.125, 160 steps per frame) on seed 5
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
R=collective/contrib/20261027T1032-c53-review-toner-tu; W=collective/contrib/20261027T0210-c51-toner-tu-eaters-fronts/world.py
python -m labkit.run $W --out $R/pack --seeds 5 6 --frames 150 --spf 80 --no-movie > $R/pack.log 2>&1 &
WORLD_P='{"v0":0}' python -m labkit.run $W --out $R/pack_v0 --seeds 5 6 --frames 150 --spf 80 --no-movie > $R/pack_v0.log 2>&1
wait
WORLD_P='{"dt":0.125}' python -m labkit.run $W --out $R/pack_dthalf --seeds 5 --frames 150 --spf 160 --dt 0.125 --no-movie > $R/pack_dthalf.log 2>&1
echo ALLDONE
