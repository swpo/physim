#!/bin/bash
# chirality scan of the eating Toner-Tu flocks (world.py = parent world + chiral rotation chi of p); seed 0, t=3000
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2; G=collective/contrib/20261027T0216-c51-chiral-flocks-negative
for c in 0.06 0.08 0.1 0.2; do WORLD_P="{\"chi\":$c}" python -m labkit.run $G/world.py --out $G/chi_$c --seeds 0 --frames 300 --spf 40 --no-movie; done
WORLD_P='{"chi":0.03}' python -m labkit.run $G/world.py --out $G/chi03_f10 --seeds 0 --frames 300 --spf 40 --threshold 0.45 --no-movie
WORLD_P='{"chi":0.03}' python -m labkit.run $G/world.py --out $G/chi03 --seeds 0 1 --frames 150 --spf 80 --no-movie
