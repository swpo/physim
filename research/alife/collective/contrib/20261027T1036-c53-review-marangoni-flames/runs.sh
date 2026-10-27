#!/bin/bash
# c53 review of 20261027T0319-c51-marangoni-flames-negative: m -0.15 and the m 0 twin on fresh seeds 32 and 33 (seeds where the
# thermals' initial burn leaves survivors), and the collapsing m -1 arm on seed 32; T=600
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
R=collective/contrib/20261027T1036-c53-review-marangoni-flames; W=collective/contrib/20261027T0319-c51-marangoni-flames-negative/world.py
WORLD_P='{"m":-0.15}' python -m labkit.run $W --out $R/pack_m15 --seeds 32 33 --frames 600 --spf 25 --no-movie > $R/m15.log 2>&1 &
WORLD_P='{"m":0}' python -m labkit.run $W --out $R/pack_m0 --seeds 32 33 --frames 600 --spf 25 --no-movie > $R/m0.log 2>&1
wait
WORLD_P='{"m":-1}' python -m labkit.run $W --out $R/pack_m100 --seeds 32 --frames 600 --spf 25 --no-movie > $R/m100.log 2>&1
echo ALLDONE
