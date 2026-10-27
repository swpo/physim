#!/bin/bash
# c58 review of c51's Toner-Tu eaters: motile (v0 0.25) seeds 5 6, v0=0 twin seed 5, motile at world dt/2 seed 5; T=3000
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=1
W=collective/contrib/20261027T0210-c51-toner-tu-eaters-fronts/world.py; R=collective/contrib/20261027T1457-c58-review-toner-tu
python -m labkit.run $W --out $R/pack --seeds 5 6 --frames 150 --spf 80 --no-movie > /dev/null 2>&1 &
WORLD_P='{"v0":0}' python -m labkit.run $W --out $R/pack_v0 --seeds 5 --frames 150 --spf 80 --no-movie > /dev/null 2>&1 &
WORLD_P='{"dt":0.125}' python -m labkit.run $W --out $R/pack_dthalf --seeds 5 --frames 150 --spf 160 --no-movie > /dev/null 2>&1 &
wait; echo ALLDONE
