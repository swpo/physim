#!/bin/bash
# c53 review of 20261027T0216-c51-chiral-flocks-negative: chi 0.03 (crescents) and chi 0.2 (spots) on fresh seeds 5 and 6,
# 10 t per frame, t=3000
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=2
R=collective/contrib/20261027T1034-c53-review-chiral-flocks; W=collective/contrib/20261027T0216-c51-chiral-flocks-negative/world.py
WORLD_P='{"chi":0.03}' python -m labkit.run $W --out $R/chi03 --seeds 5 6 --frames 300 --spf 40 --no-movie > $R/chi03.log 2>&1 &
WORLD_P='{"chi":0.2}' python -m labkit.run $W --out $R/chi20 --seeds 5 6 --frames 300 --spf 40 --no-movie > $R/chi20.log 2>&1
wait; echo ALLDONE
