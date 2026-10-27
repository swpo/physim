#!/bin/bash
# c58 review re-runs of c51's chiral eating flocks on fresh seed 7 (and 8 for chi 0.03): chi 0.03 (labkit threshold 0.45 as c51), chi 0.03 at world dt/2, chi 0.06, chi 0.1
cd /home/user/physim/research/alife; export PATH=$PWD/.labenv/bin:$PATH OMP_NUM_THREADS=1
G=collective/contrib/20261027T0216-c51-chiral-flocks-negative; R=collective/contrib/20261027T1450-c58-review-chiral-flocks
WORLD_P='{"chi":0.03}' python -m labkit.run $G/world.py --out $R/chi03_s7 --seeds 7 8 --frames 300 --spf 40 --threshold 0.45 --no-movie > $R/l1.log 2>&1 &
WORLD_P='{"chi":0.03,"dt":0.125}' python -m labkit.run $G/world.py --out $R/chi03_dthalf_s7 --seeds 7 --frames 300 --spf 80 --threshold 0.45 --no-movie > $R/l2.log 2>&1 &
wait
WORLD_P='{"chi":0.06}' python -m labkit.run $G/world.py --out $R/chi06_s7 --seeds 7 --frames 300 --spf 40 --no-movie > $R/l3.log 2>&1 &
WORLD_P='{"chi":0.1}' python -m labkit.run $G/world.py --out $R/chi10_s7 --seeds 7 --frames 300 --spf 40 --no-movie > $R/l4.log 2>&1 &
wait; echo ALLDONE
