#!/bin/bash
# packs (world.py with defaults mt 1, my 0 is the heat-Marangoni world): m -0.15 and the m 0 twin, seeds 0 1, T=600
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2; G=collective/contrib/20261027T0319-c51-marangoni-flames-negative
WORLD_P='{"m":-0.15}' python -m labkit.run $G/world.py --out $G/pack_m15 --seeds 0 1 --frames 600 --spf 25 --no-movie
WORLD_P='{"m":0}' python -m labkit.run $G/world.py --out $G/pack_m0 --seeds 0 1 --frames 600 --spf 25 --no-movie
# screen images: python quick.py world.py 600 <png> with WORLD_P as listed in contribution.json
