#!/bin/bash
# c51 review controls: g=0 twin seed 7; dt/2 (world step) seed 9; 2x resolution (dx halved: 256^2 grid, diffusivities x4, hyper x16, L x2, g x2) seed 9
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
W=collective/contrib/20261027T0040-c49-reacting-thermals-claim/world.py; R=collective/contrib/20261027T0230-c51-review-thermals
WORLD_P='{"g":0}' python -m labkit.run $W --out $R/g0 --seeds 7 --frames 600 --spf 25 --no-movie > $R/g0.log 2>&1
WORLD_P='{"dt":0.02}' python -m labkit.run $W --out $R/dthalf --seeds 9 --frames 600 --spf 50 --dt 0.02 --no-movie > $R/dthalf.log 2>&1
WORLD_P='{"nu":1.2,"kT":0.4,"kY":8.0,"hyper":0.016,"L":8.0,"g":1.0}' python -m labkit.run $W --out $R/res2x --seeds 9 --size 256 256 --frames 600 --spf 25 --no-movie > $R/res2x.log 2>&1
echo CTRLDONE
