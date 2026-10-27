#!/bin/bash
# c58 review of c51's Marangoni flames: m -0.15 seeds 4 5, m 0 twin seeds 4 5, m -0.15 at world dt/2 seed 4, m -0.6 seed 4; T=600
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=1
G=collective/contrib/20261027T0319-c51-marangoni-flames-negative; R=collective/contrib/20261027T1500-c58-review-marangoni-flames
WORLD_P='{"m":-0.15}' python -m labkit.run $G/world.py --out $R/pack_m15 --seeds 4 5 --frames 600 --spf 25 --no-movie > /dev/null 2>&1 &
WORLD_P='{"m":0}' python -m labkit.run $G/world.py --out $R/pack_m0 --seeds 4 5 --frames 600 --spf 25 --no-movie > /dev/null 2>&1 &
WORLD_P='{"m":-0.15,"dt":0.02}' python -m labkit.run $G/world.py --out $R/pack_m15_dthalf --seeds 4 --frames 600 --spf 50 --no-movie > /dev/null 2>&1 &
WORLD_P='{"m":-0.6}' python -m labkit.run $G/world.py --out $R/pack_m60 --seeds 4 --frames 600 --spf 25 --no-movie > /dev/null 2>&1 &
wait; echo ALLDONE
