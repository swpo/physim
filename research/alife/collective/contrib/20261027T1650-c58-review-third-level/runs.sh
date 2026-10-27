#!/bin/bash
# c58 review of c52's third level: world3.py defaults (nb3 2, kd3 400, mc -0.9) on fresh seed 5, and top_on 0 (two-level twin), T=10000
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
G=collective/contrib/20261027T0407-c52-third-level-negative; R=collective/contrib/20261027T1650-c58-review-third-level
python -m labkit.run $G/world3.py --out $R/w3 --seeds 5 --size 128 128 --frames 100 --no-movie > $R/w3.log 2>&1 &
WORLD_P='{"top_on":0}' python -m labkit.run $G/world3.py --out $R/w2 --seeds 5 --size 128 128 --frames 100 --no-movie > $R/w2.log 2>&1 &
wait; echo ALLDONE
